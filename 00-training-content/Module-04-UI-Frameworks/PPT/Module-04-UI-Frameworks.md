# JavaScript (Part 2) + UI Frameworks
## Module 04 | Sustain Engineering Training | Day 4-5

**1 day | Workshop + guided lab**

---

## By the end of this session

You can use modern JavaScript (ES6+), understand async patterns, work with modules, and evaluate UI frameworks (React, Angular, Vue) for sustain engineering tasks.

| Pillar | What you will do |
|--------|-----------------|
| **ES6+ Features** | Destructuring, spread/rest, template literals, optional chaining |
| **Async JavaScript** | Callbacks, Promises, async/await, fetch API |
| **Modules** | import/export, CommonJS vs ES Modules, bundlers |
| **FE Ops & Troubleshooting** | Network debugging, performance profiling, error tracking |
| **UI Frameworks** | React, Angular, Vue -- purpose, architecture, differences |
| **Component Libraries** | Bootstrap, Semantic UI -- rapid prototyping |
| **App Scaffolding** | Create React App, Angular CLI, Vue CLI |
| **Code Generation** | AI-assisted UI, low-code tools, design-to-code |

---

## Session agenda

| # | Topic |
|---|-------|
| 01 | ES6+ features: advanced syntax |
| 02 | Destructuring and spread/rest operators |
| 03 | Promises and async/await |
| 04 | Fetch API and error handling |
| 05 | JavaScript modules |
| 06 | FE Ops and troubleshooting |
| 07 | UI frameworks overview: React, Angular, Vue |
| 08 | React fundamentals |
| 09 | Angular and Vue overview |
| 10 | Component libraries: Bootstrap, Semantic UI |
| 11 | Creating apps and code generation |
| 12 | Capsule project + MCQs |

---

## ES6+: arrow functions revisited

```javascript
// Standard function
function calculateTax(amount) {
  return amount * 0.08;
}

// Arrow function (concise)
const calculateTax = (amount) => amount * 0.08;

// Arrow with no params
const getTimestamp = () => Date.now();

// Arrow with body block
const processOrder = (items) => {
  const subtotal = items.reduce((sum, i) => sum + i.price, 0);
  const tax = calculateTax(subtotal);
  return { subtotal, tax, total: subtotal + tax };
};
```

| Feature | Arrow function | Regular function |
|---------|---------------|-----------------|
| `this` binding | Inherits from parent scope | Own `this` (caller-dependent) |
| `arguments` object | Not available | Available |
| Use as constructor | No (`new` throws error) | Yes |
| Best for | Callbacks, array methods | Methods, event handlers |

> Arrow functions do NOT have their own `this`. This is the #1 source of bugs when migrating legacy code.

---

## ES6+: destructuring

```javascript
// Object destructuring
const order = { id: 'FE-1042', customer: 'Alice', total: 24.97 };
const { id, customer, total } = order;

// Rename variables
const { id: orderId, customer: customerName } = order;

// Default values
const { discount = 0, deliveryFee = 2.99 } = order;

// Nested destructuring
const restaurant = {
  name: 'Burger Barn',
  address: { city: 'Springfield', zip: '62704' },
};
const { address: { city, zip } } = restaurant;

// Array destructuring
const [first, second, ...rest] = ['pizza', 'burger', 'sushi', 'tacos'];
// first = 'pizza', second = 'burger', rest = ['sushi', 'tacos']

// Swap variables
let a = 1, b = 2;
[a, b] = [b, a];  // a = 2, b = 1
```

---

## ES6+: spread and rest operators

```javascript
// Spread: expand an array or object
const menu = ['burger', 'fries', 'shake'];
const extendedMenu = [...menu, 'salad', 'wrap'];
// ['burger', 'fries', 'shake', 'salad', 'wrap']

// Spread: merge objects (shallow copy)
const defaults = { deliveryFee: 2.99, taxRate: 0.08 };
const config = { ...defaults, deliveryFee: 0 };
// { deliveryFee: 0, taxRate: 0.08 }

// Rest: collect remaining arguments
function createOrder(customer, ...items) {
  return {
    customer,
    items,
    itemCount: items.length,
  };
}
createOrder('Alice', 'burger', 'fries', 'shake');
// { customer: 'Alice', items: ['burger', 'fries', 'shake'], itemCount: 3 }

// Rest in destructuring
const { name, ...details } = restaurant;
// name = 'Burger Barn', details = { address: {...} }
```

> Spread creates shallow copies. Nested objects are still references. Use `structuredClone()` for deep copies.

---

## ES6+: template literals and tagged templates

