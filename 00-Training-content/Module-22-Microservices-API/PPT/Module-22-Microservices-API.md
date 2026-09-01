# Microservices & API
## Module 22 | Sustain Engineering Training | Days 24-25

---

## Agenda -- Day 24

| # | Topic |
|---|-------|
| 01 | Monolithic vs Microservices Architecture |
| 02 | Microservices Architecture Patterns |
| 03 | Characteristics of Microservices |
| 04 | Data Handling in Microservices |
| 05 | Inter-Service Communication |
| 06 | Synchronous vs Asynchronous Communication |
| 07 | Service Discovery & Registry |
| 08 | API Design Principles |
| 09 | Lab: Identify Microservice Boundaries |
| 10 | Day 24 Wrap-up |

---

## Agenda -- Day 25

| # | Topic |
|---|-------|
| 01 | API Patterns & REST Best Practices |
| 02 | Domain-Driven Design (DDD) |
| 03 | API Gateway Pattern |
| 04 | CRUD Microservice: Setup & Controllers |
| 05 | Repository Pattern & Data Access |
| 06 | API Monitoring & Observability |
| 07 | API Security & Authentication |
| 08 | Routing & Load Balancing |
| 09 | LLM API Security |
| 10 | Lab: Build & Secure a Microservice |
| 11 | Module Wrap-up |

---

## Monolithic Architecture

### Traditional Single Application

```
┌─────────────────────────────────────────┐
│            FoodExpress Monolith          │
│                                         │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │   Menu   │ │  Orders  │ │ Payment │ │
│  │  Module  │ │  Module  │ │ Module  │ │
│  └──────────┘ └──────────┘ └─────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │   Auth   │ │  Rating  │ │ Delivery│ │
│  │  Module  │ │  Module  │ │ Module  │ │
│  └──────────┘ └──────────┘ └─────────┘ │
│                                         │
│         Shared Database (MySQL)         │
└─────────────────────────────────────────┘
```

All modules packaged together, deployed as one unit.

---

## Monolith: Pros and Cons

| Pros | Cons |
|------|------|
| Simple to develop initially | Grows unwieldy over time |
| Simple to deploy (one artifact) | Every change requires full redeployment |
| Simple to test (one process) | Tightly coupled modules |
| No network latency between modules | Single point of failure |
| Easy to debug (one process) | Technology lock-in |
| ACID transactions | Scaling = scaling everything |

**FoodExpress Monolith problem:** A bug in the rating module caused the entire application (including ordering and payments) to crash.

---

## Microservices Architecture

### Decomposed by Business Capability

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Menu    │  │  Order   │  │ Payment  │  │ Delivery │
│ Service  │  │ Service  │  │ Service  │  │ Service  │
│ Node.js  │  │  Java    │  │  Java    │  │ Node.js  │
│ MongoDB  │  │  MySQL   │  │ Postgres │  │  Redis   │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │             │
     └─────────────┴─────────────┴─────────────┘
                        │
                 API Gateway
                        │
                    Clients
```

Each service: independently developed, deployed, and scaled.

---

## Monolithic vs Microservices

| Aspect | Monolithic | Microservices |
|--------|-----------|---------------|
| **Deployment** | All-or-nothing | Independent per service |
| **Scaling** | Scale entire app | Scale individual services |
| **Technology** | Single stack | Polyglot (best tool per service) |
| **Team size** | Large team, one codebase | Small teams per service |
| **Failure isolation** | One failure crashes all | Failure contained to one service |
| **Data** | Shared database | Database per service |
| **Complexity** | In the codebase | In the network |
| **Testing** | Simpler E2E tests | Complex integration tests |
| **Time to market** | Slower (coordinate releases) | Faster (independent releases) |

---

## When to Use Microservices

### Not Every Project Needs Microservices

```
Startup/Small Team    ────────────>    Large/Scaling Team
     Monolith                           Microservices
     (Start here)                       (Evolve to here)

 "If you can't build a good monolith,
  what makes you think microservices
  are the answer?"
                    -- Simon Brown
