package com.foodexpress;

import com.foodexpress.model.MenuItem;
import com.foodexpress.model.OrderItem;
import com.foodexpress.model.Restaurant;

/**
 * FoodExpress Application - Module 05 Demo
 * Run this class to see the bugs in action.
 */
public class App {

    public static void main(String[] args) {
        System.out.println("=== FoodExpress Order Service ===\n");

        // --- MenuItem Bugs Demo ---
        // BUG: public fields allow direct modification — no validation
        MenuItem burger = new MenuItem("Classic Burger", "Juicy beef patty", 12.99, "Main");
        burger.price = -5.00;  // Negative price! No setter to validate
        burger.name = "";      // Empty name! No setter to validate
        System.out.println("MenuItem (with bugs): " + burger);

        // --- OrderItem Bugs Demo ---
        OrderItem item1 = new OrderItem("Classic Burger", 12.99, 2, "No onions");

        // BUG: == comparison fails for runtime-created strings
        String searchName = new String("Classic Burger"); // Created at runtime
        System.out.println("Same item (==)?  " + item1.isSameItem(searchName)); // false!
        System.out.println("Expected: true\n");

        // BUG: Static method accessing instance field — won't compile
        // Uncomment the next line to see the compilation error:
        // System.out.println("Formatted: " + OrderItem.formatPrice());

        // --- Restaurant Bugs Demo ---
        Restaurant r1 = new Restaurant(null, "123 Main St", -3.0); // null name, negative rating
        Restaurant r2 = new Restaurant("Pizza Palace", "456 Oak Ave", 4.5);

        r1.addMenuItem(new MenuItem("Test Item", "Test", 9.99, "Test"));
        System.out.println("Restaurant 1: " + r1);  // null name displayed
        System.out.println("Restaurant 2: " + r2);

        // BUG: restaurantCount never incremented
        System.out.println("Total restaurants: " + Restaurant.getRestaurantCount()); // 0!
        System.out.println("Expected: 2");
    }
}
