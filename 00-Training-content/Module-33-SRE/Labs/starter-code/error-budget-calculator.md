# FoodExpress Error Budget Calculator
## STARTER CODE -- Complete the calculations

---

## Step 1: Calculate Monthly Error Budgets

| Service | SLO Target | Error Budget (%) | Minutes in 30 days | Error Budget (minutes) |
|---------|-----------|-------------------|--------------------|-----------------------|
| order-service | 99.9% | TODO | 43,200 | TODO |
| payment-service | 99.95% | TODO | 43,200 | TODO |
| menu-service | 99.5% | TODO | 43,200 | TODO |
| delivery-tracking | 99% | TODO | 43,200 | TODO |

---

## Step 2: Track Budget Consumption (September 2026)

### Incidents this month:

| Date | Service | Duration | Description |
|------|---------|----------|-------------|
| Sept 3 | order-service | 15 min | Deploy failure, rollback needed |
| Sept 8 | payment-service | 20 min | DB connection pool exhaustion |
| Sept 12 | menu-service | 45 min | Expired TLS certificate |

### Budget tracking:

| Service | Total Budget | Consumed | Remaining | % Remaining |
|---------|-------------|----------|-----------|-------------|
| order-service | TODO | 15 min | TODO | TODO |
| payment-service | TODO | 20 min | TODO | TODO |
| menu-service | TODO | 45 min | TODO | TODO |
| delivery-tracking | TODO | 0 min | TODO | TODO |

---

## Step 3: Budget Policy Decision

Based on remaining budget, what action should each service take?

| Service | % Remaining | Policy Action |
|---------|-------------|---------------|
| order-service | TODO | TODO: Deploy freely / Extra testing / Feature freeze / Complete freeze |
| payment-service | TODO | TODO |
| menu-service | TODO | TODO |
| delivery-tracking | TODO | TODO |

---

## Step 4: Monthly Projection

If current incident rate continues, will any service exhaust its budget by month end?

| Service | Current rate (incidents/week) | Projected remaining at month end | Risk Level |
|---------|-----------------------------|---------------------------------|------------|
| order-service | TODO | TODO | TODO |
| payment-service | TODO | TODO | TODO |
| menu-service | TODO | TODO | TODO |
| delivery-tracking | TODO | TODO | TODO |
