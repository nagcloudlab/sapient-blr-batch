package com.example;

import java.util.List;

import com.example.model.Apple;

public class Why_We_Need_Lambda {

    public static void main(String[] args) {
        
        List<Apple> inventory = List.of(
            new Apple("green", 150),
            new Apple("red", 200),
            new Apple("green", 120),
            new Apple("yellow", 180)
        );

        // Req-1: Filter all green apples from the inventory

    }
    
}
