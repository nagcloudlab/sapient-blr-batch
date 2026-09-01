#!/bin/bash
# =============================================================================
# FoodExpress War Game — Fault Injection Script
# =============================================================================
#
# Purpose:   Inject controlled faults into FoodExpress Docker services during
#            the MidStage War Game (M34, Day 35) and Final War Game (M37, Day 43-44)
#
# Safety:    All faults target Docker containers only. Nothing touches the host
#            system permanently. Every fault has a matching reset command.
#            All changes are reversible within seconds using: ./inject-faults-wargame.sh reset
#
# Usage:     ./inject-faults-wargame.sh <command>
#
# Commands:
#   search-slow         Drop MongoDB text index -> restaurant search becomes slow
#   cart-memory-leak    Signal cart-service to activate leak code path
#   delivery-timeout    Add network delay to delivery-service container
#   order-db-slow       Inject sleep into MySQL queries via order-service container
#   payment-down        Block payment gateway in payment-service /etc/hosts
#   status              Show current state of all services (latency, memory, health)
#   reset               Restore all services to normal operating state
#
# Requirements:
#   - Docker and Docker Compose installed and running
#   - FoodExpress services running via: docker compose up -d
#   - tc (traffic control) available inside delivery-service container
#   - curl available on the host for health checks
#
# =============================================================================
# WAR GAME DAY SCHEDULE
# =============================================================================
#
# MID-STAGE WAR GAME — Day 35 (Module 34)
# -----------------------------------------
# 09:00   Participants arrive. Trainer confirms all services healthy via: status
# 09:30   INJECT: search-slow
#         Expected detection: Grafana shows p95 latency spike on /api/restaurants/search
#         Participants should: notice via dashboard, grep application logs, identify slow query
#         Reset when: team has written ServiceNow incident, diagnosed root cause, rebuilt index
#
# 11:00   INJECT: cart-memory-leak
#         Expected detection: container memory graph in Grafana climbs steadily
#         Participants should: spot RSS growth, correlate with cart-service, raise ticket
#         Reset when: team has proposed fix (restart container + patch leak code path)
#
# 13:30   INJECT: delivery-timeout (after lunch)
#         Expected detection: order tracking UI shows ETA timeouts; 504 errors in Apache log
#         Participants should: check delivery-service health endpoint, inspect network, escalate
#         Reset when: team has written RCA draft
#
# 15:00   INJECT: order-db-slow
#         Expected detection: order placement latency rises; MySQL slow query log fills
#         Participants should: tail slow query log inside container, identify missing index
#         Reset when: team has applied fix and verified order latency returns to baseline
#
# FINAL WAR GAME — Days 43-44 (Module 37)
# -----------------------------------------
# Day 43 09:30   INJECT: payment-down (P1 scenario — all orders failing at checkout)
#         This is the primary assessment scenario. All other faults cleared before injection.
#         Participants must:
#           1. Detect via Grafana (payment success rate drops to 0%)
#           2. Raise P1 incident in ServiceNow within 15 minutes of detection
#           3. Draft customer-facing status update (AI assist permitted)
#           4. Investigate root cause (/etc/hosts modification in container)
#           5. Apply fix (reset hosts file)
#           6. Verify payment flow end-to-end before closing ticket
#           7. Write post-mortem and problem record by Day 44 morning
#
# Day 43 14:00   INJECT: search-slow + delivery-timeout (concurrent faults)
#         Tests: can the team triage two simultaneous incidents without conflating them?
#         Each must get its own ServiceNow ticket with correct priority.
#
# Day 44 morning: Post-mortem presentations. Trainer resets environment fully.
#
# =============================================================================

set -euo pipefail

# --- Configuration -----------------------------------------------------------

COMPOSE_PROJECT="foodexpress"

# Container names (must match docker-compose.yml service names)
RESTAURANT_CONTAINER="${COMPOSE_PROJECT}-restaurant-service-1"
CART_CONTAINER="${COMPOSE_PROJECT}-cart-service-1"
DELIVERY_CONTAINER="${COMPOSE_PROJECT}-delivery-service-1"
ORDER_CONTAINER="${COMPOSE_PROJECT}-order-service-1"
PAYMENT_CONTAINER="${COMPOSE_PROJECT}-payment-service-1"
MONGO_CONTAINER="${COMPOSE_PROJECT}-mongodb-1"
MYSQL_CONTAINER="${COMPOSE_PROJECT}-mysql-1"

