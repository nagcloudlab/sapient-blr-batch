# Capsule Project: Node.js
## Module 11 | Sustain Engineering Training | Day 12

**1 day | Capsule project + presentation + MCQ**

---

## Agenda -- Full Day Schedule

| # | Activity |
|---|-------|
| 01 | Project briefing & architecture review |
| 02 | Team formation & repo setup |
| 03 | Sprint 1: Core bug fixes (Tickets 1-2) |
| 04 | Lunch break |
| 05 | Sprint 2: Feature ticket + integration (Tickets 3-4) |
| 06 | Code freeze & prepare presentation |
| 07 | Team presentations & peer review |
| 08 | MCQ assessment (Modules 09-11) |

---

## What Is a Capsule Project?

- A **time-boxed**, hands-on project that consolidates learning from Modules 09-10
- Simulates real sustain engineering work:
  - Read and understand an existing Node.js codebase
  - Fix production bugs under time pressure
  - Add features requested by stakeholders
  - Present root-cause analysis to the team

### Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Code correctness & functionality | 30% |
| Code quality & best practices | 20% |
| Bug fixes completed | 20% |
| Presentation & communication | 15% |
| MCQ score | 15% |

---

## Project: FoodExpress Restaurant Service

### Business Context

FoodExpress needs a **REST API for managing restaurants** built with:

- **Node.js** + **Express.js** for the API layer
- **MongoDB** for data persistence
- **Middleware** for logging, validation, error handling
- **Environment-based config** for dev/staging/prod

### The Problem

The previous team left the Restaurant Service half-built with critical bugs. The mobile app team is blocked. You have **one day** to stabilize it.

---

## Architecture Overview

```
FoodExpress Restaurant Service
+----------------------------------+
|        Express.js Server         |
|  +----------------------------+  |
|  |  Middleware Layer           |  |
|  |  - CORS, JSON Parser       |  |
|  |  - Auth Token Validation   |  |
|  |  - Request Logger          |  |
|  |  - Error Handler           |  |
|  +----------------------------+  |
|  |  Route Layer               |  |
|  |  - /api/restaurants        |  |
|  |  - /api/menus              |  |
|  |  - /api/health             |  |
|  +----------------------------+  |
|  |  Service Layer             |  |
|  |  - RestaurantService       |  |
|  |  - MenuService             |  |
|  +----------------------------+  |
|  |  Data Access Layer         |  |
|  |  - MongoDB Driver          |  |
|  +----------------------------+  |
+----------------------------------+
```

---

## Data Model

### Restaurant Document

```javascript
{
  _id: ObjectId("..."),
  name: "Pizza Palace",
  cuisine: "Italian",
  address: {
    street: "123 Main St",
    city: "Bangalore",
    zipCode: "560001"
  },
  rating: 4.5,
  isActive: true,
  deliveryRadius: 5,  // in km
  menu: [
    { itemId: "IT001", name: "Margherita", price: 299, category: "Pizza" },
    { itemId: "IT002", name: "Pasta Alfredo", price: 349, category: "Pasta" }
  ],
  createdAt: ISODate("2026-01-15T10:30:00Z"),
  updatedAt: ISODate("2026-07-20T14:00:00Z")
}
```

---

