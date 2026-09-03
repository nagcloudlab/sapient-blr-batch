# FoodExpress SLO Definitions
## STARTER CODE -- Contains bugs to fix

---

## Order Service

| Field | Value |
|-------|-------|
| Service | order-service |
| SLI | Availability: successful HTTP responses / total requests |
| # BUG 1: SLO target of 100% is impossible -- no deployments allowed, zero error budget |
| SLO Target | 100% |
| # BUG 3: Measurement window of 1 day is too short |
| Measurement Window | 1 day |
| Error Budget | TODO: Calculate |

---

## Payment Service

| Field | Value |
|-------|-------|
| Service | payment-service |
| # BUG 2: SLI measures server uptime, not user-facing transaction success |
| SLI | Uptime: time server process is running / total time |
| SLO Target | 99.9% |
| # BUG 3: Measurement window of 1 day is too short |
| Measurement Window | 1 day |
| Error Budget | TODO: Calculate |

---

## Menu Service

| Field | Value |
|-------|-------|
| Service | menu-service |
| SLI | Availability: successful HTTP responses / total requests |
| SLO Target | 99.5% |
| # BUG 3: Measurement window of 1 day is too short |
| Measurement Window | 1 day |
| Error Budget | TODO: Calculate |

---

## Delivery Tracking Service

| Field | Value |
|-------|-------|
| Service | delivery-tracking |
| SLI | Freshness: location updates < 30s old / total queries |
| SLO Target | 99% |
| Measurement Window | 1 day |
| Error Budget | TODO: Calculate |

---

## Error Budget Policy

TODO: Define what happens at each budget level:
- Budget > 50%: ???
- Budget 20-50%: ???
- Budget < 20%: ???
- Budget exhausted: ???
