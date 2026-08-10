# Docker Part 1 -- Project Brief
## Module 24 | Day 27

---

## Sustain Context

FoodExpress is migrating from bare-metal deployments to Docker containers. The initial Dockerfiles written by a junior developer have multiple issues preventing successful builds and secure deployments. As a sustain engineer, you need to fix the Dockerfile and demonstrate core Docker commands for container management.

---

## Client Email

```
From: priya.sharma@foodexpress.in
To: sustain-engineering@team.com
Subject: Docker Migration -- Order Service Dockerfile Broken
Date: 2026-08-04

Team,

We're containerizing the FoodExpress Order Service. The Dockerfile
is broken -- wrong base image, wrong ports, security issues.

Fix it, build it, run it, verify it.

-- Priya Sharma, DevOps Lead, FoodExpress
```

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix Dockerfile | Fix 7 bugs: base image, WORKDIR, COPY, EXPOSE, USER, CMD, HEALTHCHECK | 45 min | 25 |
| 2 | Docker Commands | Pull, run, inspect, cleanup containers and images | 30 min | 15 |
| 3 | Bonus: Static Page | Write Dockerfile from scratch for NGINX landing page | 30 min | 10 |

**Total Points Available:** 50

---

## Deliverables

1. Fixed `Dockerfile` that builds and runs successfully
2. Running container serving Order Service on port 8081
3. Docker command execution log showing all Lab 2 tasks completed
4. (Bonus) Working NGINX Dockerfile for FoodExpress landing page
