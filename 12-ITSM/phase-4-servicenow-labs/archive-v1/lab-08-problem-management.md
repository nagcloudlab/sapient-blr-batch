# Lab 08: Problem Management

**Level:** Intermediate | **Duration:** 75 minutes | **Prerequisites:** Lab 07A completed (demo stack running, `[AUTO]` incidents exist) | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand the difference between incidents and problems
- Create a problem from recurring UPI payment incidents
- Perform root cause analysis (RCA) using real monitoring data
- Document known errors and workarounds
- Link problems to incidents and change requests
- Manage the full problem lifecycle

---

## Scenario: UPI Payment Outage Investigation

```
  Day 1: Your UPI Transaction Service experiences a sudden spike in failures.
         Prometheus detects it, AlertManager fires alerts, and ServiceNow
         auto-creates 4 incidents via the snow-bridge.

  Day 2: The service desk resolves the immediate issue (workaround applied).
         But the question remains — WHY did it happen? Can it happen again?

  Day 3: The Platform Engineering team opens a PROBLEM to investigate.
         This lab follows their investigation from start to finish.
```

---

## Part 1: Incident vs Problem — The Core Difference

```
Incident:  "The UPI service is failing — restore it NOW!"      (reactive)
Problem:   "WHY do UPI payments keep failing?"                  (proactive)

  Incident = Symptom       →  Goal: Restore service ASAP
  Problem  = Root Cause    →  Goal: Prevent it from happening again
```

### How They Connect

```
  Problem: PRB0040001 — UPI Transaction Service instability
     |
     |  "One root cause caused all these incidents"
     |
     +--- INC: [AUTO] UPI transaction failure rate above 50%
     +--- INC: [AUTO] UPI settlement failures detected
     +--- INC: [AUTO] High HTTP 5xx error rate on upi-transaction-service
     +--- INC: [AUTO] UPI Transaction Service is DOWN
     |
     |  "The permanent fix goes through Change Management"
     |
     +--- CHG: Secure chaos endpoints + add circuit breaker
```

---

## Part 2: Review Your Existing Incidents

### Step 2.1: Find the Auto-Created Incidents

1. Navigate to **Incident > All** (or type `incident.list`)
2. Click the **funnel icon** to open the filter
3. Set: **Short description** | **contains** | `AUTO`
4. Click **Run**
5. You should see incidents auto-created by the monitoring stack in Lab 07A:

| Incident | Short Description | Priority |
|---|---|---|
| INC0010001 | [AUTO] UPI transaction failure rate above 50% | P1 Critical |
| INC0010002 | [AUTO] UPI settlement failures detected | P3 Moderate |
| INC0010003 | [AUTO] High HTTP 5xx error rate on upi-transaction-service | P3 Moderate |
| INC0010004 | [AUTO] UPI Transaction Service is DOWN | P1 Critical |

> **Note:** Your incident numbers may differ. Any `[AUTO]` prefixed incidents from Lab 07A will work.

### Step 2.2: Spot the Pattern

All 4 incidents share:

| Field | Common Pattern |
|---|---|
| Short description | All related to UPI Transaction Service |
| Category | Software |
| Assignment group | Platform Engineering |
| Time window | All fired within minutes of each other |
| Source | All auto-created by Prometheus AlertManager |

**Key Insight:** Multiple incidents with the same root cause = time to create a **Problem**.

---

## Part 3: Create the Problem

### Step 3.1: Open the Problem Form

Navigate to **Problem > Create New** (or type `problem.do` in Filter Navigator)

### Step 3.2: Fill in the Problem

| Field | Value |
|---|---|
| Short description | UPI Transaction Service recurring failures causing payment disruptions |
| Description | (see below) |
| Category | Software |
| Impact | 1 - High |
| Urgency | 1 - High |
| Assignment group | Platform Engineering |
| Assigned to | Ravi Kumar (or any available user) |

**Description** (paste this):
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

Click **Submit** and note the Problem number (e.g., **PRB0040001**)

