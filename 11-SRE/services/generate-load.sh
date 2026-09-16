#!/bin/bash

# Load generator for SRE Labs
# Generates a mix of valid orders, bad requests, and not-found lookups
#
# Usage:
#   ./generate-load.sh              # 50 requests with 0.5s delay
#   ./generate-load.sh 100          # 100 requests
#   ./generate-load.sh 200 0.2      # 200 requests with 0.2s delay
#   CONTINUOUS=1 ./generate-load.sh  # run forever until Ctrl+C

BASE_URL="${BASE_URL:-http://localhost:3000}"
TOTAL="${1:-50}"
DELAY="${2:-0.5}"

ITEMS=("Biryani" "Dosa" "Paneer" "Naan" "Idli" "Pizza" "Burger" "Pasta" "Momos" "Thali")
CONFIRMED=0
PAY_FAILED=0
BAD_REQUEST=0
SERVER_ERROR=0
NOT_FOUND=0
TOTAL_SENT=0

echo "============================================"
echo "  Load Generator - FoodExpress"
echo "============================================"
echo "  Target:   $BASE_URL"
echo "  Requests: $TOTAL"
echo "  Delay:    ${DELAY}s"
echo "  Mix:      70% valid orders, 15% bad requests,"
echo "            10% not-found lookups, 5% invalid payments"
echo "============================================"
echo ""

run_request() {
  local i=$1
  local roll=$((RANDOM % 100))

  if [ $roll -lt 70 ]; then
    ITEM=${ITEMS[$RANDOM % ${#ITEMS[@]}]}
    QTY=$(( RANDOM % 5 + 1 ))
    PRICE=$(( RANDOM % 500 + 50 ))

    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/orders" \
      -H "Content-Type: application/json" \
      -d "{\"item\":\"$ITEM\",\"quantity\":$QTY,\"price\":$PRICE}" 2>/dev/null)

    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    STATUS=$(echo "$BODY" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

    if [ "$STATUS" = "CONFIRMED" ]; then
      CONFIRMED=$((CONFIRMED + 1))
      echo "[$i] OK  CONFIRMED  - $QTY x $ITEM (INR $PRICE)"
    elif [ "$STATUS" = "PAYMENT_FAILED" ]; then
      PAY_FAILED=$((PAY_FAILED + 1))
      echo "[$i] !!  PAYMENT_FAILED - $QTY x $ITEM (INR $PRICE)"
    elif [ "$HTTP_CODE" = "500" ]; then
      SERVER_ERROR=$((SERVER_ERROR + 1))
      echo "[$i] XX  SERVER ERROR (500)"
    else
      PAY_FAILED=$((PAY_FAILED + 1))
      echo "[$i] !!  FAILED ($HTTP_CODE) - $QTY x $ITEM"
    fi

  elif [ $roll -lt 85 ]; then
    VARIANT=$((RANDOM % 3))
    if [ $VARIANT -eq 0 ]; then
      curl -s -o /dev/null -w "" -X POST "$BASE_URL/orders" \
        -H "Content-Type: application/json" \
        -d '{"item":"Biryani","quantity":1}' 2>/dev/null
      echo "[$i] 400 BAD REQUEST - missing price"
    elif [ $VARIANT -eq 1 ]; then
      curl -s -o /dev/null -w "" -X POST "$BASE_URL/orders" \
        -H "Content-Type: application/json" \
        -d '{}' 2>/dev/null
      echo "[$i] 400 BAD REQUEST - empty body"
    else
      curl -s -o /dev/null -w "" -X POST "$BASE_URL/orders" \
        -H "Content-Type: application/json" \
        -d '{"quantity":2,"price":99}' 2>/dev/null
      echo "[$i] 400 BAD REQUEST - missing item"
    fi
    BAD_REQUEST=$((BAD_REQUEST + 1))

  elif [ $roll -lt 95 ]; then
    FAKE_ID="non-existent-$RANDOM"
    curl -s -o /dev/null -w "" "$BASE_URL/orders/$FAKE_ID" 2>/dev/null
    echo "[$i] 404 NOT FOUND - order lookup"
    NOT_FOUND=$((NOT_FOUND + 1))

  else
    curl -s -o /dev/null -w "" -X POST "http://localhost:8080/payments" \
      -H "Content-Type: application/json" \
      -d '{"orderId":null,"amount":-1}' 2>/dev/null
    echo "[$i] 400 BAD PAYMENT - invalid amount"
    BAD_REQUEST=$((BAD_REQUEST + 1))
  fi

  TOTAL_SENT=$((TOTAL_SENT + 1))
}

if [ "${CONTINUOUS}" = "1" ]; then
  echo "Running in CONTINUOUS mode. Press Ctrl+C to stop."
  echo ""
  i=1
  trap 'echo ""; echo "Stopped after $TOTAL_SENT requests."; exit 0' INT
  while true; do
    run_request $i
    i=$((i + 1))
    sleep "$DELAY"
  done
else
  for i in $(seq 1 $TOTAL); do
    run_request $i
    sleep "$DELAY"
  done
fi

echo ""
echo "============ RESULTS ============"
echo "  Total Sent:      $TOTAL_SENT"
echo "  ---------------------------------"
echo "  Confirmed:       $CONFIRMED"
echo "  Payment Failed:  $PAY_FAILED"
echo "  Bad Requests:    $BAD_REQUEST"
echo "  Not Found:       $NOT_FOUND"
echo "  Server Errors:   $SERVER_ERROR"
echo "================================="
echo ""
echo "Check your dashboards:"
echo "  Prometheus: http://localhost:9090"
echo "  Grafana:    http://localhost:3001"
echo ""
