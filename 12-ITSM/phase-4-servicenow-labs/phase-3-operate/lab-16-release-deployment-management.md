# Lab 16: Release & Deployment Management

**Level:** Advanced | **Duration:** 60 minutes | **Prerequisites:** Labs 12-15 completed (CMDB, Incident, Problem, Change exist) | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand the ITIL 4 Release Management practice and how it differs from Change Management
- Create and manage Release records in ServiceNow
- Group multiple Change Requests into a coordinated Release
- Define Release phases with quality gates and approval checkpoints
- Build a detailed Deployment Plan with rollback procedures
- Use the Release Calendar to identify conflicts and blackout periods
- Conduct a Post-Deployment Review (PIR)
- Build a Release Dashboard for executive visibility

---

## Scenario: UPI Platform v3.2.0 — September Release

```
NPCI's UPI Platform is preparing its September major release (v3.2.0).

This release bundles four change requests that emerged from recent
Incident and Problem management activities:

  1. Circuit breaker implementation (from Problem PRB in Lab 14)
  2. Settlement batch processing optimization
  3. New merchant onboarding API endpoint
  4. PostgreSQL upgrade from 14.x to 15.x

The release must be carefully orchestrated — UPI processes 12+ billion
transactions monthly. A botched deployment could impact 350+ banks
and 300+ million users.

Release Manager: Sanjay Manager
Deployment Window: Sunday 2:00 AM - 6:00 AM IST (NPCI maintenance window)
Strategy: Canary deployment with phased traffic ramp-up
```

---

## Part 1: ITIL 4 Release Management Theory

### 1.1 What Is Release Management?

```
ITIL 4 Definition:
  "The purpose of the Release Management practice is to make new and
   changed services and features available for use."

Release Management sits between Change Management and Deployment Management:

  Change Management    →  Authorizes WHAT can change
  Release Management   →  Coordinates WHEN and HOW changes are grouped
  Deployment Management →  Executes the physical/technical deployment

Think of it this way:
  - A Change is a single modification (e.g., upgrade PostgreSQL)
  - A Release bundles multiple changes into a coherent package
  - A Deployment is the act of pushing that package to an environment
```

### 1.2 Release vs Deployment vs Change

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DISTINCTIONS                                 │
├───────────────┬──────────────────┬──────────────────────────────────┤
│ Concept       │ Scope            │ Example (UPI)                    │
├───────────────┼──────────────────┼──────────────────────────────────┤
│ Change        │ Single unit of   │ "Upgrade PostgreSQL 14→15"       │
│               │ modification     │                                  │
├───────────────┼──────────────────┼──────────────────────────────────┤
│ Release       │ Collection of    │ "UPI Platform v3.2.0" bundling   │
│               │ changes tested   │ 4 changes for coordinated        │
│               │ and deployed     │ rollout                          │
│               │ together         │                                  │
├───────────────┼──────────────────┼──────────────────────────────────┤
│ Deployment    │ Physical act of  │ Rolling restart of app servers,  │
│               │ moving release   │ database migration, LB config    │
│               │ to an environ.   │ update                           │
└───────────────┴──────────────────┴──────────────────────────────────┘
```

### 1.3 Release Types

```
Major Release (v3.2.0):
  - Significant new features or architectural changes
  - Full regression testing required
  - CAB approval mandatory
  - Example: Circuit breaker pattern + new API endpoint

Minor Release (v3.2.1):
  - Bug fixes, performance improvements
  - Targeted testing
  - Streamlined approval
  - Example: Fix settlement rounding error

Patch Release (v3.2.1.1):
  - Single critical fix
  - Minimal testing (focused)
  - Expedited approval
  - Example: Hotfix for null pointer in transaction validation

Emergency Release:
  - Critical production fix
  - Bypasses normal gates
  - Post-implementation review mandatory
  - Example: Security vulnerability patch for payment API
```

### 1.4 Release Models

```
Big-Bang Deployment:
  ┌─────────┐     ┌─────────┐
  │ Old v3.1│ ──→ │ New v3.2│   All services updated simultaneously
  └─────────┘     └─────────┘   Risk: High | Rollback: Full revert
                                Use: Small, tightly coupled systems

Phased/Rolling Deployment:
  Server 1: ■■■■ v3.2 ✓
  Server 2: ████ v3.1 → ■■■■ v3.2 ✓
  Server 3: ████ v3.1 → → → ■■■■ v3.2 ✓
  Server 4: ████ v3.1 → → → → → ■■■■ v3.2 ✓
  Risk: Medium | Rollback: Stop and revert completed servers
  Use: Stateless services behind load balancer

Canary Deployment:
  ┌──────────────────────────────────────┐
  │  95% traffic → v3.1 (stable)        │
  │   5% traffic → v3.2 (canary)        │
  │  Monitor → if OK → ramp to 25/50/100│
  └──────────────────────────────────────┘
  Risk: Low | Rollback: Redirect canary traffic back
  Use: UPI Transaction Service (THIS IS OUR STRATEGY)

Blue-Green Deployment:
  ┌────────────┐  ┌────────────┐
  │ BLUE (v3.1)│  │GREEN (v3.2)│
  │  (active)  │  │ (standby)  │
  └─────┬──────┘  └─────┬──────┘
        │               │
        └───── LB ──────┘  ← Switch traffic atomically
  Risk: Low | Rollback: Switch LB back to Blue
  Use: UPI Settlement Service (batch processing)
```

### 1.5 Release Pipeline

```
Plan → Build → Test → Deploy → Review

Detailed for UPI Platform:

  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │ PLAN     │──→│ BUILD    │──→│ TEST     │──→│ DEPLOY   │──→│ REVIEW   │
  │          │   │          │   │          │   │          │   │          │
  │ Scope    │   │ Code     │   │ Unit     │   │ Staging  │   │ PIR      │
  │ Schedule │   │ Compile  │   │ Integr.  │   │ Canary   │   │ Metrics  │
  │ Risk     │   │ Package  │   │ Perf.    │   │ Ramp-up  │   │ Lessons  │
  │ Approval │   │ Artifact │   │ UAT      │   │ Full     │   │ Sign-off │
  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
       │                             │               │
    Gate 1:                       Gate 2:         Gate 3:
    CAB Approval              Perf. Test Pass   Smoke Test Pass
```

### 1.6 Deployment Environments

```
  Dev          →    QA           →    Staging       →    Production
  ┌──────────┐     ┌──────────┐     ┌──────────┐      ┌──────────┐
  │ Feature  │     │ Integr.  │     │ Pre-prod │      │ Live UPI │
  │ branches │     │ testing  │     │ mirror   │      │ traffic  │
  │          │     │          │     │          │      │          │
  │ Devs own │     │ QA team  │     │ Ops team │      │ NOC      │
  │ it       │     │ validates│     │ validates│      │ monitors │
  └──────────┘     └──────────┘     └──────────┘      └──────────┘

  UPI Scale Reference:
    Dev:     1 app server,  1 DB
    QA:      2 app servers, 1 DB (with test data)
    Staging: 4 app servers, 2 DB (prod mirror, synthetic traffic)
    Prod:    8 app servers, 2 DB (primary + replica), load balancer
