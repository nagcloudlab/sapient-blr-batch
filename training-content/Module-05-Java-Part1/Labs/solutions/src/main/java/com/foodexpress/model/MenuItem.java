package com.foodexpress.model;

/**
 * FoodExpress MenuItem - represents a food item on a restaurant menu.
 * FIXED: proper encapsulation with private fields, getters/setters, and validation.
 */
public class MenuItem {

    // FIX #1: Fields are private (encapsulation)
    private String name;
    private String description;
    private double price;
    private String category;

    public MenuItem(String name, String description, double price, String category) {
        setName(name);           // Use setters for validation
        this.description = description;
        setPrice(price);         // Use setter for validation
        this.category = category;
    }

    // FIX #3: Setter validates name — rejects null/empty
    public void setName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Menu item name cannot be null or empty");
        }
        this.name = name;
    }

    // FIX #2: Setter validates price — rejects negative values
    public void setPrice(double price) {
        if (price < 0) {
            throw new IllegalArgumentException("Price cannot be negative: " + price);
        }
        this.price = price;
    }

    public String getName() { return name; }
    public String getDescription() { return description; }
    public double getPrice() { return price; }
    public String getCategory() { return category; }

    public void setDescription(String description) { this.description = description; }
    public void setCategory(String category) { this.category = category; }

    @Override
    public String toString() {
        return name + " ($" + price + ") - " + category;
    }
}
