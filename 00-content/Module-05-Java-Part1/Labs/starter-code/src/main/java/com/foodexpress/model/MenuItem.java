package com.foodexpress.model;

/**
 * FoodExpress MenuItem - represents a food item on a restaurant menu.
 *
 * BUGS TO FIX (3 bugs):
 * 1. Fields are public — violates encapsulation (should be private with getters/setters)
 * 2. No validation in setter for price — negative prices allowed
 * 3. No validation in setter for name — null/empty names allowed
 */
public class MenuItem {

    // BUG #1: Fields are public — violates encapsulation
    public String name;
    public String description;
    public double price;
    public String category;

    public MenuItem(String name, String description, double price, String category) {
        // BUG #2: No validation — negative price is accepted
        this.name = name;
        this.description = description;
        this.price = price;
        this.category = category;
    }

    // BUG #3: No validation — null/empty name is accepted
    // (No getters/setters at all — direct field access)

    @Override
    public String toString() {
        return name + " ($" + price + ") - " + category;
    }
}