```

### 1.7 Release Management in the Service Value Chain

```
  ┌────────────────────────────────────────────────────────────────┐
  │                   Service Value Chain                          │
  │                                                                │
  │  Plan ──→ Improve ──→ Engage ──→ Design ──→ Obtain ──→ D&S   │
  │                                                                │
  │  Release Management contributes to:                            │
  │    - Design & Transition: Coordinating release packaging       │
  │    - Obtain/Build: Managing build artifacts                    │
  │    - Deliver & Support: Deploying to production                │
  │    - Improve: Post-deployment reviews feed improvements        │
  └────────────────────────────────────────────────────────────────┘
```

---

## Part 2: ServiceNow Release Management Module

### Step 2.1: Navigate to Release Management

1. In the Application Navigator, type **Release**
2. You should see:
   - **Release > All** — view all release records
   - **Release > Create New** — create a new release
   - **Release > Release Calendar** — calendar view
   - **Release > Dashboard** — release metrics

> **Note:** If you do not see the Release module, it may need to be activated.
> Navigate to **System Definition > Plugins** and search for **Release Management**.
> Activate the plugin `com.snc.release_management` if it is not already active.

### Step 2.2: Understand the Release Record

```
The Release record (table: release_project) contains:

  ┌─────────────────────────────────────────────────────────┐
  │ Release Record Fields                                   │
  ├───────────────────┬─────────────────────────────────────┤
  │ Number            │ Auto-generated (REL0010001)         │
  │ Short description │ Name of the release                 │
  │ Type              │ Major / Minor / Patch / Emergency   │
  │ State             │ Draft → Planning → Build → Test →   │
  │                   │ Deploy → Review → Closed            │
  │ Release date      │ Planned deployment date             │
  │ Release manager   │ Person responsible                  │
  │ Description       │ Detailed scope and contents         │
  │ Risk              │ High / Medium / Low                 │
  │ Priority          │ 1-Critical to 4-Low                 │
  │ Affected CIs      │ Configuration items impacted        │
  │ Change requests   │ Linked changes in this release      │
  │ Release phases    │ Sub-tasks representing phases       │
  └───────────────────┴─────────────────────────────────────┘
```

### Step 2.3: Release States

```
  Draft → Planning → Build → Test → Deploy → Review → Closed
    │                                           │
    └── Cancelled                               └── If issues found,
                                                    can loop back
  State Transitions:
    Draft:    Initial creation, scope definition
    Planning: Requirements finalized, resources assigned
    Build:    Development and integration work
    Test:     QA, UAT, performance testing
    Deploy:   Production deployment in progress
    Review:   Post-deployment verification
    Closed:   Release complete and signed off
```

---

## Part 3: Create a Release Record

### Step 3.1: Create the September Release

1. Navigate to **Release > Create New**
2. Fill in the following fields:

| Field | Value |
|-------|-------|
| Short description | UPI Platform v3.2.0 — September Release |
| Type | Major |
| State | Draft |
| Priority | 2 - High |
| Risk | High |
| Release date | (Next Sunday at 02:00 IST) |
| Release manager | Sanjay Manager |

3. In the **Description** field, enter:

```
UPI Platform v3.2.0 — September Major Release

SCOPE:
This release includes four changes developed and tested over the
past sprint cycle:

1. Circuit Breaker Implementation (from Problem PRB)
   - Implements Resilience4j circuit breaker in UPI Transaction Service
   - Prevents cascading failures during downstream service outages
   - Addresses root cause from Incident INC: Transaction timeout spike

2. Settlement Batch Optimization
   - Refactors batch processing logic for UPI Settlement Service
   - Expected 40% improvement in end-of-day settlement processing time
   - Reduces database lock contention during batch runs

3. New Merchant Onboarding API Endpoint
   - REST API for automated merchant VPA registration
   - Replaces manual CSV upload process
   - Supports bulk onboarding (up to 10,000 merchants per request)

4. PostgreSQL Upgrade (14.x to 15.x)
   - Performance improvements in query planning
   - Enhanced logical replication support
   - Security patches (CVE-2024-xxxx addressed)

DEPLOYMENT STRATEGY:
  - Canary deployment for Transaction Service
  - Blue-green deployment for Settlement Service
  - Rolling restart for API endpoints
  - Database migration with replication slot preservation

RISK ASSESSMENT:
  - PostgreSQL upgrade carries highest risk (data integrity)
  - Circuit breaker introduces new failure handling paths
  - Mitigation: Full rollback plan for each component

MAINTENANCE WINDOW:
  Sunday 02:00 - 06:00 IST (NPCI standard maintenance window)
```

4. Click **Submit**

### Step 3.2: Add Affected CIs

1. Open the release record you just created
2. Scroll to the **Affected CIs** related list (or **Configuration Items** tab)
3. Click **Edit** or **Add**
4. Search for and add the following CIs:

| CI Name | CI Class |
|---------|----------|
| UPI Transaction Service | Business Service |
| UPI Settlement Service | Business Service |
| PostgreSQL Primary | Database Instance |
| PostgreSQL Replica | Database Instance |
| Load Balancer | Load Balancer |
| App Server 1 | Server |
| App Server 2 | Server |

5. Click **Save**

> **Why link CIs?** This creates traceability. If an incident occurs after
> deployment, the CI relationship helps identify which release may have
> caused it. This is the foundation of impact analysis.

---

## Part 4: Link Changes to Release

### Step 4.1: Create Change Requests (if not already created)

If you do not already have these Change Requests from Lab 15, create them now.

**Change 1: Circuit Breaker Implementation**

1. Navigate to **Change > Create New**
2. Fill in:

| Field | Value |
|-------|-------|
| Short description | Implement circuit breaker pattern in UPI Transaction Service |
| Type | Normal |
| Category | Software |
| Priority | 2 - High |
| Risk | Moderate |
| Assignment group | Platform Engineering |
| Assigned to | Ravi Kumar |
| Configuration item | UPI Transaction Service |
| Justification | Prevent cascading failures identified in Problem PRB (Lab 14) |

3. Click **Submit**

**Change 2: Settlement Batch Optimization**

| Field | Value |
|-------|-------|
| Short description | Optimize settlement batch processing |
| Type | Normal |
| Category | Software |
| Priority | 3 - Moderate |
| Risk | Low |
| Assignment group | Platform Engineering |
| Assigned to | Amit Verma |
| Configuration item | UPI Settlement Service |
| Justification | Reduce batch processing time by 40%, eliminate DB lock contention |

**Change 3: Merchant Onboarding API**

| Field | Value |
|-------|-------|
| Short description | Deploy new merchant onboarding API endpoint |
| Type | Normal |
| Category | Software |
| Priority | 3 - Moderate |
| Risk | Low |
| Assignment group | Platform Engineering |
| Assigned to | Ravi Kumar |
| Configuration item | UPI Transaction Service |
| Justification | Replace manual CSV-based merchant registration with REST API |

**Change 4: PostgreSQL Upgrade**

| Field | Value |
|-------|-------|
| Short description | Upgrade PostgreSQL from 14.x to 15.x |
| Type | Normal |
| Category | Hardware |
| Priority | 2 - High |
| Risk | High |
| Assignment group | Platform Engineering |
| Assigned to | Amit Verma |
| Configuration item | PostgreSQL Primary |
| Justification | Security patches, performance improvements, replication enhancements |

### Step 4.2: Link Changes to the Release

1. Open the Release record: **UPI Platform v3.2.0 — September Release**
2. Scroll down to the **Change Requests** related list
3. Click **Edit**
4. In the search box, find each of the four Change Requests by short description
5. Move them to the selected list
6. Click **Save**

```
Your release should now show:

  Release: UPI Platform v3.2.0 — September Release
  ├── CHG0010001: Implement circuit breaker pattern in UPI Transaction Service
  ├── CHG0010002: Optimize settlement batch processing
  ├── CHG0010003: Deploy new merchant onboarding API endpoint
  └── CHG0010004: Upgrade PostgreSQL from 14.x to 15.x