# Service ports (host-mapped)
RESTAURANT_PORT=3000
CART_PORT=3001
DELIVERY_PORT=3002
ORDER_PORT=8080
PAYMENT_PORT=3003

# Network delay for delivery-service fault (milliseconds)
DELIVERY_DELAY_MS=2000

# Payment gateway host to block (update to match your docker-compose environment)
PAYMENT_GATEWAY_HOST="payment-gateway.internal"
PAYMENT_GATEWAY_BLOCK_IP="0.0.0.0"

# State tracking directory
STATE_DIR="/tmp/foodexpress-wargame"

# --- Colours for terminal output ---------------------------------------------

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# --- Helper functions --------------------------------------------------------

log_inject() {
    echo -e "${RED}[FAULT INJECTED]${RESET} $*"
}

log_reset() {
    echo -e "${GREEN}[RESTORED]${RESET} $*"
}

log_info() {
    echo -e "${CYAN}[INFO]${RESET} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARNING]${RESET} $*"
}

log_header() {
    echo ""
    echo -e "${BOLD}$*${RESET}"
    echo "$(echo "$*" | sed 's/./-/g')"
}

require_container_running() {
    local container="$1"
    if ! docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        echo -e "${RED}[ERROR]${RESET} Container '${container}' is not running."
        echo "        Run: docker compose up -d"
        exit 1
    fi
}

mkdir -p "${STATE_DIR}"

# =============================================================================
# FAULT COMMANDS
# =============================================================================

cmd_search_slow() {
    log_header "FAULT: search-slow"
    log_info "Dropping MongoDB text index on restaurants collection..."
    log_info "This causes full collection scans on /api/restaurants/search"
    log_info "Expected symptom: search latency increases from ~20ms to 800ms+"

    require_container_running "${MONGO_CONTAINER}"

    docker exec "${MONGO_CONTAINER}" mongosh foodexpress --quiet --eval '
        db.restaurants.dropIndexes();
        print("All indexes dropped from restaurants collection.");
        print("Remaining indexes: " + JSON.stringify(db.restaurants.getIndexes()));
    '

    # Record state for reset
    echo "search-slow" >> "${STATE_DIR}/active-faults"

    log_inject "MongoDB text index dropped on restaurants collection."
    echo ""
    log_info "Trainer notes:"
    log_info "  - Participants should see latency spike in Grafana within 1-2 minutes"
    log_info "  - Restaurant search still works but is slow (full scan, not index)"
    log_info "  - Application logs will show: 'query executor using COLLSCAN'"
    log_info "  - Fix: rebuild index via: db.restaurants.createIndex({ name: 'text', cuisine: 'text' })"
    log_info "  - Reset this fault: $0 reset"
}

cmd_cart_memory_leak() {
    log_header "FAULT: cart-memory-leak"
    log_info "Sending SIGUSR1 to cart-service Node.js process to activate leak code path..."
    log_info "Expected symptom: container RSS memory grows ~50MB per minute"

    require_container_running "${CART_CONTAINER}"

    # The cart-service is coded with a process.on('SIGUSR1') handler that
    # activates a deliberate array accumulation loop (simulated leak).
    # This signal triggers that handler without crashing the process.
    docker exec "${CART_CONTAINER}" sh -c '
        PID=$(pgrep -f "node.*cart" | head -1)
        if [ -z "$PID" ]; then
            echo "ERROR: Node.js cart process not found inside container"
            exit 1
        fi
        kill -USR1 "$PID"
        echo "Sent SIGUSR1 to cart-service PID ${PID}"
    '

    echo "cart-memory-leak" >> "${STATE_DIR}/active-faults"

    log_inject "Memory leak activated in cart-service."
    echo ""
    log_info "Trainer notes:"
    log_info "  - Grafana container memory panel will show steady upward trend"
    log_info "  - Cart service remains functional — this is a slow leak, not a crash"
    log_info "  - Participants should correlate memory growth with cart-service container"
    log_info "  - Correct response: raise incident, identify process, plan restart + patch"
    log_info "  - Reset: $0 reset  (sends SIGUSR2 to deactivate leak handler)"
}

