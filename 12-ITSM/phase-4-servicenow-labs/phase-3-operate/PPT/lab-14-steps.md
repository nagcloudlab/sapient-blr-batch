# Lab 14: Problem Management — Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-14-problem-management.md`

---

## Pre-check

- [ ] Labs 01-13 done (incidents exist, CMDB populated)
- [ ] Groups exist: Platform Engineering, Service Desk, Network
- [ ] At least 4 `[AUTO]` incidents from Lab 12 exist (or manually created UPI incidents)
- [ ] Logged into PDI as admin

---

## Step 1: Review Existing Incidents (Spot the Pattern)

Navigate: `incident.list`

1. Click the **funnel icon** to open the filter
2. Set: **Short description** | **contains** | `AUTO`
3. Click **Run**
4. You should see incidents from Lab 12:

| Incident | Short Description | Priority |
|----------|-------------------|----------|
| INC00XXXXX | [AUTO] UPI transaction failure rate above 50% | P1 Critical |
| INC00XXXXX | [AUTO] UPI settlement failures detected | P3 Moderate |
| INC00XXXXX | [AUTO] High HTTP 5xx error rate on upi-transaction-service | P3 Moderate |
| INC00XXXXX | [AUTO] UPI Transaction Service is DOWN | P1 Critical |

> Note your actual incident numbers. All share the same root cause = time to create a Problem.

---

## Step 2: Create the Problem

Navigate: **Problem > Create New** (or type `problem.do`)

| Field | Value |
|-------|-------|
| Short description | UPI Transaction Service recurring failures causing payment disruptions |
| Description | (see below) |
| Category | Software |
| Impact | 1 - High |
| Urgency | 1 - High |
| Assignment group | Platform Engineering |
| Assigned to | Ravi Kumar (or any available user) |

**Paste this as Description:**

```
Multiple incidents reported within a short time window indicating UPI Transaction
Service instability:
- Transaction failure rate exceeded 50% (INC auto-created by monitoring)
- Settlement service failures (downstream impact)
- HTTP 5xx errors on /api/upi/pay endpoint
- Complete service outage detected

Impact: All UPI payment processing affected — estimated 500+ transactions/minute.
Detected by: Prometheus + AlertManager monitoring stack.
Affected Services: UPI Transaction Service, UPI Settlement Service.
```

Click **Submit**. Record Problem number: PRB________

---

## Step 3: Link Incidents to the Problem

### Method A: From Each Incident (Recommended)

**One-time setup — add Problem field to Incident form:**

1. Open any `[AUTO]` incident
2. Right-click the grey header bar > **Configure > Form Layout**
3. Find **Problem** in the **Available** list > click **>** to move to **Selected**
4. Click **Save**

**Link each incident:**

1. Open each `[AUTO]` incident (repeat for all 4)
2. In the **Problem** field, click the magnifying glass
3. Search for your Problem number (PRB0040001)
4. Select it > click **Update**

### Method B: Background Script (Fastest)

Run in **System Definition > Scripts - Background**:

```javascript
var prob = new GlideRecord('problem');
prob.addQuery('short_description', 'CONTAINS', 'UPI Transaction Service recurring');
prob.query();
if (prob.next()) {
  var inc = new GlideRecord('incident');
  inc.addQuery('short_description', 'CONTAINS', '[AUTO]');
  inc.query();
  while (inc.next()) {
    if (inc.problem_id.nil()) {
      inc.problem_id = prob.sys_id;
      inc.update();
      gs.info('Linked ' + inc.number + ' to ' + prob.number);
    }
  }
}
```

### Verify Links

Type in Filter Navigator:
```
incident.list?sysparm_query=problem_id.number=PRB0040001
```

Expected: 4 incidents listed.

---

## Checkpoint

Open the Problem record. Scroll to the bottom. You should see a **Related Incidents** list with 3-4 linked incidents. If not visible: right-click header > **Configure > Related Lists** > add **Incident > Problem** > Save.

---

## Step 4: Begin Root Cause Analysis (RCA)

