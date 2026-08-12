# Module 08: Java Capsule Project -- Fix the Issues

## Lab Overview

This is a full-day capsule project. The FoodExpress Order Service is a Spring Boot API with several open Jira tickets. You will reproduce each issue, find the root cause, fix it, test via Postman, and document your findings.

> "Hi Team, we have four tickets blocking the release sprint. FOOD-21 is a production 500 error that customers see when viewing order details. FOOD-22 is a feature the mobile team needs urgently. FOOD-23 is a performance issue -- the order list endpoint returns the entire database. FOOD-24 is a data integrity issue -- negative quantities are getting into the system. Full-day sprint, let's close these out."

---

## Setup

1. Open the `starter-code/order-service` project in your IDE
2. Run `mvn spring-boot:run` (or use IDE run config)
3. Confirm the API starts on `http://localhost:8080`
4. Import the Postman collection from `starter-code/postman/`
5. Try `GET /orders/1` -- notice the 500 error
6. Try `POST /orders` with `"quantity": -3` -- notice it succeeds (it should not)

---

## Ticket List

### FOOD-21: GET /orders/{id} Returns 500
- **Where:** `OrderController.java`, `OrderService.java`
- **Symptom:** Requesting an order with a missing restaurant reference throws NullPointerException. Also, requesting a non-existent order ID returns 500 instead of 404.
- **Hint:** The service calls `order.getRestaurant().getName()` without checking for null. The controller does not handle the `Optional.empty()` case.
- **Reproduce:** `GET /orders/3` (order #3 has a deleted restaurant)

### FOOD-22: Add Status Filter Endpoint
- **Where:** `OrderController.java`, `OrderRepository.java`
- **Symptom:** The mobile team needs to filter orders by status (PENDING, CONFIRMED, DELIVERED, CANCELLED) but no such endpoint exists.
- **Hint:** Add a `@RequestParam` for status. Create a `findByStatus()` method in the repository.
- **Acceptance:** `GET /orders?status=DELIVERED` returns only delivered orders

### FOOD-23: Order List Has No Pagination
- **Where:** `OrderController.java`, `OrderService.java`
- **Symptom:** `GET /orders` returns all 500+ orders in one response. The mobile app times out.
- **Hint:** Use Spring Data's `Pageable` interface and `PageRequest.of(page, size)`
- **Acceptance:** `GET /orders?page=0&size=10` returns 10 results with page metadata

### FOOD-24: Negative Quantities Accepted
- **Where:** `Order.java`, `OrderController.java`
- **Symptom:** `POST /orders` with `"quantity": -3` creates a valid order with negative quantity
- **Hint:** Add `@Min(1)` to the quantity field and `@Valid` to the controller parameter
- **Acceptance:** `POST /orders` with quantity < 1 returns 400 Bad Request

---

## Checkpoints

1. [ ] `GET /orders/3` returns order JSON with "Unknown Restaurant" (not 500)
2. [ ] `GET /orders/99999` returns 404 (not 500)
3. [ ] `GET /orders?status=PENDING` returns only pending orders
4. [ ] `GET /orders?page=0&size=5` returns exactly 5 results with page info
5. [ ] `POST /orders` with `"quantity": -1` returns 400
6. [ ] `POST /orders` with `"quantity": 2` succeeds as before
7. [ ] All existing tests still pass (`mvn test`)

## Bonus Challenges

1. Add a `GET /orders?sort=orderDate,desc` parameter using Spring Data Sort
2. Add a global exception handler with `@ControllerAdvice` that returns structured error JSON
3. Add integration tests for each ticket using `@SpringBootTest` and `MockMvc`
4. Add request logging with a `HandlerInterceptor` to log method, URI, and response time
