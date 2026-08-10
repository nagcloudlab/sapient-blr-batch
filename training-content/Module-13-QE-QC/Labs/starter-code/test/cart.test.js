/**
 * FoodExpress — Cart Tests (BUGGY VERSION — 4 bugs to find)
 *
 * BUG 1: toBe used instead of toEqual for object comparison
 * BUG 2: async test missing await — test always passes
 * BUG 3: shared state not reset in beforeEach (order-dependent)
 * BUG 4: failing test — discount calculation regression
 */

// ---- Minimal Cart implementation for testing ----
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

  getTotal() {
    return this.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  }

  applyDiscount(percent) {
    // Regression: changed from percent/100 to percent/1000
    const factor = 1 - percent / 1000;
    return Math.round(this.getTotal() * factor * 100) / 100;
  }

  async fetchDeliveryFee(pincode) {
    // Simulates an API call
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(pincode.startsWith('560') ? 30 : 50);
      }, 10);
    });
  }

  toSummary() {
    return {
      itemCount: this.items.length,
      total: this.getTotal(),
    };
  }
}

// ---- Tests ----

// BUG 3: cart is created once and shared across tests.
//        Tests depend on execution order — if addItem test runs
//        first, removeItem test may see leftover items.
const cart = new Cart();

describe('Cart', () => {
  // BUG 3 (fix needed): should use beforeEach to reset cart
  // beforeEach(() => { ... });

  test('adds an item to the cart', () => {
    cart.addItem({ id: 1, name: 'Chicken Biryani', price: 250, quantity: 2 });
    expect(cart.items.length).toBe(1);
    expect(cart.items[0].quantity).toBe(2);
  });

  test('increases quantity when same item added again', () => {
    cart.addItem({ id: 1, name: 'Chicken Biryani', price: 250, quantity: 1 });
    expect(cart.items[0].quantity).toBe(3);
  });

  test('removes an item from the cart', () => {
    cart.addItem({ id: 2, name: 'Garlic Bread', price: 120, quantity: 1 });
    cart.removeItem(2);
    expect(cart.items.find(i => i.id === 2)).toBeUndefined();
  });

  test('calculates total correctly', () => {
    expect(cart.getTotal()).toBe(750); // 250 * 3 from earlier tests
  });

  // BUG 1: toBe compares by reference, not deep equality.
  //        Two different objects with same properties will fail.
  test('returns cart summary', () => {
    const summary = cart.toSummary();
    expect(summary).toBe({ itemCount: 1, total: 750 });
  });

  // BUG 2: missing await — the expect never actually runs,
  //        so the test passes even if the assertion is wrong.
  test('fetches delivery fee for Bangalore pincode', () => {
    const fee = cart.fetchDeliveryFee('560001');
    expect(fee).toBe(30);
  });

  // BUG 4: This test FAILS because applyDiscount has a
  //        regression (divides by 1000 instead of 100).
  test('applies 10% discount correctly', () => {
    const discounted = cart.applyDiscount(10);
    expect(discounted).toBe(675); // 750 - 10% = 675
  });
});
