package com.example.service;

import org.springframework.stereotype.Service;

import com.example.entity.Account;
import com.example.repository.AccountRepository;

@Service
public class UpiTransferService implements TransferService {

    private final AccountRepository accountRepository;

    public UpiTransferService(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }

    @Override
    public void transferFunds(String fromAccountNumber, String toAccountNumber, double amount) {
       
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
        accountRepository.save(toAccount);
    }


}
