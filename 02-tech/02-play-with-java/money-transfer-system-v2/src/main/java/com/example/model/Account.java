package com.example.model;


public class Account {

    private String number;
    private double balance;

    public Account(String number){
       this(number, 0.0);
    }
    public Account(String number, double balance){
         if(number == null || number.isEmpty()){
            throw new IllegalArgumentException("Account number cannot be null or empty");
        }
        // if(!number.matches("\\d{12}")){
        //     throw new IllegalArgumentException("Account number must be 12 digits");
        // }
        if(balance < 0){
            throw new IllegalArgumentException("Balance cannot be negative");
        }
        this.number = number;
        this.balance = balance;
    }

    public void debit(double amount){
        if(amount <= 0){
            throw new IllegalArgumentException("Withdrawal amount must be positive");
        }
        if(amount > balance){
            throw new IllegalArgumentException("Insufficient funds");
        }
        balance -= amount;
    }
    public void credit(double amount){
        if(amount <= 0){
            throw new IllegalArgumentException("Deposit amount must be positive");
        }
        balance += amount;
    }

    public String getNumber() {
        return number;
    }

    public double getBalance() {
        return balance;
    }
    
}
