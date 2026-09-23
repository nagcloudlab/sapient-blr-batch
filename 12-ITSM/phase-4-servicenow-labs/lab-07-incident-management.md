# Lab 07: Incident Management

**Level:** Intermediate | **Duration:** 90 minutes | **Prerequisites:** Lab 01-06 completed

---

## Objective

By the end of this lab, you will:
- Create incidents through multiple channels
- Manage the full incident lifecycle (New → In Progress → Resolved → Closed)
- Configure the priority matrix (Impact x Urgency)
- Assign and escalate incidents
- Link incidents to CIs, problems, and knowledge articles
- Use incident templates

---

## Part 1: Create Your First Incident

### Step 1.1: Create via the Form

1. Navigate to **Incident > Create New**
2. Fill in the form:

   | Field | Value |
   |---|---|
   | Caller | Abel Tuter (search and select) |
   | Category | Software |
   | Subcategory | Email |
   | Short description | Unable to access email from mobile device |
   | Description | User reports that email on iPhone has stopped syncing after latest update. Tried restarting the device. All other apps work fine. |
   | Impact | 2 - Medium |
   | Urgency | 2 - Medium |
   | Assignment group | Service Desk |
   | Assigned to | Beth Anglin |

3. **Before clicking Submit**, observe:
   - **Priority** is auto-calculated from Impact x Urgency
   - **State** defaults to "New"
   - **Number** will be auto-assigned on submit

4. Click **Submit**
5. Note the incident number (e.g., INC0010001)

### Step 1.2: The Priority Matrix

Priority is calculated automatically:

```
                    Impact
                1-High  2-Medium  3-Low
Urgency  1-High    1        2        3
         2-Medium  2        3        4
         3-Low     3        4        5

Priority values:
  1 = Critical    (Impact:High + Urgency:High)
  2 = High        (High+Medium or Medium+High)
  3 = Moderate    (High+Low, Medium+Medium, Low+High)
  4 = Low         (Medium+Low, Low+Medium)
  5 = Planning    (Low+Low)
```

### Step 1.3: Create a P1 Critical Incident

1. Navigate to **Incident > Create New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Caller | David Loo (or any demo user) |
   | Category | Network |
   | Subcategory | VPN |
   | Short description | VPN service down - all remote users affected |
   | Description | VPN gateway is unreachable. Over 500 remote users cannot connect. Started at 9:00 AM. |
   | Impact | 1 - High |
   | Urgency | 1 - High |
   | Assignment group | Network |
   | Assigned to | (leave empty for now) |

3. Click **Submit**
4. Note: Priority = **1 - Critical** (auto-calculated)
5. Record the number: ___________

### Step 1.4: Create More Incidents

Create these additional incidents for practice:

| # | Caller | Category | Short Description | Impact | Urgency | Group |
|---|---|---|---|---|---|---|
| 3 | Fred Luddy | Hardware | Laptop screen flickering | 3-Low | 2-Med | Hardware |
| 4 | Abel Tuter | Software | Cannot print to network printer | 2-Med | 3-Low | Service Desk |
| 5 | Beth Anglin | Network | WiFi keeps disconnecting in Bldg 2 | 2-Med | 2-Med | Network |

---

## Part 2: Incident Lifecycle

### Step 2.1: Work Through the Lifecycle

Open the P1 incident you created (VPN service down).

**State 1: New → In Progress**
1. Open the incident
2. Change **Assigned to**: select a user (e.g., ITIL User or Beth Anglin)
3. Change **State** to: **In Progress**
4. Add a **Work note**: "Investigating VPN gateway. Checking firewall logs and VPN concentrator status."
5. Click **Update**

**State 2: In Progress (working on it)**
1. Reopen the incident
2. Add another work note: "Root cause identified - VPN concentrator certificate expired. Renewing certificate now."
3. Click **Update**

**State 3: In Progress → Resolved**
1. Reopen the incident
2. Change **State** to: **Resolved**
3. Fill in Resolution fields:
   - **Resolution code**: Solved (Permanently)
   - **Resolution notes**: "VPN concentrator SSL certificate had expired. Renewed the certificate and restarted the VPN service. All remote users can now connect. Monitoring for stability."
