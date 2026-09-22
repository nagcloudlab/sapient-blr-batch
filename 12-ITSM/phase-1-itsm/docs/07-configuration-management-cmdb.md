# Section 7: Configuration Management (CMDB)

## What is CMDB?

**Configuration Management Database** -- a **map of every IT asset and how they relate to each other**.

Think of it as: **"Google Maps for your IT infrastructure."** You don't just know what exists -- you know what connects to what, and what breaks if something goes down.

---

## The Core Concept: Configuration Item (CI)

A **CI** is anything that needs to be managed to deliver an IT service.

| CI Type | UPI Examples |
|---|---|
| **Hardware** | Server rack in Mumbai DC, Load balancer |
| **Software** | UPI Txn Engine v4.1, Kafka 3.5, Oracle DB |
| **Network** | VPN tunnel to HDFC, API gateway, Firewall rules |
| **Documentation** | Runbook for settlement engine, API spec for banks |
| **Service** | UPI Payments (business), Transaction Processing (IT) |
| **People/Teams** | Platform Engineering team, NOC, DBA team |

---

## UPI Example: What's in NPCI's CMDB?

```
CI-1001: UPI Transaction Engine
  |-- Type: Application
  |-- Version: v4.1
  |-- Environment: Production
  |-- Owner: Platform Engineering
  |-- Hosted on: CI-2045 (K8s Cluster-A, Mumbai DC)
  |-- Depends on:
  |     |-- CI-3012 (Oracle DB - transaction store)
  |     |-- CI-3018 (Kafka cluster - event streaming)
  |     +-- CI-4001 (PSP Gateway - connects to banks)
  |-- Supports:
  |     +-- CI-5001 (UPI Payments - business service)
  +-- Related SLA: 99.95% uptime
```

Every CI has: **identity, type, version, owner, relationships, and status.**

---

## Why CMDB Matters: The Dependency Map

Without CMDB:

```
Incident: "UPI payments are slow"
Team: "No idea what's causing it. Let's check everything."
(3 hours later, 5 teams investigating blindly)
```

With CMDB:

```
Incident: "UPI payments are slow"
CMDB lookup: UPI Payments --> Txn Engine --> Kafka --> Kafka runs on Node-7
Monitoring: Node-7 CPU at 98%
Resolution: Scale Kafka, add Node-8
Time: 12 minutes
```

---

## CMDB Relationship Types

| Relationship | Meaning | UPI Example |
|---|---|---|
| **Runs on** | Software on hardware | Txn Engine *runs on* K8s Cluster-A |
| **Depends on** | Needs this to work | Txn Engine *depends on* Oracle DB |
| **Used by** | Consumed by another CI | Oracle DB *used by* Txn Engine, Settlement Engine |
| **Supports** | Enables a business service | Txn Engine *supports* UPI Payments |
| **Connected to** | Network/integration link | NPCI Gateway *connected to* HDFC Bank API |

---

## Visualizing Dependencies

```
                    UPI Payments (Business Service)
                          |
              +-----------+-----------+
              |                       |
     Txn Engine (App)        Settlement Engine (App)
         |                           |
    +----+----+                 +----+----+
    |         |                 |         |
 Kafka     Oracle DB       Oracle DB   SFTP Server
    |         |                 |
 K8s       DB Server        DB Server
 Cluster-A  (Mumbai)        (Chennai - DR)
```

**Impact analysis:** If Oracle DB (Mumbai) goes down --> Txn Engine AND Settlement Engine are affected --> UPI Payments degraded. CMDB tells you this **instantly** without guessing.

---

## CMDB in Action: Connecting to Other Sections

| When this happens... | CMDB helps by... |
|---|---|
| **Incident** (Sec 2) | "What depends on the failed component?" --> Impact scope |
| **Problem** (Sec 3) | "Which CIs were involved?" --> Narrow RCA scope |
| **Change** (Sec 4) | "If I upgrade this, what else is affected?" --> Risk assessment |
| **Service Request** (Sec 5) | "Does this environment already exist?" --> Avoid duplicates |
| **Service Catalog** (Sec 6) | "What infrastructure backs this service?" --> Technical view |

---

## Keeping CMDB Accurate

A stale CMDB is worse than no CMDB -- it gives false confidence.

| Method | How |
|---|---|
| **Discovery tools** | Auto-scan network to find servers, apps, connections |
| **CI/CD integration** | Every deployment updates CMDB automatically |
| **Change Management link** | Every CHG must update affected CIs in CMDB |
| **Periodic audits** | Quarterly check: does CMDB match reality? |

---

## Key Takeaway

> CMDB is not a spreadsheet of servers. It's a **living map of relationships**.
>
> The question it answers is not "what do we have?" but **"if this breaks, what else breaks?"**
> That's the difference between 12-minute resolution and 3-hour chaos.
