package com.example.service;

import com.example.entity.Account;
import com.example.exception.AccountBalanceException;
import com.example.exception.AccountNotFoundException;
import com.example.repository.AccountRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class UpiTransferService implements TransferService {
    private static final Logger logger = LoggerFactory.getLogger(UpiTransferService.class);

    private AccountRepository accountRepository;

    public UpiTransferService(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
        logger.info("UpiTransferService initialized with AccountRepository");
    }
    
    @Override
    public void transfer(double amount, String fromAccountNumber, String toAccountNumber) {
        logTransferAction(amount, fromAccountNumber, toAccountNumber);
        logger.info("Transfer flow started");

        Account fromAccount = accountRepository.findByAccountNumber(fromAccountNumber);
        if(fromAccount == null) {
            logger.warn("From account not found for transfer: {}", fromAccountNumber);
            throw new AccountNotFoundException("Account not found: " + fromAccountNumber);
        }
        if(fromAccount.getBalance() < amount) {
            logger.warn("Insufficient balance for transfer from account={} balance={} amount={}", fromAccountNumber, fromAccount.getBalance(), amount);
            throw new AccountBalanceException("Insufficient balance in account: " + fromAccountNumber);
        }
        Account toAccount = accountRepository.findByAccountNumber(toAccountNumber);
        if(toAccount == null) {
            logger.warn("To account not found for transfer: {}", toAccountNumber);
            throw new AccountNotFoundException("Account not found: " + toAccountNumber);
        }

        logger.info("Applying debit and credit for transfer");
        fromAccount.debit(amount);
        toAccount.credit(amount);

        accountRepository.update(fromAccount);
        accountRepository.update(toAccount);
        
        logger.info("Transfer flow completed successfully");

    }
    
}
