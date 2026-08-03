# HTML & CSS Foundations
## Module 01 | Sustain Engineering Training | Day 1 (Second Half)

**0.5 day | Workshop + guided lab**

---

## By the end of this session

You can build a well-structured web page using semantic HTML and style it with fundamental CSS.

| Pillar | What you will do |
|--------|-----------------|
| **HTML Structure** | Tags, elements, attributes, headings, paragraphs, text formatting |
| **HTML Content** | Links, images, lists, tables |
| **Forms** | Input types, labels, form structure |
| **Semantic HTML** | Landmarks, meaningful elements, meta tags |
| **CSS Basics** | Selectors, properties, values |
| **CSS Layout** | Box model, display types, layout techniques |

---

## Session agenda

| # | Topic |
|---|-------|
| 01 | HTML basics -- tags, elements, attributes |
| 02 | Text and structure -- headings, paragraphs, formatting |
| 03 | Links, images, lists |
| 04 | Tables and semantic HTML |
| 05 | HTML forms |
| 06 | Meta tags and document head |
| 07 | CSS selectors and properties |
| 08 | Box model and layout |
| 09 | Guided lab |

---

## What is HTML?

<!--VISUAL:html-vs-css-->

- **H**yper**T**ext **M**arkup **L**anguage
- Not a programming language -- it is a **markup** language
- Tells the browser **what** content is (structure and meaning)
- Every web page is an HTML document
- Browser reads HTML top-to-bottom and builds a **DOM tree**

> HTML defines the structure. CSS defines the appearance. JavaScript defines the behavior.

---

## HTML document structure

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">
    <title>My Page Title</title>
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>
    <!-- visible content goes here -->
  </body>
</html>
```

| Part | Purpose |
|------|---------|
| `<!DOCTYPE html>` | Tells browser this is HTML5 |
| `<html lang="en">` | Root element with language |
| `<head>` | Metadata, title, stylesheets |
| `<body>` | All visible content |

---

## Tags, elements, and attributes

```html
<a href="https://example.com" target="_blank">Click here</a>
```

| Term | What it is | Example |
|------|-----------|---------|
| **Tag** | The markup markers | `<a>` and `</a>` |
| **Element** | Opening tag + content + closing tag | The entire line |
| **Attribute** | Extra info on the tag | `href="..."`, `target="_blank"` |
| **Value** | The attribute's data | `"https://example.com"` |

- Some elements are **self-closing**: `<img>`, `<br>`, `<hr>`, `<input>`
- Attributes always go in the **opening** tag

---

## Headings and paragraphs

<!--VISUAL:heading-hierarchy-->

```html
<h1>Welcome to FoodExpress</h1>
<h2>Our Restaurants</h2>
<p>Browse the best restaurants in your area
   and order food delivered to your door.</p>
<h3>Burger Barn</h3>
<p>Classic American burgers and shakes.</p>
```

- `<h1>` to `<h6>` -- six levels of headings
- `<h1>` -- one per page, the main title
- `<p>` -- paragraph of text
- Never skip heading levels (h1 then h3 -- wrong)
- Never use headings for size -- use CSS for that

---

## Text formatting

| Element | Purpose | Example |
|---------|---------|---------|
| `<strong>` | Important text (bold) | `<strong>Warning</strong>` |
| `<em>` | Emphasis (italic) | `<em>special</em>` |
| `<mark>` | Highlighted text | `<mark>new</mark>` |
| `<small>` | Fine print | `<small>terms apply</small>` |
| `<del>` | Deleted/struck text | `<del>$29.99</del>` |
| `<sub>` / `<sup>` | Subscript / superscript | H`<sub>`2`</sub>`O |
| `<br>` | Line break | Single line break |
| `<hr>` | Horizontal rule | Thematic break |

> Use `<strong>` for meaning, not `<b>`. Use `<em>` for meaning, not `<i>`.

---

## Links

```html
<!-- External link -->
<a href="https://example.com">Visit Example</a>

<!-- Internal link -->
<a href="menu.html">View Menu</a>

<!-- Jump to section on same page -->
<a href="#restaurants">Browse Restaurants</a>

