# Section 0: Introduction to ITSM

## The Problem: IT Without Structure

Imagine NPCI runs UPI -- 14+ billion transactions/month, 400+ banks connected, 300+ million daily users.

Now imagine:

- A developer pushes a config change at 2 PM. Transactions start failing. Nobody knows who changed what.
- A bank reports "payments stuck since morning." Three teams investigate the same issue independently. No one talks to each other.
- An outage happens at night. The on-call engineer has no runbook, no escalation path, no idea who to call.
- Same issue happens every month. Each time it's treated as brand new.

**This is IT without ITSM -- reactive, chaotic, and expensive.**

---

## What is ITSM?

**IT Service Management (ITSM)** = a set of policies, processes, and procedures to plan, deliver, operate, and improve IT services.

In one line: **"How do we run IT like a well-managed business, not a fire station?"**

### Without ITSM vs With ITSM

| Without ITSM | With ITSM |
|---|---|
| "Server is down, someone fix it" | Incident logged, prioritized, assigned, tracked |
| "Why does this keep happening?" | Problem record tracks root cause, prevents recurrence |
| "Who changed the firewall rules?" | Every change is reviewed, approved, and recorded |
| "Can I get access to prod?" | Service request with approval workflow |
| "What are we even responsible for?" | Service catalog lists every service with owners |
| "Did we meet our uptime promise?" | SLAs measured and reported automatically |

---

## Why Should You Care?

As engineers joining a large enterprise like Publicis Sapient, you will:

1. **Work on client systems** that follow ITSM processes -- you need to speak the language
2. **Raise and resolve incidents** through tools like ServiceNow, Jira Service Management
3. **Submit change requests** before deploying to production
4. **Participate in problem reviews** (RCA/PIR) after major outages
5. **Operate within SLAs** that your team is measured against

ITSM is not theory -- it's **how production IT actually works** in banks, telecom, healthcare, and every large org.

---

## Our Running Example: NPCI UPI

Throughout these sections, we'll use **NPCI's UPI platform** as our example because:

- It's a **real, critical national infrastructure** you use daily
- It involves **multiple organizations** (NPCI, banks, payment apps)
- It has **extreme scale** (14B+ txns/month) and **zero tolerance for downtime**
- It requires every ITSM practice we'll learn

### NPCI's IT Landscape (Simplified)

```
+---------------------------------------------------------------+
|                        End Users                               |
|  (You, merchants, businesses -- 300M+ daily active)           |
+-------------------------------+-------------------------------+
                                |
+-------------------------------v-------------------------------+
|                     UPI Apps (PSPs)                            |
|  PhonePe | Google Pay | Paytm | BHIM | Bank Apps              |
+-------------------------------+-------------------------------+
                                |
+-------------------------------v-------------------------------+
|                     NPCI UPI Platform                          |
|  +-------------+ +-------------+ +-------------+             |
|  | Transaction | | Settlement  | | Dispute     |             |
|  | Engine      | | Engine      | | Resolution  |             |
|  +-------------+ +-------------+ +-------------+             |
|  +-------------+ +-------------+ +-------------+             |
|  | Registration| | Merchant    | | Monitoring  |             |
|  | Service     | | Onboarding  | | & Alerts    |             |
|  +-------------+ +-------------+ +-------------+             |
+-------------------------------+-------------------------------+
                                |
+-------------------------------v-------------------------------+
|                     Banks (Issuers & Acquirers)               |
|  SBI | HDFC | ICICI | Axis | 400+ banks                      |
+---------------------------------------------------------------+
```

---

## Glossary of Abbreviations

These abbreviations appear throughout ITSM and in tools like ServiceNow:

### ITSM Ticket Prefixes

| Prefix | Full Form | Meaning |
|---|---|---|
| **INC** | Incident | Something broke, restore it |
| **PRB** | Problem | Root cause investigation |
| **CHG** | Change Request | Planned modification to a service |
| **REQ** | Service Request | User needs something (access, info, setup) |
| **KE** | Known Error | Root cause found, permanent fix pending |

### Domain & Infrastructure Terms

| Term | Full Form | What it means |
|---|---|---|
| **NPCI** | National Payments Corporation of India | Operates UPI, IMPS, RuPay, etc. |
| **UPI** | Unified Payments Interface | Real-time inter-bank payment system |
| **PSP** | Payment Service Provider | Apps authorized to offer UPI (PhonePe, GPay, Paytm) |
| **VPA** | Virtual Payment Address | Your UPI ID (e.g., yourname@upi) |
| **NOC** | Network Operations Center | 24/7 monitoring team watching dashboards |
| **CAB** | Change Advisory Board | Group that reviews and approves changes |
| **CMDB** | Configuration Management Database | Map of all IT assets and relationships |
| **SLA** | Service Level Agreement | Formal promise between provider and consumer |
| **SLO** | Service Level Objective | Internal target (stricter than SLA) |
| **SLI** | Service Level Indicator | The actual measured metric |
| **MTTA** | Mean Time to Acknowledge | How fast we respond to an incident |
| **MTTR** | Mean Time to Resolve | How fast we fix an incident |
| **MTBF** | Mean Time Between Failures | How often things break |
| **RCA** | Root Cause Analysis | Investigation into why something failed |
| **PIR** | Post-Incident Review | Meeting after a major incident to learn |
| **SPOC** | Single Point of Contact | One team/person as the entry point (Service Desk) |
| **ITIL** | Information Technology Infrastructure Library | The framework behind ITSM best practices |

---

## ITSM Sections Roadmap

We'll build ITSM understanding one concept at a time, each with a UPI example:

| # | Topic | One-line Summary |
|---|---|---|
| 01 | Service & IT Service | What are we managing? |
| 02 | Incident Management | Something broke -- restore it NOW |
| 03 | Problem Management | WHY did it break? Prevent recurrence |
| 04 | Change Management | Control changes so they don't cause incidents |
| 05 | Service Request Management | "I need access / a new environment" |
| 06 | Service Catalog | Menu of all services you can request |
| 07 | Configuration Management (CMDB) | Map of all IT assets and their relationships |
| 08 | Service Level Management | SLA, SLO, SLI -- promises and measurement |
| 09 | Knowledge Management | Document what you know so others don't reinvent |
| 10 | Continual Improvement | Never stop getting better |

Each section builds on the previous. By the end, you'll see how these practices connect into a **complete system** for managing IT.

---

## Key Insight Before We Begin

> ITSM is not about bureaucracy or slowing things down.
> It's about **predictability, accountability, and learning from mistakes**.
>
> When UPI goes down for 30 minutes, NPCI doesn't want heroes who magically fix things.
> They want a **system** that detects, responds, resolves, and prevents -- every single time.
