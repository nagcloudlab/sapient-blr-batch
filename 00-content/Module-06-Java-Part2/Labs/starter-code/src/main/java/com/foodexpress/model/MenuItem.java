package com.foodexpress.model;

/**
 * FoodExpress MenuItem - implements Priceable interface.
 *
 * BUGS TO FIX (2 bugs):
 * 1. Missing @Override annotation on getPrice()
 * 2. getDiscountedPrice() is declared in Priceable but NOT implemented here
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

    // BUG #1: Missing @Override annotation
    public double getPrice() {
        return price;
    }

    // BUG #2: getDiscountedPrice() is NOT implemented — compile error!
    // The Priceable interface requires this method, but it's missing.

    public String getName() { return name; }
    public String getDescription() { return description; }
    public String getCategory() { return category; }

    @Override
    public String toString() {
        return name + " ($" + price + ") - " + category;
    }
}