```javascript
// Template literals (backticks)
const name = 'Alice';
const total = 24.97;
const message = `Hi ${name}, your order total is $${total.toFixed(2)}`;

// Multi-line strings
const html = `
  <div class="card">
    <h3>${restaurant.name}</h3>
    <p>Rating: ${restaurant.rating}/5</p>
  </div>
`;

// Expressions inside ${}
const status = `Order is ${total > 20 ? 'eligible for free delivery' : 'standard delivery'}`;

// Tagged templates (advanced)
function sql(strings, ...values) {
  // Sanitize values to prevent SQL injection
  return {
    text: strings.join('?'),
    values: values,
  };
}
const query = sql`SELECT * FROM orders WHERE id = ${orderId}`;
```

---

## ES6+: optional chaining and nullish coalescing

```javascript
// Optional chaining (?.)
const order = {
  customer: { name: 'Alice' },
  delivery: null,
};

// Without optional chaining (crashes)
// const city = order.delivery.address.city; // TypeError!

// With optional chaining (safe)
const city = order.delivery?.address?.city;  // undefined

// Works with methods
const formatted = order.delivery?.getETA?.();  // undefined

// Works with arrays
const firstItem = order.items?.[0]?.name;  // undefined

// Nullish coalescing (??)
const fee = order.deliveryFee ?? 2.99;
// Uses 2.99 only if deliveryFee is null or undefined
// NOT for 0 or '' (those are valid values)

// Compare with ||
const fee2 = order.deliveryFee || 2.99;
// Uses 2.99 for null, undefined, 0, '', false
// BUG if deliveryFee is legitimately 0!
```

> Always prefer `??` over `||` when 0 or empty string are valid values.

---

## ES6+: Map, Set, and Symbol

```javascript
// Map: key-value pairs (any type as key)
const orderCache = new Map();
orderCache.set('FE-1042', { customer: 'Alice', total: 24.97 });
orderCache.set('FE-1043', { customer: 'Bob', total: 18.50 });
orderCache.get('FE-1042');     // { customer: 'Alice', total: 24.97 }
orderCache.has('FE-1042');     // true
orderCache.size;               // 2
orderCache.delete('FE-1043');

// Set: unique values only
const categories = new Set(['pizza', 'burger', 'pizza', 'sushi']);
// Set {'pizza', 'burger', 'sushi'}
categories.add('tacos');
categories.has('pizza');       // true
categories.size;               // 4

// Deduplicate an array
const unique = [...new Set(items)];

// Symbol: unique identifiers
const ID = Symbol('id');
const order = { [ID]: 42, name: 'Burger' };
order[ID];  // 42
// Symbols are NOT enumerable in for...in or Object.keys()
```

| Collection | Use when |
|-----------|----------|
| `Object` | String keys, JSON serialization needed |
| `Map` | Any type as key, frequent additions/deletions |
| `Array` | Ordered, duplicates OK |
| `Set` | Unique values, fast lookup |

---

## Callbacks: the foundation of async

```javascript
// Synchronous: blocks until complete
const data = readFileSync('orders.json');  // waits here
processData(data);                         // runs after

// Asynchronous with callback
readFile('orders.json', (error, data) => {
  if (error) {
    console.error('Failed to read:', error);
    return;
  }
  processData(data);
});
console.log('This runs BEFORE file is read');

// Callback hell (pyramid of doom)
getUser(userId, (user) => {
  getOrders(user.id, (orders) => {
    getDetails(orders[0].id, (details) => {
      getPayment(details.paymentId, (payment) => {
        // deeply nested -- hard to read and maintain
        updateUI(payment);
      });
    });
  });
});
```

> Callbacks work but create deeply nested, hard-to-read code. Promises solve this.

---

## Promises: cleaner async

```javascript
// Creating a Promise
function fetchOrder(orderId) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (orderId) {
        resolve({ id: orderId, status: 'delivered' });
      } else {
        reject(new Error('Order ID required'));
      }
    }, 1000);
  });
}

// Consuming a Promise
fetchOrder('FE-1042')
  .then(order => {
    console.log('Order:', order.status);
    return fetchOrderDetails(order.id);
  })
  .then(details => {
    console.log('Details:', details);
  })
  .catch(error => {
    console.error('Failed:', error.message);
  })
  .finally(() => {
    hideLoadingSpinner();
  });
```

| State | Meaning |
|-------|---------|
| **Pending** | Operation in progress |
| **Fulfilled** | Completed successfully (`.then()` runs) |
| **Rejected** | Failed (`.catch()` runs) |
| **Settled** | Either fulfilled or rejected (`.finally()` runs) |

---

## Promise combinators

