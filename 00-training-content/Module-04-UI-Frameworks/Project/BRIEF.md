# Module 04: UI Frameworks (React) -- Menu Card Component Bugs

## Sustain Context

The client escalated:

> "The cart and checkout fixes are solid -- orders are flowing again. But we just migrated the frontend to React and the new dev left it half-broken. The menu card doesn't update when you change quantity, the search filter lags and shows stale results, and the 'Add to Cart' button fires twice on every click. We need this stabilised before the weekend launch."

---

## Tasks

| # | Type | Issue | File |
|---|------|-------|------|
| 1 | BUG | Quantity increment shows stale value (stale state closure) | `src/components/MenuCard.jsx` |
| 2 | BUG | Search filter runs on every keystroke and shows stale results | `src/components/RestaurantList.jsx` |
| 3 | BUG | useEffect runs in infinite loop (missing dependency array) | `src/components/MenuCard.jsx` |
| 4 | BUG | Child component does not re-render when parent prop changes | `src/components/PriceTag.jsx` |
| 5 | ENH | Debounced search input using useEffect cleanup | `src/components/RestaurantList.jsx` |
| 6 | ENH | Loading spinner while menu data is being fetched | `src/components/MenuCard.jsx` |
| 7 | ENH | Cart summary sidebar using lifted state | `src/components/CartSummary.jsx` |
| 8 | DEBUG | Trace the stale state bug using React DevTools | React DevTools |

## Deliverables

- [ ] All 4 bugs fixed, 3 enhancements added
- [ ] At least one bug traced with React DevTools (screenshot)
- [ ] Brief notes: root cause and fix for each bug

## Capsule Project

Build a **FoodExpress Menu Card** React component from scratch:
- Fetches menu items from a mock JSON file
- Displays item name, image placeholder, price, and quantity selector
- "Add to Cart" updates a shared cart state (lifted to App)
- Cart summary component shows total items and total price
