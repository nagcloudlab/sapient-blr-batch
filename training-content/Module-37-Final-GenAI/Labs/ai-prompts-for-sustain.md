# AI Prompt Library for Sustain Engineering
## FoodExpress Context

> AI assists, humans decide. Always verify. Never paste PII or credentials.

This library provides ready-to-use prompts for common sustain engineering tasks on the FoodExpress
platform. Copy, adapt the bracketed placeholders, and paste into your AI tool of choice.

---

## Table of Contents

1. Log Analysis
2. Incident Communication Draft
3. Post-Mortem Draft
4. Code Review and Bug Investigation
5. Query Optimization
6. Runbook Generation
7. Test Case Generation
8. AI Tools Reference

---

## 1. Log Analysis

### When to use
During active incidents or post-incident review when you have raw logs and need to quickly identify
error patterns, correlate events, and form a root cause hypothesis.

### Prompt template

```
Analyze these application logs and identify:

1. Error patterns and frequency -- which errors appear most often, in what sequence
2. Root cause hypothesis -- what is the most likely underlying cause
3. Affected users/orders -- estimate scope from user IDs, order IDs, or session tokens visible
4. Recommended immediate actions -- what to do in the next 15 minutes to stop the bleeding

Context:
- Service: [Order Service / Payment Service / Restaurant Service / Delivery Tracking]
- Environment: [production / staging]
- Time window: [e.g., 2026-07-27 02:10 to 02:40 IST]
- Known recent changes: [e.g., deployed v2.4.1 at 01:55 IST]

Logs:
[PASTE LOGS HERE -- remove any PII, passwords, or API keys before pasting]
```

### FoodExpress example log snippet (safe to use in training)

```
2026-07-27T02:17:43Z ERROR OrderService - DB connection timeout after 30000ms pool=main
2026-07-27T02:17:43Z ERROR OrderService - Failed to place order orderId=null userId=USR-XXXX
2026-07-27T02:17:44Z WARN  ConnectionPool - Active connections: 50/50 waiting: 127
2026-07-27T02:17:45Z ERROR PaymentService - Upstream OrderService returned 503
2026-07-27T02:17:46Z ERROR NotificationService - Cannot send confirmation, order not created
```

### What to look for in the AI response
- It should identify "connection pool exhaustion" as the root cause signal
- It should note the cascade: Order -> Payment -> Notification
- It should recommend: increase pool size OR reduce connection hold time OR restart service pod

---

## 2. Incident Communication Draft

### When to use
After you understand the impact and status of an incident, when you need to draft a stakeholder
email or Slack message for a non-technical audience quickly.

### Prompt template

```
Write a stakeholder communication email for the following incident.
Use plain English -- no technical jargon. Be factual and reassuring without minimizing impact.

Incident details:
- Service: FoodExpress Order Service
- Impact: Orders were not processing for 45 minutes
- Start time: 2026-07-27 02:17 IST
- Resolution time: 2026-07-27 03:02 IST
- Root cause: Database connection pool exhausted due to a long-running batch job
  competing with live traffic
- Current status: Resolved -- all orders are processing normally
- Affected scope: Approximately 1,200 orders failed or were delayed
- Audience: Client leadership (non-technical)

Format: Professional email. Subject line + body. Approximately 150 words.
Include: what happened, impact, what we did, current status, next steps.
Do NOT include: stack traces, config values, internal hostnames.
```

### Prompt variant -- Slack message for engineering channel

```
Write a brief Slack message for the #incidents channel summarizing:
- Service: [service name]
- Status: [INVESTIGATING / MITIGATED / RESOLVED]
- Impact: [one sentence]
- What we know so far: [one to two sentences]
- Next update in: [X minutes]

Tone: factual, calm, no panic language.
```

---

## 3. Post-Mortem Draft

### When to use
Within 24-48 hours of a resolved incident, to produce a blameless post-mortem document that the
team can review and act on.

### Prompt template

```
Create a blameless post-mortem document for the following incident.
Focus on systems, processes, and tooling -- not individual blame.

Incident summary:
- Title: Payment Service memory leak caused 20-minute outage
- Date: 2026-07-27
- Duration: 20 minutes (02:17 to 02:37 IST)
- Severity: P1
- Services affected: PaymentService, OrderService (downstream)
- Root cause: Unbounded array growth in the retry handler -- each failed payment attempt
  appended the full request payload to an in-memory retryQueue array without eviction.
  After 3 hours of elevated error rate, heap exhausted and the Node.js process crashed.

Include these sections:
1. Incident timeline (use times relative to T=0 detection)
2. Root cause analysis (use the 5 Whys technique)
3. Impact summary (users, orders, revenue estimate)
4. What went well
5. What went wrong
6. Action items (owner, due date placeholders)
7. Lessons learned

Tone: blameless, analytical, constructive.
```

