# Mid-Stage Project + ITSM Introduction
## Module 34 | Sustain Engineering Training | Days 39-40

---

## Agenda -- Day 39

| # | Topic |
|---|-------|
| 01 | Mid-Stage Project Overview & Team Formation |
| 02 | Observability Stack Review: Prometheus, Grafana, Loki, Jaeger |
| 03 | FoodExpress Monitoring Architecture |
| 04 | Fault Injection: Chaos Engineering Principles |
| 05 | Fault Injection Lab: Break FoodExpress Services |
| 06 | Building Dashboards: Golden Signals for FoodExpress |
| 07 | Alert Rules & Runbooks: From Detection to Resolution |
| 08 | Mid-Stage Project Work Session |
| 09 | Day 39 Wrap-up & Demo Prep |

---

## Agenda -- Day 40

| # | Topic |
|---|-------|
| 01 | Mid-Stage Project: Final Work Session |
| 02 | Team Demos & Presentations |
| 03 | Evaluation & Feedback |
| 04 | ITSM: What is IT Service Management? |
| 05 | ITSM Process Architecture |
| 06 | Service Catalog & Service Portfolio |
| 07 | Incident Management Fundamentals |
| 08 | Day 40 Wrap-up |

---

## Mid-Stage Project: Overview

### What You Will Build

```
┌─────────────────────────────────────────────────────┐
│          FoodExpress Observability Platform          │
│                                                     │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐ │
│  │Prometheus│  │  Grafana   │  │     Jaeger       │ │
│  │ Metrics  │  │ Dashboards │  │ Distributed      │ │
│  │ Scraping │  │ & Alerts   │  │ Tracing          │ │
│  └────┬─────┘  └─────┬─────┘  └────────┬─────────┘ │
│       │              │                  │           │
│  ┌────▼──────────────▼──────────────────▼─────────┐ │
│  │         FoodExpress Microservices              │ │
│  │  Order │ Payment │ Menu │ Delivery │ Notify    │ │
│  └────────────────────────────────────────────────┘ │
│                                                     │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐ │
│  │   Loki   │  │ Alertmgr  │  │  Chaos/Fault     │ │
│  │ Log Agg  │  │ Routing   │  │  Injection       │ │
│  └──────────┘  └───────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## Golden Signals for FoodExpress

### The Four Golden Signals (Google SRE)

| Signal | What It Measures | FoodExpress Example |
|--------|-----------------|---------------------|
| **Latency** | Time to serve a request | Order API P95 < 500ms |
| **Traffic** | Demand on the system | Orders per minute |
| **Errors** | Rate of failed requests | 5xx errors on Payment API |
| **Saturation** | How full a resource is | Database connection pool at 85% |

```
FoodExpress SLIs:
  - Order placement: P99 latency < 2s
  - Menu browsing:   P99 latency < 500ms
  - Payment processing: Error rate < 0.1%
  - Delivery tracking: Availability > 99.9%
```

---

## Prometheus Metrics for FoodExpress

### Key Metric Types

```yaml
# Counter: Total orders placed (only goes up)
foodexpress_orders_total{status="confirmed", restaurant="biryani_house"} 4521

# Gauge: Current active deliveries (goes up and down)
foodexpress_active_deliveries{city="bangalore"} 47

# Histogram: Order processing duration
foodexpress_order_duration_seconds_bucket{le="0.5"} 3201
foodexpress_order_duration_seconds_bucket{le="1.0"} 4100
foodexpress_order_duration_seconds_bucket{le="2.0"} 4480
foodexpress_order_duration_seconds_count 4521
foodexpress_order_duration_seconds_sum 2847.3

# Summary: Payment response time
foodexpress_payment_latency_seconds{quantile="0.95"} 0.42
foodexpress_payment_latency_seconds{quantile="0.99"} 1.1
```

---

## Prometheus: PromQL Queries

### Essential Queries for FoodExpress Dashboards

```promql
# Request rate (orders per second, last 5 min)
rate(foodexpress_orders_total[5m])

# Error rate percentage
100 * rate(foodexpress_http_requests_total{status=~"5.."}[5m])
    / rate(foodexpress_http_requests_total[5m])

# P95 latency for order placement
histogram_quantile(0.95,
  rate(foodexpress_order_duration_seconds_bucket[5m])
)

