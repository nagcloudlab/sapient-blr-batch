/**
 * FoodExpress — Cart Tests (FIXED VERSION — all 4 bugs resolved)
 */

// ---- Minimal Cart implementation ----
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
    // FIX 4: Changed percent/1000 back to percent/100.
    //   The regression divided by 1000, making a "10%" discount
    //   only 1%. This is the root cause of the failing test.
    const factor = 1 - percent / 100;
    return Math.round(this.getTotal() * factor * 100) / 100;
  }

  async fetchDeliveryFee(pincode) {
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

describe('Cart', () => {
  let cart;

  // FIX 3: Create a fresh cart before each test.
  //   The original code created one shared `const cart` outside
  //   describe(), so tests depended on execution order. Items
  //   added in one test leaked into the next. Using beforeEach
  //   guarantees each test starts with a clean cart.
  beforeEach(() => {
    cart = new Cart();
  });

  test('adds an item to the cart', () => {
    cart.addItem({ id: 1, name: 'Chicken Biryani', price: 250, quantity: 2 });
    expect(cart.items.length).toBe(1);
    expect(cart.items[0].quantity).toBe(2);
  });

  test('increases quantity when same item added again', () => {
    cart.addItem({ id: 1, name: 'Chicken Biryani', price: 250, quantity: 2 });
    cart.addItem({ id: 1, name: 'Chicken Biryani', price: 250, quantity: 1 });
    expect(cart.items[0].quantity).toBe(3);
  });

  test('removes an item from the cart', () => {
    cart.addItem({ id: 2, name: 'Garlic Bread', price: 120, quantity: 1 });
    cart.removeItem(2);
    expect(cart.items.find(i => i.id === 2)).toBeUndefined();
  });

  test('calculates total correctly', () => {
    cart.addItem({ id: 1, name: 'Chicken Biryani', price: 250, quantity: 3 });
    expect(cart.getTotal()).toBe(750);
  });

  // FIX 1: Changed toBe() to toEqual() for object comparison.
  //   toBe uses Object.is (reference equality). Two distinct
  //   objects { a: 1 } === { a: 1 } is false. toEqual performs
  //   deep structural comparison, which is what we need here.
  test('returns cart summary', () => {
    cart.addItem({ id: 1, name: 'Chicken Biryani', price: 250, quantity: 3 });
    const summary = cart.toSummary();
    expect(summary).toEqual({ itemCount: 1, total: 750 });
  });

  // FIX 2: Added async/await to the test.
  //   Without await, fetchDeliveryFee returns a Promise object,
  //   and expect(Promise).toBe(30) passes silently because Jest
  //   does not know to wait for the async result. Adding async
  //   to the test function and await before the call ensures
  //   the resolved value is actually tested.
  test('fetches delivery fee for Bangalore pincode', async () => {
    const fee = await cart.fetchDeliveryFee('560001');
    expect(fee).toBe(30);
  });

  // FIX 4: Test now passes because applyDiscount is corrected.
  test('applies 10% discount correctly', () => {
    cart.addItem({ id: 1, name: 'Chicken Biryani', price: 250, quantity: 3 });
    const discounted = cart.applyDiscount(10);
    expect(discounted).toBe(675); // 750 - 10% = 675
  });
});
