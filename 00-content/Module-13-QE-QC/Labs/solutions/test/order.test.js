/**
 * FoodExpress — Order Service Tests (FIXED VERSION — all 2 bugs resolved)
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

  // FIX 2: Corrected argument order.
  //   Jest convention: expect(actual).toBe(expected).
  //   The original had expect(450).toBe(order.getTotal()) which
  //   passes by coincidence but produces confusing failure messages:
  //     "Expected: 450, Received: 450" vs "Expected: 450, Received: 420"
  //   Always put the value under test inside expect().
  test('calculates total with delivery fee', () => {
    expect(order.getTotal()).toBe(450);
  });

  // FIX 1: Wrapped the bare function in test().
  //   The original defined `function testCancelDeliveredOrderThrows()`
  //   but never registered it with Jest. It looked like a test in
  //   the file but was silently skipped. Wrapping it in test()
  //   ensures Jest discovers and runs it.
  test('throws when cancelling a delivered order', () => {
    order.status = 'delivered';
    expect(() => order.cancel()).toThrow('Cannot cancel a delivered order');
  });

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