```

### Step 4.3: Change Sequencing and Dependencies

Not all changes can be deployed in any order. Define the sequence:

```
Deployment Sequence and Dependencies:

  Step 1: CHG0010004 — PostgreSQL Upgrade
          Must go first (other services depend on DB)
          ↓
  Step 2: CHG0010001 — Circuit Breaker Implementation
          Depends on DB being available and stable
          ↓
  Step 3: CHG0010002 — Settlement Batch Optimization
          Can run in parallel with Step 2 (different service)
          ↓
  Step 4: CHG0010003 — Merchant Onboarding API
          Deploy last (new feature, lowest risk to existing)

  Parallel execution possible:
    Steps 2 and 3 can run simultaneously (independent services)
    Step 4 depends on Step 2 (shares Transaction Service deployment)
```

1. Open each Change Request
2. In the **Implementation plan** field, note the sequence position:
   - "Release v3.2.0 — Deploy Sequence: 1 of 4 (FIRST — database migration)"
   - "Release v3.2.0 — Deploy Sequence: 2 of 4 (after DB upgrade)"
   - "Release v3.2.0 — Deploy Sequence: 2 of 4 (parallel with circuit breaker)"
   - "Release v3.2.0 — Deploy Sequence: 3 of 4 (after Transaction Service changes)"

---

## Part 5: Release Phases & Gates

### Step 5.1: Understanding Release Phases

```
A Release Phase breaks the release lifecycle into manageable stages.
Each phase has:
  - Entry criteria (what must be true to start)
  - Activities (what happens during the phase)
  - Exit criteria / Quality gate (what must pass to proceed)

UPI Platform v3.2.0 Phases:

  Phase 1: Planning & Design
    ├── Entry: Release scope approved
    ├── Activities: Architecture review, resource allocation
    └── Gate: CAB approval to proceed

  Phase 2: Build & Integration Testing
    ├── Entry: CAB approval received
    ├── Activities: Code merge, CI pipeline, integration tests
    └── Gate: All integration tests pass, zero critical defects

  Phase 3: UAT & Performance Testing
    ├── Entry: Integration tests pass
    ├── Activities: User acceptance, load testing, security scan
    └── Gate: UAT sign-off, performance benchmarks met

  Phase 4: Production Deployment
    ├── Entry: UAT approved, maintenance window confirmed
    ├── Activities: Execute deployment plan (Part 6)
    └── Gate: Smoke tests pass, no P1/P2 incidents

  Phase 5: Post-Deployment Verification
    ├── Entry: Deployment complete
    ├── Activities: Monitor metrics, verify functionality, PIR
    └── Gate: 24-hour soak period clean, PIR completed
```

### Step 5.2: Create Release Phases in ServiceNow

1. Open the Release record: **UPI Platform v3.2.0 — September Release**
2. Navigate to the **Release Phases** related list
3. Click **New** to create each phase:

**Phase 1: Planning & Design**

| Field | Value |
|-------|-------|
| Short description | Phase 1: Planning & Design |
| Order | 100 |
| State | Open |
| Assigned to | Sanjay Manager |
| Planned start date | (Monday of release week) |
| Planned end date | (Wednesday of release week) |
| Description | Architecture review, resource allocation, risk assessment. Gate: CAB approval required before proceeding to Build phase. |

Click **Submit**, then create the next phase.

**Phase 2: Build & Integration Testing**

| Field | Value |
|-------|-------|
| Short description | Phase 2: Build & Integration Testing |
| Order | 200 |
| State | Pending |
| Assigned to | Ravi Kumar |
| Planned start date | (Thursday of release week) |
| Planned end date | (Friday of release week) |
| Description | Code freeze, merge all feature branches, run CI/CD pipeline. Gate: All integration tests pass, code coverage above 80%, zero critical/high defects. |

**Phase 3: UAT & Performance Testing**

| Field | Value |
|-------|-------|
| Short description | Phase 3: UAT & Performance Testing |
| Order | 300 |
| State | Pending |
| Assigned to | Priya Sharma |
| Planned start date | (Friday of release week) |
| Planned end date | (Saturday of release week) |
| Description | User acceptance testing in staging environment. Load test: 50,000 TPS sustained for 30 minutes. Security scan: OWASP Top 10 check. Gate: UAT sign-off from business, performance benchmarks met (p99 latency < 200ms). |

**Phase 4: Production Deployment**

| Field | Value |
|-------|-------|
| Short description | Phase 4: Production Deployment |
| Order | 400 |
| State | Pending |
| Assigned to | Amit Verma |
| Planned start date | (Sunday 02:00 IST) |
| Planned end date | (Sunday 06:00 IST) |
| Description | Execute deployment plan within NPCI maintenance window. Canary deployment with traffic ramp-up. NOC monitoring throughout. Gate: Smoke tests pass, error rate below 0.01%, no P1/P2 incidents within 1 hour. |

**Phase 5: Post-Deployment Verification**

| Field | Value |
|-------|-------|
| Short description | Phase 5: Post-Deployment Verification |
| Order | 500 |
| State | Pending |
| Assigned to | Priya Sharma |
| Planned start date | (Sunday 06:00 IST) |
| Planned end date | (Monday 06:00 IST — 24h soak) |
| Description | 24-hour monitoring period. Verify all transaction types, settlement processing, merchant onboarding. Conduct Post-Implementation Review. Gate: PIR completed, no rollback required, stakeholder sign-off. |

### Step 5.3: Quality Gate Approval Configuration

For phases that require formal approval (Phase 1 and Phase 3), configure approval:

1. Open **Phase 1: Planning & Design**
2. In the **Approvers** related list, click **New**
3. Add approver:

| Field | Value |
|-------|-------|
| Approver | Sanjay Manager |
| State | Requested |
| Type | CAB Approval — Planning Gate |

4. Similarly, for **Phase 3: UAT & Performance Testing**, add:

| Field | Value |
|-------|-------|
| Approver | Sanjay Manager |
| State | Requested |
| Type | UAT Sign-off — Deployment Gate |

```
Approval Flow:

  Phase 1 ──[CAB Approval]──→ Phase 2 ──[Auto]──→ Phase 3
                                                      │
                                              [UAT Sign-off]
                                                      │
                                                      ↓
  Phase 5 ←──[Auto]──── Phase 4 ←──[Deployment Gate]──┘
