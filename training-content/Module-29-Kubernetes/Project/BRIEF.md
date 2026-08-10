# Kubernetes -- Project Brief
## Module 29 | Day 32

---

## Sustain Context

FoodExpress has migrated to Kubernetes but the initial deployment was done hastily. Services are crashing, unreachable, and consuming unlimited resources. As a sustain engineer, you must fix the K8s manifests to achieve a stable, production-ready deployment.

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix Order Deployment | Fix 4 bugs: probe path, container port, resource limits, startup delay | 25 min | 10 |
| 2 | Fix Order Service | Fix 3 bugs: selector mismatch, targetPort, nodePort range | 20 min | 8 |
| 3 | Fix Payment Deployment | Fix 3 bugs: image tag/policy, missing readiness probe, hardcoded secret | 20 min | 8 |
| 4 | Fix Namespace Config | Fix 2 bugs: unrealistic quota, inverted limits/requests | 15 min | 6 |
| 5 | Design HPA Strategy | Write HPA manifest for order-service with scaling thresholds | 15 min | 5 |
| 6 | Bonus: Network Policy | Write a NetworkPolicy restricting traffic between services | 15 min | 5 |

**Total Points Available:** 42

---

## Deliverables

1. Fixed `order-deployment.yaml` with all 4 bugs resolved
2. Fixed `order-service.yaml` with correct selectors and ports
3. Fixed `payment-deployment.yaml` with proper image policy, readiness probe, and secret reference
4. Fixed `namespace-config.yaml` with realistic quotas and valid limit ranges
5. HPA manifest for order-service
6. (Bonus) NetworkPolicy manifest for service isolation
