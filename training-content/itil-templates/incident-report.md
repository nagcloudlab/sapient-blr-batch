# Incident Report

**Incident ID:** INC-YYYY-NNN
**Priority:** P1 / P2 / P3 / P4
**Status:** Open / Investigating / Resolved / Closed

---

## Summary

| Field              | Value                                      |
|--------------------|--------------------------------------------|
| Title              | [Short description of the incident]        |
| Reported By        | [Name / alerting system]                   |
| Reported At        | YYYY-MM-DD HH:MM IST                       |
| Resolved At        | YYYY-MM-DD HH:MM IST                       |
| Total Duration     | X hours Y minutes                          |
| Affected Service   | [e.g., Order Service / Cart Service]       |
| Environment        | Production                                 |
| Incident Commander | [Name]                                     |

---

## Timeline

| Time (IST)  | Event                                                                 | Who         |
|-------------|-----------------------------------------------------------------------|-------------|
| HH:MM       | Alert fired / issue first noticed                                     |             |
| HH:MM       | Incident declared, commander assigned                                 |             |
| HH:MM       | Investigation started                                                 |             |
| HH:MM       | Root cause identified                                                 |             |
| HH:MM       | Fix applied / service restored                                        |             |
| HH:MM       | Incident closed, monitoring confirmed stable                          |             |

Add rows as needed. Use exact timestamps wherever possible.

---

## Impact

| Metric               | Value                                                      |
|----------------------|------------------------------------------------------------|
| Affected Users       | [Estimated number of customers impacted]                   |
| Outage Duration      | [Time from first impact to service restoration]            |
| Estimated Revenue    | [Approximate order value lost during outage]               |
| SLO Error Budget     | [% consumed by this incident, e.g., "3.2% of monthly"]    |
| Services Affected    | [e.g., Restaurant Service (3000), Order Service (8080)]    |
| Downstream Impact    | [e.g., Payment Service (3003) rejected new transactions]   |

---

## Root Cause

Provide a clear, factual description of the underlying cause. Avoid assigning blame.

Example: The Order Service (Java, port 8080) exhausted its MySQL connection pool after a schema migration added a missing index, causing full table scans and connection timeouts under normal load.

---

## Resolution

Describe the steps taken to resolve the incident. Include any commands run, config changes made, or rollbacks performed.

1. [Step taken]
2. [Step taken]
3. [Step taken]

---

## Action Items

| ID  | Action                                      | Owner  | Due Date   | Status  |
|-----|---------------------------------------------|--------|------------|---------|
| 1   | [Preventive or corrective action]           |        | YYYY-MM-DD | Open    |
| 2   | [Add monitoring alert for this condition]   |        | YYYY-MM-DD | Open    |
| 3   | [Update runbook with resolution steps]      |        | YYYY-MM-DD | Open    |

---

## Lessons Learned

**What worked well:**

- [e.g., Alert fired within 2 minutes of degradation]
- [e.g., Rollback procedure was documented and executed quickly]

**What did not work well:**

- [e.g., No runbook existed for this failure mode]
- [e.g., On-call rotation was unclear]

**What would we do differently:**

- [e.g., Add a connection pool saturation alert to Grafana dashboard]
- [e.g., Include DB connection limits in the deployment checklist]

---

*This report follows the FoodExpress ITIL Incident Management process. All incidents P1-P2 must be reviewed in the next team retrospective.*
