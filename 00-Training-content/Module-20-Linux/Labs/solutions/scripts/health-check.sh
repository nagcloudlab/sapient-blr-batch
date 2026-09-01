#!/bin/bash
#
# FoodExpress Health Check Script (FIXED)
#
# ALL BUGS FIXED:
# FIX 1: Added shebang line (#!/bin/bash)
# FIX 2: Changed -eq to == for string comparison
# FIX 3: Corrected health check URL to /api/health

APP_NAME="foodexpress"
# FIX 3: Corrected health endpoint URL
HEALTH_URL="http://localhost:8080/api/health"
LOG_FILE="/var/log/foodexpress/health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Running health check for $APP_NAME..."

# Check if the application is responding
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL")

# FIX 2: Using == for string comparison instead of -eq
# -eq is for integer comparison only; == works for strings
if [ "$HTTP_STATUS" == "200" ]; then
    echo "[$TIMESTAMP] $APP_NAME is healthy (HTTP $HTTP_STATUS)" >> "$LOG_FILE"
    echo "Health check PASSED"
else
    echo "[$TIMESTAMP] $APP_NAME is UNHEALTHY (HTTP $HTTP_STATUS)" >> "$LOG_FILE"
    echo "Health check FAILED - HTTP Status: $HTTP_STATUS"

    # Check if process is running
    PID=$(pgrep -f "$APP_NAME")
    if [ -z "$PID" ]; then
        echo "[$TIMESTAMP] Process not found! Attempting restart..." >> "$LOG_FILE"
        systemctl restart "$APP_NAME"
    else
        echo "[$TIMESTAMP] Process is running (PID: $PID) but not responding" >> "$LOG_FILE"
    fi
fi

# Check disk usage
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt 85 ]; then
    echo "[$TIMESTAMP] WARNING: Disk usage at ${DISK_USAGE}%" >> "$LOG_FILE"
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2 {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 90 ]; then
    echo "[$TIMESTAMP] WARNING: Memory usage at ${MEM_USAGE}%" >> "$LOG_FILE"
fi

echo "[$TIMESTAMP] Health check complete." >> "$LOG_FILE"
