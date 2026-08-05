package com.example.pm;

public interface PriceMatrix {

    // cnstantant variables

    // no constructors

    // 2016
    double getPrice(String productCode);
    void m1();
    void m2();
    //2026
    default void m3(){
        //...
    }
}
