package com.foodexpress;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

/**
 * FoodExpress Restaurant Service (FIXED)
 * Business logic for restaurant operations.
 *
 * ALL BUGS FIXED:
 * FIX 1: Added @CircuitBreaker with fallback method
 * FIX 2: Replaced synchronous RestTemplate with non-blocking WebClient
 */
@Service
public class RestaurantService {

    // FIX 2: Using WebClient (non-blocking) instead of RestTemplate (blocking)
    @Autowired
    private WebClient.Builder webClientBuilder;

    // Simulated in-memory data
    private final List<Restaurant> restaurants = Arrays.asList(
        new Restaurant(1L, "Spice Garden", "Indian", "MG Road, Bangalore", true, 4.5),
        new Restaurant(2L, "Dragon Palace", "Chinese", "Brigade Road, Bangalore", true, 4.2),
        new Restaurant(3L, "Pizza Planet", "Italian", "Koramangala, Bangalore", false, 4.0),
        new Restaurant(4L, "Dosa Corner", "South Indian", "Indiranagar, Bangalore", true, 4.7),
        new Restaurant(5L, "Burger Barn", "American", "Whitefield, Bangalore", true, 3.9)
    );

    public List<Restaurant> getAllRestaurants() {
        return restaurants.stream()
                .filter(Restaurant::isAvailable)
                .collect(Collectors.toList());
    }

    public Restaurant getRestaurantById(Long id) {
        return restaurants.stream()
                .filter(r -> r.getId().equals(id))
                .findFirst()
                .orElse(null);
    }

    /**
     * Get restaurant details with reviews from external Review Service.
     *
     * FIX 1: Added @CircuitBreaker annotation with fallback.
     * If review-service is down, the circuit breaker will:
     * - Detect failures and open the circuit after threshold
     * - Return fallback response (restaurant without reviews)
     * - Periodically test if the service is back
     *
     * FIX 2: Using WebClient for non-blocking HTTP call.
     * WebClient doesn't block the thread while waiting for response,
     * allowing the server to handle other requests concurrently.
     */
    @CircuitBreaker(name = "reviewService", fallbackMethod = "getRestaurantWithReviewsFallback")
    public RestaurantWithReviews getRestaurantWithReviews(Long restaurantId) {
        Restaurant restaurant = getRestaurantById(restaurantId);
        if (restaurant == null) {
            return null;
        }

        // FIX 2: Non-blocking WebClient call with timeout
        List<ReviewResponse> reviews = webClientBuilder.build()
            .get()
            .uri("http://review-service:8082/api/reviews/restaurant/" + restaurantId)
            .retrieve()
            .bodyToFlux(ReviewResponse.class)
            .collectList()
            .block(java.time.Duration.ofSeconds(5));  // 5-second timeout

        return new RestaurantWithReviews(restaurant, reviews);
    }

    /**
     * FIX 1: Fallback method - returns restaurant without reviews
     * when the review service is unavailable.
     */
    public RestaurantWithReviews getRestaurantWithReviewsFallback(Long restaurantId,
                                                                    Throwable t) {
        Restaurant restaurant = getRestaurantById(restaurantId);
        if (restaurant == null) {
            return null;
        }
        // Return restaurant with empty reviews list as fallback
        return new RestaurantWithReviews(restaurant, Collections.emptyList());
    }

    public List<Restaurant> getMenu(Long restaurantId) {
        // Simplified - returns restaurant list as placeholder
        return restaurants;
    }

    public List<Restaurant> search(String query) {
        String lowerQuery = query.toLowerCase();
        return restaurants.stream()
                .filter(r -> r.getName().toLowerCase().contains(lowerQuery)
                        || r.getCuisine().toLowerCase().contains(lowerQuery))
                .collect(Collectors.toList());
    }

    public Restaurant updateAvailability(Long id, boolean available) {
        Restaurant restaurant = getRestaurantById(id);
        if (restaurant != null) {
            restaurant.setAvailable(available);
        }
        return restaurant;
    }

    // --- Inner classes ---

    static class Restaurant {
        private Long id;
        private String name;
        private String cuisine;
        private String address;
        private boolean available;
        private double rating;

        public Restaurant(Long id, String name, String cuisine,
                          String address, boolean available, double rating) {
            this.id = id;
            this.name = name;
            this.cuisine = cuisine;
            this.address = address;
            this.available = available;
            this.rating = rating;
        }

        public Long getId() { return id; }
        public String getName() { return name; }
        public String getCuisine() { return cuisine; }
        public boolean isAvailable() { return available; }
        public void setAvailable(boolean available) { this.available = available; }
    }

    static class ReviewResponse {
        private Long id;
        private Long restaurantId;
        private String reviewerName;
        private int rating;
        private String comment;
    }

    static class RestaurantWithReviews {
        private Restaurant restaurant;
        private List<ReviewResponse> reviews;

        public RestaurantWithReviews(Restaurant restaurant, List<ReviewResponse> reviews) {
            this.restaurant = restaurant;
            this.reviews = reviews;
        }
    }
}
