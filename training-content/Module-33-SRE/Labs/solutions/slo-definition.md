# FoodExpress SLO Definitions
## SOLUTION

---

## Order Service

| Field | Value |
|-------|-------|
| Service | order-service |
| SLI | Availability: HTTP responses with status < 500 / total HTTP requests |
| # FIX 1: Changed from 100% to 99.9% -- realistic target with usable error budget |
| SLO Target | 99.9% |
| # FIX 3: Changed from 1 day to 30-day rolling window |
| Measurement Window | 30-day rolling |
| Error Budget | 0.1% = 43.2 minutes/month (43,200 min x 0.001) |

---

## Payment Service

| Field | Value |
|-------|-------|
| Service | payment-service |
| # FIX 2: Changed SLI from server uptime to successful transactions (user-centric) |
| SLI | Transaction success: successful payment responses (2xx) / total payment requests |
| SLO Target | 99.95% |
| # FIX 3: Changed from 1 day to 30-day rolling window |
| Measurement Window | 30-day rolling |
| Error Budget | 0.05% = 21.6 minutes/month (43,200 min x 0.0005) |

---

## Menu Service

| Field | Value |
|-------|-------|
| Service | menu-service |
| SLI | Availability: HTTP responses with status < 500 / total HTTP requests |
| SLO Target | 99.5% |
| # FIX 3: Changed from 1 day to 30-day rolling window |
| Measurement Window | 30-day rolling |
| Error Budget | 0.5% = 216 minutes/month (43,200 min x 0.005) |

---

## Delivery Tracking Service

| Field | Value |
|-------|-------|
| Service | delivery-tracking |
| SLI | Freshness: location updates < 30s old / total location queries |
| SLO Target | 99% |
| # FIX 3: Changed from 1 day to 30-day rolling window |
| Measurement Window | 30-day rolling |
| Error Budget | 1% = 432 minutes/month (43,200 min x 0.01) |

---

## Error Budget Policy

| Budget Level | Action |
|-------------|--------|
| Budget > 50% remaining | Deploy freely; run experiments; take calculated risks |
| Budget 20-50% remaining | Deploy with extra testing; no risky experiments; review recent incidents |
| Budget < 20% remaining | Feature freeze; focus on reliability improvements only; post-mortem all recent incidents |
| Budget exhausted (0%) | Complete deployment freeze; all hands on reliability; escalate to VP Engineering |

---

## Justification for SLO Targets

| Service | Target | Rationale |
|---------|--------|-----------|
| order-service (99.9%) | Core revenue service; every failed order = lost revenue; but 100% is impossible and blocks all changes |
| payment-service (99.95%) | Higher target than orders because payment failures directly affect customer trust and revenue |
| menu-service (99.5%) | Lower target because menu browsing failures don't lose revenue immediately; customers can retry |
| delivery-tracking (99%) | Lowest target; tracking outages are annoying but don't prevent orders or payments |