<!-- Open in new tab -->
<a href="https://example.com" target="_blank"
   rel="noopener noreferrer">External Site</a>

<!-- Email link -->
<a href="mailto:support@foodexpress.com">Email Us</a>

<!-- Phone link -->
<a href="tel:+18001234567">Call Us</a>
```

- `href` -- the destination URL
- `target="_blank"` -- opens in new tab
- `rel="noopener noreferrer"` -- security for external links

---

## Images

```html
<img src="images/burger.jpg"
     alt="A classic smash burger with cheese and pickles"
     width="400"
     height="200"
     loading="lazy">
```

| Attribute | Purpose |
|-----------|---------|
| `src` | Path to the image file |
| `alt` | Text description (accessibility + fallback) |
| `width` / `height` | Prevents layout shift while loading |
| `loading="lazy"` | Defers loading until near viewport |

### Alt text rules
- Informative image: describe what it shows
- Decorative image: use `alt=""` (empty, not missing)
- Never write "image of..." -- screen readers already say "image"

---

## Lists

```html
<!-- Unordered list (bullets) -->
<ul>
  <li>Burgers</li>
  <li>Pizza</li>
  <li>Sushi</li>
</ul>

<!-- Ordered list (numbers) -->
<ol>
  <li>Place your order</li>
  <li>Restaurant prepares food</li>
  <li>Driver picks up</li>
  <li>Delivered to your door</li>
</ol>

<!-- Description list -->
<dl>
  <dt>Delivery Fee</dt>
  <dd>$2.99 for orders under $25</dd>
  <dt>Free Delivery</dt>
  <dd>On all orders above $25</dd>
</dl>
```

- `<ul>` -- when order doesn't matter (menu items)
- `<ol>` -- when order matters (steps, rankings)
- `<dl>` -- term-definition pairs (glossary, FAQ)

---

## Tables

```html
<table>
  <caption>Today's Specials</caption>
  <thead>
    <tr>
      <th>Item</th>
      <th>Price</th>
      <th>Available</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Smash Burger</td>
      <td>$8.99</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Margherita Pizza</td>
      <td>$12.99</td>
      <td>Yes</td>
    </tr>
  </tbody>
</table>
```

- `<caption>` -- describes the table's purpose
- `<thead>` / `<tbody>` -- separate header from data
- `<th>` -- header cell (bold, centered by default)
- `<td>` -- data cell
- Tables are for **tabular data only**, never for layout

---

## Semantic HTML elements

<!--VISUAL:page-layout-->

| Element | Purpose | Use for |
|---------|---------|---------|
| `<header>` | Introductory content | Logo, navigation, search |
| `<nav>` | Navigation links | Main menu, breadcrumbs |
| `<main>` | Primary content | One per page |
| `<section>` | Thematic grouping | Group of related content |
| `<article>` | Self-contained content | Blog post, card, comment |
| `<aside>` | Related but secondary | Sidebar, cart, filters |
| `<footer>` | Closing content | Copyright, contact, links |
| `<figure>` | Illustration with caption | Image + caption pair |
| `<figcaption>` | Caption for figure | Describes the figure |

> Use semantic elements instead of `<div>` wherever possible. They convey meaning to browsers, screen readers, and search engines.

---

## Semantic HTML in practice

```html
<body>
  <header>
    <nav>...</nav>
  </header>

  <main>
    <section id="restaurants">
      <h2>Popular Restaurants</h2>
      <article class="card">...</article>
      <article class="card">...</article>
    </section>
  </main>

  <aside>
    <!-- Cart sidebar -->
  </aside>

  <footer>
    <p>&copy; 2024 FoodExpress</p>
  </footer>
</body>
```

A screen reader can announce: "Navigation landmark... Main landmark... 2 articles... Complementary landmark... Footer landmark."

---

## HTML forms

<!--VISUAL:form-anatomy-->

```html
<form id="order-form" action="/submit" method="POST">
  <label for="name">Full Name</label>
  <input type="text" id="name" name="name"
         placeholder="John Doe" required>

  <label for="email">Email</label>
  <input type="email" id="email" name="email" required>

  <label for="phone">Phone</label>
  <input type="tel" id="phone" name="phone"
         pattern="[0-9]{10}">

  <label for="notes">Delivery Notes</label>
  <textarea id="notes" name="notes" rows="3"></textarea>

  <button type="submit">Place Order</button>