## API Endpoints

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/restaurants` | List all active restaurants | Buggy |
| GET | `/api/restaurants/:id` | Get restaurant by ID | Buggy |
| POST | `/api/restaurants` | Create new restaurant | Buggy |
| PUT | `/api/restaurants/:id` | Update restaurant | Working |
| DELETE | `/api/restaurants/:id` | Soft-delete restaurant | Missing |
| GET | `/api/restaurants/:id/menu` | Get restaurant menu | Missing |
| GET | `/api/health` | Health check endpoint | Working |

---

## Ticket Board -- Sprint Backlog

| Ticket | Type | Priority | Summary |
|--------|------|----------|---------|
| FOOD-31 | BUG | P1 | GET /restaurants returns 500 -- async/await missing |
| FOOD-32 | BUG | P1 | POST /restaurants silently fails -- validation crash |
| FOOD-33 | FEATURE | P2 | Add soft-delete and menu retrieval endpoints |
| FOOD-34 | BUG | P2 | Environment config not loading -- hardcoded values |

---

## Ticket FOOD-31: GET /restaurants Returns 500

### Symptom
- Mobile team reports `500 Internal Server Error` on restaurant listing
- Server console shows `UnhandledPromiseRejectionWarning`

### Investigation Hints
1. Check `routes/restaurants.js` -- is the route handler async?
2. Check `services/restaurantService.js` -- what does `getAll()` return?
3. Does the error handler middleware catch async errors?

### Acceptance Criteria
- [ ] `GET /api/restaurants` returns 200 with array of restaurants
- [ ] `GET /api/restaurants?cuisine=Italian` filters by cuisine
- [ ] Async errors are properly caught and forwarded to error handler

---

## Ticket FOOD-32: POST /restaurants Silently Fails

### Symptom
- Creating a restaurant returns `201 Created` but no document in MongoDB
- No error message in logs
- Postman shows empty response body

### Investigation Hints
1. Check the `createRestaurant()` service method
2. Is the request body being passed correctly?
3. Check if validation middleware blocks the request silently

### Acceptance Criteria
- [ ] `POST /api/restaurants` creates a document in MongoDB
- [ ] Response includes the created restaurant with `_id`
- [ ] Invalid requests return 400 with error details

---

## Ticket FOOD-33: Add Missing Endpoints

### Requirements
- Add `DELETE /api/restaurants/:id` (soft-delete: set `isActive: false`)
- Add `GET /api/restaurants/:id/menu` (return menu array for a restaurant)

### Acceptance Criteria
- [ ] DELETE returns 200 with `{ message: "Restaurant deactivated" }`
- [ ] Deleted restaurants no longer appear in GET listing
- [ ] Menu endpoint returns array of menu items
- [ ] Non-existent restaurant returns 404

---

## Ticket FOOD-34: Environment Config Not Loading

### Symptom
- `PORT`, `MONGODB_URI`, and `DB_NAME` are hardcoded in `server.js`
- Deployment to staging fails because it uses production database
- `.env` file exists but values are ignored

### Investigation Hints
1. Is `dotenv` installed and required?
2. Where is `require('dotenv').config()` called relative to `process.env` usage?
3. Check if `.env` file has the correct variable names

### Acceptance Criteria
- [ ] Server reads config from `.env` file
- [ ] Default values used when `.env` is missing
- [ ] No hardcoded connection strings in source code

---

## Codebase Structure

```
restaurant-service/
+-- server.js              # Express app setup (bugs here)
+-- .env                   # Environment variables
+-- package.json
+-- routes/
|   +-- restaurants.js     # Route handlers (bugs here)
|   +-- menus.js           # Menu routes (to be created)
+-- services/
|   +-- restaurantService.js  # Business logic (bugs here)
|   +-- menuService.js        # Menu logic (to be created)
+-- middleware/
|   +-- errorHandler.js    # Global error handler
|   +-- validateRequest.js # Request validation
|   +-- logger.js          # Request logging
+-- db/
|   +-- connection.js      # MongoDB connection
|   +-- seed.js            # Test data seeder
+-- config/
|   +-- index.js           # Config loader (bug here)
+-- tests/
|   +-- restaurants.test.js
```

---

## Sprint 1: Bug Fix Strategy

### Approach for Each Bug

1. **Reproduce** -- Use Postman or curl to confirm the bug
2. **Isolate** -- Add `console.log` statements to narrow the location
3. **Root-Cause** -- Identify exactly what is wrong
4. **Fix** -- Apply the minimal correct fix
5. **Test** -- Verify the fix and check for regressions

### Debugging Node.js

```bash
# Run with verbose logging
DEBUG=express:* node server.js

# Run with Node.js inspector
node --inspect server.js
# Open chrome://inspect in Chrome

