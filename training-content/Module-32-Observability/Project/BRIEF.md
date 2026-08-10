# Observability -- Project Brief
## Module 32 | Day 36

---

## Sustain Context

FoodExpress has invested in an observability stack (Prometheus, Grafana, Alertmanager) but the initial configuration was done hastily. Prometheus is not scraping all services, dashboards show wrong data, and alert rules cause constant false alarms. As a sustain engineer, you must fix the observability stack to provide reliable monitoring.

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix Prometheus Config | Fix 3 bugs: wrong target, missing job, wrong metrics path | 20 min | 8 |
| 2 | Fix Grafana Dashboard | Fix 3 bugs: missing rate(), wrong math, avg vs p99 | 25 min | 10 |
| 3 | Fix Alert Rules | Fix 3 bugs: wrong threshold, missing `for`, too sensitive CPU | 20 min | 8 |
| 4 | Write PromQL Queries | Write 3 queries for golden signals | 15 min | 6 |
| 5 | Design Runbook | Create a runbook for HighErrorRate alert | 15 min | 5 |
| 6 | Bonus: Alertmanager Config | Configure alert routing for critical vs warning | 15 min | 5 |

**Total Points Available:** 42

---

## Deliverables

1. Fixed `prometheus.yml` with all 3 services scraped correctly
2. Fixed `grafana-dashboard.json` with accurate PromQL queries
3. Fixed `alerts.yml` with meaningful thresholds
4. Three PromQL queries for FoodExpress golden signals
5. Runbook document for HighErrorRate alert
6. (Bonus) Alertmanager configuration with routing rules
