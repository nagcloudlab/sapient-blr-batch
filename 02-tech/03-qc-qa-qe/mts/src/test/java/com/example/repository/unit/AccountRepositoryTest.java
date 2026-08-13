package com.example.repository.unit;

import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.example.entity.Account;
import com.example.repository.AccountRepository;

import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

@SpringBootTest
public class AccountRepositoryTest {

    @Autowired
    private AccountRepository accountRepository;

    @Test
    @Disabled
    public void beTrue(){
        //..
        // Arrange
        // Act
        boolean actual = true; // Replace with actual method call to be tested
        // Assert
        boolean expected = true; // Replace with the expected result
        assertEquals(expected, actual);
    }

    @Test
    public void getAccountsByBalance(){
        List<Account> accounts = accountRepository.findByBalance(400.0);
        int actual = accounts.size();
        int expected = 1;
        assertEquals(expected, actual);
    }
    
}
