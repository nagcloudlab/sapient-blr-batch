# Observability
## Module 32 | Sustain Engineering Training | Day 36

---

## Agenda -- Day 36

| # | Topic |
|---|-------|
| 01 | Monitoring vs Observability |
| 02 | Three Pillars: Logs, Metrics, Traces |
| 03 | Golden Signals: Latency, Traffic, Errors, Saturation |
| 04 | Prometheus: Metrics Collection |
| 05 | PromQL: Querying Metrics |
| 06 | Grafana: Dashboards & Visualization |
| 07 | Alerting: Rules & Routing |
| 08 | DataDog, RUM & APM |
| 09 | Lab: Fix FoodExpress Observability Stack |
| 10 | Day 36 Wrap-up |

---

## Monitoring vs Observability

### They are related but different

| Aspect | Monitoring | Observability |
|--------|-----------|---------------|
| **Question** | "Is the system working?" | "Why is it not working?" |
| **Approach** | Predefined checks and thresholds | Explore arbitrary questions |
| **Data** | Known metrics and alerts | Logs + Metrics + Traces combined |
| **Failure mode** | Detects known failure patterns | Investigates unknown failures |
| **Example** | "CPU is above 90%" alert | "Why are orders from Mumbai 3x slower than Delhi?" |

```
Monitoring tells you SOMETHING is wrong.
Observability tells you WHAT is wrong and WHY.
```

---

## The Three Pillars of Observability

```
┌─────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                        │
│                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │          │    │          │    │          │          │
│  │   LOGS   │    │ METRICS  │    │  TRACES  │          │
│  │          │    │          │    │          │          │
│  │ What     │    │ How much │    │ Where    │          │
│  │ happened │    │ and when │    │ time is  │          │
│  │          │    │          │    │ spent    │          │
│  └──────────┘    └──────────┘    └──────────┘          │
│                                                          │
│  "Order #1234     "99th percentile  "Order #1234 took   │
│   failed with      latency is       200ms: 50ms in      │
│   NPE at line 42"  350ms"           menu, 120ms in      │
│                                      payment, 30ms       │
│                                      in delivery"        │
└─────────────────────────────────────────────────────────┘
```

All three pillars are needed for full observability.

---

## Pillar 1: Logs

### Structured event records

```json
{
  "timestamp": "2026-09-08T14:23:45.123Z",
  "level": "ERROR",
  "service": "order-service",
  "traceId": "abc-123-def-456",
  "userId": "user_789",
  "message": "Payment gateway timeout",
  "orderId": "ORD-2026-1234",
  "duration_ms": 30000,
  "error": "java.net.SocketTimeoutException"
}
```

### Log best practices for FoodExpress:
- **Structured logging** (JSON) over plain text
- Include **traceId** in every log line for correlation
- Log **business events** (order placed, payment processed) not just errors
- Use **log levels** correctly: ERROR for failures, WARN for degraded, INFO for events
- **Centralize** logs with ELK (Elasticsearch + Logstash + Kibana) or Loki

---

## Pillar 2: Metrics

### Numeric measurements over time

```
# Counter: only goes up
http_requests_total{service="order-service", method="POST", status="200"} 15234

# Gauge: goes up and down
active_orders{service="order-service"} 42

# Histogram: distribution of values
http_request_duration_seconds_bucket{le="0.1"} 12000
http_request_duration_seconds_bucket{le="0.5"} 14500
http_request_duration_seconds_bucket{le="1.0"} 15000
```

| Metric Type | Description | FoodExpress Example |
|-------------|-------------|---------------------|
| **Counter** | Monotonically increasing | Total orders placed |
| **Gauge** | Current value, can go up/down | Active delivery drivers |
| **Histogram** | Distribution of observations | Order processing time |
| **Summary** | Similar to histogram, calculates quantiles | API response times |

---

## Pillar 3: Traces

### Follow a request across microservices

```
Trace ID: abc-123-def-456

├── [order-service] POST /api/v1/orders      200ms total
│   ├── [menu-service] GET /api/v1/menu/42   50ms
│   ├── [payment-service] POST /pay          120ms
│   │   └── [payment-gateway] charge         100ms
│   └── [delivery-service] POST /assign      30ms
│       └── [notification] send SMS          10ms
```