cmd_delivery_timeout() {
    log_header "FAULT: delivery-timeout"
    log_info "Injecting ${DELIVERY_DELAY_MS}ms network delay on delivery-service container eth0..."
    log_info "Expected symptom: /api/delivery/status calls return after 2+ seconds; 504s in logs"

    require_container_running "${DELIVERY_CONTAINER}"

    # Use tc (traffic control) inside the container to add egress delay.
    # The delivery-service image must have iproute2 installed.
    docker exec --privileged "${DELIVERY_CONTAINER}" sh -c "
        if ! command -v tc > /dev/null 2>&1; then
            echo 'tc not found — installing iproute2'
            apt-get install -y iproute2 -qq
        fi
        # Clear any existing qdisc first
        tc qdisc del dev eth0 root 2>/dev/null || true
        # Add netem delay
        tc qdisc add dev eth0 root netem delay ${DELIVERY_DELAY_MS}ms 200ms distribution normal
        echo 'Network delay applied to eth0'
        tc qdisc show dev eth0
    "

    echo "delivery-timeout" >> "${STATE_DIR}/active-faults"

    log_inject "${DELIVERY_DELAY_MS}ms (+/- 200ms jitter) delay added to delivery-service network."
    echo ""
    log_info "Trainer notes:"
    log_info "  - Delivery ETA responses will timeout from order-service and frontend"
    log_info "  - Apache error log will show 504 Gateway Timeout for /api/delivery/"
    log_info "  - Grafana will show delivery-service p99 latency exceeding SLO threshold"
    log_info "  - This does NOT crash the service — it just makes it very slow"
    log_info "  - Participants should: check health endpoint, inspect network, not restart blindly"
    log_info "  - Reset: $0 reset"
}

cmd_order_db_slow() {
    log_header "FAULT: order-db-slow"
    log_info "Injecting SLEEP into MySQL query execution via order-service container..."
    log_info "Expected symptom: order placement takes 5+ seconds; slow query log fills"

    require_container_running "${MYSQL_CONTAINER}"

    # Create a MySQL stored procedure that wraps order inserts with a SLEEP call.
    # The order-service Java app calls a specific stored procedure for order creation.
    # If no stored procedure exists in the project, we inject a trigger instead.
    docker exec "${MYSQL_CONTAINER}" mysql -u root -pfoodexpress foodexpress --silent -e "
        DROP TRIGGER IF EXISTS slow_order_trigger;
        CREATE TRIGGER slow_order_trigger
        BEFORE INSERT ON orders
        FOR EACH ROW
        BEGIN
            DO SLEEP(3);
        END;
        SELECT 'Slow trigger created on orders table' AS status;
    "

    # Also set global slow query log threshold to catch it
    docker exec "${MYSQL_CONTAINER}" mysql -u root -pfoodexpress --silent -e "
        SET GLOBAL slow_query_log = 'ON';
        SET GLOBAL long_query_time = 1;
        SELECT 'Slow query logging enabled (threshold: 1s)' AS status;
    "

    echo "order-db-slow" >> "${STATE_DIR}/active-faults"

    log_inject "3-second SLEEP trigger added to MySQL orders table INSERT."
    echo ""
    log_info "Trainer notes:"
    log_info "  - Every order placement now takes 3+ seconds minimum"
    log_info "  - MySQL slow query log will record each affected INSERT"
    log_info "  - Tail slow query log: docker exec ${MYSQL_CONTAINER} tail -f /var/log/mysql/mysql-slow.log"
    log_info "  - Order service logs will show transaction timeout warnings"
    log_info "  - Correct fix: drop the trigger. This simulates a misapplied migration."
    log_info "  - Reset: $0 reset"
}

