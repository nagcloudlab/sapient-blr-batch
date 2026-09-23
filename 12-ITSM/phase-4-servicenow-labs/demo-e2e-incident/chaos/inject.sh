#!/bin/bash
# =============================================================
# UPI Chaos Injection Script
# Use this to trigger incidents during the demo
# =============================================================

TXN_SERVICE="http://localhost:8081"
STL_SERVICE="http://localhost:8082"
SNOW_BRIDGE="http://localhost:5005"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

show_menu() {
    echo ""
    echo -e "${CYAN}============================================${NC}"
    echo -e "${CYAN}   UPI Chaos Injection - Demo Control${NC}"
    echo -e "${CYAN}============================================${NC}"
    echo ""
    echo -e "  ${RED}BREAK THINGS — Transaction Service:${NC}"
    echo "    1) Enable high failure rate (80% errors)     -> triggers P1 incident"
    echo "    2) Inject high latency (5 seconds)           -> triggers P2 incident"
    echo "    3) Take transaction service DOWN              -> triggers P1 incident"
    echo ""
    echo -e "  ${RED}BREAK THINGS — Settlement Service:${NC}"
    echo "    s1) Enable settlement failure rate (80%)      -> triggers settlement alerts"
    echo "    s2) Inject settlement latency (5 seconds)     -> slow settlements"
    echo "    s3) Take settlement service DOWN              -> triggers P1 incident"
    echo ""
    echo -e "  ${GREEN}FIX THINGS:${NC}"
    echo "    4) Disable all chaos (restore normal)        -> resolves alerts"
    echo ""
    echo -e "  ${YELLOW}OBSERVE:${NC}"
    echo "    5) Check chaos status (both services)"
    echo "    6) Check active ServiceNow incidents"
    echo "    7) Send test UPI payment"
    echo "    8) Create manual test incident in ServiceNow"
    echo ""
    echo "    0) Exit"
    echo ""
}

while true; do
    show_menu
    read -p "  Choose action: " choice
    echo ""

    case $choice in
        1)
            echo -e "${RED}Enabling 80% failure rate on UPI Transaction Service...${NC}"
            curl -s -X POST "$TXN_SERVICE/chaos/enable" | python3 -m json.tool 2>/dev/null || echo "Failed to connect"
            echo -e "${YELLOW}Wait ~60s for Prometheus to detect and AlertManager to fire -> ServiceNow incident${NC}"
            ;;
        2)
            echo -e "${RED}Injecting 5s latency on UPI Transaction Service...${NC}"
            curl -s -X POST "$TXN_SERVICE/chaos/latency?ms=5000" | python3 -m json.tool 2>/dev/null || echo "Failed to connect"
            echo -e "${YELLOW}Wait ~60s for latency alert to fire${NC}"
            ;;
        3)
            echo -e "${RED}Taking UPI Transaction Service DOWN...${NC}"
            curl -s -X POST "$TXN_SERVICE/chaos/down" | python3 -m json.tool 2>/dev/null || echo "Failed to connect"
            echo -e "${YELLOW}Wait ~30s for service-down alert to fire -> P1 incident${NC}"
            ;;
        s1)
            echo -e "${RED}Enabling 80% failure rate on UPI Settlement Service...${NC}"
            curl -s -X POST "$STL_SERVICE/chaos/enable" | python3 -m json.tool 2>/dev/null || echo "Failed to connect"
            echo -e "${YELLOW}Wait ~60s for settlement failure alerts to fire${NC}"
            ;;
        s2)
            echo -e "${RED}Injecting 5s latency on UPI Settlement Service...${NC}"
            curl -s -X POST "$STL_SERVICE/chaos/latency?ms=5000" | python3 -m json.tool 2>/dev/null || echo "Failed to connect"
            ;;
        s3)
            echo -e "${RED}Taking UPI Settlement Service DOWN...${NC}"
            curl -s -X POST "$STL_SERVICE/chaos/down" | python3 -m json.tool 2>/dev/null || echo "Failed to connect"
            echo -e "${YELLOW}Wait ~30s for service-down alert to fire -> P1 incident${NC}"
            ;;
        4)
            echo -e "${GREEN}Disabling all chaos - restoring normal operations...${NC}"
            curl -s -X POST "$TXN_SERVICE/chaos/disable" | python3 -m json.tool 2>/dev/null || echo "Failed to connect"
            curl -s -X POST "$STL_SERVICE/chaos/disable" | python3 -m json.tool 2>/dev/null || echo "Failed to connect"
            echo -e "${GREEN}Both services restored. Alerts will auto-resolve in ~2 minutes.${NC}"
            ;;
        5)
            echo -e "${CYAN}Transaction Service chaos status:${NC}"
            curl -s "$TXN_SERVICE/chaos/status" | python3 -m json.tool 2>/dev/null || echo "  Service unreachable"
            echo ""
            echo -e "${CYAN}Settlement Service chaos status:${NC}"
            curl -s "$STL_SERVICE/chaos/status" | python3 -m json.tool 2>/dev/null || echo "  Service unreachable"
            ;;
        6)
            echo -e "${CYAN}Active alerts -> ServiceNow incidents:${NC}"
            curl -s "$SNOW_BRIDGE/active-alerts" | python3 -m json.tool 2>/dev/null || echo "  Bridge unreachable"
            ;;
        7)
            echo -e "${CYAN}Sending test UPI payment...${NC}"
            curl -s -X POST "$TXN_SERVICE/api/upi/pay" \
                -H "Content-Type: application/json" \
                -d '{"payerVpa":"test@okaxis","payeeVpa":"merchant@hdfcbank","amount":999.99,"remarks":"Test payment"}' \
                | python3 -m json.tool 2>/dev/null || echo "  Failed"
            ;;
        8)
            echo -e "${CYAN}Creating manual test incident in ServiceNow...${NC}"
            curl -s -X POST "$SNOW_BRIDGE/test-incident" \
                -H "Content-Type: application/json" \
                -d '{"alertname":"ManualTest","severity":"critical","summary":"UPI Payment Gateway - Manual Test Incident","description":"This is a manually triggered test incident from the demo chaos script."}' \
                | python3 -m json.tool 2>/dev/null || echo "  Failed"
            ;;
        0)
            echo "Bye!"
            exit 0
            ;;
        *)
            echo "Invalid choice"
            ;;
    esac
done
