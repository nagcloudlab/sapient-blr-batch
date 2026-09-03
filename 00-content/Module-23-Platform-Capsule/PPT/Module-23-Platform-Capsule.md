# Capsule Project -- Language + Linux + Microservices
## Module 23 | Sustain Engineering Training | Day 26

---

## Agenda -- Day 26

| # | Topic |
|---|-------|
| 01 | Project Briefing & Architecture Overview |
| 02 | Incident Triage Framework |
| 03 | FoodExpress Platform Architecture Walkthrough |
| 04 | Incident 1: Service Down (Java + Linux) |
| 05 | Hands-On: Incident 1 Resolution |
| 06 | Incident 1 Review & Discussion |
| 07 | Incident 2: Disk Full + Log Rotation |
| 08 | Hands-On: Incident 2 Resolution |
| 09 | Incident 3: API Timeout Chain |
| 10 | Hands-On: Incident 3 Resolution |
| 11 | Retrospective & Wrap-up |

---

## Project Context

### You Are a Sustain Engineer at FoodExpress

```
 Today's Shift: Sunday Peak Hours
 ┌─────────────────────────────────────────┐
 │  INCIDENT DASHBOARD -- FoodExpress      │
 │                                         │
 │  [CRITICAL] Order Service DOWN    09:15 │
 │  [HIGH]     Disk 95% on app-srv-2 10:30 │
 │  [HIGH]     API Timeout Chain     14:00 │
 │  [MEDIUM]   Log rotation failed   10:45 │
 │                                         │
 │  Active Incidents: 4                    │
 │  SLA Remaining: 2h for CRITICAL         │
 └─────────────────────────────────────────┘
```

> **Sustain Reality:** This is a typical shift for a sustain engineer. Multiple incidents, time pressure, cross-technology debugging.

---

## FoodExpress Platform Architecture

```
                    ┌──────────────┐
                    │   NGINX      │
                    │  Load Bal.   │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
   ┌──────┴──────┐  ┌─────┴──────┐  ┌─────┴──────┐
   │   Order     │  │  Payment   │  │ Restaurant │
   │  Service    │  │  Service   │  │  Service   │
   │  (Java)     │  │  (Java)    │  │  (Node.js) │
   │  :8081      │  │  :8082     │  │  :3000     │
   └──────┬──────┘  └─────┬──────┘  └─────┬──────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
                    ┌──────┴───────┐
                    │   MySQL      │
                    │   :3306      │
                    └──────────────┘
```

---

## Technology Stack in Play

| Layer | Technology | What You'll Debug |
|-------|-----------|-------------------|
| Application (Backend) | Java 17 / Spring Boot | Service config, JVM settings, heap dumps |
| Application (API) | Node.js / Express | Event loop blocking, dependency issues |
| Operating System | Linux (Ubuntu/CentOS) | Disk, logs, processes, permissions |
| Architecture | Microservices | Inter-service calls, timeouts, cascading failures |
| Database | MySQL | Connection pools, slow queries |
| Networking | TCP/HTTP | Port conflicts, firewall, DNS resolution |

---

## Incident Severity Matrix

| Severity | Response Time | Description | Example |
|----------|--------------|-------------|---------|
| P1 - Critical | 15 min | Revenue-impacting, all users affected | Order Service completely down |
| P2 - High | 30 min | Major feature broken, subset of users | Payment timeouts for 30% of orders |
| P3 - Medium | 2 hours | Minor feature degraded | Rating submission slow |
| P4 - Low | 8 hours | Cosmetic / non-urgent | Admin dashboard font issue |

> **FoodExpress:** Peak Sunday = ~5,000 orders/hour. Every minute of P1 = ~83 failed orders.

---

## Incident Response Framework

### The 5-Step DRILL Process

```
D - Detect      What alerts fired? What symptoms visible?
R - Reproduce   Can you reproduce the issue? What's the scope?
I - Investigate  Gather logs, metrics, traces. Root cause?
L - Live Fix     Apply the fix. Validate in staging first?
L - Learn        Post-mortem. How do we prevent recurrence?
```

