package com.example.repository;

import com.example.entity.Account;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public interface AccountRepository {
    Logger logger = LoggerFactory.getLogger(AccountRepository.class);

    default void logFindAction(String accountNumber) {
        logger.info("Repository find action for account={}", accountNumber);
    }

    default void logUpdateAction(Account account) {
        logger.info("Repository update action for account={}", account.getAccountNumber());
    }

    Account findByAccountNumber(String accountNumber);
    void update(Account account);
}
