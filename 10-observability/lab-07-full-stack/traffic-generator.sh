#!/bin/bash
echo "Generating traffic to order-service..."
echo "Press Ctrl+C to stop"

SUCCESS=0
FAIL=0
TOTAL=0

while true; do
  TOTAL=$((TOTAL + 1))
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8080/api/orders)

  if [ "$STATUS" = "200" ]; then
    SUCCESS=$((SUCCESS + 1))
  else
    FAIL=$((FAIL + 1))
  fi

  if [ $((TOTAL % 50)) -eq 0 ]; then
    RATE=$(echo "scale=1; $FAIL * 100 / $TOTAL" | bc)
    echo "[${TOTAL} requests] Success: ${SUCCESS} | Failed: ${FAIL} | Error Rate: ${RATE}%"
  fi

  sleep 0.1
done
