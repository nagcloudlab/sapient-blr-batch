# Lab 09: SLA, SLO & SLI — Service Level Management

**Level:** Intermediate-Advanced | **Duration:** 90 min | **Prerequisites:** Labs 07-08 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand the SLA-SLO-SLI hierarchy and how they interconnect
- Create 7 SLA definitions for NPCI UPI incident management (P1 through P4)
- Configure custom schedules for 24x7 critical support and business hours
- Define Service Level Objectives for the UPI platform
- Map Service Level Indicators from Prometheus metrics to ServiceNow
- Configure SLA breach notifications with escalation chains
- Test the full SLA lifecycle: attach, pause, resume, achieve, breach

---

## Scenario: Defining Service Levels for UPI Payment Processing

```
  NPCI has launched UPI Payment Processing as a Business Service in ServiceNow
  (Lab 08). The CIs are in the CMDB (Lab 07). But there is NO mechanism to
  track whether the support team is meeting its commitments.

  Questions that cannot be answered today:
    - "How fast do we respond to P1 incidents?"
    - "Are we meeting the RBI-mandated 99.5% uptime?"
    - "What percentage of incidents breach their resolution target?"
    - "When should a manager be alerted that an SLA is about to breach?"

  This lab builds the Service Level Management framework that answers all
  of these questions — with automatic timers, breach notifications, and
  dashboards.
```

---

## Part 1: ITIL 4 Service Level Management — Theory

### 1.1 What is Service Level Management?

Service Level Management (SLM) is one of ITIL 4's 34 practices. Its purpose:

```
  "To set clear business-based targets for service levels, and to ensure
   that delivery of services is properly assessed, monitored, and managed
   against these targets."
                                          — ITIL 4 Foundation, Axelos
```

SLM sits at the intersection of the provider and the consumer. It translates
business expectations into measurable, trackable commitments.

### 1.2 The SLA-SLO-SLI Hierarchy

This is the most important concept in this lab. These three terms are often
confused. They form a strict hierarchy:

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │                                                                     │
  │   SLA  (Service Level Agreement)                                    │
  │   ═══════════════════════════════                                   │
  │   A FORMAL AGREEMENT between provider and customer.                 │
  │   Contains multiple SLOs. Has legal/contractual weight.             │
  │                                                                     │
  │   Example: "NPCI UPI Platform Support Agreement"                    │
  │            - Signed between NPCI Operations and Member Banks        │
  │            - Valid: Apr 2024 - Mar 2025                             │
  │            - Contains 6 specific objectives (SLOs)                  │
  │                                                                     │
  │   ┌─────────────────────────────────────────────────────────────┐   │
  │   │                                                             │   │
  │   │   SLO  (Service Level Objective)                            │   │
  │   │   ═══════════════════════════════                            │   │
  │   │   A SPECIFIC MEASURABLE TARGET within the SLA.              │   │
  │   │   "What we promise to achieve."                             │   │
  │   │                                                             │   │
  │   │   Examples:                                                 │   │
  │   │     - "99.95% platform availability per month"              │   │
  │   │     - "P1 incidents resolved within 1 hour"                 │   │
  │   │     - "P95 transaction latency < 500ms"                     │   │
  │   │                                                             │   │
  │   │   ┌─────────────────────────────────────────────────────┐   │   │
  │   │   │                                                     │   │   │
  │   │   │   SLI  (Service Level Indicator)                    │   │   │
  │   │   │   ═══════════════════════════════                    │   │   │
  │   │   │   The ACTUAL METRIC that measures the SLO.          │   │   │
  │   │   │   "What we actually measure."                       │   │   │
  │   │   │                                                     │   │   │
  │   │   │   Examples:                                         │   │   │
  │   │   │     - Prometheus `up` metric → Availability         │   │   │
  │   │   │     - `http_server_requests_seconds_count`          │   │   │
  │   │   │       with status != 5xx → Success Rate             │   │   │
  │   │   │     - `histogram_quantile(0.95, ...)` → Latency     │   │   │
  │   │   │     - ServiceNow task_sla.has_breached → SLA %      │   │   │
  │   │   │                                                     │   │   │
  │   │   └─────────────────────────────────────────────────────┘   │   │
  │   │                                                             │   │
  │   └─────────────────────────────────────────────────────────────┘   │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘
```

**The key relationship:**

```
  SLA contains multiple SLOs.
  Each SLO is measured by one or more SLIs.

  SLA  →  "We agree to these service levels"         (Agreement)
  SLO  →  "Specifically, we target 99.95% uptime"    (Objective)
  SLI  →  "We measure uptime using Prometheus `up`"  (Indicator)
```

### 1.3 Watermelon SLAs — The Anti-Pattern

A "Watermelon SLA" looks green on the outside but is red on the inside:

```
  ┌─────────────────────────────────────────────────────┐
  │                                                     │
  │   SLA Report says:  "98% of SLAs met!"  ✓ GREEN    │
  │                                                     │
  │   But reality:                                      │
  │     - Users wait 45 min on hold before someone      │
  │       picks up (but "response" SLA starts when      │
  │       the ticket is created, not when user calls)   │
  │     - Incidents are "resolved" by closing them      │
  │       without actually fixing the issue             │
  │     - P1 incidents are downgraded to P3 to avoid    │
  │       SLA breach                                    │
  │     - Customer satisfaction is at 2.1 / 5.0         │
  │                                                     │
  │   The SLA metrics are GREEN but the customer        │
  │   experience is RED.                                │
  │                                                     │
  │   Hence: WATERMELON  (green outside, red inside)    │
  │                                                     │
  └─────────────────────────────────────────────────────┘
```

**How to avoid Watermelon SLAs:**
1. Measure outcomes, not just outputs (Did the user's problem get solved?)
2. Include customer satisfaction metrics (CSAT surveys after resolution)
3. Track re-open rates (Was the incident truly resolved?)
4. Use Experience Level Agreements (XLAs) alongside SLAs
5. Audit priority assignments (Are P1s being downgraded to dodge SLAs?)

### 1.4 XLA — Experience Level Agreement

XLAs go beyond SLAs by measuring the actual user experience:

```
  SLA:  "We resolved your incident in 45 minutes."
  XLA:  "How satisfied were you with the resolution? Was your work disrupted?"

  SLA metrics:                     XLA metrics:
  ├── Response time                ├── Employee satisfaction score
  ├── Resolution time              ├── Productivity impact
  ├── Uptime percentage            ├── Sentiment analysis
  └── Incidents per month          ├── Adoption / usage rates
                                   └── Digital experience score
```

For UPI, an XLA might include:
- Merchant satisfaction with onboarding process
- End-user perception of transaction speed
- Developer satisfaction with API documentation and support

### 1.5 Service Level Management in the Service Value Chain

```
  PLAN         →  Define SLA strategy, agree on service levels
  ENGAGE       →  Negotiate SLAs with stakeholders (member banks, RBI)
  DESIGN       →  Design SLA definitions in ServiceNow (THIS LAB)
  OBTAIN/BUILD →  Build monitoring to collect SLIs
  DELIVER      →  Operate services, SLA clocks running
  IMPROVE      →  Review SLA performance, adjust targets
```

### 1.6 Real-World UPI SLA Requirements

These are based on actual NPCI and RBI regulatory requirements:

```
  ┌──────────────────────────────────────────────────────────────┐
  │  NPCI UPI Service Level Requirements                        │
  ├──────────────────────────────────────────────────────────────┤
  │                                                              │
  │  Platform Availability:                                      │
  │    - UPI platform uptime: 99.5% (NPCI mandate)              │
  │    - Planned maintenance window: Sunday 1AM-5AM IST          │
  │    - Maximum unplanned downtime: 3.65 hours/month            │
  │                                                              │
  │  Transaction Performance:                                    │
  │    - End-to-end response: < 30 seconds (RBI guideline)       │
  │    - P95 API latency: < 500ms                                │
  │    - Transaction success rate: > 99.5%                       │
  │                                                              │
  │  Incident Response:                                          │
  │    - P1 (Critical) response: < 30 minutes                    │
  │    - P1 (Critical) resolution: < 1 hour                      │
  │    - P2 (High) response: < 1 hour                            │
  │    - P2 (High) resolution: < 4 hours                         │
  │    - P3 (Moderate) response: < 4 hours                       │
  │    - P3 (Moderate) resolution: < 24 hours                    │
  │    - P4 (Low) resolution: < 72 hours                         │
  │                                                              │
  │  Regulatory Reporting:                                       │
  │    - Major incident report to RBI: within 6 hours            │
  │    - Monthly SLA compliance report: by 5th of next month     │
  │    - Quarterly service review with member banks              │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

---

## Part 2: ServiceNow SLA Module Architecture

### 2.1 Core Tables

Before creating anything, understand the data model:

```
  ┌────────────────────────────────────────────────────────┐
  │  contract_sla  (SLA Definition)                        │
  │  ════════════════════════════════                       │
  │  The TEMPLATE. Defines the rules:                      │
  │    - Which tasks does this SLA apply to?               │
  │    - When does the clock start?                        │
  │    - When does it pause? Stop?                         │
  │    - What is the target duration?                      │
  │    - What schedule (business hours) applies?           │
  │                                                        │
  │  You create 7 of these in this lab.                    │
  │  They sit waiting for matching tasks to appear.        │
  └────────────────────────────────────────────────────────┘
                         │
                         │  When a matching task is created/updated,
                         │  ServiceNow automatically creates:
                         ▼
  ┌────────────────────────────────────────────────────────┐
  │  task_sla  (Task SLA)                                  │
  │  ════════════════════                                   │
  │  The INSTANCE. An individual SLA record attached to    │
  │  a specific task (incident, request, etc.)             │
  │                                                        │
  │  Contains:                                             │
  │    - Reference to the SLA Definition                   │
  │    - Reference to the Task (e.g., INC0010001)          │
  │    - Start time, end time, breach time                 │
  │    - Current state (In Progress, Paused, etc.)         │
  │    - Percentage elapsed                                │
  │    - Has breached (true/false)                         │
  │                                                        │
  │  Created AUTOMATICALLY — you never create these        │
  │  manually.                                             │
  └────────────────────────────────────────────────────────┘
```

### 2.2 SLA States

Each Task SLA moves through these states:

```
  ┌──────────┐     ┌──────────┐     ┌──────────────┐
  │          │     │          │     │              │
  │  In      │────►│  Paused  │────►│  In          │
  │ Progress │     │          │     │  Progress    │
  │          │◄────│          │     │  (resumed)   │
  └────┬─────┘     └──────────┘     └──────┬───────┘
       │                                    │
       │     ┌──────────────┐              │
       │     │              │              │
       ├────►│  Achieved    │◄─────────────┤
       │     │  (completed  │              │
       │     │   within     │              │
       │     │   target)    │              │
       │     └──────────────┘              │
       │                                    │
       │     ┌──────────────┐              │
       │     │              │              │
       └────►│  Breached    │◄─────────────┘
             │  (target     │
             │   exceeded)  │
             └──────────────┘

  States:
  ───────
  In Progress  →  SLA clock is ticking
  Paused       →  Clock stopped (e.g., waiting on customer)
  Achieved     →  Stop condition met BEFORE breach time
  Breached     →  Breach time reached BEFORE stop condition
  Cancelled    →  SLA no longer applies (e.g., incident reassigned)
```

### 2.3 SLA Workflow: Start, Pause, Stop, Breach

```
  1. START CONDITION MET
     │  (e.g., Priority = 1 AND State = New)
     │
     │  ServiceNow creates a task_sla record.
     │  Breach time = now + duration (adjusted for schedule).
     │
     ▼
  2. CLOCK TICKING
     │  Percentage increases over time.
     │  50% notification? 75% notification?
     │
     ▼
  3a. PAUSE CONDITION MET?  ──── YES ──→  Clock pauses.
     │                                     Breach time pushed forward.
     │  NO                                 Resume when pause condition
     │                                     no longer met.
     ▼
  3b. STOP CONDITION MET?  ──── YES ──→  SLA ACHIEVED (if not breached)
     │                                    or BREACHED (if past due).
     │  NO
     ▼
  4. BREACH TIME REACHED  ──→  SLA BREACHED
     │                         (but clock keeps ticking until stop
     │                          condition is met — for reporting
     │                          "how far past breach")
     ▼
  5. STOP CONDITION EVENTUALLY MET  ──→  Final state recorded.
     Actual elapsed time and breach amount captured.
```

### 2.4 Retroactive Start

ServiceNow supports retroactive SLA start. If an incident is created at 10:00 AM
but priority is changed to P1 at 10:15 AM, the SLA can start retroactively from
10:00 AM (when the incident was created) rather than 10:15 AM (when it matched).

This is controlled by the **Retroactive start** checkbox on the SLA Definition.

### 2.5 SLA Timeline Visualization

ServiceNow provides a visual timeline on each task showing:
- When each SLA started
- Current position relative to breach time
- Pause periods (shown as flat segments)
- Color coding: green (on track), yellow (warning), red (breached)

To view: open any incident, scroll to the **Task SLAs** related list, click on
the SLA record, then click the **SLA Timeline** icon.

---

## Part 3: Create SLA Definitions

### Navigation

For ALL SLA definitions in this part:

```
  All > Service Level Management > SLA > SLA Definitions
  (or type "sla definitions" in the navigator filter)
```

Click **New** to create each one.

---

### 3.1 SLA Definition 1: P1 Critical — Response SLA (30 minutes)

This SLA measures how quickly the team **responds** to a P1 incident
(moves it from New to In Progress / Acknowledged).

**Navigation:** Service Level Management > SLA > SLA Definitions > **New**

| Field | Value | Notes |
|---|---|---|
| **Name** | `NPCI UPI - P1 Critical Response` | Descriptive name with org prefix |
| **Type** | `SLA` | Options: SLA, OLA, Underpinning Contract |
| **Target** | `Response` | This is a response-time SLA |
| **Table** | `Incident [incident]` | This SLA applies to the incident table |
| **Duration** | `30 Minutes` | NPCI P1 response target |
| **Schedule** | `24x7` | P1 is always critical, no business hours |
| **Timezone** | `Asia/Kolkata` | IST — NPCI headquarters timezone |
| **Active** | Checked | Enable this SLA definition |
| **Retroactive start** | Unchecked | Start when conditions first match |
| **Reset on Breach** | Unchecked | Do not restart after breach |

**Start Conditions Tab:**

Click the **Start Conditions** tab. Build the condition:

```
  Priority  is  1 - Critical
  AND
  State     is  New
```

Explanation: The SLA clock starts the moment a P1 incident enters the "New" state.

**Pause Conditions Tab:**

Click the **Pause Conditions** tab. Build the condition:

```
  State  is  Awaiting User Info
```

Explanation: If the support team is waiting for information from the caller
(e.g., "Which UPI VPA was affected?"), the clock should pause. It is not
fair to count wait time against the support team.

**Stop Conditions Tab:**

Click the **Stop Conditions** tab. Build the condition:

```
  State  is  In Progress
  OR
  State  is  Resolved
  OR
  State  is  Closed
```

Explanation: The response SLA is satisfied when someone acknowledges the
incident (moves to In Progress) or if it is resolved directly.

**Click Save.**

You should see the SLA Definition record with:
- Sys ID populated
- Created/Updated timestamps
- The SLA is now **active** and waiting for matching incidents

---

### 3.2 SLA Definition 2: P1 Critical — Resolution SLA (1 hour)

This SLA measures how quickly the team **resolves** a P1 incident.

**Navigation:** SLA Definitions > **New**

| Field | Value | Notes |
|---|---|---|
| **Name** | `NPCI UPI - P1 Critical Resolution` | |
| **Type** | `SLA` | |
| **Target** | `Resolution` | This is a resolution-time SLA |
| **Table** | `Incident [incident]` | |
| **Duration** | `1 Hour` | NPCI P1 resolution target |
| **Schedule** | `24x7` | Critical — no business hours restriction |
| **Timezone** | `Asia/Kolkata` | |
| **Active** | Checked | |

**Start Conditions:**

```
  Priority  is  1 - Critical
  AND
  State     is  In Progress
```

Note: The resolution clock starts when someone begins working on the incident
(State = In Progress), not when it is created. This is intentional — the
response SLA covers the gap between creation and acknowledgment.

**Pause Conditions:**

```
  State  is  Awaiting User Info
  OR
  State  is  Awaiting Vendor
```

Explanation: Pauses when waiting on external parties. For UPI, "Awaiting Vendor"
might mean waiting for a member bank to provide transaction logs.

**Stop Conditions:**

```
  State  is  Resolved
```

Explanation: The resolution SLA stops when the incident is resolved. It does
NOT stop at "Closed" — resolution is the point where the fix is applied, and
closure is an administrative step afterward.

**Click Save.**

---

### 3.3 SLA Definition 3: P2 High — Response SLA (1 hour)

| Field | Value | Notes |
|---|---|---|
| **Name** | `NPCI UPI - P2 High Response` | |
| **Type** | `SLA` | |
| **Target** | `Response` | |
| **Table** | `Incident [incident]` | |
| **Duration** | `1 Hour` | P2 gets 1 hour to respond |
| **Schedule** | `24x7` | P2 is still monitored 24x7 for UPI |
| **Timezone** | `Asia/Kolkata` | |
| **Active** | Checked | |

**Start Conditions:**

```
  Priority  is  2 - High
  AND
  State     is  New
```

**Pause Conditions:**

```
  State  is  Awaiting User Info
```

**Stop Conditions:**

```
  State  is  In Progress
  OR
  State  is  Resolved
  OR
  State  is  Closed
```

**Click Save.**

---

### 3.4 SLA Definition 4: P2 High — Resolution SLA (4 hours)

| Field | Value | Notes |
|---|---|---|
| **Name** | `NPCI UPI - P2 High Resolution` | |
| **Type** | `SLA` | |
| **Target** | `Resolution` | |
| **Table** | `Incident [incident]` | |
| **Duration** | `4 Hours` | P2 resolution target |
| **Schedule** | `24x7` | |
| **Timezone** | `Asia/Kolkata` | |
| **Active** | Checked | |

**Start Conditions:**

```
  Priority  is  2 - High
  AND
  State     is  In Progress
```

**Pause Conditions:**

```
  State  is  Awaiting User Info
  OR
  State  is  Awaiting Vendor
```

**Stop Conditions:**

```
  State  is  Resolved
```

**Click Save.**

---

### 3.5 SLA Definition 5: P3 Moderate — Response SLA (4 hours)

| Field | Value | Notes |
|---|---|---|
| **Name** | `NPCI UPI - P3 Moderate Response` | |
| **Type** | `SLA` | |
| **Target** | `Response` | |
| **Table** | `Incident [incident]` | |
| **Duration** | `4 Hours` | P3 has longer response window |
| **Schedule** | `NPCI Business Hours` | P3 uses business hours (created in Part 4) |
| **Timezone** | `Asia/Kolkata` | |
| **Active** | Checked | |

**Start Conditions:**

```
  Priority  is  3 - Moderate
  AND
  State     is  New
```

**Pause Conditions:**

```
  State  is  Awaiting User Info
```

**Stop Conditions:**

```
  State  is  In Progress
  OR
  State  is  Resolved
  OR
  State  is  Closed
```

**Click Save.**

> **Note:** This SLA references the "NPCI Business Hours" schedule that we
> create in Part 4. If you have not created it yet, use the default "8-5
> weekdays excluding holidays" schedule and update it later.

---

### 3.6 SLA Definition 6: P3 Moderate — Resolution SLA (24 hours)

| Field | Value | Notes |
|---|---|---|
| **Name** | `NPCI UPI - P3 Moderate Resolution` | |
| **Type** | `SLA` | |
| **Target** | `Resolution` | |
| **Table** | `Incident [incident]` | |
| **Duration** | `24 Hours` | 24 business hours for P3 |
| **Schedule** | `NPCI Business Hours` | Business hours only |
| **Timezone** | `Asia/Kolkata` | |
| **Active** | Checked | |

**Start Conditions:**

```
  Priority  is  3 - Moderate
  AND
  State     is  In Progress
```

**Pause Conditions:**

```
  State  is  Awaiting User Info
  OR
  State  is  Awaiting Vendor
```

**Stop Conditions:**

```
  State  is  Resolved
```

**Click Save.**

---