```

---

## Part 6: Deployment Plan

### Step 6.1: Create Deployment Tasks

The Deployment Plan breaks Phase 4 (Production Deployment) into granular, sequenced tasks. Each task has a clear owner, duration, verification step, and rollback procedure.

1. Open the Release record
2. Navigate to the **Deployment Tasks** related list (or create as child tasks of Phase 4)
3. Create the following tasks:

**Task 1: Pre-Deployment Verification**

| Field | Value |
|-------|-------|
| Short description | Pre-deployment: Verify staging environment matches production |
| Order | 10 |
| Assigned to | Amit Verma |
| Estimated duration | 15 minutes |
| Description | Confirm staging deployment is healthy. Verify all artifacts are staged. Check rollback scripts are tested. Confirm NOC team is online and monitoring dashboards are active. |

**Task 2: Database Backup**

| Field | Value |
|-------|-------|
| Short description | Create full PostgreSQL backup (primary + replica) |
| Order | 20 |
| Assigned to | Amit Verma |
| Estimated duration | 20 minutes |
| Description | pg_dump full backup of production database. Verify backup integrity with checksum. Store in S3 with 30-day retention. Confirm replication slot state is captured. |

**Task 3: Database Migration (PostgreSQL 14 to 15)**

| Field | Value |
|-------|-------|
| Short description | Execute PostgreSQL upgrade 14.x to 15.x |
| Order | 30 |
| Assigned to | Amit Verma |
| Estimated duration | 30 minutes |
| Description | Stop replication. Upgrade primary using pg_upgrade. Run post-upgrade optimizer statistics. Verify data integrity (row counts, checksums). Restart replication to replica. Verify replica sync. |

```
Rollback Plan (Task 3):
  If pg_upgrade fails:
    1. Stop the failed upgrade process
    2. Restore from backup (Task 2)
    3. Restart PostgreSQL 14.x
    4. Verify data integrity
    5. Abort remaining release tasks
    6. Estimated rollback time: 25 minutes
```

**Task 4: Backend Services Deployment (Circuit Breaker + Settlement)**

| Field | Value |
|-------|-------|
| Short description | Deploy backend services with rolling restart |
| Order | 40 |
| Assigned to | Ravi Kumar |
| Estimated duration | 20 minutes |
| Description | Deploy UPI Transaction Service with circuit breaker (canary — 1 server first). Deploy UPI Settlement Service with batch optimization (blue-green — switch to green). Verify health endpoints on all deployed instances. |

```
Rollback Plan (Task 4):
  If service deployment fails:
    1. Transaction Service: Route traffic away from canary server
    2. Redeploy previous version to canary server
    3. Settlement Service: Switch LB back to blue environment
    4. Estimated rollback time: 10 minutes
```

**Task 5: Merchant Onboarding API Deployment**

| Field | Value |
|-------|-------|
| Short description | Deploy merchant onboarding API endpoint |
| Order | 50 |
| Assigned to | Ravi Kumar |
| Estimated duration | 10 minutes |
| Description | Deploy new API endpoint alongside existing services. This is additive (new endpoint) — does not modify existing functionality. Verify endpoint responds to health check. Run sample API call with test merchant data. |

```
Rollback Plan (Task 5):
  If API deployment fails:
    1. Remove new endpoint route from API gateway
    2. Existing merchant onboarding (CSV upload) remains unaffected
    3. Estimated rollback time: 5 minutes
```

**Task 6: Load Balancer Configuration Update**

| Field | Value |
|-------|-------|
| Short description | Update load balancer configuration for canary traffic split |
| Order | 60 |
| Assigned to | Amit Verma |
| Estimated duration | 10 minutes |
| Description | Configure LB to route 5% of UPI transaction traffic to canary (v3.2.0) server. Remaining 95% continues to v3.1.x servers. Configure health check thresholds for automatic canary removal if error rate exceeds 1%. |

**Task 7: Smoke Tests**

| Field | Value |
|-------|-------|
| Short description | Execute production smoke test suite |
| Order | 70 |
| Assigned to | Priya Sharma |
| Estimated duration | 15 minutes |
| Description | Run automated smoke tests against production. Tests include: UPI P2P transaction (send/receive), UPI P2M transaction (merchant payment), Settlement batch trigger (manual test batch), Merchant onboarding API (test merchant), Database query performance (explain analyze on key queries). All tests must pass. Any failure triggers immediate rollback assessment. |

**Task 8: Traffic Ramp-Up (Canary)**

| Field | Value |
|-------|-------|
| Short description | Canary traffic ramp-up: 5% → 25% → 50% → 100% |
| Order | 80 |
| Assigned to | Priya Sharma |
| Estimated duration | 40 minutes |
| Description | Gradually increase traffic to v3.2.0 servers. Monitor at each stage for 10 minutes before proceeding. |

```
Canary Ramp-Up Schedule:

  02:45  →   5% traffic to v3.2.0  (monitor 10 min)
  02:55  →  25% traffic to v3.2.0  (monitor 10 min)
  03:05  →  50% traffic to v3.2.0  (monitor 10 min)
  03:15  → 100% traffic to v3.2.0  (deploy to remaining servers)

  At each stage, monitor:
    - Error rate (must stay below 0.01%)
    - p99 latency (must stay below 200ms)
    - Transaction success rate (must stay above 99.95%)
    - Database connection pool utilization (must stay below 80%)

  Decision criteria:
    GREEN:  All metrics within threshold → proceed to next stage
    YELLOW: One metric marginal → hold at current stage, investigate
    RED:    Any metric breached → immediate rollback to v3.1.x
