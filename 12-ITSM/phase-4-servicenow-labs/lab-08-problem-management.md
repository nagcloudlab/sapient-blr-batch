# Lab 08: Problem Management

**Level:** Intermediate | **Duration:** 75 minutes | **Prerequisites:** Lab 07/07A completed (incidents exist) | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand the difference between incidents and problems
- Create problems from recurring incidents
- Perform root cause analysis (RCA)
- Document known errors and workarounds
- Link problems to incidents and change requests
- Use the problem lifecycle (New → Investigation → Root Cause Identified → Known Error → Closed)

---

## Key Concept: Incident vs Problem

```
Incident:  "The service is down — fix it NOW"          (reactive, restore service)
Problem:   "WHY does the service keep going down?"      (proactive, find root cause)

Incident = Symptom
Problem  = Disease

One Problem can cause many Incidents.
```

```
                 Problem: UPI Transaction Service instability
                    |
        +-----------+-----------+-----------+
        |           |           |           |
   INC0010005  INC0010006  INC0010007  INC0010008
   (Failure    (Settlement (HTTP 5xx   (Service
    rate 50%)   failures)   errors)     down)
```

---

## Part 1: View Existing Incidents

### Step 1.1: Identify Recurring Incidents

1. Navigate to **Incident > All**
2. Filter: Short description **contains** `AUTO`
3. You should see the incidents auto-created by the monitoring stack in Lab 07A:
   - `[AUTO] UPI transaction failure rate above 50%`
   - `[AUTO] UPI settlement failures detected`
   - `[AUTO] High HTTP 5xx error rate on upi-transaction-service`
   - `[AUTO] UPI Transaction Service is DOWN`
4. Note: These are all symptoms of the **same underlying problem**

### Step 1.2: Analyze the Pattern

Look at the incidents and identify commonalities:

| Field | Common Pattern |
|---|---|
| Category | Software |
| Assignment group | Platform Engineering |
| Configuration item | UPI Transaction Service |
| Time window | All occurred within minutes of each other |
| Root cause | Same — service instability |

**Key insight:** When you see multiple incidents with the same root cause, it's time to create a **Problem**.

---

## Part 2: Create a Problem

### Step 2.1: Navigate to Problem Management

1. Navigate to **Problem > Create New** (or type `problem.do` in Filter Navigator)
2. You'll see the Problem form — similar to Incident but with different fields

### Step 2.2: Create a Problem Record

Fill in the Problem form:

| Field | Value |
|---|---|
| Short description | UPI Transaction Service recurring failures causing payment disruptions |
| Description | Multiple incidents reported within a short time window indicating UPI Transaction Service instability. Incidents include high failure rates (>50%), settlement failures, HTTP 5xx errors, and complete service outages. All incidents trace back to the UPI Transaction Service. Impact: Payment processing for all UPI users. |
| Category | Software |
| Impact | 1 - High |
| Urgency | 1 - High |
| Assignment group | Platform Engineering |
| Assigned to | Ravi Kumar |

Click **Submit** and note the Problem number (e.g., PRB0040001)

### Step 2.3: Understand Problem Fields

Open the Problem you just created and note these key fields:

| Field | Purpose |
|---|---|
| **State** | Lifecycle state (New, Open, etc.) |
| **Known error** | Checkbox — is this a documented known error? |
| **Root cause** | Text field for the identified root cause |
| **Fix** | Text field for the permanent fix |
| **Workaround** | Text field for temporary workaround |
| **Related Links** | "Create Known Error article" and other actions |

---

## Part 3: Link Incidents to the Problem

There are three ways to link incidents to a problem. Use whichever works on your PDI.

### Method A: From the Incident Form (Recommended)

**Step 1 — Add the Problem field to the Incident form (one-time setup):**