```javascript
// Promise.all: wait for ALL to complete (fail-fast)
const [menu, reviews, hours] = await Promise.all([
  fetch('/api/menu').then(r => r.json()),
  fetch('/api/reviews').then(r => r.json()),
  fetch('/api/hours').then(r => r.json()),
]);
// If ANY fails, the whole thing rejects

// Promise.allSettled: wait for ALL (never fails)
const results = await Promise.allSettled([
  fetch('/api/menu'),
  fetch('/api/reviews'),
  fetch('/api/hours'),
]);
results.forEach(r => {
  if (r.status === 'fulfilled') console.log(r.value);
  if (r.status === 'rejected') console.error(r.reason);
});

// Promise.race: first to settle wins
const result = await Promise.race([
  fetch('/api/data'),
  timeout(5000),  // reject after 5 seconds
]);

// Promise.any: first to fulfill wins
const fastest = await Promise.any([
  fetch('https://cdn1.example.com/data'),
  fetch('https://cdn2.example.com/data'),
]);
```

---

## async / await: modern async syntax

```javascript
// async function always returns a Promise
async function loadRestaurantPage(id) {
  try {
    // await pauses until Promise resolves
    const restaurant = await fetch(`/api/restaurants/${id}`);
    const data = await restaurant.json();

    const menu = await fetch(`/api/restaurants/${id}/menu`);
    const menuData = await menu.json();

    renderPage(data, menuData);
  } catch (error) {
    console.error('Failed to load:', error);
    showErrorPage();
  } finally {
    hideLoadingSpinner();
  }
}

// Parallel with async/await
async function loadDashboard() {
  const [orders, stats, alerts] = await Promise.all([
    fetch('/api/orders').then(r => r.json()),
    fetch('/api/stats').then(r => r.json()),
    fetch('/api/alerts').then(r => r.json()),
  ]);
  renderDashboard(orders, stats, alerts);
}
```

> `await` can only be used inside an `async` function (or at top-level in ES Modules).

---

## Fetch API: making HTTP requests

```javascript
// GET request
async function getRestaurants() {
  const response = await fetch('/api/restaurants');
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

// POST request
async function placeOrder(order) {
  const response = await fetch('/api/orders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(order),
  });
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message);
  }
  return response.json();
}

// DELETE request
async function cancelOrder(id) {
  await fetch(`/api/orders/${id}`, { method: 'DELETE' });
}
```

| `response` property | Returns |
|---------------------|---------|
| `response.ok` | `true` if status 200-299 |
| `response.status` | HTTP status code (200, 404, 500) |
| `response.json()` | Promise that resolves to parsed JSON |
| `response.text()` | Promise that resolves to raw text |
| `response.headers` | Response headers |

---

## Fetch: common pitfalls

```javascript
// PITFALL 1: fetch does NOT reject on HTTP errors
const response = await fetch('/api/orders');
// 404 or 500 does NOT throw -- you must check manually
if (!response.ok) {
  throw new Error(`HTTP ${response.status}`);
}

// PITFALL 2: JSON.parse errors
try {
  const data = await response.json();  // throws if not valid JSON
} catch (e) {
  console.error('Response is not JSON');
}

// PITFALL 3: no timeout by default
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch('/api/orders', {
    signal: controller.signal,
  });
  clearTimeout(timeoutId);
} catch (e) {
  if (e.name === 'AbortError') {
    console.error('Request timed out');
  }
}

// PITFALL 4: CORS errors
// Cannot fetch from a different domain unless server sends
// Access-Control-Allow-Origin header
```

> In sustain engineering, most API bugs are: missing error checks on fetch, no timeout handling, and CORS misconfigurations.

---

## JavaScript modules: import / export

```javascript
// --- menuService.js ---
// Named exports
export const TAX_RATE = 0.08;

export function calculateSubtotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.qty, 0);
}

export function calculateTotal(items) {
  const subtotal = calculateSubtotal(items);
  return subtotal + (subtotal * TAX_RATE);
}

// Default export (one per file)
export default class MenuService {
  constructor(apiUrl) {
    this.apiUrl = apiUrl;
  }
  async getMenu() {
    const res = await fetch(`${this.apiUrl}/menu`);
    return res.json();
  }
}

// --- app.js ---
// Named imports
import { calculateTotal, TAX_RATE } from './menuService.js';

// Default import
import MenuService from './menuService.js';

// Rename import
import { calculateTotal as calcTotal } from './menuService.js';

// Import all
import * as menu from './menuService.js';
menu.calculateTotal(items);
```

---

## Module systems: ESM vs CommonJS

