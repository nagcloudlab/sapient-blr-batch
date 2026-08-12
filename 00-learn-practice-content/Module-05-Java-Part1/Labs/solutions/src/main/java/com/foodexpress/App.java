package com.foodexpress;

import com.foodexpress.model.MenuItem;
import com.foodexpress.model.OrderItem;
import com.foodexpress.model.Restaurant;

/**
 * FoodExpress Application - Module 05 Demo (Fixed)
 * All bugs resolved — proper encapsulation, validation, and correct comparisons.
 */
public class App {

    public static void main(String[] args) {
        System.out.println("=== FoodExpress Order Service ===\n");

        // --- MenuItem: Encapsulation enforced ---
        MenuItem burger = new MenuItem("Classic Burger", "Juicy beef patty", 12.99, "Main");
        // burger.price = -5.00;  // FIXED: Won't compile — field is private
        // burger.setPrice(-5.00); // Would throw IllegalArgumentException
        System.out.println("MenuItem: " + burger);

        // --- OrderItem: .equals() and instance method ---
        OrderItem item1 = new OrderItem("Classic Burger", 12.99, 2, "No onions");

        String searchName = new String("Classic Burger");
        System.out.println("Same item (.equals())?  " + item1.isSameItem(searchName)); // true!

        // FIXED: formatPrice() is now an instance method
        System.out.println("Formatted: " + item1.formatPrice());
        System.out.println();

        // --- Restaurant: Validation and counter ---
        // new Restaurant(null, "123 Main St", -3.0); // Would throw IllegalArgumentException
        Restaurant r1 = new Restaurant("Burger Barn", "123 Main St", 4.2);
        Restaurant r2 = new Restaurant("Pizza Palace", "456 Oak Ave", 4.5);

        r1.addMenuItem(burger);
        System.out.println("Restaurant 1: " + r1);
        System.out.println("Restaurant 2: " + r2);

        // FIXED: restaurantCount is correctly incremented
        System.out.println("Total restaurants: " + Restaurant.getRestaurantCount()); // 2
    }
}
