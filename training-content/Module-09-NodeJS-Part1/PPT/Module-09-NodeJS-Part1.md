# Node.js (Part 1)
## Module 09 | Sustain Engineering Training | Day 10

**1 day | Workshop + guided lab**

---

## Agenda

| Session | Topics |
|---------|--------|
| Morning (1st half) | Intro to Node.js, Installing Node & NPM, Node Modules, Path Module, FS Module |
| Afternoon (2nd half) | Asynchronous JavaScript, Callbacks, Promises, Async/Await |

> Transitioning from Java to JavaScript -- server-side development with Node.js.

---

## What Is Node.js?

- **JavaScript runtime** built on Chrome's V8 engine
- Runs JavaScript **outside the browser** -- on servers, CLI tools, scripts
- Created by Ryan Dahl in 2009
- **Event-driven**, **non-blocking I/O** model

### Why Node.js for Sustain Engineering?

| Reason | Detail |
|--------|--------|
| Ubiquity | Many production systems use Node.js |
| NPM ecosystem | Largest package registry (2M+ packages) |
| Full-stack JS | Same language for frontend and backend |
| Fast prototyping | Quick to build APIs and microservices |
| Sustain relevance | You will maintain Node.js services in production |

---

## Node.js vs Browser JavaScript

| Feature | Browser | Node.js |
|---------|---------|---------|
| DOM manipulation | Yes (`document`, `window`) | No |
| File system access | No (security) | Yes (`fs` module) |
| Network servers | No | Yes (`http`, `net`) |
| Global object | `window` | `global` |
| Module system | ES Modules (`import`) | CommonJS (`require`) + ES Modules |
| Package manager | N/A | NPM, Yarn, pnpm |

```javascript
// This works in Node.js but NOT in the browser
const fs = require('fs');
const data = fs.readFileSync('menu.json', 'utf8');

// This works in the browser but NOT in Node.js
document.getElementById('menu');  // ReferenceError: document is not defined
```

---

## Node.js Architecture

### Single-Threaded Event Loop

```
        Incoming Requests
              |
        +-----v------+
        | Event Queue |
        +-----+------+
              |
        +-----v------+
        | Event Loop  |  <-- Single thread
        +-----+------+
              |
     +--------+--------+
     |                  |
  Blocking?          Non-blocking
     |                  |
  Thread Pool       Execute immediately
  (libuv, 4 threads)   |
     |               Return result
  Callback when done
```

### Key Insight

- Node.js is **single-threaded** for JavaScript execution
- I/O operations (file, network, DB) are delegated to the **thread pool**
- Results come back via **callbacks** or **promises**

---

## Installing Node.js and NPM

### Installation

```bash
# Check if already installed
node --version    # v20.x.x
npm --version     # 10.x.x

# Install via official website: https://nodejs.org
# LTS (Long Term Support) version recommended for production
```

### Node.js Version Manager (nvm)

```bash
# Install nvm (recommended for managing multiple versions)
# Linux/Mac:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Windows: use nvm-windows
# https://github.com/coreybutler/nvm-windows

# Usage
nvm install 20        # Install Node.js 20
nvm use 20            # Switch to Node.js 20
nvm list              # List installed versions
```

> **Sustain tip:** Different projects may require different Node versions. Always use `nvm`.

---

## Your First Node.js Program

### hello.js

```javascript
console.log('Hello from Node.js!');
console.log('Process ID:', process.pid);
console.log('Node version:', process.version);
console.log('Platform:', process.platform);
console.log('Current directory:', process.cwd());
```

### Run It

```bash
node hello.js
```

### Output

```
Hello from Node.js!
Process ID: 12345
Node version: v20.11.0
Platform: win32
Current directory: C:\projects\foodexpress
```

---

## NPM -- Node Package Manager

### What NPM Does

- **Installs** third-party packages (libraries)
- **Manages** project dependencies via `package.json`
- **Runs** scripts defined in `package.json`
- **Publishes** packages to the npm registry

### Initialize a Project

```bash
# Create a new project with package.json
npm init -y

# This creates package.json:
{
  "name": "foodexpress-restaurant-service",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

---

## Installing Packages

### Types of Dependencies

```bash
# Production dependency (needed at runtime)
npm install express
npm install mongoose

# Dev dependency (needed only during development)
npm install --save-dev nodemon
npm install --save-dev jest

