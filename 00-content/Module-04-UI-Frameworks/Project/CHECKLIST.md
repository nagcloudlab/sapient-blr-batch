# Module 04 Checklist -- Participant Submission

## Bug Fixes
- [ ] Bug #1: Rapid quantity clicks increment correctly (no stale values)
- [ ] Bug #2: Search filter returns correct results and debounces input
- [ ] Bug #3: useEffect runs only once on mount (no infinite loop)
- [ ] Bug #4: PriceTag component updates when parent price prop changes

## Enhancements
- [ ] Search input is debounced with useEffect cleanup
- [ ] Loading spinner displays while menu data is fetched
- [ ] Cart summary sidebar shows total items and total price

## Debugging Evidence
- [ ] Screenshot of React DevTools showing the stale state or infinite loop
- [ ] Brief description of how you traced the bug

## Self-Check Questions
1. What is the difference between `useState(value)` and `setState(prev => ...)` updater form?
2. Why does an empty dependency array `[]` mean "run once on mount"?
3. When should you return a cleanup function from useEffect?
4. Why is copying a prop into local state usually a mistake?
5. What is "lifting state up" and when do you need it?