1. Navigate to **Incident > All** and open any `[AUTO]` incident
2. Right-click the grey header bar (where it says "Incident - INC00XXXXX")
3. Select **Configure > Form Layout**
4. In the **Available** list, find `Problem` (or `problem_id`)
5. Move it to the **Selected** list (place it near the Category/Assignment group area)
6. Click **Save**
7. You should now see a **Problem** reference field on the incident form

**Step 2 — Link each incident:**

For each `[AUTO]` incident:

1. Open the incident
2. Find the **Problem** field (you just added it)
3. Click the magnifying glass and search for your Problem number (e.g., PRB0040001)
4. Select it
5. Click **Update**

Repeat for all 4 `[AUTO]` UPI incidents.

### Method B: From the Problem Form (Related Incidents List)

On some PDI versions (Zurich and earlier), the Problem form supports a Related Incidents related list:

1. Open the Problem record (PRB0040001)
2. Right-click the header bar → **Configure > Related Lists**
3. Find **Incident > Problem** in the Available list
4. Move it to the Selected list → click **Save**
5. The **Related Incidents** related list now appears on the Problem form
6. Click **Edit** in the Related Incidents list
7. Search for the `[AUTO]` incidents and add them
8. Click **Save**

### Method C: Use a Script (Fastest)

Run this in **System Definition > Scripts - Background**:

```javascript
// Link all [AUTO] incidents to a problem
var prob = new GlideRecord('problem');
prob.addQuery('short_description', 'CONTAINS', 'UPI Transaction Service recurring');
prob.query();
if (prob.next()) {
  var inc = new GlideRecord('incident');
  inc.addQuery('short_description', 'CONTAINS', '[AUTO]');
  inc.query();
  while (inc.next()) {
    inc.problem_id = prob.sys_id;
    inc.update();
    gs.info('Linked ' + inc.number + ' to ' + prob.number);
  }
}
```

### Verify the Links

1. Open any `[AUTO]` incident — the **Problem** field should show PRB0040001
2. To see all incidents linked to the problem from the list view:
   - Type `incident.list` in Filter Navigator
   - Filter: **Problem** | **is** | PRB0040001
   - You should see all 4 linked incidents
3. Or type this directly in Filter Navigator:
   ```
   incident.list?sysparm_query=problem_id.number=PRB0040001
   ```

---

## Part 4: Problem Investigation

### Step 4.1: Change State to Investigation

1. Open the Problem record
2. Change **State** to: **Open** (or **Assess** depending on your PDI)
3. Add a work note: "Beginning investigation into recurring UPI Transaction Service failures. Reviewing monitoring data, application logs, and infrastructure metrics."
4. Click **Update**

### Step 4.2: Document the Investigation

Add work notes at each stage of the investigation:

**Work note 1 — Initial triage:**
```
Investigation started.
- 4 related incidents identified, all within a 5-minute window
- All incidents originate from the UPI Transaction Service
- Monitoring dashboard shows sudden spike in error rate from 0% to 80%
- Settlement service failures are a downstream effect
```

**Work note 2 — Data gathering:**
```
Reviewed Prometheus metrics and Grafana dashboards:
- upi_transactions_total{status="failed"} spiked at [timestamp]
- P95 latency remained normal during failure period
- JVM heap usage was within normal range
- No deployment or config changes recorded at that time
```

**Work note 3 — Hypothesis:**
```
Hypothesis: The service has an exposed chaos/configuration endpoint that can be
triggered externally, causing the service to enter a degraded state. This is a
design vulnerability — the chaos endpoints should not be accessible in production.
```

### Step 4.3: Identify Root Cause

1. Open the Problem record
2. Fill in the **Root cause** field:
   ```
   The UPI Transaction Service exposes chaos engineering endpoints (/chaos/enable,
   /chaos/down, /chaos/latency) without authentication. These endpoints can be
   triggered to inject failures, high latency, or complete service outage.
   Additionally, there is no circuit breaker pattern between the Settlement
   Service and Transaction Service, causing cascading failures.
   ```