# Global installation (CLI tools)
npm install -g nodemon
```

### package.json After Install

```json
{
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.6.3"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.7.0"
  }
}
```

### Version Syntax

| Prefix | Meaning | Example |
|--------|---------|---------|
| `^4.18.2` | Compatible (minor + patch) | 4.18.2 to < 5.0.0 |
| `~4.18.2` | Approximate (patch only) | 4.18.2 to < 4.19.0 |
| `4.18.2` | Exact version | Only 4.18.2 |

---

## node_modules and package-lock.json

### node_modules/

- Directory where all installed packages live
- Can be **very large** (hundreds of MB)
- **Never commit to Git** -- add to `.gitignore`

### package-lock.json

- Auto-generated file that locks exact dependency versions
- **Always commit** to Git -- ensures reproducible builds
- Prevents "works on my machine" issues

### .gitignore for Node.js Projects

```
node_modules/
.env
*.log
dist/
coverage/
```

### Reinstalling Dependencies

```bash
# On a fresh clone, install from package-lock.json
npm ci          # Clean install (faster, stricter than npm install)
npm install     # Also works, but may update lock file
```

---

## Node.js Module System -- CommonJS

### Creating a Module

```javascript
// menuItem.js
class MenuItem {
    constructor(id, name, price, category) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.category = category;
    }

    getDisplayPrice() {
        return `$${this.price.toFixed(2)}`;
    }
}

// Export for use by other files
module.exports = MenuItem;
```

### Using a Module

```javascript
// app.js
const MenuItem = require('./menuItem');

const pizza = new MenuItem('ITEM001', 'Margherita Pizza', 12.99, 'Italian');
console.log(pizza.getDisplayPrice());  // $12.99
```

---

## Module Export Patterns

### Single Export

```javascript
// logger.js
class Logger { /* ... */ }
module.exports = Logger;

// Usage
const Logger = require('./logger');
```

### Multiple Named Exports

```javascript
// utils.js
function formatCurrency(amount) {
    return `$${amount.toFixed(2)}`;
}

function generateId() {
    return `ORD-${Date.now()}`;
}

module.exports = { formatCurrency, generateId };

// Usage
const { formatCurrency, generateId } = require('./utils');
console.log(formatCurrency(12.5));   // $12.50
console.log(generateId());           // ORD-1690000000000
```

### exports Shorthand

```javascript
// Same as module.exports = { ... }
exports.formatCurrency = function(amount) { return `$${amount.toFixed(2)}`; };
exports.generateId = function() { return `ORD-${Date.now()}`; };
```

---

## ES Modules in Node.js

### Enabling ES Modules

```json
// package.json -- add "type": "module"
{
  "type": "module"
}
```

### ES Module Syntax

```javascript
// menuItem.mjs (or .js with "type": "module")
export class MenuItem {
    constructor(id, name, price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }
}

export function formatPrice(price) {
    return `$${price.toFixed(2)}`;
}

// Default export
export default class Restaurant {
    constructor(name) { this.name = name; }
}
```

```javascript
// app.mjs
import Restaurant, { MenuItem, formatPrice } from './menuItem.mjs';

const r = new Restaurant('FoodExpress');
const item = new MenuItem('001', 'Pizza', 12.99);
```

### CommonJS vs ES Modules

| Feature | CommonJS | ES Modules |
|---------|----------|------------|
| Syntax | `require()` / `module.exports` | `import` / `export` |
| Loading | Synchronous | Asynchronous |
| File extension | `.js` (default) | `.mjs` or `"type": "module"` |
| Legacy support | Full | Node 12+ |

---

## Built-in Modules Overview

Node.js ships with many built-in modules -- no `npm install` needed.

| Module | Purpose | Common Use |
|--------|---------|------------|
| `path` | File path utilities | Join, resolve, parse paths |
| `fs` | File system operations | Read, write, delete files |
| `http` | HTTP server/client | Create web servers |
| `url` | URL parsing | Parse and format URLs |
| `os` | Operating system info | CPU, memory, hostname |
| `events` | Event emitter | Custom event handling |
| `crypto` | Cryptography | Hashing, encryption |
| `util` | Utility functions | Promisify, inspect |
| `child_process` | Run system commands | Execute shell commands |

```javascript
// No install needed -- just require
const path = require('path');
const fs = require('fs');
const os = require('os');
```

---

## Path Module

### Why Use path?

- File paths differ across operating systems
- Windows: `C:\Users\data\file.txt`
- Linux/Mac: `/home/user/data/file.txt`
- `path` module handles this **cross-platform**

```javascript
const path = require('path');

