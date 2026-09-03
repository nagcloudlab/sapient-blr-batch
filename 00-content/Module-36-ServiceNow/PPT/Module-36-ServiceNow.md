# ServiceNow
## Module 36 | Sustain Engineering Training | Days 43-44

---

## Agenda -- Day 43

| # | Topic |
|---|-------|
| 01 | ServiceNow Introduction & Architecture |
| 02 | Instance Types & Navigator |
| 03 | Applications & Modules |
| 04 | Forms, Lists & Tables |
| 05 | System Administration Overview |
| 06 | Users, Groups & Roles |
| 07 | Tables Administration |
| 08 | Auditing & System Logs |
| 09 | Data Recovery & Backup |
| 10 | Lab: ServiceNow Configuration |
| 11 | Hands-on: Navigate ServiceNow PDI |
| 12 | Day 43 Wrap-up |

---

## Agenda -- Day 44

| # | Topic |
|---|-------|
| 01 | Change Management in ServiceNow |
| 02 | Workflows & Flow Designer |
| 03 | Service Catalog Overview |
| 04 | Catalog Items, Categories & Variables |
| 05 | SLA Definitions & Triggers |
| 06 | Schedules, Templates & Events |
| 07 | Email Notifications |
| 08 | ITSM + ServiceNow MCQ Assessment |
| 09 | ITSM Role Play (90 min, 2 rounds) |
| 10 | Role Play Debrief |
| 11 | Module Wrap-up |

---

## ServiceNow: Introduction

### What is ServiceNow?

**ServiceNow** is a cloud-based platform that provides IT Service Management (ITSM) and business process automation.

```
┌──────────────────────────────────────────────────────┐
│              ServiceNow Platform                     │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │            Now Platform                       │   │
│  │                                              │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌───────┐ │   │
│  │  │  ITSM  │ │  ITOM  │ │  ITAM  │ │  HR   │ │   │
│  │  │        │ │        │ │        │ │Service│ │   │
│  │  └────────┘ └────────┘ └────────┘ └───────┘ │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌───────┐ │   │
│  │  │  CSM   │ │SecOps  │ │  GRC   │ │  App  │ │   │
│  │  │        │ │        │ │        │ │Engine │ │   │
│  │  └────────┘ └────────┘ └────────┘ └───────┘ │   │
│  │                                              │   │
│  │  Single Data Model | Workflow Engine | AI    │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Cloud-based | Multi-tenant | Bi-annual releases     │
└──────────────────────────────────────────────────────┘
```

---

## ServiceNow Architecture

### Technical Stack

```
┌──────────────────────────────────────────────────────┐
│                  Users                               │
│    Browser | Mobile | API | Chat | Email             │
└──────────────────┬───────────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────────┐
│              Application Layer                       │
│  ITSM | ITOM | CSM | HR | Custom Apps               │
├──────────────────────────────────────────────────────┤
│              Platform Layer                          │
│  Flow Designer | Service Portal | Reporting          │
│  Integration Hub | AI/ML | Performance Analytics     │
├──────────────────────────────────────────────────────┤
│              Data Layer                              │
│  Single System of Record (CMDB)                      │
│  Tables | Forms | Business Rules | ACLs              │
├──────────────────────────────────────────────────────┤
│              Infrastructure                          │
│  Cloud-hosted | Multi-instance | High Availability   │
└──────────────────────────────────────────────────────┘
```

**Key concept:** Everything in ServiceNow is stored in **tables**. Incidents, users, CIs, changes -- all tables.

---

## Instance Types

### ServiceNow Instances

| Instance Type | Purpose | URL Pattern |
|--------------|---------|-------------|
| **Production** | Live environment for end users | `company.service-now.com` |
| **Sub-production** | Testing and staging | `companytest.service-now.com` |
| **Development** | Building and customizing | `companydev.service-now.com` |
| **PDI (Personal Developer)** | Free learning instance | `devXXXXX.service-now.com` |

```
Development ──> Sub-production ──> Production
  (build)        (test/UAT)        (live)

  Update Sets move changes between instances:
  ┌─────────┐  Export   ┌─────────┐  Preview   ┌──────────┐
  │   Dev   │ ────────> │  Test   │ ─────────> │   Prod   │
  │Instance │  XML file │Instance │  Commit    │ Instance │
  └─────────┘           └─────────┘            └──────────┘
```

