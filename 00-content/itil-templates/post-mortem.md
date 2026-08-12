# Blameless Post-Mortem

**Incident ID:** INC-YYYY-NNN
**Post-Mortem Date:** YYYY-MM-DD
**Facilitator:** [Name]
**Attendees:** [Names]

---

## Executive Summary

Provide a 3-5 sentence plain-language summary suitable for a non-technical stakeholder. Describe what happened, how long it lasted, what the impact was, and what is being done to prevent recurrence.

Example: On [date], the FoodExpress Order Service became unavailable for approximately 47 minutes due to a MySQL connection pool exhaustion caused by a slow-query regression introduced in the previous deployment. Approximately 620 customer orders could not be placed during the outage. The service was restored by rolling back the deployment and restarting the Order Service. Three action items have been raised to prevent recurrence.

---

## Impact Summary

| Metric                  | Value                                                   |
|-------------------------|---------------------------------------------------------|
| Start Time              | YYYY-MM-DD HH:MM IST                                    |
| End Time                | YYYY-MM-DD HH:MM IST                                    |
| Total Duration          | X hours Y minutes                                       |
| Customers Affected      | [Estimated number]                                      |
| Orders Lost / Delayed   | [Estimated number and value]                            |
| Services Affected       | [e.g., Order Service (8080), Cart Service (3001)]       |
| SLO Impact              | [e.g., Monthly error budget reduced by 4.1%]            |
| Severity                | P1 / P2 / P3                                            |

---

## Detailed Timeline

List events in chronological order. Include what was observed, what actions were taken, and by whom.

| Time (IST)  | Event                                                                        | Who         |
|-------------|------------------------------------------------------------------------------|-------------|
| HH:MM       | Deployment of v2.4.1 to Order Service completed                              |             |
| HH:MM       | Grafana alert: Order Service error rate exceeded 5%                          |             |
| HH:MM       | On-call engineer paged; investigation started                                |             |
| HH:MM       | MySQL slow query log reviewed; N+1 query pattern identified                  |             |
| HH:MM       | Decision made to roll back to v2.4.0                                         |             |
| HH:MM       | Rollback completed; Order Service restarted on port 8080                     |             |
| HH:MM       | Error rate returned to baseline; incident declared resolved                  |             |
| HH:MM       | Post-mortem scheduled; all stakeholders notified                             |             |

---

## Root Cause

### Statement

[One clear sentence stating the root cause.]

Example: A code change in v2.4.1 introduced an ORM query inside a loop over order line items, causing N+1 database queries that saturated the MySQL connection pool under normal order volume.

### 5 Whys

| Why | Answer                                                                                       |
|-----|----------------------------------------------------------------------------------------------|
| 1   | Why did the Order Service fail? -- The MySQL connection pool was exhausted.                  |
| 2   | Why was the pool exhausted? -- Each order request was issuing N+1 queries instead of one.   |
| 3   | Why were N+1 queries issued? -- A loop was added that called the ORM for each line item.    |
| 4   | Why was this not caught before deployment? -- No load test or query review was in the CI pipeline. |
| 5   | Why was there no query review gate? -- The deployment checklist did not require it.          |

---

## Contributing Factors

Check all that applied to this incident.

- [ ] Insufficient testing before deployment
- [ ] Missing or incomplete monitoring / alerting
- [ ] Runbook did not exist or was outdated
- [ ] On-call process unclear or not followed
- [ ] Configuration or environment difference between staging and production
- [ ] External dependency failure (e.g., payment gateway, third-party API)
- [ ] Communication delay between team members
- [ ] Documentation gap (architecture, data flow, etc.)
- [ ] Insufficient access or tooling during response
- [ ] Other: [describe]

---

## What Went Well

- [e.g., Alert fired within 2 minutes of degradation beginning]
- [e.g., On-call engineer responded within SLA]
- [e.g., Rollback was pre-tested and executed in under 5 minutes]
- [e.g., Stakeholder communication was timely and clear]

---

## What Did Not Go Well

- [e.g., No query performance gate in the CI pipeline]
- [e.g., Staging environment does not replicate production order volume]
- [e.g., Runbook for Order Service restarts was missing]
- [e.g., Root cause took 25 minutes to identify due to lack of distributed tracing]

---

## What We Got Lucky With

- [e.g., Incident occurred at a low-traffic hour, limiting customer impact]
- [e.g., A team member happened to be online who had seen a similar issue before]
- [e.g., The previous deployment artifact was still available for immediate rollback]

---

## Action Items

| ID  | Action                                                           | Owner  | Due Date   | Status  |
|-----|------------------------------------------------------------------|--------|------------|---------|
| 1   | Add query count assertion to Order Service integration tests     |        | YYYY-MM-DD | Open    |
| 2   | Add MySQL connection pool saturation alert to Grafana            |        | YYYY-MM-DD | Open    |
| 3   | Create runbook for Order Service restart and rollback procedure  |        | YYYY-MM-DD | Open    |
| 4   | Add load test stage to CI pipeline (minimum 500 requests/min)   |        | YYYY-MM-DD | Open    |
| 5   | Review deployment checklist; add query review step              |        | YYYY-MM-DD | Open    |

---

## Recurrence Prevention

Describe the specific changes that will make this class of incident impossible or significantly less likely to recur. Link to the action items above.

- **Detection:** Action Item 2 (Grafana alert) will surface connection pool pressure before exhaustion occurs.
- **Prevention:** Action Items 1 and 4 (query assertion + load test in CI) will catch N+1 regressions before they reach production.
- **Response:** Action Item 3 (runbook) will reduce time-to-resolve for future Order Service incidents.
- **Process:** Action Item 5 (deployment checklist update) will close the process gap that allowed this change through.

---

*This post-mortem was conducted as a blameless exercise. The goal is to understand system and process failures, not to assign individual fault. All findings and action items are shared with the full team in the spirit of collective improvement.*
