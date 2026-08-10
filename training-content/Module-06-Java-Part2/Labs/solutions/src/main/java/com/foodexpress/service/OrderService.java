package com.foodexpress.service;

import com.foodexpress.exception.OrderNotFoundException;
import com.foodexpress.model.MenuItem;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * FoodExpress OrderService - processes orders and loads menu data.
 * FIXED: catch blocks in correct order, exceptions properly logged.
 */
public class OrderService {

    private List<MenuItem> menu = new ArrayList<>();

    /**
     * Loads menu items from a file path.
     * Fixed exception handling.
     */
    public void loadMenu(String filePath) {
        try {
            if (filePath == null) {
                throw new FileNotFoundException("File path is null");
            }
            if (filePath.endsWith(".bad")) {
                throw new IOException("Corrupt file: " + filePath);
            }
            System.out.println("Menu loaded from: " + filePath);

        // FIX #2: IOException (child) caught BEFORE Exception (parent)
        } catch (FileNotFoundException e) {
            System.err.println("File not found: " + e.getMessage());
        } catch (IOException e) {
            // FIX #1: Exception is logged, not silently swallowed
            System.err.println("IO error loading menu: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Unexpected error: " + e.getMessage());
        }
    }

    /**
     * Finds an order by ID. Throws custom exception if not found.
     */
    public String findOrder(String orderId) throws OrderNotFoundException {
        if ("ORD-001".equals(orderId)) {
            return "Order ORD-001: 2x Classic Burger, 1x Fries";
        }
        throw new OrderNotFoundException(orderId);
    }

    public void addMenuItem(MenuItem item) {
        menu.add(item);
    }

    public List<MenuItem> getMenu() {
        return menu;
    }
}
