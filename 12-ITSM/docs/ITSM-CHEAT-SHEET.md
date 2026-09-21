# ITSM / ITIL / ServiceNow -- Revision Cheat Sheet

**Domain:** NPCI UPI | **Sections:** 21 (3 Phases) | **Print target:** 2-3 pages

---

## Quick Reference

```
Incident  = Something BROKE         --> restore ASAP          --> INC
Problem   = WHY it broke            --> prevent recurrence     --> PRB
Change    = Planned modification    --> controlled deployment  --> CHG
Request   = User NEEDS something    --> fulfill it             --> REQ/RITM/SCTASK
SLA       = What you PROMISE (contract, penalties)
SLO       = What you TARGET (internal, stricter than SLA)
SLI       = What you MEASURE (actual metric right now)
CMDB      = Map of every CI and their relationships
CI        = Any managed component (server, app, doc, network)
```

---

## Phase 1: ITSM Terminology (Sections 0-10)

| # | Concept | One-liner | UPI Example |
|---|---------|-----------|-------------|
| 0 | **ITSM** | Managing IT as a *service*, not just technology | NPCI delivers "payment processing" not "servers" |
| 1 | **Service / IT Service** | Value delivered to consumers without them owning the cost/risk | Banks use UPI infra without managing it |
| 2 | **Incident** | Unplanned interruption -- restore ASAP, don't investigate | Axis Bank txn success drops to 34% -- reroute traffic |
| 3 | **Problem** | Unknown root cause of incidents -- prevent recurrence (5 Whys, RCA) | Axis deployed upgrade without telling NPCI -- add change protocol |
| 4 | **Change** | Controlled add/modify/remove to IT services (Standard/Normal/Emergency) | Upgrade Txn Engine v4.1 to v4.2 via CAB-approved Normal change |
| 5 | **Service Request** | Formal ask for something (not a break) | "Give me production log access" |
| 6 | **Service Catalog** | Menu of all available services with SLAs and request forms | Portal: Bank Onboarding, Prod Access, VPN Reset |
| 7 | **CMDB** | Database of CIs + relationships ("Google Maps for IT") | Server -> Txn Engine -> Kafka -> Oracle DB dependency chain |
| 8 | **SLA/SLO/SLI** | Promise vs Target vs Measurement | SLA 99.5% (penalty) > SLO 99.9% (internal) > SLI 99.94% (actual) |
| 9 | **Knowledge Mgmt** | Capture + share so problems aren't solved twice | Runbook: "Settlement engine stuck -- restart consumer group" |
| 10 | **Continual Improvement** | Never done, always improving (PDCA cycle) | Reduce P1 MTTR from 30 min to 15 min over 2 quarters |

---

## Priority Matrix (Impact x Urgency)

```
                 High Urgency     Low Urgency
High Impact  -->  P1 (Critical)    P2 (High)
Low Impact   -->  P3 (Medium)      P4 (Low)
```

| Priority | Response Target | Resolution Target | UPI Example |
|----------|----------------|-------------------|-------------|
| P1 | 2 min | 30 min | UPI completely down |
| P2 | 15 min | 4 hours | Success rate at 85% |
| P3 | 1 hour | 24 hours | One bank's txns failing |
| P4 | 4 hours | 72 hours | "My VPA not working" |

---

## Key Metrics

| Metric | Full Name | Meaning | Typical Target |
|--------|-----------|---------|----------------|
| **MTTA** | Mean Time to Acknowledge | How fast we respond | P1: < 2 min |
| **MTTR** | Mean Time to Resolve | How fast we fix | P1: < 30 min |
| **MTBF** | Mean Time Between Failures | Reliability indicator | Higher = better |
| **RTO** | Recovery Time Objective | Max tolerable downtime | 15 min for UPI core |
| **RPO** | Recovery Point Objective | Max tolerable data loss | 0 for transactions |

### Uptime Translation

| Uptime | Downtime/month | UPI Impact |
|--------|---------------|------------|
| 99% | 7h 18m | ~150 Cr failed txns |
| 99.9% | 43m 50s | ~15 Cr failed txns |
| 99.99% | 4m 23s | ~1.5 Cr failed txns |

---

## Phase 2: ITIL 4 Framework (Sections 11-16)

### 7 Guiding Principles

| # | Principle | In Practice (UPI) |
|---|-----------|-------------------|
| 1 | **Focus on value** | Send exception-based reports, not 47 daily reports nobody reads |
| 2 | **Start where you are** | Import existing 70%-accurate spreadsheet into CMDB, fix the 30% |
| 3 | **Progress iteratively with feedback** | UPI launched with 21 banks, iterated to 400+ |
| 4 | **Collaborate and promote visibility** | Break silos -- NOC + Dev + Bank ops on shared dashboards |
| 5 | **Think and work holistically** | A Kafka change affects Txn Engine, Settlement, AND monitoring |
| 6 | **Keep it simple and practical** | 3-step approval for standard changes, not 12-step bureaucracy |
| 7 | **Optimize and automate** | Auto-create P1 incidents from monitoring alerts, auto-assign |

### Service Value System (SVS)

```
+--------------------------------------------------------------------+
|                    Service Value System                              |
|                                                                      |
|  Opportunity/  +-------------------------------+                     |
|  Demand ------>|    Service Value Chain         |------> VALUE       |
|                +-------------------------------+                     |
|                                                                      |
|  Governed by: Governance | Guiding Principles                       |
|  Enabled by:  34 Practices | Continual Improvement                  |
+--------------------------------------------------------------------+
```