// Join path segments (handles OS separators)
const filePath = path.join(__dirname, 'data', 'menu.json');
// Windows: C:\projects\foodexpress\data\menu.json
// Linux:   /projects/foodexpress/data/menu.json

// Resolve to absolute path
const abs = path.resolve('data', 'menu.json');

// Parse a path
const parsed = path.parse('/data/menu.json');
console.log(parsed);
// { root: '/', dir: '/data', base: 'menu.json', ext: '.json', name: 'menu' }

// Get parts
console.log(path.basename('/data/menu.json'));     // menu.json
console.log(path.dirname('/data/menu.json'));       // /data
console.log(path.extname('/data/menu.json'));       // .json
```

---

## Path Module -- Key Methods

| Method | Input | Output |
|--------|-------|--------|
| `path.join('a', 'b', 'c.txt')` | segments | `a/b/c.txt` or `a\b\c.txt` |
| `path.resolve('data', 'file.txt')` | segments | Absolute path |
| `path.basename('/a/b/c.txt')` | path | `c.txt` |
| `path.dirname('/a/b/c.txt')` | path | `/a/b` |
| `path.extname('file.json')` | path | `.json` |
| `path.parse('/a/b/c.txt')` | path | `{ root, dir, base, ext, name }` |
| `path.isAbsolute('/data')` | path | `true` |

### Special Variables

```javascript
console.log(__dirname);   // Directory of current file
console.log(__filename);  // Full path of current file

// Example: read a config file relative to this script
const configPath = path.join(__dirname, 'config', 'database.json');
```

> **Sustain tip:** Always use `path.join()` instead of string concatenation for file paths.

---

## FS Module -- File System

### Reading Files

```javascript
const fs = require('fs');
const path = require('path');

// Synchronous read (blocks the event loop!)
const data = fs.readFileSync(path.join(__dirname, 'menu.json'), 'utf8');
const menu = JSON.parse(data);
console.log(menu);

// Asynchronous read (callback-based -- non-blocking)
fs.readFile(path.join(__dirname, 'menu.json'), 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading file:', err.message);
        return;
    }
    const menu = JSON.parse(data);
    console.log(menu);
});
```

### Sync vs Async

| Sync (`readFileSync`) | Async (`readFile`) |
|-----------------------|-------------------|
| Blocks event loop | Non-blocking |
| Simpler code | Requires callback/promise |
| OK for startup config | **Required** for production I/O |
| Returns data directly | Data via callback |

---

## FS Module -- Writing Files

```javascript
const fs = require('fs');
const path = require('path');

const menuData = [
    { id: 'ITEM001', name: 'Margherita Pizza', price: 12.99, category: 'Italian' },
    { id: 'ITEM002', name: 'Chicken Tikka', price: 14.99, category: 'Indian' },
    { id: 'ITEM003', name: 'Sushi Roll', price: 16.99, category: 'Japanese' }
];

// Write file (creates or overwrites)
fs.writeFileSync(
    path.join(__dirname, 'data', 'menu.json'),
    JSON.stringify(menuData, null, 2),  // Pretty print with 2-space indent
    'utf8'
);

// Append to file
fs.appendFileSync(
    path.join(__dirname, 'logs', 'app.log'),
    `[${new Date().toISOString()}] Server started\n`
);

// Async write
fs.writeFile('output.txt', 'Hello', 'utf8', (err) => {
    if (err) console.error('Write failed:', err.message);
    else console.log('File written successfully');
});
```

---

## FS Module -- Directory & File Operations

```javascript
const fs = require('fs');

// Check if file/directory exists
if (fs.existsSync('data/menu.json')) {
    console.log('File exists');
}

// Create directory
fs.mkdirSync('data/backups', { recursive: true });

// List directory contents
const files = fs.readdirSync('data');
console.log(files);  // ['menu.json', 'orders.json', 'backups']

// Get file info
const stats = fs.statSync('data/menu.json');
console.log('Size:', stats.size, 'bytes');
console.log('Is file:', stats.isFile());
console.log('Is directory:', stats.isDirectory());
console.log('Modified:', stats.mtime);

