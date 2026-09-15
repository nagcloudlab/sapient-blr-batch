# Lab 02: Add Prometheus Metrics
## 35 min | Prerequisite: Lab 01

Choose your stack: **[Node.js](#option-a-nodejs)** or **[Spring Boot](#option-b-spring-boot)**

Both versions expose the same endpoints and metrics -- Prometheus doesn't care what language your app uses.

```
lab-02-add-metrics/
├── nodejs/          # Express + prom-client
│   ├── order-service.js
│   ├── package.json
│   └── Dockerfile
├── springboot/      # Spring Boot + Micrometer
│   ├── pom.xml
│   ├── src/
│   └── Dockerfile
└── README.md
```

---

## What You'll Learn
- How to instrument a service with Prometheus metrics
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
| **Exposition format** | The plain-text format Prometheus uses to read metrics. Each metric is a line like `http_requests_total{method="POST"} 42` |

---

## Same Endpoints, Same Metrics -- Both Versions

| Endpoint | Method | Behavior |
|----------|--------|----------|
| `/` | GET | Service info |
| `/api/orders` | POST | Place order (10% fail, 5% slow) |
| `/health` | GET | Health check |
| `/metrics` | GET | Prometheus metrics |

| Metric | Type | Labels |
|--------|------|--------|
| `http_requests_total` | Counter | method, path, status |
| `http_request_duration_seconds` | Histogram | method, path |
| `orders_placed_total` | Counter | status |
| `active_orders` | Gauge | -- |

---

# Option A: Node.js

## A1: Set up the project

```bash
cd ~/obs-labs
npm init -y
npm install express prom-client
```

> **What is prom-client?** The official Prometheus client library for Node.js. It lets your app create metrics and expose them in Prometheus format at a `/metrics` endpoint.

## A2: Create the instrumented service

Copy `nodejs/order-service.js` from this folder. Let's understand each section:

### Default metrics
```javascript
client.collectDefaultMetrics();
```
> Automatically collects Node.js runtime metrics -- CPU usage, memory, event loop lag, garbage collection.

### Custom metrics

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

### Middleware (measure every request automatically)
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

### The `/metrics` endpoint
```javascript
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});
```

## A3: Run it

```bash
node nodejs/order-service.js &
curl http://localhost:8080/metrics
```

## A4: Containerize

```bash
cd nodejs
docker build -t foodexpress-order:v1 .
docker run -d --name order-service -p 8080:8080 foodexpress-order:v1
```

---

# Option B: Spring Boot

## B1: Set up the project

```bash
cd ~/obs-labs
```

Copy the `springboot/` folder from this lab. Key dependencies in `pom.xml`:

```xml
<!-- Web framework -->
<artifactId>spring-boot-starter-web</artifactId>

<!-- Actuator: exposes /health, /metrics, /prometheus -->
<artifactId>spring-boot-starter-actuator</artifactId>

<!-- Prometheus format for metrics -->
<artifactId>micrometer-registry-prometheus</artifactId>
```

| Term | Meaning |
|------|---------|
| **Micrometer** | A metrics facade for JVM-based apps (like SLF4J for logging). Supports Prometheus, Datadog, CloudWatch, and more. |
| **Spring Boot Actuator** | A Spring Boot module that exposes operational endpoints: `/health`, `/metrics`, `/prometheus`, etc. |
| **micrometer-registry-prometheus** | The Micrometer backend that formats metrics in Prometheus exposition format. |
| **Timer** | Micrometer's equivalent of a Prometheus Histogram. Measures duration and publishes buckets for percentile calculation. |

## B2: Understand the metrics code

### Counters (like `orders_placed_total` in Node.js)
```java
Counter ordersSuccessCounter = Counter.builder("orders_placed_total")
        .tag("status", "success")           // label
        .description("Total orders placed")
        .register(registry);
```

### Timer/Histogram (like `http_request_duration_seconds` in Node.js)
```java
Timer orderDurationTimer = Timer.builder("http_request_duration_seconds")
        .publishPercentileHistogram()       // enables bucket-based histograms
        .sla(Duration.ofMillis(10), ...)    // custom bucket boundaries
        .register(registry);
```

### Gauge (like `active_orders` in Node.js)
```java
AtomicInteger activeOrders = new AtomicInteger(0);
Gauge.builder("active_orders", activeOrders, AtomicInteger::get)
        .register(registry);
```

> **Key Difference:** In Node.js, you call `gauge.inc()` / `gauge.dec()`. In Micrometer, a Gauge observes a value source (like an AtomicInteger) -- you update the source, the Gauge reads it automatically.

## B3: Run it

```bash
cd springboot
mvn spring-boot:run
```

```bash
curl http://localhost:8080/metrics
```

## B4: Containerize

```bash
cd springboot
docker build -t foodexpress-order-spring:v1 .
docker run -d --name order-service-spring -p 8080:8080 foodexpress-order-spring:v1
```

---

## Node.js vs Spring Boot -- Side by Side

| Concept | Node.js (prom-client) | Spring Boot (Micrometer) |
|---------|----------------------|--------------------------|
| Metrics library | `prom-client` | `micrometer-registry-prometheus` |
| Counter | `new client.Counter({...})` | `Counter.builder("name").register(registry)` |
| Gauge | `new client.Gauge({...})` | `Gauge.builder("name", ref, fn).register(registry)` |
| Histogram | `new client.Histogram({...})` | `Timer.builder("name").publishPercentileHistogram().register(registry)` |
| Labels | `labelNames: ['status']` | `.tag("status", "success")` |
| Metrics endpoint | Manual route: `app.get('/metrics', ...)` | Auto via Actuator config |
| Default metrics | `client.collectDefaultMetrics()` | Automatic (JVM memory, GC, threads, CPU) |

> **Key Insight:** The Prometheus exposition format is the same regardless of language. Prometheus doesn't care if your app is Node.js, Java, Python, or Go -- it just scrapes the `/metrics` endpoint.

---

## Exercise -- Identify metric types

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

## Generate traffic and verify (either version)

```bash
for i in $(seq 1 100); do
  curl -s -X POST http://localhost:8080/api/orders > /dev/null
  sleep 0.05
done
```

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
