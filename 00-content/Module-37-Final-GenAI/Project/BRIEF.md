# Final Project + Generative AI -- Project Brief
## Module 37 | Days 45-47

---

## Sustain Context

This is the capstone project for the Sustain Engineering training programme. FoodExpress has experienced a major payment service outage that escalated over three days. As a sustain engineering team, you must handle the full ITSM lifecycle -- from incident response through problem analysis, change management, and post-incident review. On Day 47, you will also demonstrate responsible use of Generative AI tools in a sustain engineering context.

---

## Scenario

### The Payment Outage (3-Day Timeline)

**Day 1 (Monday):** Intermittent payment failures noticed. INC-2026-0470 created at P3. Workaround: retry button. Failure rate ~2%.

**Day 2 (Tuesday):** Failures increase to 8%. Reprioritized to P2. Pattern: correlates with high order volume. Temporary fix: scale from 3 to 8 replicas.

**Day 3 (Wednesday):** Complete payment service outage at 07:30. All pods crash-looping. Major Incident declared (P1). Root cause found at 08:00: memory leak in payment retry logic (v3.1.0) -- each failed retry allocates a new HTTP client without closing. Rollback to v3.0.2 at 08:15. Service restored at 08:30.

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Major Incident Record | Complete INC-2026-0475: timeline (all 3 days), priority, impact, communication plan, resolution, linked records | 60 min | 15 |
| 2 | Problem Record | PRB-2026-0030: 5 Whys analysis, known error workaround, permanent fix plan, trend data | 45 min | 12 |
| 3 | Change Request | CHG-2026-0095: Fix memory leak in payment retry logic. Risk assessment, rollback, implementation plan, CAB approval | 45 min | 12 |
| 4 | SLA Definition | Payment Processing service SLA with availability targets, response times, penalties, reporting | 30 min | 8 |
| 5 | Service Catalog Entry | Payment Processing service entry with dependencies, support model, contacts | 30 min | 8 |
| 6 | Post-Incident Review | Blameless PIR: timeline reconstruction, contributing factors, action items with owners and deadlines | 45 min | 10 |
| 7 | Dashboard Design | Payment service monitoring dashboard with golden signals panels | 20 min | 5 |
| 8 | AI Labs | Fix AI prompt templates (6 bugs), evaluation harness (6 bugs), trust guidelines (5 bugs) | 60 min | -- |
| 9 | Presentation | 15-minute team demo covering all deliverables with Q&A | 15 min | 10 |

**Total Points (ITSM Project):** 80

---

## Deliverables

### Days 45-46 (ITSM Final Project)

1. Major Incident Record (INC-2026-0475)
2. Problem Record (PRB-2026-0030)
3. Change Request (CHG-2026-0095)
4. SLA Definition for Payment Processing
5. Service Catalog Entry for Payment Processing
6. Post-Incident Review document
7. Dashboard design (diagram or mockup)
8. Team presentation (15 minutes + 5 minutes Q&A)

### Day 47 (GenAI Labs)

9. Fixed `ai-prompts.yaml` with all 6 bugs resolved
10. Fixed `ai-eval.py` with all 6 bugs resolved
11. Fixed `ai-trust-guidelines.yaml` with all 5 bugs resolved
