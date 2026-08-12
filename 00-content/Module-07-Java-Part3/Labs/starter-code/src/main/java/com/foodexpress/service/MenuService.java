package com.foodexpress.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * FoodExpress MenuService - manages menu items and categories.
 *
 * BUGS TO FIX (2 bugs):
 * 1. Uses ArrayList where HashSet is needed — allows duplicate menu item names
 * 2. Wrong Map iteration — uses keySet() then get() instead of entrySet()
 */
public class MenuService {

    // BUG #1: ArrayList allows duplicates — should use HashSet
    private List<String> menuItemNames = new ArrayList<>();
    private Map<String, Double> itemPrices = new HashMap<>();

    public void addMenuItem(String name, double price) {
        // BUG #1: Duplicates are added because ArrayList allows them
        menuItemNames.add(name);
        itemPrices.put(name, price);
        System.out.println("Added: " + name + " ($" + price + ")");
    }

    /**
     * Prints all menu items with prices.
     * BUG #2: Inefficient Map iteration — uses keySet() + get() instead of entrySet()
     */
    public void printMenu() {
        System.out.println("=== FoodExpress Menu ===");

        // BUG #2: Inefficient — iterates keys, then does a separate get() for each
        // Should use entrySet() for direct access to key-value pairs
        for (String key : itemPrices.keySet()) {
            Double price = itemPrices.get(key);  // Extra lookup for each key
            System.out.println("  " + key + ": $" + price);
        }
    }

    /**
     * Returns the number of unique menu items.
     * Due to BUG #1, this count includes duplicates.
     */
    public int getMenuItemCount() {
        return menuItemNames.size();  // Inflated by duplicates!
    }

    public List<String> getMenuItemNames() {
        return menuItemNames;
    }

    public Map<String, Double> getItemPrices() {
        return itemPrices;
    }
}