cmd_payment_down() {
    log_header "FAULT: payment-down (P1 SCENARIO)"
    log_warn "This is the PRIMARY P1 assessment fault for the Final War Game."
    log_warn "All checkout attempts will fail. Payment success rate drops to 0%."
    echo ""
    log_info "Blocking payment gateway in payment-service /etc/hosts..."

    require_container_running "${PAYMENT_CONTAINER}"

    # Backup the original hosts file
    docker exec "${PAYMENT_CONTAINER}" sh -c "
        cp /etc/hosts ${STATE_DIR}/hosts.backup 2>/dev/null || cp /etc/hosts /tmp/hosts.backup
        echo '${PAYMENT_GATEWAY_BLOCK_IP} ${PAYMENT_GATEWAY_HOST}' >> /etc/hosts
        echo 'Hosts file modified. Payment gateway blocked.'
        grep '${PAYMENT_GATEWAY_HOST}' /etc/hosts
    " || {
        # Fallback: write to /tmp inside container
        docker exec "${PAYMENT_CONTAINER}" sh -c "
            cp /etc/hosts /tmp/hosts.backup
            echo '${PAYMENT_GATEWAY_BLOCK_IP} ${PAYMENT_GATEWAY_HOST}' >> /etc/hosts
            echo 'Hosts file modified. Payment gateway blocked.'
        "
    }

    echo "payment-down" >> "${STATE_DIR}/active-faults"

    log_inject "Payment gateway '${PAYMENT_GATEWAY_HOST}' blocked in payment-service container."
    echo ""
    log_info "Trainer notes:"
    log_info "  - All POST /api/payment/charge requests will return connection refused"
    log_info "  - Frontend will show: 'Payment failed. Please try again.'"
    log_info "  - Grafana: payment_success_total counter stops incrementing"
    log_info "  - ServiceNow P1 must be raised within 15 minutes of detection"
    log_info "  - Root cause: /etc/hosts modification (simulates DNS poisoning / misconfiguration)"
    log_info "  - Fix: remove the injected line from /etc/hosts inside the container"
    log_info "  - Reset: $0 reset"
    echo ""
    log_warn "Do not reset until participants have: raised P1 ticket, drafted status update,"
    log_warn "investigated root cause, and proposed the fix. Let them work through the process."
}

# =============================================================================
# STATUS COMMAND
# =============================================================================

cmd_status() {
    log_header "FoodExpress War Game — Service Status"
    echo ""

    local all_ok=true

    check_service() {
        local name="$1"
        local port="$2"
        local endpoint="${3:-/health}"

        printf "  %-25s port %-6s  " "${name}" "${port}"
        local http_code
        http_code=$(curl -s -o /dev/null -w "%{http_code}" \
            --max-time 3 "http://localhost:${port}${endpoint}" 2>/dev/null || echo "000")
        local latency_ms
        latency_ms=$(curl -s -o /dev/null -w "%{time_total}" \
            --max-time 5 "http://localhost:${port}${endpoint}" 2>/dev/null | \
            awk '{printf "%.0f", $1 * 1000}' || echo "---")

        if [ "${http_code}" = "200" ]; then
            echo -e "${GREEN}OK${RESET}   HTTP ${http_code}   ${latency_ms}ms"
        elif [ "${http_code}" = "000" ]; then
            echo -e "${RED}DOWN${RESET} (no response)"
            all_ok=false
        else
            echo -e "${YELLOW}WARN${RESET} HTTP ${http_code}   ${latency_ms}ms"
        fi
    }

    echo "  Service Health Endpoints:"
    check_service "restaurant-service"  "${RESTAURANT_PORT}"  "/health"
    check_service "cart-service"        "${CART_PORT}"        "/health"
    check_service "delivery-service"    "${DELIVERY_PORT}"    "/health"
    check_service "order-service"       "${ORDER_PORT}"       "/actuator/health"
    check_service "payment-service"     "${PAYMENT_PORT}"     "/health"
    echo ""

    echo "  Container Memory Usage:"
    docker stats --no-stream --format \
        "  {{.Name}}\t{{.MemUsage}}\t{{.MemPerc}}" \
        "${RESTAURANT_CONTAINER}" \
        "${CART_CONTAINER}" \
        "${DELIVERY_CONTAINER}" \
        "${ORDER_CONTAINER}" \
        "${PAYMENT_CONTAINER}" 2>/dev/null | \
        column -t || echo "  (could not retrieve container stats)"
    echo ""

    echo "  Active Faults:"
    if [ -f "${STATE_DIR}/active-faults" ] && [ -s "${STATE_DIR}/active-faults" ]; then
        while IFS= read -r fault; do
            echo -e "  ${RED}[ACTIVE]${RESET} ${fault}"
        done < "${STATE_DIR}/active-faults"
    else
        echo -e "  ${GREEN}No active faults. All services in normal state.${RESET}"
    fi
    echo ""

    echo "  Network Delay Check (delivery-service):"
    docker exec "${DELIVERY_CONTAINER}" tc qdisc show dev eth0 2>/dev/null | \
        grep -E "netem|qdisc" | head -3 | sed 's/^/  /' || \
        echo "  (tc not available or no delay configured)"
    echo ""

    echo "  MongoDB Indexes on restaurants:"
    docker exec "${MONGO_CONTAINER}" mongosh foodexpress --quiet --eval \
        'db.restaurants.getIndexes().forEach(i => print("  " + JSON.stringify({name: i.name, key: i.key})))' \
        2>/dev/null || echo "  (could not query MongoDB)"
    echo ""

    if $all_ok; then
        log_info "All services responding. Check active faults list above for injected conditions."
    else
        log_warn "One or more services are not responding. Check docker ps and service logs."
    fi
}