---

## ServiceNow Navigator

### Finding Your Way Around

```
┌──────────────────────────────────────────────────────┐
│  ServiceNow Interface                                │
│                                                      │
│  ┌──────────────┐  ┌──────────────────────────────┐ │
│  │  Application  │  │  Content Frame               │ │
│  │  Navigator    │  │                              │ │
│  │               │  │  ┌────────────────────────┐  │ │
│  │  Filter: ___  │  │  │  Form / List / Report  │  │ │
│  │               │  │  │                        │  │ │
│  │  > Incident   │  │  │  (Selected module      │  │ │
│  │    > Create   │  │  │   content appears      │  │ │
│  │    > Open     │  │  │   here)                │  │ │
│  │    > All      │  │  │                        │  │ │
│  │               │  │  └────────────────────────┘  │ │
│  │  > Change     │  │                              │ │
│  │  > Problem    │  │  ┌────────────────────────┐  │ │
│  │  > CMDB       │  │  │  Banner / Header       │  │ │
│  │  > Catalog    │  │  │  (User menu, search,   │  │ │
│  │               │  │  │   notifications)       │  │ │
│  │  > System     │  │  └────────────────────────┘  │ │
│  │    Admin      │  │                              │ │
│  └──────────────┘  └──────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

**Tip:** Type in the Filter Navigator to find any module. Example: typing "incident" shows all incident-related modules.

---

## Applications & Modules

### Key ITSM Applications

| Application | Modules | FoodExpress Use |
|------------|---------|-----------------|
| **Incident** | Create New, Open, All, Resolved | Track production incidents |
| **Problem** | Create New, Open, Known Errors | Root cause analysis |
| **Change** | Create New, Open, CAB Workbench | Manage code deployments |
| **Service Catalog** | Browse, Cart, Requests | Employee self-service |
| **CMDB** | CI List, Relationships, Health | Track infrastructure |
| **Knowledge** | Articles, Search, Create | Runbooks and documentation |
| **SLA** | Definitions, Schedules, Breached | Monitor SLA compliance |
| **Reports** | Create, View, Schedule | Management dashboards |

### Navigating Modules

```
Application: Incident Management
├── Module: Create New          (opens blank form)
├── Module: Open                (list of open incidents)
├── Module: All                 (all incidents, any state)
├── Module: Resolved            (resolved, pending closure)
└── Module: Overview            (dashboard/stats)
```

---

## Forms, Lists & Tables

### The Three Core UI Elements

```
┌──────────────────────────────────────────────────────┐
│  TABLE: incident (sys_class_name)                    │
│  Contains all incident records                       │
│                                                      │
│  LIST VIEW (shows multiple records):                 │
│  ┌────────┬──────────────┬──────────┬────────────┐  │
│  │ Number │ Short Desc   │ Priority │ State      │  │
│  ├────────┼──────────────┼──────────┼────────────┤  │
│  │INC0001 │ Payment 503  │ P1       │ In Progress│  │
│  │INC0002 │ Menu slow    │ P3       │ Open       │  │
│  │INC0003 │ Login fail   │ P2       │ Resolved   │  │
│  └────────┴──────────────┴──────────┴────────────┘  │
│                                                      │
│  FORM VIEW (shows single record):                    │
│  ┌──────────────────────────────────────────────┐   │
│  │  Incident: INC0001                           │   │
│  │                                              │   │
│  │  Number:      INC0001                        │   │
│  │  Caller:      Priya Sharma                   │   │
│  │  Category:    Application                    │   │
│  │  Priority:    1 - Critical                   │   │
│  │  State:       In Progress                    │   │
│  │  Assignment:  Platform Engineering           │   │
│  │  Short Desc:  Payment service 503 errors     │   │
│  │                                              │   │
│  │  [Work Notes]  [Additional Comments]         │   │
│  │  [Activities]  [Related Records]             │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

---

## System Administration

### Key Admin Tasks

