package com.example;

import java.io.FileInputStream;
import java.io.ObjectInputStream;
import java.io.IOException;
public class DeSerializationExample {

    public static void main(String[] args) throws IOException, ClassNotFoundException {


        FileInputStream fis = new FileInputStream("account.ser");
        ObjectInputStream ois = new ObjectInputStream(fis);
        Account account1 = (Account) ois.readObject();
        ois.close();
        fis.close();

        System.out.println("Account Number: " + account1.accountNumber);
        System.out.println("Balance: " + account1.balance);

    }
    
}
