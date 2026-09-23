# Lab 09: Change Management

**Level:** Intermediate | **Duration:** 90 minutes | **Prerequisites:** Lab 08 completed (Problem + Change Request exist) | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand Normal, Standard, and Emergency change types
- Walk the Change Request from Lab 08 through its full lifecycle
- Navigate state transitions: New → Assess → Authorize → Scheduled → Implement → Review → Closed
- Simulate CAB approval process
- Use the Change Calendar and conflict detection
- Create Standard Change templates for routine UPI operations
- Handle a failed change with rollback

---

## Scenario: Deploying the UPI Security Fix

```
In Lab 08, we identified the root cause of UPI Transaction Service failures:
  - Unprotected chaos endpoints
  - Missing circuit breaker

We created Change Request: "Secure UPI Transaction Service chaos endpoints
and add circuit breaker"

Now we take that change through the full Change Management lifecycle —
planning, approval, implementation, and review.
```

---

## Part 1: Change Types Overview

```
Normal Change:     Full lifecycle — planning, CAB approval, scheduled window
                   Example: Secure chaos endpoints + add circuit breaker

Standard Change:   Pre-approved, low risk, from a template
                   Example: Add new UPI merchant VPA to whitelist

Emergency Change:  Fast-track for critical production issues
                   Example: UPI SSL certificate expired — renew immediately
```

### State Flow Comparison

```
Normal:    New → Assess → Authorize → Scheduled → Implement → Review → Closed
                            ↑ CAB approval required

Standard:  New → Scheduled → Implement → Review → Closed
                 (pre-approved — no CAB needed)

Emergency: New → Authorize → Implement → Review → Closed
                 (verbal approval, post-implementation CAB review)
```

---

## Part 2: Normal Change — Full Lifecycle

### Step 2.1: Open the Change Request from Lab 08

1. Navigate to **Change > All** (or type `change_request.list`)
2. Find the Change Request created in Lab 08:
   - Short description: "Secure UPI Transaction Service chaos endpoints and add circuit breaker"
3. Open it

> **Note:** If you didn't create this in Lab 08, create it now — see Part 2.2.

### Step 2.2: Create the Change (if not already created)

1. Navigate to **Change > Create New** (or type `change_request.do`)
2. Fill in:

| Field | Value |
|---|---|
| Type | Normal |
| Short description | Secure UPI Transaction Service chaos endpoints and add circuit breaker |
| Description | Implement security controls on chaos engineering endpoints and add Resilience4j circuit breaker to prevent cascading failures. Root cause from Problem PRB0040001. |
| Category | Software |
| Risk | Moderate |
| Impact | 1 - High |
| Assignment group | Platform Engineering |
| Assigned to | Ravi Kumar |

3. Click **Submit**

### Step 2.3: Fill in the Planning Section

1. Open the Change Request
2. Navigate to the **Planning** tab/section
3. Fill in:

| Field | Value |
|---|---|
| Planned start date | (pick a date next week, 2:00 AM IST) |
| Planned end date | (same date, 5:00 AM IST) |
| Justification | Fix root cause of 4 P1/P3 incidents (PRB0040001). Unprotected chaos endpoints allowed unauthorized service degradation. Missing circuit breaker caused cascading settlement failures. UPI payment processing for all users was impacted. |

**Implementation plan** (paste in the field):
```
1. Pre-implementation (2:00 AM):
   - Notify operations team and merchant support
   - Take configuration backup of both services
   - Verify staging environment tests passed (Spring Security + Resilience4j)

2. Deploy UPI Transaction Service v2.1 (2:15 AM):
   - Pull new Docker image with Spring Security on /chaos/* endpoints
   - Rolling restart: docker compose up -d --build upi-transaction-service
   - Verify /chaos/status returns 401 Unauthorized without auth token
   - Verify /api/upi/pay still works without auth (public endpoint)

3. Deploy UPI Settlement Service v2.1 (2:45 AM):
   - Pull new Docker image with Resilience4j circuit breaker
   - Rolling restart: docker compose up -d --build upi-settlement-service
   - Verify circuit breaker metrics in Prometheus

4. Smoke test (3:00 AM):
   - Send 100 test UPI transactions
   - Verify 100% success rate
   - Verify settlement processing works
   - Confirm circuit breaker is in CLOSED state (healthy)

5. Chaos test (3:15 AM):
   - Attempt to call /chaos/enable without auth → expect 401
   - Temporarily stop transaction service → verify circuit breaker OPENS
   - Restart transaction service → verify circuit breaker recovers to CLOSED
   - Verify settlement service queued failed settlements for retry

6. Monitor (3:30 AM - 5:00 AM):
   - Watch Grafana dashboard for 90 minutes
   - Confirm zero errors, normal latency, stable heap usage
   - Declare change successful or initiate rollback
```

