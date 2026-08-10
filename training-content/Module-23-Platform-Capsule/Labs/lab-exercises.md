# Capsule Project: Language + Linux + Microservices -- Lab Exercises
## Module 23 | Day 26

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

The starter-code/ folder contains the actual config files and
scripts from our servers. Fix all bugs and restore service.

-- Vikram Mehta, SRE Lead, FoodExpress
```

---

## Incident 1: Order Service DOWN (6 bugs)

### Duration: 2 hours | Points: 20

**Files to fix:**
- `starter-code/order-service-start.sh` -- Service startup script
- `starter-code/application.yml` -- Spring Boot configuration

### Bugs to Find and Fix

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the Java command in the startup script | Wrong Java version path specified | Service fails to start |
| 2 | Look at the port number in application.yml | Port 8082 conflicts with Payment Service | Address already in use error |
| 3 | Check the MySQL connection URL | Hostname `db-server` should be `localhost` (or `mysql-host`) | Connection refused |
| 4 | Look at the JVM heap flags in the startup script | `-Xmx64m` is far too small for production | OutOfMemoryError under load |
| 5 | Check the systemd ExecStart path in the script comments | Path references old directory structure | systemd can't find the script |
| 6 | Examine the log directory permissions line | `chmod 644` on log directory (should be 755) | App can't create log files |

### Verification Steps

```bash
# After fixing all bugs:
# 1. Run the startup script
bash order-service-start.sh

# 2. Verify the process is running
ps aux | grep java | grep order

# 3. Check the port
ss -tlnp | grep 8081

# 4. Health check
curl -s http://localhost:8081/actuator/health
```

---

## Incident 2: Disk Full + Log Rotation (5 bugs)

### Duration: 1.5 hours | Points: 15

**Files to fix:**
- `starter-code/disk-cleanup.sh` -- Cleanup script
- `starter-code/foodexpress-logrotate.conf` -- Log rotation config

### Bugs to Find and Fix

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the log path in logrotate config | Path is `/var/logs/` but should be `/var/log/` | Logs never rotated |
| 2 | Check the `find` command in cleanup script | Missing `-type f` and wrong `-mtime` syntax | Old files not cleaned |
| 3 | Look at the cron schedule comment in cleanup script | Schedule `0 * 2 * *` is wrong; should be `0 2 * * *` | Runs wrong times |
| 4 | Check for `compress` directive in logrotate | Missing `compress` and `delaycompress` | Rotated logs take full space |
| 5 | Check the log level in application.yml | Set to DEBUG in production | 10x more log volume than needed |

### Verification Steps

```bash
# After fixing:
# 1. Test logrotate config
sudo logrotate -d /etc/logrotate.d/foodexpress

# 2. Test cleanup script
bash disk-cleanup.sh --dry-run

# 3. Verify disk usage improved
df -h /var/log
```

---

## Incident 3: API Timeout Chain (5 bugs)

### Duration: 1.5 hours | Points: 15

**Files to fix:**
- `starter-code/restaurant-service.js` -- Node.js Restaurant Service
- `starter-code/application.yml` -- Spring Boot config (Order Service timeout settings)

### Bugs to Find and Fix

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Look at how the menu file is read in restaurant-service.js | Uses `readFileSync` -- blocks event loop | 8-second response times |
| 2 | Check the HTTP client timeout in application.yml | No timeout set for RestTemplate calls | Threads blocked indefinitely |
| 3 | Look for circuit breaker configuration | No circuit breaker configured | Cascading failures |
| 4 | Check error handling in restaurant-service.js | Missing uncaughtException handler | Silent crashes |
| 5 | Check connection pool size in application.yml | `maximum-pool-size: 2` is too small | Connection starvation |

### Verification Steps

```bash
# After fixing:
# 1. Restart Restaurant Service
pm2 restart restaurant-service

# 2. Test response time
time curl http://localhost:3000/api/v1/restaurants/1/menu

# 3. Should respond in < 500ms (not 8 seconds)

# 4. Test Order Service with Restaurant Service down
# (should get fallback response, not timeout)
```

---

## Bonus Challenge: Write a Post-Mortem (5 points)

Choose one of the three incidents and write a post-mortem using this template:

```
## Post-Mortem: [Incident Title]

### Summary
One paragraph describing what happened.

### Impact
- Duration:
- Orders affected:
- Revenue impact:

### Timeline
- HH:MM - Event 1
- HH:MM - Event 2

### Root Cause
Technical explanation.

### Fix Applied
What you changed and why.

### Prevention
What changes would prevent recurrence?
- Monitoring:
- Process:
- Automation:
```

---

## Scoring

| Task | Points |
|------|--------|
| Incident 1: All 6 bugs fixed, service running | 20 |
| Incident 2: All 5 bugs fixed, disk cleaned | 15 |
| Incident 3: All 5 bugs fixed, < 2s response | 15 |
| Bonus: Post-mortem document | 5 |
| **Total** | **55** |
