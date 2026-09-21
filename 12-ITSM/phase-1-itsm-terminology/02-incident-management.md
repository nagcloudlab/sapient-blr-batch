# Section 2: Incident Management

## What is an Incident?

An **unplanned interruption** to a service, or a **reduction in quality** of a service.

Goal: **Restore service ASAP.** Not find root cause -- just get it working again.

---

## UPI Example: "Transactions are failing on Axis Bank"

**12:03 PM** -- NPCI's monitoring dashboard shows transaction success rate for Axis Bank drops from 99.2% -> 34%.

---

## Incident Lifecycle

### Step 1: Detection & Logging

| Field | Value |
|---|---|
| Incident ID | INC-20260921-0047 |
| Source | Monitoring alert (auto-created) |
| Affected Service | UPI Transaction Processing |
| Affected Entity | Axis Bank PSP node |
| Impact | ~2.8 crore users can't send/receive via Axis |
| Urgency | High |

### Step 2: Classification & Priority

ITSM uses a simple matrix:

```
                    High Urgency    Low Urgency
High Impact    -->    P1 (Critical)   P2 (High)
Low Impact     -->    P3 (Medium)     P4 (Low)
```

Axis Bank down = **High Impact + High Urgency = P1 (Critical)**

### Step 3: Escalation Path

```
L1 (NOC Operator)      --> "Axis node not responding, restarting service"
        |  (not resolved in 5 min)
L2 (Platform Engineer)  --> "Connection pool exhausted, clearing stale connections"
        |  (not resolved in 15 min)
L3 (Architect + Axis)   --> "Axis core banking upgrade broke API contract"
```

### Step 4: Resolution & Closure

- **Workaround applied:** NPCI routes Axis traffic through backup PSP node
- **Service restored:** 12:22 PM (19 min outage)
- **Incident closed** after user confirmation

---

## Key Metrics

| Metric | What it measures | Target Example |
|---|---|---|
| **MTTA** (Mean Time to Acknowledge) | How fast we respond | P1: < 2 min |
| **MTTR** (Mean Time to Resolve) | How fast we fix | P1: < 30 min |
| **First Call Resolution** | Fixed at L1 itself? | > 60% |
| **Reopen Rate** | Came back after closing? | < 5% |

---

## The Service Desk

The **Service Desk** is the single point of contact (SPOC) for all incidents and requests.

```
Banks / UPI Apps (PhonePe, GPay)
        |
   NPCI Service Desk  <-->  Monitoring Tools (auto-tickets)
        |
   L1 --> L2 --> L3 teams
```

It's NOT just a helpdesk. It **owns the incident lifecycle** -- even when L3 is fixing it, the Service Desk tracks and communicates status.

---

## Types of Incidents at NPCI

| Type | Example | Priority |
|---|---|---|
| Service outage | UPI completely down | P1 |
| Degradation | Success rate drops to 85% | P2 |
| Partial failure | One bank's transactions failing | P2/P3 |
| User-reported | "My VPA not working" | P3/P4 |

---

## Key Takeaway

> Incident Management = **firefighting with discipline**.
> You don't investigate why the fire started. You put it out first, then investigate (that's Problem Management -- next section).
