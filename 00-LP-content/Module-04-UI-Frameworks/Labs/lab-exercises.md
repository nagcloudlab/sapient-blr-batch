# Module 04: UI Frameworks (React) -- Fix the Issues

## Lab Overview

The FoodExpress frontend has been migrated to React. The new components render the menu, handle search filtering, and manage cart state. But the migration introduced several bugs.

> "Hi Team, the React migration is causing problems. Customers click the + button and the quantity jumps unpredictably, the search shows wrong results, the menu page freezes after load, and the price tag never updates when we run promotions. Please investigate and fix."

---

## Setup

1. Open `starter-code/foodexpress-react/` in VS Code
2. Run `npm install` then `npm start`
3. Open the app in Chrome and open React DevTools (Components + Profiler tabs)
4. Try clicking the + button on any menu item 5 times fast -- notice the quantity is wrong
5. Try typing in the search box -- notice stale/wrong results
6. Watch the console -- notice the useEffect firing repeatedly

---

## Bug List

### Bug #1: Quantity Shows Stale Value
- **Where:** `src/components/MenuCard.jsx` -- `handleIncrement()` function
- **Symptom:** Clicking + five times fast only increments by 1 or 2 instead of 5
- **Hint:** The state updater captures a stale closure. Use the functional updater form `prev => prev + 1`
- **Debug:** Add `console.log(quantity)` inside handleIncrement. Click 5 times fast. Notice all logs show the same value.

### Bug #2: Search Filter Shows Stale Results
- **Where:** `src/components/RestaurantList.jsx` -- `handleSearch()` function
- **Symptom:** Typing "Pizza" in the search box shows results for previous keystrokes
- **Hint:** The setTimeout callback captures the old `searchTerm`. There is no cleanup to cancel previous timeouts.
- **Debug:** Type "Pi" then immediately "zza". Check which filter value actually runs.

### Bug #3: useEffect Infinite Loop
- **Where:** `src/components/MenuCard.jsx` -- useEffect for fetching data
- **Symptom:** Page freezes or console fills with repeated fetch requests
- **Hint:** The useEffect has no dependency array, so it runs after every render. Each run sets state, which triggers another render.
- **Fix:** Add an empty dependency array `[]` so it runs once on mount

### Bug #4: PriceTag Does Not Update
- **Where:** `src/components/PriceTag.jsx`
- **Symptom:** When parent component changes the price prop (e.g., during a promotion), PriceTag still shows the old price
- **Hint:** The component copies the `price` prop into local state with `useState(price)` on mount and never syncs again
- **Fix:** Use the prop directly instead of copying it into state

### Enhancement #5: Debounced Search with Cleanup
- **Where:** `src/components/RestaurantList.jsx`
- **Hint:** Move the search logic into a useEffect with `searchTerm` as a dependency. Return a cleanup function that clears the timeout.

### Enhancement #6: Loading Spinner
- **Where:** `src/components/MenuCard.jsx`
- **Hint:** Add a `loading` state. Set it to `true` before fetch, `false` after. Conditionally render a spinner.

---

## Checkpoints

1. [ ] Clicking + five times fast increments quantity to 5
2. [ ] Search for "Pizza" returns only pizza items (no stale results)
3. [ ] Page loads without freezing; fetch fires only once
4. [ ] Changing price prop in parent updates PriceTag immediately
5. [ ] Search is debounced (no filter on every keystroke)
6. [ ] Loading spinner appears while data is being fetched
7. [ ] Cart summary shows correct total items and price

## Bonus Challenges

1. Add a `useReducer` to manage cart state instead of multiple `useState` calls
2. Memoize the filtered list with `useMemo` to avoid recalculating on every render
3. Create a custom hook `useDebounce(value, delay)` and reuse it for search
4. Add animated transitions when menu items appear/disappear during filtering
