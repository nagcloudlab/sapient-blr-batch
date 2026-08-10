package com.foodexpress.controller;

import com.foodexpress.service.OrderService;

import java.util.Map;

/**
 * FoodExpress OrderController - handles HTTP-like request routing.
 * FIXED: Null check on findById result, returns 404 when order not found.
 */
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    /**
     * Simulates GET /orders/{id}
     * FIX #1: Checks for null and returns 404 status when order is not found.
     */
    public Map<String, Object> getOrder(String orderId) {
        // FIX #1: Null check — return 404 if order not found
        Map<String, Object> order = orderService.findById(orderId);
        if (order == null) {
            return Map.of(
                    "status", 404,
                    "body", "Order not found: " + orderId
            );
        }

        return Map.of(
                "status", 200,
                "body", order.toString()
        );
    }

    /**
     * Simulates GET /orders?page=1&size=10
     */
    public Map<String, Object> listOrders(int page, int size) {
        var orders = orderService.listOrders(page, size);
        return Map.of(
                "status", 200,
                "body", orders
        );
    }

    /**
     * Simulates GET /orders/{id}/total
     */
    public Map<String, Object> getOrderTotal(String orderId) {
        double total = orderService.calculateTotal(orderId);
        return Map.of(
                "status", 200,
                "body", "Total: $" + String.format("%.2f", total)
        );
    }
}
