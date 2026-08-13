package com.example.service.integration;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Optional;


import com.example.entity.Account;
import com.example.repository.AccountRepository;
import com.example.service.TransferService;

@SpringBootTest
public class UpiTransferServiceIntegrationTest {

    @Autowired
    private TransferService transferService;
    @Autowired
    private AccountRepository accountRepository;

    @Transactional // end of test, rollback the changes made to the database
    @Test
    public void testSuccessfulUpiTransfer() {
        // Arrange
        // Implement the test logic for a successful UPI transfer
        String fromAccountNumber = "1234567890";
        String toAccountNumber = "0987654321";
        double amount = 100.0;

        // Act
        transferService.transferFunds(fromAccountNumber, toAccountNumber, amount);

        // Assert
        Optional<Account> fromAccountOpt = accountRepository.findById(fromAccountNumber);
        Optional<Account> toAccountOpt = accountRepository.findById(toAccountNumber);

        assertEquals(true, fromAccountOpt.isPresent());
        assertEquals(true, toAccountOpt.isPresent());
        assertEquals(200.0, fromAccountOpt.get().getBalance());
        assertEquals(1300.0, toAccountOpt.get().getBalance());
        
    }
    
}
