package com.example;

import com.example.bill.Billing;
import com.example.bill.StoreBilling;
import com.example.pm.DatabasePriceMatrix;
import com.example.pm.ExcelPriceMatrix;
import com.example.pm.PriceMatrix;

public class ShopApplication {

    public static void main(String[] args) {
        
       //--------------------
       //Initialization
        //--------------------

        PriceMatrix excelPriceMatrix = new ExcelPriceMatrix();
        PriceMatrix databasePriceMatrix = new DatabasePriceMatrix();

        Billing storeBilling= new StoreBilling(databasePriceMatrix);


        //--------------------
        // Use
        //--------------------

        String[] cart ={"A001","A002","A003"}; // store's cart with product codes
        double totalPrice = storeBilling.getTotalPrice(cart);
        System.out.println("Total Price: "+totalPrice);




    }
    
}
