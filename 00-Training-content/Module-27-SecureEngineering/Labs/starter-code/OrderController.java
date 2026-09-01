package com.foodexpress.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    @Autowired
    private OrderRepository orderRepository;

    // BUG: Hardcoded database password -- should be in environment variable
    private static final String DB_ADMIN_PASSWORD = "FoodExpress_Prod_2026!";

    /**
     * Get order by ID
     * BUG: Insecure Direct Object Reference (IDOR)
     * Any authenticated user can view any order by guessing the ID
     */
    @GetMapping("/{orderId}")
    public ResponseEntity<Order> getOrder(@PathVariable Long orderId,
                                           Authentication auth) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new NotFoundException("Order not found"));

        // BUG: No authorization check! Should verify order belongs to the user
        // Any logged-in user can access any order: /api/v1/orders/12345

        return ResponseEntity.ok(order);
    }

    /**
     * Create a new order
     * BUG: No input validation on critical fields
     */
    @PostMapping
    public ResponseEntity<Order> createOrder(@RequestBody Order order,
                                              Authentication auth) {
        // BUG: No validation on totalAmount -- could be negative (free food!)
        // BUG: No validation on quantity -- could be 0 or 999999
        // Should validate: totalAmount > 0, quantity between 1 and 99

        order.setCustomerId(auth.getUserId());
        order.setStatus("PLACED");
        Order saved = orderRepository.save(order);

        return ResponseEntity.status(201).body(saved);
    }
}
