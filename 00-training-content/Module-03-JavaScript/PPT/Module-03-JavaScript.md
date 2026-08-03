# JavaScript (Part 1)
## Module 03 | Sustain Engineering Training | Day 3

**1 day | Workshop + guided lab + FE Ops**

---

## By the end of this session

You can write, debug and maintain JavaScript that manipulates the DOM, validates forms, handles errors, and follows object-oriented patterns.

| Pillar | What you will do |
|--------|-----------------|
| **Syntax & Structure** | Variables, types, operators, control flow |
| **Functions** | Declaration, expressions, arrow functions, scope, closures |
| **Objects & Arrays** | Literals, methods, destructuring, array methods |
| **DOM Manipulation** | Selecting, creating, modifying, removing elements |
| **OOP** | Constructor functions, prototypes, classes, inheritance |
| **Forms & Validation** | Client-side validation, preventDefault, input handling |
| **Error Handling** | try/catch/finally, custom errors, defensive coding |
| **Debugging** | Console, breakpoints, call stack, watch expressions |
| **FE Ops** | Performance, lazy load, security, logging |

---

## Session agenda

| # | Topic |
|---|-------|
| 01 | JavaScript fundamentals: variables, types, operators |
| 02 | Control flow: conditionals, loops, iteration |
| 03 | Functions: declaration, scope, closures |
| 04 | Objects and arrays |
| 05 | DOM manipulation |
| 06 | OOP: constructors, prototypes, classes |
| 07 | Form validation and event handling |
| 08 | Error handling and debugging |
| 09 | Frontend Ops & Troubleshooting |
| 10 | Guided lab |

---

## Where JavaScript fits

- **HTML** defines structure (Module 01)
- **CSS** defines presentation (Module 02)
- **JavaScript** defines **behavior and interactivity**

JavaScript runs in the browser and can:
- Respond to user actions (clicks, typing, scrolling)
- Modify the page without reloading (DOM manipulation)
- Validate form input before submission
- Fetch data from servers (covered in later modules)
- Animate and transition elements

<!--VISUAL:browser-pipeline-->

> JavaScript operates at stage 5 (Interact) -- after the page is built and painted.

---

## Adding JavaScript to a page

```javascript
<!-- Method 1: External file (recommended) -->
<script src="js/app.js"></script>

<!-- Method 2: Inline script -->
<script>
  console.log('Hello from inline script');
</script>

<!-- Method 3: Event attribute (avoid) -->
<button onclick="alert('clicked')">Click</button>
```

| Method | Pros | Cons |
|--------|------|------|
| External file | Cached, reusable, maintainable | Extra HTTP request |
| Inline script | No extra request | Not reusable, hard to maintain |
| Event attribute | Quick prototype | Mixes HTML and JS, no separation |

> Always place `<script>` before `</body>` or use `defer` attribute. This ensures the DOM is built before JS runs.

---

## Variables: let, const, var

```javascript
// const: cannot be reassigned (use by default)
const restaurantName = 'Burger Barn';
const deliveryFee = 2.99;

// let: can be reassigned (use when value changes)
let cartTotal = 0;
let itemCount = 0;
cartTotal = 15.98;  // OK

// var: old style (avoid in modern code)
var oldWay = 'legacy';  // function-scoped, not block-scoped
```

| Keyword | Reassign? | Scope | Use when |
|---------|-----------|-------|----------|
| `const` | No | Block | Default choice -- value won't change |
| `let` | Yes | Block | Value will be updated (counters, totals) |
| `var` | Yes | Function | Legacy code only -- avoid in new code |

> Start with `const`. Switch to `let` only when you need to reassign. Never use `var`.

---

## Data types

```javascript
// Primitives
const name = 'Burger Barn';        // string
const price = 8.99;                // number
const isOpen = true;               // boolean
const rating = null;               // null (intentionally empty)
let deliveryTime;                  // undefined
const orderId = Symbol('id');      // symbol (unique)
const bigNum = 9007199254740991n;  // bigint

// Reference types
const menu = ['burger', 'fries'];  // array (object)
const restaurant = { name, price };// object
```

