# Module 22: Microservices & API -- Lab Setup

## Prerequisites

- Node.js 18+ (`node -v`)
- Java JDK 17+ (`java -version`)
- Maven 3.8+ (`mvn -version`)
- curl or Postman

## Running the Starter Code

Start each service in a separate terminal:

```bash
# Terminal 1 -- Java Order Service (port 8080)
cd Labs/starter-code/order-service
mvn spring-boot:run

# Terminal 2 -- Node.js Restaurant Service (port 3001)
cd Labs/starter-code/restaurant-service
npm install && npm start

# Terminal 3 -- Node.js API Gateway (port 4000)
cd Labs/starter-code/gateway
npm install && npm start
```

## Verifying Your Fixes

```bash
# Test REST controller on Order Service directly
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId":1,"items":[{"menuItemId":1,"qty":2}]}'

# Test through API Gateway
curl http://localhost:4000/api/restaurants
curl http://localhost:4000/api/orders

# Test inter-service call (gateway calls order service internally)
curl http://localhost:4000/api/summary
```

## Expected Behavior

- REST controller returns proper HTTP status codes (201, 200, 404, 400) -- not always 200.
- API gateway routes requests to the correct service based on path prefix.
- Inter-service HTTP calls complete and the response is returned to the client.
- Error responses are JSON objects with a `message` field, not HTML error pages.

## Troubleshooting

**Gateway returns HTML error page instead of JSON:** The downstream service is throwing an unhandled
exception. Check the downstream service's console for the root cause.

**Inter-service call times out:** Verify the service URL configured in the gateway matches the port
the downstream service is actually listening on. Check `starter-code/gateway/config.js`.
