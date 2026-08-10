#!/bin/bash
# fault-injection.sh -- FoodExpress Chaos Experiment -- FIXED VERSION

EXPERIMENT_NAME="payment-latency-test"
NAMESPACE="foodexpress"            # Fix 1: Changed from "default" to "foodexpress"
STEADY_STATE_METRIC="foodexpress_order_success_rate"
THRESHOLD=0.99

echo "=== Chaos Experiment: $EXPERIMENT_NAME ==="
echo "Hypothesis: Order success rate stays above 99% when payment has 2s latency"

# Step 1: Record steady state
echo "[1/4] Recording steady state..."
# Fix 5: Added -s flag and corrected API path to /api/v1
# Fix 6: Corrected JSON path to .data.result[0].value[1]
BASELINE=$(curl -s "http://prometheus:9090/api/v1/query?query=$STEADY_STATE_METRIC" \
  | jq '.data.result[0].value[1]')
echo "  Baseline: $BASELINE"

# Step 2: Inject fault
echo "[2/4] Injecting 2s latency on payment-service..."
kubectl exec -n $NAMESPACE deploy/payment-service -- \
  tc qdisc add dev eth0 root netem delay 2000ms

# Step 3: Observe
echo "[3/4] Observing for 3 minutes..."
sleep 180                          # Fix 4: Changed from 5 to 180 seconds

# Fix 5 & 6 applied here too
CURRENT=$(curl -s "http://prometheus:9090/api/v1/query?query=$STEADY_STATE_METRIC" \
  | jq '.data.result[0].value[1]')

echo "  Current: $CURRENT"

# Step 4: Rollback
echo "[4/4] Rolling back fault injection..."
# Fix 3: Changed 'add' to 'del' to remove the latency
kubectl exec -n $NAMESPACE deploy/payment-service -- \
  tc qdisc del dev eth0 root netem

# Evaluate
# Fix 2: Changed < to >= (PASS when current >= threshold)
if (( $(echo "$CURRENT >= $THRESHOLD" | bc -l) )); then
  echo "PASS: Steady state maintained ($CURRENT >= $THRESHOLD)"
else
  echo "FAIL: Steady state violated ($CURRENT < $THRESHOLD)"
  echo "ACTION: Implement circuit breaker on Order->Payment call"
fi

echo "=== Experiment Complete ==="
