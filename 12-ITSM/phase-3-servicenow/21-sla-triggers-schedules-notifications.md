# Section 21: SLAs, Triggers, Schedules, Events & Notifications

## Purpose

How ServiceNow **automates time-based rules, alerts, and communications** -- the invisible engine that keeps ITSM running without manual follow-up.

---

## 21.1: SLA Definitions

An SLA Definition = a **timer** that starts, pauses, and stops based on conditions.

### Anatomy of an SLA Definition

```
+------------------------------------------------------------------+
| SLA Definition: P1 Incident Resolution                           |
+------------------------------------------------------------------+
| Name:           P1 Incident Resolution                            |
| Table:          incident                                          |
| Type:           SLA                                               |
| Target:         30 minutes                                        |
|                                                                    |
| START condition:                                                   |
|   priority = 1 AND state = In Progress                            |
|   (Timer starts when P1 incident is acknowledged)                 |
|                                                                    |
| PAUSE condition:                                                   |
|   state = Awaiting User Info                                      |
|   (Timer pauses when waiting for the caller to respond)           |
|                                                                    |
| STOP condition:                                                    |
|   state = Resolved OR state = Closed                              |
|   (Timer stops when incident is resolved)                         |
|                                                                    |
| RESET condition:                                                   |
|   priority changes from 1 to something else                      |
|   (If downgraded from P1, this SLA no longer applies)            |
+------------------------------------------------------------------+
```

### UPI Example: NPCI's SLA Definitions

| SLA Definition | Table | Target | Start When | Stop When |
|---|---|---|---|---|
| P1 Incident Response | incident | 2 min | P1 created | Assigned to someone |
| P1 Incident Resolution | incident | 30 min | P1 in progress | Resolved |
| P2 Incident Resolution | incident | 4 hours | P2 in progress | Resolved |
| Normal Change Approval | change_request | 3 days | CHG submitted | CAB approves/rejects |
| Service Request Fulfillment | sc_req_item | Varies per item | RITM approved | RITM fulfilled |
| Bank Onboarding | sc_req_item | 30 days | RITM created | RITM closed |

### SLA States & Visual Indicators

```
SLA Timer on an Incident form:

+-------------------------------------------------+
| SLA: P1 Incident Resolution                    |
| Target: 30 minutes                              |
|                                                  |
| [==========>                    ]  12 min / 30   |
|                                                  |
| Status: In Progress                              |
| Time left: 18 minutes                            |
| Has breached: No                                 |
+-------------------------------------------------+

Color coding:
  GREEN  = > 50% time remaining
  YELLOW = 25-50% time remaining (warning)
  RED    = < 25% time remaining (critical)
  BLACK  = BREACHED (past target)
```

### SLA Percentage Stages

```
SLA: P1 Incident Resolution (30 min)

  0%  (0 min)  --> Timer starts
 50%  (15 min) --> Warning: "15 min left, still unresolved"
 75%  (22 min) --> Escalation: notify manager, reassign to L3
100%  (30 min) --> BREACHED: notify VP, mark SLA as breached
```

---

## 21.2: Schedules

Schedules define **when SLA timers count time**.

### Schedule Types

| Schedule | When time counts | UPI Example |
|---|---|---|
| **24x7** | All hours, all days | P1 incidents -- UPI never sleeps |
| **Business Hours** | Mon-Fri 9 AM - 6 PM | Service requests, normal changes |
| **Extended Hours** | Mon-Sat 8 AM - 8 PM | P2/P3 incidents |
| **Custom** | Org-specific | Banking hours: Mon-Fri 8 AM - 5 PM |

### How Schedules Affect SLA

```
SLA: Service Request Fulfillment
Target: 4 business hours
Schedule: Business Hours (Mon-Fri 9 AM - 6 PM)

Scenario:
  REQ submitted: Friday 4:00 PM
  Clock starts: Friday 4:00 PM
  Friday 4 PM - 6 PM = 2 hours counted
  Saturday & Sunday = 0 hours (not business hours)
  Monday 9 AM - 11 AM = 2 hours counted
  Total: 4 business hours

  SLA due: Monday 11:00 AM
  (NOT Saturday 8 PM -- weekends don't count)
```

