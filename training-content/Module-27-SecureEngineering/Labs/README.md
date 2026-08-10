# Module 27: Secure Engineering -- Lab Setup

## Prerequisites

- Node.js 18+ (`node -v`)
- Java JDK 17+ (`java -version`)
- A text editor for code review
- curl for sending test payloads

## Running the Starter Code

```bash
# Node.js service (contains XSS and injection vulnerabilities)
cd Labs/starter-code/restaurant-service
npm install && npm start
# Starts on port 3001

# Java service (contains SQL injection vulnerability)
cd Labs/starter-code/order-service
mvn spring-boot:run
# Starts on port 8080
```

Run both services simultaneously to test all vulnerability scenarios.

## Verifying Your Fixes

Test that the fixes prevent the attacks without breaking normal functionality:

```bash
# SQL injection test (should return 400 Bad Request, NOT a database dump)
curl "http://localhost:8080/api/orders?customerId=1' OR '1'='1"

# XSS test (should be sanitised in the response, NOT executed as script)
curl -X POST http://localhost:3001/api/reviews \
  -H "Content-Type: application/json" \
  -d '{"text":"<script>alert(1)</script>"}'

# Secrets check -- .env must not be committed
ls Labs/starter-code/.env    # file should exist locally
cat Labs/starter-code/.gitignore | grep .env   # .env must be listed
```

## Expected Behavior

- SQL injection payloads return a `400` or `403` response, not query results.
- XSS payloads are HTML-encoded in responses (`&lt;script&gt;`, not `<script>`).
- All secrets (DB passwords, API keys) are loaded from environment variables or `.env`, not
  hard-coded in source files.
- Normal requests continue to work correctly after security fixes.

## Troubleshooting

**Normal queries break after parameterising SQL:** Ensure you are using `?` placeholders (JDBC) or
prepared statement parameters -- do not concatenate user input back into the query string.

**`.env` already tracked by Git:** Run `git rm --cached .env` then add `.env` to `.gitignore` and
commit. The file stays on disk but is no longer tracked.