```

**Task 9: Full Rollout Verification**

| Field | Value |
|-------|-------|
| Short description | Full rollout complete — final verification |
| Order | 90 |
| Assigned to | Sanjay Manager |
| Estimated duration | 10 minutes |
| Description | All servers running v3.2.0. Final verification of all services. Confirm NOC dashboards show green. Update release state to "Review". Send deployment completion notification to stakeholders. |

### Step 6.2: Deployment Timeline Summary

```
Sunday Maintenance Window: 02:00 - 06:00 IST

  02:00 - 02:15  Task 1: Pre-deployment verification
  02:15 - 02:35  Task 2: Database backup
  02:35 - 03:05  Task 3: PostgreSQL upgrade
  03:05 - 03:25  Task 4: Backend services deployment
  03:25 - 03:35  Task 5: Merchant API deployment
  03:35 - 03:45  Task 6: Load balancer configuration
  03:45 - 04:00  Task 7: Smoke tests
  04:00 - 04:40  Task 8: Canary traffic ramp-up
  04:40 - 04:50  Task 9: Final verification

  Total estimated: 2 hours 50 minutes
  Buffer remaining: 1 hour 10 minutes (for troubleshooting)

  ■ = Complete  □ = Pending  ▓ = In Progress

  02:00  02:30  03:00  03:30  04:00  04:30  05:00  05:30  06:00
  |------|------|------|------|------|------|------|------|
  ■■■■■ DB-BKP ■■■■■ PG-UPG ■■■■ SVC ■■ API ■ LB ■■ SMOKE ■■■■■■ CANARY ■■ VER ░░░░ BUFFER ░░░░
```

---

## Part 7: Release Calendar

### Step 7.1: View the Release Calendar

1. Navigate to **Release > Release Calendar**
2. The calendar displays all planned releases with their deployment dates
3. Your release **UPI Platform v3.2.0** should appear on the planned Sunday

```
Release Calendar View:

  September 2026
  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┐
  │ Mon │ Tue │ Wed │ Thu │ Fri │ Sat │ Sun │
  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤
  │  7  │  8  │  9  │ 10  │ 11  │ 12  │ 13  │
  │     │     │     │     │     │     │     │
  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤
  │ 14  │ 15  │ 16  │ 17  │ 18  │ 19  │ 20  │
  │     │     │     │     │     │     │ REL │
  │     │     │     │     │     │     │v3.2 │
  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤
  │ 21  │ 22  │ 23  │ 24  │ 25  │ 26  │ 27  │
  │     │     │     │     │     │     │     │
  ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤
  │ 28  │ 29  │ 30  │     │     │     │     │
  │ EOM │ EOM │ EOM │     │     │     │     │
  │BLKOT│BLKOT│BLKOT│     │     │     │     │
  └─────┴─────┴─────┴─────┴─────┴─────┴─────┘

  Legend:
    REL  = Planned Release
    BLKOT = Blackout Period (no deployments)
    EOM   = End of Month (settlement processing)
```

### Step 7.2: Identify Conflicts

Check for potential conflicts:

1. **Other releases** scheduled in the same window
2. **Change freeze periods** that overlap
3. **Resource conflicts** (same team assigned to multiple releases)

```
Conflict Detection Checklist:

  ✓ No other releases on same Sunday
  ✓ No change freeze active
  ✓ NOC team (Priya Sharma) available for monitoring
  ✓ Platform Engineering (Ravi, Amit) available for deployment
  ✗ POTENTIAL CONFLICT: Month-end settlement processing
    → Release is 2 weeks before month-end — SAFE
```

### Step 7.3: Define Blackout Periods

Blackout periods prevent releases during critical business times.

1. Navigate to **Change > Change Blackout** (or **Change > Blackout Schedules**)
2. Click **New**
3. Create the following blackout periods:

**Blackout 1: Month-End Settlement**

| Field | Value |
|-------|-------|
| Name | Month-End Settlement Processing |
| Type | Blackout |
| Start date | Last 3 days of each month |
| End date | First day of next month |
| Description | No deployments during end-of-month settlement reconciliation. UPI settlement volumes peak during this period. Any deployment failure could impact settlement accuracy for 350+ banks. |

**Blackout 2: Festival Period (Diwali)**

| Field | Value |
|-------|-------|
| Name | Diwali Festival — Transaction Peak |
| Type | Blackout |
| Start date | (Diwali week start) |
| End date | (Diwali week end + 2 days) |
| Description | UPI transaction volumes surge 300-400% during Diwali festival. No changes permitted. All hands on monitoring. |

**Blackout 3: RBI Audit Window**

| Field | Value |
|-------|-------|
| Name | RBI Quarterly Audit — System Freeze |
| Type | Blackout |
| Start date | (Audit start date) |
| End date | (Audit end date) |
| Description | Reserve Bank of India quarterly audit. System must remain stable and unchanged during audit period. All deployment activity frozen. |

### Step 7.4: Release Windows

Define the approved maintenance windows:

```
NPCI Standard Release Windows:

  Primary Window:
    Day:   Sunday
    Time:  02:00 - 06:00 IST
    Type:  Major/Minor releases
    Note:  Lowest UPI transaction volume period

  Secondary Window:
    Day:   Wednesday
    Time:  02:00 - 04:00 IST
    Type:  Minor/Patch releases only
    Note:  Mid-week window for non-critical updates

  Emergency Window:
    Day:   Any day
    Time:  Any time (with CISO + CTO approval)
    Type:  Emergency releases only
    Note:  For critical security patches or P1 incident fixes

  Excluded Periods:
    - Last 3 days of each month (settlement)
    - Major festivals (Diwali, Holi, Eid, Christmas)
    - RBI audit windows
    - National holidays
    - Election days (high UPI usage for donations)
```

---

## Part 8: Post-Deployment Review (PIR)

### Step 8.1: What Is a PIR?

```
Post-Implementation Review (PIR) / Post-Deployment Review:

  Purpose: Evaluate the success of the release deployment and
           capture lessons learned for continuous improvement.

  A PIR answers:
    1. Was the release deployed successfully?
    2. Did we stay within the maintenance window?
    3. Were there any unexpected issues?
    4. Was a rollback required? If so, why?
    5. What metrics changed post-deployment?
    6. What should we do differently next time?

  PIR is a key input to the ITIL 4 Continual Improvement practice.
```

### Step 8.2: Create a PIR Record

After deployment completes, create the PIR:

1. Open the Release record: **UPI Platform v3.2.0 — September Release**
2. Change State to **Review**
3. In the **Post-Implementation Review** section (or create as a related record), document:

```
POST-IMPLEMENTATION REVIEW: UPI Platform v3.2.0

Date: [Deployment Sunday]
Reviewer: Sanjay Manager
Attendees: Ravi Kumar, Amit Verma, Priya Sharma