| Task | Navigation | Description |
|------|-----------|-------------|
| **System Properties** | System Properties > All | Global configuration settings |
| **Email Config** | System Notification > Email | Inbound/outbound email setup |
| **Update Sets** | System Update Sets > Local | Track and move customizations |
| **Scheduled Jobs** | System Definition > Scheduled Jobs | Automated recurring tasks |
| **System Logs** | System Logs > All | Debug and troubleshoot |
| **Performance** | System Diagnostics > Stats | Monitor instance performance |

```
┌──────────────────────────────────────────────────────┐
│  System Administration Best Practices               │
│                                                      │
│  1. Always work in an Update Set (never "Default")  │
│  2. Test changes in sub-production before prod      │
│  3. Document all customizations                      │
│  4. Follow naming conventions (u_ prefix for custom)│
│  5. Use ACLs for security, not client scripts       │
│  6. Minimize business rules on insert/update        │
│  7. Regular instance health checks                   │
└──────────────────────────────────────────────────────┘
```

---

## Users, Groups & Roles

### Access Control Model

```
┌──────────────────────────────────────────────────────┐
│            ServiceNow Access Model                   │
│                                                      │
│  USER ──── belongs to ────> GROUP                    │
│    │                          │                      │
│    │                          │                      │
│    └── has ──> ROLE           └── has ──> ROLE       │
│                 │                          │         │
│                 ▼                          ▼         │
│            ACCESS (via ACLs)                         │
│                                                      │
│  Example:                                            │
│  User: ravi.kumar@foodexpress.in                    │
│  ├── Group: Platform Engineering                    │
│  │   └── Role: itil (can work incidents, changes)   │
│  ├── Group: Change Advisory Board                   │
│  │   └── Role: change_manager                       │
│  └── Direct Role: sn_incident_write                 │
└──────────────────────────────────────────────────────┘
```

### Key Roles

| Role | Access | FoodExpress User |
|------|--------|-----------------|
| `admin` | Full system access | ServiceNow Admin |
| `itil` | Work ITSM records | Sustain Engineers |
| `change_manager` | Approve changes, CAB | Engineering Leads |
| `catalog_admin` | Manage service catalog | IT Ops Manager |
| `knowledge_admin` | Manage knowledge base | Documentation Lead |
| `sn_customerservice_agent` | Customer service module | Support Team |

---

## Tables Administration

### Understanding ServiceNow Tables

```
┌──────────────────────────────────────────────────────┐
│  Table Hierarchy (Inheritance)                       │
│                                                      │
│  task (base table)                                   │
│  ├── incident                                       │
│  ├── problem                                        │
│  ├── change_request                                 │
│  ├── sc_request (service request)                   │
│  │   └── sc_req_item (request item)                │
│  ├── kb_knowledge (knowledge article)               │
│  └── sc_task (catalog task)                         │
│                                                      │
│  cmdb_ci (base CI table)                            │
│  ├── cmdb_ci_computer                               │
│  ├── cmdb_ci_server                                 │
│  ├── cmdb_ci_app_server                             │
│  ├── cmdb_ci_service                                │
│  └── cmdb_ci_kubernetes_cluster                     │
│                                                      │
│  sys_user (users)                                    │
│  sys_user_group (groups)                             │
│  sys_user_role (roles)                               │
└──────────────────────────────────────────────────────┘
```

### Custom Tables for FoodExpress

```
u_foodexpress_service (extends cmdb_ci_service)
├── u_service_tier (Choice: Tier1, Tier2, Tier3)
├── u_oncall_group (Reference: sys_user_group)
├── u_pagerduty_id (String)
└── u_grafana_dashboard_url (URL)
```

---

## Auditing & System Logs

### Tracking Changes and Activity

| Log Type | Table | What It Tracks |
|----------|-------|---------------|
| **Audit Log** | sys_audit | Field-level changes on records |
| **System Log** | syslog | System events, errors, warnings |
| **Transaction Log** | syslog_transaction | HTTP transactions, performance |
| **Email Log** | sys_email | All email activity |
| **Import Log** | sys_import_log | Data import results |
| **Login History** | sysevent_login | User login/logout events |

### Audit Configuration

