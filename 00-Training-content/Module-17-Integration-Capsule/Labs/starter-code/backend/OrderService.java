package com.foodexpress.order;

import java.util.List;
import java.util.ArrayList;
import java.util.Optional;

/**
 * FoodExpress Order Service
 * Handles order creation, pricing, and confirmation.
 *
 * CONTAINS BUGS - Find and fix them!
 */
public class OrderService {

    private final InventoryService inventoryService;
    private final NotificationService notificationService;

    public OrderService(InventoryService inventoryService,
                        NotificationService notificationService) {
        this.inventoryService = inventoryService;
        this.notificationService = notificationService;
    }

    /**
     * Creates a new order with discount applied.
     * BUG: Order confirmation shows the original price, not the discounted price.
     * The discountedTotal is calculated but never used in the confirmation.
     */
    public OrderConfirmation createOrder(Customer customer, List<OrderItem> items,
                                          String discountCode) {
        // Calculate original total
        double originalTotal = 0;
        for (OrderItem item : items) {
            originalTotal += item.getPrice() * item.getQuantity();
        }

        // Apply discount
        double discountPercent = getDiscountPercent(discountCode);
        double discountedTotal = originalTotal * (1 - discountPercent);

        // Create order record
        Order order = new Order();
        order.setCustomerId(customer.getId());
        order.setItems(items);
        order.setOriginalTotal(originalTotal);
        order.setDiscountedTotal(discountedTotal);
        order.setDiscountCode(discountCode);
        order.setStatus("CONFIRMED");

        // Save order (simulated)
        String orderId = "ORD-" + System.currentTimeMillis();
        order.setOrderId(orderId);

        // BUG: Confirmation uses originalTotal instead of discountedTotal
        // Customer sees the pre-discount price in their confirmation!
        OrderConfirmation confirmation = new OrderConfirmation(
            orderId,
            customer.getName(),
            items,
            originalTotal,  // BUG: Should be discountedTotal
            "Your order has been confirmed!"
        );

        // Send notification
        notificationService.sendOrderConfirmation(customer.getEmail(), confirmation);

        return confirmation;
    }

    /**
     * Returns discount percentage for a given code.
     */
    private double getDiscountPercent(String discountCode) {
        if (discountCode == null) return 0.0;
        switch (discountCode) {
            case "WELCOME10": return 0.10;
            case "FOOD20":    return 0.20;
            case "FIRST50":   return 0.50;
            default:          return 0.0;
        }
    }

    /**
     * Get order status by ID.
     */
    public String getOrderStatus(String orderId) {
        // Simulated lookup
        return "CONFIRMED";
    }

    // --- Inner classes for compilation context ---

    static class Order {
        private String orderId;
        private String customerId;
        private List<OrderItem> items;
        private double originalTotal;
        private double discountedTotal;
        private String discountCode;
        private String status;

        // Getters and setters
        public void setOrderId(String id) { this.orderId = id; }
        public void setCustomerId(String id) { this.customerId = id; }
        public void setItems(List<OrderItem> items) { this.items = items; }
        public void setOriginalTotal(double t) { this.originalTotal = t; }
        public void setDiscountedTotal(double t) { this.discountedTotal = t; }
        public void setDiscountCode(String c) { this.discountCode = c; }
        public void setStatus(String s) { this.status = s; }
    }

    static class OrderItem {
        private String name;
        private double price;
        private int quantity;

        public double getPrice() { return price; }
        public int getQuantity() { return quantity; }
    }

    static class Customer {
        private String id;
        private String name;
        private String email;

        public String getId() { return id; }
        public String getName() { return name; }
        public String getEmail() { return email; }
    }

    static class OrderConfirmation {
        private String orderId;
        private String customerName;
        private List<OrderItem> items;
        private double total;
        private String message;

        public OrderConfirmation(String orderId, String customerName,
                                  List<OrderItem> items, double total, String message) {
            this.orderId = orderId;
            this.customerName = customerName;
            this.items = items;
            this.total = total;
            this.message = message;
        }

        public double getTotal() { return total; }
    }

    interface InventoryService {
        boolean checkAvailability(String itemId, int quantity);
        void decrementStock(String itemId, int quantity);
    }

    interface NotificationService {
        void sendOrderConfirmation(String email, OrderConfirmation confirmation);
    }
}
