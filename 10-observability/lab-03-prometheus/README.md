# Lab 03: Set Up Prometheus and Learn PromQL
## 30 min | Prerequisite: Lab 02 (order-service running in Docker)

---

## What You'll Learn
- How Prometheus works (pull model, scraping, time-series storage)
- How to configure Prometheus to scrape your service
- PromQL: the query language for time-series data
- Key functions: `rate()`, `histogram_quantile()`, `increase()`

## Why This Matters
Your `/metrics` endpoint (Lab 02) is just raw text that resets on restart. Prometheus stores this data over time, lets you query historical trends, and is the foundation for dashboards (Lab 04) and alerts (Lab 06). Prometheus is the industry standard for cloud-native monitoring -- used by Google, Spotify, DigitalOcean, and most Kubernetes clusters.

## New Terms

| Term | Meaning |
|------|---------|
| **Pull model** | Prometheus FETCHES (scrapes) metrics FROM your service by calling `/metrics`. The opposite of "push" where the app sends data to a collector. |
| **Scrape** | The act of Prometheus making an HTTP GET request to your `/metrics` endpoint. Happens every N seconds (configurable). |
| **TSDB** | Time Series Database -- a database optimized for storing timestamped numeric data. Prometheus stores ~1-2 bytes per sample. |
| **PromQL** | Prometheus Query Language -- a powerful language for querying time-series data. Think of it as "SQL for metrics." |
| **Range vector** | A time window of data points. `[5m]` means "the last 5 minutes of samples." Used inside functions like `rate()`. |
| **rate()** | A PromQL function that calculates the per-second rate of increase of a counter. Essential because counters only go up. |
| **histogram_quantile()** | A PromQL function that calculates percentiles (p50, p95, p99) from histogram data. |
| **Scrape interval** | How often Prometheus fetches metrics from a target. Default: 15 seconds. |

---

## How Prometheus Works (The Pull Model)

```
Prometheus ----[HTTP GET /metrics every 10s]----> order-service:8080/metrics
    |
    +-- Stores: "at 10:00:01, http_requests_total was 42"
    +-- Stores: "at 10:00:11, http_requests_total was 47"
    +-- rate() calculates: (47-42) / 10 seconds = 0.5 requests/second
```

> **Quick Question:** Why does Prometheus PULL metrics from services, instead of services PUSHING metrics to Prometheus?
>
> Hint: What happens if a service dies? With pull: Prometheus notices it can't reach the service = instant "service down" detection. With push: silence could mean "nothing to report" OR "it crashed" -- you can't tell the difference.

---

## Step 1: Create Prometheus configuration

```bash
cd ~/obs-labs
```

Create `prometheus.yml` (or copy from this folder):

```yaml
global:
  scrape_interval: 15s        # Default: scrape all targets every 15 seconds
  evaluation_interval: 15s    # How often to evaluate alert rules (Lab 06)

scrape_configs:
  # Prometheus monitors itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Our FoodExpress order service
  - job_name: 'order-service'
    scrape_interval: 10s       # Override: scrape this target every 10 seconds
    static_configs:
      - targets: ['host.docker.internal:8080']
```

> **Config explained:**
> - `scrape_interval`: how often Prometheus fetches `/metrics`
> - `job_name`: logical group name for targets (appears as a label in queries)
> - `targets`: list of `host:port` to scrape
> - `host.docker.internal`: Docker's special hostname to reach the host machine from inside a container
>
> **On Linux VMs:** Replace `host.docker.internal` with your VM's IP: `hostname -I | awk '{print $1}'`

---

## Step 2: Run Prometheus

```bash
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

---

## Step 3: Verify targets

Open `http://<IP>:9090` in your browser. Go to **Status > Targets**.

| Job | Target | Expected State |
|-----|--------|-------|
| prometheus | localhost:9090 | **UP** (green) |
| order-service | host.docker.internal:8080 | **UP** (green) |

> **If order-service shows DOWN:** Is the container running? (`docker ps`). Try your VM's IP instead of `host.docker.internal`.

---

## Step 4: Your first PromQL queries

Go to the **Graph** tab. Type each query, click **Execute**, then click **Graph** to see it as a time series.

### Query 1: Is the service up?
```promql
up
```
> `up{job="order-service"} 1` means Prometheus can reach it. `0` means it's down. This is the simplest health check.