```
Navigate: System Definition > Audit

FoodExpress Audit Settings:
┌──────────────────────────────────────────┐
│  Tables to Audit:                        │
│  ✓ incident (all fields)                │
│  ✓ change_request (all fields)          │
│  ✓ problem (all fields)                 │
│  ✓ cmdb_ci (key fields only)            │
│  ✓ sys_user (role changes)              │
│                                          │
│  Audit Retention: 365 days              │
│  Audit Deletions: Yes                    │
│  Audit Reads: No (performance impact)    │
└──────────────────────────────────────────┘
```

---

## Data Recovery & Backup

### Protecting ServiceNow Data

```
┌──────────────────────────────────────────────────────┐
│           Data Recovery Options                      │
│                                                      │
│  1. TABLE ROLLBACK                                   │
│     System Definition > Table Rollback              │
│     Roll back a table to a specific point in time    │
│     Requires: admin role + audit enabled on table    │
│                                                      │
│  2. RECORD RESTORE                                   │
│     Right-click record > Audit > Restore previous   │
│     Restore individual record to previous state      │
│                                                      │
│  3. EXPORT / IMPORT                                  │
│     System Import > Export > Export to XML           │
│     Manual backup and restore of data sets           │
│                                                      │
│  4. INSTANCE CLONE                                   │
│     Admin > Clone > Request Clone                   │
│     Copy production instance to sub-prod             │
│     (Managed by ServiceNow -- request via HI)       │
│                                                      │
│  5. UPDATE SETS                                      │
│     Capture and rollback configuration changes       │
│     Can "back out" an update set                     │
└──────────────────────────────────────────────────────┘
```

---

## Change Management in ServiceNow

### Change Request Workflow

```
┌──────────────────────────────────────────────────────┐
│         Change Request Lifecycle                     │
│                                                      │
│  New ──> Assess ──> Authorize ──> Scheduled          │
│                      │                │              │
│                   CAB Review     Implement            │
│                      │                │              │
│                   Approved?      Review              │
│                   /     \            │               │
│                 Yes      No      Closed              │
│                  │        │                          │
│              Schedule   Canceled                     │
│                                                      │
│  Change Types in ServiceNow:                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ Standard │ │  Normal  │ │Emergency │            │
│  │          │ │          │ │          │            │
│  │Pre-auth'd│ │ CAB      │ │ ECAB     │            │
│  │Template  │ │ approval │ │ retrosp. │            │
│  │Auto-close│ │ schedule │ │ approval │            │
│  └──────────┘ └──────────┘ └──────────┘            │
└──────────────────────────────────────────────────────┘
```

---

## Workflows & Flow Designer

### Automating Processes

```
┌──────────────────────────────────────────────────────┐
│  Legacy Workflow vs Flow Designer                    │
│                                                      │
│  WORKFLOW ENGINE (legacy)                            │
│  ├── Visual drag-and-drop workflow                  │
│  ├── Tied to specific tables                        │
│  ├── Activities: Approvals, Notifications, Tasks    │
│  └── Being replaced by Flow Designer                │
│                                                      │
│  FLOW DESIGNER (modern)                              │
│  ├── No-code / low-code automation                  │
│  ├── Triggers: Record created/updated, schedule     │
│  ├── Actions: Update record, email, REST call       │
│  ├── Subflows: Reusable process blocks              │
│  └── Integration Hub: Connect external systems      │
└──────────────────────────────────────────────────────┘
```

### FoodExpress Flow: Auto-assign P1 Incidents

```
Trigger: Incident created with Priority = 1
  │
  ├── Action: Set assignment_group = "Platform Engineering"
  ├── Action: Send PagerDuty notification
  ├── Action: Post to Slack #foodexpress-p1
  ├── Action: Create conference bridge link
  └── Action: Notify VP Engineering via email
```

---

## Service Catalog

### Self-Service Portal