### Exclusions (Holidays)

```
Schedule: Business Hours India
  Mon-Fri: 9:00 AM - 6:00 PM IST
  Exclusions:
    - Sep 14, 2026 (Holiday)
    - Oct 10-11, 2026 (Diwali)
    - Nov 1, 2026 (Kannada Rajyotsava)

  These days are SKIPPED in SLA calculation
```

---

## 21.3: Events

**Event** = an internal signal within ServiceNow that something happened.

```
Event is NOT the same as Monitoring Event (Section 16.1)

Monitoring Event:   "Server CPU at 95%"  (external, from infrastructure)
ServiceNow Event:   "Incident priority changed to P1"  (internal, platform)
```

### How Events Work

```
Something happens in ServiceNow
       |
       v
Business Rule fires (server-side script)
       |
       v
Event generated: gs.eventQueue('incident.priority.changed', ...)
       |
       v
Event registered in sysevent table
       |
       v
Notification Engine picks it up
       |
       v
Email / SMS / Slack sent
```

### UPI Example: Events at NPCI

| Event Name | Trigger | What happens next |
|---|---|---|
| `incident.created.p1` | P1 incident created | Page on-call, email NOC manager |
| `incident.sla.breach` | SLA timer reaches 100% | Email VP Engineering, create escalation task |
| `change.approved` | CAB approves a change | Email requester, update change calendar |
| `change.rejected` | CAB rejects a change | Email requester with rejection reason |
| `request.fulfilled` | Service request completed | Email requesting user |
| `problem.rca.completed` | RCA field populated | Email service owner, link to KB article |
| `ci.status.changed` | CMDB CI status changes | Notify CI owner |

---

## 21.4: Triggers

**Trigger** = a rule that fires automated actions when specific conditions are met.

### SLA Trigger Examples

```
Trigger: P1 SLA at 50%
  Condition: SLA "P1 Incident Resolution" reaches 50% (15 min)
  Actions:
    1. Send email to assignment group manager
    2. Add work note: "SLA WARNING: 15 min remaining"

Trigger: P1 SLA at 75%
  Condition: SLA "P1 Incident Resolution" reaches 75% (22 min)
  Actions:
    1. Reassign to L3 escalation group
    2. Send email to VP Engineering
    3. Add work note: "SLA CRITICAL: Auto-escalated to L3"

Trigger: P1 SLA BREACHED
  Condition: SLA "P1 Incident Resolution" reaches 100% (30 min)
  Actions:
    1. Send email to CTO
    2. Create escalation task for Incident Commander
    3. Add work note: "SLA BREACHED: Executive notification sent"
    4. Update dashboard: breach counter +1
```

### UPI Example: Escalation Timeline

```
Incident: INC0010042 (Axis Bank transactions failing) - P1

Timeline:
  08:03  Created, timer starts
         --> Event: incident.created.p1
         --> Notification: page on-call, email NOC

  08:10  (7 min, 23%) Still unresolved
         --> No trigger yet (below 50%)

  08:18  (15 min, 50%) Still unresolved
         --> TRIGGER: 50% warning
         --> Email to Platform Engineering manager

  08:25  (22 min, 75%) Still unresolved
         --> TRIGGER: 75% escalation
         --> Auto-reassign to L3 group
         --> Email to VP Engineering

  08:28  Resolved by L3! (25 min)
         --> SLA MET (under 30 min target)
         --> Timer stops
         --> No breach triggers fired
```

---

## 21.5: Email Notifications

### Notification Anatomy

