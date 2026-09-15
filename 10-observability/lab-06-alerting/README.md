# Lab 06: Prometheus Alerting
## 30 min | Prerequisite: Lab 03 (Prometheus running)

---

## What You'll Learn
- How to write Prometheus alert rules
- Alert lifecycle: Inactive -> Pending -> Firing
- The `for` duration and why it matters
- Severity levels: critical, warning, info
- What alert fatigue is and how to avoid it

## Why This Matters
Dashboards are great, but nobody stares at them 24/7. Alerts NOTIFY you when something is wrong -- they're the safety net that wakes the on-call engineer at 2 AM. But bad alerts (too many, too sensitive) cause "alert fatigue" -- the team ignores ALL alerts, including real ones. Getting alerting right is critical.

## New Terms

| Term | Meaning |
|------|---------|
| **Alert rule** | A PromQL condition that, when true for a specified duration, triggers a notification. Example: "if error rate > 1% for 5 minutes, fire an alert." |
| **`for` duration** | How long the condition must be TRUE before the alert actually fires. Filters out transient spikes. `for: 5m` means "only alert if this has been bad for 5 straight minutes." |
| **Severity** | Priority level of an alert. Determines who gets notified and how urgently. |
| **Alert fatigue** | When a team receives so many false/noisy alerts that they start ignoring ALL alerts -- including real incidents. The #1 reason production outages get missed. |
| **AlertManager** | A separate component that receives alerts from Prometheus and routes them: critical -> PagerDuty (phone call), warning -> Slack, info -> email. |
| **Runbook** | A step-by-step document that tells the on-call engineer exactly what to do when a specific alert fires. "If HighErrorRate fires, check these things in this order." |
| **False positive** | An alert that fires when there's no real problem. Example: CPU spike for 2 seconds during a batch job triggers HighCPU alert. |
| **Error budget** | The amount of "allowed" downtime or errors within your SLO. If your SLO is 99.9% uptime, your error budget is 0.1% = ~43 minutes/month. (Covered more in SRE module.) |

---

## Alert Rule Anatomy

```yaml
- alert: HighErrorRate              # NAME: what is this alert about?
  expr: >                           # EXPR: PromQL condition (when should it fire?)
    rate(http_requests_total{status="500"}[5m])
    / rate(http_requests_total[5m]) > 0.01
  for: 5m                          # FOR: how long must it be true before firing?
  labels:
    severity: critical              # SEVERITY: who gets notified?
  annotations:
    summary: "Error rate > 1%"      # SUMMARY: human-readable message
```

### Alert States

```
INACTIVE ----[condition becomes true]----> PENDING ----[for duration elapsed]----> FIRING
    ^                                         |                                      |
    +------[condition becomes false]----------+--------[condition becomes false]------+
```

| State | Color | What it means |
|-------|-------|---------------|
| **Inactive** | Green | Condition is false -- everything is fine |
| **Pending** | Yellow | Condition just became true, timer started, waiting for `for` to elapse |
| **Firing** | Red | Condition has been true for the entire `for` duration -- notification sent! |

