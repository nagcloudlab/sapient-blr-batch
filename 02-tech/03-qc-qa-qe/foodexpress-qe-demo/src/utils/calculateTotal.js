// FoodExpress: Order total calculation
// Calculates subtotal, tax, discount, and final total

const TAX_RATE = 0.05; // 5% GST

/**
 * Calculate the total for a FoodExpress order
 * @param {Array} items - Array of { name, price, qty }
 * @param {number} discountPercent - Discount percentage (0-100)
 * @returns {{ subtotal, tax, discount, total }}
 */
export function calculateTotal(items, discountPercent = 0) {
  if (!Array.isArray(items)) {
    throw new Error('Items must be an array');
  }

  for (const item of items) {
    if (item.qty < 0) {
      throw new Error('Invalid quantity');
    }
    if (item.price < 0) {
      throw new Error('Invalid price');
    }
  }

  if (discountPercent < 0 || discountPercent > 100) {
    throw new Error('Invalid discount percentage');
  }

  // Calculate subtotal
  const subtotal = items.reduce((sum, item) => sum + item.price * item.qty, 0);

  // Calculate tax on subtotal
  const tax = Math.round(subtotal * TAX_RATE);

  // Calculate discount amount
  const discount = Math.round(subtotal * (discountPercent / 100));

  // ============================================================
  //  BUG: discount is calculated above but NOT subtracted below!
  //  The correct line should be: const total = subtotal + tax - discount;
  // ============================================================
  const total = subtotal + tax;

  return { subtotal, tax, discount, total };
}

/**
 * Validate an order before submission
 * @param {{ customerId, restaurantId, items }} order
 * @returns {{ valid: boolean, error?: string }}
 */
export function validateOrder(order) {
  if (!order.customerId) {
    return { valid: false, error: 'Customer ID is required' };
  }
  if (!order.restaurantId) {
    return { valid: false, error: 'Restaurant ID is required' };
  }
  if (!order.items || order.items.length === 0) {
    return { valid: false, error: 'Cart is empty' };
  }
  return { valid: true };
}
