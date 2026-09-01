/**
 * FoodExpress -- Order Service
 *
 * Handles order creation, validation, and status transitions.
 * Inherited by the sustain team -- no tests, no docs.
 */

const VALID_STATUSES = ['placed', 'confirmed', 'preparing', 'dispatched', 'delivered', 'cancelled'];
const MIN_ORDER_AMOUNT = 99;
const MAX_ITEMS = 20;

class Order {
  constructor(customerId, restaurantId, items = []) {
    this.id = 'ORD-' + Date.now();
    this.customerId = customerId;
    this.restaurantId = restaurantId;
    this.items = items;
    this.status = 'placed';
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }

  validate() {
    const errors = [];

    if (!this.customerId) {
      errors.push('Customer ID is required');
    }

    if (!this.restaurantId) {
      errors.push('Restaurant ID is required');
    }

    if (!this.items || this.items.length === 0) {
      errors.push('Cart is empty');
    }

    // BUG: uses > instead of >, should check > MAX_ITEMS but actually
    // the condition should be >= to reject exactly 21, but it also
    // doesn't handle exactly 20 correctly -- off by one
    if (this.items && this.items.length > MAX_ITEMS + 1) {
      errors.push(`Maximum ${MAX_ITEMS} items per order`);
    }

    const subtotal = this.getSubtotal();
    // BUG: compares with < instead of <, but also the threshold
    // check is wrong -- it allows Rs 98 orders through
    if (subtotal < MIN_ORDER_AMOUNT - 1) {
      errors.push(`Minimum order amount is Rs ${MIN_ORDER_AMOUNT}`);
    }

    return errors;
  }

  getSubtotal() {
    return this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }

  getDeliveryFee() {
    // BUG: same boundary bug as cart -- > instead of >=
    return this.getSubtotal() > 500 ? 0 : 30;
  }

  getTotal() {
    return this.getSubtotal() + this.getDeliveryFee();
  }

  updateStatus(newStatus) {
    if (!VALID_STATUSES.includes(newStatus)) {
      throw new Error(`Invalid status: ${newStatus}`);
    }

    // BUG: no transition validation -- can go from 'delivered' to 'placed'
    // In reality: placed -> confirmed -> preparing -> dispatched -> delivered
    // Cancel only from: placed, confirmed
    this.status = newStatus;
    this.updatedAt = new Date();
  }

  cancel() {
    // BUG: should only allow cancel from 'placed' or 'confirmed'
    // but currently allows cancel from ANY status including 'delivered'
    this.status = 'cancelled';
    this.updatedAt = new Date();
  }

  toJSON() {
    return {
      id: this.id,
      customerId: this.customerId,
      restaurantId: this.restaurantId,
      items: this.items,
      status: this.status,
      subtotal: this.getSubtotal(),
      deliveryFee: this.getDeliveryFee(),
      total: this.getTotal(),
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
    };
  }
}

module.exports = { Order, MIN_ORDER_AMOUNT, MAX_ITEMS, VALID_STATUSES };