# Quick test with curl
curl -X GET http://localhost:3000/api/restaurants
curl -X POST http://localhost:3000/api/restaurants \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "cuisine": "Indian"}'
```

---

## Common Node.js Bug Patterns

| Bug Pattern | Example | Fix |
|-------------|---------|-----|
| Missing `await` | `const data = db.find()` | `const data = await db.find()` |
| Unhandled promise | `app.get('/', async (req, res) => { ... })` | Wrap in try/catch or use express-async-errors |
| Wrong `this` context | `class.method` as callback loses `this` | Use arrow function or `.bind(this)` |
| Middleware order | Body parser after routes | Move `app.use(express.json())` before routes |
| Missing `next()` call | Custom middleware blocks request | Call `next()` to pass control |
| Port conflict | `EADDRINUSE` error | Kill process or use different port |

---

## Async/Await Error Handling in Express

### The Problem

```javascript
// Express does NOT catch async errors automatically
app.get('/restaurants', async (req, res) => {
  const data = await restaurantService.getAll(); // throws!
  res.json(data); // never reached
  // Express returns 500 with no useful message
});
```

### The Solution

```javascript
// Option 1: Try/Catch
app.get('/restaurants', async (req, res, next) => {
  try {
    const data = await restaurantService.getAll();
    res.json(data);
  } catch (err) {
    next(err); // forward to error handler
  }
});

// Option 2: Wrapper function
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

app.get('/restaurants', asyncHandler(async (req, res) => {
  const data = await restaurantService.getAll();
  res.json(data);
}));
```

---

## MongoDB Connection Best Practices

### Singleton Pattern

```javascript
// db/connection.js
const { MongoClient } = require('mongodb');

let db = null;

async function connect(uri, dbName) {
  if (db) return db;
  const client = await MongoClient.connect(uri);
  db = client.db(dbName);
  console.log(`Connected to ${dbName}`);
  return db;
}

function getDb() {
  if (!db) throw new Error('Database not connected');
  return db;
}

module.exports = { connect, getDb };
```

### Common Mistake

```javascript
// BAD: Creates new connection for every request
async function getRestaurants() {
  const client = await MongoClient.connect(uri);
  const db = client.db('foodexpress');
  // Connection never closed = connection leak!
}
```

---

## Input Validation Middleware

```javascript
// middleware/validateRequest.js
function validateRestaurant(req, res, next) {
  const { name, cuisine, address } = req.body;
  const errors = [];

  if (!name || typeof name !== 'string') {
    errors.push('name is required and must be a string');
  }
  if (!cuisine || typeof cuisine !== 'string') {
    errors.push('cuisine is required and must be a string');
  }
  if (!address || !address.city) {
    errors.push('address with city is required');
  }

  if (errors.length > 0) {
    return res.status(400).json({ errors });
  }
  next();
}

module.exports = { validateRestaurant };
```

---

## Error Handler Middleware

```javascript
// middleware/errorHandler.js
function errorHandler(err, req, res, next) {
  console.error(`[ERROR] ${err.message}`);
  console.error(err.stack);

  // MongoDB duplicate key error
  if (err.code === 11000) {
    return res.status(409).json({
      error: 'Duplicate entry',
      field: Object.keys(err.keyPattern)[0]
    });
  }

  // Validation error
  if (err.name === 'ValidationError') {
    return res.status(400).json({ error: err.message });
  }

  // Default
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error'
  });
}

// IMPORTANT: Must have 4 parameters (err, req, res, next)
// Express identifies error handlers by the 4-param signature
module.exports = errorHandler;
```

---

## Sprint 2: Feature Development

### Soft Delete Pattern

```javascript
// Instead of removing the document:
await db.collection('restaurants').deleteOne({ _id: id });

// Mark as inactive (preserves data for auditing):
await db.collection('restaurants').updateOne(
  { _id: new ObjectId(id) },
  { $set: { isActive: false, deletedAt: new Date() } }
);

