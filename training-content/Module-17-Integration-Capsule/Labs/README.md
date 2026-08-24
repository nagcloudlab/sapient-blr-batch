# Module 17: Integration Capsule -- Lab Setup

## Prerequisites

- Node.js 18+ (`node -v`)
- Java JDK 17+ (`java -version`)
- Maven 3.8+ (`mvn -version`)
- MySQL 8.0 running locally
- MongoDB 7.0 running locally

## Running the Starter Code

Start services in this order (each in a separate terminal):

```bash
# 1. Ensure MySQL and MongoDB are running

# 2. Start the Java Order Service
cd Labs/starter-code/order-service
mvn spring-boot:run
# Starts on port 8080

# 3. Start the Node.js Restaurant Service
cd Labs/starter-code/restaurant-service
npm install && npm start
# Starts on port 3000

# 4. Start the Node.js API Gateway
cd Labs/starter-code/gateway
npm install && npm start
# Starts on port 4000
```

## Verifying Your Fixes

```bash
# Test through the gateway (port 4000)
curl http://localhost:4000/api/orders
curl http://localhost:4000/api/restaurants
```

All four cross-stack bugs must be fixed before requests flow end-to-end without errors.
Run the unit tests in each service: `mvn test` (Java) and `npm test` (Node).

## Expected Behavior

- Gateway routes requests to the correct downstream service.
- Order service persists to MySQL; restaurant service persists to MongoDB.
- Cross-service calls complete within 2 seconds.
- Unit tests pass in all three services.

## Troubleshooting

**Gateway returns 502 Bad Gateway:** The downstream service is not running or is on a different port.
Check that all three services started successfully before testing through the gateway.

**Maven test failures after fixing bugs:** Ensure you also update any unit test data or mock values
that relied on the buggy behaviour.
