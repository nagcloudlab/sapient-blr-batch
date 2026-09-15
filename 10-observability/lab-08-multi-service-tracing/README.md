# Lab 08: Multi-Service Distributed Tracing (Third Pillar)
## 45 min | Prerequisite: Lab 07

---

## What You'll Learn
- How distributed tracing works (Trace ID propagation via HTTP headers)
- How to follow a single request across 3 microservices
- Why traces are the third pillar of observability
- How to identify which service is the bottleneck
- Comparing metrics across multiple services

## Why This Matters
In a monolith, a slow request stays in one process -- you can debug with a stack trace. In microservices, a single user action ("place order") calls 3-5 services. When it's slow or fails, WHICH service is responsible? Without distributed tracing, debugging microservices is like solving a mystery with half the clues missing.

## New Terms

| Term | Meaning |
|------|---------|
| **Distributed tracing** | Following a single request as it travels across multiple services. Shows the complete journey with timing for each step. |
| **Trace** | The complete end-to-end journey of one request across all services. Made up of multiple spans. |
| **Span** | A single unit of work within a trace. One service call, one database query, one cache lookup. Each span has a start time, end time, and status. |
| **Trace ID** | A unique identifier shared across ALL services for ONE request. Every log entry and span includes this ID so you can connect them. |
| **Context propagation** | Passing the Trace ID from one service to another via HTTP headers. Without this, each service's data is disconnected. |
| **Bottleneck** | The service or operation that takes the most time. In a trace, it's the longest span. If order takes 650ms total and payment takes 400ms of that, payment is the bottleneck. |
| **OpenTelemetry (OTel)** | The industry standard for instrumentation. Provides auto-instrumentation for many languages. In production, you'd use OTel instead of manual Trace ID headers. |
| **Jaeger** | An open-source distributed tracing tool (CNCF project). Collects and visualizes traces. Production alternative to grepping logs like we do in this lab. |

---

## Architecture

```
Client --POST /api/orders--> Order Service (8080)
                                  |
                                  +--POST /api/pay--> Payment Service (8081)
                                  |                     (200-800ms, 8% failure)
                                  |
                                  +--POST /api/notify--> Notification Service (8082)
                                                          (50-200ms)

    +-------- Trace ID passed in X-Trace-Id HTTP header --------+
```

> **Quick Question:** If the order endpoint takes 650ms total, and payment takes 400ms while notification takes 200ms, which service should you optimize first? (Payment -- it accounts for 62% of the total time.)

---

## What Changed from Lab 07

| Before (Lab 07) | Now (Lab 08) |
|-----------------|-------------|
| 1 service | 3 microservices (Order, Payment, Notification) |
| Standalone request handling | Order calls Payment, then Notification |
| requestId (local to one service) | **Trace ID** propagated across all 3 services via HTTP header |
| 1 set of metrics | 3 sets of metrics, one per service |

---

## Step 1: Understand context propagation

The key concept in this lab is how the Trace ID flows:

```javascript
// ORDER SERVICE: generates Trace ID, passes it downstream
const traceId = crypto.randomUUID().substring(0, 12);
await callService(PAYMENT_HOST, 8081, '/api/pay', data, traceId);
//                                                       ^^^^^^^^ passed in header

// Inside callService():
headers: { 'X-Trace-Id': traceId }   // <-- THE MAGIC: header carries the ID

// PAYMENT SERVICE: reads Trace ID from incoming header
const traceId = req.headers['x-trace-id'];
log('INFO', 'Payment received', { traceId });  // Same ID in logs!
```

> **Think About It:** In production, you wouldn't pass Trace IDs manually like this. OpenTelemetry does it automatically using the W3C Traceparent header standard. But understanding HOW it works under the hood is important.

---

## Step 2: Review the three services

Copy all files from this folder: `order-service-v3.js`, `payment-service.js`, `notification-service.js`, `package.json`, `Dockerfile`, `docker-compose.yml`, `prometheus.yml`, and `grafana-provisioning/`.

Key behaviors:
- **Order Service** (8080): Generates Trace ID, calls Payment then Notification
- **Payment Service** (8081): 200-800ms latency, 8% failure rate
- **Notification Service** (8082): 50-200ms latency, no failures

---

## Step 3: Launch with Docker Compose

