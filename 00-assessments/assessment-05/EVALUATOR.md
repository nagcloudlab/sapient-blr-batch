# Assessment 5 -- Evaluator Answer Key & Rubric

**TRAINER ONLY -- Do not share with candidates**

**Assessment:** Database & QE/QC Coding Assessment | **Domain:** QuickTicket Event Booking
**Duration:** 90 minutes | **Total:** 100 marks
**Questions:** 3 (Simple: 30 | Medium: 35 | Complex: 35)

---

## Simulation Template Evaluation Parameters

| Parameter | Weightage | What to Observe |
|-----------|-----------|-----------------|
| Ability to apply concepts | 20 | SQL JOINs, aggregation, schema constraints, JUnit/Mockito, Postman API |
| Coding Standards | 20 | SQL formatting, Java test conventions, JS assertion style |
| Exception Handling | 20 | NULL handling (COALESCE/HAVING), FK cascade, mock setup |
| Completeness wrt Timelines | 15 | All defects + new queries addressed within 90 min |
| Problem solving ability | 10 | Correct JOIN type choice, index reasoning, mock vs real DB |
| Debugging / troubleshooting | 15 | Assertion order, missing annotations, slow query diagnosis |
| **Total** | **100** | |

---

## Starter Code -- Spring Boot Project

The starter code is a runnable Spring Boot 3.2 project with H2 in-memory database.

**How to run:**
```bash
cd starter-code
mvn clean install -DskipTests   # Build
mvn spring-boot:run             # Start app at http://localhost:8080
mvn test                        # Run JUnit tests (will fail before fixes)
```

**Before fixes -- expected `mvn test` output:**
- Tests run: **2** (testCalculateTotal_singleTicket is skipped -- missing @Test)
- Failures: **1** (testFindEvent_returnsEvent -- DB connection error)
- testCalculateTotal_multipleTickets passes but has wrong assertion order (subtle bug)

**After fixes -- expected `mvn test` output:**
- Tests run: **3**, Failures: **0**, Errors: **0**

**API verification:** Start app, then test with Postman collection (`QuickTicket-API-Tests.postman_collection.json`) or curl.

**H2 Console:** http://localhost:8080/h2-console (JDBC URL: `jdbc:h2:mem:quickticket`, user: `sa`, no password)
Use this to verify SQL queries from Q1 against the sample data.

**Files candidates must edit (4 files only):**
| File | Location |
|------|----------|
| `queries.sql` | Project root |
| `schema.sql` | Project root |
| `BookingServiceTest.java` | `src/test/java/com/quickticket/service/` |
| `api-tests.js` | Project root |

---

## Question 1 Answers -- SQL Queries [Simple] (30 marks)

### DEF-101: Revenue report query (10 marks)

**Fixed:**
```sql
SELECT e.name AS event_name, COALESCE(SUM(p.amount), 0) AS total_revenue
FROM events e
LEFT JOIN bookings b ON b.event_id = e.id AND b.status = 'confirmed'
LEFT JOIN payments p ON p.booking_id = b.id
GROUP BY e.id, e.name
HAVING COALESCE(SUM(p.amount), 0) > 1000
ORDER BY total_revenue DESC;
```

**Scoring:** LEFT JOIN: 2 pts | status filter: 3 pts | GROUP BY: 2 pts | HAVING: 3 pts

### DEF-102: Top 3 spenders (10 marks)

**Fixed:**
```sql
SELECT u.name AS user_name, u.email, SUM(p.amount) AS total_spent
FROM users u
JOIN bookings b ON b.user_id = u.id
JOIN payments p ON p.booking_id = b.id
WHERE b.status = 'confirmed'
GROUP BY u.id, u.name, u.email
ORDER BY total_spent DESC
LIMIT 3;
```

**Scoring:** Correct joins: 3 pts | WHERE confirmed: 2 pts | GROUP BY + ORDER BY: 3 pts | LIMIT 3: 2 pts

### DEF-103: Slow query fix (10 marks)

**Fixed:**
```sql
SELECT id, name, date, price FROM events WHERE name LIKE 'concert%';
-- Leading wildcard ('%concert%') prevents B-tree index usage.
-- Alternatives: trailing wildcard, full-text search index.
```

**Scoring:** Remove SELECT *: 3 pts | Fix wildcard: 4 pts | Explanation: 3 pts

---

## Question 2 Answers -- Schema & JUnit [Medium] (35 marks)

### Schema Fixes (20 marks, 5 each)

**DEF-201:** Add FK constraints:
```sql
user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
event_id INT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
```