| Type | typeof | Example |
|------|--------|---------|
| String | `"string"` | `'hello'`, `"world"`, `` `template` `` |
| Number | `"number"` | `42`, `3.14`, `NaN`, `Infinity` |
| Boolean | `"boolean"` | `true`, `false` |
| Null | `"object"` (bug!) | `null` |
| Undefined | `"undefined"` | uninitialized variable |
| Object | `"object"` | `{}`, `[]`, `new Date()` |
| Function | `"function"` | `function() {}`, `() => {}` |

---

## Operators

```javascript
// Arithmetic
const total = price * quantity;     // + - * / %
const remainder = 10 % 3;          // 1

// Comparison (always use strict)
price === 8.99    // true (strict equal - type + value)
price == '8.99'   // true (loose equal - AVOID!)
price !== 9.99    // true (strict not equal)
price > 5         // true

// Logical
isOpen && hasItems    // AND: both must be true
isOpen || isTakeaway  // OR: at least one true
!isOpen               // NOT: invert

// Template literals
const msg = `Order total: $${total.toFixed(2)}`;

// Ternary
const status = isOpen ? 'Open' : 'Closed';

// Nullish coalescing
const fee = deliveryFee ?? 2.99;  // use right if left is null/undefined
```

> Always use `===` and `!==`. Never use `==` or `!=`. Loose equality causes subtle bugs.

---

## Control flow: conditionals

```javascript
// if / else if / else
if (cartTotal >= 25) {
  deliveryFee = 0;
  console.log('Free delivery!');
} else if (cartTotal >= 15) {
  deliveryFee = 1.99;
} else {
  deliveryFee = 2.99;
}

// switch
switch (orderStatus) {
  case 'placed':
    showConfirmation();
    break;
  case 'preparing':
    showProgress();
    break;
  case 'delivered':
    showComplete();
    break;
  default:
    showUnknown();
}
```

> Every `case` needs a `break`. Without it, execution falls through to the next case.

---

## Control flow: loops

```javascript
// for loop (when you know the count)
for (let i = 0; i < menuItems.length; i++) {
  console.log(menuItems[i]);
}

// for...of (iterate values -- preferred for arrays)
for (const item of menuItems) {
  console.log(item.name, item.price);
}

// for...in (iterate keys -- use for objects)
for (const key in restaurant) {
  console.log(key, restaurant[key]);
}

// while (when condition-based)
let attempts = 0;
while (attempts < 3) {
  attempts++;
}

// do...while (run at least once)
do {
  retryConnection();
} while (!isConnected);
```

> Prefer `for...of` for arrays. Use `for...in` only for objects. Avoid `for...in` on arrays (it iterates indices as strings).

---

## Functions: three ways to define

```javascript
// 1. Function declaration (hoisted)
function calculateTotal(items) {
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }
  return total;
}

// 2. Function expression (not hoisted)
const getDeliveryFee = function(distance) {
  return distance > 5 ? 4.99 : 2.99;
};

// 3. Arrow function (concise, no own 'this')
const formatPrice = (price) => `$${price.toFixed(2)}`;

// Arrow with multiple statements
const applyDiscount = (total, code) => {
  const discounts = { SAVE10: 0.10, SAVE20: 0.20 };
  const rate = discounts[code] || 0;
  return total * (1 - rate);
};
```

| Style | Hoisted? | Has `this`? | Use for |
|-------|----------|------------|---------|
| Declaration | Yes | Yes | Named functions, methods |
| Expression | No | Yes | Callbacks, conditionals |
| Arrow | No | No (inherits) | Short callbacks, array methods |

---

## Scope and closures

