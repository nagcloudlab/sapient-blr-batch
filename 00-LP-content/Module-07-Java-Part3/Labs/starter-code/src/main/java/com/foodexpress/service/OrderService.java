package com.foodexpress.service;

import java.util.ArrayList;
import java.util.List;

/**
 * FoodExpress OrderService - manages the order lifecycle.
 *
 * BUGS TO FIX (2 bugs):
 * 1. ConcurrentModificationException — modifying list during for-each iteration
 * 2. Raw types used — no generics (List instead of List<String>)
 */
public class OrderService {

    // BUG #2: Raw type — should be List<String>
    private List activeOrderIds = new ArrayList();
    private List<Double> orderTotals = new ArrayList<>();

    public void addOrder(String orderId, double total) {
        activeOrderIds.add(orderId);
        orderTotals.add(total);
        System.out.println("Added order: " + orderId + " ($" + total + ")");
    }

    /**
     * Cancels all orders below a minimum amount.
     * BUG #1: Modifying list during for-each iteration causes ConcurrentModificationException
     */
    public void cancelSmallOrders(double minimumAmount) {
        // BUG #1: ConcurrentModificationException!
        // Cannot remove from a list while iterating with for-each
        for (Double total : orderTotals) {
            if (total < minimumAmount) {
                orderTotals.remove(total);
            }
        }
        System.out.println("Cancelled orders below $" + minimumAmount);
    }

    /**
     * Gets all active order IDs.
     * BUG #2: Returns raw List — caller gets no type safety
     */
    public List getActiveOrderIds() {
        return activeOrderIds;
    }

    public void printSummary() {
        System.out.println("Active orders: " + activeOrderIds.size());
        System.out.println("Order totals: " + orderTotals);
    }
}
