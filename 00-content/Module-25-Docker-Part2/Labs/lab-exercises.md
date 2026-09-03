# Docker Part 2 -- Lab Exercises
## Module 25 | Day 28

---

## Client Email

```
From: priya.sharma@foodexpress.in
To: sustain-engineering@team.com
Subject: Restaurant Service Docker Issues + MySQL Data Loss
Date: 2026-08-05

Team,

Two issues to fix today:

1. The Restaurant Service (Node.js) Dockerfile has multiple bugs.
   It builds but the container crashes on startup.

2. Our MySQL container keeps losing data when it restarts.
   We need proper volume configuration so order data persists.

Fix both issues. The Dockerfile should follow best practices
(multi-stage, non-root, health check).

-- Priya Sharma, DevOps Lead, FoodExpress
```

---

## Lab 1: Fix the Restaurant Service Dockerfile (8 bugs)

### Duration: 45 minutes | Points: 25

**File to fix:** `starter-code/Dockerfile.restaurant`

### Bugs to Find and Fix

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check base image tag | `FROM node:latest` -- unpredictable | Non-reproducible builds |
| 2 | Look at COPY order | Source code copied before npm install | Cache busted on every code change |
| 3 | Check the npm command | Uses `npm install` instead of `npm ci` | Non-deterministic dependency versions |
| 4 | Look for .dockerignore usage | node_modules copied into image | Bloated image, overrides installed deps |
| 5 | Check EXPOSE port | EXPOSE 8080 but app runs on 3000 | Misleading documentation |
| 6 | Look for non-root user | Runs as root | Security vulnerability |
| 7 | Check CMD form | Shell form used | Signals not forwarded correctly |
| 8 | Look for HEALTHCHECK | No HEALTHCHECK defined | Container health unknown |

### Verification Steps

```bash
# Build
docker build -f Dockerfile.restaurant -t foodexpress/restaurant-service:1.0 .

# Run
docker run -d --name restaurant-svc -p 3000:3000 \
  foodexpress/restaurant-service:1.0

# Test
curl http://localhost:3000/health

# Check user
docker exec restaurant-svc whoami   # Should be: appuser

# Check image size
docker images foodexpress/restaurant-service:1.0
```

---

## Lab 2: Fix Volume Configuration (5 bugs)

### Duration: 30 minutes | Points: 15

**File to fix:** `starter-code/run-mysql.sh`

### Bugs to Find and Fix

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the volume mount syntax | `-v mysql-data` missing the mount path | Volume not mounted to correct directory |
| 2 | Check the data directory path | Mount path is `/data/mysql` instead of `/var/lib/mysql` | MySQL can't find its data |
| 3 | Look at restart policy | No restart policy set | Container doesn't auto-restart after host reboot |
| 4 | Check environment variables | `MYSQL_ROOT_PASSWORD` not set | MySQL refuses to start |
| 5 | Check for init script volume | No init SQL mounted | Database and tables not created on first run |

### Verification Steps

```bash
# Run fixed script
bash run-mysql.sh

# Verify data persistence
docker exec fe-mysql mysql -uroot -psecret -e "SHOW DATABASES;"

# Remove and recreate container
docker rm -f fe-mysql
bash run-mysql.sh

# Data should still be there
docker exec fe-mysql mysql -uroot -psecret -e "USE foodexpress; SHOW TABLES;"
```

---

## Lab 3: Multi-Stage Build (Bonus)

### Duration: 30 minutes | Points: 10

Create a multi-stage Dockerfile for the FoodExpress Order Service:

**Requirements:**
- Stage 1: Use `maven:3.9-eclipse-temurin-17` to build
- Stage 2: Use `eclipse-temurin:17-jre-alpine` for runtime
- Copy only the JAR from stage 1
- Non-root user, HEALTHCHECK, correct EXPOSE
- Compare image size: single-stage vs multi-stage

---

## Scoring

| Task | Points |
|------|--------|
| Lab 1: Fix Dockerfile (8 bugs) | 25 |
| Lab 2: Fix volume config (5 bugs) | 15 |
| Lab 3: Bonus multi-stage build | 10 |
| **Total** | **50** |
