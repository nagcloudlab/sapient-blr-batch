# Module 01: HTML & CSS -- Frontend Layout Issues

## Sustain Context

Today is Day 1. Welcome to the FoodExpress sustain engineering team.

The dev team built FoodExpress and handed it over to you. They moved on to another project. Your team is now responsible for keeping it running, fixing bugs, and making improvements.

This morning, the client sent this email:

> "Hi Team, we launched FoodExpress last week and it looks great on desktop. But we're getting a flood of complaints from mobile and tablet users:
>
> 1. Restaurant cards look terrible on tablets -- they're either too wide or too narrow
> 2. The cart sidebar covers the restaurant list on phones -- users can't browse
> 3. Images take forever to load on mobile (data-conscious users are complaining)
> 4. The checkout page buttons look broken on Safari
>
> Also, our marketing team wants two small additions before we run ads next week:
> - A 'Free Delivery' badge on qualifying restaurants
> - A footer with support contact info that stays at the bottom
> - A 'Back to Top' button for users who scroll past many restaurants
>
> Can you fix these ASAP? We have a marketing push starting Monday."

---

## Your Tasks

### Day 1 (Morning) -- Bug Fixes

| # | Type | Issue | File(s) to check |
|---|------|-------|-------------------|
| 1 | BUG | Restaurant grid breaks on tablet (items stack wrong below 768px) | `index.html`, `css/style.css` |
| 2 | BUG | Cart sidebar overlaps restaurant list on mobile screens | `index.html`, `css/style.css` |
| 3 | BUG | Cart total text doesn't align properly on small screens | `css/style.css` |
| 4 | PERF | Restaurant images load slowly -- no lazy loading | `index.html` |

### Day 1 (Afternoon) -- Enhancements

| # | Type | Issue | File(s) to check |
|---|------|-------|-------------------|
| 5 | ENH | Add a "Free Delivery" badge on restaurants that qualify | `index.html`, `css/style.css` |
| 6 | ENH | Add a sticky footer with support email and phone | `index.html`, `css/style.css` |
| 7 | ENH | Add a "Back to Top" button (visible when scrolled down) | `index.html`, `css/style.css`, `js/cart.js` |
| 8 | BUG | Checkout form fields misaligned on Safari and mobile | `checkout.html`, `css/style.css` |

---

## Code Files

You receive the FoodExpress frontend -- this is the code the dev team wrote. It works on desktop but has issues on other devices.

Files:
- `frontend/index.html` -- Main homepage with restaurant listing
- `frontend/checkout.html` -- Checkout page
- `frontend/css/style.css` -- Stylesheet (bugs are here)
- `frontend/js/cart.js` -- Basic cart JS (minimal for this module)

---

## How to Run

1. Open `frontend/index.html` in Chrome
2. Press F12 to open DevTools
3. Click the device toolbar icon to test mobile/tablet views
4. Test at: 375px (phone), 768px (tablet), 1200px (desktop)

---

## Deliverables

By end of Day 1:
- [ ] All 4 bugs fixed
- [ ] All 3 enhancements added (badge, footer, back-to-top)
- [ ] Checkout form alignment fixed
- [ ] Page looks correct on mobile (< 576px), tablet (768px), and desktop (1200px+)
- [ ] Screenshots: before and after for at least 3 fixes (save in a `screenshots/` folder)
- [ ] Brief notes: what was wrong and how you fixed it (2-3 lines per bug)
