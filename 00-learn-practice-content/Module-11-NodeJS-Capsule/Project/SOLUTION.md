# Module 11 Solutions -- TRAINER ONLY

## Bug #1: Missing await on Async Service Call (FOOD-31)

**Root Cause:** `restaurantService.getAll()` returns a Promise (it is an async function that queries MongoDB). The route handler does not `await` the result, so it tries to `res.json()` a Promise object, which fails.

**Fix:**
```javascript
// Before
router.get('/', (req, res) => {
  const restaurants = restaurantService.getAll();
  res.json(restaurants);
});

// After
router.get('/', async (req, res, next) => {
  try {
    const restaurants = await restaurantService.getAll();
    res.json(restaurants);
  } catch (err) {
    next(err);
  }
});
```

## Bug #2: Async Errors Bypass Error Handler (FOOD-31b)

**Root Cause:** Express does not automatically catch exceptions thrown inside `async` route handlers. Without `try/catch` + `next(err)`, the error becomes an `UnhandledPromiseRejection` and the error handler middleware is never invoked.

**Fix:**
```javascript
// Option A: try/catch in each handler (shown above)

// Option B: asyncHandler wrapper (DRY)
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

router.get('/', asyncHandler(async (req, res) => {
  const restaurants = await restaurantService.getAll();
  res.json(restaurants);
}));
```

## Bug #3: Parameter Name Mismatch in createRestaurant (FOOD-32)

**Root Cause:** The function signature is `createRestaurant(restaurantData)` but the function body uses `data` (a different variable name). Since `data` is never defined, `insertOne(undefined)` is called, which silently inserts an empty-ish document or fails silently.

**Fix:**
```javascript
// Before
async function createRestaurant(restaurantData) {
  const result = await db.collection('restaurants').insertOne(data);
  return result;
}

// After
async function createRestaurant(restaurantData) {
  const result = await db.collection('restaurants').insertOne(restaurantData);
  return result;
}
```

## Bug #4: Validation Middleware Missing Return (FOOD-32b)

**Root Cause:** The validation function checks for errors and sends a 400 response, but does not `return` after sending. Execution falls through and `next()` is called, allowing the invalid request to proceed to the route handler.

**Fix:**
```javascript
// Before
function validateRestaurant(req, res, next) {
  if (!req.body.name) {
    res.status(400).json({ error: 'name is required' });
    // BUG: no return -- execution continues!
  }
  next();
}

// After
function validateRestaurant(req, res, next) {
  if (!req.body.name) {
    return res.status(400).json({ error: 'name is required' });
  }
  next();
}
```

## Bug #5: dotenv Loaded Too Late (FOOD-34)

**Root Cause:** In `server.js`, `process.env.PORT` is read at the top of the file. The `config/index.js` module (which calls `require('dotenv').config()`) is imported later. By the time dotenv loads the `.env` file, the port variable has already been set to `undefined`.

**Fix:**
```javascript
// server.js -- BEFORE
const port = process.env.PORT || 3000;  // process.env.PORT is undefined here
const config = require('./config');      // dotenv loads here, too late

// server.js -- AFTER
require('dotenv').config();              // Load .env FIRST
const config = require('./config');
const port = config.port;               // Now reads from loaded env
```

## Enhancement #1: Soft-Delete Endpoint (FOOD-33a)

```javascript
// routes/restaurants.js
router.delete('/:id', asyncHandler(async (req, res) => {
  const result = await restaurantService.deactivate(req.params.id);
  if (!result) {
    return res.status(404).json({ error: 'Restaurant not found' });
  }
  res.json({ message: 'Restaurant deactivated' });
}));

// services/restaurantService.js
async function deactivate(id) {
  const result = await db.collection('restaurants').updateOne(
    { _id: new ObjectId(id) },
    { $set: { isActive: false, deletedAt: new Date() } }
  );
  return result.matchedCount > 0;
}
```

## Enhancement #2: Menu Retrieval Endpoint (FOOD-33b)

```javascript
// routes/restaurants.js
router.get('/:id/menu', asyncHandler(async (req, res) => {
  const restaurant = await restaurantService.getById(req.params.id);
  if (!restaurant) {
    return res.status(404).json({ error: 'Restaurant not found' });
  }
  let menu = restaurant.menu || [];
  if (req.query.category) {
    menu = menu.filter(item => item.category === req.query.category);
  }
  res.json(menu);
}));
```

## Hints

| Bug | Level 1 | Level 2 |
|-----|---------|---------|
| #1 | "What does an async function return if you don't await it?" | "Add `await` before `restaurantService.getAll()` and make the handler `async`" |
| #2 | "What happens when an async function throws inside Express?" | "Wrap in try/catch and call `next(err)`, or use an asyncHandler wrapper" |
| #3 | "Log the variable being passed to insertOne -- is it what you expect?" | "The parameter is named `restaurantData` but the body uses `data`" |
| #4 | "Send an empty POST body. Does it return 400 or 201?" | "Add `return` before `res.status(400)` so `next()` is not called" |
| #5 | "Log `process.env.PORT` at line 1 of server.js. Is it defined?" | "Call `require('dotenv').config()` at the very top of server.js, before any process.env access" |
