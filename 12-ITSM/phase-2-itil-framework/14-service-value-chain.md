# Section 14: Service Value Chain

## What is the Service Value Chain?

The 6 interconnected activities that an organization performs to **convert demand into value**.

Think of it as: **"The assembly line inside the SVS -- but unlike a factory, steps can happen in any order, skip steps, or loop back."**

---

## The 6 Activities

```
         +----------+
         |   PLAN   |
         +----+-----+
              |
    +---------+---------+
    |                   |
+---v----+        +-----v------+
| IMPROVE|        |   ENGAGE   |
+---+----+        +-----+------+
    |                   |
    |         +---------+---------+
    |         |                   |
    |   +-----v-------+    +-----v--------+
    |   | DESIGN &    |    | OBTAIN /     |
    |   | TRANSITION  |    | BUILD        |
    |   +-----+-------+    +-----+--------+
    |         |                   |
    |         +---------+---------+
    |                   |
    |            +------v--------+
    |            | DELIVER &     |
    +----------->| SUPPORT       |
                 +---------------+
```

**Key insight:** This is NOT a linear pipeline. Different value streams take different paths through these activities.

---

## Activity 1: PLAN

**Purpose:** Ensure a shared understanding of the vision, current status, and direction for all services.

| Question it answers | UPI Example |
|---|---|
| Where are we now? | "Current UPI success rate: 99.2%" |
| Where do we want to be? | "Target: 99.9% by Q4" |
| How do we get there? | "Fix top 3 failing bank integrations, add circuit breakers" |
| What resources do we need? | "2 platform engineers, Kafka upgrade budget, 6 weeks" |

### UPI Scenario

```
NPCI Annual Planning:

Portfolio of services:
  - UPI Payments: Healthy (99.4%), focus on international expansion
  - UPI Lite: Struggling (85%), needs urgent reliability work
  - Settlement: Stable (99.9%), optimize for speed
  - Dispute Resolution: Backlog growing, need automation

Resource allocation:
  - 40% of engineering -> UPI Lite reliability (highest priority)
  - 25% -> International UPI (strategic opportunity)
  - 20% -> Dispute automation
  - 15% -> BAU operations
```

**Inputs:** Policies, strategies, demand from Engage, improvement from Improve
**Outputs:** Strategic/tactical plans, portfolio decisions, architecture decisions

---

## Activity 2: IMPROVE

**Purpose:** Ensure continual improvement of products, services, and practices across ALL value chain activities.

| What it does | UPI Example |
|---|---|
| Identify improvement opportunities | "P1 incidents take 28 min avg -- industry best is 12 min" |
| Prioritize improvements | CSI register ranked by impact |
| Track improvement initiatives | Dashboard showing progress of all CSI items |
| Measure results | "After auto-escalation, P1 MTTR dropped to 14 min" |

**Key:** Improve doesn't just improve services -- it improves **how you Plan, Engage, Design, Build, and Deliver**.

```
Improve applies to:
  +-- Plan: "Are we planning effectively?"
  +-- Engage: "Are we communicating well with banks?"
  +-- Design: "Are our architecture reviews thorough?"
  +-- Obtain/Build: "Is our CI/CD pipeline fast enough?"
  +-- Deliver: "Is our incident process efficient?"
  +-- Improve itself: "Are we picking the right improvements?"
```

---

## Activity 3: ENGAGE

**Purpose:** Understand stakeholder needs, ensure transparency, and maintain good relationships.

| Stakeholder | How NPCI Engages |
|---|---|
| **Banks** | Quarterly business reviews, API portal, support tickets |
| **PSPs (PhonePe, GPay)** | Developer portal, sandbox testing, integration support |
| **RBI (regulator)** | Compliance reports, audit responses, incident notifications |
| **Internal teams** | Sprint reviews, architecture councils, war rooms |
| **End users** | Via banks/PSPs -- NPCI doesn't engage end users directly |

### UPI Scenario

```
PhonePe reaches out:
  "Our users are complaining about UPI Lite failures.
   Can we get a dedicated support channel and weekly status updates?"

Engage activity:
  - Acknowledge the request
  - Understand the need (not just "fix failures" but "keep us informed")
  - Set up weekly sync calls
  - Share real-time dashboard access
  - Feed the technical requirement into Design & Transition
```

**Inputs:** Demand from consumers, feedback, incidents, requests
**Outputs:** Requirements for Design, demand prioritized for Plan, service requests for Deliver

---

## Activity 4: DESIGN & TRANSITION

**Purpose:** Ensure services are designed to meet quality expectations and smoothly transitioned into production.

| Design | Transition |
|---|---|
| "How should UPI Lite's retry logic work?" | "How do we deploy it without breaking current UPI?" |
| Architecture, APIs, data models | Testing, staging, deployment plans, rollback |
| "What should it look like?" | "How do we get it into production safely?" |

### UPI Scenario

