# Module 10: Node.js (Part 2) -- Fix the Issues

## Lab Overview

The FoodExpress Restaurant Service now needs Express API routes and MongoDB integration. The existing code has route configuration bugs, middleware issues, and MongoDB query errors. Fix these and then add the remaining CRUD endpoints.

> "Hi Team, we added Express and MongoDB to the Restaurant Service but nothing works. POST creates nothing, every route returns 404, and the MongoDB queries return empty results even though we have data. Also the update endpoint is corrupting restaurant names. Half-day to fix and ship."

---

## Setup

1. Navigate to `starter-code/restaurant-service/`
2. Ensure MongoDB is running locally (`mongod` or Docker container)
3. Run `node db/seed.js` to populate test data
4. Run `npm start` to start the Express server
5. Try `POST /api/restaurants` with a JSON body -- notice `req.body` is undefined
6. Try `GET /api/restaurants` -- notice it returns 404

---

## Bug List

### Bug #1: Create Route Uses Wrong HTTP Verb
- **Where:** `routes/restaurants.js`
- **Symptom:** `POST /api/restaurants` returns 404. Looking at the route file, the create handler is mapped to `router.get()`.
- **Hint:** Change `router.get` to `router.post` for the create endpoint.
- **Debug:** Check the route definition. What HTTP method should a create operation use?

### Bug #2: Missing Body Parser Middleware
- **Where:** `server.js`
- **Symptom:** Even after fixing Bug #1, `req.body` is `undefined` in POST and PUT handlers.
- **Hint:** `express.json()` must be registered as middleware before route handlers. Add `app.use(express.json())`.
- **Debug:** Add `console.log(req.body)` in the route handler. It will print `undefined`.

### Bug #3: Catch-All Route Blocks Everything
- **Where:** `server.js`
- **Symptom:** Every request returns 404 "Route not found" -- even valid routes.
- **Hint:** The catch-all `app.use('*', ...)` is defined before specific routes. Express matches in order. Move it to the end.
- **Debug:** Comment out the catch-all line. Do the other routes work now?

### Bug #4: MongoDB Query Uses Wrong Field Name
- **Where:** `services/restaurantService.js`
- **Symptom:** `getActiveRestaurants()` returns an empty array despite data existing.
- **Hint:** The query filters `{ status: "active" }` but the documents use `{ isActive: true }`. Check the seed data schema.
- **Debug:** Run `db.restaurants.findOne()` in MongoDB shell and compare field names.

### Bug #5: MongoDB Update Corrupts Data
- **Where:** `services/restaurantService.js`
- **Symptom:** After updating a restaurant name, the `name` field becomes an array like `["Pizza Palace"]` instead of a string.
- **Hint:** The code uses `$push` (appends to array) instead of `$set` (sets value). Change the update operator.
- **Debug:** Update a restaurant, then query it in MongoDB shell. Notice the name is now an array.

### Enhancement #6: Complete CRUD Routes
- **Where:** `routes/restaurants.js`
- **Hint:** Add `GET /:id`, `PUT /:id`, `DELETE /:id` routes. Return appropriate status codes (200, 201, 204, 404).

### Enhancement #7: Add MongoDB Index
- **Where:** `db/setup.js`
- **Hint:** Add `db.collection('restaurants').createIndex({ cuisine: 1 })` so cuisine filtering is fast.

---

## Checkpoints

1. [ ] `POST /api/restaurants` with JSON body creates a restaurant (returns 201)
2. [ ] `req.body` is populated in POST and PUT handlers
3. [ ] `GET /api/restaurants` returns the restaurant list (not 404)
4. [ ] Active restaurant query returns results (not empty array)
5. [ ] Updating restaurant name keeps it as a string (not array)
6. [ ] `GET /api/restaurants/:id` returns a single restaurant
7. [ ] `DELETE /api/restaurants/:id` removes the restaurant (returns 204)
8. [ ] MongoDB index exists on `cuisine` field (verify with `db.restaurants.getIndexes()`)

## Bonus Challenges

1. Add error-handling middleware that catches async errors and returns structured JSON
2. Add request validation middleware using `joi` or manual checks
3. Add a `GET /api/restaurants?cuisine=Italian&limit=5` with query parameter support
4. Add a simple health check endpoint `GET /health` that pings MongoDB
