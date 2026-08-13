package com.example.service;

public interface TransferService {
    public void transferFunds(String fromAccountNumber, String toAccountNumber, double amount);
}
