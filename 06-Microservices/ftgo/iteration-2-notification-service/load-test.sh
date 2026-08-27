#!/bin/bash

# Load test script: sends 100 orders to POST /api/orders on localhost:8080

BASE_URL="http://localhost:8080/api/orders"

RESTAURANTS=(1 2 3)
CONSUMERS=("Alice" "Bob" "Charlie" "Diana" "Eve")
ADDRESSES=("123 Main St" "456 Oak Ave" "789 Pine Rd" "321 Elm St" "654 Maple Dr")
PAYMENTS=("CREDIT_CARD" "DEBIT_CARD" "UPI" "NET_BANKING")

echo "=== FTGO Load Test: Sending 100 Orders ==="
echo "Target: $BASE_URL"
echo ""

SUCCESS=0
FAIL=0

for i in $(seq 1 100); do
  CONSUMER_ID=$(( (RANDOM % 5) + 1 ))
  CONSUMER_NAME=${CONSUMERS[$((RANDOM % 5))]}
  CONSUMER_CONTACT="555-$(printf '%04d' $((RANDOM % 10000)))"
  RESTAURANT_ID=${RESTAURANTS[$((RANDOM % 3))]}
  ADDRESS=${ADDRESSES[$((RANDOM % 5))]}
  PAYMENT=${PAYMENTS[$((RANDOM % 4))]}

  # Random 1-3 items per order
  NUM_ITEMS=$(( (RANDOM % 3) + 1 ))
  ITEMS="["
  for j in $(seq 1 $NUM_ITEMS); do
    MENU_ITEM_ID=$(( (RANDOM % 5) + 1 ))
    QTY=$(( (RANDOM % 3) + 1 ))
    if [ $j -gt 1 ]; then
      ITEMS="$ITEMS,"
    fi
    ITEMS="$ITEMS{\"menuItemId\":$MENU_ITEM_ID,\"quantity\":$QTY}"
  done
  ITEMS="$ITEMS]"

  PAYLOAD=$(cat <<EOF
{
  "consumerId": $CONSUMER_ID,
  "consumerName": "$CONSUMER_NAME",
  "consumerContact": "$CONSUMER_CONTACT",
  "restaurantId": $RESTAURANT_ID,
  "deliveryAddress": "$ADDRESS",
  "paymentMethod": "$PAYMENT",
  "items": $ITEMS
}
EOF
)

  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

  if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 201 ]; then
    SUCCESS=$((SUCCESS + 1))
    echo "Order #$i -> $HTTP_CODE OK"
  else
    FAIL=$((FAIL + 1))
    echo "Order #$i -> $HTTP_CODE FAILED"
  fi
done

echo ""
echo "=== Load Test Complete ==="
echo "Success: $SUCCESS | Failed: $FAIL | Total: 100"
