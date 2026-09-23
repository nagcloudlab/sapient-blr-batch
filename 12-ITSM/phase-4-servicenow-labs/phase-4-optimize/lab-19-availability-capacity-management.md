# Lab 19: Availability & Capacity Management

**Level:** Advanced | **Duration:** 60 min | **Prerequisites:** Labs 17-18 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand ITIL 4 Availability Management practice and its core metrics (MTBF, MTRS, MTTR)
- Calculate service availability from CMDB and incident data using the standard formula
- Perform Single Point of Failure (SPOF) analysis using CMDB relationship maps
- Understand ITIL 4 Capacity & Performance Management practice
- Map Prometheus metrics to capacity indicators (CPU, memory, throughput, DB connections)
- Build availability and capacity dashboards in ServiceNow
- Create capacity plans with growth projections for UPI services
- Establish availability targets and capacity baselines linked to CIs and SLAs

---

## Scenario: Measuring and Planning UPI Platform Resilience

```
NPCI management has requested two critical reports:

1. AVAILABILITY REPORT
   "What is the actual uptime of each UPI service component?
    Are we meeting our 99.95% SLO? Where are the gaps?"

2. CAPACITY PLAN
   "UPI transaction volume grew 40% last year. Will our infrastructure
    handle the next 12 months? When do we need to scale?"

You will use ServiceNow CMDB data, incident records from Labs 13-15,
and Prometheus metrics from the demo stack to answer both questions
with mathematical precision.

Current State (from previous labs):
  - CMDB populated with UPI CIs and relationships (Lab 07)
  - SLOs defined: 99.95% availability, P95 latency < 500ms (Lab 09)
  - Incidents recorded with CI associations (Lab 13)
  - Problems identified root causes (Lab 14)
  - Changes deployed and reviewed (Lab 15)
  - Prometheus + Grafana monitoring live (Lab 12)
  - CSI register tracking improvements (Lab 18)
```

---

## Part 1: ITIL 4 Availability Management — Theory

### 1.1 The Availability Management Practice

```
ITIL 4 Definition:
  "The purpose of the availability management practice is to ensure
   that services deliver agreed levels of availability to meet the
   needs of customers and users."

Scope:
  ├── Service Availability    — end-to-end user experience
  ├── Component Availability  — individual CI uptime
  └── Vital Business Functions (VBF) — critical capabilities that
       must be protected above all else

For UPI:
  VBF #1: Transaction Processing (pay/collect)
  VBF #2: Settlement Processing (end-of-day bank settlements)
  VBF #3: Merchant Onboarding (new merchant registration)
```

### 1.2 Core Availability Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│                   AVAILABILITY METRICS                          │
├──────────┬──────────────────────────────────────────────────────┤
│ Metric   │ Definition                                          │
├──────────┼──────────────────────────────────────────────────────┤
│ AST      │ Agreed Service Time — total time the service        │
│          │ should be available (e.g., 24x7 = 720 hrs/month)    │
├──────────┼──────────────────────────────────────────────────────┤
│ DT       │ Downtime — total time the service was unavailable   │
│          │ during AST                                          │
├──────────┼──────────────────────────────────────────────────────┤
│ MTBF     │ Mean Time Between Failures — average time between   │
│          │ the end of one failure and the start of the next    │
│          │ Formula: (AST - DT) / number_of_failures            │
├──────────┼──────────────────────────────────────────────────────┤
│ MTRS     │ Mean Time to Restore Service — average time to      │
│          │ restore service after a failure                      │
│          │ Formula: total_DT / number_of_failures              │
├──────────┼──────────────────────────────────────────────────────┤
│ MTTR     │ Mean Time to Repair — average time to repair the    │
│          │ failed component (subset of MTRS)                   │
├──────────┼──────────────────────────────────────────────────────┤
│ MTBSI    │ Mean Time Between System Incidents                  │
│          │ Formula: MTBF + MTRS                                │
└──────────┴──────────────────────────────────────────────────────┘
```

### 1.3 The Availability Formula

```
                    (AST - DT)
  Availability % = ──────────── x 100
                       AST

  Where:
    AST = Agreed Service Time (hours in measurement period)
    DT  = Downtime (hours of unplanned outage)

  Example:
    AST = 720 hours (30-day month, 24x7 service)
    DT  = 4.5 hours (3 outages totaling 4.5 hours)

    Availability = (720 - 4.5) / 720 x 100
                 = 715.5 / 720 x 100
                 = 99.375%
```

### 1.4 The "Nines" Table — Availability Targets

```
┌───────────────┬──────────────────┬──────────────────┬──────────────────┐
│ Availability  │ Annual Downtime  │ Monthly Downtime │ Weekly Downtime  │
├───────────────┼──────────────────┼──────────────────┼──────────────────┤
│ 99.0%         │ 3 days 15 hrs    │ 7 hrs 18 min     │ 1 hr 41 min      │
│ 99.5%         │ 1 day 19.5 hrs   │ 3 hrs 39 min     │ 50 min 24 sec    │
│ 99.9%         │ 8 hrs 46 min     │ 43 min 50 sec    │ 10 min 5 sec     │
│ 99.95%  ◄ UPI │ 4 hrs 23 min     │ 21 min 55 sec    │ 5 min 2 sec      │
│ 99.99%        │ 52 min 36 sec    │ 4 min 23 sec     │ 1 min 0.5 sec    │
│ 99.999%       │ 5 min 16 sec     │ 26.3 sec         │ 6 sec            │
└───────────────┴──────────────────┴──────────────────┴──────────────────┘

UPI SLO Target: 99.95%
  → Maximum allowed downtime: 4 hrs 23 min per YEAR
  → Maximum allowed downtime: 21 min 55 sec per MONTH
  → This is extremely tight — requires redundancy at every layer
```

### 1.5 The Expanded Incident Lifecycle

```
An incident's impact on availability spans multiple phases:

  ┌──────────┐   ┌───────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │  DETECT  │──►│ DIAGNOSE  │──►│  REPAIR  │──►│ RESTORE  │──►│ RECOVER  │
  └──────────┘   └───────────┘   └──────────┘   └──────────┘   └──────────┘
       │              │               │               │              │
   Time to       Time to          Time to         Time to        Time to
   detect        diagnose         repair          restore        recover
   the failure   root cause       the component   the service    full
                                                                 performance

  ◄─────────────── MTRS (Mean Time to Restore Service) ──────────────────►
                     ◄──── MTTR (Mean Time to Repair) ────►

  Reducing MTRS requires improvement at EVERY stage:
    - Faster detection → better monitoring, lower alert thresholds
    - Faster diagnosis → runbooks, known error database, AI assist
    - Faster repair    → automation, hot-swap components
    - Faster restore   → failover, redundancy, DR procedures
    - Faster recover   → cache warming, connection pool refill
```

### 1.6 Component vs Service Availability

```
Component availability:   Each CI has its own uptime metric
Service availability:     Depends on architecture — serial vs parallel

SERIAL configuration (all components must be up):

  Service Availability = A(component1) x A(component2) x ... x A(componentN)

  Example: UPI Transaction Flow (serial)
    App Server:     99.99%
    Load Balancer:  99.999%
    PostgreSQL:     99.95%
    Payment GW:     99.99%

    Service = 0.9999 x 0.99999 x 0.9995 x 0.9999
            = 0.9993 (99.93%)

  Even though each component is above 99.95%, the SERVICE is below!

PARALLEL configuration (redundant — all must fail for service failure):

  Failure Probability = (1 - A1) x (1 - A2)
  Availability = 1 - Failure Probability

  Example: Two redundant app servers, each 99.99%
    Failure = (1 - 0.9999) x (1 - 0.9999) = 0.0001 x 0.0001 = 0.00000001
    Combined Availability = 1 - 0.00000001 = 99.999999%