> **Quick Question:** Why does the Pending state exist? Why not fire immediately when the condition becomes true?
>
> (Because transient spikes happen all the time. A 1-second CPU spike shouldn't wake someone up at 3 AM. The `for` duration filters these out.)

---

## Severity Levels

| Severity | What it means | How you're notified | Example |
|----------|--------------|---------------------|---------|
| **critical** | Users are affected RIGHT NOW, needs immediate action | PagerDuty (phone call / SMS) | Error rate > 5%, service completely down |
| **warning** | Something is degraded, investigate during business hours | Slack message | P99 latency > 1 second, CPU > 90% |
| **info** | FYI, no action needed right now | Email / dashboard | Disk 70% full (still have time) |

> **The rule for every alert:** "If this fires at 3 AM, is there something I need to DO right now?" If yes -> critical. If it can wait until morning -> warning. If nobody needs to act -> info or delete the alert.

---

## Step 1: Create alert rules

Copy `alerts.yml` from this folder, or create it:

```yaml
groups:
  - name: foodexpress
    rules:
      # Golden Signal: ERRORS
      - alert: HighErrorRate
        expr: >
          rate(http_requests_total{status="500"}[5m])
          / rate(http_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.job }}"

      # Golden Signal: LATENCY
      - alert: HighLatency
        expr: >
          histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency > 1s on {{ $labels.job }}"

      # Health: SERVICE DOWN
      - alert: ServiceDown
        expr: up{job="order-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "{{ $labels.job }} is DOWN"
```

> **Why these thresholds?**
> - Error rate > 1% for 5 min = real problem, not a blip
> - P99 > 1 second for 5 min = consistently slow for the worst 1% of users
> - Service down for 1 min = not a brief restart, it's genuinely unreachable

---

## Step 2: Update Prometheus config

Add `rule_files` to `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s    # Evaluate alert rules every 15 seconds

rule_files:
  - "alerts.yml"              # Load our alert rules

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'order-service'
    scrape_interval: 10s
    static_configs:
      - targets: ['host.docker.internal:8080']
```

---

## Step 3: Restart Prometheus with alert rules

```bash
docker stop prometheus && docker rm prometheus
docker run -d --name prometheus -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v $(pwd)/alerts.yml:/etc/prometheus/alerts.yml \
  prom/prometheus
```

---

## Step 4: View alerts in Prometheus

Open `http://<IP>:9090/alerts`

You should see 3 alert rules:
- **HighErrorRate** -- likely **FIRING** (our app has ~10% error rate, way above the 1% threshold)
- **HighLatency** -- **PENDING** or FIRING
- **ServiceDown** -- **INACTIVE** (green -- service is up)

> **Think About It:** HighErrorRate is FIRING because our simulated app has ~10% error rate. In production, you'd see this alert and immediately investigate. The alert links to the dashboard (Lab 04), and the dashboard leads you to logs (Lab 05) for details.

---

## Step 5: Trigger the ServiceDown alert (incident simulation!)

```bash
docker stop order-service
```

Watch `http://<IP>:9090/alerts`:
1. **ServiceDown** goes from Inactive -> **Pending** (condition just became true)
2. After 1 minute: Pending -> **FIRING** (condition has been true for `for: 1m`)

Recover:
```bash
docker start order-service
```

ServiceDown returns to **Inactive** after the next scrape.

> **Discussion:** What just happened is exactly what happens in production when a pod crashes. Prometheus detects it within seconds, alert fires after the `for` duration, on-call gets paged. The whole detection loop took ~1 minute.

---

## Step 6: Exercise -- Fix bad alert rules

These 3 rules have real problems found in production. What's wrong with each?

```yaml
# Rule 1
- alert: AnyError
  expr: http_requests_total{status="500"} > 0
  for: 0m
  labels:
    severity: critical

# Rule 2
- alert: SlowRequests
  expr: avg(http_request_duration_seconds_sum / http_request_duration_seconds_count) > 0.5
  for: 1m
  labels:
    severity: critical

# Rule 3
- alert: HighCPU
  expr: 100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 50
  for: 10m
  labels:
    severity: critical
```

> **Hint for each:** Rule 1 has 3 problems. Rule 2 uses the wrong function for latency. Rule 3's threshold is wrong for real-world workloads.

<details>
<summary>Answers</summary>

**Rule 1 -- Three problems:**
1. Uses raw counter (`http_requests_total > 0`) instead of `rate()` -- fires if there's EVER been a single error, even from weeks ago
2. `for: 0m` -- fires instantly on any transient spike
3. Every error is "critical" -- single 500 error pages someone at 3 AM
- **Fix:** `rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m]) > 0.01`, `for: 5m`

**Rule 2 -- Average hides outliers:**
- `avg()` of [100ms, 100ms, 100ms, 5000ms] = 1325ms -- looks bad
- But `avg()` of [100ms x 99, 5000ms x 1] = 149ms -- looks fine, but 1 user waited 5 seconds!
- **Fix:** Use `histogram_quantile(0.99, rate(bucket[5m])) > 1.0` for real p99

**Rule 3 -- Threshold too low:**
- CPU at 50-60% is NORMAL under load (lunch rush, batch jobs, deployments)
- This alert fires every day at noon, team ignores it, then misses real 95% CPU saturation
- Not everything is "critical" -- CPU high is a warning
- **Fix:** Threshold `90`, severity `warning`

</details>

---

## Alert Design Best Practices

| Principle | Bad | Good |
|-----------|-----|------|
| **Alert on symptoms, not causes** | "CPU > 90%" (cause) | "Error rate > 1%" (symptom users feel) |
| **Use `for` duration** | `for: 0m` (any blip pages you) | `for: 5m` (sustained problem only) |
| **Meaningful thresholds** | CPU > 50% (normal under load) | CPU > 90% for 10 min (real saturation) |
| **Right severity** | Everything is critical | Critical = wake up, Warning = morning, Info = FYI |
| **Actionable** | "Something is wrong" | "Error rate 5% on payment-service, see runbook" |

---

## Discussion

1. Why is `for: 0m` dangerous in production? (Every transient spike pages someone -- could be 50 false alerts per night)
2. Our app has ~10% error rate. Should we set the threshold to 10%? (No -- the threshold should be what's ACCEPTABLE, like 1%, not what's "current." You want to know when things are BAD, not when they're worse than usual.)
3. If a team gets 200 alerts per day, what happens? (Alert fatigue -- they start ignoring all alerts. When a REAL outage happens, nobody notices.)

---

## What's Next

You've been running services, Prometheus, and Grafana as separate containers with individual `docker run` commands. In Lab 07, you'll use **Docker Compose** to run the entire observability stack with one command -- the way real projects are organized.
