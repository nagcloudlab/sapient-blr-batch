#!/bin/bash
# =============================================================
# FAULT INJECTION: Simulate Database Connection Pool Exhaustion
# Purpose: Open many idle MySQL connections to exhaust the pool
# Used in: M37 (Final)
# Safety:  Uses mysql client, connections are tracked and killed
#          on cleanup. Max 50 connections (configurable).
# Requires: MySQL client installed, MySQL server running
# =============================================================

ACTION=${1:-help}
NUM_CONNECTIONS=${2:-20}  # Default: 20 idle connections
DB_HOST=${3:-localhost}
DB_USER=${4:-root}
DB_PASS=${5:-password}

PID_FILE_PREFIX="/tmp/foodexpress-db-exhaust"

show_help() {
    echo "Usage: $0 {start|stop|status} [num_connections] [host] [user] [password]"
    echo ""
    echo "  start [n] [host] [user] [pass]  - Open n idle DB connections"
    echo "  stop                            - Close all idle connections"
    echo "  status                          - Show connection count"
    echo ""
    echo "Examples:"
    echo "  $0 start 20 localhost root password  # Open 20 idle connections"
    echo "  $0 stop                              # Close all"
    echo "  $0 status                            # Check current connections"
}

case "$ACTION" in
    start)
        # Safety: cap at 50
        if [ "$NUM_CONNECTIONS" -gt 50 ]; then
            echo "[SAFETY] Maximum is 50 connections. Using 50."
            NUM_CONNECTIONS=50
        fi

        echo "[FAULT INJECTION] Opening $NUM_CONNECTIONS idle MySQL connections..."
        echo "  Host: $DB_HOST"
        echo "  User: $DB_USER"

        OPENED=0
        for i in $(seq 1 $NUM_CONNECTIONS); do
            # Each mysql client runs SELECT SLEEP(3600) to hold connection for 1 hour
            mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" -e "SELECT SLEEP(3600);" \
                --connect-timeout=5 > /dev/null 2>&1 &
            PID=$!
            echo "$PID" >> "${PID_FILE_PREFIX}.pids"
            OPENED=$((OPENED + 1))
        done

        echo ""
        echo "[FAULT INJECTED] $OPENED idle connections opened."
        echo "[INFO] Check MySQL: mysql -e 'SHOW STATUS LIKE \"Threads_connected\";'"
        echo "[INFO] Participants should see 'Too many connections' errors."
        echo "[INFO] Run '$0 stop' to clean up."
        ;;

    stop)
        echo "[RECOVERY] Closing all idle connections..."
        if [ -f "${PID_FILE_PREFIX}.pids" ]; then
            COUNT=0
            while read PID; do
                kill $PID 2>/dev/null
                COUNT=$((COUNT + 1))
            done < "${PID_FILE_PREFIX}.pids"
            rm -f "${PID_FILE_PREFIX}.pids"
            echo "[CLEANUP] Killed $COUNT idle connection processes."
        else
            echo "[INFO] No PID file found. Connections may have already timed out."
        fi
        ;;

    status)
        echo "[STATUS] Checking MySQL connections..."
        if [ -f "${PID_FILE_PREFIX}.pids" ]; then
            TOTAL=$(wc -l < "${PID_FILE_PREFIX}.pids")
            ALIVE=0
            while read PID; do
                kill -0 $PID 2>/dev/null && ALIVE=$((ALIVE + 1))
            done < "${PID_FILE_PREFIX}.pids"
            echo "[FAULT ACTIVE] $ALIVE of $TOTAL injected connections still alive."
        else
            echo "[NO FAULT] No injected connections."
        fi

        # Also show actual MySQL status if accessible
        mysql -h "${DB_HOST:-localhost}" -u "${DB_USER:-root}" -p"${DB_PASS:-password}" \
            -e "SHOW STATUS LIKE 'Threads_connected';" 2>/dev/null || true
        ;;

    *)
        show_help
        ;;
esac
