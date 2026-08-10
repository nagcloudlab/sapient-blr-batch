#!/bin/bash
#
# FoodExpress Disk Cleanup Script (FIXED)
#
# ALL BUGS FIXED:
# FIX 1: Added safety checks before rm commands
# FIX 2: Added sudo where root privileges are needed
# FIX 3: Corrected find syntax - using +30 instead of 30

LOG_DIR="/var/log/foodexpress"
TEMP_DIR="/tmp/foodexpress"
BACKUP_DIR="/opt/foodexpress/backups"
BUILD_DIR="/opt/foodexpress/builds"
DAYS_TO_KEEP=30

echo "=== FoodExpress Disk Cleanup ==="
echo "Date: $(date)"
echo ""

# Show current disk usage
echo "Current disk usage:"
df -h / /var /tmp
echo ""

# FIX 1: Safety check - verify TEMP_DIR is set and is a valid directory
echo "Cleaning temp directory..."
if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"/*
    echo "Temp directory cleaned: $TEMP_DIR"
else
    echo "WARNING: Temp directory not found or variable is empty. Skipping."
fi

# FIX 3: Using +30 (older than 30 days) instead of 30 (exactly 30 days)
echo "Removing old log files (older than $DAYS_TO_KEEP days)..."
find "$LOG_DIR" -name "*.log" -mtime +30 -delete

# FIX 2: Added sudo for system journal cleanup
echo "Cleaning system journal logs older than 7 days..."
sudo journalctl --vacuum-time=7d

# FIX 3: Corrected find syntax with + sign
echo "Removing old backups (older than $DAYS_TO_KEEP days)..."
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$DAYS_TO_KEEP -delete

# FIX 2: Added sudo for docker commands
echo "Cleaning Docker resources..."
sudo docker system prune -f
sudo docker volume prune -f

# Clean npm cache
echo "Cleaning npm cache..."
npm cache clean --force

# FIX 1: Safety check before removing build artifacts
echo "Cleaning build artifacts..."
if [ -n "$BUILD_DIR" ] && [ -d "$BUILD_DIR/target" ]; then
    rm -rf "$BUILD_DIR/target"/*
    echo "Build artifacts cleaned."
else
    echo "WARNING: Build directory not found. Skipping."
fi

echo ""
echo "Disk usage after cleanup:"
df -h / /var /tmp

echo ""
echo "Cleanup complete!"
