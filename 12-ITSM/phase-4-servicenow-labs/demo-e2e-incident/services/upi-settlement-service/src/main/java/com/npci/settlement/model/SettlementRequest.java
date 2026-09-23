package com.npci.settlement.model;

public class SettlementRequest {
    private String payerVpa;
    private String payeeVpa;
    private double amount;
    private String remarks;
    private String settlementCycle;  // IMMEDIATE, HOURLY, EOD

    public SettlementRequest() {}

    public String getPayerVpa() { return payerVpa; }
    public void setPayerVpa(String payerVpa) { this.payerVpa = payerVpa; }
    public String getPayeeVpa() { return payeeVpa; }
    public void setPayeeVpa(String payeeVpa) { this.payeeVpa = payeeVpa; }
    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }
    public String getRemarks() { return remarks; }
    public void setRemarks(String remarks) { this.remarks = remarks; }
    public String getSettlementCycle() { return settlementCycle; }
    public void setSettlementCycle(String settlementCycle) { this.settlementCycle = settlementCycle; }
}
