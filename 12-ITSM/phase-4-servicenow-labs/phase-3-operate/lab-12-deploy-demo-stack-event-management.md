# Lab 07A: End-to-End Incident Demo — UPI Services to ServiceNow

**Level:** Intermediate | **Duration:** 60 minutes | **Prerequisites:** Lab 07 completed, Docker installed

---

## Objective

Experience a **real-world ITSM workflow** end to end:
- Run UPI microservices (Spring Boot) with live traffic
- Monitor with Prometheus + Grafana
- Inject failures (chaos engineering)
- Watch alerts auto-create incidents in ServiceNow
- Manage the incident lifecycle in ServiceNow
- Resolve the incident, confirm alert recovery

This demo stack is reused in later labs (Problem Management, Change Management, Reporting).

---

## Architecture

```
                                    ┌─────────────────────┐
                                    │    ServiceNow PDI    │
                                    │  (Incident created)  │
                                    └──────────▲──────────┘
                                               │ REST API
                                    ┌──────────┴──────────┐
                                    │    Snow Bridge       │
                                    │  (Webhook → SNOW)    │
                                    └──────────▲──────────┘
                                               │ webhook
                                    ┌──────────┴──────────┐
                                    │    AlertManager      │
                                    │  (Route alerts)      │
                                    └──────────▲──────────┘
                                               │ alert rules
┌──────────────┐  scrape   ┌───────┴───────────────────┐
│  Grafana     │◄──────────│      Prometheus           │
│  Dashboard   │           │  (Scrape + Evaluate)      │
└──────────────┘           └───┬───────────────────┬───┘
                               │ /actuator/prometheus│
                    ┌──────────┴──────┐  ┌─────────┴────────┐
                    │ UPI Transaction  │  │ UPI Settlement    │
                    │ Service (8081)   │◄─│ Service (8082)    │
                    │ Spring Boot      │  │ Spring Boot       │
                    └──────────▲──────┘  └──────────────────┘
                               │
                    ┌──────────┴──────┐
                    │ Traffic          │
                    │ Generator        │
                    └─────────────────┘
```

### Services

| Service | Port | Tech | Purpose |
|---|---|---|---|
| UPI Transaction Service | 8081 | Spring Boot 3.2 | Processes UPI payments (pay, status) |
| UPI Settlement Service | 8082 | Spring Boot 3.2 | NPCI settlement & reconciliation |
| Snow Bridge | 5005 | Python/Flask | AlertManager webhook → ServiceNow incident |
| Prometheus | 9090 | Prometheus | Metrics scraping + alert evaluation |
| AlertManager | 9093 | AlertManager | Alert routing → Snow Bridge |
| Grafana | 3000 | Grafana | Dashboards (auto-provisioned) |
| Traffic Generator | - | Python | Continuous UPI payment/settlement traffic |

---

## Part 1: Setup

### Step 1.1: Configure ServiceNow Connection

```bash
cd demo-e2e-incident
cp .env.example .env
```

Edit `.env` with your PDI details:
```
SNOW_INSTANCE=https://devXXXXXX.service-now.com
SNOW_USER=admin
SNOW_PASSWORD=your_password
SNOW_ENABLED=true
TRAFFIC_RPS=2
```

> **Tip:** Set `SNOW_ENABLED=false` first for a dry run — incidents will be logged but not created in ServiceNow. Switch to `true` when ready.

### Step 1.2: Build and Start

```bash
docker compose up --build -d
```

First build takes 3-5 minutes (Maven downloads dependencies). Subsequent starts are fast.

### Step 1.3: Verify Everything is Running

```bash
docker compose ps
```

Expected: all 7 containers running and healthy.

```bash
# Test UPI Transaction Service
curl http://localhost:8081/actuator/health

# Test UPI Settlement Service
curl http://localhost:8082/actuator/health

# Test Snow Bridge
curl http://localhost:5005/health

# Test a UPI payment
curl -X POST http://localhost:8081/api/upi/pay \
  -H "Content-Type: application/json" \
  -d '{"payerVpa":"rahul@okaxis","payeeVpa":"swiggy@hdfcbank","amount":450.00,"remarks":"Food order"}'
```

### Step 1.4: Open Dashboards

| Tool | URL | Credentials |
|---|---|---|
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | - |
| AlertManager | http://localhost:9093 | - |

In Grafana, navigate to **Dashboards > UPI Monitoring > UPI Services - Operations Dashboard**.