3. Change **State** to the next appropriate state (e.g., **Root Cause Identified** or **Fix in Progress**)
4. Add a work note: "Root cause identified. The chaos endpoints are unprotected and there is no circuit breaker for cascading failure protection."
5. Click **Update**

---

## Part 5: Known Error and Workaround

### Step 5.1: Document the Workaround

1. Open the Problem record
2. Fill in the **Workaround** field:
   ```
   Temporary workaround:
   1. Disable chaos injection: curl -X POST http://upi-transaction-service:8081/chaos/disable
   2. Monitor the Grafana dashboard for recovery (failure rate should drop to 0%)
   3. Verify settlement service resumes normal operation
   4. If service is completely down, restart the container:
      docker compose restart upi-transaction-service
   ```
3. Click **Update**

### Step 5.2: Mark as Known Error

1. Open the Problem record
2. Check the **Known error** checkbox
3. Fill in the **Fix** field:
   ```
   Permanent fix (requires Change Request):
   1. Remove or secure chaos endpoints behind authentication in production builds
   2. Implement Spring Security to protect /chaos/* endpoints with admin role
   3. Add circuit breaker (Resilience4j) between Settlement and Transaction services
   4. Add rate limiting on the UPI payment endpoint
   5. Configure AlertManager to auto-remediate by calling /chaos/disable
      when failure rate exceeds threshold
   ```
4. Add a work note: "Marked as Known Error. Workaround documented. Permanent fix requires a Change Request for code deployment."
5. Click **Update**

### Step 5.3: What is a Known Error?

```
Known Error = A Problem where the root cause is identified AND a workaround exists

Problem Lifecycle:
  New → Open/Investigate → Root Cause Identified → Known Error → Closed

A Known Error stays open until the permanent fix is deployed via a Change Request.
```

### Step 5.4: Known Error Database (KEDB)

1. Navigate to **Problem > Known Errors** (or filter problems where Known error = true)
2. This is the **Known Error Database** — a searchable list of all documented known errors
3. This is valuable because:
   - When a new incident comes in, agents can search KEDB for a matching workaround
   - Faster resolution: "We know about this issue. Here's the workaround."

---

## Part 6: Link Problem to a Change Request

### Step 6.1: Create a Change Request (Preview for Lab 09)

1. Navigate to **Change > Create New** (or type `change_request.do`)
2. Fill in:

   | Field | Value |
   |---|---|
   | Short description | Secure UPI Transaction Service chaos endpoints and add circuit breaker |
   | Description | Implement security controls on chaos engineering endpoints and add Resilience4j circuit breaker pattern to prevent cascading failures. See Problem PRB0040001 for root cause analysis. |
   | Category | Software |
   | Type | Normal |
   | Risk | Moderate |
   | Impact | 1 - High |
   | Assignment group | Platform Engineering |
   | Assigned to | Ravi Kumar |

3. Click **Submit**
4. Note the Change number (e.g., CHG0030001)

### Step 6.2: Link the Change to the Problem

1. Open the Problem record (PRB0040001)
2. Scroll down to the related lists at the bottom
3. Look for the **Change Requests** tab (or related list)
   - If not visible: right-click the header → **Configure > Related Lists** → add **Change Request > Problem** → **Save**
4. Click **New** or **Edit** in the Change Requests related list
5. Search for the Change Request you just created (CHG0030001)
6. Select it and click **Save**
7. Add a work note: "Change Request CHG0030001 created for permanent fix. Awaiting CAB approval."
8. Click **Update**

### Step 6.3: The Full Picture

```
Problem: PRB0040001 (UPI Transaction Service instability)
    |
    |-- Root Cause: Unprotected chaos endpoints + no circuit breaker
    |-- Workaround: curl /chaos/disable + restart container
    |-- Known Error: YES
    |
    |-- Related Incidents:
    |     INC0010005 - Transaction failure rate >50%
    |     INC0010006 - Settlement failures
    |     INC0010007 - HTTP 5xx errors
    |     INC0010008 - Service DOWN
    |
    |-- Change Request:
          CHG0030001 - Secure chaos endpoints + add circuit breaker
```

