# Module 08: Java Capsule Project -- API Bug Fixes and Feature Tickets

## Sustain Context

The client escalated:

> "We finished the Java backend review yesterday, and today we need hands on keyboards. The FoodExpress Order Service has three open Jira tickets blocking the release. FOOD-21 is a 500 error on the order detail endpoint, FOOD-22 needs a new filter endpoint the mobile team is waiting on, and FOOD-23 is a pagination gap that is killing the app when we have more than 50 orders. Full-day sprint -- reproduce, fix, test via Postman, and document everything."

---

## Tasks

| # | Ticket | Type | Issue | File(s) |
|---|--------|------|-------|---------|
| 1 | FOOD-21 | BUG | `GET /orders/{id}` returns 500 -- NullPointerException on missing restaurant reference | `OrderController.java`, `OrderService.java` |
| 2 | FOOD-22 | FEATURE | Add `GET /orders?status={status}` filter endpoint | `OrderController.java`, `OrderRepository.java` |
| 3 | FOOD-23 | BUG | `GET /orders` returns entire table -- no pagination | `OrderController.java`, `OrderService.java` |
| 4 | FOOD-24 | BUG | `POST /orders` accepts negative item quantities | `Order.java`, `OrderService.java` |

## Deliverables

- [ ] All 4 tickets resolved (2 bugs fixed, 1 feature added, 1 validation added)
- [ ] Each fix tested via Postman (export collection or screenshots)
- [ ] Brief root-cause notes for each bug (2-3 sentences)
- [ ] Code committed with meaningful commit messages
