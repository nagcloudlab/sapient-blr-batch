# Section 16: Key ITIL Practices Deep Dive

The practices from Phase 1 (Incident, Problem, Change, Request, Catalog, CMDB, SLA, Knowledge, Continual Improvement) are your core. This section covers the **remaining high-value practices** you'll encounter regularly.

---

## 16.1: Monitoring & Event Management

**Purpose:** Systematically observe services and components, and detect/classify events that are significant.

### What is an Event?

An **event** = any change of state that is significant to the management of a service.

| Event Type | Meaning | UPI Example |
|---|---|---|
| **Informational** | Something happened, no action needed | "Settlement batch completed successfully" |
| **Warning** | Approaching a threshold, watch closely | "Kafka disk usage at 75% (threshold: 85%)" |
| **Exception** | Threshold breached, action needed NOW | "Transaction success rate dropped below 98%" |

### Event Flow

```
Source (server, app, network)
    |
    v
Monitoring Tool (Prometheus, Grafana, Datadog)
    |
    v
Event detected & classified
    |
    +-- Informational --> Log it, move on
    |
    +-- Warning --> Alert team, create dashboard ticket
    |
    +-- Exception --> Auto-create INCIDENT (INC)
```

### UPI Example: NPCI's Monitoring Stack

```
What's monitored:                    Tool:
+----------------------------------+----------------------+
| Transaction success rate          | Prometheus + Grafana |
| Per-bank response latency         | Prometheus + Grafana |
| Kafka consumer lag                | Kafka Manager        |
| Database connection pool usage    | Oracle Enterprise Mgr|
| K8s pod health & restarts         | Kubernetes Dashboard |
| Network latency between DCs       | SNMP + custom probes |
| Settlement batch status           | Custom dashboard     |
| API gateway error rates           | API Gateway console  |
+----------------------------------+----------------------+

Alert rules:
  - Success rate < 99%     --> P2 Incident auto-created
  - Success rate < 95%     --> P1 Incident auto-created + page on-call
  - Kafka lag > 100K msgs  --> Warning alert to platform team
  - Pod restart > 3 in 5m  --> Exception alert
  - DB connections > 80%   --> Warning alert to DBA team
```

**Connection to Incident Management:** Most P1/P2 incidents at NPCI are **auto-detected** by monitoring, not reported by users. The goal: **detect before users notice**.

---

## 16.2: Availability Management

**Purpose:** Ensure services deliver agreed levels of availability to meet business needs.

### Key Concepts

| Term | Meaning | UPI Example |
|---|---|---|
| **Availability** | % of time a service is operational | UPI available 99.95% of the month |
| **Reliability** | How long a service runs without failure | UPI runs 72 hours avg between failures |
| **Maintainability** | How quickly a failed service is restored | Avg restore time: 12 minutes |
| **Serviceability** | Ability of external suppliers to meet their contracts | Cloud provider delivers 99.99% compute uptime |

### The Availability Formula

```
Availability % = (Agreed Service Time - Downtime) / Agreed Service Time x 100

UPI Example:
  Agreed service time: 24x7 = 43,200 min/month
  Downtime this month: 22 min (one P1 incident)
  Availability: (43200 - 22) / 43200 x 100 = 99.95%
```

### Availability Techniques at NPCI

| Technique | How | UPI Example |
|---|---|---|
| **Redundancy** | Duplicate critical components | Two data centers (Mumbai + Chennai DR) |
| **Failover** | Auto-switch to backup on failure | If Mumbai DC fails, Chennai takes over |
| **Load balancing** | Distribute load across nodes | Transactions spread across 20 Txn Engine pods |
| **Clustering** | Multiple nodes act as one | Oracle RAC database cluster |
| **Elimination of SPOFs** | Remove single points of failure | No single server handles all traffic |

### SPOF Analysis for UPI

```
Is there a single point of failure?

  Transaction Engine  --> 20 pods across 2 clusters  --> NO SPOF (good)
  Kafka               --> 5-node cluster, replication --> NO SPOF (good)
  Oracle DB           --> RAC cluster, DR replica     --> NO SPOF (good)
  API Gateway         --> Active-active, 2 DCs        --> NO SPOF (good)
  DNS                 --> Single provider              --> SPOF! (fix this)
  NPCI Core Switch    --> Dual switches, same vendor   --> Partial SPOF
```

