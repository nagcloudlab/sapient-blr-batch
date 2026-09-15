# Lab 05: Structured Logging (Second Pillar)
## 30 min | Prerequisite: Lab 02 (order-service)

---

## What You'll Learn
- Why structured (JSON) logging is essential for production
- How to implement a structured logger in Node.js
- Request IDs for correlating logs across a request's lifecycle
- Log levels: ERROR, WARN, INFO, DEBUG -- when to use each
- How to search and filter structured logs

## Why This Matters
Metrics (Lab 02-04) tell you THAT 5% of orders are failing. But WHICH orders? WHY? Logs answer these questions. In a 2 AM incident, after the dashboard tells you "error rate is high," your next step is always: "show me the error logs."

## New Terms

| Term | Meaning |
|------|---------|
| **Structured logging** | Writing logs in a machine-readable format (JSON) with consistent fields. Opposite of plain text logs like `"Error occurred"`. |
| **Unstructured log** | Plain text: `"Error processing order for user john"`. Can't be easily searched or filtered by a machine. |
| **Request ID** | A unique identifier assigned to each incoming request. Lets you find ALL log entries related to a single user action. |
| **Correlation** | Connecting related data across different sources. Example: "The error rate spike at 14:23 (metric) matches these payment timeout logs (log)." |
| **Log level** | Severity classification of a log entry. From most severe: FATAL > ERROR > WARN > INFO > DEBUG > TRACE. |
| **Log aggregation** | Collecting logs from all services into one searchable system. Tools: ELK (Elasticsearch + Logstash + Kibana), Loki, DataDog Logs. |
| **PII** | Personally Identifiable Information -- data like names, emails, phone numbers that must NEVER be logged for security/compliance reasons. |

---

## Structured vs Unstructured Logs

```
BAD (unstructured):
"Error processing order for user john"
--> Which order? When exactly? What error? Which service? Can't search programmatically.

GOOD (structured):
{"timestamp":"2026-09-15T10:23:46Z","level":"ERROR","service":"order-service",
 "requestId":"a1b2","orderId":"ORD-1234","error":"PaymentTimeout",
 "message":"Payment gateway timeout","duration_ms":5000}
--> Every field is searchable. Machines can parse it. Dashboards can aggregate it.
```

> **Quick Question:** If you had 10 million log lines and needed to find all payment timeouts that took more than 3 seconds -- which format (structured or unstructured) would make this possible?

---

## What Changed from Lab 02

| Change | Why |
|--------|-----|
| Added `log()` function | Consistent JSON output for every log entry |
| Added `crypto.randomUUID()` | Generate unique `requestId` for each request |
| Middleware now logs every request | Automatic audit trail with status code and duration |
| Business events logged with context | `orderId`, `error`, `duration_ms` in every log line |

---

## Step 1: Update the service with structured logging

Copy `order-service-v2.js` from this folder. Key sections explained:

### The structured logger
```javascript
function log(level, message, fields = {}) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),   // WHEN did it happen?
    level,                                  // How bad is it? (ERROR, WARN, INFO)
    service: 'order-service',              // WHICH service? (essential with 20+ services)
    ...fields,                             // Context: requestId, orderId, error, duration
    message                                // WHAT happened (human-readable)
  }));
}
```

> **Why these fields?**
> - `timestamp`: reconstruct the timeline of events
> - `level`: filter noise (only show ERRORs in production)
> - `service`: in microservices, you MUST know which service logged this
> - `requestId`: follow ONE request through all its log entries
> - `message`: human-readable summary for debugging

### Request ID generation
```javascript
app.use((req, res, next) => {
  req.requestId = crypto.randomUUID().substring(0, 8);
  // ...
});
```
> Every incoming request gets a unique 8-character ID. This ID appears in EVERY log entry for that request. In microservices, this becomes a **Trace ID** passed between services (Lab 08).

---

## Step 2: Rebuild and run

```bash
cd ~/obs-labs
docker stop order-service && docker rm order-service
cp order-service-v2.js order-service.js
docker build -t foodexpress-order:v2 .
docker run -d --name order-service -p 8080:8080 foodexpress-order:v2
```

---

## Step 3: Watch structured logs in real-time

Terminal 1 -- watch logs:
```bash
docker logs -f order-service
```

Terminal 2 -- generate traffic:
```bash
for i in $(seq 1 20); do curl -s -X POST http://localhost:8080/api/orders > /dev/null; sleep 0.2; done
```

