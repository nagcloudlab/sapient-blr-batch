package com.foodexpress.service;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/**
 * FoodExpress OrderService - manages the order lifecycle.
 * FIXED: Uses Iterator.remove() to avoid ConcurrentModificationException, proper generics.
 */
public class OrderService {

    // FIX #2: Proper generics — List<String> instead of raw List
    private List<String> activeOrderIds = new ArrayList<>();
    private List<Double> orderTotals = new ArrayList<>();

    public void addOrder(String orderId, double total) {
        activeOrderIds.add(orderId);
        orderTotals.add(total);
        System.out.println("Added order: " + orderId + " ($" + total + ")");
    }

    /**
     * Cancels all orders below a minimum amount.
     * FIX #1: Uses Iterator.remove() to safely modify list during iteration.
     */
    public void cancelSmallOrders(double minimumAmount) {
        // FIX #1: Use Iterator to safely remove during iteration
        Iterator<Double> iterator = orderTotals.iterator();
        while (iterator.hasNext()) {
            Double total = iterator.next();
            if (total < minimumAmount) {
                iterator.remove();  // Safe removal via Iterator
            }
        }
        System.out.println("Cancelled orders below $" + minimumAmount);
    }

    /**
     * Gets all active order IDs.
     * FIX #2: Returns properly typed List<String>
     */
    public List<String> getActiveOrderIds() {
        return activeOrderIds;
    }

    public void printSummary() {
        System.out.println("Active orders: " + activeOrderIds.size());
        System.out.println("Order totals: " + orderTotals);
    }
}
