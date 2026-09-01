# Microservices & API -- Project Brief
## Module 22 | Days 24-25

---

## Sustain Context

FoodExpress has migrated from a monolith to microservices, but the transition left several issues: poorly designed REST APIs, missing API Gateway security, fragile inter-service communication, and an insecure LLM integration. As a sustain engineer, you need to review and fix these issues to bring the platform up to production standards.

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix REST Controller | Fix 8 bugs: versioning, service layer, HTTP methods, pagination, status codes, validation | 40 min | 12 |
| 2 | Fix API Gateway | Fix 6 bugs: routing, TRACE method, auth, IP restriction, rate limiting | 30 min | 10 |
| 3 | Fix Inter-Service Communication | Fix 5 bugs: timeouts, circuit breaker, async notifications, service discovery, error handling | 30 min | 10 |
| 4 | Fix LLM Security | Fix 5 bugs: API key exposure, input sanitization, rate limiting, prompt injection, token limits | 25 min | 8 |
| 5 | Design Service Boundaries | Identify 6+ bounded contexts from the monolith with APIs and communication patterns | 25 min | 5 |
| 6 | Bonus: Error Response Standard | Design standard error response JSON schema for all services | 20 min | 5 |

**Total Points Available:** 50

---

## Deliverables

1. Fixed `MenuController.java` with all 8 bugs resolved
2. Fixed API Gateway YAML configuration
3. Fixed `OrderService.java` with resilient communication patterns
4. Fixed `menu_description_service.py` with LLM security controls
5. Microservice boundary design document with communication diagram
6. (Bonus) Standard error response schema with examples
