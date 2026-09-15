# Lab 09: Fix Buggy Observability Configs (9 Bugs)
## 30 min | Prerequisite: Labs 03-06

---

## What You'll Learn
- Common Prometheus misconfiguration patterns
- PromQL mistakes that produce misleading dashboards
- Alert rule anti-patterns that cause alert fatigue
- How to validate observability configs

## Why This Matters
In sustain engineering, you inherit configurations someone else wrote (often under time pressure). Misconfigurations are subtle -- the system "works" but gives WRONG data. Teams make decisions based on incorrect dashboards. A dashboard showing 0% errors when the real error rate is 5% is worse than having no dashboard at all -- it creates a false sense of security.

## New Terms

| Term | Meaning |
|------|---------|
| **Scrape target** | A `host:port` that Prometheus fetches `/metrics` from. If the target is wrong, Prometheus scrapes the wrong service or nothing at all. |
| **metrics_path** | The URL path where metrics are exposed. Default is `/metrics`, but Spring Boot uses `/actuator/prometheus`. Wrong path = Prometheus gets 404 errors. |
| **Alert fatigue** | When engineers receive so many false alerts that they start ignoring ALL alerts -- including real ones. The #1 cause of missed incidents. |
| **False positive** | An alert that fires when there's no actual problem. Example: CPU briefly spikes to 55% during a deployment and triggers a "HighCPU" alert set at 50%. |
| **Cardinality** | The number of unique values a label can have. `status` has ~5 values (low cardinality, good). `user_id` has millions (high cardinality, bad for metrics). |

---

## Concepts Being Tested

| Bug Category | From Lab | What goes wrong |
|-------------|----------|-----------------|
| Wrong scrape target | Lab 03 | Prometheus scrapes itself instead of the service |
| Missing service | Lab 03 | One service is completely invisible to monitoring |
| Wrong metrics_path | Lab 03 | Prometheus gets 404 on every scrape attempt |
| Counter without rate() | Lab 03 | Dashboard shows ever-growing number, not percentage |
| Multiply vs divide | Lab 03 | Orders/min shows 0.02 instead of 142 |
| avg() vs histogram_quantile() | Lab 03 | Dashboard hides the slow outliers |
| Threshold too low | Lab 06 | Alert fires constantly on normal traffic |
| for: 0m | Lab 06 | Every transient spike triggers a page |
| CPU threshold 50% | Lab 06 | Normal workload triggers alerts daily |

---

## Scenario

```
From: arjun.reddy@foodexpress.in
Subject: Observability Stack Not Working

Team,

Three problems:
1. Prometheus is only scraping 1 out of 3 services
2. Grafana dashboard shows incorrect metrics
3. We're getting flooded with false alerts at 3 AM

Fix these configs before the Diwali traffic surge.
-- Arjun Reddy, SRE Lead
```

> **Think About It:** You have 20 minutes to find and fix all 9 bugs across 3 files. Work through them systematically -- don't just guess.

---

## File 1: `prometheus.yml` (3 bugs)

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'order-service'
    metrics_path: /metrics
    static_configs:
      - targets: ['order-service:8080']
    scrape_interval: 10s

  - job_name: 'payment-service'
    metrics_path: /actuator/prometheus
    static_configs:
      - targets: ['localhost:9090']
    scrape_interval: 10s
