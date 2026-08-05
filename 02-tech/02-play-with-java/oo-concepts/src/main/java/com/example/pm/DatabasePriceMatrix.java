package com.example.pm;

public class DatabasePriceMatrix extends AbstractPriceMatrix implements PriceMatrix {
    
    @Override
    public double getPrice(String productCode) {
        // Simulating a database price lookup
        return 200.00; // For simplicity, returning a fixed price
    }

   

}
