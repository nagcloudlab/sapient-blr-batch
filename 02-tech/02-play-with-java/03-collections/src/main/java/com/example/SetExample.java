package com.example;

import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

import com.example.model.Product;

public class SetExample {

    public static void main(String[] args) {
        

        // Set<Product> products = new TreeSet<>((product1, product2) -> {
        //     // Compare by price
        //     return Double.compare(product1.getPrice(), product2.getPrice());
        // });
        Set<Product> products=new LinkedHashSet<>();

        Product p1 = new Product("Laptop", 1200.00, 5);
        Product p2 = new Product("Mobile", 1300.00, 10);

        System.out.println(p1.hashCode());
        System.out.println(p2.hashCode());

        products.add(p1);
        products.add(p2);

        displayProducts(products);

    }

    private static void displayProducts(Set<Product> products){
        for(Product p : products){
            System.out.println(p);
        }
    }

}
