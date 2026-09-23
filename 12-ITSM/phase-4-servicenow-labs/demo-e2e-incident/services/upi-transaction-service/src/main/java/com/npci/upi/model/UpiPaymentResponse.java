package com.npci.upi.model;

public class UpiPaymentResponse {
    private String transactionId;
    private String status;         // SUCCESS, FAILED, PENDING
    private String payerVpa;
    private String payeeVpa;
    private double amount;
    private String rrn;            // Retrieval Reference Number
    private String errorCode;
    private String errorMessage;

    public UpiPaymentResponse() {}

    public String getTransactionId() { return transactionId; }
    public void setTransactionId(String transactionId) { this.transactionId = transactionId; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public String getPayerVpa() { return payerVpa; }
    public void setPayerVpa(String payerVpa) { this.payerVpa = payerVpa; }
    public String getPayeeVpa() { return payeeVpa; }
    public void setPayeeVpa(String payeeVpa) { this.payeeVpa = payeeVpa; }
    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }
    public String getRrn() { return rrn; }
    public void setRrn(String rrn) { this.rrn = rrn; }
    public String getErrorCode() { return errorCode; }
    public void setErrorCode(String errorCode) { this.errorCode = errorCode; }
    public String getErrorMessage() { return errorMessage; }
    public void setErrorMessage(String errorMessage) { this.errorMessage = errorMessage; }
}
