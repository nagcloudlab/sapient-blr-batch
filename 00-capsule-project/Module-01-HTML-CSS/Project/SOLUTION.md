# Module 01 Solutions -- TRAINER ONLY

## Bug #1: Restaurant Grid Breaks on Tablet

**Root Cause:** Missing `col-sm-6` class on restaurant card columns. Only `col-md-4` is set, so below 768px all cards go full-width instead of 2 per row.

**Fix:** In `index.html`, change every restaurant column:
```html
<!-- Before -->
<div class="col-md-4 mb-4">

<!-- After -->
<div class="col-sm-6 col-md-4 mb-4">
```

**Key concept:** Bootstrap's grid breakpoints -- `col-sm-6` means 2 columns (6/12) starting at 576px. Without it, cards jump from 3 columns to 1 with no intermediate step.

---

## Bug #2: Cart Sidebar Overlaps on Mobile

**Root Cause:** `.cart-sidebar` uses `position: fixed` with `width: 23%`. On mobile, this creates a tiny floating box that overlaps content.

**Fix in `style.css`:** Replace the fixed positioning with responsive rules:
```css
/* Remove from .cart-sidebar: */
/* position: fixed; top: 80px; width: 23%; */

/* Add responsive rules: */
@media (min-width: 768px) {
  .cart-sidebar {
    position: sticky;
    top: 80px;
  }
}

@media (max-width: 767.98px) {
  .cart-sidebar {
    position: relative;
    width: 100%;
    top: 0;
    margin-top: 20px;
  }
}
```

**Also in `index.html`:** Change the aside column to `col-12 col-md-3` so it goes full-width on mobile.

**Key concept:** `position: fixed` removes element from normal flow. On mobile, use `relative` or `static` so it stacks normally. On desktop, use `sticky` for scroll-following behavior.

---

## Bug #3: Cart Total Alignment on Small Screens

**Root Cause:** `.cart-total` flex container wraps incorrectly on small screens.

**Fix in `style.css`:**
```css
.cart-total {
  font-size: 1.2rem;
  flex-wrap: nowrap;
  align-items: center;
}

@media (max-width: 576px) {
  .cart-total {
    font-size: 1rem;
  }
}
```

**Key concept:** `flex-wrap: nowrap` prevents flex items from wrapping to a new line. Combined with smaller font on mobile, it keeps the total on one line.

---

## Bug #4: Slow Image Loading (Performance)

**Root Cause:** Images don't have `loading="lazy"` attribute. All 9 restaurant images load immediately on page load.

**Fix:** Add `loading="lazy"` to all restaurant images in `index.html`:
```html
<img src="https://placehold.co/400x200/e84c3d/fff?text=Burger+Barn"
     class="card-img-top" alt="Burger Barn" loading="lazy" width="400" height="200">
```

**Bonus:** Add explicit `width` and `height` attributes to prevent layout shift (CLS).

**Key concept:** `loading="lazy"` is a native HTML attribute that defers loading images until they're near the viewport. Check Network tab -- images should load as you scroll down.

---

## ENH #5: Free Delivery Badge

**Fix:** Add badge div inside each qualifying card. The `.free-delivery-badge` CSS already exists.

```html
<div class="card h-100" style="position: relative;">
  <span class="free-delivery-badge">Free Delivery</span>
  <img src="..." ...>
  ...
</div>
```

Qualifying restaurants: Burger Barn, Pizza Palace, Dragon Wok, Taco Fiesta (popular ones likely to have orders > $25).

**Key concept:** Absolute positioning inside a relative container. The badge sits in the top-right corner of the card because `.free-delivery-badge` has `position: absolute` and the card has `position: relative`.

---

## ENH #6: Sticky Footer with Support Contact

**Fix CSS (body):**
```css
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
```

**Fix CSS (footer):** The footer already has styling. Just ensure `margin-top: auto` pushes it down:
```css
.footer {
  background-color: #2c3e50;
  color: #ffffff;
  padding: 20px 0;
  /* mt-auto on HTML element handles push-to-bottom */
}
```

**Fix HTML (body tag):** Add `class="d-flex flex-column min-vh-100"`

**Fix HTML (footer):** Change `mt-5` to `mt-auto` and add content:
```html
<footer class="footer mt-auto">
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-6">
        <p>&copy; 2024 FoodExpress. All rights reserved.</p>
      </div>
      <div class="col-md-6 text-end">
        <p>Support: support@foodexpress.com | +1-800-FOOD-EXP</p>
      </div>
    </div>
  </div>
</footer>
```

**Key concept:** Flexbox sticky footer pattern. Body is a flex column with min-height 100vh. Footer uses margin-top auto to push itself to the bottom of the available space.

---

## ENH #7: Back to Top Button

**Fix HTML (before closing body tag):**
```html
<button class="back-to-top" id="backToTop"
        onclick="window.scrollTo({top:0, behavior:'smooth'})">&#8593;</button>
```

**Fix JS (add to cart.js):**
```javascript
window.addEventListener('scroll', function() {
  const btn = document.getElementById('backToTop');
  if (btn) {
    if (window.scrollY > 300) {
      btn.style.display = 'block';
    } else {
      btn.style.display = 'none';
    }
  }
});
```

**Key concept:** CSS has the button styled and hidden by default (`display: none`). JS listens for scroll events and shows the button after 300px of scrolling. `scrollTo` with `behavior: 'smooth'` animates the scroll.

---

## Bug #8: Checkout Form Flexbox Alignment

**Root Cause:** `.checkout-actions` doesn't handle wrapping on small screens. Safari also needs explicit `align-items`.

**Fix in `style.css`:**
```css
.checkout-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

@media (max-width: 576px) {
  .checkout-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .checkout-actions h5 {
    text-align: center;
    margin-bottom: 10px;
  }
}
```

**Key concept:** `flex-wrap: wrap` + `gap` handles graceful wrapping. On mobile, `flex-direction: column` stacks items vertically.

---

## Hints to Give (If Participants Are Stuck)

| Bug | Hint Level 1 | Hint Level 2 |
|-----|--------------|--------------|
| #1 | "Check Bootstrap grid docs -- what class controls the tablet breakpoint?" | "Look at col-sm-* classes. col-sm-6 = 2 columns." |
| #2 | "Open DevTools, toggle device toolbar to phone view. What CSS property causes the overlap?" | "position: fixed doesn't work on mobile. Try relative or sticky." |
| #3 | "Inspect the total element on mobile -- is flex wrapping?" | "Try flex-wrap: nowrap" |
| #4 | "Google 'lazy loading images HTML5'. It's a single attribute." | "loading='lazy'" |
| #5 | "The CSS for .free-delivery-badge already exists. You just need the HTML." | "Add a span inside the card. Card needs position: relative." |
| #6 | "Google 'CSS sticky footer flexbox'" | "body needs flex column + min-vh-100; footer needs mt-auto" |
| #7 | "You need: HTML button + JS scroll listener. CSS already exists." | "window.addEventListener('scroll', ...) + display block/none" |
| #8 | "Test on different screen sizes. What happens to the flex container?" | "Add flex-wrap and a mobile flex-direction: column" |