# =============================================================================
# RESET COMMAND
# =============================================================================

cmd_reset() {
    log_header "RESET: Restoring all FoodExpress services to normal"
    echo ""

    local reset_count=0

    # --- Reset: search-slow ---
    log_info "Restoring MongoDB indexes on restaurants collection..."
    if docker exec "${MONGO_CONTAINER}" mongosh foodexpress --quiet --eval '
        db.restaurants.createIndex({ name: "text", cuisine: "text", description: "text" },
            { name: "restaurants_text_search", default_language: "english" });
        db.restaurants.createIndex({ cuisine: 1 }, { name: "idx_cuisine" });
        db.restaurants.createIndex({ isOpen: 1 }, { name: "idx_is_open" });
        db.restaurants.createIndex({ rating: -1 }, { name: "idx_rating_desc" });
        print("Indexes rebuilt: " + db.restaurants.getIndexes().length + " indexes active");
    ' 2>/dev/null; then
        log_reset "MongoDB text index restored on restaurants collection."
        reset_count=$((reset_count + 1))
    else
        log_warn "Could not rebuild MongoDB indexes (container may not be running)."
    fi
    echo ""

    # --- Reset: cart-memory-leak ---
    log_info "Deactivating cart-service memory leak handler (SIGUSR2)..."
    if docker exec "${CART_CONTAINER}" sh -c '
        PID=$(pgrep -f "node.*cart" | head -1)
        if [ -n "$PID" ]; then
            kill -USR2 "$PID"
            echo "Sent SIGUSR2 to cart-service PID ${PID} — leak deactivated"
        else
            echo "Cart process not found; no signal sent"
        fi
    ' 2>/dev/null; then
        log_reset "Cart-service memory leak handler deactivated."
        reset_count=$((reset_count + 1))
    else
        log_warn "Could not signal cart-service (container may not be running)."
    fi
    echo ""

    # --- Reset: delivery-timeout ---
    log_info "Removing network delay from delivery-service container..."
    if docker exec --privileged "${DELIVERY_CONTAINER}" sh -c \
        'tc qdisc del dev eth0 root 2>/dev/null && echo "Delay removed" || echo "No delay was active"' \
        2>/dev/null; then
        log_reset "Network delay removed from delivery-service eth0."
        reset_count=$((reset_count + 1))
    else
        log_warn "Could not modify delivery-service network (container may not be running)."
    fi
    echo ""

    # --- Reset: order-db-slow ---
    log_info "Dropping slow query trigger from MySQL orders table..."
    if docker exec "${MYSQL_CONTAINER}" mysql -u root -pfoodexpress foodexpress --silent -e \
        "DROP TRIGGER IF EXISTS slow_order_trigger; SELECT 'Trigger dropped' AS status;" \
        2>/dev/null; then
        docker exec "${MYSQL_CONTAINER}" mysql -u root -pfoodexpress --silent -e \
            "SET GLOBAL slow_query_log = 'OFF';" 2>/dev/null || true
        log_reset "MySQL slow trigger removed from orders table."
        reset_count=$((reset_count + 1))
    else
        log_warn "Could not remove MySQL trigger (container may not be running)."
    fi
    echo ""

    # --- Reset: payment-down ---
    log_info "Restoring payment-service /etc/hosts..."
    if docker exec "${PAYMENT_CONTAINER}" sh -c "
        if [ -f /tmp/hosts.backup ]; then
            cp /tmp/hosts.backup /etc/hosts
            echo 'Hosts file restored from backup'
        else
            # Remove the injected line manually
            grep -v '${PAYMENT_GATEWAY_HOST}' /etc/hosts > /tmp/hosts.clean && \
                cp /tmp/hosts.clean /etc/hosts && \
                echo 'Injected hosts entry removed'
        fi
    " 2>/dev/null; then
        log_reset "Payment-service /etc/hosts restored. Payment gateway unblocked."
        reset_count=$((reset_count + 1))
    else
        log_warn "Could not restore payment-service hosts file (container may not be running)."
    fi
    echo ""

    # --- Clear state file ---
    rm -f "${STATE_DIR}/active-faults"
    echo "" > "${STATE_DIR}/active-faults"

    echo ""
    log_reset "Reset complete. ${reset_count} fault(s) cleared."
    log_info "Run '$0 status' to verify all services are healthy before proceeding."
    echo ""
    log_info "Tip: give participants 2-3 minutes after reset before announcing the all-clear."
    log_info "     Let them discover the recovery themselves via their monitoring dashboards."
}

