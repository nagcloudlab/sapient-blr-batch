# Module 03: JavaScript Part 1 -- Lab Setup

## Prerequisites

- Google Chrome (latest)
- Visual Studio Code (or any text editor)
- No build tools required

## Running the Starter Code

1. Navigate to `Labs/starter-code/frontend/`.
2. Open `index.html` in Chrome.
3. The page runs plain JavaScript -- no bundler or Node.js needed.

## Verifying Your Fixes

1. Open Chrome DevTools (`F12`) and go to the Console tab before interacting with the page.
2. Test the cart workflow:
   - Click "Add to Cart" on a menu item -- the cart count should increment.
   - Change quantity in the cart -- the subtotal should recalculate.
   - Click "Checkout" -- the form validation should highlight empty required fields.
3. Each bug in `lab-exercises.md` has a specific interaction that triggers it; follow those steps.
4. Confirm no uncaught errors remain in the Console after all fixes.

## Expected Behavior

- "Add to Cart" button updates the cart item count in the header.
- Quantity changes recalculate the line total and order total correctly.
- Checkout form rejects submission when required fields are blank.
- Validation messages appear next to the relevant fields, not as browser `alert()` dialogs.
- Removing an item from the cart deletes its row and updates the total.

## Troubleshooting

**"Cannot read properties of null" error:** A DOM selector is targeting an element that does not exist;
check that the `id` or `class` name in the JS matches exactly what is in the HTML.

**Function not defined:** Ensure the `<script>` tag is at the bottom of `<body>` or uses the `defer`
attribute so the DOM is ready before the script runs.