```

### Use Microservices When:
- Team is large (multiple squads)
- Different parts need different scaling
- Different parts need different tech stacks
- Independent deployment is critical
- Organization structure supports it (Conway's Law)

---

## Microservices Characteristics

### The 9 Key Characteristics

| # | Characteristic | Description |
|---|---------------|-------------|
| 1 | Componentization via services | Not libraries, but independently deployable services |
| 2 | Organized around business capabilities | Not technical layers (UI, DB) but business domains |
| 3 | Products, not projects | Teams own services for their lifetime |
| 4 | Smart endpoints, dumb pipes | Logic in services, not in middleware |
| 5 | Decentralized governance | Each team chooses its own tech stack |
| 6 | Decentralized data management | Database per service |
| 7 | Infrastructure automation | CI/CD, containers, orchestration |
| 8 | Design for failure | Circuit breakers, fallbacks, retries |
| 9 | Evolutionary design | Services can be replaced independently |

---

## FoodExpress Microservice Decomposition

| Service | Responsibility | Tech Stack | Database |
|---------|---------------|-----------|----------|
| **Menu Service** | CRUD menu items, search, categories | Node.js + Express | MongoDB |
| **Order Service** | Create/track orders, order history | Java + Spring Boot | MySQL |
| **Payment Service** | Process payments, refunds | Java + Spring Boot | PostgreSQL |
| **User Service** | Auth, profiles, addresses | Node.js + Express | PostgreSQL |
| **Delivery Service** | Assign riders, track delivery | Node.js + Express | Redis + MongoDB |
| **Rating Service** | Restaurant/rider ratings | Python + FastAPI | MongoDB |
| **Notification Service** | Email, SMS, push notifications | Node.js + Express | Redis (queue) |

---

## Data Handling in Microservices

### Database Per Service

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Menu    │    │  Order   │    │ Payment  │
│ Service  │    │ Service  │    │ Service  │
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
┌────▼─────┐    ┌────▼─────┐    ┌────▼─────┐
│ MongoDB  │    │  MySQL   │    │ Postgres │
│ (menus)  │    │ (orders) │    │(payments)│
└──────────┘    └──────────┘    └──────────┘
```

### Rules

- Each service owns its data exclusively
- No direct database access from other services
- Services communicate via APIs, not shared databases
- Data consistency via eventual consistency patterns (Saga)

---

## Data Consistency: Saga Pattern

### Example: FoodExpress Order Flow

```
Order Created                Payment                 Delivery
    │                           │                       │
    ▼                           ▼                       ▼
┌─────────┐  success  ┌──────────────┐  success  ┌───────────┐
│ Create  │──────────>│   Process    │──────────>│  Assign   │
│  Order  │           │   Payment    │           │  Rider    │
└─────────┘           └──────────────┘           └───────────┘
    │                       │                         │
    │  failure              │  failure                │  failure
    ▼                       ▼                         ▼
┌─────────┐           ┌──────────────┐           ┌───────────┐
│ Cancel  │<──────────│    Refund    │<──────────│  Cancel   │
│  Order  │           │   Payment    │           │ Delivery  │
└─────────┘           └──────────────┘           └───────────┘
```

Each step has a **compensating transaction** for rollback.

---

## Inter-Service Communication

### Synchronous (Request-Response)

```
Menu Service ──── HTTP/REST ────> Order Service
                 <── Response ──
```

- **REST APIs:** Most common, HTTP + JSON
- **gRPC:** High-performance, binary protocol, Protocol Buffers
- Caller waits for response (blocking)

### Asynchronous (Event-Driven)

```
Order Service ──── Event ────> Message Broker ────> Notification Service
                              (RabbitMQ/Kafka)  ──> Delivery Service
                                                ──> Analytics Service
```

- **Message queues:** RabbitMQ, SQS
- **Event streams:** Kafka, Kinesis
- Caller does not wait (non-blocking)

---

## Sync vs Async: When to Use

