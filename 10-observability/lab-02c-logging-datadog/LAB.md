# Lab 02c - Centralized Logging with Datadog

## What You Will Learn

- How Datadog Agent collects logs from Docker containers
- How Datadog auto-discovers containers and their logs
- How a fully managed SaaS logging solution works
- How Datadog compares to self-hosted ELK and Loki

## Prerequisites

- A Datadog account (free trial at datadoghq.com - 14 day trial)
- A Datadog API key

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
                           | reads via Docker socket
                           v
                  +-------------------+
                  |  Datadog Agent    |
                  |  (runs locally)   |
                  |  - auto-discovers |
                  |    containers     |
                  |  - parses JSON    |
                  |  - adds tags      |
                  |  - buffers +      |
                  |    compresses     |
                  +--------+----------+
                           |
                           | HTTPS (encrypted)
                           | sends to Datadog cloud
                           v
                  +-------------------+
                  |  Datadog Cloud    |
                  |  (SaaS)           |
                  |  - stores logs    |
                  |  - indexes        |
                  |  - dashboards     |
                  |  - alerts         |
                  |  - APM            |
                  |  app.datadoghq.com|
                  +-------------------+

  Key difference from ELK/Loki:
  - No Elasticsearch/Loki to manage
  - No Kibana/Grafana to set up
  - Everything is managed by Datadog
  - You just run the agent + pay per GB
```

## How Datadog Auto-Discovery Works

```
Datadog Agent connects to Docker socket
          |
          v
Discovers all running containers
          |
          v
Reads container labels for config:
  com.datadoghq.ad.logs: '[{
    "source": "nodejs",           <-- tells DD how to parse logs
    "service": "order-service"    <-- service name in DD UI
  }]'
          |
          v
Collects logs, adds tags:
  - container_name: order-service
  - service: order-service
  - source: nodejs
  - docker_image: order-service:latest
          |
          v
Ships to Datadog Cloud via HTTPS
```

## How To Run

### Step 1: Get Your Datadog API Key
1. Sign up at https://www.datadoghq.com (free 14-day trial)
2. Go to Organization Settings > API Keys
3. Create a new API key or copy existing one

### Step 2: Set API Key and Start

```bash
# Set your Datadog API key
export DD_API_KEY=your-api-key-here

# Start all services
sudo -E docker compose up --build -d
# (-E preserves the DD_API_KEY environment variable)

# Check agent status
sudo docker compose logs datadog-agent | tail -20

# Check service health
curl http://localhost:3000/health
curl http://localhost:8080/health
```

### Step 3: Generate Load

```bash
chmod +x generate-load.sh
./generate-load.sh 50
```

## What To Observe in Datadog UI (app.datadoghq.com)

### Step 1: Live Tail
- Go to Logs > Live Tail
- You should see logs streaming in real-time from both services
- Notice the auto-parsed JSON fields

### Step 2: Log Explorer
- Go to Logs > Explorer
- Try these searches:

```
# All logs from order service
service:order-service

# All errors
status:error

# Find a specific order
@orderId:paste-order-id-here

# Payment failures
service:payment-service @message:*DECLINED*

# Slow requests
@duration:>1000

# Combine filters
service:order-service status:error @message:*TIMEOUT*
```

### Step 3: Log Patterns
- Datadog automatically groups similar log lines into patterns
- Go to Logs > Patterns
- See which log messages are most frequent

### Step 4: Log Analytics
- Go to Logs > Analytics
- Group by: service, status
- Visualize error rate over time

## ELK vs Loki vs Datadog Comparison

```
+-------------------+----------------+----------------+------------------+
|                   | ELK            | Loki           | Datadog          |
+-------------------+----------------+----------------+------------------+
| Deploy            | Self-hosted    | Self-hosted    | SaaS (nothing    |
|                   | 4-6 containers | 3 containers   | to host)         |
+-------------------+----------------+----------------+------------------+
| RAM needed        | 4-8 GB         | 512MB-1GB      | Agent: ~256MB    |
+-------------------+----------------+----------------+------------------+
| Setup time        | 30 min         | 10 min         | 5 min            |
+-------------------+----------------+----------------+------------------+
| Log storage       | You manage     | You manage     | Datadog manages  |
+-------------------+----------------+----------------+------------------+
| Retention         | You configure  | You configure  | Based on plan    |
|                   | (disk space)   | (disk space)   | (15 days free)   |
+-------------------+----------------+----------------+------------------+
| Search speed      | Very fast      | Moderate       | Very fast        |
|                   | (full-text     | (label filter  | (full-text       |
|                   |  indexed)      |  + grep)       |  indexed)        |
+-------------------+----------------+----------------+------------------+
| Query language    | KQL / Lucene   | LogQL          | Datadog search   |
+-------------------+----------------+----------------+------------------+
| Cost              | Free (infra    | Free (infra    | $$$              |
|                   | costs only)    | costs only)    | (~$0.10/GB/day)  |
+-------------------+----------------+----------------+------------------+
| Extras included   | Kibana viz     | Grafana viz    | APM, Metrics,    |
|                   |                |                | Alerts, AI,      |
|                   |                |                | Dashboards       |
+-------------------+----------------+----------------+------------------+
| Best for          | Large orgs     | Prometheus     | Teams that want  |
|                   | with ops team  | + Grafana      | zero ops, have   |
|                   |                | users          | budget           |
+-------------------+----------------+----------------+------------------+
```

## How Docker Labels Configure Datadog

```yaml
# In docker-compose.yml, these labels tell the agent how to handle logs:
labels:
  com.datadoghq.ad.logs: '[{
    "source": "nodejs",           # Log source (parsing rules)
    "service": "order-service",   # Service name in Datadog
    "tags": ["env:lab"]           # Optional extra tags
  }]'

# source values:
#   "nodejs"  -> Datadog knows to parse Node.js log format
#   "java"    -> Datadog knows to parse Java/Spring log format
#   "python"  -> Datadog knows to parse Python log format
```

## File Structure

```
lab-02c-logging-datadog/
├── LAB.md
├── docker-compose.yml                        # Services + Datadog Agent
├── generate-load.sh
├── order-service/                            # same as lab-02a
│   ├── Dockerfile
│   ├── package.json
│   └── src/
│       └── index.js
└── payment-service/                          # same as lab-02a
    ├── Dockerfile
    ├── pom.xml
    └── src/main/...
```

Notice: No Elasticsearch, no Logstash, no Kibana, no Loki, no Promtail, no Grafana.
Just the Datadog Agent - everything else is in the cloud.

## Cleanup

```bash
sudo docker compose down
```
