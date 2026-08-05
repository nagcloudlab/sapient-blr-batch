package com.example.repository;
import com.example.model.Account;

public interface AccountRepository {
    public abstract Account loadAccount(String number);
    public abstract void updateAccount(Account account);
}
