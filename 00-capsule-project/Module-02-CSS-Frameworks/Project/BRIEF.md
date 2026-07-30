# Module 02: CSS Frameworks -- Bootstrap Integration Issues

## Sustain Context

The FoodExpress frontend was recently migrated from a custom CSS setup to Bootstrap 5 by the development team. They delivered and moved on to another project. This morning, the client sent this email:

> "Hi Team, the Bootstrap migration has several issues. The mobile hamburger menu doesn't work at all -- our mobile users (40% of traffic) can't navigate. The restaurant cards look messy with different heights. The menu modal is impossible to close without reloading. The FAQ section where all answers open at once is confusing. Also, we paid for a hero carousel and it just sits on one slide. Can your sustain team fix these before our marketing push tomorrow? Thanks."

You are the sustain engineering team. Fix these issues.

---

## Your Tasks

### Priority 1 -- Critical (Fix Today)

| # | Type | Issue | File(s) to check |
|---|------|-------|-------------------|
| 1 | BUG | Navbar toggler doesn't work on mobile (hamburger icon dead) | `index.html` |
| 3 | BUG | Menu modal can't be closed (users stuck) | `index.html` |
| 9 | BUG | Hero carousel doesn't auto-advance (marketing issue) | `index.html` |

### Priority 2 -- Visual/UX (Fix Today)

| # | Type | Issue | File(s) to check |
|---|------|-------|-------------------|
| 2 | BUG | Restaurant cards have inconsistent heights | `index.html` |
| 4 | BUG | Cuisine filter pills go behind cards on tablet | `css/style.css` |
| 8 | BUG | No tablet breakpoint -- cards jump from 3-col to 1-col | `index.html` |
| 10 | BUG | FAQ accordion doesn't collapse other items | `index.html` |

### Priority 3 -- Enhancement & Performance

| # | Type | Issue | File(s) to check |
|---|------|-------|-------------------|
| 5 | PERF | Duplicate Popper.js loading (extra 25KB) | `index.html` |
| 6 | ENH | Add "Free Delivery" badges on qualifying restaurants | `index.html` |
| 7 | ENH | Footer not sticky on short-content pages | `index.html`, `css/style.css` |

---

## Code Files

You receive the FoodExpress frontend with Module 01 (HTML/CSS) fixes already applied:
- Responsive layout working
- Lazy loading on images
- Proper footer with contact info

New issues are all related to **Bootstrap 5 component integration**.

---

## Deliverables

By end of Day 2:
- [ ] All 7 bugs fixed
- [ ] All 3 enhancements/perf improvements done
- [ ] Page tested on: Mobile (375px), Tablet (768px), Desktop (1200px+)
- [ ] Screenshots: before and after for the modal fix and navbar fix
- [ ] Brief notes: for each fix, what was wrong and what Bootstrap concept it relates to
