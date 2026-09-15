# Lab 03 - OpenTelemetry: Unified Metrics, Logs & Traces

## What You Will Learn

- What OpenTelemetry (OTel) is and why it's the industry standard
- How OTel collects all 3 pillars: metrics, logs, and traces
- How the OTel Collector works as a central pipeline
- How to instrument Node.js with OTel SDK (traces + metrics + logs)
- How to instrument Spring Boot with OTel Java Agent (zero code changes)
- How to export to multiple backends (Jaeger, Prometheus, Loki)
- How to correlate traces, metrics, and logs in Grafana

## The Problem OTel Solves

```
Before OpenTelemetry:
  +----------+     +-- Prometheus client ---> Prometheus
  | Your App |-----|-- Jaeger client -------> Jaeger
  +----------+     +-- Fluentd/Filebeat ----> Elasticsearch

  Problems:
  - 3 different libraries to install
  - 3 different configs to maintain
  - 3 different data formats
  - No correlation between metrics, logs, and traces
  - Vendor lock-in (switching backends = rewrite instrumentation)


After OpenTelemetry:
  +----------+     +-- OTel SDK ---> OTel Collector ---> Any Backend
  | Your App |-----|                      |
  +----------+     (one library)          +---> Jaeger (traces)
                   (one config)           +---> Prometheus (metrics)
                   (one protocol: OTLP)   +---> Loki (logs)

  Benefits:
  - ONE library for all 3 signals
  - ONE protocol (OTLP) to send everything
  - Collector routes to ANY backend
  - Switch backends without changing app code
  - Traces, metrics, logs are CORRELATED (same trace_id)
```

## Architecture

```
  +-------------------+         +-------------------+
  |  Order Service    |  HTTP   | Payment Service   |
  |  (Node.js)        +-------->+  (Spring Boot)    |
  |  port 3000        |         |  port 8080        |
  |                   |         |                   |
  |  OTel SDK         |         |  OTel Java Agent  |
  |  (in code)        |         |  (zero code!)     |
  +--------+----------+         +--------+----------+
           |                             |
           |  OTLP (HTTP :4318)          |  OTLP (gRPC :4317)
           |  traces + metrics + logs    |  traces + metrics + logs
           v                             v
  +------------------------------------------------+
  |          OpenTelemetry Collector                |
  |          (central pipeline)                     |
  |                                                 |
  |  receivers:   OTLP (gRPC + HTTP)               |
  |  processors:  batch (buffer + send in bulk)     |
  |  exporters:   see below                         |
  +-----+------------------+------------------+----+
        |                  |                  |
        | traces           | metrics          | logs
        v                  v                  v
  +-----------+    +------------+    +-----------+
  |  Jaeger   |    | Prometheus |    |   Loki    |
  |  :16686   |    |  :9090     |    |  :3100    |
  +-----------+    +------------+    +-----------+
        \               |                /
         \              |               /
          v             v              v
        +-----------------------------------+
        |            Grafana                |
        |          port 3001                |
        |                                   |
        |  All 3 datasources in ONE UI:     |
        |  - Prometheus (metrics)           |
        |  - Loki (logs)                    |
        |  - Jaeger (traces)               |
        +-----------------------------------+
```

## OTel Collector Pipeline Explained

```
The collector has 3 stages:

  RECEIVERS          PROCESSORS         EXPORTERS
  (how data          (transform         (where data
   comes in)          in flight)         goes out)

  +----------+      +----------+      +---------------+
  | OTLP     |      | batch    |      | otlp/jaeger   | --> Jaeger
  | gRPC     +----->+          +----->+ prometheus    | --> Prometheus
  | HTTP     |      | (buffer  |      | loki          | --> Loki
  +----------+      |  & send  |      | debug         | --> console
                    |  in bulk)|      +---------------+
                    +----------+

Config file (otel-collector-config.yml):

  service:
    pipelines:
      traces:                          <-- pipeline for traces
        receivers: [otlp]
        processors: [batch]
        exporters: [otlp/jaeger]

      metrics:                         <-- pipeline for metrics
        receivers: [otlp]
        processors: [batch]
        exporters: [prometheus]

      logs:                            <-- pipeline for logs
        receivers: [otlp]
        processors: [batch]
        exporters: [loki]
```

