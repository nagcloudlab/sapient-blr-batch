# Lab 03: Error Budgets

## Objective

Calculate error budgets, simulate budget consumption through real incidents,
and make data-driven decisions about feature velocity vs reliability work.

---

## Concepts

### What is an Error Budget?

```
Error Budget = 1 - SLO

If SLO = 99.9%, then:
  Error Budget = 0.1%
  = 0.1% of 30 days
  = 0.1% of 43,200 minutes
  = 43.2 minutes of allowed downtime per month
```

### Why Error Budgets Matter

```
WITHOUT Error Budgets:                WITH Error Budgets:
─────────────────────                 ────────────────────
Dev: "Let's ship fast!"              Dev: "Budget is 80% full,
Ops: "No! It might break!"               let's ship with extra testing"
     -> Endless conflict                  -> Data-driven decision

Dev: "We need to deploy"             Dev: "Budget is healthy (30% used),
Ops: "Last deploy caused outage"          we have room for risk"
     -> Blame game                        -> Shared ownership
```

---

## Part 1: Calculate Error Budgets

### Exercise: Budget Math

Complete this table:

```
+------------------+--------+----------------+--------------+----------------+
| Service          | SLO    | Error Budget % | Budget (min)  | Budget (hours) |
|                  |        | (= 1 - SLO)   | (per 30 days) |                |
+------------------+--------+----------------+--------------+----------------+
| order-service    | 99.9%  | _____%         | _____ min     | _____ hrs      |
| payment-service  | 99.95% | _____%         | _____ min     | _____ hrs      |
| menu-service     | 99.5%  | _____%         | _____ min     | _____ hrs      |
| delivery-tracker | 99.9%  | _____%         | _____ min     | _____ hrs      |
+------------------+--------+----------------+--------------+----------------+

Formula: Budget in minutes = Error Budget % x 30 days x 24 hours x 60 minutes
```

<details>
<summary>Check your answers</summary>

| Service | SLO | Error Budget | Minutes/Month | Hours/Month |
|---------|-----|-------------|---------------|-------------|
| order-service | 99.9% | 0.1% | 43.2 min | 0.72 hrs |
| payment-service | 99.95% | 0.05% | 21.6 min | 0.36 hrs |
| menu-service | 99.5% | 0.5% | 216 min | 3.6 hrs |
| delivery-tracker | 99.9% | 0.1% | 43.2 min | 0.72 hrs |

</details>

---

## Part 2: Simulate Budget Consumption

### Scenario: September at FoodExpress

Three incidents happened this month:

```
Incident 1 (Sept 3):
  Service: order-service
  Duration: 12 minutes
  Cause: Bad deployment -- new code had a null pointer exception
  Impact: All orders returning 500 errors

Incident 2 (Sept 11):
  Service: payment-service
  Duration: 8 minutes
  Cause: Database connection pool exhausted during lunch rush
  Impact: Payments timing out

Incident 3 (Sept 18):
  Service: order-service
  Duration: 25 minutes
  Cause: Memory leak -- pod OOMKilled, took time to diagnose
  Impact: Intermittent 503 errors
```

### Exercise: Track Budget Burn

Fill in the budget tracker:

```
ORDER SERVICE (Budget: 43.2 min)
────────────────────────────────────────────────────────────
Date    | Incident           | Duration | Remaining | % Used
--------+--------------------+----------+-----------+-------
Sept 1  | Month starts       | --       | 43.2 min  | 0%
Sept 3  | Bad deployment     | 12 min   | _____ min | ____%
Sept 18 | Memory leak        | 25 min   | _____ min | ____%
────────────────────────────────────────────────────────────

PAYMENT SERVICE (Budget: 21.6 min)
────────────────────────────────────────────────────────────
Date    | Incident           | Duration | Remaining | % Used
--------+--------------------+----------+-----------+-------
Sept 1  | Month starts       | --       | 21.6 min  | 0%
Sept 11 | DB pool exhausted  | 8 min    | _____ min | ____%
────────────────────────────────────────────────────────────
```

<details>
<summary>Check your answers</summary>

**Order service:** 43.2 - 12 - 25 = 6.2 min remaining (85.6% consumed!)
**Payment service:** 21.6 - 8 = 13.6 min remaining (37% consumed)

</details>

---

## Part 3: Error Budget Policy

Based on budget consumption, what actions should the team take?

### Error Budget Policy Template

```
+---------------------------+--------------------------------------------+
| Budget Remaining          | Actions                                    |
+---------------------------+--------------------------------------------+
| > 50% remaining           | - Deploy normally                          |
|                           | - Run experiments                          |
|                           | - Standard code review                     |
+---------------------------+--------------------------------------------+
| 20% - 50% remaining      | - Deploy with extra caution                |
|                           | - Require additional testing               |
|                           | - Review recent incidents                  |
|                           | - No risky experiments                     |
+---------------------------+--------------------------------------------+
| < 20% remaining           | - Feature freeze                           |
|                           | - Only reliability improvements allowed    |
|                           | - Post-mortem all recent incidents          |
|                           | - Increase monitoring                      |
+---------------------------+--------------------------------------------+
| 0% (exhausted)            | - Complete deployment freeze               |
|                           | - All engineering on reliability            |
|                           | - Escalate to engineering leadership       |
|                           | - Daily review until budget replenishes     |
+---------------------------+--------------------------------------------+
```

### Exercise: Apply the Policy

Answer these questions based on the September scenario:

```
1. Order service has 6.2 min remaining (14.4% of budget).
   What policy level applies?        _________________________
   Can the team deploy new features?  _________________________
   What should they focus on?         _________________________

2. Payment service has 13.6 min remaining (63% of budget).
   What policy level applies?        _________________________
   Can the team deploy new features?  _________________________

3. It's Sept 22. A developer wants to deploy a big refactor to order-service.
   Should you allow it?              _________________________
   Why / why not?                    _________________________

4. The product manager says "we MUST ship this feature by month end."
   How do you respond using error budget data?
   _______________________________________________________________
```

---

## Part 4: Visualize Budget Burn Rate

### Burn Rate Concept

```
Budget: 43.2 min over 30 days

Ideal burn rate: 43.2 / 30 = 1.44 min/day

If you're burning faster than this, you'll exhaust the budget before month end.

   Budget
   Remaining
   (min)
   43.2 |*
        | *  <-- Ideal burn (1.44 min/day)
        |  *
        |   *
   21.6 |----*---------------------------------
        |     *
        |      *      * <-- Actual burn (incident spikes)
        |       *    *  *
        |        *  *    *
    0   |─────────*───────*──────────────────> Days
        1    5   10   15   20   25   30
```

### Discussion

- A single 30-minute outage on day 1 burns 69% of a 99.9% SLO budget
- This means the team must be extremely careful for the rest of the month
- **Burn rate alerts** notify you when you're consuming budget too fast

---

## Key Takeaways

1. **Error Budget = 1 - SLO** -- it's your "failure allowance"
2. Every incident **consumes** error budget -- track it like money
3. Error budgets **align dev and ops** -- both share the same budget
4. When budget is low: **slow down**. When budget is healthy: **ship faster**
5. Error budget policies remove politics from deploy decisions -- it's just math

> **Next:** Lab 04 -- Set up SLI-based monitoring so you can track budget burn in real-time
