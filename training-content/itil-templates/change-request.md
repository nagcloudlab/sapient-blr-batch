# Change Request

**CR ID:** CR-YYYY-NNN
**Type:** Standard / Normal / Emergency
**Status:** Draft / Submitted / Approved / Implemented / Closed / Rejected

---

## Change Details

| Field                | Value                                                      |
|----------------------|------------------------------------------------------------|
| Title                | [Short description of the change]                          |
| Requested By         | [Name]                                                     |
| Requested Date       | YYYY-MM-DD                                                 |
| Planned Start        | YYYY-MM-DD HH:MM IST                                       |
| Planned End          | YYYY-MM-DD HH:MM IST                                       |
| Maintenance Window   | [e.g., Saturday 02:00 -- 04:00 IST]                        |
| Affected Service(s)  | [e.g., Order Service (Java, port 8080)]                    |
| Environment          | Production                                                 |
| Change Lead          | [Name]                                                     |

---

## Description

Provide a clear description of what is changing and why.

Example: Deploying a database index on the `orders` table (`customer_id`, `created_at`) in the MySQL instance used by the Order Service to reduce query response times under peak load.

---

## Business Justification

Explain the business reason for this change. Link to the originating incident or Jira ticket where applicable.

- **Problem being solved:** [e.g., Order history page takes 8-12 seconds to load during dinner peak]
- **Business impact if not done:** [e.g., Customer complaints increasing; risk of SLO breach]
- **Originating ticket:** [JIRA-NNN or INC-NNN]

---

## Technical Plan

Step-by-step implementation plan. Be specific enough that another engineer can execute it.

1. [Step 1 -- e.g., Take a MySQL dump backup of the `orders` table]
2. [Step 2 -- e.g., Apply index migration script via Flyway]
3. [Step 3 -- e.g., Verify index creation with EXPLAIN on affected queries]
4. [Step 4 -- e.g., Monitor Order Service (port 8080) response times for 15 minutes]
5. [Step 5 -- e.g., Confirm no increase in error rate on /api/orders endpoints]

---

## Rollback Plan

Describe exactly how to undo this change if problems arise. Estimate rollback time.

- **Rollback trigger:** [e.g., P99 latency exceeds 5s or error rate exceeds 1% after change]
- **Rollback steps:**
  1. [Step 1 -- e.g., DROP INDEX on `orders` table]
  2. [Step 2 -- e.g., Restart Order Service]
  3. [Step 3 -- e.g., Confirm service healthy on port 8080]
- **Estimated rollback time:** [e.g., 10 minutes]
- **Rollback owner:** [Name]

---

## Testing Done

- [ ] Change tested in the Development environment
- [ ] Change tested in the Staging environment
- [ ] Rollback procedure tested in a non-production environment
- [ ] Affected API endpoints tested (e.g., GET /api/orders, GET /api/orders/:id)
- [ ] Load test or query EXPLAIN run to confirm improvement
- [ ] Monitoring dashboards reviewed pre- and post-test
- [ ] Relevant team members notified

---

## Risk Assessment

| Risk                                      | Likelihood | Impact | Mitigation                                      |
|-------------------------------------------|------------|--------|-------------------------------------------------|
| Index build locks table during migration  | Low        | High   | Run during maintenance window; use ALGORITHM=INPLACE |
| Rollback script fails                     | Low        | Medium | Pre-tested in staging; DBA on standby           |
| Unintended effect on other services       | Low        | Low    | Only Order Service reads this table             |
| Change window overruns                    | Medium     | Low    | Hard stop at window end; rollback if incomplete |

**Overall Risk Rating:** Low / Medium / High

---

## Approvals

| Role               | Name   | Decision          | Date       |
|--------------------|--------|-------------------|------------|
| Change Requester   |        | Submitted         | YYYY-MM-DD |
| Technical Reviewer |        | Approved/Rejected | YYYY-MM-DD |
| CAB / Team Lead    |        | Approved/Rejected | YYYY-MM-DD |

---

## Post-Implementation Review

To be completed within 24 hours of the change window closing.

| Field                        | Value                                                      |
|------------------------------|------------------------------------------------------------|
| Actual Start                 | YYYY-MM-DD HH:MM IST                                       |
| Actual End                   | YYYY-MM-DD HH:MM IST                                       |
| Outcome                      | Successful / Rolled Back / Partially Successful            |
| Deviations from Plan         | [Describe any steps that differed from the technical plan] |
| Monitoring Result            | [e.g., P99 latency dropped from 9s to 0.4s post-change]   |
| Follow-up Actions Required   | [Link to Jira tickets created, or "None"]                  |

---

*This change request follows the FoodExpress ITIL Change Management process. All Normal and Emergency changes require CAB approval before implementation.*