```
┌──────────────────────────────────────────────────────┐
│  FoodExpress Service Catalog                         │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  Categories                                    │  │
│  │                                                │  │
│  │  [Access & Permissions]  [Infrastructure]      │  │
│  │  [Development Tools]     [Monitoring]          │  │
│  │  [Onboarding]            [General IT]          │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Popular Items:                                      │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │
│  │ Request      │ │ New          │ │ VPN        │  │
│  │ Grafana      │ │ Namespace    │ │ Access     │  │
│  │ Access       │ │ Request      │ │ Request    │  │
│  │              │ │              │ │            │  │
│  │ [Order Now]  │ │ [Order Now]  │ │ [Order Now]│  │
│  └──────────────┘ └──────────────┘ └────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## Catalog Items, Categories & Variables

### Anatomy of a Catalog Item

```
┌──────────────────────────────────────────────────────┐
│  Catalog Item: "Request Grafana Dashboard Access"    │
│                                                      │
│  Category:     Access & Permissions                  │
│  Price:        $0 (internal service)                 │
│  Fulfillment:  Automated (Flow Designer)             │
│  SLA:          4 hours                               │
│  Approval:     Manager approval required             │
│                                                      │
│  Variables (form fields):                            │
│  ┌──────────────────────────────────────────────┐   │
│  │ Employee Name:    [Auto-filled from profile] │   │
│  │ Dashboard:        [Dropdown: Operations |    │   │
│  │                    Payment | Delivery | All]  │   │
│  │ Access Level:     [Read-only | Edit]          │   │
│  │ Justification:    [Text area]                 │   │
│  │ Duration:         [Permanent | 30 days |      │   │
│  │                    90 days]                    │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Workflow:                                           │
│  Submit ──> Manager Approve ──> IT Provision ──>    │
│  Notify User ──> Close                               │
└──────────────────────────────────────────────────────┘
```

### Variable Types

| Type | Example | Use Case |
|------|---------|----------|
| Single Line Text | Employee ID | Short text input |
| Multi Line Text | Justification | Long text input |
| Select Box | Dashboard name | Dropdown choices |
| Reference | Assigned group | Link to another table |
| Checkbox | VPN required? | Boolean toggle |
| Date | Start date | Date picker |
| Attachment | Supporting doc | File upload |

---

## SLA Definitions

### Configuring SLAs in ServiceNow

```
┌──────────────────────────────────────────────────────┐
│  SLA Definition: P1 Incident Resolution              │
│                                                      │
│  Name:           P1 Resolution SLA                   │
│  Table:          incident                            │
│  Duration:       4 hours                             │
│  Schedule:       24x7 (excludes nothing)             │
│                                                      │
│  Start Condition:                                    │
│    Priority = 1 AND State = New                      │
│                                                      │
│  Stop Condition:                                     │
│    State = Resolved OR State = Closed                │
│                                                      │
│  Pause Condition:                                    │
│    State = Pending (waiting for customer)             │
│                                                      │
│  Stages:                                             │
│  ┌────────────────────────────────────────────┐     │
│  │  0%──────25%─────50%──────75%──────100%   │     │
│  │  │  Green  │  Green  │  Yellow │   Red    │     │
│  │  │         │         │ (warn)  │ (breach) │     │
│  │  0h       1h        2h       3h         4h │     │
│  └────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────┘
```

---

## SLA Triggers & Schedules

### How SLAs Are Triggered

```
┌──────────────────────────────────────────────────────┐
│  SLA Trigger Flow                                    │
│                                                      │
│  Incident Created ──> SLA Engine evaluates           │
│      │                    │                          │
│      │              Match Start Condition?           │
│      │              (Priority = 1?)                  │
│      │                /        \                     │
│      │             Yes          No                   │
│      │              │           └── No SLA attached  │
│      │              ▼                                │
│      │         Attach SLA                            │
│      │         Start timer                           │
│      │              │                                │
│      │         Monitor: Has Stop Condition met?      │
│      │              │                                │
│      │         At 75%: Send warning notification     │
│      │         At 100%: Mark as BREACHED             │
│      │              │                                │
│      │         Stop Condition met → Complete SLA     │
└──────────────────────────────────────────────────────┘
```

### Schedule Types

| Schedule | Hours | Used For |
|----------|-------|----------|
| **24x7** | All hours, all days | P1/P2 critical services |
| **Business Hours** | Mon-Fri 09:00-17:00 | P3/P4 standard services |
| **Extended Hours** | Mon-Sat 07:00-22:00 | Important but not critical |
| **Maintenance Window** | Tue/Thu 02:00-06:00 | Planned changes |

---

## Templates & Events

### Record Templates

```
┌──────────────────────────────────────────────────────┐
│  FoodExpress Incident Templates                      │
│                                                      │
│  Template: "Payment Service Outage"                  │
│  ├── Category: Application > Payment                │
│  ├── Assignment Group: Platform Engineering         │
│  ├── Priority: 1 - Critical                        │
│  ├── Impact: 1 - High                              │
│  ├── Urgency: 1 - High                             │
│  ├── Short Description: "Payment service outage -   │
│  │    [describe symptoms]"                          │
│  └── Work Notes: "Check: 1) Payment pod health     │
│       2) Gateway connectivity 3) DB connections"    │
│                                                      │
│  Template: "Deployment Issue"                        │
│  ├── Category: Application > Deployment             │
│  ├── Assignment Group: DevOps                       │
│  ├── Priority: 2 - High                            │
│  └── Short Description: "Deployment issue -         │
│       [service] [version] [environment]"            │
└──────────────────────────────────────────────────────┘
```

### System Events

| Event | Trigger | Action |
|-------|---------|--------|
| `incident.created` | New incident record | Send notification to assignment group |
| `incident.priority.changed` | Priority field updated | Re-evaluate SLA, notify management |
| `sla.breached` | SLA timer reaches 100% | Escalation notification |
| `change.approved` | CAB approves change | Notify implementer, schedule |

---

## Email Notifications

### Configuring ServiceNow Email

```
┌──────────────────────────────────────────────────────┐
│  Email Notification Configuration                    │
│                                                      │
│  Notification: "P1 Incident Created"                 │
│                                                      │
│  When to send:                                       │
│    Table:     incident                               │
│    Event:     incident.created                       │
│    Condition: priority = 1                           │
│                                                      │
│  Who receives:                                       │
│    ☑ Assignment group members                       │
│    ☑ Additional: VP Engineering, On-call manager    │
│    ☐ Caller (not for internal P1 notifications)     │
│                                                      │
│  What it contains:                                   │
│    Subject: "[P1] ${number}: ${short_description}"   │
│    Body:                                             │
│    ┌────────────────────────────────────────────┐   │
│    │ Priority 1 Incident Created                │   │
│    │                                            │   │
│    │ Number: ${number}                          │   │
│    │ Description: ${short_description}          │   │
│    │ Affected Service: ${cmdb_ci}               │   │
│    │ Assignment Group: ${assignment_group}       │   │
│    │ Created: ${sys_created_on}                 │   │
│    │                                            │   │
│    │ [View Incident] [Acknowledge]              │   │
│    └────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

