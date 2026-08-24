# Linux OS -- Lab Exercises
## Module 20 | Days 21-22

---

## Client Email

```
From: deepa.nair@foodexpress.in
To: sustain-engineering@team.com
Subject: Production Server Issues -- Need Debugging Help
Date: 2026-07-31

Team,

Our production Linux server is experiencing several issues:
1. Disk space is running low on the log partition
2. Several shell scripts have bugs causing cron job failures
3. Log analysis is needed to find the root cause of order failures
4. A health check script needs to be fixed

All work must be done via the Linux terminal. Please fix the
scripts, analyze the logs, and clean up the server.

-- Deepa Nair, SRE Lead, FoodExpress
```

---

## Lab 1: Log Analysis with Display & Search Commands (6 bugs)

### Setup

Create the sample log file for analysis:

```bash
# Create sample FoodExpress log file
cat > /tmp/foodexpress_app.log << 'EOF'
2026-07-27 09:00:01 INFO  [order-service] Application started on port 8080
2026-07-27 09:01:15 INFO  [order-service] Order #1001 created for customer_id=42 total=599.00
2026-07-27 09:02:30 ERROR [order-service] Order #1002 failed: NullPointerException at OrderService.java:45
2026-07-27 09:03:45 INFO  [menu-service] Menu items refreshed: 156 items loaded
2026-07-27 09:04:00 WARN  [order-service] Slow query: SELECT * FROM orders WHERE customer_id=42 (query_time=2500ms)
2026-07-27 09:05:12 ERROR [payment-service] Payment failed for order #1003: Connection timeout to payment gateway
2026-07-27 09:06:30 INFO  [order-service] Order #1004 created for customer_id=15 total=299.00
2026-07-27 09:07:45 ERROR [order-service] Order #1005 failed: NullPointerException at OrderService.java:45
2026-07-27 09:08:00 INFO  [menu-service] Search query: "Chicken & Waffles" returned 0 results
2026-07-27 09:09:15 WARN  [order-service] Slow query: SELECT * FROM orders WHERE customer_id=108 (query_time=3200ms)
2026-07-27 09:10:30 ERROR [payment-service] Payment failed for order #1006: Invalid card number
2026-07-27 09:11:45 INFO  [order-service] Order #1007 created for customer_id=42 total=450.00
2026-07-27 09:12:00 ERROR [order-service] Order #1008 failed: NullPointerException at OrderService.java:45
2026-07-27 09:13:15 FATAL [database] Connection pool exhausted: max_connections=100 active=100
2026-07-27 09:14:30 ERROR [order-service] Order #1009 failed: Database connection unavailable
2026-07-27 09:15:45 INFO  [order-service] Order #1010 created for customer_id=33 total=199.00
EOF
```

### Tasks (with buggy commands to fix)

| # | Buggy Command | Problem | Correct Command |
|---|--------------|---------|-----------------|
| 1 | `grep ERROR /tmp/foodexpress_app.log` | Also matches "NullPointerError" or other non-level uses. Need word boundary | `grep -w "ERROR" /tmp/foodexpress_app.log` |
| 2 | `grep -c "error" /tmp/foodexpress_app.log` | Case-sensitive; misses "ERROR" lines | `grep -ci "error" /tmp/foodexpress_app.log` |
| 3 | `cat /tmp/foodexpress_app.log \| grep "query_time=[0-9]"` | Does not capture multi-digit query times properly | `egrep "query_time=[0-9]+" /tmp/foodexpress_app.log` |
| 4 | `tail -5 /tmp/foodexpress_app.log > /tmp/last_errors.log` | Gets last 5 lines, but they may not all be errors | `grep "ERROR\|FATAL" /tmp/foodexpress_app.log \| tail -5 > /tmp/last_errors.log` |
| 5 | `cut -d' ' -f5 /tmp/foodexpress_app.log` | Wrong field number due to multiple spaces; does not extract service name properly | `awk '{print $4}' /tmp/foodexpress_app.log \| sort \| uniq -c \| sort -rn` |
| 6 | `find /tmp -name "*.log" -exec cat {}` | Missing `\;` at the end of -exec | `find /tmp -name "*.log" -exec cat {} \;` |

### Analysis Questions

Answer these using Linux commands:

1. How many ERROR lines are in the log? (Expected: 5)
2. How many unique services have errors? (Expected: 3)
3. What is the most common error? (Expected: NullPointerException)
4. Which customer has the most orders? (Expected: customer_id=42)
5. What are the slow query times? (Expected: 2500ms, 3200ms)

### Checkpoint
- [ ] All 6 buggy commands identified and fixed
- [ ] All 5 analysis questions answered with correct commands
- [ ] Understand difference between `grep`, `egrep`, and `awk`
- [ ] Can use pipes to chain commands effectively

---

## Lab 2: Fix the Shell Script (8 bugs)

### Buggy Script: deploy.sh

```bash
#!/bin/sh
# FoodExpress Deployment Script

# Bug 1: No error handling (script continues on failure)

APP_NAME = "order-service"          # Bug 2: Spaces around = in assignment
VERSION=$1
DEPLOY_DIR=/opt/foodexpress/$APP_NAME
LOG_FILE=/var/log/foodexpress/deploy.log

# Bug 3: Not checking if VERSION argument was provided

echo "Deploying $APP_NAME version $VERSION"
echo "Timestamp: $(date)" >> LOG_FILE   # Bug 4: Missing $ for variable

# Check if deploy directory exists
if [ -d $DEPLOY_DIR ]              # Bug 5: Missing quotes around variable
then
    echo "Deploy directory found"
else
    echo "Deploy directory not found"
    # Bug 6: Script continues even when directory is missing
fi

# Stop the service
systemctl stop $APP_NAME

# Copy new artifact
cp /tmp/${APP_NAME}-${VERSION}.jar ${DEPLOY_DIR}/app.jar

# Start the service
systemctl start $APP_NAME

# Health check
sleep 5
HEALTH=$(curl -s http://localhost:8080/health)
if [ $HEALTH = "UP" ]             # Bug 7: Unquoted variable; fails if HEALTH is empty
then
    echo "Deployment successful"
else
    echo "Deployment failed"
    # Bug 8: No rollback on failure
fi
```

### Bugs to Find and Fix

| # | Hint | Impact |
|---|------|--------|
| 1 | No `set -euo pipefail` at the top; script ignores errors | Failures go unnoticed; deployment may leave system in bad state |
| 2 | Spaces around `=` in `APP_NAME = "order-service"` | bash treats `APP_NAME` as a command, not a variable assignment |
| 3 | Script does not check if `$1` (VERSION) was provided | Deploys with empty version; copies wrong file |
| 4 | `LOG_FILE` used without `$` prefix: `>> LOG_FILE` instead of `>> $LOG_FILE` | Creates a literal file named "LOG_FILE" instead of writing to the log |
| 5 | `$DEPLOY_DIR` not quoted in `[ -d $DEPLOY_DIR ]` | Breaks if path contains spaces |
| 6 | Script continues after "directory not found" -- no `exit 1` | Tries to copy to non-existent directory |
| 7 | `$HEALTH` not quoted; if curl fails and HEALTH is empty, `[ = "UP" ]` causes syntax error | Health check always errors, never reports correctly |
| 8 | No rollback procedure when deployment fails | Failed deployment leaves the service broken |

### Fixed Script

```bash
#!/bin/bash
set -euo pipefail

APP_NAME="order-service"
VERSION="${1:-}"
DEPLOY_DIR="/opt/foodexpress/$APP_NAME"
LOG_FILE="/var/log/foodexpress/deploy.log"
BACKUP_DIR="/opt/foodexpress/backups"

# Check if VERSION argument was provided
if [ -z "$VERSION" ]; then
    echo "ERROR: Usage: $0 <version>"
    exit 1
fi

echo "Deploying $APP_NAME version $VERSION"
echo "Timestamp: $(date)" >> "$LOG_FILE"

# Check if deploy directory exists
if [ ! -d "$DEPLOY_DIR" ]; then
    echo "ERROR: Deploy directory not found: $DEPLOY_DIR"
    exit 1
fi

# Backup current version
if [ -f "${DEPLOY_DIR}/app.jar" ]; then
    mkdir -p "$BACKUP_DIR"
    cp "${DEPLOY_DIR}/app.jar" "${BACKUP_DIR}/app.jar.$(date +%Y%m%d%H%M%S)"
    echo "Backup created" >> "$LOG_FILE"
fi

# Stop the service
systemctl stop "$APP_NAME"

# Copy new artifact
cp "/tmp/${APP_NAME}-${VERSION}.jar" "${DEPLOY_DIR}/app.jar"

# Start the service
systemctl start "$APP_NAME"

# Health check
sleep 5
HEALTH=$(curl -s http://localhost:8080/health || echo "DOWN")
if [ "$HEALTH" = "UP" ]; then
    echo "Deployment successful" | tee -a "$LOG_FILE"
else
    echo "Deployment FAILED -- rolling back" | tee -a "$LOG_FILE"
    cp "${BACKUP_DIR}/$(ls -t ${BACKUP_DIR} | head -1)" "${DEPLOY_DIR}/app.jar"
    systemctl restart "$APP_NAME"
    exit 1
fi
```