| Aspect | Synchronous | Asynchronous |
|--------|------------|--------------|
| Use when | Need immediate response | Fire-and-forget, or long processing |
| Coupling | Tight (caller depends on callee) | Loose (decoupled via broker) |
| Failure | Cascading failures possible | Resilient (messages queued) |
| Latency | Adds up across service calls | Better for high latency operations |
| Debugging | Easier to trace | Harder to trace (distributed) |

### FoodExpress Examples

| Flow | Type | Why |
|------|------|-----|
| Get menu items | Sync (REST) | Need immediate response for UI |
| Place order | Sync (REST) | Need order ID immediately |
| Send order confirmation email | Async (Queue) | Can be delayed seconds |
| Update analytics | Async (Kafka) | Doesn't block user flow |

---

## Service Discovery

### The Problem

In microservices, service instances come and go (scaling, restarts, deployments). How does Service A find Service B?

### Solutions

| Pattern | How It Works | Example |
|---------|-------------|---------|
| **Client-side discovery** | Client queries registry, picks instance | Netflix Eureka |
| **Server-side discovery** | Load balancer queries registry | AWS ALB, Kubernetes Service |
| **DNS-based** | Services registered as DNS records | Consul, Route53 |

```
┌─────────────┐    1. Register    ┌──────────────┐
│ Order Svc   │ ───────────────> │   Service    │
│ (3 instances)│                  │  Registry    │
└─────────────┘                  │  (Eureka)    │
                                 └──────┬───────┘
┌─────────────┐    2. Discover        │
│ Menu Svc    │ <─────────────────────┘
│             │    3. Call Order Svc
│             │ ──> Order Svc Instance 2
└─────────────┘
```

---

## API Design Principles

### RESTful API Design

| Principle | Description | Example |
|-----------|-------------|---------|
| **Resources** | Use nouns, not verbs | `/api/orders` not `/api/getOrders` |
| **HTTP methods** | Use proper methods | GET, POST, PUT, DELETE |
| **Status codes** | Use standard codes | 200, 201, 400, 404, 500 |
| **Versioning** | Version your APIs | `/api/v1/orders` |
| **Pagination** | Don't return everything | `?page=1&size=10` |
| **Filtering** | Let clients filter | `?status=delivered&date=2026-07-27` |
| **HATEOAS** | Include navigation links | `"_links": { "next": "/api/orders?page=2" }` |

---

## REST API Design: HTTP Methods

```
Resource: /api/v1/orders

GET    /api/v1/orders          → List orders (with pagination)
GET    /api/v1/orders/1001     → Get order #1001
POST   /api/v1/orders          → Create a new order
PUT    /api/v1/orders/1001     → Update order #1001 (full replace)
PATCH  /api/v1/orders/1001     → Partial update order #1001
DELETE /api/v1/orders/1001     → Cancel order #1001
```

### Response Format (JSON)

```json
{
  "id": 1001,
  "customerId": 42,
  "items": [
    { "name": "Butter Chicken", "quantity": 2, "price": 349.00 },
    { "name": "Naan", "quantity": 4, "price": 49.00 }
  ],
  "total": 894.00,
  "status": "IN_PROGRESS",
  "createdAt": "2026-07-27T09:15:30Z",
  "_links": {
    "self": "/api/v1/orders/1001",
    "customer": "/api/v1/customers/42",
    "cancel": "/api/v1/orders/1001/cancel"
  }
}
```

---

## HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| `200` | OK | Successful GET, PUT, PATCH |
| `201` | Created | Successful POST (resource created) |
| `204` | No Content | Successful DELETE |
| `400` | Bad Request | Invalid input, validation error |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Authenticated but not authorized |
| `404` | Not Found | Resource doesn't exist |
| `409` | Conflict | Duplicate resource, version conflict |
| `422` | Unprocessable Entity | Validation errors on the body |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Unexpected server-side error |
| `502` | Bad Gateway | Upstream service unavailable |
| `503` | Service Unavailable | Service temporarily down |

---

## API Patterns: Domain-Driven Design (DDD)

### Bounded Contexts

