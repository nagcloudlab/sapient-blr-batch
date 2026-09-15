# Lab 02a - Centralized Logging with ELK Stack

## What You Will Learn

- Why centralized logging is essential for microservices
- What structured (JSON) logging is and why it beats plain text
- How Winston (Node.js) and Logback (Spring Boot) produce JSON logs
- What MDC (Mapped Diagnostic Context) is and why it matters
- How the ELK pipeline works: Filebeat -> Logstash -> Elasticsearch -> Kibana
- How to search, filter, and correlate logs across services in Kibana

## Architecture

```
  +-------------------+         +-------------------+
  |  Order Service    |  HTTP   | Payment Service   |
  |  (Node.js)        +-------->+  (Spring Boot)    |
  |  Winston JSON     |         |  Logback JSON     |
  |  port 3000        |         |  + MDC context    |
  +--------+----------+         +--------+----------+
           |                             |
           | stdout (JSON logs)          | stdout (JSON logs)
           v                             v
  +------------------------------------------------+
  |        Docker Container Logs                    |
  |   /var/lib/docker/containers/*/*.log            |
  +------------------------+-----------------------+
                           |
                           | tails log files
                           v
                  +-------------------+
                  |     Filebeat      |
                  |  (log shipper)    |
                  |  lightweight      |
                  |  agent            |
                  +--------+----------+
                           |
                           | sends over TCP
                           v
                  +-------------------+
                  |     Logstash      |
                  |  (log pipeline)   |
                  |  - parse JSON     |
                  |  - add fields     |
                  |  - transform      |
                  |  port 5000        |
                  +--------+----------+
                           |
                           | bulk index
                           v
                  +-------------------+
                  |  Elasticsearch    |
                  |  (search engine)  |
                  |  - full-text      |
                  |    indexing       |
                  |  - stores all     |
                  |    log fields     |
                  |  port 9200        |
                  +--------+----------+
                           |
                           | queries
                           v
                  +-------------------+
                  |     Kibana        |
                  |  (web UI)         |
                  |  - search logs    |
                  |  - build filters  |
                  |  - dashboards     |
                  |  port 5601        |
                  +-------------------+
```

## Structured vs Unstructured Logging

```
UNSTRUCTURED (plain text - hard to search):
  2024-01-15 10:30:00 INFO Payment completed for order abc-123, amount 999.99

  Problems:
  - How do you search for all logs for order abc-123?
  - How do you filter by amount > 500?
  - How do you count errors per service?
  - Every service formats differently


STRUCTURED (JSON - machine parseable):
  {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "level": "info",
    "service": "payment-service",
    "message": "Payment COMPLETED successfully",
    "orderId": "abc-123",
    "paymentId": "def-456",
    "amount": 999.99
  }

  Benefits:
  - Search by any field: orderId, amount, level, service
  - Aggregate: count errors per service per minute
  - Correlate: find all logs for one order across services
  - Parse: machines can read it automatically
```

## What Gets Logged (Failure Scenarios)

### Order Service Logs

| Level | Message | When |
|-------|---------|------|
| INFO | "Order created" | Every new order with orderId, item, quantity, amount |
| INFO | "Payment successful" | Payment service returned COMPLETED |
| WARN | "Invalid order request" | Missing item, quantity, or price (400) |
| WARN | "Payment declined" | Payment returned FAILED status |
| WARN | "Order not found" | GET /orders/:id with invalid ID (404) |
| ERROR | "Payment service TIMEOUT" | Payment took > 5 seconds |
| ERROR | "Payment service INTERNAL ERROR" | Payment returned 500 |
| ERROR | "Payment service UNREACHABLE" | Connection refused (service down) |

### Payment Service Logs (with MDC context)

| Level | Message | MDC Fields |
|-------|---------|------------|
| INFO | "Payment COMPLETED successfully" | orderId, paymentId, amount |
| WARN | "Invalid payment request" | - |
| WARN | "Payment DECLINED - insufficient funds" | orderId, paymentId, amount |
| WARN | "SLOW PROCESSING detected" | orderId, paymentId, amount |
| ERROR | "DATABASE CONNECTION FAILED" | orderId, paymentId, amount |
| ERROR | "GATEWAY TIMEOUT" | orderId, paymentId, amount |

## How MDC Works (Spring Boot)