1. DEPLOYMENT SUMMARY
   ─────────────────────────────────────────────
   Planned Start:     02:00 IST
   Actual Start:      02:00 IST
   Planned End:       04:50 IST (estimated)
   Actual End:        05:15 IST
   Overrun:           25 minutes
   Reason:            PostgreSQL upgrade took longer than estimated
                      (optimizer statistics rebuild was slower on
                       production data volume)

2. DEPLOYMENT RESULTS BY CHANGE
   ─────────────────────────────────────────────
   CHG0010004: PostgreSQL Upgrade    → SUCCESS (with delay)
   CHG0010001: Circuit Breaker       → SUCCESS
   CHG0010002: Settlement Batch Opt. → SUCCESS
   CHG0010003: Merchant API          → SUCCESS

   Overall: SUCCESSFUL — No rollback required

3. ISSUES ENCOUNTERED
   ─────────────────────────────────────────────
   Issue 1: PostgreSQL optimizer statistics rebuild
     Severity: Low
     Impact:   25-minute delay, no service impact
     Action:   Pre-compute statistics in staging next time

   Issue 2: Canary health check false alarm at 25% traffic
     Severity: Medium
     Impact:   5-minute investigation delay
     Cause:    Health check threshold too sensitive (0.005% error
               rate triggered alert, threshold was 0.01%)
     Action:   Adjust health check thresholds in monitoring config

4. METRICS COMPARISON
   ─────────────────────────────────────────────
   Metric                    Before    After     Change
   ──────────────────────────────────────────────────────
   Avg transaction latency   145ms     128ms     -12%
   p99 transaction latency   280ms     195ms     -30%
   Settlement batch time     47min     29min     -38%
   Error rate                0.008%    0.005%    -37%
   DB query avg time         12ms      8ms       -33%
   Circuit breaker trips     N/A       0         New metric

5. ROLLBACK ASSESSMENT
   ─────────────────────────────────────────────
   Was rollback required?    NO
   Was rollback tested?      Yes (in staging)
   Rollback readiness:       All rollback scripts were staged
                             and verified pre-deployment

6. LESSONS LEARNED
   ─────────────────────────────────────────────
   a. Database upgrade time estimation:
      - Production data volume is 10x staging
      - Optimizer stats rebuild scales non-linearly
      - ACTION: Add 50% buffer to DB migration estimates

   b. Health check thresholds:
      - Canary health checks need different thresholds than
        steady-state monitoring
      - ACTION: Create separate "deployment mode" alert profiles

   c. Communication:
      - Stakeholder updates every 30 minutes worked well
      - ACTION: Formalize as standard deployment communication plan

   d. Positive:
      - Canary deployment strategy proved its value
      - Phase gate approach prevented premature deployment
      - All team members were well-prepared and responsive

7. SIGN-OFF
   ─────────────────────────────────────────────
   Release Manager:    Sanjay Manager    — APPROVED
   NOC Lead:          Priya Sharma       — APPROVED
   Engineering Lead:  Ravi Kumar         — APPROVED
   Date:              [Monday after deployment]
```

### Step 8.3: Link PIR to Release

1. Ensure the PIR content is captured in the Release record's **Close notes** or a dedicated PIR record
2. Update the Release record:

| Field | Value |
|-------|-------|
| State | Closed |
| Close notes | PIR completed. Release successful with 25-min overrun. All metrics improved. Two lessons learned documented for process improvement. |

3. Click **Update**

---

## Part 9: Release Dashboard

### Step 9.1: View the Release Dashboard

1. Navigate to **Release > Dashboard** (or **Release > Overview**)
2. The dashboard shows:

```
Release Dashboard Widgets:

  ┌─────────────────────────────────┬─────────────────────────────────┐
  │ Releases by State               │ Releases by Type                │
  │                                 │                                 │
  │ Draft:    ██░░░░░░░░  2         │ Major:     ███░░░░░░░  3       │
  │ Planning: ░░░░░░░░░░  0         │ Minor:     ██████░░░░  6       │
  │ Build:    █░░░░░░░░░  1         │ Patch:     ████░░░░░░  4       │
  │ Test:     ░░░░░░░░░░  0         │ Emergency: █░░░░░░░░░  1       │
  │ Deploy:   ░░░░░░░░░░  0         │                                 │
  │ Review:   █░░░░░░░░░  1         │                                 │
  │ Closed:   ██████████ 10         │                                 │
  └─────────────────────────────────┴─────────────────────────────────┘
  ┌─────────────────────────────────┬─────────────────────────────────┐
  │ Release Success Rate            │ Avg Deployment Duration          │
  │                                 │                                 │
  │ Q1: ████████░░  80%             │ Major:     3h 15m               │
  │ Q2: █████████░  90%             │ Minor:     1h 30m               │
  │ Q3: ██████████  96%             │ Patch:     0h 45m               │
  │                                 │ Emergency: 0h 30m               │
  │ Target: 95%  Current: 96%      │                                 │
  └─────────────────────────────────┴─────────────────────────────────┘
```

### Step 9.2: Create a Custom Release Report

1. Navigate to **Reports > Create New**
2. Configure:

| Field | Value |
|-------|-------|
| Report name | UPI Release Management — Quarterly Summary |
| Source type | Table |
| Table | Release [release_project] |
| Type | Bar chart |
| Group by | Type |
| Filter | Release date is in the last 3 months |

3. Click **Save** and **Run**

4. Add additional reports:

**Report 2: Release Timeline**

| Field | Value |
|-------|-------|
| Report name | UPI Release Timeline |
| Type | Calendar |
| Table | Release [release_project] |
| Date field | Release date |

**Report 3: Changes per Release**

| Field | Value |
|-------|-------|
| Report name | Changes per Release |
| Type | Bar chart |
| Table | Change Request [change_request] |
| Group by | Release |
| Filter | Release is not empty |

---

## Practice Exercises

### Exercise 1: Create a Minor Release (Hotfix)

Create a minor release for an emergency fix:

```
Release: UPI Platform v3.2.1 — Hotfix
Type:    Emergency
Reason:  Circuit breaker threshold misconfigured in v3.2.0,
         causing premature circuit opens during normal peak hours

Steps:
  1. Create Release record (Type: Emergency, Priority: 1-Critical)
  2. Create one Emergency Change Request:
     "Adjust circuit breaker threshold from 50% to 80% failure rate"
  3. Link the change to the release
  4. Skip Phase 1-3 (emergency — direct to deployment)
  5. Create 3 deployment tasks:
     a. Update circuit breaker configuration
     b. Rolling restart of Transaction Service
     c. Verify circuit breaker behavior under load
  6. Complete PIR with lessons learned:
     "Original threshold was based on staging traffic patterns.
      Production traffic is burstier — threshold needs adjustment."