```

### Find & fix 3 bugs:

| # | Hint |
|---|------|
| 1 | One service's target URL is pointing to the wrong host entirely |
| 2 | One of the 3 FoodExpress services (order, payment, menu) has no config at all |
| 3 | One metrics_path doesn't match what Spring Boot Actuator exposes |

> **How to verify your fix:** All 3 services should appear in Prometheus **Status > Targets** as UP.

<details>
<summary>Fixes</summary>

1. **payment-service target:** `localhost:9090` should be `payment-service:8080` (was scraping Prometheus itself!)
2. **menu-service missing:** Add a complete job for `menu-service` with target `menu-service:8080`
3. **order-service metrics_path:** `/metrics` should be `/actuator/prometheus` (Spring Boot Actuator path)

</details>

---

## File 2: `grafana-dashboard.json` (3 bugs)

```json
{
  "panels": [
    {
      "title": "Error Rate (%)",
      "expr": "http_requests_total{status=~\"5..\"} / http_requests_total * 100"
    },
    {
      "title": "Orders per Minute",
      "expr": "rate(orders_placed_total{service=\"order-service\"}[1m]) / 60"
    },
    {
      "title": "P99 Latency (ms)",
      "expr": "avg(http_request_duration_seconds_sum / http_request_duration_seconds_count) * 1000"
    }
  ]
}
```

### Find & fix 3 bugs:

| # | Symptom | Hint |
|---|---------|------|
| 1 | Error Rate shows a number in millions, not a percentage | What PromQL function converts a counter into a per-second rate? |
| 2 | Orders/min shows 0.02 instead of ~142 | `rate()` returns per-second. To get per-minute, do you multiply or divide by 60? |
| 3 | P99 Latency panel says "P99" but actually shows the average | What function calculates the 99th percentile from histogram buckets? |

> **Quick Question:** Bug #3 is the most dangerous. Why? (Because the dashboard SAYS "P99" but SHOWS average. The team thinks p99 is 200ms when it's actually 2 seconds. They believe performance is fine when users are suffering.)

<details>
<summary>Fixes</summary>

1. Wrap with `rate()`: `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) * 100`
2. Change `/ 60` to `* 60` (rate returns per-second, multiply to get per-minute)
3. Replace `avg(...)` with `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) * 1000`

</details>

---

## File 3: `alerts.yml` (3 bugs)

```yaml
groups:
  - name: foodexpress-alerts
    rules:
      - alert: HighErrorRate
        expr: >
          rate(http_requests_total{status=~"5.."}[5m])
          / rate(http_requests_total[5m]) > 0.001
        for: 5m
        labels:
          severity: critical

      - alert: HighLatency
        expr: >
          histogram_quantile(0.99,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1.0
        for: 0m
        labels:
          severity: warning

      - alert: HighCPU
        expr: >
          100 - (avg by(instance)
            (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100
          ) > 50
        for: 10m
        labels:
          severity: warning
```

### Find & fix 3 bugs:

| # | Symptom | Hint |
|---|---------|------|
| 1 | HighErrorRate fires constantly, even when traffic is normal | Normal error rate is ~0.2%. What threshold would avoid false alarms? |
| 2 | HighLatency fires on every tiny spike, even for 1 second | What does `for: 0m` mean? How long should a condition persist? |
| 3 | HighCPU fires every day during the lunch rush | CPU at 60% is normal under load. What percentage means REAL saturation? |

<details>
<summary>Fixes</summary>

1. Threshold `0.001` (0.1%) -> `0.01` (1%). Normal error rate ~0.2% constantly triggers 0.1%
2. `for: 0m` -> `for: 5m`. Without a buffer, a single slow request triggers the alert
3. CPU threshold `50` -> `90`. 60% is normal under load; 90% indicates real saturation

</details>

---

## Scoring

| File | Bugs | Points | Focus Area |
|------|------|--------|------------|
| prometheus.yml | 3 | 8 | Config: targets, paths, service discovery |
| grafana-dashboard.json | 3 | 10 | PromQL: rate(), math, percentiles |
| alerts.yml | 3 | 8 | Alerting: thresholds, duration, fatigue |
| **Total** | **9** | **26** | |

---

## Discussion

1. Which of the 9 bugs would be hardest to spot in production? Why?
2. Bug #3 in the dashboard (avg vs p99) gives WRONG numbers but doesn't crash anything. Why is this the most dangerous bug?
3. How would you prevent these bugs in a real team? (Config changes go through code review, dashboards validated against known test data, alert runbooks tested regularly)

---

## What's Next

Lab 10 -- Deploy the multi-service stack on **Kubernetes** with Prometheus auto-discovery. No more hardcoded targets!
