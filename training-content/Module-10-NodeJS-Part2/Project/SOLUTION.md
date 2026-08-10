# Module 10 Solutions -- TRAINER ONLY

## Bug #1: Wrong HTTP Verb on Create Route

**Root Cause:** `router.get('/restaurants', ...)` is used for the create endpoint instead of `router.post(...)`. GET requests cannot carry a request body in standard usage.

**Fix:**
```javascript
// Before
router.get('/restaurants', async (req, res) => { /* create logic */ });

// After
router.post('/restaurants', async (req, res) => { /* create logic */ });
```

## Bug #2: Missing JSON Body Parser Middleware

**Root Cause:** `express.json()` is not registered in `server.js`. Without it, `req.body` is `undefined` for all POST/PUT requests.

**Fix:**
```javascript
// Add before route registration
app.use(express.json());
```

## Bug #3: Catch-All Route Defined Too Early

**Root Cause:** `app.use('/*', notFoundHandler)` is defined before the `/restaurants` routes. Express matches routes in order, so every request hits the catch-all first and gets a 404.

**Fix:**
```javascript
// Move catch-all AFTER all specific routes
app.use('/api/restaurants', restaurantRoutes);
app.use('/api/menus', menuRoutes);

// Catch-all LAST
app.use('*', notFoundHandler);
```

## Bug #4: Wrong MongoDB Field Name in Query

**Root Cause:** The query uses `{ status: "active" }` but the document schema has the field `isActive: true`. The query matches zero documents.

**Fix:**
```javascript
// Before
const restaurants = await db.collection('restaurants').find({ status: "active" }).toArray();

// After
const restaurants = await db.collection('restaurants').find({ isActive: true }).toArray();
```

## Bug #5: Wrong MongoDB Update Operator

**Root Cause:** `$push` appends to an array. Using it on a string field like `name` converts the field to an array, corrupting the document.

**Fix:**
```javascript
// Before
await db.collection('restaurants').updateOne(
  { _id: id },
  { $push: { name: newName } }
);

// After
await db.collection('restaurants').updateOne(
  { _id: id },
  { $set: { name: newName } }
);
```

## Hints

| Bug | Level 1 | Level 2 |
|-----|---------|---------|
| #1 | "What HTTP method is used for creating resources?" | "Change router.get to router.post" |
| #2 | "Log req.body in the route handler -- what do you see?" | "Add app.use(express.json()) before routes" |
| #3 | "Comment out the catch-all route. Do other routes work now?" | "Move the catch-all after all specific route registrations" |
| #4 | "Open MongoDB shell and check the actual field names" | "The field is isActive (boolean), not status (string)" |
| #5 | "What does $push do vs $set?" | "$push is for arrays. Use $set to update a scalar field" |