---

## Part 7: Close the Problem

### Step 7.1: Close After Fix Deployment

Once the Change Request is approved and deployed (we'll do this in Lab 09), close the Problem:

1. Open the Problem record
2. Change **State** to: **Closed** (or **Resolved**)
3. Fill in close fields:
   - **Close code**: Fix Applied
   - **Close notes**: "Permanent fix deployed via CHG0030001. Chaos endpoints secured behind authentication. Circuit breaker added between Settlement and Transaction services. Monitoring confirms no further occurrences."
4. Click **Update**

> **Note:** For this lab, you can close the problem now for practice. In a real environment, you would wait until the change is deployed and verified.

---

## Part 8: Practice Exercises

### Exercise 1: Create a Problem from Scratch

1. Create 3 new incidents with a common theme:
   - "Database connection timeout on HR portal"
   - "HR self-service page loading slowly"
   - "HR leave request submission failing"
2. Create a Problem: "HR Portal database performance degradation"
3. Link all 3 incidents to the problem
4. Document root cause: "Database connection pool exhausted due to long-running queries from new reporting module"
5. Add workaround: "Restart the database connection pool service and disable the new reporting module queries"
6. Mark as Known Error
7. Create a Change Request for the permanent fix

### Exercise 2: Problem Reporting

1. Navigate to **Problem > All** (`problem.list`)
2. How many open problems exist? ___
3. How many are marked as Known Errors? ___
4. Filter by Priority = 1 — how many critical problems? ___

### Exercise 3: Proactive Problem Management

Create a proactive problem (before any incidents occur):

1. Navigate to **Problem > Create New**
2. Short description: "UPI Settlement Service single point of failure — no redundancy"
3. Description: "The settlement service runs as a single instance. If it goes down, all UPI settlements halt. This is a design risk identified during architecture review."
4. This is a **proactive** problem — identified before incidents happen
5. Document recommended fix: "Deploy settlement service with minimum 2 replicas behind a load balancer"

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created a Problem from recurring incidents | Move from reactive (incidents) to proactive (root cause) |
| Linked incidents to a problem | Shows the relationship — one cause, many symptoms |
| Performed root cause analysis | Structured investigation to find the real issue |
| Documented Known Error + workaround | Teams can use the workaround while awaiting permanent fix |
| Linked to a Change Request | Connects the fix to the change management process |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Problem** | The underlying cause of one or more incidents |
| **Root Cause Analysis (RCA)** | Structured investigation to identify why incidents occurred |
| **Known Error** | A problem with an identified root cause and documented workaround |
| **KEDB** | Known Error Database — searchable list of documented known errors |
| **Workaround** | Temporary fix to reduce/eliminate impact until permanent fix is deployed |
| **Proactive Problem Management** | Identifying and resolving problems before incidents occur |
| **Problem → Change** | Permanent fixes are deployed through Change Management |

---

## What's Next

In **Lab 09**, you'll work with **Change Management** — submitting change requests, CAB approval process, implementing changes, and post-implementation review. You'll complete the fix for the UPI problem identified in this lab.

---

## Appendix: Bulk Setup via Background Script

> **Shortcut:** This script creates the Problem record, links it to the auto-created incidents from Lab 07A, documents the root cause, workaround, marks it as Known Error, and creates the Change Request — all in one run.

### How to Run

1. Navigate to **System Definition > Scripts - Background** (or type `scripts` in Filter Navigator)
2. Paste the entire script below and click **Run script**
3. Check the output pane for confirmation messages

### What This Script Covers

| Manual Steps | What the Script Does |
|---|---|
| Step 2.2 | Creates the Problem record with full description |
| Steps 3.1-3.2 | Links all `[AUTO]` incidents to the problem |
| Steps 4.2-4.3 | Adds investigation work notes and root cause |
| Steps 5.1-5.2 | Documents workaround and marks as Known Error |
| Step 6.1 | Creates the Change Request for the permanent fix |
| Step 6.2 | Links the Change Request to the Problem |
| Exercise 1 | Creates 3 HR incidents + HR Problem + links them |
| Exercise 3 | Creates the proactive settlement service problem |

### What You Still Need to Do Manually

- **Part 4** — Read through the investigation notes to understand the RCA process
- **Part 7** — Practice closing the problem through the UI
- **Part 8 Exercise 2** — Problem reporting queries

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

// ============================================================
// PART A: Create the main UPI Problem (Step 2.2)
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
  prob.description = 'Multiple incidents reported within a short time window indicating UPI Transaction Service instability. Incidents include high failure rates (>50%), settlement failures, HTTP 5xx errors, and complete service outages. All incidents trace back to the UPI Transaction Service.\n\nImpact: Payment processing for all UPI users.\nAffected Services: UPI Transaction Service, UPI Settlement Service\nDetected by: Prometheus + AlertManager monitoring stack';
  prob.category = 'software';
  prob.impact = 1;
  prob.urgency = 1;
  prob.assignment_group = ensureGroup('Platform Engineering');
  prob.assigned_to = getUserSysId('ravi.kumar');
  prob.cause_notes = 'The UPI Transaction Service exposes chaos engineering endpoints (/chaos/enable, /chaos/down, /chaos/latency) without authentication. These endpoints can be triggered to inject failures, high latency, or complete service outage. Additionally, there is no circuit breaker pattern between the Settlement Service and Transaction Service, causing cascading failures.';
  prob.fix_notes = 'Permanent fix (requires Change Request):\n1. Remove or secure chaos endpoints behind authentication in production builds\n2. Implement Spring Security to protect /chaos/* endpoints with admin role\n3. Add circuit breaker (Resilience4j) between Settlement and Transaction services\n4. Add rate limiting on the UPI payment endpoint\n5. Configure AlertManager to auto-remediate by calling /chaos/disable when failure rate exceeds threshold';
  prob.workaround = 'Temporary workaround:\n1. Disable chaos injection: curl -X POST http://upi-transaction-service:8081/chaos/disable\n2. Monitor the Grafana dashboard for recovery (failure rate should drop to 0%)\n3. Verify settlement service resumes normal operation\n4. If service is completely down, restart the container: docker compose restart upi-transaction-service';
  prob.known_error = true;
  problemSysId = prob.insert();
  gs.info('Created Problem: ' + prob.number + ' (sys_id: ' + problemSysId + ')');

  // Add investigation work notes
  var pUpdate = new GlideRecord('problem');
  if (pUpdate.get(problemSysId)) {
    pUpdate.work_notes = 'Investigation started.\n- 4 related incidents identified, all within a 5-minute window\n- All incidents originate from the UPI Transaction Service\n- Monitoring dashboard shows sudden spike in error rate from 0% to 80%\n- Settlement service failures are a downstream effect';
    pUpdate.update();
    pUpdate.work_notes = 'Reviewed Prometheus metrics and Grafana dashboards:\n- upi_transactions_total{status="failed"} spiked suddenly\n- P95 latency remained normal during failure period\n- JVM heap usage was within normal range\n- No deployment or config changes recorded at that time';
    pUpdate.update();
    pUpdate.work_notes = 'Root cause identified: The service has exposed chaos/configuration endpoints that can be triggered externally without authentication, causing the service to enter a degraded state. This is a design vulnerability. Additionally, no circuit breaker exists between Settlement and Transaction services, leading to cascading failures.';
    pUpdate.update();
    pUpdate.work_notes = 'Marked as Known Error. Workaround documented. Permanent fix requires a Change Request for code deployment.';
    pUpdate.update();
    gs.info('  Added investigation work notes');
  }
}

