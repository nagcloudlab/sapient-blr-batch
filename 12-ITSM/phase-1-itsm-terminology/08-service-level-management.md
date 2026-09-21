# Section 8: Service Level Management (SLA / SLO / SLI)

## What is Service Level Management?

Defining, agreeing, monitoring, and reporting on **promises about service quality**.

Think of it as: **"What did we promise? Are we keeping that promise? Can we prove it?"**

---

## The Three Pillars: SLI -> SLO -> SLA

```
SLI  =  What you MEASURE        (the thermometer)
SLO  =  What you TARGET          (the internal goal)
SLA  =  What you PROMISE          (the contract with penalties)
```

| | Full Form | Who cares | UPI Example |
|---|---|---|---|
| **SLI** | Service Level Indicator | Engineers | Transaction success rate = 99.4% right now |
| **SLO** | Service Level Objective | Engineering + Management | We target 99.9% success rate |
| **SLA** | Service Level Agreement | Business + Legal + Customer | We promise banks 99.5% -- breach = financial penalty |

**SLO is always stricter than SLA.** You aim higher internally so you never breach the external promise.

```
SLA: 99.5%  <-- breach this, you pay penalty
SLO: 99.9%  <-- breach this, internal alert, teams mobilize
SLI: 99.94% <-- actual current measurement

        99.0%     99.5%      99.9%   99.94%   100%
         |         |          |        |        |
         |    SLA--+     SLO--+   SLI--+        |
         |   (promise)  (target)  (actual)      |
```

---

## UPI Example: SLAs Between NPCI and Banks

### NPCI -> Banks (External SLA)

| Service | SLI (Metric) | SLO (Target) | SLA (Contractual) | Breach Penalty |
|---|---|---|---|---|
| Transaction Processing | Success rate | 99.9% | 99.5% | Financial penalty per 0.1% below |
| Transaction Latency | P95 response time | < 800ms | < 1500ms | Penalty if monthly avg exceeds |
| Settlement | On-time delivery | 100% by 6 AM | By 8 AM | Late settlement = escalation to RBI |
| Dispute Resolution | Acknowledgment time | < 30 min | < 1 hour | Regulatory non-compliance |
| Platform Availability | Uptime % | 99.99% | 99.9% | Per-minute credit for downtime |

### What does 99.9% uptime actually mean?

| Uptime | Allowed downtime/month | UPI Impact |
|---|---|---|
| 99% | 7 hours 18 min | ~150 crore failed transactions |
| 99.5% | 3 hours 39 min | ~75 crore failed transactions |
| 99.9% | 43 min 50 sec | ~15 crore failed transactions |
| 99.95% | 21 min 55 sec | ~7 crore failed transactions |
| 99.99% | 4 min 23 sec | ~1.5 crore failed transactions |

Every decimal point matters at NPCI scale.

---

## Internal SLAs: OLA (Operational Level Agreement)

SLA between **internal teams** that together fulfill the external SLA.

| From Team | To Team | Promise |
|---|---|---|
| NOC | Platform Engineering | Escalate P1 incidents within 2 min |
| Platform Engineering | NOC | Acknowledge escalation within 5 min |
| DBA Team | Platform Engineering | Database restore within 30 min |
| Infra Team | All teams | New environment provisioned within 2 business days |

OLAs are the **internal gears** that make external SLAs achievable.

```
External SLA: "Resolve P1 in 30 min"

That 30 min is split across internal OLAs:
  NOC detects + escalates:     2 min  (OLA)
  Platform acknowledges:       5 min  (OLA)
  Investigation + fix:        18 min  (team effort)
  Verify + close:              5 min  (OLA)
                              --------
  Total:                      30 min  = SLA met
```

---

## Underpinning Contracts (UC)

Agreements with **external vendors/partners**.

| Vendor | Promise to NPCI |
|---|---|
| Cloud Provider (AWS/Azure) | 99.99% compute uptime |
| Telecom (MPLS provider) | Network latency < 10ms between DCs |
| Axis Bank | API response time < 500ms for 95% of requests |

```
SLA (NPCI -> Banks) depends on:
    |-- OLA (internal teams)
    +-- UC (external vendors)
```

---

## Error Budget (Connecting SRE to ITSM)

Error budget is the flip side of SLO:

```
SLO: 99.9% success rate
Error budget: 0.1% = ~430,000 failed transactions/month allowed

Budget remaining:  0.06% used -> 0.04% left -> safe to deploy changes
Budget exhausted:  0.1% used -> FREEZE all changes, focus on reliability
```

This directly connects to **Change Management (Section 4)**: when error budget is low, CAB rejects non-critical changes.

---

## SLA Breach: What Happens?

```
Month: August 2026
SLA: 99.5% transaction success rate
Actual SLI: 99.3% (breached by 0.2%)

Consequences:
  1. Financial penalty to affected banks
  2. RBI scrutiny and possible audit
  3. Major Problem record raised (PRB)
  4. Executive review + improvement plan
  5. SLA breach report published to all banks
```

---

## Connection to Previous Sections

```
SLA defines promises for --> Services (Sec 1) listed in --> Service Catalog (Sec 6)

SLA breach triggers --> Incident (Sec 2) -> Problem (Sec 3)

Error budget controls --> Change approval (Sec 4)

SLA fulfillment tracked for --> Service Requests (Sec 5)

SLI data comes from --> Monitoring of CIs in CMDB (Sec 7)
```

---

## Key Takeaway

> **SLI** = the number on the dashboard
> **SLO** = the target you aim for internally
> **SLA** = the promise you can't break without consequences
>
> SLO is ALWAYS stricter than SLA. If your SLO and SLA are the same number, you have no safety margin -- you're driving at the edge of a cliff.
