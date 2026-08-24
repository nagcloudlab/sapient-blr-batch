# Docker Part 1 -- Lab Exercises
## Module 24 | Day 27

---

## Client Email

```
From: priya.sharma@foodexpress.in
To: sustain-engineering@team.com
Subject: Docker Migration -- Order Service Dockerfile Broken
Date: 2026-08-04

Team,

We're containerizing the FoodExpress Order Service (Java/Spring Boot).
A junior developer wrote the initial Dockerfile but it doesn't build
or run correctly. There are multiple issues.

Please fix the Dockerfile so we can build and deploy the Order Service
as a Docker container.

Requirements:
- Must use Java 17 JRE (not JDK, to keep image small)
- Must expose port 8081
- Must run as non-root user
- Must have a health check

-- Priya Sharma, DevOps Lead, FoodExpress
```

---

## Lab 1: Fix the Dockerfile (7 bugs)

### Duration: 45 minutes | Points: 25

**File to fix:** `starter-code/Dockerfile`

### Bugs to Find and Fix

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the FROM image | `python:3.11` is not Java-compatible | Build succeeds but app can't run (no JVM) |
| 2 | Look for WORKDIR | No WORKDIR set; files copied to root `/` | Messy filesystem, hard to debug |
| 3 | Check the COPY instruction | JAR file path is wrong (`app.jar` vs actual name) | COPY fails, build breaks |
| 4 | Check EXPOSE port | EXPOSE 3000 but Order Service runs on 8081 | Misleading; orchestrators route to wrong port |
| 5 | Check who runs the process | No USER directive; runs as root | Security vulnerability; container has root access |
| 6 | Check CMD syntax | CMD uses shell form with wrong class path | App fails to start |
| 7 | Look for HEALTHCHECK | No HEALTHCHECK defined | Orchestrator can't detect if app is healthy |

### Verification Steps

```bash
# Build the image
docker build -t foodexpress/order-service:1.0 .

# Run the container
docker run -d --name order-svc -p 8081:8081 foodexpress/order-service:1.0

# Verify health
curl http://localhost:8081/actuator/health

# Check logs
docker logs order-svc

# Verify non-root user
docker exec order-svc whoami
# Should output: appuser (NOT root)
```

---

## Lab 2: Docker Commands Practice (5 tasks)

### Duration: 30 minutes | Points: 15

Complete these tasks using Docker CLI:

### Task 1: Pull and Run NGINX
```bash
# Pull nginx 1.25
# Run it on port 8080, name it "fe-nginx"
# Verify with curl http://localhost:8080
```

### Task 2: Container Inspection
```bash
# List all running containers
# Get the IP address of the fe-nginx container
# View the last 20 lines of fe-nginx logs
```

### Task 3: Interactive Container
```bash
# Run an Ubuntu 22.04 container interactively
# Inside: install curl, then curl http://fe-nginx (will it work? why/why not?)
# Exit the container
```

### Task 4: Cleanup
```bash
# Stop all running containers
# Remove all stopped containers
# Remove all unused images
# Verify nothing is left
```

### Task 5: Image Exploration
```bash
# Pull eclipse-temurin:17-jre-alpine
# Check its size (docker images)
# View its layer history (docker history)
# Compare size with eclipse-temurin:17-jre (non-alpine)
```

---

## Lab 3: Build a Simple Dockerfile from Scratch (Bonus)

### Duration: 30 minutes | Points: 10

Write a Dockerfile for the FoodExpress static landing page:

**Requirements:**
- Use `nginx:1.25-alpine` as base
- Copy `index.html` to `/usr/share/nginx/html/`
- Expose port 80
- Add a HEALTHCHECK that curls localhost
- Build and run it
- Verify the page loads at `http://localhost:9090`

```html
<!-- starter-code/index.html is provided -->
```

---

## Scoring

| Task | Points |
|------|--------|
| Lab 1: Fix Dockerfile (7 bugs) | 25 |
| Lab 2: Docker commands (5 tasks) | 15 |
| Lab 3: Bonus Dockerfile | 10 |
| **Total** | **50** |
