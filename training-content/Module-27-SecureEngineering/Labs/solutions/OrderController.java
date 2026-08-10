package com.foodexpress.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import jakarta.validation.constraints.*;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderController {

    @Autowired
    private OrderRepository orderRepository;

    // FIX: Removed hardcoded password -- use environment variable or secrets manager
    // DB password is now configured via application.yml with ${DB_PASSWORD} reference

    /**
     * Get order by ID
     * FIX: Added authorization check -- user can only view their own orders
     */
    @GetMapping("/{orderId}")
    public ResponseEntity<Order> getOrder(@PathVariable Long orderId,
                                           Authentication auth) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new NotFoundException("Order not found"));

        // FIX: Authorization check -- verify order belongs to the authenticated user
        if (!order.getCustomerId().equals(auth.getUserId())) {
            throw new AccessDeniedException("You are not authorized to view this order");
        }

        return ResponseEntity.ok(order);
    }

    /**
     * Create a new order
     * FIX: Added input validation on critical fields
     */
    @PostMapping
    public ResponseEntity<Order> createOrder(@RequestBody @Valid OrderRequest orderRequest,
                                              Authentication auth) {
        // FIX: Validation is handled by @Valid annotation and OrderRequest constraints
        // totalAmount must be > 0, quantity must be 1-99

        Order order = new Order();
        order.setCustomerId(auth.getUserId());
        order.setRestaurantId(orderRequest.getRestaurantId());
        order.setTotalAmount(orderRequest.getTotalAmount());
        order.setStatus("PLACED");
        Order saved = orderRepository.save(order);

        return ResponseEntity.status(201).body(saved);
    }

    // FIX: Validation DTO with constraints
    public static class OrderRequest {
        @NotNull
        private Long restaurantId;

        @NotNull
        @DecimalMin(value = "0.01", message = "Total amount must be positive")
        @DecimalMax(value = "50000.00", message = "Total amount exceeds maximum")
        private Double totalAmount;

        @NotNull
        @Min(value = 1, message = "Quantity must be at least 1")
        @Max(value = 99, message = "Quantity cannot exceed 99")
        private Integer quantity;

        // Getters and setters
        public Long getRestaurantId() { return restaurantId; }
        public void setRestaurantId(Long restaurantId) { this.restaurantId = restaurantId; }
        public Double getTotalAmount() { return totalAmount; }
        public void setTotalAmount(Double totalAmount) { this.totalAmount = totalAmount; }
        public Integer getQuantity() { return quantity; }
        public void setQuantity(Integer quantity) { this.quantity = quantity; }
    }
}
