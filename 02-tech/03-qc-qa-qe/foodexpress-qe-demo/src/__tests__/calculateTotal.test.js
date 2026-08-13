// ============================================================
// FoodExpress: Unit Tests for calculateTotal
// Demonstrates: Unit Testing, Edge Cases, Test Case Design
// Maps to Slides: 10, 11, 16 (Test Case Design)
// ============================================================

import { calculateTotal, validateOrder } from '../utils/calculateTotal';

// ----------------------------------------------------------
// TC-01 to TC-03: Basic calculation (Happy Path)
// ----------------------------------------------------------

describe('calculateTotal - Basic Calculations', () => {
  test('TC-01: should calculate total for single item', () => {
    const items = [{ name: 'Pizza', price: 299, qty: 1 }];
    const result = calculateTotal(items);
    expect(result.subtotal).toBe(299);
    expect(result.tax).toBe(15);        // 5% of 299 = 14.95, rounded to 15
    expect(result.total).toBe(314);      // 299 + 15
  });
  test('TC-02: should calculate total for multiple items', () => {
    const items = [
      { name: 'Pizza', price: 299, qty: 2 },
      { name: 'Coke', price: 49, qty: 1 },
    ];
    const result = calculateTotal(items);
    expect(result.subtotal).toBe(647);   // (299*2) + (49*1)
    expect(result.tax).toBe(32);         // 5% of 647 = 32.35, rounded to 32
    expect(result.total).toBe(679);      // 647 + 32
  });
  test('TC-03: should return 0 for empty cart', () => {
    const result = calculateTotal([]);
    expect(result.subtotal).toBe(0);
    expect(result.tax).toBe(0);
    expect(result.total).toBe(0);
  });
});

// ----------------------------------------------------------
// TC-04 to TC-06: Input Validation (Negative Testing)
// ----------------------------------------------------------
describe('calculateTotal - Input Validation', () => {
  test('TC-04: should throw error for negative quantity', () => {
    const items = [{ name: 'Pizza', price: 299, qty: -1 }];
    expect(() => calculateTotal(items)).toThrow('Invalid quantity');
  });

  test('TC-05: should throw error for negative price', () => {
    const items = [{ name: 'Pizza', price: -100, qty: 1 }];
    expect(() => calculateTotal(items)).toThrow('Invalid price');
  });

  test('TC-06: should throw error if items is not an array', () => {
    expect(() => calculateTotal('not-an-array')).toThrow('Items must be an array');
    expect(() => calculateTotal(null)).toThrow('Items must be an array');
  });
});

// ----------------------------------------------------------
// TC-07 to TC-10: Discount Logic
//    ** TC-09 WILL FAIL - This catches the planted BUG! **
// ----------------------------------------------------------
describe('calculateTotal - Discount Logic', () => {
  test('TC-07: should calculate discount amount correctly', () => {
    const items = [{ name: 'Pizza', price: 500, qty: 1 }];
    const result = calculateTotal(items, 20);
    expect(result.discount).toBe(100);   // 20% of 500
  });

  test('TC-08: should throw error for invalid discount', () => {
    const items = [{ name: 'Pizza', price: 500, qty: 1 }];
    expect(() => calculateTotal(items, -10)).toThrow('Invalid discount percentage');
    expect(() => calculateTotal(items, 110)).toThrow('Invalid discount percentage');
  });

  // ===================================================
  //  THIS TEST CATCHES THE BUG!
  //  The discount is calculated but never subtracted
  //  from the total. Expected: 425, Actual: 525
  // ===================================================
  test('TC-09: BUG CATCHER - total should subtract discount', () => {
    const items = [{ name: 'Pizza', price: 500, qty: 1 }];
    const result = calculateTotal(items, 20);
    // subtotal=500, tax=25 (5%), discount=100 (20%)
    // Expected total = 500 + 25 - 100 = 425
    expect(result.total).toBe(425);
  });

  test('TC-10: should not discount when percentage is 0', () => {
    const items = [{ name: 'Pizza', price: 500, qty: 1 }];
    const result = calculateTotal(items, 0);
    expect(result.discount).toBe(0);
    expect(result.total).toBe(525);      // 500 + 25 tax
  });
});

// ----------------------------------------------------------
// TC-11 to TC-13: Edge Cases
// ----------------------------------------------------------
describe('calculateTotal - Edge Cases', () => {
  test('TC-11: should handle very large order (100 items)', () => {
    const items = Array.from({ length: 100 }, (_, i) => ({
      name: `Item ${i}`,
      price: 100,
      qty: 1,
    }));
    const result = calculateTotal(items);
    expect(result.subtotal).toBe(10000);
    expect(result.total).toBe(10500);    // 10000 + 500 tax
  });

  test('TC-12: should handle zero-price items', () => {
    const items = [{ name: 'Free Sample', price: 0, qty: 5 }];
    const result = calculateTotal(items);
    expect(result.total).toBe(0);
  });

  test('TC-13: should handle quantity of zero', () => {
    const items = [{ name: 'Pizza', price: 299, qty: 0 }];
    const result = calculateTotal(items);
    expect(result.subtotal).toBe(0);
  });
});

// ----------------------------------------------------------
// Order Validation Tests
// ----------------------------------------------------------
describe('validateOrder', () => {
  test('should return valid for complete order', () => {
    const order = {
      customerId: 'C1',
      restaurantId: 'R1',
      items: [{ name: 'Pizza', price: 299, qty: 1 }],
    };
    expect(validateOrder(order)).toEqual({ valid: true });
  });

  test('should reject order without customer ID', () => {
    const order = { customerId: '', restaurantId: 'R1', items: [{}] };
    expect(validateOrder(order)).toEqual({ valid: false, error: 'Customer ID is required' });
  });

  test('should reject order with empty cart', () => {
    const order = { customerId: 'C1', restaurantId: 'R1', items: [] };
    expect(validateOrder(order)).toEqual({ valid: false, error: 'Cart is empty' });
  });
});