You'll see JSON logs like:
```json
{"timestamp":"2026-09-15T10:23:45Z","level":"INFO","service":"order-service","requestId":"a1b2c3d4","orderId":"ORD-123","message":"Order placed","duration_ms":145}
{"timestamp":"2026-09-15T10:23:46Z","level":"ERROR","service":"order-service","requestId":"e5f6g7h8","orderId":"ORD-124","error":"PaymentGatewayTimeout","message":"Payment gateway timeout","duration_ms":5000}
```

---

## Step 4: Search and filter logs

```bash
# Only show errors
docker logs order-service 2>&1 | grep '"level":"ERROR"'

# Only show slow requests (> 1 second)
docker logs order-service 2>&1 | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        e = json.loads(line)
        if e.get('duration_ms', 0) > 1000: print(json.dumps(e))
    except: pass
"

# Follow one request by its requestId (pick one from the output above)
docker logs order-service 2>&1 | grep '"requestId":"a1b2c3d4"'

# Count errors vs successes
echo "Errors: $(docker logs order-service 2>&1 | grep '"level":"ERROR"' | wc -l)"
echo "Success: $(docker logs order-service 2>&1 | grep '"Order placed"' | wc -l)"
```

> **Think About It:** In production, tools like ELK or DataDog Logs give you a search UI for this. But the principle is the same -- structured JSON lets you filter by ANY field.

---

## Step 5: Exercise -- Log Levels

### Log Level Guide

| Level | When to use | On in production? | Example |
|-------|-------------|-------------------|---------|
| **ERROR** | Operation failed, needs attention | Always | Payment timeout, DB connection failed |
| **WARN** | Unexpected but recovered, needs investigation | Always | Retry succeeded on 2nd attempt, slow query |
| **INFO** | Normal business events | Usually | Order placed, user logged in |
| **DEBUG** | Developer troubleshooting detail | No (too verbose) | SQL query text, full request body |

### Exercise: Which level for each?

| Event | Level? | Why? |
|-------|--------|------|
| Order cancelled by user | ? | |
| Database query took 3 seconds (normal < 100ms) | ? | |
| Payment retry succeeded on 2nd attempt | ? | |
| Cannot connect to Redis cache, falling back to DB | ? | |
| User logged in successfully | ? | |

<details>
<summary>Answers</summary>

| Event | Level | Why |
|-------|-------|-----|
| Order cancelled by user | **INFO** | Normal business event -- user chose to cancel |
| Database query took 3 seconds | **WARN** | Working but abnormally slow -- needs investigation |
| Payment retry succeeded on 2nd attempt | **WARN** | Succeeded, but the retry indicates the gateway is unstable |
| Cannot connect to Redis, falling back to DB | **WARN** | Degraded performance but still working |
| User logged in successfully | **INFO** | Normal event, useful for audit trail |

</details>

---

## Logs vs Metrics -- When to Use Which

| Aspect | Metrics | Logs |
|--------|---------|------|
| **Answers** | "Error rate is 5%" | "Order ORD-1234 failed with PaymentTimeout" |
| **Shows** | Trends, patterns, aggregates | Individual events, details |
| **Storage cost** | Cheap (just numbers) | Expensive (text, high volume) |
| **Query speed** | Very fast | Slower (text search) |
| **Use for** | Dashboards, alerts, SLOs | Debugging, audit trails, forensics |
| **Cardinality** | Low (don't use user_id as label) | High (can include any field) |

**Both are needed.** Metrics tell you THERE'S a problem. Logs tell you WHAT the problem is.

> **Quick Question:** The Grafana dashboard shows error rate jumped to 15% at 2:00 PM. What's your next step? (Filter logs for `level=ERROR` between 2:00-2:05 PM, look for common error messages. This is metrics + logs working together.)

---

## Discussion

1. Why is `requestId` important? What would debugging look like without it?
2. What should you NEVER log? (Passwords, credit card numbers, PII -- security and compliance)
3. In production with 100,000 log lines per minute, how do you find the one that matters? (Structured logging + centralized search tools like ELK)

---

## What's Next

You have metrics (Labs 02-04) and logs (Lab 05). But you still need to be NOTIFIED when something goes wrong -- you can't stare at dashboards 24/7. In Lab 06, you'll create **Prometheus alert rules** that automatically detect problems and fire alerts.