4. Add **Additional comments** (customer-visible): "The VPN service has been restored. Please try connecting again. Contact us if you still experience issues."
5. Click **Update**

**State 4: Resolved → Closed**
1. Reopen the incident
2. Change **State** to: **Closed**
3. Fill in:
   - **Close code**: Solved (Permanently)
   - **Close notes**: "Confirmed VPN is stable. No further reports from users."
4. Click **Update**

### Step 2.2: Review the Activity Stream

1. Open the closed incident
2. Scroll to the **Activity Stream**
3. Review the full timeline:
   ```
   [timestamp] State changed from New to In Progress
   [timestamp] Work note: "Investigating VPN gateway..."
   [timestamp] Work note: "Root cause identified..."
   [timestamp] State changed from In Progress to Resolved
   [timestamp] Resolution notes: "VPN concentrator SSL..."
   [timestamp] Additional comments: "The VPN service has been restored..."
   [timestamp] State changed from Resolved to Closed
   [timestamp] Close notes: "Confirmed VPN is stable..."
   ```
4. This is the complete audit trail -- essential for compliance and review

---

## Part 3: Assignment and Escalation

### Step 3.1: Assignment Rules

Assignment rules auto-assign incidents based on conditions.

1. Navigate to **System Policy > Rules > Assignment** (or type `sysrule_assignment.list`)
2. Click **New**
3. Create a rule:

   | Field | Value |
   |---|---|
   | Name | Auto-assign Network incidents |
   | Table | Incident [incident] |
   | Active | Checked |
   | Conditions | Category is Network |
   | Group | Network |

4. Click **Submit**
5. **Test it:** Create a new incident with Category = Network
6. After submit, open it -- it should be auto-assigned to the Network group

### Step 3.2: Manual Escalation

1. Open an incident that's assigned to Service Desk
2. Change **Assignment group** to: **Network** (escalating to a different team)
3. Add a work note: "Escalating to Network team - this requires network infrastructure expertise"
4. Click **Update**
5. Note: The **Reassignment count** field increments automatically

### Step 3.3: Functional Escalation (L1 → L2 → L3)

Simulate a tiered support escalation:

1. Create a new incident:
   - Short description: "Application timeout errors on internal portal"
   - Assignment group: **Service Desk** (L1)
   - Priority: 2 - High

2. As L1 (Service Desk):
   - Add work note: "Attempted basic troubleshooting. Cleared user cache, verified network. Issue persists. Escalating to L2."
   - Change Assignment group to: **Software** (L2)
   - Click **Update**

3. As L2 (Software):
   - Add work note: "Application logs show database connection pool exhaustion. This is a database issue. Escalating to L3."
   - Change Assignment group to: **Database** (L3, create this group if needed)
   - Click **Update**

4. As L3 (Database):
   - Add work note: "Found deadlock in transaction processing. Killed blocking sessions. Increased connection pool. Issue resolved."
   - Change State to: **Resolved**
   - Add resolution notes
   - Click **Update**

---

## Part 4: Linking Incidents to Other Records

### Step 4.1: Link to a Configuration Item (CI)

1. Open any incident
2. Find the **Configuration item** field (cmdb_ci)
3. Click the magnifying glass and search for a CI (e.g., "Web Server" or any available CI)
4. Select the CI
5. Click **Update**
6. Now this incident is linked to a specific infrastructure component

### Step 4.2: Link to a Problem

1. Open an incident
2. Find the **Problem** field (or look in Related Records tab)
3. Search for an existing problem or create a new one first
4. Link the incident to the problem
5. This creates a relationship: "This incident was caused by this problem"

### Step 4.3: Create a Child Incident

1. Open any incident
2. Look for a **Create Child Incident** button or related link
3. Click it -- a new incident form opens pre-filled with the parent reference
4. Fill in additional details
5. Submit
6. Back on the parent incident, check the **Child Incidents** related list

### Step 4.4: Link to a Knowledge Article

1. Open an incident
2. Look for a **Knowledge** section or search icon
3. Search for relevant KB articles
4. If you find one, attach it to the incident
5. This helps future agents who encounter the same issue

