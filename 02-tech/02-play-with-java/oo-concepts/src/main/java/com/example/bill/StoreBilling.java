package com.example.bill;

import com.example.pm.PriceMatrix;

/*
Author: team-2
*/

public class StoreBilling implements Billing {

    private PriceMatrix priceMatrix;

    public StoreBilling(PriceMatrix priceMatrix) {
        this.priceMatrix = priceMatrix;
    }

    public void setPriceMatrix(PriceMatrix priceMatrix) {
        this.priceMatrix = priceMatrix;
    }

    public double getTotalPrice(String[] cart){
        double total=0.0;
        for(String itemCode: cart){
            total += priceMatrix.getPrice(itemCode);
        }
        total-=500;
        return total;
    }
    
}