</form>
```

---

## Input types

| Type | Renders as | Mobile keyboard |
|------|-----------|----------------|
| `text` | Plain text field | Standard |
| `email` | Text field | @ and .com keys |
| `tel` | Text field | Numeric keypad |
| `number` | Spinner | Numeric |
| `password` | Masked field | Standard |
| `date` | Date picker | Date wheel |
| `url` | Text field | .com and / keys |
| `search` | Text with clear button | Standard |
| `checkbox` | Toggle box | Tap |
| `radio` | Option circle | Tap |
| `file` | File browser | File picker |
| `hidden` | Not visible | N/A |

> The correct `type` gives users the right keyboard on mobile and enables native validation.

---

## Form attributes and validation

| Attribute | Purpose |
|-----------|---------|
| `required` | Cannot be blank |
| `placeholder` | Hint text (disappears on focus) |
| `minlength` / `maxlength` | Character limits |
| `min` / `max` | Number/date range |
| `pattern` | Regex validation |
| `disabled` | Cannot interact |
| `readonly` | Can see but not edit |
| `autofocus` | Focus on page load |

- `<label for="id">` must match `<input id="id">`
- `name` attribute is what gets sent to the server
- Never rely solely on client validation -- always validate server-side too

---

## Select, radio, and checkbox

```html
<!-- Dropdown select -->
<label for="cuisine">Cuisine Type</label>
<select id="cuisine" name="cuisine">
  <option value="">Choose...</option>
  <option value="american">American</option>
  <option value="italian">Italian</option>
  <option value="indian">Indian</option>
</select>

<!-- Radio buttons (pick one) -->
<fieldset>
  <legend>Delivery Speed</legend>
  <input type="radio" id="standard" name="speed"
         value="standard" checked>
  <label for="standard">Standard (30-45 min)</label>
  <input type="radio" id="express" name="speed"
         value="express">
  <label for="express">Express (15-20 min)</label>
</fieldset>

<!-- Checkbox (pick multiple) -->
<input type="checkbox" id="cutlery" name="cutlery">
<label for="cutlery">Include cutlery</label>
```

---

## Meta tags and the document head

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, initial-scale=1.0">
  <meta name="description"
        content="Order food online from the best restaurants">
  <meta name="author" content="FoodExpress">
  <title>FoodExpress - Order Food Online</title>
  <link rel="stylesheet" href="css/style.css">
  <link rel="icon" href="favicon.ico">
</head>
```

| Meta tag | Purpose |
|----------|---------|
| `charset` | Character encoding (always UTF-8) |
| `viewport` | Enables responsive design on mobile |
| `description` | Search engine snippet |
| `author` | Page author |
| `title` | Browser tab text + search result title |

---

## What is CSS?

- **C**ascading **S**tyle **S**heets
- Controls the **visual presentation** of HTML elements
- Separated from HTML -- keeps structure and style independent
- Three ways to apply CSS:
  1. **External** stylesheet (recommended): `<link rel="stylesheet" href="style.css">`
  2. **Internal** style block: `<style>` in `<head>`
  3. **Inline** style attribute: `style="color: red"` (avoid)

> Always use external stylesheets for maintainability.

---

## CSS syntax: selectors, properties, values

```css
/* Selector { property: value; } */

h1 {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: bold;
}

.card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
}

#cart-total {
  color: #e84c3d;
  font-weight: bold;
}
```

| Selector | Targets | Specificity |
|----------|---------|-------------|
| `h1` | All h1 elements | Lowest |
| `.card` | Elements with class="card" | Medium |
| `#cart-total` | Element with id="cart-total" | Highest |

---

## CSS selectors deep dive