**DEF-202:** Add CHECK constraint on bookings table: `CHECK (total_amount >= 0)`

**DEF-203:** Add UNIQUE: `email VARCHAR(255) NOT NULL UNIQUE`

**DEF-204:** Add index: `CREATE INDEX idx_bookings_booked_at ON bookings(booked_at);`

### JUnit Fixes (15 marks)

**DEF-205:** Missing @Test annotation (5 marks)
Add `@Test` annotation to `testCalculateTotal_singleTicket` method.

**DEF-206:** assertEquals order (5 marks)
Fix: `assertEquals(150.0, result)` -- expected value first, actual second.

**DEF-207:** Mock instead of real DB (5 marks)
The starter code already has `@Mock BookingRepository` and `@InjectMocks BookingService`.
Fix: Add `@Mock EventRepository eventRepository` field, then rewrite the test body to use:
```java
Event event = new Event();
event.setId(1L);
event.setName("Summer Concert");
when(eventRepository.findById(1L)).thenReturn(Optional.of(event));
Event result = bookingService.findEvent(1L);
assertEquals("Summer Concert", result.getName());
```
Remove all raw JDBC code (`DriverManager`, `Connection`, `Statement`, `ResultSet`).

### Q2 Scoring

| Marks | Criteria |
|-------|----------|
| 35 | All 7 fixes correct |
| 28 | 5-6 correct |
| 20 | 3-4 correct |
| 10 | 1-2 correct |
| 0 | No meaningful changes |

---

## Question 3 Answers -- API Test Design & Assertions [Complex] (35 marks)

### TEST-301: Happy Path -- Create Booking (7 marks)

```js
pm.test("POST /api/bookings creates a pending booking", function () {
    pm.response.to.have.status(201);
    const body = pm.response.json();
    pm.expect(body).to.have.property('id');
    pm.expect(body.status).to.eql('pending');
    pm.expect(body.totalAmount).to.eql(150.00);  // 75.00 x 2 seats
});

// Save booking ID
var jsonData = pm.response.json();
if (jsonData && jsonData.id) {
    pm.collectionVariables.set("bookingId", jsonData.id);
}
```

**Scoring:** status 201: 1pt | has id: 1pt | status pending: 2pts | totalAmount check: 2pts | save ID: 1pt

### TEST-302: Retrieve & Validate (7 marks)

```js
pm.test("GET /api/bookings/:id returns the created booking with correct data", function () {
    pm.response.to.have.status(200);
    const body = pm.response.json();
    pm.expect(body.userId).to.eql(1);
    pm.expect(body.eventId).to.eql(1);
    pm.expect(body.seats).to.eql(2);
});
```

**Scoring:** status 200: 1pt | userId match: 2pts | eventId match: 2pts | seats match: 2pts

### TEST-303: Negative Testing (7 marks)

**Scenario A -- GET non-existent:**
```js
pm.test("GET non-existent booking returns 404 with error", function () {
    pm.response.to.have.status(404);
    const body = pm.response.json();
    pm.expect(body).to.have.property('error');
});
```

**Scenario B -- POST with invalid eventId:**
```js
pm.test("POST with invalid eventId returns error", function () {
    pm.response.to.have.status(400);
    const body = pm.response.json();
    pm.expect(body).to.have.property('error');
});
```

**Scoring:** Scenario A (404 + error): 3pts | Scenario B (400 + error): 4pts
**Acceptable:** Any non-2xx status check for Scenario B (400 or `pm.response.code !== 201`)

### TEST-304: Delete & Verify Flow (7 marks)

```js
// DELETE request
pm.test("DELETE /api/bookings/:id returns 200", function () {
    pm.response.to.have.status(200);
});

// GET after DELETE request
pm.test("GET deleted booking returns 404", function () {
    pm.response.to.have.status(404);
});
```

**Scoring:** DELETE 200 check: 3pts | GET 404 check: 4pts

### TEST-305: Edge Case -- Invalid Input (7 marks)

```js
pm.test("POST with zero seats is rejected", function () {
    // Boundary test: seats=0 should be rejected as invalid input
    // The API must validate that seats > 0 before creating a booking
    pm.response.to.have.status(400);
    const body = pm.response.json();
    pm.expect(body).to.have.property('error');
});
```

**Scoring:** status not 201 / status 400: 2pts | error field check: 2pts | meaningful comment: 3pts
**Acceptable:** `pm.expect(pm.response.code).to.not.eql(201)` as equivalent status check.
**Comment must explain:** what is being tested (boundary/edge case) and why (data integrity / validation).