| Feature | ES Modules (ESM) | CommonJS (CJS) |
|---------|------------------|----------------|
| Syntax | `import` / `export` | `require()` / `module.exports` |
| Loading | Static (compile-time) | Dynamic (runtime) |
| Browser support | Yes (with `type="module"`) | No (Node.js only) |
| Tree-shaking | Yes (bundlers can remove unused) | No |
| File extension | `.mjs` or `"type": "module"` | `.cjs` or default in Node |
| Top-level await | Yes | No |

```html
<!-- Using ES Modules in the browser -->
<script type="module" src="app.js"></script>
```

```javascript
// CommonJS (Node.js)
const express = require('express');
module.exports = { startServer };

// ES Modules (modern)
import express from 'express';
export { startServer };
```

> New projects should use ES Modules. You will encounter CommonJS in legacy Node.js code.

---

## Bundlers and build tools

| Tool | Role | Use case |
|------|------|----------|
| **Webpack** | Bundler | Combines modules into single file, code splitting |
| **Vite** | Dev server + bundler | Fast development, HMR, modern default |
| **esbuild** | Bundler/transpiler | Extremely fast, used by Vite internally |
| **Babel** | Transpiler | Converts modern JS to older syntax for compatibility |
| **Rollup** | Bundler | Library bundling, tree-shaking |
| **Parcel** | Bundler | Zero-config, beginner-friendly |

```bash
# Create a Vite project (modern approach)
npm create vite@latest my-app -- --template react
cd my-app
npm install
npm run dev    # starts dev server with HMR
npm run build  # creates production bundle
```

> Sustain engineers need to understand bundler configs when debugging build failures and performance issues.

---

## FE Ops: network debugging

<!--VISUAL:devtools-panels-->

### Network tab workflow

1. Open DevTools (F12) > Network tab
2. Reload the page to capture all requests
3. Look for red entries (failed requests)
4. Click a request to inspect:
   - **Headers**: request/response headers, status code
   - **Payload**: request body (POST/PUT)
   - **Response**: what the server returned
   - **Timing**: DNS, connect, TTFB, download

| Status | Meaning | Common cause |
|--------|---------|-------------|
| 200 | OK | Success |
| 301/302 | Redirect | URL changed |
| 400 | Bad Request | Invalid payload |
| 401 | Unauthorized | Missing/expired token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Wrong endpoint URL |
| 500 | Internal Server Error | Server-side bug |
| CORS | Blocked | Missing CORS headers |

---

## FE Ops: performance profiling

```javascript
// Measure execution time
console.time('renderCards');
renderRestaurantCards(data);
console.timeEnd('renderCards');  // "renderCards: 45ms"

// Performance API
const start = performance.now();
heavyComputation();
const duration = performance.now() - start;
console.log(`Took ${duration.toFixed(2)}ms`);

// Lighthouse metrics to watch
// FCP  - First Contentful Paint (< 1.8s)
// LCP  - Largest Contentful Paint (< 2.5s)
// TTI  - Time to Interactive (< 3.8s)
// CLS  - Cumulative Layout Shift (< 0.1)
// TBT  - Total Blocking Time (< 200ms)
```

| Optimization | How |
|-------------|-----|
| Reduce bundle size | Tree-shaking, code splitting, dynamic imports |
| Optimize images | WebP format, `loading="lazy"`, correct dimensions |
| Minimize render-blocking | `defer` scripts, inline critical CSS |
| Cache API responses | Service worker, `Cache-Control` headers |
| Reduce DOM nodes | Virtual scrolling, pagination |

---

## FE Ops: error tracking in production

```javascript
// Global error handler
window.addEventListener('error', (event) => {
  reportError({
    type: 'uncaught',
    message: event.message,
    source: event.filename,
    line: event.lineno,
    column: event.colno,
    stack: event.error?.stack,
  });
});

// Unhandled promise rejection
window.addEventListener('unhandledrejection', (event) => {
  reportError({
    type: 'promise',
    message: event.reason?.message || String(event.reason),
    stack: event.reason?.stack,
  });
});

// Report to monitoring service
function reportError(error) {
  fetch('/api/errors', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...error,
      url: window.location.href,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
    }),
  }).catch(() => {}); // don't let error reporting cause errors
}
```

> Production apps use services like Sentry, LogRocket, or Datadog RUM for error tracking.

---

## Why UI frameworks exist

**Problems with vanilla JavaScript at scale:**
- DOM manipulation code becomes verbose and fragile
- State management is manual and error-prone
- No built-in component reuse
- Full page re-renders on data changes
- Hard to coordinate team development

**What frameworks provide:**
- **Component model** -- reusable, self-contained UI pieces
- **Reactive data binding** -- UI auto-updates when data changes
- **Virtual DOM / change detection** -- efficient DOM updates
- **Routing** -- single-page navigation without reloads
- **Ecosystem** -- testing, state management, tooling