// ============================================================
// PART B: Link [AUTO] incidents to the Problem (Steps 3.1-3.2)
// ============================================================

gs.info('--- Linking incidents to Problem ---');

var incGr = new GlideRecord('incident');
incGr.addQuery('short_description', 'CONTAINS', '[AUTO]');
incGr.query();
var linkedCount = 0;
while (incGr.next()) {
  if (incGr.problem_id.nil()) {
    incGr.problem_id = problemSysId;
    incGr.update();
    linkedCount++;
    gs.info('  Linked incident ' + incGr.number + ' to problem');
  } else {
    gs.info('  Incident ' + incGr.number + ' already linked to a problem');
  }
}
gs.info('  Total incidents linked: ' + linkedCount);

// ============================================================
// PART C: Create Change Request (Step 6.1)
// ============================================================

gs.info('--- Creating Change Request ---');

var chgSysId;
var chgCheck = new GlideRecord('change_request');
chgCheck.addQuery('short_description', 'Secure UPI Transaction Service chaos endpoints and add circuit breaker');
chgCheck.query();
if (chgCheck.next()) {
  gs.info('Change Request already exists: ' + chgCheck.number);
  chgSysId = chgCheck.sys_id.toString();
} else {
  var chg = new GlideRecord('change_request');
  chg.initialize();
  chg.short_description = 'Secure UPI Transaction Service chaos endpoints and add circuit breaker';
  chg.description = 'Implement security controls on chaos engineering endpoints and add Resilience4j circuit breaker pattern to prevent cascading failures between UPI Settlement and Transaction services.\n\nRoot cause from Problem: Unprotected chaos endpoints allow unauthorized service degradation.\n\nChanges required:\n1. Add Spring Security to /chaos/* endpoints (admin role only)\n2. Add Resilience4j circuit breaker in Settlement Service\n3. Add rate limiting on /api/upi/pay endpoint\n4. Update monitoring alerts for circuit breaker state changes';
  chg.category = 'Software';
  chg.type = 'normal';
  chg.risk = 'moderate';
  chg.impact = 1;
  chg.assignment_group = ensureGroup('Platform Engineering');
  chg.assigned_to = getUserSysId('ravi.kumar');
  chgSysId = chg.insert();
  gs.info('Created Change Request: ' + chg.number);
}