```
+------------------------------------------------------------------+
| Notification: P1 Incident Created                                 |
+------------------------------------------------------------------+
| WHEN to send:                                                      |
|   Event: incident.created.p1                                      |
|   OR Condition: priority = 1 AND state = New                      |
|                                                                    |
| WHO to send to:                                                    |
|   - Assignment group members                                      |
|   - Assignment group manager                                      |
|   - CI owner (from CMDB)                                          |
|   - On-call rotation (from schedule)                               |
|                                                                    |
| WHAT to send:                                                      |
|   Subject: [P1] INC0010042: ${short_description}                  |
|   Body:                                                            |
|     Priority: ${priority}                                          |
|     Caller: ${caller_id.name}                                     |
|     Description: ${description}                                    |
|     Affected CI: ${cmdb_ci.name}                                  |
|     SLA Target: ${sla_due}                                        |
|     Link: ${URI}                                                   |
+------------------------------------------------------------------+
```

### Variable Substitution

ServiceNow uses `${field_name}` to inject live data into emails:

```
Subject: [P1] INC0010042: Axis Bank transactions failing

Body:
  A P1 incident has been created and assigned to your group.

  Priority:     1 - Critical
  Caller:       HDFC Bank Integration Team
  Description:  Transaction success rate for Axis Bank dropped to 34%.
                Affecting approximately 2.8 crore users.
  Affected CI:  CI-4001 PSP Gateway
  SLA Target:   Sep 21, 2026 08:33:00 (30 min from now)
```

### Common Notification Scenarios

| Scenario | Recipients | Channel |
|---|---|---|
| P1 incident created | On-call, NOC manager, assignment group | Email + PagerDuty |
| SLA about to breach (75%) | Assignment group manager, VP | Email + Slack |
| SLA breached | CTO, service owner | Email + SMS |
| Change approved by CAB | Requester, implementation team | Email |
| Change rejected | Requester | Email with reason |
| Service request fulfilled | Requesting user | Email |
| Knowledge article published | Relevant service teams | Email |

---

## 21.6: Templates

**Templates** = pre-filled forms that speed up common actions.

```
Template: "Bank Transaction Failure - P1"
+--------------------------------------------------+
| Pre-fills:                                        |
|   Category: Network/Transaction                   |
|   Subcategory: Bank Connectivity                  |
|   Priority: 1 - Critical                          |
|   Assignment group: Platform Engineering           |
|   Impact: 1 - High                                |
|   Urgency: 1 - High                               |
|   Short description: "[BankName] transactions     |
|                       failing - success rate [X]%" |
|                                                    |
| User fills in:                                     |
|   Bank name                                        |
|   Current success rate                             |
|   Additional details                               |
+--------------------------------------------------+

Without template: NOC types 12 fields manually (errors, inconsistency)
With template: NOC fills 3 fields, submits in 30 seconds
```

---

## End-to-End Automated Flow

```
P1 Incident at NPCI -- Full Automated Flow:

1. MONITORING detects Axis Bank failure rate drop
       |
2. Auto-creates INCIDENT (INC0010042) via API
       |
3. EVENT fired: incident.created.p1
       |
4. NOTIFICATION sent: email + PagerDuty to on-call
       |
5. SLA TIMER starts: 30 min countdown
       |
6. SCHEDULE applied: 24x7 (P1 = always counting)
       |
7. At 50% (15 min) --> TRIGGER fires warning notification
       |
8. At 75% (22 min) --> TRIGGER fires escalation, auto-reassigns
       |
9. Resolved at 25 min --> SLA STOPS, marked as MET
       |
10. EVENT fired: incident.resolved
        |
11. NOTIFICATION sent: resolution email to caller + stakeholders
        |
12. SLA REPORT updated: P1 resolution metrics dashboard refreshes
```

**Zero manual follow-up needed.** The system tracks, escalates, notifies, and reports -- automatically.

---

## Key Takeaway

> SLAs, triggers, schedules, events, and notifications are the **nervous system** of ServiceNow.
>
> - **SLA Definitions** = the clock (how long do we have?)
> - **Schedules** = when the clock ticks (business hours? 24x7?)
> - **Events** = internal signals (something happened)
> - **Triggers** = automated reactions (if X then do Y)
> - **Notifications** = communication (tell the right people)
> - **Templates** = speed and consistency (don't type from scratch)
>
> Together, they ensure: **nothing falls through the cracks, and the right people know at the right time -- without anyone chasing manually.**