```

---

## Part 2: ITIL 4 Capacity & Performance Management — Theory

### 2.1 The Capacity & Performance Management Practice

```
ITIL 4 Definition:
  "The purpose of the capacity and performance management practice is
   to ensure that services achieve agreed and expected performance,
   satisfying current and future demand in a cost-effective way."

Three sub-practices:
  ├── Business Capacity Management
  │     What: Translate business demand into resource requirements
  │     UPI: "40% YoY transaction growth → how many more servers?"
  │
  ├── Service Capacity Management
  │     What: Monitor and manage service-level performance
  │     UPI: "P95 latency < 500ms under current load"
  │
  └── Component Capacity Management
        What: Monitor and manage individual component resources
        UPI: "CPU at 72%, memory at 65%, DB connections at 80%"
```

### 2.2 Capacity vs Performance

```
┌──────────────────────────────────────────────────────────────────┐
│  CAPACITY is about having ENOUGH resources                       │
│  PERFORMANCE is about resources working FAST ENOUGH              │
│                                                                  │
│  You can have enough capacity but poor performance:              │
│    → 16 CPU cores (plenty) but unoptimized queries (slow)        │
│                                                                  │
│  You can have good performance but insufficient capacity:        │
│    → Fast queries (10ms) but only 100 DB connections (not enough)│
│                                                                  │
│  Both must be managed together for service health                │
└──────────────────────────────────────────────────────────────────┘
```

### 2.3 Capacity Planning Techniques

```
1. TREND ANALYSIS
   Collect historical data → identify growth patterns → extrapolate
   UPI: Transaction count per month → linear regression → predict exhaustion

2. MODELING
   Analytical: mathematical models (queueing theory, etc.)
   Simulation: test with synthetic load before deploying
   Baseline:   measure current capacity and compare against demand

3. DEMAND MANAGEMENT
   Influence demand to match available capacity
   UPI: Rate limiting per PSP, off-peak batch processing for settlements

4. APPLICATION SIZING
   Estimate resources required for new or changed services
   UPI: "New merchant onboarding feature needs 2 additional app servers"
```

---

## Part 3: Calculate Availability from CMDB & Incidents

### 3.1 Gather Incident Data for Availability Calculation

Navigate: **All > Incidents > All**

Apply filter to find UPI-related outage incidents:

| Filter Field | Operator | Value |
|---|---|---|
| Configuration Item | is not empty | — |
| State | is | Closed |
| Priority | is one of | 1 - Critical, 2 - High |

> **Note:** Only P1 and P2 incidents are considered for availability calculation because lower priority incidents typically represent degraded service rather than outright unavailability.

### 3.2 Calculate Downtime Per CI

For each CI, sum the time between incident creation and resolution:

```
Downtime per incident = Resolved Date - Opened Date
                       (only counting time within AST)

For 24x7 services like UPI, AST = all hours, so:
  Downtime = Resolved - Opened (no exclusions)
```

**Step-by-step:**

1. Open a closed P1/P2 incident
2. Note the **Configuration Item** field
3. Note the **Opened** timestamp
4. Note the **Resolved** timestamp
5. Calculate the difference in hours

### 3.3 Worked Example — UPI Transaction Service

```
Measurement Period: Last 30 days (September 2026)
AST = 30 days x 24 hours = 720 hours

Incident Data for CI "UPI Transaction Service":
┌────────┬────────────────────────┬────────────────────────┬──────────┐
│ INC #  │ Opened                 │ Resolved               │ Downtime │
├────────┼────────────────────────┼────────────────────────┼──────────┤
│ INC001 │ Sep 03 14:22           │ Sep 03 16:07           │ 1.75 hrs │
│ INC002 │ Sep 11 02:45           │ Sep 11 03:30           │ 0.75 hrs │
│ INC003 │ Sep 19 09:15           │ Sep 19 11:15           │ 2.00 hrs │
├────────┼────────────────────────┼────────────────────────┼──────────┤
│ TOTAL  │                        │                        │ 4.50 hrs │
└────────┴────────────────────────┴────────────────────────┴──────────┘

Availability Calculation:
  Availability = (AST - DT) / AST x 100
               = (720 - 4.5) / 720 x 100
               = 715.5 / 720 x 100
               = 99.375%

  SLO Target:   99.95%
  Actual:       99.375%
  Variance:     -0.575%  ← BELOW TARGET

  Monthly downtime budget at 99.95%: 21.9 minutes
  Actual downtime: 270 minutes (4.5 hours)
  Overrun: 248.1 minutes (12.3x the budget!)
```

### 3.4 Calculate MTBF and MTRS

```
For UPI Transaction Service (September 2026):

MTRS (Mean Time to Restore Service):
  = Total Downtime / Number of Failures
  = 4.5 hours / 3 failures
  = 1.5 hours per failure

MTBF (Mean Time Between Failures):
  = (AST - Total Downtime) / Number of Failures
  = (720 - 4.5) / 3
  = 715.5 / 3
  = 238.5 hours between failures
  = approximately 9.9 days between failures

MTBSI (Mean Time Between System Incidents):
  = MTBF + MTRS
  = 238.5 + 1.5
  = 240 hours (10 days)
```

### 3.5 Calculate Availability for All UPI CIs

Run a similar analysis for each CI:

```
┌──────────────────────────┬────────┬────────┬──────────┬─────────┬────────┐
│ Configuration Item       │ AST(h) │ DT(h)  │ Avail %  │ SLO %   │ Status │
├──────────────────────────┼────────┼────────┼──────────┼─────────┼────────┤
│ UPI Transaction Service  │ 720    │ 4.50   │ 99.375%  │ 99.95%  │ BREACH │
│ UPI Settlement Service   │ 720    │ 1.25   │ 99.826%  │ 99.95%  │ BREACH │
│ PostgreSQL Primary       │ 720    │ 2.00   │ 99.722%  │ 99.95%  │ BREACH │
│ Load Balancer            │ 720    │ 0.00   │ 100.00%  │ 99.95%  │ OK     │
│ App Server 1             │ 720    │ 0.50   │ 99.931%  │ 99.95%  │ BREACH │
│ App Server 2             │ 720    │ 0.00   │ 100.00%  │ 99.95%  │ OK     │
│ DB Server 1 (Primary)    │ 720    │ 2.00   │ 99.722%  │ 99.95%  │ BREACH │
│ DB Server 2 (Replica)    │ 720    │ 0.25   │ 99.965%  │ 99.95%  │ OK     │
├──────────────────────────┼────────┼────────┼──────────┼─────────┼────────┤
│ Overall UPI Service      │ 720    │ 4.50   │ 99.375%  │ 99.95%  │ BREACH │
└──────────────────────────┴────────┴────────┴──────────┴─────────┴────────┘

Key Observations:
  1. UPI Transaction Service has the worst availability — 3 major outages
  2. PostgreSQL Primary is a reliability concern — single primary, no auto-failover
  3. Load Balancer and App Server 2 had zero downtime — well-architected
  4. 5 of 8 CIs breached SLO — systemic reliability problem
```

---

## Part 4: Single Point of Failure (SPOF) Analysis

### 4.1 Review CMDB Relationship Map

Navigate: **All > Configuration > CI Class Manager > UPI Transaction Service > Dependency Views**

Or use the Service Map:

Navigate: **All > Service Mapping > Service Maps** and select **UPI Payment Processing**

```
The CMDB dependency view shows:

  UPI Payment Processing (Business Service)
    │
    ├── UPI Transaction Service (Application)
    │     ├── depends_on → Load Balancer ──► App Server 1
    │     │                                 ──► App Server 2
    │     ├── depends_on → PostgreSQL Primary ← SPOF!
    │     └── depends_on → Payment Gateway    ← SPOF!
    │
    ├── UPI Settlement Service (Application)
    │     ├── depends_on → PostgreSQL Primary ← same SPOF!
    │     └── depends_on → Settlement Gateway
    │
    ├── Snow Bridge (Integration)                ← SPOF!
    │     └── connects → ServiceNow instance
    │
    └── Monitoring Stack
          ├── Prometheus
          ├── Grafana
          └── AlertManager
