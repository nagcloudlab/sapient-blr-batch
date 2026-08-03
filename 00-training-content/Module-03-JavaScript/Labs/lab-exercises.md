# Module 03: JavaScript (Part 1) -- Fix the Issues

## Lab Overview

The FoodExpress frontend now has interactive JavaScript for cart management, cuisine filtering, and checkout. But the dev team left several bugs.

> "Hi Team, customers are reporting: items duplicate in the cart instead of increasing quantity, the total shows NaN when they use a discount code, and the checkout form lets them submit with empty fields. Also the cuisine filter crashes the page. Please fix urgently."

---

## Setup

1. Open `starter-code/frontend/index.html` in Chrome
2. Open DevTools (F12) -- you will use Console, Sources, and Network panels
3. Try adding the same item to cart twice -- notice the duplicate
4. Try applying discount code "SAVE10" -- notice NaN total
5. Try clicking a cuisine filter pill -- notice the page crashes

---

## Bug List

### Bug #1: Cart Creates Duplicate Items
- **Where:** `js/app.js` -- `addToCart()` function
- **Symptom:** Adding the same burger twice creates two separate entries instead of incrementing quantity
- **Hint:** The function always pushes a new object. It should first check if the item already exists using `find()`
- **Debug:** Set a breakpoint on line with `cart.push()`. Add the same item twice. Watch the cart array grow with duplicates.

### Bug #2: Cart Total Shows NaN
- **Where:** `js/app.js` -- `getCartTotal()` function
- **Symptom:** Applying discount code "SAVE10" makes the total show "NaN"
- **Hint:** Two bugs: (1) `price + quantity` should be `price * quantity`. (2) The discount subtracts the code string instead of a number.
- **Debug:** Set a breakpoint in `getCartTotal()`. Step through. Watch the `total` variable. When does it become NaN?

### Bug #3: Checkout Form Submits Without Validation
- **Where:** `js/app.js` -- `handleCheckout()` function
- **Symptom:** Form reloads the page with empty fields accepted
- **Hint:** Missing `e.preventDefault()` and no field validation logic
- **Fix:** Add preventDefault, check each field, show error messages

### Bug #4: Cuisine Filter Destroys the Page
- **Where:** `js/app.js` -- `filterByCuisine()` function
- **Symptom:** Clicking any cuisine filter pill blanks the entire page
- **Hint:** The function uses `document.body.innerHTML = ''` and `location.reload()`. It should only hide/show cards in `#restaurant-grid`.
- **Fix:** Use `querySelectorAll` on the grid cards, check cuisine text, toggle `display: none`

### Enhancement #5: Disable Closed Restaurant Buttons
- **Where:** `js/app.js` -- DOMContentLoaded listener
- **Hint:** Find cards with "Closed" text and add `disabled` class to their button

### Enhancement #6: Update Cart Badge Count
- **Where:** `js/app.js` -- `updateCartDisplay()` function
- **Hint:** The `#cart-count` element should show total quantity across all items

---

## Checkpoints

1. [ ] Adding same item twice: quantity increments (not duplicated)
2. [ ] Cart total calculates correctly (price * quantity)
3. [ ] Discount code "SAVE10" applies 10% discount (no NaN)
4. [ ] Cuisine filter shows/hides cards (no page crash)
5. [ ] Checkout form validates name, phone, address
6. [ ] Error messages appear next to invalid fields
7. [ ] Closed restaurants have disabled buttons
8. [ ] Cart badge shows correct item count

## Bonus Challenges

1. Add quantity +/- buttons to each cart item
2. Show a toast notification when item is added to cart
3. Add a "Clear Cart" button that removes all items
4. Add a search input that filters restaurants by name in real-time (debounced)
