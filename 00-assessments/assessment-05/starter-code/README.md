# Assessment 5 -- Database & QE/QC Coding Assessment

**Domain:** QuickTicket Event Booking | **Duration:** 90 minutes | **Total:** 100 marks

---

## About the Application

QuickTicket is an event booking platform built with **Spring Boot 3.2**, **Spring Data JPA**, and **H2 in-memory database**. It provides REST APIs for creating, viewing, and deleting event bookings.

### Tech Stack

| Layer        | Technology                         |
|--------------|------------------------------------|
| Language     | Java 17                            |
| Framework    | Spring Boot 3.2.5                  |
| Database     | H2 (in-memory, auto-configured)    |
| ORM          | Spring Data JPA / Hibernate        |
| Testing      | JUnit 5, Mockito                   |
| API Testing  | Postman / Newman (pm.test format)  |
| Build Tool   | Maven                              |

---

## Project Structure

```
starter-code/
├── pom.xml                          # Maven build configuration
├── schema.sql                       # [FIX THIS] Buggy database schema (Q2a)
├── queries.sql                      # [FIX THIS] Buggy SQL queries (Q1)
├── api-tests.js                     # [FIX THIS] Empty API test assertions (Q3)
├── QuickTicket-API-Tests.postman_collection.json  # Import into Postman
├── src/
│   ├── main/
│   │   ├── java/com/quickticket/
│   │   │   ├── QuickTicketApplication.java
│   │   │   ├── model/
│   │   │   │   ├── User.java
│   │   │   │   ├── Event.java
│   │   │   │   ├── Booking.java
│   │   │   │   └── Payment.java
│   │   │   ├── repository/
│   │   │   │   ├── UserRepository.java
│   │   │   │   ├── EventRepository.java
│   │   │   │   ├── BookingRepository.java
│   │   │   │   └── PaymentRepository.java
│   │   │   ├── service/
│   │   │   │   └── BookingService.java
│   │   │   └── controller/
│   │   │       └── BookingController.java
│   │   └── resources/
│   │       ├── application.properties
│   │       └── data.sql              # Sample seed data
│   └── test/
│       └── java/com/quickticket/service/
│           └── BookingServiceTest.java  # [FIX THIS] Buggy unit tests (Q2b)
```

---

## Prerequisites

- **Java 17** or higher (`java -version`)
- **Maven 3.8+** (`mvn -version`)
- **Postman** (for API testing) or **Newman** CLI (`npm install -g newman`)

---

## Setup & Run

### 1. Build the project

```bash
cd starter-code
mvn clean install -DskipTests
```

### 2. Run the application

```bash
mvn spring-boot:run
```

The application starts at **http://localhost:8080**.

### 3. Verify the application is running

```bash
curl http://localhost:8080/api/bookings/1
```

You should see a JSON response with booking details.

### 4. Access H2 Console (optional)

Open **http://localhost:8080/h2-console** in your browser:
- JDBC URL: `jdbc:h2:mem:quickticket`
- Username: `sa`
- Password: *(leave blank)*

### 5. Run unit tests

```bash
mvn test
```

> Note: Tests will fail initially -- that's expected. Your job is to fix them.

---

## API Endpoints

| Method | Endpoint              | Description                | Success | Error |
|--------|-----------------------|----------------------------|---------|-------|
| POST   | `/api/bookings`       | Create a new booking       | 201     | 400   |
| GET    | `/api/bookings/{id}`  | Get booking by ID          | 200     | 404   |
| DELETE | `/api/bookings/{id}`  | Delete a booking           | 200     | 404   |

### Sample POST request body

```json
{
    "userId": 1,
    "eventId": 1,
    "seats": 2
}
```

### Sample API calls with curl

```bash
# Create a booking
curl -X POST http://localhost:8080/api/bookings \
  -H "Content-Type: application/json" \
  -d '{"userId": 1, "eventId": 1, "seats": 2}'

# Get a booking
curl http://localhost:8080/api/bookings/1

# Get a non-existent booking (returns 404)
curl http://localhost:8080/api/bookings/99999

# Delete a booking
curl -X DELETE http://localhost:8080/api/bookings/1
```

---

## Database Schema

The application uses 4 tables: `users`, `events`, `bookings`, and `payments`.