// ============================================================
// PART D: Exercise 1 — HR Problem with 3 incidents
// ============================================================

gs.info('--- Creating HR exercise incidents and problem ---');

var hrGroup = ensureGroup('Service Desk');

var hrIncidents = [
  { short_description: 'Database connection timeout on HR portal',      category: 'software', impact: 2, urgency: 2 },
  { short_description: 'HR self-service page loading slowly',           category: 'software', impact: 2, urgency: 3 },
  { short_description: 'HR leave request submission failing',           category: 'software', impact: 2, urgency: 2 }
];

var hrIncSysIds = [];
for (var i = 0; i < hrIncidents.length; i++) {
  var hi = hrIncidents[i];
  var hiCheck = new GlideRecord('incident');
  hiCheck.addQuery('short_description', hi.short_description);
  hiCheck.query();
  if (hiCheck.next()) {
    gs.info('  HR incident already exists: ' + hiCheck.number);
    hrIncSysIds.push(hiCheck.sys_id.toString());
  } else {
    var hiRec = new GlideRecord('incident');
    hiRec.initialize();
    hiRec.short_description = hi.short_description;
    hiRec.category = hi.category;
    hiRec.impact = hi.impact;
    hiRec.urgency = hi.urgency;
    hiRec.assignment_group = hrGroup;
    var hiSysId = hiRec.insert();
    gs.info('  Created HR incident: ' + hiRec.number);
    hrIncSysIds.push(hiSysId);
  }
}

