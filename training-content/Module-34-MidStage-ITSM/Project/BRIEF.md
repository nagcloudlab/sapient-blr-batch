# Mid-Stage Project + ITSM Introduction -- Project Brief
## Module 34 | Days 39-40

---

## Sustain Context

FoodExpress has deployed its microservices platform but lacks comprehensive observability and structured incident management. As a sustain engineer, you must build a monitoring and alerting system, conduct chaos experiments to identify weaknesses, and establish ITSM processes for incident response.

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix Prometheus Alerts | Fix 8 bugs in alerting rules: division-by-zero guard, thresholds, severity, metric names, runbook URLs | 30 min | 12 |
| 2 | Fix Fault Injection Script | Fix 6 bugs: namespace, comparison logic, rollback command, observation time, API path, JSON parsing | 25 min | 10 |
| 3 | Fix Incident Template | Fix 6 bugs: priority, affected users, timeline order, resolution, escalation, prevention | 25 min | 10 |
| 4 | Fix ITSM Process Flow | Fix 5 bugs: categories, priority matrix, escalation timers, SLA targets, notification channels | 20 min | 8 |
| 5 | Design Grafana Dashboard | Design a FoodExpress operations dashboard layout with panels for golden signals | 30 min | 5 |
| 6 | Bonus: Write a Runbook | Create a complete runbook for order service 500 errors | 20 min | 5 |

**Total Points Available:** 50

---

## Deliverables

1. Fixed `prometheus-alerts.yaml` with all 8 bugs resolved
2. Fixed `fault-injection.sh` with all 6 bugs resolved
3. Fixed incident template with complete, accurate information
4. Fixed `itsm-process-flow.yaml` with correct process configuration
5. Dashboard design document (diagram or mockup)
6. (Bonus) Complete runbook for order service errors
