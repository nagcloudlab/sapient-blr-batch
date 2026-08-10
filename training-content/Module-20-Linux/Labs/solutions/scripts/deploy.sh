#!/bin/bash
#
# FoodExpress Deployment Script (FIXED)
#
# ALL BUGS FIXED:
# FIX 1: All variables are properly quoted
# FIX 2: Error checks added after each critical step
# FIX 3: Paths use configurable variables instead of hardcoded values

# FIX 3: Configurable paths - can be overridden via environment variables
DEPLOY_DIR="${DEPLOY_DIR:-/opt/foodexpress/app}"
BACKUP_DIR="${BACKUP_DIR:-/opt/foodexpress/backups}"
WAR_FILE="${WAR_FILE:-/opt/foodexpress/builds/foodexpress.war}"

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

echo "Starting FoodExpress deployment..."

# FIX 2: Verify source WAR file exists before starting
if [ ! -f "$WAR_FILE" ]; then
    echo "ERROR: WAR file not found: $WAR_FILE"
    exit 1
fi

# Step 1: Create backup of current deployment
# FIX 1: Variables are quoted to handle paths with spaces
echo "Creating backup..."
cp -r "$DEPLOY_DIR" "$BACKUP_DIR/foodexpress_$TIMESTAMP"

# FIX 2: Check if backup was successful
if [ $? -ne 0 ]; then
    echo "ERROR: Backup failed! Aborting deployment."
    exit 1
fi
echo "Backup created at: $BACKUP_DIR/foodexpress_$TIMESTAMP"

# Step 2: Stop the application
echo "Stopping application..."
systemctl stop foodexpress

# FIX 2: Verify service stopped
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to stop application! Aborting deployment."
    exit 1
fi

# Step 3: Deploy new version
# FIX 1: Quoted variable
echo "Deploying new version..."
cp "$WAR_FILE" "$DEPLOY_DIR/foodexpress.war"

# FIX 2: Check if copy was successful
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to copy WAR file! Rolling back..."
    cp -r "$BACKUP_DIR/foodexpress_$TIMESTAMP"/* "$DEPLOY_DIR/"
    systemctl start foodexpress
    exit 1
fi

# Step 4: Start the application
echo "Starting application..."
systemctl start foodexpress

# FIX 2: Verify service started
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start application! Rolling back..."
    cp -r "$BACKUP_DIR/foodexpress_$TIMESTAMP"/* "$DEPLOY_DIR/"
    systemctl start foodexpress
    exit 1
fi

# Step 5: Verify deployment
echo "Verifying deployment..."
sleep 10
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/health)

if [ "$HTTP_STATUS" != "200" ]; then
    echo "Deployment verification FAILED! HTTP Status: $HTTP_STATUS"
    # FIX 2: Automatic rollback on verification failure
    echo "Rolling back to previous version..."
    systemctl stop foodexpress
    cp -r "$BACKUP_DIR/foodexpress_$TIMESTAMP"/* "$DEPLOY_DIR/"
    systemctl start foodexpress
    echo "Rollback complete."
    exit 1
else
    echo "Deployment successful!"
fi

echo "Deployment complete at $(date)"
