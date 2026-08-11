# Assessment 4 -- Node.js Coding Assessment

**Duration:** 90 minutes | **Total:** 100 marks | **Domain:** QuickTicket Event Booking
**Files:** `routes/events.js`, `middleware/auth.js`, `models/Event.js`, `routes/auth.js`

---

## Instructions

- The QuickTicket Node.js API has defects reported by the QA and security teams.
- The server starts but multiple endpoints behave incorrectly. Investigate and fix all issues.
- Fix only the 4 listed files -- do not modify `server.js` or `package.json`
- `npm start` must work after fixes
- Do not add new npm packages
- Push all fixed files to your assigned branch before the timer ends.

---

## Question 1 -- Event Routes & Middleware Fixes [Simple] (30 marks)

**DEF-101:** GET `/api/events` returns `{ "data": {}, "count": undefined }` instead of the actual event list. The database contains 5 events confirmed via MongoDB shell.

**DEF-102:** POST `/api/events` with an empty body `{}` creates a record with all fields undefined. Mongoose validation errors are returned as 500 Internal Server Error instead of 400.

**DEF-103:** After successful JWT verification, authenticated requests hang indefinitely. The server never sends a response for valid tokens. Only invalid/missing tokens get a response (401).

**Files to fix:** `routes/events.js`, `middleware/auth.js`

---

## Question 2 -- Data Model & Validation Fixes [Medium] (35 marks)

**DEF-201:** Events can be created without a name field. The name should be mandatory.

**DEF-202:** An event was created with `price: -50`. Prices must be zero or positive.

**DEF-203:** The `findByCategory('Music')` static method returns ALL events instead of only Music events.

**DEF-204:** There is no REST-compliant DELETE endpoint. Instead, a GET request to `/api/events/:id/delete` is used. This should follow REST conventions.

**DEF-205:** When any route throws an unhandled error, the error middleware does not catch it. Express returns its default HTML error page instead of the custom error handler.

**Files to fix:** `models/Event.js`, `routes/events.js`, `middleware/auth.js`

---

## Question 3 -- Authentication & Security Fixes [Complex] (35 marks)

**DEF-301:** A security audit found that user passwords are stored as plain text in MongoDB. Passwords must be hashed before storage.

**DEF-302:** Login always returns "Invalid credentials" even with the correct password. The password comparison logic is incorrect.

**DEF-303:** JWT tokens never expire. A stolen token works forever. Tokens should expire after 24 hours.

**Files to fix:** `routes/auth.js`

---

## Evaluation Parameters

| Parameter | Weightage |
|-----------|-----------|
| Ability to apply concepts and any additional functionality asked to implement | 20 |
| Coding Standards (Naming Conventions, Comments and Indentation) | 20 |
| Exception Handling | 20 |
| Completeness wrt Timelines as per requirements & Working application | 15 |
| Problem solving ability (think, evaluate and choose among alternates, and innovation/creativity) | 10 |
| Debugging / troubleshooting skills | 15 |
| **Total** | **100** |

---

## Submission

Push all fixed files to your assigned branch before the timer ends.