---

## ITSM + ServiceNow: MCQ Topics

### Assessment Coverage

```
┌──────────────────────────────────────────────────────┐
│           MCQ Assessment Structure                   │
│                                                      │
│  Section 1: ITSM Fundamentals (10 questions)        │
│  ├── ITIL 4 guiding principles                      │
│  ├── Service Value System                            │
│  ├── ITSM vs ITIL vs DevOps                         │
│  └── Service lifecycle stages                        │
│                                                      │
│  Section 2: ITIL Practices (15 questions)           │
│  ├── Incident vs Problem vs Change                  │
│  ├── Priority matrix (Impact x Urgency)             │
│  ├── SLA / OLA / UC hierarchy                       │
│  ├── Change types and authorization                 │
│  ├── Problem management techniques (5 Whys)         │
│  └── Service catalog and request management         │
│                                                      │
│  Section 3: ServiceNow (15 questions)               │
│  ├── Navigation and interface                       │
│  ├── Tables and forms                               │
│  ├── Users, groups, roles                           │
│  ├── SLA configuration                              │
│  ├── Workflows and Flow Designer                    │
│  └── Change management workflow                     │
│                                                      │
│  Total: 40 questions | Duration: 60 minutes         │
│  Pass mark: 70% (28/40)                             │
└──────────────────────────────────────────────────────┘
```

---

## ITSM Role Play: Overview

### Simulated Incident Response (90 minutes, 2 rounds)

