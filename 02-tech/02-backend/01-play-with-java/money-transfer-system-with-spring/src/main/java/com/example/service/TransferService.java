package com.example.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public interface TransferService {
    Logger logger = LoggerFactory.getLogger(TransferService.class);

    default void logTransferAction(double amount, String fromAccountNumber, String toAccountNumber) {
        logger.info("Transfer action requested: amount={}, from={}, to={}", amount, fromAccountNumber, toAccountNumber);
    }

    void transfer(double amount,String fromAccountNumber, String toAccountNumber);
}