```

### Exercise 2: Plan a Blue-Green Deployment

Design a blue-green deployment plan for UPI Settlement Service:

```
Blue-Green Deployment Plan:

  1. Create new Release: "UPI Settlement Service v2.1 — Blue-Green"
  2. Deployment tasks:
     a. Deploy v2.1 to Green environment (4 servers)
     b. Run settlement batch test on Green (synthetic data)
     c. Verify Green results match Blue results (reconciliation)
     d. Switch load balancer from Blue to Green
     e. Monitor Green for 30 minutes
     f. If stable: decommission Blue
     f. If issues: switch LB back to Blue (instant rollback)

  Document this in ServiceNow with proper deployment tasks.
```

### Exercise 3: Create a Release Blackout Period

Create a blackout period for Diwali week:

```
Blackout Details:
  Name:        Diwali 2026 — Complete Change Freeze
  Start:       October 19, 2026 00:00 IST
  End:         October 26, 2026 23:59 IST
  Scope:       All production environments
  Exceptions:  P1 security vulnerabilities only (CISO approval)
  Justification:
    UPI transaction volumes during Diwali 2025: 480 million/day
    Expected Diwali 2026: 600+ million/day
    Any service disruption during this period has severe
    financial and reputational impact across 350+ banks.
```

### Exercise 4: Build a Deployment Checklist Template

Create a reusable deployment checklist for UPI services:

```
UPI Service Deployment Checklist Template:

PRE-DEPLOYMENT:
  □ All change requests in "Scheduled" state
  □ Deployment artifacts verified (checksums match)
  □ Rollback scripts tested in staging
  □ Database backup completed and verified
  □ NOC team briefed and dashboards active
  □ Stakeholder notification sent (T-30 minutes)
  □ War room bridge line opened
  □ Monitoring alerts in "deployment mode"

DEPLOYMENT:
  □ Service health check — pre-deployment baseline captured
  □ Database migration executed (if applicable)
  □ Application deployment executed
  □ Load balancer updated
  □ Smoke tests executed — all passing
  □ Canary traffic ramp-up — metrics verified at each stage
  □ Full rollout complete — all instances healthy

POST-DEPLOYMENT:
  □ Smoke tests re-run — all passing
  □ Performance metrics compared to baseline
  □ Error rates within acceptable range
  □ Settlement processing verified (if applicable)
  □ Monitoring alerts restored to "normal mode"
  □ Stakeholder notification sent (completion)
  □ War room bridge closed
  □ Release record updated to "Review"
  □ PIR scheduled within 48 hours

ROLLBACK TRIGGERS:
  □ Error rate exceeds 0.1%
  □ p99 latency exceeds 500ms
  □ Transaction success rate drops below 99.9%
  □ Any P1 incident raised during deployment
  □ Database integrity check fails
```

To implement this in ServiceNow:
1. Navigate to **Service Catalog > Catalog Definitions > Maintain Items**
2. Create a new catalog item: "UPI Deployment Checklist"
3. Add checklist variables for each item above
4. Link the checklist to the release workflow

### Exercise 5: Generate a Release Report

Create a comprehensive release report:

1. Navigate to **Reports > Create New**
2. Create the following report:

| Field | Value |
|-------|-------|
| Report name | UPI Releases — Last Quarter |
| Table | Release [release_project] |
| Type | List |
| Filter | Release date is in the last 90 days |
| Columns | Number, Short description, Type, State, Release date, Risk, Close notes |

3. Run the report and export to PDF
4. Answer these questions from the report:
   - How many releases were deployed in the last quarter?
   - What percentage were successful (no rollback)?
   - What was the average deployment duration by release type?
   - Were there any emergency releases? What caused them?
   - Which CIs were most frequently affected by releases?

---

## Appendix A: Background Scripts for Lab Setup

> Navigate to **System Definition > Scripts - Background** to run these scripts.
> These scripts automate the creation of records for this lab.

### Script 1: Create Release Record

```javascript
// Create the Release Record for UPI Platform v3.2.0
var rel = new GlideRecord('release_project');
rel.initialize();
rel.short_description = 'UPI Platform v3.2.0 — September Release';
rel.description = 'Major release including circuit breaker implementation, settlement batch optimization, merchant onboarding API, and PostgreSQL upgrade.';
rel.type = 'major';
rel.state = 'draft';
rel.priority = 2;
rel.risk = 'high';

// Set release date to next Sunday at 02:00
var releaseDate = new GlideDateTime();
var dayOfWeek = releaseDate.getDayOfWeekLocalTime();
var daysUntilSunday = (7 - dayOfWeek) % 7;
if (daysUntilSunday === 0) daysUntilSunday = 7;
releaseDate.addDaysLocalTime(daysUntilSunday);
releaseDate.setDisplayValue(releaseDate.getDate().getByFormat('yyyy-MM-dd') + ' 02:00:00');
rel.release_date = releaseDate;

// Set release manager
var mgr = new GlideRecord('sys_user');
if (mgr.get('user_name', 'sanjay.manager') || mgr.get('name', 'Sanjay Manager')) {
    rel.release_manager = mgr.sys_id;
}

var relSysId = rel.insert();
gs.info('Created Release: ' + rel.number + ' (sys_id: ' + relSysId + ')');
```

### Script 2: Create Change Requests and Link to Release

```javascript
// Create Change Requests for the Release
var relSysId = ''; // PASTE YOUR RELEASE SYS_ID HERE

var changes = [
    {
        short_description: 'Implement circuit breaker pattern in UPI Transaction Service',
        type: 'normal',
        category: 'Software',
        priority: 2,
        risk: 'moderate',
        assignment_group: 'Platform Engineering',
        assigned_to: 'ravi.kumar',
        justification: 'Prevent cascading failures identified in Problem PRB from Lab 14'
    },
    {
        short_description: 'Optimize settlement batch processing',
        type: 'normal',
        category: 'Software',
        priority: 3,
        risk: 'low',
        assignment_group: 'Platform Engineering',
        assigned_to: 'amit.verma',
        justification: 'Reduce batch processing time by 40%, eliminate DB lock contention'
    },
    {
        short_description: 'Deploy new merchant onboarding API endpoint',
        type: 'normal',
        category: 'Software',
        priority: 3,
        risk: 'low',
        assignment_group: 'Platform Engineering',
        assigned_to: 'ravi.kumar',
        justification: 'Replace manual CSV-based merchant registration with REST API'
    },
    {
        short_description: 'Upgrade PostgreSQL from 14.x to 15.x',
        type: 'normal',
        category: 'Hardware',
        priority: 2,
        risk: 'high',
        assignment_group: 'Platform Engineering',
        assigned_to: 'amit.verma',
        justification: 'Security patches, performance improvements, replication enhancements'
    }
];

