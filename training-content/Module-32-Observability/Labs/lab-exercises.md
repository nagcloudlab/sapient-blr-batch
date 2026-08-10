# Observability -- Lab Exercises
## Module 32 | Day 36

---

## Client Email

```
From: arjun.reddy@foodexpress.in
To: sustain-engineering@team.com
Subject: Observability Stack Not Working Properly
Date: 2026-09-08

Team,

Our observability stack for FoodExpress is misconfigured:

1. Prometheus is only scraping 1 out of 3 services
2. The Grafana dashboard shows incorrect metrics --
   error rate panel shows request count instead of percentage
3. We're getting flooded with false-alarm alerts at 3 AM
   because thresholds are way too sensitive

Please fix these configs. We need reliable monitoring before
our Diwali traffic surge.

-- Arjun Reddy, SRE Lead, FoodExpress
```

---

## Lab 1: Fix Prometheus Configuration (3 bugs)

### File: `starter-code/prometheus.yml`

| # | Hint | Impact |
|---|------|--------|
| 1 | The `job_name` for payment-service is present but `targets` points to `localhost:9090` (Prometheus itself) instead of the actual payment service | Prometheus scrapes itself instead of payment-service; payment metrics are missing |
| 2 | The menu-service scrape config is missing entirely -- no `job_name` entry for it | No metrics collected from menu-service; it is invisible to monitoring |
| 3 | The `metrics_path` for order-service is `/metrics` but Spring Boot Actuator exposes metrics at `/actuator/prometheus` | Prometheus gets 404 on every scrape attempt; order-service shows as DOWN |

### Verification
- Prometheus targets page (`/targets`) shows all 3 services as UP
- `up{job="order-service"}` returns 1
- `up{job="payment-service"}` returns 1
- `up{job="menu-service"}` returns 1

---

## Lab 2: Fix Grafana Dashboard (3 bugs)

### File: `starter-code/grafana-dashboard.json`

| # | Hint | Impact |
|---|------|--------|
| 1 | The "Error Rate" panel uses `http_requests_total{status=~"5.."}` without `rate()` -- shows cumulative count instead of rate | Panel shows ever-increasing number (millions) instead of percentage; useless for monitoring |
| 2 | The "Orders per Minute" panel divides by 60 instead of multiplying -- shows orders per second divided by 60 | Shows 0.02 instead of 142 orders/min; misleading dashboard |
| 3 | The "P99 Latency" panel uses `avg()` instead of `histogram_quantile(0.99, ...)` -- shows average instead of 99th percentile | Average hides outliers; p99 could be 5x higher than average but dashboard looks fine |

### Verification
- Error Rate panel shows a percentage (e.g., 0.3%)
- Orders per Minute shows a reasonable number (e.g., 50-200)
- P99 Latency panel shows 99th percentile (higher than average)

---

## Lab 3: Fix Alert Rules (3 bugs)

### File: `starter-code/alerts.yml`

| # | Hint | Impact |
|---|------|--------|
| 1 | The HighErrorRate alert threshold is `> 0.001` (0.1%) instead of `> 0.01` (1%) | Alert fires on normal error rates; team gets paged for non-issues (alert fatigue) |
| 2 | The HighLatency alert has `for: 0m` (fires immediately on any spike) instead of `for: 5m` | Single slow request triggers alert; no buffering for transient spikes |
| 3 | The HighCPU alert uses `> 50` (50%) as threshold | CPU at 60% is normal under load; fires constantly during lunch rush, team ignores all alerts |

### Verification
- Alerts do not fire during normal operation
- HighErrorRate only fires when error rate exceeds 1% for 5 minutes
- HighLatency only fires when p99 > 1s for 5 minutes
- HighCPU fires at 90% threshold (meaningful saturation)

---

## Bonus Challenges

1. **Write a PromQL query** that calculates the request rate per service and displays it in a Grafana table
2. **Create an Alertmanager config** that routes critical alerts to PagerDuty and warnings to Slack
3. **Design a runbook** for the "HighErrorRate" alert: what steps should the on-call engineer follow?
4. **Add a business metric** panel showing revenue per minute based on `payment_amount_total`

---

## Summary

| Lab | Files | Bugs | Focus Area |
|-----|-------|------|------------|
| 1 | prometheus.yml | 3 | Scrape targets, metrics path, job config |
| 2 | grafana-dashboard.json | 3 | PromQL queries, rate vs count, percentiles |
| 3 | alerts.yml | 3 | Thresholds, `for` duration, meaningful alerts |
| **Total** | **3 files** | **9 bugs** | |
