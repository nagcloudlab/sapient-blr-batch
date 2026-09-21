# Section 15: ITIL 4 -- 34 Practices Overview

## What is a Practice?

A set of organizational resources designed for performing work or accomplishing an objective.

ITIL v3 called them "processes." ITIL 4 calls them **"practices"** because they include not just processes, but also **people, tools, information, and partners**.

```
ITIL v3 Process = just the workflow
ITIL 4 Practice = people + process + tools + information + partners
```

---

## Three Categories

```
+---------------------------+
| General Management (14)   |  --> Apply to ALL of business, not just IT
+---------------------------+
| Service Management (17)   |  --> Specific to IT service management
+---------------------------+
| Technical Management (3)  |  --> Technical/infrastructure focused
+---------------------------+
```

---

## Category 1: General Management Practices (14)

These come from **general business management** -- not unique to IT.

| # | Practice | Purpose | UPI Example |
|---|---|---|---|
| 1 | **Architecture Management** | Understand how components fit together | UPI system architecture: microservices, Kafka, Oracle |
| 2 | **Continual Improvement** | Always get better (Sec 10) | CSI register, PDCA cycles |
| 3 | **Information Security Mgmt** | Protect information CIA (Confidentiality, Integrity, Availability) | Encrypt UPI transaction data, PCI-DSS compliance |
| 4 | **Knowledge Management** | Share what you know (Sec 9) | Runbooks, Known Error articles |
| 5 | **Measurement & Reporting** | Measure what matters, report to stakeholders | Monthly SLA reports to banks, RBI |
| 6 | **Organizational Change Mgmt** | Manage the people side of change | Training NOC team on new monitoring tools |
| 7 | **Portfolio Management** | Manage the full set of services | Decide: invest in UPI Lite vs International UPI |
| 8 | **Project Management** | Deliver projects on time and budget | "UPI 3.0 rollout" project |
| 9 | **Relationship Management** | Maintain good stakeholder relationships | Quarterly reviews with top 20 banks |
| 10 | **Risk Management** | Identify and manage risks | "What if a major bank goes offline during Diwali?" |
| 11 | **Service Financial Mgmt** | Manage budgets and costs | Cost per UPI transaction, infrastructure budget |
| 12 | **Strategy Management** | Define direction and priorities | "UPI to become India's primary digital payment rail" |
| 13 | **Supplier Management** | Manage external vendors | Cloud provider SLAs, telecom contracts |
| 14 | **Workforce & Talent Mgmt** | Right people, right skills | Hiring SREs, training L1 on ITSM tools |

---

## Category 2: Service Management Practices (17)

The **core ITSM practices** -- most of Phase 1 lives here.

| # | Practice | Purpose | Covered in |
|---|---|---|---|
| 1 | **Availability Management** | Ensure services are available when needed | New |
| 2 | **Business Analysis** | Understand business needs and recommend solutions | New |
| 3 | **Capacity & Performance Mgmt** | Ensure services have enough capacity | New |
| 4 | **Change Enablement** | Control changes to minimize risk | **Section 4** |
| 5 | **Incident Management** | Restore service ASAP | **Section 2** |
| 6 | **IT Asset Management** | Track lifecycle of IT assets | Related to Sec 7 |
| 7 | **Monitoring & Event Mgmt** | Detect and respond to events | New |
| 8 | **Problem Management** | Find and eliminate root causes | **Section 3** |
| 9 | **Release Management** | Make new features available | New |
| 10 | **Service Catalog Mgmt** | Maintain the service menu | **Section 6** |
| 11 | **Service Configuration Mgmt** | Manage CI information (CMDB) | **Section 7** |
| 12 | **Service Continuity Mgmt** | Ensure services survive disasters | New |
| 13 | **Service Design** | Design services that meet needs | New |
| 14 | **Service Desk** | Single point of contact | **Section 2** |
| 15 | **Service Level Mgmt** | Define and monitor SLAs | **Section 8** |
| 16 | **Service Request Mgmt** | Handle user requests | **Section 5** |
| 17 | **Service Validation & Testing** | Ensure services meet requirements | New |

---

## Category 3: Technical Management Practices (3)

Focused on **technology and infrastructure**.

| # | Practice | Purpose | UPI Example |
|---|---|---|---|
| 1 | **Deployment Management** | Move components to live environments | Rolling deployment of Txn Engine v4.2 |
| 2 | **Infrastructure & Platform Mgmt** | Manage infrastructure and platforms | K8s clusters, Kafka, Oracle DB, network |
| 3 | **Software Development & Mgmt** | Build and maintain software | Developing UPI Lite circuit breaker module |

---

## How They Connect: The Practice Map

```
                    General (14)
                    Foundation for everything
                         |
          +--------------+--------------+
          |                             |
    Service (17)                  Technical (3)
    Day-to-day ITSM              Build & deploy
          |                             |
    +-----+-----+              +--------+--------+
    |     |     |              |        |        |
  Incident Change Problem   Deploy  Infra    Software
  Request  SLA   Catalog    Mgmt    Mgmt     Dev
```

---

## Which Practices Matter Most?

Not all 34 are equally important in daily work:

```
DAILY USE (you'll touch these every day):
  * Incident Management
  * Service Desk
  * Monitoring & Event Management
  * Change Enablement
  * Service Request Management
  * Knowledge Management

WEEKLY USE (regular cadence):
  * Problem Management
  * Release Management
  * Deployment Management
  * Service Level Management

PERIODIC (monthly/quarterly):
  * Continual Improvement
  * Capacity & Performance Management
  * Availability Management
  * Risk Management

STRATEGIC (annual/as-needed):
  * Strategy Management
  * Portfolio Management
  * Architecture Management
  * Service Continuity Management
```

---

## UPI Day-in-the-Life: Which Practices Fire?

```
06:00  Settlement completes          -> Monitoring & Event, Deployment
08:00  NOC shift handover            -> Service Desk, Knowledge Mgmt
09:15  PNB transactions slow         -> Incident Mgmt, Monitoring & Event
09:22  Fix applied from KB           -> Knowledge Mgmt, Incident Mgmt
10:00  Deploy circuit breaker canary -> Change Enablement, Deployment, Release
11:30  ICICI requests TPS increase   -> Service Request, Capacity & Performance
12:00  Monitor canary metrics        -> Monitoring & Event, Service Level
14:00  Expand canary rollout         -> Deployment, Change Enablement
15:30  PRB review meeting            -> Problem Mgmt, Continual Improvement
16:00  CAB meeting for Kafka upgrade -> Change Enablement, Risk Mgmt
18:00  Schedule full rollout         -> Release, Deployment
```

**In one day, NPCI uses 12+ practices.** They're not separate -- they're interwoven.

---

## Key Takeaway

> You don't need to memorize all 34 practices. You need to understand:
>
> 1. **General practices** = business foundation (applies everywhere)
> 2. **Service practices** = core ITSM (your daily work)
> 3. **Technical practices** = build & deploy (engineering focus)
>
> The 8-10 practices from Phase 1 (Sections 1-10) cover 80% of what you'll use daily. The rest are supporting practices you'll encounter as needed.