---

## 16.3: Capacity & Performance Management

**Purpose:** Ensure services have sufficient capacity to meet current and future demand.

### The Three Sub-Practices

| Sub-Practice | Question | UPI Example |
|---|---|---|
| **Business Capacity** | Will we have enough for future demand? | "Diwali is in 6 weeks -- UPI volume will 3x" |
| **Service Capacity** | Can the service handle current load? | "Txn Engine handles 8,000 TPS, peak is 6,500 -- headroom OK" |
| **Component Capacity** | Can each component handle its share? | "Kafka can handle 50K msg/s, current peak 35K -- OK" |

### UPI Example: Diwali Planning

```
Normal day:   ~450 million transactions
Diwali peak:  ~1,400 million transactions (3x normal)

Capacity check (6 weeks before Diwali):
+------------------+----------+----------+---------+---------+
| Component        | Current  | Diwali   | Capacity| Action  |
|                  | Peak     | Expected | Limit   | Needed? |
+------------------+----------+----------+---------+---------+
| Txn Engine       | 6,500 TPS| 19,500   | 25,000  | OK      |
| Kafka            | 35K msg/s| 105K     | 80K     | SCALE!  |
| Oracle DB        | 4,000 QPS| 12,000   | 15,000  | OK      |
| API Gateway      | 10K req/s| 30K      | 50K     | OK      |
| Network (DC)     | 8 Gbps   | 24 Gbps  | 40 Gbps | OK      |
+------------------+----------+----------+---------+---------+

Action: Add 3 Kafka nodes (CHG-20261015-0032), test by Oct 25
```

---

## 16.4: Release Management

**Purpose:** Make new and changed services and features **available for use**.

### Release vs Deployment vs Change

| Term | What | UPI Example |
|---|---|---|
| **Change** | Approval to modify something | CHG: "Upgrade Txn Engine to v4.2" |
| **Release** | A collection of changes packaged together | Release 4.2: circuit breaker + retry + new dashboard |
| **Deployment** | Physically moving it into production | Rolling deployment across 20 pods |

```
Change (permission) --> Release (package) --> Deployment (action)

Think of it as:
  Change  = "You MAY renovate the kitchen"
  Release = "Here's the new kitchen (cabinets + sink + tiles)"
  Deploy  = "Install it in the house"
```

### Release Types

| Type | Scope | UPI Example |
|---|---|---|
| **Major** | Significant new features | UPI 3.0 with international payments |
| **Minor** | Small enhancements | Add circuit breaker to Txn Engine |
| **Patch** | Bug fixes only | Fix timeout handling for Axis Bank |
| **Emergency** | Urgent fix for live issue | Hotfix for settlement calculation error |

### UPI Release Example

```
Release: UPI Platform v4.2
+-----------------------------------------+
| Contains:                               |
|   CHG-001: Circuit breaker module       |
|   CHG-002: Retry with backoff           |
|   CHG-003: New Grafana dashboards       |
|   CHG-004: Updated runbooks             |
|                                         |
| Release date: Oct 5, 2026 (Sunday 2AM) |
| Release manager: Platform Lead          |
| Deployment strategy: Rolling canary     |
| Rollback plan: Revert to v4.1 images   |
| Go/No-Go checklist:                     |
|   [ ] All CHGs approved by CAB          |
|   [ ] Staging tests passed              |
|   [ ] Rollback tested                   |
|   [ ] NOC briefed on new alerts         |
|   [ ] Banks notified of maintenance     |
+-----------------------------------------+
```

---

## 16.5: Deployment Management

**Purpose:** Move new or changed components to **live environments** safely.

### Deployment Approaches

| Approach | How | Risk | UPI Example |
|---|---|---|---|
| **Big Bang** | Everything at once | High | Replace entire Txn Engine (not recommended) |
| **Phased/Rolling** | One group at a time | Medium | Update pods 1-5, then 6-10, then 11-20 |
| **Canary** | Small % first, then expand | Low | 5% traffic -> 25% -> 50% -> 100% |
| **Blue/Green** | Two identical environments, switch traffic | Low | Green (v4.1) live, Blue (v4.2) ready, swap |
| **Feature Flag** | Deploy code but toggle feature on/off | Lowest | Circuit breaker deployed but disabled, flip flag to enable |

### UPI Deployment: Canary in Action