**Rollback plan**:
```
1. Stop both services
2. Revert to previous Docker images (v2.0 tags)
3. docker compose up -d upi-transaction-service upi-settlement-service
4. Verify services are healthy
5. Re-apply workaround: monitor and manually disable chaos if triggered
6. Notify operations team of rollback
7. Schedule post-mortem for failed change
```

**Test plan**:
```
1. Tested in staging for 5 days with production-equivalent traffic
2. Spring Security blocks /chaos/* without valid admin JWT token
3. Resilience4j circuit breaker tested with 10-second outage injection
4. Circuit breaker opens after 5 failures, half-opens after 30s
5. Failed settlements queued and retried successfully on recovery
6. No performance degradation — P95 latency unchanged
7. JVM heap usage stable under load
```

4. Click **Update**

### Step 2.4: Move to Assess

1. Click **Assess** button (or change State to **Assess**)
2. Add work note: "All planning documents complete. Implementation, rollback, and test plans verified. Submitting for CAB review."
3. Click **Update**

### Step 2.5: Move to Authorize (CAB Approval)

1. Open the change
2. Click **Authorize** (or change State to **Authorize**)
3. Add work note: "Assessment complete. Risk: Moderate. Submitting for CAB approval."
4. Click **Update**

### Step 2.6: Simulate CAB Approval

**Add an approver:**

1. Scroll to the **Approvers** related list (or **Approval** tab)
2. If no approvers are listed, click **New**:
   - Approver: **Sanjay Manager** (or any user with `approver_user` role)
   - State: Requested
3. Click **Save**

**Approve the change:**

1. Click your **User icon** (top-right) → **Impersonate User**
2. Search for **Sanjay Manager** → select him
3. Navigate to **Self-Service > My Approvals** (or type `sysapproval_approver.list`)
4. Find the approval for your Change Request
5. Open it → click **Approve**
6. Click your **User icon** → **End Impersonation** (back to admin)

### Step 2.7: Move to Scheduled

1. Open the change (should be approved now)
2. Change State to **Scheduled**
3. Add work note: "CAB approved. Change scheduled for maintenance window."
4. Click **Update**
5. The change now appears on the **Change Calendar**

### Step 2.8: Implement

1. Change State to **Implement**
2. Add work notes simulating the implementation:

**Work note 1:**
```
2:00 AM - Pre-implementation started
- Operations team notified
- Configuration backup taken for both services
- Staging test results verified: all passed
```

**Work note 2:**
```
2:15 AM - Deploying UPI Transaction Service v2.1
- New Docker image pulled
- Rolling restart completed
- /chaos/status now returns 401 without auth token ✓
- /api/upi/pay still works without auth ✓
```

**Work note 3:**
```
2:45 AM - Deploying UPI Settlement Service v2.1
- New Docker image pulled with Resilience4j
- Rolling restart completed
- Circuit breaker metrics visible in Prometheus ✓
- Circuit breaker state: CLOSED (healthy) ✓
```

**Work note 4:**
```
3:00 AM - Smoke test results
- 100 test transactions: 100% success rate ✓
- Settlement processing: normal ✓
- P95 latency: 45ms (within SLA) ✓

3:15 AM - Chaos test results
- /chaos/enable without auth: 401 Unauthorized ✓
- Transaction service stopped → circuit breaker OPENED ✓
- Transaction service restarted → circuit breaker recovered to CLOSED ✓
- Failed settlements queued and retried successfully ✓

3:30 AM - Monitoring phase started
- Grafana dashboard shows green across all metrics
```

3. Click **Update**

### Step 2.9: Review and Close

1. Change State to **Review**
2. Add work note:
   ```
   5:00 AM - Monitoring phase complete
   - 90 minutes of stable operation
   - Zero errors, zero failed transactions
   - Circuit breaker remained in CLOSED state
   - JVM heap stable at 42% (no growth pattern)
   - Change declared SUCCESSFUL
   ```
