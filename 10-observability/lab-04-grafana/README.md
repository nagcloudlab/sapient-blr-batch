# Lab 04: Build Grafana Dashboards (Golden Signals)
## 40 min | Prerequisite: Lab 03 (Prometheus running and scraping)

---

## What You'll Learn
- What Grafana is and how it connects to Prometheus
- The Four Golden Signals and how to visualize each one
- How to build a production-style dashboard
- Panel types: Stat, Gauge, Time Series
- Thresholds and color coding for at-a-glance status

## Why This Matters
Numbers in a PromQL console aren't useful during a 2 AM incident. Dashboards give you a visual overview in seconds. A well-designed dashboard answers "is anything wrong?" in one glance. This is what every on-call engineer looks at when they get paged.

## New Terms

| Term | Meaning |
|------|---------|
| **Grafana** | Open-source visualization platform. Connects to data sources (Prometheus, MySQL, CloudWatch, etc.) and turns queries into visual panels. Think of it as "Excel charts but for live server data." |
| **Dashboard** | A screen of panels showing related metrics. Like a car dashboard -- all important info in one view. |
| **Golden Signals** | Four key metrics every service should track (from Google's SRE book): **Latency, Traffic, Errors, Saturation**. They cover all critical failure modes. |
| **SLO** | Service Level Objective -- a target you set for your service. Example: "p99 latency < 500ms." It's your promise to users. |
| **SLA** | Service Level Agreement -- a contract with your customer. "99.9% uptime or we pay penalties." SLOs are internal targets; SLAs are legal contracts. |
| **SLI** | Service Level Indicator -- the actual metric you measure. "p99 latency is currently 350ms." SLI is the measurement, SLO is the target, SLA is the contract. |
| **Threshold** | A value boundary that changes the panel's color. Example: error rate < 1% = green, 1-5% = yellow, > 5% = red. |
| **Data source** | Where Grafana gets its data from. In our case, Prometheus. Grafana doesn't store data -- it queries Prometheus in real-time. |

### SLI / SLO / SLA -- How They Fit Together

```
SLI (what you measure):   p99 latency is currently 350ms
SLO (your target):        p99 latency should be < 500ms
SLA (your contract):      "99.9% of requests under 500ms, or customer gets credit"

   SLI < SLO  -->  "We're within budget, all good"
   SLI > SLO  -->  "We're burning error budget, investigate!"
   SLI > SLA  -->  "We're breaching our contract, customers affected"
```

---

## The Four Golden Signals

> **Quick Question:** If you could only monitor ONE metric for a food ordering service, which would you choose and why?

| Signal | What it measures | FoodExpress Example | Why it matters |
|--------|-----------------|---------------------|----------------|
| **Latency** | How long requests take | Order placement time (p99) | Slow = bad user experience |
| **Traffic** | How much demand exists | Orders per minute | Know your baseline, detect anomalies |
| **Errors** | Rate of failures | 5xx responses / total | Users are directly affected |
| **Saturation** | How full the system is | CPU %, memory % | Predicts FUTURE problems before they happen |

---

## Step 1: Run Grafana

```bash
docker run -d \
  --name grafana \
  -p 3000:3000 \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin123" \
  grafana/grafana
```

Open `http://<IP>:3000` -- login: `admin` / `admin123`

---

## Step 2: Connect Grafana to Prometheus

1. Left sidebar: **Connections > Data Sources > Add data source**
2. Select **Prometheus**
3. URL: `http://<VM_IP>:9090`
4. Click **Save & Test** -- should say "Successfully queried the Prometheus API"

> **How this works:** Grafana doesn't store metrics -- it queries Prometheus in real-time. Every time you view a dashboard, Grafana sends PromQL queries to Prometheus and renders the results.

---

## Step 3: Create the FoodExpress Dashboard

Click **+ > New Dashboard**. You'll create 6 panels.

### Panel 1: Error Rate -- Golden Signal: ERRORS

> **Why first?** Errors directly impact users. If this is red, nothing else matters until you fix it.

1. Click **Add visualization**, select Prometheus
2. Query: `rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m]) * 100`
3. Panel title: **Error Rate (%)**
4. Right sidebar: Visualization = **Stat**, Unit = Percent (0-100)
5. Thresholds: 0 = Green, 1 = Yellow, 5 = Red
6. Click **Apply**

> **Reading this panel:** Green (< 1%) = healthy. Yellow (1-5%) = investigate. Red (> 5%) = incident.

### Panel 2: P99 Latency -- Golden Signal: LATENCY

1. Add visualization
2. Query: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) * 1000`
3. Title: **P99 Latency (ms)**
4. Visualization: **Gauge** | Unit: milliseconds | Min: 0, Max: 2000
5. Thresholds: 0 = Green, 500 = Yellow, 1000 = Red

> **Think About It:** If the SLO is "p99 latency < 500ms", what color would this panel be when the SLO is being met? (Green.) When it's close to breaching? (Yellow.) When it's breached? (Red.) The thresholds directly map to your SLO.

### Panel 3: Orders per Minute -- Golden Signal: TRAFFIC

1. Add visualization
2. Query: `rate(orders_placed_total[1m]) * 60`
3. Title: **Orders / Minute**
4. Visualization: **Stat**

> **Why monitor traffic?** If traffic drops to 0 when it should be 100 orders/min, something is broken. If it spikes to 10x normal, you might need to scale.

### Panel 4: Request Rate by Status Code

1. Add visualization
2. Query A: `rate(http_requests_total{status="200"}[5m])` -- Legend: `200 OK`
3. Add Query B: `rate(http_requests_total{status="500"}[5m])` -- Legend: `500 Error`
4. Title: **Request Rate by Status**
5. Visualization: **Time Series**

### Panel 5: Active Orders

1. Add visualization
2. Query: `active_orders`
3. Title: **Active Orders** | Visualization: **Gauge** | Min: 0, Max: 100

### Panel 6: Memory Usage -- Golden Signal: SATURATION

1. Add visualization
2. Query: `process_resident_memory_bytes{job="order-service"} / 1024 / 1024`
3. Title: **Memory Usage (MB)** | Visualization: **Time Series** | Unit: MB

> **Why memory?** Memory leaks cause OOM (Out of Memory) kills. Tracking memory over time reveals slow leaks before they crash your service.

---

## Step 4: Arrange the layout

Drag panels to create this layout (top row = Golden Signals at a glance):

```
+---------------+---------------+---------------+
| Error Rate    | P99 Latency   | Orders/Min    |  <-- Glance row: "Is anything wrong?"
+---------------+---------------+---------------+
|          Request Rate by Status               |  <-- Trend: "Is it getting worse?"
+---------------------+------------------------+
| Active Orders        | Memory Usage           |  <-- Details
+---------------------+------------------------+
```

Set refresh to **10s** (top right). Set time range to **Last 15 minutes**. Save as **"FoodExpress Production"**.

---

## Step 5: Watch it live

Make sure the traffic generator is running (from Lab 03). Watch the dashboard update every 10 seconds.

> **Quick Question:** Look at the dashboard. What's the first thing that stands out? Is the error rate in green, yellow, or red? What would you do if you saw this in production?

---

## Step 6: Exercise -- Add two more panels

| # | Panel Title | Query | Type |
|---|-------------|-------|------|
| 1 | Success vs Failed Orders | `rate(orders_placed_total[5m])` split by `status` label | Time Series |
| 2 | CPU Usage (%) | `rate(process_cpu_seconds_total{job="order-service"}[5m]) * 100` | Time Series |

---

## Dashboard Design Principles

| Principle | Why |
|-----------|-----|
| **Top row = Golden Signals** | Answer "is anything wrong?" in 1 second |
| **Use color thresholds** | Red/yellow/green = instant visual status |
| **Show percentiles, not averages** | Averages hide problems (p99 reveals the worst user experience) |
| **Include both current values AND trends** | "Is it 5%?" (Stat) vs "Is it getting worse?" (Time Series) |
| **Match thresholds to SLOs** | If SLO is "p99 < 500ms", then yellow threshold = 500ms |

---

## Discussion

1. What's the first panel you'd look at during a 2 AM alert? Why?
2. How do SLI, SLO, and SLA relate to what you see on this dashboard? (SLI = the actual metric value on the panel. SLO = the threshold. SLA = the contractual obligation.)
3. What's missing from this dashboard? (Downstream dependencies, database metrics, business metrics like revenue per minute)

---

## What's Next

You have metrics and a dashboard. But when something fails, metrics tell you THAT it failed, not WHAT failed. In Lab 05, you'll add **structured logging** -- the second pillar of observability -- to capture the details behind the numbers.
