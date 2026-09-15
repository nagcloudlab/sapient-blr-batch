# Lab 01: Why Observability?
## 25 min | No prerequisites beyond Node.js

---

## What You'll Learn
- What it feels like to debug a service with ZERO monitoring
- Why we need observability in production systems

## Why This Matters
In production, services fail silently. Users complain, but engineers can't answer basic questions like "how many requests are failing?" or "when did it start?" This lab makes you feel that pain firsthand.

## New Terms

| Term | Meaning |
|------|---------|
| **Monitoring** | Collecting and displaying data about a system to know if it's working right now |
| **Observability** | The ability to understand a system's internal state by looking at its external outputs (logs, metrics, traces) |
| **Incident** | An unplanned event that disrupts a service (e.g., orders failing at 2 AM) |
| **On-call** | An engineer assigned to respond to incidents outside business hours |
| **MTTR** | Mean Time To Recovery -- how long it takes to fix an incident (lower = better) |
| **MTTD** | Mean Time To Detect -- how long before you even KNOW there's a problem |

---

## Step 1: Run a service with no monitoring

```bash
mkdir -p ~/obs-labs && cd ~/obs-labs
```

Copy `blind-app.js` from this folder, or create it:

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/api/orders' && req.method === 'POST') {
    // 10% of requests fail silently
    if (Math.random() < 0.1) {
      res.writeHead(500);
      res.end(JSON.stringify({ error: 'Payment timeout' }));
      return;
    }
    // 5% of requests are extremely slow (3 seconds)
    const delay = Math.random() < 0.05 ? 3000 : Math.floor(Math.random() * 200);
    setTimeout(() => {
      res.writeHead(200);
      res.end(JSON.stringify({ orderId: `ORD-${Date.now()}`, status: 'placed' }));
    }, delay);
    return;
  }
  res.writeHead(200);
  res.end('FoodExpress Order Service');
});

server.listen(8080, () => console.log('Running on port 8080'));
```

```bash
node blind-app.js &
```

> **Quick Question:** Look at the code. Can you tell just by reading it what percentage of requests will fail? In a real production service with thousands of lines of code, could you figure this out by reading code alone?

---

## Step 2: Simulate real traffic

```bash
for i in $(seq 1 200); do
  curl -s -o /dev/null -w "%{http_code} %{time_total}s\n" -X POST http://localhost:8080/api/orders
  sleep 0.05
done
```

You'll see a mix of `200` and `500` responses with varying response times.

---

## Step 3: Try to answer these questions

Imagine you're the on-call engineer at 2 AM. Users are complaining. Try to answer:

| # | Question | Can you answer? | What you'd need |
|---|----------|----------------|-----------------|
| 1 | How many requests succeeded vs failed? | No | **Metrics** (counters) |
| 2 | What's the average response time? | No | **Metrics** (histogram) |
| 3 | What's the p99 latency (worst 1%)? | No | **Metrics** (percentiles) |
| 4 | When did failures start? | No | **Logs** (timestamps) |
| 5 | Which specific requests were slow and why? | No | **Traces** (request flow) |
| 6 | Is CPU/memory causing the problem? | No | **Infrastructure monitoring** |

### New Terms

| Term | Meaning |
|------|---------|
| **p99 latency** | The response time below which 99% of requests fall. If p99 = 2 seconds, then 99 out of 100 requests are faster than 2s, but 1 out of 100 is slower. It measures the WORST experience your users have. |
| **p50 latency** | The median -- 50% of requests are faster, 50% are slower. Also called the "typical" user experience. |
| **Percentile** | A way to describe where a value falls in a distribution. p95 = 95th percentile = "95% of values are below this." |

**You can't answer ANY of the questions above. This is running blind.**

> **Think About It:** If you can't answer these questions, how would you even begin debugging? What's your MTTD (time to detect) and MTTR (time to fix) when you have zero visibility?

---

## The Three Pillars of Observability

The questions in Step 3 map directly to three types of data:

```
+-----------+    +-----------+    +-----------+
|   LOGS    |    |  METRICS  |    |  TRACES   |
|           |    |           |    |           |
| WHAT      |    | HOW MUCH  |    | WHERE     |
| happened  |    | and WHEN  |    | time is   |
|           |    |           |    | spent     |
+-----------+    +-----------+    +-----------+
```

- **Metrics** answer questions 1-3 (numbers over time)
- **Logs** answer question 4 (timestamped event records)
- **Traces** answer question 5 (request journey across services)

All three are needed. Metrics tell you THERE'S a problem. Logs tell you WHAT the problem is. Traces tell you WHERE the problem is.

---

## Monitoring vs Observability

| | Monitoring | Observability |
|--|-----------|---------------|
| **Question it answers** | "Is it broken?" | "Why is it broken?" |
| **Approach** | Predefined checks, known patterns | Explore any question, unknown unknowns |
| **Analogy** | Car dashboard warning light | Mechanic's diagnostic tools |
| **Example** | "CPU is above 90%" alert | "Why are orders from Mumbai 3x slower than Delhi?" |

**One-liner:** Monitoring tells you SOMETHING is wrong. Observability tells you WHAT is wrong and WHY.

---

## Discussion

1. Have you ever tried to find a bug with no logs or monitoring data? What was that like?
2. Which pillar (logs, metrics, traces) do you think would have helped most?
3. If FoodExpress loses Rs. 50,000 per minute of downtime, and your MTTD is 30 minutes because you have no monitoring, how much money is lost before you even KNOW there's a problem?

---

## Cleanup

```bash
kill %1
```

## What's Next

In Lab 02, you'll add **metrics** to this same service and finally answer all the questions from Step 3.