3. Click **Update**
4. Change State to **Closed**
5. Set **Close code**: Successful
6. **Close notes**:
   ```
   Change implemented successfully during maintenance window (2:00-5:00 AM).
   - Chaos endpoints secured with Spring Security (JWT auth required)
   - Circuit breaker added between Settlement and Transaction services
   - Smoke and chaos tests passed
   - 90-minute monitoring period: zero issues
   - Workaround (manual /chaos/disable) no longer needed
   - Problem PRB0040001 can now be closed
   ```
7. Click **Update**

---

## Part 3: Standard Change — UPI Merchant Onboarding

### Step 3.1: Understand Standard Changes

Standard changes are pre-approved, low-risk, routine operations:

| Standard Change Example | Why Pre-Approved |
|---|---|
| Add UPI merchant VPA to whitelist | Done 50+ times, well-documented, low risk |
| Rotate UPI API authentication keys | Routine security, scripted procedure |
| Update UPI transaction rate limits | Configuration change, easily reversible |

### Step 3.2: Create a Standard Change

1. Navigate to **Change > Create New**
2. Set Type: **Standard**
3. Fill in:

| Field | Value |
|---|---|
| Type | Standard |
| Short description | Add new merchant VPA to UPI whitelist — BigBasket |
| Description | Standard procedure: Add merchant VPA bigbasket@hdfcbank to the UPI payment whitelist. Pre-approved, low risk. |
| Category | Software |
| Risk | Low |
| Impact | 3 - Low |
| Assignment group | Platform Engineering |

**Implementation plan**:
```
1. Add VPA entry to merchant whitelist configuration
2. Reload configuration: curl -X POST http://upi-transaction-service:8081/actuator/refresh
3. Verify merchant can receive test UPI payment
4. Confirm in merchant portal
```

**Rollback plan**: "Remove VPA entry from whitelist, reload configuration"

4. Click **Submit**

### Step 3.3: Standard Change Lifecycle

Standard changes skip the Assess and Authorize steps — no CAB needed:

1. Open the standard change
2. Move: **New → Scheduled → Implement → Review → Closed**
3. Close code: Successful
4. Close notes: "Merchant VPA bigbasket@hdfcbank added successfully. Test payment confirmed."

---

## Part 4: Emergency Change — UPI SSL Certificate Expired

### Step 4.1: Create an Emergency Change

1. Navigate to **Change > Create New**
2. Set Type: **Emergency**
3. Fill in:

| Field | Value |
|---|---|
| Type | Emergency |
| Short description | EMERGENCY: UPI payment gateway SSL certificate expired — all transactions failing |
| Description | SSL certificate on UPI payment gateway expired at 11:30 PM IST. All UPI transactions returning SSL handshake failures. Estimated impact: 500+ transactions/minute failing. Revenue loss: significant. |
| Category | Network |
| Risk | High |
| Impact | 1 - High |
| Assignment group | Platform Engineering |
| Justification | Production UPI payment processing is completely down. Immediate certificate renewal required. Verbal approval obtained from VP Engineering (Sanjay) at 11:35 PM. |

4. Click **Submit**

### Step 4.2: Emergency Change Lifecycle

```
Emergency changes get verbal approval first, formal review after:

  11:30 PM — Incident detected (auto-created by monitoring)
  11:35 PM — Verbal approval from VP Engineering
  11:40 PM — Emergency change created in ServiceNow
  11:45 PM — New SSL certificate installed
  11:50 PM — Service restored, monitoring confirmed
  Next day — Post-implementation review with CAB
```

1. Move State to **Implement**
2. Add work note:
   ```
   11:45 PM - Emergency implementation
   - New SSL certificate obtained from CA (wildcard *.npci-upi.internal)
   - Certificate installed on payment gateway
   - UPI transaction processing restored at 11:50 PM
   - Monitoring confirms 100% success rate
   - Verbal approval from Sanjay Manager at 11:35 PM (to be formalized)
   ```
3. Move to **Review**
4. Add work note:
   ```
   Post-implementation review:
   - Root cause: Certificate expiry was not monitored (no alert for cert expiry)
   - Action item: Add SSL certificate expiry monitoring (alert 30 days before expiry)
   - Action item: Create Standard Change template for SSL certificate renewal
   - This should become a proactive Problem (certificate monitoring gap)
   ```
5. Move to **Closed** → Close code: Successful

---

## Part 5: Change Calendar

### Step 5.1: View the Change Calendar

