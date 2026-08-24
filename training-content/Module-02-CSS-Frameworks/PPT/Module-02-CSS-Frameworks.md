# CSS & Frameworks
## Module 02 | Sustain Engineering Training | Day 2

**1 day | Workshop + guided lab + capsule project**

---

## By the end of this session

You can build responsive, styled interfaces using CSS layout systems and evaluate CSS frameworks for production use.

| Pillar | What you will do |
|--------|-----------------|
| **Responsive Design** | Media queries, breakpoints, mobile-first approach |
| **Typography** | Font stacks, sizing, line-height, web fonts |
| **Visual Design** | Colors, backgrounds, gradients, shadows |
| **Motion** | Transitions, animations, reduced-motion |
| **Frameworks** | Bootstrap 5, Semantic UI -- compare and integrate |
| **Capsule Project** | Apply all concepts to FoodExpress |

---

## Session agenda

| # | Topic |
|---|-------|
| 01 | Responsive design & media queries |
| 02 | Typography & web fonts |
| 03 | Colors, backgrounds & gradients |
| 04 | Animations & transitions |
| 05 | CSS Frameworks: Bootstrap 5 |
| 06 | CSS Frameworks: Semantic UI |
| 07 | Framework comparison & selection |
| 08 | Capsule project + MCQs |

---

## Responsive design: one codebase, every screen

- The same HTML and CSS must work on phones, tablets, and desktops
- Responsive design adapts **layout** to available space
- Content and meaning stay the same -- only composition changes

### Three pillars of responsive design
1. **Fluid grids** -- use percentages and fr units, not fixed px widths
2. **Flexible images** -- `max-width: 100%` prevents overflow
3. **Media queries** -- change rules at specific breakpoints

> The viewport meta tag enables responsive behavior on mobile. Without it, phones render the desktop version scaled down.

---

## The viewport meta tag

```html
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">
```

| Attribute | Purpose |
|-----------|---------|
| `width=device-width` | Match layout width to the device screen |
| `initial-scale=1.0` | No zoom on page load |

### Without this tag
- Mobile browsers assume a 980px-wide page
- Everything appears tiny and zoomed out
- Media queries do not trigger correctly

> This was covered in Module 01. Verify it exists before writing any responsive CSS.

---

## Media queries: change layout at breakpoints

```css
/* Base: mobile-first (no media query needed) */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* Tablet: 2 columns at 768px */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* Desktop: 3 columns at 1200px */
@media (min-width: 1200px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

> Mobile-first: write base styles for small screens. Add complexity as the screen grows.

---

## Common breakpoints

<!--VISUAL:responsive-breakpoints-->

| Breakpoint | Target | Typical use |
|-----------|--------|-------------|
| 576px | Landscape phones | Stack to 2 columns |
| 768px | Tablets | Sidebar visible, 2-col grid |
| 992px | Desktops | Full layout, sticky sidebars |
| 1200px | Large desktops | 3-4 column grids |
| 1400px | Extra large | Max content width |

### How to choose breakpoints
- Do NOT target specific devices (iPhone, Galaxy, iPad)
- Resize slowly and add a breakpoint **where the content breaks**
- Test with Chrome DevTools Device Toolbar (Ctrl+Shift+M)

> Breakpoints are about content, not devices. Add one when the layout becomes cramped.

---

## Flexbox: one-axis layout

<!--VISUAL:flexbox-axes-->

```css
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.nav-links {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}
```

| Property | What it controls |
|----------|-----------------|
| `display: flex` | Enable flexbox on container |
| `flex-direction` | row (default) or column |
| `justify-content` | Alignment along main axis |
| `align-items` | Alignment along cross axis |
| `flex-wrap` | Allow items to wrap to next line |
| `gap` | Space between flex items |
| `flex: 1` | Item grows to fill available space |

---

## Flexbox patterns you will use

<!--VISUAL:sticky-footer-->

### Sticky footer
```css
body { display: flex; flex-direction: column; min-height: 100vh; }
main { flex: 1; }
footer { margin-top: auto; }
```

### Centered content
```css
.hero { display: flex; justify-content: center; align-items: center; min-height: 50vh; }
```

### Space between items
```css
.card-footer { display: flex; justify-content: space-between; align-items: center; }
```

### Responsive switch
```css
.layout { display: flex; flex-wrap: wrap; gap: 1rem; }
.layout > * { flex: 1 1 300px; }  /* Items wrap when < 300px */
```

---

## CSS Grid: two-axis layout

<!--VISUAL:grid-visual-->

```css
/* Fixed columns */
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

