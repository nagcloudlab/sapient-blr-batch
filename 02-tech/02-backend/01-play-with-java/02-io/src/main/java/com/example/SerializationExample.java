package com.example;

import java.io.FileOutputStream;
import java.io.ObjectOutputStream;

class Account implements java.io.Serializable {
    int accountNumber;
    transient double balance;
    Account(int accountNumber, double balance){
        this.accountNumber = accountNumber;
        this.balance = balance;
    }
}

public class SerializationExample {

    public static void main(String[] args) {

        Account account1 = new Account(101, 1000.0);

        try {
            FileOutputStream fos = new FileOutputStream("account.ser");
            ObjectOutputStream oos = new ObjectOutputStream(fos);
            oos.writeObject(account1);
            oos.close();
            fos.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
}
