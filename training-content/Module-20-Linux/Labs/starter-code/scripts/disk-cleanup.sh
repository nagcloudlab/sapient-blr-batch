#!/bin/bash
#
# FoodExpress Disk Cleanup Script
#
# CONTAINS BUGS - Find and fix them!
#
# BUG 1: Dangerous rm without path check - could delete root filesystem
# BUG 2: Missing sudo - cleanup commands need root privileges
# BUG 3: Wrong find syntax - -mtime argument is incorrect

LOG_DIR="/var/log/foodexpress"
TEMP_DIR="/tmp/foodexpress"
BACKUP_DIR="/opt/foodexpress/backups"
DAYS_TO_KEEP=30

echo "=== FoodExpress Disk Cleanup ==="
echo "Date: $(date)"
echo ""

# Show current disk usage
echo "Current disk usage:"
df -h / /var /tmp
echo ""

# BUG 1: Dangerous! If TEMP_DIR is empty/unset, this becomes 'rm -rf /*'
# The variable $TEMP_DIR could be empty, making this 'rm -rf /*'
# which would DELETE EVERYTHING on the system!
echo "Cleaning temp directory..."
rm -rf $TEMP_DIR/*

# BUG 3: Wrong find syntax
# -mtime 30 means exactly 30 days old, not "older than 30 days"
# Should be -mtime +30 (with plus sign) for "older than 30 days"
echo "Removing old log files..."
find $LOG_DIR -name "*.log" -mtime 30 -delete

# BUG 2: Missing sudo - /var/log cleanup needs root privileges
echo "Cleaning system journal logs older than 7 days..."
journalctl --vacuum-time=7d

# BUG 3: Same wrong find syntax - missing the + sign
echo "Removing old backups..."
find $BACKUP_DIR -name "*.tar.gz" -mtime $DAYS_TO_KEEP -delete

# BUG 2: Missing sudo for docker commands (unless user is in docker group)
echo "Cleaning Docker resources..."
docker system prune -f
docker volume prune -f

# Clean npm cache
echo "Cleaning npm cache..."
npm cache clean --force

# BUG 1: Another dangerous rm - no check if directory variable is set
echo "Cleaning build artifacts..."
rm -rf $BUILD_DIR/target/*

echo ""
echo "Disk usage after cleanup:"
df -h / /var /tmp

echo ""
echo "Cleanup complete!"
