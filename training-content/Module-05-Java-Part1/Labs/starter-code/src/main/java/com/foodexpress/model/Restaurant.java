package com.foodexpress.model;

import java.util.ArrayList;
import java.util.List;

/**
 * FoodExpress Restaurant - represents a partner restaurant.
 *
 * BUGS TO FIX (2 bugs):
 * 1. Constructor doesn't validate parameters (null name, negative rating)
 * 2. Missing static counter for total restaurants created (restaurantCount never incremented)
 */
public class Restaurant {

    private String name;
    private String address;
    private double rating;
    private List<MenuItem> menu;

    // BUG #2: Static counter declared but never incremented in constructor
    private static int restaurantCount = 0;

    // BUG #1: No validation — null name and negative rating accepted
    public Restaurant(String name, String address, double rating) {
        this.name = name;
        this.address = address;
        this.rating = rating;
        this.menu = new ArrayList<>();
        // Missing: restaurantCount++;
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