1. Open the Problem record
2. Change **State** to **Assess** (or click the **Assess** button if available)
3. Add **Work note**:

```
Starting RCA for UPI Transaction Service failures.

Investigation plan:
1. Review Prometheus metrics and Grafana dashboards at time of incident
2. Analyze application logs from upi-transaction-service container
3. Check for recent deployments or configuration changes
4. Review service architecture for single points of failure
```

4. Click **Update**

---

## Step 5: Document RCA Findings (Work Notes)

### Work note 2 — Metrics analysis

Reopen the Problem. Add **Work note**:

```
Reviewed Prometheus and Grafana data:
- upi_transactions_total{status="failed"} spiked from 0% to 80% instantaneously
- Settlement failures cascaded within 30 seconds
- P95 latency remained normal — only error rate changed
- JVM heap at 45% — not resource exhaustion
- No deployment recorded in change calendar

Conclusion: External trigger toggled service into failure state.
```

Click **Update**.

### Work note 3 — Code review

Reopen the Problem. Add **Work note**:

```
Code review findings:
- Service exposes /chaos/enable, /chaos/down, /chaos/latency endpoints
- NO authentication on these endpoints
- Any network-reachable client can trigger production outage
- Settlement Service has no circuit breaker — cascading failures with no fallback
```

Click **Update**.

---

## Step 6: Document Root Cause (Cause Notes — 5 Whys)

1. Open the Problem record
2. Click the **Analysis Information** tab (or scroll to Cause Notes / Fix Notes / Workaround fields)
3. In the **Cause Notes** field, paste:

```
ROOT CAUSE ANALYSIS — 5 Whys:

Why 1: Why did UPI payments fail?
  -> Transaction Service returned errors for 80% of requests.
Why 2: Why did the service return errors?
  -> /chaos/enable endpoint was called, injecting 80% failure rate.
Why 3: Why could /chaos/enable be called in production?
  -> Chaos endpoints have NO authentication. Any client can trigger failures.
Why 4: Why did settlement also fail?
  -> No circuit breaker between Settlement and Transaction services.
Why 5: Why no network restriction on chaos endpoints?
  -> No network segmentation for management endpoints.

SUMMARY: (1) Unprotected chaos endpoints (2) Missing circuit breaker (3) No network segmentation
```

4. Click **Update**

---

## Step 7: Document Workaround and Fix Notes

### Workaround field

In the **Workaround** field on the Analysis Information tab, paste:

```
Immediate workaround (restores service within 30 seconds):

1. Disable chaos mode:
   curl -X POST http://upi-transaction-service:8081/chaos/disable

2. Verify recovery on Grafana dashboard:
   - Transaction failure rate should drop to 0%
   - Settlement success rate should recover

3. If service is completely unresponsive, restart:
   docker compose restart upi-transaction-service

4. Monitor for 15 minutes to confirm stability
```

### Fix Notes field

In the **Fix Notes** field, paste:

```
Permanent fix (requires Change Request):

1. SECURITY: Add Spring Security to /chaos/* endpoints
   - Require admin role authentication
   - Disable chaos endpoints entirely in production profile

2. RESILIENCE: Add Resilience4j circuit breaker in Settlement Service
   - Circuit opens after 5 consecutive failures
   - Half-open after 30 seconds for retry
   - Fallback: queue settlement for retry

3. RATE LIMITING: Add rate limiter on /api/upi/pay

4. MONITORING: Add circuit breaker state change alerts

5. NETWORK: Restrict /chaos/* to management network only
```

Click **Update**.

Add **Work note**: "Root cause identified. Workaround and permanent fix documented."

Click **Update**.

---

## Step 8: Create Known Error KB Article

1. Open the Problem record
2. Scroll to **Related Links** at the bottom > click **"Create Known Error article"**
3. A Knowledge article form opens pre-filled. Update it:

| Field | Value |
|-------|-------|
| Short description | Known Error: UPI Transaction Service — unprotected chaos endpoints cause payment failures |
| Knowledge base | Known Errors (select from dropdown) |
| Category | Software |

