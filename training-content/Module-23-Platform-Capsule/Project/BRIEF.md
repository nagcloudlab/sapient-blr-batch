# Platform Capsule Project -- Project Brief
## Module 23 | Day 26

---

## Sustain Context

It's Sunday peak hours at FoodExpress. Three production incidents have hit simultaneously. As a sustain engineer on call, you must triage, investigate, and resolve all incidents within your shift. This capsule project combines Java, Node.js, Linux, and Microservices skills from previous modules into a realistic on-call simulation.

---

## Client Email

```
From: vikram.mehta@foodexpress.in
To: sustain-engineering@team.com
Subject: URGENT -- Multiple Production Incidents This Sunday
Date: 2026-08-03 (Sunday)

Team,

We have 3 active incidents that need immediate resolution:

1. [P1 CRITICAL] Order Service is completely down since 09:15.
   Customers cannot place orders. Revenue impact: ~$4,000/hour.

2. [P2 HIGH] Disk at 95% on app-srv-2. Log rotation hasn't
   run in a week. If disk hits 100%, all services crash.

3. [P2 HIGH] Cascading timeouts across services since 14:00.
   40% of orders failing with timeout errors.

Fix everything. Write a post-mortem for the P1 incident.

-- Vikram Mehta, SRE Lead, FoodExpress
```

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix Order Service Startup | Fix 6 bugs in startup script and application.yml: Java version, port, DB host, heap size, systemd path, permissions | 2 hours | 20 |
| 2 | Fix Disk & Log Rotation | Fix 5 bugs: logrotate path, find command, cron schedule, compression, log level | 1.5 hours | 15 |
| 3 | Fix API Timeout Chain | Fix 5 bugs: sync file read, missing timeouts, no circuit breaker, missing error handlers, pool size | 1.5 hours | 15 |
| 4 | Post-Mortem Document | Write incident post-mortem for the P1 (Order Service down) | 30 min | 5 |

**Total Points Available:** 55

---

## Deliverables

1. Fixed `order-service-start.sh` with all 6 bugs resolved
2. Fixed `application.yml` with correct port, DB, pool, logging, timeouts, circuit breaker
3. Fixed `disk-cleanup.sh` with correct find syntax and cron schedule
4. Fixed `foodexpress-logrotate.conf` with correct path and compression
5. Fixed `restaurant-service.js` with async file reads and error handlers
6. Post-mortem document for the P1 incident
