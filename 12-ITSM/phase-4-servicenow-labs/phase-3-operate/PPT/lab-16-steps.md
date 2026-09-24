# Lab 16: Release & Deployment Management — Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-16-release-deployment-management.md`

---

## Pre-check

- [ ] Labs 12-15 done (CMDB, Incident, Problem, Change records exist)
- [ ] Users exist: ravi.kumar, amit.verma, priya.sharma, sanjay.mgr
- [ ] Groups exist: Platform Engineering, NOC
- [ ] Release Management plugin active (check: **System Definition > Plugins** > search `com.snc.release_management`)
- [ ] Logged into PDI as admin

---

## Step 1: Create the Release Record

Navigate: **Release > Create New** (or `release_project.do`)

| Field | Value |
|-------|-------|
| Short description | UPI Platform v3.2.0 — September Release |
| Type | Major |
| State | Draft |
| Priority | 2 - High |
| Risk | High |
| Release date | (Next Sunday, 02:00 AM IST) |
| Release manager | Sanjay Manager |

**Description** (paste into field):
```
UPI Platform v3.2.0 — September Major Release

SCOPE:
1. Circuit Breaker Implementation (from Problem PRB in Lab 14)
   - Resilience4j circuit breaker in UPI Transaction Service
   - Prevents cascading failures during downstream outages

2. Settlement Batch Processing Optimization
   - 40% improvement in end-of-day settlement processing time
   - Reduced database lock contention

3. New Merchant Onboarding API Endpoint
   - REST API for automated merchant VPA registration
   - Supports bulk onboarding (up to 10,000 merchants/request)

4. PostgreSQL Upgrade (14.x to 15.x)
   - Query planning improvements, security patches

DEPLOYMENT STRATEGY: Canary deployment with phased traffic ramp-up
MAINTENANCE WINDOW: Sunday 02:00 - 06:00 IST
```

Click **Submit**. Note the REL number.

---

## Step 2: Create 4 Change Requests

### Change 1: Circuit Breaker

Navigate: `change_request.do` > **New**

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

Click **Submit**.

### Change 2: Settlement Optimization

Navigate: `change_request.do` > **New**

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

Click **Submit**.

### Change 3: Merchant Onboarding API

Navigate: `change_request.do` > **New**

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

Click **Submit**.

### Change 4: PostgreSQL Upgrade

Navigate: `change_request.do` > **New**

| Field | Value |
|-------|-------|
| Short description | Upgrade PostgreSQL from 14.x to 15.x |
| Type | Normal |
| Category | Hardware |
| Priority | 2 - High |
| Risk | High |
| Assignment group | Platform Engineering |
| Assigned to | Amit Verma |
| Configuration item | UPI PostgreSQL Primary |
| Justification | Security patches, performance improvements, replication enhancements |

Click **Submit**.

---

## Step 3: Link Changes to the Release

1. Open the Release record: **UPI Platform v3.2.0 — September Release**
2. Scroll to **Change Requests** related list > click **Edit**
3. Search and add all 4 changes:
   - Implement circuit breaker pattern in UPI Transaction Service
   - Optimize settlement batch processing
   - Deploy new merchant onboarding API endpoint
   - Upgrade PostgreSQL from 14.x to 15.x
4. Click **Save**

### Add Deployment Sequence to Each Change

Open each Change > add to **Implementation plan** field:

| Change | Sequence Note |
|--------|--------------|
| PostgreSQL Upgrade | Release v3.2.0 — Deploy Sequence: 1 of 4 (FIRST — database migration) |
| Circuit Breaker | Release v3.2.0 — Deploy Sequence: 2 of 4 (after DB upgrade) |
| Settlement Optimization | Release v3.2.0 — Deploy Sequence: 2 of 4 (parallel with circuit breaker) |
| Merchant Onboarding API | Release v3.2.0 — Deploy Sequence: 3 of 4 (after Transaction Service changes) |

---

## Step 4: Add Affected CIs to Release

1. Open the Release record
2. Scroll to **Affected CIs** (or **Configuration Items**) related list > click **Edit/Add**
3. Add these CIs from Lab 07 CMDB:

| CI Name |
|---------|
| UPI Transaction Service |
| UPI Settlement Service |
| UPI PostgreSQL Primary |
| UPI PostgreSQL Replica |
| UPI Production LB |
| UPI App Server 01 |
| UPI App Server 02 |

