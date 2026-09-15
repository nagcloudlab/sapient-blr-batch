# Lab 02: Add Prometheus Metrics to a Node.js App
## 35 min | Prerequisite: Lab 01

---

## What You'll Learn
- How to instrument a Node.js service with Prometheus metrics
- The four metric types: Counter, Gauge, Histogram, Summary
- What the `/metrics` endpoint looks like (Prometheus exposition format)
- How to containerize an instrumented service

## Why This Matters
Metrics are the foundation of monitoring. Without them, you're flying blind (Lab 01). Every production service MUST expose metrics. This is the first thing you add to any service -- before dashboards, before alerts, before anything else.

## New Terms

| Term | Meaning |
|------|---------|
| **Instrumentation** | Adding code to your app that collects and exposes metrics. Like adding sensors to a machine. |
| **Counter** | A metric that only goes UP (like a car's odometer). Example: total requests served. It never decreases -- when the app restarts, it resets to 0. |
| **Gauge** | A metric that goes UP and DOWN (like a speedometer). Example: currently active users, temperature. |
| **Histogram** | A metric that counts observations falling into configurable buckets. Example: "500 requests took 0-100ms, 300 took 100-500ms, 10 took 500ms-1s." Used to calculate percentiles (p50, p99). |
| **Summary** | Similar to histogram but calculates percentiles on the client side. Less flexible -- prefer Histogram in most cases. |
| **Labels** | Key-value pairs on metrics that create dimensions. `http_requests_total{method="POST", status="500"}` lets you filter for just POST requests that returned 500. |
| **prom-client** | The official Node.js library for creating Prometheus metrics. `npm install prom-client` |
| **Exposition format** | The plain-text format Prometheus uses to read metrics. Each metric is a line like `http_requests_total{method="POST"} 42` |

---

## Step 1: Set up the project

```bash
cd ~/obs-labs
npm init -y
npm install express prom-client
```

> **What is prom-client?** The official Prometheus client library for Node.js. It lets your app create metrics and expose them in Prometheus format at a `/metrics` endpoint.

---

## Step 2: Create the instrumented service

Copy `order-service.js` from this folder, or create it. Let's understand each section:

### Section 1: Default metrics
```javascript
client.collectDefaultMetrics();
```
> **What:** Automatically collects Node.js runtime metrics -- CPU usage, memory, event loop lag, garbage collection.
> **Why:** Free visibility into your process health without writing any code.

### Section 2: Custom metrics

```javascript
// COUNTER: Total requests (only goes up)
const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',       // Metric name (convention: snake_case_total for counters)
  help: 'Total HTTP requests',       // Human-readable description
  labelNames: ['method', 'path', 'status']  // Dimensions for slicing data
});

// HISTOGRAM: Request duration (for percentile calculations like p50, p99)
const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',   // Convention: use base units (seconds, not ms)
  help: 'Request duration in seconds',
  labelNames: ['method', 'path'],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]  // Bucket boundaries in seconds
});

// COUNTER: Business metric -- total orders placed
const ordersTotal = new client.Counter({
  name: 'orders_placed_total',
  help: 'Total orders placed',
  labelNames: ['status']   // 'success' or 'failed'
});

// GAUGE: Currently active orders (goes up and down)
const activeOrders = new client.Gauge({
  name: 'active_orders',
  help: 'Currently active orders'
});
```

> **Quick Question:** For each of these real-world measurements, which metric type would you use?
> - Total page views on a website: ___
> - Number of items currently in a shopping cart: ___
> - API response time distribution: ___
> - Current temperature of a server room: ___

<details>
<summary>Answers</summary>

- Total page views: **Counter** (only goes up)
- Items in cart: **Gauge** (items are added and removed)
- API response time: **Histogram** (need percentiles for SLOs)
- Temperature: **Gauge** (goes up and down)

</details>

### Section 3: Middleware (measure every request automatically)
```javascript
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer({ method: req.method, path: req.path });
  res.on('finish', () => {
    httpRequestsTotal.inc({ method: req.method, path: req.path, status: res.statusCode });
    end();  // Stops timer and records duration in histogram
  });
  next();
});
```
> **How this works:** Express middleware runs BEFORE every request. We start a timer, then when the response finishes, we increment the counter and record the duration. EVERY request is measured automatically without touching route code.

### Section 4: The `/metrics` endpoint
```javascript
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});
```
> **This is what Prometheus will scrape (in Lab 03).** It returns all metrics in Prometheus exposition format -- plain text that looks like:
> ```
> # HELP http_requests_total Total HTTP requests
> # TYPE http_requests_total counter
> http_requests_total{method="POST",path="/api/orders",status="200"} 42
> ```

---

## Step 3: Run and explore the metrics endpoint

```bash
node order-service.js &
curl http://localhost:8080/metrics
```

> **Take a moment to read the output.** Notice:
> - `# HELP` = description of the metric
> - `# TYPE` = counter, gauge, or histogram
> - Labels are in `{curly braces}`
> - Histogram has three sub-metrics: `_bucket` (distribution), `_sum` (total), `_count` (count)

---

## Step 4: Generate traffic and answer Lab 01's questions

```bash
for i in $(seq 1 100); do
  curl -s -X POST http://localhost:8080/api/orders > /dev/null
  sleep 0.05
done
```

Now answer the questions that were IMPOSSIBLE in Lab 01:

```bash
# Q1: How many succeeded vs failed?
curl -s http://localhost:8080/metrics | grep orders_placed_total

# Q2: Total request count by status code?
curl -s http://localhost:8080/metrics | grep http_requests_total

# Q3: Latency distribution (histogram buckets)?
curl -s http://localhost:8080/metrics | grep http_request_duration_seconds_bucket

# Q6: Process CPU and memory?
curl -s http://localhost:8080/metrics | grep -E "process_(cpu|resident_memory)"
```

> **Think About It:** In Lab 01, you couldn't answer ANY of these. Now you can answer 4 out of 6 just by adding metrics. Logs and traces (coming in Labs 05 and 08) will cover the remaining questions.

---

## Step 5: Exercise -- Identify metric types

| Metric | Type? | Why? |
|--------|-------|------|
| `http_requests_total` | ? | |
| `active_orders` | ? | |
| `http_request_duration_seconds` | ? | |
| `process_resident_memory_bytes` | ? | |

<details>
<summary>Answers</summary>

| Metric | Type | Why |
|--------|------|-----|
| `http_requests_total` | **Counter** | Only goes up -- you can't "un-receive" a request |
| `active_orders` | **Gauge** | Goes up (order placed) and down (order completed) |
| `http_request_duration_seconds` | **Histogram** | Tracks distribution in buckets for percentile calculation |
| `process_resident_memory_bytes` | **Gauge** | Current memory usage -- goes up and down |

</details>

---

## Step 6: Containerize the instrumented service

```bash
kill %1   # Stop the previous process
docker build -t foodexpress-order:v1 .
docker run -d --name order-service -p 8080:8080 foodexpress-order:v1
curl http://localhost:8080/metrics   # Verify it works in Docker
```

> **Why containerize now?** From Lab 03 onward, we'll run Prometheus in Docker too. Having everything in containers makes networking between services straightforward.

---

## Naming Conventions (Industry Standard)

| Rule | Example | Why |
|------|---------|-----|
| Use `snake_case` | `http_requests_total` not `httpRequestsTotal` | Prometheus convention |
| Counters end with `_total` | `orders_placed_total` | Makes it clear this only goes up |
| Use base units | `_seconds` not `_milliseconds` | Avoid confusion across teams |
| Keep label cardinality low | `{status="200"}` (few values) | `{user_id="..."}` has millions of values -- crashes Prometheus |

> **Discussion:** Why is `user_id` a bad metric label? (Hint: if you have 1 million users, that's 1 million time series just for one metric. Prometheus stores each label combination separately. Use logs for high-cardinality data like user IDs.)

---

## Discussion

1. What's the difference between a Counter and a Gauge? Give a real-world example of each beyond what we covered.
2. Why do we use Histograms instead of just tracking average response time?
3. What happens to a Counter when the service restarts? (It resets to 0 -- that's why we'll use `rate()` in PromQL in Lab 03.)

---

## What's Next

The `/metrics` endpoint is just raw text right now. In Lab 03, you'll set up **Prometheus** to automatically scrape this endpoint every 10 seconds, store the data over time, and query it with a powerful language called **PromQL**.
