# Lab 04 - Alerting with Prometheus Alertmanager

## What You Will Learn

- How Prometheus alert rules work (expr + for + labels + annotations)
- How Alertmanager routes alerts to the right channels
- How to create alerts for all 4 Golden Signals (Latency, Traffic, Errors, Saturation)
- How alert grouping, inhibition, and silencing work
- How to test alerts by triggering real failure scenarios
- How to visualize alert state in Prometheus and Grafana

## Architecture

```
  +-------------------+         +-------------------+
  |  Order Service    |  HTTP   | Payment Service   |
  |  (Node.js)        +-------->+  (Spring Boot)    |
  |  port 3000        |         |  port 8080        |
  +--------+----------+         +--------+----------+
           |                             |
           | scrapes /metrics            | scrapes /actuator/prometheus
           v                             v
  +------------------------------------------------+
  |              Prometheus                         |
  |              port 9090                          |
  |                                                 |
  |  1. Scrapes metrics every 15s                   |
  |  2. Evaluates alert RULES every 15s             |
  |  3. If rule matches for 'for' duration:         |
  |     -> sends alert to Alertmanager              |
  +------------------------+-----------------------+
                           |
                           | fires alerts
                           v
                  +-------------------+
                  |  Alertmanager     |
                  |  port 9093        |
                  |                   |
                  |  1. Groups alerts |
                  |  2. Routes by     |
                  |     severity      |
                  |  3. Sends to      |
                  |     receivers     |
                  +--------+----------+
                           |
              +------------+------------+
              |            |            |
              v            v            v
        +---------+  +---------+  +---------+
        | Webhook |  | Slack   |  | Email   |
        | Logger  |  | (opt)   |  | (opt)   |
        | :9095   |  |         |  |         |
        +---------+  +---------+  +---------+
              |
              v
        +---------+
        | Web UI  |  <-- see alerts at http://localhost:9095
        +---------+
```

## Alert Rule Anatomy

```yaml
- alert: HighPaymentFailureRate        # Alert name
  expr: >                               # PromQL expression
    rate(payments_failed_total[2m])
    / rate(payments_completed_total[2m])
    > 0.15
  for: 1m                               # Must be true for this long
  labels:                                # Metadata for routing
    severity: critical
    service: payment-service
  annotations:                           # Human-readable info
    summary: "High payment failure rate"
    description: "Failure rate is {{ $value | humanizePercentage }}"
```

```
How it works:

  Time 0:00  expr evaluates to true     -> state: PENDING
  Time 0:15  expr still true            -> state: PENDING
  Time 0:30  expr still true            -> state: PENDING
  Time 0:45  expr still true            -> state: PENDING
  Time 1:00  true for > 1m (for: 1m)    -> state: FIRING -> send to Alertmanager!

  If expr becomes false before 'for' duration:
  Time 0:00  expr true                  -> state: PENDING
  Time 0:15  expr true                  -> state: PENDING
  Time 0:30  expr FALSE                 -> state: INACTIVE (reset!)

  The 'for' clause prevents flapping (brief spikes don't trigger alerts)
```

## Alert Rules in This Lab (Mapped to Golden Signals)

### Golden Signal: ERRORS

```yaml
# Alert when > 15% of payments fail
- alert: HighPaymentFailureRate
  expr: (failed + errors) / total > 0.15
  for: 1m
  severity: critical

# Alert when order service gets errors calling payment service
- alert: PaymentServiceErrors
  expr: rate(payment_service_errors_total[2m]) > 0.05
  for: 1m
  severity: warning
```

### Golden Signal: LATENCY

```yaml
# Alert when p95 order latency > 1 second
- alert: HighOrderLatencyP95
  expr: histogram_quantile(0.95, rate(...bucket[2m])) > 1.0
  for: 1m
  severity: warning

# Alert when p95 payment call latency > 2 seconds
- alert: HighPaymentCallLatencyP95
  expr: histogram_quantile(0.95, rate(...bucket[2m])) > 2.0
  for: 1m
  severity: critical
```

### Golden Signal: TRAFFIC

```yaml
# Alert when no orders received for 5 minutes
- alert: NoTraffic
  expr: rate(orders_count[5m]) == 0
  for: 5m
  severity: warning
```

### Golden Signal: SATURATION

```yaml
# Alert when Node.js memory > 256MB
- alert: HighMemoryUsage
  expr: process_resident_memory_bytes > 256MB
  for: 2m
  severity: warning

# Alert when JVM heap usage > 80%
- alert: HighJvmHeapUsage
  expr: jvm_heap_used / jvm_heap_max > 0.80
  for: 2m
  severity: warning
```

### Service Health

```yaml
# Alert when Prometheus can't scrape a service
- alert: ServiceDown
  expr: up == 0
  for: 30s
  severity: critical
```

## Alertmanager Routing

```
                    All Alerts
                        |
                   group_by: [alertname, service]
                   group_wait: 10s
                        |
               +--------+--------+
               |                 |
          severity:          severity:
          critical           warning
               |                 |
               v                 v
       +---------------+  +---------------+
       | critical-alerts|  | warning-alerts|
       | (webhook +     |  | (webhook)    |
       |  Slack/PD)     |  |              |
       +---------------+  +---------------+

  group_wait:      Wait 10s to batch alerts of same group
  group_interval:  After first notification, wait 30s before sending updates
  repeat_interval: Re-send same alert every 5m if still firing
```