---

## Part 5: Incident Templates

### Step 5.1: Create an Incident Template

1. Navigate to **Incident > Create New**
2. Fill in common fields for a recurring incident type:

   | Field | Value |
   |---|---|
   | Category | Network |
   | Subcategory | VPN |
   | Impact | 1 - High |
   | Urgency | 1 - High |
   | Assignment group | Network |
   | Short description | VPN service disruption - [LOCATION] |

3. Right-click the form header
4. Select **Save as Template** (or **Insert and Stay** > then Template)
5. Or navigate to **System Templates > Templates** (`sys_template.list`)
6. Click **New**:
   - Name: `VPN Outage P1`
   - Table: Incident
   - Template fields: set the pre-filled values
7. Click **Submit**

### Step 5.2: Use the Template

1. Navigate to **Incident > Create New**
2. Look for a **Template** bar or icon at the top of the form
3. Search for "VPN Outage P1"
4. Select it -- the form auto-fills with the template values
5. Fill in the remaining fields (caller, specific details)
6. Click **Submit**

---

## Part 6: Incident Reports (Quick Look)

### Step 6.1: View Incident Overview

1. Navigate to **Incident > Overview** (or type `incident_overview` in Filter Navigator)
2. If an overview page exists, you'll see:
   - Open incidents by priority
   - Incidents opened today
   - Average resolution time
   - Top categories

### Step 6.2: Quick Count

1. Navigate to **Incident > All**
2. Build filters and note the record count:
   - All open incidents: ___
   - Open P1 incidents: ___
   - Unassigned incidents: ___
   - Incidents opened this week: ___

---

## Part 7: Practice Exercises

### Exercise 1: Full Lifecycle

Create an incident and take it through every state:
1. New → In Progress → On Hold → In Progress → Resolved → Closed
2. At each state change, add appropriate work notes
3. When putting On Hold, set the **On hold reason** (e.g., "Awaiting Vendor")
4. Review the Activity Stream at the end -- it should show the complete history

### Exercise 2: Major Incident Simulation

1. Create a P1 incident: "Payment processing system down - all transactions failing"
2. Create 3 child incidents:
   - "Payment gateway not responding"
   - "Database replication lag detected"
   - "Load balancer health check failing"
3. Assign each child to a different group
4. Resolve child incidents one by one
5. Resolve the parent incident last
6. Add a "Cause" reference linking to a change request (if any exist)

### Exercise 3: Reporting Data

Create at least 10 incidents with varied:
- Priorities (mix of P1, P2, P3, P4)
- Categories (Network, Software, Hardware)
- Assignment groups
- States (some Open, some In Progress, some Resolved)

This data will be used in later labs for reporting and dashboards.

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created incidents through forms | Standard incident creation process |
| Managed full lifecycle | New → In Progress → Resolved → Closed |
| Configured priority matrix | Impact x Urgency = consistent prioritization |
| Escalated incidents (L1→L2→L3) | Functional escalation when expertise needed |
| Linked incidents to CIs, problems, KB | Relationships enable root cause analysis |
| Created templates | Speed and consistency for recurring incident types |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Incident** | An unplanned interruption or reduction in quality of an IT service |
| **Priority Matrix** | Impact x Urgency determines priority (auto-calculated) |
| **Lifecycle States** | New → In Progress → On Hold → Resolved → Closed |
| **Escalation** | Moving an incident to a higher-skill team (L1→L2→L3) |
| **Child Incident** | A sub-incident linked to a parent (for major incidents) |
| **Assignment Rule** | Auto-assigns incidents based on conditions |
| **Template** | Pre-filled form for recurring incident types |

---

## What's Next

In **Lab 08**, you'll work with **Problem Management** -- creating problems from recurring incidents, performing root cause analysis, and documenting known errors.

---

## Appendix: Bulk Setup via Background Script

> **Shortcut:** This script creates all incidents (including exercise data), assignment rules, and templates. The lifecycle walkthrough (Part 2), escalation practice (Part 3), and linking records (Part 4) must be done manually through the UI -- those are the core learning exercises.