```javascript
// Block scope (let and const)
if (true) {
  const local = 'only here';
  let alsoLocal = 'same';
}
// console.log(local); // Error! Not accessible

// Closure: inner function remembers outer variables
function createCounter() {
  let count = 0;           // private variable
  return {
    increment: () => ++count,
    getCount: () => count,
  };
}

const counter = createCounter();
counter.increment();       // 1
counter.increment();       // 2
counter.getCount();        // 2
// count is not accessible directly -- it's enclosed
```

- **Scope** determines where a variable is accessible
- **Closure** is a function that remembers its outer scope even after the outer function returns
- Closures are used for private state, event handlers, and callbacks

---

## Objects: key-value containers

```javascript
// Object literal
const restaurant = {
  name: 'Burger Barn',
  cuisine: 'American',
  rating: 4.5,
  isOpen: true,
  address: {
    street: '123 Main St',
    city: 'Springfield',
  },
  getInfo() {
    return `${this.name} (${this.cuisine})`;
  },
};

// Access properties
restaurant.name;              // dot notation
restaurant['cuisine'];        // bracket notation
restaurant.address.city;      // nested access

// Destructuring
const { name, rating, isOpen } = restaurant;

// Spread operator
const updated = { ...restaurant, rating: 4.7 };

// Optional chaining
const zip = restaurant.address?.zip;  // undefined (no error)
```

---

## Arrays: ordered collections

```javascript
const cart = [
  { id: 1, name: 'Burger', price: 8.99, qty: 2 },
  { id: 2, name: 'Fries', price: 4.99, qty: 1 },
  { id: 3, name: 'Shake', price: 5.99, qty: 1 },
];

// Essential array methods
cart.push({ id: 4, name: 'Soda', price: 1.99, qty: 1 });
cart.pop();                           // remove last
cart.length;                          // 3

// find: first match
const burger = cart.find(item => item.name === 'Burger');

// filter: all matches
const expensive = cart.filter(item => item.price > 5);

// map: transform each item
const names = cart.map(item => item.name);
// ['Burger', 'Fries', 'Shake']

// reduce: accumulate to single value
const total = cart.reduce(
  (sum, item) => sum + item.price * item.qty, 0
);

// some / every: boolean checks
const hasExpensive = cart.some(item => item.price > 10);
const allInStock = cart.every(item => item.qty > 0);

// forEach: iterate (no return value)
cart.forEach(item => console.log(item.name));
```

---

## Array methods at a glance

| Method | Returns | Mutates? | Use for |
|--------|---------|----------|---------|
| `push(item)` | new length | Yes | Add to end |
| `pop()` | removed item | Yes | Remove from end |
| `unshift(item)` | new length | Yes | Add to start |
| `shift()` | removed item | Yes | Remove from start |
| `splice(i, n)` | removed items | Yes | Remove/insert at index |
| `find(fn)` | first match | No | Lookup by condition |
| `filter(fn)` | new array | No | Subset by condition |
| `map(fn)` | new array | No | Transform each item |
| `reduce(fn, init)` | accumulated | No | Sum, count, group |
| `some(fn)` | boolean | No | Any match? |
| `every(fn)` | boolean | No | All match? |
| `sort(fn)` | sorted array | Yes | Order items |
| `includes(val)` | boolean | No | Contains value? |
| `indexOf(val)` | index / -1 | No | Find position |

> Prefer non-mutating methods (`map`, `filter`, `reduce`) over mutating ones. Create new arrays instead of changing originals.

---

## The DOM: your bridge between JS and the page

The **Document Object Model** is a tree of nodes representing the HTML page. JavaScript can read and modify this tree.

```javascript
// Select elements
const header = document.getElementById('header');
const cards = document.querySelectorAll('.card');
const firstCard = document.querySelector('.card');

// Read content
header.textContent;           // text only
header.innerHTML;             // HTML string (security risk!)

// Modify content
header.textContent = 'New Title';

// Modify attributes
img.setAttribute('src', 'new-image.jpg');
img.alt = 'Description';

// Modify styles
card.style.display = 'none';
card.classList.add('active');
card.classList.remove('hidden');
card.classList.toggle('selected');
```