1. Navigate to **Change > Change Calendar** (or type `change_calendar`)
2. You should see your scheduled changes on the calendar
3. Click on any change to see its details
4. Use the calendar to identify potential scheduling conflicts

### Step 5.2: Create a Blackout Window

1. Navigate to **Change > Administration > Blackout Schedule** (or type `change_blackout.list`)
2. Click **New**
3. Fill in:

| Field | Value |
|---|---|
| Name | UPI Year-End Freeze — No Changes |
| Begin date | Dec 20, 2026 |
| End date | Jan 3, 2027 |
| Type | Blackout |

4. Click **Submit**
5. Any change scheduled during this window will get a warning

---

## Part 6: Practice Exercises

### Exercise 1: Failed Change with Rollback

1. Create a Normal Change: "Upgrade UPI Settlement Service database from PostgreSQL 14 to 16"
2. Walk it through: New → Assess → Authorize → Scheduled → Implement
3. During Implement, simulate a failure:
   - Work note: "Database migration script failed at step 3. Foreign key constraint violation on settlement_transactions table. Initiating rollback."
   - Work note: "Rollback complete. PostgreSQL 14 restored from backup. All settlements processing normally."
4. Move to **Review**
5. Close as **Unsuccessful** with notes on what went wrong and remediation plan

### Exercise 2: Create Change Data for Reporting

Create these changes for use in future reporting labs:

| # | Type | Short Description | Close Code |
|---|---|---|---|
| 1 | Normal | Add rate limiting to UPI /api/upi/pay endpoint | Successful |
| 2 | Normal | Migrate UPI logs to centralized ELK stack | Successful |
| 3 | Standard | Rotate UPI API authentication keys — quarterly | Successful |
| 4 | Standard | Update UPI transaction daily limit from 1L to 2L | Successful |
| 5 | Emergency | Hotfix: UPI duplicate transaction detection bypass | Successful |
| 6 | Normal | Upgrade Spring Boot from 3.2 to 3.3 across UPI services | Unsuccessful |

---

## Lab Summary

| What You Did | ITSM Value |
|---|---|
| Full Normal Change lifecycle | Structured process: plan → approve → implement → review |
| Detailed implementation plan | Reduces change failure rate — everyone knows the steps |
| CAB approval simulation | Governance — changes reviewed before production impact |
| Standard Change template | Pre-approved routine tasks — faster, no CAB bottleneck |
| Emergency Change | Fast-track for critical issues — restore first, review later |
| Failed Change with rollback | Not every change succeeds — rollback plan is essential |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Normal Change** | Full assessment + CAB approval required |
| **Standard Change** | Pre-approved template, low risk, no CAB |
| **Emergency Change** | Fast-track for critical issues, post-implementation review |
| **CAB** | Change Advisory Board — reviews and approves changes |
| **Change Calendar** | Visual schedule of all planned changes |
| **Blackout Window** | Period when no changes are permitted |
| **Rollback Plan** | Steps to undo a change if it fails |
| **Close Code** | Successful / Unsuccessful / Incomplete |

---

## What's Next

In **Lab 10: Service Catalog**, you'll create catalog items for requesting UPI services — like "Request New Merchant Onboarding" and "Request UPI API Access" — with approval workflows and fulfillment tasks.

---

## Appendix: Bulk Setup via Background Script

> **Shortcut:** This script creates all the change requests (Normal, Standard, Emergency), fills in planning details, and creates the exercise data.

### How to Run

1. Navigate to **System Definition > Scripts - Background**
2. Paste the script below → click **Run script**

### What This Script Covers

| Lab Section | What the Script Does |
|---|---|
| Part 2 | Creates the Normal Change (UPI security fix) with full planning details |
| Part 3 | Creates the Standard Change (merchant VPA onboarding) |
| Part 4 | Creates the Emergency Change (SSL certificate expired) |
| Exercise 1 | Creates the failed database upgrade change |
| Exercise 2 | Creates 6 additional changes for reporting data |

### What You Still Do Manually

- **Step 2.4-2.9** — Walk through state transitions (Assess → Authorize → Implement → Close)
- **Step 2.6** — Impersonate approver for CAB approval simulation
- **Part 5** — View Change Calendar and create Blackout Window

### The Script

