package com.npci.settlement.model;

public class SettlementResponse {
    private String settlementId;
    private String transactionId;
    private String status;          // SETTLED, PENDING, FAILED
    private double amount;
    private String payerBank;
    private String payeeBank;
    private String errorMessage;

    public SettlementResponse() {}

    public String getSettlementId() { return settlementId; }
    public void setSettlementId(String settlementId) { this.settlementId = settlementId; }
    public String getTransactionId() { return transactionId; }
    public void setTransactionId(String transactionId) { this.transactionId = transactionId; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }
    public String getPayerBank() { return payerBank; }
    public void setPayerBank(String payerBank) { this.payerBank = payerBank; }
    public String getPayeeBank() { return payeeBank; }
    public void setPayeeBank(String payeeBank) { this.payeeBank = payeeBank; }
    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }
}
