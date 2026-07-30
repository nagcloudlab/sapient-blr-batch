# Module 02 Checklist -- Participant Submission

## Bug Fixes

- [ ] Bug #1: Navbar toggler works on mobile (hamburger opens/closes menu)
- [ ] Bug #2: All restaurant cards are equal height in each row
- [ ] Bug #3: Menu modal closes with both X button and Close button
- [ ] Bug #4: Cuisine filter pills stay above cards on tablet view
- [ ] Bug #9: Hero carousel auto-advances every 4 seconds
- [ ] Bug #10: FAQ accordion collapses previous answer when opening a new one

## Enhancements & Performance

- [ ] Bug #5: Only one Bootstrap JS bundle loaded (check DevTools > Network)
- [ ] Bug #6: At least 3 restaurants show "Free Delivery" green badge
- [ ] Bug #7: Footer stays at bottom on pages with little content
- [ ] Bug #8: Restaurant grid shows 2 columns on tablet (768px)

## Testing

- [ ] Tested on Mobile view (375px) -- navbar, cards stack to 1 column
- [ ] Tested on Tablet view (768px) -- cards show 2 columns, filter visible
- [ ] Tested on Desktop view (1200px+) -- cards show 3 columns, full layout
- [ ] Tested modal open/close cycle (open, add item, close, reopen)
- [ ] Tested carousel manual controls (prev/next buttons still work)

## Documentation

- [ ] Brief notes written: per bug, what was wrong and which Bootstrap concept
- [ ] Notes include the Bootstrap 4 vs 5 migration difference (data-* vs data-bs-*)

## Self-Check Questions

1. What is the difference between `bootstrap.min.js` and `bootstrap.bundle.min.js`?
2. Name the 6 Bootstrap breakpoints (xs, sm, md, lg, xl, xxl) and their pixel values.
3. Why does Bootstrap 5 use `data-bs-*` instead of `data-*`?
4. How does the flexbox sticky footer pattern work?
5. What does `data-bs-parent` do in an accordion?