/* Responsive auto-fit */
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
```

| Property | Purpose |
|----------|---------|
| `grid-template-columns` | Define column tracks |
| `grid-template-rows` | Define row tracks |
| `gap` | Space between cells |
| `auto-fit` | Browser chooses column count |
| `minmax(280px, 1fr)` | Min 280px, max equal share |
| `grid-column: span 2` | Item spans 2 columns |

> Grid `auto-fit` + `minmax` is responsive without media queries.

---

## Grid vs Flexbox: when to use each

| Criterion | Flexbox | Grid |
|-----------|---------|------|
| Axis | One (row OR column) | Two (rows AND columns) |
| Best for | Navbars, card rows, form actions | Page layouts, dashboards, galleries |
| Item sizing | Content-driven | Track-driven |
| Alignment | Main + cross axis | Row + column axis |
| Wrapping | `flex-wrap` | `auto-fit` / `auto-fill` |

### Rule of thumb
- **Flexbox** when items should flow and wrap naturally
- **Grid** when you need rows AND columns to align
- They can nest: Grid for page layout, Flexbox inside each card

---

## Positioning for responsive layouts

| Value | Behavior | Mobile-safe? |
|-------|----------|-------------|
| `static` | Default document flow | Yes |
| `relative` | Offset from normal position | Yes |
| `absolute` | Inside positioned parent | Yes (if parent is bounded) |
| `fixed` | Relative to viewport | **Dangerous on mobile** |
| `sticky` | Hybrid relative + fixed | Yes (use for sidebars) |

```css
/* Mobile: normal flow */
.sidebar { position: relative; width: 100%; }

/* Desktop: sticky sidebar */
@media (min-width: 768px) {
  .sidebar { position: sticky; top: 80px; }
}
```

> Never use `position: fixed` with percentage width on mobile. It creates overlapping elements.

---

## Typography fundamentals

```css
body {
  font-family: -apple-system, BlinkMacSystemFont,
               "Segoe UI", Roboto, "Helvetica Neue",
               Arial, sans-serif;
  font-size: 16px;         /* Base size */
  line-height: 1.5;        /* 1.5x the font size */
  color: #333;
}

