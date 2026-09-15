# Lab 01 - Metrics with Prometheus & Grafana

## What You Will Learn

- What metrics are and why they matter in production systems
- The difference between Counter, Gauge, Histogram, and Summary metric types
- How to instrument a Node.js app with `prom-client`
- How to instrument a Spring Boot app with Micrometer + Actuator
- How Prometheus scrapes (pulls) metrics from services
- How to write PromQL queries to analyze metrics
- How to build Grafana dashboards for real-time monitoring
- How inter-service latency shows up in metrics

## Architecture

```
                         +-------------------+
                         |     Grafana       |
                         |   localhost:3001  |
                         |  (admin/admin)    |
                         +--------+----------+
                                  |
                                  | queries via PromQL
                                  v
                         +-------------------+
                         |    Prometheus     |
                         |   localhost:9090  |
                         |  (time-series DB) |
                         +--------+----------+
                                  |
                    +-------------+-------------+
                    |                            |
              scrapes every 15s           scrapes every 15s
              GET /metrics                GET /actuator/prometheus
                    |                            |
                    v                            v
          +-------------------+        +-------------------+
          |  Order Service    |  HTTP  | Payment Service   |
          |  (Node.js)        +------->+  (Spring Boot)    |
          |  port 3000        |  POST  |  port 8080        |
          |                   | /pay   |                   |
          |  prom-client      | ments  |  Micrometer +     |
          |  library          |        |  Actuator         |
          +-------------------+        +-------------------+
```

## Flow: What Happens When You Create an Order

```
1. Client sends POST /orders to Order Service
2. Order Service creates order record
3. Order Service calls POST /payments on Payment Service
4. Payment Service processes payment (50-250ms random delay)
5. Payment Service returns success (90%) or failure (10%)
6. Order Service updates order status (CONFIRMED or PAYMENT_FAILED)
7. Order Service returns response to client

During this flow, these metrics get updated:
  - http_request_duration_seconds  (how long the whole request took)
  - orders_created_total           (counter incremented by 1)
  - payment_service_call_duration  (how long the payment call took)
  - payments_completed_total       (if payment succeeded)
  - payments_failed_total          (if payment failed)
```

## Services Overview

### Order Service (Node.js - port 3000)

- **Library:** `prom-client` (Prometheus client for Node.js)
- **Metrics endpoint:** `GET /metrics`
- **Custom metrics defined in code:**

| Metric Name | Type | Labels | What It Tracks |
|---|---|---|---|
| `http_request_duration_seconds` | Histogram | method, route, status_code | Latency of every HTTP request |
| `orders_created_total` | Counter | status | Total orders, split by CONFIRMED/PAYMENT_FAILED |
| `payment_service_call_duration_seconds` | Histogram | - | How long each call to payment service takes |

- **Default metrics** (collected automatically by prom-client):
  - `nodejs_heap_size_total_bytes` - total heap memory
  - `nodejs_active_handles_total` - active handles (connections, timers)
  - `nodejs_eventloop_lag_seconds` - event loop lag
  - `process_cpu_seconds_total` - CPU usage

### Payment Service (Spring Boot - port 8080)

- **Library:** Spring Boot Actuator + `micrometer-registry-prometheus`
- **Metrics endpoint:** `GET /actuator/prometheus`
- **Custom metrics defined in code:**

| Metric Name | Type | Labels | What It Tracks |
|---|---|---|---|
| `payments_completed_total` | Counter | - | Total successful payments |
| `payments_failed_total` | Counter | - | Total failed payments |
| `payment_processing_duration` | Timer | - | Time spent processing each payment |

- **Default metrics** (collected automatically by Micrometer):
  - `jvm_memory_used_bytes` - JVM heap and non-heap memory
  - `jvm_threads_live_threads` - active thread count
  - `jvm_gc_pause_seconds` - garbage collection pause duration
  - `http_server_requests_seconds` - all HTTP request durations
  - `system_cpu_usage` - system CPU utilization

### How Metrics Are Defined in Code

**Node.js (prom-client):**
```javascript
const ordersCreatedTotal = new client.Counter({
  name: "orders_created_total",
  help: "Total number of orders created",
  labelNames: ["status"],
});

// Increment when an order is created
ordersCreatedTotal.inc({ status: "CONFIRMED" });
```

**Spring Boot (Micrometer):**
```java
private final Counter paymentsCompletedCounter;

public PaymentController(MeterRegistry registry) {
    this.paymentsCompletedCounter = Counter.builder("payments_completed_total")
            .description("Total completed payments")
            .register(registry);
}

// Increment when a payment completes
paymentsCompletedCounter.increment();
```

## How To Run