// Delete file
fs.unlinkSync('data/temp.json');

// Delete directory
fs.rmdirSync('data/backups');          // Empty dir only
fs.rmSync('data/backups', { recursive: true });  // Non-empty dir
```

---

## FoodExpress: Restaurant Data Manager

```javascript
const fs = require('fs');
const path = require('path');

class RestaurantDataManager {
    constructor(dataDir) {
        this.dataDir = dataDir;
        // Ensure data directory exists
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
        }
    }

    getFilePath(filename) {
        return path.join(this.dataDir, filename);
    }

    loadRestaurants() {
        const filePath = this.getFilePath('restaurants.json');
        if (!fs.existsSync(filePath)) return [];
        const data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
    }

    saveRestaurants(restaurants) {
        const filePath = this.getFilePath('restaurants.json');
        fs.writeFileSync(filePath, JSON.stringify(restaurants, null, 2), 'utf8');
    }

    addRestaurant(restaurant) {
        const restaurants = this.loadRestaurants();
        restaurant.id = `REST-${Date.now()}`;
        restaurant.createdAt = new Date().toISOString();
        restaurants.push(restaurant);
        this.saveRestaurants(restaurants);
        return restaurant;
    }

    findByCategory(category) {
        const restaurants = this.loadRestaurants();
        return restaurants.filter(r => r.category === category);
    }
}

module.exports = RestaurantDataManager;
```

---

## Asynchronous JavaScript -- The Problem

### Why Async?

```javascript
// Imagine this runs synchronously...
const data = db.query('SELECT * FROM restaurants');  // Takes 500ms
console.log(data);  // Waits 500ms before this line runs

// In that 500ms, Node.js can't handle ANY other requests
// With 1000 concurrent users, each waiting 500ms = terrible performance
```

### The Solution: Non-Blocking I/O

```javascript
// Node.js way -- non-blocking
db.query('SELECT * FROM restaurants', (err, data) => {
    console.log(data);  // Runs when data is ready
});
// This line runs IMMEDIATELY -- doesn't wait for DB
console.log('Query sent, continuing...');
```

### Blocking vs Non-Blocking

| Blocking | Non-Blocking |
|----------|-------------|
| Waits for operation to complete | Continues immediately |
| Simple, sequential code | Requires callbacks/promises |
| Wastes CPU time waiting | CPU handles other work |
| Bad for servers | Great for servers |

---

## Callbacks

### What Is a Callback?

A function passed as an argument, to be called when an operation completes.

```javascript
// setTimeout -- simplest callback example
console.log('1. Before timeout');

setTimeout(() => {
    console.log('2. Inside timeout (after 2 seconds)');
}, 2000);

console.log('3. After timeout call');

// Output:
// 1. Before timeout
// 3. After timeout call
// 2. Inside timeout (after 2 seconds)
```

### Node.js Error-First Callback Convention

```javascript
const fs = require('fs');

fs.readFile('menu.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Failed to read:', err.message);
        return;
    }
    // err is null -- success!
    console.log('Menu data:', data);
});
```

> **Convention:** First argument is always `err`. If null, operation succeeded.

---

## Callback Hell

### The Problem

```javascript
// Read config, then connect DB, then query, then process...
fs.readFile('config.json', 'utf8', (err, config) => {
    if (err) return console.error(err);
    db.connect(JSON.parse(config).dbUrl, (err, conn) => {
        if (err) return console.error(err);
        conn.query('SELECT * FROM restaurants', (err, restaurants) => {
            if (err) return console.error(err);
            restaurants.forEach(r => {
                conn.query(`SELECT * FROM menu WHERE restaurant_id = ${r.id}`, (err, menu) => {
                    if (err) return console.error(err);
                    console.log(r.name, menu);
                    // More nesting... "Pyramid of doom"
                });
            });
        });
    });
});
```

### Problems with Callback Hell

- Hard to read (deep nesting)
- Hard to handle errors consistently
- Hard to add sequential or parallel logic
- Hard to debug (stack traces are confusing)

---

## Promises -- The Solution

### What Is a Promise?

An object representing the **eventual completion or failure** of an async operation.

```
Promise States:
  PENDING  ----> FULFILLED (resolved with value)
     |
     +--------> REJECTED (rejected with error)
