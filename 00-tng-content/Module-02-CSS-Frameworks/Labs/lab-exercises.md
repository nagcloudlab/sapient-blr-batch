# Module 02: CSS Frameworks -- Fix the Issues

## Lab Overview

You've been assigned to the FoodExpress sustain team. The frontend was recently migrated from custom CSS to Bootstrap 5, but the dev team left several Bootstrap integration bugs. The client reports:

> "The mobile menu doesn't open, some cards look different heights, and that modal is impossible to close. Also the FAQ section is broken -- clicking one answer should close the others. Please fix ASAP."

Your job: find and fix all 10 issues in the FoodExpress frontend.

---

## Setup

1. Open `starter-code/frontend/index.html` in your browser
2. Open Chrome DevTools (F12)
3. Test on mobile view (Toggle Device Toolbar) to see bugs #1, #4, #8

---

## Bug List

### Bug #1: Navbar Toggler Broken on Mobile
- **Where to look:** `index.html` -- the `<nav>` section, specifically the toggler `<button>`
- **Symptom:** On mobile (< 992px), clicking the hamburger icon does nothing
- **Hint:** Compare the toggler button with Bootstrap 5 navbar documentation. What data attributes are needed?
- **Impact:** Mobile users cannot navigate the site at all
- **Category:** Bootstrap 5 component -- Navbar

### Bug #2: Inconsistent Card Heights
- **Where to look:** `index.html` -- the restaurant card `<div class="card">` elements
- **Symptom:** Restaurant cards have different heights; buttons aren't aligned at bottom
- **Hint:** Bootstrap has a utility class that makes cards equal height within a row. Check the card documentation.
- **Impact:** Messy visual layout, unprofessional appearance
- **Category:** Bootstrap 5 utility -- Card layout

### Bug #3: Menu Modal Won't Close
- **Where to look:** `index.html` -- the `#menuModal` close buttons (there are 2)
- **Symptom:** Clicking the X button or "Close" button doesn't dismiss the modal
- **Hint:** Bootstrap 5 changed its data attribute prefix. The old version used `data-dismiss`, the new version uses...?
- **Impact:** Users are stuck in the modal and must reload the page
- **Category:** Bootstrap 5 migration -- data attributes

### Bug #4: Filter Pills Disappear Behind Cards on Tablet
- **Where to look:** `css/style.css` -- the `.nav-pills` rule
- **Symptom:** On tablet view, when scrolling, cuisine filter pills go behind the restaurant cards
- **Hint:** Check the z-index value. Is it high enough to stay above card hover effects?
- **Impact:** Users can't switch cuisines on tablet devices
- **Category:** CSS z-index stacking context

### Bug #5: Duplicate JavaScript Loading (Performance)
- **Where to look:** `index.html` -- the `<script>` tags at the bottom of the file
- **Symptom:** Page loads unnecessary extra JavaScript (Popper.js loaded twice)
- **Hint:** `bootstrap.bundle.min.js` already includes Popper.js. What's being loaded separately?
- **Impact:** ~25KB extra download, potential conflicts, slower page load
- **Category:** Bootstrap bundle optimization

### Bug #6: Missing "Free Delivery" Badge
- **Where to look:** `index.html` -- restaurant cards that qualify (most restaurants)
- **Symptom:** Restaurants offering free delivery (orders > $25) don't show any badge
- **Hint:** The CSS class `.free-delivery-badge` already exists in `style.css`. The card needs `position: relative` and a `<span>` element.
- **Impact:** Users don't know about the free delivery promotion
- **Category:** Bootstrap badges + CSS positioning

### Bug #7: Footer Not Sticky on Short Pages
- **Where to look:** `index.html` -- the `<footer>` element and the `<body>` tag
- **Symptom:** If you remove some restaurant cards, the footer floats in the middle of the page
- **Hint:** Bootstrap's flex utilities can push the footer to the bottom. The body needs `d-flex flex-column min-vh-100` and the footer needs `mt-auto`.
- **Impact:** Unprofessional layout on pages with little content
- **Category:** Bootstrap flex utilities -- sticky footer pattern

### Bug #8: No Tablet Breakpoint for Restaurant Grid
- **Where to look:** `index.html` -- the `col-md-4` classes on restaurant card columns
- **Symptom:** Grid jumps from 3 columns (desktop) to 1 column (mobile) with no 2-column tablet step
- **Hint:** Bootstrap's grid system has breakpoints: col-sm, col-md, col-lg, col-xl. Which class gives 2 columns on tablet?
- **Impact:** Awkward layout on tablets -- too few items visible
- **Category:** Bootstrap grid system -- responsive breakpoints

### Bug #9: Carousel Doesn't Auto-Advance
- **Where to look:** `index.html` -- the `#heroCarousel` element
- **Symptom:** The hero carousel sits on the first slide and never advances automatically
- **Hint:** Bootstrap carousel needs a specific attribute to enable automatic cycling. Check the carousel docs.
- **Impact:** Promotional slides never shown, missed marketing
- **Category:** Bootstrap 5 component -- Carousel

### Bug #10: FAQ Accordion Doesn't Collapse Others
- **Where to look:** `index.html` -- the `#faqAccordion` section, specifically `data-bs-parent` attributes
- **Symptom:** Opening one FAQ item doesn't close the others -- all stay open simultaneously
- **Hint:** The `data-bs-parent` attribute controls this behavior. Does it reference the correct element ID?
- **Impact:** FAQ section becomes a long wall of text, hard to scan
- **Category:** Bootstrap 5 component -- Accordion

---

## Checkpoints

After fixing all bugs, verify:

1. [ ] **Mobile nav:** Hamburger icon opens/closes the nav menu on mobile
2. [ ] **Card heights:** All restaurant cards in a row are the same height
3. [ ] **Modal close:** Both X button and Close button dismiss the menu modal
4. [ ] **Filter z-index:** Cuisine pills stay above cards when scrolling on tablet
5. [ ] **No duplicate JS:** Only one Bootstrap JS file loaded (check Network tab)
6. [ ] **Free Delivery badges:** At least 3 restaurants show the green badge
7. [ ] **Sticky footer:** Footer stays at bottom even on short-content pages
8. [ ] **Tablet grid:** 2 columns on tablet (768px-991px), 3 on desktop, 1 on mobile
9. [ ] **Carousel auto-play:** Hero slides advance automatically every 4 seconds
10. [ ] **Accordion:** Only one FAQ answer is open at a time

---

## Bonus Challenges

1. **Toast notification:** When a user adds an item to cart, show a Bootstrap Toast notification (top-right corner) confirming the item was added.

2. **Tooltip on ratings:** Add a Bootstrap Tooltip on the star rating badges that says "Based on X reviews."

3. **Dark mode toggle:** Add a button in the navbar that toggles Bootstrap's dark mode (`data-bs-theme="dark"` on `<html>`).
