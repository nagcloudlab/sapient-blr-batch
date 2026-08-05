package com.example.repository;

import org.slf4j.Logger;

import com.example.model.Account;

public class SqlAccountRepository {

    private static Logger logger = org.slf4j.LoggerFactory.getLogger("mts");

    public SqlAccountRepository() {
        logger.info("SqlAccountRepository component is initialized...");
    }

    public Account loadAccount(String number){
        logger.info("Loading account details for account number: {}", number);
        //...sql query to load account from database
        return new Account(number,1000.00);
    }
    public void updateAccount(Account account){
        logger.info("Updating account details for account number: {}", account.getNumber());
        //...sql query to update account in database
    }
}