| Selector | Example | Selects |
|----------|---------|---------|
| Element | `p` | All paragraphs |
| Class | `.btn` | All elements with class="btn" |
| ID | `#header` | The one element with id="header" |
| Descendant | `.card p` | All p inside .card |
| Child | `.card > p` | Direct child p of .card |
| Group | `h1, h2, h3` | All h1, h2, and h3 |
| Attribute | `[type="email"]` | Inputs with type email |
| Pseudo-class | `a:hover` | Links on mouse hover |
| Pseudo-element | `p::first-line` | First line of paragraphs |

> Use **classes** for styling. Reserve **IDs** for JavaScript and anchor links.

---

## Common CSS properties

### Text and typography
```css
body {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #333333;
}
```

### Colors and backgrounds
```css
.hero {
  background-color: #e84c3d;
  color: white;
  background-image: url('hero-bg.jpg');
  background-size: cover;
  background-position: center;
}
```

### Borders and shadows
```css
.card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```

---

## CSS units

| Unit | Type | Use for |
|------|------|---------|
| `px` | Absolute | Borders, shadows, precise sizing |
| `rem` | Relative to root font-size | Font sizes, spacing (scalable) |
| `em` | Relative to parent font-size | Component-local sizing |
| `%` | Relative to parent | Widths, heights |
| `vw` / `vh` | Relative to viewport | Full-screen sections |

```css
h1 { font-size: 2rem; }        /* 32px if root is 16px */
.container { width: 90%; }      /* 90% of parent width */
.hero { min-height: 50vh; }     /* Half the viewport height */
.border { border: 1px solid; }  /* Precise 1px border */
```

> Prefer `rem` for font sizes so users who increase browser font size get larger text.

---

## The CSS box model

<!--VISUAL:box-model-->

```
+-------------------------------+
|           MARGIN              |
|  +-------------------------+  |
|  |        BORDER           |  |
|  |  +-------------------+  |  |
|  |  |     PADDING       |  |  |
|  |  |  +-------------+  |  |  |
|  |  |  |   CONTENT   |  |  |  |
|  |  |  +-------------+  |  |  |
|  |  +-------------------+  |  |
|  +-------------------------+  |
+-------------------------------+
```

| Layer | What it is | Affects size? |
|-------|-----------|---------------|
| Content | Text, image inside | Yes |
| Padding | Space inside the border | Yes (content-box) |
| Border | The visible edge | Yes (content-box) |
| Margin | Space outside the border | No (not part of element) |

---

## box-sizing: border-box

```css
/* Default: width = content only */
.box-content {
  box-sizing: content-box;
  width: 300px;
  padding: 20px;
  border: 2px solid;
  /* Actual width: 300 + 40 + 4 = 344px */
}

/* Better: width includes padding + border */
.box-border {
  box-sizing: border-box;
  width: 300px;
  padding: 20px;
  border: 2px solid;
  /* Actual width: 300px (as declared) */
}

/* Apply globally */
*, *::before, *::after {
  box-sizing: border-box;
}
```

> `border-box` makes width predictable. Most frameworks set this globally.

---

## CSS display property

<!--VISUAL:display-types-->

| Value | Behavior | Examples |
|-------|----------|---------|
| `block` | Full width, stacks vertically | `<div>`, `<p>`, `<h1>` |
| `inline` | Width of content, flows horizontally | `<span>`, `<a>`, `<strong>` |
| `inline-block` | Inline flow + block sizing | Buttons, badges |
| `none` | Hidden, removed from flow | Toggle visibility |
| `flex` | Flexbox container | Layouts (covered in Module 02) |
| `grid` | Grid container | Layouts (covered in Module 02) |

```css
.badge {
  display: inline-block;
  padding: 4px 10px;
  background: #27ae60;
  color: white;
  border-radius: 4px;
}
```

---

## Layout techniques: width, margin, padding

```css
/* Centered container with max width */
.container {
  max-width: 1200px;
  margin: 0 auto;        /* auto centers horizontally */
  padding: 0 20px;       /* gutters on sides */
}

/* Spacing between elements */
.card {
  margin-bottom: 20px;   /* space below each card */
  padding: 16px;         /* space inside the card */
}

/* Full-width hero section */
.hero {
  width: 100%;
  padding: 60px 20px;
}
```