```
Vanilla JS:  document.getElementById('price').textContent = newPrice;
React:       setPrice(newPrice);  // UI updates automatically
Angular:     this.price = newPrice;  // two-way binding updates UI
Vue:         this.price = newPrice;  // reactivity system updates UI
```

---

## Framework comparison at a glance

| Feature | React | Angular | Vue |
|---------|-------|---------|-----|
| Created by | Meta (Facebook) | Google | Evan You (community) |
| Released | 2013 | 2016 (v2+) | 2014 |
| Type | Library (view layer) | Full framework | Progressive framework |
| Language | JSX (JavaScript + HTML) | TypeScript | Template + JS/TS |
| Data binding | One-way | Two-way | Two-way |
| DOM strategy | Virtual DOM | Incremental DOM | Virtual DOM |
| Learning curve | Moderate | Steep | Gentle |
| Bundle size | ~42 KB | ~143 KB | ~33 KB |
| State management | Redux, Zustand, Context | NgRx, Services | Pinia, Vuex |
| CLI tool | Create React App, Vite | Angular CLI | Vue CLI, Vite |

> All three are production-ready. Choice depends on team skills, project needs, and organizational standards.

---

## React: core concepts

```jsx
// A React component is a function that returns JSX
function RestaurantCard({ name, cuisine, rating, isOpen }) {
  return (
    <div className="card">
      <h3>{name}</h3>
      <p>{cuisine} | Rating: {rating}/5</p>
      <span className={isOpen ? 'badge-open' : 'badge-closed'}>
        {isOpen ? 'Open' : 'Closed'}
      </span>
    </div>
  );
}

// Using the component
function App() {
  return (
    <div className="grid">
      <RestaurantCard
        name="Burger Barn"
        cuisine="American"
        rating={4.5}
        isOpen={true}
      />
      <RestaurantCard
        name="Sushi Palace"
        cuisine="Japanese"
        rating={4.8}
        isOpen={false}
      />
    </div>
  );
}
```

- JSX looks like HTML but is JavaScript
- Components receive data via **props** (read-only)
- `className` instead of `class` (reserved word in JS)

---

## React: state and hooks

```jsx
import { useState, useEffect } from 'react';

function Cart() {
  // useState: manage component state
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);

  // useEffect: run side effects (fetch, subscribe, etc.)
  useEffect(() => {
    fetch('/api/cart')
      .then(res => res.json())
      .then(data => setItems(data));
  }, []); // empty array = run once on mount

  // Recalculate total when items change
  useEffect(() => {
    const newTotal = items.reduce(
      (sum, item) => sum + item.price * item.qty, 0
    );
    setTotal(newTotal);
  }, [items]); // runs when items changes

  const addItem = (item) => {
    setItems(prev => [...prev, item]);
  };

  return (
    <div>
      <h2>Cart ({items.length} items)</h2>
      <p>Total: ${total.toFixed(2)}</p>
    </div>
  );
}
```

| Hook | Purpose |
|------|---------|
| `useState` | Local state management |
| `useEffect` | Side effects (fetch, timers, subscriptions) |
| `useRef` | Persistent mutable reference (DOM access) |
| `useContext` | Access shared state without prop drilling |
| `useMemo` | Memoize expensive calculations |
| `useCallback` | Memoize functions to prevent re-renders |

---

## React: component lifecycle

```
Mount (first render)
  |
  +--> useState initializes state
  +--> Component renders JSX
  +--> useEffect(() => {...}, []) runs
  |
Update (state or props change)
  |
  +--> Component re-renders with new data
  +--> useEffect(() => {...}, [deps]) runs if deps changed
  |
Unmount (component removed)
  |
  +--> useEffect cleanup function runs
```

```jsx
useEffect(() => {
  // Setup: runs on mount
  const interval = setInterval(checkOrderStatus, 30000);

  // Cleanup: runs on unmount
  return () => {
    clearInterval(interval);
  };
}, []);
```

> Always clean up intervals, event listeners, and subscriptions in the useEffect return function to prevent memory leaks.

---

## Angular: core concepts

```typescript
// Component: a class with a decorator
@Component({
  selector: 'app-restaurant-card',
  template: `
    <div class="card">
      <h3>{{ name }}</h3>
      <p>{{ cuisine }} | Rating: {{ rating }}/5</p>
      <span [class]="isOpen ? 'badge-open' : 'badge-closed'">
        {{ isOpen ? 'Open' : 'Closed' }}
      </span>
      <button (click)="onOrder()">Order Now</button>
    </div>
  `,
})
export class RestaurantCardComponent {
  @Input() name: string;
  @Input() cuisine: string;
  @Input() rating: number;
  @Input() isOpen: boolean;

  onOrder() {
    console.log(`Ordering from ${this.name}`);
  }
}
```