```

### 4.2 Identify SPOFs

A Single Point of Failure is any component whose failure alone causes service failure and which has no redundancy.

```
┌─────┬──────────────────────────┬──────────────┬──────────────────────────────┐
│ #   │ SPOF Component           │ Impact       │ Why It's a SPOF              │
├─────┼──────────────────────────┼──────────────┼──────────────────────────────┤
│  1  │ PostgreSQL Primary       │ Critical     │ Single primary database.     │
│     │                          │              │ Replica exists but NO auto-  │
│     │                          │              │ failover configured.         │
│     │                          │              │ If primary fails, manual     │
│     │                          │              │ promotion required (30+ min) │
├─────┼──────────────────────────┼──────────────┼──────────────────────────────┤
│  2  │ Payment Gateway          │ Critical     │ Single instance. No          │
│     │                          │              │ redundancy. All transactions │
│     │                          │              │ route through this one       │
│     │                          │              │ gateway.                     │
├─────┼──────────────────────────┼──────────────┼──────────────────────────────┤
│  3  │ Snow Bridge              │ High         │ Single integration point     │
│     │                          │              │ between Prometheus/Alert-    │
│     │                          │              │ Manager and ServiceNow.      │
│     │                          │              │ If down, alerts don't create │
│     │                          │              │ incidents automatically.     │
├─────┼──────────────────────────┼──────────────┼──────────────────────────────┤
│  4  │ Settlement Gateway       │ High         │ Single instance for bank     │
│     │                          │              │ settlement processing.       │
│     │                          │              │ Failure blocks EOD           │
│     │                          │              │ settlements.                 │
└─────┴──────────────────────────┴──────────────┴──────────────────────────────┘
```

### 4.3 SPOF Risk Assessment and Recommendations

```
SPOF #1: PostgreSQL Primary — No Auto-Failover
───────────────────────────────────────────────
  Current State:
    - Primary handles all reads and writes
    - Replica exists for read queries only
    - Manual failover procedure: ~30 minutes
    - Last failure: Sep 19, caused 2-hour outage

  Recommendation:
    - Deploy Patroni or pg_auto_failover for automatic failover
    - Target failover time: < 30 seconds
    - Estimated cost: 0 (open-source tooling) + 2 sprint points
    - Risk reduction: eliminates 44% of measured downtime

  Availability Impact if Fixed:
    DT would reduce from 4.5h to 2.5h
    Availability = (720 - 2.5) / 720 x 100 = 99.653%
    Still below 99.95% — need to fix more SPOFs

SPOF #2: Payment Gateway — Single Instance
──────────────────────────────────────────
  Current State:
    - Single gateway instance processes all UPI transactions
    - No active-active or active-passive configuration
    - Failure means 100% transaction failure

  Recommendation:
    - Deploy second Payment Gateway instance behind load balancer
    - Active-active configuration with health checks
    - Estimated cost: additional infrastructure + licensing
    - Risk reduction: eliminates gateway as failure mode

SPOF #3: Snow Bridge — Single Integration Instance
───────────────────────────────────────────────────
  Current State:
    - Single Python process translating AlertManager → ServiceNow
    - If Snow Bridge fails, alerts still fire but no incident created
    - MTTR increases because NOC must manually check Grafana

  Recommendation:
    - Deploy Snow Bridge as a redundant pair behind a load balancer
    - Add dead-letter queue for alerts that fail to deliver
    - Add heartbeat monitoring for Snow Bridge health
    - Estimated cost: minimal (container duplication)
```

### 4.4 Create Risk Register Entries

Navigate: **All > GRC > Risk > Risk Register** (if GRC is enabled)

If GRC module is not available, create risk entries in a custom table or track them in the CSI Register from Lab 18.

| Field | Value |
|---|---|
| Risk Title | PostgreSQL Primary is a Single Point of Failure |
| Risk Category | Technology |
| Risk Owner | Ravi Kumar |
| Likelihood | High |
| Impact | Critical |
| Risk Score | 20 (5 x 4) |
| Mitigation | Deploy Patroni auto-failover |
| Target Date | 2026-11-30 |
| Related CI | PostgreSQL Primary |
| Related Incidents | INC001, INC003 |

Repeat for each identified SPOF.

---

## Part 5: Availability Dashboard in ServiceNow

### 5.1 Create CI Availability Report (Bar Chart)

Navigate: **All > Reports > Create New**

| Field | Value |
|---|---|
| Report Name | CI Availability — Last 30 Days |
| Source Type | Table |
| Table | Incident [incident] |
| Type | Bar |

**Configure the Report:**

Since ServiceNow does not have a built-in availability percentage field, we will use a combination approach:

1. **Option A: Manual report** — Create a report from a custom table (see Part 8)
2. **Option B: Performance Analytics** — Create PA indicators (recommended)

### 5.2 Performance Analytics — Availability Indicator

Navigate: **All > Performance Analytics > Indicators > Create New**

| Field | Value |
|---|---|
| Name | CI Availability % |
| Direction | Maximize |
| Unit | Percent |
| Precision | 3 |
| Target | 99.95 |
| Warning Threshold | 99.90 |
| Critical Threshold | 99.50 |

> **Note:** PA indicators require data collection jobs. For this lab, we will populate them manually or via background script (see Appendix).

### 5.3 Service Availability Trend (Line Chart)

Create a report showing monthly availability trend:

Navigate: **All > Reports > Create New**

| Field | Value |
|---|---|
| Report Name | UPI Service Availability — Monthly Trend |
| Type | Line |
| Source | Custom table (u_availability_record) |
| Group By | Month |
| Aggregation | Average |
| Metric | Availability % |

Expected trend:

```
Availability %
100.0 ─┬─────────────────────────────────────── SLO: 99.95%
       │                                    ╱
99.8  ─┤                              ╱────
       │                         ╱────
99.6  ─┤                    ╱────
       │               ╱────
99.4  ─┤          ╱────         ← Current: 99.375%
       │     ╱────
99.2  ─┤────
       │
99.0  ─┼────┬────┬────┬────┬────┬────┬────
       Apr  May  Jun  Jul  Aug  Sep  Oct
                                     (projected)

Trend shows improvement but still below SLO.
SPOF remediation (Part 4) is required to reach 99.95%.
```

### 5.4 MTBF and MTTR Reports (Bar Charts)

**MTBF by CI:**

Navigate: **All > Reports > Create New**

| Field | Value |
|---|---|
| Report Name | MTBF by Configuration Item |
| Type | Bar (horizontal) |
| Source | Custom table or calculated data |

```
Expected MTBF Results:
  Load Balancer:           720.0 hrs (no failures) ███████████████████████████
  App Server 2:            720.0 hrs (no failures) ███████████████████████████
  DB Server 2 (Replica):   719.75 hrs              ██████████████████████████
  App Server 1:            719.5 hrs               ██████████████████████████
  Settlement Service:      718.75 hrs              █████████████████████████
  PostgreSQL Primary:      718.0 hrs               █████████████████████████
  UPI Transaction Service: 238.5 hrs (per failure) █████████
```

**MTTR by CI:**

```
Expected MTTR Results:
  DB Server 2 (Replica):   0.25 hrs  █
  App Server 1:            0.50 hrs  ██
  Settlement Service:      0.63 hrs  ██
  UPI Transaction Service: 1.50 hrs  ██████
  PostgreSQL Primary:      2.00 hrs  ████████
                                     ↑
                           PostgreSQL takes longest to restore
                           because manual failover is required
