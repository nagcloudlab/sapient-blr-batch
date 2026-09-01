#!/bin/bash
# fault-injection.sh -- FoodExpress Chaos Experiment
# THIS FILE CONTAINS 6 BUGS -- Find and fix them all!

EXPERIMENT_NAME="payment-latency-test"
NAMESPACE="default"               # Bug 1: Should be "foodexpress"
STEADY_STATE_METRIC="foodexpress_order_success_rate"
THRESHOLD=0.99

echo "=== Chaos Experiment: $EXPERIMENT_NAME ==="
echo "Hypothesis: Order success rate stays above 99% when payment has 2s latency"

# Step 1: Record steady state
echo "[1/4] Recording steady state..."
# Bug 5: Missing -s flag and wrong API path (/api/v2 doesn't exist)
BASELINE=$(curl "http://prometheus:9090/api/v2/query?query=$STEADY_STATE_METRIC" \
  | jq '.result[0].value[1]')     # Bug 6: Wrong JSON path (should be .data.result[0].value[1])
echo "  Baseline: $BASELINE"

# Step 2: Inject fault
echo "[2/4] Injecting 2s latency on payment-service..."
kubectl exec -n $NAMESPACE deploy/payment-service -- \
  tc qdisc add dev eth0 root netem delay 2000ms

# Step 3: Observe
echo "[3/4] Observing..."
sleep 5                           # Bug 4: Should be 180 seconds (3 minutes)

# Bug 5 again: Same wrong API path
CURRENT=$(curl "http://prometheus:9090/api/v2/query?query=$STEADY_STATE_METRIC" \
  | jq '.result[0].value[1]')    # Bug 6 again: Wrong JSON path

echo "  Current: $CURRENT"

# Step 4: Rollback
echo "[4/4] Rolling back fault injection..."
# Bug 3: Uses 'add' instead of 'del' -- doubles the latency instead of removing it
kubectl exec -n $NAMESPACE deploy/payment-service -- \
  tc qdisc add dev eth0 root netem delay 2000ms

# Evaluate
# Bug 2: Comparison is inverted (< instead of >=)
if (( $(echo "$CURRENT < $THRESHOLD" | bc -l) )); then
  echo "PASS: Steady state maintained ($CURRENT >= $THRESHOLD)"
else
  echo "FAIL: Steady state violated ($CURRENT < $THRESHOLD)"
  echo "ACTION: Implement circuit breaker on Order->Payment call"
fi

echo "=== Experiment Complete ==="
