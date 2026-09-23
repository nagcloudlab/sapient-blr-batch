# ServiceNow ITSM Labs — Master Curriculum

**Theme:** NPCI UPI Payment Platform | **PDI Version:** Zurich | **Total Labs:** 22 | **Total Duration:** ~40 hours

---

## Curriculum Architecture

```
                    ITIL 4 Service Value System (SVS)
    ════════════════════════════════════════════════════════

    Demand ──►  SERVICE VALUE CHAIN  ──► Value (UPI Payments)
                │                  │
    ┌───────────┼──────────────────┼──────────────┐
    │           │                  │              │
    │   PLAN  ──┤──  DESIGN &    ──┤──  DELIVER  │
    │           │   TRANSITION     │   & SUPPORT  │
    │   Phase 1 │   Phase 2        │   Phase 3    │
    │   Labs    │   Labs           │   Labs       │
    │   01-06   │   07-11          │   12-16      │
    │           │                  │              │
    │           ├── IMPROVE ───────┤              │
    │           │   Phase 4        │              │
    │           │   Labs 17-19     │              │
    │           │                  │              │
    │           ├── OBTAIN/BUILD ──┤              │
    │           │   Phase 5        │              │
    │           │   Labs 20-22     │              │
    └───────────┴──────────────────┴──────────────┘
                         │
              PRACTICES (34 ITIL Practices)
              GOVERNANCE & CONTINUAL IMPROVEMENT
```

---

## Scenario: NPCI UPI Payment Processing Platform

Every lab uses this consistent scenario:

```
Organization:  NPCI (National Payments Corporation of India)
Platform:      UPI (Unified Payments Interface)
Services:
  ├── Business Service: UPI Payment Processing
  │     ├── Technical Service: UPI Transaction Service (Spring Boot, port 8081)
  │     ├── Technical Service: UPI Settlement Service (Spring Boot, port 8082)
  │     ├── Infrastructure: PostgreSQL Database
  │     ├── Infrastructure: Payment Gateway (SSL/TLS)
  │     └── Infrastructure: Load Balancer
  │
  ├── Monitoring Stack:
  │     ├── Prometheus (metrics collection)
  │     ├── Grafana (dashboards)
  │     ├── AlertManager (alert routing)
  │     └── Snow Bridge (alert → ServiceNow incident)
  │
  └── Support Teams:
        ├── Platform Engineering (L2/L3 — Ravi Kumar, Amit Verma)
        ├── NOC (L1 monitoring — Priya Sharma)
        ├── Service Desk (L1 support — Meera Joshi)
        ├── IT Administration (admin — Vijay Admin)
        └── IT Management (approvals — Sanjay Manager)
```

---

## Phase 1: Platform Foundation

> **ITIL Value Chain:** Plan
> **Goal:** Learn ServiceNow platform basics before building anything

| Lab | Title | Duration | ITIL Practice | What You Learn |
|---|---|---|---|---|
| 01 | PDI Setup & First Login | 30 min | — | Get your Personal Developer Instance |
| 02 | Platform Navigation | 30 min | — | Navigator, menus, workspaces, search |
| 03 | Lists & Forms | 45 min | — | List views, form layout, personalization |
| 04 | Users, Groups & Roles | 60 min | — | Create UPI team users, assign roles |
| 05 | Tables & Columns | 60 min | — | Table structure, inheritance, custom tables |
| 06 | Filters, Views & Encoded Queries | 45 min | — | Advanced filtering, saved views, PromQL-style queries |

**Output:** Platform configured with UPI team users, groups, roles, and a custom Server Health Check table.

**Folder:** `phase-1-foundation/`

---

## Phase 2: Build the UPI Service

> **ITIL Value Chain:** Design & Transition
> **Goal:** Define the service in ServiceNow BEFORE operating it — CMDB, SLAs, KB, Catalog

