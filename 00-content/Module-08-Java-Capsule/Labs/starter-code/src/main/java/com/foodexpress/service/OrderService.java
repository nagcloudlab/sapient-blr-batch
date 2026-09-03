package com.foodexpress.service;

import com.foodexpress.repository.OrderRepository;

import java.util.List;
import java.util.Map;

/**
 * FoodExpress OrderService - business logic layer.
 *
 * BUGS TO FIX (2 bugs / Ticket #2):
 * 1. listOrders() ignores pagination — returns ALL orders regardless of page/size
 * 2. calculateTotal() doesn't apply bulk discount for quantity > 10
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
     *
     * BUG #1: Pagination parameters (page, size) are completely ignored.
     * Returns ALL orders from the repository — causes performance issues
     * when the orders table has millions of rows.
     */
    public List<Map<String, Object>> listOrders(int page, int size) {
        // BUG #1: Ignores page and size — returns everything
        return orderRepository.findAll();
    }

    /**
     * Calculates total for an order, applying business rules.
     *
     * BUG #2: Missing bulk discount logic.
     * Business rule: If any item has quantity > 10, apply 10% discount on that item.
     * This method just sums up (price * qty) without checking for bulk discount.
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

            // BUG #2: No bulk discount applied for qty > 10
            // Should apply 10% discount when quantity exceeds 10
            total += price * qty;
        }
        return total;
    }
}