```

### Creating a Promise

```javascript
function readMenuFile(filePath) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                reject(err);       // Operation failed
            } else {
                resolve(data);     // Operation succeeded
            }
        });
    });
}
```

### Using a Promise

```javascript
readMenuFile('menu.json')
    .then(data => {
        console.log('Menu:', JSON.parse(data));
    })
    .catch(err => {
        console.error('Error:', err.message);
    });
```

---

## Promise Chaining

### Solving Callback Hell with Promises

```javascript
readConfig('config.json')
    .then(config => connectDB(config.dbUrl))
    .then(conn => conn.query('SELECT * FROM restaurants'))
    .then(restaurants => {
        console.log('Restaurants:', restaurants);
        return restaurants;
    })
    .catch(err => {
        console.error('Error at any step:', err.message);
    })
    .finally(() => {
        console.log('Cleanup: close connections');
    });
```

### Key Rules

| Rule | Example |
|------|---------|
| `.then()` returns a new Promise | Enables chaining |
| Return a value from `.then()` | Next `.then()` receives it |
| Return a Promise from `.then()` | Next `.then()` waits for it |
| `.catch()` handles any error in the chain | Single error handler |
| `.finally()` runs regardless | Cleanup code |

---

## Promise Utility Methods

### Promise.all -- Run in Parallel

```javascript
// Fetch multiple restaurants simultaneously
const promises = [
    fetchRestaurant('REST001'),
    fetchRestaurant('REST002'),
    fetchRestaurant('REST003')
];

Promise.all(promises)
    .then(results => {
        console.log('All restaurants:', results);
        // results is an array: [rest1, rest2, rest3]
    })
    .catch(err => {
        // Fails if ANY promise fails
        console.error('One failed:', err.message);
    });
```

### Promise.allSettled -- All Results (No Short-Circuit)

```javascript
Promise.allSettled(promises)
    .then(results => {
        results.forEach(result => {
            if (result.status === 'fulfilled') {
                console.log('Success:', result.value);
            } else {
                console.log('Failed:', result.reason.message);
            }
        });
    });
```

---

## More Promise Utilities

### Promise.race -- First to Complete

```javascript
// Timeout pattern
const fetchData = fetch('https://api.foodexpress.com/restaurants');
const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error('Request timed out')), 5000)
);

Promise.race([fetchData, timeout])
    .then(data => console.log('Got data:', data))
    .catch(err => console.error(err.message));  // 'Request timed out'
```

### Promise.any -- First to Succeed

```javascript
// Try multiple API endpoints, use whichever responds first
Promise.any([
    fetch('https://api-primary.foodexpress.com/menu'),
    fetch('https://api-backup.foodexpress.com/menu'),
    fetch('https://api-cdn.foodexpress.com/menu')
])
.then(response => console.log('Got response from fastest server'))
.catch(err => console.error('All servers failed'));
```

| Method | Resolves When | Rejects When |
|--------|--------------|--------------|
| `Promise.all` | All succeed | Any fails |
| `Promise.allSettled` | All complete | Never rejects |
| `Promise.race` | First completes | First completes (if rejected) |
| `Promise.any` | First succeeds | All fail |

---

## Async/Await

### The Modern Way

`async/await` is **syntactic sugar** over Promises. Makes async code look synchronous.

```javascript
// Promise chain version
function getRestaurantMenu(restaurantId) {
    return fetchRestaurant(restaurantId)
        .then(restaurant => fetchMenu(restaurant.menuId))
        .then(menu => menu.items)
        .catch(err => console.error(err));
}

// Async/await version (same behavior, cleaner syntax)
async function getRestaurantMenu(restaurantId) {
    try {
        const restaurant = await fetchRestaurant(restaurantId);
        const menu = await fetchMenu(restaurant.menuId);
        return menu.items;
    } catch (err) {
        console.error(err);
    }
}
```

### Rules

- `async` keyword before function declaration
- `await` can only be used inside `async` functions
- `await` pauses execution until the Promise resolves
- `async` functions always return a Promise

---

## Async/Await Error Handling

### try/catch Pattern

```javascript
async function loadRestaurantData(id) {
    try {
        const restaurant = await fetchRestaurant(id);
        const menu = await fetchMenu(restaurant.menuId);
        const reviews = await fetchReviews(id);

        return {
            restaurant,
            menu: menu.items,
            rating: reviews.average
        };
    } catch (err) {
        if (err.code === 'NOT_FOUND') {
            console.error(`Restaurant ${id} not found`);
            return null;
        }
        throw err;  // Re-throw unexpected errors
    } finally {
        console.log(`Finished loading data for ${id}`);
    }
}
```

### Common Mistake: Forgetting await

```javascript
async function badExample() {
    const data = fetchRestaurant('REST001');  // Missing await!
    console.log(data);  // Prints: Promise { <pending> }  -- NOT the data!
}