```
┌─────────────────────┐  ┌─────────────────────┐
│   Order Context     │  │  Delivery Context    │
│                     │  │                      │
│  Order              │  │  Delivery            │
│  OrderItem          │  │  Rider               │
│  OrderStatus        │  │  Route               │
│  Customer (subset)  │  │  Order (reference)   │
└─────────────────────┘  └──────────────────────┘

┌─────────────────────┐  ┌─────────────────────┐
│   Menu Context      │  │  Payment Context     │
│                     │  │                      │
│  MenuItem           │  │  Payment             │
│  Category           │  │  Transaction         │
│  Restaurant         │  │  Refund              │
│  Price              │  │  Order (reference)   │
└─────────────────────┘  └──────────────────────┘
```

Each bounded context has its own **ubiquitous language** and **data model**.

---

## DDD: Strategic Patterns

| Pattern | Description | FoodExpress Example |
|---------|-------------|---------------------|
| **Bounded Context** | Clear boundary around a domain model | Order context vs Payment context |
| **Ubiquitous Language** | Shared vocabulary within a context | "Order" means different things in Order vs Delivery |
| **Context Map** | Relationships between contexts | Order publishes events, Delivery consumes |
| **Aggregate** | Cluster of entities treated as a unit | Order + OrderItems = Order Aggregate |
| **Entity** | Object with identity | Order (identified by orderId) |
| **Value Object** | Object without identity | Money (amount + currency) |
| **Domain Event** | Something that happened | OrderPlaced, PaymentCompleted |
| **Repository** | Abstraction for data access | OrderRepository |

---

## API Gateway Pattern

### The Problem

Clients must know about every microservice and make multiple calls.

### The Solution

```
                              ┌──────────────┐
   Mobile App ──────────────> │              │ ──> Menu Service
   Web Browser ─────────────> │  API Gateway │ ──> Order Service
   Third-party ─────────────> │              │ ──> Payment Service
                              └──────────────┘ ──> User Service

Gateway responsibilities:
- Request routing
- Authentication/Authorization
- Rate limiting
- Load balancing
- Response aggregation
- SSL termination
- Logging/Monitoring
```

---

## API Gateway: Implementation

```yaml
# Kong API Gateway configuration for FoodExpress

services:
  - name: menu-service
    url: http://menu-service:3000
    routes:
      - name: menu-route
        paths: ["/api/v1/menu"]
        methods: ["GET"]
    plugins:
      - name: rate-limiting
        config:
          minute: 100
      - name: jwt
        config:
          secret_is_base64: false

  - name: order-service
    url: http://order-service:8080
    routes:
      - name: order-route
        paths: ["/api/v1/orders"]
        methods: ["GET", "POST", "PUT"]
    plugins:
      - name: rate-limiting
        config:
          minute: 50
      - name: jwt
      - name: request-size-limiting
        config:
          allowed_payload_size: 10  # MB
```

**Popular API Gateways:** Kong, AWS API Gateway, Nginx, Spring Cloud Gateway, Apigee

---

## CRUD Microservice: Project Setup

### FoodExpress Menu Service (Spring Boot)

```java
// pom.xml dependencies
// spring-boot-starter-web
// spring-boot-starter-data-jpa
// spring-boot-starter-validation
// mysql-connector-java
// lombok

// application.yml
server:
  port: 8080
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/foodexpress_menu
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
```

---

## CRUD Microservice: Entity

```java
@Entity
@Table(name = "menu_items")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class MenuItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Name is required")
    @Size(max = 100)
    private String name;

    @NotBlank(message = "Description is required")
    @Size(max = 500)
    private String description;

    @NotNull(message = "Price is required")
    @DecimalMin(value = "0.01", message = "Price must be positive")
    private BigDecimal price;

    @NotBlank
    private String category;

    @Column(name = "is_vegetarian")
    private boolean vegetarian;

    @Column(name = "is_available")
    private boolean available = true;

    @Column(name = "image_url")
    private String imageUrl;

    @Column(name = "restaurant_id")
    private Long restaurantId;
}
```

---

## CRUD Microservice: Repository