| Angular concept | Purpose |
|----------------|---------|
| **Modules** | Organize app into cohesive blocks |
| **Components** | UI building blocks with template + logic |
| **Services** | Business logic and data access (injectable) |
| **Directives** | `*ngIf`, `*ngFor` -- control DOM rendering |
| **Dependency Injection** | Framework manages object creation |
| **TypeScript** | Required (static typing, interfaces) |

---

## Angular: key differences from React

| Aspect | React | Angular |
|--------|-------|---------|
| Template | JSX (JS + HTML mixed) | HTML template with directives |
| Binding | `{value}` one-way | `{{ value }}` interpolation, `[(ngModel)]` two-way |
| Events | `onClick={handler}` | `(click)="handler()"` |
| Conditionals | JS ternary in JSX | `*ngIf="condition"` |
| Loops | `.map()` in JSX | `*ngFor="let item of items"` |
| Styling | CSS Modules, styled-components | Component-scoped CSS (built-in) |
| HTTP | fetch or axios | HttpClient (built-in, Observable-based) |
| Forms | Controlled components | Template-driven or Reactive forms |

```html
<!-- Angular template directives -->
<div *ngIf="isLoading">Loading...</div>

<div *ngFor="let item of menuItems">
  <p>{{ item.name }} - {{ item.price | currency }}</p>
</div>

<input [(ngModel)]="searchQuery" />
```

---

## Vue: core concepts

```html
<!-- Vue Single-File Component (SFC) -->
<template>
  <div class="card">
    <h3>{{ name }}</h3>
    <p>{{ cuisine }} | Rating: {{ rating }}/5</p>
    <span :class="isOpen ? 'badge-open' : 'badge-closed'">
      {{ isOpen ? 'Open' : 'Closed' }}
    </span>
    <button @click="onOrder">Order Now</button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  name: String,
  cuisine: String,
  rating: Number,
  isOpen: Boolean,
});

function onOrder() {
  console.log(`Ordering from ${props.name}`);
}
</script>

<style scoped>
.card { border: 1px solid #ddd; padding: 1rem; }
.badge-open { color: green; }
.badge-closed { color: red; }
</style>
```

- Vue SFCs combine template, script, and style in one file
- `v-if`, `v-for`, `v-model` directives
- Composition API (`setup`) is the modern approach (Options API still supported)

---

## Vue: reactivity system

```javascript
// Vue 3 Composition API
import { ref, computed, watch, onMounted } from 'vue';

export default {
  setup() {
    // Reactive state
    const items = ref([]);
    const searchQuery = ref('');

    // Computed property (auto-updates)
    const filteredItems = computed(() =>
      items.value.filter(item =>
        item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      )
    );

    // Watcher (react to changes)
    watch(searchQuery, (newVal, oldVal) => {
      console.log(`Search changed: ${oldVal} -> ${newVal}`);
    });

    // Lifecycle hook
    onMounted(async () => {
      const res = await fetch('/api/menu');
      items.value = await res.json();
    });

    return { items, searchQuery, filteredItems };
  },
};
```

> Vue's reactivity system is similar to React hooks but uses proxies under the hood. Changes to `.value` automatically trigger UI updates.

---

## When to choose which framework

| Scenario | Recommended | Why |
|----------|-------------|-----|
| Large enterprise app | Angular | Opinionated structure, DI, TypeScript enforced |
| Startup / rapid prototyping | React or Vue | Flexible, fast to start, large ecosystem |
| Existing jQuery codebase | Vue | Can be added incrementally to existing pages |
| Mobile + Web | React (React Native) | Code sharing between platforms |
| Small team, simple app | Vue | Gentle learning curve, good docs |
| Microservices UI (micro-frontends) | Any | All support module federation / web components |
| Sustain engineering | **Match existing stack** | Don't rewrite -- maintain what's there |

> As a sustain engineer, you will work with whatever framework the project uses. Focus on understanding patterns, not picking favorites.

---

## Component libraries: Bootstrap

```html
<!-- Bootstrap via CDN -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3/dist/css/bootstrap.min.css"
      rel="stylesheet">

<!-- Bootstrap card -->
<div class="card" style="width: 18rem;">
  <img src="burger.jpg" class="card-img-top" alt="Burger">
  <div class="card-body">
    <h5 class="card-title">Smash Burger</h5>
    <p class="card-text">Double patty with cheese</p>
    <span class="badge bg-success">$8.99</span>
    <button class="btn btn-primary">Add to Cart</button>
  </div>
</div>
```