### 5 Whys starter for FoodExpress (include in prompt or do manually)

```
Walk through 5 Whys for: "The Payment Service crashed at 02:17 IST"

Seed answers:
- Why 1: Heap memory exhausted
- Why 2: retryQueue array grew without bound
- Why 3: No eviction policy or size cap on the array
- Why 4: Code review did not catch the unbounded growth pattern
- Why 5: No memory profiling in the CI pipeline or load tests

Let the AI complete or extend the chain and suggest the systemic fix at each level.
```

---

## 4. Code Review and Bug Investigation

### When to use
When inheriting unfamiliar code, investigating a reported bug, or doing a pre-deployment review
on a sustain engineering change.

### Prompt template -- Node.js

```
Review the following Node.js code from the FoodExpress [OrderService / PaymentService /
RestaurantService / DeliveryTrackingService] and identify:

1. Memory leaks -- event listeners not removed, closures holding references, unbounded arrays
2. Unhandled promise rejections -- missing .catch() or try/catch in async functions
3. NoSQL injection risks -- unsanitized user input passed to MongoDB queries
4. Race conditions -- concurrent writes to shared state without locks
5. Performance bottlenecks -- N+1 query patterns, missing indexes, synchronous blocking calls
6. Missing input validation -- no schema validation on request bodies

For each issue found:
- Line reference or code snippet
- Severity (Critical / High / Medium / Low)
- Explanation of why it is a problem
- Suggested fix

Code:
[PASTE CODE HERE]
```

### Prompt template -- Java

```
Review the following Java code from the FoodExpress backend and identify:

1. Memory leaks -- unclosed streams, connections not returned to pool, static collections growing
2. SQL injection risks -- string concatenation in JDBC queries instead of PreparedStatement
3. Null pointer risks -- missing null checks before dereferencing
4. Thread safety issues -- shared mutable state accessed from multiple threads
5. Exception handling -- swallowed exceptions, overly broad catch blocks
6. Resource management -- missing try-with-resources for AutoCloseable objects

Code:
[PASTE CODE HERE]
```

### Example FoodExpress bug to paste (safe training example)

```javascript
// OrderService - route handler
app.post('/api/orders', async (req, res) => {
  const { restaurantId, items } = req.body;
  // BUG: no input validation, no sanitization
  const restaurant = await db.collection('restaurants').findOne({ _id: restaurantId });
  const order = await db.collection('orders').insertOne({ restaurantId, items, status: 'pending' });
  res.json(order);
  // BUG: no try/catch, unhandled rejection if db fails
});
```

---

## 5. Query Optimization

### When to use
When a specific MongoDB or MySQL query is identified as slow (via slow query logs, APM, or Grafana).

### Prompt template -- MongoDB

```
Optimize this MongoDB query for the FoodExpress Orders collection.
The collection has approximately 5 million documents.

Current query:
[PASTE QUERY]

Schema context:
- orders: { _id, customerId, restaurantId, status, createdAt, items: [...], totalAmount }
- restaurants: { _id, name, cuisineType, city, isActive, averageRating }
- menu_items: { _id, restaurantId, name, price, category, isAvailable }

Tell me:
1. What indexes are missing
2. Whether the query does a collection scan
3. Rewritten query with projection (fetch only needed fields)
4. Suggested index definition (db.collection.createIndex)
5. Expected performance improvement
```

### Prompt template -- MySQL

```
Optimize this MySQL query for the FoodExpress database.
The orders table has approximately 8 million rows.

Current query:
[PASTE QUERY]

Table schemas:
- orders (id, customer_id, restaurant_id, status, created_at, total_amount, delivery_address_id)
- restaurants (id, name, city, cuisine_type, is_active)
- order_items (id, order_id, menu_item_id, quantity, unit_price)
- menu_items (id, restaurant_id, name, category, price, is_available)

Tell me:
1. EXPLAIN plan interpretation -- which steps are full table scans
2. Missing indexes
3. Rewritten query if a JOIN or subquery can be improved
4. Suggested index DDL statements
```

### FoodExpress slow query example (training use)