# Saturation: DB connection pool usage
foodexpress_db_connections_active / foodexpress_db_connections_max * 100

# Apdex score (satisfied < 0.5s, tolerating < 2s)
(
  rate(foodexpress_order_duration_seconds_bucket{le="0.5"}[5m])
  + rate(foodexpress_order_duration_seconds_bucket{le="2.0"}[5m])
) / 2 / rate(foodexpress_order_duration_seconds_count[5m])
```

---

## Grafana Dashboard Design

### FoodExpress Operations Dashboard Layout

```
┌─────────────────────────────────────────────────────┐
│  FoodExpress Operations Dashboard                   │
├─────────────┬─────────────┬─────────────┬───────────┤
│ Orders/min  │ Error Rate  │ P95 Latency │ Uptime    │
│   127       │   0.3%      │   420ms     │  99.97%   │
│  (stat)     │  (stat)     │  (stat)     │ (stat)    │
├─────────────┴─────────────┴─────────────┴───────────┤
│  Request Rate by Service           (time series)    │
│  ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄        │
├─────────────────────────┬───────────────────────────┤
│  Error Rate by Service  │  Latency Heatmap          │
│  (time series)          │  (heatmap)                │
├─────────────────────────┴───────────────────────────┤
│  Active Deliveries by City          (geo map)       │
├─────────────────────────┬───────────────────────────┤
│  DB Connection Pool     │  CPU/Memory per Pod       │
│  (gauge)                │  (time series)            │
└─────────────────────────┴───────────────────────────┘
```

---

## Alerting Rules for FoodExpress

### Prometheus Alerting Rules

```yaml
groups:
  - name: foodexpress-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          rate(foodexpress_http_requests_total{status=~"5.."}[5m])
          / rate(foodexpress_http_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
          team: sustain-engineering
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook: "https://wiki.foodexpress.in/runbooks/high-error-rate"

      - alert: OrderLatencyHigh
        expr: |
          histogram_quantile(0.95,
            rate(foodexpress_order_duration_seconds_bucket[5m])
          ) > 2
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "Order P95 latency exceeds 2s"

      - alert: PaymentServiceDown
        expr: up{job="payment-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Payment service is down"
          runbook: "https://wiki.foodexpress.in/runbooks/payment-down"
```

---

## Alertmanager: Routing & Notification

### Alert Routing Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/T00/B00/xxx'

route:
  receiver: 'default-slack'
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      group_wait: 10s
    - match:
        severity: warning
      receiver: 'slack-warnings'

receivers:
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<pagerduty-key>'
  - name: 'slack-warnings'
    slack_configs:
      - channel: '#foodexpress-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
  - name: 'default-slack'
    slack_configs:
      - channel: '#foodexpress-ops'
```

---

## Chaos Engineering: Principles

### What is Chaos Engineering?

**The discipline of experimenting on a system to build confidence in its ability to withstand turbulent conditions in production.**

```
┌──────────────────────────────────────────┐
│         Chaos Engineering Cycle          │
│                                          │
│  1. Define "steady state"                │
│     (e.g., 99.9% order success rate)     │
│              │                           │
│              ▼                           │
│  2. Hypothesize: "The system will        │
│     maintain steady state even if..."    │
│              │                           │
│              ▼                           │
│  3. Inject fault                         │
│     (kill a pod, add latency, etc.)      │
│              │                           │
│              ▼                           │
│  4. Observe: Did steady state hold?      │
│              │                           │
│        ┌─────┴─────┐                     │
│        ▼           ▼                     │
│      YES          NO                     │
│   Confidence    Fix weakness,            │
│   increased     then re-test             │
└──────────────────────────────────────────┘
```

---

## Fault Injection Techniques

### Common Fault Types for FoodExpress

| Fault Type | Tool | FoodExpress Scenario |
|-----------|------|---------------------|
| **Pod kill** | kubectl delete pod | Payment pod dies mid-transaction |
| **Network latency** | tc netem | 3s delay between Order and Payment |
| **Network partition** | iptables | Menu service cannot reach DB |
| **CPU stress** | stress-ng | Delivery service CPU spike |
| **Disk fill** | dd/fallocate | Log volume fills up on Order service |
| **DNS failure** | CoreDNS manipulation | Service discovery fails |
| **Dependency failure** | Mock server | External payment gateway timeout |

```bash
# Example: Add 3s latency to payment service
kubectl exec -it payment-pod -- tc qdisc add dev eth0 root netem delay 3000ms

# Example: Kill a pod
kubectl delete pod order-service-abc123 --grace-period=0

# Example: CPU stress for 60 seconds
kubectl exec -it delivery-pod -- stress-ng --cpu 4 --timeout 60s
```

---

## Fault Injection Script: FoodExpress

### Structured Fault Injection Exercise

```bash
#!/bin/bash
# fault-injection.sh -- FoodExpress Chaos Experiment

EXPERIMENT_NAME="payment-latency-test"
NAMESPACE="foodexpress"
STEADY_STATE_METRIC="foodexpress_order_success_rate"
THRESHOLD=0.99

echo "=== Chaos Experiment: $EXPERIMENT_NAME ==="
echo "Hypothesis: Order success rate stays above 99% when payment has 2s latency"

# Step 1: Record steady state
echo "[1/4] Recording steady state..."
BASELINE=$(curl -s "http://prometheus:9090/api/v1/query?query=$STEADY_STATE_METRIC" \
  | jq '.data.result[0].value[1]')
echo "  Baseline: $BASELINE"

# Step 2: Inject fault
echo "[2/4] Injecting 2s latency on payment-service..."
kubectl exec -n $NAMESPACE deploy/payment-service -- \
  tc qdisc add dev eth0 root netem delay 2000ms

# Step 3: Observe (wait 3 minutes)
echo "[3/4] Observing for 3 minutes..."
sleep 180

CURRENT=$(curl -s "http://prometheus:9090/api/v1/query?query=$STEADY_STATE_METRIC" \
  | jq '.data.result[0].value[1]')
echo "  Current: $CURRENT"

# Step 4: Rollback
echo "[4/4] Rolling back fault injection..."
kubectl exec -n $NAMESPACE deploy/payment-service -- \
  tc qdisc del dev eth0 root netem

# Evaluate
if (( $(echo "$CURRENT >= $THRESHOLD" | bc -l) )); then
  echo "PASS: Steady state maintained ($CURRENT >= $THRESHOLD)"
else
  echo "FAIL: Steady state violated ($CURRENT < $THRESHOLD)"
  echo "ACTION: Implement circuit breaker on Order->Payment call"
fi
```

---

## Distributed Tracing with Jaeger

### Following a FoodExpress Order

```
Trace ID: abc123def456

├── [200ms] POST /api/v1/orders (order-service)
│   ├── [10ms]  Validate order items
│   ├── [45ms]  GET /api/v1/menu/items (menu-service)
│   │           Check item availability
│   ├── [120ms] POST /api/v1/payments (payment-service)
│   │   ├── [15ms]  Validate payment method
│   │   ├── [80ms]  Charge payment gateway (external)
│   │   └── [25ms]  Update payment record
│   ├── [15ms]  Create order record
│   └── [10ms]  Publish OrderPlaced event
│
├── [50ms] OrderPlaced -> notification-service (async)
│   └── [30ms]  Send order confirmation email
│
└── [30ms] OrderPlaced -> delivery-service (async)
    └── [20ms]  Assign rider
```

**Key insight:** The payment gateway call (80ms) is the bottleneck. If it times out, the entire order flow stalls.

---

## Log Aggregation with Loki

### Structured Logging for FoodExpress

```json
{
  "timestamp": "2026-09-05T14:23:45.123Z",
  "level": "ERROR",
  "service": "order-service",
  "traceId": "abc123def456",
  "spanId": "span789",
  "message": "Payment service timeout",
  "orderId": "ORD-2026-45678",
  "customerId": "CUST-1234",
  "errorCode": "PAYMENT_TIMEOUT",
  "duration_ms": 5000,
  "retryCount": 3,
  "context": {
    "paymentAmount": 450.00,
    "paymentMethod": "UPI",
    "restaurant": "Biryani House"
  }
}
```

### LogQL Query Examples

```logql
# Find all errors for a specific order
{service="order-service"} |= "ORD-2026-45678" | json | level="ERROR"

# Payment timeouts in last hour
{service="order-service"} | json | errorCode="PAYMENT_TIMEOUT" | count_over_time([1h])

# Slow queries (> 2 seconds)
{service=~".*-service"} | json | duration_ms > 2000
```

---

## Runbook: High Error Rate

### FoodExpress Incident Runbook Template

```markdown
# Runbook: High Error Rate on Order Service

## Trigger
Alert: HighErrorRate (order-service error rate > 1% for 5 min)

## Severity
Critical -- Directly impacts revenue

## Quick Diagnosis (first 5 minutes)
1. Check which endpoint is failing:
   - Dashboard: FoodExpress Operations > Error Rate by Endpoint
   - PromQL: rate(http_requests_total{service="order",status=~"5.."}[5m])
2. Check recent deployments:
   - `kubectl rollout history deploy/order-service -n foodexpress`
3. Check dependent service health:
   - Payment: up{job="payment-service"}
   - Menu: up{job="menu-service"}
   - Database: mysql_up{instance="order-db"}

## Common Causes & Fixes
| Cause | Check | Fix |
|-------|-------|-----|
| Bad deployment | Recent rollout | `kubectl rollout undo deploy/order-service` |
| DB connection exhaustion | Connection pool metrics | Restart pods, increase pool size |
| Payment service down | Payment health check | Enable circuit breaker fallback |
| Memory leak | Pod memory usage | Restart pod, investigate heap dump |

## Escalation
If not resolved in 15 minutes:
- Page on-call SRE: @sre-oncall
- Notify engineering lead: @eng-lead
```

---

## Demo Preparation

### What Makes a Good Demo

| Element | Description | Time |
|---------|-------------|------|
| **Context** | What problem are you solving? | 1 min |
| **Architecture** | Show the system diagram | 2 min |
| **Live Demo** | Walk through dashboards and alerts | 5 min |
| **Fault Injection** | Inject a fault, show detection & recovery | 5 min |
| **Lessons Learned** | What surprised you? What would you change? | 2 min |

### Evaluation Criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| Monitoring Coverage | 25% | Are all services instrumented? Golden signals covered? |
| Alert Quality | 20% | Meaningful alerts with proper thresholds and runbooks? |
| Fault Resilience | 25% | Does the system handle injected faults gracefully? |
| Dashboard Design | 15% | Clear, actionable dashboards with proper panels? |
| Presentation | 15% | Clear communication, good demo flow? |

---

## Mid-Stage Project Evaluation Rubric

### Scoring Guide

```
┌──────────────────────────────────────────────────────┐
│                 Scoring (out of 100)                 │
├──────────────────┬───────────────────────────────────┤
│ Monitoring (25)  │ 25: All services, all 4 signals  │
│                  │ 20: Most services, 3+ signals     │
│                  │ 15: Some services, basic metrics   │
│                  │ 10: Minimal monitoring             │
├──────────────────┼───────────────────────────────────┤
│ Alerting (20)    │ 20: Smart alerts, runbooks, routing│
│                  │ 15: Good alerts, some runbooks     │
│                  │ 10: Basic alerts, no runbooks      │
│                  │  5: No alerting configured         │
├──────────────────┼───────────────────────────────────┤
│ Resilience (25)  │ 25: All faults handled gracefully │
│                  │ 20: Most faults handled            │
│                  │ 15: Some fault handling            │
│                  │ 10: No fault handling              │
├──────────────────┼───────────────────────────────────┤
│ Dashboards (15)  │ 15: Professional, actionable      │
│                  │ 10: Good layout, useful panels     │
│                  │  5: Basic or cluttered             │
├──────────────────┼───────────────────────────────────┤
│ Presentation (15)│ 15: Clear, confident, structured  │
│                  │ 10: Adequate communication         │
│                  │  5: Unclear or disorganized        │
└──────────────────┴───────────────────────────────────┘
```

---

## ITSM: What is IT Service Management?

<!--VISUAL:itsm-service-model-->

### Definition

**IT Service Management (ITSM)** is a set of practices for designing, delivering, managing, and improving the way IT is used within an organization.

```
┌──────────────────────────────────────────────────────┐
│                 ITSM Core Concept                    │
│                                                      │
│   IT is not just technology --                       │
│   IT is a SERVICE delivered to the business.         │
│                                                      │
│   ┌──────────┐    Service    ┌───────────────┐      │
│   │  IT Org  │ ───────────> │   Business    │      │
│   │          │              │   (Customer)  │      │
│   │ People   │ <─────────── │               │      │
│   │ Process  │   Value      │  FoodExpress  │      │
│   │ Tech     │              │  Operations   │      │
│   └──────────┘              └───────────────┘      │
│                                                      │
│   Key shift: From "managing technology"              │
│              To "managing services"                  │
└──────────────────────────────────────────────────────┘
```

---

## ITSM vs ITIL vs DevOps

### How They Relate

| Aspect | ITSM | ITIL | DevOps |
|--------|------|------|--------|
| **What** | Overall discipline | Framework for ITSM | Culture & practices |
| **Focus** | Service delivery | Best practices & processes | Speed & collaboration |
| **Scope** | End-to-end service lifecycle | Structured guidance | Dev + Ops integration |
| **Approach** | Process-oriented | Practice-based (ITIL 4) | Automation-oriented |
| **Relation** | The "what" | The "how" (one option) | Complementary approach |

```
┌─────────────────────────────────────────┐
│              ITSM (discipline)          │
│                                         │
│  ┌──────────────┐  ┌────────────────┐  │
│  │    ITIL 4    │  │    DevOps      │  │
│  │  (framework) │  │  (culture)     │  │
│  │              │  │                │  │
│  │  Practices   │◄─┤  Automation    │  │
│  │  Governance  │  │  CI/CD         │  │
│  │  Continual   │  │  Collaboration │  │
│  │  improvement │  │  Feedback      │  │
│  └──────────────┘  └────────────────┘  │
└─────────────────────────────────────────┘
```

---

## ITSM: The Service Value System

### ITIL 4 Service Value System (SVS)

```
┌───────────────────────────────────────────────────────┐
│                Service Value System                   │
│                                                       │
│  Opportunity/     ┌─────────────────────┐    Value    │
│  Demand ─────────>│  Service Value      │──────────>  │
│                   │  Chain              │             │
│                   │  (Plan, Improve,    │             │
│                   │   Engage, Design,   │             │
│                   │   Obtain, Deliver)  │             │
│                   └──────┬──────────────┘             │
│                          │                            │
│  ┌──────────────┐  ┌─────▼──────┐  ┌──────────────┐ │
│  │  Guiding     │  │ Practices  │  │  Governance   │ │
│  │  Principles  │  │ (34 ITIL   │  │              │ │
│  │              │  │  practices)│  │              │ │
│  └──────────────┘  └────────────┘  └──────────────┘ │
│                                                       │
│            Continual Improvement                      │
└───────────────────────────────────────────────────────┘
```

---

## ITIL 4 Guiding Principles

### Seven Principles for FoodExpress

| # | Principle | FoodExpress Example |
|---|-----------|---------------------|
| 1 | **Focus on value** | Every process should improve customer experience (faster delivery, fewer errors) |
| 2 | **Start where you are** | Assess current monitoring before adding new tools |
| 3 | **Progress iteratively with feedback** | Deploy observability in phases, gather team feedback |
| 4 | **Collaborate and promote visibility** | Dev and Ops share dashboards and on-call rotations |
| 5 | **Think and work holistically** | A payment fix must consider order flow, notifications, delivery |
| 6 | **Keep it simple and practical** | Don't over-engineer alerting; start with golden signals |
| 7 | **Optimize and automate** | Auto-scaling, self-healing pods, automated runbooks |

---

## ITSM Process Architecture

### Core Process Areas

```
┌─────────────────────────────────────────────────────┐
│           ITSM Process Architecture                 │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │          Service Strategy                     │  │
│  │  Service Portfolio │ Financial Mgmt │ Demand  │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │          Service Design                       │  │
│  │  Service Catalog │ SLA │ Capacity │ Avail.    │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │          Service Transition                   │  │
│  │  Change Mgmt │ Release │ Config │ Knowledge   │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │          Service Operation                    │  │
│  │  Incident │ Problem │ Event │ Request │ Access │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │          Continual Service Improvement        │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Service Catalog

### FoodExpress IT Service Catalog

| Service | Description | SLA | Owner |
|---------|-------------|-----|-------|
| **Order Platform** | End-to-end food ordering | 99.9% uptime, P95 < 2s | Platform Team |
| **Payment Processing** | Payment handling, refunds | 99.95% uptime, PCI compliant | Payment Team |
| **Delivery Tracking** | Real-time rider tracking | 99.5% uptime, < 30s GPS update | Logistics Team |
| **Menu Management** | Restaurant menu CRUD | 99.5% uptime | Content Team |
| **Customer Support** | Support portal and chatbot | 99% uptime, < 5 min first response | Support Team |
| **Partner Portal** | Restaurant onboarding | 99% uptime | Partner Team |
| **Internal IT** | Email, VPN, laptops | 99.5% uptime | IT Ops |

### Service Catalog Structure

```
Business Services (visible to customers)
├── Order Platform
├── Delivery Tracking
└── Customer Support

Technical Services (supporting services)
├── Kubernetes Cluster
├── MySQL Database Cluster
├── Redis Cache
├── Message Queue (RabbitMQ)
└── Monitoring Stack
```

---

## Service Portfolio vs Service Catalog

### The Full Picture

```
┌─────────────────────────────────────────────────┐
│              Service Portfolio                   │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │  Service Pipeline (planned)             │    │
│  │  - AI-powered food recommendations     │    │
│  │  - Voice ordering via smart speakers    │    │
│  │  - Drone delivery pilot                │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │  Service Catalog (live)                 │    │
│  │  - Order Platform        ✅ Active      │    │
│  │  - Payment Processing    ✅ Active      │    │
│  │  - Delivery Tracking     ✅ Active      │    │
│  │  - Menu Management       ✅ Active      │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
│  ┌─────────────────────────────────────────┐    │
│  │  Retired Services                       │    │
│  │  - Legacy monolith v1    ❌ Retired     │    │
│  │  - SMS-only ordering     ❌ Retired     │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## Incident Management: Overview

### What is an Incident?

**An unplanned interruption to a service or reduction in the quality of a service.**

| Term | Definition | FoodExpress Example |
|------|-----------|---------------------|
| **Incident** | Unplanned service disruption | Payment gateway returning 503 errors |
| **Major Incident** | High-impact incident | Complete order platform outage |
| **Event** | Observable occurrence | CPU usage above 80% threshold |
| **Alert** | Notification triggered by an event | PagerDuty alert for high error rate |
| **Problem** | Root cause of one or more incidents | Memory leak in order service v2.3 |

---

## Incident Lifecycle

<!--VISUAL:itsm-incident-flow-->

### From Detection to Closure

```
┌──────────┐   ┌──────────┐   ┌───────────┐   ┌──────────┐
│ Detection│──>│  Logging  │──>│  Category │──>│ Priority │
│          │   │& Recording│   │& Classify │   │ Matrix   │
└──────────┘   └──────────┘   └───────────┘   └────┬─────┘
                                                     │
┌──────────┐   ┌──────────┐   ┌───────────┐   ┌────▼─────┐
│ Closure  │<──│Resolution│<──│Escalation │<──│ Diagnosis│
│& Review  │   │          │   │(if needed)│   │& Invest. │
└──────────┘   └──────────┘   └───────────┘   └──────────┘

FoodExpress Incident Flow:
1. Prometheus alert fires (Detection)
2. PagerDuty notifies on-call engineer (Logging)
3. Engineer classifies: Order Service > Payment Integration (Categorize)
4. Priority: P1 (Critical impact, 500+ users affected) (Prioritize)
5. Engineer investigates using Grafana, Jaeger, Loki (Diagnose)
6. Applies fix or rollback (Resolve)
7. Post-incident review within 48 hours (Close & Review)
```

---

## Incident Priority Matrix

### Impact vs Urgency

```
                        URGENCY
                 High        Medium       Low
         ┌──────────┬──────────┬──────────┐
  High   │   P1     │   P2     │   P3     │
         │ Critical │  High    │ Medium   │
I        ├──────────┼──────────┼──────────┤
M Medium │   P2     │   P3     │   P4     │
P        │  High    │ Medium   │  Low     │
A        ├──────────┼──────────┼──────────┤
C  Low   │   P3     │   P4     │   P5     │
T        │ Medium   │  Low     │ Planning │
         └──────────┴──────────┴──────────┘
```

| Priority | Response Time | Resolution Time | FoodExpress Example |
|----------|--------------|-----------------|---------------------|
| P1 | 15 min | 4 hours | Complete order platform down |
| P2 | 30 min | 8 hours | Payment service degraded |
| P3 | 2 hours | 24 hours | Delivery tracking delayed |
| P4 | 4 hours | 48 hours | Partner portal slow |
| P5 | 1 business day | 5 business days | Report generation failing |

---

## Incident Record Template

### What to Capture

```
┌──────────────────────────────────────────────────┐
│              INCIDENT RECORD                     │
├──────────────────────────────────────────────────┤
│ INC Number:    INC-2026-0456                     │
│ Title:         Payment Service 503 Errors        │
│ Priority:      P1 - Critical                     │
│ Status:        Resolved                          │
│ Category:      Application > Payment > Gateway   │
│                                                  │
│ Affected Service: Payment Processing             │
│ Affected Users:   ~2,000 customers               │
│ Business Impact:  Orders failing, est. Rs 5L/hr  │
│                   revenue loss                   │
│                                                  │
│ Timeline:                                        │
│   09:15  Alert fired (HighErrorRate)             │
│   09:18  On-call engineer acknowledged           │
│   09:25  Root cause: DB connection pool exhaust  │
│   09:30  Fix applied: increased pool size        │
│   09:35  Error rate normalized                   │
│   09:40  Incident resolved                       │
│                                                  │
│ Root Cause:    Connection pool max=10 too low     │
│                after traffic spike                │
│ Resolution:    Increased pool to 50, added        │
│                connection timeout                 │
│ Prevention:    Add auto-scaling for DB pool,      │
│                alert on pool saturation > 70%     │
│                                                  │
│ Assigned To:   Ravi Kumar (Sustain Eng)           │
│ Resolved By:   Ravi Kumar                        │
│ Created:       2026-09-05 09:15                  │
│ Resolved:      2026-09-05 09:40                  │
│ Duration:      25 minutes                        │
└──────────────────────────────────────────────────┘
```

---

## Major Incident Process

### When Things Go Really Wrong

```
┌─────────────────────────────────────────────────────┐
│           Major Incident Process                    │
│                                                     │
│  1. DECLARE Major Incident                          │
│     - Incident Manager takes ownership              │
│     - Communication channel opened (#war-room)      │
│                                                     │
│  2. ASSEMBLE Response Team                          │
│     - Incident Commander (coordinates)              │
│     - Technical Lead (investigates)                 │
│     - Communications Lead (updates stakeholders)    │
│                                                     │
│  3. COMMUNICATE Status                              │
│     - Status page updated every 15 min              │
│     - Business stakeholders notified                │
│     - Customer-facing message posted                │
│                                                     │
│  4. RESOLVE & RECOVER                               │
│     - Apply fix / rollback / workaround             │
│     - Verify service restoration                    │
│     - Monitor for recurrence                        │
│                                                     │
│  5. POST-INCIDENT REVIEW (within 48 hours)          │
│     - Blameless retrospective                       │
│     - Timeline reconstruction                       │
│     - Action items with owners and deadlines        │
└─────────────────────────────────────────────────────┘
```

---

## Incident Management KPIs

### Measuring Incident Management Effectiveness

| KPI | Formula | Target | FoodExpress |
|-----|---------|--------|-------------|
| **MTTR** | Mean Time to Resolve | P1 < 4h, P2 < 8h | Currently: P1 = 2.5h |
| **MTTA** | Mean Time to Acknowledge | P1 < 15 min | Currently: 8 min |
| **MTTD** | Mean Time to Detect | < 5 min for critical | Currently: 3 min |
| **Incident Volume** | Incidents per month | Trending down | 45 last month |
| **Reopen Rate** | % incidents reopened | < 5% | Currently: 3% |
| **First Contact Resolution** | % resolved at first touch | > 70% | Currently: 65% |
| **SLA Compliance** | % resolved within SLA | > 95% | Currently: 92% |

```
MTTR Breakdown:

  MTTD + MTTA + MTTI + MTTR = Total Resolution Time
  ────   ────   ────   ────
  Detect  Ack   Invest  Repair

  For FoodExpress P1:
  3 min + 8 min + 60 min + 79 min = 150 min (2.5 hours)
```

---

## ITSM in Practice: FoodExpress Scenario

### A Day in the Life of a Sustain Engineer

```
09:00  Check overnight alerts in Slack (#foodexpress-alerts)
       - 2 warnings: Delivery service memory usage high
       - 1 resolved: Payment timeout (auto-recovered)

09:15  Review Grafana dashboard for anomalies
       - Order rate normal, error rate stable at 0.2%

10:00  Incoming incident: INC-2026-0457
       "Customer complaints: Some orders showing wrong total"
       - Categorize: Application > Order > Calculation
       - Priority: P3 (Medium impact, not widespread)
       - Assign to self

10:30  Investigate using Jaeger traces
       - Find race condition in discount calculation
       - Fix applied and deployed via CI/CD

11:00  Update incident record, close with root cause

14:00  Proactive: Review Problem PRB-2026-0023
       "Recurring memory spikes in delivery service"
       - Analyze trends in Prometheus
       - Identify memory leak in WebSocket connections
       - Create change request CHG-2026-0089

16:00  Change Advisory Board (CAB) review
       - Present CHG-2026-0089 for approval
       - Scheduled for next maintenance window
```

---

## Connecting Observability to ITSM

### The Bridge

```
┌──────────────────────┐      ┌──────────────────────┐
│    OBSERVABILITY     │      │        ITSM          │
│                      │      │                      │
│  Prometheus Alert ───┼──────┼──> Incident Created  │
│                      │      │                      │
│  Grafana Dashboard ──┼──────┼──> KPI Reporting     │
│                      │      │                      │
│  Jaeger Trace ───────┼──────┼──> Root Cause in     │
│                      │      │    Incident Record   │
│                      │      │                      │
│  Loki Logs ──────────┼──────┼──> Evidence for      │
│                      │      │    Problem Record    │
│                      │      │                      │
│  Chaos Experiment ───┼──────┼──> Proactive Problem │
│  Results             │      │    Identification    │
│                      │      │                      │
│  SLI/SLO Dashboards─┼──────┼──> SLA Compliance    │
│                      │      │    Reporting         │
└──────────────────────┘      └──────────────────────┘

Observability provides the DATA.
ITSM provides the PROCESS.
Together they deliver VALUE.
```

---

## ITSM Tools Landscape

### Common ITSM Platforms

| Tool | Type | Key Strength | Used By |
|------|------|-------------|---------|
| **ServiceNow** | Enterprise ITSM | Comprehensive, workflow automation | Large enterprises |
| **Jira Service Management** | Agile ITSM | Dev integration, flexibility | Mid-size teams |
| **BMC Helix** | Enterprise ITSM | AI-powered, multi-cloud | Large enterprises |
| **Freshservice** | Cloud ITSM | Easy setup, good UX | SMBs |
| **Zendesk** | Help desk + ITSM | Customer-centric | Customer-facing teams |
| **PagerDuty** | Incident management | On-call, escalation | DevOps/SRE teams |

**FoodExpress uses:** ServiceNow (ITSM) + PagerDuty (alerting) + Jira (dev tracking)

We will deep-dive into **ServiceNow** in Module 36.

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Golden Signals | Latency, Traffic, Errors, Saturation -- monitor all four for every service |
| Prometheus + Grafana | Metrics collection and visualization; PromQL for powerful queries |
| Alerting | Meaningful alerts with runbooks; route by severity; avoid alert fatigue |
| Chaos Engineering | Proactively inject faults to find weaknesses before production does |
| Distributed Tracing | Follow requests across services; identify bottlenecks with Jaeger |
| Log Aggregation | Structured JSON logs; correlate with traceId; query with LogQL |
| ITSM Overview | IT as a service to the business; process + people + technology |
| ITSM vs ITIL vs DevOps | ITSM is the discipline, ITIL is a framework, DevOps is complementary |
| Service Catalog | Document all services with SLAs, owners, and dependencies |
| Incident Management | Detection -> Logging -> Classification -> Priority -> Diagnosis -> Resolution |
| Priority Matrix | Impact x Urgency = Priority; drives response and resolution times |
| Observability + ITSM | Observability provides data, ITSM provides process; together they deliver value |

> **Next: Module 35 -- ITIL Practices**