---

## DOM: creating and removing elements

```javascript
// Create a new element
const card = document.createElement('div');
card.className = 'card';
card.innerHTML = `
  <h3>${restaurant.name}</h3>
  <p>${restaurant.cuisine}</p>
`;

// Add to page
document.getElementById('grid').appendChild(card);

// Insert before another element
grid.insertBefore(card, grid.firstChild);

// Remove element
card.remove();
// or: card.parentNode.removeChild(card);

// Clone element
const clone = card.cloneNode(true);  // true = deep clone
```

> Prefer `textContent` over `innerHTML` when inserting user data. `innerHTML` is an XSS vector if the content is not sanitized.

---

## DOM: event handling

```javascript
// addEventListener (recommended)
button.addEventListener('click', function(event) {
  console.log('Clicked!', event.target);
});

// Arrow function
button.addEventListener('click', (e) => {
  e.preventDefault();   // stop default behavior
  e.stopPropagation();  // stop event bubbling
});

// Event delegation (efficient for dynamic content)
document.getElementById('grid').addEventListener('click', (e) => {
  const card = e.target.closest('.card');
  if (card) {
    const id = card.dataset.id;
    openMenu(id);
  }
});

// Common events
// click, dblclick, mouseenter, mouseleave
// keydown, keyup, keypress
// submit, change, input, focus, blur
// load, DOMContentLoaded, scroll, resize
```

| Pattern | When to use |
|---------|-------------|
| Direct listener | Static elements that exist on page load |
| Event delegation | Dynamic elements added/removed by JS |
| `e.preventDefault()` | Stop form submit, link navigation |
| `e.stopPropagation()` | Prevent event from reaching parent |

---

## Checkpoint: DOM practice

Open the FoodExpress page and try in the Console (F12):

```javascript
// 1. Select all restaurant cards
document.querySelectorAll('.card');

// 2. Change a card title
document.querySelector('.card-title').textContent = 'My Restaurant';

// 3. Add a class
document.querySelector('.card').classList.add('highlight');

// 4. Create a new element
const badge = document.createElement('span');
badge.textContent = 'NEW';
badge.className = 'badge bg-info';
document.querySelector('.card-body').prepend(badge);

// 5. Listen for clicks
document.querySelector('.btn').addEventListener('click', () => {
  alert('Button clicked!');
});
```

> 5 minutes | Try each command in the DevTools Console.

---

## OOP: constructor functions

```javascript
// Constructor function (pre-ES6)
function MenuItem(name, price, category) {
  this.name = name;
  this.price = price;
  this.category = category;
  this.isAvailable = true;
}

// Add method to prototype (shared across instances)
MenuItem.prototype.getInfo = function() {
  return `${this.name} - $${this.price.toFixed(2)}`;
};

MenuItem.prototype.toggleAvailability = function() {
  this.isAvailable = !this.isAvailable;
};

// Create instances
const burger = new MenuItem('Smash Burger', 8.99, 'mains');
const fries = new MenuItem('Loaded Fries', 4.99, 'sides');

burger.getInfo();  // "Smash Burger - $8.99"
```

- `new` creates a new object, sets `this`, returns it
- Methods on `prototype` are shared (memory efficient)
- Without `new`, `this` points to `window` (bug!)

---

## OOP: ES6 classes

```javascript
class MenuItem {
  constructor(name, price, category) {
    this.name = name;
    this.price = price;
    this.category = category;
    this.isAvailable = true;
  }

  getInfo() {
    return `${this.name} - $${this.price.toFixed(2)}`;
  }

  toggleAvailability() {
    this.isAvailable = !this.isAvailable;
  }
}

// Inheritance
class SpecialItem extends MenuItem {
  constructor(name, price, category, discount) {
    super(name, price, category);
    this.discount = discount;
  }

  getDiscountedPrice() {
    return this.price * (1 - this.discount);
  }
}

const special = new SpecialItem('Holiday Burger', 12.99, 'mains', 0.15);
special.getInfo();            // "Holiday Burger - $12.99"
special.getDiscountedPrice(); // 11.04
```

