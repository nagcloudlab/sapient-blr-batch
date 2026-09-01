# FoodExpress Error Budget Calculator
## SOLUTION

---

## Step 1: Monthly Error Budgets

| Service | SLO Target | Error Budget (%) | Minutes in 30 days | Error Budget (minutes) |
|---------|-----------|-------------------|--------------------|-----------------------|
| order-service | 99.9% | 0.1% | 43,200 | 43.2 min |
| payment-service | 99.95% | 0.05% | 43,200 | 21.6 min |
| menu-service | 99.5% | 0.5% | 43,200 | 216 min |
| delivery-tracking | 99% | 1% | 43,200 | 432 min |

---

## Step 2: Budget Consumption (September 2026)

### Incidents:

| Date | Service | Duration | Description |
|------|---------|----------|-------------|
| Sept 3 | order-service | 15 min | Deploy failure, rollback needed |
| Sept 8 | payment-service | 20 min | DB connection pool exhaustion |
| Sept 12 | menu-service | 45 min | Expired TLS certificate |

### Budget tracking:

| Service | Total Budget | Consumed | Remaining | % Remaining |
|---------|-------------|----------|-----------|-------------|
| order-service | 43.2 min | 15 min | 28.2 min | 65.3% |
| payment-service | 21.6 min | 20 min | 1.6 min | 7.4% |
| menu-service | 216 min | 45 min | 171 min | 79.2% |
| delivery-tracking | 432 min | 0 min | 432 min | 100% |

---

## Step 3: Budget Policy Decision

| Service | % Remaining | Policy Action |
|---------|-------------|---------------|
| order-service | 65.3% | Deploy freely; budget is healthy |
| payment-service | 7.4% | COMPLETE FREEZE: budget nearly exhausted; focus on reliability improvements; escalate to VP |
| menu-service | 79.2% | Deploy freely; budget is healthy |
| delivery-tracking | 100% | Deploy freely; full budget available |

---

## Step 4: Monthly Projection

| Service | Current rate | Projected remaining at month end | Risk Level |
|---------|-------------|----------------------------------|------------|
| order-service | ~1 incident / 2 weeks (15 min each) | 28.2 - 15 = 13.2 min (30.6%) | MEDIUM: approaching 20% threshold |
| payment-service | ~1 incident / 2 weeks (20 min each) | 1.6 - 20 = NEGATIVE | CRITICAL: budget will be exhausted |
| menu-service | ~1 incident / 2 weeks (45 min each) | 171 - 45 = 126 min (58.3%) | LOW: budget healthy |
| delivery-tracking | 0 incidents | 432 min (100%) | LOW: no consumption |

### Key Insight:
Payment-service is in critical condition. At current incident rate, it will exhaust its budget before month end. Immediate actions needed:
1. Freeze all non-critical deployments to payment-service
2. Investigate and fix root causes of DB connection pool issues
3. Consider if 99.95% SLO is appropriate, or should it be 99.9%?
