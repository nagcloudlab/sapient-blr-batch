#!/bin/bash
# FoodExpress Disk Cleanup Script
# Should run daily via cron at 2:00 AM
# BUG: Cron schedule in comment says: 0 * 2 * * (wrong format, should be: 0 2 * * *)

APP_DIR="/opt/foodexpress"
LOG_DIR="/var/log/foodexpress"
RETENTION_DAYS=30

echo "=== FoodExpress Disk Cleanup ==="
echo "Date: $(date)"
echo "Disk usage before cleanup:"
df -h /var/log

# Clean old log files
echo ""
echo "Cleaning log files older than ${RETENTION_DAYS} days..."
# BUG: Missing -type f (will also try to delete directories) and -mtime should be +30 not -30
find ${LOG_DIR} -name "*.log.*" -mtime -30 -delete
echo "Log cleanup complete"

# Clean old deployment artifacts
echo ""
echo "Cleaning old deployment releases..."
RELEASES_DIR="${APP_DIR}/releases"
if [ -d "${RELEASES_DIR}" ]; then
    # Keep only last 3 releases
    ls -dt ${RELEASES_DIR}/*/ | tail -n +4 | xargs rm -rf
fi

# Clean temp files
echo ""
echo "Cleaning temp files..."
find /tmp -name "foodexpress-*" -type f -mtime +7 -delete

# Clean old heap dumps
echo ""
echo "Cleaning old heap dumps..."
find ${APP_DIR} -name "*.hprof" -type f -mtime +3 -delete

echo ""
echo "Disk usage after cleanup:"
df -h /var/log

echo ""
echo "=== Cleanup Complete ==="