```java
@Repository
public interface MenuItemRepository extends JpaRepository<MenuItem, Long> {

    List<MenuItem> findByCategory(String category);

    List<MenuItem> findByCategoryAndAvailableTrue(String category);

    List<MenuItem> findByVegetarianTrueAndAvailableTrue();

    @Query("SELECT m FROM MenuItem m WHERE m.name LIKE %:query% " +
           "OR m.description LIKE %:query%")
    List<MenuItem> search(@Param("query") String query);

    List<MenuItem> findByRestaurantIdAndAvailableTrue(Long restaurantId);

    @Query("SELECT m FROM MenuItem m WHERE m.price BETWEEN :min AND :max " +
           "AND m.available = true ORDER BY m.price ASC")
    List<MenuItem> findByPriceRange(@Param("min") BigDecimal min,
                                    @Param("max") BigDecimal max);
}
```

---

## CRUD Microservice: Controller

```java
@RestController
@RequestMapping("/api/v1/menu")
@Validated
public class MenuController {

    private final MenuItemService menuService;

    @Autowired
    public MenuController(MenuItemService menuService) {
        this.menuService = menuService;
    }

    @GetMapping("/items")
    public ResponseEntity<Page<MenuItem>> getItems(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String category) {
        Page<MenuItem> items = menuService.getItems(page, size, category);
        return ResponseEntity.ok(items);
    }

    @GetMapping("/items/{id}")
    public ResponseEntity<MenuItem> getItem(@PathVariable Long id) {
        return menuService.getItemById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/items")
    public ResponseEntity<MenuItem> createItem(
            @Valid @RequestBody MenuItem item) {
        MenuItem created = menuService.createItem(item);
        URI location = URI.create("/api/v1/menu/items/" + created.getId());
        return ResponseEntity.created(location).body(created);
    }

    @PutMapping("/items/{id}")
    public ResponseEntity<MenuItem> updateItem(
            @PathVariable Long id,
            @Valid @RequestBody MenuItem item) {
        return menuService.updateItem(id, item)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/items/{id}")
    public ResponseEntity<Void> deleteItem(@PathVariable Long id) {
        menuService.deleteItem(id);
        return ResponseEntity.noContent().build();
    }
}
```

---

## CRUD Microservice: Error Handling

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(
            ResourceNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage(),
            LocalDateTime.now()
        );
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
            MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .collect(Collectors.toList());

        ErrorResponse error = new ErrorResponse(
            HttpStatus.BAD_REQUEST.value(),
            "Validation failed",
            errors,
            LocalDateTime.now()
        );
        return ResponseEntity.badRequest().body(error);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneral(Exception ex) {
        // Log the full exception internally
        log.error("Unexpected error", ex);
        // Return sanitized message to client
        ErrorResponse error = new ErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "An internal error occurred",
            LocalDateTime.now()
        );
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

---

## API Monitoring & Observability

### The Three Pillars

| Pillar | What | Tools |
|--------|------|-------|
| **Logs** | Textual records of events | ELK Stack, Loki, CloudWatch |
| **Metrics** | Numeric measurements over time | Prometheus, Grafana, Datadog |
| **Traces** | Request flow across services | Jaeger, Zipkin, AWS X-Ray |

### Key API Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Request rate | Requests per second | Drop > 50% |
| Error rate | % of 4xx/5xx responses | > 1% for 5 min |
| Latency (P50, P95, P99) | Response time percentiles | P99 > 2s |
| Saturation | CPU, memory, connection pool | > 80% |

---

## API Monitoring: Health Endpoints

```java
// Spring Boot Actuator health endpoint
// Dependency: spring-boot-starter-actuator

// application.yml
management:
  endpoints:
    web:
      exposure:
        include: health, metrics, info
  endpoint:
    health:
      show-details: when-authorized

// Custom health indicator
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    @Autowired
    private DataSource dataSource;

    @Override
    public Health health() {
        try (Connection conn = dataSource.getConnection()) {
            if (conn.isValid(2)) {
                return Health.up()
                    .withDetail("database", "MySQL")
                    .withDetail("status", "Connected")
                    .build();
            }
        } catch (SQLException e) {
            return Health.down()
                .withDetail("error", e.getMessage())
                .build();
        }
        return Health.down().build();
    }
}
```

