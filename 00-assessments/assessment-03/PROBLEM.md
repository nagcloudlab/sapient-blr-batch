# Assessment 3 -- Java Coding Assessment

**Duration:** 90 minutes | **Total:** 100 marks | **Domain:** QuickTicket Event Booking
**Files:** `Event.java`, `BookingService.java`, `EventController.java`

---

## Instructions

- The QuickTicket Java backend has defects reported across 3 areas.
- The application compiles but fails at runtime. Investigate each report, locate the root cause, and fix it.
- Java 17, Spring Boot, Maven
- `mvn compile` must succeed after all fixes
- Do not add external dependencies beyond what is in `pom.xml`
- Push all fixed Java files to your assigned branch before the timer ends.

---

## Question 1 -- Event Model & Collection Fixes [Simple] (30 marks)

**DEF-101:** Any external class can directly modify an Event's price and seat count without going through any method. The fields should be accessible only through getter/setter methods.

**DEF-102:** When Event objects are added to a HashSet, logically identical events (same ID) appear as duplicates. Two Event objects with the same ID should be treated as equal by all collection types.

**DEF-103:** Logging an Event object prints `com.quickticket.model.Event@5a2e4553` instead of meaningful information like the event name, venue, and price.

**DEF-104:** The `removeSoldOut()` method throws `ConcurrentModificationException` at runtime when processing a list containing sold-out events.

**Files to fix:** `Event.java`, `BookingService.java`

---

## Question 2 -- Database Layer Fixes [Medium] (35 marks)

**DEF-201:** A penetration test found that the `findByName()` method is vulnerable to SQL injection. Entering `'; DROP TABLE events; --` as a search term executes destructive SQL.

**DEF-202:** After several hours of traffic, the application throws "Too many connections" errors. Database connections opened in `findByName()` are never returned to the pool.

**DEF-203:** When `bookTicket()` successfully decrements the seat count but fails on the booking insert, the seat count remains decremented with no corresponding booking record. Both operations should succeed or fail together.

**DEF-204:** The `sortByPrice()` method produces compiler warnings about raw types and requires unsafe casts. Events priced at $9.99 and $9.50 are sorted incorrectly -- the comparator produces incorrect results for prices with small differences.

**Files to fix:** `BookingService.java`

---

## Question 3 -- REST Controller Fixes [Complex] (35 marks)

**DEF-301:** POST `/api/events` receives the request but all fields in the created Event object are null, even though the request body contains valid JSON.

**DEF-302:** POST `/api/events` returns HTTP 200 instead of HTTP 201 Created.

**DEF-303:** GET `/api/events/1` returns a 500 error with a Spring framework exception about a missing path variable binding.

**Files to fix:** `EventController.java`

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

Push all fixed Java files to your assigned branch before the timer ends.