h1 { font-size: 2.5rem; }  /* 40px */
h2 { font-size: 2rem; }    /* 32px */
h3 { font-size: 1.5rem; }  /* 24px */
```

| Property | Purpose | Tip |
|----------|---------|-----|
| `font-family` | Font stack (fallback chain) | Always end with generic family |
| `font-size` | Text size | Use `rem` for scalability |
| `line-height` | Vertical spacing | 1.5 for body, 1.2 for headings |
| `font-weight` | Bold/light | 400 normal, 700 bold |
| `letter-spacing` | Space between characters | Subtle: 0.5px for headings |
| `text-transform` | Uppercase/lowercase | `uppercase` for labels |

---

## Web fonts and @font-face

```css
/* Google Fonts (external) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

body { font-family: 'Inter', sans-serif; }

/* Self-hosted (better performance) */
@font-face {
  font-family: 'CustomFont';
  src: url('fonts/custom.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}
```

| Approach | Pros | Cons |
|----------|------|------|
| System fonts | Fastest, no download | Limited choices |
| Google Fonts | Easy, huge library | External dependency |
| Self-hosted | Full control, faster | More setup |

> `font-display: swap` shows fallback font immediately, swaps when custom font loads.

---

## Colors in CSS

```css
/* Named */
color: red;

/* Hex */
color: #e84c3d;
color: #e84c3d80;      /* 50% transparent */

/* RGB / RGBA */
color: rgb(232, 76, 61);
color: rgba(232, 76, 61, 0.5);

/* HSL / HSLA (most readable) */
color: hsl(6, 78%, 57%);
color: hsla(6, 78%, 57%, 0.5);

/* Modern (oklch) */
color: oklch(0.63 0.26 29);
```

| Format | Best for |
|--------|----------|
| Hex | Compact, widely used |
| RGB | When you have numeric values |
| HSL | Intuitive: hue, saturation, lightness |
| OKLCH | Perceptually uniform (modern) |

> Use CSS custom properties for brand colors: `--brand-red: #e84c3d;`

---

## Backgrounds and gradients

```css
/* Solid color */
.hero { background-color: #2c3e50; }

/* Image */
.hero {
  background-image: url('hero-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* Linear gradient */
.banner {
  background: linear-gradient(135deg, #e84c3d, #2c3e50);
}

/* Radial gradient */
.spotlight {
  background: radial-gradient(circle, #fff, #f0f0f0);
}

/* Overlay pattern */
.hero-overlay {
  background:
    linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
    url('hero.jpg') center/cover;
}
```

---

## CSS transitions

```css
/* Smooth hover effect */
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* Button color transition */
.btn {
  background: #e84c3d;
  transition: background 0.3s ease;
}
.btn:hover {
  background: #c0392b;
}
```

| Property | Purpose |
|----------|---------|
| `transition-property` | Which property to animate |
| `transition-duration` | How long (0.2s, 300ms) |
| `transition-timing-function` | Easing curve (ease, linear, ease-in-out) |
| `transition-delay` | Wait before starting |

> Shorthand: `transition: property duration timing delay;`

---

## CSS animations with @keyframes

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fadeIn 0.5s ease-out;
}

@keyframes pulse {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.notification-badge {
  animation: pulse 2s infinite;
}
```

| Property | Purpose |
|----------|---------|
| `animation-name` | Which @keyframes to use |
| `animation-duration` | Length of one cycle |
| `animation-iteration-count` | How many times (or `infinite`) |
| `animation-direction` | Normal, reverse, alternate |
| `animation-fill-mode` | State before/after animation |

---

## Respect prefers-reduced-motion

```css
/* Remove ALL animations for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

- Some users experience motion sickness or vestibular disorders
- This media query respects the OS-level accessibility setting
- Always provide this rule in production CSS
- Test: toggle the setting in your OS accessibility preferences

> Animations are enhancement, not requirement. The page must work without them.

---

## Checkpoint: responsive and animated

Open your Module 01 page and try these:

1. Add a media query that changes the layout at 768px
2. Add a `transition` on card hover (transform + shadow)
3. Add a `@keyframes` fade-in animation on page load
4. Add the `prefers-reduced-motion` media query
5. Test with Chrome DevTools Device Toolbar at 375px, 768px, 1200px

> 10 minutes | Individual practice

---

## CSS frameworks: what problem do they solve?

- Writing responsive CSS from scratch is repetitive
- Cross-browser consistency is tedious to maintain
- Common components (navbars, modals, cards) are rebuilt constantly
- Accessibility defaults (focus, ARIA) require expertise

### What a framework gives you
- Pre-built **grid system** with breakpoints
- Ready-to-use **components** (navbar, modal, carousel, accordion)
- **Utility classes** for spacing, display, text alignment
- **Consistent** cross-browser rendering
- Built-in **accessibility** (keyboard navigation, ARIA attributes)

> A framework is a constraint system, not a shortcut. You trade flexibility for speed and consistency.

---

## Bootstrap 5: the industry standard

```html
<!-- Include via CDN -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js">
</script>
```

### Key features
- 12-column responsive grid system
- 6 breakpoints (xs, sm, md, lg, xl, xxl)
- 30+ components (navbar, modal, carousel, accordion, toast...)
- Utility-first classes for spacing, display, flex, text
- No jQuery dependency (since v5)
- `bootstrap.bundle.min.js` includes Popper.js

---

## Bootstrap grid system

```html
<div class="container">
  <div class="row">
    <div class="col-sm-6 col-md-4 mb-4">Card 1</div>
    <div class="col-sm-6 col-md-4 mb-4">Card 2</div>
    <div class="col-sm-6 col-md-4 mb-4">Card 3</div>
  </div>
</div>
```

| Class | Breakpoint | Columns shown |
|-------|-----------|---------------|
| `col-12` | Always | 1 (full width) |
| `col-sm-6` | >= 576px | 2 per row |
| `col-md-4` | >= 768px | 3 per row |
| `col-lg-3` | >= 992px | 4 per row |

- 12 columns total: `col-6` = half width, `col-4` = third, `col-3` = quarter
- Combine breakpoints: `col-sm-6 col-md-4` = 2 on tablet, 3 on desktop

---

## Bootstrap components: navbar

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">FoodExpress</a>
    <button class="navbar-toggler" type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navMenu">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav me-auto">
        <li class="nav-item">
          <a class="nav-link active" href="#">Home</a>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

### Critical attributes
- `data-bs-toggle="collapse"` -- activates the toggler
- `data-bs-target="#navMenu"` -- points to the collapsible element
- Without these, the mobile hamburger menu does nothing

---

## Bootstrap components: modal

```html
<!-- Trigger -->
<button data-bs-toggle="modal" data-bs-target="#myModal">
  Open
</button>

<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Title</h5>
        <button type="button" class="btn-close"
                data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">Content here</div>
      <div class="modal-footer">
        <button class="btn btn-secondary"
                data-bs-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
```

> `data-bs-dismiss="modal"` closes the modal. Bootstrap 4 used `data-dismiss` (no `bs-` prefix) -- this is the #1 migration bug.

---

## Bootstrap components: carousel and accordion

### Carousel
```html
<div id="hero" class="carousel slide"
     data-bs-ride="carousel" data-bs-interval="4000">
  <div class="carousel-inner">
    <div class="carousel-item active">Slide 1</div>
    <div class="carousel-item">Slide 2</div>
  </div>
</div>
```
- `data-bs-ride="carousel"` enables auto-play
- Without it, carousel stays on slide 1

### Accordion
```html
<div class="accordion" id="faq">
  <div class="accordion-item">
    <button data-bs-toggle="collapse"
            data-bs-target="#faq1">Question</button>
    <div id="faq1" class="collapse"
         data-bs-parent="#faq">Answer</div>
  </div>
</div>
```
- `data-bs-parent="#faq"` auto-closes other items
- Wrong parent ID = all items stay open

---

## Bootstrap utility classes

| Category | Examples | Purpose |
|----------|---------|---------|
| Spacing | `m-3`, `p-4`, `mt-2`, `mb-4`, `mx-auto` | Margin and padding |
| Display | `d-none`, `d-md-block`, `d-flex` | Show/hide at breakpoints |
| Flex | `justify-content-between`, `align-items-center` | Flexbox alignment |
| Text | `text-center`, `text-muted`, `fw-bold` | Typography utilities |
| Color | `text-danger`, `bg-dark`, `text-white` | Bootstrap color palette |
| Border | `rounded`, `border`, `shadow-sm` | Borders and shadows |
| Sizing | `w-100`, `h-100`, `min-vh-100` | Width and height |

### Sticky footer with utilities only
```html
<body class="d-flex flex-column min-vh-100">
  <main class="flex-grow-1">...</main>
  <footer class="mt-auto bg-dark text-white py-4">...</footer>
</body>
```

---

## Bootstrap 4 vs 5: migration pitfalls

| Feature | Bootstrap 4 | Bootstrap 5 |
|---------|------------|-------------|
| Data attributes | `data-toggle`, `data-target` | `data-bs-toggle`, `data-bs-target` |
| Close button | `data-dismiss` | `data-bs-dismiss` |
| JavaScript | jQuery required | Vanilla JS (no jQuery) |
| Jumbotron | `<div class="jumbotron">` | Removed (use utilities) |
| Margin left/right | `.ml-3`, `.mr-3` | `.ms-3`, `.me-3` (start/end) |
| Float | `.float-left` | `.float-start` |
| Form groups | `.form-group` | Simplified (no wrapper needed) |
| RTL support | None | Built-in |

> The `data-bs-*` prefix change silently breaks every interactive component. Modal close, navbar toggle, carousel, accordion -- all fail without the prefix.

---

## Bootstrap performance

### Bundle options (pick ONE)

| File | Includes | Size |
|------|---------|------|
| `bootstrap.bundle.min.js` | Bootstrap + Popper.js | ~80KB |
| `bootstrap.min.js` | Bootstrap only | ~60KB |
| `popper.min.js` | Popper.js only | ~20KB |

- Use `bootstrap.bundle.min.js` (recommended)
- **Never** load both bundle AND separate Popper.js
- Loading both = Popper runs twice = bugs + wasted bandwidth

### CSS optimization
- Load only the CSS you need (tree shaking via Sass)
- Use CDN for prototyping, npm for production
- Defer non-critical CSS with `media="print"` trick

---

## Semantic UI: human-readable class vocabulary

```html
<!-- Include via CDN -->
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.css">
<script
  src="https://cdn.jsdelivr.net/npm/semantic-ui@2.5.0/dist/semantic.min.js">
</script>
```

### Philosophy
- Classes read like natural language: `ui red button`, `ui stackable grid`
- Components are self-describing: `ui card`, `ui modal`, `ui dropdown`
- Theming is built-in with variables

```html
<div class="ui stackable three column grid">
  <div class="column">
    <div class="ui card">
      <div class="content">
        <div class="header">Burger Barn</div>
        <div class="description">Classic burgers</div>
      </div>
    </div>
  </div>
</div>
```

---

## Semantic UI components

### Button variations
```html
<button class="ui red button">Order Now</button>
<button class="ui basic button">Cancel</button>
<button class="ui icon button"><i class="cart icon"></i></button>
<div class="ui buttons">
  <button class="ui button">Standard</button>
  <button class="ui green button">Express</button>
</div>
```

### Cards
```html
<div class="ui cards">
  <div class="card">
    <div class="image"><img src="burger.jpg"></div>
    <div class="content">
      <div class="header">Burger Barn</div>
      <div class="meta">American</div>
      <div class="description">Classic burgers and shakes</div>
    </div>
    <div class="extra content">
      <span><i class="star icon"></i> 4.5 rating</span>
    </div>
  </div>
</div>
```

---

## Bootstrap vs Semantic UI: comparison

| Criterion | Bootstrap 5 | Semantic UI |
|-----------|------------|-------------|
| Class style | Utility-first (`d-flex`, `mt-3`) | Human-readable (`ui red button`) |
| Grid system | 12 columns, 6 breakpoints | 16 columns, stackable |
| Components | 30+ built-in | 50+ built-in |
| JavaScript | Vanilla JS (no jQuery) | **Requires jQuery** |
| Theming | Sass variables | Built-in theme system |
| Bundle size | ~200KB CSS + ~80KB JS | ~600KB CSS + ~300KB JS |
| Active development | Yes (v5.3+) | Limited (community forks: Fomantic UI) |
| Enterprise adoption | Very high | Moderate |
| Learning curve | Medium | Low (readable classes) |
| RTL support | Built-in | Plugin needed |

---

## Choosing a framework: decision criteria

| Factor | Question to ask |
|--------|----------------|
| **Project fit** | Does it support the components we need? |
| **Team skill** | Does the team already know one framework? |
| **Bundle size** | Can we afford the download cost? |
| **Active maintenance** | Is it still receiving updates and security patches? |
| **Dependency chain** | Does it require jQuery or other libraries? |
| **Accessibility** | Does it provide ARIA attributes and keyboard navigation? |
| **Customization** | Can we theme it to match our brand? |
| **Documentation** | Is the documentation clear and complete? |

> In sustain engineering, you inherit the framework. Your job is to master it and fix issues within its constraints.

---

## Framework integration: best practices

- Load CSS in the `<head>`, JS before `</body>`
- Use the framework's grid system, not custom floats
- Prefer utility classes over custom CSS for spacing
- Override framework styles with classes, never `!important`
- Use `data-bs-*` attributes correctly (Bootstrap 5)
- Test at every breakpoint, not just desktop
- Check bundle size in DevTools Network tab

### Common integration bugs
1. Missing JS bundle (components don't work)
2. Wrong data attribute prefix (BS4 vs BS5)
3. Duplicate Popper.js loading
4. jQuery missing for Semantic UI
5. CSS specificity conflicts with custom styles

---

## Troubleshooting framework issues

### Component not working?
1. Is the JS bundle loaded? (check DevTools Console for errors)
2. Are `data-bs-*` attributes correct? (not old `data-*` prefix)
3. Does `data-bs-target` match the element's `id`?
4. Is the `id` unique on the page?
5. Is Popper loaded separately AND in the bundle? (conflict)

### Layout broken?
1. Is the viewport meta tag present?
2. Are you using the correct `col-*` breakpoint classes?
3. Is `box-sizing: border-box` applied globally?
4. Check DevTools Device Toolbar at multiple widths

> 90% of Bootstrap bugs are data attribute typos or missing JS.

---

## Capsule project: build a responsive FoodExpress page

Apply everything from today:

| Task | What to demonstrate |
|------|-------------------|
| Responsive grid | 1 col mobile, 2 col tablet, 3 col desktop |
| Media queries | Layout changes at 768px and 1200px |
| Typography | Font stack, heading hierarchy, line-height |
| Colors | Brand colors via CSS custom properties |
| Transitions | Card hover effect (transform + shadow) |
| Animation | Fade-in on page load + reduced-motion query |
| Framework | Bootstrap OR Semantic UI for navbar + cards |
| Components | Navbar with mobile toggler, card layout, footer |

---

## Capsule project acceptance criteria

- [ ] Page uses a CSS framework (Bootstrap 5 or Semantic UI)
- [ ] Responsive grid: 1/2/3 columns at correct breakpoints
- [ ] Navbar collapses to hamburger on mobile
- [ ] At least one transition (hover effect on cards)
- [ ] At least one animation (@keyframes fade-in or similar)
- [ ] `prefers-reduced-motion` media query included
- [ ] Typography: clear heading hierarchy with readable line-height
- [ ] Colors: brand palette using CSS custom properties
- [ ] Footer stays at bottom (sticky footer pattern)
- [ ] Tested at 375px, 768px, and 1200px
- [ ] No framework JS errors in DevTools Console

---

## MCQ: test your understanding

1. Which CSS unit scales with the user's browser font size setting?
2. What does `@media (min-width: 768px)` mean?
3. What is the difference between `transition` and `animation`?
4. Why does Bootstrap 5 use `data-bs-toggle` instead of `data-toggle`?
5. What does `bootstrap.bundle.min.js` include that `bootstrap.min.js` does not?
6. What CSS property should you use for card hover effects to avoid triggering layout reflow?
7. What does `font-display: swap` do for web fonts?
8. When would you choose Grid over Flexbox?
9. What happens if you omit the viewport meta tag?
10. Why is `prefers-reduced-motion` important?

---

## Key takeaways

| Concept | Remember |
|---------|----------|
| Responsive | Mobile-first + media queries at content breakpoints |
| Flexbox | One axis, use for navbars, card rows, forms |
| Grid | Two axes, use for page layouts, dashboards |
| Typography | System font stack + rem units + line-height 1.5 |
| Transitions | Smooth state changes (hover, focus) |
| Animations | @keyframes for entrance effects, respect reduced-motion |
| Bootstrap 5 | `data-bs-*` prefix, bundle includes Popper, no jQuery |
| Semantic UI | Human-readable classes, requires jQuery, large bundle |
| Selection | Choose based on project needs, not personal preference |

> **Next: Module 03 -- JavaScript (Part 1): Syntax, Functions, Objects, Arrays, DOM**
