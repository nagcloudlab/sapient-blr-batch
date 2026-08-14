package com.foodexpress.exception;

/**
 * Custom exception for FoodExpress — thrown when an order ID is not found.
 * This file is correct — no changes needed.
 */
public class OrderNotFoundException extends Exception {

    private final String orderId;

    public OrderNotFoundException(String orderId) {
        super("Order not found: " + orderId);
        this.orderId = orderId;
    }

    public String getOrderId() {
        return orderId;
    }
}