```

### 5.5 Outage Timeline

Create a calendar-style view of incidents impacting availability:

Navigate: **All > Reports > Create New**

| Field | Value |
|---|---|
| Report Name | UPI Outage Calendar — September 2026 |
| Type | Calendar |
| Table | Incident [incident] |
| Date Field | Opened |
| Color | Priority |

```
September 2026 Outage Timeline:
  Mon  Tue  Wed  Thu  Fri  Sat  Sun
                  1    2    3    4    5
                            ██ INC001 (P1, 1.75h)
                            UPI Txn Service
   7    8    9   10   11   12   13
                       ██ INC002 (P2, 0.75h)
                       UPI Txn Service
  14   15   16   17   18   19   20
                            ██ INC003 (P1, 2.0h)
                            PostgreSQL Primary
  21   22   23   24   25   26   27
  (no outages — improvement after changes deployed)
  28   29   30
```

### 5.6 Build Combined Availability Dashboard

Navigate: **All > Self-Service > Dashboards > Create New**

| Field | Value |
|---|---|
| Dashboard Name | UPI Availability & Capacity |
| Layout | 2-column |

Add the following widgets:

```
┌─────────────────────────────────────┬─────────────────────────────────────┐
│  CI Availability (Bar Chart)        │  Service Availability Trend (Line)  │
│                                     │                                     │
│  Shows each CI's uptime %           │  Shows monthly trend with SLO line  │
│  Color: Red < 99.5%, Yellow < 99.95 │  Target: 99.95% horizontal line     │
│         Green >= 99.95%             │                                     │
├─────────────────────────────────────┼─────────────────────────────────────┤
│  MTBF by CI (Bar Chart)             │  MTTR by CI (Bar Chart)             │
│                                     │                                     │
│  Higher is better                   │  Lower is better                    │
│                                     │                                     │
├─────────────────────────────────────┼─────────────────────────────────────┤
│  Outage Calendar (Calendar View)    │  SPOF Risk Register (List)          │
│                                     │                                     │
│  Visual timeline of all outages     │  Active SPOFs with risk scores      │
│                                     │                                     │
└─────────────────────────────────────┴─────────────────────────────────────┘
```

---

## Part 6: Capacity Metrics from Prometheus

### 6.1 Map Prometheus Metrics to Capacity Indicators

The UPI demo stack (from Lab 12) exposes metrics via Spring Boot Actuator and Prometheus. Here is how each metric maps to ITIL capacity management:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Prometheus Metric            │ Capacity Type   │ What It Measures       │
├──────────────────────────────┼─────────────────┼────────────────────────┤
│ process_cpu_usage            │ Component       │ CPU utilization of     │
│                              │                 │ the JVM process        │
│                              │                 │ (0.0 to 1.0)          │
├──────────────────────────────┼─────────────────┼────────────────────────┤
│ jvm_memory_used_bytes        │ Component       │ Current heap/non-heap  │
│ jvm_memory_max_bytes         │                 │ memory usage           │
│ Ratio: used / max            │                 │ (capacity exhaustion   │
│                              │                 │  when ratio → 1.0)    │
├──────────────────────────────┼─────────────────┼────────────────────────┤
│ http_server_requests_        │ Service         │ Transaction throughput │
│ seconds_count                │                 │ (requests per second)  │
│ rate(...[5m])                │                 │                        │
├──────────────────────────────┼─────────────────┼────────────────────────┤
│ http_server_requests_        │ Service         │ Response time (latency)│
│ seconds_sum /                │                 │ Average per interval   │
│ http_server_requests_        │                 │                        │
│ seconds_count                │                 │                        │
├──────────────────────────────┼─────────────────┼────────────────────────┤
│ hikaricp_connections_active  │ Component       │ Active DB connections  │
│ hikaricp_connections_max     │                 │ vs pool maximum        │
│ Ratio: active / max          │                 │ (exhaustion = outage)  │
├──────────────────────────────┼─────────────────┼────────────────────────┤
│ jvm_threads_live_threads     │ Component       │ Active JVM threads     │
│                              │                 │ (thread pool capacity) │
├──────────────────────────────┼─────────────────┼────────────────────────┤
│ disk_free_bytes              │ Component       │ Available disk space   │
│ disk_total_bytes             │                 │ (logs, data growth)    │
└──────────────────────────────┴─────────────────┴────────────────────────┘
```

### 6.2 Query Current Capacity in Grafana

