# Linux Lab Setup -- FoodExpress Production Server Simulation

## Day 19-20 | Sustain Engineering Training

---

## What This Is

We simulate a production Linux server for FoodExpress. Instead of teaching commands in isolation, you'll investigate a **real production incident** using the terminal.

**Scenario:** FoodExpress order service is DOWN. 47 customer complaints in 10 minutes. You SSH into the server. All you have is a terminal.

---

## Setup Instructions

### For WSL (Windows) users:

```bash
# Open PowerShell as Administrator and run:
wsl --install
# Restart your laptop. Then open "Ubuntu" from Start Menu.
```

### For Git Bash (Windows) users:

```bash
# Git Bash is already installed from the Git module.
# Open Git Bash from Start Menu.
# Most Day 1 commands work. For top/ps/kill, use the browser terminal below.
```

### Browser fallback (if WSL/Git Bash doesn't work):

Open **https://bellard.org/jslinux/** → Click **Alpine Linux 3.12.0 Console**

---

## Create the Simulated Server

Copy and paste this ENTIRE block into your terminal. It creates the FoodExpress server directory structure with realistic log files, config files, and process data.

```bash
# Create directory structure
mkdir -p /tmp/foodexpress-server/{var/log/foodexpress/archived,opt/foodexpress/order-service,etc/foodexpress,tmp,proc}

# Create the application log (35 entries, realistic incident timeline)
cat > /tmp/foodexpress-server/var/log/foodexpress/app.log << 'EOF'
2026-08-24 09:00:01 INFO  [order-service] Application started on port 8080
2026-08-24 09:00:05 INFO  [menu-service] Application started on port 3000
2026-08-24 09:00:08 INFO  [payment-service] Application started on port 8081
2026-08-24 09:01:15 INFO  [order-service] Order #1001 created for customer_id=42 total=599.00
2026-08-24 09:01:30 INFO  [order-service] Order #1002 created for customer_id=15 total=299.00
2026-08-24 09:02:30 ERROR [order-service] Order #1003 failed: NullPointerException at OrderService.java:45
2026-08-24 09:03:45 INFO  [menu-service] Menu items refreshed: 156 items loaded
2026-08-24 09:04:00 WARN  [order-service] Slow query: SELECT * FROM orders WHERE customer_id=42 (query_time=2500ms)
2026-08-24 09:05:12 ERROR [payment-service] Payment failed for order #1004: Connection timeout to payment gateway
2026-08-24 09:06:30 INFO  [order-service] Order #1005 created for customer_id=42 total=450.00
2026-08-24 09:07:15 INFO  [order-service] Order #1006 created for customer_id=88 total=320.00
2026-08-24 09:07:45 ERROR [order-service] Order #1007 failed: NullPointerException at OrderService.java:45
2026-08-24 09:08:00 INFO  [menu-service] Search query: "Chicken Biryani" returned 3 results
2026-08-24 09:08:30 INFO  [menu-service] Search query: "Paneer Tikka" returned 5 results
2026-08-24 09:09:15 WARN  [order-service] Slow query: SELECT * FROM orders WHERE customer_id=108 (query_time=3200ms)
2026-08-24 09:09:45 WARN  [payment-service] Retry attempt 1 for order #1004
2026-08-24 09:10:30 ERROR [payment-service] Payment failed for order #1008: Invalid card number
2026-08-24 09:11:00 INFO  [order-service] Order #1009 created for customer_id=42 total=150.00
2026-08-24 09:11:45 INFO  [order-service] Order #1010 created for customer_id=33 total=199.00
2026-08-24 09:12:00 ERROR [order-service] Order #1011 failed: NullPointerException at OrderService.java:45
2026-08-24 09:12:30 WARN  [order-service] Slow query: SELECT * FROM orders WHERE customer_id=42 (query_time=4100ms)
2026-08-24 09:13:15 FATAL [database] Connection pool exhausted: max_connections=100 active=100 waiting=23
2026-08-24 09:13:16 ERROR [order-service] Order #1012 failed: Database connection unavailable
2026-08-24 09:13:17 ERROR [order-service] Order #1013 failed: Database connection unavailable
2026-08-24 09:13:18 ERROR [payment-service] Payment processing halted: upstream database unavailable
2026-08-24 09:13:20 ERROR [order-service] Order #1014 failed: Database connection unavailable
2026-08-24 09:13:30 WARN  [menu-service] Cache miss rate exceeding threshold: 78%
2026-08-24 09:14:00 ERROR [order-service] Order #1015 failed: Database connection unavailable
2026-08-24 09:14:30 FATAL [database] Auto-restart failed: lock file exists /tmp/db.lock
2026-08-24 09:15:00 INFO  [order-service] Order #1016 created for customer_id=33 total=199.00
2026-08-24 09:15:15 WARN  [order-service] Response time degraded: avg=4500ms (threshold=1000ms)
2026-08-24 09:15:30 ERROR [order-service] Order #1017 failed: Read timed out
2026-08-24 09:16:00 INFO  [menu-service] Health check: OK
2026-08-24 09:16:15 ERROR [order-service] Health check: FAIL (database unreachable)
2026-08-24 09:16:30 ERROR [payment-service] Health check: FAIL (upstream unavailable)
EOF

# Create the access log (28 HTTP requests)
cat > /tmp/foodexpress-server/var/log/foodexpress/access.log << 'EOF'
192.168.1.10 - - [24/Aug/2026:09:01:15 +0530] "POST /api/orders HTTP/1.1" 201 342 0.045
192.168.1.22 - - [24/Aug/2026:09:01:30 +0530] "POST /api/orders HTTP/1.1" 201 342 0.038
192.168.1.10 - - [24/Aug/2026:09:02:30 +0530] "POST /api/orders HTTP/1.1" 500 128 0.002
192.168.1.45 - - [24/Aug/2026:09:03:45 +0530] "GET /api/menu HTTP/1.1" 200 15234 0.120
192.168.1.10 - - [24/Aug/2026:09:04:00 +0530] "GET /api/orders?customer_id=42 HTTP/1.1" 200 8921 2.501
192.168.1.33 - - [24/Aug/2026:09:05:12 +0530] "POST /api/payments HTTP/1.1" 504 89 30.001
192.168.1.10 - - [24/Aug/2026:09:06:30 +0530] "POST /api/orders HTTP/1.1" 201 342 0.052
192.168.1.88 - - [24/Aug/2026:09:07:15 +0530] "POST /api/orders HTTP/1.1" 201 342 0.041
192.168.1.10 - - [24/Aug/2026:09:07:45 +0530] "POST /api/orders HTTP/1.1" 500 128 0.002
192.168.1.55 - - [24/Aug/2026:09:08:00 +0530] "GET /api/menu/search?q=Chicken+Biryani HTTP/1.1" 200 2341 0.089
192.168.1.77 - - [24/Aug/2026:09:08:30 +0530] "GET /api/menu/search?q=Paneer+Tikka HTTP/1.1" 200 3892 0.095
192.168.1.108 - - [24/Aug/2026:09:09:15 +0530] "GET /api/orders?customer_id=108 HTTP/1.1" 200 12043 3.201
192.168.1.10 - - [24/Aug/2026:09:10:30 +0530] "POST /api/payments HTTP/1.1" 400 67 0.015
192.168.1.10 - - [24/Aug/2026:09:11:00 +0530] "POST /api/orders HTTP/1.1" 201 342 0.048
192.168.1.33 - - [24/Aug/2026:09:11:45 +0530] "POST /api/orders HTTP/1.1" 201 342 0.039
192.168.1.10 - - [24/Aug/2026:09:12:00 +0530] "POST /api/orders HTTP/1.1" 500 128 0.002
192.168.1.10 - - [24/Aug/2026:09:12:30 +0530] "GET /api/orders?customer_id=42 HTTP/1.1" 200 8921 4.102
192.168.1.10 - - [24/Aug/2026:09:13:15 +0530] "POST /api/orders HTTP/1.1" 503 45 0.001
192.168.1.22 - - [24/Aug/2026:09:13:16 +0530] "POST /api/orders HTTP/1.1" 503 45 0.001
192.168.1.45 - - [24/Aug/2026:09:13:17 +0530] "POST /api/payments HTTP/1.1" 503 45 0.001
192.168.1.88 - - [24/Aug/2026:09:13:18 +0530] "POST /api/orders HTTP/1.1" 503 45 0.001
192.168.1.55 - - [24/Aug/2026:09:13:20 +0530] "POST /api/orders HTTP/1.1" 503 45 0.001
192.168.1.10 - - [24/Aug/2026:09:14:00 +0530] "POST /api/orders HTTP/1.1" 503 45 0.001
192.168.1.33 - - [24/Aug/2026:09:14:30 +0530] "GET /api/health HTTP/1.1" 503 22 0.001
192.168.1.10 - - [24/Aug/2026:09:15:00 +0530] "POST /api/orders HTTP/1.1" 201 342 0.055
192.168.1.33 - - [24/Aug/2026:09:15:30 +0530] "POST /api/orders HTTP/1.1" 500 128 0.002
192.168.1.10 - - [24/Aug/2026:09:16:15 +0530] "GET /api/health HTTP/1.1" 503 22 0.001
192.168.1.10 - - [24/Aug/2026:09:16:30 +0530] "GET /api/health HTTP/1.1" 503 22 0.001
EOF

# Create production config
cat > /tmp/foodexpress-server/etc/foodexpress/config_prod.properties << 'EOF'
## FoodExpress Production Configuration
app.name=foodexpress
app.env=production
app.port=8080

## Database
db.host=prod-db-01.foodexpress.internal
db.port=5432
db.name=foodexpress_prod
db.username=app_user
db.password=Pr0d$ecure!2026
db.max_connections=100
db.connection_timeout=5000

## Payment Gateway
payment.gateway.url=https://api.razorpay.com/v2
payment.gateway.timeout=30000
payment.gateway.retry_count=3

## Logging
log.level=INFO
log.file=/var/log/foodexpress/app.log
log.max_size=100MB
log.retention_days=30
EOF

# Create staging config
cat > /tmp/foodexpress-server/etc/foodexpress/config_staging.properties << 'EOF'
## FoodExpress Staging Configuration
app.name=foodexpress
app.env=staging
app.port=8080

## Database
db.host=staging-db-01.foodexpress.internal
db.port=5432
db.name=foodexpress_staging
db.username=app_user
db.password=St@ging2026
db.max_connections=50
db.connection_timeout=10000

## Payment Gateway
payment.gateway.url=https://sandbox.razorpay.com/v2
payment.gateway.timeout=60000
payment.gateway.retry_count=5

## Logging
log.level=DEBUG
log.file=/var/log/foodexpress/app.log
log.max_size=50MB
log.retention_days=7
EOF

# Create the lock file (this is what blocks DB restart)
touch /tmp/foodexpress-server/tmp/db.lock

# Create some large files to simulate disk usage
dd if=/dev/zero of=/tmp/foodexpress-server/var/log/foodexpress/app.log.2026-08-20 bs=1024 count=5120 2>/dev/null
dd if=/dev/zero of=/tmp/foodexpress-server/var/log/foodexpress/app.log.2026-08-21 bs=1024 count=2048 2>/dev/null
dd if=/dev/zero of=/tmp/foodexpress-server/var/log/foodexpress/gc.log bs=1024 count=15360 2>/dev/null
dd if=/dev/zero of=/tmp/foodexpress-server/var/log/foodexpress/access.log.2026-08-20 bs=1024 count=8192 2>/dev/null

# Create other server files
touch /tmp/foodexpress-server/var/log/foodexpress/app.log.2026-08-22
touch /tmp/foodexpress-server/var/log/foodexpress/app.log.2026-08-23
touch /tmp/foodexpress-server/var/log/foodexpress/error.log
touch /tmp/foodexpress-server/opt/foodexpress/order-service/app.jar
touch /tmp/foodexpress-server/opt/foodexpress/order-service/config.yml
touch /tmp/foodexpress-server/etc/foodexpress/.env.backup
touch /tmp/foodexpress-server/var/log/foodexpress/archived/app.log.2026-07-15.gz
touch /tmp/foodexpress-server/var/log/foodexpress/archived/app.log.2026-07-20.gz

echo ""
echo "=========================================="
echo "  FoodExpress Server Simulation Ready!"
echo "=========================================="
echo ""
echo "  cd /tmp/foodexpress-server"
echo ""
echo "  Your server has:"
echo "  - Application logs  : var/log/foodexpress/app.log"
echo "  - Access logs       : var/log/foodexpress/access.log"
echo "  - Prod config       : etc/foodexpress/config_prod.properties"
echo "  - Staging config    : etc/foodexpress/config_staging.properties"
echo "  - A lock file       : tmp/db.lock"
echo "  - Large old log files for disk cleanup exercises"
echo ""
echo "  Start with: cd /tmp/foodexpress-server"
echo "=========================================="
```

---

## Verify Setup

After running the setup script, verify it worked:

```bash
cd /tmp/foodexpress-server
ls -R
```

You should see:
```
etc/foodexpress/
opt/foodexpress/order-service/
tmp/
var/log/foodexpress/
var/log/foodexpress/archived/
```

You're ready. Start with **Section 1**.