> Classes are syntactic sugar over prototypes. Same behavior, cleaner syntax.

---

## Form validation

```javascript
const form = document.getElementById('order-form');

form.addEventListener('submit', (e) => {
  e.preventDefault();  // stop page reload

  const name = document.getElementById('name').value.trim();
  const email = document.getElementById('email').value.trim();
  const phone = document.getElementById('phone').value.trim();

  // Manual validation
  const errors = [];

  if (!name) {
    errors.push('Name is required');
  }

  if (!email || !email.includes('@')) {
    errors.push('Valid email is required');
  }

  if (phone && !/^\d{10}$/.test(phone)) {
    errors.push('Phone must be 10 digits');
  }

  if (errors.length > 0) {
    showErrors(errors);
    return;
  }

  // All valid -- submit
  submitOrder({ name, email, phone });
});
```

- `e.preventDefault()` stops the form from reloading the page
- Validate on `submit` event, not on individual field changes
- Show all errors at once, not one at a time
- Client validation is UX -- server validation is security

---

## Error handling: try / catch / finally

```javascript
// Basic try/catch
try {
  const data = JSON.parse(responseText);
  processOrder(data);
} catch (error) {
  console.error('Failed to parse:', error.message);
  showUserError('Something went wrong. Please try again.');
} finally {
  hideLoadingSpinner();
}

// Custom error
class ValidationError extends Error {
  constructor(field, message) {
    super(message);
    this.name = 'ValidationError';
    this.field = field;
  }
}

// Throw custom error
function validatePrice(price) {
  if (typeof price !== 'number' || price < 0) {
    throw new ValidationError('price', 'Price must be a positive number');
  }
  return price;
}

// Catch specific error type
try {
  validatePrice(-5);
} catch (e) {
  if (e instanceof ValidationError) {
    highlightField(e.field);
  }
  console.error(e.name, e.message);
}
```

---

## Debugging with DevTools

<!--VISUAL:devtools-panels-->

### Debugging workflow
1. **Console** -- `console.log()`, `console.error()`, `console.table()`
2. **Breakpoints** -- Click line number in Sources panel to pause execution
3. **Step through** -- Step over (F10), step into (F11), step out (Shift+F11)
4. **Watch** -- Add expressions to watch panel to monitor values
5. **Call stack** -- See which function called which
6. **Scope** -- Inspect local, closure, and global variables

```javascript
// Useful console methods
console.log('Value:', variable);
console.table(arrayOfObjects);
console.group('Cart');
  console.log('Items:', cart.length);
  console.log('Total:', total);
console.groupEnd();
console.time('render');
  renderCards();
console.timeEnd('render');  // "render: 12ms"
```

> Never ship `console.log` statements to production. Use a logging framework or remove them.

---

## Common JavaScript bugs and fixes

| Bug | Cause | Fix |
|-----|-------|-----|
| `NaN` in calculations | String + number | Use `parseFloat()` or `Number()` |
| Duplicate items in array | No existence check before `push` | Use `find()` first |
| Form submits with empty fields | No `preventDefault()` | Add `e.preventDefault()` + validation |
| `Cannot read property of undefined` | Accessing nested property on null | Use optional chaining `?.` |
| Event listener not working | Element not in DOM when script runs | Use `DOMContentLoaded` or `defer` |
| `this` is undefined | Arrow function in method | Use regular function for methods |
| Array modified during iteration | `splice` in `forEach` | Use `filter` to create new array |

> These are the bugs sustain engineers fix most often in frontend code.

---

## Frontend Ops: performance optimization

- **Minimize DOM access** -- cache selectors, batch updates
- **Debounce events** -- scroll and resize fire 100+ times/second
- **Lazy load images** -- `loading="lazy"` (Module 01)
- **Defer scripts** -- `<script defer>` loads without blocking render
- **Reduce reflows** -- change classes, not individual styles
- **Bundle and minify** -- fewer HTTP requests, smaller files

