# SRE Automation -- Lab Exercises
## Module 33 | Days 37-38

---

## Client Email

```
From: meera.krishnan@foodexpress.in
To: sustain-engineering@team.com
Subject: SRE Foundation Setup for FoodExpress
Date: 2026-09-10

Team,

We are formalizing our SRE practices for FoodExpress. We need
your help with:

1. Defining SLIs and SLOs for our core services
2. Setting up error budget tracking
3. Assessing our toil and creating an automation roadmap
4. Writing a post-mortem for last week's delivery outage
5. Building an incident response playbook

Please complete the templates and exercises in the starter code.

-- Meera Krishnan, VP Engineering, FoodExpress
```

---

## Lab 1: Define SLOs for FoodExpress (Day 37)

### File: `starter-code/slo-definition.md`

The SLO definition template has bugs and gaps:

| # | Issue | Impact |
|---|-------|--------|
| 1 | The order-service SLO is set to 100% availability | Impossible target; error budget = 0; no deployments allowed |
| 2 | The payment-service SLI measures "server uptime" instead of "successful transactions" | Measures infrastructure, not user experience; server can be up but returning errors |
| 3 | The measurement window is "1 day" for all SLOs | Too short; a single bad hour could exhaust the budget; 30-day rolling is standard |
| 4 | Error budget calculations are missing | Cannot track budget consumption without calculations |

### Tasks
1. Fix the SLO targets to realistic values
2. Fix the SLI definitions to be user-centric
3. Change measurement windows to 30-day rolling
4. Calculate error budgets for each service

---

## Lab 2: Error Budget Calculator (Day 37)

### File: `starter-code/error-budget-calculator.md`

Complete the error budget tracking worksheet:

| # | Task | Description |
|---|------|-------------|
| 1 | Calculate monthly error budget in minutes | For each SLO (99.9%, 99.95%, 99.5%) |
| 2 | Track budget consumption | Given 3 incidents, calculate remaining budget |
| 3 | Determine budget policy action | Based on remaining budget, what actions to take |
| 4 | Project budget for the month | Will the budget last? What adjustments needed? |

### Given incidents:
- Sept 3: Order service down 15 min (deploy failure)
- Sept 8: Payment service degraded 20 min (DB connection pool)
- Sept 12: Menu service down 45 min (expired certificate)

---

## Lab 3: Toil Assessment (Day 38)

### File: `starter-code/toil-assessment.md`

The toil assessment template has issues:

| # | Issue | Impact |
|---|-------|--------|
| 1 | "Monitoring dashboards" is listed as toil | Monitoring is engineering work, not toil; toil must be repetitive and automatable |
| 2 | Tasks are not prioritized by automation potential | Without prioritization, team may automate low-value tasks first |
| 3 | Automation effort estimates are missing | Cannot build a roadmap without understanding cost of automation |

### Tasks
1. Identify which items are actually toil (vs engineering work)
2. Prioritize by frequency x impact
3. Estimate automation effort for each task
4. Create a 3-month automation roadmap

---

## Lab 4: Write a Blameless Post-Mortem (Day 38)

### File: `starter-code/postmortem-template.md`

Write a post-mortem for the following incident:

**Incident:** FoodExpress delivery tracking outage
**Date:** September 5, 2026, 20:15 - 20:52 IST
**Duration:** 37 minutes
**Severity:** SEV-2

**Facts:**
- Delivery tracking service became unreachable at 20:15
- Root cause: TLS certificate expired on delivery-service
- 12,000 customers could not see delivery status
- On-call engineer received alert at 20:18, acknowledged at 20:30 (at dinner)
- Certificate was manually renewed at 20:48
- Service verified healthy at 20:52
- Certificate expiry was known (warning email sent 14 days prior, not actioned)

### The template has intentional gaps:

| # | Issue | Impact |
|---|-------|--------|
| 1 | Timeline section is empty | Cannot learn from sequence of events |
| 2 | "What Went Wrong" section blames the engineer by name | Violates blameless principle; creates fear culture |
| 3 | Action items have no owners or deadlines | Items never get completed without accountability |

---

## Lab 5: Observability + SRE MCQ (Day 38)

### 30-question assessment covering Modules 32-33

Complete the MCQ assessment. Topics:
- Three pillars of observability (5 questions)
- Prometheus & PromQL (5 questions)
- Grafana & Alerting (4 questions)
- SLIs & SLOs (5 questions)
- Error Budgets (4 questions)
- Toil & Automation (3 questions)
- Incident Response & Post-Mortems (4 questions)

Time limit: 30 minutes

---

## Summary

| Lab | Files | Focus Area | Day |
|-----|-------|------------|-----|
| 1 | slo-definition.md | SLI/SLO design, realistic targets | 37 |
| 2 | error-budget-calculator.md | Budget math, policy decisions | 37 |
| 3 | toil-assessment.md | Identify toil, prioritize automation | 38 |
| 4 | postmortem-template.md | Blameless post-mortem writing | 38 |
| 5 | MCQ Assessment | Observability + SRE knowledge check | 38 |