```
Without MDC - you must manually add context to every log:
  log.info("Payment completed for order {} payment {} amount {}", orderId, paymentId, amount);
  log.info("Validating for order {} payment {}", orderId, paymentId);
  log.info("Saving for order {} payment {}", orderId, paymentId);
  // tedious, easy to forget

With MDC - set once, appears in ALL logs automatically:
  MDC.put("orderId", orderId);
  MDC.put("paymentId", paymentId);

  log.info("Payment completed");   // orderId and paymentId auto-included
  log.info("Validating");          // orderId and paymentId auto-included
  log.info("Saving");              // orderId and paymentId auto-included

  MDC.clear();  // clean up after request

Output JSON:
  {"message":"Payment completed","orderId":"abc-123","paymentId":"def-456"}
  {"message":"Validating","orderId":"abc-123","paymentId":"def-456"}
  {"message":"Saving","orderId":"abc-123","paymentId":"def-456"}
```

## How To Run

```bash
# Start all services (Elasticsearch takes ~60 seconds)
sudo docker compose up --build -d

# Check all containers are running
sudo docker compose ps

# Wait for Kibana to be ready
curl -s http://localhost:5601/api/status | grep -o '"level":"[^"]*"'

# Check service health
curl http://localhost:3000/health
curl http://localhost:8080/health
```

## How To Test

```bash
# Generate load (creates mix of success, failures, bad requests)
chmod +x generate-load.sh
./generate-load.sh 50

# Or manual tests
curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "laptop", "quantity": 1, "price": 999.99}'

# Trigger 400 (bad request)
curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "laptop"}'

# Trigger 404
curl http://localhost:3000/orders/does-not-exist
```

## What To Observe in Kibana (localhost:5601)

### Step 1: Create Index Pattern
- Go to Management > Stack Management > Index Patterns (or Data Views)
- Create pattern: `services-logs-*`
- Select `@timestamp` as time field

### Step 2: Discover Logs
- Go to Analytics > Discover
- Select the `services-logs-*` index pattern
- Set time range to "Last 15 minutes"
- You should see logs from both services

### Step 3: Search and Filter

```
# Find all errors
level: "error" OR level: "ERROR"

# Find all logs for a specific order
orderId: "paste-order-id-here"

# Find payment failures
message: "DECLINED" OR message: "TIMEOUT" OR message: "FAILED"

# Find slow requests (duration > 1000ms)
duration > 1000

# Find all 500 errors
statusCode: 500

# Logs from order service only
service: "order-service"
```

### Step 4: Correlate Across Services
1. Create an order and copy the orderId from the response
2. In Kibana, search for that orderId
3. You'll see logs from BOTH services for that single order:
   - Order Service: "Order created" -> "Payment successful" (or failed)
   - Payment Service: "Payment COMPLETED" (or DECLINED/TIMEOUT/ERROR)

## ELK Component Details

```
+----------+     +----------+     +---------------+     +--------+
| Filebeat |     | Logstash |     | Elasticsearch |     | Kibana |
+----------+     +----------+     +---------------+     +--------+
|          |     |          |     |               |     |        |
| - Reads  |---->| - Input: |---->| - Stores JSON |---->| - Web  |
|   Docker |     |   TCP    |     |   documents   |     |   UI   |
|   log    |     | - Filter:|     | - Full-text   |     | - KQL  |
|   files  |     |   parse  |     |   index on    |     |   query|
| - Light- |     |   JSON   |     |   EVERY field |     | - Dash-|
|   weight |     | - Output:|     | - Very fast   |     |   board|
| - No     |     |   Elastic|     |   searching   |     | - Viz  |
|   config |     |   search |     | - Heavy on    |     |        |
|   needed |     |          |     |   RAM + disk  |     |        |
+----------+     +----------+     +---------------+     +--------+
  ~50MB RAM       ~500MB RAM        2-4GB RAM             ~500MB
```

## File Structure

```
lab-02a-logging-elk/
├── LAB.md
├── docker-compose.yml
├── generate-load.sh
├── order-service/
│   ├── Dockerfile
│   ├── package.json                          # winston dependency
│   └── src/
│       └── index.js                          # Winston JSON logger + error handling
├── payment-service/
│   ├── Dockerfile
│   ├── pom.xml                               # logstash-logback-encoder
│   └── src/main/
│       ├── java/com/example/payment/
│       │   ├── PaymentServiceApplication.java
│       │   ├── Payment.java
│       │   └── PaymentController.java        # SLF4J + MDC + failure scenarios
│       └── resources/
│           ├── application.properties
│           └── logback-spring.xml            # LogstashEncoder for JSON output
├── filebeat/
│   └── filebeat.yml                          # Docker container log collection
└── logstash/
    ├── config/
    │   └── logstash.yml
    └── pipeline/
        └── logstash.conf                     # JSON parse + Elasticsearch output
```

## Cleanup

```bash
sudo docker compose down -v   # -v removes Elasticsearch data volume
```
