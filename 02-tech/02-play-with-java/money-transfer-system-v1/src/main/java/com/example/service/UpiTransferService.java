package com.example.service;

import org.slf4j.Logger;

import com.example.exception.AccountBalanceException;
import com.example.exception.AccountNotFoundException;
import com.example.model.Account;
import com.example.repository.SqlAccountRepository;

public class UpiTransferService {

    private static Logger logger = org.slf4j.LoggerFactory.getLogger("mts");

    public UpiTransferService() {
        logger.info("UpiTransferService component is initialized...");
    }


    public void transfer(double amount, String fromAccountNumber, String toAccountNumber) {

        logger.info("Transfer request received for amount: {} from account: {} to account: {}", amount, fromAccountNumber, toAccountNumber);
        
        SqlAccountRepository accountRepository = new SqlAccountRepository();
        
        // step-1: Load 'from' account details from database
        Account fromAccount = accountRepository.loadAccount(fromAccountNumber);
        if(fromAccount == null) {
            logger.error("From account not found: {}", fromAccountNumber);
            throw new AccountNotFoundException("From account not found: " + fromAccountNumber);
        }
        if(fromAccount.getBalance() < amount) {
            logger.error("Insufficient balance in account: {}", fromAccountNumber);
            throw new AccountBalanceException("Insufficient balance in account: " + fromAccountNumber);
        }
        // step-2: Load 'to' account details from database
        Account toAccount = accountRepository.loadAccount(toAccountNumber);
        if(toAccount == null) {
            logger.error("To account not found: {}", toAccountNumber);
            throw new AccountNotFoundException("To account not found: " + toAccountNumber);
        }
        // step-3: Deduct amount from 'from' account 
        fromAccount.debit(amount);
        logger.info("Amount: {} debited from account: {}", amount, fromAccountNumber);
        // step-4: Add amount to 'to' account 
        toAccount.credit(amount);
        logger.info("Amount: {} credited to account: {}", amount, toAccountNumber);
        // step-5: Save updated account details back to database
        accountRepository.updateAccount(fromAccount);
        logger.info("From account updated successfully: {}", fromAccountNumber);
        accountRepository.updateAccount(toAccount);
        logger.info("To account updated successfully: {}", toAccountNumber);

        logger.info("Transfer of amount: {} from account: {} to account: {} completed successfully", amount, fromAccountNumber, toAccountNumber);

    }
    
}