---

## API Security: Authentication

### JWT (JSON Web Token) Flow

```
1. Login
Client ──── POST /auth/login ────> Auth Service
       <── JWT Token ──────────

2. Authenticated Request
Client ──── GET /api/orders ──────> API Gateway
            Header: Authorization:    │
            Bearer eyJhbGciOi...      │ Verify JWT
                                      │
                                      ▼
                              ┌──────────────┐
                              │ Order Service │
                              │ (trusted)     │
                              └──────────────┘
```

### JWT Structure

```
Header.Payload.Signature

{                           {                          HMACSHA256(
  "alg": "HS256",            "sub": "42",               base64(header) + "." +
  "typ": "JWT"                "name": "Priya",           base64(payload),
}                             "role": "CUSTOMER",        secret
                              "exp": 1722000000        )
                            }
```

---

## API Security: Best Practices

| Practice | Implementation | FoodExpress |
|----------|---------------|-------------|
| **HTTPS everywhere** | TLS certificates on all endpoints | All APIs enforce HTTPS |
| **Authentication** | JWT or OAuth2 tokens | JWT with 1-hour expiry |
| **Authorization** | Role-based access (RBAC) | CUSTOMER, ADMIN, DELIVERY roles |
| **Rate limiting** | Token bucket or fixed window | 100 req/min per user |
| **Input validation** | Schema validation, sanitization | Bean Validation in Spring |
| **CORS** | Restrict allowed origins | Only `foodexpress.in` |
| **API keys** | For third-party integrations | Partner restaurants get API keys |
| **Audit logging** | Log who did what when | All write operations logged |

---

## API Security: OAuth2 Flows

```
┌────────┐     1. Auth Request     ┌─────────────┐
│        │ ──────────────────────> │             │
│ Client │     2. Login Page       │   Auth      │
│  (App) │ <────────────────────── │  Server     │
│        │     3. Credentials      │ (Keycloak)  │
│        │ ──────────────────────> │             │
│        │     4. Auth Code        │             │
│        │ <────────────────────── │             │
│        │     5. Exchange Code    │             │
│        │ ──────────────────────> │             │
│        │     6. Access Token     │             │
│        │ <────────────────────── │             │
└───┬────┘                        └─────────────┘
    │
    │ 7. API call with token
    ▼
┌──────────┐
│ Resource │
│  Server  │
│ (API)    │
└──────────┘
```

---

## Routing & Load Balancing

### Load Balancing Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Round Robin** | Distribute requests sequentially | Equal-capacity servers |
| **Least Connections** | Route to server with fewest active connections | Varying request durations |
| **IP Hash** | Same client IP always goes to same server | Session affinity |
| **Weighted** | Route based on server capacity | Mixed hardware |
| **Random** | Random server selection | Simple, works well at scale |

```
                    Load Balancer (Nginx/HAProxy)
                           │
              ┌────────────┼────────────┐
              │            │            │
         Instance 1   Instance 2   Instance 3
         (weight: 3)  (weight: 2)  (weight: 1)
```

---

## Circuit Breaker Pattern

### Prevent Cascade Failures

```
         CLOSED                  OPEN                    HALF-OPEN
    ┌──────────────┐        ┌──────────┐           ┌──────────────┐
    │ Normal flow  │        │ Fast fail │           │ Test request │
    │ Track errors │        │ No calls  │           │ If success:  │
    │              │        │ to service│           │   → CLOSED   │
    │ If errors >  │        │           │           │ If failure:  │
    │ threshold:   │──────> │ After     │──────────>│   → OPEN     │
    │ → OPEN       │        │ timeout:  │           │              │
    └──────────────┘        │ → HALF-   │           └──────────────┘
                            │   OPEN    │
                            └──────────┘
```

```java
// Resilience4j Circuit Breaker
@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
public PaymentResponse processPayment(PaymentRequest request) {
    return paymentClient.charge(request);
}

public PaymentResponse paymentFallback(PaymentRequest request, Exception ex) {
    return new PaymentResponse("PENDING", "Payment queued for retry");
}
```