4. Ensure the article body includes: **Symptoms** (failure rate > 50%, HTTP 5xx, service outage), **Root Cause** (unprotected /chaos/* endpoints, no circuit breaker), **Workaround** (`curl -X POST .../chaos/disable`), **Permanent Fix** (Spring Security + Resilience4j)
5. Set **Workflow** to **Published** > click **Submit**

### Verify in KEDB

Navigate: `kb_knowledge.list` > filter by Knowledge Base = "Known Errors" > your article should appear

---

## Step 10: Link Problem to Change Request

### 10a: Create the Change Request

Navigate: **Change > Create New** (or type `change_request.do`)

| Field | Value |
|-------|-------|
| Short description | Secure UPI Transaction Service chaos endpoints and add circuit breaker |
| Description | Implement security controls on chaos endpoints and add Resilience4j circuit breaker. See Problem PRB0040001 for RCA details. |
| Category | Software |
| Type | Normal |
| Risk | Moderate |
| Impact | 1 - High |
| Assignment group | Platform Engineering |

Click **Submit**. Record Change number: CHG________

### 10b: Link Change to Problem

1. Open the Problem record (PRB0040001)
2. Scroll to the **Change Requests** related list at the bottom
   - If not visible: right-click header > **Configure > Related Lists** > add **Change Request** > Save
3. Click **Edit** in the Change Requests related list
4. Search for your CHG number > add it > click **Save**
5. Add **Work note**: "Change Request created for permanent fix. Awaiting CAB approval."
6. Click **Update**

---

## Step 11: Problem Lifecycle — Walk Through States

### 11a: Assess --> Root Cause Analysis

1. Open the Problem
2. Change **State** to **Root Cause Analysis** (if not already)
3. Add work note: "RCA complete. Root cause documented in Cause Notes."
4. Click **Update**

### 11b: Root Cause Analysis --> Fix in Progress

1. Reopen the Problem
2. Change **State** to **Fix in Progress**
3. Add work note: "Change Request CHG________ submitted. Fix implementation in progress."
4. Click **Update**

### 11c: Fix in Progress --> Resolved

1. Reopen the Problem
2. Change **State** to **Resolved** (or **Closed**)
3. Fill in:
   - **Close code**: Fix Applied
   - **Close notes**: "Permanent fix deployed via CHG________. Chaos endpoints secured with Spring Security. Circuit breaker added via Resilience4j. Monitoring confirms zero recurrence over 72 hours."
4. Click **Update**

### 11d: Resolved --> Closed

1. Reopen the Problem (if separate Closed state exists)
2. Change **State** to **Closed**
3. Add work note: "Fix verified in production. Problem closed."
4. Click **Update**

---

## Quick Verification Checklist

- [ ] Problem created with full description
- [ ] 3-4 incidents linked to the Problem
- [ ] RCA documented with 5 Whys in Cause Notes
- [ ] Workaround documented in Workaround field
- [ ] Permanent fix documented in Fix Notes field
- [ ] 3+ investigation work notes added
- [ ] Known Error article created and published
- [ ] KB workaround article accessible in KEDB
- [ ] Change Request created and linked to Problem
- [ ] Problem walked through lifecycle: New > Assess > RCA > Fix in Progress > Resolved > Closed
- [ ] Activity stream shows complete investigation trail

---

## Problem Lifecycle Reference

```
New --> Assess --> Root Cause Analysis --> Fix in Progress --> Resolved --> Closed
                        |
                        v
                  Known Error (stays open until fix deployed)
```

---

## Shortcut: Background Script

If running behind, go to **System Definition > Scripts - Background** and run the script from the Appendix in `lab-14-problem-management.md`. Creates the Problem, links incidents, adds investigation notes, and creates the Change Request. The Known Error article (Step 8), KB article (Step 9), and lifecycle walkthrough (Step 11) must be done manually through the UI.

---

*For incident vs problem theory, ITSM chain diagrams, practice exercises, and background script code, see the full lab doc.*
