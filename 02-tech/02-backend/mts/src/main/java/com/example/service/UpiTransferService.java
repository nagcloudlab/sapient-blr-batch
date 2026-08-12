package com.example.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.entity.Account;

@Service
public class UpiTransferService implements TransferService {

    private final com.example.repository.AccountRepository accountRepository;

    //@Autowired
    public UpiTransferService(com.example.repository.AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }

    /*
    
    ACID

    A -> Atomicity: The transfer operation is atomic, meaning that either both the debit and credit operations succeed, or neither does. If an exception occurs during the transfer, the transaction will be rolled back, ensuring that no partial updates are made to the accounts.
    C -> Consistency: The transfer operation maintains the consistency of the database. The total balance across all accounts remains the same before and after the transfer, ensuring that the system remains in a valid state.
    I -> Isolation: The transfer operation is isolated from other concurrent transactions. If multiple transfers are
    D -> Durability: Once the transfer operation is successfully completed and committed, the changes to the account balances are durable and will persist even in the event of a system failure. The updated balances will be stored in the database and can be retrieved later.
    
    */

    @Override
    @Transactional(
        transactionManager = "transactionManager",
        rollbackFor = RuntimeException.class,
        isolation = org.springframework.transaction.annotation.Isolation.READ_COMMITTED
    )
    public void transfer(String fromAccountNumber, String toAccountNumber, double amount) {

        Account fromAccount = accountRepository.findById(fromAccountNumber)
                .orElseThrow(() -> new IllegalArgumentException("Invalid from account number: " + fromAccountNumber));
        Account toAccount = accountRepository.findById(toAccountNumber)
                .orElseThrow(() -> new IllegalArgumentException("Invalid to account number: " + toAccountNumber));

        if (fromAccount.getBalance() < amount) {
            throw new IllegalArgumentException("Insufficient balance in from account: " + fromAccountNumber);
        }

        fromAccount.setBalance(fromAccount.getBalance() - amount);
        toAccount.setBalance(toAccount.getBalance() + amount);

        accountRepository.save(fromAccount);

        boolean simulateException = false; // Change this to true to simulate an exception
        if(simulateException){
            throw new RuntimeException("Simulated exception during UPI transfer");
        }

        accountRepository.save(toAccount);
        
    }
    
}