// Create HR Problem
var hrProbSysId;
var hrProbCheck = new GlideRecord('problem');
hrProbCheck.addQuery('short_description', 'HR Portal database performance degradation');
hrProbCheck.query();
if (hrProbCheck.next()) {
  gs.info('HR Problem already exists: ' + hrProbCheck.number);
  hrProbSysId = hrProbCheck.sys_id.toString();
} else {
  var hrProb = new GlideRecord('problem');
  hrProb.initialize();
  hrProb.short_description = 'HR Portal database performance degradation';
  hrProb.description = 'Multiple incidents related to HR portal performance — connection timeouts, slow page loads, and submission failures. All point to database performance issues.';
  hrProb.category = 'software';
  hrProb.impact = 2;
  hrProb.urgency = 2;
  hrProb.assignment_group = hrGroup;
  hrProb.cause_notes = 'Database connection pool exhausted due to long-running queries from new reporting module.';
  hrProb.workaround = 'Restart the database connection pool service and temporarily disable the new reporting module queries.';
  hrProb.known_error = true;
  hrProbSysId = hrProb.insert();
  gs.info('Created HR Problem: ' + hrProb.number);
}

// Link HR incidents to HR problem
for (var j = 0; j < hrIncSysIds.length; j++) {
  var hrInc = new GlideRecord('incident');
  if (hrInc.get(hrIncSysIds[j]) && hrInc.problem_id.nil()) {
    hrInc.problem_id = hrProbSysId;
    hrInc.update();
    gs.info('  Linked ' + hrInc.number + ' to HR problem');
  }
}

// ============================================================
// PART E: Exercise 3 — Proactive Problem
// ============================================================

gs.info('--- Creating proactive problem ---');

var proCheck = new GlideRecord('problem');
proCheck.addQuery('short_description', 'UPI Settlement Service single point of failure — no redundancy');
proCheck.query();
if (proCheck.next()) {
  gs.info('Proactive problem already exists: ' + proCheck.number);
} else {
  var proPrb = new GlideRecord('problem');
  proPrb.initialize();
  proPrb.short_description = 'UPI Settlement Service single point of failure — no redundancy';
  proPrb.description = 'The settlement service runs as a single instance with no redundancy. If it goes down, all UPI settlements halt. This is a design risk identified during architecture review — no incidents have occurred yet, but the risk is significant.';
  proPrb.category = 'software';
  proPrb.impact = 1;
  proPrb.urgency = 3;
  proPrb.assignment_group = ensureGroup('Platform Engineering');
  proPrb.fix_notes = 'Deploy settlement service with minimum 2 replicas behind a load balancer. Implement health-check based failover. Add Kubernetes HPA for auto-scaling.';
  proPrb.insert();
  gs.info('Created proactive problem: ' + proPrb.number);
}

gs.info('=== Lab 08 setup complete! ===');
```

### Verify After Running

1. **Problems:** Navigate to `problem.list` — you should see 3 problems (UPI, HR, Proactive)
2. **Linked Incidents:** Open the UPI Problem — Related Incidents should list the `[AUTO]` incidents
3. **Known Errors:** Filter problems by `Known error = true` — UPI and HR problems should appear
4. **Change Request:** Navigate to `change_request.list` — find the chaos endpoint security change

### Records Created

| Record | Details |
|---|---|
| Problem: UPI failures | Root cause + workaround + Known Error + investigation notes |
| Problem: HR Portal | Exercise 1 — with 3 linked incidents |
| Problem: Settlement SPOF | Exercise 3 — proactive, no incidents yet |
| Change Request | Secure chaos endpoints + circuit breaker (feeds into Lab 09) |
| 3 HR Incidents | Linked to HR Problem |

> **Note:** This script is idempotent — you can run it multiple times safely. After running, walk through **Part 4 (Investigation)** to understand the RCA process and **Part 7 (Close)** to practice closing a problem through the UI.