### 3.7 SLA Definition 7: P4 Low — Resolution SLA (72 hours)

P4 incidents typically do not have a separate response SLA — only resolution.

| Field | Value | Notes |
|---|---|---|
| **Name** | `NPCI UPI - P4 Low Resolution` | |
| **Type** | `SLA` | |
| **Target** | `Resolution` | |
| **Table** | `Incident [incident]` | |
| **Duration** | `72 Hours` | 72 business hours — roughly 6 business days |
| **Schedule** | `NPCI Business Hours` | Business hours only |
| **Timezone** | `Asia/Kolkata` | |
| **Active** | Checked | |

**Start Conditions:**

```
  Priority  is  4 - Low
  AND
  State     is  In Progress
```

**Pause Conditions:**

```
  State  is  Awaiting User Info
  OR
  State  is  Awaiting Vendor
```

**Stop Conditions:**

```
  State  is  Resolved
```

**Click Save.**

---

### 3.8 Summary of All SLA Definitions

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │  NPCI UPI SLA Definitions — Complete Matrix                            │
  ├────────┬───────────────────────────────────┬──────────┬─────────────────┤
  │ Priority│ SLA Name                          │ Duration │ Schedule        │
  ├────────┼───────────────────────────────────┼──────────┼─────────────────┤
  │ P1     │ NPCI UPI - P1 Critical Response   │ 30 min   │ 24x7            │
  │ P1     │ NPCI UPI - P1 Critical Resolution │ 1 hour   │ 24x7            │
  │ P2     │ NPCI UPI - P2 High Response       │ 1 hour   │ 24x7            │
  │ P2     │ NPCI UPI - P2 High Resolution     │ 4 hours  │ 24x7            │
  │ P3     │ NPCI UPI - P3 Moderate Response   │ 4 hours  │ Business Hours  │
  │ P3     │ NPCI UPI - P3 Moderate Resolution │ 24 hours │ Business Hours  │
  │ P4     │ NPCI UPI - P4 Low Resolution      │ 72 hours │ Business Hours  │
  └────────┴───────────────────────────────────┴──────────┴─────────────────┘

  Total: 7 SLA Definitions
  When a matching incident is created/updated, ServiceNow AUTOMATICALLY
  attaches the relevant Task SLA records. No manual action needed.
```

---

## Part 4: SLA Schedules & Business Hours

### 4.1 Understanding Schedules

SLA schedules determine WHEN the clock ticks. A "4-hour resolution SLA" with
a business-hours schedule means 4 hours of **business time**, not wall-clock time.

```
  Scenario: P3 incident created Friday at 4:00 PM IST
  Schedule: NPCI Business Hours (Mon-Sat 8AM-8PM)

  Clock ticks:  4:00 PM - 8:00 PM Friday    =  4 hours
  Clock paused: 8:00 PM Friday - 8:00 AM Saturday (overnight)
  Clock ticks:  8:00 AM - 8:00 PM Saturday   = 12 hours (but only need 4 more)

  Total business hours elapsed: 4 + 4 = 8 hours
  Wall clock elapsed: 20 hours (Friday 4PM to Saturday 12PM)

  Without schedule: SLA would breach at 8:00 PM Friday (4 hours wall clock)
  With schedule: SLA breach at 12:00 PM Saturday (4 hours business time)
```

### 4.2 Create Schedule: "NPCI 24x7 Critical Support"

**Navigation:** System Scheduler > Schedules > **New**

(or type `sys_schedule.do` in the navigator)

| Field | Value |
|---|---|
| **Name** | `NPCI 24x7 Critical Support` |
| **Time zone** | `Asia/Kolkata` |
| **Type** | `Standard` |
| **Document** | (leave blank) |

**Click Save** (to get the sys_id), then add schedule entries.

**Add Schedule Entries:**

In the **Schedule Entries** related list, click **New** and create 7 entries
(one for each day):

| Entry Name | Type | Day | Start | End |
|---|---|---|---|---|
| `Sunday` | `Time range` | `Sunday` | `00:00:00` | `23:59:59` |
| `Monday` | `Time range` | `Monday` | `00:00:00` | `23:59:59` |
| `Tuesday` | `Time range` | `Tuesday` | `00:00:00` | `23:59:59` |
| `Wednesday` | `Time range` | `Wednesday` | `00:00:00` | `23:59:59` |
| `Thursday` | `Time range` | `Thursday` | `00:00:00` | `23:59:59` |
| `Friday` | `Time range` | `Friday` | `00:00:00` | `23:59:59` |
| `Saturday` | `Time range` | `Saturday` | `00:00:00` | `23:59:59` |

> **Tip:** ServiceNow includes a built-in "24x7" schedule. You can use that
> instead. Creating a custom one is useful if you want to exclude specific
> maintenance windows (e.g., Sunday 1AM-5AM IST for planned maintenance).

### 4.3 Create Schedule: "NPCI Business Hours" (Mon-Sat 8AM-8PM IST)

**Navigation:** System Scheduler > Schedules > **New**

| Field | Value |
|---|---|
| **Name** | `NPCI Business Hours` |
| **Time zone** | `Asia/Kolkata` |
| **Type** | `Standard` |

**Click Save**, then add entries:

| Entry Name | Type | Day | Start | End |
|---|---|---|---|---|
| `Monday` | `Time range` | `Monday` | `08:00:00` | `20:00:00` |
| `Tuesday` | `Time range` | `Tuesday` | `08:00:00` | `20:00:00` |
| `Wednesday` | `Time range` | `Wednesday` | `08:00:00` | `20:00:00` |
| `Thursday` | `Time range` | `Thursday` | `08:00:00` | `20:00:00` |
| `Friday` | `Time range` | `Friday` | `08:00:00` | `20:00:00` |
| `Saturday` | `Time range` | `Saturday` | `08:00:00` | `20:00:00` |

Note: Sunday is intentionally excluded — NPCI observes Sunday as a non-business
day for P3/P4 incidents.

### 4.4 Create Holiday Schedule: Indian Bank Holidays

**Navigation:** System Scheduler > Schedules > **New**

| Field | Value |
|---|---|
| **Name** | `Indian Bank Holidays 2024-2025` |
| **Time zone** | `Asia/Kolkata` |
| **Type** | `Exclude` |

**Click Save**, then add entries for each holiday:

| Entry Name | Type | Start Date | End Date |
|---|---|---|---|
| `Republic Day` | `Exclude` | `2025-01-26` | `2025-01-26` |
| `Holi` | `Exclude` | `2025-03-14` | `2025-03-14` |
| `Good Friday` | `Exclude` | `2025-04-18` | `2025-04-18` |
| `Dr Ambedkar Jayanti` | `Exclude` | `2025-04-14` | `2025-04-14` |
| `May Day` | `Exclude` | `2025-05-01` | `2025-05-01` |
| `Independence Day` | `Exclude` | `2025-08-15` | `2025-08-15` |
| `Mahatma Gandhi Jayanti` | `Exclude` | `2025-10-02` | `2025-10-02` |
| `Dussehra` | `Exclude` | `2025-10-02` | `2025-10-02` |
| `Diwali` | `Exclude` | `2025-10-20` | `2025-10-21` |
| `Christmas` | `Exclude` | `2025-12-25` | `2025-12-25` |

### 4.5 Link Holiday Schedule to Business Hours

1. Open the **NPCI Business Hours** schedule
2. In the **Child Schedules** related list, click **Edit**
3. Add `Indian Bank Holidays 2024-2025` as a child schedule
4. **Save**

Now the business hours schedule will automatically exclude Indian bank holidays.

```
  Result:  NPCI Business Hours
           ├── Mon-Sat 8AM-8PM IST
           └── MINUS Indian Bank Holidays

  Example: If a P3 incident is created on August 14 at 6PM:
           - Clock ticks: 6PM-8PM (2 hours)
           - August 15 (Independence Day): clock paused ALL day
           - Clock resumes: August 16 at 8AM
```

### 4.6 Assign Schedules to SLA Definitions

Go back to each SLA Definition and set the correct schedule:

| SLA Definition | Schedule |
|---|---|
| P1 Critical Response | `24x7` or `NPCI 24x7 Critical Support` |
| P1 Critical Resolution | `24x7` or `NPCI 24x7 Critical Support` |
| P2 High Response | `24x7` or `NPCI 24x7 Critical Support` |
| P2 High Resolution | `24x7` or `NPCI 24x7 Critical Support` |
| P3 Moderate Response | `NPCI Business Hours` |
| P3 Moderate Resolution | `NPCI Business Hours` |
| P4 Low Resolution | `NPCI Business Hours` |

### 4.7 Timezone Handling Deep Dive

```
  Why timezone matters for SLAs:

  1. NPCI is headquartered in Mumbai (IST = UTC+5:30)
  2. Some member banks operate in different timezones
  3. ServiceNow stores all times in UTC internally
  4. The SLA schedule must specify the correct timezone

  Common pitfall:
    - Admin sets schedule to "8AM-8PM" but timezone is UTC
    - Business hours become 1:30 PM - 1:30 AM IST
    - SLA calculations are completely wrong

  Rule: ALWAYS set the schedule timezone to match the support team's
        working timezone. For NPCI, this is Asia/Kolkata (IST).
```

---

## Part 5: SLO Configuration

### 5.1 Defining Service Level Objectives for UPI

SLOs are the specific targets within our service level agreement. ServiceNow
does not have a dedicated "SLO" module in the base platform, but we can
represent SLOs using Performance Analytics (PA) indicators, custom tables,
or the Service Level Management module.

Here are the SLOs we need to track:

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │  UPI Platform Service Level Objectives                                │
  ├──────┬──────────────────────────────┬──────────┬──────────────────────┤
  │  ID  │  Objective                   │  Target  │  Measurement Period  │
  ├──────┼──────────────────────────────┼──────────┼──────────────────────┤
  │ SLO1 │ Platform Availability        │ 99.95%   │ Monthly              │
  │ SLO2 │ Transaction Success Rate     │ 99.5%    │ Daily                │
  │ SLO3 │ P95 Transaction Latency      │ < 500ms  │ Hourly (rolling)     │
  │ SLO4 │ Incident Resolution in SLA   │ > 95%    │ Monthly              │
  │ SLO5 │ Change Success Rate          │ > 98%    │ Quarterly            │
  │ SLO6 │ MTTR for P1 Incidents        │ < 30 min │ Monthly              │
  └──────┴──────────────────────────────┴──────────┴──────────────────────┘
```

