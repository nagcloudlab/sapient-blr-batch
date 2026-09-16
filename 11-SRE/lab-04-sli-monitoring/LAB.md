# Lab 04: SLI-Based Monitoring & Alerting

## Objective

Build a Grafana dashboard that tracks SLIs in real-time, configure SLO-based
alerts, and understand multi-window burn rate alerting.

**Prerequisite:** Services running (`cd ../services && docker compose up -d`)

---

## Concepts

### Traditional Monitoring vs SLI-Based Monitoring

```
Traditional (BAD for SRE):          SLI-Based (GOOD for SRE):
─────────────────────────           ────────────────────────
Alert: CPU > 80%                    Alert: Availability SLI < 99.9%
Alert: Memory > 90%                 Alert: Latency p99 > 500ms
Alert: Disk > 85%                   Alert: Error budget burn rate > 1x

Problem: CPU can be 80%             Measures what USERS experience.
but users are fine.                 Alerts only when users are affected.
Too many false alerts.              Fewer, more meaningful alerts.
```

---

## Part 1: Create an SLI Dashboard in Grafana

A pre-built SRE dashboard is already provisioned at `services/grafana/dashboards/sre-dashboard.json`.
Open it in Grafana or build your own from scratch using the steps below.

Open Grafana: http://localhost:3001 (admin/admin)

### Step 1: Create a new dashboard

1. Click "+" > "New Dashboard" > "Add visualization"
2. Select "Prometheus" as data source

### Step 2: Add Availability SLI Panel

Create a **Gauge** panel with this query:

```promql
# Availability SLI: % of non-5xx responses
sum(rate(http_request_duration_seconds_count{status_code!~"5.."}[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))
* 100
```

Panel settings:
- Title: "Order Service - Availability SLI"
- Unit: Percent (0-100)
- Thresholds: Green > 99.9, Yellow > 99.0, Red < 99.0
- Min: 95, Max: 100

### Step 3: Add Latency SLI Panel

Create a **Gauge** panel:

```promql
# Latency SLI: % of requests under 500ms
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))
* 100
```

Panel settings:
- Title: "Order Service - Latency SLI (< 500ms)"
- Unit: Percent (0-100)
- Thresholds: Green > 95, Yellow > 90, Red < 90

### Step 4: Add Error Budget Remaining Panel

Create a **Stat** panel:

```promql
# Error budget remaining (assuming 99.9% SLO, 30-day window)
# Simplified: shows current budget consumption rate
(1 - (
  sum(rate(http_request_duration_seconds_count{status_code=~"5.."}[1h]))
  /
  sum(rate(http_request_duration_seconds_count[1h]))
)) * 100
```

Panel settings:
- Title: "Current Reliability (Target: 99.9%)"
- Unit: Percent (0-100)

### Step 5: Add Request Rate Timeline

Create a **Time series** panel:

```promql
# Successful vs failed requests over time
sum(rate(http_request_duration_seconds_count{status_code!~"5.."}[1m])) # Legend: Successful
sum(rate(http_request_duration_seconds_count{status_code=~"5.."}[1m]))  # Legend: Failed
```

Panel settings:
- Title: "Request Rate (Success vs Error)"
- Colors: Green for successful, Red for failed

### Step 6: Add Latency Percentiles

Create a **Time series** panel:

```promql
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))  # p50
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))  # p95
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))  # p99
```

Panel settings:
- Title: "Latency Percentiles (p50 / p95 / p99)"
- Unit: seconds

---

## Part 2: Generate Traffic and Observe

Run the load generator and watch the dashboard:

```bash
# Use the provided load generator
cd ../services
./generate-load.sh 200 0.2

# Or run it continuously
CONTINUOUS=1 ./generate-load.sh
```

While traffic flows, observe on the dashboard:
1. What is the availability SLI showing?
2. What is the latency distribution (p50 vs p99)?
3. Are you meeting the 99.9% SLO?

---

## Part 3: Configure SLO-Based Alerts

### Why Not Just Alert on Every Error?

```
Scenario: SLO = 99.9% (43.2 min budget/month)

Bad Alert: "Alert if any 5xx error occurs"
  -> You'll get paged 50 times a day for normal error rates
  -> Alert fatigue -> team ignores alerts -> miss real outages

Good Alert: "Alert if error budget burn rate exceeds 2x"
  -> Only fires when you're burning budget faster than sustainable
  -> Meaningful, actionable alerts
```

### Burn Rate Alerting

```
Burn rate = actual consumption rate / ideal consumption rate

Ideal: budget burns evenly over 30 days = 1x burn rate
2x:    budget will exhaust in 15 days
10x:   budget will exhaust in 3 days
14.4x: budget will exhaust in 2 days (severe!)

Alert Windows:
  - 5m window at 14.4x burn rate  -> SEV-1 (page immediately)
  - 1h window at 6x burn rate     -> SEV-2 (urgent ticket)
  - 6h window at 2x burn rate     -> SEV-3 (warning, review needed)
```

### Step 1: Create Alert Rule in Grafana

1. Go to Alerting > Alert rules > New alert rule
2. Name: "Order Service SLO Breach"
3. Query:

```promql
# Error rate over 5 minutes
(
  sum(rate(http_request_duration_seconds_count{status_code=~"5.."}[5m]))
  /
  sum(rate(http_request_duration_seconds_count[5m]))
) > 0.001
```

This alerts when error rate exceeds 0.1% (which would breach a 99.9% SLO).

4. Set evaluation interval: every 1 minute
5. Set "for" duration: 2 minutes (must be sustained, not a blip)

### Step 2: Create a Latency Alert

```promql
# Alert when p99 latency exceeds 1 second for 5 minutes
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1.0
```

---

## Part 4: Discussion -- Alerting Best Practices

### The Alerting Triangle

```
                 URGENT + IMPORTANT
                 (Page the on-call)
                       /\
                      /  \
                     / S1 \
                    /      \
                   /--------\
                  /   S2     \
                 / (Ticket)   \
                /--------------\
               /      S3        \
              / (Review next day) \
             /--------------------\
            /    INFORMATIONAL      \
           / (Dashboard only, no     \
          /   notification needed)    \
         /--------------------------\
```

### Questions for the Class

1. Should you alert when CPU is high but SLIs are fine?
2. What's the danger of too many alerts? (Alert fatigue)
3. Why use multiple time windows for burn rate alerts?
4. Who should get paged at 2 AM? Only for what severity?

---

## Key Takeaways

1. Monitor **SLIs** (user experience), not just infrastructure metrics
2. Alert on **SLO breaches**, not every individual error
3. Use **burn rate** to predict when you'll exhaust the error budget
4. **Multi-window alerts** catch both sudden spikes and slow degradation
5. Every alert should be **actionable** -- if you can't do anything about it, don't alert

> **Next:** Lab 05 -- When an alert fires, what happens next? Incident Response.