## How To Run

```bash
sudo docker compose up --build -d

# Check all 6 containers
sudo docker compose ps

# Wait for services
curl http://localhost:3000/health
curl http://localhost:8080/health
```

## How To Test

### Step 1: Check Alert Rules in Prometheus (localhost:9090)

- Go to **Status > Rules** — see all defined alert rules
- Go to **Alerts** — see current alert states (inactive/pending/firing)
- Initially "NoTraffic" will go to PENDING (no orders yet)

### Step 2: Generate Normal Traffic

```bash
chmod +x generate-load.sh
./generate-load.sh 30 0.3
```

- Check Prometheus Alerts page — "NoTraffic" should go back to INACTIVE
- Some alerts may fire due to payment failures

### Step 3: Check Alert Webhook Logger (localhost:9095)

- Open `http://localhost:9095` in browser
- See fired/resolved alerts with severity, service, description
- Auto-refreshes every 5 seconds

### Step 4: Trigger Specific Alerts

```bash
# Trigger ServiceDown alert (stop payment service)
sudo docker compose stop payment-service
# Wait ~30 seconds, check Prometheus Alerts -> ServiceDown = FIRING
# Check webhook logger -> critical alert received

# Restart payment service
sudo docker compose start payment-service
# Wait ~30 seconds -> alert RESOLVED
# Check webhook logger -> resolved notification

# Trigger high error rate (send many bad requests)
for i in $(seq 1 50); do
  curl -s -X POST http://localhost:3000/orders \
    -H "Content-Type: application/json" \
    -d '{"item":"x","quantity":1,"price":1}' &
done
wait
# The 25% failure rate should trigger HighPaymentFailureRate
```

### Step 5: View in Alertmanager UI (localhost:9093)

- See active alerts grouped by alertname + service
- Try **Silencing** an alert:
  1. Click an alert
  2. Click "Silence"
  3. Set duration (e.g., 1 hour)
  4. The alert won't notify during silence period

### Step 6: View in Grafana (localhost:3001)

- Go to **Alerting** in left sidebar
- You can also create Grafana-native alerts
- Go to **Explore** > query: `ALERTS{alertstate="firing"}`

## Key Concepts

### Alert States

```
  INACTIVE ──── expr is false, all good
      |
      v  (expr becomes true)
  PENDING ───── expr is true, waiting for 'for' duration
      |
      v  (still true after 'for' duration)
  FIRING ────── alert sent to Alertmanager
      |
      v  (expr becomes false)
  RESOLVED ──── Alertmanager sends "resolved" notification
      |
      v
  INACTIVE ──── back to normal
```

### Alertmanager Features

```
GROUPING:
  Without grouping:
    Alert: HighLatency (order-service)     -> notification 1
    Alert: HighLatency (payment-service)   -> notification 2
    Alert: HighLatency (menu-service)      -> notification 3
    = 3 separate notifications (noisy!)

  With group_by: [alertname]:
    Alert: HighLatency (order, payment, menu)  -> 1 notification
    = 1 grouped notification (clean!)

INHIBITION:
  If ServiceDown is firing, suppress HighLatency for same service
  (service is down, of course latency is bad — no need to alert twice)

SILENCING:
  Maintenance window? Silence alerts for 2 hours
  (manual, via Alertmanager UI)

ROUTING:
  severity: critical  -> PagerDuty (wake someone up)
  severity: warning   -> Slack #alerts channel
  severity: info      -> email digest
```

### Best Practices

```
DO:
  - Alert on symptoms (high error rate) not causes (CPU high)
  - Use 'for' duration to avoid flapping (1-5 minutes)
  - Include runbook links in annotations
  - Route critical alerts to pager, warnings to Slack
  - Test alerts by intentionally causing failures

DON'T:
  - Alert on every metric (alert fatigue)
  - Set thresholds too low (too many false alarms)
  - Skip 'for' clause (every spike triggers alert)
  - Have unactionable alerts (if nobody can fix it, don't alert)
  - Alert on the same issue multiple ways (use inhibition)

RULE OF THUMB:
  If an alert fires and nobody needs to DO anything -> delete it
  If an alert fires too often and is ignored -> fix threshold or delete
```

## File Structure

```
lab-04-alerting/
├── LAB.md
├── docker-compose.yml
├── generate-load.sh
├── order-service/                        # same as lab-01 (with metrics)
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       └── index.js
├── payment-service/                      # same as lab-01 (with metrics)
│   ├── Dockerfile
│   ├── pom.xml
│   └── src/main/...
├── prometheus/
│   ├── prometheus.yml                    # scrape config + alertmanager target
│   └── alerts.yml                        # all alert rules (Golden Signals)
├── alertmanager/
│   └── alertmanager.yml                  # routing rules + receivers
├── webhook-logger/                       # simple Node.js alert receiver
│   ├── Dockerfile
│   ├── server.js                         # catches alerts + shows web UI
└── grafana/
    └── provisioning/
        └── datasources/
            └── datasource.yml
```

## Cleanup

```bash
sudo docker compose down
```