```
users ──────┐
            ├──> bookings ──> payments
events ─────┘
```

### Sample Data (pre-loaded)

- **5 users** (Alice, Bob, Charlie, Diana, Eve)
- **5 events** (Summer Concert, Tech Conference, Comedy Night, Art Exhibition, Concert Under Stars)
- **9 bookings** (mix of confirmed, pending, cancelled)
- **6 payments** (only for confirmed bookings)

---

## What You Need to Fix

### Question 1 -- SQL Query Fixes (30 marks) --> `queries.sql`

| Defect   | Marks | Task |
|----------|-------|------|
| DEF-101  | 10    | Fix the buggy revenue report query |
| DEF-102  | 10    | Write a new query: top 3 spenders |
| DEF-103  | 10    | Fix the slow event search query + add explanation |

### Question 2 -- Schema & JUnit Fixes (35 marks) --> `schema.sql` + `BookingServiceTest.java`

| Defect   | Marks | File | Task |
|----------|-------|------|------|
| DEF-201  | 5     | schema.sql | Add foreign key constraints |
| DEF-202  | 5     | schema.sql | Prevent negative total_amount |
| DEF-203  | 5     | schema.sql | Enforce unique email |
| DEF-204  | 5     | schema.sql | Add index on booked_at |
| DEF-205  | 5     | BookingServiceTest.java | Test not being executed |
| DEF-206  | 5     | BookingServiceTest.java | assertEquals fails despite correct value |
| DEF-207  | 5     | BookingServiceTest.java | Test uses real DB instead of mock |

### Question 3 -- API Test Assertions (35 marks) --> Postman Collection + `api-tests.js`

| Test     | Marks | Task |
|----------|-------|------|
| TEST-301 | 12    | POST /api/bookings -- verify 201, id, and pending status |
| TEST-302 | 12    | GET /api/bookings/99999 -- verify 404 and error field |
| TEST-303 | 11    | DELETE then GET -- verify 200 then 404 |

---

## Files You Must Edit

| # | File | Location |
|---|------|----------|
| 1 | `queries.sql` | Project root |
| 2 | `schema.sql` | Project root |
| 3 | `BookingServiceTest.java` | `src/test/java/com/quickticket/service/` |
| 4 | `api-tests.js` | Project root (write assertions in Postman, copy back here) |

> **Do NOT modify** any other files (models, service, controller, application.properties).

---

## How to Verify Your Fixes

### SQL Queries (Q1)
Run your fixed queries in the **H2 Console** (http://localhost:8080/h2-console) to verify they return correct results.

### Schema (Q2a)
Review the `schema.sql` file for correct MySQL DDL syntax. The evaluator will check for proper constraints and index.

### JUnit Tests (Q2b)
```bash
mvn test
```
All 3 tests should pass after your fixes.

### API Tests (Q3)

1. Start the application:
   ```bash
   mvn spring-boot:run
   ```
2. Open **Postman** and import the collection:
   - Click **Import** > select `QuickTicket-API-Tests.postman_collection.json`
   - This creates 4 requests with empty test stubs in the **Tests** tab
3. For each request, open the **Tests** tab and write your `pm.test()` assertions
4. Run the full collection using **Collection Runner** (click "Run" on the collection)
5. All tests should show green checkmarks after writing correct assertions
6. Copy your final assertions back into `api-tests.js` before submitting

**Postman Quick Reference:**
```js
// Check status code
pm.response.to.have.status(200);

// Parse response body
const body = pm.response.json();

// Check property exists
pm.expect(body).to.have.property('fieldName');

// Check property value
pm.expect(body.fieldName).to.eql('expectedValue');
```

---

## Submission

Push all fixed files to your assigned branch before the timer ends.

```bash
git add queries.sql schema.sql api-tests.js src/test/java/com/quickticket/service/BookingServiceTest.java
git commit -m "Assessment 5 - fixes"
git push origin <your-branch-name>
```

---

## Evaluation Parameters

| Parameter | Weightage |
|-----------|-----------|
| Ability to apply concepts and implement functionality | 20 |
| Coding Standards (naming, comments, indentation) | 20 |
| Exception Handling | 20 |
| Completeness wrt timelines and working application | 15 |
| Problem solving ability | 10 |
| Debugging / troubleshooting skills | 15 |
| **Total** | **100** |
