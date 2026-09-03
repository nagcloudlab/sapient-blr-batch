# ITIL Practices -- Lab Exercises
## Module 35 | Days 41-42

---

## Client Email

```
From: meera.patel@foodexpress.in
To: sustain-engineering@team.com
Subject: ITIL Process Documentation Needs Fixing
Date: 2026-09-08

Team,

Our ITIL process documentation has several errors that are
causing operational confusion:

1. The incident management template has wrong priority
   assignments and missing fields
2. The change request form has incorrect risk assessments
   and missing rollback plans
3. The problem record is poorly structured with wrong root
   cause analysis
4. The SLA definitions have unrealistic targets and missing
   penalty clauses

Please review and fix these templates so our ITSM processes
are accurate and actionable.

-- Meera Patel, CTO, FoodExpress
```

---

## Lab 1: Fix the Incident Management Template (7 bugs)

**File:** `starter-code/incident-record.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the priority assignment | Impact=High, Urgency=High but Priority is P4 | Critical incident not treated urgently |
| 2 | Look at the category path | "Infrastructure > Application > Order" is backwards | Misrouted to infrastructure team |
| 3 | Check the SLA response target | P1 response time is "24 hours" | Customers wait a full day for critical issue |
| 4 | Look at the assignment group | Assigned to "Marketing Team" | Wrong team entirely |
| 5 | Check the status transitions | Status goes from "New" directly to "Closed" | Skips investigation and resolution |
| 6 | Look at the related CI | Related CI says "email-server" for an order service incident | Wrong configuration item linked |
| 7 | Check the communication plan | No stakeholder notifications defined | Business unaware of major outage |

### Verification

Walk through the incident lifecycle: is priority correct? Is it assigned to the right team? Does the status flow make sense?

---

## Lab 2: Fix the Change Request Template (6 bugs)

**File:** `starter-code/change-request.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the change type | A database schema migration is marked as "Standard" | High-risk change bypasses CAB approval |
| 2 | Look at the risk assessment | Risk is "None" for a production database change | No risk mitigation planned |
| 3 | Check the implementation plan | Plan says "Run migration script" with no test step | Change deployed without validation |
| 4 | Look at the rollback plan | Rollback plan says "N/A -- not needed" | No way to recover if migration fails |
| 5 | Check the implementation window | Scheduled during peak hours (12:00-13:00 weekday) | Maximum user impact if something goes wrong |
| 6 | Look at the CAB approval | CAB approval field says "Not Required" | Violates change control for Normal changes |

### Verification

Apply the 7 Rs to the fixed change request. Every question should have a clear answer.

---

## Lab 3: Fix the Problem Record (6 bugs)

**File:** `starter-code/problem-record.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the problem status | Status is "Closed" but no root cause documented | Problem closed without being solved |
| 2 | Look at the related incidents | Lists 0 related incidents | Problem exists without any triggering incidents |
| 3 | Check the 5 Whys analysis | Only has 2 Whys, and the second is "Because it broke" | Root cause not properly identified |
| 4 | Look at the known error record | Known error workaround is "Ignore the issue" | No actionable workaround for operations team |
| 5 | Check the permanent fix | Permanent fix field is empty | No plan to actually resolve the problem |
| 6 | Look at the trend data | Trend says "First occurrence" but there are 5 related incidents | Trend data contradicts incident count |

### Verification

Does the problem record tell a complete story? Can someone pick it up and understand what happened, why, and what to do?

---

## Lab 4: Fix the SLA Definition (6 bugs)

**File:** `starter-code/sla-definition.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the availability target | Target is 50% for a critical service | Effectively no SLA (down half the time) |
| 2 | Look at the P1 resolution time | P1 resolution is 30 days | A month to fix a critical outage |
| 3 | Check the measurement period | "Yearly" measurement hides monthly bad performance | One bad month averaged out by 11 good months |
| 4 | Look at the penalty clause | Penalty for breach is "Written apology" | No financial consequence for SLA violation |
| 5 | Check the exclusions list | "All weekends and holidays" excluded from a 24x7 service | Outages on weekends don't count toward SLA |
| 6 | Look at the reporting frequency | Reports generated "On request only" | No proactive SLA visibility |

### Verification

Would you sign this SLA as a customer? If not, what needs to change?

---

## Lab 5: ITIL Practice Mapping Exercise

This is a non-coding exercise. For each FoodExpress scenario below, identify which ITIL practice(s) are involved:

| # | Scenario | Which Practice(s)? |
|---|---------|-------------------|
| 1 | A customer reports they cannot place an order | ? |
| 2 | The team discovers payment failures happen every Tuesday | ? |
| 3 | A developer requests access to production logs | ? |
| 4 | The team plans to upgrade MySQL from 8.0 to 8.2 | ? |
| 5 | Diwali is coming and traffic will 5x | ? |
| 6 | A new restaurant wants to onboard to the platform | ? |
| 7 | The order service container image has a CVE vulnerability | ? |
| 8 | Monthly SLA report shows 99.7% (below 99.9% target) | ? |

---

## Lab Submission

| # | Item | Done? |
|---|------|-------|
| 1 | All 7 incident template bugs fixed | [ ] |
| 2 | All 6 change request bugs fixed | [ ] |
| 3 | All 6 problem record bugs fixed | [ ] |
| 4 | All 6 SLA definition bugs fixed | [ ] |
| 5 | Practice mapping exercise completed | [ ] |