### Q3 Overall Notes

**Acceptable alternatives:** `pm.expect(pm.response.code).to.equal(201)` is equivalent to `pm.response.to.have.status(201)`.
**Deduction:** -2 per test with no assertions. -1 per test missing meaningful assertions (only status, no body check).
**Bonus observation:** If candidate also tests `seats: -1` or missing required fields, note as strong problem-solving.

---

## Per-Candidate Scoring Sheet

### Raw Question Scores

| Question | Max | Score |
|----------|-----|-------|
| Q1 -- SQL Queries (Simple) | 30 | |
| Q2 -- Schema & JUnit (Medium) | 35 | |
| Q3 -- API Test Design (Complex) | 35 | |
| **Raw Total** | **100** | |

### Simulation Template Parameter Scores

| Parameter | Weightage | Score | Notes |
|-----------|-----------|-------|-------|
| Ability to apply concepts | 20 | | JOINs, constraints, Mockito, Postman |
| Coding Standards | 20 | | SQL format, Java conventions, JS style |
| Exception Handling | 20 | | NULL handling, FK cascade, mock setup |
| Completeness wrt Timelines | 15 | | All defects + new queries addressed |
| Problem solving ability | 10 | | JOIN choice, index reasoning |
| Debugging / troubleshooting | 15 | | Assertion order, annotation issues |
| **Total** | **100** | | |

---

## Verification Checklist

- [ ] Revenue query uses LEFT JOIN, filters confirmed, has GROUP BY + HAVING (Q1)
- [ ] Top 3 spenders query returns correct columns with LIMIT 3 (Q1)
- [ ] Slow query uses specific columns, no leading wildcard, has explanation (Q1)
- [ ] FK constraints on bookings.user_id and bookings.event_id (Q2)
- [ ] CHECK constraint prevents negative total_amount (Q2)
- [ ] UNIQUE constraint on users.email (Q2)
- [ ] Index on bookings.booked_at (Q2)
- [ ] @Test annotation present on testCalculateTotal_singleTicket (Q2)
- [ ] assertEquals has expected value first: assertEquals(150.0, result) (Q2)
- [ ] @Mock EventRepository + when/thenReturn replaces raw JDBC connection (Q2)
- [ ] POST test checks 201, id, pending status, and totalAmount (Q3)
- [ ] GET test verifies userId, eventId, seats match POST data (Q3)
- [ ] Negative tests check 404 + error and 400 + error (Q3)
- [ ] DELETE + GET flow verifies 200 then 404 (Q3)
- [ ] Edge case test rejects seats=0, has meaningful comment (Q3)

---

## Candidate Feedback Template

```
Assessment 5 Results -- [Candidate Name]
Date: [Date]

QUESTION 1 -- SQL Queries [Simple]: ___/30
- DEF-101 (revenue query): [PASS / PARTIAL / FAIL]
- DEF-102 (top spenders): [PASS / PARTIAL / FAIL]
- DEF-103 (slow query): [PASS / PARTIAL / FAIL]

QUESTION 2 -- Schema & JUnit [Medium]: ___/35
- DEF-201 (FK constraints): [PASS / PARTIAL / FAIL]
- DEF-202 (CHECK amount): [PASS / PARTIAL / FAIL]
- DEF-203 (UNIQUE email): [PASS / PARTIAL / FAIL]
- DEF-204 (index): [PASS / PARTIAL / FAIL]
- DEF-205 (@Test): [PASS / PARTIAL / FAIL]
- DEF-206 (assertEquals): [PASS / PARTIAL / FAIL]
- DEF-207 (mock): [PASS / PARTIAL / FAIL]

QUESTION 3 -- API Test Design [Complex]: ___/35
- TEST-301 (POST happy path): [PASS / PARTIAL / FAIL]
- TEST-302 (GET verify data): [PASS / PARTIAL / FAIL]
- TEST-303 (negative tests): [PASS / PARTIAL / FAIL]
- TEST-304 (DELETE flow): [PASS / PARTIAL / FAIL]
- TEST-305 (edge case): [PASS / PARTIAL / FAIL]

PARAMETER SCORES:
- Ability to apply concepts:     ___/20
- Coding Standards:              ___/20
- Exception Handling:            ___/20
- Completeness wrt Timelines:    ___/15
- Problem solving ability:       ___/10
- Debugging / troubleshooting:   ___/15

FINAL SCORE: ___/100

STRENGTHS:
- ___

AREAS TO REVIEW:
- ___
```
