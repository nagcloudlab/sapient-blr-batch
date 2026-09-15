package com.example.payment;

import java.time.Instant;
import java.util.UUID;

public class Payment {
    private String id;
    private String orderId;
    private double amount;
    private String status;
    private String createdAt;

    public Payment() {}

    public Payment(String orderId, double amount) {
        this.id = UUID.randomUUID().toString();
        this.orderId = orderId;
        this.amount = amount;
        this.status = "COMPLETED";
        this.createdAt = Instant.now().toString();
    }

    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }
    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getCreatedAt() { return createdAt; }
    public void setCreatedAt(String createdAt) { this.createdAt = createdAt; }
}