### 5.2 SLO1: Platform Availability (99.95%)

**What it means:**

```
  99.95% uptime per month = maximum 21.9 minutes downtime

  Calculation:
    Availability = (Total minutes - Downtime minutes) / Total minutes * 100

    30-day month = 43,200 minutes
    99.95% of 43,200 = 43,178.4 minutes of uptime
    Maximum downtime = 21.6 minutes

  Compare to NPCI mandate (99.5%):
    99.5% = 216 minutes (3.6 hours) downtime allowed
    Our target (99.95%) is 10x stricter than the mandate
```

**How to track in ServiceNow:**

Option A — Performance Analytics Indicator:

1. Navigate to **Performance Analytics > Indicators > Create New**
2. Configure:

| Field | Value |
|---|---|
| **Name** | `UPI Platform Availability %` |
| **Direction** | `Maximize` |
| **Unit** | `%` |
| **Frequency** | `Monthly` |
| **Breakdown** | `Service` |
| **Target** | `99.95` |

3. Data collection: This indicator would be populated by an integration
   from Prometheus (via scheduled import or REST call) or by a Business Rule
   that calculates uptime from incident downtime records.

Option B — Custom Table (`u_slo_tracking`):

Create a custom table to store SLO snapshots. This is more explicit than PA.

| Column | Type | Description |
|---|---|---|
| `u_slo_name` | String | e.g., "Platform Availability" |
| `u_target_value` | Decimal | e.g., 99.95 |
| `u_actual_value` | Decimal | e.g., 99.97 |
| `u_measurement_period` | Date range | e.g., Sep 1-30, 2024 |
| `u_service` | Reference (cmdb_ci_service) | UPI Payment Processing |
| `u_status` | Choice | Met / Not Met / At Risk |
| `u_breach_margin` | Decimal | How far from target |

### 5.3 SLO2: Transaction Success Rate (99.5%)

```
  Success Rate = (Total Transactions - Failed Transactions) / Total * 100

  Source SLI: Prometheus metric
    http_server_requests_seconds_count{status!~"5.."}  (successful)
    http_server_requests_seconds_count                  (total)

  Daily target: 99.5%
  Example: 10,000,000 daily transactions
           Maximum failures allowed: 50,000

  In ServiceNow: Tracked via PA indicator or integration from Grafana
```

### 5.4 SLO3: P95 Transaction Latency (< 500ms)

```
  P95 = 95th percentile latency
  Meaning: 95% of transactions complete in less than 500ms

  Source SLI: Prometheus metric
    histogram_quantile(0.95,
      rate(http_server_requests_seconds_bucket[5m])
    )

  If P95 > 500ms, it indicates performance degradation.
  This SLO is measured on a rolling hourly basis.
```

### 5.5 SLO4: Incident Resolution Within SLA (> 95%)

This SLO can be calculated DIRECTLY from ServiceNow data:

```
  SLA Compliance % = (Achieved Task SLAs / Total Task SLAs) * 100

  Query:
    Table: task_sla
    Filter: type = Resolution AND end_time IN last 30 days
    Group by: has_breached (true/false)

  Target: > 95% achieved (< 5% breached)
```

**Build this as a ServiceNow Report:**

1. Navigate to **Reports > Create New**
2. Configure:

| Field | Value |
|---|---|
| **Name** | `SLO4 - Incident Resolution SLA Compliance` |
| **Source type** | `Table` |
| **Table** | `Task SLA [task_sla]` |
| **Type** | `Pie chart` |
| **Group by** | `Has breached` |
| **Filter** | `Type = SLA AND Stage = Achieved or Breached AND Ended AFTER 30 days ago` |

3. **Save and run** — you will see the split between Achieved and Breached.

### 5.6 SLO5: Change Success Rate (> 98%)

```
  Change Success Rate = (Successful Changes / Total Changes) * 100

  Query:
    Table: change_request
    Filter: closed_at IN last quarter
    Group by: close_code (Successful / Unsuccessful)

  Target: > 98% successful
  Measured: Quarterly
```

### 5.7 SLO6: MTTR for P1 Incidents (< 30 minutes)

```
  MTTR = Mean Time to Restore = Average time from incident start to resolution
         for P1 incidents

  Calculation:
    For each resolved P1 incident:
      restore_time = resolved_at - sys_created_on (adjusted for pause periods)
    MTTR = average(restore_time) across all P1 incidents in the period

  Target: < 30 minutes average
  Measured: Monthly

  ServiceNow field mapping:
    Start:  incident.sys_created_on
    End:    incident.resolved_at
    Delta:  incident.calendar_duration or incident.business_duration
```

**Build MTTR Report:**

1. Navigate to **Reports > Create New**
2. Configure:

| Field | Value |
|---|---|
| **Name** | `SLO6 - MTTR P1 Incidents` |
| **Source type** | `Table` |
| **Table** | `Incident [incident]` |
| **Type** | `Bar chart` |
| **Aggregation** | `Average` |
| **Aggregate by** | `Business resolve time` |
| **Filter** | `Priority = 1 AND State = Resolved AND Resolved IN last 30 days` |
| **Trend by** | `Resolved (Monthly)` |

3. **Save and run** — shows average resolution time trending over months.

### 5.8 SLO Dashboard

Create a dashboard that shows all SLOs at a glance:

1. Navigate to **Self-Service > Dashboards** (or **Performance Analytics > Dashboards**)
2. Click **New** and name it `NPCI UPI - SLO Dashboard`
3. Add these widgets:

```
  ┌──────────────────────────────────────────────────────────────────────┐
  │  NPCI UPI — Service Level Objectives Dashboard                      │
  ├──────────────────────┬──────────────────────┬───────────────────────┤
  │                      │                      │                       │
  │  SLO1: Availability  │  SLO2: Success Rate  │  SLO3: P95 Latency   │
  │  Target: 99.95%      │  Target: 99.5%       │  Target: < 500ms     │
  │  Actual: 99.97%      │  Actual: 99.7%       │  Actual: 320ms       │
  │  [Gauge chart]       │  [Gauge chart]       │  [Gauge chart]       │
  │                      │                      │                       │
  ├──────────────────────┼──────────────────────┼───────────────────────┤
  │                      │                      │                       │
  │  SLO4: SLA Compliance│  SLO5: Change Success│  SLO6: MTTR P1       │
  │  Target: > 95%       │  Target: > 98%       │  Target: < 30 min    │
  │  Actual: 96.2%       │  Actual: 99.1%       │  Actual: 22 min      │
  │  [Pie chart]         │  [Pie chart]         │  [Bar chart]         │
  │                      │                      │                       │
  └──────────────────────┴──────────────────────┴───────────────────────┘
```

---

## Part 6: SLI Mapping from Prometheus

### 6.1 The Monitoring-to-ITSM Pipeline

In Labs 07A and 12, you deploy a monitoring stack. Here is how SLIs flow from
infrastructure to ServiceNow:

```
  ┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
  │  UPI Service │     │  Prometheus  │     │  AlertManager    │
  │  (Spring     │────►│  (scrapes    │────►│  (evaluates      │
  │   Boot)      │     │   /actuator/ │     │   alert rules,   │
  │              │     │   prometheus)│     │   routes alerts)  │
  └──────────────┘     └──────┬───────┘     └────────┬─────────┘
                              │                       │
                      SLI metrics              Alert fires when
                      collected here           SLI breaches SLO
                                                      │
                                                      ▼
                                              ┌──────────────────┐
                                              │  Snow Bridge     │
                                              │  (Python app,    │
                                              │   receives       │
                                              │   webhook,       │
                                              │   creates        │
                                              │   ServiceNow     │
                                              │   incident via   │
                                              │   REST API)      │
                                              └────────┬─────────┘
                                                       │
                                                       ▼
                                              ┌──────────────────┐
                                              │  ServiceNow      │
                                              │  Incident        │
                                              │  (auto-created,  │
                                              │   SLA clock      │
                                              │   starts         │
                                              │   automatically) │
                                              └──────────────────┘
```

### 6.2 SLI: Transaction Success Rate

**Prometheus metric:**

```promql
# Total requests (all statuses)
http_server_requests_seconds_count

# Failed requests (5xx status codes)
http_server_requests_seconds_count{status=~"5.."}

# Success rate calculation
(
  sum(rate(http_server_requests_seconds_count{status!~"5.."}[5m]))
  /
  sum(rate(http_server_requests_seconds_count[5m]))
) * 100
```

**AlertManager rule (from `alerts.yml`):**

```yaml
- alert: UPITransactionFailureRateHigh
  expr: |
    (
      sum(rate(http_server_requests_seconds_count{status=~"5.."}[5m]))
      /
      sum(rate(http_server_requests_seconds_count[5m]))
    ) * 100 > 0.5
  for: 2m
  labels:
    severity: critical
    service: upi-transaction-service
  annotations:
    summary: "UPI transaction failure rate above 0.5%"
    description: "Transaction success rate SLO (99.5%) is being violated"
```

**What happens when this fires:**

```
  1. Prometheus evaluates rule every 15s
  2. Failure rate exceeds 0.5% for 2 consecutive minutes
  3. Alert transitions to FIRING state
  4. AlertManager receives the alert
  5. AlertManager routes to snow-bridge webhook
  6. Snow Bridge calls ServiceNow REST API:
     POST /api/now/table/incident
     {
       "short_description": "[AUTO] UPI transaction failure rate above 0.5%",
       "priority": "1",
       "assignment_group": "Platform Engineering",
       "cmdb_ci": "<upi-transaction-service CI sys_id>",
       "description": "Transaction success rate SLO (99.5%) is being violated..."
     }
  7. ServiceNow creates incident INC0010XXX
  8. SLA engine evaluates: "Priority = 1 AND State = New" → MATCH
  9. Task SLA record created: P1 Critical Response (30 min clock starts)
  10. Task SLA record created: P1 Critical Resolution (starts when In Progress)
```

### 6.3 SLI: Transaction Latency (P95)

**Prometheus metric:**