| Bootstrap feature | Classes |
|-------------------|---------|
| Grid | `container`, `row`, `col-md-4` |
| Buttons | `btn btn-primary`, `btn-outline-danger` |
| Cards | `card`, `card-body`, `card-title` |
| Alerts | `alert alert-success`, `alert-danger` |
| Navbar | `navbar`, `navbar-expand-lg` |
| Forms | `form-control`, `form-label`, `form-select` |
| Utilities | `mt-3`, `p-2`, `d-flex`, `text-center` |

---

## Component libraries: Semantic UI

```html
<!-- Semantic UI card -->
<div class="ui card">
  <div class="image">
    <img src="burger.jpg" alt="Burger">
  </div>
  <div class="content">
    <a class="header">Smash Burger</a>
    <div class="meta">American</div>
    <div class="description">Double patty with cheese</div>
  </div>
  <div class="extra content">
    <span class="right floated">$8.99</span>
    <span><i class="star icon"></i> 4.5</span>
  </div>
</div>
```

| Library | Philosophy | Best for |
|---------|-----------|----------|
| **Bootstrap** | Utility-first classes | Rapid prototyping, admin panels |
| **Semantic UI** | Natural language classes | Readable HTML, human-friendly markup |
| **Tailwind CSS** | Atomic utility classes | Custom designs, no pre-built components |
| **Material UI** | Google Material Design | React apps following Material guidelines |
| **Ant Design** | Enterprise UI | Data-heavy dashboards, forms |

---

## Creating apps with CLI tools

```bash
# React (with Vite -- recommended)
npm create vite@latest foodexpress-react -- --template react
cd foodexpress-react && npm install && npm run dev

# Angular
npm install -g @angular/cli
ng new foodexpress-angular
cd foodexpress-angular && ng serve

# Vue (with Vite)
npm create vite@latest foodexpress-vue -- --template vue
cd foodexpress-vue && npm install && npm run dev
```

### Project structure comparison

```
React (Vite)          Angular               Vue (Vite)
src/                  src/app/              src/
  App.jsx               app.component.ts      App.vue
  main.jsx              app.module.ts         main.js
  components/           components/           components/
  assets/               services/             assets/
index.html            angular.json          index.html
vite.config.js        tsconfig.json         vite.config.js
package.json          package.json          package.json
```

---

## Designing and auto-generating code

### AI-assisted development tools

| Tool | What it does |
|------|-------------|
| **GitHub Copilot** | AI code completion in IDE (VS Code, JetBrains) |
| **Cursor** | AI-first code editor with chat and auto-edit |
| **v0 by Vercel** | Generate React + Tailwind UI from text prompts |
| **Claude** | Generate components, debug code, explain patterns |
| **Figma to Code** | Export Figma designs to HTML/CSS/React |

### Design-to-code workflow

```
1. Design in Figma/Sketch
   |
2. Export as component specifications
   |
3. Generate boilerplate with AI tool
   |
4. Review, test, and refine
   |
5. Integrate into existing codebase
```

> AI-generated code must be reviewed. It often produces working code with subtle issues: wrong accessibility, missing error handling, or non-standard patterns.

---

## SPA vs MPA vs SSR

| Architecture | Description | Example |
|-------------|-------------|---------|
| **SPA** (Single Page App) | One HTML page, JS handles all routing | Gmail, Trello |
| **MPA** (Multi Page App) | Server returns full HTML for each page | Wikipedia, StackOverflow |
| **SSR** (Server-Side Rendering) | Server renders first page, then SPA takes over | Next.js, Nuxt.js |
| **SSG** (Static Site Generation) | Pre-render all pages at build time | Docs sites, blogs |

```
User clicks link in SPA:
  1. JavaScript intercepts click
  2. Updates URL (History API)
  3. Fetches data from API
  4. Renders new view (no page reload)

User clicks link in MPA:
  1. Browser sends request to server
  2. Server returns full HTML page
  3. Browser loads and renders entire page
```

> Most modern web apps are SPAs built with React/Angular/Vue. Legacy apps tend to be MPAs with jQuery.

---

## Checkpoint: framework recognition

Look at these code snippets and identify the framework:

```
// Snippet A
<template>
  <div v-for="item in items" :key="item.id">
    {{ item.name }}
  </div>
</template>
```

```
// Snippet B
{items.map(item => (
  <div key={item.id}>{item.name}</div>
))}
```

```
// Snippet C
<div *ngFor="let item of items">
  {{ item.name }}
</div>
```

| Snippet | Framework | Key indicator |
|---------|-----------|---------------|
| A | Vue | `<template>`, `v-for`, `:key` |
| B | React | JSX, `.map()`, `key={}` |
| C | Angular | `*ngFor`, `let item of items` |