## Two Instrumentation Approaches

```
+---------------------------+----------------------------+
| Node.js: OTel SDK         | Java: OTel Java Agent      |
+---------------------------+----------------------------+
|                           |                            |
| Install npm packages      | Download ONE .jar file     |
| Write telemetry.js file   | Add -javaagent flag        |
| Import in code for        | ZERO code changes          |
| custom metrics/spans      |                            |
|                           |                            |
| Auto-instruments:         | Auto-instruments:          |
| - Express                 | - Spring MVC               |
| - Axios                   | - JDBC                     |
| - http module             | - Logback (captures logs!) |
|                           | - RestTemplate             |
| Manual for:               | - Kafka, gRPC, etc.        |
| - Custom metrics          |                            |
| - Custom spans            | Also captures:             |
| - Log export via API      | - JVM metrics (heap, GC)   |
|                           | - System metrics (CPU)     |
+---------------------------+----------------------------+

Node.js (telemetry.js - loaded before app):
  const sdk = new NodeSDK({
    traceExporter,     // sends traces via OTLP
    metricReader,      // sends metrics via OTLP
    logRecordProcessor,// sends logs via OTLP
    instrumentations,  // auto-wrap Express, Axios
  });
  sdk.start();

Java (just a JVM flag - no code changes):
  java -javaagent:opentelemetry-javaagent.jar \
       -jar app.jar

  Environment variables configure it:
    OTEL_SERVICE_NAME=payment-service
    OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317
```

## How To Run

```bash
sudo docker compose up --build -d

# Check all 8 containers are running
sudo docker compose ps

# Wait for Spring Boot (~30s) then check health
curl http://localhost:3000/health
curl http://localhost:8080/health
```

## How To Test

```bash
chmod +x generate-load.sh
./generate-load.sh 50

# Or manual
curl -X POST http://localhost:3000/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "laptop", "quantity": 1, "price": 999.99}'
```

## What To Observe

### 1. Traces in Jaeger (localhost:16686)

- Select service: `order-service` > Find Traces
- Click a trace to see the waterfall spanning both services
- Look for error traces (red) and slow traces (long duration)
- Each span has attributes: `order.id`, `order.item`, `error.type`

### 2. Metrics in Prometheus (localhost:9090)

```
# Custom metrics from Order Service (via OTel Collector)
orders_created_total
payment_call_duration_ms_bucket
payment_errors_total

# Auto-collected JVM metrics from Payment Service (via Java Agent)
jvm_memory_used_bytes
jvm_threads_live_threads
process_runtime_jvm_gc_duration

# HTTP metrics (auto-instrumented)
http_server_request_duration_seconds_bucket
```

### 3. Logs in Grafana (localhost:3001 -> Explore -> Loki)

```
# All logs from order service
{exporter="OTLP"} |= "order-service"

# Error logs only
{exporter="OTLP"} |= "ERROR"

# Find logs for a specific order
{exporter="OTLP"} |= "paste-order-id-here"
```

### 4. Correlate All 3 in Grafana

This is the power of OpenTelemetry - all 3 signals share the same context:

```
Step 1: See a spike in error metrics (Prometheus)
         orders_created_total{status="PAYMENT_FAILED"} is rising

Step 2: Switch to Logs (Loki) to find the error details
         {exporter="OTLP"} |= "ERROR"
         -> "Payment service TIMEOUT for order abc-123"

Step 3: Switch to Traces (Jaeger) to see exactly where it was slow
         Find trace for order abc-123
         -> payment-service process-payment span: 3200ms (SLOW!)

All from ONE Grafana UI, all correlated by trace_id and orderId.
```

