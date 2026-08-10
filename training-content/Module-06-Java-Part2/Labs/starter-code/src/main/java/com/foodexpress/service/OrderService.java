package com.foodexpress.service;

import com.foodexpress.exception.OrderNotFoundException;
import com.foodexpress.model.MenuItem;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * FoodExpress OrderService - processes orders and loads menu data.
 *
 * BUGS TO FIX (2 bugs):
 * 1. Empty catch block swallows IOException — errors are silently ignored
 * 2. Catch blocks in wrong order — Exception before IOException (unreachable catch)
 */
public class OrderService {

    private List<MenuItem> menu = new ArrayList<>();

    /**
     * Loads menu items from a file path.
     * Contains exception handling bugs.
     */
    public void loadMenu(String filePath) {
        try {
            // Simulate file operations that may throw exceptions
            if (filePath == null) {
                throw new FileNotFoundException("File path is null");
            }
            if (filePath.endsWith(".bad")) {
                throw new IOException("Corrupt file: " + filePath);
            }
            System.out.println("Menu loaded from: " + filePath);

        // BUG #2: Exception (parent) caught before IOException (child) — unreachable catch
        } catch (Exception e) {
            // BUG #1: Empty catch block — exception silently swallowed
        } catch (IOException e) {
            System.err.println("IO error: " + e.getMessage());
        }
    }

    /**
     * Finds an order by ID. Throws custom exception if not found.
     */
    public String findOrder(String orderId) throws OrderNotFoundException {
        // Simulated lookup — only "ORD-001" exists
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