changes.forEach(function(chg) {
    var cr = new GlideRecord('change_request');
    cr.initialize();
    cr.short_description = chg.short_description;
    cr.type = chg.type;
    cr.category = chg.category;
    cr.priority = chg.priority;
    cr.risk = chg.risk;
    cr.justification = chg.justification;

    // Set assignment group
    var grp = new GlideRecord('sys_user_group');
    if (grp.get('name', chg.assignment_group)) {
        cr.assignment_group = grp.sys_id;
    }

    // Set assigned to
    var usr = new GlideRecord('sys_user');
    if (usr.get('user_name', chg.assigned_to)) {
        cr.assigned_to = usr.sys_id;
    }

    var chgSysId = cr.insert();
    gs.info('Created Change: ' + cr.number + ' - ' + chg.short_description);

    // Link change to release (via M2M table if applicable)
    // In some ServiceNow versions, this is done via the release field on CHG
    var crUpdate = new GlideRecord('change_request');
    if (crUpdate.get(chgSysId)) {
        crUpdate.release = relSysId;
        crUpdate.update();
        gs.info('  Linked to Release: ' + relSysId);
    }
});
```

### Script 3: Create Release Phases

```javascript
// Create Release Phases
var relSysId = ''; // PASTE YOUR RELEASE SYS_ID HERE

var phases = [
    {
        short_description: 'Phase 1: Planning & Design',
        order: 100,
        state: 1, // Open
        description: 'Architecture review, resource allocation, risk assessment. Gate: CAB approval required.'
    },
    {
        short_description: 'Phase 2: Build & Integration Testing',
        order: 200,
        state: -5, // Pending
        description: 'Code freeze, CI/CD pipeline, integration tests. Gate: All tests pass, zero critical defects.'
    },
    {
        short_description: 'Phase 3: UAT & Performance Testing',
        order: 300,
        state: -5,
        description: 'User acceptance testing, load test (50K TPS), security scan. Gate: UAT sign-off, p99 < 200ms.'
    },
    {
        short_description: 'Phase 4: Production Deployment',
        order: 400,
        state: -5,
        description: 'Execute deployment plan within Sunday 02:00-06:00 IST window. Canary deployment with ramp-up.'
    },
    {
        short_description: 'Phase 5: Post-Deployment Verification',
        order: 500,
        state: -5,
        description: '24-hour soak period. Monitor metrics, verify functionality, conduct PIR.'
    }
];

phases.forEach(function(phase) {
    var ph = new GlideRecord('release_phase');
    ph.initialize();
    ph.release = relSysId;
    ph.short_description = phase.short_description;
    ph.order = phase.order;
    ph.state = phase.state;
    ph.description = phase.description;

    var phSysId = ph.insert();
    gs.info('Created Phase: ' + phase.short_description + ' (sys_id: ' + phSysId + ')');
});
```

### Script 4: Create Deployment Tasks

```javascript
// Create Deployment Tasks for Phase 4
var phaseSysId = ''; // PASTE YOUR PHASE 4 SYS_ID HERE

var tasks = [
    { order: 10,  desc: 'Pre-deployment: Verify staging matches production',     duration: 15 },
    { order: 20,  desc: 'Create full PostgreSQL backup (primary + replica)',      duration: 20 },
    { order: 30,  desc: 'Execute PostgreSQL upgrade 14.x to 15.x',              duration: 30 },
    { order: 40,  desc: 'Deploy backend services with rolling restart',          duration: 20 },
    { order: 50,  desc: 'Deploy merchant onboarding API endpoint',               duration: 10 },
    { order: 60,  desc: 'Update load balancer for canary traffic split',         duration: 10 },
    { order: 70,  desc: 'Execute production smoke test suite',                   duration: 15 },
    { order: 80,  desc: 'Canary traffic ramp-up: 5% → 25% → 50% → 100%',       duration: 40 },
    { order: 90,  desc: 'Full rollout complete — final verification',            duration: 10 }
];

tasks.forEach(function(task) {
    var t = new GlideRecord('release_task');
    t.initialize();
    t.parent = phaseSysId;
    t.short_description = task.desc;
    t.order = task.order;
    t.state = -5; // Pending
    t.description = 'Estimated duration: ' + task.duration + ' minutes';

    var tSysId = t.insert();
    gs.info('Created Task: ' + task.order + ' - ' + task.desc);
});

gs.info('All deployment tasks created successfully.');
```

---

## Appendix B: Key Tables Reference

```
Release Management Tables in ServiceNow:

  ┌──────────────────────┬──────────────────────────────────────────┐
  │ Table                │ Purpose                                  │
  ├──────────────────────┼──────────────────────────────────────────┤
  │ release_project           │ Release records                          │
  │ release_phase     │ Phases within a release                  │
  │ release_task              │ Tasks within a release/phase             │
  │ change_request       │ Change requests linked to releases       │
  │ cmdb_ci              │ Configuration items affected             │
  │ release_feature     │ Features within a release                │
  │ change_blackout      │ Blackout/freeze periods                  │
  └──────────────────────┴──────────────────────────────────────────┘

  Key Relationships:
    release_project → release_phase (one-to-many)
    release_project → change_request   (one-to-many via release field)
    release_project → cmdb_ci          (many-to-many via affected CIs)
    release_phase → release_task    (one-to-many)
```

---

## Appendix C: ITIL 4 Exam Alignment

```
Release Management concepts tested in ITIL 4 Foundation & CDS:

  1. Purpose of Release Management practice
  2. Difference between release, deployment, and change
  3. Release types and when to use each
  4. Release models (big-bang, phased, canary, blue-green)
  5. Role of release management in the Service Value Chain
  6. Post-Implementation Review purpose and content
  7. Relationship between Release Management and:
     - Change Enablement
     - Deployment Management
     - Service Validation and Testing
     - IT Asset Management

  Key exam tips:
  - Release Management makes services AVAILABLE FOR USE
  - Deployment Management handles the TECHNICAL MOVEMENT
  - Change Enablement provides the AUTHORIZATION
  - All three work together but are DISTINCT practices
```

---

## Summary

```
What you accomplished in this lab:

  ✓ Understood ITIL 4 Release Management practice and its distinctions
    from Change and Deployment Management

  ✓ Created a major Release record (UPI Platform v3.2.0) with full
    scope documentation

  ✓ Linked four Change Requests to the release with proper sequencing

  ✓ Defined five release phases with quality gates and approval
    checkpoints

  ✓ Built a detailed deployment plan with nine sequenced tasks,
    including canary traffic ramp-up and rollback procedures

  ✓ Used the Release Calendar to identify conflicts and defined
    blackout periods for month-end, Diwali, and RBI audits

  ✓ Completed a Post-Implementation Review with metrics, lessons
    learned, and stakeholder sign-off

  ✓ Explored the Release Dashboard for executive reporting

Next Lab: Lab 17 will cover Service Level Management — defining,
monitoring, and reporting on SLAs for UPI services.
```

---

**End of Lab 16**
