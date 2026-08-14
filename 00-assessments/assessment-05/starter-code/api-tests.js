// =============================================================
// QuickTicket API Tests (Postman pm.test format)
// =============================================================
// TASK 3 (35 pts): Design and write pm.test() assertions.
//
// HOW TO USE:
//   1. Start the app: mvn spring-boot:run
//   2. Open Postman and import: QuickTicket-API-Tests.postman_collection.json
//   3. Write your assertions in the "Tests" tab of each request
//   4. Run the collection using Postman Collection Runner
//   5. Copy your final assertions back into this file before submitting
// =============================================================


// =============================================================
// TEST-301 (7 marks): Happy Path -- Create Booking
//
// Request: POST http://localhost:8080/api/bookings
// Body: { "userId": 1, "eventId": 1, "seats": 2 }
//
// Verify:
//   - Response status is 201
//   - Body contains "id" field
//   - Body "status" equals "pending"
//   - Body "totalAmount" is correctly calculated (price x seats)
//   - Save the booking ID for later tests
// =============================================================
pm.test("POST /api/bookings creates a pending booking", function () {
    // Write your assertions here
});


// =============================================================
// TEST-302 (7 marks): Retrieve & Validate -- Verify Created Booking
//
// Request: GET http://localhost:8080/api/bookings/{{bookingId}}
//   (use the ID saved from TEST-301)
//
// Verify:
//   - Response status is 200
//   - Body "userId", "eventId", "seats" match what was sent in TEST-301
// =============================================================
pm.test("GET /api/bookings/:id returns the created booking with correct data", function () {
    // Write your assertions here
});


// =============================================================
// TEST-303 (7 marks): Negative Testing -- Error Handling
//
// Scenario A: GET http://localhost:8080/api/bookings/99999
// Scenario B: POST http://localhost:8080/api/bookings
//             Body: { "userId": 1, "eventId": 99999, "seats": 2 }
//
// Verify:
//   Scenario A: status 404, body has "error" field
//   Scenario B: error status (not 201), body has "error" field
// =============================================================
pm.test("GET non-existent booking returns 404 with error", function () {
    // Write your assertions here
});

pm.test("POST with invalid eventId returns error", function () {
    // Write your assertions here
});


// =============================================================
// TEST-304 (7 marks): Delete & Verify -- Flow Test
//
// Step 1: DELETE http://localhost:8080/api/bookings/{{bookingId}}
// Step 2: GET http://localhost:8080/api/bookings/{{bookingId}}
//
// Verify:
//   - DELETE returns status 200
//   - Subsequent GET returns status 404
// =============================================================
pm.test("DELETE /api/bookings/:id returns 200", function () {
    // Write your assertions here
});

pm.test("GET deleted booking returns 404", function () {
    // Write your assertions here
});


// =============================================================
// TEST-305 (7 marks): Edge Case -- Invalid Input
//
// Request: POST http://localhost:8080/api/bookings
// Body: { "userId": 1, "eventId": 1, "seats": 0 }
//
// Verify:
//   - Response status is NOT 201 (booking should be rejected)
//   - Body contains "error" field
//   - Add a comment explaining what you are testing and why
// =============================================================
pm.test("POST with zero seats is rejected", function () {
    // Write your assertions here
    // Add a comment explaining what you are testing and why
});