---

## Essential Linux Commands for Incident Response

| Category | Command | Purpose |
|----------|---------|---------|
| Process | `ps aux \| grep java` | Find running services |
| Process | `top -bn1 \| head -20` | CPU/memory overview |
| Disk | `df -h` | Disk space usage |
| Disk | `du -sh /var/log/*` | Log directory sizes |
| Logs | `tail -f /var/log/app.log` | Live log monitoring |
| Logs | `journalctl -u order-service -f` | Systemd service logs |
| Network | `ss -tlnp` | Open ports and listeners |
| Network | `curl -v http://localhost:8081/health` | Health check |

---

## Java Service Debugging Essentials

### Common JVM Issues in Production

```
# Check JVM memory
jstat -gcutil <pid> 1000

# Thread dump (stuck threads?)
jstack <pid> > thread-dump.txt

# Heap dump (memory leak?)
jmap -dump:format=b,file=heap.hprof <pid>

# Check application.yml for config issues
cat /opt/foodexpress/order-service/config/application.yml
```

---

## Node.js Service Debugging Essentials

### Common Node.js Issues in Production

```
# Check if Node process is running
pm2 status

# View Node.js logs
pm2 logs restaurant-service --lines 50

# Check for blocked event loop
node --prof app.js    # generate profiling data

# Common issues:
# - Unhandled promise rejections
# - Synchronous file reads blocking event loop
# - Missing error handlers on streams
```

---

## INCIDENT 1: Order Service DOWN

### Severity: P1 - Critical

```
Alert: FoodExpress Order Service is not responding
Time:  09:15 IST, Sunday
Impact: All new orders failing
SLA:   Must resolve within 2 hours

Symptoms:
- Customers see "Unable to place order" error
- Health check endpoint returns HTTP 503
- Last successful order: 09:12 IST
```

---

## Incident 1: Investigation Path

### Step-by-Step Triage

```
Step 1: Is the process running?
  $ ps aux | grep java | grep order
  $ systemctl status order-service

Step 2: Check recent logs
  $ tail -100 /var/log/foodexpress/order-service.log
  $ journalctl -u order-service --since "09:00" --no-pager

Step 3: Check port binding
  $ ss -tlnp | grep 8081

Step 4: Check disk and memory
  $ df -h
  $ free -h

Step 5: Check configuration
  $ cat /opt/foodexpress/order-service/config/application.yml
```

---

## Incident 1: Root Causes (Multiple)

### What You'll Find in the Starter Code

| # | Issue | Category | Symptom |
|---|-------|----------|---------|
| 1 | Wrong Java version in startup script | Linux/Shell | Service fails to start |
| 2 | Incorrect port in application.yml | Java/Config | Port conflict with another service |
| 3 | MySQL connection string has wrong host | Java/Config | DB connection refused |
| 4 | systemd service file has wrong ExecStart path | Linux | Service won't auto-restart |
| 5 | Heap size too small (-Xmx64m) for production | Java/JVM | OutOfMemoryError under load |
| 6 | Log directory permissions wrong | Linux | Application can't write logs |

---

## Incident 1: Fix Verification

### How to Confirm Resolution

```bash
# 1. Fix all issues in config and scripts

# 2. Restart the service
sudo systemctl restart order-service

# 3. Verify it's running
systemctl status order-service
ss -tlnp | grep 8081

# 4. Health check
curl -s http://localhost:8081/actuator/health | jq .

# 5. Test an order
curl -X POST http://localhost:8081/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId": 1, "restaurantId": 5, "items": [...]}'
```

---

## INCIDENT 2: Disk Full on App Server

### Severity: P2 - High

```
Alert: Disk usage at 95% on app-srv-2
Time:  10:30 IST, Sunday
Impact: Services may crash if disk reaches 100%

Symptoms:
- /var/log partition at 95%
- Log rotation cron job hasn't run in 7 days
- Application logs growing at ~500MB/day
- Old deployment artifacts not cleaned up
```

---

## Incident 2: Investigation Path