```promql
# P95 latency over 5-minute window
histogram_quantile(0.95,
  sum(rate(http_server_requests_seconds_bucket[5m])) by (le)
)
```

**AlertManager rule:**

```yaml
- alert: UPITransactionLatencyHigh
  expr: |
    histogram_quantile(0.95,
      sum(rate(http_server_requests_seconds_bucket[5m])) by (le)
    ) > 0.5
  for: 5m
  labels:
    severity: high
    service: upi-transaction-service
  annotations:
    summary: "UPI P95 latency exceeds 500ms"
    description: "P95 latency SLO (< 500ms) is being violated"
```

### 6.4 SLI: Service Availability

**Prometheus metric:**

```promql
# `up` metric: 1 = target is up, 0 = target is down
up{job="upi-transaction-service"}

# Availability over time
avg_over_time(up{job="upi-transaction-service"}[30d]) * 100
```

**AlertManager rule:**

```yaml
- alert: UPITransactionServiceDown
  expr: up{job="upi-transaction-service"} == 0
  for: 30s
  labels:
    severity: critical
    service: upi-transaction-service
  annotations:
    summary: "UPI Transaction Service is DOWN"
    description: "Availability SLO (99.95%) is at risk"
```

### 6.5 SLI-to-SLO-to-SLA Mapping Table

```
  ┌─────────────────────────┬───────────────────────┬───────────────────────┐
  │  SLI (What we measure)  │  SLO (What we target) │  SLA (What we agree)  │
  ├─────────────────────────┼───────────────────────┼───────────────────────┤
  │  Prometheus `up` metric │  99.95% availability  │  NPCI UPI Support     │
  │                         │  per month            │  Agreement, Section   │
  │                         │                       │  3.1 - Availability   │
  ├─────────────────────────┼───────────────────────┼───────────────────────┤
  │  http_server_requests   │  99.5% success rate   │  Section 3.2 -        │
  │  _seconds_count         │  per day              │  Transaction          │
  │  (success vs total)     │                       │  Reliability          │
  ├─────────────────────────┼───────────────────────┼───────────────────────┤
  │  histogram_quantile     │  P95 < 500ms          │  Section 3.3 -        │
  │  (0.95, ...)            │                       │  Performance          │
  ├─────────────────────────┼───────────────────────┼───────────────────────┤
  │  task_sla.has_breached  │  > 95% SLAs met       │  Section 4.1 -        │
  │  (ServiceNow internal)  │  per month            │  Support Response     │
  ├─────────────────────────┼───────────────────────┼───────────────────────┤
  │  change_request         │  > 98% changes        │  Section 4.2 -        │
  │  .close_code            │  successful           │  Change Management    │
  ├─────────────────────────┼───────────────────────┼───────────────────────┤
  │  incident.business_     │  MTTR < 30 min        │  Section 4.3 -        │
  │  resolve_time (avg)     │  for P1               │  Restoration          │
  └─────────────────────────┴───────────────────────┴───────────────────────┘
```

---

## Part 7: SLA Breach Notifications & Escalation

### 7.1 Notification Strategy

We will configure a tiered notification strategy:

```
  SLA Timeline:
  ════════════════════════════════════════════════════════►
  0%         50%              75%              100% (BREACH)
  │           │                │                │
  │           ▼                ▼                ▼
  │       Notification 1    Notification 2    Notification 3
  │       "SLA Warning"     "SLA Critical"    "SLA BREACHED"
  │       → Assignment      → Group Manager   → VP/Director
  │         Group           + Assignment       + Group Manager
  │                           Group            + Assignment Group
```

### 7.2 Notification 1: SLA at 50% — Warning to Assignment Group

**Navigation:** Service Level Management > SLA > SLA Notifications > **New**

Or configure via SLA workflow. Here we use the SLA notification approach:

**Step 1: Create a Notification**

Navigate to **System Notification > Email > Notifications > New**

| Field | Value |
|---|---|
| **Name** | `NPCI SLA Warning - 50% Elapsed` |
| **Table** | `Task SLA [task_sla]` |
| **Active** | Checked |
| **Send when** | `Record updated` |
| **Conditions** | (see below) |

**Conditions:**

```
  Business percentage  >=  50
  AND
  Business percentage  <   75
  AND
  Stage               is   In Progress
  AND
  SLA Definition.Name  starts with  NPCI UPI
```

**Who will receive:**

| Field | Value |
|---|---|
| **Users/Groups in fields** | `Task.Assignment group` |
| **Send to event creator** | Unchecked |

**Email template:**

Subject: `[SLA WARNING] ${task_sla.sla.name} at ${task_sla.business_percentage}% — ${task_sla.task.number}`

Body:
```
SLA Warning — 50% of time elapsed

Incident: ${task_sla.task.number}
Short Description: ${task_sla.task.short_description}
SLA: ${task_sla.sla.name}
Target Duration: ${task_sla.sla.duration}
Time Remaining: ${task_sla.business_time_left}
Breach Time: ${task_sla.planned_end_time}

Current Assignment Group: ${task_sla.task.assignment_group}
Assigned To: ${task_sla.task.assigned_to}

Action Required: Please prioritize this incident to avoid SLA breach.

View Incident: ${task_sla.task.URI}
```

**Click Save.**

### 7.3 Notification 2: SLA at 75% — Escalation to Manager

**Navigation:** System Notification > Email > Notifications > **New**

| Field | Value |
|---|---|
| **Name** | `NPCI SLA Critical - 75% Elapsed` |
| **Table** | `Task SLA [task_sla]` |
| **Active** | Checked |
| **Send when** | `Record updated` |

**Conditions:**

```
  Business percentage  >=  75
  AND
  Business percentage  <   100
  AND
  Stage               is   In Progress
  AND
  SLA Definition.Name  starts with  NPCI UPI
```

**Who will receive:**

| Field | Value |
|---|---|
| **Users/Groups in fields** | `Task.Assignment group` |
| **Users** | `Sanjay Manager` (IT Management) |

**Email template:**

Subject: `[SLA CRITICAL] ${task_sla.sla.name} at ${task_sla.business_percentage}% — ${task_sla.task.number} — MANAGER ATTENTION NEEDED`

Body:
```
SLA CRITICAL — 75% of time elapsed, breach imminent

MANAGER ACTION REQUIRED

Incident: ${task_sla.task.number}
Short Description: ${task_sla.task.short_description}
Priority: ${task_sla.task.priority}
SLA: ${task_sla.sla.name}
Time Remaining: ${task_sla.business_time_left}
Breach Time: ${task_sla.planned_end_time}

Assignment Group: ${task_sla.task.assignment_group}
Assigned To: ${task_sla.task.assigned_to}

This incident is at risk of breaching its SLA. Please review and
consider additional resources or escalation.

View Incident: ${task_sla.task.URI}
```

**Click Save.**

### 7.4 Notification 3: SLA Breached — Escalation to VP

**Navigation:** System Notification > Email > Notifications > **New**

| Field | Value |
|---|---|
| **Name** | `NPCI SLA BREACHED - VP Notification` |
| **Table** | `Task SLA [task_sla]` |
| **Active** | Checked |
| **Send when** | `Record updated` |

**Conditions:**

```
  Has breached     is   true
  AND
  Stage           is    Breached
  AND
  SLA Definition.Name  starts with  NPCI UPI
```

**Who will receive:**

| Field | Value |
|---|---|
| **Users/Groups in fields** | `Task.Assignment group` |
| **Users** | `Sanjay Manager`, `VP Engineering` (add this user if needed) |

**Email template:**

Subject: `[SLA BREACHED] ${task_sla.sla.name} — ${task_sla.task.number} — IMMEDIATE ACTION REQUIRED`

Body:
```
*** SLA BREACHED ***

Incident: ${task_sla.task.number}
Short Description: ${task_sla.task.short_description}
Priority: ${task_sla.task.priority}
SLA: ${task_sla.sla.name}
Breach Time: ${task_sla.planned_end_time}
Actual Breach Duration: The SLA target has been exceeded.

Assignment Group: ${task_sla.task.assignment_group}
Assigned To: ${task_sla.task.assigned_to}

Business Impact: ${task_sla.task.business_impact}

This SLA has breached. The incident remains open and requires
immediate resolution. This breach will be included in the monthly
SLA compliance report to stakeholders.

View Incident: ${task_sla.task.URI}
```

**Click Save.**

### 7.5 SLA Workflow Escalation (Alternative Approach)

Instead of (or in addition to) notifications, you can use the SLA's built-in
workflow to trigger escalation actions.

**Step 1: Open any SLA Definition** (e.g., NPCI UPI - P1 Critical Resolution)

**Step 2: Click the "SLA Workflow" related link** (or navigate to the Workflow tab)

ServiceNow attaches a default SLA workflow. You can customize it:

```
  SLA Workflow Activities:

  ┌─────────────────┐
  │  SLA Starts      │
  │  (Begin)         │
  └────────┬─────────┘
           │
           ▼
  ┌─────────────────┐     At 50%
  │  Timer: 50%     │────────────────►  Send Warning Email
  └────────┬────────┘                   (to assignment group)
           │
           ▼
  ┌─────────────────┐     At 75%
  │  Timer: 75%     │────────────────►  Send Critical Email
  └────────┬────────┘                   (to manager)
           │                            + Reassign to senior
           ▼
  ┌─────────────────┐     At 100%
  │  SLA Breaches   │────────────────►  Send Breach Email
  └────────┬────────┘                   (to VP)
           │                            + Create escalation task
           ▼                            + Update incident priority
  ┌─────────────────┐
  │  SLA Stops       │
  │  (End)           │
  └──────────────────┘
```

To access the workflow editor:
1. Open the SLA Definition
2. Look for the **Flow** or **Workflow** field
3. Click to open the Workflow Editor
4. Add activities at the appropriate percentage points

> **Note (Zurich):** In Zurich, Flow Designer is the recommended approach
> over legacy Workflow Editor. You can create a Flow that triggers on
> `task_sla` record updates and checks the `business_percentage` field.

---

## Part 8: Test Your SLAs

### 8.1 Create a P1 Incident and Watch the SLA Timer

**Step 1: Create a new P1 incident**

Navigate to **Incident > Create New**

