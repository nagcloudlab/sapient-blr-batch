#!/bin/bash
# =============================================================
# FAULT INJECTION: Simulate Service Down
# Purpose: Kill a FoodExpress service to simulate a crash
# Used in: M34 (MidStage), M37 (Final)
# Safety:  Only kills local Node.js/Java processes by port
# =============================================================

SERVICE_PORT=${2:-3000}  # Default: Restaurant Service on port 3000
ACTION=${1:-help}

show_help() {
    echo "Usage: $0 {start|stop|status} [port]"
    echo ""
    echo "  start [port]  - Kill the service running on the specified port"
    echo "  stop  [port]  - Restart the service (runs npm start in background)"
    echo "  status [port] - Check if the port is listening"
    echo ""
    echo "Examples:"
    echo "  $0 start 3000   # Kill Restaurant Service"
    echo "  $0 start 3001   # Kill Cart Service"
    echo "  $0 start 8080   # Kill Order Service (Java)"
    echo "  $0 status 3000  # Check if port 3000 is listening"
}

case "$ACTION" in
    start)
        echo "[FAULT INJECTION] Simulating service crash on port $SERVICE_PORT..."

        # Find the PID listening on the port
        PID=$(lsof -ti :$SERVICE_PORT 2>/dev/null || netstat -tlnp 2>/dev/null | grep ":$SERVICE_PORT " | awk '{print $7}' | cut -d'/' -f1)

        if [ -z "$PID" ]; then
            echo "[WARNING] No process found on port $SERVICE_PORT. Is the service running?"
            exit 1
        fi

        # Save the PID for recovery
        echo "$PID" > "/tmp/foodexpress-fault-$SERVICE_PORT.pid"

        # Kill the process
        kill -9 $PID 2>/dev/null
        echo "[FAULT INJECTED] Process $PID on port $SERVICE_PORT has been killed."
        echo "[INFO] Participants should now investigate why the service is down."
        echo "[INFO] Run '$0 stop $SERVICE_PORT' to restart when ready."
        ;;

    stop)
        echo "[RECOVERY] Fault injection cleanup for port $SERVICE_PORT..."
        echo "[INFO] Restart the service manually using the appropriate command:"
        echo "  - Node.js: cd <service-dir> && npm start &"
        echo "  - Java:    cd order-service && mvn spring-boot:run &"
        echo "  - Docker:  docker start <container-name>"

        # Clean up PID file
        rm -f "/tmp/foodexpress-fault-$SERVICE_PORT.pid"
        echo "[CLEANUP] Fault injection artifacts removed."
        ;;

    status)
        echo "[STATUS] Checking port $SERVICE_PORT..."
        if lsof -i :$SERVICE_PORT > /dev/null 2>&1; then
            echo "[OK] Port $SERVICE_PORT is listening."
            lsof -i :$SERVICE_PORT | head -5
        else
            echo "[DOWN] Nothing is listening on port $SERVICE_PORT."
        fi
        ;;

    *)
        show_help
        ;;
esac