### Distributed tracing tools:
- **Jaeger** (CNCF, open source)
- **Zipkin** (Twitter, open source)
- **OpenTelemetry** (CNCF standard for instrumentation)
- **DataDog APM** (commercial)

Traces answer: "Where is the bottleneck in this request?"

---

## Golden Signals

### Four key metrics every service should track (Google SRE book)

```
┌──────────────────────────────────────────────────┐
│              THE FOUR GOLDEN SIGNALS              │
│                                                    │
│  ┌────────────┐          ┌────────────┐           │
│  │  LATENCY   │          │  TRAFFIC   │           │
│  │            │          │            │           │
│  │ How long   │          │ How much   │           │
│  │ requests   │          │ demand     │           │
│  │ take       │          │ exists     │           │
│  └────────────┘          └────────────┘           │
│                                                    │
│  ┌────────────┐          ┌────────────┐           │
│  │   ERRORS   │          │ SATURATION │           │
│  │            │          │            │           │
│  │ Rate of    │          │ How full   │           │
│  │ failed     │          │ the system │           │
│  │ requests   │          │ is         │           │
│  └────────────┘          └────────────┘           │
└──────────────────────────────────────────────────┘
```

---

## Golden Signals: FoodExpress Examples

| Signal | What to Measure | FoodExpress Example | Alert Threshold |
|--------|----------------|---------------------|-----------------|
| **Latency** | Response time (p50, p95, p99) | Order placement: p99 < 500ms | p99 > 1s for 5 min |
| **Traffic** | Requests per second | Orders/min, API calls/sec | > 2x normal for 10 min |
| **Errors** | Error rate (%) | 5xx errors / total requests | > 1% for 5 min |
| **Saturation** | Resource utilization | CPU > 80%, memory > 85% | CPU > 90% for 10 min |

**Key insight:** Separate successful request latency from error latency. A fast error (10ms 500 response) should not lower your average latency.

---

## Prometheus

### Open-source monitoring and alerting system

```
┌─────────────────────────────────────────────────┐
│                  Prometheus                     │
│                                                  │
│  ┌──────────┐    ┌───────────┐   ┌──────────┐  │
│  │  TSDB    │    │  HTTP     │   │ Alert    │  │
│  │ (Time    │◄───│  Pull     │   │ Manager  │  │
│  │  Series  │    │  Scraper  │   │          │  │
│  │  DB)     │    └───────────┘   └──────────┘  │
│  └──────────┘         │                         │
│                       │ scrapes every 15s        │
└───────────────────────┼─────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │  Order   │   │  Menu    │   │ Payment  │
  │ Service  │   │ Service  │   │ Service  │
  │ :8080    │   │ :8080    │   │ :8080    │
  │ /metrics │   │ /metrics │   │ /metrics │
  └──────────┘   └──────────┘   └──────────┘
```

Prometheus **pulls** metrics from targets (services expose `/metrics` endpoint).

---

## Prometheus Configuration

### prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerts.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  - job_name: 'order-service'
    metrics_path: /actuator/prometheus
    static_configs:
      - targets: ['order-service:8080']
    scrape_interval: 10s

  - job_name: 'menu-service'
    metrics_path: /actuator/prometheus
    static_configs:
      - targets: ['menu-service:8080']

  - job_name: 'payment-service'
    metrics_path: /actuator/prometheus
    static_configs:
      - targets: ['payment-service:8080']
```

---

## PromQL: Querying Metrics

### Prometheus Query Language

```promql
# Total HTTP requests in the last 5 minutes
rate(http_requests_total[5m])

# Error rate (percentage)
rate(http_requests_total{status=~"5.."}[5m])
  / rate(http_requests_total[5m]) * 100

# 99th percentile latency
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[5m])
)

# Orders per minute for FoodExpress
rate(orders_placed_total{service="order-service"}[1m]) * 60

# Memory usage percentage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
  / node_memory_MemTotal_bytes * 100