```javascript
// Slow: fetches ALL orders then filters in app code
const allOrders = await db.collection('orders').find({}).toArray();
const pending = allOrders.filter(o => o.status === 'pending' && o.restaurantId === id);

// Ask AI to rewrite using a compound index on { restaurantId: 1, status: 1 }
```

---

## 6. Runbook Generation

### When to use
When a new alert type appears repeatedly and no runbook exists, or when updating a stale runbook
after a postmortem identifies gaps.

### Prompt template

```
Create a runbook for handling the following alert in the FoodExpress production environment.

Alert name: Order Service connection pool exhaustion
Alert condition: Active DB connections >= 45 out of pool max 50, sustained for 2 minutes
Severity: P1
Service: OrderService (Node.js, MongoDB Atlas, Kubernetes pod)

Include these sections:
1. Alert meaning -- what this alert tells us in plain English
2. Immediate triage steps -- first 5 minutes, what to check and in what order
3. Common causes -- list the 3-5 most likely root causes with how to confirm each
4. Remediation steps -- step-by-step commands and actions, including kubectl and mongo shell
5. Escalation path -- when to escalate and to whom
6. Prevention -- long-term fixes to reduce recurrence
7. Related alerts -- other alerts that commonly fire at the same time

Format: Numbered steps. Include exact commands where possible.
Use placeholders like [NAMESPACE] and [POD_NAME] for environment-specific values.
```

### FoodExpress runbook stubs (expand with AI)

Common runbooks needed for FoodExpress:
- Payment Service 5xx spike
- Restaurant Service slow response (P95 latency > 2s)
- Delivery Tracking WebSocket disconnects
- Order Service pod OOMKilled
- MongoDB Atlas connection limit reached
- Redis cache miss rate > 80%

---

## 7. Test Case Generation

### When to use
Before a deployment, after a bug fix, or when writing tests for a legacy endpoint that has no
coverage. Use to quickly generate a comprehensive test suite skeleton.

### Prompt template -- REST endpoint

```
Generate test cases for the following FoodExpress API endpoint.
Provide both positive (happy path) and negative (error/edge) cases.

Endpoint: POST /api/orders
Request body schema:
{
  "customerId": "string (required)",
  "restaurantId": "string (required)",
  "items": [
    { "menuItemId": "string", "quantity": "integer >= 1" }
  ],
  "deliveryAddress": {
    "street": "string",
    "city": "string",
    "pincode": "string (6 digits)"
  },
  "paymentMethod": "CARD | UPI | CASH_ON_DELIVERY"
}

For each test case provide:
- Test case ID and name
- Input data
- Expected HTTP status code
- Expected response body (key fields)
- What is being validated

Categories to cover:
- Happy path (valid order created)
- Missing required fields
- Invalid data types
- Empty items array
- Restaurant not found
- Menu item not available
- Customer not found
- Payment method invalid
- Database failure simulation
- Concurrent duplicate order (idempotency)
```

### Prompt variant -- unit test code generation

```
Write Jest unit tests for the following Node.js function from FoodExpress OrderService.
Use describe/it blocks. Mock the database calls with jest.mock().
Cover: success path, validation failure, database error, edge cases.

Function:
[PASTE FUNCTION]
```

---

## 8. AI Tools Reference

The following AI tools are used at different points in the FoodExpress training programme.

| Tool | Primary Use in Programme | Modules |
|---|---|---|
| GitHub Copilot | Code completion, boilerplate generation, test stubs | M03, M05, M09, M22 |
| ChatGPT / Claude | Prompt-based tasks: incident drafts, postmortems, runbooks, code review | M13, M20, M35, M37 |
| Gemini Code Assist | IDE-integrated review, Google Cloud context | M18, M22 |
| Sonar AI | Automated code quality and security scan in CI pipeline | M16, M25 |
| Datadog AI | Anomaly detection, alert correlation, suggested remediations | M29, M31 |
| Grafana Sift | Root cause analysis from metrics and traces | M29, M31 |

### Ground rules for AI use in sustain engineering

1. Never paste PII (customer names, addresses, phone numbers, email, order details with identifiers).
2. Never paste credentials (API keys, passwords, connection strings, tokens).
3. Always review AI output before applying -- AI can hallucinate commands, flag false positives, or
   miss context it was not given.
4. Use AI to accelerate, not to replace -- the sustain engineer owns the decision and the fix.
5. Document AI-assisted fixes in the change record so the team knows what was done.
6. In a P1 incident, use AI for drafts and suggestions while a human leads the bridge call.

---

> AI assists, humans decide. Always verify. Never paste PII or credentials.
