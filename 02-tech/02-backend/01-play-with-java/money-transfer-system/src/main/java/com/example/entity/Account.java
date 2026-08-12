package com.example.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Account {
    private static final Logger logger = LoggerFactory.getLogger(Account.class);

    private String accountNumber;
    private String accountHolderName;
    private double balance;

    public void debit(double amount) {
        logger.info("Debiting amount={} from account={}", amount, accountNumber);
        this.balance = this.balance - amount;
    }

    public void credit(double amount) {
        logger.info("Crediting amount={} to account={}", amount, accountNumber);
        this.balance = this.balance + amount;
    }
    
}
