# Module 04 Solutions -- TRAINER ONLY

## Bug #1: Stale State on Quantity Increment

**Root Cause:** The `setQuantity(quantity + 1)` inside an event handler captures the stale closure value of `quantity`. Rapid clicks queue multiple updates that all read the same stale value.

**Fix:**
```jsx
// Before
const handleIncrement = () => {
  setQuantity(quantity + 1);
};

// After -- use functional updater
const handleIncrement = () => {
  setQuantity(prev => prev + 1);
};
```

## Bug #2: Search Shows Stale Results

**Root Cause:** The filter function uses a stale `searchTerm` captured in a `setTimeout` callback. The timeout is never cleared, so previous searches still fire.

**Fix:**
```jsx
// Before
const handleSearch = (e) => {
  setTimeout(() => {
    setFilteredItems(items.filter(i => i.name.includes(searchTerm)));
  }, 300);
};

// After -- useEffect with cleanup
useEffect(() => {
  const timer = setTimeout(() => {
    setFilteredItems(items.filter(i =>
      i.name.toLowerCase().includes(searchTerm.toLowerCase())
    ));
  }, 300);
  return () => clearTimeout(timer);
}, [searchTerm, items]);
```

## Bug #3: useEffect Infinite Loop

**Root Cause:** `useEffect` calls `setMenuItems(data)` without a dependency array, causing a re-render on every state update, which triggers the effect again.

**Fix:**
```jsx
// Before
useEffect(() => {
  fetch('/api/menu').then(r => r.json()).then(data => setMenuItems(data));
}); // missing dependency array

// After
useEffect(() => {
  fetch('/api/menu').then(r => r.json()).then(data => setMenuItems(data));
}, []); // empty array = run once on mount
```

## Bug #4: Child Does Not Re-render on Prop Change

**Root Cause:** `PriceTag` stores the `price` prop in local state during mount and never updates when the prop changes.

**Fix:**
```jsx
// Before
const PriceTag = ({ price }) => {
  const [displayPrice] = useState(price); // copies prop once, never updates
  return <span>{displayPrice}</span>;
};

// After -- use prop directly (no local copy)
const PriceTag = ({ price }) => {
  return <span>{price}</span>;
};

// Or if local state is needed, sync with useEffect:
useEffect(() => { setDisplayPrice(price); }, [price]);
```

## Hints

| Bug | Level 1 | Level 2 |
|-----|---------|---------|
| #1 | "Click the + button 5 times fast. How many increments happen?" | "Use the functional updater form: `setQuantity(prev => prev + 1)`" |
| #2 | "Add a console.log inside the setTimeout. Which value of searchTerm does it see?" | "Clear the timeout on cleanup. Use useEffect with searchTerm as a dependency." |
| #3 | "Open React DevTools Profiler. How many renders happen in 1 second?" | "Add `[]` as the second argument to useEffect for mount-only execution." |
| #4 | "Change the price in parent. Does PriceTag update? Why not?" | "Don't copy props into state. Use the prop directly, or sync with useEffect." |
