# INCIDENT RECORD -- FoodExpress -- FIXED VERSION

## Incident Details

| Field | Value |
|-------|-------|
| INC Number | INC-2026-0458 |
| Title | FoodExpress Order Platform Complete Outage |
| Priority | P1 - Critical |
| Status | Resolved |
| Category | Application > Order > Platform |
| Affected Service | Order Platform |
| Affected Users | ~5,000 customers (all orders failing during outage window) |
| Business Impact | Complete order failure for 20 minutes, est. revenue loss Rs 2L |

## Timeline

| Time | Event |
|------|-------|
| 09:15 | Prometheus HighErrorRate alert fired |
| 09:18 | On-call engineer Priya acknowledged PagerDuty alert |
| 09:20 | Priya opened war room channel #inc-0458 |
| 09:25 | Root cause identified: null pointer in new discount logic (v2.3.1) |
| 09:30 | Fix applied: rolled back deployment v2.3.1 to v2.3.0 |
| 09:35 | Error rate normalized, incident resolved |

## Root Cause

A null pointer exception was introduced in release v2.3.1 in the discount
calculation module. The `applyDiscount()` method did not handle the case
where a customer had no loyalty tier assigned, causing orders with new
customers to fail with HTTP 500.

## Resolution

Rolled back deployment from v2.3.1 to v2.3.0 using:
`kubectl rollout undo deploy/order-service -n foodexpress`

This matches the root cause because the bug was introduced in v2.3.1,
and rolling back removes the faulty discount logic.

## Escalation Path

| Timeframe | Action | Contact |
|-----------|--------|---------|
| 0-15 min | On-call engineer investigates | Priya (PagerDuty) |
| 15-30 min | Escalate to Engineering Lead | Ravi Kumar (phone: +91-XXXXX) |
| 30-60 min | Escalate to VP Engineering | Amit Shah (phone: +91-XXXXX) |
| 60+ min | Executive notification | CTO Meera Patel |

## Prevention / Follow-up Actions

| # | Action | Owner | Deadline |
|---|--------|-------|----------|
| 1 | Add null-safety check in `applyDiscount()` for loyalty tier | Dev Team | 2026-09-07 |
| 2 | Add unit test for new customer (no loyalty tier) path | QE Team | 2026-09-07 |
| 3 | Add integration test for discount calculation in CI/CD pipeline | DevOps | 2026-09-10 |
| 4 | Review all nullable fields in customer model | Dev Team | 2026-09-12 |
| 5 | Implement canary deployment for order-service | DevOps | 2026-09-15 |

## Post-Incident Review

- Scheduled: 2026-09-07, 10:00 AM
- Attendees: Priya, Ravi, QE Lead, DevOps Lead
- Format: Blameless retrospective
- Focus: Why did the null pointer escape code review and testing?
