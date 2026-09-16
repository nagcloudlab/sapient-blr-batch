#!/bin/bash
# Automated Health Check & Restart Script
# Replaces manual toil: "check service health and restart if down"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICES_DIR="$SCRIPT_DIR/../services"
SERVICES=("http://localhost:3000/health:order-service" "http://localhost:8080/health:payment-service")
LOG_FILE="$SCRIPT_DIR/health-check.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_service() {
    local url=$1
    local name=$2

    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null)

    if [ "$response" = "200" ]; then
        log "OK: $name is healthy (HTTP $response)"
        return 0
    else
        log "FAIL: $name is unhealthy (HTTP $response)"
        return 1
    fi
}

restart_service() {
    local name=$1
    log "ACTION: Restarting $name..."
    cd "$SERVICES_DIR" && docker compose restart "$name" 2>/dev/null
    cd - > /dev/null
    sleep 5
}

log "========== Health Check Started =========="

for entry in "${SERVICES[@]}"; do
    url="${entry%:*}"
    # Fix: extract name properly (everything after the last colon)
    name="${entry##*:}"

    if ! check_service "$url" "$name"; then
        restart_service "$name"

        # Verify after restart
        if check_service "$url" "$name"; then
            log "RECOVERED: $name is back up after restart"
        else
            log "ALERT: $name still unhealthy after restart -- needs manual intervention!"
        fi
    fi
done

log "========== Health Check Complete =========="