```

| Function | Purpose |
|----------|---------|
| `rate()` | Per-second rate of increase for counters |
| `histogram_quantile()` | Calculate percentiles from histograms |
| `increase()` | Total increase over a time range |
| `avg_over_time()` | Average value over a time range |

---

## Grafana

### Visualization and dashboarding platform

```
┌─────────────────────────────────────────────────────────┐
│  FoodExpress Production Dashboard            🔄 Last 1h │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Orders/min  │  │ Error Rate  │  │ p99 Latency │     │
│  │    142      │  │   0.3%      │  │   245ms     │     │
│  │   ▲ 12%     │  │   ✓ < 1%   │  │   ✓ < 500ms │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Request Rate by Service                          │  │
│  │  ▓▓▓▓▓▓▓▓▓░░░░  order-service: 85 req/s         │  │
│  │  ▓▓▓▓▓░░░░░░░░  menu-service:  42 req/s         │  │
│  │  ▓▓▓░░░░░░░░░░  payment-service: 28 req/s       │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  CPU & Memory Usage by Pod                        │  │
│  │  📊 [Time series graph]                          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

Grafana connects to Prometheus (and many other data sources) to build dashboards.

---

## Grafana Dashboard JSON

### Dashboards are defined as JSON

```json
{
  "dashboard": {
    "title": "FoodExpress Production",
    "panels": [
      {
        "title": "Orders per Minute",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(orders_placed_total[1m]) * 60",
            "legendFormat": "Orders/min"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "gauge",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100",
            "legendFormat": "Error %"
          }
        ],
        "thresholds": [
          { "value": 0, "color": "green" },
          { "value": 1, "color": "yellow" },
          { "value": 5, "color": "red" }
        ]
      }
    ]
  }
}
```

---

## Alerting: Rules & Routing

### Prometheus Alert Rules

```yaml
# alerts.yml
groups:
  - name: foodexpress-alerts
    rules:
      - alert: HighErrorRate
        expr: >
          rate(http_requests_total{status=~"5.."}[5m])
          / rate(http_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 1%)"

      - alert: HighLatency
        expr: >
          histogram_quantile(0.99,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High p99 latency on {{ $labels.service }}"
          description: "p99 latency is {{ $value }}s (threshold: 1s)"
```

---

## Alert Routing with Alertmanager

### Route alerts to the right people

```yaml
# alertmanager.yml
route:
  receiver: 'default-receiver'
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
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
        text: '{{ .CommonAnnotations.summary }}'
  - name: 'default-receiver'
    email_configs:
      - to: 'sustain-team@foodexpress.in'
```

---

## DataDog

### Commercial observability platform

```
┌─────────────────────────────────────────────────┐
│                   DataDog                       │
│                                                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │  APM     │ │  Logs    │ │ Infra    │        │
│  │ (traces) │ │          │ │ Metrics  │        │
│  └──────────┘ └──────────┘ └──────────┘        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │  RUM     │ │ Synthetics│ │ Security │        │
│  │ (browser)│ │ (uptime)  │ │ Monitor  │        │
│  └──────────┘ └──────────┘ └──────────┘        │
│                                                  │
│  ┌──────────────────────────────────────┐       │
│  │    Unified Dashboard & Alerting     │       │
│  └──────────────────────────────────────┘       │
└─────────────────────────────────────────────────┘
```

| Feature | Description |
|---------|-------------|
| **APM** | Application Performance Monitoring (traces) |
| **RUM** | Real User Monitoring (browser performance) |
| **Synthetics** | Automated uptime checks |
| **Log Management** | Centralized log aggregation |
| **Infrastructure** | Host, container, K8s metrics |

---

## RUM: Real User Monitoring

### Measure performance from the user's browser

```javascript
// DataDog RUM initialization for FoodExpress
import { datadogRum } from '@datadog/browser-rum';

datadogRum.init({
  applicationId: 'foodexpress-web',
  clientToken: 'pub_xxx',
  site: 'datadoghq.com',
  service: 'foodexpress-frontend',
  env: 'production',
  version: '1.2.0',
  trackInteractions: true,
  trackResources: true,
  trackLongTasks: true,
});
```

### What RUM captures:
- **Page load time** (FCP, LCP, TTFB)
- **User interactions** (clicks, scrolls, navigation)
- **JavaScript errors** in the browser
- **Resource loading** (API calls, images, scripts)
- **Core Web Vitals** (Google ranking signals)

---

## APM: Application Performance Monitoring

