# Module 11: Node.js Capsule Project -- Fix the Issues

## Lab Overview

This is a full-day capsule project. You will receive the FoodExpress Restaurant Service codebase with multiple bugs and missing features. Your job is to reproduce, diagnose, fix, and test each issue -- then present your findings.

> "Hi Team, the Restaurant Service we deployed last week is down. The GET endpoint crashes with a 500, the POST endpoint pretends to create but saves nothing, and the environment config is broken so staging is hitting the production database. We also need soft-delete and menu endpoints before the mobile team can integrate. Full-day sprint -- fix everything, test via Postman, and present root-cause analysis by 4 PM."

---

## Setup

1. Navigate to `starter-code/restaurant-service/`
2. Run `npm install`
3. Start MongoDB (`docker start mongo` or `mongod`)
4. Run `node db/seed.js` to populate test data (5 restaurants)
5. Run `npm start` to start the Express server
6. Try `GET /api/restaurants` -- notice the 500 error
7. Try `POST /api/restaurants` with valid JSON -- notice it "succeeds" but saves nothing

---

## Bug List

### Bug #1: GET /restaurants Returns 500 (Ticket FOOD-31)
- **Where:** `routes/restaurants.js`, `services/restaurantService.js`
- **Symptom:** `GET /api/restaurants` returns `500 Internal Server Error`. Console shows `UnhandledPromiseRejectionWarning`.
- **Hint:** The route handler calls `restaurantService.getAll()` which is async, but the handler does not use `await`. The returned Promise is sent as the response, and when it rejects, there is no catch.
- **Debug:** Add `console.log(typeof result)` after the service call. You will see `object` (a Promise), not an array.
- **Impact:** Mobile app cannot display restaurant listings -- P1 blocker.

### Bug #2: Async Errors Not Caught by Error Handler
- **Where:** `routes/restaurants.js`
- **Symptom:** Even after fixing Bug #1 with `await`, if the database is down, Express returns a generic 500 instead of the custom error response from `errorHandler.js`.
- **Hint:** Express does not automatically catch errors thrown inside `async` route handlers. You need `try/catch` with `next(err)`, or an `asyncHandler` wrapper.
- **Debug:** Temporarily stop MongoDB and hit the endpoint. Does the error handler's custom JSON format appear?
- **Impact:** Operations team cannot diagnose production issues from generic error responses.

### Bug #3: POST /restaurants Creates Nothing (Ticket FOOD-32)
- **Where:** `services/restaurantService.js`
- **Symptom:** `POST /api/restaurants` returns 201 but no document exists in MongoDB. No error in logs.
- **Hint:** The `createRestaurant()` method calls `db.collection('restaurants').insertOne(data)` but `data` is `undefined` because the parameter name is `restaurantData` in the function signature but `data` is used in the body.
- **Debug:** Add `console.log(data)` inside `createRestaurant()`. It will print `undefined`.
- **Impact:** No new restaurants can be added to the platform.

### Bug #4: Validation Middleware Swallows Errors
- **Where:** `middleware/validateRequest.js`
- **Symptom:** Sending a POST with missing `name` field does not return a 400 error -- it passes validation and creates an invalid document.
- **Hint:** The validation function checks `if (!req.body.name)` but then calls `next()` regardless (the `return` statement is missing before `next()` in the error branch).
- **Debug:** POST with `{}` as body. Does it return 400 or 201?
- **Impact:** Corrupt data enters the database, causing downstream display issues.

### Bug #5: Environment Config Not Loading (Ticket FOOD-34)
- **Where:** `config/index.js`, `server.js`
- **Symptom:** Server always uses `mongodb://localhost:27017` and port `3000` regardless of `.env` file contents.
- **Hint:** `require('dotenv').config()` is called in `config/index.js`, but `server.js` reads `process.env.PORT` directly at the top of the file BEFORE importing `config/index.js`. Move the dotenv call to the very top of `server.js`.
- **Debug:** Add `console.log(process.env.PORT)` at the top of `server.js`. It prints `undefined`.
- **Impact:** Staging deployment connects to production database -- data corruption risk.

---

## Enhancement List

### Enhancement #1: Add Soft-Delete Endpoint (Ticket FOOD-33a)
- **Where:** `routes/restaurants.js`, `services/restaurantService.js`
- **Task:** Add `DELETE /api/restaurants/:id` that sets `isActive: false` instead of removing the document.
- **Requirements:**
  - Return `200` with `{ message: "Restaurant deactivated" }`
  - Return `404` if restaurant not found
  - Deactivated restaurants must not appear in `GET /api/restaurants`
  - The `getAll()` query must filter by `{ isActive: true }`

### Enhancement #2: Add Menu Retrieval Endpoint (Ticket FOOD-33b)
- **Where:** `routes/restaurants.js`, `services/restaurantService.js`
- **Task:** Add `GET /api/restaurants/:id/menu` that returns the `menu` array for a specific restaurant.
- **Requirements:**
  - Return `200` with the menu array
  - Return `404` if restaurant not found
  - Support optional query param `?category=Pizza` to filter menu items

---

## Checkpoints

### Checkpoint 1 (10:30 AM)
- [ ] Bug #1 fixed: `GET /api/restaurants` returns 200 with restaurant array
- [ ] Root cause documented: "Missing `await` on async service call"

### Checkpoint 2 (11:30 AM)
- [ ] Bug #2 fixed: Async errors reach the error handler middleware
- [ ] Bug #3 fixed: `POST /api/restaurants` creates documents in MongoDB

### Checkpoint 3 (12:30 PM -- Sprint 1 Complete)
- [ ] Bug #4 fixed: Invalid POST requests return 400
- [ ] Bug #5 fixed: `.env` values are loaded correctly
- [ ] All 5 bugs tested via Postman

### Checkpoint 4 (14:30 PM)
- [ ] Enhancement #1: Soft-delete endpoint working
- [ ] Enhancement #2: Menu retrieval endpoint working

### Checkpoint 5 (15:30 PM -- Code Freeze)
- [ ] All endpoints tested end-to-end
- [ ] Presentation slides/notes prepared
- [ ] Root-cause document completed

---

## Bonus Challenges

1. **Add pagination** to `GET /api/restaurants` using `?page=1&limit=10` query parameters
2. **Add a request logger middleware** that logs method, URL, status code, and response time
3. **Add input sanitization** -- strip HTML tags from restaurant name and address fields
4. **Write a simple integration test** using `supertest` for the GET and POST endpoints
5. **Add MongoDB index** on `cuisine` field and measure query performance improvement

---

## Presentation Format

Each team presents for 5-7 minutes:

1. Show the original error (screenshot/Postman)
2. Explain root cause for each bug
3. Show your fix (code diff)
4. Live demo: walk through all endpoints in Postman
5. Lessons learned: what surprised you?

---

## MCQ Assessment

30-minute MCQ covering Modules 09-11 (Node.js Part 1, Part 2, and Capsule). Topics include:
- Node.js event loop and module system
- npm and package.json
- Callbacks, Promises, async/await
- Express.js routing and middleware
- MongoDB CRUD and query operators
- REST API design principles
- Error handling patterns
- Environment configuration