---

## Part 4: Link Incidents to the Problem

There are multiple ways to link incidents. Choose the one that works on your PDI.

### Method A: From the Incident Form (Recommended for Zurich)

**One-time setup — add the Problem field to the Incident form:**

1. Open any `[AUTO]` incident
2. Right-click the grey header bar → **Configure > Form Layout**
3. In the **Available** list, find **Problem** (scroll to the P section)
4. Select it and click **>** to move it to the **Selected** list
5. Click **Save**

**Now link each incident:**

1. Open an `[AUTO]` incident
2. In the **Problem** field, click the magnifying glass
3. Search for your Problem number (PRB0040001)
4. Select it → click **Update**
5. Repeat for all `[AUTO]` incidents

### Method B: From the Problem Form (Related Lists)

1. Open the Problem record (PRB0040001)
2. Right-click the header → **Configure > Related Lists**
3. Find **Incident > Problem** in the Available list
4. Move it to Selected → click **Save**
5. A **Related Incidents** list now appears at the bottom of the Problem form
6. Click **Edit** → search for `[AUTO]` incidents → add them → **Save**

### Method C: Script (Fastest)

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

### Verify the Links

Type this in Filter Navigator to see all incidents linked to your problem:
```
incident.list?sysparm_query=problem_id.number=PRB0040001
```

---

## Part 5: Root Cause Analysis (RCA)

### Step 5.1: Begin Investigation

1. Open the Problem record
2. Click **Assess** (or change **State** to **Open**)
3. Add a **Work note**:
   ```
   Starting RCA for UPI Transaction Service failures.

   Investigation plan:
   1. Review Prometheus metrics and Grafana dashboards at time of incident
   2. Analyze application logs from upi-transaction-service container
   3. Check for recent deployments or configuration changes
   4. Review service architecture for single points of failure
   ```
4. Click **Update**

### Step 5.2: Document Findings (Add Work Notes)

**Work note 2 — Metrics analysis:**
```
Reviewed Prometheus and Grafana data:
- upi_transactions_total{status="failed"} spiked from 0% to 80% at [timestamp]
- Rate of change was instantaneous — not a gradual degradation
- upi_settlement_duration_seconds showed cascading failures within 30 seconds
- P95 transaction latency remained normal — only error rate changed
- JVM heap usage was within normal limits (45% of committed heap)
- No deployment recorded in the change calendar at that time

Conclusion: Not a resource exhaustion issue. Something toggled the service
into a failure state externally.
```

**Work note 3 — Code review findings:**
```
Reviewed UPI Transaction Service source code (Spring Boot application):

FINDING: The service exposes chaos engineering endpoints at:
  POST /chaos/enable    → sets failure rate to 80%
  POST /chaos/down      → simulates complete outage
  POST /chaos/latency   → injects artificial latency

These endpoints have NO authentication. Any network-reachable client can
trigger a production outage by calling /chaos/enable.

Additionally, the UPI Settlement Service calls the Transaction Service
without a circuit breaker — when transactions fail, settlements cascade-fail
with no fallback or timeout protection.
```

### Step 5.3: Document Root Cause, Workaround, and Fix

1. Open the Problem record
2. Click the **Analysis Information** tab (between Notes and Resolution Information)
3. Fill in the three fields:

**Cause Notes** (root cause):
```
ROOT CAUSE: Unprotected chaos engineering endpoints + missing circuit breaker

1. The UPI Transaction Service exposes /chaos/* endpoints without any
   authentication or authorization. These endpoints can inject failures,
   latency, or complete outages into the production service.

2. No circuit breaker pattern exists between the UPI Settlement Service
   and Transaction Service. When transactions fail, settlement requests
   cascade-fail with no fallback, timeout, or bulkhead isolation.

3. No network segmentation prevents internal services from reaching
   the chaos endpoints.
```

**Workaround**:
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

**Fix Notes** (permanent fix):
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
   - Prevent thundering herd on recovery

