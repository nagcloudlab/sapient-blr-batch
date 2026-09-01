#!/bin/bash

APP_DIR="."
LOG_DIR="./logs"
APP_NAME="quickticket"

echo "Starting QuickTicket deployment..."

mkdir $LOG_DIR

cd $APP_DIR

npm install --production

echo "Running database migrations..."
node scripts/migrate.js

echo "Starting application..."
nohup node server.js > $LOG_DIR/app.log 2>&1 &

echo "Deployment complete. PID: $!"
echo "Logs: tail -f $LOG_DIR/app.log"
