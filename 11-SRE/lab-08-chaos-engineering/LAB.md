# Lab 08: Chaos Engineering

## Objective

Learn to deliberately inject failures into your system to discover weaknesses
BEFORE they cause real outages. Practice the chaos engineering loop.

**Prerequisite:** Services running (`cd ../services && docker compose up -d`)

---

## Concepts

### What is Chaos Engineering?

```
"Chaos Engineering is the discipline of experimenting on a system
 in order to build confidence in the system's capability to withstand
 turbulent conditions in production."
                                    -- Principles of Chaos Engineering

NOT: Randomly breaking things for fun
IS:  Controlled experiments with hypotheses and measurements
```

### The Chaos Engineering Loop

```
    1. STEADY STATE
    "What does normal look like?"
          |
          v
    2. HYPOTHESIS
    "What do we expect when X fails?"
          |
          v
    3. INJECT FAILURE
    "Break X in a controlled way"
          |
          v
    4. OBSERVE
    "Did the system behave as expected?"
          |
          v
    5. LEARN & FIX
    "What did we discover? How do we improve?"
          |
          └──────> Back to step 1
```

### Fragile vs Robust vs Anti-Fragile

```
FRAGILE              ROBUST               ANTI-FRAGILE
────────             ──────               ────────────
Breaks easily        Withstands stress     Gets STRONGER from stress

Glass                Rock                  Muscle / Immune system
No redundancy        Redundancy            Redundancy + Learning
No failure testing   Disaster recovery     Chaos engineering
                     plans exist           + automated remediation
```

---

## Part 1: Establish Steady State

Before breaking anything, document what "normal" looks like.

### Measure Baseline Metrics

Generate some normal traffic:
```bash
for i in $(seq 1 30); do
  curl -s -X POST http://localhost:3000/orders \
    -H "Content-Type: application/json" \
    -d '{"item": "Idli", "quantity": 3, "price": 80}' \
    -o /dev/null -w "HTTP %{http_code} - %{time_total}s\n"
  sleep 0.5
done
```

Record your steady state:

```
STEADY STATE MEASUREMENTS
────────────────────────────────────────────
Order success rate:       _____%
Average response time:    _____ms
p99 response time:        _____ms
Payment success rate:     _____%
Orders per minute:        _____
Error rate:               _____%
────────────────────────────────────────────
```

---

## Part 2: Chaos Experiments

### Experiment 1: Kill the Payment Service

```
EXPERIMENT CARD
────────────────────────────────────────────
Name:       Payment Service Crash
Target:     payment-service container
Method:     Stop the container
Hypothesis: Order service should handle payment failures gracefully.
            Orders should be created with PAYMENT_FAILED status.
            Order service itself should NOT crash.
Expected:   Order API still returns 201, but with failed payment status
Blast radius: Payment processing only
Rollback:   cd ../services && docker compose start payment-service
────────────────────────────────────────────
```

**Execute:**

```bash
# Terminal 1: Watch order service logs
cd ../services && docker compose logs -f order-service

# Terminal 2: Stop payment service
cd ../services && docker compose stop payment-service

# Terminal 3: Try placing orders
for i in $(seq 1 5); do
  echo "--- Order $i ---"
  curl -s -X POST http://localhost:3000/orders \
    -H "Content-Type: application/json" \
    -d '{"item": "Chai", "quantity": 1, "price": 30}' | jq '{status, id}'
  sleep 1
done
```

**Record observations:**

```
RESULTS
────────────────────────────────────────────
Did order-service crash?       YES / NO
Did orders get created?        YES / NO
What status did orders have?   _______________
What errors appeared in logs?  _______________
Response time change?          _______________
────────────────────────────────────────────

HYPOTHESIS VALIDATED?          YES / NO
FINDING:                       _______________
ACTION NEEDED:                 _______________
```

**Rollback:**
```bash
cd ../services && docker compose start payment-service
sleep 5
curl -s http://localhost:8080/health
```

---

### Experiment 2: Simulate Network Latency

```
EXPERIMENT CARD
────────────────────────────────────────────
Name:       High Latency on Payment Service
Target:     payment-service response time
Method:     Send concurrent requests to trigger built-in slow paths (2-5s)
Hypothesis: When payment service responds slowly (> 5s timeout),
            order service should timeout and handle gracefully.
Expected:   Orders fail fast with PAYMENT_FAILED status, don't hang forever
Blast radius: Order creation speed
Rollback:   None needed (uses existing service behavior)
────────────────────────────────────────────
```

We'll use Docker's `tc` (traffic control) equivalent by injecting a slow-response
proxy container into the network. A simpler approach: send many concurrent requests
so the payment service's built-in slow responses (5% chance of 2-5s delay) stack up.

```bash
# Send 20 concurrent orders -- some will hit the payment service's slow path
# Order service has a 5-second timeout on payment calls
echo "Sending 20 concurrent orders to trigger timeout behavior..."
for i in $(seq 1 20); do
  time curl -s -X POST http://localhost:3000/orders \
    -H "Content-Type: application/json" \
    -d '{"item": "Coffee", "quantity": 1, "price": 100}' \
    -w "  Order $i: HTTP %{http_code} in %{time_total}s\n" -o /dev/null &
done
wait
echo "--- All orders sent ---"
```