```bash
# Start all services (Spring Boot takes ~30 seconds to start)
sudo docker compose up --build -d

# Check all containers are running
sudo docker compose ps

# Check health endpoints
curl http://localhost:3000/health
curl http://localhost:8080/health
```

## How To Test

### Manual Testing

```bash
# Create a single order
curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "laptop", "quantity": 1, "price": 999.99}'

# Create more orders with different items
curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "mouse", "quantity": 2, "price": 29.99}'

curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "keyboard", "quantity": 1, "price": 79.99}'

# List all orders
curl http://localhost:3000/orders

# Get a specific order (use an ID from the response above)
curl http://localhost:3000/orders/<order-id>
```

### Generate Load (use the load script)

```bash
# Run the load generator script
chmod +x generate-load.sh
./generate-load.sh

# Or run it for a specific number of requests
./generate-load.sh 100
```

## What To Observe

### Step 1: Check Raw Metrics Endpoints

```bash
# Node.js metrics - look for our custom metrics in the output
curl -s http://localhost:3000/metrics | grep orders_created
curl -s http://localhost:3000/metrics | grep http_request_duration
curl -s http://localhost:3000/metrics | grep payment_service_call

# Spring Boot metrics - look for our custom metrics
curl -s http://localhost:8080/actuator/prometheus | grep payments_completed
curl -s http://localhost:8080/actuator/prometheus | grep payments_failed
curl -s http://localhost:8080/actuator/prometheus | grep payment_processing
```

Notice the output format:
```
# HELP orders_created_total Total number of orders created
# TYPE orders_created_total counter
orders_created_total{status="CONFIRMED"} 8
orders_created_total{status="PAYMENT_FAILED"} 2
```

- Lines starting with `# HELP` describe the metric
- Lines starting with `# TYPE` declare the type (counter, histogram, etc.)
- Data lines have the format: `metric_name{labels} value`

### Step 2: Explore Prometheus UI (localhost:9090)

**Check targets are being scraped:**
- Go to Status > Targets
- Both `order-service` and `payment-service` should show State = "UP"
- "Last Scrape" shows when it last pulled metrics
- "Scrape Duration" shows how long the scrape took

**Try these PromQL queries (paste into the query box, click Execute):**

```
# 1. Simple counter - total orders created
orders_created_total

# 2. Counter with label filter - only confirmed orders
orders_created_total{status="CONFIRMED"}

# 3. Rate - orders per second over last 1 minute
rate(orders_created_total[1m])

# 4. Request rate for order service by route
rate(http_request_duration_seconds_count[1m])

# 5. 95th percentile latency for order service
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))

# 6. Average payment call duration
rate(payment_service_call_duration_seconds_sum[1m]) / rate(payment_service_call_duration_seconds_count[1m])

# 7. Payment success rate (percentage)
payments_completed_total / (payments_completed_total + payments_failed_total) * 100

# 8. JVM memory usage of payment service
jvm_memory_used_bytes{area="heap"} / 1024 / 1024

# 9. Node.js event loop lag
nodejs_eventloop_lag_seconds

# 10. Compare request counts across both services
{__name__=~"orders_created_total|payments_completed_total|payments_failed_total"}
```

**Understanding PromQL:**
```
rate(metric[1m])          = per-second rate over last 1 minute
sum(metric)               = sum across all label combinations
histogram_quantile(0.95)  = 95th percentile from histogram buckets
increase(metric[5m])      = total increase over last 5 minutes
metric{label="value"}     = filter by label
```

### Step 3: Explore Grafana Dashboard (localhost:3001)

- Login with **admin / admin** (skip password change)
- Click hamburger menu (top left) > Dashboards
- Click **"Order & Payment Services"**
- You should see 5 panels:

```
+------------------------------+------------------------------+
|  Order Service Request Rate  | Payment Service Request Rate |
|  (requests/sec by route)     | (requests/sec by endpoint)   |
+------------------------------+------------------------------+
+-------------------+--------------------+---------------------+
| Orders Created    | Payments           | Payment Latency     |
| (CONFIRMED vs     | (Completed vs      | (p50 and p95 from   |
|  PAYMENT_FAILED)  |  Failed counters)  |  order service POV) |
+-------------------+--------------------+---------------------+
```

- Run the load script and watch the graphs update in real-time
- Notice how the payment failure rate is ~10%
- Notice the latency varies between 50-250ms

### Step 4: Try Building Your Own Dashboard

1. In Grafana, click + > New Dashboard > Add Visualization
2. Select "Prometheus" as datasource
3. Try these queries:
   - `process_resident_memory_bytes` - memory usage of both services
   - `rate(http_request_duration_seconds_count{route="/orders"}[1m])` - just POST orders rate
   - `jvm_threads_live_threads` - JVM thread count