| Technique | CSS |
|-----------|-----|
| Center a block element | `margin: 0 auto` + `max-width` |
| Side gutters | `padding: 0 20px` |
| Space between elements | `margin-bottom` |
| Space inside element | `padding` |

---

## CSS cascade and specificity

<!--VISUAL:cascade-flow-->

```css
p { color: blue; }                  /* Specificity: 0,0,1 */
.intro { color: green; }           /* Specificity: 0,1,0 */
#welcome { color: red; }           /* Specificity: 1,0,0 */
```

| Level | Selector type | Specificity | Wins over |
|-------|--------------|-------------|-----------|
| 1 | Element (`p`, `div`) | 0,0,1 | Nothing |
| 2 | Class (`.card`) | 0,1,0 | Elements |
| 3 | ID (`#header`) | 1,0,0 | Classes |
| 4 | Inline style | 1,0,0,0 | Everything |
| 5 | `!important` | Overrides all | Use sparingly! |

> Same specificity? Last rule in source order wins.

---

## Pseudo-classes and pseudo-elements

```css
/* Pseudo-classes: state-based */
a:hover { color: #e84c3d; }
a:visited { color: purple; }
input:focus { border-color: #3D8DFF; }
li:first-child { font-weight: bold; }
tr:nth-child(even) { background: #f8f9fa; }

/* Pseudo-elements: generated content */
.required::after {
  content: " *";
  color: red;
}

p::first-line {
  font-weight: bold;
}
```

| Pseudo-class | Triggers when |
|-------------|---------------|
| `:hover` | Mouse over element |
| `:focus` | Element is focused (click/tab) |
| `:active` | Element is being clicked |
| `:first-child` | First child of parent |
| `:nth-child(n)` | nth child of parent |

---

## Checkpoint: inspect the page

<!--VISUAL:devtools-panels-->

Open Chrome DevTools (F12) and inspect any element:

1. **Elements panel** -- see the HTML structure (DOM tree)
2. **Styles panel** -- see which CSS rules apply
3. **Computed panel** -- see the final calculated values
4. **Box model** -- visualize margin, border, padding, content

### Try this:
- Right-click any heading and choose "Inspect"
- Look at the box model diagram
- Try changing a CSS property live in the Styles panel
- Toggle a property off by unchecking its checkbox

> DevTools lets you test changes before editing your files.

---

## Guided lab: build a FoodExpress page

| Step | Task |
|------|------|
| 01 | Create the HTML skeleton (DOCTYPE, html, head, body) |
| 02 | Add navigation with links |
| 03 | Add a hero banner with heading and paragraph |
| 04 | Build restaurant cards with images, headings, text |
| 05 | Add a table showing menu items and prices |
| 06 | Build a simple order form with labels and inputs |
| 07 | Add a footer with semantic markup |
| 08 | Style everything with an external CSS file |

---

## Lab acceptance criteria

- [ ] Valid HTML5 document structure (DOCTYPE, html, head, body)
- [ ] At least 3 heading levels used correctly (h1, h2, h3)
- [ ] At least one image with alt text, width, and height
- [ ] An unordered list and/or ordered list
- [ ] A table with caption, thead, tbody
- [ ] A form with labels, inputs, and a submit button
- [ ] Semantic elements used (header, nav, main, footer)
- [ ] External CSS file linked and working
- [ ] Box model understood (padding, margin, border visible)
- [ ] Page looks reasonable in the browser

---

## Key takeaways

| Concept | Remember |
|---------|----------|
| HTML tags | `<tag attribute="value">content</tag>` |
| Semantic HTML | Use `<header>`, `<main>`, `<footer>` not just `<div>` |
| Forms | Every input needs a `<label>` with matching `for`/`id` |
| Images | Always include `alt`, `width`, `height` |
| CSS selectors | Element < Class < ID (specificity) |
| Box model | Content + Padding + Border + Margin |
| `border-box` | Makes width include padding and border |
| DevTools | F12 to inspect, edit CSS live, test changes |

> **Next: Module 02 -- CSS Frameworks, Responsive Design, Media Queries, Animations**
