package com.foodexpress.model;

/**
 * FoodExpress Priceable interface — any item that has a price.
 * This file is correct — no changes needed.
 */
public interface Priceable {

    double getPrice();

    double getDiscountedPrice(double discountPercent);
}