| Field | Value |
|---|---|
| **Caller** | `Priya Sharma` (NOC) |
| **Short description** | `UPI Real-time settlement failure — all banks affected` |
| **Description** | `Multiple member banks reporting settlement failures. Transaction clearing is halted. Estimated 50,000 transactions stuck in pending state.` |
| **Impact** | `1 - High` |
| **Urgency** | `1 - High` |
| **Priority** | (auto-calculates to `1 - Critical`) |
| **Category** | `Software` |
| **Subcategory** | `Operating System` |
| **Assignment Group** | `Platform Engineering` |
| **Configuration Item** | `UPI Settlement Service` (from Lab 07 CMDB) |
| **Business Service** | `UPI Payment Processing` (from Lab 08) |

**Click Save** (do NOT submit yet — stay on the form).

**Step 2: Verify SLA Attached**

1. Scroll down to the **Task SLAs** related list
2. You should see a new Task SLA record:

| Task SLA | SLA Definition | Stage | Start Time | Planned End Time |
|---|---|---|---|---|
| SLA0000001 | NPCI UPI - P1 Critical Response | In Progress | (now) | (now + 30 min) |

The **Resolution SLA** has NOT started yet because the incident is still in
"New" state. The resolution SLA starts when state changes to "In Progress."

**Step 3: Observe the SLA Timer**

1. Click on the Task SLA record (SLA0000001)
2. Note these fields:
   - **Start time:** When the incident was saved
   - **Planned end time:** Start time + 30 minutes
   - **Business elapsed percentage:** Increasing in real-time
   - **Has breached:** false
   - **Stage:** In Progress
3. Look for the **SLA Timeline** visualization (icon near the top of the form)

```
  SLA Timeline Visualization:

  NPCI UPI - P1 Critical Response (30 min)
  ┌────────────────────────────────────────────────────────┐
  │████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
  │  15%                                             100%  │
  │  4.5 min elapsed                   25.5 min remaining  │
  └────────────────────────────────────────────────────────┘
  ██ = elapsed (green)   ░░ = remaining
```

### 8.2 Start the Resolution SLA

**Step 1: Move incident to In Progress**

1. Go back to the incident form
2. Change **State** to `In Progress`
3. Set **Assigned to** to `Ravi Kumar` (Platform Engineering)
4. Click **Save**

**Step 2: Verify**

1. Check the Task SLAs related list
2. You should now see TWO Task SLA records:

| Task SLA | SLA Definition | Stage | Status |
|---|---|---|---|
| SLA0000001 | NPCI UPI - P1 Critical Response | Achieved | Completed within target |
| SLA0000002 | NPCI UPI - P1 Critical Resolution | In Progress | Clock ticking (1 hour) |

The Response SLA has been **Achieved** because the stop condition (State = In
Progress) was met before the 30-minute breach time.

The Resolution SLA has **Started** because its start condition (Priority = 1
AND State = In Progress) is now met.

### 8.3 Pause the SLA

**Step 1: Simulate waiting on customer**

1. On the incident form, change **State** to `Awaiting User Info`
2. Add a **Work note:** "Requested transaction IDs from SBI to investigate settlement failure. Awaiting response."
3. Click **Save**

**Step 2: Verify pause**

1. Open the Resolution Task SLA (SLA0000002)
2. Note:
   - **Stage:** Paused
   - **Pause time:** (current timestamp)
   - The **business elapsed percentage** has stopped increasing
   - The **Planned end time** will be pushed forward by the pause duration

```
  SLA Timeline with Pause:

  NPCI UPI - P1 Critical Resolution (1 hour)
  ┌────────────────────────────────────────────────────────┐
  │██████████████      ════════      ░░░░░░░░░░░░░░░░░░░░│
  │  elapsed      paused (flat)         remaining          │
  │  20 min       (waiting)             40 min             │
  └────────────────────────────────────────────────────────┘
  ██ = elapsed   ════ = paused   ░░ = remaining
```

### 8.4 Resume the SLA

**Step 1: Customer responds**

1. Change **State** back to `In Progress`
2. Add **Work note:** "SBI provided transaction IDs. Resuming investigation."
3. Click **Save**

**Step 2: Verify resume**

1. Open the Resolution Task SLA
2. Note:
   - **Stage:** In Progress (resumed)
   - **Planned end time:** Pushed forward by the duration of the pause
   - Clock is ticking again

### 8.5 Resolve the Incident — SLA Achieved

**Step 1: Resolve the incident**

1. Change **State** to `Resolved`
2. Set **Close code** to `Solved (Permanently)`
3. Set **Close notes:** "Root cause: Settlement batch job had stale database connection pool. Recycled connection pool and reprocessed 50,000 pending transactions. All settlements completed successfully."
4. Click **Save**

**Step 2: Verify SLA outcome**

1. Check the Task SLAs related list:

| Task SLA | SLA Definition | Stage | Has Breached |
|---|---|---|---|
| SLA0000001 | NPCI UPI - P1 Critical Response | Achieved | false |
| SLA0000002 | NPCI UPI - P1 Critical Resolution | Achieved | false |

Both SLAs show **Achieved** — the incident was responded to within 30 minutes
and resolved within 1 hour (excluding pause time).

### 8.6 Test a Breached SLA

To see what a breach looks like:

1. Create a new P3 incident:
   - **Short description:** `UPI QR code generation slow for Axis Bank merchants`
   - **Priority:** `3 - Moderate`
   - **Assignment Group:** `Service Desk`
2. Save it and note the SLA start time
3. Move it to **In Progress** (starts Resolution SLA — 24 business hours)
4. **Wait** (or use the system clock trick below) until the SLA breaches

**System Clock Trick (for testing only):**

In a PDI, you can use a Background Script to simulate time passage:

Navigate to **System Definition > Scripts - Background**

```javascript
// WARNING: ONLY use this in a PDI for testing. NEVER in production.
// This script backdates a Task SLA to simulate a breach.

var taskSLA = new GlideRecord('task_sla');
taskSLA.addQuery('task.number', 'INC0010XXX'); // Replace with your incident number
taskSLA.addQuery('sla.name', 'NPCI UPI - P3 Moderate Resolution');
taskSLA.query();

if (taskSLA.next()) {
    // Set the start time to 48 hours ago to force a breach
    var startTime = new GlideDateTime();
    startTime.addSeconds(-172800); // 48 hours ago
    taskSLA.start_time = startTime;
    taskSLA.update();
    gs.info('Task SLA start time backdated. SLA should now show as breached.');
}
```

After running this script, the SLA engine will recalculate and mark the SLA
as **Breached** because the 24-hour target (in business hours) will have
been exceeded.

---

## Practice Exercises

### Exercise 1: P1 Incident SLA Verification

**Task:** Create a P1 incident and verify SLA auto-attachment.

1. Create a new incident:
   - **Short description:** `UPI Real-time settlement failure — HDFC Bank transactions stuck`
   - **Priority:** 1 - Critical
   - **Assignment Group:** Platform Engineering
   - **CI:** UPI Settlement Service
2. Save and verify the Response SLA (30 min) attaches automatically
3. Move to In Progress within 5 minutes — verify Response SLA shows "Achieved"
4. Verify Resolution SLA (1 hour) starts
5. Resolve within 30 minutes — verify Resolution SLA shows "Achieved"

**Expected outcome:** Both Task SLAs show Stage = Achieved, Has Breached = false.

### Exercise 2: SLA Breach Observation

**Task:** Let a P3 SLA breach and observe the notification.

1. Create a P3 incident:
   - **Short description:** `UPI Collect request timeout for PayTM users`
   - **Priority:** 3 - Moderate
2. Move to In Progress (starts Resolution SLA — 24 business hours)
3. Use the Background Script from section 8.6 to backdate the SLA start time
4. Observe:
   - Task SLA stage changes to "Breached"
   - Breach notification is sent (check System Mailbox: System Logs > Emails)
   - The SLA timer continues past 100% (showing actual breach duration)

**Verification:** Navigate to **System Logs > Emails** (or `sys_email.do`) and
search for emails with subject containing "SLA BREACHED."

### Exercise 3: Service Request SLA — Merchant Onboarding

**Task:** Create a custom SLA for Service Requests.

1. Navigate to SLA Definitions > **New**
2. Configure:

| Field | Value |
|---|---|
| **Name** | `NPCI UPI - Merchant Onboarding Fulfillment` |
| **Type** | `SLA` |
| **Table** | `Requested Item [sc_req_item]` |
| **Duration** | `5 Days` |
| **Schedule** | `NPCI Business Hours` |
| **Timezone** | `Asia/Kolkata` |

**Start Conditions:**

```
  State           is  Open
  AND
  Cat Item.Name   is  Request Merchant Onboarding
```

(Note: The Catalog Item "Request Merchant Onboarding" is created in Lab 11.
If you haven't done Lab 11 yet, use any catalog item or skip the Cat Item
condition.)

**Stop Conditions:**

```
  State  is  Closed Complete
```

3. Save the SLA Definition
4. Submit a Service Request for Merchant Onboarding (from the Service Catalog)
5. Verify the 5-day SLA attaches to the Requested Item (RITM)

### Exercise 4: SLA Compliance Report

**Task:** Build a report showing SLA Compliance % by Priority.

1. Navigate to **Reports > Create New**
2. Configure:

| Field | Value |
|---|---|
| **Name** | `NPCI UPI - SLA Compliance by Priority` |
| **Source type** | `Table` |
| **Table** | `Task SLA [task_sla]` |
| **Type** | `Bar chart` |
| **Group by** | `Task.Priority` |
| **Stack by** | `Has breached` |
| **Aggregation** | `Count` |
| **Filter** | `Stage is Achieved OR Stage is Breached` |
| **Filter** | `AND SLA Definition.Name starts with NPCI UPI` |

3. **Run** the report
4. You should see a stacked bar chart showing Achieved vs Breached per priority level

```
  Expected visualization:

  P1 Critical  ████████████████░░
  P2 High      ████████████████████░
  P3 Moderate  ██████████████████████░░░
  P4 Low       █████████████████████████░░

  ████ = Achieved (green)    ░░ = Breached (red)
```

5. Save the report and add it to the SLO Dashboard from Part 5.

### Exercise 5: Calculate MTTR

**Task:** Calculate Mean Time to Restore from resolved incidents.

**Option A: Report**

