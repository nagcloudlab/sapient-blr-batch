package com.example;

import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import com.example.model.Product;

public class ListExample {

    public static void main(String[] args) {
        // compareList(new java.util.Vector<>());
        // compareList(new java.util.ArrayList<>());
        // compareList(new java.util.LinkedList<>());


        List<Product> products = new java.util.ArrayList<>();
        products.add(new Product("Product 1", 10.0, 4));
        products.add(new Product("Product 3", 30.0, 1));
        products.add(new Product("Product 2", 20.0, 3));
        products.add(new Product("Product 5", 50.0, 5));
        products.add(new Product("Product 4", 40.0, 2));
        products.add(new Product("Product 5", 50.0, 5));

        displayProducts(products);

        System.out.println("Sorting products by price (natural order)...");
        
        class PriceComparator implements Comparator<Product>{
            @Override
            public int compare(Product p1, Product p2) {
                return Double.compare(p1.getPrice(), p2.getPrice());
            }
        }
        
        Collections.sort(products,new PriceComparator());

        displayProducts(products);

    }

    private static void displayProducts(List<Product> products){
        for(Product p : products){
            System.out.println(p);
        }
    }

    private static void compareList(List<Product> list){
        long start = System.currentTimeMillis();
        for(int i=0; i<100000; i++){
            Product p = new Product("Product " + i, i * 10.0, i);
            list.add(p);
        }
        long end = System.currentTimeMillis();
        System.out.println("Time taken to add 10 thousand products: " + (end - start) + " ms");
    }
    

    
}