### How to Run

1. Navigate to **System Definition > Scripts - Background** (or type `scripts` in Filter Navigator)
2. Paste the entire script below and click **Run script**
3. Check the output pane for confirmation messages

### What This Script Covers

| Manual Steps | What the Script Does |
|---|---|
| Steps 1.1, 1.3, 1.4 | Creates 5 initial incidents with varied priorities |
| Step 3.1 | Creates "Auto-assign Network incidents" assignment rule |
| Step 3.3 | Creates the "Application timeout" escalation incident + Database group |
| Step 5.1 | Creates the "VPN Outage P1" incident template |
| Exercise 2 | Creates the Major Incident (payment system down) + 3 child incidents |
| Exercise 3 | Creates 10 additional incidents with varied priorities, categories, and states |

### What You Still Need to Do Manually

- **Part 2** — Walk through the incident lifecycle (New → In Progress → Resolved → Closed) on the VPN incident
- **Part 3** — Practice manual escalation and reassignment through the UI
- **Part 4** — Link incidents to CIs, problems, and knowledge articles
- **Part 5** — Test using the template to create a new incident via the form
- **Part 6** — View reports and do quick counts

### The Script

```javascript
// ============================================================
// Lab 07 - Setup: Incidents, Assignment Rules, Templates
// Run in: System Definition > Scripts - Background
// Idempotent -- safe to run multiple times
// ============================================================

// --- Helper: Get sys_id of a user by user_name or name ---
function getUserSysId(userName) {
  var gr = new GlideRecord('sys_user');
  gr.addQuery('user_name', userName);
  gr.query();
  if (gr.next()) return gr.sys_id.toString();
  // Try by name
  gr = new GlideRecord('sys_user');
  gr.addQuery('name', userName);
  gr.query();
  if (gr.next()) return gr.sys_id.toString();
  return null;
}

// --- Helper: Get sys_id of a group by name ---
function getGroupSysId(groupName) {
  var gr = new GlideRecord('sys_user_group');
  gr.addQuery('name', groupName);
  gr.query();
  if (gr.next()) return gr.sys_id.toString();
  return null;
}

// --- Helper: Create a group if it doesn't exist ---
function ensureGroup(name, description) {
  var sysId = getGroupSysId(name);
  if (sysId) return sysId;
  var gr = new GlideRecord('sys_user_group');
  gr.initialize();
  gr.name = name;
  gr.description = description || '';
  gr.active = true;
  sysId = gr.insert();
  gs.info('Created group: ' + name);
  return sysId;
}

// --- Helper: Create an incident ---
function createIncident(data) {
  // Check if already exists by short_description
  var check = new GlideRecord('incident');
  check.addQuery('short_description', data.short_description);
  check.query();
  if (check.next()) {
    gs.info('Incident already exists: ' + data.short_description);
    return check.sys_id.toString();
  }
  var gr = new GlideRecord('incident');
  gr.initialize();
  gr.short_description = data.short_description;
  if (data.description) gr.description = data.description;
  if (data.caller_id) gr.caller_id = data.caller_id;
  if (data.category) gr.category = data.category;
  if (data.subcategory) gr.subcategory = data.subcategory;
  if (data.impact) gr.impact = data.impact;
  if (data.urgency) gr.urgency = data.urgency;
  if (data.assignment_group) gr.assignment_group = data.assignment_group;
  if (data.assigned_to) gr.assigned_to = data.assigned_to;
  if (data.state) gr.state = data.state;
  if (data.parent_incident) gr.parent_incident = data.parent_incident;
  var sysId = gr.insert();
  gs.info('Created incident: ' + gr.number + ' - ' + data.short_description);
  return sysId;
}

// ============================================================
// PART A: Ensure required groups exist
// ============================================================

gs.info('--- Ensuring groups exist ---');
ensureGroup('Service Desk', 'Level 1 support');
ensureGroup('Network', 'Network infrastructure team');
ensureGroup('Hardware', 'Hardware support team');
ensureGroup('Software', 'Application support team');
ensureGroup('Database', 'Database administration team');

// ============================================================
// PART B: Create initial incidents (Steps 1.1, 1.3, 1.4)
// ============================================================

gs.info('--- Creating initial incidents ---');

// Step 1.1: Email incident (P3)
createIncident({
  short_description: 'Unable to access email from mobile device',
  description: 'User reports that email on iPhone has stopped syncing after latest update. Tried restarting the device. All other apps work fine.',
  caller_id: getUserSysId('Abel Tuter'),
  category: 'software',
  subcategory: 'email',
  impact: 2,
  urgency: 2,
  assignment_group: getGroupSysId('Service Desk'),
  assigned_to: getUserSysId('Beth Anglin')
});

// Step 1.3: VPN P1 incident (leave open for lifecycle exercise)
createIncident({
  short_description: 'VPN service down - all remote users affected',
  description: 'VPN gateway is unreachable. Over 500 remote users cannot connect. Started at 9:00 AM.',
  caller_id: getUserSysId('David Loo'),
  category: 'network',
  subcategory: 'vpn',
  impact: 1,
  urgency: 1,
  assignment_group: getGroupSysId('Network')
});

// Step 1.4: Laptop screen (P4)
createIncident({
  short_description: 'Laptop screen flickering',
  caller_id: getUserSysId('Fred Luddy'),
  category: 'hardware',
  impact: 3,
  urgency: 2,
  assignment_group: getGroupSysId('Hardware')
});

// Step 1.4: Printer (P4)
createIncident({
  short_description: 'Cannot print to network printer',
  caller_id: getUserSysId('Abel Tuter'),
  category: 'software',
  impact: 2,
  urgency: 3,
  assignment_group: getGroupSysId('Service Desk')
});

// Step 1.4: WiFi (P3)
createIncident({
  short_description: 'WiFi keeps disconnecting in Bldg 2',
  caller_id: getUserSysId('Beth Anglin'),
  category: 'network',
  impact: 2,
  urgency: 2,
  assignment_group: getGroupSysId('Network')
});

// ============================================================
// PART C: Escalation incident (Step 3.3)
// ============================================================

gs.info('--- Creating escalation incident ---');

createIncident({
  short_description: 'Application timeout errors on internal portal',
  description: 'Users experiencing frequent timeout errors on the internal company portal. Issue affects multiple departments.',
  category: 'software',
  impact: 2,
  urgency: 1,
  assignment_group: getGroupSysId('Service Desk')
});

// ============================================================
// PART D: Major Incident + Child Incidents (Exercise 2)
// ============================================================

gs.info('--- Creating major incident with children ---');

var majorIncSysId = createIncident({
  short_description: 'Payment processing system down - all transactions failing',
  description: 'Complete payment processing outage. No transactions are being processed. Customer impact is severe.',
  category: 'software',
  impact: 1,
  urgency: 1,
  assignment_group: getGroupSysId('Software')
});

// Child incidents
createIncident({
  short_description: 'Payment gateway not responding',
  description: 'The payment gateway API returns 503 errors for all requests.',
  category: 'software',
  impact: 1,
  urgency: 1,
  assignment_group: getGroupSysId('Software'),
  parent_incident: majorIncSysId
});

createIncident({
  short_description: 'Database replication lag detected',
  description: 'Primary to replica replication lag exceeds 30 seconds. Queries timing out.',
  category: 'software',
  impact: 1,
  urgency: 1,
  assignment_group: getGroupSysId('Database'),
  parent_incident: majorIncSysId
});

createIncident({
  short_description: 'Load balancer health check failing',
  description: 'Load balancer reports all backend nodes as unhealthy. Traffic not being distributed.',
  category: 'network',
  impact: 1,
  urgency: 1,
  assignment_group: getGroupSysId('Network'),
  parent_incident: majorIncSysId
});

// ============================================================
// PART E: Exercise 3 - 10 varied incidents for reporting data
// ============================================================

gs.info('--- Creating reporting data incidents ---');

var reportingIncidents = [
  { short_description: 'Server CPU utilization above 95%',          category: 'hardware',  impact: 1, urgency: 2, group: 'Hardware',     state: 2 },
  { short_description: 'Disk space critically low on file server',  category: 'hardware',  impact: 2, urgency: 1, group: 'Hardware',     state: 2 },
  { short_description: 'DNS resolution failures intermittent',      category: 'network',   impact: 2, urgency: 2, group: 'Network',      state: 1 },
  { short_description: 'SSO login page returning 500 error',        category: 'software',  impact: 1, urgency: 1, group: 'Software',     state: 2 },
  { short_description: 'Backup job failed on database server',      category: 'software',  impact: 2, urgency: 3, group: 'Database',     state: 6 },
  { short_description: 'Office 365 license activation issue',       category: 'software',  impact: 3, urgency: 3, group: 'Service Desk', state: 6 },
  { short_description: 'Monitor not detected after docking',        category: 'hardware',  impact: 3, urgency: 3, group: 'Hardware',     state: 1 },
  { short_description: 'Network switch port flapping in MDF',       category: 'network',   impact: 1, urgency: 2, group: 'Network',      state: 2 },
  { short_description: 'LDAP sync not updating new hires',          category: 'software',  impact: 2, urgency: 2, group: 'Software',     state: 1 },
  { short_description: 'Printer queue stuck on 3rd floor',          category: 'hardware',  impact: 3, urgency: 2, group: 'Service Desk', state: 6 }
];

for (var i = 0; i < reportingIncidents.length; i++) {
  var ri = reportingIncidents[i];
  createIncident({
    short_description: ri.short_description,
    category: ri.category,
    impact: ri.impact,
    urgency: ri.urgency,
    assignment_group: getGroupSysId(ri.group),
    state: ri.state
  });
}

// ============================================================
// PART F: Assignment Rule (Step 3.1)
// ============================================================

gs.info('--- Creating assignment rule ---');

var ar = new GlideRecord('sysrule_assignment');
ar.addQuery('name', 'Auto-assign Network incidents');
ar.query();
if (ar.next()) {
  gs.info('Assignment rule already exists: Auto-assign Network incidents');
} else {
  ar.initialize();
  ar.name = 'Auto-assign Network incidents';
  ar.table = 'incident';
  ar.active = true;
  ar.condition = 'category=network';
  ar.group = getGroupSysId('Network');
  ar.insert();
  gs.info('Created assignment rule: Auto-assign Network incidents');
}

// ============================================================
// PART G: Incident Template (Step 5.1)
// ============================================================

gs.info('--- Creating incident template ---');

var tmpl = new GlideRecord('sys_template');
tmpl.addQuery('name', 'VPN Outage P1');
tmpl.addQuery('table', 'incident');
tmpl.query();
if (tmpl.next()) {
  gs.info('Template already exists: VPN Outage P1');
} else {
  tmpl.initialize();
  tmpl.name = 'VPN Outage P1';
  tmpl.table = 'incident';
  tmpl.template = 'category=network^subcategory=vpn^impact=1^urgency=1^assignment_group=' + getGroupSysId('Network') + '^short_description=VPN service disruption - [LOCATION]';
  tmpl.active = true;
  tmpl.insert();
  gs.info('Created template: VPN Outage P1');
}

gs.info('=== Lab 07 setup complete! ===');
```

### Verify After Running

1. **Incidents:** Navigate to `incident.list` -- you should see 18+ new incidents
2. **Assignment Rule:** Navigate to `sysrule_assignment.list` -- check "Auto-assign Network incidents"
3. **Template:** Navigate to `sys_template.list` -- check "VPN Outage P1"
4. **Major Incident:** Search for "Payment processing" -- verify 3 child incidents are linked

### Incident Summary

| Category | Count | Priorities |
|---|---|---|
| Network | 5 | P1 x2, P2 x1, P3 x1, child x1 |
| Software | 6 | P1 x2, P2 x1, P3 x1, P4 x1, child x1 |
| Hardware | 5 | P2 x2, P4 x2, P5 x1 |
| Total | 18 | Mixed for reporting |

> **Note:** This script is idempotent -- you can run it multiple times safely. After running, work through **Part 2 (Lifecycle)** manually on the VPN incident, and **Part 4 (Linking)** to practice connecting incidents to CIs and problems.
