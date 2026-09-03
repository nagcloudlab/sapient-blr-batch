# Module 08: Java Capsule -- Lab Setup

## Prerequisites

- Java JDK 17 or higher (`java -version` to confirm)
- Maven 3.8 or higher (`mvn -version` to confirm)
- curl or Postman (for API testing)

## Running the Starter Code

```bash
cd Labs/starter-code/order-service
mvn spring-boot:run
```

Spring Boot starts on port 8080. The first run downloads dependencies -- this may take a few minutes
on a slow connection. Leave the terminal open while testing.

## Verifying Your Fixes

Test each REST endpoint with curl (examples below) or import the collection into Postman:

```bash
# Create an order
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId":1,"items":[{"menuItemId":2,"quantity":1}]}'

# Get all orders
curl http://localhost:8080/api/orders

# Get order by ID
curl http://localhost:8080/api/orders/1
```

## Expected Behavior

- `POST /api/orders` returns `201 Created` with the new order body.
- `GET /api/orders` returns a JSON array of all orders.
- `GET /api/orders/{id}` returns the order or `404 Not Found` for unknown IDs.
- `DELETE /api/orders/{id}` returns `204 No Content`.
- No `500 Internal Server Error` responses for valid requests.

## Troubleshooting

**Port 8080 already in use:** Stop any other running Spring Boot or Tomcat process, or add
`--server.port=8081` to the run command and update your curl URLs accordingly.

**`BeanCreationException` on startup:** A component annotation is missing or a constructor dependency is
unresolvable -- read the full stack trace; the root cause line is usually near the bottom.
