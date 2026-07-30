# Module 01: HTML & CSS -- Fix the Issues

## Lab Overview

Welcome to the FoodExpress sustain engineering team! You've just inherited this food delivery platform from the development team. The client is reporting issues with the layout, especially on mobile devices.

> "Hi Team, we're getting complaints from mobile users. The restaurant cards look broken on tablets, the cart sidebar overlaps everything on phones, and images are loading very slowly. Also, we'd like a 'Free Delivery' badge on qualifying restaurants and a sticky footer with support contact info. Can you fix these before we launch our marketing campaign? Thanks."

Your job: find and fix all 8 issues in the FoodExpress homepage.

---

## Setup

1. Open `starter-code/frontend/index.html` in your browser (Chrome recommended)
2. Open Chrome DevTools (F12)
3. Click the "Toggle Device Toolbar" icon (phone/tablet icon) to test responsive layouts
4. Try these screen sizes: 375px (mobile), 768px (tablet), 1200px+ (desktop)

---

## Bug List

### Bug #1: Restaurant Grid Breaks on Tablet
- **Where to look:** `index.html` -- the `<div class="col-md-4">` on each restaurant card column
- **Symptom:** On tablet (768px), restaurants show 3 columns. Below 768px, they jump to 1 column with no 2-column step.
- **Hint:** Bootstrap grid has a breakpoint class between mobile and md. What class gives 2 columns on smaller screens?
- **Impact:** Awkward layout on tablets -- too much empty space
- **Category:** CSS Grid / Bootstrap responsive grid

### Bug #2: Cart Sidebar Overlaps Content on Mobile
- **Where to look:** `css/style.css` -- the `.cart-sidebar` rule
- **Symptom:** On phones (< 768px), the cart sidebar floats on top of the restaurant cards because it uses `position: fixed` with a percentage width.
- **Hint:** On mobile screens, the sidebar should become part of the normal page flow (not fixed). What CSS position value does that?
- **Impact:** Mobile users can't see or click on restaurants -- cart blocks everything
- **Category:** CSS positioning (fixed vs relative vs sticky)

### Bug #3: Cart Total Misaligned on Small Screens
- **Where to look:** `css/style.css` -- the `.cart-total` rule
- **Symptom:** The "Subtotal" / "Total" text wraps oddly on small screens
- **Hint:** The flex container is wrapping its children. What flex property prevents wrapping?
- **Impact:** Cart total looks broken and unprofessional
- **Category:** CSS Flexbox (flex-wrap)

### Bug #4: Images Load All at Once (Performance)
- **Where to look:** `index.html` -- all the `<img>` tags for restaurant images
- **Symptom:** All 9 restaurant images load immediately on page load (check DevTools > Network tab)
- **Hint:** HTML5 has a single attribute that tells the browser to load images only when they're about to enter the viewport. It's one word.
- **Impact:** Slow initial page load, wastes bandwidth on images not yet visible
- **Category:** HTML performance (lazy loading)

### Bug #5: Missing "Free Delivery" Badge (Enhancement)
- **Where to look:** `index.html` -- restaurant cards that qualify for free delivery
- **Symptom:** Some restaurants offer free delivery (on orders > $25) but there's no visual indicator
- **Hint:** The CSS class `.free-delivery-badge` already exists in `style.css`. You need to add the HTML `<span>` element. The parent card also needs `position: relative`.
- **Impact:** Users don't know about the free delivery promotion
- **Category:** CSS positioning (absolute inside relative) + HTML

### Bug #6: Footer Not Sticky + Missing Contact Info (Enhancement)
- **Where to look:** `index.html` -- the `<footer>` element; `css/style.css` -- the `.footer` rule
- **Symptom:** The footer doesn't stick to the bottom of the page. Also, the right column is empty -- needs support contact info.
- **Hint:** Modern sticky footer uses flexbox: body = flex column + min-height: 100vh, footer = margin-top: auto
- **Impact:** On pages with little content, footer floats in the middle; no way for users to contact support
- **Category:** CSS Flexbox (sticky footer pattern)

### Bug #7: No "Back to Top" Button (Enhancement)
- **Where to look:** `index.html` -- before the closing `</body>` tag; `js/cart.js` -- need to add scroll listener
- **Symptom:** When a user scrolls down to see more restaurants, there's no easy way to get back to the top
- **Hint:** You need: 1) An HTML `<button>` element with class `back-to-top` (CSS already exists). 2) A JavaScript scroll event listener that shows/hides the button based on scroll position. 3) An onclick that scrolls to top smoothly.
- **Impact:** Poor UX on long pages -- user must scroll manually
- **Category:** HTML + CSS + JavaScript (scroll behavior)

### Bug #8: Checkout Form Buttons Misaligned
- **Where to look:** `checkout.html` -- the `.checkout-actions` div; `css/style.css` -- the `.checkout-actions` rule
- **Symptom:** On mobile/Safari, the "Total" text and "Place Order" button don't align properly. On very small screens, they overlap.
- **Hint:** The flex container needs `flex-wrap: wrap` and a `gap`. On mobile, switch to `flex-direction: column` with `align-items: stretch`.
- **Impact:** Checkout looks broken on mobile -- users may abandon their order
- **Category:** CSS Flexbox (responsive flex layout)

---

## Checkpoints

After fixing all bugs, verify:

1. [ ] **Tablet grid (768px):** Restaurants show 2 columns
2. [ ] **Mobile cart:** Cart sidebar stacks below restaurants (no overlap)
3. [ ] **Cart total:** Text aligned properly at all screen sizes
4. [ ] **Lazy loading:** Images load on scroll (check Network tab -- scroll down and watch new requests)
5. [ ] **Free Delivery badges:** At least 3 restaurants show the green badge
6. [ ] **Sticky footer:** Footer stays at bottom; shows support email and phone
7. [ ] **Back to Top:** Button appears when scrolled down, scrolls to top smoothly
8. [ ] **Checkout form:** "Place Order" button and total align on mobile and desktop

---

## Bonus Challenges

1. **Add a hover effect** on restaurant cards that shows a subtle red border (FoodExpress brand color: #e84c3d).

2. **Dark mode footer:** Style the footer with the FoodExpress dark blue (#2c3e50) and add social media icon placeholders.

3. **Responsive hero banner:** Make the hero banner text smaller on mobile (use a media query to reduce font-size).

4. **Image placeholder effect:** Add a light gray background-color to `.card-img-top` so there's a placeholder visible while images are lazy loading.