> In sustain work you will read unfamiliar code. Recognizing the framework from syntax patterns is an essential skill.

---

## MCQ practice

**Q1.** What does `async/await` provide over raw Promises?

| Option | Answer |
|--------|--------|
| A) Better performance | |
| B) Synchronous execution | |
| C) Cleaner syntax for Promise chains | Correct |
| D) Automatic error handling | |

**Q2.** Which method waits for ALL promises and never rejects?

| Option | Answer |
|--------|--------|
| A) `Promise.all()` | |
| B) `Promise.race()` | |
| C) `Promise.any()` | |
| D) `Promise.allSettled()` | Correct |

**Q3.** In React, what triggers a re-render?

| Option | Answer |
|--------|--------|
| A) Calling a regular function | |
| B) Calling `setState` / `useState` setter | Correct |
| C) Modifying a variable directly | |
| D) Using `console.log` | |

---

## MCQ practice (continued)

**Q4.** What is the main difference between `??` and `||`?

| Option | Answer |
|--------|--------|
| A) `??` is faster | |
| B) `??` only checks null/undefined; `||` checks all falsy | Correct |
| C) They are identical | |
| D) `||` works with objects, `??` does not | |

**Q5.** Which directive is Angular-specific?

| Option | Answer |
|--------|--------|
| A) `v-for` | |
| B) `*ngFor` | Correct |
| C) `.map()` | |
| D) `v-if` | |

**Q6.** What does `export default` allow?

| Option | Answer |
|--------|--------|
| A) Exporting multiple named values | |
| B) Exporting one value that can be imported with any name | Correct |
| C) Exporting to CommonJS only | |
| D) Making the export immutable | |

---

## Capsule project: FoodExpress restaurant listing

### Task

Build a **single-page restaurant listing** using any ONE framework (React, Vue, or vanilla JS with Bootstrap):

| Step | Requirement |
|------|------------|
| 1 | Scaffold the project with CLI tool or use CDN |
| 2 | Create a RestaurantCard component (name, cuisine, rating, status) |
| 3 | Render at least 4 restaurant cards from an array of data |
| 4 | Add a search/filter input that filters by name |
| 5 | Add a "View Menu" button that fetches mock data (use `setTimeout` to simulate) |
| 6 | Show loading state while "fetching" |
| 7 | Handle errors gracefully (show user-friendly message) |

### Acceptance criteria

- [ ] At least 4 restaurant cards rendered
- [ ] Search input filters cards in real-time
- [ ] Loading spinner shown during mock fetch
- [ ] Error message shown on failure
- [ ] No `console.log` in final code
- [ ] Responsive layout (works on mobile width)

---

## Guided lab: fix the FoodExpress SPA

| Step | Bug description |
|------|----------------|
| 01 | Fix: `fetch('/api/restaurants')` silently fails on 404 (no error shown to user) |
| 02 | Fix: Search filter does not reset when input is cleared |
| 03 | Fix: `async` function missing `try/catch` -- unhandled promise rejection |
| 04 | Fix: `import` statement uses wrong path (module not found) |
| 05 | Fix: Component re-renders infinitely (missing dependency array in `useEffect`) |
| 06 | Fix: Cart total shows `NaN` because quantity is a string from input |
| 07 | Add: Loading spinner during API calls |
| 08 | Add: AbortController timeout for slow API responses |

---

## Lab acceptance criteria

- [ ] Fetch errors are caught and displayed to the user
- [ ] Search filter works correctly (including empty input)
- [ ] All async functions have proper error handling
- [ ] Module imports resolve without errors
- [ ] No infinite re-render loops
- [ ] Cart total is always a valid number
- [ ] Loading state is visible during data fetching
- [ ] API requests time out after 5 seconds

---

## Key takeaways

| Concept | Remember |
|---------|----------|
| ES6+ | Destructuring, spread/rest, `??`, `?.` are daily tools |
| Async | `async/await` over raw Promise chains for readability |
| Fetch | Always check `response.ok` -- fetch does NOT throw on HTTP errors |
| Modules | Use ES Modules (`import`/`export`). CommonJS is legacy |
| React | Components + hooks (`useState`, `useEffect`). One-way data flow |
| Angular | Full framework. TypeScript required. DI and services |
| Vue | Progressive. SFCs with `<template>`, `<script>`, `<style>` |
| Component libs | Bootstrap (utility), Semantic UI (natural language) |
| FE Ops | Network tab, performance profiling, error tracking |
| Sustain rule | Match the existing stack. Don't rewrite -- maintain |

> **Next: Module 05 -- Java Programming (Part 1): Core Java, OOP basics, encapsulation**