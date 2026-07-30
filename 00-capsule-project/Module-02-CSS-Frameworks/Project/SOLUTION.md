# Module 02 Solutions -- TRAINER ONLY

## Bug #1: Navbar Toggler Broken on Mobile

**Root Cause:** The toggler `<button>` is missing `data-bs-toggle="collapse"` and `data-bs-target="#navMenu"`. Without these Bootstrap 5 data attributes, the collapse plugin doesn't know what to toggle.

**Fix:** Add the attributes to the toggler button:
```html
<!-- Before -->
<button class="navbar-toggler" type="button">

<!-- After -->
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu"
        aria-controls="navMenu" aria-expanded="false" aria-label="Toggle navigation">
```

**Key concept:** Bootstrap 5 uses `data-bs-*` prefix (not `data-*` like Bootstrap 4).

---

## Bug #2: Inconsistent Card Heights

**Root Cause:** The `<div class="card">` elements are missing the `h-100` class, so each card is only as tall as its content.

**Fix:** Add `h-100` to each card:
```html
<!-- Before -->
<div class="card">

<!-- After -->
<div class="card h-100">
```

**Key concept:** Bootstrap's `h-100` utility makes elements 100% height of their parent, which within a row creates equal-height cards.

---

## Bug #3: Modal Won't Close

**Root Cause:** The close buttons use Bootstrap 4 syntax `data-dismiss="modal"` instead of Bootstrap 5 syntax `data-bs-dismiss="modal"`.

**Fix:** Update both close buttons in the modal:
```html
<!-- Before (Bootstrap 4 syntax) -->
<button type="button" class="btn-close btn-close-white" data-dismiss="modal">
<button type="button" class="btn btn-secondary" data-dismiss="modal">

<!-- After (Bootstrap 5 syntax) -->
<button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal">
<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
```

**Key concept:** Bootstrap 5 migrated all data attributes from `data-*` to `data-bs-*` to avoid conflicts with other libraries.

---

## Bug #4: Filter Pills Behind Cards

**Root Cause:** `.nav-pills` has `z-index: 0` in CSS, which puts it below card hover effects.

**Fix:** In `style.css`, change:
```css
/* Before */
.nav-pills {
  position: relative;
  z-index: 0;
}

/* After */
.nav-pills {
  position: relative;
  z-index: 10;
}
```

**Key concept:** CSS stacking context -- elements with higher z-index appear on top.

---

## Bug #5: Duplicate Popper.js

**Root Cause:** `bootstrap.bundle.min.js` already includes Popper.js, but Popper is also loaded separately as a standalone script.

**Fix:** Remove the separate Popper.js script tag:
```html
<!-- Remove this line -->
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
```

**Key concept:** Bootstrap bundle = Bootstrap + Popper. No need to load Popper separately.

---

## Bug #6: Missing Free Delivery Badge

**Root Cause:** The `.free-delivery-badge` CSS class exists but no HTML elements use it. Cards also need `position: relative` for the absolute-positioned badge.

**Fix:** Add to qualifying restaurant cards:
```html
<div class="card h-100" style="position: relative;">
  <span class="free-delivery-badge"><i class="bi bi-truck"></i> Free Delivery</span>
  <img src="..." ...>
  ...
</div>
```

Add to Burger Barn, Pizza Palace, and Dragon Wok (restaurants likely to have orders > $25).

---

## Bug #7: Footer Not Sticky

**Root Cause:** The body doesn't use flex column layout and the footer doesn't have `mt-auto` to push itself to the bottom.

**Fix:**
1. Add to `<body>`: `class="d-flex flex-column min-vh-100"`
2. Add to `<footer>`: Replace `mt-5` with `mt-auto`

```html
<body class="d-flex flex-column min-vh-100">
  ...
  <footer class="bg-dark text-white py-4 mt-auto">
```

**Key concept:** Flexbox sticky footer pattern -- body is a flex column, footer uses margin-top auto.

---

## Bug #8: No Tablet Breakpoint

**Root Cause:** Cards use `col-md-4` only, jumping from 3 columns (>= 768px) to 1 column (< 768px).

**Fix:** Add `col-sm-6` to each restaurant card column:
```html
<!-- Before -->
<div class="col-md-4 mb-4">

<!-- After -->
<div class="col-sm-6 col-md-4 mb-4">
```

**Key concept:** Bootstrap breakpoints: sm (>= 576px), md (>= 768px), lg (>= 992px).

---

## Bug #9: Carousel Doesn't Auto-Advance

**Root Cause:** Missing `data-bs-ride="carousel"` on the carousel element. Without this, Bootstrap doesn't auto-cycle.

**Fix:**
```html
<!-- Before -->
<div id="heroCarousel" class="carousel slide" data-bs-interval="4000">

<!-- After -->
<div id="heroCarousel" class="carousel slide" data-bs-ride="carousel" data-bs-interval="4000">
```

**Key concept:** `data-bs-ride="carousel"` enables automatic cycling.

---

## Bug #10: Accordion Doesn't Collapse Others

**Root Cause:** The `data-bs-parent` attribute references `#faq-wrong-id` instead of the actual accordion ID `#faqAccordion`.

**Fix:**
```html
<!-- Before -->
<div id="faq1" class="accordion-collapse collapse show" data-bs-parent="#faq-wrong-id">

<!-- After -->
<div id="faq1" class="accordion-collapse collapse show" data-bs-parent="#faqAccordion">
```

Apply to all three FAQ items (faq1, faq2, faq3).

**Key concept:** `data-bs-parent` must reference the correct parent accordion ID for the auto-collapse behavior.

---

## Hints to Give (If Participants Are Stuck)

| Bug | Hint Level 1 | Hint Level 2 |
|-----|--------------|--------------|
| #1 | "Check Bootstrap 5 navbar docs -- what attributes does the toggler need?" | "data-bs-toggle and data-bs-target" |
| #2 | "Bootstrap has a height utility class that makes elements fill their parent" | "h-100 on the card element" |
| #3 | "Bootstrap 5 changed its data attribute prefix from Bootstrap 4" | "data-dismiss -> data-bs-dismiss" |
| #4 | "Inspect the nav-pills in DevTools. What's its z-index?" | "Change z-index from 0 to 10+" |
| #5 | "Check the Network tab -- how many JS files are loaded? Which seem redundant?" | "bootstrap.bundle.min.js already includes Popper" |
| #6 | "The CSS class already exists in style.css. What HTML do you need?" | "span with class free-delivery-badge inside a position:relative card" |
| #7 | "Google 'Bootstrap 5 sticky footer flexbox'" | "body needs d-flex flex-column min-vh-100; footer needs mt-auto" |
| #8 | "What Bootstrap grid class gives 2 columns between 576px and 768px?" | "col-sm-6" |
| #9 | "Read the Bootstrap carousel docs -- what attribute enables auto-play?" | "data-bs-ride='carousel'" |
| #10 | "Inspect the accordion collapse elements. What does data-bs-parent point to?" | "It points to #faq-wrong-id -- should be #faqAccordion" |