## Key Concepts

### Why Metrics Matter

```
Without metrics:
  "The app feels slow" -> How slow? Since when? Which endpoint?

With metrics:
  "POST /orders p95 latency jumped from 200ms to 2s
   at 14:30, correlating with payment_service_call_duration increase"
```

### Metric Types Explained

```
COUNTER - only goes up, resets to 0 on restart
+---+
|   |     Use for: total requests, total errors, total bytes sent
| 42|     Example: orders_created_total
|   |     You almost always use rate() on counters
+---+

GAUGE - goes up and down
+---+
|   |     Use for: current temperature, memory usage, queue size
|~~ |     Example: nodejs_active_handles_total
|   |     You read gauges directly (no rate needed)
+---+

HISTOGRAM - samples values into configurable buckets
+---+
||| |     Use for: request duration, response size
||  |     Example: http_request_duration_seconds
|   |     Lets you compute percentiles (p50, p95, p99)
+---+     Buckets: [0.01, 0.05, 0.1, 0.3, 0.5, 1, 2, 5]

SUMMARY - similar to histogram but calculates quantiles client-side
+---+
|/\ |     Use for: when you need exact percentiles
|  \|     Less common than histograms
+---+     Cannot be aggregated across instances
```

### Pull vs Push Model

```
PULL (Prometheus) - used in this lab:
+------------+         +----------+
| Prometheus +-------->+ Service  |
|            | GET     |          |
| "I'll come | /metrics| "Here's  |
|  ask you"  +<--------+ my data" |
+------------+         +----------+

PUSH (e.g., StatsD, Datadog Agent):
+----------+         +------------+
| Service  +-------->+ Collector  |
|          | send    |            |
| "Here's  | metrics | "I'll wait |
|  my data"+-------->+  for data" |
+----------+         +------------+

Pull advantages:
  - Prometheus knows if a service is down (scrape fails)
  - No risk of overwhelming the collector
  - Services don't need to know where Prometheus is
```

### How Prometheus Stores Data

```
Every metric is a time-series:

metric_name{label1="val1", label2="val2"}  value  @timestamp

Example stored data:
orders_created_total{status="CONFIRMED"}    1   @14:00:00
orders_created_total{status="CONFIRMED"}    3   @14:00:15
orders_created_total{status="CONFIRMED"}    7   @14:00:30
orders_created_total{status="CONFIRMED"}   12   @14:00:45

Labels create separate time-series:
orders_created_total{status="CONFIRMED"}      -> one series
orders_created_total{status="PAYMENT_FAILED"} -> another series
```

### Prometheus Scrape Config Explained

```yaml
# prometheus/prometheus.yml
scrape_configs:
  - job_name: "order-service"       # label added to all metrics
    metrics_path: /metrics           # endpoint to scrape
    static_configs:
      - targets: ["order-service:3000"]  # host:port to scrape

  - job_name: "payment-service"
    metrics_path: /actuator/prometheus    # Spring Boot uses different path
    static_configs:
      - targets: ["payment-service:8080"]
```

## File Structure

```
lab-01-metrics/
├── LAB.md                                  # this file
├── docker-compose.yml                      # runs all 4 services
├── generate-load.sh                        # load generator script
├── order-service/
│   ├── Dockerfile
│   ├── package.json                        # prom-client dependency
│   └── src/
│       └── index.js                        # Express app + metrics setup
├── payment-service/
│   ├── Dockerfile
│   ├── pom.xml                             # actuator + micrometer-registry-prometheus
│   └── src/main/
│       ├── java/com/example/payment/
│       │   ├── PaymentServiceApplication.java
│       │   ├── Payment.java
│       │   └── PaymentController.java      # Counter + Timer metrics
│       └── resources/
│           └── application.properties      # actuator endpoint exposure config
├── prometheus/
│   └── prometheus.yml                      # scrape targets config
└── grafana/
    ├── provisioning/
    │   ├── datasources/
    │   │   └── datasource.yml              # auto-configure Prometheus datasource
    │   └── dashboards/
    │       └── dashboard.yml               # auto-load dashboard JSON files
    └── dashboards/
        └── services.json                   # pre-built dashboard with 5 panels
```

## Troubleshooting

- **Prometheus target shows DOWN:** check `docker compose logs payment-service` - Spring Boot may still be starting
- **Grafana shows "No data":** generate some load first, then wait 15-30 seconds for Prometheus to scrape
- **Grafana dashboard not found:** restart grafana with `docker compose restart grafana`
- **Metrics endpoint returns empty:** make sure you've sent at least one request to create an order

## Cleanup

```bash
sudo docker compose down
```
