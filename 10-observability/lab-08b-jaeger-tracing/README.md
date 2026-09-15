# Lab 08b: Real Distributed Tracing with Jaeger & OpenTelemetry
## 45 min | Prerequisite: Lab 08

---

## What You'll Learn
- How to set up Jaeger -- a real distributed tracing backend
- How to instrument Node.js services with OpenTelemetry (auto-instrumentation)
- How to read a trace waterfall in the Jaeger UI (spans, durations, parent-child)
- How to visually identify bottlenecks across services
- How real production tracing differs from grepping logs

## Why This Matters
In Lab 08, you manually passed a `traceId` in headers and grepped logs to follow a request. That works for 3 services and 10 requests. In production with 50 services and 10,000 requests/second, you need a proper tracing tool that collects, stores, and visualizes traces automatically. That's what Jaeger + OpenTelemetry provide.

## New Terms

| Term | Meaning |
|------|---------|
| **Jaeger** | Open-source distributed tracing platform (CNCF graduated project, originally from Uber). Collects traces and provides a UI to search and visualize them. |
| **OpenTelemetry (OTel)** | The industry standard for instrumentation (CNCF project). Provides SDKs for Node.js, Java, Python, Go, etc. Merges two older projects: OpenTracing + OpenCensus. |
| **Auto-instrumentation** | OTel can automatically instrument HTTP calls, database queries, and framework code WITHOUT changing your application code. You add it at startup, and it traces everything. |
| **Span** | One unit of work. Has: operation name, start time, duration, status, parent span ID. Example: "POST /api/pay took 400ms, parent = order-service span." |
| **Trace waterfall** | A visual timeline showing all spans in a trace, nested by parent-child relationship. Immediately shows which span is the bottleneck. |
| **Exporter** | The component that sends trace data from your app to a tracing backend (Jaeger, Zipkin, DataDog). OTel supports many exporters. |
| **W3C Traceparent** | An industry-standard HTTP header for passing trace context between services. Format: `traceparent: 00-<traceId>-<spanId>-01`. "W3C" is the web standards body (same people who define HTML). OpenTelemetry uses this automatically -- replaces our manual `X-Trace-Id` from Lab 08. |
| **Collector** | A service that receives traces from apps, processes them, and forwards them to storage. Jaeger all-in-one includes a built-in collector. |
| **Sampling** | Deciding which requests to trace. Head-based = decide at start (e.g., 10%). Tail-based = decide after trace completes (keep errors/slow). At scale, you can't trace 100% of requests. |

---

## Lab 08 vs Lab 08b

| Lab 08 (Manual) | Lab 08b (Production-grade) |
|-----------------|---------------------------|
| Manual `X-Trace-Id` header | W3C Traceparent (automatic) |
| `grep` logs to follow a request | Jaeger UI: search, filter, waterfall |
| No timing per span | Each span shows exact duration |
| No parent-child relationships | Nested spans show call hierarchy |
| Can't search by service/duration/error | Full search: "show me all traces > 1s from payment-service" |

---

## Architecture

```
                        +---> Jaeger Collector ---> Jaeger UI (:16686)
                        |     (receives traces)     (visualize)
                        |
Order Service (8080) ---+---> Payment Service (8081)
     |                  |
     |  OTel SDK        +---> Notification Service (8082)
     |  auto-instruments
     |  HTTP calls and
     |  sends spans to Jaeger
```

---

## Step 1: Create the tracing setup file

This file initializes OpenTelemetry BEFORE your app code loads. Create `tracing.js`:

```javascript
'use strict';

const { NodeSDK } = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { Resource } = require('@opentelemetry/resources');
const { ATTR_SERVICE_NAME } = require('@opentelemetry/semantic-conventions');

const serviceName = process.env.OTEL_SERVICE_NAME || 'unknown-service';

const sdk = new NodeSDK({
  resource: new Resource({
    [ATTR_SERVICE_NAME]: serviceName,
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/traces',
  }),
  instrumentations: [
    getNodeAutoInstrumentations({
      // Auto-instrument HTTP, Express, and more -- no code changes needed!
      '@opentelemetry/instrumentation-http': { enabled: true },
      '@opentelemetry/instrumentation-express': { enabled: true },
    }),
  ],
});

sdk.start();
console.log(`OpenTelemetry initialized for service: ${serviceName}`);

// Graceful shutdown
process.on('SIGTERM', () => sdk.shutdown());
```

