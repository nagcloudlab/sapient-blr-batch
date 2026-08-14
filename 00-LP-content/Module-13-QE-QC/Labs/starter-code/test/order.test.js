/**
 * FoodExpress — Order Service Tests (BUGGY VERSION — 2 bugs)
 *
 * These tests are written in a JUnit-inspired style using Jest
 * to simulate what participants will see in Java-based testing.
 *
 * BUG 1: Missing "test" wrapper — function defined but never runs
 * BUG 2: assertEquals arguments in wrong order (expected, actual swapped)
 */

// ---- Minimal Order model ----
class Order {
  constructor(customerId, restaurantId, items = []) {
    this.customerId = customerId;
    this.restaurantId = restaurantId;
    this.items = items;
    this.status = 'placed';
    this.createdAt = new Date();
  }

  getSubtotal() {
    return this.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  }

  getTotal(deliveryFee = 30) {
    return this.getSubtotal() + deliveryFee;
  }

  cancel() {
    if (this.status === 'delivered') {
      throw new Error('Cannot cancel a delivered order');
    }
    this.status = 'cancelled';
  }

  confirm() {
    if (this.status !== 'placed') {
      throw new Error('Only placed orders can be confirmed');
    }
    this.status = 'confirmed';
  }
}

// ---- Tests ----

describe('Order Service', () => {
  let order;

  beforeEach(() => {
    order = new Order(1, 2, [
      { id: 5, name: 'Margherita Pizza', price: 300, quantity: 1 },
      { id: 7, name: 'Garlic Bread',     price: 120, quantity: 1 },
    ]);
  });

  test('creates order with placed status', () => {
    expect(order.status).toBe('placed');
  });

  test('calculates subtotal from items', () => {
    expect(order.getSubtotal()).toBe(420);
  });

  // BUG 2: Arguments are swapped — Jest convention is
  //        expect(actual).toBe(expected), but here the
  //        actual and expected are reversed in the comment
  //        and the values don't match the intent.
  //        The test passes by accident because 450 is correct,
  //        but the message on failure would be confusing.
  test('calculates total with delivery fee', () => {
    // Swapped: should be expect(order.getTotal()).toBe(450)
    expect(450).toBe(order.getTotal());
  });

  // BUG 1: This function is defined but NOT wrapped in test().
  //        It looks like a test but Jest will never execute it.
  //        Participants must spot that it is silently skipped.
  function testCancelDeliveredOrderThrows() {
    order.status = 'delivered';
    expect(() => order.cancel()).toThrow('Cannot cancel a delivered order');
  }

  test('cancels a placed order', () => {
    order.cancel();
    expect(order.status).toBe('cancelled');
  });

  test('confirms a placed order', () => {
    order.confirm();
    expect(order.status).toBe('confirmed');
  });

  test('throws when confirming a non-placed order', () => {
    order.status = 'confirmed';
    expect(() => order.confirm()).toThrow('Only placed orders can be confirmed');
  });
});
