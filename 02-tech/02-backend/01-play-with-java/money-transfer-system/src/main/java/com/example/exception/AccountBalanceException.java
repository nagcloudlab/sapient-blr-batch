package com.example.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AccountBalanceException  extends RuntimeException {
    private static final Logger logger = LoggerFactory.getLogger(AccountBalanceException.class);

    public AccountBalanceException(String message) {
        super(message);
        logger.error("AccountBalanceException thrown: {}", message);
    }
    
}
