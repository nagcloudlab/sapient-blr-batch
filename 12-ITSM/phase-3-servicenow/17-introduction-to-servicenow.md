# Section 17: Introduction to ServiceNow

## What is ServiceNow?

A cloud-based platform that **implements ITSM practices as software**. Everything from Phase 1 and 2 becomes screens, workflows, dashboards, and automation.

Think of it as: **"ITIL is the recipe book. ServiceNow is the kitchen where you cook."**

---

## Overview

| Question | Answer |
|---|---|
| What? | Cloud-based IT service management platform |
| Why? | Automate and manage ITSM processes at scale |
| Who uses it? | 80% of Fortune 500 companies |
| How? | SaaS -- accessed via browser, no installation |
| Pricing? | Per-user licensing, enterprise contracts |

---

## ITSM Concepts -> ServiceNow Modules

| ITSM Concept (Phase 1) | ServiceNow Module | What you see |
|---|---|---|
| Incident Management (Sec 2) | **Incident** | INC forms, priority matrix, escalation rules |
| Problem Management (Sec 3) | **Problem** | PRB records, RCA fields, Known Error DB |
| Change Management (Sec 4) | **Change** | CHG forms, CAB workbench, change calendar |
| Service Request (Sec 5) | **Service Catalog + Request** | REQ forms, approval workflows |
| Service Catalog (Sec 6) | **Service Catalog** | Self-service portal, catalog items |
| CMDB (Sec 7) | **CMDB** | CI records, dependency maps, discovery |
| SLA Management (Sec 8) | **SLA Definitions** | SLA timers, breach alerts |
| Knowledge Base (Sec 9) | **Knowledge** | KB articles, search, article lifecycle |

---

## ServiceNow Architecture

```
+----------------------------------------------------------+
|                    Browser (User)                         |
+---------------------------+------------------------------+
                            |
+---------------------------v------------------------------+
|              ServiceNow Instance                          |
|  +--------------------------------------------------+    |
|  |  Applications                                     |    |
|  |  +----------+ +--------+ +--------+ +----------+ |    |
|  |  | Incident | | Change | | Problem| | Catalog  | |    |
|  |  +----------+ +--------+ +--------+ +----------+ |    |
|  |  +----------+ +--------+ +--------+ +----------+ |    |
|  |  |   CMDB   | |  SLA   | |   KB   | | Reports  | |    |
|  |  +----------+ +--------+ +--------+ +----------+ |    |
|  +--------------------------------------------------+    |
|                                                           |
|  +--------------------------------------------------+    |
|  |  Platform Layer                                    |    |
|  |  Workflow Engine | Forms | Lists | Tables          |    |
|  |  Notifications | Scripting | Integration APIs     |    |
|  +--------------------------------------------------+    |
|                                                           |
|  +--------------------------------------------------+    |
|  |  Database (single data model for everything)       |    |
|  +--------------------------------------------------+    |
+----------------------------------------------------------+
```

**Key insight:** Everything in ServiceNow sits in **one database**. An incident links to a CI in CMDB, which links to a change, which links to a knowledge article. It's all connected -- just like ITIL says it should be.

---

## ServiceNow Instances

| Instance Type | Purpose | UPI Example |
|---|---|---|
| **Production** | Live system used daily | NPCI teams log real incidents here |
| **Sub-Production (Test)** | Testing changes to ServiceNow itself | Test a new workflow before going live |
| **Developer** | Personal sandbox for learning | Free at developer.servicenow.com |
| **Demo** | Pre-configured for demonstrations | Show to management |

**For training:** You'll use a **Personal Developer Instance (PDI)** -- free, full-featured, resets after 10 days of inactivity.

---

## ServiceNow Navigation

```
+------------------------------------------------------------------+
| Banner (top)                                                       |
| [Logo] [All menu] [Favorites] [History] [Search]    [User] [Help] |
+------------------------------------------------------------------+
|                    |                                                |
| Application        |  Content Frame                                |
| Navigator          |  (where forms, lists, dashboards appear)     |
| (left sidebar)     |                                                |
|                    |                                                |
| > Incident         |  +--------------------------------------+    |
|   - Create New     |  | INC0010042                            |    |
|   - All            |  | Caller: HDFC Bank                     |    |
|   - My Incidents   |  | Short desc: Transactions failing      |    |
|                    |  | Priority: P1 - Critical               |    |
| > Problem          |  | State: In Progress                    |    |
|   - Create New     |  | Assigned to: Platform Team            |    |
|   - All            |  | ...                                   |    |
|                    |  +--------------------------------------+    |
| > Change           |                                                |
| > Service Catalog  |                                                |
| > CMDB             |                                                |
| > Knowledge        |                                                |
+------------------------------------------------------------------+
```

---

## Core Building Blocks

| Building Block | What it is | Example |
|---|---|---|
| **Tables** | Store data (like DB tables) | `incident` table, `cmdb_ci` table, `change_request` table |
| **Forms** | UI for one record | Incident form with fields: caller, description, priority |
| **Lists** | UI showing multiple records | All open P1 incidents |
| **Modules** | Menu items in the navigator | "Incident > Create New" |
| **Applications** | Group of modules | "Incident Management" app |

Everything is a **table row**. An incident is a row in the `incident` table. A CI is a row in the `cmdb_ci` table. A change is a row in the `change_request` table. Simple.

---

## UPI Example: Day 1 on ServiceNow at NPCI

```
08:00  Log in to ServiceNow
       Dashboard shows: 3 open P1 incidents, 12 P2, 45 P3

08:05  Click INC0010042: "Axis Bank transactions failing"
       See: timeline, related CIs, linked problems, SLA timer ticking

08:10  Update incident: add work notes "Checking Axis PSP node"
       SLA timer shows: 22 min remaining before SLA breach

08:15  Resolve incident: select resolution code, link KB article
       SLA: MET (resolved in 8 min, SLA was 30 min)

08:20  Check change calendar: Kafka upgrade scheduled for Sunday
       CHG0004521 status: "Approved" -- rollback plan attached

08:25  Open Service Catalog: bank requests TPS increase
       REQ0008834: auto-routed to Platform team, approval pending
```

---

## Key Takeaway

> ServiceNow is not magic -- it's ITSM Phase 1 and Phase 2 turned into software.
> If you understand the concepts, ServiceNow is just the tool.
> If you skip the concepts and just learn ServiceNow buttons, you'll never understand WHY.
>
> **That's why we did Phase 1 and 2 first.**