> **What just happened?** This file:
> 1. Creates an OpenTelemetry SDK instance
> 2. Configures it to send traces to Jaeger via OTLP (OpenTelemetry Protocol)
> 3. Enables **auto-instrumentation** -- every HTTP request (incoming AND outgoing) is automatically traced
> 4. You don't change ANY of your app code from Lab 08!

> **Quick Question:** Notice we didn't add any tracing code to our route handlers. How does OpenTelemetry know to trace HTTP calls? (Auto-instrumentation hooks into Node.js `http` module at startup. Every `http.request()` and every incoming Express request gets a span automatically.)

---

## Step 2: Update package.json

Create `package.json`:

```json
{
  "name": "foodexpress-traced",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "prom-client": "^14.2.0",
    "@opentelemetry/sdk-node": "^0.52.0",
    "@opentelemetry/exporter-trace-otlp-http": "^0.52.0",
    "@opentelemetry/auto-instrumentations-node": "^0.48.0",
    "@opentelemetry/resources": "^1.25.0",
    "@opentelemetry/semantic-conventions": "^1.25.0"
  }
}
```

---

## Step 3: Update Dockerfile

Create `Dockerfile`:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY *.js ./
EXPOSE 8080 8081 8082
# KEY: Load tracing.js BEFORE the app code using --require
# This ensures OpenTelemetry hooks into http module before Express uses it
CMD ["node", "--require", "./tracing.js", "order-service-v3.js"]
```

> **The `--require ./tracing.js` flag is critical.** It loads OpenTelemetry BEFORE your app starts. This allows it to hook into the `http` module and automatically create spans for every HTTP call.

---

## Step 4: Create Docker Compose with Jaeger

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # ── Jaeger: trace collector + UI ──
  jaeger:
    image: jaegertracing/all-in-one:1.57
    container_name: jaeger
    ports:
      - "16686:16686"    # Jaeger UI
      - "4318:4318"      # OTLP HTTP receiver (traces come in here)
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    networks:
      - observability

  # ── Order Service ──
  order-service:
    build: .
    container_name: order-service
    ports:
      - "8080:8080"
    environment:
      - PAYMENT_HOST=payment-service
      - NOTIFY_HOST=notification-service
      - OTEL_SERVICE_NAME=order-service
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4318/v1/traces
    command: ["node", "--require", "./tracing.js", "order-service-v3.js"]
    networks:
      - observability
    depends_on:
      - jaeger

  # ── Payment Service ──
  payment-service:
    build: .
    container_name: payment-service
    ports:
      - "8081:8081"
    environment:
      - OTEL_SERVICE_NAME=payment-service
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4318/v1/traces
    command: ["node", "--require", "./tracing.js", "payment-service.js"]
    networks:
      - observability
    depends_on:
      - jaeger

  # ── Notification Service ──
  notification-service:
    build: .
    container_name: notification-service
    ports:
      - "8082:8082"
    environment:
      - OTEL_SERVICE_NAME=notification-service
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4318/v1/traces
    command: ["node", "--require", "./tracing.js", "notification-service.js"]
    networks:
      - observability
    depends_on:
      - jaeger

  # ── Prometheus (for metrics alongside traces) ──
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - observability

networks:
  observability:
    driver: bridge
```

---

## Step 5: Copy service files and config

Copy these files from `lab-08-multi-service-tracing/`:
- `order-service-v3.js`
- `payment-service.js`
- `notification-service.js`

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 10s
scrape_configs:
  - job_name: 'order-service'
    static_configs:
      - targets: ['order-service:8080']
  - job_name: 'payment-service'
    static_configs:
      - targets: ['payment-service:8081']
  - job_name: 'notification-service'
    static_configs:
      - targets: ['notification-service:8082']
```

---

## Step 6: Launch everything

```bash
docker compose up -d --build
docker compose ps   # Should show: jaeger, order-service, payment-service, notification-service, prometheus
```

---

## Step 7: Generate some traces

```bash
# Place 20 orders
for i in $(seq 1 20); do
  curl -s -X POST http://localhost:8080/api/orders > /dev/null
  sleep 0.3
done
```

---

## Step 8: Open Jaeger UI and explore traces

Open **http://localhost:16686** (Jaeger UI)

### Search for traces:
1. **Service** dropdown: select `order-service`
2. Click **Find Traces**
3. You'll see a list of traces with:
   - Trace ID
   - Total duration
   - Number of spans
   - Services involved

### Click on any trace to see the waterfall:

```
order-service: POST /api/orders ─────────────────────── 620ms
  ├── payment-service: POST /api/pay ────────────────── 420ms  ← BOTTLENECK
  │    └── (payment processing) ──────────────────────── 400ms
  └── notification-service: POST /api/notify ─────────── 150ms
       └── (send notification) ───────────────────────── 130ms
