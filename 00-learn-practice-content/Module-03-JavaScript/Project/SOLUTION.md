# Module 03 Solutions -- TRAINER ONLY

## Bug #1: Cart Duplicates Items

**Root Cause:** `addToCart()` always pushes a new object without checking if the item exists.

**Fix:**
```javascript
// Before
cart.push({ id, name, price, restaurant, quantity: 1 });

// After
const existing = cart.find(item => item.id === id);
if (existing) {
  existing.quantity += 1;
} else {
  cart.push({ id, name, price: parseFloat(price), restaurant, quantity: 1 });
}
```

## Bug #2: NaN Total

**Root Cause:** Two issues:
1. `total + item.price + item.quantity` should be `total + item.price * item.quantity`
2. `discountCode` stores the string "SAVE10", and `total - "SAVE10"` = NaN

**Fix:**
```javascript
total += item.price * item.quantity;  // multiplication, not addition
// Store numeric discount: discountValue = validCodes[code]; // e.g., 10
total = total * (1 - discountValue / 100);  // apply percentage
```

## Bug #3: Form Submits Without Validation

**Root Cause:** Missing `e.preventDefault()` and no validation logic.

**Fix:** Add `e.preventDefault()`, check required fields, show errors using Bootstrap's `is-invalid` class.

## Bug #4: Filter Destroys Page

**Root Cause:** `document.body.innerHTML = ''` clears everything. `location.reload()` resets state.

**Fix:** Use `querySelectorAll('#restaurant-grid > div')` and toggle `display: none` per card based on cuisine text match.

## Hints

| Bug | Level 1 | Level 2 |
|-----|---------|---------|
| #1 | "Check if the item exists before pushing" | "Use `cart.find(item => item.id === id)`" |
| #2 | "Set a breakpoint in getCartTotal. When does NaN appear?" | "price + quantity is wrong. And the discount is a string." |
| #3 | "What does e.preventDefault() do?" | "Check required fields, push errors to an array" |
| #4 | "Should filtering clear the entire body?" | "Use querySelectorAll on just the grid, toggle display:none" |