### Service Value Chain -- 6 Activities

```
PLAN --> shared vision, direction, resource allocation
IMPROVE --> continual improvement across ALL activities
ENGAGE --> understand stakeholder needs, maintain relationships
DESIGN & TRANSITION --> meet specs, get into production smoothly
OBTAIN/BUILD --> acquire or build components
DELIVER & SUPPORT --> day-to-day operations, meet SLAs
```

Not linear -- different value streams take different paths through these activities.

### 34 Practices (grouped)

| Category | Count | Practices |
|----------|-------|-----------|
| **General Management** | 14 | Architecture, Continual Improvement, InfoSec, Knowledge, Measurement & Reporting, Org Change, Portfolio, Project, Relationship, Risk, Service Financial, Strategy, Supplier, Workforce & Talent |
| **Service Management** | 17 | Availability, Business Analysis, Capacity & Performance, Change Enablement, Incident, IT Asset, Monitoring & Event, Problem, Release, Service Catalog, Service Config (CMDB), Service Continuity, Service Design, Service Desk, Service Level, Service Request, Service Validation & Testing |
| **Technical Management** | 3 | Deployment, Infrastructure & Platform, Software Dev & Mgmt |

---

## Phase 3: ServiceNow (Sections 17-21)

### Key Tables & Prefixes

| Table | Stores | Ticket Prefix |
|-------|--------|---------------|
| `incident` | Incidents | INC |
| `problem` | Problems | PRB |
| `change_request` | Changes | CHG |
| `sc_request` | Requests (cart) | REQ |
| `sc_req_item` | Request items | RITM |
| `sc_task` | Fulfillment tasks | SCTASK |
| `cmdb_ci` | Configuration items | -- |
| `kb_knowledge` | Knowledge articles | KB |
| `sys_user` | Users | -- |
| `sys_user_group` | Groups | -- |
| `sla_definition` | SLA definitions | -- |

### Core Roles

| Role | Grants |
|------|--------|
| `itil` | Create/edit incidents, problems, changes, KB articles |
| `admin` | Full system configuration |
| `catalog_admin` | Manage service catalog items |
| `knowledge_admin` | Manage KB articles and categories |
| `sn_change_mgr` | Approve/reject changes |
| `approver_user` | Approve requests and changes |

### Change Workflow States

```
New --> Assess --> Authorize --> Scheduled --> Implement --> Review --> Closed
               |  (CAB rejects)              | (failed)
               v                             v
          Assess again                  Closed (failed)
```

| Type | Risk | Approval | Example |
|------|------|----------|---------|
| Standard | Low, pre-approved | No CAB | Add new merchant |
| Normal | Medium-High | CAB required | Upgrade Txn Engine |
| Emergency | Critical (live incident) | Fast-track, post-approval | Midnight hotfix |

### Service Request Flow: REQ --> RITM --> SCTASK

```
User clicks "Order Now"
       |
  REQ (Request) -------- the shopping cart
       |
  RITM (Request Item) -- one specific item, goes through approval
       |
  SCTASK (Catalog Task) - fulfillment work assigned to a team
```

One REQ can have multiple RITMs. Each RITM can generate multiple SCTASKs.

### SLA Timer in ServiceNow

```
SLA Definition = timer with conditions:
  START:  priority=1 AND state=In Progress
  PAUSE:  state=Awaiting User Info
  STOP:   state=Resolved OR Closed
  RESET:  priority changes away from P1
```

**Percentage stages:**

| % Elapsed | Action | Color |
|-----------|--------|-------|
| 0-50% | Normal | GREEN |
| 50-75% | Warning notification | YELLOW |
| 75-100% | Escalate to manager, reassign to L3 | RED |
| >100% | BREACHED -- notify VP, SLA marked failed | BLACK |

**Schedule types:** 24x7 (P1), Business Hours Mon-Fri 9-6 (requests), Extended Mon-Sat 8-8 (P2/P3)

---

## Connections Map

```
                         MONITORING
                             |
                        detects event
                             |
                             v
  Known Error <---- INCIDENT ----triggers----> SLA Timer
  (from Problem)    (restore service)              |
       |                 |                    breach? escalate
       |          unresolved / recurring
       |                 |
       v                 v
   KNOWLEDGE        PROBLEM (RCA)
   (runbooks)            |
                    root cause found
                         |
                         v
    SERVICE          CHANGE (fix)
    CATALOG              |
       |           needs new CI?
       |                 |
       v                 v
   REQUEST           CMDB (update)
   (REQ/RITM/            |
    SCTASK)          all feeds into
                         |
                         v
                CONTINUAL IMPROVEMENT
                   (PDCA cycle)
```

---

## Incident vs Problem vs Change -- The Trilogy

```
INCIDENT:  "The house is on fire!"        --> grab extinguisher (restore)
PROBLEM:   "Why did it catch fire?"        --> faulty wiring found (RCA)
CHANGE:    "Rewire the house properly"     --> planned, approved, tested (prevent)
```

---

## PDCA (Deming Cycle)

```
PLAN  --> What to improve, set target
DO    --> Implement (small scale first)
CHECK --> Did it work? Measure.
ACT   --> Standardize if yes, adjust if no. Repeat.
```

---

*21 sections. 3 phases. 1 domain. Zero excuses.*
