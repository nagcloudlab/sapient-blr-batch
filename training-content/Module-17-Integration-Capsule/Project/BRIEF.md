# Integration Capsule Project -- Project Brief
## Module 17 | Day 18

---

## Sustain Context

You are a sustain engineering team at FoodExpress. Over the weekend, the production system received several critical bug reports from customers and the support team. Your VP of Engineering, Priya Sharma, has escalated these issues and expects all P1/P2 bugs resolved by end of day.

Your team has access to the full FoodExpress codebase spanning frontend (JavaScript), backend (Java Spring Boot + Node.js Express), and database (MySQL). Each bug requires investigation across multiple layers.

---

## Sprint Goal

Fix all cross-stack production bugs, write tests, document root cause analysis, and present findings to stakeholders.

---

## Task Table

| # | Task | Description | Layer(s) | Priority | Points |
|---|------|-------------|----------|----------|--------|
| 1 | Fix Price NaN Bug | Checkout page shows NaN for combo meal prices due to currency symbol in API response | Frontend + Backend | P1 | 8 |
| 2 | Fix Search Special Characters | Menu search fails with `&`, `'`, and other special characters; SQL injection vulnerability | Frontend + Backend + DB | P2 | 5 |
| 3 | Fix Order History | Only latest order displays; missing pagination, sorting, and index | Frontend + Backend + DB | P2 | 5 |
| 4 | Fix Rating 500 Error | Rating submission fails due to type mismatch across all layers | Frontend + Backend + DB | P3 | 8 |
| 5 | Write Unit Tests | Minimum 2 unit tests per bug fix | All | Required | 4 |
| 6 | Write RCA Documents | 5 Whys analysis for each bug | Documentation | Required | 3 |
| 7 | Update JIRA Board | Move tickets through workflow, add comments with RCA | Process | Required | 2 |
| 8 | Team Presentation | 15-minute presentation with demo, RCA, and learnings | Presentation | Required | 5 |

**Total Points Available:** 40

---

## Team Formation

- Teams of 3-4 members
- Assign roles: Frontend Lead, Backend Lead, Database Lead, QE/Integration
- All members participate in cross-stack debugging
- Rotate roles if team is smaller than 4

---

## Timeline

| Time | Activity |
|------|----------|
| 09:00 - 09:30 | Form teams, review bugs, plan sprint |
| 09:30 - 12:30 | Sprint 1: Fix P1 and P2 bugs |
| 12:30 - 13:30 | Lunch break |
| 13:30 - 15:30 | Sprint 2: Fix P3 bugs, write tests |
| 15:30 - 16:30 | Sprint 3: Documentation, presentation prep |
| 16:30 - 17:00 | Team presentations and retrospective |

---

## Constraints

- All fixes must include at least one test per layer affected
- No shortcuts: parameterized queries for all SQL, proper error handling for all APIs
- JIRA tickets must be updated with comments (simulated or actual)
- Code must follow existing project conventions
