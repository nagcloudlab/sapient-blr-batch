# Module 23: Platform Capsule -- Lab Setup

## Prerequisites

- All tools from Modules 01-22 (Node.js 18+, Java 17+, Maven, MySQL, MongoDB, Apache, Git, Bash/WSL2)
- curl for API testing

## Running the Starter Code

Follow the startup sequence in `Project/BRIEF.md`. The order matters:

```bash
# 1. Start databases (MySQL, MongoDB)

# 2. Start the Java Order Service
cd Labs/starter-code/order-service && mvn spring-boot:run

# 3. Start the Node.js Restaurant Service
cd Labs/starter-code/restaurant-service && npm install && npm start

# 4. Run the startup validation script
bash Labs/starter-code/scripts/startup-check.sh
```

The startup script is one of the artefacts with bugs -- it may fail or hang.

## Verifying Your Fixes

```bash
# API responds within 2 seconds
curl -w "\nTime: %{time_total}s\n" http://localhost:4000/api/health

# Logs rotate correctly (check log files after running for a few minutes)
ls -lh Labs/starter-code/logs/

# Run unit tests across all services
cd order-service && mvn test
cd restaurant-service && npm test
```

Review the completed post-mortem document against the template in `BRIEF.md`.

## Expected Behavior

- All services start cleanly with no errors in the first 30 seconds.
- API health endpoint responds in under 2 seconds.
- Log files rotate at the configured size limit without crashing the service.
- Unit tests pass for all four bug scenarios.
- Post-mortem document covers timeline, root cause, contributing factors, and action items.

## Troubleshooting

**Startup script hangs:** A `wait` or `sleep` loop may have an infinite condition. Add a timeout
counter or replace with a fixed `sleep 5` and a single readiness check.

**Log rotation not triggering:** Check the log rotation config for correct file path glob and size
threshold. Ensure the application has write permission on the log directory.