4. Click **Save**

---

## Checkpoint

Open the Release record. Verify:
- 4 Change Requests in related list
- 7 Affected CIs linked
- State = Draft

---

## Step 5: Create 5 Release Phases

Open the Release record > scroll to **Release Phases** related list > click **New** for each.

### Phase 1: Planning & Design

| Field | Value |
|-------|-------|
| Short description | Phase 1: Planning & Design |
| Order | 100 |
| State | Open |
| Assigned to | Sanjay Manager |
| Planned start date | (Monday of release week) |
| Planned end date | (Wednesday of release week) |
| Description | Architecture review, resource allocation, risk assessment. Quality Gate: CAB approval required before proceeding to Build phase. |

Click **Submit**.

### Phase 2: Build & Integration Testing

| Field | Value |
|-------|-------|
| Short description | Phase 2: Build & Integration Testing |
| Order | 200 |
| State | Pending |
| Assigned to | Ravi Kumar |
| Planned start date | (Thursday of release week) |
| Planned end date | (Friday of release week) |
| Description | Code freeze, merge feature branches, run CI/CD pipeline. Quality Gate: All integration tests pass, code coverage above 80%, zero critical defects. |

Click **Submit**.

### Phase 3: UAT & Performance Testing

| Field | Value |
|-------|-------|
| Short description | Phase 3: UAT & Performance Testing |
| Order | 300 |
| State | Pending |
| Assigned to | Priya Sharma |
| Planned start date | (Friday of release week) |
| Planned end date | (Saturday of release week) |
| Description | User acceptance testing in staging. Load test: 50,000 TPS sustained for 30 minutes. Security scan: OWASP Top 10. Quality Gate: UAT sign-off, p99 latency < 200ms. |

Click **Submit**.

### Phase 4: Production Deployment

| Field | Value |
|-------|-------|
| Short description | Phase 4: Production Deployment |
| Order | 400 |
| State | Pending |
| Assigned to | Amit Verma |
| Planned start date | (Sunday 02:00 IST) |
| Planned end date | (Sunday 06:00 IST) |
| Description | Execute deployment plan within NPCI maintenance window. Canary deployment with traffic ramp-up. NOC monitoring throughout. Quality Gate: Smoke tests pass, error rate below 0.01%, no P1/P2 incidents within 1 hour. |

Click **Submit**.

### Phase 5: Post-Deployment Verification

| Field | Value |
|-------|-------|
| Short description | Phase 5: Post-Deployment Verification |
| Order | 500 |
| State | Pending |
| Assigned to | Priya Sharma |
| Planned start date | (Sunday 06:00 IST) |
| Planned end date | (Monday 06:00 IST — 24h soak) |
| Description | 24-hour monitoring period. Verify all transaction types, settlement processing, merchant onboarding. Conduct Post-Implementation Review. Quality Gate: PIR completed, no rollback required, stakeholder sign-off. |

Click **Submit**.

### Add Quality Gate Approvers

1. Open **Phase 1: Planning & Design** > **Approvers** related list > **New**
   - Approver: Sanjay Manager | State: Requested
   - Save

2. Open **Phase 3: UAT & Performance Testing** > **Approvers** related list > **New**
   - Approver: Sanjay Manager | State: Requested
   - Save

---

## Step 6: Create Deployment Tasks (Under Phase 4)

Open the Release record > find **Phase 4: Production Deployment** in phases > open it.

Navigate to the **Release Tasks** (or child tasks) related list > click **New** for each task.

### Task 1

| Field | Value |
|-------|-------|
| Short description | Pre-deployment: Verify staging matches production |
| Order | 10 |
| State | Pending |
| Assigned to | Amit Verma |
| Description | Confirm staging deployment is healthy. Verify all artifacts staged. Check rollback scripts tested. Confirm NOC team online. Est. duration: 15 min. |

### Task 2

| Field | Value |
|-------|-------|
| Short description | Create full PostgreSQL backup (primary + replica) |
| Order | 20 |
| State | Pending |
| Assigned to | Amit Verma |
| Description | pg_dump full backup of production database. Verify backup integrity with checksum. Store in S3 with 30-day retention. Est. duration: 20 min. |