1. Navigate to **Reports > Create New**
2. Configure:

| Field | Value |
|---|---|
| **Name** | `NPCI UPI - MTTR by Priority` |
| **Source type** | `Table` |
| **Table** | `Incident [incident]` |
| **Type** | `Bar chart` |
| **Group by** | `Priority` |
| **Aggregation** | `Average` |
| **Aggregate field** | `Business resolve time` |
| **Filter** | `State is Resolved AND Resolved IN last 30 days` |

3. Run — shows average resolution time per priority level.

**Option B: Background Script**

Navigate to **System Definition > Scripts - Background** and run:

```javascript
// Calculate MTTR for P1 incidents resolved in the last 30 days
var gr = new GlideRecord('incident');
gr.addQuery('priority', '1');
gr.addQuery('state', '6'); // Resolved
var thirtyDaysAgo = new GlideDateTime();
thirtyDaysAgo.addDaysUTC(-30);
gr.addQuery('resolved_at', '>=', thirtyDaysAgo);
gr.query();

var totalTime = 0;
var count = 0;

while (gr.next()) {
    var created = new GlideDateTime(gr.sys_created_on.toString());
    var resolved = new GlideDateTime(gr.resolved_at.toString());
    var diff = GlideDateTime.subtract(created, resolved);
    var seconds = diff.getNumericValue() / 1000;
    totalTime += seconds;
    count++;
    gs.info('  ' + gr.number + ': ' + Math.round(seconds / 60) + ' minutes');
}

if (count > 0) {
    var mttr = totalTime / count;
    gs.info('');
    gs.info('=== MTTR Report ===');
    gs.info('P1 Incidents Resolved (last 30 days): ' + count);
    gs.info('Average MTTR: ' + Math.round(mttr / 60) + ' minutes');
    gs.info('SLO Target: < 30 minutes');
    gs.info('Status: ' + (mttr / 60 < 30 ? 'MEETING SLO' : 'VIOLATING SLO'));
} else {
    gs.info('No P1 incidents resolved in the last 30 days.');
}
```

---

## Appendix A: Background Script — Create All SLA Definitions

Use this script to create all 7 SLA definitions programmatically. Run it in
**System Definition > Scripts - Background**.

```javascript
// ============================================================================
// NPCI UPI — Create All SLA Definitions
// Run in: System Definition > Scripts - Background
// Prerequisites: Labs 07-08 completed (CMDB CIs and Services exist)
// ============================================================================

(function() {
    'use strict';

    gs.info('=== NPCI UPI SLA Definitions — Creation Script ===');
    gs.info('');

    // -----------------------------------------------------------------------
    // Helper function to create an SLA Definition
    // -----------------------------------------------------------------------
    function createSLADefinition(config) {
        var sla = new GlideRecord('contract_sla');
        sla.initialize();

        sla.name                = config.name;
        sla.collection          = config.table || 'incident';
        sla.duration            = new GlideDuration(config.duration);
        sla.active              = true;
        sla.timezone            = 'Asia/Kolkata';
        sla.retroactive         = config.retroactive || false;

        // Set schedule if specified
        if (config.schedule) {
            var sched = new GlideRecord('cmn_schedule');
            sched.addQuery('name', config.schedule);
            sched.query();
            if (sched.next()) {
                sla.schedule = sched.sys_id;
            } else {
                gs.warn('Schedule not found: ' + config.schedule);
            }
        }

        // Set start condition
        if (config.startCondition) {
            sla.start_condition = config.startCondition;
        }

        // Set stop condition
        if (config.stopCondition) {
            sla.stop_condition = config.stopCondition;
        }

        // Set pause condition
        if (config.pauseCondition) {
            sla.pause_condition = config.pauseCondition;
        }

        var sysId = sla.insert();

        if (sysId) {
            gs.info('  CREATED: ' + config.name + ' (sys_id: ' + sysId + ')');
        } else {
            gs.error('  FAILED: ' + config.name);
        }

        return sysId;
    }

    // -----------------------------------------------------------------------
    // Define all 7 SLA Definitions
    // -----------------------------------------------------------------------
    var slaDefinitions = [

        // 1. P1 Critical — Response (30 minutes)
        {
            name: 'NPCI UPI - P1 Critical Response',
            table: 'incident',
            duration: '0 00:30:00',  // 30 minutes
            schedule: '24x7',
            startCondition: 'priority=1^state=1',      // P1 AND New
            stopCondition:  'state=2^ORstate=6^ORstate=7', // In Progress OR Resolved OR Closed
            pauseCondition: 'state=-5',                 // Awaiting User Info
            retroactive: false
        },

        // 2. P1 Critical — Resolution (1 hour)
        {
            name: 'NPCI UPI - P1 Critical Resolution',
            table: 'incident',
            duration: '0 01:00:00',  // 1 hour
            schedule: '24x7',
            startCondition: 'priority=1^state=2',      // P1 AND In Progress
            stopCondition:  'state=6',                  // Resolved
            pauseCondition: 'state=-5^ORstate=-16',     // Awaiting User Info OR Awaiting Vendor
            retroactive: false
        },

        // 3. P2 High — Response (1 hour)
        {
            name: 'NPCI UPI - P2 High Response',
            table: 'incident',
            duration: '0 01:00:00',  // 1 hour
            schedule: '24x7',
            startCondition: 'priority=2^state=1',      // P2 AND New
            stopCondition:  'state=2^ORstate=6^ORstate=7',
            pauseCondition: 'state=-5',
            retroactive: false
        },

        // 4. P2 High — Resolution (4 hours)
        {
            name: 'NPCI UPI - P2 High Resolution',
            table: 'incident',
            duration: '0 04:00:00',  // 4 hours
            schedule: '24x7',
            startCondition: 'priority=2^state=2',      // P2 AND In Progress
            stopCondition:  'state=6',                  // Resolved
            pauseCondition: 'state=-5^ORstate=-16',
            retroactive: false
        },

        // 5. P3 Moderate — Response (4 hours)
        {
            name: 'NPCI UPI - P3 Moderate Response',
            table: 'incident',
            duration: '0 04:00:00',  // 4 hours
            schedule: 'NPCI Business Hours',
            startCondition: 'priority=3^state=1',      // P3 AND New
            stopCondition:  'state=2^ORstate=6^ORstate=7',
            pauseCondition: 'state=-5',
            retroactive: false
        },

        // 6. P3 Moderate — Resolution (24 hours)
        {
            name: 'NPCI UPI - P3 Moderate Resolution',
            table: 'incident',
            duration: '1 00:00:00',  // 24 hours (1 day)
            schedule: 'NPCI Business Hours',
            startCondition: 'priority=3^state=2',      // P3 AND In Progress
            stopCondition:  'state=6',                  // Resolved
            pauseCondition: 'state=-5^ORstate=-16',
            retroactive: false
        },

        // 7. P4 Low — Resolution (72 hours)
        {
            name: 'NPCI UPI - P4 Low Resolution',
            table: 'incident',
            duration: '3 00:00:00',  // 72 hours (3 days)
            schedule: 'NPCI Business Hours',
            startCondition: 'priority=4^state=2',      // P4 AND In Progress
            stopCondition:  'state=6',                  // Resolved
            pauseCondition: 'state=-5^ORstate=-16',
            retroactive: false
        }
    ];

    // -----------------------------------------------------------------------
    // Create all SLA Definitions
    // -----------------------------------------------------------------------
    gs.info('Creating ' + slaDefinitions.length + ' SLA Definitions...');
    gs.info('');

    for (var i = 0; i < slaDefinitions.length; i++) {
        createSLADefinition(slaDefinitions[i]);
    }

    gs.info('');
    gs.info('=== SLA Definitions creation complete ===');
    gs.info('');
    gs.info('Next steps:');
    gs.info('  1. Verify at: Service Level Management > SLA > SLA Definitions');
    gs.info('  2. Create schedules (NPCI Business Hours) if not already done');
    gs.info('  3. Create a P1 incident to test SLA auto-attachment');
    gs.info('  4. Configure breach notifications (Part 7 of Lab 09)');

})();
```

---

## Appendix B: Background Script — Create Schedules

```javascript
// ============================================================================
// NPCI UPI — Create Custom Schedules
// Run in: System Definition > Scripts - Background
// ============================================================================

(function() {
    'use strict';

    gs.info('=== NPCI UPI Schedules — Creation Script ===');

    // -----------------------------------------------------------------------
    // Helper: Create a schedule with entries
    // -----------------------------------------------------------------------
    function createSchedule(name, timezone, entries) {
        // Check if schedule already exists
        var existing = new GlideRecord('cmn_schedule');
        existing.addQuery('name', name);
        existing.query();
        if (existing.next()) {
            gs.info('  Schedule already exists: ' + name + ' (skipping)');
            return existing.sys_id;
        }

        var sched = new GlideRecord('cmn_schedule');
        sched.initialize();
        sched.name = name;
        sched.time_zone = timezone;
        var schedId = sched.insert();

        if (!schedId) {
            gs.error('  Failed to create schedule: ' + name);
            return null;
        }

        gs.info('  CREATED schedule: ' + name);

        // Add entries
        for (var i = 0; i < entries.length; i++) {
            var entry = new GlideRecord('cmn_schedule_span');
            entry.initialize();
            entry.schedule = schedId;
            entry.name = entries[i].name;
            entry.type = entries[i].type || 'time_range';
            entry.start_date_time = entries[i].start;
            entry.end_date_time = entries[i].end;
            entry.all_day = entries[i].allDay || false;
            entry.repeat_type = entries[i].repeatType || '';
            entry.days_of_week = entries[i].daysOfWeek || '';

            var entryId = entry.insert();
            if (entryId) {
                gs.info('    + Entry: ' + entries[i].name);
            }
        }

        return schedId;
    }

    // -----------------------------------------------------------------------
    // Create NPCI Business Hours (Mon-Sat 8AM-8PM IST)
    // -----------------------------------------------------------------------
    var businessHoursEntries = [];
    var days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];

    for (var d = 0; d < days.length; d++) {
        businessHoursEntries.push({
            name: days[d].charAt(0).toUpperCase() + days[d].slice(1),
            type: 'time_range',
            start: '08:00:00',
            end: '20:00:00',
            daysOfWeek: days[d]
        });
    }

    createSchedule('NPCI Business Hours', 'Asia/Kolkata', businessHoursEntries);

    // -----------------------------------------------------------------------
    // Create NPCI 24x7 Critical Support
    // -----------------------------------------------------------------------
    var allDays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
    var criticalEntries = [];

    for (var c = 0; c < allDays.length; c++) {
        criticalEntries.push({
            name: allDays[c].charAt(0).toUpperCase() + allDays[c].slice(1),
            type: 'time_range',
            start: '00:00:00',
            end: '23:59:59',
            daysOfWeek: allDays[c]
        });
    }

    createSchedule('NPCI 24x7 Critical Support', 'Asia/Kolkata', criticalEntries);

    gs.info('');
    gs.info('=== Schedules creation complete ===');
    gs.info('Verify at: System Scheduler > Schedules');

})();
```

