#!/bin/bash
#
# FoodExpress Deployment Script
#
# CONTAINS BUGS - Find and fix them!
#
# BUG 1: Unquoted variables - will break if paths contain spaces
# BUG 2: Missing error checks - script continues even if steps fail
# BUG 3: Hardcoded paths - not configurable, won't work on different servers

# BUG 3: Hardcoded paths - should use variables or config file
# These paths may not exist on every server
DEPLOY_DIR=/home/john/apps/foodexpress
BACKUP_DIR=/home/john/backups
WAR_FILE=/home/john/builds/foodexpress.war

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

echo "Starting FoodExpress deployment..."

# Step 1: Create backup of current deployment
# BUG 1: Unquoted variable - breaks if path contains spaces
echo "Creating backup..."
cp -r $DEPLOY_DIR $BACKUP_DIR/foodexpress_$TIMESTAMP

# BUG 2: No error check - if backup fails, we still proceed with deployment!
# If the backup directory doesn't exist or disk is full, we lose the old version.

# Step 2: Stop the application
echo "Stopping application..."
systemctl stop foodexpress
# BUG 2: Should check if the service stopped successfully

# Step 3: Deploy new version
# BUG 1: Unquoted variable - breaks if WAR_FILE path has spaces
echo "Deploying new version..."
cp $WAR_FILE $DEPLOY_DIR/foodexpress.war

# Step 4: Start the application
echo "Starting application..."
systemctl start foodexpress
# BUG 2: Should check if the service started successfully

# Step 5: Verify deployment
echo "Verifying deployment..."
sleep 10
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/health)

if [ "$HTTP_STATUS" != "200" ]; then
    echo "Deployment verification FAILED! HTTP Status: $HTTP_STATUS"
    # BUG 2: Even though verification failed, there's no rollback!
    # Should restore from backup if verification fails
else
    echo "Deployment successful!"
fi

echo "Deployment complete at $(date)"
