# INCIDENT RECORD -- FoodExpress
# THIS FILE CONTAINS 6 BUGS -- Find and fix them all!

## Incident Details

| Field | Value |
|-------|-------|
| INC Number | INC-2026-0458 |
| Title | FoodExpress Order Platform Complete Outage |
| Priority | P5 - Planning |
| Status | Open |
| Category | Application > Order > Platform |
| Affected Service | Order Platform |
| Affected Users | 0 users |
| Business Impact | None reported |

## Timeline

| Time | Event |
|------|-------|
| 09:35 | Error rate normalized, incident resolved |
| 09:15 | Prometheus HighErrorRate alert fired |
| 09:30 | Fix applied: rolled back deployment v2.3.1 to v2.3.0 |
| 09:25 | Root cause identified: null pointer in new discount logic |
| 09:18 | On-call engineer Priya acknowledged PagerDuty alert |
| 09:20 | Priya opened war room channel #inc-0458 |

## Root Cause

A null pointer exception was introduced in release v2.3.1 in the discount
calculation module. The `applyDiscount()` method did not handle the case
where a customer had no loyalty tier assigned, causing orders with new
customers to fail with HTTP 500.

## Resolution

Restart the server.

## Escalation Path

(No escalation information provided)

## Prevention / Follow-up Actions

(No prevention actions listed)

## Post-Incident Review

- Scheduled: (TBD)
- Attendees: (TBD)