# =============================================================================
# HELP / USAGE
# =============================================================================

show_help() {
    cat << EOF

${BOLD}FoodExpress War Game — Fault Injection Script${RESET}
Usage: $0 <command>

FAULT COMMANDS
  search-slow         Drop MongoDB text index. Restaurant search degrades to full scan.
  cart-memory-leak    Activate memory leak in cart-service (SIGUSR1 to Node.js process).
  delivery-timeout    Add ${DELIVERY_DELAY_MS}ms network delay to delivery-service container.
  order-db-slow       Inject 3s SLEEP trigger on MySQL orders table INSERT.
  payment-down        Block payment gateway in payment-service /etc/hosts (P1 scenario).

CONTROL COMMANDS
  status              Check health, memory, latency, and active faults across all services.
  reset               Remove all injected faults and restore normal operating state.

EXAMPLES
  $0 search-slow              # Inject slow search fault
  $0 status                   # Check current state of all services
  $0 reset                    # Clear all faults

WAR GAME SCHEDULE
  Day 35 (M34 Mid-Stage):  09:30 search-slow | 11:00 cart-memory-leak
                            13:30 delivery-timeout | 15:00 order-db-slow
  Day 43-44 (M37 Final):   09:30 payment-down (P1) | 14:00 search-slow + delivery-timeout

SAFETY
  All faults target Docker containers only. Nothing modifies the host system permanently.
  Run 'reset' at any time to restore all services. Individual fault reversals are idempotent.

EOF
}

# =============================================================================
# ENTRY POINT
# =============================================================================

COMMAND="${1:-help}"

case "${COMMAND}" in
    search-slow)
        cmd_search_slow
        ;;
    cart-memory-leak)
        cmd_cart_memory_leak
        ;;
    delivery-timeout)
        cmd_delivery_timeout
        ;;
    order-db-slow)
        cmd_order_db_slow
        ;;
    payment-down)
        cmd_payment_down
        ;;
    status)
        cmd_status
        ;;
    reset)
        cmd_reset
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}[ERROR]${RESET} Unknown command: '${COMMAND}'"
        show_help
        exit 1
        ;;
esac
