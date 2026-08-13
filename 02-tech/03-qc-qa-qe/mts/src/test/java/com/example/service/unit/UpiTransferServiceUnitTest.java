package com.example.service.unit;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;

import com.example.entity.Account;
import com.example.repository.AccountRepository;
import com.example.service.TransferService;
import com.example.service.UpiTransferService;

public class UpiTransferServiceUnitTest {


    private TransferService transferService;
    private AccountRepository accountRepositoryMock;

    @BeforeEach
    public void setUp() {
        // Initialize the mock AccountRepository before each test
        accountRepositoryMock = org.mockito.Mockito.mock(AccountRepository.class);
        transferService = new UpiTransferService(accountRepositoryMock);
    }

    // Positive test cases for UPI transfer functionality
    @Test
    public void testSuccessfulUpiTransfer() {
        // Arrange
        // Implement the test logic for a successful UPI transfer
        String fromAccountNumber = "1234567890";
        String toAccountNumber = "0987654321";
        double amount = 100.0;

        // Mock the behavior of the accountRepositoryMock to simulate a successful transfer
        
        Account fromAccount = new Account(fromAccountNumber, 500.0);
        Account toAccount = new Account(toAccountNumber, 200.0);
        when(accountRepositoryMock.findById(fromAccountNumber)).thenReturn(Optional.of(fromAccount));
        when(accountRepositoryMock.findById(toAccountNumber)).thenReturn(Optional.of(toAccount));

        // Act
        transferService.transferFunds(fromAccountNumber, toAccountNumber, amount);

        // Assert
        assertEquals(400.0, fromAccount.getBalance());
        assertEquals(300.0, toAccount.getBalance());

        verify(accountRepositoryMock).save(fromAccount);
        verify(accountRepositoryMock).save(toAccount);
        
    }
    
}
