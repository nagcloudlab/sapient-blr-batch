package com.foodexpress.model;

import java.util.ArrayList;
import java.util.List;

/**
 * FoodExpress Restaurant - represents a partner restaurant.
 * FIXED: constructor validates parameters, static counter incremented.
 */
public class Restaurant {

    private String name;
    private String address;
    private double rating;
    private List<MenuItem> menu;

    private static int restaurantCount = 0;

    // FIX #1: Constructor validates name (not null) and rating (0-5 range)
    public Restaurant(String name, String address, double rating) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Restaurant name cannot be null or empty");
        }
        if (rating < 0 || rating > 5) {
            throw new IllegalArgumentException("Rating must be between 0 and 5: " + rating);
        }
        this.name = name;
        this.address = address;
        this.rating = rating;
        this.menu = new ArrayList<>();
        // FIX #2: Increment static counter
        restaurantCount++;
    }

    public void addMenuItem(MenuItem item) {
        menu.add(item);
    }

    public List<MenuItem> getMenu() {
        return menu;
    }

    public static int getRestaurantCount() {
        return restaurantCount;
    }

    public String getName() { return name; }
    public String getAddress() { return address; }
    public double getRating() { return rating; }

    @Override
    public String toString() {
        return name + " (" + rating + " stars) - " + address + " [" + menu.size() + " items]";
    }
}
