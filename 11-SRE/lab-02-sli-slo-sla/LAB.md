# Lab 02: SLIs, SLOs, and SLAs

## Objective

Learn to define what "reliable" means using measurable indicators (SLIs),
set targets (SLOs), and understand contractual agreements (SLAs).

**Prerequisite:** Lab 01 services running (`cd ../services && docker compose up -d`)

---

## Concepts

### The Three Levels

```
SLA  (Service Level Agreement)   -- Contract with CONSEQUENCES
 |                                  "99.9% uptime or we refund 10%"
 |                                  WHO: Business/Legal decides
 |
SLO  (Service Level Objective)   -- Internal TARGET
 |                                  "We aim for 99.95% availability"
 |                                  WHO: Engineering + Product decides
 |
SLI  (Service Level Indicator)   -- The actual MEASUREMENT
                                    "Successful requests / Total requests"
                                    WHO: Engineering measures
```

### Golden Rule
```
SLI = good events / total events (expressed as a percentage)
SLO = target value for the SLI
SLA = SLO + business consequences for missing it
```

---

## Part 1: Identify SLIs for Our Services

### The Four Golden SLIs

| SLI Type | What It Measures | Formula |
|----------|-----------------|---------|
| **Availability** | Is the service responding? | Non-5xx responses / Total responses |
| **Latency** | Is it fast enough? | Requests < threshold / Total requests |
| **Throughput** | Can it handle the load? | Successful requests / second |
| **Error Rate** | Are responses correct? | Failed requests / Total requests |

### Exercise: Map SLIs to Our Services

For each service, identify which SLIs matter most. Fill in the table:

```
+------------------+--------------------+--------------------------------+
| Service          | SLI                | How to Measure                 |
+------------------+--------------------+--------------------------------+
| order-service    | Availability       | ______________________________  |
| order-service    | Latency (p95)      | ______________________________  |
| payment-service  | Availability       | ______________________________  |
| payment-service  | Success Rate       | ______________________________  |
| payment-service  | Latency (p99)      | ______________________________  |
+------------------+--------------------+--------------------------------+
```

### Measure Real SLIs from Prometheus

The services are already exporting metrics. Let's query them:

```bash
# Open Prometheus
open http://localhost:9090
```

**Availability SLI for order-service:**
```promql
# Successful requests (non-5xx) / Total requests
sum(rate(http_request_duration_seconds_count{status_code!~"5.."}[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))
```

**Latency SLI for order-service (% of requests under 500ms):**
```promql
# Requests completing within 500ms / Total requests
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))
```

**Payment success rate:**
```promql
# Completed payments / Total payment attempts
rate(payments_completed_total[5m])
/
(rate(payments_completed_total[5m]) + rate(payments_failed_total[5m]) + rate(payments_error_total[5m]))
```

Generate some traffic so you have data:
```bash
for i in $(seq 1 50); do
  curl -s -X POST http://localhost:3000/orders \
    -H "Content-Type: application/json" \
    -d '{"item": "Dosa", "quantity": 1, "price": 150}' -o /dev/null &
done
wait
```

Now run each PromQL query and note the values.

---

## Part 2: Set SLOs

### The Nines Table

| Target | Downtime/Year | Downtime/Month | Downtime/Day |
|--------|---------------|----------------|--------------|
| 90% | 36.5 days | 72 hours | 2.4 hours |
| 99% | 3.65 days | 7.3 hours | 14.4 min |
| 99.5% | 1.83 days | 3.65 hours | 7.2 min |
| 99.9% | 8.76 hours | 43.8 min | 1.44 min |
| 99.95% | 4.38 hours | 21.9 min | 43.2 sec |
| 99.99% | 52.6 min | 4.38 min | 8.6 sec |

### Why Not 100%?

```
Cost to achieve reliability:

$
|                                          * 100%
|                                      *
|                                  *
|                             *
|                        *
|                  *
|            *
|       *
|   *
| *
+----------------------------------------> Reliability %
  90%   99%   99.9%  99.99% 99.999%

Each additional "nine" costs roughly 10x more.
```

### Exercise: Define SLOs for FoodExpress

Based on what you observed in Lab 01, set realistic SLOs:

```
+------------------+----------------+----------+-------------------+-----------------+
| Service          | SLI            | SLO      | Window            | Justification   |
+------------------+----------------+----------+-------------------+-----------------+
| order-service    | Availability   | ____%    | 30-day rolling    | _______________  |
| order-service    | Latency (p95)  | ____ms   | 30-day rolling    | _______________  |
| payment-service  | Success Rate   | ____%    | 30-day rolling    | _______________  |
| payment-service  | Latency (p99)  | ____ms   | 30-day rolling    | _______________  |
+------------------+----------------+----------+-------------------+-----------------+
```

**Hints:**
- order-service availability: 99.9% is common for user-facing APIs
- payment-service: should be MORE reliable than order-service (money is involved)
- Latency: look at your actual p95/p99 values from Prometheus and add some margin

---

## Part 3: SLAs vs SLOs

### The Difference Matters

```
                 SLO (Internal)                    SLA (External)
                 ─────────────                     ─────────────
Target:          99.95% availability               99.9% availability
Set by:          Engineering team                   Business + Legal
Consequence:     Team focuses on reliability        Refund customers 10%
Buffer:          0.05% between SLO and SLA          None -- it's a contract

WHY the buffer?
  SLO = 99.95%  (internal goal)
  SLA = 99.9%   (customer promise)
  Gap = 0.05%   (safety margin before you owe money)
```

### Exercise: Write an SLA for FoodExpress

Scenario: FoodExpress wants to offer an SLA to restaurant partners.

Fill in:

```
FoodExpress Order Platform SLA
─────────────────────────────────────────────
Service: Order Processing API

Availability commitment: ____%  (should be LOWER than your SLO)

Measurement: _________________________________

Measurement window: __________________________

Exclusions: __________________________________
(e.g., scheduled maintenance, force majeure)

Breach consequences:
  - Availability < ____% : ________________
  - Availability < ____% : ________________
```

---

## Part 4: SLI/SLO Decision Framework (Discussion)

### Class Discussion

| Question | Think About |
|----------|------------|
| Who are the users of order-service? | End customers ordering food |
| What do they care about most? | Orders go through, fast response |
| What SLI best captures their experience? | Availability + Latency |
| Should payment-service have a higher SLO than menu-service? | Yes -- money > menus |
| What happens if we set SLO too high? | No room for changes, team burns out |
| What happens if we set SLO too low? | Users leave, business loses money |

---

## Key Takeaways

1. **SLI** = What you measure (good events / total events)
2. **SLO** = What you aim for (99.9% over 30 days)
3. **SLA** = What you promise externally (with penalties)
4. Always set **SLO stricter than SLA** to have a safety buffer
5. Different services deserve different SLO levels based on business impact
6. **Measure from the user's perspective**, not from the server's perspective

> **Next:** Lab 03 -- Error Budgets (what happens when you miss your SLO)
