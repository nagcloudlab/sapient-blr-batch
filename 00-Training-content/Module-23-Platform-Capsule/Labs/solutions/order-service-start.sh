#!/bin/bash
# FoodExpress Order Service Startup Script
# Systemd ExecStart should point to: /opt/foodexpress/order-service/start.sh
# FIX: Corrected systemd ExecStart path to /opt/foodexpress/order-service/start.sh

APP_NAME="order-service"
APP_DIR="/opt/foodexpress/order-service"
LOG_DIR="/var/log/foodexpress"
PID_FILE="/var/run/foodexpress/${APP_NAME}.pid"

# FIX: Changed from java-11 to java-17
JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
JAVA_CMD="${JAVA_HOME}/bin/java"

# FIX: Increased heap from 64m to 512m for production workload
JVM_OPTS="-Xms256m -Xmx512m -XX:+UseG1GC"

JAR_FILE="${APP_DIR}/order-service-1.0.0.jar"
CONFIG_FILE="${APP_DIR}/config/application.yml"

# Ensure log directory exists with correct permissions
mkdir -p ${LOG_DIR}
# FIX: Changed from 644 to 755 -- directories need execute permission for traversal
chmod 755 ${LOG_DIR}

echo "Starting ${APP_NAME}..."
echo "Java: ${JAVA_CMD}"
echo "JVM Options: ${JVM_OPTS}"
echo "Config: ${CONFIG_FILE}"

# Check if already running
if [ -f ${PID_FILE} ]; then
    OLD_PID=$(cat ${PID_FILE})
    if ps -p ${OLD_PID} > /dev/null 2>&1; then
        echo "${APP_NAME} is already running with PID ${OLD_PID}"
        exit 1
    else
        echo "Removing stale PID file"
        rm -f ${PID_FILE}
    fi
fi

# Start the service
${JAVA_CMD} ${JVM_OPTS} \
    -jar ${JAR_FILE} \
    --spring.config.location=${CONFIG_FILE} \
    >> ${LOG_DIR}/${APP_NAME}.log 2>&1 &

NEW_PID=$!
echo ${NEW_PID} > ${PID_FILE}
echo "${APP_NAME} started with PID ${NEW_PID}"

# Wait and verify
sleep 5
if ps -p ${NEW_PID} > /dev/null 2>&1; then
    echo "${APP_NAME} is running successfully"
else
    echo "ERROR: ${APP_NAME} failed to start. Check ${LOG_DIR}/${APP_NAME}.log"
    exit 1
fi