4. MONITORING: Add circuit breaker state change alerts
   - Alert when circuit opens (early warning)

5. NETWORK: Restrict /chaos/* to management network only
```

4. Click **Update**
5. Add a work note: "Root cause identified. Workaround and fix documented."
6. Click **Update**

---

## Part 6: Create Known Error Article

In the Zurich release, Known Errors are created as **Knowledge Base articles** linked to the Problem (not a checkbox).

### Step 6.1: Create the Known Error Article

1. Open the Problem record (PRB0040001)
2. Scroll to **Related Links** at the bottom of the form
3. Click **"Create Known Error article"**
4. A Knowledge article form opens, pre-filled with your Problem data
5. Review and update the article:

   | Field | Value |
   |---|---|
   | Short description | Known Error: UPI Transaction Service — unprotected chaos endpoints cause payment failures |
   | Knowledge base | Known Errors (select or use default) |
   | Category | Software |
   | Article body | (pre-filled from Problem — add any extra detail) |

6. Ensure the article includes:
   - **Symptoms:** Transaction failure rate >50%, settlement failures, HTTP 5xx, service outage
   - **Root Cause:** Unprotected /chaos/* endpoints + no circuit breaker
   - **Workaround:** `curl -X POST .../chaos/disable`
   - **Permanent Fix:** Spring Security + Resilience4j (requires Change Request)
7. Set **Workflow** to **Published** (or click Publish if available)
8. Click **Submit**

### Step 6.2: Other Related Links

You also have these useful links on the Problem form:
- **Communicate Workaround** — notify affected users/teams about the workaround
- **Communicate Fix** — notify when the permanent fix is deployed
- **Related Search Results** — find similar problems or knowledge articles

### Step 6.3: View the Known Error Database (KEDB)

The KEDB in Zurich is part of the Knowledge Base:

1. Navigate to **Knowledge > Articles** (or type `kb_knowledge.list`)
2. Filter by Knowledge Base = "Known Errors" (or search for "UPI" in the search bar)
3. Your Known Error article should appear
4. Service desk agents can search this KEDB when new incidents come in:
   - New incident about UPI failures → search KEDB → find the workaround → faster resolution

```
KEDB Workflow:
  New incident comes in → Agent searches KEDB → Finds matching Known Error
  → Applies workaround → Incident resolved in minutes (not hours)
  → Links incident to existing Problem
```

---

## Part 7: Link to Change Request

### Step 7.1: Create a Change Request

1. Navigate to **Change > Create New** (or type `change_request.do`)
2. Fill in:

   | Field | Value |
   |---|---|
   | Short description | Secure UPI Transaction Service chaos endpoints and add circuit breaker |
   | Description | Implement security controls on chaos engineering endpoints and add Resilience4j circuit breaker. See Problem PRB0040001. |
   | Category | Software |
   | Type | Normal |
   | Risk | Moderate |
   | Impact | 1 - High |
   | Assignment group | Platform Engineering |

3. Click **Submit** and note the Change number (e.g., CHG0030001)

### Step 7.2: Link Change to Problem

1. Open the Problem (PRB0040001)
2. Scroll to the **Change Requests** related list at the bottom
   - If not visible: right-click header → **Configure > Related Lists** → add **Change Request** → Save
3. Click **New** or **Edit** in the Change Requests list
4. Search for CHG0030001 → add it → **Save**
5. Add a work note: "Change Request created for permanent fix. Awaiting CAB approval."
6. Click **Update**

### Step 7.3: The Complete ITSM Chain

```
DETECTION           RESPONSE            INVESTIGATION         RESOLUTION
---------           --------            -------------         ----------
Prometheus     →    AlertManager   →    Snow Bridge     →     ServiceNow
(metrics)           (routing)           (webhook)             (incident)
                                                                  |
                                                                  v
                                                              Problem
                                                              (RCA)
                                                                  |
                                                                  v
                                                            Known Error
                                                            (workaround)
                                                                  |
                                                                  v
                                                          Change Request
                                                          (permanent fix)
                                                                  |
                                                                  v
                                                            Problem Closed
                                                          (fix verified)
```

---

## Part 8: Problem Lifecycle

### Step 8.1: Lifecycle States

```
New → Assess → Root Cause Analysis → Fix in Progress → Resolved/Closed
                      |
                      v
                Known Error (stays open until permanent fix deployed)
```

### Step 8.2: Close the Problem (Practice)

1. Open the Problem record
2. Change **State** to **Resolved** (or **Closed**)
3. Fill in:
   - **Close code**: Fix Applied
   - **Close notes**: "Permanent fix deployed via CHG0030001. Chaos endpoints secured with Spring Security. Circuit breaker added. Monitoring confirms zero recurrence over 72 hours."
4. Click **Update**

> **Note:** In a real environment, you'd close only after the Change is deployed and verified (Lab 09). For practice, close it now.

---

## Part 9: Practice Exercises

### Exercise 1: UPI QR Code Payment Problem

1. Create 3 incidents:
   - "UPI QR code scan timeout on merchant POS terminals"
   - "QR code payment confirmation delayed by 60+ seconds"
   - "Merchant settlement report missing QR transactions"
2. Create a Problem: "UPI QR Code payment processing delays across merchant network"
3. Link all 3 incidents
4. Document root cause: "QR code validation service DNS resolver configured with expired upstream nameserver, causing 60-second timeout fallback"
5. Workaround: "Manually update /etc/resolv.conf on QR validation pods to use secondary DNS"
6. Mark as Known Error
7. Create a Change Request: "Update DNS configuration for QR code validation service"

### Exercise 2: Proactive Problem Management

Create a problem BEFORE any incidents occur:

1. Navigate to **Problem > Create New**
2. Short description: "UPI Settlement Service single point of failure — no redundancy"
3. Description: "The settlement service runs as a single container. If it crashes, all settlements halt. Architecture review recommends minimum 2 replicas."
4. This is **proactive** — no incidents have happened yet
5. Document fix: "Deploy with 2+ replicas behind load balancer with health-check failover"

### Exercise 3: Problem Reporting

1. Navigate to `problem.list`
2. Answer:
   - Total open problems: ___
   - Known Errors: ___
   - Problems with linked Change Requests: ___
   - Problems with 3+ related incidents: ___

---

## Lab Summary

| What You Did | ITSM Value |
|---|---|
| Identified recurring incidents | Pattern recognition — multiple symptoms, one cause |
| Created a Problem record | Shift from reactive firefighting to structured investigation |
| Performed RCA with real data | Used Prometheus/Grafana evidence in the investigation |
| Documented Known Error + workaround | Service desk can resolve future incidents faster (lower MTTR) |
| Linked Problem → Change Request | Permanent fix follows Change Management process |
| Closed the loop | Detection → Incident → Problem → Known Error → Change → Closed |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Problem** | The underlying root cause of one or more incidents |
| **Root Cause Analysis** | Structured investigation: What happened? Why? How to prevent? |
| **Known Error** | Problem with identified root cause + documented workaround |
| **KEDB** | Known Error Database — searchable by service desk for faster resolution |
| **Workaround** | Temporary fix that restores service until permanent fix is deployed |
| **Proactive Problem** | Identified through review/analysis before incidents occur |
| **Problem → Change** | Permanent fixes go through Change Management (Lab 09) |

---

## What's Next

In **Lab 09: Change Management**, you'll take the Change Request created here (CHG0030001) through the full change lifecycle — planning, CAB approval, implementation, and post-implementation review.

---

## Appendix: Bulk Setup via Background Script

> **Shortcut:** Run this single script to create all Problem records, link incidents, add investigation notes, create the Change Request, and set up exercise data.

### How to Run

1. Navigate to **System Definition > Scripts - Background**
2. Paste the script below → click **Run script**
3. Check the output pane for confirmation

### What This Script Covers

| Lab Section | What the Script Does |
|---|---|
| Part 3 | Creates the UPI Problem with full description |
| Part 4 | Links all `[AUTO]` incidents to the problem |
| Part 5 | Adds 4 investigation work notes + root cause + workaround + fix notes |
| Part 6 | Known Error article must be created manually via "Create Known Error article" link |
| Part 7 | Creates the Change Request |
| Exercise 1 | Creates 3 UPI QR Code incidents + Problem + links |
| Exercise 2 | Creates the proactive Settlement SPOF problem |

### What You Still Do Manually

- **Part 5** — Read the investigation notes to understand the RCA thought process
- **Part 6** — Click "Create Known Error article" on the Problem form (cannot be scripted)
- **Part 8** — Practice closing the problem through the UI
- **Exercise 3** — Run the reporting queries yourself

### The Script

```javascript
// ============================================================
// Lab 08 - Full Setup: Problems, Known Errors, Change Request
// Run in: System Definition > Scripts - Background
// Idempotent -- safe to run multiple times
// ============================================================

// --- Helpers ---
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
  sysId = gr.insert();
  gs.info('Created group: ' + name);
  return sysId;
}

function createIncident(data) {
  var check = new GlideRecord('incident');
  check.addQuery('short_description', data.short_description);
  check.query();
  if (check.next()) {
    gs.info('  Incident exists: ' + check.number);
    return check.sys_id.toString();
  }
  var gr = new GlideRecord('incident');
  gr.initialize();
  gr.short_description = data.short_description;
  gr.category = data.category || 'software';
  gr.impact = data.impact || 2;
  gr.urgency = data.urgency || 2;
  if (data.assignment_group) gr.assignment_group = data.assignment_group;
  var sysId = gr.insert();
  gs.info('  Created incident: ' + gr.number);
  return sysId;
}

// ============================================================
// PART A: UPI Problem + Link Incidents + Investigation Notes
// ============================================================

gs.info('--- Creating UPI Problem ---');

var problemSysId;
var pCheck = new GlideRecord('problem');
pCheck.addQuery('short_description', 'UPI Transaction Service recurring failures causing payment disruptions');
pCheck.query();
if (pCheck.next()) {
  gs.info('Problem already exists: ' + pCheck.number);
  problemSysId = pCheck.sys_id.toString();
} else {
  var prob = new GlideRecord('problem');
  prob.initialize();
  prob.short_description = 'UPI Transaction Service recurring failures causing payment disruptions';
  prob.description = 'Multiple incidents reported within a short time window indicating UPI Transaction Service instability:\n- Transaction failure rate exceeded 50%\n- Settlement service failures (downstream impact)\n- HTTP 5xx errors on /api/upi/pay endpoint\n- Complete service outage detected\n\nImpact: All UPI payment processing affected.\nDetected by: Prometheus + AlertManager monitoring stack.\nAffected Services: UPI Transaction Service, UPI Settlement Service.';
  prob.category = 'software';
  prob.impact = 1;
  prob.urgency = 1;
  prob.assignment_group = ensureGroup('Platform Engineering');
  prob.assigned_to = getUserSysId('ravi.kumar');
  prob.cause_notes = 'ROOT CAUSE: Unprotected chaos engineering endpoints + missing circuit breaker\n\n1. The UPI Transaction Service exposes /chaos/* endpoints without authentication. These endpoints can inject failures, latency, or outages.\n2. No circuit breaker between Settlement and Transaction services — failures cascade.\n3. No network segmentation prevents internal services from reaching chaos endpoints.';
  prob.fix_notes = 'Permanent fix:\n1. Add Spring Security to /chaos/* endpoints (admin role only)\n2. Add Resilience4j circuit breaker in Settlement Service\n3. Add rate limiting on /api/upi/pay\n4. Add circuit breaker state change alerts\n5. Restrict /chaos/* to management network only';
  prob.workaround = 'Immediate workaround:\n1. Disable chaos: curl -X POST http://upi-transaction-service:8081/chaos/disable\n2. Verify recovery on Grafana (failure rate drops to 0%)\n3. If unresponsive: docker compose restart upi-transaction-service\n4. Monitor 15 minutes for stability';
  // In Zurich, Known Error is created via "Create Known Error article" link on the form
  problemSysId = prob.insert();
  gs.info('Created Problem: ' + prob.number);

  // Add investigation work notes
  var pUpdate = new GlideRecord('problem');
  if (pUpdate.get(problemSysId)) {
    pUpdate.work_notes = 'Starting RCA for UPI Transaction Service failures.\n\nInvestigation plan:\n1. Review Prometheus metrics at time of incident\n2. Analyze application logs\n3. Check for recent deployments or config changes\n4. Review service architecture for failure points';
    pUpdate.update();
    pUpdate.work_notes = 'Metrics analysis:\n- upi_transactions_total{status="failed"} spiked from 0% to 80% instantaneously\n- Settlement failures cascaded within 30 seconds\n- P95 latency remained normal — only error rate changed\n- JVM heap at 45% — not resource exhaustion\n- No deployment in change calendar\n\nConclusion: External trigger toggled service into failure state.';
    pUpdate.update();
    pUpdate.work_notes = 'Code review findings:\n- Service exposes /chaos/enable, /chaos/down, /chaos/latency endpoints\n- NO authentication on these endpoints\n- Any network-reachable client can trigger production outage\n- Settlement Service has no circuit breaker — cascading failures';
    pUpdate.update();
    pUpdate.work_notes = 'Root cause identified. Marked as Known Error. Workaround documented. Permanent fix requires Change Request.';
    pUpdate.update();
    gs.info('  Added investigation work notes');
  }
}

// Link [AUTO] incidents
gs.info('--- Linking [AUTO] incidents ---');
var incGr = new GlideRecord('incident');
incGr.addQuery('short_description', 'CONTAINS', '[AUTO]');
incGr.query();
var linkedCount = 0;
while (incGr.next()) {
  if (incGr.problem_id.nil()) {
    incGr.problem_id = problemSysId;
    incGr.update();
    linkedCount++;
    gs.info('  Linked ' + incGr.number);
  }
}
gs.info('  Total linked: ' + linkedCount);

// ============================================================
// PART B: Change Request
// ============================================================

gs.info('--- Creating Change Request ---');
var chgCheck = new GlideRecord('change_request');
chgCheck.addQuery('short_description', 'Secure UPI Transaction Service chaos endpoints and add circuit breaker');
chgCheck.query();
if (chgCheck.next()) {
  gs.info('Change Request exists: ' + chgCheck.number);
} else {
  var chg = new GlideRecord('change_request');
  chg.initialize();
  chg.short_description = 'Secure UPI Transaction Service chaos endpoints and add circuit breaker';
  chg.description = 'Implement security controls on chaos endpoints and add Resilience4j circuit breaker.\nSee Problem PRB0040001 for root cause analysis.\n\nChanges:\n1. Spring Security on /chaos/* endpoints\n2. Resilience4j circuit breaker in Settlement Service\n3. Rate limiting on /api/upi/pay\n4. Circuit breaker state alerts';
  chg.category = 'Software';
  chg.type = 'normal';
  chg.risk = 'moderate';
  chg.impact = 1;
  chg.assignment_group = ensureGroup('Platform Engineering');
  chg.assigned_to = getUserSysId('ravi.kumar');
  chg.insert();
  gs.info('Created Change Request: ' + chg.number);
}

// ============================================================
// PART C: Exercise 1 — UPI QR Code Problem
// ============================================================

gs.info('--- Creating Exercise 1: QR Code Problem ---');
var peGroup = ensureGroup('Platform Engineering');

var qrIncidents = [
  { short_description: 'UPI QR code scan timeout on merchant POS terminals',        assignment_group: peGroup, impact: 2, urgency: 1 },
  { short_description: 'QR code payment confirmation delayed by 60+ seconds',       assignment_group: peGroup, impact: 2, urgency: 2 },
  { short_description: 'Merchant settlement report missing QR transactions',         assignment_group: peGroup, impact: 2, urgency: 2 }
];

var qrSysIds = [];
for (var i = 0; i < qrIncidents.length; i++) {
  qrSysIds.push(createIncident(qrIncidents[i]));
}

var qrProbSysId;
var qrCheck = new GlideRecord('problem');
qrCheck.addQuery('short_description', 'UPI QR Code payment processing delays across merchant network');
qrCheck.query();
if (qrCheck.next()) {
  gs.info('QR Problem exists: ' + qrCheck.number);
  qrProbSysId = qrCheck.sys_id.toString();
} else {
  var qrProb = new GlideRecord('problem');
  qrProb.initialize();
  qrProb.short_description = 'UPI QR Code payment processing delays across merchant network';
  qrProb.description = 'Multiple incidents related to QR code payment delays — scan timeouts, confirmation delays, and missing transactions in settlement reports.';
  qrProb.category = 'software';
  qrProb.impact = 2;
  qrProb.urgency = 1;
  qrProb.assignment_group = peGroup;
  qrProb.cause_notes = 'QR code validation service DNS resolver configured with expired upstream nameserver, causing 60-second timeout fallback on every DNS lookup.';
  qrProb.workaround = 'Manually update /etc/resolv.conf on QR validation pods to use secondary DNS (10.0.1.53).';
  qrProb.known_error = true;
  qrProbSysId = qrProb.insert();
  gs.info('Created QR Problem: ' + qrProb.number);
}

for (var j = 0; j < qrSysIds.length; j++) {
  var qrInc = new GlideRecord('incident');
  if (qrInc.get(qrSysIds[j]) && qrInc.problem_id.nil()) {
    qrInc.problem_id = qrProbSysId;
    qrInc.update();
    gs.info('  Linked ' + qrInc.number + ' to QR problem');
  }
}

// ============================================================
// PART D: Exercise 2 — Proactive Problem
// ============================================================

gs.info('--- Creating Exercise 2: Proactive Problem ---');
var proCheck = new GlideRecord('problem');
proCheck.addQuery('short_description', 'CONTAINS', 'Settlement Service single point of failure');
proCheck.query();
if (proCheck.next()) {
  gs.info('Proactive problem exists: ' + proCheck.number);
} else {
  var proPrb = new GlideRecord('problem');
  proPrb.initialize();
  proPrb.short_description = 'UPI Settlement Service single point of failure — no redundancy';
  proPrb.description = 'The settlement service runs as a single container with no redundancy. If it crashes, all UPI settlements halt. Architecture review recommends minimum 2 replicas with health-check failover.';
  proPrb.category = 'software';
  proPrb.impact = 1;
  proPrb.urgency = 3;
  proPrb.assignment_group = peGroup;
  proPrb.fix_notes = 'Deploy with 2+ replicas behind load balancer. Add health-check based failover. Configure auto-scaling for peak transaction periods.';
  proPrb.insert();
  gs.info('Created proactive problem: ' + proPrb.number);
}

gs.info('=== Lab 08 setup complete! ===');
```

### Verify After Running

| Check | How |
|---|---|
| Problems created | `problem.list` — should see 3 problems (UPI, QR Code, Proactive SPOF) |
| Incidents linked | `incident.list?sysparm_query=problem_id.number=PRB0040001` |
| Known Error article | **Knowledge > Articles** → search "UPI" (created via Related Links on Problem form) |
| Change Request | `change_request.list` → find chaos endpoint security change |
| Work notes | Open UPI Problem → scroll to Activity → 4 investigation notes |

> **Note:** This script is idempotent — safe to run multiple times. After running, walk through **Part 5 (RCA)** to understand the investigation thought process and **Part 8 (Close)** to practice closing through the UI.