Navigate to Grafana (http://localhost:3000) and run these PromQL queries:

**CPU Utilization:**
```promql
process_cpu_usage{application="upi-transaction-service"} * 100
```
Expected result: 15-35% under normal traffic generator load.

**Memory Utilization:**
```promql
jvm_memory_used_bytes{area="heap", application="upi-transaction-service"}
  /
jvm_memory_max_bytes{area="heap", application="upi-transaction-service"}
  * 100
```
Expected result: 40-65% heap usage.

**Transaction Throughput:**
```promql
rate(http_server_requests_seconds_count{
  application="upi-transaction-service",
  uri="/api/v1/upi/pay"
}[5m]) * 60
```
Expected result: varies based on traffic generator settings (e.g., 30-120 requests/minute).

**Database Connection Pool Utilization:**
```promql
hikaricp_connections_active{application="upi-transaction-service"}
  /
hikaricp_connections_max{application="upi-transaction-service"}
  * 100
```
Expected result: 20-50% under normal load.

### 6.3 Capacity Trending — Identify Growth Patterns

```
Capacity Trending Example:

  CPU Utilization over 3 months (daily average):
  100% ─┬──────────────────────────────────────── Danger Zone
        │
   85% ─┤- - - - - - - - - - - - - - - - - - - - Critical Threshold
        │                                    ╱
   70% ─┤- - - - - - - - - - - - - - -╱- - -  Warning Threshold
        │                         ╱────
   55% ─┤                    ╱────
        │               ╱────
   40% ─┤          ╱────
        │     ╱────
   25% ─┤────
        │
    0% ─┼────┬────┬────┬────┬────┬────┬────┬────┬
        Jul  Aug  Sep  Oct  Nov  Dec  Jan  Feb
                        ↑              ↑
                     Today          Projected
                                   Warning
                                   Breach

  At current growth rate (40% YoY = 2.84% monthly compound):
    Current:  Sep = 42% CPU
    Oct:      43.2%
    Nov:      44.4%
    Dec:      45.7%
    ...
    Warning threshold (70%) reached: approximately June 2027
    Critical threshold (85%) reached: approximately October 2027

  But this assumes LINEAR growth. UPI often sees SPIKES:
    - Diwali season (October): 2-3x normal volume
    - Month-end salary payments: 1.5x normal volume
    - New merchant onboarding campaigns: step-change increase
```

### 6.4 Capacity Forecasting Formula

```
Simple linear forecasting:

  Current_Load = C
  Growth_Rate  = G (monthly, as decimal — e.g., 0.0284 for 2.84%)
  Threshold    = T (e.g., 0.70 for 70%)

  Months_to_threshold = ln(T / C) / ln(1 + G)

  Example:
    C = 0.42 (42% CPU)
    G = 0.0284 (2.84% monthly)
    T = 0.70 (70% warning)

    Months = ln(0.70 / 0.42) / ln(1.0284)
           = ln(1.667) / ln(1.0284)
           = 0.5108 / 0.0280
           = 18.24 months ≈ June 2028

  With Diwali spike factor (2x in October each year):
    Need headroom by October 2027 → only 13 months away
    Effective planning horizon: scale by August 2027
```

---

## Part 7: Capacity Planning

### 7.1 Current Capacity Assessment

```
UPI Platform — Current Capacity Baseline (September 2026)
═════════════════════════════════════════════════════════════

Component                 │ Metric          │ Current │ Warning │ Critical
──────────────────────────┼─────────────────┼─────────┼─────────┼─────────
App Server 1              │ CPU %           │ 42%     │ 70%     │ 85%
App Server 1              │ Memory %        │ 61%     │ 80%     │ 90%
App Server 2              │ CPU %           │ 38%     │ 70%     │ 85%
App Server 2              │ Memory %        │ 58%     │ 80%     │ 90%
PostgreSQL Primary        │ CPU %           │ 35%     │ 70%     │ 85%
PostgreSQL Primary        │ Storage %       │ 55%     │ 80%     │ 90%
PostgreSQL Primary        │ Connections %   │ 45%     │ 80%     │ 90%
PostgreSQL Replica        │ CPU %           │ 20%     │ 70%     │ 85%
PostgreSQL Replica        │ Repl Lag (sec)  │ 0.5     │ 5.0     │ 30.0
Load Balancer             │ Throughput (rps)│ 850     │ 2000    │ 2500
UPI Transaction Service   │ P95 Latency (ms)│ 320    │ 500     │ 1000
UPI Settlement Service    │ P95 Latency (ms)│ 450    │ 500     │ 1000

Overall Assessment: ADEQUATE for current load, but limited headroom
                    for seasonal spikes.
```

### 7.2 Growth Projections

```
UPI Transaction Growth Data:
  FY 2023-24:  7.1 billion transactions/month
  FY 2024-25:  10.2 billion transactions/month (43.7% growth)
  FY 2025-26:  14.5 billion transactions/month (42.2% growth — estimated)
  FY 2026-27:  20.3 billion transactions/month (40% growth — projected)

For our demo platform, scale proportionally:
  Current throughput:     850 requests/second (peak)
  Projected (12 months):  1,190 requests/second (40% growth)
  Projected (24 months):  1,666 requests/second (compound growth)

Resource Impact Projections:
┌──────────────────────┬─────────┬──────────┬──────────┬──────────┐
│ Resource             │ Current │ +6 months│ +12 months│ +24 months│
├──────────────────────┼─────────┼──────────┼──────────┼──────────┤
│ App Server CPU       │ 42%     │ 50%      │ 59%      │ 82%      │
│ App Server Memory    │ 61%     │ 67%      │ 74%      │ 87%      │
│ DB CPU               │ 35%     │ 42%      │ 49%      │ 69%      │
│ DB Storage           │ 55%     │ 63%      │ 72%      │ 89%      │
│ DB Connections       │ 45%     │ 52%      │ 60%      │ 81%      │
│ Network Bandwidth    │ 30%     │ 36%      │ 42%      │ 59%      │
└──────────────────────┴─────────┴──────────┴──────────┴──────────┘

CRITICAL FINDINGS:
  1. App Server Memory breaches WARNING (80%) at ~14 months
  2. DB Storage breaches WARNING (80%) at ~15 months
  3. DB Connections breach WARNING (80%) at ~20 months
  4. App Server CPU breaches CRITICAL (85%) at ~22 months
  5. Diwali 2027 spike (2x) could cause CRITICAL breach in ~13 months
```

### 7.3 Capacity Threshold Alerts

Configure alerts in Prometheus/Grafana for proactive capacity management:

**Alert Rule: CPU Warning**
```yaml
# In Prometheus alerting rules (prometheus-rules.yml)
groups:
  - name: capacity_alerts
    rules:
      - alert: CPU_Warning
        expr: process_cpu_usage > 0.70
        for: 15m
        labels:
          severity: warning
          practice: capacity_management
        annotations:
          summary: "CPU utilization above 70% for {{ $labels.application }}"
          description: "CPU at {{ $value | humanizePercentage }} for 15+ minutes"

      - alert: CPU_Critical
        expr: process_cpu_usage > 0.85
        for: 5m
        labels:
          severity: critical
          practice: capacity_management
        annotations:
          summary: "CPU utilization above 85% for {{ $labels.application }}"

      - alert: Memory_Warning
        expr: |
          jvm_memory_used_bytes{area="heap"}
          / jvm_memory_max_bytes{area="heap"} > 0.80
        for: 10m
        labels:
          severity: warning
          practice: capacity_management
        annotations:
          summary: "Heap memory above 80% for {{ $labels.application }}"

      - alert: DB_Connection_Pool_Warning
        expr: |
          hikaricp_connections_active
          / hikaricp_connections_max > 0.80
        for: 5m
        labels:
          severity: warning
          practice: capacity_management
        annotations:
          summary: "DB connection pool above 80% for {{ $labels.application }}"
```

### 7.4 Right-Sizing Recommendations

```
Based on capacity assessment and growth projections:

┌─────┬────────────────────────────┬───────────────┬──────────────────────────┐
│ Pri │ Recommendation             │ Timeline      │ Cost Impact              │
├─────┼────────────────────────────┼───────────────┼──────────────────────────┤
│  1  │ Add App Server 3           │ Before        │ +33% app server cost     │
│     │ (horizontal scaling)       │ Diwali 2027   │ Offsets CPU + memory     │
│     │                            │ (Oct 2027)    │ projections              │
├─────┼────────────────────────────┼───────────────┼──────────────────────────┤
│  2  │ Increase DB storage        │ Within        │ +50% storage allocation  │
│     │ allocation                 │ 6 months      │ Prevents storage breach  │
├─────┼────────────────────────────┼───────────────┼──────────────────────────┤
│  3  │ Increase DB connection     │ Within        │ Minimal — config change  │
│     │ pool max from 20 to 30     │ 3 months      │ May need more DB memory  │
├─────┼────────────────────────────┼───────────────┼──────────────────────────┤
│  4  │ Enable read replicas for   │ Within        │ +50% DB read capacity    │
│     │ read-heavy queries         │ 6 months      │ Offloads primary         │
├─────┼────────────────────────────┼───────────────┼──────────────────────────┤
│  5  │ Implement response caching │ Within        │ -30% DB load             │
│     │ (Redis) for merchant data  │ 6 months      │ Requires new CI in CMDB  │
├─────┼────────────────────────────┼───────────────┼──────────────────────────┤
│  6  │ Review JVM heap settings   │ Immediate     │ Zero cost — tuning only  │
│     │ (current: -Xmx512m,        │               │ Increase to -Xmx768m    │
│     │  recommend: -Xmx768m)     │               │                          │
└─────┴────────────────────────────┴───────────────┴──────────────────────────┘

Estimated annual cost of scaling plan: ~20% increase in infrastructure spend
Cost of NOT scaling (potential Diwali outage):
  - Revenue loss: ~INR 2-5 crore per hour of downtime
  - Reputational damage: significant (national payment infrastructure)
  - Regulatory penalties: RBI mandates 99.5% minimum for payment systems
```

---

## Part 8: Create Availability & Capacity Records in ServiceNow

### 8.1 Create Custom Table for Availability Records

Navigate: **All > System Definition > Tables > New**

| Field | Value |
|---|---|
| Label | Availability Record |
| Name | u_availability_record |
| Extends table | Task [task] |
| Create module | Yes |
| Module category | ITSM Custom |

**Add Columns:**

| Column Label | Column Name | Type | Max Length | Reference |
|---|---|---|---|---|
| Configuration Item | u_configuration_item | Reference | — | cmdb_ci |
| Measurement Period Start | u_period_start | Date/Time | — | — |
| Measurement Period End | u_period_end | Date/Time | — | — |
| Agreed Service Time (hours) | u_ast_hours | Decimal | — | — |
| Downtime (hours) | u_downtime_hours | Decimal | — | — |
| Availability Percentage | u_availability_pct | Decimal | — | — |
| SLO Target (%) | u_slo_target_pct | Decimal | — | — |
| SLO Status | u_slo_status | Choice | — | — |
| Number of Failures | u_failure_count | Integer | — | — |
| MTBF (hours) | u_mtbf_hours | Decimal | — | — |
| MTRS (hours) | u_mtrs_hours | Decimal | — | — |

**SLO Status Choice Values:**

| Value | Label |
|---|---|
| met | Met |
| breach | Breach |
| warning | Warning |

### 8.2 Create Custom Table for Capacity Records

Navigate: **All > System Definition > Tables > New**

| Field | Value |
|---|---|
| Label | Capacity Record |
| Name | u_capacity_record |
| Extends table | Task [task] |
| Create module | Yes |

**Add Columns:**

| Column Label | Column Name | Type | Reference |
|---|---|---|---|
| Configuration Item | u_configuration_item | Reference | cmdb_ci |
| Measurement Date | u_measurement_date | Date/Time | — |
| Metric Name | u_metric_name | String | — |
| Current Value | u_current_value | Decimal | — |
| Warning Threshold | u_warning_threshold | Decimal | — |
| Critical Threshold | u_critical_threshold | Decimal | — |
| Unit | u_unit | String | — |
| Capacity Status | u_capacity_status | Choice | — |
| Projected Exhaustion Date | u_projected_exhaustion | Date | — |
| Growth Rate (% monthly) | u_growth_rate_pct | Decimal | — |

**Capacity Status Choice Values:**

| Value | Label |
|---|---|
| normal | Normal |
| warning | Warning |
| critical | Critical |
| exhausted | Exhausted |

### 8.3 Create Business Rule for Auto-Calculation

Navigate: **All > System Definition > Business Rules > New**

| Field | Value |
|---|---|
| Name | Calculate Availability Metrics |
| Table | Availability Record [u_availability_record] |
| When | before |
| Insert | Yes |
| Update | Yes |

**Script:**

```javascript
(function executeRule(current, previous) {

    // Auto-calculate availability percentage
    if (current.u_ast_hours > 0) {
        var ast = parseFloat(current.u_ast_hours);
        var dt = parseFloat(current.u_downtime_hours);
        var availability = ((ast - dt) / ast) * 100;
        current.u_availability_pct = availability.toFixed(4);

        // Calculate MTBF and MTRS if failure count is provided
        var failures = parseInt(current.u_failure_count);
        if (failures > 0) {
            current.u_mtbf_hours = ((ast - dt) / failures).toFixed(2);
            current.u_mtrs_hours = (dt / failures).toFixed(2);
        } else {
            current.u_mtbf_hours = ast;
            current.u_mtrs_hours = 0;
        }

        // Determine SLO status
        var sloTarget = parseFloat(current.u_slo_target_pct);
        if (availability >= sloTarget) {
            current.u_slo_status = 'met';
        } else if (availability >= sloTarget - 0.5) {
            current.u_slo_status = 'warning';
        } else {
            current.u_slo_status = 'breach';
        }
    }

})(current, previous);
```

### 8.4 Populate Availability Records

Create records for each CI. Navigate: **All > ITSM Custom > Availability Records > New**

**Record 1: UPI Transaction Service**

| Field | Value |
|---|---|
| Configuration Item | UPI Transaction Service |
| Measurement Period Start | 2026-09-01 00:00:00 |
| Measurement Period End | 2026-09-30 23:59:59 |
| Agreed Service Time (hours) | 720 |
| Downtime (hours) | 4.50 |
| SLO Target (%) | 99.95 |
| Number of Failures | 3 |

> The business rule will auto-calculate: Availability = 99.3750%, MTBF = 238.50, MTRS = 1.50, SLO Status = Breach

**Record 2: UPI Settlement Service**

| Field | Value |
|---|---|
| Configuration Item | UPI Settlement Service |
| Measurement Period Start | 2026-09-01 00:00:00 |
| Measurement Period End | 2026-09-30 23:59:59 |
| Agreed Service Time (hours) | 720 |
| Downtime (hours) | 1.25 |
| SLO Target (%) | 99.95 |
| Number of Failures | 2 |

**Record 3: PostgreSQL Primary**

| Field | Value |
|---|---|
| Configuration Item | PostgreSQL Primary |
| Measurement Period Start | 2026-09-01 00:00:00 |
| Measurement Period End | 2026-09-30 23:59:59 |
| Agreed Service Time (hours) | 720 |
| Downtime (hours) | 2.00 |
| SLO Target (%) | 99.95 |
| Number of Failures | 1 |

Create similar records for Load Balancer (DT=0), App Servers, and DB Servers.

### 8.5 Populate Capacity Records

Navigate: **All > ITSM Custom > Capacity Records > New**

**Record 1: App Server 1 — CPU**

| Field | Value |
|---|---|
| Configuration Item | App Server 1 |
| Measurement Date | 2026-09-23 |
| Metric Name | CPU Utilization |
| Current Value | 42.0 |
| Warning Threshold | 70.0 |
| Critical Threshold | 85.0 |
| Unit | Percent |
| Capacity Status | Normal |
| Growth Rate (% monthly) | 2.84 |
| Projected Exhaustion Date | 2028-06-01 |

Create additional records for memory, DB connections, storage, and other metrics for each CI.

---

## Practice Exercises

### Exercise 1: Calculate Settlement Service Availability

Using the following incident data for **UPI Settlement Service** in September 2026, calculate:

```
Incident Data:
  INC-S01: Sep 08, 06:30 to 07:15 (0.75 hours)
  INC-S02: Sep 22, 23:00 to 23:30 (0.50 hours)

Calculate:
  a) Total downtime in hours
  b) Availability percentage (AST = 720 hours)
  c) MTBF
  d) MTRS
  e) Is the 99.95% SLO met?
  f) How much downtime budget remains for the month?
```

**Expected Answers:**

```
  a) Total downtime = 0.75 + 0.50 = 1.25 hours
  b) Availability = (720 - 1.25) / 720 x 100 = 99.826%
  c) MTBF = (720 - 1.25) / 2 = 359.375 hours
  d) MTRS = 1.25 / 2 = 0.625 hours (37.5 minutes)
  e) SLO NOT met: 99.826% < 99.95% (shortfall of 0.124%)
  f) Monthly budget at 99.95% = 720 x 0.0005 = 0.36 hours (21.6 min)
     Used: 1.25 hours — budget exceeded by 0.89 hours (53.4 minutes)
```

### Exercise 2: Identify SPOFs and Propose Solutions

Review the UPI CMDB relationship map and:

```
  a) List 3 Single Points of Failure not already discussed
  b) For each, explain the failure scenario
  c) Propose a redundancy solution
  d) Estimate the availability improvement if each SPOF is resolved
  e) Calculate the combined service availability after all fixes
```

**Hint:** Consider DNS, NTP, certificate management, monitoring pipeline, and the ServiceNow instance itself as potential SPOFs.

### Exercise 3: Capacity Trending Report

Using the following monthly CPU data for App Server 1:

```
  April 2026:  28%
  May 2026:    31%
  June 2026:   33%
  July 2026:   36%
  August 2026: 39%
  September:   42%

  a) Calculate the average monthly growth rate
  b) Using the formula: months = ln(threshold/current) / ln(1 + growth_rate),
     predict when CPU will hit 70% warning threshold
  c) Predict when CPU will hit 85% critical threshold
  d) Factor in a Diwali spike (2x load in October): will any threshold
     be breached during the spike?
  e) Recommend scaling actions with timelines
```

### Exercise 4: Availability SLA Dashboard

Build a ServiceNow dashboard that shows:

```
  a) A single-score widget showing overall UPI service availability
  b) A bar chart comparing each CI's availability against the SLO target
  c) A trend line showing month-over-month availability improvement
  d) A list widget showing all SLO breaches with root cause
  e) A pie chart showing downtime by root cause category
```

### Exercise 5: Disaster Recovery Plan from CMDB Dependencies

Using the CMDB service map, design a DR plan:

```
  a) Identify the Recovery Time Objective (RTO) for each CI based on
     its MTRS from incident data
  b) Identify the Recovery Point Objective (RPO) for data-bearing CIs
     (PostgreSQL — what is the replication lag?)
  c) Define recovery sequence based on dependency order:
     What must come up first? What depends on what?
  d) Document the DR runbook as a ServiceNow Knowledge article
  e) Calculate the theoretical maximum RTO for full service restoration
     given serial dependencies
```

---

## Lab Summary

### What You Accomplished

```
1. AVAILABILITY MANAGEMENT
   ├── Learned availability metrics: MTBF, MTRS, MTTR, MTBSI
   ├── Calculated availability from incident data per CI
   ├── Identified SLO breaches (99.375% vs 99.95% target)
   ├── Performed SPOF analysis on UPI architecture
   ├── Built availability dashboards and reports
   └── Created custom availability tracking in ServiceNow

2. CAPACITY MANAGEMENT
   ├── Mapped Prometheus metrics to capacity indicators
   ├── Assessed current capacity baselines
   ├── Projected resource exhaustion timelines
   ├── Configured capacity threshold alerts
   ├── Developed right-sizing recommendations
   └── Created custom capacity tracking in ServiceNow

3. KEY FINDINGS FOR UPI PLATFORM
   ├── UPI Transaction Service: 99.375% (BELOW 99.95% SLO)
   ├── 4 critical SPOFs identified with remediation plans
   ├── CPU warning threshold projected at ~18 months
   ├── Diwali 2027 spike risk requires scaling by August 2027
   └── Infrastructure cost increase of ~20% recommended
```

### Why This Matters

```
Availability Management ensures:
  → Services meet agreed uptime targets
  → SPOFs are identified and eliminated BEFORE they cause outages
  → Downtime trends are tracked and reduced over time
  → Investment in redundancy is justified with data

Capacity Management ensures:
  → Infrastructure scales ahead of demand
  → Cost optimization — no over-provisioning
  → Seasonal spikes are anticipated and handled
  → Growth projections drive procurement timelines
```

---

## Key Concepts

| Term | Definition | UPI Example |
|---|---|---|
| Availability | (AST - DT) / AST x 100 | 99.375% for UPI Transaction Service |
| AST | Agreed Service Time | 720 hours/month (24x7) |
| DT | Downtime | 4.5 hours total in September |
| MTBF | Mean Time Between Failures | 238.5 hours for UPI Transaction Service |
| MTRS | Mean Time to Restore Service | 1.5 hours average restoration time |
| MTTR | Mean Time to Repair | Time to fix the component (subset of MTRS) |
| MTBSI | Mean Time Between System Incidents | MTBF + MTRS = 240 hours |
| VBF | Vital Business Function | Transaction processing, settlements |
| SPOF | Single Point of Failure | PostgreSQL Primary (no auto-failover) |
| Component Availability | Uptime of individual CI | PostgreSQL: 99.722% |
| Service Availability | End-to-end availability | Product of serial components |
| Capacity Planning | Forecasting resource needs | CPU exhaustion in 18 months |
| Right-Sizing | Matching resources to demand | Add App Server 3 before Diwali |
| RTO | Recovery Time Objective | Maximum acceptable restoration time |
| RPO | Recovery Point Objective | Maximum acceptable data loss |

---

## What's Next

```
Lab 19 (this lab) measured WHERE we stand — availability gaps and capacity limits.

Next: Phase 5 — Automate & Integrate
  Lab 20: Flow Designer & Workflow Automation
    → Automate the availability calculations (scheduled flow)
    → Auto-create capacity alerts as incidents
    → SLA breach escalation workflows
    → Connect capacity thresholds to change requests

The insights from this lab feed directly into automation:
  - SPOF remediation → becomes Change Requests (Lab 15 process)
  - Capacity scaling → becomes Service Catalog items (Lab 11)
  - Availability trends → feed CSI register (Lab 18)
  - Threshold alerts → auto-create incidents (Lab 13 pipeline)
```

---

## Appendix: Background Script — Generate Availability & Capacity Data

Navigate: **All > System Definition > Scripts - Background**

### Script 1: Generate Availability Records

```javascript
// ============================================================
// Lab 19: Generate Availability Records for UPI CIs
// Run in: Scripts - Background (Scope: Global)
// ============================================================

(function() {
    gs.info('=== Lab 19: Generating Availability Records ===');

    // Define CI availability data for September 2026
    var availabilityData = [
        {
            ci_name: 'UPI Transaction Service',
            ast: 720,
            downtime: 4.50,
            failures: 3,
            slo_target: 99.95
        },
        {
            ci_name: 'UPI Settlement Service',
            ast: 720,
            downtime: 1.25,
            failures: 2,
            slo_target: 99.95
        },
        {
            ci_name: 'PostgreSQL Primary',
            ast: 720,
            downtime: 2.00,
            failures: 1,
            slo_target: 99.95
        },
        {
            ci_name: 'Load Balancer',
            ast: 720,
            downtime: 0.00,
            failures: 0,
            slo_target: 99.95
        },
        {
            ci_name: 'App Server 1',
            ast: 720,
            downtime: 0.50,
            failures: 1,
            slo_target: 99.95
        },
        {
            ci_name: 'App Server 2',
            ast: 720,
            downtime: 0.00,
            failures: 0,
            slo_target: 99.95
        },
        {
            ci_name: 'DB Server 1',
            ast: 720,
            downtime: 2.00,
            failures: 1,
            slo_target: 99.95
        },
        {
            ci_name: 'DB Server 2',
            ast: 720,
            downtime: 0.25,
            failures: 1,
            slo_target: 99.95
        }
    ];

    for (var i = 0; i < availabilityData.length; i++) {
        var data = availabilityData[i];

        // Find the CI in CMDB
        var ciGR = new GlideRecord('cmdb_ci');
        ciGR.addQuery('name', data.ci_name);
        ciGR.query();

        var ciSysId = '';
        if (ciGR.next()) {
            ciSysId = ciGR.sys_id.toString();
        } else {
            gs.warn('CI not found: ' + data.ci_name + ' — creating record without CI link');
        }

        // Calculate metrics
        var availability = ((data.ast - data.downtime) / data.ast) * 100;
        var mtbf = data.failures > 0 ? ((data.ast - data.downtime) / data.failures) : data.ast;
        var mtrs = data.failures > 0 ? (data.downtime / data.failures) : 0;
        var sloStatus = availability >= data.slo_target ? 'met' :
                        availability >= (data.slo_target - 0.5) ? 'warning' : 'breach';

        // Create availability record
        var ar = new GlideRecord('u_availability_record');
        ar.initialize();
        ar.short_description = 'Availability — ' + data.ci_name + ' — Sep 2026';
        if (ciSysId) {
            ar.u_configuration_item = ciSysId;
        }
        ar.u_period_start = '2026-09-01 00:00:00';
        ar.u_period_end = '2026-09-30 23:59:59';
        ar.u_ast_hours = data.ast;
        ar.u_downtime_hours = data.downtime;
        ar.u_availability_pct = availability.toFixed(4);
        ar.u_slo_target_pct = data.slo_target;
        ar.u_slo_status = sloStatus;
        ar.u_failure_count = data.failures;
        ar.u_mtbf_hours = mtbf.toFixed(2);
        ar.u_mtrs_hours = mtrs.toFixed(2);
        ar.insert();

        gs.info('Created availability record: ' + data.ci_name +
                ' | Avail: ' + availability.toFixed(4) + '%' +
                ' | MTBF: ' + mtbf.toFixed(2) + 'h' +
                ' | MTRS: ' + mtrs.toFixed(2) + 'h' +
                ' | SLO: ' + sloStatus);
    }

    gs.info('=== Availability Records Created Successfully ===');
})();
```

### Script 2: Generate Capacity Records

```javascript
// ============================================================
// Lab 19: Generate Capacity Records for UPI CIs
// Run in: Scripts - Background (Scope: Global)
// ============================================================

(function() {
    gs.info('=== Lab 19: Generating Capacity Records ===');

    var capacityData = [
        // App Server 1
        { ci: 'App Server 1', metric: 'CPU Utilization', value: 42.0,
          warn: 70.0, crit: 85.0, unit: 'Percent', growth: 2.84,
          exhaustion: '2028-06-01' },
        { ci: 'App Server 1', metric: 'Memory Utilization', value: 61.0,
          warn: 80.0, crit: 90.0, unit: 'Percent', growth: 2.10,
          exhaustion: '2028-01-01' },

        // App Server 2
        { ci: 'App Server 2', metric: 'CPU Utilization', value: 38.0,
          warn: 70.0, crit: 85.0, unit: 'Percent', growth: 2.84,
          exhaustion: '2028-08-01' },
        { ci: 'App Server 2', metric: 'Memory Utilization', value: 58.0,
          warn: 80.0, crit: 90.0, unit: 'Percent', growth: 2.10,
          exhaustion: '2028-03-01' },

        // PostgreSQL Primary
        { ci: 'PostgreSQL Primary', metric: 'CPU Utilization', value: 35.0,
          warn: 70.0, crit: 85.0, unit: 'Percent', growth: 3.20,
          exhaustion: '2028-07-01' },
        { ci: 'PostgreSQL Primary', metric: 'Storage Utilization', value: 55.0,
          warn: 80.0, crit: 90.0, unit: 'Percent', growth: 4.50,
          exhaustion: '2027-06-01' },
        { ci: 'PostgreSQL Primary', metric: 'Connection Pool', value: 45.0,
          warn: 80.0, crit: 90.0, unit: 'Percent', growth: 2.50,
          exhaustion: '2028-09-01' },

        // PostgreSQL Replica
        { ci: 'PostgreSQL Replica', metric: 'CPU Utilization', value: 20.0,
          warn: 70.0, crit: 85.0, unit: 'Percent', growth: 3.20,
          exhaustion: '2029-06-01' },
        { ci: 'PostgreSQL Replica', metric: 'Replication Lag', value: 0.5,
          warn: 5.0, crit: 30.0, unit: 'Seconds', growth: 0.50,
          exhaustion: '2030-01-01' },

        // Load Balancer
        { ci: 'Load Balancer', metric: 'Throughput', value: 850,
          warn: 2000, crit: 2500, unit: 'req/sec', growth: 2.84,
          exhaustion: '2029-01-01' },

        // Services
        { ci: 'UPI Transaction Service', metric: 'P95 Latency', value: 320,
          warn: 500, crit: 1000, unit: 'ms', growth: 1.50,
          exhaustion: '2028-12-01' },
        { ci: 'UPI Settlement Service', metric: 'P95 Latency', value: 450,
          warn: 500, crit: 1000, unit: 'ms', growth: 1.50,
          exhaustion: '2027-02-01' }
    ];

    for (var i = 0; i < capacityData.length; i++) {
        var data = capacityData[i];

        // Find CI
        var ciGR = new GlideRecord('cmdb_ci');
        ciGR.addQuery('name', data.ci);
        ciGR.query();
        var ciSysId = ciGR.next() ? ciGR.sys_id.toString() : '';

        // Determine status
        var status = 'normal';
        if (data.value >= data.crit) {
            status = 'critical';
        } else if (data.value >= data.warn) {
            status = 'warning';
        }

        // Create capacity record
        var cr = new GlideRecord('u_capacity_record');
        cr.initialize();
        cr.short_description = 'Capacity — ' + data.ci + ' — ' + data.metric;
        if (ciSysId) {
            cr.u_configuration_item = ciSysId;
        }
        cr.u_measurement_date = '2026-09-23 12:00:00';
        cr.u_metric_name = data.metric;
        cr.u_current_value = data.value;
        cr.u_warning_threshold = data.warn;
        cr.u_critical_threshold = data.crit;
        cr.u_unit = data.unit;
        cr.u_capacity_status = status;
        cr.u_projected_exhaustion = data.exhaustion;
        cr.u_growth_rate_pct = data.growth;
        cr.insert();

        gs.info('Created capacity record: ' + data.ci +
                ' | ' + data.metric + ': ' + data.value + ' ' + data.unit +
                ' | Status: ' + status);
    }

    gs.info('=== Capacity Records Created Successfully ===');
})();
```

### Script 3: Availability Summary Report

```javascript
// ============================================================
// Lab 19: Generate Availability Summary Report
// Run in: Scripts - Background (Scope: Global)
// Outputs a formatted availability report to system log
// ============================================================

(function() {
    gs.info('');
    gs.info('╔══════════════════════════════════════════════════════════════╗');
    gs.info('║     UPI PLATFORM — AVAILABILITY REPORT — SEPTEMBER 2026    ║');
    gs.info('╠══════════════════════════════════════════════════════════════╣');

    var gr = new GlideRecord('u_availability_record');
    gr.addQuery('u_period_start', '>=', '2026-09-01');
    gr.addQuery('u_period_end', '<=', '2026-09-30 23:59:59');
    gr.orderBy('u_availability_pct');
    gr.query();

    var totalAST = 0;
    var totalDT = 0;
    var totalFailures = 0;
    var breachCount = 0;
    var ciCount = 0;

    while (gr.next()) {
        ciCount++;
        var ast = parseFloat(gr.u_ast_hours);
        var dt = parseFloat(gr.u_downtime_hours);
        var avail = parseFloat(gr.u_availability_pct);
        var status = gr.u_slo_status.toString().toUpperCase();
        var ciName = gr.u_configuration_item.getDisplayValue() || gr.short_description;

        totalAST += ast;
        totalDT += dt;
        totalFailures += parseInt(gr.u_failure_count);
        if (status === 'BREACH') breachCount++;

        var statusIcon = status === 'MET' ? '[OK]' : '[!!]';
        gs.info('║  ' + statusIcon + ' ' + ciName);
        gs.info('║       Availability: ' + avail.toFixed(4) + '% | ' +
                'DT: ' + dt + 'h | ' +
                'MTBF: ' + gr.u_mtbf_hours + 'h | ' +
                'MTRS: ' + gr.u_mtrs_hours + 'h');
    }

    gs.info('╠══════════════════════════════════════════════════════════════╣');
    var overallAvail = totalAST > 0 ? ((totalAST - totalDT) / totalAST * 100) : 0;
    gs.info('║  SUMMARY:');
    gs.info('║    CIs Monitored:     ' + ciCount);
    gs.info('║    SLO Breaches:      ' + breachCount + ' of ' + ciCount);
    gs.info('║    Total Downtime:    ' + totalDT.toFixed(2) + ' hours');
    gs.info('║    Total Failures:    ' + totalFailures);
    gs.info('║    Overall Avail:     ' + overallAvail.toFixed(4) + '%');
    gs.info('║    SLO Target:        99.9500%');
    gs.info('║    Status:            ' + (overallAvail >= 99.95 ? 'MET' : 'BREACH'));
    gs.info('╚══════════════════════════════════════════════════════════════╝');
    gs.info('');
})();
```

---

**End of Lab 19**