---

## LLM API Security

### Securing AI/LLM Integrations

| Risk | Description | Mitigation |
|------|-------------|------------|
| **Prompt Injection** | Malicious input manipulating LLM behavior | Input sanitization, prompt hardening |
| **Data Leakage** | LLM exposing sensitive data in responses | Output filtering, PII detection |
| **API Key Exposure** | LLM API keys committed to code | Secrets management (Vault, env vars) |
| **Cost Abuse** | Unlimited API calls to expensive LLM endpoints | Rate limiting, budget caps, token limits |
| **Model Poisoning** | Training data manipulation | Use trusted models, validate outputs |

### FoodExpress AI Use Case

```python
# FoodExpress uses LLM for menu item descriptions
# Security controls:

# 1. Rate limit LLM API calls
@rate_limit(max_calls=100, period=3600)
def generate_description(item_name, ingredients):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "Generate a menu description. Max 50 words. "
                       "Do NOT include pricing or health claims."
        }, {
            "role": "user",
            "content": f"Item: {sanitize(item_name)}, "
                       f"Ingredients: {sanitize(ingredients)}"
        }],
        max_tokens=100  # 2. Token limit
    )
    # 3. Output validation
    description = response.choices[0].message.content
    return validate_output(description)
```

---

## LLM API Security: Best Practices

```
┌─────────────────────────────────────────────┐
│           LLM API Security Layers           │
│                                             │
│  1. INPUT LAYER                             │
│     ├── Sanitize user input                 │
│     ├── Validate input length               │
│     └── Block injection patterns            │
│                                             │
│  2. API LAYER                               │
│     ├── API key rotation                    │
│     ├── Rate limiting per user              │
│     ├── Request/response logging            │
│     └── Token budget per request            │
│                                             │
│  3. OUTPUT LAYER                            │
│     ├── PII detection and redaction         │
│     ├── Content filtering                   │
│     ├── Response validation                 │
│     └── Hallucination detection             │
│                                             │
│  4. MONITORING LAYER                        │
│     ├── Cost tracking per endpoint          │
│     ├── Anomaly detection                   │
│     ├── Usage dashboards                    │
│     └── Audit logging                       │
└─────────────────────────────────────────────┘
```

---

## Microservices Anti-Patterns

| Anti-Pattern | Description | Fix |
|-------------|-------------|-----|
| **Distributed Monolith** | Services coupled, must deploy together | Proper bounded contexts, async communication |
| **Shared Database** | Multiple services access same tables | Database per service |
| **No API Versioning** | Breaking changes affect all consumers | Version your APIs: `/api/v1/`, `/api/v2/` |
| **Chatty Services** | Too many inter-service calls per request | Aggregate data, use BFF pattern |
| **No Circuit Breaker** | One slow service cascades failures | Implement circuit breakers (Resilience4j) |
| **Too Many Services** | Nano-services with trivial logic | Merge related services, right-size boundaries |
| **No Observability** | Can't trace requests across services | Distributed tracing (Jaeger/Zipkin) |

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Monolith vs Microservices | Start with monolith; evolve to microservices when team/scale demands it |
| Characteristics | Independent deployment, database per service, organized by business capability |
| Data handling | Database per service; Saga pattern for distributed transactions |
| Communication | Sync (REST) for immediate responses; Async (queues) for fire-and-forget |
| API Design | RESTful resources, proper HTTP methods and status codes, versioning |
| DDD | Bounded contexts define service boundaries; ubiquitous language within each |
| API Gateway | Single entry point for routing, auth, rate limiting, monitoring |
| CRUD Service | Entity -> Repository -> Service -> Controller pattern |
| Security | JWT/OAuth2, HTTPS, rate limiting, CORS, input validation |
| LLM Security | Prompt injection defense, output filtering, cost controls, PII detection |
| Patterns | Circuit breaker, service discovery, saga, event-driven |

> **Next: Module 23 -- Docker (Containerization)**
