package com.foodexpress.service;

import com.foodexpress.repository.OrderRepository;

import java.util.List;
import java.util.Map;

/**
 * FoodExpress OrderService - business logic layer.
 * FIXED: Pagination implemented, bulk discount applied for qty > 10.
 */
public class OrderService {

    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    /**
     * Finds an order by ID. May return null if not found.
     */
    public Map<String, Object> findById(String orderId) {
        return orderRepository.findById(orderId);
    }

    /**
     * Lists orders with pagination.
     * FIX #1: Now delegates to paginated findAll(page, size) in repository.
     */
    public List<Map<String, Object>> listOrders(int page, int size) {
        // FIX #1: Use paginated repository method
        return orderRepository.findAll(page, size);
    }

    /**
     * Calculates total for an order, applying business rules.
     * FIX #2: Applies 10% bulk discount for items with quantity > 10.
     */
    public double calculateTotal(String orderId) {
        Map<String, Object> order = orderRepository.findById(orderId);
        if (order == null) return 0.0;

        @SuppressWarnings("unchecked")
        List<Map<String, Object>> items = (List<Map<String, Object>>) order.get("items");

        double total = 0.0;
        for (Map<String, Object> item : items) {
            double price = (double) item.get("price");
            int qty = (int) item.get("quantity");
            double itemTotal = price * qty;

            // FIX #2: Apply 10% bulk discount when quantity exceeds 10
            if (qty > 10) {
                itemTotal *= 0.90;  // 10% discount
            }

            total += itemTotal;
        }
        return total;
    }
}