```javascript
// ============================================================
// Lab 09 - Full Setup: Change Requests (Normal, Standard, Emergency)
// Run in: System Definition > Scripts - Background
// Idempotent -- safe to run multiple times
// ============================================================

function getUserSysId(userName) {
  var gr = new GlideRecord('sys_user');
  gr.addQuery('user_name', userName);
  gr.query();
  if (gr.next()) return gr.sys_id.toString();
  gr = new GlideRecord('sys_user');
  gr.addQuery('name', userName);
  gr.query();
  if (gr.next()) return gr.sys_id.toString();
  return null;
}

function getGroupSysId(groupName) {
  var gr = new GlideRecord('sys_user_group');
  gr.addQuery('name', groupName);
  gr.query();
  if (gr.next()) return gr.sys_id.toString();
  return null;
}

function ensureGroup(name) {
  var sysId = getGroupSysId(name);
  if (sysId) return sysId;
  var gr = new GlideRecord('sys_user_group');
  gr.initialize();
  gr.name = name;
  gr.active = true;
  return gr.insert();
}

function createChange(data) {
  var check = new GlideRecord('change_request');
  check.addQuery('short_description', data.short_description);
  check.query();
  if (check.next()) {
    gs.info('Change exists: ' + check.number + ' - ' + data.short_description);
    return check.sys_id.toString();
  }
  var gr = new GlideRecord('change_request');
  gr.initialize();
  gr.short_description = data.short_description;
  if (data.description) gr.description = data.description;
  if (data.type) gr.type = data.type;
  if (data.category) gr.category = data.category;
  if (data.risk) gr.risk = data.risk;
  if (data.impact) gr.impact = data.impact;
  if (data.assignment_group) gr.assignment_group = data.assignment_group;
  if (data.assigned_to) gr.assigned_to = data.assigned_to;
  if (data.justification) gr.justification = data.justification;
  if (data.implementation_plan) gr.implementation_plan = data.implementation_plan;
  if (data.backout_plan) gr.backout_plan = data.backout_plan;
  if (data.test_plan) gr.test_plan = data.test_plan;
  var sysId = gr.insert();
  gs.info('Created change: ' + gr.number + ' - ' + data.short_description);
  return sysId;
}

var peGroup = ensureGroup('Platform Engineering');
var raviId = getUserSysId('ravi.kumar');

// ============================================================
// PART A: Normal Change — UPI Security Fix (Part 2)
// ============================================================

gs.info('--- Creating Normal Change: UPI Security Fix ---');

createChange({
  short_description: 'Secure UPI Transaction Service chaos endpoints and add circuit breaker',
  description: 'Implement security controls on chaos engineering endpoints and add Resilience4j circuit breaker to prevent cascading failures between UPI Settlement and Transaction services.\n\nRoot cause from Problem PRB0040001:\n- Unprotected /chaos/* endpoints allow unauthorized service degradation\n- No circuit breaker between Settlement and Transaction services\n\nChanges:\n1. Spring Security on /chaos/* endpoints (admin JWT required)\n2. Resilience4j circuit breaker in Settlement Service\n3. Rate limiting on /api/upi/pay\n4. Circuit breaker state change alerts in Prometheus',
  type: 'normal',
  category: 'Software',
  risk: 'moderate',
  impact: 1,
  assignment_group: peGroup,
  assigned_to: raviId,
  justification: 'Fix root cause of 4 P1/P3 incidents (PRB0040001). Unprotected chaos endpoints allowed unauthorized service degradation. Missing circuit breaker caused cascading settlement failures.',
  implementation_plan: '1. Pre-implementation: Notify ops, take config backup, verify staging tests\n2. Deploy Transaction Service v2.1 with Spring Security\n3. Deploy Settlement Service v2.1 with Resilience4j\n4. Smoke test: 100 test transactions\n5. Chaos test: verify /chaos/* returns 401, circuit breaker opens/closes correctly\n6. Monitor 90 minutes on Grafana',
  backout_plan: '1. Stop both services\n2. Revert to v2.0 Docker images\n3. Restart services\n4. Verify health\n5. Re-apply manual workaround\n6. Notify ops of rollback',
  test_plan: '1. Tested in staging 5 days\n2. Spring Security blocks /chaos/* without JWT\n3. Circuit breaker opens after 5 failures, half-opens after 30s\n4. Failed settlements queued and retried on recovery\n5. No performance impact — P95 latency unchanged'
});

// ============================================================
// PART B: Standard Change — Merchant Onboarding (Part 3)
// ============================================================

gs.info('--- Creating Standard Change: Merchant Onboarding ---');

createChange({
  short_description: 'Add new merchant VPA to UPI whitelist — BigBasket',
  description: 'Standard procedure: Add merchant VPA bigbasket@hdfcbank to the UPI payment whitelist. Pre-approved, low risk.',
  type: 'standard',
  category: 'Software',
  risk: 'low',
  impact: 3,
  assignment_group: peGroup,
  implementation_plan: '1. Add VPA to merchant whitelist config\n2. Reload config\n3. Send test payment\n4. Confirm in merchant portal',
  backout_plan: 'Remove VPA from whitelist, reload configuration'
});

// ============================================================
// PART C: Emergency Change — SSL Certificate (Part 4)
// ============================================================

gs.info('--- Creating Emergency Change: SSL Certificate ---');

createChange({
  short_description: 'EMERGENCY: UPI payment gateway SSL certificate expired — all transactions failing',
  description: 'SSL certificate on UPI payment gateway expired at 11:30 PM IST. All UPI transactions returning SSL handshake failures. Impact: 500+ transactions/minute failing.',
  type: 'emergency',
  category: 'Network',
  risk: 'high',
  impact: 1,
  assignment_group: peGroup,
  justification: 'Production UPI payment processing completely down. Immediate certificate renewal required. Verbal approval from VP Engineering at 11:35 PM.',
  implementation_plan: '1. Obtain new SSL certificate from CA\n2. Install certificate on payment gateway\n3. Restart gateway service\n4. Verify transaction processing restored',
  backout_plan: 'Restore previous certificate from backup if new cert causes issues'
});

// ============================================================
// PART D: Exercise 1 — Failed Change
// ============================================================

gs.info('--- Creating Failed Change ---');

createChange({
  short_description: 'Upgrade UPI Settlement Service database from PostgreSQL 14 to 16',
  description: 'Database upgrade to PostgreSQL 16 for improved performance and security patches.',
  type: 'normal',
  category: 'Software',
  risk: 'high',
  impact: 1,
  assignment_group: peGroup,
  assigned_to: raviId,
  implementation_plan: '1. Full database backup\n2. Stop settlement service\n3. Run pg_upgrade from 14 to 16\n4. Run migration scripts\n5. Start settlement service\n6. Verify settlements processing',
  backout_plan: '1. Stop settlement service\n2. Restore PostgreSQL 14 from backup\n3. Restart settlement service\n4. Verify data integrity'
});

// ============================================================
// PART E: Exercise 2 — Reporting Data Changes
// ============================================================

gs.info('--- Creating reporting data changes ---');

var reportChanges = [
  { short_description: 'Add rate limiting to UPI /api/upi/pay endpoint',                type: 'normal',    risk: 'moderate', impact: 2, category: 'Software' },
  { short_description: 'Migrate UPI logs to centralized ELK stack',                      type: 'normal',    risk: 'moderate', impact: 2, category: 'Software' },
  { short_description: 'Rotate UPI API authentication keys — quarterly',                 type: 'standard',  risk: 'low',      impact: 3, category: 'Software' },
  { short_description: 'Update UPI transaction daily limit from 1L to 2L',               type: 'standard',  risk: 'low',      impact: 2, category: 'Software' },
  { short_description: 'Hotfix: UPI duplicate transaction detection bypass',             type: 'emergency', risk: 'high',     impact: 1, category: 'Software' },
  { short_description: 'Upgrade Spring Boot from 3.2 to 3.3 across UPI services',       type: 'normal',    risk: 'moderate', impact: 2, category: 'Software' }
];

for (var i = 0; i < reportChanges.length; i++) {
  var rc = reportChanges[i];
  rc.assignment_group = peGroup;
  createChange(rc);
}

gs.info('=== Lab 09 setup complete! ===');
```

### Verify After Running

| Check | How |
|---|---|
| All changes created | `change_request.list` — should see 10 change requests |
| Normal Change | Find "Secure UPI Transaction Service..." with full planning details |
| Standard Change | Find "Add new merchant VPA..." with Type = Standard |
| Emergency Change | Find "EMERGENCY: UPI payment gateway SSL..." with Type = Emergency |
| Exercise data | 6 additional changes with varied types and risk levels |

> **Note:** This script creates the change records with planning details pre-filled. You still need to walk through the **state transitions** (Part 2.4-2.9), **simulate CAB approval** (Part 2.6), and **view the Change Calendar** (Part 5) manually through the UI — those are the core learning exercises.
