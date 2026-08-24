# Docker Part 2 -- Project Brief
## Module 25 | Day 28

---

## Sustain Context

FoodExpress is standardizing its Docker images across all microservices. The Restaurant Service Dockerfile and MySQL container configuration have multiple issues causing build failures, bloated images, and data loss. As a sustain engineer, you need to fix these issues and ensure all images follow Docker best practices.

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix Dockerfile | Fix 8 bugs in Restaurant Service Dockerfile: tag, COPY order, npm ci, EXPOSE, USER, CMD form, HEALTHCHECK | 45 min | 25 |
| 2 | Fix Volume Config | Fix 5 bugs in MySQL run script: volume path, data dir, restart policy, password, init script | 30 min | 15 |
| 3 | Bonus: Multi-Stage | Create multi-stage Dockerfile for Order Service, compare sizes | 30 min | 10 |

**Total Points Available:** 50

---

## Deliverables

1. Fixed `Dockerfile.restaurant` building and running successfully
2. Fixed `run-mysql.sh` with data persisting across container restarts
3. (Bonus) Multi-stage Dockerfile with size comparison