### Task 3

| Field | Value |
|-------|-------|
| Short description | Execute PostgreSQL upgrade 14.x to 15.x |
| Order | 30 |
| State | Pending |
| Assigned to | Amit Verma |
| Description | Stop replication. Upgrade primary via pg_upgrade. Run post-upgrade optimizer stats. Verify data integrity. Restart replication. Rollback: restore from Task 2 backup (25 min). Est. duration: 30 min. |

### Task 4

| Field | Value |
|-------|-------|
| Short description | Deploy backend services with rolling restart |
| Order | 40 |
| State | Pending |
| Assigned to | Ravi Kumar |
| Description | Deploy Transaction Service with circuit breaker (canary — 1 server first). Deploy Settlement Service with batch optimization (blue-green). Verify health endpoints. Rollback: revert canary, switch LB to blue (10 min). Est. duration: 20 min. |

### Task 5

| Field | Value |
|-------|-------|
| Short description | Deploy merchant onboarding API endpoint |
| Order | 50 |
| State | Pending |
| Assigned to | Ravi Kumar |
| Description | Deploy new API endpoint (additive — no existing functionality modified). Verify health check. Run sample API call with test merchant. Rollback: remove endpoint route (5 min). Est. duration: 10 min. |

### Task 6

| Field | Value |
|-------|-------|
| Short description | Update load balancer for canary traffic split |
| Order | 60 |
| State | Pending |
| Assigned to | Amit Verma |
| Description | Route 5% of UPI transaction traffic to canary (v3.2.0). 95% stays on v3.1.x. Auto-remove canary if error rate > 1%. Est. duration: 10 min. |

### Task 7

| Field | Value |
|-------|-------|
| Short description | Execute production smoke test suite |
| Order | 70 |
| State | Pending |
| Assigned to | Priya Sharma |
| Description | Run smoke tests: UPI P2P transaction, P2M payment, settlement batch trigger, merchant API test, DB query performance. Any failure triggers rollback assessment. Est. duration: 15 min. |

### Task 8

| Field | Value |
|-------|-------|
| Short description | Canary traffic ramp-up: 5% to 25% to 50% to 100% |
| Order | 80 |
| State | Pending |
| Assigned to | Priya Sharma |
| Description | Ramp traffic to v3.2.0: 5% (10 min) > 25% (10 min) > 50% (10 min) > 100%. At each stage monitor error rate < 0.01%, p99 < 200ms, success rate > 99.95%. RED = immediate rollback. Est. duration: 40 min. |

### Task 9

| Field | Value |
|-------|-------|
| Short description | Full rollout complete — final verification |
| Order | 90 |
| State | Pending |
| Assigned to | Sanjay Manager |
| Description | All servers running v3.2.0. Final verification of all services. Confirm NOC dashboards green. Send deployment completion notification. Update release state to Review. Est. duration: 10 min. |

---

## Step 7: Walk Release Through States

### 7a: Draft to Planning

1. Open the Release record
2. Set State = **Planning**
3. Add work note: "Release scope finalized. 4 changes linked, 7 CIs identified. 5 phases defined with quality gates."
4. Click **Update**

### 7b: Planning to Build

1. Impersonate Sanjay Manager > approve Phase 1 quality gate > End impersonation
2. Set State = **Build**
3. Add work note: "CAB approval received. Code freeze initiated. CI/CD pipeline triggered."
4. Click **Update**

### 7c: Build to Test

1. Set State = **Test**
2. Add work note: "All integration tests passed. Code coverage: 84%. Zero critical defects. Proceeding to UAT."
3. Click **Update**

### 7d: Test to Deploy

1. Impersonate Sanjay Manager > approve Phase 3 quality gate (UAT sign-off) > End impersonation
2. Set State = **Deploy**
3. Add work note: "UAT approved. Performance benchmarks met (p99: 185ms). Sunday maintenance window confirmed. NOC team briefed."
4. Click **Update**

### 7e: Deploy to Review

1. Add work note:
   ```
   Deployment completed at 05:15 AM (25 min overrun — PG upgrade took longer).
   All 4 changes deployed successfully:
   - PostgreSQL upgraded to 15.x
   - Circuit breaker active, state: CLOSED
   - Settlement batch optimization live
   - Merchant API responding to health checks
   Canary ramp-up completed with no rollback triggers.
   ```
