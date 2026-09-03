# Microservices & API -- Submission Checklist
## Module 22 | Days 24-25

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | REST Controller: API version prefix `/api/v1/` | [ ] |
| 2 | REST Controller: Service layer between controller and repository | [ ] |
| 3 | REST Controller: GET method for retrieval (no POST) | [ ] |
| 4 | REST Controller: Pagination on list endpoints | [ ] |
| 5 | REST Controller: 404 for missing resources | [ ] |
| 6 | REST Controller: @Valid on request body | [ ] |
| 7 | REST Controller: 201 Created with Location header on POST | [ ] |
| 8 | REST Controller: Existence check before delete | [ ] |
| 9 | API Gateway: TRACE method removed | [ ] |
| 10 | API Gateway: JWT auth on payment and order services | [ ] |
| 11 | API Gateway: Admin endpoints restricted by IP | [ ] |
| 12 | API Gateway: Rate limiting on all services | [ ] |
| 13 | Inter-Service: RestTemplate has timeouts | [ ] |
| 14 | Inter-Service: Circuit breaker with fallback | [ ] |
| 15 | Inter-Service: Notification sent asynchronously | [ ] |
| 16 | Inter-Service: Payment failure handled correctly | [ ] |
| 17 | LLM: API key from environment variable | [ ] |
| 18 | LLM: Input sanitized and validated | [ ] |
| 19 | LLM: Rate limiting applied | [ ] |
| 20 | LLM: Prompt has injection guardrails | [ ] |
| 21 | LLM: max_tokens limit set | [ ] |
| 22 | Service boundaries: 6+ services identified | [ ] |

---

## Self-Check Questions

1. **Why use `/api/v1/` versioning?** So you can introduce breaking changes in `/api/v2/` without affecting existing consumers.
2. **Why not use POST for retrieving data?** GET is idempotent and cacheable; POST is for creating resources. Using POST for reads violates REST semantics.
3. **What happens if you return `null` with 200 status?** Client thinks the request succeeded and tries to use null data, causing NPE.
4. **Why is the TRACE HTTP method dangerous?** It echoes the request back including cookies and auth headers, enabling cross-site tracing (XST) attacks.
5. **What is a circuit breaker?** A pattern that stops calling a failing service after a threshold, returning a fallback response instead of cascading the failure.
6. **Why send notifications asynchronously?** The customer shouldn't wait for an email to be sent before seeing their order confirmation.
7. **What is prompt injection?** When a user crafts input that overrides the system prompt, causing the LLM to execute unintended instructions.
8. **Why database per service?** Loose coupling; each service can evolve its schema independently without breaking others.
9. **What is the Saga pattern?** A sequence of local transactions where each step has a compensating transaction for rollback if a subsequent step fails.
10. **Why is a traceId essential in microservices?** It allows you to follow a single request across multiple services for debugging.
