package com.foodexpress;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * FoodExpress Restaurant Service
 * Business logic for restaurant operations.
 *
 * CONTAINS BUGS - Find and fix them!
 *
 * BUG 1: No circuit breaker on external call - if review service is down,
 *         this service will hang and eventually cascade failures
 * BUG 2: Synchronous call blocks thread - external API call blocks the
 *         request thread, reducing throughput under load
 */
@Service
public class RestaurantService {

    @Autowired
    private RestTemplate restTemplate;

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
     * BUG 1: No circuit breaker!
     * If the review-service is down or slow, this method will:
     * - Block for the full connection timeout (default: 30 seconds)
     * - Cause cascading failures as threads pile up
     * - Eventually bring down the restaurant-service too
     *
     * BUG 2: Synchronous blocking call!
     * RestTemplate.getForObject() blocks the current thread.
     * Under load, all threads could be waiting for the review service,
     * leaving no threads to handle other requests.
     */
    public RestaurantWithReviews getRestaurantWithReviews(Long restaurantId) {
        Restaurant restaurant = getRestaurantById(restaurantId);
        if (restaurant == null) {
            return null;
        }

        // BUG 1 & 2: Synchronous call with no circuit breaker, no timeout,
        // no fallback. If review-service is down, this hangs.
        ReviewResponse[] reviews = restTemplate.getForObject(
            "http://review-service:8082/api/reviews/restaurant/" + restaurantId,
            ReviewResponse[].class
        );

        return new RestaurantWithReviews(restaurant, Arrays.asList(reviews));
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
