# CSS Training Plan — Incremental & Complete

## Module 1: CSS Foundations
1. **What is CSS** — Purpose, how it separates style from structure
2. **3 Ways to Add CSS** — Inline, Internal (`<style>`), External (`<link>`)
3. **CSS Syntax** — Selectors, properties, values, semicolons, curly braces
4. **Basic Selectors** — Element, Class (`.`), ID (`#`), Universal (`*`)
5. **Colors** — Named, HEX, RGB, RGBA, HSL
6. **Fonts & Text** — `font-family`, `font-size`, `font-weight`, `text-align`, `text-decoration`, `line-height`, Google Fonts

**Practice:** Style a simple profile card with text and colors

---

## Module 2: The Box Model
7. **Box Model Concept** — Content → Padding → Border → Margin (diagram)
8. **`box-sizing: border-box`** — Why it matters
9. **Margin Collapsing** — When and why margins collapse
10. **Width & Height** — `px`, `%`, `auto`, `min-*`, `max-*`
11. **Borders** — `border`, `border-radius`, `outline`
12. **Backgrounds** — `background-color`, `background-image`, `background-size`, `background-position`

**Practice:** Build a styled card with proper spacing, borders, and background

---

## Module 3: Selectors & Specificity
13. **Combinator Selectors** — Descendant (` `), Child (`>`), Adjacent (`+`), Sibling (`~`)
14. **Attribute Selectors** — `[type="text"]`, `[href^="https"]`
15. **Pseudo-classes** — `:hover`, `:focus`, `:first-child`, `:nth-child()`, `:not()`
16. **Pseudo-elements** — `::before`, `::after`, `::placeholder`
17. **Specificity Rules** — Inline > ID > Class > Element, the cascade
18. **`!important`** — When (not) to use it

**Practice:** Style a navigation menu using advanced selectors

---

## Module 4: Display & Positioning
19. **Display Types** — `block`, `inline`, `inline-block`, `none`
20. **Position** — `static`, `relative`, `absolute`, `fixed`, `sticky`
21. **`z-index`** — Stacking context
22. **Float & Clear** — Legacy layout (brief overview)
23. **Overflow** — `visible`, `hidden`, `scroll`, `auto`

**Practice:** Build a sticky header + overlapping card layout

---

## Module 5: Flexbox
24. **Flex Container** — `display: flex`, `flex-direction`, `flex-wrap`
25. **Main Axis Alignment** — `justify-content`
26. **Cross Axis Alignment** — `align-items`, `align-self`
27. **Flex Items** — `flex-grow`, `flex-shrink`, `flex-basis`, shorthand `flex`
28. **`gap`** — Spacing between flex items
29. **`order`** — Reordering items

**Practice:** Build a responsive navbar + card row layout

---

## Module 6: CSS Grid
30. **Grid Container** — `display: grid`, `grid-template-columns`, `grid-template-rows`
31. **`fr` unit, `repeat()`, `minmax()`**
32. **Placing Items** — `grid-column`, `grid-row`, `span`
33. **Grid Areas** — `grid-template-areas` (named layout)
34. **`gap`** in Grid
35. **Auto-fit & Auto-fill** — Responsive grids without media queries

**Practice:** Build a full page layout (header, sidebar, content, footer)

---

## Module 7: Responsive Design
36. **Viewport Meta Tag** — Why it's needed
37. **Relative Units** — `em`, `rem`, `%`, `vw`, `vh`, `vmin`, `vmax`
38. **Media Queries** — `@media (max-width: ...)`, breakpoints
39. **Mobile-First vs Desktop-First**
40. **Responsive Images** — `max-width: 100%`, `object-fit`
41. **Container Queries** — `@container` (modern CSS)

**Practice:** Make the grid layout from Module 6 fully responsive

---

## Module 8: Transitions & Animations
42. **Transitions** — `transition-property`, `transition-duration`, `transition-timing-function`
43. **Transform** — `translate`, `rotate`, `scale`, `skew`
44. **Keyframe Animations** — `@keyframes`, `animation-name`, `animation-duration`, `animation-iteration-count`
45. **Performance** — Animating `transform` & `opacity` vs layout properties

**Practice:** Animated button hover effects + loading spinner

---

## Module 9: Advanced & Modern CSS
46. **CSS Variables** — `--custom-property`, `var()`, theming
47. **`calc()`** — Dynamic calculations
48. **Shadows** — `box-shadow`, `text-shadow`
49. **Gradients** — `linear-gradient`, `radial-gradient`
50. **Filters** — `blur`, `grayscale`, `brightness`
51. **`clamp()`** — Fluid typography
52. **Nesting** — Native CSS nesting (modern browsers)

**Practice:** Build a dark/light theme toggle using CSS variables

---

## Module 10: Capstone Project
53. **Build a complete responsive landing page** combining:
    - Semantic HTML
    - CSS Variables for theming
    - Flexbox (navbar, sections)
    - Grid (feature cards, footer)
    - Media queries (responsive)
    - Transitions & hover effects
    - Proper specificity & clean selectors

---

## Suggested Flow Per Module

| Step | Activity | Time |
|------|----------|------|
| 1 | Concept explanation with live demo | 15 min |
| 2 | Code-along with students | 15 min |
| 3 | Hands-on practice exercise | 15 min |
| 4 | Review & Q/A | 5 min |