You should see live traffic flowing — green lines for successful transactions.

---

## Part 2: Observe Normal Operations (5 minutes)

### Step 2.1: Watch the Grafana Dashboard

With traffic flowing, observe:
- **Service Health**: Both services show "UP" (green)
- **UPI Transactions/sec**: Steady ~2 req/s, all green (success)
- **Transaction Failure Rate**: Gauge at 0% (green)
- **P95 Latency**: Under 1 second
- **Settlement Status**: Steady settled rate
- **Total Amount Processed**: Counter increasing

### Step 2.2: Check Prometheus Targets

1. Open http://localhost:9090/targets
2. Both UPI services should show **UP** (green)

### Step 2.3: Check Prometheus Alerts

1. Open http://localhost:9090/alerts
2. All alerts should show **Inactive** (green) — no problems detected

**This is your "normal state" baseline.**

---

## Part 3: Inject Chaos — Trigger Incidents

### Step 3.1: Start the Chaos Script

Open a new terminal:

```bash
cd demo-e2e-incident
./chaos/inject.sh
```

This gives you an interactive menu to break and fix things.

### Step 3.2: Scenario A — High Error Rate (P1 Critical)

1. In the chaos script, choose **1** (Enable 80% failure rate)
2. Watch Grafana:
   - **Failure Rate gauge** climbs from 0% to ~80% (turns red)
   - **Transactions/sec** chart shows red (failed) bars dominating
   - **Settlement failures** start appearing
3. After ~60 seconds:
   - Prometheus detects `UpiHighTransactionFailureRate` alert fires
   - AlertManager routes to Snow Bridge
   - **Snow Bridge creates a P1 incident in ServiceNow**

4. Check the Snow Bridge logs:
   ```bash
   docker compose logs snow-bridge --tail=20
   ```
   You should see: `Incident created in ServiceNow: INC00XXXXX`

5. **Go to ServiceNow** → Incident > All → find the auto-created incident
   - Short description: `[AUTO] UPI transaction failure rate above 50%`
   - Priority: **1 - Critical** (Impact: High, Urgency: High)
   - Category: Software
   - Assignment group: Platform Engineering
   - Description: Contains alert details, current failure rate, runbook

### Step 3.3: Manage the Incident in ServiceNow (Lifecycle)

Now do what you learned in Lab 07:

1. **Assign** the incident to Ravi Kumar (Platform Engineering)
2. Change state to **In Progress**
3. Add work note: "Investigating high failure rate on UPI Transaction Service. Checking chaos/config status."
4. Add work note: "Root cause identified — configuration issue causing 80% payment rejections. Applying fix."

### Step 3.4: Fix the Issue

1. In the chaos script, choose **4** (Disable all chaos)
2. Watch Grafana:
   - Failure rate drops back to 0%
   - Success rate recovers
   - Alerts auto-resolve in ~2 minutes

3. Check Snow Bridge logs — it adds a resolution note to the incident

4. **Back in ServiceNow:**
   - Add work note: "Fix applied. Transaction success rate restored to 100%. Monitoring for stability."
   - Change state to **Resolved**
   - Resolution code: Solved (Permanently)
   - Resolution notes: "Payment service configuration was causing transaction rejections. Configuration corrected. All UPI payments processing normally."

### Step 3.5: Scenario B — Service Down (P1 Critical)

1. Choose **3** in chaos script (Take service DOWN)
2. Watch Grafana — Service Health goes RED
3. Prometheus fires `UpiTransactionServiceDown` alert
4. New P1 incident auto-created in ServiceNow
5. Fix with option **4**, resolve the incident

### Step 3.6: Scenario C — High Latency (P2 Warning)

1. Choose **2** in chaos script (Inject 5s latency)
2. Watch Grafana — P95 latency spikes above 3s threshold
3. Prometheus fires `UpiHighTransactionLatency` alert
4. P3 incident created in ServiceNow (Impact: Medium, Urgency: Medium)
5. Fix with option **4**, resolve

---

## Part 4: Key Metrics for Incident Creation

These are the metrics that trigger ServiceNow incidents:

| Metric | Alert | Threshold | Priority |
|---|---|---|---|
| `up{job="upi-transaction-service"}` | UpiTransactionServiceDown | == 0 for 30s | P1 Critical |
| `upi_transactions_total{status="failed"}` | UpiHighTransactionFailureRate | > 50% for 1m | P1 Critical |
| `upi_transaction_duration_seconds` (p95) | UpiHighTransactionLatency | > 3s for 1m | P3 Moderate |
| `upi_settlements_total{status="failed"}` | UpiSettlementFailures | > 0.1/s for 1m | P3 Moderate |
| `http_server_requests_seconds_count{status=~"5.."}` | UpiHighHttpErrorRate | > 30% for 1m | P3 Moderate |
| `jvm_memory_used_bytes{area="heap"}` | UpiJvmHeapHigh | > 85% for 2m | P3 Moderate |

### Alert → Incident Mapping

| Alert Severity | ServiceNow Impact | ServiceNow Urgency | Resulting Priority |
|---|---|---|---|
| critical | 1 - High | 1 - High | P1 Critical |
| warning | 2 - Medium | 2 - Medium | P3 Moderate |
| info | 3 - Low | 3 - Low | P5 Planning |

---

## Part 5: Useful Prometheus Queries

Open http://localhost:9090 and try these:

```promql
# Transaction success rate (should be 100% normally)
rate(upi_transactions_total{status="success"}[2m])
/ (rate(upi_transactions_total{status="success"}[2m]) + rate(upi_transactions_total{status="failed"}[2m]))

# P95 transaction latency
histogram_quantile(0.95, rate(upi_transaction_duration_seconds_bucket[2m]))

# Total amount processed
upi_transaction_amount_total

# Settlement failure rate
rate(upi_settlements_total{status="failed"}[2m])

# JVM heap usage percentage
jvm_memory_used_bytes{area="heap"} / jvm_memory_max_bytes{area="heap"}

# HTTP 5xx error rate by service
rate(http_server_requests_seconds_count{status=~"5.."}[2m])
```

---

## Part 6: Cleanup

### Stop the stack (preserves data)
```bash
docker compose stop
```

### Start again later
```bash
docker compose start
```

### Full cleanup (remove containers, images, volumes)
```bash
docker compose down --rmi local -v
```

---

## How This Demo Connects to Future Labs

| Future Lab | How This Demo is Used |
|---|---|
| **Lab 08: Problem Management** | Create a problem from the recurring UPI failure incidents |
| **Lab 09: Change Management** | Submit a change request to fix the root cause (e.g., deploy a patch) |
| **Lab 10: Knowledge Management** | Write a KB article documenting the UPI failure resolution |
| **Lab 11: SLA Management** | Track SLA compliance on the P1 UPI incidents |
| **Lab 12: Reporting & Dashboards** | Build ServiceNow dashboards from the incident data |
| **Lab 13: Service Catalog** | Create a catalog item for "Request UPI Service Health Check" |

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Deployed UPI microservices | Real services = realistic incidents |
| Monitoring with Prometheus + Grafana | Industry-standard observability stack |
| Alert → Incident automation | Reduces MTTD (Mean Time to Detect) |
| Chaos injection → incident creation | Simulates real production failures |
| Full incident lifecycle in ServiceNow | End-to-end ITSM workflow |
| Resolved incident + alert recovery | Closed-loop incident management |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Observability** | Ability to understand system state from external outputs (metrics, logs, traces) |
| **Prometheus** | Open-source metrics collection and alerting toolkit |
| **AlertManager** | Handles alert deduplication, grouping, routing, and silencing |
| **Webhook** | HTTP callback that delivers real-time notifications |
| **Chaos Engineering** | Deliberately injecting failures to test system resilience |
| **MTTD** | Mean Time to Detect — how fast you identify an incident |
| **MTTR** | Mean Time to Resolve — how fast you fix an incident |
| **Closed-loop** | Alert fires → incident created → fixed → alert resolves → incident closed |

---

## Quick Reference

```bash
# Start everything
docker compose up --build -d

# Watch logs
docker compose logs -f

# Run chaos script
./chaos/inject.sh

# Manual UPI payment
curl -X POST http://localhost:8081/api/upi/pay \
  -H "Content-Type: application/json" \
  -d '{"payerVpa":"user@okaxis","payeeVpa":"merchant@hdfcbank","amount":500,"remarks":"Test"}'

# Check active alerts → incidents
curl http://localhost:5005/active-alerts

# Create test incident manually
curl -X POST http://localhost:5005/test-incident \
  -H "Content-Type: application/json" \
  -d '{"severity":"critical","summary":"UPI Gateway Down - Manual Test"}'

# URLs
# Grafana:      http://localhost:3000  (admin/admin)
# Prometheus:   http://localhost:9090
# AlertManager: http://localhost:9093
```