// All queries filter by isActive:
await db.collection('restaurants')
  .find({ isActive: true })
  .toArray();
```

---

## Environment Configuration

### Correct Pattern

```javascript
// config/index.js
require('dotenv').config(); // MUST be first!

module.exports = {
  port: process.env.PORT || 3000,
  mongoUri: process.env.MONGODB_URI || 'mongodb://localhost:27017',
  dbName: process.env.DB_NAME || 'foodexpress',
  nodeEnv: process.env.NODE_ENV || 'development'
};
```

### .env File

```
PORT=3000
MONGODB_URI=mongodb://localhost:27017
DB_NAME=foodexpress
NODE_ENV=development
```

### Common Mistake

```javascript
// BAD: Using process.env BEFORE dotenv.config()
const port = process.env.PORT; // undefined!
require('dotenv').config();    // too late
```

---

## Testing with Postman/curl

### Test Sequence

```bash
# 1. Health check
curl http://localhost:3000/api/health

# 2. Create a restaurant
curl -X POST http://localhost:3000/api/restaurants \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Spice Garden",
    "cuisine": "Indian",
    "address": { "street": "45 MG Road", "city": "Bangalore", "zipCode": "560001" },
    "rating": 4.2,
    "deliveryRadius": 7
  }'

# 3. List restaurants
curl http://localhost:3000/api/restaurants

# 4. Get by ID (use _id from step 2)
curl http://localhost:3000/api/restaurants/<id>

# 5. Filter by cuisine
curl "http://localhost:3000/api/restaurants?cuisine=Indian"

# 6. Soft delete
curl -X DELETE http://localhost:3000/api/restaurants/<id>

# 7. Verify deleted restaurant is gone from listing
curl http://localhost:3000/api/restaurants
```

---

## Presentation Guidelines

### Structure (5-7 minutes per team)

1. **Architecture diagram** -- Show the layers of the service
2. **Bug walkthrough** -- For each ticket:
   - How you reproduced it
   - Root cause analysis
   - Your fix (show code diff)
3. **Demo** -- Live Postman walkthrough of all endpoints
4. **Lessons learned** -- What would you do differently?

### Tips
- Show the actual error before and after the fix
- Explain the **root cause**, not just the fix
- Mention any regressions you caught
- Time management: 2 min per ticket max

---

## MCQ Topics (Modules 09-11)

The MCQ assessment covers all Node.js content:

| Topic | Key Concepts |
|-------|-------------|
| Node.js Core | Event loop, modules, npm, package.json |
| Async Programming | Callbacks, Promises, async/await, error handling |
| Express.js | Routing, middleware, request/response, status codes |
| MongoDB | CRUD operations, query operators, update operators |
| REST API Design | HTTP methods, status codes, URL patterns |
| Error Handling | try/catch, error middleware, unhandled rejections |
| Environment Config | dotenv, process.env, 12-factor app |

---

## MCQ Sample Questions

**Q1.** What happens if you forget `await` before a MongoDB `find().toArray()` call?

- A) It returns an empty array
- B) It returns a pending Promise object
- C) It throws a SyntaxError
- D) It returns `undefined`

**Answer:** B -- Without `await`, the async call returns a Promise, not the actual data.

---

**Q2.** Which Express middleware signature indicates an error handler?

- A) `(req, res)`
- B) `(req, res, next)`
- C) `(err, req, res, next)`
- D) `(error, response)`

**Answer:** C -- Express identifies error handlers by the 4-parameter signature `(err, req, res, next)`.

---

## MCQ Sample Questions (continued)

**Q3.** What is the correct order of Express middleware?

- A) Routes -> Body Parser -> Error Handler
- B) Body Parser -> Routes -> Error Handler
- C) Error Handler -> Routes -> Body Parser
- D) Routes -> Error Handler -> Body Parser

**Answer:** B -- Body parser must come before routes (so `req.body` is populated), and error handler must come last.

---

**Q4.** Which MongoDB update operator should you use to change a single field's value?

- A) `$push`
- B) `$set`
- C) `$inc`
- D) `$unset`

**Answer:** B -- `$set` replaces a field's value. `$push` appends to an array. `$inc` increments a number. `$unset` removes a field.

---

## MCQ Sample Questions (continued)

**Q5.** What does `require('dotenv').config()` do?

- A) Creates a `.env` file automatically
- B) Reads `.env` file and loads key-value pairs into `process.env`
- C) Encrypts environment variables
- D) Validates environment variable types

**Answer:** B -- dotenv reads the `.env` file and merges the variables into `process.env`.

---

**Q6.** Which HTTP status code should a soft-delete endpoint return?

- A) 200 OK
- B) 201 Created
- C) 204 No Content
- D) Both A and C are acceptable

**Answer:** D -- 200 (with a message body) or 204 (without body) are both valid for successful deletes.

---

## Team Formation

### Team Size
- 2-3 members per team
- Assign roles: **Driver** (codes), **Navigator** (reviews), **Tester** (Postman)
- Rotate roles between Sprint 1 and Sprint 2

### Repo Setup
```bash
# Clone the starter repo
cd ~/workspace
cp -r starter-code/restaurant-service .
cd restaurant-service
npm install