### Trace every request through your backend

```
FoodExpress Order Flow - APM Trace:

[Browser] ──────────────────────────────── 650ms total
  └─ [API Gateway] ──────────────────────── 620ms
      ├─ [order-service] POST /orders ────── 580ms
      │   ├─ Validate order ────────────────── 20ms
      │   ├─ [menu-service] GET /menu/items ── 80ms
      │   │   └─ MySQL query ──────────────── 15ms
      │   ├─ [payment-service] POST /charge ── 400ms  ← BOTTLENECK
      │   │   └─ Payment gateway API ──────── 380ms
      │   └─ [delivery-service] POST /assign ── 50ms
      │       └─ MongoDB query ────────────── 10ms
      └─ Response to browser ──────────────── 30ms
```

APM immediately shows: payment gateway is the bottleneck (400ms out of 650ms).

---

## Monitoring Types Summary

| Type | What | Tools | FoodExpress Use |
|------|------|-------|-----------------|
| **Infrastructure** | CPU, memory, disk, network | Prometheus, DataDog, CloudWatch | Node health |
| **Application** | Response time, error rate, throughput | APM (DataDog, New Relic, Jaeger) | Service performance |
| **Business** | Orders/min, revenue, conversion | Custom metrics + Grafana | Business KPIs |
| **Synthetic** | Simulated user journeys | DataDog Synthetics, Pingdom | Uptime monitoring |
| **Real User** | Actual browser performance | RUM (DataDog, New Relic) | Frontend experience |
| **Log** | Event records | ELK, Loki, DataDog Logs | Debugging, audit trail |

---

## Observability in Practice: Incident Investigation

### Scenario: FoodExpress orders failing

```
1. ALERT: Error rate > 5% on order-service (Prometheus)

2. DASHBOARD: Grafana shows spike started at 14:23
   - order-service error rate: 8%
   - payment-service latency: p99 = 5s (normally 200ms)
   - menu-service: normal

3. TRACES: Jaeger shows payment-service calls timing out
   - 90% of traces show payment-gateway > 5s
   - payment-gateway health: degraded

4. LOGS: Order-service logs show:
   "Payment gateway timeout after 5000ms for order ORD-2026-5678"
   All errors have same payment gateway endpoint

5. ROOT CAUSE: Payment gateway vendor degradation
   ACTION: Increase timeout, enable circuit breaker, notify vendor
```

All three pillars worked together to identify the root cause.

---

## Lab: Fix FoodExpress Observability Stack

### Scenario

FoodExpress observability setup has bugs causing:
- Prometheus not scraping all services
- Grafana dashboard showing wrong data
- Alert rules with wrong thresholds (too many false alarms)

### Files to fix:
1. `prometheus.yml` -- 3 bugs
2. `grafana-dashboard.json` -- 3 bugs
3. `alerts.yml` -- 3 bugs

See `Labs/lab-exercises.md` for detailed bug list.

---

## Observability Best Practices

| Practice | Why |
|----------|-----|
| Use structured logging (JSON) | Parseable by log aggregators |
| Include traceId in every log | Correlate logs across services |
| Track the four golden signals | Cover the most important failure modes |
| Set meaningful alert thresholds | Too low = alert fatigue; too high = missed incidents |
| Use dashboards for exploration | Quick visual identification of anomalies |
| Separate error latency from success latency | Errors skew averages |
| Alert on symptoms, not causes | "Error rate high" not "CPU high" |
| Practice runbooks for common alerts | Reduce MTTR |

---

## Key Takeaways

| Concept | Key Point |
|---------|-----------|
| Monitoring vs Observability | Monitoring = is it working? Observability = why is it not? |
| Three Pillars | Logs (what), Metrics (how much), Traces (where) |
| Golden Signals | Latency, Traffic, Errors, Saturation |
| Prometheus | Pull-based metrics; PromQL for queries |
| Grafana | Dashboard visualization; connects to many data sources |
| Alerting | Rules in Prometheus; routing in Alertmanager |
| APM | Traces across microservices; find bottlenecks |
| RUM | Real user browser performance; Core Web Vitals |

> **Next:** Module 33 -- SRE Automation (SLI, SLO, Error Budgets, Incident Response)
