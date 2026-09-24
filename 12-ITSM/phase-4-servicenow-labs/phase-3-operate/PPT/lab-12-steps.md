# Lab 12: Deploy Demo Stack & Event Management — Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-12-deploy-demo-stack-event-management.md`

---

## Pre-check

- [ ] Labs 01-07 done (CMDB CIs exist: UPI Transaction Service, UPI Settlement Service, etc.)
- [ ] Groups exist: Platform Engineering, NOC, Service Desk
- [ ] Docker and Docker Compose installed on your machine
- [ ] Logged into PDI as admin
- [ ] PDI URL, username, and password ready

---

## Step 1: Configure ServiceNow Connection

Navigate to the demo stack folder:

```bash
cd demo-e2e-incident
```

Copy the environment template:

```bash
cp .env.example .env
```

Edit `.env` with your PDI details:

| Variable | Value |
|----------|-------|
| SNOW_INSTANCE | `https://devXXXXXX.service-now.com` |
| SNOW_USER | `admin` |
| SNOW_PASSWORD | your PDI admin password |
| SNOW_ENABLED | `false` (start with dry run) |
| TRAFFIC_RPS | `2` |

> Tip: Keep `SNOW_ENABLED=false` for the first run. Switch to `true` once services are healthy.

---

## Step 2: Build and Start the Stack

```bash
docker compose up --build -d
```

First build takes 3-5 minutes (Maven downloads dependencies). Wait for completion.

---

## Step 3: Verify All Services Running

```bash
docker compose ps
```

Expected: **7 containers** — all showing `running` and `healthy`.

### Health checks

```bash
# UPI Transaction Service
curl http://localhost:8081/actuator/health

# UPI Settlement Service
curl http://localhost:8082/actuator/health

# Snow Bridge
curl http://localhost:5005/health
```

All should return `{"status":"UP"}` or similar.

### Test a UPI payment

```bash
curl -X POST http://localhost:8081/api/upi/pay \
  -H "Content-Type: application/json" \
  -d '{"payerVpa":"rahul@okaxis","payeeVpa":"swiggy@hdfcbank","amount":450.00,"remarks":"Food order"}'
```

Expected: JSON response with transaction ID and status `SUCCESS`.

---

## Checkpoint

All 7 services up? Health checks passing? Test payment successful? Proceed.

---

## Step 4: Check Prometheus Targets

1. Open http://localhost:9090/targets
2. Verify both UPI services show **UP** (green)
3. Open http://localhost:9090/alerts
4. All alerts should show **Inactive** (green) — this is your baseline

---

## Step 5: View Grafana Dashboard

1. Open http://localhost:3000
2. Login: `admin` / `admin` (skip password change)
3. Navigate: **Dashboards > UPI Monitoring > UPI Services - Operations Dashboard**
4. Observe baseline metrics:

| Panel | Expected Value |
|-------|---------------|
| Service Health | Both services UP (green) |
| UPI Transactions/sec | ~2 req/s, all green |
| Transaction Failure Rate | 0% (green gauge) |
| P95 Latency | Under 1 second |
| Settlement Status | Steady settled rate |
| Total Amount Processed | Counter increasing |

> This is your "normal state" baseline. Take a screenshot for comparison.

---

## Step 6: Enable ServiceNow Integration

1. Edit `.env` — change `SNOW_ENABLED=true`
2. Restart Snow Bridge:

```bash
docker compose restart snow-bridge
```

3. Verify:

```bash
docker compose logs snow-bridge --tail=5
```

Should show: `ServiceNow integration enabled`

---

## Step 7: Inject Chaos — Scenario A (High Error Rate)

Open a new terminal:

```bash
cd demo-e2e-incident
./chaos/inject.sh
```

1. Choose **1** (Enable 80% failure rate)
2. Watch Grafana:
   - Failure Rate gauge climbs to ~80% (turns red)
   - Red bars dominate Transactions/sec chart
3. Wait ~60 seconds — Prometheus fires `UpiHighTransactionFailureRate` alert
4. Check Snow Bridge logs:

```bash
docker compose logs snow-bridge --tail=20
```