# Start MongoDB (if using Docker)
docker run -d -p 27017:27017 --name mongo mongo:7

# Seed test data
node db/seed.js

# Start the server
npm start
```

---

## Scoring Rubric

### Bug Fixes (50%)

| Ticket | Points | Criteria |
|--------|--------|----------|
| FOOD-31 | 15 | Async/await fix + error handler integration |
| FOOD-32 | 15 | Validation fix + correct response |
| FOOD-34 | 10 | dotenv config loading correctly |
| Bonus | 10 | Clean code, meaningful comments |

### Feature (20%)

| Ticket | Points | Criteria |
|--------|--------|----------|
| FOOD-33 | 15 | Both endpoints working with edge cases |
| Bonus | 5 | Menu filtering, pagination |

### Presentation (15%) + MCQ (15%)

---

## Timeline Checkpoints

| Time | Checkpoint | Expected State |
|------|-----------|----------------|
| 10:30 | Checkpoint 1 | FOOD-31 reproduced and root cause identified |
| 11:30 | Checkpoint 2 | FOOD-31 fixed, FOOD-32 in progress |
| 12:30 | Sprint 1 End | FOOD-31 + FOOD-32 fixed, tested |
| 14:30 | Checkpoint 3 | FOOD-33 endpoints added |
| 15:30 | Code Freeze | All tickets addressed, tests passing |
| 16:00 | Presentations | Demo ready |

---

## Troubleshooting Guide

| Problem | Quick Fix |
|---------|-----------|
| `ECONNREFUSED` on MongoDB | Start MongoDB: `docker start mongo` or `mongod` |
| `EADDRINUSE` port 3000 | Kill process: `lsof -i :3000` then `kill <PID>` |
| `Cannot find module` | Run `npm install` in the project directory |
| `SyntaxError: Unexpected token` | Check for missing brackets, commas, or quotes |
| Postman shows empty body | Ensure `Content-Type: application/json` header is set |
| MongoDB returns `null` for `findOne` | Check if `_id` is wrapped in `new ObjectId()` |

---

## Key Takeaways

| Concept | Key Lesson |
|---------|------------|
| Async/Await | Always `await` async calls; unhandled promises crash Node.js |
| Express Middleware | Order matters: parser -> routes -> error handler |
| Error Handling | Use try/catch + `next(err)` for async route handlers |
| MongoDB Operations | Use `$set` for updates, `$push` for arrays; check field names |
| Environment Config | Load dotenv before accessing `process.env`; never hardcode secrets |
| Soft Delete | Prefer deactivation over deletion for audit trails |
| REST Conventions | Use correct HTTP verbs and status codes |

> **Next: Module 12 -- Database SQL: Mastering relational databases with MySQL for the FoodExpress backend.**