| Lab | Title | Duration | ITIL Practice | What Gets Built |
|---|---|---|---|---|
| **07** | **CMDB & Configuration Management** | 90 min | Service Configuration Mgmt | CIs for all UPI components. Relationships: depends_on, runs_on, used_by. Service Map. CI Classes. Discovery simulation. |
| **08** | **Service Portfolio & Business Services** | 60 min | Service Portfolio Mgmt, Relationship Mgmt | "UPI Payment Processing" Business Service. Technical Services underneath. Service Owner. Support groups. Service-CI mapping. |
| **09** | **SLA, SLO & SLI — Service Level Management** | 90 min | Service Level Mgmt | SLA definitions (P1: 1hr resolve, P2: 4hr). SLOs (99.9% uptime, P95 < 500ms). SLI mapping from Prometheus. SLA breach rules & escalation. |
| **10** | **Knowledge Management** | 60 min | Knowledge Mgmt | KB structure: UPI Operations, Troubleshooting, Onboarding. Articles: UPI error codes, runbooks. Knowledge workflow: draft → review → publish. Templates. |
| **11** | **Service Catalog & Request Management** | 90 min | Service Request Mgmt | Catalog categories: UPI Services. Items: "Request Merchant Onboarding", "Report UPI Issue", "Request API Access". Variables, approval flows. REQ → RITM → SCTASK. |

**Output:** A fully defined UPI service in ServiceNow with CMDB, SLAs, KB, and Service Catalog — ready for operations.

**Folder:** `phase-2-build-service/`

### Dependency Graph (Phase 2)

```
Lab 07: CMDB ──────────┬──► Lab 08: Service Portfolio
  (CIs created)        │        (Services reference CIs)
                       │
                       ├──► Lab 09: SLA/SLO/SLI
                       │        (SLAs attached to services & CIs)
                       │
                       ├──► Lab 10: Knowledge Base
                       │        (KB articles reference CIs & services)
                       │
                       └──► Lab 11: Service Catalog
                                (Catalog items reference CIs & services)
```

---

## Phase 3: Operate the UPI Service

> **ITIL Value Chain:** Deliver & Support
> **Goal:** Run the UPI service with real monitoring, handle incidents/problems/changes with full CMDB & SLA context

| Lab | Title | Duration | ITIL Practice | What Happens |
|---|---|---|---|---|
| **12** | **Deploy UPI Demo Stack & Event Management** | 60 min | Monitoring & Event Mgmt | Deploy Docker Compose stack. Traffic generator. Prometheus + Grafana. Alert → Event → Incident pipeline. Event rules & correlation. |
| **13** | **Incident Management — Full Lifecycle** | 90 min | Incident Mgmt | Chaos injection → auto-incident WITH CI attached, SLA clock starts, KB suggested. Assignment rules. Escalation (L1→L2→L3). Major incident. SLA tracking. |
| **14** | **Problem Management — RCA to Known Error** | 75 min | Problem Mgmt | Create problem from recurring incidents. RCA using CMDB impact map. Known Error → KB article. Problem → Change Request. |
| **15** | **Change Management — Plan to Deploy** | 90 min | Change Enablement | Normal/Standard/Emergency changes. CI impact analysis from CMDB. CAB approval. Change Calendar. Conflict detection. Failed change + rollback. |
| **16** | **Release & Deployment Management** | 60 min | Release Mgmt, Deployment Mgmt | Release record grouping multiple changes. Deployment plan. Release calendar. Post-deployment verification. |

**Output:** Full operational cycle demonstrated end-to-end with real monitoring data, CMDB context, SLA tracking, and KB integration.

**Folder:** `phase-3-operate/`

### The Operational Loop

```
  ┌─ Monitoring (Prometheus) ──► Event (ServiceNow) ──► Incident
  │                                                        │
  │   SLA clock starts ◄──── CI attached from CMDB         │
  │   KB articles suggested ◄── Knowledge Base              │
  │                                                        │
  │   Incident ──► Problem (recurring?) ──► RCA            │
  │                    │                     │              │
  │                    │              Known Error ──► KB    │
  │                    │                     │              │
  │                    └──► Change Request ──┘              │
  │                           │                            │
  │                    CI Impact Analysis (CMDB)            │
  │                    CAB Approval                         │
  │                    Implementation                       │
  │                    Post-Implementation Review           │
  │                           │                            │
  └───────────────────────────┘                            │
        Monitoring confirms fix ◄──────────────────────────┘
```

