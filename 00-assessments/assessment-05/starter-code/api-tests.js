// =============================================================
// QuickTicket API Tests (Postman pm.test format)
// =============================================================
// TASK 3 (35 pts): Write pm.test() assertions for each test below.
//
// HOW TO USE:
//   1. Start the app: mvn spring-boot:run
//   2. Open Postman and import: QuickTicket-API-Tests.postman_collection.json
//   3. Write your assertions in the "Tests" tab of each request
//   4. Run the collection using Postman Collection Runner
//   5. Copy your final assertions back into this file before submitting
// =============================================================


// =============================================================
// TEST-301 (12 marks): POST /api/bookings
//
// Request:
//   POST http://localhost:8080/api/bookings
//   Body: { "userId": 1, "eventId": 1, "seats": 2 }
//
// Verify:
//   - Response status is 201
//   - Response body contains an "id" field
//   - Response body "status" equals "pending"
// =============================================================
pm.test("POST /api/bookings returns 201 and pending booking", function () {
    // Write your assertions here
});


// =============================================================
// TEST-302 (12 marks): GET /api/bookings/99999 (non-existent booking)
//
// Request:
//   GET http://localhost:8080/api/bookings/99999
//
// Verify:
//   - Response status is 404
//   - Response body contains an "error" field
// =============================================================
pm.test("GET /api/bookings/99999 returns 404 with error field", function () {
    // Write your assertions here
});


// =============================================================
// TEST-303 (11 marks): DELETE /api/bookings/:id then GET same ID
//
// Step 1 Request:
//   DELETE http://localhost:8080/api/bookings/:id
// Step 2 Request:
//   GET http://localhost:8080/api/bookings/:id
//
// Verify:
//   - DELETE returns status 200
//   - Subsequent GET to same ID returns 404
// =============================================================
pm.test("DELETE /api/bookings/:id returns 200", function () {
    // Write your assertions here
});

pm.test("GET deleted booking returns 404", function () {
    // Write your assertions here
});
