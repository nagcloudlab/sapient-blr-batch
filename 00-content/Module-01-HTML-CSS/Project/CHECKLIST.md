# Module 01 Checklist -- Participant Submission

## Bug Fixes

- [ ] Bug #1: Restaurant grid shows 2 columns on tablet (768px)
- [ ] Bug #2: Cart sidebar doesn't overlap on mobile -- stacks below restaurants
- [ ] Bug #3: Cart total text aligned properly at all screen sizes
- [ ] Bug #4: Images have lazy loading (check Network tab -- images load on scroll)

## Enhancements

- [ ] ENH #5: At least 3 restaurants show a "Free Delivery" green badge
- [ ] ENH #6: Footer is sticky at bottom, shows support email and phone
- [ ] ENH #7: "Back to Top" button appears when scrolled down, scrolls to top on click
- [ ] Bug #8: Checkout form buttons align correctly on mobile and Safari

## Testing

- [ ] Tested on Mobile (375px): cart stacks below, cards 1 column
- [ ] Tested on Tablet (768px): cards 2 columns, cart visible
- [ ] Tested on Desktop (1200px+): cards 3 columns, cart sidebar sticky
- [ ] Tested checkout.html on at least 2 screen sizes

## Documentation

- [ ] Screenshots saved: before and after for at least 3 fixes
- [ ] Brief notes written: what was wrong + how you fixed it (per bug)

## Self-Check Questions

1. Can you explain what `col-sm-6 col-md-4` means in Bootstrap's grid system?
2. What's the difference between `position: fixed`, `position: sticky`, and `position: relative`?
3. Why does `loading="lazy"` improve page performance?
4. How does the flexbox sticky footer pattern work? (body flex-column + footer mt-auto)
5. Why does a positioned child element need `position: relative` on its parent for absolute positioning to work?