---

## Appendix C: Background Script — Create Notification Rules

```javascript
// ============================================================================
// NPCI UPI — Create SLA Breach Notification Rules
// Run in: System Definition > Scripts - Background
// ============================================================================

(function() {
    'use strict';

    gs.info('=== NPCI UPI SLA Notifications — Creation Script ===');

    function createNotification(config) {
        var notif = new GlideRecord('sysevent_email_action');
        notif.initialize();
        notif.name           = config.name;
        notif.collection     = 'task_sla';
        notif.action_update  = true;
        notif.active         = true;
        notif.condition      = config.condition;
        notif.subject        = config.subject;
        notif.message_html   = config.body;
        notif.recipient_fields = config.recipientFields || '';
        notif.send_self      = false;

        var sysId = notif.insert();
        if (sysId) {
            gs.info('  CREATED notification: ' + config.name);
        } else {
            gs.error('  FAILED notification: ' + config.name);
        }
        return sysId;
    }

    // 50% Warning
    createNotification({
        name: 'NPCI SLA Warning - 50% Elapsed',
        condition: 'business_percentage>=50^business_percentage<75^stage=in_progress^sla.nameSTARTSWITHNPCI UPI',
        subject: '[SLA WARNING] ${sla.name} at ${business_percentage}% — ${task.number}',
        body: '<p>SLA Warning: ${sla.name} is at ${business_percentage}% for incident ${task.number}.</p><p>Time remaining: ${business_time_left}</p>',
        recipientFields: 'task.assignment_group'
    });

    // 75% Critical
    createNotification({
        name: 'NPCI SLA Critical - 75% Elapsed',
        condition: 'business_percentage>=75^business_percentage<100^stage=in_progress^sla.nameSTARTSWITHNPCI UPI',
        subject: '[SLA CRITICAL] ${sla.name} at ${business_percentage}% — ${task.number} — MANAGER ATTENTION',
        body: '<p><strong>SLA CRITICAL:</strong> ${sla.name} is at ${business_percentage}% for incident ${task.number}.</p><p>Breach time: ${planned_end_time}</p><p>Manager action required.</p>',
        recipientFields: 'task.assignment_group'
    });

    // 100% Breached
    createNotification({
        name: 'NPCI SLA BREACHED - VP Notification',
        condition: 'has_breached=true^stage=breached^sla.nameSTARTSWITHNPCI UPI',
        subject: '[SLA BREACHED] ${sla.name} — ${task.number} — IMMEDIATE ACTION',
        body: '<p><strong>*** SLA BREACHED ***</strong></p><p>Incident: ${task.number}</p><p>SLA: ${sla.name}</p><p>Priority: ${task.priority}</p><p>Assignment Group: ${task.assignment_group}</p><p>This breach will appear in the monthly SLA compliance report.</p>',
        recipientFields: 'task.assignment_group'
    });

    gs.info('');
    gs.info('=== Notification creation complete ===');
    gs.info('Verify at: System Notification > Email > Notifications');
    gs.info('Filter by name: NPCI SLA');

})();
```

---

## Appendix D: Quick Reference — SLA Encoded Queries

These encoded queries are useful for reports, dashboards, and list filters:

```
  All active Task SLAs for NPCI:
    sla.nameSTARTSWITHNPCI UPI^stage=in_progress

  All breached SLAs:
    sla.nameSTARTSWITHNPCI UPI^has_breached=true

  P1 SLAs breached in the last 30 days:
    sla.nameSTARTSWITHNPCI UPI^has_breached=true^task.priority=1^end_timeONLast 30 days@javascript:gs.beginningOfLast30Days()@javascript:gs.endOfLast30Days()

  SLA compliance (achieved, not breached):
    sla.nameSTARTSWITHNPCI UPI^stage=achieved^has_breached=false

  Currently at risk (>75% elapsed, not yet breached):
    sla.nameSTARTSWITHNPCI UPI^business_percentage>=75^stage=in_progress

  All Task SLAs grouped by SLA Definition:
    sla.nameSTARTSWITHNPCI UPI^ORDERBYsla
```

---

## Appendix E: Key Tables Reference

| Table | Label | Purpose |
|---|---|---|
| `contract_sla` | SLA Definition | Template defining start/stop/pause/duration |
| `task_sla` | Task SLA | Individual SLA instance attached to a task |
| `cmn_schedule` | Schedule | Defines business hours / 24x7 |
| `cmn_schedule_span` | Schedule Entry | Individual time ranges within a schedule |
| `sysevent_email_action` | Notification | Email notification rules |
| `incident` | Incident | The task table SLAs attach to |
| `sc_req_item` | Requested Item | Service request SLAs attach here |
| `sla_condition_class` | SLA Condition Class | Maps SLA conditions to tables |

---

## Appendix F: Troubleshooting SLAs

### SLA Not Attaching to Incident

```
  Symptom: Created a P1 incident but no Task SLA appears in the related list.

  Checks:
  1. Is the SLA Definition active? (contract_sla.active = true)
  2. Do the start conditions match?
     - Check priority value: 1 = Critical, not "1 - Critical" in condition
     - Check state value: 1 = New (numeric, not label)
  3. Is the SLA table set to "incident"? (contract_sla.collection = incident)
  4. Run the SLA Debug:
     - Navigate to System Diagnostics > SLA Diagnostics
     - Or check system logs: System Logs > All
     - Filter for source = "SLA" or message contains "SLA"
  5. Is the SLA engine running?
     - Navigate to SLA Administration > Properties
     - Verify: com.snc.sla.engine.enabled = true
```

### SLA Shows Wrong Duration

```
  Symptom: P1 Resolution SLA shows planned end time 9 hours from now,
           but duration is set to 1 hour.

  Cause: Schedule mismatch.
  - If the schedule is "8-5 weekdays" and the incident is created at 4 PM Friday,
    the 1-hour SLA will breach at 9 AM Monday (next business hour).
  - For P1 incidents, use 24x7 schedule.

  Fix: Update the SLA Definition's Schedule field to "24x7" for P1/P2.
```

### SLA Not Pausing

```
  Symptom: Changed incident to "Awaiting User Info" but SLA clock keeps ticking.

  Checks:
  1. Verify pause condition matches exactly:
     - State value for "Awaiting User Info" = -5 (check sys_choice table)
  2. Check if pause condition uses the correct field name
  3. Verify the Task SLA stage — it should show "Paused"
  4. Check SLA workflow — is there a custom workflow overriding pause behavior?
```

### Notifications Not Sending

```
  Symptom: SLA breached but no email was sent.

  Checks:
  1. Is email enabled on the PDI?
     - System Properties > Email Properties
     - glide.email.enabled = true (PDIs often have this disabled)
  2. Is the notification active?
  3. Check System Logs > Emails for queued/failed messages
  4. Verify the condition on the notification matches the Task SLA record
  5. Check recipient — is the assignment group populated?
```

---

## Summary

In this lab, you built a complete Service Level Management framework for the
NPCI UPI platform:

```
  What you created:
  ┌────────────────────────────────────────────────────────────────────┐
  │                                                                    │
  │  7 SLA Definitions                                                 │
  │    ├── P1 Critical: 30 min response, 1 hour resolution (24x7)     │
  │    ├── P2 High: 1 hour response, 4 hour resolution (24x7)        │
  │    ├── P3 Moderate: 4 hour response, 24 hour resolution (biz hrs) │
  │    └── P4 Low: 72 hour resolution (biz hrs)                       │
  │                                                                    │
  │  2 Custom Schedules                                                │
  │    ├── NPCI 24x7 Critical Support                                  │
  │    └── NPCI Business Hours (Mon-Sat 8AM-8PM IST)                  │
  │                                                                    │
  │  1 Holiday Schedule                                                │
  │    └── Indian Bank Holidays 2024-2025                              │
  │                                                                    │
  │  6 Service Level Objectives                                        │
  │    ├── Platform Availability: 99.95%                               │
  │    ├── Transaction Success Rate: 99.5%                             │
  │    ├── P95 Latency: < 500ms                                        │
  │    ├── SLA Compliance: > 95%                                       │
  │    ├── Change Success Rate: > 98%                                  │
  │    └── MTTR P1: < 30 minutes                                       │
  │                                                                    │
  │  3 Notification Rules                                              │
  │    ├── 50% elapsed → Assignment Group                              │
  │    ├── 75% elapsed → Manager + Assignment Group                    │
  │    └── 100% breached → VP + Manager + Assignment Group             │
  │                                                                    │
  │  SLI Mapping                                                       │
  │    ├── Prometheus metrics → SLO targets                            │
  │    └── AlertManager → Snow Bridge → ServiceNow → SLA clock        │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘
```

**What connects to what:**

```
  Lab 07 (CMDB)     → CIs are set on incidents → SLAs reference those CIs
  Lab 08 (Services) → Business Service on incident → SLA reports by service
  Lab 09 (THIS LAB) → SLA definitions → auto-attach to incidents
  Lab 10 (KB)       → KB articles referenced during SLA-tracked resolution
  Lab 11 (Catalog)  → Service Request SLAs (Merchant Onboarding)
  Lab 12 (Stack)    → Prometheus SLIs → AlertManager → incidents → SLAs
  Lab 13 (Incident) → Full lifecycle WITH SLA tracking
```

---

**Next Lab:** [Lab 10: Knowledge Management](lab-10-knowledge-management.md) —
Build the knowledge base that supports faster incident resolution (improving
SLA compliance).