### Query 2: Raw counter value (not very useful by itself)
```promql
http_requests_total
```
> **Notice:** This number only goes UP. It shows the TOTAL since the service started. Not useful by itself -- we need the RATE of change.

### Query 3: Request rate -- THE most important PromQL function
```promql
rate(http_requests_total[5m])
```

### New Term: rate()

| | |
|--|--|
| **What it does** | Calculates per-second rate of increase over a time window |
| **Why you need it** | Counters only go up. `rate()` tells you HOW FAST they're going up. |
| **The `[5m]`** | Look at the last 5 minutes of data points to calculate the rate |
| **Example** | Counter went from 100 to 200 in 5 minutes = `rate()` returns 0.33/sec |
| **Handles restarts** | If the counter resets to 0 (service restart), `rate()` handles it correctly. Plain math would show a negative spike. |

### Query 4: Error rate as a percentage
```promql
rate(http_requests_total{status="500"}[5m]) / rate(http_requests_total[5m]) * 100
```
> **How to read this:** "Of all requests in the last 5 minutes, what percentage returned 500?"

### Query 5: P99 latency
```promql
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

### New Terms: Percentiles Explained

| Term | Meaning | Example |
|------|---------|---------|
| **p50** | 50% of requests are faster than this (the median) | p50 = 100ms means the "typical" experience |
| **p90** | 90% faster, 10% slower | p90 = 300ms means 1 in 10 users waits 300ms+ |
| **p95** | 95% faster, 5% slower | Often used in SLOs |
| **p99** | 99% faster, 1% slower | p99 = 2s means 1 in 100 users waits 2+ seconds |
| **Average** | Total time / number of requests | **MISLEADING!** avg of [100, 100, 100, 5000] = 1325ms, but 75% of users had 100ms |

> **Think About It:** Why do we measure p99 instead of average? Because the average HIDES the worst experiences. If your average is 200ms but your p99 is 5 seconds, 1% of your users are having a terrible time -- and that 1% might be your biggest customers.

### Query 6: Orders per minute
```promql
rate(orders_placed_total[1m]) * 60
```
> **Why multiply by 60?** `rate()` returns per-SECOND. Multiply by 60 for per-minute. This is a common gotcha -- don't divide by 60!

---

## Step 5: Generate sustained traffic

In another terminal:

```bash
while true; do
  curl -s -X POST http://localhost:8080/api/orders > /dev/null
  sleep 0.1
done
```

Wait 2-3 minutes, then re-run the PromQL queries. Click **Graph** to see trends over time.

---

## Step 6: PromQL exercises (try yourself first)

| # | Task | Hint |
|---|------|------|
| 1 | Total orders placed in the last hour | `increase()` function |
| 2 | Memory usage in MB | `process_resident_memory_bytes / 1024 / 1024` |
| 3 | Median (p50) latency | `histogram_quantile(0.5, ...)` |
| 4 | POST request rate only | Label filter `{method="POST"}` |

<details>
<summary>Answers</summary>

```promql
# 1. Total orders in last hour (increase = total increase of a counter over time)
increase(orders_placed_total[1h])

# 2. Memory in MB
process_resident_memory_bytes{job="order-service"} / 1024 / 1024

# 3. Median latency (50th percentile)
histogram_quantile(0.5, rate(http_request_duration_seconds_bucket[5m]))

# 4. POST only
rate(http_requests_total{method="POST"}[5m])
```

</details>

---

## PromQL Cheat Sheet

| Function | Use with | What it does |
|----------|----------|-------------|
| `rate()` | Counters | Per-second rate of increase |
| `increase()` | Counters | Total increase over time window |
| `histogram_quantile()` | Histograms | Calculate percentiles (p50, p99) |
| `sum()` | Any | Add up across all label values |
| `sum by(label)` | Any | Add up, keeping a specific label |

> **The #1 mistake beginners make:** Using a raw counter without `rate()`. It shows an ever-increasing number that means nothing. ALWAYS use `rate()` or `increase()` with counters.

---

## Discussion

1. Why does Prometheus use a PULL model instead of apps pushing metrics?
2. What happens if a service goes down -- how does Prometheus know? (Hint: `up` metric)
3. What's the difference between p50 and p99? If you had to pick ONE for an SLO, which would you choose and why?

---

## What's Next

You can query data, but staring at numbers isn't great. In Lab 04, you'll build **Grafana dashboards** to visualize these queries as live graphs, gauges, and stat panels -- the way production teams monitor their services.
