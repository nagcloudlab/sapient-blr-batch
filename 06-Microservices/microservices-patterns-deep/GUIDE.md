# Microservices Patterns Deep Dive - Complete Teaching Guide

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & Request Flow](#architecture--request-flow)
3. [Prerequisites & Setup](#prerequisites--setup)
4. [Topic 1: Service Discovery (Eureka)](#topic-1-service-discovery-eureka)
5. [Topic 2: API Gateway Pattern](#topic-2-api-gateway-pattern)
6. [Topic 3: Dynamic Routing](#topic-3-dynamic-routing)
7. [Topic 4: Traffic Management](#topic-4-traffic-management)
8. [Topic 5: Security & Authentication](#topic-5-security--authentication)
9. [Topic 6: API Monitoring & Correlation](#topic-6-api-monitoring--correlation)
10. [Topic 7: Circuit Breaker & Resilience](#topic-7-circuit-breaker--resilience)
11. [Topic 8: Observability with Actuator](#topic-8-observability-with-actuator)
12. [Topic 9: Metrics with Prometheus & Grafana](#topic-9-metrics-with-prometheus--grafana)
13. [Topic 10: Centralized Logging with Loki](#topic-10-centralized-logging-with-loki)
14. [Topic 11: Distributed Tracing with Tempo](#topic-11-distributed-tracing-with-tempo)
15. [Topic 12: Correlating Metrics, Logs & Traces](#topic-12-correlating-metrics-logs--traces)
16. [All Ports & URLs Reference](#all-ports--urls-reference)
17. [Cleanup](#cleanup)

---

## Project Overview

This project teaches **11 core microservices patterns** using a simple e-commerce scenario with 4 Spring Boot services. Every pattern is implemented with real, working code you can run, test, and inspect.

### What You'll Learn

| # | Pattern | What It Solves |
|---|---------|---------------|
| 1 | **Service Discovery** | How do services find each other without hardcoded URLs? |
| 2 | **API Gateway** | How do clients access multiple services through a single entry point? |
| 3 | **Dynamic Routing** | How do you route requests based on headers, methods, paths, or traffic weights? |
| 4 | **Traffic Management** | How do you protect services from overload and do canary deployments? |
| 5 | **Security & Auth** | How do you authenticate requests once at the gateway and propagate identity? |
| 6 | **API Monitoring** | How do you track requests across services with correlation IDs and custom metrics? |
| 7 | **Circuit Breaker** | How do you prevent cascading failures when a service goes down? |
| 8 | **Observability** | How do you expose health checks, configs, and metrics from each service? |
| 9 | **Metrics Collection** | How do you collect and visualize metrics from all services in dashboards? |
| 10 | **Centralized Logging** | How do you aggregate logs from all services into one searchable place? |
| 11 | **Distributed Tracing** | How do you trace a single request as it flows through multiple services? |

### Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| Spring Boot | 4.1.1 | Application framework |
| Spring Cloud | 2025.1.3 | Microservices infrastructure |
| Spring Cloud Gateway | (WebFlux) | API Gateway (reactive, non-blocking) |
| Netflix Eureka | | Service discovery and registration |
| Resilience4j | | Circuit breaker, retry, rate limiter |
| Bucket4j | 8.10.1 | In-memory rate limiting (token bucket) |
| JJWT | 0.12.6 | JWT token generation and validation |
| Micrometer | | Application metrics (counters, timers, gauges) |
| Micrometer Tracing + OTel | | Distributed tracing bridge |
| Prometheus | (Docker) | Metrics scraping and storage |
| Grafana | (Docker) | Dashboards for metrics, logs, traces |
| Loki | (Docker) | Log aggregation and search |
| Promtail | (Docker) | Log file collector (ships to Loki) |
| Tempo | (Docker) | Distributed trace storage |
| Logstash Logback Encoder | 8.1 | JSON structured logging |

---

## Architecture & Request Flow

### Service Architecture

```
                        +-------------------+
                        | Discovery Server  |
                        |   (Eureka 8761)   |
                        +-------------------+
                               ▲  ▲  ▲
                register       │  │  │       register
          ┌────────────────────┘  │  └────────────────────┐
          │                       │                        │
+─────────┴─────────+  +─────────┴────────+  +────────────┴──────+
|    API Gateway     |  |  Order Service   |  | Inventory Service |
|     (8080)         |  |    (8081)        |  |     (8082)        |
|                    |  |                  |  |                   |
| Filters:           |  | Endpoints:       |  | Endpoints:        |
|  LoggingFilter     |  |  GET  /orders    |  |  GET  /inventory  |
|  RateLimitingFilter|  |  GET  /orders/id |  |  GET  /inventory/ |
|  SecurityHeaders   |  |  POST /orders    |  |       {productId} |
|  JwtAuthFilter     |  |                  |  |                   |
|  MetricsFilter     |  | Calls:           |  | Seeded Data:      |
|                    |  |  inventory-svc   |  |  PROD-001: Laptop |
| Routes:            |  |  via RestTemplate|  |  PROD-002: Phone  |
|  Header-based      |  |                  |  |  PROD-003: Tablet |
|  Method-based      |  | Metrics:         |  |                   |
|  Weight-based      |  |  orders.created  |  | Metrics:          |
|  Path-rewrite      |  |  orders.time     |  |  inventory.checks |
|  Circuit-breaker   |  |                  |  |                   |
+────────────────────+  +──────────────────+  +───────────────────+
```

### Observability Stack

```
Spring Boot Services (host machine)               Docker Containers
┌─────────────────────────────┐            ┌──────────────────────────┐
│                             │            │                          │
│  API Gateway    :8080       │──metrics──→│  Prometheus    :9090     │──┐
│  Order Service  :8081       │──metrics──→│  (scrapes /actuator/     │  │
│  Inventory Svc  :8082       │──metrics──→│   prometheus every 5s)   │  │
│                             │            └──────────────────────────┘  │
│                             │                                         │
│  All services export traces │            ┌──────────────────────────┐  │
│  via Zipkin protocol ───────┼──traces──→ │  Tempo         :3200     │  │
│  (micrometer-tracing-otel)  │  (:9411)   │  (Zipkin receiver)       │  │
│                             │            └──────────────────────────┘  │
│                             │                                         │
│  logback writes JSON logs   │            ┌──────────────────────────┐  │
│  to ./logs/ directory  ─────┼──volume──→ │  Promtail → Loki  :3100  │  │
│  (logstash-logback-encoder) │  mount     │  (log aggregation)       │  │
│                             │            └──────────────────────────┘  │
└─────────────────────────────┘                                         │
                                           ┌──────────────────────────┐  │
                                           │  Grafana        :3000    │←─┘
                                           │   - Prometheus (metrics) │
                                           │   - Loki (logs)          │
                                           │   - Tempo (traces)       │
                                           │   - Pre-built Dashboard  │
                                           └──────────────────────────┘
```

### Complete Request Flow (What happens when a client calls the gateway)

```
Client (curl/browser)
    │
    ▼
┌────────────── API Gateway Filter Chain (:8080) ──────────────┐
│                                                              │
│  ① LoggingFilter (order=-2)    ← runs FIRST                 │
│     • Generates X-Correlation-ID (8-char UUID) if absent     │
│     • Logs: [abc123] >>> GET /orders from 127.0.0.1          │
│     • Injects correlation ID into downstream request headers │
│     • After response: logs status code + duration            │
│                                                              │
│  ② RateLimitingFilter (order=-1)                             │
│     • Looks up token bucket for this client IP               │
│     • If tokens available: consume 1, add X-RateLimit headers│
│     • If empty: return 429 Too Many Requests immediately     │
│     • Skips /actuator/** paths                               │
│                                                              │
│  ③ SecurityHeadersFilter (order=0)                           │
│     • Adds security headers to EVERY response:               │
│       X-Content-Type-Options: nosniff                        │
│       X-Frame-Options: DENY                                  │
│       X-XSS-Protection: 1; mode=block                       │
│       X-Gateway-Instance: api-gateway-8080                   │
│                                                              │
│  ④ JwtAuthenticationFilter (order=1)                         │
│     • PUBLIC paths (/auth/**, /actuator/**, /public/**): skip│
│     • Check 1: X-API-Key header == "demo-api-key-2024"?      │
│       → Yes: set X-User=api-key-user, X-User-Role=SERVICE   │
│     • Check 2: Authorization: Bearer <jwt-token>?            │
│       → Validate JWT signature (HMAC-SHA256)                 │
│       → Extract subject → X-User header                      │
│       → Extract "role" claim → X-User-Role header            │
│     • Neither? → return 401 Unauthorized JSON                │
│                                                              │
│  ⑤ MetricsFilter (GatewayMetricsConfig)                      │
│     • Increments gateway.requests.total counter              │
│     • Increments gateway.route.requests{route=xxx} counter   │
│     • After response: if status >= 400, increment error count│
│                                                              │
│  ⑥ Route Matching (DynamicRouteConfig.java)                  │
│     • Evaluates routes in defined order:                     │
│       1. Header-based: path=/orders + header X-Version=v2    │
│       2. Method-based: path=/orders + method=POST            │
│       3. Weight-based: path=/inventory + weight 80/20        │
│       4. Circuit-breaker: path=/orders + CB + retry(2)       │
│       5. Path-rewrite: /api/v1/inventory/** → /inventory/**  │
│     • First matching route wins                              │
│                                                              │
│  ⑦ Eureka Lookup                                             │
│     • URI lb://order-service → query Eureka for instances    │
│     • Eureka returns: localhost:8081                          │
│     • Gateway forwards the HTTP request to that address      │
│                                                              │
│  ⑧ LoggingFilter (post-filter phase)                         │
│     • Logs: [abc123] <<< GET /orders | Status: 200 | 45ms   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
┌─── Order Service (:8081) ─────────────┐
│                                       │
│  POST /orders handler:                │
│   1. Read X-Correlation-ID header     │
│   2. Read X-User and X-User-Role      │
│   3. Call inventory-service via        │
│      @LoadBalanced RestTemplate:       │
│      GET http://inventory-service/     │
│          inventory/{productId}         │
│      (Eureka resolves the hostname)    │
│   4. Create order with:               │
│      - productId, quantity from body   │
│      - createdBy from X-User header   │
│      - inventoryCheck result           │
│   5. Increment orders.created counter  │
│   6. Record processing time            │
│   7. Return order JSON                 │
│                                       │
└───────────────┬───────────────────────┘
                │
                ▼
┌─── Inventory Service (:8082) ─────────┐
│                                       │
│  GET /inventory/{productId} handler:  │
│   1. Read X-Correlation-ID header     │
│   2. Look up product in memory map    │
│   3. Increment inventory.checks count │
│   4. Return product details JSON      │
│      (or "Product not found" if N/A)  │
│                                       │
└───────────────────────────────────────┘
```

### Source Files Reference

| File | Location | Purpose |
|------|----------|---------|
| `DiscoveryServerApplication.java` | discovery-server/src/main/java/.../discovery/ | Eureka Server with `@EnableEurekaServer` |
| `ApiGatewayApplication.java` | api-gateway/src/main/java/.../gateway/ | Gateway application entry point |
| `DynamicRouteConfig.java` | api-gateway/src/main/java/.../gateway/config/ | All programmatic route definitions |
| `LoggingGlobalFilter.java` | api-gateway/src/main/java/.../gateway/filter/ | Request/response logging + correlation ID |
| `RateLimitingFilter.java` | api-gateway/src/main/java/.../gateway/filter/ | Per-IP rate limiting (Bucket4j) |
| `SecurityHeadersFilter.java` | api-gateway/src/main/java/.../gateway/filter/ | Security response headers |
| `JwtAuthenticationFilter.java` | api-gateway/src/main/java/.../gateway/filter/ | JWT + API Key auth, role propagation |
| `GatewayMetricsConfig.java` | api-gateway/src/main/java/.../gateway/config/ | Custom Micrometer metrics |
| `GatewayStatsController.java` | api-gateway/src/main/java/.../gateway/config/ | Public stats endpoint |
| `FallbackController.java` | api-gateway/src/main/java/.../gateway/config/ | Circuit breaker fallback responses |
| `AuthController.java` | api-gateway/src/main/java/.../gateway/config/ | JWT token generation endpoint |
| `application.yml` | api-gateway/src/main/resources/ | Gateway config, Eureka, Resilience4j, Actuator |
| `logback-spring.xml` | api-gateway/src/main/resources/ | JSON structured logging for Loki |
| `OrderServiceApplication.java` | order-service/src/main/java/.../order/ | Order service entry point |
| `OrderController.java` | order-service/src/main/java/.../order/ | Order CRUD + inventory check |
| `RestTemplateConfig.java` | order-service/src/main/java/.../order/ | `@LoadBalanced` RestTemplate bean |
| `application.properties` | order-service/src/main/resources/ | Port, Eureka, Actuator, tracing config |
| `logback-spring.xml` | order-service/src/main/resources/ | JSON structured logging for Loki |
| `InventoryServiceApplication.java` | inventory-service/src/main/java/.../inventory/ | Inventory service entry point |
| `InventoryController.java` | inventory-service/src/main/java/.../inventory/ | Inventory CRUD with seeded data |
| `application.properties` | inventory-service/src/main/resources/ | Port, Eureka, Actuator, tracing config |
| `logback-spring.xml` | inventory-service/src/main/resources/ | JSON structured logging for Loki |
| `prometheus.yml` | observability/prometheus/ | Prometheus scrape targets |
| `tempo-config.yaml` | observability/tempo/ | Tempo trace storage config |
| `loki-config.yaml` | observability/loki/ | Loki log storage config |
| `promtail-config.yaml` | observability/promtail/ | Log file collection config |
| `datasources.yaml` | observability/grafana/provisioning/datasources/ | Grafana datasource auto-provisioning |
| `dashboards.yaml` | observability/grafana/provisioning/dashboards/ | Grafana dashboard auto-provisioning |
| `microservices-overview.json` | observability/grafana/dashboards/ | Pre-built Grafana dashboard |
| `docker-compose-observability.yml` | project root | Docker Compose for observability stack |

---

## Prerequisites & Setup

### Prerequisites

- Java 17+
- Maven 3.8+
- Docker & Docker Compose (for observability stack)
- curl (for testing)

### Step 1: Build all modules

```bash
cd microservices-patterns-deep
mvn clean package -DskipTests
```

**Expected output:**
```
[INFO] Reactor Summary:
[INFO] Microservices Patterns Deep - API Operations ....... SUCCESS
[INFO] Discovery Server ................................... SUCCESS
[INFO] API Gateway ........................................ SUCCESS
[INFO] Order Service ...................................... SUCCESS
[INFO] Inventory Service .................................. SUCCESS
[INFO] BUILD SUCCESS
```

### Step 2: Start the Observability Stack (Docker)

```bash
docker compose -f docker-compose-observability.yml up -d
```

**Verify containers:**
```bash
docker compose -f docker-compose-observability.yml ps
```

**Expected — all 5 containers running:**
```
NAME         IMAGE                    STATUS    PORTS
grafana      grafana/grafana:latest   Up        0.0.0.0:3000->3000/tcp
loki         grafana/loki:latest      Up        0.0.0.0:3100->3100/tcp
prometheus   prom/prometheus:latest   Up        0.0.0.0:9090->9090/tcp
promtail     grafana/promtail:latest  Up        0.0.0.0:9080->9080/tcp
tempo        grafana/tempo:latest     Up        0.0.0.0:3200->3200/tcp, 0.0.0.0:9411->9411/tcp
```

### Step 3: Start Spring Boot services (each in a separate terminal)

**Important:** Start in this order. Discovery Server must be up before other services register.

```bash
# Terminal 1 — Discovery Server (start first, wait until ready)
cd discovery-server && mvn spring-boot:run
# Wait for log: "Started DiscoveryServerApplication"

# Terminal 2 — Order Service
cd order-service && mvn spring-boot:run
# Wait for log: "Started OrderServiceApplication"

# Terminal 3 — Inventory Service
cd inventory-service && mvn spring-boot:run
# Wait for log: "Started InventoryServiceApplication"

# Terminal 4 — API Gateway (start last)
cd api-gateway && mvn spring-boot:run
# Wait for log: "Started ApiGatewayApplication"
```

### Step 4: Verify all services are registered with Eureka

```bash
# Open Eureka dashboard in browser
open http://localhost:8761
```

**What you should see:** A web page with "Instances currently registered with Eureka" showing:
- `API-GATEWAY` — 1 instance
- `ORDER-SERVICE` — 1 instance
- `INVENTORY-SERVICE` — 1 instance

**Verify via API:**
```bash
curl -s http://localhost:8761/eureka/apps | grep "<name>"
```

**Expected:**
```xml
<name>API-GATEWAY</name>
<name>ORDER-SERVICE</name>
<name>INVENTORY-SERVICE</name>
```

### Step 5: Verify observability endpoints

```bash
# Prometheus — all 3 targets should show "UP"
open http://localhost:9090/targets

# Grafana
open http://localhost:3000
# Login: admin / admin (skip password change prompt)
```

---

## Topic 1: Service Discovery (Eureka)

### What is Service Discovery?

In a microservices architecture, services need to find each other. Hardcoding URLs like `http://localhost:8081` doesn't work because:
- Services may run on different hosts in production
- Multiple instances may exist (for load balancing)
- Instances may start/stop dynamically (auto-scaling)

**Service Discovery** solves this by providing a **registry** where services register themselves and look up other services by name.

### How Eureka Works

```
1. REGISTRATION
   Order Service starts → registers with Eureka: "I am order-service at 192.168.1.10:8081"
   Inventory Service starts → registers: "I am inventory-service at 192.168.1.11:8082"

2. HEARTBEAT
   Every 30 seconds, each service sends a heartbeat to Eureka
   If Eureka misses 3 heartbeats → marks the instance as DOWN

3. DISCOVERY
   Order Service needs to call Inventory Service
   → asks Eureka: "Where is inventory-service?"
   → Eureka returns: "192.168.1.11:8082"
   → Order Service calls that address directly
```

### Code Walkthrough

**Discovery Server** (`discovery-server/src/main/java/.../DiscoveryServerApplication.java`):
```java
@SpringBootApplication
@EnableEurekaServer    // This single annotation starts the Eureka registry
public class DiscoveryServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(DiscoveryServerApplication.class, args);
    }
}
```

**Discovery Server config** (`discovery-server/src/main/resources/application.properties`):
```properties
spring.application.name=discovery-server
server.port=8761

# Don't register with yourself (this IS the registry)
eureka.client.register-with-eureka=false
eureka.client.fetch-registry=false
```

**Client services** (order-service, inventory-service, api-gateway) just need this in their config:
```properties
eureka.client.service-url.defaultZone=http://localhost:8761/eureka
```

Spring Cloud automatically registers the service on startup and deregisters on shutdown.

**Service-to-service calls** use `@LoadBalanced RestTemplate` (`order-service/.../RestTemplateConfig.java`):
```java
@Configuration
public class RestTemplateConfig {
    @Bean
    @LoadBalanced   // This annotation enables Eureka-based hostname resolution
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

With `@LoadBalanced`, you can use the **service name** instead of a hostname:
```java
// "inventory-service" is resolved by Eureka → actual IP:port
restTemplate.getForObject("http://inventory-service/inventory/PROD-001", String.class);
```

### Hands-On Steps

**Step 1: See the Eureka dashboard**
```bash
open http://localhost:8761
```

Observe the registered instances, their status (UP/DOWN), and their metadata.

**Step 2: Query Eureka REST API**
```bash
# List all registered applications
curl -s http://localhost:8761/eureka/apps | head -50

# Get details for a specific service
curl -s -H "Accept: application/json" http://localhost:8761/eureka/apps/ORDER-SERVICE | python3 -m json.tool
```

**Step 3: See what happens when a service goes down**
```bash
# Stop the inventory-service (Ctrl+C in Terminal 3)
# Wait 30 seconds, then refresh Eureka dashboard
open http://localhost:8761
# inventory-service will disappear from the list

# Restart it
cd inventory-service && mvn spring-boot:run
# It re-registers within seconds
```

**Key takeaway:** Services register automatically. You never hardcode URLs. You call services by name, and Eureka resolves them at runtime.

---

## Topic 2: API Gateway Pattern

### What is an API Gateway?

An API Gateway is a **single entry point** for all client requests. Instead of clients calling each microservice directly, they call the gateway, which routes requests to the appropriate service.

### Why Do You Need It?

```
WITHOUT Gateway:                    WITH Gateway:
Client knows every service URL      Client knows ONE URL (gateway)

Client → order-service:8081         Client → Gateway:8080
Client → inventory-service:8082              │
Client → payment-service:8083                ├→ order-service
Client → user-service:8084                   ├→ inventory-service
                                             ├→ payment-service
Problems:                                    └→ user-service
- Client is tightly coupled
- Cross-cutting concerns (auth,       Benefits:
  logging, rate limiting) must be      - Single entry point
  implemented in EVERY service         - Auth handled ONCE at gateway
- No central place for routing         - Centralized logging & metrics
                                       - Rate limiting in ONE place
                                       - Can change backends without
                                         affecting clients
```

### How Spring Cloud Gateway Works

Spring Cloud Gateway is built on **WebFlux** (reactive, non-blocking). It processes requests through a pipeline:

```
Incoming Request
    │
    ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Pre-Filters │ ──→ │ Route Match  │ ──→ │ Proxy to    │
│ (ordered)   │     │ (predicates) │     │ Downstream  │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                                                ▼
                                         ┌─────────────┐
                                         │ Post-Filters│
                                         │ (response)  │
                                         └─────────────┘
```

**Three core concepts:**
1. **Route** — maps a request (by path, header, method) to a downstream URI
2. **Predicate** — condition that must be true for the route to match (e.g., path matches `/orders/**`)
3. **Filter** — modifies the request or response (e.g., add headers, rate limit, authenticate)

### Code Walkthrough

**Gateway config** (`api-gateway/src/main/resources/application.yml`):
```yaml
server:
  port: 8080           # Gateway listens on port 8080

spring:
  application:
    name: api-gateway
  cloud:
    gateway:
      metrics:
        enabled: true   # Enable built-in gateway metrics
      default-filters:
        - name: RequestSize
          args:
            maxSize: 5MB  # Reject requests larger than 5MB
      discovery:
        locator:
          enabled: false  # We define routes EXPLICITLY (not auto-discovered)

eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka  # Register with Eureka
```

**Global Filters** are beans that implement `GlobalFilter` and apply to EVERY route. They are ordered by the `Ordered` interface:

| Order | Filter | File | Purpose |
|-------|--------|------|---------|
| -2 | `LoggingGlobalFilter` | `LoggingGlobalFilter.java` | Logs request/response, generates correlation ID |
| -1 | `RateLimitingFilter` | `RateLimitingFilter.java` | Token bucket rate limiting per IP |
| 0 | `SecurityHeadersFilter` | `SecurityHeadersFilter.java` | Adds security response headers |
| 1 | `JwtAuthenticationFilter` | `JwtAuthenticationFilter.java` | Validates JWT or API key |
| (auto) | `metricsFilter` | `GatewayMetricsConfig.java` | Counts requests, errors, per-route stats |

```
Filter Chain Order:
Request → Logging(-2) → RateLimit(-1) → SecurityHeaders(0) → JwtAuth(1) → Metrics → Route → Service
                                                                                         ↓
Response ← Logging(-2) ← SecurityHeaders(0) ←──────────────────────────────────── Service Response
```

### Hands-On Steps

**Step 1: See all gateway routes**
```bash
curl -s http://localhost:8080/actuator/gateway/routes | python3 -m json.tool
```

This shows every route with its predicates (matching conditions) and filters.

**Step 2: See all global filters and their order**
```bash
curl -s http://localhost:8080/actuator/gateway/globalfilters | python3 -m json.tool
```

**Step 3: Make a request and observe the full filter chain**
```bash
# Verbose output shows all response headers added by filters
curl -v http://localhost:8080/inventory -H "X-API-Key: demo-api-key-2024" 2>&1 | grep "< "
```

**Expected response headers (each added by a different filter):**
```
< X-Content-Type-Options: nosniff       ← SecurityHeadersFilter
< X-Frame-Options: DENY                 ← SecurityHeadersFilter
< X-XSS-Protection: 1; mode=block       ← SecurityHeadersFilter
< X-Gateway-Instance: api-gateway-8080  ← SecurityHeadersFilter
< X-RateLimit-Remaining: 29             ← RateLimitingFilter
< X-RateLimit-Limit: 30                 ← RateLimitingFilter
< X-Canary: false                       ← DynamicRouteConfig (route filter)
```

**Step 4: Watch gateway logs (Terminal 4) while making a request**
```bash
curl -s http://localhost:8080/inventory -H "X-API-Key: demo-api-key-2024" > /dev/null
```

**In the Gateway terminal:**
```
14:00:00.123 [reactor-http-nio-2] [abc12345,def67890] INFO  LoggingGlobalFilter
  - [a1b2c3d4] >>> GET /inventory from 127.0.0.1 | Headers: Host=localhost:8080
14:00:00.168 [reactor-http-nio-2] [abc12345,def67890] INFO  JwtAuthenticationFilter
  - Request authenticated via API Key for path: /inventory
14:00:00.250 [reactor-http-nio-2] [abc12345,def67890] INFO  LoggingGlobalFilter
  - [a1b2c3d4] <<< GET /inventory | Status: 200 | Duration: 127ms
```

**Key takeaway:** The gateway is a single entry point. Every request flows through ordered filters that handle logging, rate limiting, security, and metrics — before the request ever reaches a downstream service.

---

## Topic 3: Dynamic Routing

### What is Dynamic Routing?

Dynamic routing means the gateway can route the **same URL** to different backends based on runtime conditions — request headers, HTTP methods, path patterns, or traffic weights.

### Why Do You Need It?

| Use Case | Routing Strategy | Example |
|----------|-----------------|---------|
| **API versioning** | Header-based | `X-Version: v2` → route to v2 service |
| **Read vs Write** | Method-based | GET → read-replica, POST → primary |
| **URL evolution** | Path-rewrite | `/api/v1/inventory/**` → `/inventory/**` |
| **Canary deploys** | Weight-based | 80% → stable, 20% → new version |

### Code Walkthrough

All routes are defined in `DynamicRouteConfig.java`. Let's examine each one:

**Route 1: Header-based routing**
```java
.route("order-service-v2-header", r -> r
    .path("/orders/**")                           // Match path /orders/**
    .and().header("X-Version", "v2")              // AND header X-Version equals "v2"
    .filters(f -> f
        .addRequestHeader("X-Routed-By", "header-predicate-v2")  // Tag for debugging
        .addResponseHeader("X-Route-Match", "header-based"))     // Prove which route matched
    .uri("lb://order-service"))                   // Forward to order-service via Eureka
```

**Route 2: Method-based routing**
```java
.route("order-service-post-only", r -> r
    .path("/orders")                              // Match exact path /orders
    .and().method(HttpMethod.POST)                // AND method is POST
    .filters(f -> f
        .addRequestHeader("X-Routed-By", "method-predicate-POST")
        .addResponseHeader("X-Route-Match", "method-based"))
    .uri("lb://order-service"))
```

**Route 3 & 4: Weight-based routing (Canary)**
```java
// 80% of /inventory traffic → stable route
.route("inventory-stable", r -> r
    .path("/inventory/**")
    .and().weight("inventory-group", 8)           // Weight 8 out of 10
    .filters(f -> f
        .addResponseHeader("X-Canary", "false"))
    .uri("lb://inventory-service"))

// 20% of /inventory traffic → canary route
.route("inventory-canary", r -> r
    .path("/inventory/**")
    .and().weight("inventory-group", 2)           // Weight 2 out of 10
    .filters(f -> f
        .addRequestHeader("X-Canary-Version", "v2")  // Tells service it's canary
        .addResponseHeader("X-Canary", "true"))
    .uri("lb://inventory-service"))
```

**Route 5: Circuit breaker with retry**
```java
.route("order-service-circuit-breaker", r -> r
    .path("/orders/**")
    .filters(f -> f
        .circuitBreaker(cb -> cb
            .setName("orderServiceCB")                       // Named circuit breaker
            .setFallbackUri("forward:/fallback/orders"))     // Fallback URL
        .retry(retryConfig -> retryConfig.setRetries(2)))    // Retry up to 2 times
    .uri("lb://order-service"))
```

**Route 6: Path rewriting**
```java
.route("inventory-path-rewrite", r -> r
    .path("/api/v1/inventory/**")                 // Match versioned URL
    .filters(f -> f
        .rewritePath("/api/v1/inventory/(?<segment>.*)", "/inventory/${segment}")
        .addResponseHeader("X-Route-Match", "path-rewrite"))
    .uri("lb://inventory-service"))
```

**Route evaluation order matters:** Routes are evaluated in the order they're defined. The first matching route wins. Header-based and method-based routes (more specific) are defined before the general circuit-breaker route (catch-all for `/orders/**`).

### Hands-On Steps

**Step 1: Header-based routing**

```bash
# Without X-Version header → matches the circuit-breaker catch-all route
curl -v http://localhost:8080/orders \
  -H "X-API-Key: demo-api-key-2024" 2>&1 | grep "X-Route-Match"
# No X-Route-Match header (circuit-breaker route doesn't add one)

# With X-Version: v2 → matches the header-based route
curl -v http://localhost:8080/orders \
  -H "X-API-Key: demo-api-key-2024" \
  -H "X-Version: v2" 2>&1 | grep "X-Route-Match"
```

**Expected:**
```
< X-Route-Match: header-based
```

Both requests go to the same service (order-service), but they matched **different routes** with different filters. In production, you could route `v2` requests to a different service instance.

**Step 2: Path rewriting**

```bash
# Client sends: /api/v1/inventory/PROD-001
# Gateway rewrites to: /inventory/PROD-001 before forwarding
curl -s http://localhost:8080/api/v1/inventory/PROD-001 \
  -H "X-API-Key: demo-api-key-2024" | python3 -m json.tool
```

**Expected:**
```json
{
    "productId": "PROD-001",
    "name": "Laptop",
    "quantity": 50,
    "available": true,
    "version": "v1",
    "port": 8082
}
```

```bash
# Verify the path-rewrite route was used
curl -v http://localhost:8080/api/v1/inventory/PROD-001 \
  -H "X-API-Key: demo-api-key-2024" 2>&1 | grep "X-Route-Match"
```

**Expected:** `< X-Route-Match: path-rewrite`

The inventory-service never knows the client used `/api/v1/inventory/...` — it only sees `/inventory/PROD-001`.

**Step 3: Method-based routing**

```bash
# POST to create an order → matches the method-based route
curl -s -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-2024" \
  -d '{"productId": "PROD-001", "quantity": 2}' | python3 -m json.tool
```

**Expected:** An order object with `orderId`, `productId`, `status: CREATED`, and `inventoryCheck` showing the Laptop details.

**Key takeaway:** Dynamic routing lets you version APIs, split read/write traffic, rewrite URLs, and do canary deployments — all at the gateway level without changing any downstream service.

---

## Topic 4: Traffic Management

### What is Traffic Management?

Traffic management controls **how much** traffic reaches your services and **how** it's distributed. The two key techniques here are:

1. **Rate Limiting** — cap the number of requests per client to prevent overload
2. **Canary Routing** — gradually shift traffic to a new version to test in production

### Rate Limiting — How It Works

This project uses the **Token Bucket algorithm** (via Bucket4j):

```
Bucket (30 tokens, refills every 60 seconds)
┌─────────────────────────────────────────┐
│ ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●       │  ← 30 tokens at start
└─────────────────────────────────────────┘

Request 1: consume 1 token → 29 remaining → 200 OK
Request 2: consume 1 token → 28 remaining → 200 OK
...
Request 30: consume 1 token → 0 remaining → 200 OK
Request 31: no tokens left! → 429 Too Many Requests
...
(after 60 seconds, bucket refills to 30 tokens)
```

### Code Walkthrough — RateLimitingFilter

```java
@Component
public class RateLimitingFilter implements GlobalFilter, Ordered {

    private static final int REQUESTS_PER_MINUTE = 30;
    private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();  // One bucket per IP

    private Bucket createBucket() {
        return Bucket.builder()
            .addLimit(Bandwidth.simple(REQUESTS_PER_MINUTE, Duration.ofMinutes(1)))
            .build();
    }

    private Bucket resolveBucket(String clientIp) {
        return buckets.computeIfAbsent(clientIp, k -> createBucket());  // Create bucket on first request
    }

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String path = exchange.getRequest().getURI().getPath();
        if (path.startsWith("/actuator")) {
            return chain.filter(exchange);  // Skip rate limiting for actuator
        }

        String clientIp = exchange.getRequest().getRemoteAddress()...getHostAddress();
        Bucket bucket = resolveBucket(clientIp);

        if (bucket.tryConsume(1)) {                                        // Try to consume 1 token
            long remaining = bucket.getAvailableTokens();
            exchange.getResponse().getHeaders().add("X-RateLimit-Remaining", String.valueOf(remaining));
            exchange.getResponse().getHeaders().add("X-RateLimit-Limit", "30");
            return chain.filter(exchange);                                 // Allow request
        } else {
            exchange.getResponse().setStatusCode(HttpStatus.TOO_MANY_REQUESTS);  // 429
            exchange.getResponse().getHeaders().add("X-RateLimit-Retry-After", "60");
            return exchange.getResponse().setComplete();                   // Block request
        }
    }

    @Override
    public int getOrder() { return -1; }  // Run after logging, before auth
}
```

**Key design decisions:**
- **Per-IP buckets:** Each client IP gets its own token bucket (stored in `ConcurrentHashMap`)
- **In-memory:** No external store (Redis) needed — simpler for demos, but doesn't scale across gateway instances
- **Actuator excluded:** Health checks and metrics endpoints are never rate-limited

### Hands-On Steps — Rate Limiting

**Step 1: Send 35 rapid requests (limit is 30/min)**
```bash
for i in $(seq 1 35); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    http://localhost:8080/inventory \
    -H "X-API-Key: demo-api-key-2024")
  echo "Request $i: HTTP $STATUS"
done
```

**Expected output:**
```
Request 1: HTTP 200
Request 2: HTTP 200
...
Request 30: HTTP 200
Request 31: HTTP 429    ← Rate limit exceeded!
Request 32: HTTP 429
Request 33: HTTP 429
Request 34: HTTP 429
Request 35: HTTP 429
```

**Step 2: Inspect rate limit headers**
```bash
curl -v http://localhost:8080/inventory \
  -H "X-API-Key: demo-api-key-2024" 2>&1 | grep "X-RateLimit"
```

**Expected (if tokens remain):**
```
< X-RateLimit-Remaining: 28
< X-RateLimit-Limit: 30
```

**Expected (if limit exceeded):**
```
< X-RateLimit-Retry-After: 60
```

**Step 3: Wait 60 seconds, then try again — tokens refill:**
```bash
# After waiting ~60 seconds
curl -s -o /dev/null -w "%{http_code}" \
  http://localhost:8080/inventory -H "X-API-Key: demo-api-key-2024"
# Should return 200 again
```

### Hands-On Steps — Canary Routing

**Step 1: Send 20 requests and observe the canary split**
```bash
for i in $(seq 1 20); do
  CANARY=$(curl -s -D - http://localhost:8080/inventory \
    -H "X-API-Key: demo-api-key-2024" 2>&1 | grep "X-Canary:" | tr -d '\r')
  echo "Request $i: $CANARY"
done
```

**Expected (approximately 80/20 split):**
```
Request 1:  X-Canary: false
Request 2:  X-Canary: false
Request 3:  X-Canary: false
Request 4:  X-Canary: true     ← 20% goes to canary
Request 5:  X-Canary: false
Request 6:  X-Canary: false
Request 7:  X-Canary: false
Request 8:  X-Canary: false
Request 9:  X-Canary: true     ← canary again
Request 10: X-Canary: false
...
```

In production, the "canary" route would point to a newer version of the service. If the canary version works well, you'd gradually increase the weight from 20% to 100%.

**Key takeaway:** Rate limiting prevents abuse and overload. Canary routing enables safe, gradual deployments. Both are configured at the gateway — no changes needed in downstream services.

---

## Topic 5: Security & Authentication

### What is Gateway-Level Authentication?

Instead of every microservice implementing authentication independently, the **gateway authenticates once** and passes the verified identity to downstream services via headers.

```
WITHOUT gateway auth:                WITH gateway auth:
Client → Service A (auth logic)      Client → Gateway (auth logic)
Client → Service B (auth logic)               │ ✓ verified
Client → Service C (auth logic)               ├→ Service A (trusts gateway)
                                              ├→ Service B (trusts gateway)
Problems:                                     └→ Service C (trusts gateway)
- Duplicate auth code in every service
- Each service needs the JWT secret     Benefits:
- Hard to change auth strategy          - Auth in ONE place
                                        - Services receive X-User, X-User-Role headers
                                        - Easy to add/change auth (API key, OAuth, etc.)
```

### Two Auth Methods Supported

| Method | Header | Use Case |
|--------|--------|----------|
| **API Key** | `X-API-Key: demo-api-key-2024` | Service-to-service calls, simple integrations |
| **JWT Token** | `Authorization: Bearer <token>` | User authentication with roles |

### Code Walkthrough — JwtAuthenticationFilter

```java
@Component
public class JwtAuthenticationFilter implements GlobalFilter, Ordered {

    // These paths skip authentication entirely
    private static final List<String> PUBLIC_PATHS = List.of(
        "/auth/", "/actuator/", "/public/"
    );

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String path = exchange.getRequest().getURI().getPath();

        // 1. Skip auth for public paths
        if (isPublicPath(path)) return chain.filter(exchange);

        // 2. Check API Key (simplest auth — just a shared secret)
        String apiKey = exchange.getRequest().getHeaders().getFirst("X-API-Key");
        if ("demo-api-key-2024".equals(apiKey)) {
            // API key is valid → set identity headers and continue
            ServerWebExchange mutated = exchange.mutate()
                .request(r -> r.header("X-User", "api-key-user")
                               .header("X-User-Role", "SERVICE"))
                .build();
            return chain.filter(mutated);
        }

        // 3. Check JWT Bearer token
        String authHeader = exchange.getRequest().getHeaders().getFirst("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return unauthorizedResponse(exchange, "Missing or invalid Authorization header");
        }

        String token = authHeader.substring(7);  // Remove "Bearer " prefix
        try {
            // 4. Validate JWT signature and extract claims
            SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
            Claims claims = Jwts.parser()
                .verifyWith(key)           // Verify HMAC-SHA256 signature
                .build()
                .parseSignedClaims(token)
                .getPayload();

            String username = claims.getSubject();         // "admin" or "user"
            String role = claims.get("role", String.class); // "ADMIN" or "USER"

            // 5. Pass identity to downstream services via headers
            ServerWebExchange mutated = exchange.mutate()
                .request(r -> r.header("X-User", username)
                               .header("X-User-Role", role != null ? role : "USER"))
                .build();

            return chain.filter(mutated);
        } catch (Exception e) {
            return unauthorizedResponse(exchange, "Invalid or expired JWT token");
        }
    }

    @Override
    public int getOrder() { return 1; }  // Run after rate limiting
}
```

### Code Walkthrough — AuthController (Token Generation)

```java
@RestController
@RequestMapping("/auth")
public class AuthController {

    @PostMapping("/login")
    public Mono<ResponseEntity<Map<String, Object>>> login(@RequestBody Map<String, String> credentials) {
        String username = credentials.getOrDefault("username", "");
        String password = credentials.getOrDefault("password", "");

        // Demo users (in production, this would query a database)
        String role;
        if ("admin".equals(username) && "admin123".equals(password)) {
            role = "ADMIN";
        } else if ("user".equals(username) && "user123".equals(password)) {
            role = "USER";
        } else {
            return Mono.just(ResponseEntity.status(401).body(errorMap));
        }

        // Build JWT with username as subject, role as custom claim
        String token = Jwts.builder()
            .subject(username)                                    // "admin"
            .claim("role", role)                                  // "ADMIN"
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + 3600000))  // 1 hour
            .signWith(key)                                        // HMAC-SHA256
            .compact();

        return Mono.just(ResponseEntity.ok(Map.of("token", token, ...)));
    }
}
```

### How Identity Flows End-to-End

```
Client                    Gateway                      Order Service
  │                         │                              │
  │ POST /orders            │                              │
  │ Authorization: Bearer   │                              │
  │   eyJhbGciOiJIUzI1...  │                              │
  │ ───────────────────────→│                              │
  │                         │ JwtAuthFilter:               │
  │                         │  parse token                 │
  │                         │  subject = "admin"           │
  │                         │  role = "ADMIN"              │
  │                         │                              │
  │                         │ POST /orders                 │
  │                         │ X-User: admin                │
  │                         │ X-User-Role: ADMIN           │
  │                         │ ────────────────────────────→│
  │                         │                              │ reads X-User header
  │                         │                              │ sets createdBy = "admin"
  │                         │                              │
  │                         │        200 OK                │
  │                         │ ←────────────────────────────│
  │      200 OK             │                              │
  │ { "createdBy": "admin" }│                              │
  │ ←───────────────────────│                              │
```

### Hands-On Steps

**Step 1: Request without any auth → 401**
```bash
curl -s http://localhost:8080/orders | python3 -m json.tool
```

**Expected:**
```json
{
    "error": "Unauthorized",
    "message": "Missing or invalid Authorization header"
}
```

**Step 2: Authenticate with API Key**
```bash
curl -s http://localhost:8080/orders \
  -H "X-API-Key: demo-api-key-2024" | python3 -m json.tool
```

**Expected:** 200 OK with order list.

**Step 3: Get a JWT token**
```bash
# Login as admin
curl -s -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | python3 -m json.tool
```

**Expected:**
```json
{
    "token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWI...",
    "type": "Bearer",
    "username": "admin",
    "role": "ADMIN",
    "expiresIn": "3600s"
}
```

**Step 4: Use the JWT token**
```bash
# Save token to a variable
TOKEN=$(curl -s -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# Use it
curl -s http://localhost:8080/orders \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Step 5: Create an order and see identity propagation**
```bash
curl -s -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"productId": "PROD-002", "quantity": 1}' | python3 -m json.tool
```

**Expected — notice `createdBy: admin` (extracted from JWT):**
```json
{
    "orderId": 1,
    "productId": "PROD-002",
    "quantity": 1,
    "status": "CREATED",
    "createdBy": "admin",
    "inventoryCheck": "...",
    "instancePort": 8081
}
```

**Step 6: Try with invalid token → 401**
```bash
curl -s http://localhost:8080/orders \
  -H "Authorization: Bearer this-is-not-valid" | python3 -m json.tool
```

**Step 7: Public endpoints skip auth entirely**
```bash
# These work without any auth
curl -s http://localhost:8080/auth/info | python3 -m json.tool
curl -s http://localhost:8080/actuator/health | python3 -m json.tool
curl -s http://localhost:8080/public/gateway-stats | python3 -m json.tool
```

**Step 8: Check security headers on any response**
```bash
curl -v http://localhost:8080/inventory \
  -H "X-API-Key: demo-api-key-2024" 2>&1 | grep "< X-"
```

**Expected:**
```
< X-Content-Type-Options: nosniff       ← prevents MIME-type sniffing
< X-Frame-Options: DENY                 ← prevents clickjacking
< X-XSS-Protection: 1; mode=block       ← enables browser XSS filter
< X-Gateway-Instance: api-gateway-8080  ← identifies which gateway handled this
```

**Key takeaway:** Authentication happens ONCE at the gateway. Downstream services receive clean `X-User` and `X-User-Role` headers — they never need to parse JWTs or validate API keys.

---

## Topic 6: API Monitoring & Correlation

### What is Correlation ID?

When a single user request flows through multiple services (Gateway → Order → Inventory), how do you correlate logs across all three? **Correlation IDs** — a unique identifier generated at the gateway and passed to every downstream service.

```
Request arrives at Gateway
    │
    ▼
Generate correlationId = "abc12345"
    │
    ├→ Gateway logs:     [abc12345] >>> GET /orders
    ├→ Order Service logs: [correlationId=abc12345] processing order
    └→ Inventory logs:     [correlationId=abc12345] checking PROD-001
```

### Code Walkthrough — LoggingGlobalFilter

```java
@Component
public class LoggingGlobalFilter implements GlobalFilter, Ordered {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        long startTime = System.currentTimeMillis();

        // Generate or reuse correlation ID
        String correlationId = exchange.getRequest().getHeaders().getFirst("X-Correlation-ID");
        if (correlationId == null) {
            correlationId = UUID.randomUUID().toString().substring(0, 8);  // Short 8-char ID
        }

        String method = exchange.getRequest().getMethod().name();
        String path = exchange.getRequest().getURI().getPath();
        String clientIp = exchange.getRequest().getRemoteAddress()...getHostAddress();

        // PRE-filter: log incoming request
        log.info("[{}] >>> {} {} from {} | Headers: Host={}",
            correlationId, method, path, clientIp, ...);

        // Inject correlation ID into downstream request
        String finalCorrelationId = correlationId;
        ServerWebExchange mutatedExchange = exchange.mutate()
            .request(r -> r.header("X-Correlation-ID", finalCorrelationId))
            .build();

        // POST-filter: log response with timing
        return chain.filter(mutatedExchange).then(Mono.fromRunnable(() -> {
            long duration = System.currentTimeMillis() - startTime;
            int statusCode = mutatedExchange.getResponse().getStatusCode().value();
            log.info("[{}] <<< {} {} | Status: {} | Duration: {}ms",
                finalCorrelationId, method, path, statusCode, duration);
        }));
    }

    @Override
    public int getOrder() { return -2; }  // FIRST filter — runs before everything else
}
```

### Code Walkthrough — Custom Metrics (GatewayMetricsConfig)

```java
@Configuration
public class GatewayMetricsConfig {

    private final AtomicLong totalRequests = new AtomicLong(0);
    private final AtomicLong totalErrors = new AtomicLong(0);

    @Bean
    public GlobalFilter metricsFilter(MeterRegistry meterRegistry) {
        Counter requestCounter = Counter.builder("gateway.requests.total")
            .description("Total requests through gateway")
            .register(meterRegistry);                     // Registers with Micrometer → Prometheus

        Counter errorCounter = Counter.builder("gateway.errors.total")
            .description("Total error responses from gateway")
            .register(meterRegistry);

        return (exchange, chain) -> {
            totalRequests.incrementAndGet();
            requestCounter.increment();

            // Track per-route: "order-service", "inventory-service", etc.
            String routeKey = extractRouteKey(exchange.getRequest().getURI().getPath());
            Counter.builder("gateway.route.requests")
                .tag("route", routeKey)        // Tag for filtering in Prometheus
                .register(meterRegistry)
                .increment();

            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                int status = exchange.getResponse().getStatusCode().value();
                if (status >= 400) {
                    totalErrors.incrementAndGet();
                    errorCounter.increment();
                }
            }));
        };
    }
}
```

### Hands-On Steps

**Step 1: Observe request logging in Gateway terminal**
```bash
curl -s http://localhost:8080/inventory -H "X-API-Key: demo-api-key-2024" > /dev/null
```

**Watch Terminal 4 (Gateway):**
```
[a1b2c3d4] >>> GET /inventory from 127.0.0.1 | Headers: Host=localhost:8080
[a1b2c3d4] <<< GET /inventory | Status: 200 | Duration: 45ms
```

**Step 2: Send a custom correlation ID**
```bash
curl -s http://localhost:8080/orders \
  -H "X-API-Key: demo-api-key-2024" \
  -H "X-Correlation-ID: my-trace-001" | python3 -m json.tool
```

**Expected in response:** `"correlationId": "my-trace-001"`

**Watch Terminal 2 (Order Service):**
```
[correlationId=my-trace-001] GET /orders from instance port 8081
```

The same ID appears in both the gateway and order-service logs!

**Step 3: View custom metrics via Actuator**
```bash
# Total requests through gateway
curl -s http://localhost:8080/actuator/metrics/gateway.requests.total | python3 -m json.tool

# Requests per route
curl -s http://localhost:8080/actuator/metrics/gateway.route.requests | python3 -m json.tool

# Total errors
curl -s http://localhost:8080/actuator/metrics/gateway.errors.total | python3 -m json.tool

# Order-service: total orders created
curl -s http://localhost:8081/actuator/metrics/orders.created.total | python3 -m json.tool

# Order-service: processing time
curl -s http://localhost:8081/actuator/metrics/orders.processing.time | python3 -m json.tool

# Inventory-service: total checks
curl -s http://localhost:8082/actuator/metrics/inventory.checks.total | python3 -m json.tool
```

**Step 4: View gateway stats (custom endpoint)**
```bash
curl -s http://localhost:8080/public/gateway-stats | python3 -m json.tool
```

**Expected:**
```json
{
    "totalRequests": 42,
    "totalErrors": 2,
    "errorRate": "4.76%",
    "routeStats": {
        "order-service": 15,
        "inventory-service": 20,
        "auth": 5,
        "actuator": 2
    }
}
```

**Key takeaway:** Correlation IDs link logs across services. Custom Micrometer metrics give you counters and timers for business operations (orders created, inventory checks). Both are available via Actuator and scraped by Prometheus.

---

## Topic 7: Circuit Breaker & Resilience

### What is a Circuit Breaker?

When a downstream service is down or slow, the circuit breaker **prevents cascading failures** by short-circuiting requests and returning a fallback response.

```
CLOSED state (normal):
  All requests go through to downstream service
  Failures are counted in a sliding window (10 requests)

  If failure rate >= 50% in the window → OPEN

OPEN state (tripped):
  ALL requests immediately return fallback response
  No requests reach the downstream service
  After 10 seconds → HALF-OPEN

HALF-OPEN state (testing):
  Allow 3 test requests through
  If they succeed → CLOSED (recovered)
  If they fail → OPEN again
```

### Code Walkthrough — Resilience4j Configuration

```yaml
# api-gateway/src/main/resources/application.yml
resilience4j:
  circuitbreaker:
    configs:
      default:
        slidingWindowSize: 10                          # Track last 10 requests
        failureRateThreshold: 50                       # Open if >= 50% fail
        waitDurationInOpenState: 10000                 # Stay open for 10 seconds
        permittedNumberOfCallsInHalfOpenState: 3       # Allow 3 test requests
        slidingWindowType: COUNT_BASED                 # Count-based (not time-based)
    instances:
      orderServiceCB:
        baseConfig: default                            # Use the default config above
  timelimiter:
    configs:
      default:
        timeoutDuration: 3s                            # Timeout after 3 seconds
```

**Route with circuit breaker** (in `DynamicRouteConfig.java`):
```java
.route("order-service-circuit-breaker", r -> r
    .path("/orders/**")
    .filters(f -> f
        .circuitBreaker(cb -> cb
            .setName("orderServiceCB")                  // Uses the config above
            .setFallbackUri("forward:/fallback/orders")) // Where to route on failure
        .retry(retryConfig -> retryConfig.setRetries(2))) // Retry up to 2 times first
    .uri("lb://order-service"))
```

**Fallback controller** (`FallbackController.java`):
```java
@RestController
@RequestMapping("/fallback")
public class FallbackController {

    @GetMapping("/orders")
    public Mono<ResponseEntity<Map<String, Object>>> ordersFallback() {
        Map<String, Object> fallback = new LinkedHashMap<>();
        fallback.put("service", "order-service");
        fallback.put("status", "SERVICE_UNAVAILABLE");
        fallback.put("message", "Order service is temporarily unavailable. Please try again later.");
        fallback.put("fallback", true);
        return Mono.just(ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(fallback));
    }
}
```

### Hands-On Steps

**Step 1: Normal operation — circuit is CLOSED**
```bash
curl -s http://localhost:8080/orders \
  -H "X-API-Key: demo-api-key-2024" | python3 -m json.tool
# Returns: order list from order-service
```

**Step 2: Check circuit breaker state**
```bash
curl -s http://localhost:8080/actuator/circuitbreakers | python3 -m json.tool
```

**Expected:** `"state": "CLOSED"` (healthy)

**Step 3: Stop order-service → trigger fallback**
```bash
# In Terminal 2: press Ctrl+C to stop order-service

# Now call /orders through the gateway
curl -s http://localhost:8080/orders \
  -H "X-API-Key: demo-api-key-2024" | python3 -m json.tool
```

**Expected (fallback response):**
```json
{
    "service": "order-service",
    "status": "SERVICE_UNAVAILABLE",
    "message": "Order service is temporarily unavailable. Please try again later.",
    "fallback": true,
    "timestamp": "2026-08-31T14:05:00"
}
```

**Step 4: Check circuit breaker state again**
```bash
curl -s http://localhost:8080/actuator/circuitbreakers | python3 -m json.tool
```

**Expected:** `"state": "OPEN"` (tripped)

**Step 5: Restart order-service and verify recovery**
```bash
# In Terminal 2:
cd order-service && mvn spring-boot:run
# Wait for: "Started OrderServiceApplication"

# After ~10 seconds (waitDurationInOpenState), the circuit tries HALF-OPEN
# Successful requests will move it back to CLOSED
curl -s http://localhost:8080/orders \
  -H "X-API-Key: demo-api-key-2024" | python3 -m json.tool
# Returns: normal order list again
```

**Key takeaway:** The circuit breaker prevents cascading failures. When order-service is down, the gateway returns an immediate fallback instead of waiting and failing. The retry filter attempts 2 retries before giving up.

---

## Topic 8: Observability with Actuator

### What is Spring Boot Actuator?

Actuator exposes **production-ready endpoints** for monitoring and managing your application: health checks, metrics, configuration, and environment info.

### Key Actuator Endpoints

| Endpoint | What It Shows |
|----------|---------------|
| `/actuator/health` | Service health status (UP/DOWN) with component details |
| `/actuator/prometheus` | Metrics in Prometheus text format (for scraping) |
| `/actuator/metrics/{name}` | Individual metric values |
| `/actuator/env` | Environment variables and config properties |
| `/actuator/configprops` | All `@ConfigurationProperties` beans |
| `/actuator/gateway/routes` | All gateway routes with predicates/filters |
| `/actuator/gateway/globalfilters` | Global filters with their order |
| `/actuator/circuitbreakers` | Circuit breaker states |

### Configuration

```properties
# Expose ALL actuator endpoints (for demo — in production, limit this!)
management.endpoints.web.exposure.include=*
management.endpoint.health.show-details=always    # Show health details
management.endpoint.prometheus.enabled=true        # Enable /actuator/prometheus
management.metrics.tags.application=${spring.application.name}  # Tag all metrics
```

### Hands-On Steps

**Step 1: Health endpoints**
```bash
# Gateway health (includes Eureka connection, disk space, etc.)
curl -s http://localhost:8080/actuator/health | python3 -m json.tool

# Order service health
curl -s http://localhost:8081/actuator/health | python3 -m json.tool

# Custom health details (business-level)
curl -s http://localhost:8081/orders/health-details | python3 -m json.tool
curl -s http://localhost:8082/inventory/health-details | python3 -m json.tool
```

**Step 2: Prometheus metrics (raw scrape data)**
```bash
# See what Prometheus scrapes from each service
curl -s http://localhost:8080/actuator/prometheus | head -30

# Filter for custom metrics
curl -s http://localhost:8080/actuator/prometheus | grep "gateway_"
curl -s http://localhost:8081/actuator/prometheus | grep "orders_"
curl -s http://localhost:8082/actuator/prometheus | grep "inventory_"
```

**Step 3: List all actuator endpoints**
```bash
curl -s http://localhost:8080/actuator | python3 -m json.tool
```

**Step 4: Gateway-specific actuator**
```bash
# All routes
curl -s http://localhost:8080/actuator/gateway/routes | python3 -m json.tool

# Global filters (with order numbers)
curl -s http://localhost:8080/actuator/gateway/globalfilters | python3 -m json.tool

# Route filters
curl -s http://localhost:8080/actuator/gateway/routefilters | python3 -m json.tool
```

**Key takeaway:** Actuator gives you deep runtime visibility into every service — health, metrics, configuration, and gateway-specific details — all through HTTP endpoints.

---

## Topic 9: Metrics with Prometheus & Grafana

### How Metrics Flow

```
Spring Boot App                    Prometheus                   Grafana
┌──────────────┐    scrape every   ┌──────────────┐   query    ┌──────────┐
│ Micrometer   │    5 seconds      │ Time-series  │   PromQL   │Dashboard │
│ Counters     │◄──────────────────│ Database     │◄───────────│ Panels   │
│ Timers       │    GET /actuator/ │              │            │          │
│ Gauges       │    prometheus     │ Stores all   │            │ Graphs   │
│              │                   │ metrics with │            │ Gauges   │
│ micrometer-  │                   │ timestamps   │            │ Alerts   │
│ registry-    │                   │              │            │          │
│ prometheus   │                   │ Retention:   │            │          │
│              │                   │ 15 days      │            │          │
└──────────────┘                   └──────────────┘            └──────────┘
```

### Prometheus Configuration

```yaml
# observability/prometheus/prometheus.yml
global:
  scrape_interval: 5s     # Scrape every 5 seconds

scrape_configs:
  - job_name: 'api-gateway'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['host.docker.internal:8080']   # Docker → host machine
        labels:
          application: 'api-gateway'

  - job_name: 'order-service'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['host.docker.internal:8081']
        labels:
          application: 'order-service'

  - job_name: 'inventory-service'
    metrics_path: '/actuator/prometheus'
    static_configs:
      - targets: ['host.docker.internal:8082']
        labels:
          application: 'inventory-service'
```

### Hands-On Steps

**Step 1: Verify Prometheus targets**
```bash
open http://localhost:9090/targets
```

**What to see:** Three targets, all showing state `UP` with the last scrape time.

**Step 2: Open the pre-built Grafana dashboard**
```bash
open http://localhost:3000
# Login: admin / admin
```

Navigate to: **Dashboards → Microservices → "Microservices Overview - Metrics, Logs & Traces"**

**Dashboard panels:**
- **Service Health Status** — green UP/red DOWN indicators
- **HTTP Request Rate** — requests per second per service
- **HTTP Response Time (p95)** — 95th percentile latency
- **Gateway Total Requests** — running counter
- **Gateway Error Rate** — percentage gauge
- **Orders Created** — business metric counter
- **Inventory Checks** — business metric counter
- **JVM Memory Used** — heap memory per service
- **Circuit Breaker State** — Resilience4j state

**Step 3: Generate traffic to see live metrics**
```bash
for i in $(seq 1 20); do
  curl -s http://localhost:8080/inventory -H "X-API-Key: demo-api-key-2024" > /dev/null
  curl -s http://localhost:8080/orders -H "X-API-Key: demo-api-key-2024" > /dev/null
  curl -s -X POST http://localhost:8080/orders \
    -H "Content-Type: application/json" \
    -H "X-API-Key: demo-api-key-2024" \
    -d "{\"productId\": \"PROD-00$((i % 3 + 1))\", \"quantity\": $i}" > /dev/null
done
echo "Traffic sent! Refresh Grafana."
```

**Step 4: Explore PromQL queries manually**

Navigate to: Grafana → **Explore** → select **Prometheus** datasource

```promql
# Request rate per service
rate(http_server_requests_seconds_count[1m])

# 95th percentile response time
histogram_quantile(0.95, rate(http_server_requests_seconds_bucket[1m]))

# Custom gateway counters
gateway_requests_total_total
gateway_errors_total_total

# Business metrics
orders_created_total_total
inventory_checks_total_total

# JVM heap memory
jvm_memory_used_bytes{area="heap"}

# Circuit breaker state
resilience4j_circuitbreaker_state
```

**Key takeaway:** Prometheus scrapes metrics from every service automatically. Grafana visualizes them in real-time dashboards. Custom Micrometer counters (orders created, inventory checks) appear alongside JVM and HTTP metrics.

---

## Topic 10: Centralized Logging with Loki

### How Logs Flow

```
Spring Boot Service
    │
    ▼
logback-spring.xml
    │
    ├→ CONSOLE appender (human-readable for terminal)
    │   Format: 14:00:00.123 [thread] [traceId,spanId] INFO class - message
    │
    └→ JSON_FILE appender (for Loki ingestion)
        File: ./logs/<service-name>.log
        Format: {"@timestamp":"...","level":"INFO","message":"...","service":"order-service","traceId":"abc123"}
            │
            ▼
        Promtail (Docker container)
            │ reads JSON files via volume mount
            │ extracts labels: service, level, traceId, spanId
            │ ships to Loki
            ▼
        Loki (Docker container)
            │ stores and indexes logs
            │ queryable via LogQL
            ▼
        Grafana
            │ Explore → Loki datasource
            └ Dashboard → Logs panel
```

### Logback Configuration

Each service has `logback-spring.xml` with two appenders:

```xml
<!-- Console: human-readable -->
<appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
        <pattern>%d{HH:mm:ss.SSS} [%thread] [%mdc{traceId:-},%mdc{spanId:-}] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
</appender>

<!-- JSON file: for Promtail → Loki -->
<appender name="JSON_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
    <file>../logs/${serviceName}.log</file>
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
        <customFields>{"service":"${serviceName}"}</customFields>
        <includeMdcKeyName>traceId</includeMdcKeyName>
        <includeMdcKeyName>spanId</includeMdcKeyName>
    </encoder>
</appender>
```

**LogstashEncoder** outputs each log line as a JSON object with automatic fields:
- `@timestamp`, `level`, `logger_name`, `message`, `thread_name`
- Plus custom: `service`, `traceId`, `spanId`

### Hands-On Steps

**Step 1: View logs in Grafana Explore**

Navigate to: Grafana → **Explore** → select **Loki** datasource

```logql
# All logs from all services
{job="spring-boot"}

# Logs from a specific service
{service="order-service"}
{service="api-gateway"}
{service="inventory-service"}

# Filter by log level
{service="api-gateway"} |= "ERROR"
{service="api-gateway"} |= "WARN"

# Search for a specific correlation ID
{job="spring-boot"} |= "correlationId=my-trace-001"

# Search for order creation logs
{service="order-service"} |= "Order" |= "created"

# Parse JSON and filter by structured fields
{job="spring-boot"} | json | level="ERROR"

# Count log lines per service per minute (log-based metric)
sum by (service) (rate({job="spring-boot"}[1m]))
```

**Step 2: Generate interesting log entries**
```bash
# 1. Successful order (INFO logs across 3 services)
curl -s -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-2024" \
  -d '{"productId": "PROD-001", "quantity": 2}' > /dev/null

# 2. Invalid JWT (WARN log in gateway)
curl -s http://localhost:8080/orders \
  -H "Authorization: Bearer invalid-token" > /dev/null

# 3. Non-existent product (logs in inventory-service)
curl -s http://localhost:8080/inventory/PROD-999 \
  -H "X-API-Key: demo-api-key-2024" > /dev/null

# 4. Rate limiting (WARN log in gateway)
for i in $(seq 1 35); do
  curl -s -o /dev/null http://localhost:8080/inventory -H "X-API-Key: demo-api-key-2024"
done
```

**Step 3: Search for these logs in Loki**
```logql
# Find the invalid JWT warning
{service="api-gateway"} |= "Invalid JWT"

# Find rate limit warnings
{service="api-gateway"} |= "Rate limit exceeded"

# Find inventory check for non-existent product
{service="inventory-service"} |= "PROD-999"
```

**Step 4: Use the Logs panel in the dashboard**

The pre-built dashboard has an **"Application Logs (Loki)"** panel at the bottom showing a live log stream from all services. Click any log line to expand and see all JSON fields.

**Key takeaway:** All service logs are aggregated in Loki. You can search across all services by text, filter by service/level, and use structured JSON fields. The traceId in log entries links directly to distributed traces.

---

## Topic 11: Distributed Tracing with Tempo

### What is Distributed Tracing?

When a request flows through multiple services, distributed tracing records the **timing and path** of each step as a "trace" made up of "spans":

```
                         ┌─── Trace (single request) ────────────────────────┐
                         │                                                    │
Trace ID: abc123         │                                                    │
                         │                                                    │
┌─ Span 1: api-gateway ─┼─── POST /orders ────────────── 150ms ─────────────┐│
│                        │                                                   ││
│  ┌─ Span 2: order ────┼─── POST /orders ───────── 120ms ──────────────┐  ││
│  │                     │                                               │  ││
│  │  ┌─ Span 3: inv ───┼── GET /inventory/PROD-001 ─── 25ms ─────┐   │  ││
│  │  └─────────────────┘│                                         │   │  ││
│  └─────────────────────┘                                         │   │  ││
└─────────────────────────────────────────────────────────────────────────────┘│
                         │                                                    │
                         └────────────────────────────────────────────────────┘

All 3 spans share the same Trace ID (abc123).
Each span records: service name, operation, duration, status code.
```

### How Tracing Works in This Project

```
Spring Boot                  Micrometer                 OpenTelemetry              Tempo
┌──────────────┐            ┌──────────────┐           ┌──────────────┐          ┌──────┐
│ HTTP request │ → observe →│ Observation  │ → bridge →│ OTel SDK     │ → export │Zipkin│
│ received     │            │ API          │           │ (creates     │   Zipkin  │receiv│
│              │            │              │           │  spans)      │   format  │er    │
│ RestTemplate │ → observe →│ Observation  │ → bridge →│ OTel SDK     │ → export │:9411 │
│ call         │            │ API          │           │ (child span) │          │      │
└──────────────┘            └──────────────┘           └──────────────┘          └──────┘
```

**Dependencies that enable this:**
```xml
<!-- Bridges Micrometer's Observation API to OpenTelemetry -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>

<!-- Exports spans in Zipkin format to Tempo -->
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-zipkin</artifactId>
</dependency>
```

**Configuration:**
```properties
# Trace 100% of requests (for demo; in production use 0.1 = 10%)
management.tracing.sampling.probability=1.0

# Send traces to Tempo's Zipkin receiver
management.zipkin.tracing.endpoint=http://localhost:9411/api/v2/spans
```

### Hands-On Steps

**Step 1: Generate a multi-service trace**
```bash
# POST /orders goes: Gateway → Order Service → Inventory Service (3 spans)
curl -s -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-2024" \
  -d '{"productId": "PROD-001", "quantity": 2}' | python3 -m json.tool
```

**Step 2: Search for traces in Grafana**

Navigate to: Grafana → **Explore** → select **Tempo** datasource

**Search options:**
- **Service Name:** select `api-gateway`, `order-service`, or `inventory-service`
- **Span Name:** `POST`, `GET`
- **Min Duration:** `50ms` (to find slow traces)
- Click **"Run query"**

**Step 3: Read the trace waterfall**

Click on any trace result to open the **span waterfall view**:

```
┌─ api-gateway ────────── POST /orders ──────────── 150ms ──────┐
│                                                                │
│  ┌─ order-service ────── POST /orders ──────── 120ms ────┐    │
│  │                                                        │    │
│  │  ┌─ inventory-service ── GET /inventory ── 25ms ──┐   │    │
│  │  └────────────────────────────────────────────────┘   │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────┘
```

**Click on each span to see details:**
- **Service name** — which service handled it
- **Duration** — how long it took
- **HTTP method, URL, status code**
- **Tags:** `http.method=POST`, `http.url=/orders`, `http.status_code=200`

**Step 4: Use TraceQL to query traces**

In Tempo's **TraceQL** tab:
```
{ .service.name = "order-service" && duration > 100ms }
```

**Step 5: Search by specific Trace ID**

If you have a traceId from a log entry, paste it directly into Tempo's **Trace ID** search field to jump to that exact trace.

**Key takeaway:** Distributed tracing shows the complete journey of a request across services. You can see exactly where time is spent and which service is the bottleneck.

---

## Topic 12: Correlating Metrics, Logs & Traces

### The Golden Triangle of Observability

The real power comes from **connecting all three signals**:

```
        METRICS                    TRACES                     LOGS
   "What is happening?"      "Where is it slow?"       "Why is it failing?"
         │                          │                         │
   ┌─────┴─────┐             ┌──────┴──────┐           ┌─────┴─────┐
   │ Dashboard │             │ Waterfall   │           │ Search    │
   │ shows p95 │────────────→│ shows slow  │──────────→│ shows     │
   │ latency   │  "find the  │ span in     │ "find the │ exact     │
   │ spike     │   trace"    │ order-svc   │  logs"    │ error msg │
   └───────────┘             └─────────────┘           └───────────┘
```

### How Correlation Works

1. **Metrics → Traces:** Spot a metric anomaly → search Tempo for traces matching that service and time range
2. **Traces → Logs:** Found a trace → copy the `traceId` → search Loki for all log lines with that ID
3. **Logs → Traces:** See a traceId in a log line → click it → Grafana jumps to the trace in Tempo

The **Loki-to-Tempo auto-linking** is configured in `datasources.yaml`:
```yaml
- name: Loki
  jsonData:
    derivedFields:
      - name: TraceID
        datasourceUid: tempo
        matcherRegex: "traceId=(\\w+)"    # Regex to find traceId in logs
        url: "$${__value.raw}"             # Click → opens trace in Tempo
```

### Hands-On Steps — Full Correlation Workflow

**Step 1: Generate traffic**
```bash
for i in $(seq 1 15); do
  curl -s -X POST http://localhost:8080/orders \
    -H "Content-Type: application/json" \
    -H "X-API-Key: demo-api-key-2024" \
    -d "{\"productId\": \"PROD-00$((i % 3 + 1))\", \"quantity\": $i}" > /dev/null
done
echo "Orders created!"
```

**Step 2: Check metrics in Prometheus (Grafana Explore)**

Navigate to: Grafana → Explore → **Prometheus**
```promql
# Order creation rate
rate(orders_created_total_total[1m])

# Order processing time (p95)
histogram_quantile(0.95, rate(orders_processing_time_seconds_bucket[1m]))
```

**Step 3: Find traces in Tempo (Grafana Explore)**

Navigate to: Grafana → Explore → **Tempo**
- Service Name: `order-service`
- Min Duration: `50ms`
- Click "Run query"
- Click the longest trace

**Observe the span waterfall:** See whether delay is in order-service processing or inventory-service call.

**Step 4: Correlate with logs in Loki**

Copy the `traceId` from the Tempo trace, then:

Navigate to: Grafana → Explore → **Loki**
```logql
{job="spring-boot"} |= "traceId=<paste-your-trace-id>"
```

You'll see log lines from ALL services that participated in that trace.

### Hands-On Steps — Failure Scenario

**Step 1: Stop inventory-service**
```bash
# In Terminal 3: Ctrl+C to stop inventory-service
```

**Step 2: Create an order (inventory check will fail gracefully)**
```bash
curl -s -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-2024" \
  -d '{"productId": "PROD-001", "quantity": 5}' | python3 -m json.tool
```

**Expected:**
```json
{
    "orderId": 16,
    "productId": "PROD-001",
    "quantity": 5,
    "status": "CREATED",
    "createdBy": "api-key-user",
    "inventoryCheck": "UNAVAILABLE",
    "correlationId": "def45678"
}
```

**Step 3: Investigate in Grafana**

1. **Metrics:** Check gateway error rate — has it spiked?
   ```promql
   gateway_errors_total_total
   ```

2. **Traces:** Search Tempo for recent `order-service` traces — you'll see the `inventory-service` span is missing or shows an error.

3. **Logs:** Search Loki for the exact error:
   ```logql
   {service="order-service"} |= "Inventory service unavailable"
   ```

**Step 4: Restart inventory-service**
```bash
cd inventory-service && mvn spring-boot:run
```

Verify recovery:
```bash
curl -s -X POST http://localhost:8080/orders \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-2024" \
  -d '{"productId": "PROD-001", "quantity": 1}' | python3 -m json.tool
# inventoryCheck should now show product details again
```

**Key takeaway:** The three pillars of observability — metrics, logs, and traces — work together. Metrics tell you WHAT is wrong, traces tell you WHERE the problem is, and logs tell you WHY it happened. Grafana connects all three with auto-linking between Loki and Tempo.

---

## All Ports & URLs Reference

| Service/Tool | Port | URL | Purpose |
|-------------|------|-----|---------|
| **Eureka Dashboard** | 8761 | http://localhost:8761 | Service registry UI |
| **API Gateway** | 8080 | http://localhost:8080 | Single entry point for all API calls |
| **Order Service** | 8081 | http://localhost:8081 | Order management |
| **Inventory Service** | 8082 | http://localhost:8082 | Inventory management |
| **Prometheus** | 9090 | http://localhost:9090 | Metrics storage & queries |
| **Prometheus Targets** | 9090 | http://localhost:9090/targets | Verify scrape targets |
| **Grafana** | 3000 | http://localhost:3000 | Dashboards (admin/admin) |
| **Loki** | 3100 | http://localhost:3100 | Log aggregation |
| **Promtail** | 9080 | http://localhost:9080 | Log file collector |
| **Tempo API** | 3200 | http://localhost:3200 | Trace storage API |
| **Tempo Zipkin** | 9411 | http://localhost:9411 | Zipkin trace receiver |

---

## Cleanup

```bash
# Stop all Spring Boot services (Ctrl+C in each terminal)

# Stop observability stack (keeps data)
docker compose -f docker-compose-observability.yml down

# Stop AND remove all persistent data (volumes)
docker compose -f docker-compose-observability.yml down -v

# Remove generated log files
rm -rf logs/
```