```
┌──────────────────────────────────────────────────────┐
│           ITSM Role Play Exercise                    │
│                                                      │
│  ROUND 1 (45 min): Major Incident                   │
│                                                      │
│  Scenario: FoodExpress payment service is down.      │
│  Orders are failing. Customer complaints rising.     │
│                                                      │
│  Roles:                                              │
│  ├── Incident Commander (1 person)                  │
│  ├── Technical Lead (1-2 people)                    │
│  ├── Communications Lead (1 person)                 │
│  ├── Service Desk Agent (1 person)                  │
│  └── Business Stakeholder (1 person, played by      │
│       trainer or another team)                       │
│                                                      │
│  ROUND 2 (45 min): Change + Problem                 │
│                                                      │
│  Scenario: Root cause identified. Plan the fix,      │
│  create change request, get CAB approval, deploy.    │
│                                                      │
│  Roles rotate so everyone experiences different      │
│  perspectives.                                       │
└──────────────────────────────────────────────────────┘
```

---

## ITSM Role Play: Round 1 Script

### Major Incident Scenario

```
Time 0:00 -- TRIGGER
  Alert: "PaymentServiceDown" fires in PagerDuty
  Customer complaints in support queue: 15 and rising
  Status page: No update yet

INJECT at 10:00:
  "VP of Engineering is asking for an update on Slack.
   What do you tell them?"

INJECT at 20:00:
  "A journalist tweets: 'Is FoodExpress down? Can't order food.'
   What do you do?"

INJECT at 30:00:
  "Technical Lead has identified the root cause:
   Payment gateway certificate expired.
   What are the next steps?"

INJECT at 40:00:
  "Service is restored. Error rate back to normal.
   What's left to do before closing the incident?"

DEBRIEF (5 min):
  - What went well?
  - What was the biggest challenge?
  - How would you improve the process?
```

---

## ITSM Role Play: Round 2 Script

### Change + Problem Scenario

```
Time 0:00 -- SETUP
  Problem record created: PRB-2026-0030
  "Payment gateway certificates expire without warning"
  Root cause: No certificate monitoring or auto-renewal

TASK 1 (0:00-15:00): Problem Management
  - Complete the problem record
  - Define workaround (manual cert check weekly)
  - Plan permanent fix (auto-renewal + monitoring)

TASK 2 (15:00-30:00): Change Request
  - Create change request for certificate auto-renewal
  - Risk assessment (What if auto-renewal fails?)
  - Implementation plan with test steps
  - Rollback plan

INJECT at 25:00:
  "CAB member asks: 'What if the auto-renewal system
   itself has a bug and installs an invalid certificate?'"

TASK 3 (30:00-40:00): CAB Review
  - Present change to CAB (other teams play CAB members)
  - Answer questions, get approval

DEBRIEF (5 min):
  - Was the change request complete enough?
  - Did the CAB ask the right questions?
```

---

## ServiceNow Best Practices for Sustain Engineers

### Daily Operations

| Activity | ServiceNow Action | Frequency |
|----------|-------------------|-----------|
| Check assigned incidents | Filter: `assigned_to=me AND state!=resolved` | Start of day |
| Review SLA breaches | SLA > Breached | Morning |
| Update work notes | Add investigation notes to incident | During work |
| Link related records | Incident > Related Records tab | As discovered |
| Update CMDB after changes | CMDB > CI form | After deployment |
| Knowledge article | Knowledge > Create New | After resolution |

### Common Pitfalls

```
DO:
  ✓ Always add work notes (not just close with resolution)
  ✓ Link incidents to problems (pattern detection)
  ✓ Use templates for common incident types
  ✓ Set correct priority using Impact x Urgency matrix
  ✓ Update the CMDB after every change

DON'T:
  ✗ Close incidents without root cause
  ✗ Skip the change process for "quick fixes"
  ✗ Create duplicate incidents (search first)
  ✗ Leave SLA breaches unacknowledged
  ✗ Assign incidents to individuals (use groups)
```

---

## ServiceNow: Reporting & Dashboards

### Building Management Reports

