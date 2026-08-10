package com.foodexpress.controller;

import com.foodexpress.service.OrderService;

import java.util.Map;

/**
 * FoodExpress OrderController - handles HTTP-like request routing.
 * (Simulated controller — no Spring dependency needed for this exercise.)
 *
 * BUG TO FIX (1 bug / Ticket #1):
 * 1. GET /orders/{id} returns 500 when order not found — should return 404
 *    (missing null check on service result)
 */
public class OrderController {

    private final OrderService orderService;

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    /**
     * Simulates GET /orders/{id}
     * Returns a response map with "status" and "body" keys.
     *
     * BUG #1: No null check — when order is not found, calling .toString()
     * on null result causes NullPointerException (HTTP 500 in production).
     * Should return 404 status instead.
     */
    public Map<String, Object> getOrder(String orderId) {
        // BUG #1: No null check — if findById returns null, .toString() throws NPE
        Map<String, Object> order = orderService.findById(orderId);
        String orderDetails = order.toString();  // NPE if order is null!

        return Map.of(
                "status", 200,
                "body", orderDetails
        );
    }

    /**
     * Simulates GET /orders?page=1&size=10
     * Returns all orders (delegates to service).
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