---

## Phase 4: Optimize & Report

> **ITIL Value Chain:** Improve
> **Goal:** Measure, analyze, and improve UPI service delivery

| Lab | Title | Duration | ITIL Practice | What You Learn |
|---|---|---|---|---|
| **17** | **Reporting & Performance Analytics** | 90 min | Measurement & Reporting | Dashboards: MTTR, MTBF, SLA compliance %, change success rate, incident trend. PA indicators. Scheduled reports. |
| **18** | **Continual Improvement (CSI)** | 60 min | Continual Improvement | CSI register. Improvement initiatives from incident/problem data. PDCA cycle. Improvement tracking in ServiceNow. |
| **19** | **Availability & Capacity Management** | 60 min | Availability Mgmt, Capacity Mgmt | CI availability from CMDB. Uptime calculations. Capacity metrics from Prometheus. Capacity planning. |

**Output:** Data-driven insights into UPI service performance, with improvement initiatives tracked.

**Folder:** `phase-4-optimize/`

---

## Phase 5: Automate & Integrate

> **ITIL Value Chain:** Obtain/Build
> **Goal:** Extend ServiceNow with automation, custom logic, and external integrations

| Lab | Title | Duration | ITIL Practice | What You Build |
|---|---|---|---|---|
| **20** | **Flow Designer & Workflow Automation** | 90 min | — | Auto-assignment rules. SLA breach escalation. Auto-close resolved incidents. Approval flows for catalog items. Scheduled flows. |
| **21** | **Business Rules, Client Scripts & UI Policies** | 90 min | — | Server-side: auto-populate CI from category. Client-side: mandatory fields on P1. UI Policies: show/hide fields by state. Script Includes for reuse. |
| **22** | **REST API, Integration Hub & Update Sets** | 90 min | — | Inbound API: create incidents from external systems. Outbound: webhook on state change. Integration with Prometheus/Grafana. Update Sets for SDLC. ATF for testing. |

**Output:** Automated, integrated ServiceNow instance with custom business logic and external system connectivity.

**Folder:** `phase-5-automate/`

---

## Lab Format Standard

Every lab follows this consistent structure:

```
# Lab XX: Title

**Level:** ... | **Duration:** ... | **Prerequisites:** ... | **PDI Version:** Zurich

## Objective (what you'll learn)
## Scenario (UPI context for this lab)
## Part 1-N (step-by-step with UI instructions)
  - Each step: field-by-field tables
  - Screenshots guidance for Zurich UI
  - Work notes with realistic UPI content
## Practice Exercises (hands-on challenges)
## Lab Summary (what you did → why it matters)
## Key Concepts (ITIL terminology table)
## What's Next (connection to next lab)
## Appendix: Background Script (bulk setup alternative)
```

---

## ITIL 4 Practices Coverage Matrix

| ITIL 4 Practice | Lab(s) | Depth |
|---|---|---|
| Service Configuration Management | 07 | Deep — CMDB, CIs, relationships, service map |
| Service Portfolio Management | 08 | Moderate — business/technical services |
| Service Level Management | 09 | Deep — SLA, SLO, SLI, breach rules |
| Knowledge Management | 10 | Deep — KB structure, workflow, KEDB |
| Service Request Management | 11 | Deep — catalog, variables, approvals, fulfillment |
| Monitoring & Event Management | 12 | Deep — Prometheus → Event → Incident pipeline |
| Incident Management | 13 | Deep — full lifecycle with CMDB + SLA context |
| Problem Management | 14 | Deep — RCA, known error, CMDB impact |
| Change Enablement | 15 | Deep — Normal/Standard/Emergency, CAB, calendar |
| Release Management | 16 | Moderate — release records, deployment plans |
| Measurement & Reporting | 17 | Deep — dashboards, PA, scheduled reports |
| Continual Improvement | 18 | Moderate — CSI register, improvement initiatives |
| Availability Management | 19 | Moderate — CI availability, uptime |
| Information Security Management | 21 | Light — ACLs, role-based access in scripts |
| IT Asset Management | 07 | Light — asset records linked to CIs |

