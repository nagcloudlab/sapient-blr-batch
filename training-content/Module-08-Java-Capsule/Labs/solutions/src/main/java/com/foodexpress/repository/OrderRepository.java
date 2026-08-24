package com.foodexpress.repository;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * FoodExpress OrderRepository - in-memory data store (simulates database).
 * FIXED: Uses .equals() for String comparison in findByCustomer().
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
     * FIX #1: Uses .equals() for String comparison instead of ==
     */
    public List<Map<String, Object>> findByCustomer(String customerName) {
        List<Map<String, Object>> results = new ArrayList<>();
        for (Map<String, Object> order : orders) {
            // FIX #1: .equals() compares values, not references
            if (customerName.equals(order.get("customer"))) {
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
