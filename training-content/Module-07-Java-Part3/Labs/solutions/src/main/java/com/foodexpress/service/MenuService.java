package com.foodexpress.service;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * FoodExpress MenuService - manages menu items and categories.
 * FIXED: Uses HashSet to prevent duplicates, entrySet() for efficient Map iteration.
 */
public class MenuService {

    // FIX #1: HashSet prevents duplicate menu item names
    private Set<String> menuItemNames = new HashSet<>();
    private Map<String, Double> itemPrices = new HashMap<>();

    public void addMenuItem(String name, double price) {
        // FIX #1: HashSet automatically rejects duplicates
        boolean added = menuItemNames.add(name);
        itemPrices.put(name, price);
        if (added) {
            System.out.println("Added: " + name + " ($" + price + ")");
        } else {
            System.out.println("Updated price for: " + name + " ($" + price + ")");
        }
    }

    /**
     * Prints all menu items with prices.
     * FIX #2: Uses entrySet() for efficient Map iteration.
     */
    public void printMenu() {
        System.out.println("=== FoodExpress Menu ===");

        // FIX #2: entrySet() gives direct access to key-value pairs — no extra get()
        for (Map.Entry<String, Double> entry : itemPrices.entrySet()) {
            System.out.println("  " + entry.getKey() + ": $" + entry.getValue());
        }
    }

    /**
     * Returns the number of unique menu items.
     * FIX #1: HashSet size is always the unique count.
     */
    public int getMenuItemCount() {
        return menuItemNames.size();  // Accurate — no duplicates
    }

    public Set<String> getMenuItemNames() {
        return menuItemNames;
    }

    public Map<String, Double> getItemPrices() {
        return itemPrices;
    }
}
