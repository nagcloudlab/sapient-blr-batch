/**
 * FoodExpress -- Shopping Cart Module
 *
 * This module handles cart operations for the FoodExpress platform.
 * It was written 6 months ago by a developer who has since left.
 * No tests were ever written.
 */

class Cart {
  constructor() {
    this.items = [];
  }

  addItem(item) {
    const existing = this.items.find(i => i.id === item.id);
    if (existing) {
      existing.quantity += item.quantity;
    } else {
      this.items.push({ ...item });
    }
  }

  removeItem(itemId) {
    this.items = this.items.filter(i => i.id !== itemId);
  }

  updateQuantity(itemId, newQuantity) {
    const item = this.items.find(i => i.id === itemId);
    if (item) {
      item.quantity = newQuantity;
    }
  }

  getItemCount() {
    return this.items.length;
  }

  getSubtotal() {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }

  getDeliveryFee() {
    const subtotal = this.getSubtotal();
    // BUG: uses > instead of >=, so exactly Rs 500 still gets charged
    if (subtotal > 500) {
      return 0;
    }
    return 30;
  }

  applyDiscount(percent) {
    // BUG: divides by 1000 instead of 100 (regression from a previous "fix")
    const factor = 1 - percent / 1000;
    return Math.round(this.getSubtotal() * factor * 100) / 100;
  }

  getTotal() {
    return this.getSubtotal() + this.getDeliveryFee();
  }

  getTotalWithDiscount(percent) {
    return this.applyDiscount(percent) + this.getDeliveryFee();
  }

  toSummary() {
    return {
      itemCount: this.getItemCount(),
      subtotal: this.getSubtotal(),
      deliveryFee: this.getDeliveryFee(),
      total: this.getTotal(),
    };
  }

  clear() {
    this.items = [];
  }
}

module.exports = Cart;