```
Design:
  - Circuit breaker pattern: trip after 10 failures in 60s
  - Retry: exponential backoff, max 3 attempts, idempotent only
  - Fallback: route to backup PSP node when circuit open
  - Monitoring: new Grafana dashboard for circuit breaker state

Transition:
  - Deploy to staging -> run 1M synthetic transactions
  - Canary deployment: 5% traffic -> monitor 24 hours
  - Rollback plan: revert feature flag in < 2 min
  - Update CMDB with new circuit breaker component
  - Update runbooks in knowledge base
  - Train NOC on new alert patterns
```

**Inputs:** Requirements from Engage, architecture from Plan
**Outputs:** Tested, deployment-ready components for Obtain/Build and Deliver

---

## Activity 5: OBTAIN / BUILD

**Purpose:** Ensure service components are available -- whether built in-house, bought, or sourced from partners.

| Obtain (Buy/Source) | Build (Create) |
|---|---|
| Purchase Kafka license | Write the circuit breaker code |
| Contract with cloud provider | Build the Grafana dashboard |
| Onboard a new bank's API | Develop automated test suite |
| Hire additional SREs | Create deployment scripts |

### UPI Scenario

```
Obtain:
  - Procure additional Kafka nodes from cloud provider (3-day lead time)
  - Get Axis Bank to provide updated API specs (dependency on external party)
  - License for new APM tool (PagerDuty)

Build:
  - Develop circuit breaker module (Sprint 1: 2 weeks)
  - Build retry logic with idempotency checks (Sprint 1)
  - Create automated integration tests (Sprint 2)
  - Build monitoring dashboards (Sprint 2)
  - Write runbooks and KB articles (Sprint 2)
```

**Inputs:** Designs from Design & Transition, architecture decisions
**Outputs:** Built/acquired components ready for Deliver & Support

---

## Activity 6: DELIVER & SUPPORT

**Purpose:** Ensure services are delivered and supported according to agreed SLAs.

This is where **day-to-day operations** happen -- the biggest activity by volume.

| Deliver | Support |
|---|---|
| Deploy to production | Handle incidents |
| Fulfill service requests | Resolve problems |
| Operate services 24/7 | Manage escalations |
| Monitor SLIs | Communicate with stakeholders |

### UPI Scenario -- A Typical Day

```
06:00  Settlement batch completed, reports generated (Deliver)
08:00  NOC shift handover, review overnight alerts (Support)
09:15  INC: PNB transactions slow -- L1 investigates (Support)
09:22  L1 applies KB workaround, PNB restored (Support + Knowledge)
10:00  Deploy circuit breaker v1.0 to 5% canary (Deliver)
11:30  REQ: ICICI requests TPS limit increase (Deliver)
12:00  Monitor canary metrics -- success rate 99.8% (Support)
14:00  Expand canary to 25% (Deliver)
15:30  PRB review meeting for last week's P1 (Support)
16:00  CHG review for tomorrow's Kafka upgrade (Support + Change)
18:00  All canary metrics green -- schedule 100% rollout for tonight (Deliver)
22:00  Full rollout deployed, monitoring active (Deliver + Support)
```

---

## Value Streams: Different Paths Through the Chain

Not every piece of work follows all 6 activities. Different **value streams** take different paths:

### Value Stream 1: New Bank Onboarding

```
Engage -> Plan -> Design & Transition -> Obtain/Build -> Deliver & Support
(All 6 activities, takes 30 days)
```

### Value Stream 2: Incident Resolution

```
Deliver & Support -> (done)
(Just one activity -- maybe Improve if it's a recurring incident)
```

### Value Stream 3: P1 Post-Incident Improvement

```
Deliver & Support -> Improve -> Design & Transition -> Obtain/Build -> Deliver & Support
(Loop back through the chain)
```

### Value Stream 4: Emergency Hotfix

```
Engage -> Obtain/Build -> Deliver & Support
(Skip formal design -- fast-track)
```

---

## Connection to Previous Sections

```
PLAN         uses -> Service Level Mgmt (Sec 8), Service Catalog (Sec 6)
IMPROVE      uses -> Continual Improvement (Sec 10)
ENGAGE       uses -> Service Request (Sec 5), Service Desk (Sec 2)
DESIGN       uses -> CMDB (Sec 7), Change Mgmt (Sec 4)
OBTAIN/BUILD uses -> Change Mgmt (Sec 4)
DELIVER      uses -> Incident (Sec 2), Problem (Sec 3), Knowledge (Sec 9)
```

---

## Key Takeaway

> The Value Chain is NOT a waterfall. It's a **flexible set of activities** that you combine differently depending on the type of work.
>
> A new service goes through all 6. An incident might only touch Deliver & Support. A post-mortem improvement loops through Improve -> Design -> Build -> Deliver.
>
> The power is in the **flexibility** -- you pick the path that fits the work.