```

> **This is a trace waterfall!** Each bar is a **span**. The length shows duration. Nesting shows parent-child relationships. You can immediately see:
> - Total request time: 620ms
> - Payment took 420ms (68% of total) -- the **bottleneck**
> - Notification took 150ms
> - Order service's own work: ~50ms

> **Think About It:** Compare this to Lab 08 where you had to `grep` logs and manually piece together the timeline. The Jaeger waterfall shows the SAME information but visually and instantly. Which approach would you want at 2 AM?

---

## Step 9: Find slow traces

In the Jaeger UI:
1. Set **Service**: `order-service`
2. Set **Min Duration**: `1s`
3. Click **Find Traces**

This shows only traces that took more than 1 second. Click on one to see WHICH span was slow.

> **Quick Question:** If you find a trace where the total is 3 seconds and the payment span is 2.8 seconds, where should the team focus optimization efforts?

---

## Step 10: Find error traces

In the Jaeger UI:
1. Set **Service**: `order-service`
2. Set **Tags**: `error=true` or `http.status_code=500`
3. Click **Find Traces**

Error traces show red spans. Click on the red span to see the error details.

---

## Step 11: Compare trace with metrics

Open two tabs:
1. **Jaeger** (http://localhost:16686) -- individual request detail
2. **Prometheus** (http://localhost:9090) -- aggregate metrics

```promql
# In Prometheus: average payment duration
rate(payment_processing_seconds_sum[5m]) / rate(payment_processing_seconds_count[5m])
```

> **Discussion:** Metrics show "average payment time is 400ms." But Jaeger shows you that SOME payments take 800ms while others take 200ms. Metrics show the trend. Traces show individual outliers. Both are needed.

---

## Step 12: Service dependency graph

In Jaeger UI, click **System Architecture** (or **Dependencies** tab).

You'll see a graph showing:
```
order-service --> payment-service
order-service --> notification-service
```

This is automatically generated from trace data. In a system with 50 services, this dependency graph is invaluable for understanding how services are connected.

---

## Key Concept: Tracing in Production

| Aspect | This Lab | Production |
|--------|----------|-----------|
| Instrumentation | `--require tracing.js` (manual setup) | OTel Operator (K8s auto-injects) |
| Trace backend | Jaeger all-in-one | Jaeger with Elasticsearch/Cassandra, or Tempo, or DataDog APM |
| Sampling | 100% (trace everything) | 1-10% head sampling + tail sampling for errors |
| Storage | In-memory (lost on restart) | Elasticsearch or object storage (weeks of retention) |
| Scale | 3 services, 10 req/s | 50+ services, 10,000+ req/s |

---

## Cleanup

```bash
docker compose down
```

---

## The Three Pillars -- Now Complete

| Pillar | Lab | Tool | Answers |
|--------|-----|------|---------|
| **Metrics** | 02-04 | Prometheus + Grafana | "Error rate is 5%, p99 is 2s" (HOW MUCH) |
| **Logs** | 05 | Structured JSON + grep | "Order ORD-1234 failed with PaymentTimeout" (WHAT) |
| **Traces** | 08 + **08b** | Jaeger + OpenTelemetry | "Payment gateway span took 2.8s out of 3s total" (WHERE) |

### Incident debugging flow:
```
1. ALERT fires: "Error rate > 5%"               ← Metrics (Lab 06)
2. DASHBOARD shows: spike started at 14:23       ← Metrics (Lab 04)
3. JAEGER shows: payment spans are failing        ← Traces (Lab 08b)
4. LOGS show: "PaymentGateway: connection refused" ← Logs (Lab 05)
5. ROOT CAUSE: Payment gateway is down
6. ACTION: Enable fallback provider, notify vendor
```

---

## Discussion

1. What can you learn from a Jaeger trace waterfall that you CAN'T learn from metrics?
2. Why can't you trace 100% of requests at scale? (Storage cost, network overhead, performance impact)
3. If a trace shows order-service took 600ms total but all downstream spans add up to only 300ms, where did the other 300ms go? (In order-service's own code -- validations, serialization, queue wait time, etc.)
4. In production, would you still keep the manual `X-Trace-Id` from Lab 08? (Not needed -- OpenTelemetry handles propagation automatically. But understanding the concept from Lab 08 helps you debug tracing issues.)
