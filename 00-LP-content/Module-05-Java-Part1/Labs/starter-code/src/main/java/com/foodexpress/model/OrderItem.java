package com.foodexpress.model;

/**
 * FoodExpress OrderItem - links a MenuItem with a quantity in an order.
 *
 * BUGS TO FIX (2 bugs):
 * 1. Uses == for String comparison instead of .equals()
 * 2. Static method tries to access instance field (won't compile or gives wrong result)
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

    // BUG #1: Uses == for String comparison instead of .equals()
    // This will fail when comparing strings created at runtime (e.g., from user input)
    public boolean isSameItem(String otherName) {
        return menuItemName == otherName;
    }

    // BUG #2: Static method tries to access instance field 'unitPrice'
    // Static methods cannot access instance fields
    public static String formatPrice() {
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