Expected: `Incident created in ServiceNow: INC00XXXXX`

---

## Step 8: Verify Incident Auto-Created in ServiceNow

1. Go to ServiceNow PDI > **Incident > All**
2. Find the auto-created incident:

| Field | Expected Value |
|-------|---------------|
| Short description | [AUTO] UPI transaction failure rate above 50% |
| Priority | 1 - Critical |
| Impact | 1 - High |
| Urgency | 1 - High |
| Category | Software |
| Assignment group | Platform Engineering |

3. Open the incident — description should contain alert details and runbook link

---

## Step 9: Manage the Incident Lifecycle

1. **Assign** the incident to Ravi Kumar
2. Change **State** to **In Progress**
3. Add work note: "Investigating high failure rate on UPI Transaction Service."
4. Click **Update**

---

## Step 10: Fix the Issue and Resolve

1. In chaos script, choose **4** (Disable all chaos)
2. Watch Grafana — failure rate drops to 0% within ~30 seconds
3. Alerts auto-resolve in ~2 minutes
4. Check Snow Bridge logs — resolution note added to incident
5. Back in ServiceNow:
   - Add work note: "Fix applied. Success rate restored to 100%."
   - Change **State** to **Resolved**
   - Resolution code: `Solved (Permanently)`
   - Resolution notes: "Payment service configuration corrected. All UPI payments processing normally."
   - Click **Update**

---

## Step 11: Scenario B — Service Down (P1)

1. In chaos script, choose **3** (Take service DOWN)
2. Watch Grafana — Service Health goes RED
3. Prometheus fires `UpiTransactionServiceDown` alert
4. New P1 incident auto-created in ServiceNow
5. Fix with option **4** in chaos script
6. Resolve the incident in ServiceNow

---

## Step 12: Scenario C — High Latency (P3)

1. In chaos script, choose **2** (Inject 5s latency)
2. Watch Grafana — P95 latency spikes above 3s
3. Prometheus fires `UpiHighTransactionLatency` alert
4. P3 incident created in ServiceNow (Impact: Medium, Urgency: Medium)
5. Fix with option **4**, resolve the incident

---

## Step 13: Check Snow Bridge Active Alerts

```bash
curl http://localhost:5005/active-alerts
```

After all chaos disabled, this should return an empty list `[]`.

To create a manual test incident:

```bash
curl -X POST http://localhost:5005/test-incident \
  -H "Content-Type: application/json" \
  -d '{"severity":"critical","summary":"UPI Gateway Down - Manual Test"}'
```

---

## Quick Verification Checklist

- [ ] 7 Docker containers running and healthy
- [ ] Prometheus targets show both UPI services UP
- [ ] Grafana dashboard displays live traffic metrics
- [ ] Chaos injection caused failure rate spike on Grafana
- [ ] P1 incident auto-created in ServiceNow (high error rate)
- [ ] P1 incident auto-created in ServiceNow (service down)
- [ ] P3 incident auto-created in ServiceNow (high latency)
- [ ] At least one incident walked through full lifecycle (New > In Progress > Resolved)
- [ ] Snow Bridge active-alerts endpoint returns empty after fix
- [ ] Alerts auto-resolved in Prometheus after chaos disabled

---

## Alert-to-Incident Mapping Reference

| Alert | Threshold | ServiceNow Priority |
|-------|-----------|-------------------|
| UpiTransactionServiceDown | Service unreachable for 30s | P1 Critical |
| UpiHighTransactionFailureRate | > 50% for 1m | P1 Critical |
| UpiHighTransactionLatency | P95 > 3s for 1m | P3 Moderate |
| UpiSettlementFailures | > 0.1/s for 1m | P3 Moderate |
| UpiHighHttpErrorRate | > 30% 5xx for 1m | P3 Moderate |
| UpiJvmHeapHigh | > 85% heap for 2m | P3 Moderate |

---

## Cleanup

```bash
# Stop (preserves data)
docker compose stop

# Start again later
docker compose start

# Full cleanup (remove containers, images, volumes)
docker compose down --rmi local -v
```

---

*For architecture diagrams, PromQL queries, and detailed theory, see the full lab doc.*