```javascript
// Debounce: wait until user stops typing
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

const searchInput = document.getElementById('search');
searchInput.addEventListener('input',
  debounce((e) => filterRestaurants(e.target.value), 300)
);
```

---

## Frontend Ops: security

- **Never trust user input** -- validate and sanitize
- **Use `textContent`, not `innerHTML`** for user data (XSS prevention)
- **Avoid `eval()`** -- executes arbitrary code
- **Use `rel="noopener noreferrer"`** on external links
- **Sanitize before rendering** -- use DOMPurify for HTML content
- **Never store secrets in JS** -- API keys, passwords visible in source

```javascript
// DANGEROUS: XSS vulnerability
element.innerHTML = userInput;

// SAFE: textContent escapes HTML
element.textContent = userInput;

// SAFE: DOMPurify for HTML content
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(htmlContent);
```

> Security audits flag `innerHTML` with user input. Know the safe alternatives.

---

## Frontend Ops: logging and monitoring

```javascript
// Structured logging
function log(level, message, data = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...data,
  };
  console[level](JSON.stringify(entry));
}

log('info', 'Order placed', { orderId: 'FE-1042', total: 24.97 });
log('error', 'Payment failed', { orderId: 'FE-1042', reason: 'timeout' });

// Error boundary: catch unhandled errors
window.addEventListener('error', (event) => {
  log('error', 'Unhandled error', {
    message: event.message,
    file: event.filename,
    line: event.lineno,
  });
});

// Performance monitoring
window.addEventListener('load', () => {
  const perf = performance.getEntriesByType('navigation')[0];
  log('info', 'Page load', {
    domReady: Math.round(perf.domContentLoadedEventEnd),
    fullLoad: Math.round(perf.loadEventEnd),
  });
});
```

---

## Guided lab: add interactivity to FoodExpress

| Step | Task |
|------|------|
| 01 | Fix: "Add to Cart" creates duplicate items instead of incrementing quantity |
| 02 | Fix: Cart total shows `NaN` when discount code is applied |
| 03 | Fix: Checkout form submits with empty required fields |
| 04 | Fix: Cuisine filter re-renders entire page (use DOM manipulation) |
| 05 | Add: Disable "View Menu" button for closed restaurants |
| 06 | Add: Cart item count updates in the navbar badge |
| 07 | Add: Form validation with error messages next to fields |
| 08 | Debug: Use DevTools breakpoints to trace the discount bug |

---

## Lab acceptance criteria

- [ ] Adding same item twice increments quantity (no duplicates)
- [ ] Cart total calculates correctly (price * quantity, no NaN)
- [ ] Form validates name, email, phone before submission
- [ ] Cuisine filter updates only the grid (no page reload/flash)
- [ ] Closed restaurants have disabled buttons
- [ ] Cart badge in navbar shows correct item count
- [ ] Error messages appear next to invalid fields
- [ ] At least one bug traced with DevTools breakpoints
- [ ] `console.log` used for debugging, not left in final code
- [ ] No `innerHTML` with unsanitized user input

---

## Key takeaways

| Concept | Remember |
|---------|----------|
| Variables | `const` by default, `let` when reassigning, never `var` |
| Comparison | Always `===`, never `==` |
| Functions | Declaration, expression, arrow -- know when to use each |
| Arrays | `find`, `filter`, `map`, `reduce` -- prefer non-mutating |
| DOM | `querySelector` to select, `textContent` to write safely |
| Events | `addEventListener` + delegation for dynamic content |
| Forms | `preventDefault()` + validate before submit |
| Errors | `try/catch` for parsing, network, and risky operations |
| Debugging | Breakpoints > console.log. Inspect scope and call stack |
| Security | `textContent` over `innerHTML`. Never trust user input |

> **Next: Module 04 -- JavaScript (Part 2) + UI Frameworks (React, Angular, Vue)**