## OTLP Protocol

```
OTLP = OpenTelemetry Protocol

The universal protocol for sending telemetry data.
All signals (traces, metrics, logs) use the same protocol.

Two transport options:
  gRPC (port 4317) - binary, fast, used by Java Agent
  HTTP  (port 4318) - JSON, simpler, used by Node.js SDK

Endpoints:
  POST /v1/traces   - send trace spans
  POST /v1/metrics  - send metric data points
  POST /v1/logs     - send log records

Every OTel-compatible backend supports OTLP:
  Jaeger, Zipkin, Datadog, New Relic, Grafana Cloud, etc.
```

## OTel Signals Comparison

```
+----------+------------------+------------------+-----------------+
|          | TRACES           | METRICS          | LOGS            |
+----------+------------------+------------------+-----------------+
| What     | Request journey  | Aggregated       | Event records   |
|          | across services  | measurements     | with context    |
+----------+------------------+------------------+-----------------+
| Answers  | "Where is the    | "How many?       | "What happened  |
|          |  bottleneck?"    |  How fast?       |  and why?"      |
|          |                  |  How much?"      |                 |
+----------+------------------+------------------+-----------------+
| Example  | POST /orders     | orders_total=42  | "Payment failed |
|          |  250ms total     | p95_latency=200ms|  for order X -  |
|          |  -> payment 230ms| error_rate=5%    |  insufficient   |
|          |                  |                  |  funds"         |
+----------+------------------+------------------+-----------------+
| Storage  | Jaeger / Zipkin  | Prometheus       | Loki / ELK     |
|          | / Tempo          | / InfluxDB       | / CloudWatch   |
+----------+------------------+------------------+-----------------+
| Sampling | Often sampled    | Always collected | Always collected|
|          | (not every req)  | (aggregated)     | (can be heavy)  |
+----------+------------------+------------------+-----------------+
```

## File Structure

```
lab-03-opentelemetry/
├── LAB.md
├── docker-compose.yml                        # 8 services
├── generate-load.sh
├── order-service/
│   ├── Dockerfile
│   ├── package.json                          # @opentelemetry/* (all signals)
│   └── src/
│       ├── telemetry.js                      # OTel SDK: traces + metrics + logs
│       └── index.js                          # App + custom spans + custom metrics + OTel logs
├── payment-service/
│   ├── Dockerfile                            # Downloads OTel Java Agent jar
│   ├── pom.xml                               # Plain Spring Boot (no OTel deps needed!)
│   └── src/main/
│       ├── java/com/example/payment/
│       │   ├── PaymentServiceApplication.java
│       │   ├── Payment.java
│       │   └── PaymentController.java        # Just SLF4J logging (agent captures it)
│       └── resources/
│           └── application.properties
├── otel-collector/
│   └── otel-collector-config.yml             # Receives OTLP, exports to 3 backends
├── prometheus/
│   └── prometheus.yml                        # Scrapes OTel Collector metrics endpoint
├── loki/
│   └── loki-config.yml                       # Log storage backend
└── grafana/
    └── provisioning/
        └── datasources/
            └── datasource.yml                # Prometheus + Loki + Jaeger datasources
```

## Key Takeaway

```
+---------------------------------------------+
|  OpenTelemetry = Instrument ONCE,            |
|                  Export ANYWHERE              |
|                                               |
|  Your app code stays the same whether you    |
|  use Jaeger, Datadog, New Relic, or Grafana  |
|  Cloud. Just change the Collector config.    |
+---------------------------------------------+

  Today:   OTel Collector --> Jaeger + Prometheus + Loki (self-hosted)
  Tomorrow: OTel Collector --> Datadog (SaaS)
  Next week: OTel Collector --> Grafana Cloud (managed)

  App code? ZERO changes. Just update the collector config.
```

## Cleanup

```bash
sudo docker compose down
```
