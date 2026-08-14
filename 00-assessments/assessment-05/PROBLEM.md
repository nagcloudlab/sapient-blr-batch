# Assessment 5 -- Database & QE/QC Coding Assessment

**Duration:** 90 minutes | **Total:** 100 marks | **Domain:** QuickTicket Event Booking
**Files:** `queries.sql`, `schema.sql`, `BookingServiceTest.java`, `api-tests.js`

---

## Instructions

- The QuickTicket database team and QA team have reported defects in SQL queries, schema design, unit tests, and API test coverage.
- Fix existing issues and write missing queries/tests.
- SQL must be valid MySQL syntax
- JUnit 5 with Mockito for Java tests
- Postman pm.test() format for API tests
- Push all fixed files to your assigned branch before the timer ends.

---

## Question 1 -- SQL Query Fixes [Simple] (30 marks)

**DEF-101 (10 marks):** The revenue report query in `queries.sql` returns incorrect results:
- It excludes events with zero bookings (they should appear with 0 revenue)
- It includes cancelled bookings in the revenue calculation (only confirmed bookings should count)
- It returns an aggregate error because results are not grouped
- It shows all events regardless of revenue (should only show events with revenue above 1000)

Fix the query to return: `event_name`, `total_revenue` -- including zero-revenue events, counting only confirmed bookings, grouped by event, filtered to revenue > 1000, sorted descending.

**DEF-102 (10 marks):** Write a new query to find the top 3 users by total spending on confirmed bookings.
Expected columns: `user_name`, `email`, `total_spent`. Sorted descending, limited to top 3.

**DEF-103 (10 marks):** The event search query uses `SELECT *` and a LIKE pattern with leading wildcard that prevents index usage. Rewrite with proper column selection and add a SQL comment explaining why the pattern is slow and what alternatives exist.

**Files to fix:** `queries.sql`

---

## Question 2 -- Schema Design & JUnit Fixes [Medium] (35 marks)

**Schema fixes (20 marks):** The DBA has identified 4 data integrity issues in `schema.sql`:

**DEF-201:** The bookings table references users and events by ID but has no foreign key constraints. Orphan records can be created.

**DEF-202:** A booking was created with `total_amount: -500`. Negative amounts should be impossible.

**DEF-203:** Two users registered with the same email address. Email addresses must be unique.

**DEF-204:** Queries filtering bookings by date are slow. The `booked_at` column has no index.

**JUnit fixes (15 marks):** Three unit tests in `BookingServiceTest.java` have issues:

**DEF-205:** The `testCalculateTotal_singleTicket` test never appears in test reports. The test runner does not execute it.

**DEF-206:** The `testCalculateTotal_multipleTickets` test fails with `expected: <150.0> but was: <150.0>`. The assertion parameters are in the wrong order.

**DEF-207:** The `testFindEvent_returnsEvent` test fails with a database connection error. Unit tests should use mocking, not a real database.

**Files to fix:** `schema.sql`, `BookingServiceTest.java`

---

## Question 3 -- API Test Assertions [Complex] (35 marks)

Three test stubs in `api-tests.js` have empty assertion bodies. Write the Postman `pm.test()` assertions:

**TEST-301 (12 marks):** POST `/api/bookings` -- Verify response status is 201, response body contains an `id` field, and `status` equals `"pending"`.

**TEST-302 (12 marks):** GET `/api/bookings/99999` (non-existent) -- Verify response status is 404 and response body contains an `error` field.

**TEST-303 (11 marks):** After DELETE `/api/bookings/:id` returns 200, a subsequent GET to the same ID should return 404.

**Files to fix:** `api-tests.js`

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