```
┌──────────────────────────────────────────────────────┐
│  ServiceNow Report Types                            │
│                                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────────┐  │
│  │    Bar     │ │   Pie      │ │  Time Series   │  │
│  │   Chart    │ │   Chart    │ │    (Trend)     │  │
│  │           │ │            │ │               │  │
│  │ Incidents │ │ By Priority│ │ Monthly MTTR  │  │
│  │ by Group  │ │            │ │ over 6 months │  │
│  └────────────┘ └────────────┘ └────────────────┘  │
│                                                      │
│  ┌────────────┐ ┌────────────┐ ┌────────────────┐  │
│  │   List    │ │  Scorecard │ │   Dial/Gauge   │  │
│  │  Report   │ │            │ │                │  │
│  │           │ │ SLA        │ │ Current SLA    │  │
│  │ Open P1s  │ │ Compliance │ │ Compliance %   │  │
│  └────────────┘ └────────────┘ └────────────────┘  │
│                                                      │
│  Navigate: Reports > Create New                     │
│  Schedule: Daily, Weekly, Monthly auto-generation   │
│  Share: Dashboard, Email, PDF export                │
└──────────────────────────────────────────────────────┘
```

---

## ServiceNow: Integration with Monitoring

### Connecting Observability to ITSM

```
┌──────────────────────────────────────────────────────┐
│     Prometheus/PagerDuty → ServiceNow Integration   │
│                                                      │
│  Prometheus Alert ──> Alertmanager                   │
│         │                  │                         │
│         │            PagerDuty                       │
│         │                  │                         │
│         │            ServiceNow                      │
│         │            (via REST API or                │
│         │             Integration Hub)               │
│         ▼                  ▼                         │
│  ┌──────────────────────────────────────────────┐   │
│  │  Auto-created Incident in ServiceNow         │   │
│  │                                              │   │
│  │  Number: INC0012345                          │   │
│  │  Source: Prometheus/PagerDuty                │   │
│  │  Category: Auto-classified from alert labels │   │
│  │  Priority: Mapped from alert severity        │   │
│  │  Assignment: Based on alert routing rules    │   │
│  │  CI: Auto-linked from alert metadata         │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Benefit: Zero-touch incident creation from         │
│  monitoring alerts                                   │
└──────────────────────────────────────────────────────┘
```

---

## ServiceNow: Knowledge Management

### Building a Knowledge Base for FoodExpress

| Article Type | Example | Audience |
|-------------|---------|----------|
| **Runbook** | "Payment Service 503 Errors" | Sustain Engineers |
| **How-to** | "How to request Grafana access" | All employees |
| **FAQ** | "What is our deployment schedule?" | New team members |
| **Known Error** | "Tuesday payment timeouts (PRB-0025)" | Support + Engineering |
| **Architecture** | "FoodExpress microservices overview" | Engineering |

```
Knowledge Base Structure:
├── Service Desk Knowledge (L1)
│   ├── Common user issues
│   └── Password reset, VPN setup
├── Technical Knowledge (L2/L3)
│   ├── Runbooks (per service)
│   ├── Architecture docs
│   └── Known errors and workarounds
└── Onboarding
    ├── New joiner guides
    └── Tool access setup
```

**Knowledge article lifecycle:** Draft > Review > Published > Retired

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| ServiceNow Platform | Cloud-based ITSM platform; everything is a table; single system of record |
| Instances | Dev > Test > Prod promotion via Update Sets; PDI for learning |
| Navigation | Filter Navigator to find any module; Applications contain Modules |
| Forms/Lists/Tables | Tables store data; Lists show multiple records; Forms show one record |
| Users/Groups/Roles | Users belong to Groups; Roles grant access; ACLs enforce permissions |
| Tables Admin | Task is the base table; incident, problem, change extend it |
| Auditing | Enable audit on key tables; retention policy; sys_audit for field changes |
| Change Management | Standard (pre-auth), Normal (CAB), Emergency (ECAB); follow the 7 Rs |
| Flow Designer | Modern no-code automation; replaces legacy workflows; triggers + actions |
| Service Catalog | Self-service portal; catalog items with variables; approval workflows |
| SLA Definitions | Start/Stop/Pause conditions; schedules; breach notifications at 75% and 100% |
| Email Notifications | Event-driven; configurable recipients, conditions, and templates |
| Role Play | Practice incident response, change management, and communication under pressure |

> **Next: Module 37 -- Final Project + Generative AI**
