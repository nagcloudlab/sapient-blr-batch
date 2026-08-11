package com.foodexpress.model;

/**
 * FoodExpress OrderItem - links a MenuItem with a quantity in an order.
 * FIXED: .equals() for String comparison, static method no longer accesses instance field.
 */
public class OrderItem {

    private String menuItemName;
    private double unitPrice;
    private int quantity;
    private String specialInstructions;

    public OrderItem(String menuItemName, double unitPrice, int quantity, String specialInstructions) {
        this.menuItemName = menuItemName;
        this.unitPrice = unitPrice;
        this.quantity = quantity;
        this.specialInstructions = specialInstructions;
    }

    public double getSubtotal() {
        return unitPrice * quantity;
    }

    // FIX #1: Use .equals() for String comparison
    public boolean isSameItem(String otherName) {
        return menuItemName.equals(otherName);
    }

    // FIX #2: Changed to instance method (removed static) so it can access unitPrice
    public String formatPrice() {
        return String.format("$%.2f", unitPrice);
    }

    public String getMenuItemName() { return menuItemName; }
    public double getUnitPrice() { return unitPrice; }
    public int getQuantity() { return quantity; }
    public String getSpecialInstructions() { return specialInstructions; }

    @Override
    public String toString() {
        return quantity + "x " + menuItemName + " @ $" + unitPrice + " = $" + getSubtotal();
    }
}
