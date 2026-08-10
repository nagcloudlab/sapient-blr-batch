package com.foodexpress.repository;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * FoodExpress OrderRepository - in-memory data store (simulates database).
 *
 * BUG TO FIX (1 bug / Ticket #3):
 * 1. findByCustomer() uses == instead of .equals() for String comparison
 */
public class OrderRepository {

    private final List<Map<String, Object>> orders = new ArrayList<>();

    public OrderRepository() {
        // Seed sample data
        Map<String, Object> order1 = new HashMap<>();
        order1.put("id", "ORD-001");
        order1.put("customer", "Alice Johnson");
        order1.put("items", List.of(
                Map.of("name", "Classic Burger", "price", 12.99, "quantity", 2),
                Map.of("name", "Fries", "price", 4.99, "quantity", 1)
        ));
        orders.add(order1);

        Map<String, Object> order2 = new HashMap<>();
        order2.put("id", "ORD-002");
        order2.put("customer", "Bob Smith");
        order2.put("items", List.of(
                Map.of("name", "Pizza Margherita", "price", 15.99, "quantity", 12),
                Map.of("name", "Garlic Bread", "price", 5.49, "quantity", 3)
        ));
        orders.add(order2);
    }

    public Map<String, Object> findById(String orderId) {
        for (Map<String, Object> order : orders) {
            if (orderId.equals(order.get("id"))) {
                return order;
            }
        }
        return null;
    }

    /**
     * BUG #1: Uses == for String comparison instead of .equals()
     * This will fail when customerName is created at runtime (e.g., from user input).
     */
    public List<Map<String, Object>> findByCustomer(String customerName) {
        List<Map<String, Object>> results = new ArrayList<>();
        for (Map<String, Object> order : orders) {
            // BUG #1: == compares references, not values — fails for runtime strings
            if (order.get("customer") == customerName) {
                results.add(order);
            }
        }
        return results;
    }

    public List<Map<String, Object>> findAll() {
        return new ArrayList<>(orders);
    }

    /**
     * Returns a paginated subset of orders.
     */
    public List<Map<String, Object>> findAll(int page, int size) {
        int start = page * size;
        int end = Math.min(start + size, orders.size());
        if (start >= orders.size()) {
            return new ArrayList<>();
        }
        return new ArrayList<>(orders.subList(start, end));
    }
}
