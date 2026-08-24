# FoodExpress Health Check Script
#
# CONTAINS BUGS - Find and fix them!
#
# BUG 1: Missing shebang (#!/bin/bash) - script may not run with correct shell
# BUG 2: Wrong comparison operator - using -eq (numeric) for string comparison
# BUG 3: Wrong curl URL - health endpoint path is incorrect

# BUG 1: Missing shebang line!
# Without #!/bin/bash, the script might be interpreted by sh or another shell,
# causing bash-specific features to fail.

APP_NAME="foodexpress"
# BUG 3: Wrong health check URL - should be /api/health not /health-check
HEALTH_URL="http://localhost:8080/health-check"
LOG_FILE="/var/log/foodexpress/health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Running health check for $APP_NAME..."

# Check if the application is responding
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

# BUG 2: Using -eq (numeric comparison) to compare a string HTTP status
# -eq is for integers only. For string comparison, use == or =
# This will cause "integer expression expected" error if HTTP_STATUS is not a number
if [ "$HTTP_STATUS" -eq "200" ]; then
    echo "[$TIMESTAMP] $APP_NAME is healthy (HTTP $HTTP_STATUS)" >> $LOG_FILE
    echo "Health check PASSED"
else
    echo "[$TIMESTAMP] $APP_NAME is UNHEALTHY (HTTP $HTTP_STATUS)" >> $LOG_FILE
    echo "Health check FAILED - HTTP Status: $HTTP_STATUS"

    # Check if process is running
    PID=$(pgrep -f $APP_NAME)
    if [ -z "$PID" ]; then
        echo "[$TIMESTAMP] Process not found! Attempting restart..." >> $LOG_FILE
        systemctl restart $APP_NAME
    else
        echo "[$TIMESTAMP] Process is running (PID: $PID) but not responding" >> $LOG_FILE
    fi
fi

# Check disk usage
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt 85 ]; then
    echo "[$TIMESTAMP] WARNING: Disk usage at ${DISK_USAGE}%" >> $LOG_FILE
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2 {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 90 ]; then
    echo "[$TIMESTAMP] WARNING: Memory usage at ${MEM_USAGE}%" >> $LOG_FILE
fi

echo "[$TIMESTAMP] Health check complete." >> $LOG_FILE
