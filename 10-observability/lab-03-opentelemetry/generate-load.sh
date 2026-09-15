#!/bin/bash
BASE_URL="${BASE_URL:-http://localhost:3000}"
TOTAL="${1:-50}"
DELAY="${2:-0.5}"
ITEMS=("laptop" "mouse" "keyboard" "monitor" "headphones" "webcam" "usb-hub" "charger")

echo "Generating $TOTAL requests to $BASE_URL (delay: ${DELAY}s)"
echo "---------------------------------------------------"

for i in $(seq 1 $TOTAL); do
  roll=$((RANDOM % 100))
  if [ $roll -lt 70 ]; then
    ITEM=${ITEMS[$RANDOM % ${#ITEMS[@]}]}
    QTY=$(( RANDOM % 5 + 1 ))
    PRICE=$(( RANDOM % 500 + 10 ))
    STATUS=$(curl -s -X POST "$BASE_URL/orders" \
      -H "Content-Type: application/json" \
      -d "{\"item\":\"$ITEM\",\"quantity\":$QTY,\"price\":$PRICE}" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    echo "[$i/$TOTAL] ORDER: $STATUS - $QTY x $ITEM"
  elif [ $roll -lt 85 ]; then
    curl -s -o /dev/null -X POST "$BASE_URL/orders" \
      -H "Content-Type: application/json" -d '{"item":"laptop"}'
    echo "[$i/$TOTAL] BAD REQUEST (400)"
  elif [ $roll -lt 95 ]; then
    curl -s -o /dev/null "$BASE_URL/orders/fake-$RANDOM"
    echo "[$i/$TOTAL] NOT FOUND (404)"
  else
    curl -s -o /dev/null -X POST "${BASE_URL%:3000}:8080/payments" \
      -H "Content-Type: application/json" -d '{"orderId":null,"amount":-1}'
    echo "[$i/$TOTAL] BAD PAYMENT (400)"
  fi
  sleep "$DELAY"
done
echo ""
echo "Done! Check:"
echo "  Traces:  http://localhost:16686 (Jaeger)"
echo "  Metrics: http://localhost:9090  (Prometheus)"
echo "  Logs:    http://localhost:3001  (Grafana -> Explore -> Loki)"
echo "  All:     http://localhost:3001  (Grafana - all 3 datasources)"