Check which orders timed out vs succeeded:
```bash
# Look at recent orders
curl -s http://localhost:3000/orders | jq '[.[-20:][].status]| group_by(.) | map({status: .[0], count: length})'

# Check payment service logs for slow processing
cd ../services && docker compose logs payment-service 2>&1 | grep "SLOW PROCESSING" | tail -10
```

**Record observations:**

```
RESULTS
────────────────────────────────────────────
How many orders timed out?        _____
Fastest response time?            _____s
Slowest response time?            _____s
Did order-service handle timeouts gracefully?  YES / NO
What status did timed-out orders get?          _______________
────────────────────────────────────────────

HYPOTHESIS VALIDATED?             YES / NO
FINDING:                          _______________
```

---

### Experiment 3: Simulate Resource Exhaustion

```
EXPERIMENT CARD
────────────────────────────────────────────
Name:       High Load / Connection Exhaustion
Target:     order-service under heavy concurrent load
Method:     Send 200 concurrent requests
Hypothesis: Order service should handle load gracefully,
            rejecting excess requests rather than crashing.
Expected:   Some requests may fail but service stays up.
Blast radius: Order service performance
Rollback:   Stop load generation
────────────────────────────────────────────
```

**Execute:**

```bash
# Blast 200 concurrent requests
echo "Starting load test at $(date)"
for i in $(seq 1 200); do
  curl -s -X POST http://localhost:3000/orders \
    -H "Content-Type: application/json" \
    -d '{"item": "Stress-Test-Item", "quantity": 1, "price": 100}' \
    -o /dev/null -w "%{http_code}\n" --max-time 10 &
done | sort | uniq -c | sort -rn
wait
echo "Load test complete at $(date)"

# Check if order-service is still alive
curl -s http://localhost:3000/health | jq .
```

**Record observations:**

```
RESULTS
────────────────────────────────────────────
HTTP 201 (success):         ____ requests
HTTP 5xx (server error):    ____ requests
HTTP 000 (timeout/refused): ____ requests
Service still healthy?      YES / NO
────────────────────────────────────────────
```

---

## Part 3: Chaos Experiment Report

### Compile Your Findings

```
CHAOS ENGINEERING REPORT -- FoodExpress
═══════════════════════════════════════════════════════════════

Date:     _______________
Team:     _______________

EXPERIMENT SUMMARY:
+----+---------------------------+-------------+------------------+-----------+
| #  | Experiment                | Hypothesis  | Result           | Action    |
|    |                           | Validated?  |                  | Needed?   |
+----+---------------------------+-------------+------------------+-----------+
| 1  | Kill payment service      |  YES / NO   |                  |           |
| 2  | Add 8s payment latency    |  YES / NO   |                  |           |
| 3  | 200 concurrent requests   |  YES / NO   |                  |           |
+----+---------------------------+-------------+------------------+-----------+

TOP FINDINGS:
1. _______________________________________________________________
2. _______________________________________________________________
3. _______________________________________________________________

RECOMMENDED IMPROVEMENTS:
1. _______________________________________________________________
2. _______________________________________________________________
3. _______________________________________________________________

NEXT EXPERIMENTS TO RUN:
1. _______________________________________________________________
2. _______________________________________________________________
```

---

## Part 4: Discussion -- Chaos in Production?

### When to Run Chaos Experiments

```
STAGING first:
  - All experiments start here
  - No customer impact
  - Build confidence

PRODUCTION (carefully):
  - Only after staging validates
  - Start with smallest blast radius
  - Have rollback ready
  - During business hours (team available)
  - Never on peak traffic days

NEVER:
  - On databases without backups
  - Without a rollback plan
  - Without team awareness
  - On services you don't own
```

### Real-World Chaos Tools

| Tool | Company | What It Does |
|------|---------|-------------|
| Chaos Monkey | Netflix | Randomly kills production instances |
| Litmus Chaos | CNCF | Kubernetes-native chaos experiments |
| Gremlin | Gremlin Inc | SaaS platform for chaos engineering |
| Toxiproxy | Shopify | Simulates network conditions |
| ChaosBlade | Alibaba | Multi-platform chaos toolkit |

---

## Key Takeaways

1. **Chaos engineering is NOT random destruction** -- it's controlled experiments with hypotheses
2. **Establish steady state first** -- you can't detect anomalies without a baseline
3. **Start small** -- kill one container before you kill a whole zone
4. **Hypothesize before injecting** -- "I expect X to happen" keeps experiments scientific
5. **Every failed hypothesis is a WIN** -- you found a weakness before customers did
6. **Fix what you find** -- chaos without remediation is just destruction

---

## Course Wrap-Up

```
Lab 01: Why Reliability?       --> You felt the pain of unreliability
Lab 02: SLIs/SLOs/SLAs         --> You learned to MEASURE reliability
Lab 03: Error Budgets           --> You learned to BUDGET for failure
Lab 04: Monitoring & Alerting   --> You learned to DETECT problems
Lab 05: Incident Response       --> You learned to RESPOND to problems
Lab 06: Blameless Post-Mortems  --> You learned to LEARN from problems
Lab 07: Toil & Automation       --> You learned to PREVENT recurring problems
Lab 08: Chaos Engineering        --> You learned to FIND problems proactively

SRE = Making systems reliable through engineering, not heroics.
```