```bash
cd ~/obs-labs/lab-08-multi-service-tracing   # or wherever your files are
docker compose up -d --build
docker compose ps   # All 5 services should be running
```

---

## Step 4: Place an order and get a Trace ID

```bash
curl -s -X POST http://localhost:8080/api/orders | python3 -m json.tool
```

Output:
```json
{
  "orderId": "ORD-1726398225123",
  "status": "placed",
  "traceId": "a1b2c3d4e5f6",
  "total_ms": 450
}
```

> Note the `traceId` in the response. This same ID was passed to Payment and Notification via HTTP headers.

---

## Step 5: Trace the request across all 3 services

Copy the `traceId` from Step 4 and search across ALL service logs:

```bash
docker compose logs | grep "a1b2c3d4e5f6" | sort
```

Output -- **the complete journey of this single request**:
```
order-service        | {"service":"order-service",       "traceId":"a1b2c3d4e5f6","message":"Order received"}
order-service        | {"service":"order-service",       "traceId":"a1b2c3d4e5f6","message":"Calling payment service"}
payment-service      | {"service":"payment-service",     "traceId":"a1b2c3d4e5f6","message":"Payment request received"}
payment-service      | {"service":"payment-service",     "traceId":"a1b2c3d4e5f6","message":"Payment processed","duration_ms":450}
order-service        | {"service":"order-service",       "traceId":"a1b2c3d4e5f6","message":"Calling notification service"}
notification-service | {"service":"notification-service","traceId":"a1b2c3d4e5f6","message":"Notification sent","duration_ms":120}
order-service        | {"service":"order-service",       "traceId":"a1b2c3d4e5f6","message":"Order completed","total_ms":620}
```

**This is distributed tracing!** One ID, three services, complete story.

> **Think About It:** Without the Trace ID, how would you connect these 7 log lines from 3 different containers? You couldn't. Each service's logs would be isolated, and debugging a slow order would mean guessing which payment and notification logs matched.

---

## Step 6: Generate load and compare services

```bash
for i in $(seq 1 100); do
  curl -s -X POST http://localhost:8080/api/orders > /dev/null
  sleep 0.1
done
```

In Prometheus (`http://localhost:9090`):

```promql
# Which service has the highest error rate?
rate(payments_total{status="failed"}[5m]) / rate(payments_total[5m]) * 100

# Which service is the slowest (bottleneck)?
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(payment_processing_seconds_bucket[5m]))
```

---

## Step 7: Find the failure source

```bash
docker compose logs | grep '"level":"ERROR"' | head -10
```

> **Quick Question:** When an order fails, the user sees "order failed." The order-service logs say "payment error." But where's the ROOT CAUSE? (In the payment-service logs -- grep for the same traceId to find the actual error message like "InsufficientFunds".)

---

## How the Three Pillars Work Together

```
1. METRICS (Grafana):  Error rate spiked to 8% at 14:23
2. TRACES (Trace ID):  Failed requests all show payment-service timing out
3. LOGS (grep):         payment-service logs show "InsufficientFunds" errors
4. ROOT CAUSE:          Payment gateway rejecting cards from a specific bank
5. ACTION:              Contact bank, enable fallback payment provider
```

No single pillar could solve this alone:
- Metrics alone: "Something is broken" (but what?)
- Traces alone: "Payment is failing" (but why?)
- Logs alone: "InsufficientFunds error" (but how widespread? when did it start?)

---

## Cleanup

```bash
docker compose down
```

---

## Discussion

1. What's the difference between a `requestId` (Lab 05) and a `traceId` (this lab)? (requestId is local to one service. traceId crosses service boundaries.)
2. If the order service takes 650ms total, and payment takes 400ms, what percentage of time is spent in payment? How would you reduce total latency?
3. At 10,000 requests/second, can you trace EVERY request? (No -- you'd use sampling: trace 10% of requests, but always trace errors and slow requests.)

---

## What's Next

In Lab 08b, you'll set up **Jaeger + OpenTelemetry** for production-grade tracing -- waterfall visualization, span timings, and service dependency graphs (instead of grepping logs manually).

Then Lab 09 covers fixing **buggy observability configs**, and Lab 10 deploys everything on **Kubernetes** with automatic service discovery.