2. Set State = **Review**
3. Click **Update**

### 7f: Post-Implementation Review

Add work note with PIR content:
```
POST-IMPLEMENTATION REVIEW: UPI Platform v3.2.0

Planned End: 04:50 | Actual End: 05:15 | Overrun: 25 min
Cause: PostgreSQL optimizer stats rebuild slower on production data volume

RESULTS:
  CHG: PostgreSQL Upgrade      - SUCCESS (with delay)
  CHG: Circuit Breaker         - SUCCESS
  CHG: Settlement Optimization - SUCCESS
  CHG: Merchant API            - SUCCESS
  Overall: SUCCESSFUL - No rollback required

METRICS (Before vs After):
  Avg latency:    145ms -> 128ms (-12%)
  p99 latency:    280ms -> 195ms (-30%)
  Settlement:     47min -> 29min (-38%)
  Error rate:     0.008% -> 0.005% (-37%)

LESSONS LEARNED:
  1. Add 50% buffer to DB migration time estimates
  2. Create separate "deployment mode" alert profiles for canary
  3. Formalize 30-minute stakeholder communication cadence
```

Click **Update**.

### 7g: Review to Closed

1. Set State = **Closed**
2. Close notes: "PIR completed. Release successful with 25-min overrun. All metrics improved. Two process improvements documented."
3. Click **Update**

---

## Step 8: Create Blackout Periods

Navigate: **Change > Administration > Blackout Schedule** (or `change_blackout.list`)

### Blackout 1: Month-End Settlement

Click **New**.

| Field | Value |
|-------|-------|
| Name | Month-End Settlement Processing — No Deployments |
| Type | Blackout |
| Begin date | Sep 28, 2026 00:00 |
| End date | Oct 1, 2026 23:59 |
| Description | No deployments during end-of-month settlement reconciliation. UPI settlement volumes peak. Any deployment failure could impact settlement accuracy for 350+ banks. |

Click **Submit**.

### Blackout 2: Diwali Festival

Click **New**.

| Field | Value |
|-------|-------|
| Name | Diwali 2026 — Complete Change Freeze |
| Type | Blackout |
| Begin date | Oct 19, 2026 00:00 |
| End date | Oct 26, 2026 23:59 |
| Description | UPI transaction volumes surge 300-400% during Diwali. No changes permitted. All hands on monitoring. Exceptions: P1 security vulnerabilities only (CISO approval). Expected volume: 600+ million transactions/day. |

Click **Submit**.

---

## Step 9: Verify Release Calendar

1. Navigate: **Release > Release Calendar** (or **Change > Change Calendar**)
2. Verify:
   - Your release **UPI Platform v3.2.0** appears on the planned Sunday
   - Blackout periods visible on the calendar (Month-End, Diwali)
   - No scheduling conflicts with blackout windows
3. Click on the release to confirm linked changes and phases are visible

---

## Quick Verification Checklist

- [ ] Release record created: UPI Platform v3.2.0 (release_project table)
- [ ] 4 Change Requests created and linked to the release
- [ ] 7 Affected CIs linked to the release
- [ ] 5 Release Phases created with quality gates (Phases 1 and 3 have approvers)
- [ ] 9 Deployment Tasks created under Phase 4
- [ ] Release walked through all states: Draft > Planning > Build > Test > Deploy > Review > Closed
- [ ] PIR documented with metrics comparison and lessons learned
- [ ] 2 Blackout periods created (Month-End, Diwali)
- [ ] Release Calendar verified with release and blackout visibility

---

## Shortcut: Background Script

If running behind, go to **System Definition > Scripts - Background** and run the scripts from the Appendix in `lab-16-release-deployment-management.md`. Run them in order:

1. **Script 1** — Creates the Release record (note the sys_id from output)
2. **Script 2** — Creates 4 Change Requests and links to release (paste release sys_id)
3. **Script 3** — Creates 5 Release Phases (paste release sys_id)
4. **Script 4** — Creates 9 Deployment Tasks (paste Phase 4 sys_id)

You still need to walk through state transitions, quality gate approvals, PIR, and blackout periods manually.

---

*For detailed ITIL theory, deployment models, release pipeline diagrams, exercises, and background script code, see the full lab doc.*
