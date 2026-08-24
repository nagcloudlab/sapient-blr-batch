package com.foodexpress;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * FoodExpress Restaurant Controller (FIXED)
 * Handles REST API endpoints for restaurant operations.
 *
 * ALL BUGS FIXED:
 * FIX 1: Added @RestController annotation
 * FIX 2: Corrected @RequestMapping path to /api/restaurants
 */

// FIX 1: Added @RestController annotation
// This tells Spring Boot to register this class as a REST controller
// and automatically serialize return values to JSON
@RestController
// FIX 2: Corrected path to include /api prefix
@RequestMapping("/api/restaurants")
public class RestaurantController {

    @Autowired
    private RestaurantService restaurantService;

    /**
     * Get all restaurants
     * GET /api/restaurants
     */
    @GetMapping
    public ResponseEntity<List<Restaurant>> getAllRestaurants() {
        List<Restaurant> restaurants = restaurantService.getAllRestaurants();
        return ResponseEntity.ok(restaurants);
    }

    /**
     * Get restaurant by ID
     * GET /api/restaurants/{id}
     */
    @GetMapping("/{id}")
    public ResponseEntity<Restaurant> getRestaurantById(@PathVariable Long id) {
        Restaurant restaurant = restaurantService.getRestaurantById(id);
        if (restaurant == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(restaurant);
    }

    /**
     * Get restaurant menu
     * GET /api/restaurants/{id}/menu
     */
    @GetMapping("/{id}/menu")
    public ResponseEntity<List<MenuItem>> getMenu(@PathVariable Long id) {
        List<MenuItem> menu = restaurantService.getMenu(id);
        return ResponseEntity.ok(menu);
    }

    /**
     * Search restaurants by cuisine or name
     * GET /api/restaurants/search?q=Indian
     */
    @GetMapping("/search")
    public ResponseEntity<List<Restaurant>> searchRestaurants(
            @RequestParam String q) {
        List<Restaurant> results = restaurantService.search(q);
        return ResponseEntity.ok(results);
    }

    /**
     * Update restaurant availability
     * PUT /api/restaurants/{id}/availability
     */
    @PutMapping("/{id}/availability")
    public ResponseEntity<Restaurant> updateAvailability(
            @PathVariable Long id,
            @RequestBody AvailabilityRequest request) {
        Restaurant updated = restaurantService.updateAvailability(id, request.isAvailable());
        return ResponseEntity.ok(updated);
    }

    // --- Inner classes for request/response models ---

    static class Restaurant {
        private Long id;
        private String name;
        private String cuisine;
        private String address;
        private boolean available;
        private double rating;

        public Long getId() { return id; }
        public String getName() { return name; }
    }

    static class MenuItem {
        private Long id;
        private String name;
        private double price;
        private String category;
        private boolean available;
    }

    static class AvailabilityRequest {
        private boolean available;
        public boolean isAvailable() { return available; }
    }
}