async function goodExample() {
    const data = await fetchRestaurant('REST001');
    console.log(data);  // Prints actual restaurant data
}
```

---

## Parallel Execution with Async/Await

### Sequential (Slow)

```javascript
async function loadDashboard() {
    const restaurants = await fetchRestaurants();    // Wait...
    const orders = await fetchOrders();              // Wait...
    const reviews = await fetchReviews();            // Wait...
    // Total time: sum of all three
    return { restaurants, orders, reviews };
}
```

### Parallel (Fast)

```javascript
async function loadDashboard() {
    const [restaurants, orders, reviews] = await Promise.all([
        fetchRestaurants(),
        fetchOrders(),
        fetchReviews()
    ]);
    // Total time: maximum of the three
    return { restaurants, orders, reviews };
}
```

> **Sustain tip:** If operations are independent, always run them in parallel with `Promise.all`.

---

## FS Promises API

### Modern Approach (Node 10+)

```javascript
const fs = require('fs').promises;
// or: const { readFile, writeFile } = require('fs').promises;
const path = require('path');

async function loadMenu() {
    try {
        const data = await fs.readFile(
            path.join(__dirname, 'data', 'menu.json'),
            'utf8'
        );
        return JSON.parse(data);
    } catch (err) {
        if (err.code === 'ENOENT') {
            console.log('Menu file not found, returning empty array');
            return [];
        }
        throw err;
    }
}

async function saveMenu(menu) {
    const filePath = path.join(__dirname, 'data', 'menu.json');
    await fs.writeFile(filePath, JSON.stringify(menu, null, 2), 'utf8');
    console.log('Menu saved successfully');
}
```

> **Best practice:** Use `fs.promises` (async) instead of `fs.readFileSync` (sync) in production code.

---

## FoodExpress: Async Restaurant Service

```javascript
const fs = require('fs').promises;
const path = require('path');

class RestaurantService {
    constructor(dataDir) {
        this.dataDir = dataDir;
        this.filePath = path.join(dataDir, 'restaurants.json');
    }

    async loadAll() {
        try {
            const data = await fs.readFile(this.filePath, 'utf8');
            return JSON.parse(data);
        } catch (err) {
            if (err.code === 'ENOENT') return [];
            throw err;
        }
    }

    async save(restaurants) {
        await fs.writeFile(this.filePath, JSON.stringify(restaurants, null, 2));
    }

    async addRestaurant(restaurant) {
        const restaurants = await this.loadAll();
        restaurant.id = `REST-${Date.now()}`;
        restaurants.push(restaurant);
        await this.save(restaurants);
        return restaurant;
    }

    async findById(id) {
        const restaurants = await this.loadAll();
        const restaurant = restaurants.find(r => r.id === id);
        if (!restaurant) throw new Error(`Restaurant ${id} not found`);
        return restaurant;
    }

    async updateRating(id, newRating) {
        const restaurants = await this.loadAll();
        const index = restaurants.findIndex(r => r.id === id);
        if (index === -1) throw new Error(`Restaurant ${id} not found`);
        restaurants[index].rating = newRating;
        await this.save(restaurants);
        return restaurants[index];
    }
}

module.exports = RestaurantService;
```

---

## Error Handling Best Practices

### Custom Error Classes

```javascript
class AppError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.name = this.constructor.name;
        this.statusCode = statusCode;
    }
}

class NotFoundError extends AppError {
    constructor(resource, id) {
        super(`${resource} with id ${id} not found`, 404);
    }
}

class ValidationError extends AppError {
    constructor(message) {
        super(message, 400);
    }
}

