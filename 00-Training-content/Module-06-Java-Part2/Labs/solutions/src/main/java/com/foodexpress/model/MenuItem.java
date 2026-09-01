package com.foodexpress.model;

/**
 * FoodExpress MenuItem - implements Priceable interface.
 * FIXED: @Override annotation added, getDiscountedPrice() implemented.
 */
public class MenuItem implements Priceable {

    private String name;
    private String description;
    private double price;
    private String category;

    public MenuItem(String name, String description, double price, String category) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Name cannot be null or empty");
        }
        if (price < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
        this.name = name;
        this.description = description;
        this.price = price;
        this.category = category;
    }

    // FIX #1: Added @Override annotation
    @Override
    public double getPrice() {
        return price;
    }

    // FIX #2: Implemented getDiscountedPrice() as required by Priceable
    @Override
    public double getDiscountedPrice(double discountPercent) {
        if (discountPercent < 0 || discountPercent > 100) {
            throw new IllegalArgumentException("Discount must be between 0 and 100");
        }
        return price * (1 - discountPercent / 100.0);
    }

    public String getName() { return name; }
    public String getDescription() { return description; }
    public String getCategory() { return category; }

    @Override
    public String toString() {
        return name + " ($" + price + ") - " + category;
    }
}