```bash
# What's consuming space?
df -h
du -sh /var/log/* | sort -rh | head -10
du -sh /opt/foodexpress/*/releases/* | sort -rh

# Check log rotation config
cat /etc/logrotate.d/foodexpress

# Check cron jobs
crontab -l
cat /etc/cron.d/foodexpress-maintenance

# Check when logrotate last ran
cat /var/lib/logrotate/status | grep foodexpress
```

---

## Incident 2: Root Causes

| # | Issue | Category | Symptom |
|---|-------|----------|---------|
| 1 | Log rotation config uses wrong path | Linux | Logs never rotated |
| 2 | Cleanup script has wrong find command syntax | Shell | Old releases not deleted |
| 3 | Cron job has wrong schedule format | Linux | Maintenance never runs |
| 4 | Missing `compress` directive in logrotate | Linux | Old logs take full space |
| 5 | No log level filtering -- DEBUG in production | Java/Config | Excessive log volume |

---

## INCIDENT 3: API Timeout Chain

### Severity: P2 - High

```
Alert: Cascading timeouts across FoodExpress services
Time:  14:00 IST, Sunday
Impact: 40% of orders timing out

Symptoms:
- Restaurant Service (Node.js) responding slowly (~8s)
- Order Service (Java) timing out waiting for Restaurant
- Payment Service timing out waiting for Order
- No circuit breaker -- failures cascade
```

---

## Incident 3: Cascading Failure Diagram

```
Customer Request
      │
      ▼
┌─────────────┐  timeout=30s   ┌──────────────┐
│   Order     │────────────────▶│  Restaurant  │
│  Service    │  waiting...    │  Service     │
│  (Java)     │◀───────────────│  (Node.js)   │
│             │  8s response   │  SLOW        │
└──────┬──────┘                └──────────────┘
       │
       │ timeout=30s
       ▼
┌─────────────┐
│  Payment    │  Also waiting for Order to respond
│  Service    │  before processing payment
│  (Java)     │
└─────────────┘

Result: Customer waits 30+ seconds, then gets error
```

---

## Incident 3: Root Causes

| # | Issue | Category | Symptom |
|---|-------|----------|---------|
| 1 | Restaurant Service has sync file read blocking event loop | Node.js | 8-second response times |
| 2 | No timeout configured on Order -> Restaurant HTTP call | Microservices | Thread pool exhaustion |
| 3 | No circuit breaker pattern implemented | Microservices | Cascading failures |
| 4 | Node.js service missing error handler for uncaught exceptions | Node.js | Silent crashes |
| 5 | Connection pool too small in application.yml | Java/Config | Connection starvation |

---

## MCQ -- Quick Check 1

**Question:** A P1 incident is raised because Order Service returns HTTP 503. The first thing you should check is:

A) The database schema for recent migrations
B) Whether the service process is running (`ps aux | grep java`)
C) The source code for recent commits
D) The load balancer configuration

> **Answer:** B -- Always verify the process is alive first. This is the fastest diagnostic.

---

## MCQ -- Quick Check 2

**Question:** You see this in the logs:
```
java.lang.OutOfMemoryError: Java heap space
```
What is the most likely immediate fix?

A) Add more RAM to the server
B) Increase `-Xmx` JVM parameter and restart
C) Delete old log files
D) Restart MySQL

> **Answer:** B -- Increase the max heap allocation. Investigate the memory leak later, but the immediate fix is to give the JVM more memory to stay alive.

---

## MCQ -- Quick Check 3

**Question:** The cron entry `0 * 2 * *` means:

A) Every 2 hours
B) At minute 0 of every hour on the 2nd day of the month
C) Invalid syntax -- it has only 5 fields but the second field is wrong
D) Every day at 2:00 AM

> **Answer:** B -- The format is `minute hour day-of-month month day-of-week`. This runs at minute 0, every hour, but only on the 2nd of the month. To run daily at 2 AM, use `0 2 * * *`.

---

## MCQ -- Quick Check 4

**Question:** A Node.js service becomes unresponsive. `top` shows it using 100% CPU. Most likely cause:

A) Too many npm packages installed
B) Synchronous blocking operation in the event loop
C) Missing `package-lock.json`
D) Wrong Node.js version

> **Answer:** B -- A synchronous operation (like `fs.readFileSync` on a large file or an infinite loop) blocks the single-threaded event loop, making the service unresponsive.

---

## MCQ -- Quick Check 5

**Question:** In a microservices architecture, the Restaurant Service is down. What pattern prevents the Order Service from also failing?

A) Singleton pattern
B) Observer pattern
C) Circuit Breaker pattern
D) Factory pattern

> **Answer:** C -- The Circuit Breaker pattern detects repeated failures and stops making calls to the failing service, returning a cached/fallback response instead.

---

## Post-Incident Review Template

### After Every Incident

```
INCIDENT POST-MORTEM
====================
Incident ID:    INC-2026-0723
Severity:       P1 - Critical
Duration:       09:15 - 10:45 (1h 30m)
Impact:         ~7,500 orders failed

Timeline:
- 09:12 Last successful order
- 09:15 Alert fired
- 09:20 Engineer acknowledged
- 09:35 Root cause identified
- 10:30 Fix deployed
- 10:45 Service fully recovered

Root Cause:     Wrong JVM heap size after deployment
Fix:            Updated startup script with -Xmx512m
Prevention:     Add heap size to deployment checklist
                Add JVM memory monitoring alert
```

---

## Incident Communication

### Stakeholder Updates During P1

| Time | Audience | Message |
|------|----------|---------|
| +5 min | Team Slack | "Investigating Order Service outage. Impact: new orders failing." |
| +15 min | Manager | "Root cause identified: JVM config issue. ETA to fix: 30 min." |
| +30 min | Stakeholders | "Fix deployed. Monitoring recovery. Orders resuming." |
| +1 hour | All | "Incident resolved. Post-mortem scheduled for Tuesday." |

> **FoodExpress:** Communication is as important as the technical fix. Customers need to know what's happening.

---

## Skills Assessment Matrix

### What This Capsule Project Tests

| Skill | Incident 1 | Incident 2 | Incident 3 |
|-------|-----------|-----------|-----------|
| Linux commands (ps, df, ss) | X | X | |
| Shell scripting | X | X | |
| Log analysis | X | X | X |
| Java/Spring Boot config | X | | X |
| Node.js debugging | | | X |
| Microservices patterns | | | X |
| Systemd/cron management | X | X | |
| Network debugging | X | | X |
| Incident communication | X | X | X |

---

## Timeline & Expectations

| Phase | Time | Deliverable |
|-------|------|-------------|
| Incident 1 | 10:00 - 12:00 | Fixed startup script + config. Service running. |
| Incident 2 | 13:30 - 15:00 | Fixed log rotation + cleanup script. Disk < 80%. |
| Incident 3 | 15:00 - 16:30 | Fixed Node.js blocking + added timeouts. All services responding < 2s. |
| Retro | 16:30 - 17:00 | Post-mortem for one incident (your choice). |

---

## Evaluation Criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| Root Cause Identification | 30% | Did you find all bugs? |
| Fix Quality | 25% | Are fixes correct and production-ready? |
| Systematic Approach | 20% | Did you follow DRILL process? |
| Documentation | 15% | Post-mortem quality |
| Communication | 10% | Stakeholder updates during incidents |

---

## Key Takeaways

| # | Takeaway |
|---|----------|
| 1 | Always check if the process is running first -- don't start debugging code |
| 2 | Disk space and log rotation are the #1 silent killers in production |
| 3 | Cascading failures in microservices require circuit breakers and timeouts |
| 4 | JVM configuration (heap, GC) is critical -- defaults are rarely production-ready |
| 5 | Node.js event loop blocking turns a single slow call into total unresponsiveness |
| 6 | Post-mortems prevent recurrence; without them you'll fix the same bug twice |
| 7 | Communication during incidents is as important as the technical fix |

> **Next: Module 24 -- Docker Part 1: Introduction to Containerization**
