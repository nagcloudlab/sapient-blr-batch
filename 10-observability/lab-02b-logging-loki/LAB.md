# Lab 02b - Centralized Logging with Grafana Loki

## What You Will Learn

- How Loki differs from Elasticsearch (label-based vs full-text indexing)
- How Promtail collects and ships logs to Loki
- How to query logs using LogQL (similar to PromQL)
- How to use Grafana Explore to search and filter logs
- Why Loki is a lightweight alternative to ELK

## ELK vs Loki - Key Difference

```
ELK (Elasticsearch):
  - Indexes EVERY word in EVERY log line
  - Very fast full-text search
  - Heavy: needs 2-4GB RAM minimum
  - Stores: the full log content + full-text index

Loki:
  - Only indexes LABELS (service, level, container)
  - Log content is stored but NOT indexed
  - Lightweight: needs ~512MB RAM
  - Stores: labels (indexed) + compressed log chunks

Think of it like:
  Elasticsearch = Google (indexes everything, search any word)
  Loki          = Gmail labels (filter by label, then grep within)
```

## Architecture

```
  +-------------------+         +-------------------+
  |  Order Service    |  HTTP   | Payment Service   |
  |  (Node.js)        +-------->+  (Spring Boot)    |
  |  Winston JSON     |         |  Logback JSON     |
  |  port 3000        |         |  port 8080        |
  +--------+----------+         +--------+----------+
           |                             |
           | stdout (JSON logs)          | stdout (JSON logs)
           v                             v
  +------------------------------------------------+
  |        Docker Container Logs                    |
  +------------------------+-----------------------+
                           |
                           | tails via Docker socket
                           v
                  +-------------------+
                  |    Promtail       |
                  |  (log collector)  |
                  |  - discovers      |
                  |    containers     |
                  |  - extracts       |
                  |    labels from    |
                  |    JSON logs      |
                  |  - ships to Loki  |
                  +--------+----------+
                           |
                           | push logs + labels
                           v
                  +-------------------+
                  |      Loki         |
                  |  (log backend)    |
                  |  - stores logs    |
                  |  - indexes only   |
                  |    labels         |
                  |  - lightweight    |
                  |  port 3100        |
                  +--------+----------+
                           |
                           | LogQL queries
                           v
                  +-------------------+
                  |     Grafana       |
                  |  (same UI as      |
                  |   metrics lab!)   |
                  |  - Explore view   |
                  |  - log search     |
                  |  port 3001        |
                  +-------------------+
```

## How Promtail Discovers and Labels Logs

```
Promtail connects to Docker socket
          |
          v
Discovers all running containers
          |
          v
For each container, it:
  1. Reads the container log file
  2. Adds labels automatically:
     - container = "order-service"
     - service   = "order-service" (from docker-compose)
     - logstream = "stdout"
  3. Parses JSON and extracts more labels:
     - level        = "info" / "warn" / "error"
     - service_name = "order-service"
          |
          v
Pushes to Loki: { labels } + "log line"
```

## How To Run

```bash
# Start all services (Loki starts in ~10 seconds - much faster than ELK!)
sudo docker compose up --build -d

# Check all containers
sudo docker compose ps

# Check health
curl http://localhost:3000/health
curl http://localhost:8080/health

# Verify Loki is running
curl http://localhost:3100/ready
```

## How To Test

```bash
# Generate load
chmod +x generate-load.sh
./generate-load.sh 50

# Or manual
curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "laptop", "quantity": 1, "price": 999.99}'
```

## What To Observe in Grafana (localhost:3001)

### Step 1: Open Explore View
- Login: admin / admin
- Click the compass icon (Explore) in the left sidebar
- Select "Loki" as the datasource (top dropdown)

### Step 2: LogQL Queries

```
# All logs from order service
{service="order-service"}

# All logs from payment service
{service="payment-service"}

# Only error logs
{service=~"order-service|payment-service"} |= "ERROR"

# Only warning logs from payment service
{service="payment-service"} |= "WARN"

# Find logs for a specific order (grep within logs)
{service=~".*"} |= "paste-order-id-here"

# Parse JSON and filter by field
{service="order-service"} | json | level="error"

# Parse JSON and show specific fields
{service="payment-service"} | json | line_format "{{.orderId}} - {{.message}}"

# Count errors per service over time
count_over_time({service=~".+"} |= "ERROR" [1m])

# Log volume (rate of logs per service)
sum by (service) (rate({service=~".+"} [1m]))
```

### Step 3: Compare with Kibana

```
Kibana (KQL):                          Grafana Loki (LogQL):
  service: "order-service"               {service="order-service"}
  level: "error"                         {service=~".+"} |= "ERROR"
  orderId: "abc-123"                     {service=~".+"} |= "abc-123"
  message: "TIMEOUT"                     {service=~".+"} |= "TIMEOUT"
  statusCode > 400                       {service=~".+"} | json | statusCode > 400
```

## LogQL Syntax Explained

```
LogQL has two parts:

1. STREAM SELECTOR (like PromQL label selectors):
   {service="order-service"}              exact match
   {service=~"order.*"}                   regex match
   {service!="payment-service"}           not equal
   {service=~"order-service|payment-service"}  multiple

2. LOG PIPELINE (filter + transform):
   |= "error"                            line contains "error"
   != "health"                            line does NOT contain "health"
   |~ "TIMEOUT|FAILED"                   line matches regex
   | json                                 parse JSON fields
   | json | level="error"                parse then filter field
   | line_format "{{.message}}"          reformat output

Combined:
   {service="order-service"} |= "Payment" | json | level="error"

Metric queries (for dashboards):
   count_over_time({service="order-service"} |= "ERROR" [5m])
   rate({service=~".+"} [1m])
   sum by (level) (count_over_time({service=~".+"} | json [1m]))
```

## Why Choose Loki Over ELK?

```
+---------------------+------------------+------------------+
|                     | ELK              | Loki             |
+---------------------+------------------+------------------+
| RAM needed          | 4-8 GB           | 512MB - 1GB      |
| Startup time        | 60-90 seconds    | 5-10 seconds     |
| Storage             | Heavy (indexes   | Light (only      |
|                     | everything)      | indexes labels)  |
| Full-text search    | Very fast        | Slower (grep)    |
| Already use Grafana?| Need Kibana too  | Same Grafana!    |
| Scaling             | Complex          | Simple           |
| Best for            | Large orgs,      | Teams already    |
|                     | compliance,      | using Prometheus  |
|                     | full-text search | + Grafana stack  |
+---------------------+------------------+------------------+
```

## File Structure

```
lab-02b-logging-loki/
├── LAB.md
├── docker-compose.yml
├── generate-load.sh
├── order-service/                            # same as lab-02a
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       └── index.js
├── payment-service/                          # same as lab-02a
│   ├── Dockerfile
│   ├── pom.xml
│   └── src/main/...
├── loki/
│   └── loki-config.yml                      # Loki server config
├── promtail/
│   └── promtail-config.yml                  # Docker log discovery + JSON parsing
└── grafana/
    └── provisioning/
        └── datasources/
            └── datasource.yml               # Auto-configure Loki datasource
```

## Cleanup

```bash
sudo docker compose down
```
