package com.npci.upi.model;

public class UpiPaymentRequest {
    private String payerVpa;      // e.g., user@upi
    private String payeeVpa;      // e.g., merchant@upi
    private double amount;
    private String remarks;

    public UpiPaymentRequest() {}

    public String getPayerVpa() { return payerVpa; }
    public void setPayerVpa(String payerVpa) { this.payerVpa = payerVpa; }
    public String getPayeeVpa() { return payeeVpa; }
    public void setPayeeVpa(String payeeVpa) { this.payeeVpa = payeeVpa; }
    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }
    public String getRemarks() { return remarks; }
    public void setRemarks(String remarks) { this.remarks = remarks; }
}
