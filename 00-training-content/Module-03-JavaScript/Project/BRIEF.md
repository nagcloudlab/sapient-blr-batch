# Module 03: JavaScript (Part 1) -- Cart and Checkout Bugs

## Sustain Context

The client escalated:

> "The mobile layout and Bootstrap fixes look great. But we have critical functional issues now. Customers are complaining: the cart is broken (items duplicate, totals wrong), the cuisine filter crashes the page, and the checkout accepts empty forms. This is blocking real orders. Priority 1."

---

## Tasks

| # | Type | Issue | File |
|---|------|-------|------|
| 1 | BUG | Add to cart creates duplicates instead of incrementing | `js/app.js` |
| 2 | BUG | Cart total shows NaN when discount applied | `js/app.js` |
| 3 | BUG | Checkout form submits with empty fields | `js/app.js` |
| 4 | BUG | Cuisine filter destroys entire page | `js/app.js` |
| 5 | ENH | Disable buttons for closed restaurants | `js/app.js` |
| 6 | ENH | Cart badge count in navbar | `js/app.js` |
| 7 | ENH | Field-level error messages on checkout | `js/app.js` |
| 8 | DEBUG | Trace the NaN bug using DevTools breakpoints | DevTools |

## Deliverables

- [ ] All 4 bugs fixed, 3 enhancements added
- [ ] At least one bug traced with DevTools breakpoints (screenshot)
- [ ] Brief notes: root cause and fix for each bug
