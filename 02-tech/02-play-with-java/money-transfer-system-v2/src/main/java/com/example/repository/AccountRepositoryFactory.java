package com.example.repository;

// Factory class to create instances of AccountRepository based on the specified type
public class AccountRepositoryFactory {

    // Factory method to create an AccountRepository instance based on the provided type
   public static AccountRepository createAccountRepository(String type) {
        if(type.equalsIgnoreCase("SQL")) {
            return new SqlAccountRepository();
        } else if(type.equalsIgnoreCase("NoSQL")) {
            return new NoSqlAccountRepository();
        } else {
            throw new IllegalArgumentException("Unknown repository type: " + type);
        }
    }
    
}