### Checkpoint
- [ ] All 8 bugs identified and fixed
- [ ] Script has `set -euo pipefail`
- [ ] VERSION argument is validated
- [ ] Variables are properly quoted
- [ ] Script exits on errors (directory missing, health check fails)
- [ ] Rollback procedure implemented
- [ ] Log file is written to correctly

---

## Lab 3: Disk Space Cleanup (5 tasks)

### Scenario

The FoodExpress server is at 92% disk usage. You need to find and clean up space.

### Tasks

```bash
# Task 1: Find which directories are using the most space
# Buggy: du /var/log          (no human-readable, no depth limit)
# Fix:
du -sh /var/log/* | sort -hr | head -10

# Task 2: Find log files larger than 100MB
# Buggy: find /var/log -size 100M     (missing + prefix)
# Fix:
find /var/log -size +100M -exec ls -lh {} \;

# Task 3: Find log files older than 30 days
# Buggy: find /var/log -mtime 30      (exactly 30 days, not older)
# Fix:
find /var/log -name "*.log" -mtime +30

# Task 4: Archive old logs before deleting
# Buggy: tar -cvf old_logs.tar.gz /var/log/foodexpress/*.old
#        (missing -z flag for gzip compression)
# Fix:
tar -czvf /tmp/old_logs_$(date +%Y%m%d).tar.gz /var/log/foodexpress/*.old

# Task 5: Create a crontab entry for weekly cleanup
# Buggy: 0 2 * * * find /var/log -mtime +30 -delete
#        (deletes ALL files older than 30 days, not just logs)
# Fix:
# 0 2 * * 0 find /var/log/foodexpress -name "*.log" -mtime +30 -delete
```

### Checkpoint
- [ ] Identified top space-consuming directories
- [ ] Found files larger than 100MB
- [ ] Found files older than 30 days
- [ ] Archived old logs with compression
- [ ] Crontab entry targets only log files, not all files

---

## Lab 4: Fix the Health Check Script (6 bugs)

### Buggy Script: healthcheck.sh

```bash
#!/bin/bash
# FoodExpress Health Check

SERVICES="order-service:8080 menu-service:3000 payment-service:8081"

for svc in $SERVICES; do
    name=$(echo $svc | cut -d: -f1)
    port=$(echo $svc | cut -d: -f2)

    # Bug 1: No timeout on curl (hangs if service is unresponsive)
    result=$(curl http://localhost:$port/health)

    # Bug 2: Using = instead of == for string comparison (works in bash but not sh)
    # Bug 3: Not quoting $result (fails if empty)
    if [ $result = "UP" ]; then
        echo "$name is healthy"
    else
        echo "$name is DOWN"
        # Bug 4: No alerting mechanism
    fi
done

# Bug 5: No exit code reflecting overall health
# Bug 6: No logging
```

### Checkpoint
- [ ] curl has `--max-time` or `--connect-timeout`
- [ ] Variables are quoted in comparisons
- [ ] Alert mechanism added (email, log, or exit code)
- [ ] Script exits with non-zero code if any service is down
- [ ] Results are logged to a file with timestamps
- [ ] Script handles curl failures gracefully

---

## Bonus Challenge: Write a Log Rotation Script

Write a shell script that:

1. Finds all `.log` files in `/var/log/foodexpress/` larger than 50MB
2. Compresses them with gzip (adds `.gz` extension)
3. Deletes compressed logs older than 90 days
4. Logs its own actions to `/var/log/foodexpress/logrotate.log`
5. Sends an email summary if any files were rotated

Use: `find`, `gzip`, `wc`, `date`, functions, and control statements.
