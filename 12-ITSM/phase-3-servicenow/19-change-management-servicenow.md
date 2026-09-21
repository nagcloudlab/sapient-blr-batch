# Section 19: Change Management in ServiceNow

## Purpose

How the Change Management concepts from Section 4 become **real workflows, forms, and approvals** in ServiceNow.

---

## Change Types in ServiceNow

| Type | Risk | Approval | Auto-created? | UPI Example |
|---|---|---|---|---|
| **Standard** | Low, pre-approved | No CAB needed | Template-based | Add new merchant to UPI |
| **Normal** | Medium to High | CAB approval required | Manual creation | Upgrade Txn Engine v4.1 -> v4.2 |
| **Emergency** | Critical, live incident | Fast-track (post-approval) | From incident | Hotfix for midnight transaction failures |

---

## Change Request Form

```
+------------------------------------------------------------------+
| CHG0004521                                          [State: New]  |
+------------------------------------------------------------------+
| Type: Normal                                                      |
|                                                                    |
| Requested by:   Ravi (Platform Engineering)                       |
| Assignment group: Platform Engineering                             |
| Assigned to:     Ravi                                             |
|                                                                    |
| Short description: Upgrade UPI Txn Engine v4.1 -> v4.2            |
|                                                                    |
| Description:                                                       |
|   Deploy new circuit breaker module, retry logic, and updated     |
|   Grafana dashboards. Rolling canary deployment.                   |
|                                                                    |
| Category:      Software                                           |
| Priority:      2 - High                                            |
|                                                                    |
| +--- Planning Tab ---+                                             |
| | Planned start: Oct 5, 2026 02:00 AM                             |
| | Planned end:   Oct 5, 2026 04:00 AM                             |
| | Justification: Reduce UPI Lite failure rate from 15% to <2%     |
| | Implementation plan: (attached document)                         |
| | Rollback plan: Revert to v4.1 container images                  |
| | Test plan: 1M synthetic transactions in staging                  |
| +--------------------+                                             |
|                                                                    |
| +--- Risk Tab ---+                                                 |
| | Risk: Medium                                                     |
| | Impact: High (all 400+ banks)                                   |
| | Risk score: Auto-calculated based on answers                     |
| +----------------+                                                 |
|                                                                    |
| +--- Schedule Tab ---+                                             |
| | Change window:   Maintenance window (Sun 2-4 AM)                |
| | Conflict check:  No other changes in this window                |
| | Blackout check:  Not in blackout period                         |
| +--------------------+                                             |
+------------------------------------------------------------------+
```

---

## Change Workflow: State Transitions

ServiceNow enforces a workflow -- you can't skip states:

```
New --> Assess --> Authorize --> Scheduled --> Implement --> Review --> Closed
 |                   |                           |
 |              (CAB rejects)              (failed)
 |                   |                           |
 v                   v                           v
Canceled         Assess again              Review --> Closed (failed)
```

### UPI Walkthrough: CHG0004521

| State | Who | What happens in ServiceNow |
|---|---|---|
| **New** | Ravi | Creates CHG, fills in all tabs |
| **Assess** | Change Manager | Reviews risk, impact, rollback plan. Risk auto-scored |
| **Authorize** | CAB | CAB workbench shows this CHG. Members vote: Approve/Reject |
| **Scheduled** | System | Appears on change calendar. Conflict detection runs |
| **Implement** | Ravi | Clicks "Implement" when deployment starts. Timer begins |
| **Review** | Change Manager | Post-Implementation Review: was it successful? |
| **Closed** | Change Manager | Close as Successful / Unsuccessful / Incomplete |

---

## Risk Assessment (Auto-calculated)

ServiceNow asks questions and auto-calculates risk score:

```
Risk Assessment Questionnaire:
+---------------------------------------------------+----------+
| Question                                          | Answer   |
+---------------------------------------------------+----------+
| Has this type of change been done before?         | Yes      |
| Is there a rollback plan?                         | Yes      |
| Will there be downtime?                           | No       |
| Does it affect production?                        | Yes      |
| How many users/services are affected?             | 400+     |
| Is it being done in a maintenance window?         | Yes      |
| Has it been tested in staging?                    | Yes      |
+---------------------------------------------------+----------+

Auto-calculated risk: MEDIUM (score: 14/35)
```

---

## CAB Workbench

The CAB has a dedicated view in ServiceNow:

```
+------------------------------------------------------------------+
| CAB Workbench                                    [Next CAB: Oct 2] |
+------------------------------------------------------------------+
|                                                                    |
| Changes Pending Approval:                                          |
| +------+------------------+----------+------+--------+----------+ |
| | #    | Description      | Type     | Risk | Impact | Requester| |
| +------+------------------+----------+------+--------+----------+ |
| | 4521 | Txn Engine v4.2  | Normal   | Med  | High   | Ravi     | |
| | 4522 | Kafka node add   | Normal   | Low  | Med    | Priya    | |
| | 4523 | DB patch 19.21   | Standard | Low  | Low    | DBA team | |
| | 4524 | Firewall rule add| Normal   | Med  | Med    | SecOps   | |
| +------+------------------+----------+------+--------+----------+ |
|                                                                    |
| For each change, CAB can:                                          |
|   [Approve]  [Reject]  [Request More Info]  [Defer]               |
|                                                                    |
| Note: CHG4523 is Standard -- pre-approved, shown for visibility   |
+------------------------------------------------------------------+
```

---

## Change Calendar

Visual calendar showing all scheduled changes -- prevents conflicts:

```
October 2026
+--------+--------+--------+--------+--------+--------+--------+
| Mon    | Tue    | Wed    | Thu    | Fri    | Sat    | Sun    |
+--------+--------+--------+--------+--------+--------+--------+
|        |        | 1      | 2      | 3      | 4      | 5      |
|        |        |        | CAB    |        |        | CHG4521|
|        |        |        | meeting|        |        | 2-4 AM |
+--------+--------+--------+--------+--------+--------+--------+
| 6      | 7      | 8      | 9      | 10     | 11     | 12     |
|        | CHG4522|        |        |BLACKOUT|BLACKOUT| CHG4524|
|        | Kafka  |        |        |Diwali  |Diwali  | 3-4 AM |
+--------+--------+--------+--------+--------+--------+--------+

BLACKOUT = No changes allowed (Diwali weekend)
CONFLICT = ServiceNow auto-detects if two changes touch same CI
```

---

## Standard Change: Template & Auto-Approval

```
Standard Change Template: "Add New UPI Merchant"
+--------------------------------------------------+
| Pre-filled fields:                                |
|   Type: Standard                                  |
|   Category: Configuration                         |
|   Risk: Low                                       |
|   Assignment group: Merchant Onboarding           |
|   Implementation plan: (pre-written steps)        |
|   Rollback plan: Remove merchant config entry     |
|   Approval: Auto-approved                          |
|                                                    |
| User fills in:                                     |
|   Merchant name: [_______________]                |
|   Merchant ID:   [_______________]                |
|   VPA handle:    [_______________]                |
+--------------------------------------------------+

Workflow: New --> Scheduled --> Implement --> Closed
(No Assess or Authorize -- pre-approved)
```

---

## Emergency Change: Fast-Track Workflow

```
Situation: Settlement calculation bug found at midnight.
           Wrong amounts being sent to banks.

Emergency Change workflow:
  1. Create CHG with type: Emergency
  2. Skip CAB -- get verbal approval from Change Manager (phone/Slack)
  3. Implement the fix immediately
  4. Post-approval: CAB reviews in next meeting (retroactive)
  5. Full documentation added after the fact

ServiceNow tracks:
  - Who approved verbally (captured in work notes)
  - What was changed
  - Post-implementation review: mandatory within 48 hours
```

---

## Change Management Reports

```
Monthly Change Report -- September 2026
+--------------------------------+---------+
| Metric                         | Value   |
+--------------------------------+---------+
| Total changes                  | 142     |
| Standard                       | 89 (63%)|
| Normal                         | 48 (34%)|
| Emergency                      | 5 (3%)  |
| Successful                     | 136(96%)|
| Failed                         | 4 (3%)  |
| Unauthorized (no approval)     | 2 (1%)  |
| Changes causing incidents      | 3       |
| Avg lead time (Normal)         | 4.2 days|
| CAB approval rate              | 92%     |
+--------------------------------+---------+

Trend: Emergency changes down from 8% to 3% (improvement!)
Action: Investigate 2 unauthorized changes
```

---

## Connection to Previous Sections

```
Change form links to:
  |-- cmdb_ci --> Which CIs are affected? (Sec 7)
  |-- incident --> Did this change cause any incidents? (Sec 2)
  |-- problem --> Is this change fixing a known problem? (Sec 3)
  |-- sla --> Was the change completed within SLA? (Sec 8)
  |-- kb_knowledge --> Runbook for implementation (Sec 9)
```

---

## Key Takeaway

> ServiceNow Change Management is Section 4 brought to life:
>
> - **Normal** = CAB reviews in the workbench, risk auto-scored
> - **Standard** = templates, auto-approved, fast
> - **Emergency** = fast-track now, document later
>
> The change calendar prevents conflicts. The audit trail proves compliance. The reports show trends. All automatic.
