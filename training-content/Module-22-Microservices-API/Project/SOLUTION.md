# Microservices & API -- Trainer Solutions & Hints
## Module 22 | Days 24-25

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix REST Controller | Version prefix `/api/v1/`, service layer, GET for retrieval, pagination, 404 for missing, @Valid, 201 Created, existence check on delete | Students fix the HTTP method but keep the verb in the URL (`/getItems`). REST uses nouns + HTTP methods | Ask: "If you add a new required field next month, how do v1 consumers handle it?" (API versioning) |
| 2 | Fix API Gateway | Remove TRACE, add version to routes, JWT on payment/orders, IP restrict admin, rate limit all services | Students add auth to all services including public menu browsing. Discuss which endpoints need auth | Ask: "Should the menu browsing endpoint require authentication?" (No -- it's public) |
| 3 | Fix Inter-Service Communication | Timeout on RestTemplate, circuit breaker with fallback, async notification via queue, config-based URLs, handle payment failure | Students add try-catch but still mark order as CONFIRMED in the catch block. Emphasize the state machine | Ask: "What should the order status be if payment fails?" (PAYMENT_FAILED, not CONFIRMED) |
| 4 | Fix LLM Security | Environment variable for API key, input regex validation, rate limiting decorator, structured prompt with guardrails, max_tokens=100, output validation | Students sanitize input but forget output validation. LLM can generate anything | Ask: "What if the LLM responds with customer data from its training set?" (Output filtering needed) |
| 5 | Service Boundaries | 6+ services: User, Menu/Restaurant, Order, Payment, Delivery, Notification. Critical path: Menu->Order->Payment->Delivery. Notification and analytics async | Students create too many tiny services (nano-services). Guide toward right-sizing | Ask: "Does Rating need its own service, or can it live in the Restaurant service?" |
| 6 | Error Response | Standard JSON: timestamp, status, error code, message, details array, traceId, path. GlobalExceptionHandler for all controllers | Students forget the traceId field which is critical for distributed debugging | Ask: "If a customer reports an error, how do you find it across 7 services?" (TraceId) |

---

## Key Discussion Points

1. When should you break a monolith into microservices? (Team size, scaling needs, organizational structure)
2. What is the difference between choreography and orchestration in Saga pattern?
3. Why "database per service"? What challenges does it create? (No joins across services)
4. When to use REST vs gRPC vs messaging? (REST: external APIs; gRPC: internal high-performance; messaging: async)
5. How does Conway's Law apply to microservices? (Architecture mirrors organization structure)
6. What is the OWASP Top 10 for LLM applications? (Prompt injection, data leakage, etc.)

---

## Recommended Microservice Boundaries for FoodExpress

| Service | Bounded Context | Owns | Communicates With |
|---------|----------------|------|-------------------|
| User Service | Identity & Access | users, addresses, sessions | Auth for all services |
| Menu Service | Restaurant & Menu | restaurants, menu_items, categories | Order Service (sync) |
| Order Service | Order Management | orders, order_items | Payment (sync), Delivery (sync), Notification (async) |
| Payment Service | Billing | payments, transactions, refunds | Order (callback) |
| Delivery Service | Logistics | deliveries, riders, routes | Order (status update), Notification (async) |
| Notification Service | Communication | notification_templates, notification_log | Consumed by: Order, Delivery, User |
| Rating Service | Feedback | ratings, reviews | Menu (aggregate score update, async) |