```
Timeline for Txn Engine v4.2 deployment:

Sunday 02:00  Deploy v4.2 to 1 pod (5% traffic)
              Monitor: success rate, latency, error rate
       02:30  Metrics green --> expand to 5 pods (25%)
       03:00  Metrics green --> expand to 10 pods (50%)
       03:30  Metrics green --> expand to 20 pods (100%)
       04:00  Full rollout complete. v4.1 containers kept warm for 24h.

Monday 04:00  No issues in 24h --> decommission v4.1 containers

If at ANY stage metrics go red:
  --> STOP rollout
  --> Route all traffic back to v4.1 pods
  --> Rollback time: < 2 minutes (just traffic switch)
```

---

## 16.6: Service Continuity Management

**Purpose:** Ensure services can continue at acceptable levels following a **disaster** (not just an incident -- a major catastrophe).

### Incident vs Disaster

| | Incident | Disaster |
|---|---|---|
| **Scale** | One service or component fails | Entire data center or region fails |
| **Example** | Txn Engine pod crashes | Mumbai DC destroyed by flood |
| **Recovery** | Minutes to hours | Hours to days |
| **Process** | Incident Management | Service Continuity Management |

### UPI Disaster Scenarios

| Disaster | Impact | Recovery Strategy |
|---|---|---|
| Mumbai DC power failure | All services down | Failover to Chennai DR |
| Ransomware attack | Data encrypted, services locked | Restore from offline backups |
| Submarine cable cut | Network between DCs lost | Reroute via satellite/alternative ISP |
| Key vendor goes bankrupt | Cloud services unavailable | Multi-cloud strategy, data portability |

### Business Impact Analysis (BIA)

| Service | RTO | RPO |
|---|---|---|
| UPI Transaction Processing | 15 minutes | 0 (zero data loss) |
| Settlement Engine | 2 hours | Last settlement batch |
| Dispute Resolution | 4 hours | Last backup (1 hour) |
| Reporting Portal | 8 hours | Last backup (4 hours) |

```
RTO = How FAST must we recover?        (max acceptable downtime)
RPO = How much DATA can we lose?       (max acceptable data loss)

UPI Payments:
  RTO = 15 min  --> Must be back in 15 minutes
  RPO = 0       --> Cannot lose a single transaction

  This means: real-time replication to DR site,
              automatic failover, tested quarterly
```

### DR Testing at NPCI

```
Quarterly DR drill:
  1. Simulate Mumbai DC failure (controlled shutdown)
  2. Verify auto-failover to Chennai DC
  3. Run synthetic transactions through Chennai
  4. Measure: Did we meet RTO (15 min)? Did we lose data (RPO = 0)?
  5. Document gaps and fix before next drill

If DR drill fails --> P1 Problem record raised
                  --> Fix before next quarter
                  --> RBI notified of gap
```

---

## Connection Map: All Phase 2 Practices

```
Monitoring & Event (16.1)
    |-- detects --> Incidents (Sec 2)
    |-- feeds  --> Availability metrics (16.2)
    |-- feeds  --> Capacity metrics (16.3)

Availability (16.2)
    |-- measured by --> SLIs (Sec 8)
    |-- protected by --> Redundancy, failover
    |-- extreme case --> Service Continuity (16.6)

Capacity (16.3)
    |-- triggers --> Change requests (Sec 4) for scaling
    |-- informs  --> Release planning (16.4)

Release (16.4)
    |-- packages --> Changes (Sec 4)
    |-- executed via --> Deployment (16.5)

Deployment (16.5)
    |-- updates --> CMDB (Sec 7)
    |-- monitored by --> Monitoring & Event (16.1)

Service Continuity (16.6)
    |-- tested via --> Disaster Recovery drills
    |-- defines --> RTO/RPO for each service
    |-- depends on --> CMDB for dependency mapping (Sec 7)
```

---

## Key Takeaway

> These 6 practices complete the operational picture:
>
> - **Monitoring** = your eyes (see what's happening)
> - **Availability** = your promise (uptime targets)
> - **Capacity** = your planning (enough resources for tomorrow)
> - **Release** = your packaging (bundle changes together)
> - **Deployment** = your delivery (get it into production safely)
> - **Continuity** = your insurance (survive disasters)
>
> Combined with Phase 1 practices, you now have the **full toolkit** for managing IT services at any scale.