// Usage
async function getRestaurant(id) {
    const restaurant = await db.findById(id);
    if (!restaurant) {
        throw new NotFoundError('Restaurant', id);
    }
    return restaurant;
}
```

---

## Process and Environment Variables

```javascript
// Access environment variables
const port = process.env.PORT || 3000;
const dbUrl = process.env.DATABASE_URL || 'mongodb://localhost:27017/foodexpress';
const nodeEnv = process.env.NODE_ENV || 'development';

console.log(`Running in ${nodeEnv} mode on port ${port}`);

// Exit handling
process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
    process.exit(1);
});

process.on('unhandledRejection', (reason) => {
    console.error('Unhandled Rejection:', reason);
    process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received. Shutting down gracefully...');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});
```

> **Sustain tip:** Always handle `uncaughtException` and `unhandledRejection` in production Node.js apps.

---

## Event Emitter

```javascript
const EventEmitter = require('events');

class OrderEvents extends EventEmitter {}

const orderEvents = new OrderEvents();

// Register listeners
orderEvents.on('orderPlaced', (order) => {
    console.log(`New order: ${order.id} from ${order.customerName}`);
});

orderEvents.on('orderPlaced', (order) => {
    // Send notification (another listener for same event)
    console.log(`Notification sent to restaurant for order ${order.id}`);
});

orderEvents.on('orderDelivered', (order) => {
    console.log(`Order ${order.id} delivered successfully`);
});

// Emit events
orderEvents.emit('orderPlaced', {
    id: 'ORD-001',
    customerName: 'John',
    items: ['Pizza', 'Coke']
});

orderEvents.emit('orderDelivered', { id: 'ORD-001' });
```

> Many Node.js core modules (http, fs streams) extend EventEmitter.

---

## Lab: FoodExpress Restaurant File Manager

### Objective

Build a Node.js application that manages restaurant and menu data using the file system.

### Tasks

1. **Project Setup:**
   - Initialize with `npm init`
   - Create directory structure: `data/`, `src/`, `src/models/`, `src/services/`

2. **Restaurant Model (`src/models/restaurant.js`):**
   - Export a class with: id, name, category, rating, menu (array)
   - Validation: name required, rating 0-5, category from allowed list

3. **Data Service (`src/services/dataService.js`):**
   - `loadRestaurants()` -- async, reads from `data/restaurants.json`
   - `saveRestaurants()` -- async, writes to `data/restaurants.json`
   - `addRestaurant()`, `findById()`, `findByCategory()`, `updateRating()`
   - Use `fs.promises` and `path.join()` throughout

4. **Menu Manager (`src/services/menuService.js`):**
   - Add/remove menu items for a restaurant
   - Search menu items by price range
   - Use async/await for all operations

---

## Lab: Async Operations Challenge

### Tasks (continued)

5. **App Entry Point (`src/app.js`):**
   - Load restaurant data on startup
   - Display menu with options: list, add, search, update, quit
   - Handle errors gracefully with try/catch

6. **Bonus: Parallel Operations**
   - Load data from multiple JSON files simultaneously using `Promise.all`
   - Implement a backup function that copies data files to `data/backups/`
   - Add logging with timestamps to `logs/app.log`

### Acceptance Criteria

- [ ] All file operations use `fs.promises` (not sync)
- [ ] All paths use `path.join()` (no string concatenation)
- [ ] Error handling on every async operation
- [ ] `ENOENT` errors handled gracefully (file not found = empty array)
- [ ] No callback hell -- use async/await throughout
- [ ] No unhandled promise rejections

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Node.js | JavaScript runtime on V8; event-driven, non-blocking I/O |
| NPM | Package manager; `package.json` for deps, `package-lock.json` for reproducibility |
| Modules | CommonJS (`require/module.exports`) and ES Modules (`import/export`) |
| Path module | Cross-platform path handling; always use `path.join()` |
| FS module | File operations; prefer `fs.promises` over sync methods |
| Callbacks | Error-first convention; avoid deep nesting (callback hell) |
| Promises | Objects representing async results; `.then()/.catch()/.finally()` |
| Promise.all | Run independent operations in parallel |
| Async/Await | Syntactic sugar over Promises; cleaner, readable async code |
| Error handling | try/catch with async/await; custom error classes |
| Event Emitter | Pub/sub pattern; core of Node.js architecture |

> **Next: Module 10 -- Node.js Part 2 (Express.js, REST APIs, MongoDB)**