---

## What Each Lab Produces (Cumulative)

```
After Lab 06:  Users + Groups + Roles + Custom Table
After Lab 07:  + CMDB with 10+ UPI CIs and relationships
After Lab 08:  + "UPI Payment Processing" Business Service defined
After Lab 09:  + SLA definitions, SLO targets, SLI metrics mapped
After Lab 10:  + Knowledge Base with 10+ UPI articles
After Lab 11:  + Service Catalog with 5+ UPI request items
After Lab 12:  + Live demo stack with monitoring → ServiceNow pipeline
After Lab 13:  + 15+ incidents with CIs, SLAs tracking, KB links
After Lab 14:  + 3+ problems with RCA, known errors, CMDB impact
After Lab 15:  + 10+ changes (Normal/Standard/Emergency) with CI impact
After Lab 16:  + Release records grouping changes
After Lab 17:  + Dashboards: MTTR, SLA compliance, change success rate
After Lab 18:  + CSI register with improvement initiatives
After Lab 19:  + Availability and capacity reports
After Lab 20:  + 5+ automated flows (assignment, escalation, approval)
After Lab 21:  + Business rules, client scripts, UI policies
After Lab 22:  + REST API integration, update sets, ATF tests
```

---

## File Structure

```
phase-4-servicenow-labs/
├── CURRICULUM.md                      ← This file (master plan)
├── demo-e2e-incident/                 ← Docker Compose UPI stack
│
├── phase-1-foundation/
│   ├── lab-01-pdi-setup.md
│   ├── lab-02-platform-navigation.md
│   ├── lab-03-lists-and-forms.md
│   ├── lab-04-users-groups-roles.md
│   ├── lab-05-tables-and-columns.md
│   └── lab-06-filters-views-queries.md
│
├── phase-2-build-service/
│   ├── lab-07-cmdb-configuration-management.md
│   ├── lab-08-service-portfolio-business-services.md
│   ├── lab-09-sla-slo-sli-service-levels.md
│   ├── lab-10-knowledge-management.md
│   └── lab-11-service-catalog-request-management.md
│
├── phase-3-operate/
│   ├── lab-12-deploy-demo-stack-event-management.md
│   ├── lab-13-incident-management.md
│   ├── lab-14-problem-management.md
│   ├── lab-15-change-management.md
│   └── lab-16-release-deployment-management.md
│
├── phase-4-optimize/
│   ├── lab-17-reporting-performance-analytics.md
│   ├── lab-18-continual-improvement.md
│   └── lab-19-availability-capacity-management.md
│
├── phase-5-automate/
│   ├── lab-20-flow-designer-automation.md
│   ├── lab-21-business-rules-client-scripts.md
│   └── lab-22-rest-api-integration-update-sets.md
│
└── archive-v1/                        ← Previous lab versions (backup)
```

---

## Teaching Schedule Suggestion

| Day | Phase | Labs | Hours |
|---|---|---|---|
| Day 1 | Phase 1 | Labs 01-06 (Platform Foundation) | 5 hrs |
| Day 2 | Phase 2 | Labs 07-09 (CMDB, Services, SLAs) | 5 hrs |
| Day 3 | Phase 2 + 3 | Labs 10-12 (KB, Catalog, Deploy Stack) | 5 hrs |
| Day 4 | Phase 3 | Labs 13-15 (Incident, Problem, Change) | 5 hrs |
| Day 5 | Phase 3 + 4 | Labs 16-18 (Release, Reporting, CSI) | 5 hrs |
| Day 6 | Phase 4 + 5 | Labs 19-22 (Availability, Automation, API) | 5 hrs |
