# Lab 21: Business Rules, Client Scripts & UI Policies

**Level:** Advanced | **Duration:** 90 minutes | **Prerequisites:** Lab 20 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand the ServiceNow execution model (server-side vs client-side)
- Create Business Rules for automated server-side data manipulation and enforcement
- Build Client Scripts to control form behavior and user interactions
- Configure UI Policies for no-code field visibility, mandatory, and read-only control
- Write reusable Script Includes (class-based and client-callable)
- Create UI Actions (buttons and links) on forms
- Debug and troubleshoot scripts using ServiceNow diagnostic tools

---

## Scenario Context

NPCI's UPI Payment Platform is fully configured in ServiceNow from Labs 01-20. The ITSM processes are working, but the team needs **automation and enforcement** to reduce manual errors and speed up incident handling.

**Current Pain Points:**
- Agents forget to fill critical fields on P1 incidents
- CIs are not consistently linked to incidents
- VIP callers (bank executives, NPCI leadership) do not get priority notification
- Recurring incidents on the same CI are not automatically escalated to Problem Management
- Resolution fields are visible even when the incident is still open, causing confusion

**Your Mission:** Implement Business Rules, Client Scripts, and UI Policies to automate workflows, enforce data quality, and improve the user experience for the NOC and Service Desk teams.

**Key CIs from CMDB (Lab 12):**
| CI Name | Class | Support Group |
|---|---|---|
| UPI Transaction Service | Application Server | Platform Engineering |
| UPI Settlement Service | Application Server | Platform Engineering |
| PostgreSQL Primary | Database | Database Admin |
| NPCI API Gateway | Web Server | Platform Engineering |
| UPI Monitoring Stack | Application | NOC |

**Key Personnel:**
| Name | Role | Group |
|---|---|---|
| Ravi Kumar | Lead Engineer | Platform Engineering |
| Priya Sharma | NOC Manager | NOC |
| Meera Joshi | Service Desk Lead | Service Desk |
| Sanjay Patel | VP Engineering | Management |

---

## Part 1: Server-Side vs Client-Side Scripting

### 1.1 The ServiceNow Execution Model

ServiceNow runs code in two distinct environments:

```
┌─────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                       │
│                                                         │
│   Client Scripts  ──┐                                   │
│   UI Policies     ──┤  JavaScript (ES6+)                │
│   UI Actions*     ──┘  APIs: g_form, g_user, g_list     │
│                                                         │
│         │  HTTP / GlideAjax / Form Submit               │
│         ▼                                               │
├─────────────────────────────────────────────────────────┤
│                 SERVICENOW SERVER                       │
│                                                         │
│   Business Rules  ──┐                                   │
│   Script Includes ──┤  JavaScript (Rhino/ES5)           │
│   Scheduled Jobs  ──┤  APIs: GlideRecord, GlideSystem  │
│   UI Actions*     ──┘  current, previous, gs            │
│                                                         │
│         │                                               │
│         ▼                                               │
│   ┌─────────────┐                                       │
│   │  Database    │                                       │
│   └─────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

### 1.2 When to Use What

| Mechanism | Side | Use Case | Example |
|---|---|---|---|
| **Business Rule** | Server | Data manipulation, enforcement, cascading updates | Auto-set CI based on category |
| **Client Script** | Client | UI behavior, field interactions, real-time validation | Make fields mandatory on P1 |
| **UI Policy** | Client | No-code field visibility/mandatory/read-only | Show resolution fields when resolved |
| **Script Include** | Server | Reusable libraries, GlideAjax handlers | Utility functions for UPI operations |
| **UI Action** | Both | Buttons, links, context menu items on forms | "Escalate to P1" button |

### 1.3 Key API Comparison

| API | Side | Purpose | Example |
|---|---|---|---|
| `GlideRecord` | Server | Query/insert/update/delete records | `var gr = new GlideRecord('incident');` |
| `GlideSystem (gs)` | Server | System utilities, logging, user info | `gs.getUser().getID()` |
| `current` / `previous` | Server | Current record and its previous values (in BR) | `current.state`, `previous.state` |
| `g_form` | Client | Manipulate form fields | `g_form.setValue('priority', '1');` |
| `g_user` | Client | Current user info in browser | `g_user.hasRole('itil')` |
| `GlideAjax` | Client | Call server-side Script Include from client | Fetch data without full page reload |

### 1.4 Performance Guidelines

**Server-Side Best Practices:**
- Use `addQuery()` and `addEncodedQuery()` instead of looping through all records
- Limit GlideRecord queries in Business Rules (avoid nested loops)
- Use Async Business Rules for heavy operations (email, external calls)
- Set appropriate conditions to prevent unnecessary execution

**Client-Side Best Practices:**
- Minimize GlideAjax calls (each is an HTTP round-trip)
- Use UI Policies instead of Client Scripts for simple show/hide/mandatory
- Avoid `getReference()` in Client Scripts (synchronous, blocks UI)
- Use `g_form.getReference()` with callback instead

---

## Part 2: Business Rules — Deep Dive

### 2.1 Business Rule Types

| Type | When | Use Case | `current` writable? |
|---|---|---|---|
| **Before** | Before DB operation | Validate, modify data before save | Yes |
| **After** | After DB operation | Trigger actions after save | No (changes not saved) |
| **Async** | After (in background) | Heavy processing, external calls | No |
| **Display** | Before form loads | Add data to scratchpad for client | Read-only |

### 2.2 Execution Order

Business Rules execute in this order:
1. **Before** rules (ordered by priority 100-1000, lower = first)
2. Database operation (insert/update/delete)
3. **After** rules (ordered by priority)
4. **Async** rules (queued for background processing)
5. **Display** rules (only when form is rendered)

**Priority values:**
- 100 = runs first (highest priority)
- 1000 = runs last (lowest priority)
- Default = 100

### 2.3 The `current` and `previous` Objects

```javascript
// current = the record being saved (with new values)
// previous = the record as it was before this update

// Check if a field changed
if (current.state.changesTo(6)) {
    // State just changed to Resolved (6)
}

// Compare old and new values
if (current.priority != previous.priority) {
    gs.info('Priority changed from ' + previous.priority + ' to ' + current.priority);
}

// Check if a field has changed at all
if (current.assignment_group.changes()) {
    // Assignment group was modified
}
```

---

### Exercise 2.4: Create Business Rule — "Auto-populate CI from Category"

This rule automatically links the correct CI when an agent selects the UPI category.

**Navigation:** System Definition > Business Rules > New

| Field | Value |
|---|---|
| Name | NPCI - Auto-populate CI from Category |
| Table | Incident [incident] |
| Active | true |
| Advanced | true (check this box) |
| When to run | before |
| Insert | true |
| Update | true |
| Filter Conditions | Category is upi |
| Order | 100 |

**Script tab:**

```javascript
(function executeRule(current, previous /*null when insert*/) {

    // Map subcategory to the correct CI name
    var ciMapping = {
        'transaction':  'UPI Transaction Service',
        'settlement':   'UPI Settlement Service',
        'dispute':      'UPI Dispute Resolution',
        'merchant':     'NPCI API Gateway',
        'monitoring':   'UPI Monitoring Stack'
    };

    var subcategory = current.subcategory.toString().toLowerCase();
    var ciName = ciMapping[subcategory];

    if (!ciName) {
        // No mapping found for this subcategory — skip
        return;
    }

    // Look up the CI in the CMDB
    var gr = new GlideRecord('cmdb_ci_app_server');
    gr.addQuery('name', ciName);
    gr.setLimit(1);
    gr.query();

    if (gr.next()) {
        current.cmdb_ci = gr.sys_id;
        gs.info('NPCI BR: Auto-set CI to "' + ciName + '" for incident ' + current.number);
    } else {
        // Try the broader cmdb_ci table if not found in app_server
        var grBroad = new GlideRecord('cmdb_ci');
        grBroad.addQuery('name', ciName);
        grBroad.setLimit(1);
        grBroad.query();

        if (grBroad.next()) {
            current.cmdb_ci = grBroad.sys_id;
            gs.info('NPCI BR: Auto-set CI (broad search) to "' + ciName + '" for incident ' + current.number);
        } else {
            gs.warn('NPCI BR: CI "' + ciName + '" not found in CMDB for subcategory "' + subcategory + '"');
        }
    }

})(current, previous);
```

**Verification:**
1. Navigate to **Incident > Create New**
2. Set Category = "UPI", Subcategory = "Transaction"
3. Observe that Configuration Item is auto-populated with "UPI Transaction Service"
4. Change Subcategory to "Settlement" and save — CI should update to "UPI Settlement Service"

---

### Exercise 2.5: Create Business Rule — "Prevent P1 Close Without Root Cause"

This rule enforces data quality by blocking closure of P1 incidents without required information.

**Navigation:** System Definition > Business Rules > New

| Field | Value |
|---|---|
| Name | NPCI - Prevent P1 Close Without Root Cause |
| Table | Incident [incident] |
| Active | true |
| Advanced | true |
| When to run | before |
| Update | true |
| Filter Conditions | Priority is 1 - Critical AND State changes to Closed |
| Order | 200 |

**Script tab:**

```javascript
(function executeRule(current, previous /*null when insert*/) {

    // Only run when state is changing to Closed (7)
    if (!current.state.changesTo(7)) {
        return;
    }

    // Only enforce for P1 (Critical) incidents
    if (current.priority != 1) {
        return;
    }

    var errors = [];

    // Check for close notes
    if (current.close_notes.nil()) {
        errors.push('Close Notes are required for P1 incidents');
    }

    // Check for close code
    if (current.close_code.nil()) {
        errors.push('Close Code (Resolution Code) is required for P1 incidents');
    }

    // Check that a cause CI is identified
    if (current.cmdb_ci.nil()) {
        errors.push('Configuration Item must be set before closing a P1 incident');
    }

    // Check for root cause in work notes (look for substantial close notes)
    if (!current.close_notes.nil() && current.close_notes.toString().length < 50) {
        errors.push('Close Notes must contain at least 50 characters describing the root cause');
    }

    // If any validation errors, abort the update
    if (errors.length > 0) {
        var message = 'Cannot close P1 incident. Please address the following:\n';
        for (var i = 0; i < errors.length; i++) {
            message += '- ' + errors[i] + '\n';
        }
        gs.addErrorMessage(message);
        current.setAbortAction(true);
        gs.info('NPCI BR: Blocked closure of P1 incident ' + current.number + ' — missing required fields');
    }

})(current, previous);
```

**Verification:**
1. Open a P1 incident
2. Try to change State to "Closed" without filling Close Notes — you should see an error
3. Fill in Close Notes (fewer than 50 characters) — you should still see an error
4. Fill in Close Notes (50+ characters), Close Code, and Configuration Item
5. Now changing State to "Closed" should succeed

---

### Exercise 2.6: Create Business Rule — "Notify VIP Callers"

When a VIP caller raises an incident, automatically notify management and add a work note.

**Navigation:** System Definition > Business Rules > New

| Field | Value |
|---|---|
| Name | NPCI - Notify VIP Callers |
| Table | Incident [incident] |
| Active | true |
| Advanced | true |
| When to run | after |
| Insert | true |
| Order | 100 |

**Script tab:**

```javascript
(function executeRule(current, previous /*null when insert*/) {

    // Check if the caller is a VIP user
    if (!current.caller_id.vip.toString() == 'true') {
        return;
    }

    var callerName = current.caller_id.getDisplayValue();
    var incNumber = current.number.toString();
    var shortDesc = current.short_description.toString();
    var priority = current.priority.getDisplayValue();

    // Add a prominent work note
    var workNote = '*** VIP CALLER ALERT ***\n';
    workNote += 'Caller: ' + callerName + '\n';
    workNote += 'Priority: ' + priority + '\n';
    workNote += 'Description: ' + shortDesc + '\n';
    workNote += 'This incident has been flagged for expedited handling.\n';
    workNote += 'Management has been notified automatically.';

    current.work_notes = workNote;
    current.update();

    // Send email notification to VP Engineering (Sanjay Patel)
    var managerEmail = '';
    var grManager = new GlideRecord('sys_user');
    grManager.addQuery('name', 'Sanjay Patel');
    grManager.setLimit(1);
    grManager.query();

    if (grManager.next()) {
        managerEmail = grManager.email.toString();
    }

    if (managerEmail) {
        // Use gs.eventQueue to trigger a notification event
        gs.eventQueue('npci.vip.incident.created', current, callerName, managerEmail);
        gs.info('NPCI BR: VIP incident notification sent for ' + incNumber + ' — caller: ' + callerName);
    }

    // Also escalate priority if not already Critical
    if (current.priority > 2) {
        var grUpdate = new GlideRecord('incident');
        if (grUpdate.get(current.sys_id)) {
            grUpdate.urgency = 1;
            grUpdate.update();
            gs.info('NPCI BR: Escalated urgency to High for VIP caller incident ' + incNumber);
        }
    }

})(current, previous);
```

> **Note:** For the `gs.eventQueue` call to trigger an email, you would need to create a corresponding Event Registration and Notification. This is covered in Lab 13 (SLAs & Notifications). For now, the work note and log entry will confirm the rule is firing.

**Verification:**
1. Navigate to **User Administration > Users**
2. Find or create a user and check the **VIP** checkbox on their record
3. Create a new incident with that user as the Caller
4. After submission, open the incident and check Work Notes — you should see the VIP alert
5. Check **System Logs > System Log > All** and filter for "NPCI BR" to see the log entry

---

### Exercise 2.7: Create Business Rule — "Calculate Business Duration"

When an incident is resolved, calculate the business hours elapsed.

**Navigation:** System Definition > Business Rules > New

| Field | Value |
|---|---|
| Name | NPCI - Calculate Business Duration |
| Table | Incident [incident] |
| Active | true |
| Advanced | true |
| When to run | after |
| Update | true |
| Filter Conditions | State changes to Resolved |
| Order | 300 |

**Script tab:**

```javascript
(function executeRule(current, previous /*null when insert*/) {

    // Only run when state changes to Resolved (6)
    if (!current.state.changesTo(6)) {
        return;
    }

    var openedAt = current.opened_at.getGlideObject();
    var resolvedAt = current.resolved_at.getGlideObject();

    if (!openedAt || !resolvedAt) {
        gs.warn('NPCI BR: Cannot calculate duration — opened_at or resolved_at is empty for ' + current.number);
        return;
    }

    // Calculate total elapsed time in milliseconds
    var openedMs = openedAt.getNumericValue();
    var resolvedMs = resolvedAt.getNumericValue();
    var totalMs = resolvedMs - openedMs;

    // Convert to human-readable format
    var totalMinutes = Math.floor(totalMs / 60000);
    var hours = Math.floor(totalMinutes / 60);
    var minutes = totalMinutes % 60;
    var days = Math.floor(hours / 24);
    hours = hours % 24;

    var durationText = '';
    if (days > 0) {
        durationText += days + ' day(s) ';
    }
    durationText += hours + ' hour(s) ' + minutes + ' minute(s)';

    // Calculate using the business calendar (schedule)
    var schedule = new GlideSchedule();
    // Load the default 8-5 schedule; adjust sys_id if you have a custom NPCI schedule
    // To find your schedule sys_id: System Scheduler > Schedules
    // For now, use the default schedule
    var businessDuration = schedule.duration(
        new GlideDateTime(current.opened_at.toString()),
        new GlideDateTime(current.resolved_at.toString())
    );

    var businessMs = businessDuration.getNumericValue();
    var businessMinutes = Math.floor(businessMs / 60000);
    var businessHours = Math.floor(businessMinutes / 60);
    var businessMins = businessMinutes % 60;

    // Add a work note with the calculation
    var workNote = '--- Resolution Duration Summary ---\n';
    workNote += 'Total Elapsed Time: ' + durationText + '\n';
    workNote += 'Business Hours: ' + businessHours + ' hour(s) ' + businessMins + ' minute(s)\n';
    workNote += 'Opened: ' + current.opened_at.getDisplayValue() + '\n';
    workNote += 'Resolved: ' + current.resolved_at.getDisplayValue();

    var grUpdate = new GlideRecord('incident');
    if (grUpdate.get(current.sys_id)) {
        grUpdate.work_notes = workNote;
        grUpdate.update();
    }

    gs.info('NPCI BR: Calculated resolution duration for ' + current.number +
            ' — Total: ' + durationText + ', Business: ' + businessHours + 'h ' + businessMins + 'm');

})(current, previous);
```

**Verification:**
1. Open an existing incident (note the Opened timestamp)
2. Change the state to "Resolved" and fill in Resolution Code and Resolution Notes
3. Save the record
4. Check Work Notes for the "Resolution Duration Summary"

---

### Exercise 2.8: Create Business Rule — "Auto-create Problem for Recurring Incidents"

This Async rule detects patterns of recurring incidents on the same CI and automatically creates a Problem record.

**Navigation:** System Definition > Business Rules > New

| Field | Value |
|---|---|
| Name | NPCI - Auto-create Problem for Recurring Incidents |
| Table | Incident [incident] |
| Active | true |
| Advanced | true |
| When to run | async |
| Update | true |
| Filter Conditions | State is Resolved |
| Order | 500 |

**Script tab:**

```javascript
(function executeRule(current, previous /*null when insert*/) {

    // Only proceed if a CI is linked
    if (current.cmdb_ci.nil()) {
        return;
    }

    var ciSysId = current.cmdb_ci.toString();
    var ciName = current.cmdb_ci.getDisplayValue();
    var thresholdCount = 3;   // Minimum incidents to trigger
    var lookbackDays = 30;    // Look back period in days

    // Calculate the date 30 days ago
    var lookbackDate = new GlideDateTime();
    lookbackDate.addDaysUTC(-lookbackDays);

    // Count resolved/closed incidents on this CI in the last 30 days
    var ga = new GlideAggregate('incident');
    ga.addQuery('cmdb_ci', ciSysId);
    ga.addQuery('state', 'IN', '6,7');  // Resolved (6) or Closed (7)
    ga.addQuery('opened_at', '>=', lookbackDate);
    ga.addAggregate('COUNT');
    ga.query();

    var incidentCount = 0;
    if (ga.next()) {
        incidentCount = parseInt(ga.getAggregate('COUNT'), 10);
    }

    if (incidentCount < thresholdCount) {
        gs.info('NPCI BR: CI "' + ciName + '" has ' + incidentCount +
                ' incidents in last ' + lookbackDays + ' days (threshold: ' + thresholdCount + '). No problem created.');
        return;
    }

    // Check if a Problem already exists for this CI (avoid duplicates)
    var existingProblem = new GlideRecord('problem');
    existingProblem.addQuery('cmdb_ci', ciSysId);
    existingProblem.addQuery('state', 'NOT IN', '4,7');  // Not Closed (7) or Resolved with workaround
    existingProblem.addQuery('short_description', 'CONTAINS', 'Recurring');
    existingProblem.setLimit(1);
    existingProblem.query();

    if (existingProblem.next()) {
        // Problem already exists — add a note instead
        existingProblem.work_notes = 'Additional recurring incident detected: ' +
            current.number + ' (' + current.short_description + ')\n' +
            'Total incidents on this CI in last ' + lookbackDays + ' days: ' + incidentCount;
        existingProblem.update();

        gs.info('NPCI BR: Updated existing problem ' + existingProblem.number +
                ' with new recurring incident ' + current.number);
        return;
    }

    // Gather details about the recurring incidents for the problem description
    var incidentList = [];
    var grInc = new GlideRecord('incident');
    grInc.addQuery('cmdb_ci', ciSysId);
    grInc.addQuery('state', 'IN', '6,7');
    grInc.addQuery('opened_at', '>=', lookbackDate);
    grInc.orderByDesc('opened_at');
    grInc.setLimit(10);
    grInc.query();

    while (grInc.next()) {
        incidentList.push(grInc.number + ' - ' + grInc.short_description +
                         ' (Opened: ' + grInc.opened_at.getDisplayValue() + ')');
    }

    // Create the Problem record
    var problem = new GlideRecord('problem');
    problem.initialize();
    problem.short_description = 'Recurring incidents on CI: ' + ciName;

    var description = 'This problem was auto-created because CI "' + ciName + '" has had ' +
        incidentCount + ' incidents in the last ' + lookbackDays + ' days.\n\n';
    description += 'Affected CI: ' + ciName + '\n';
    description += 'Incident Count: ' + incidentCount + '\n';
    description += 'Analysis Period: Last ' + lookbackDays + ' days\n\n';
    description += 'Related Incidents:\n';
    for (var i = 0; i < incidentList.length; i++) {
        description += '  ' + (i + 1) + '. ' + incidentList[i] + '\n';
    }
    description += '\nPlease investigate the root cause of these recurring incidents.';

    problem.description = description;
    problem.cmdb_ci = ciSysId;
    problem.category = current.category.toString();
    problem.impact = current.impact;
    problem.urgency = current.urgency;

    // Assign to the CI's support group if available
    if (!current.cmdb_ci.support_group.nil()) {
        problem.assignment_group = current.cmdb_ci.support_group;
    } else {
        problem.assignment_group = current.assignment_group;
    }

    var problemSysId = problem.insert();

    if (problemSysId) {
        gs.info('NPCI BR: Auto-created Problem ' + problem.number +
                ' for recurring incidents on CI "' + ciName + '" (' + incidentCount + ' incidents)');

        // Link the current incident to the new problem
        var grUpdate = new GlideRecord('incident');
        if (grUpdate.get(current.sys_id)) {
            grUpdate.problem_id = problemSysId;
            grUpdate.work_notes = 'Auto-linked to Problem ' + problem.number +
                ' — recurring incident pattern detected on CI "' + ciName + '"';
            grUpdate.update();
        }
    }

})(current, previous);
```

**Verification:**
1. Ensure you have a CI (e.g., "UPI Transaction Service") with at least 2 resolved incidents
2. Create and resolve a third incident on the same CI
3. Wait a moment (async rules run in background)
4. Navigate to **Problem > All** and look for a problem titled "Recurring incidents on CI: UPI Transaction Service"
5. Open the problem and verify the description lists all related incidents

---

## Part 3: Client Scripts — Deep Dive

### 3.1 Client Script Types

| Type | Trigger | Use Case |
|---|---|---|
| **onLoad** | Form loads | Set defaults, show messages, initialize state |
| **onChange** | Field value changes | React to user input, cascade field updates |
| **onSubmit** | Form is submitted | Validate before save, confirm dialogs |
| **onCellEdit** | List cell is edited | Validate inline list edits |

### 3.2 Core Client APIs

**g_form — Form Manipulation:**
```javascript
// Get and set values
g_form.getValue('priority');                    // Returns internal value ('1')
g_form.getDisplayValue('priority');              // Returns display value ('1 - Critical')
g_form.setValue('priority', '1');                // Sets value
g_form.clearValue('assignment_group');            // Clears field

// Field properties
g_form.setMandatory('description', true);        // Make mandatory
g_form.setVisible('close_notes', true);          // Show/hide field
g_form.setReadOnly('opened_at', true);           // Make read-only
g_form.setLabel('cmdb_ci', 'Affected System');   // Change label
g_form.setDisplay('close_code', false);          // Hide (removes from DOM)

// Messages
g_form.addInfoMessage('This is an informational message');
g_form.addErrorMessage('This is an error message');
g_form.showFieldMsg('priority', 'P1 requires all fields', 'error');
g_form.hideFieldMsg('priority');
g_form.clearMessages();

// Options for choice fields
g_form.addOption('subcategory', 'transaction', 'Transaction');
g_form.removeOption('subcategory', 'transaction');
g_form.clearOptions('subcategory');

// Sections
g_form.setSectionDisplay('resolution_information', true);

// Reference fields
g_form.getReference('caller_id', function(ref) {
    // ref is the full GlideRecord from the server
    alert('Caller email: ' + ref.email);
});
```

**g_user — Current User:**
```javascript
g_user.userName;           // 'admin'
g_user.userID;             // sys_id of the current user
g_user.firstName;          // 'System'
g_user.lastName;           // 'Administrator'
g_user.hasRole('itil');    // true/false
g_user.hasRoleExactly('admin');  // true/false (no inherited roles)
```

### 3.3 GlideAjax — Client-to-Server Calls

GlideAjax lets Client Scripts call server-side Script Includes:

```javascript
// Client-side call
var ga = new GlideAjax('UPIAjaxUtils');        // Script Include name
ga.addParam('sysparm_name', 'getCallerInfo');   // Method name
ga.addParam('sysparm_user_id', userId);         // Custom parameter
ga.getXMLAnswer(function(answer) {
    // answer is a string — parse JSON if needed
    var data = JSON.parse(answer);
    g_form.setValue('contact_phone', data.phone);
});
```

---

### Exercise 3.4: Create Client Script — "Mandatory Fields on P1"

When an agent sets Priority to Critical, enforce that all essential fields are filled.

**Navigation:** System Definition > Client Scripts > New

| Field | Value |
|---|---|
| Name | NPCI - Mandatory Fields on P1 |
| Table | Incident [incident] |
| Type | onChange |
| Field name | Priority |
| Active | true |

**Script:**

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading || newValue === '') {
        return;
    }

    // Priority 1 = Critical
    if (newValue == '1') {
        // Make critical fields mandatory
        g_form.setMandatory('assignment_group', true);
        g_form.setMandatory('cmdb_ci', true);
        g_form.setMandatory('description', true);
        g_form.setMandatory('contact_type', true);

        // Visual indicators
        g_form.showFieldMsg('assignment_group', 'Required for P1 Critical incidents', 'info');
        g_form.showFieldMsg('cmdb_ci', 'Required for P1 Critical incidents', 'info');
        g_form.showFieldMsg('description', 'Required for P1 Critical incidents', 'info');

        // Info banner
        g_form.addInfoMessage('P1 CRITICAL INCIDENT: Assignment Group, Configuration Item, Description, and Contact Type are all required. Please ensure all fields are completed before submitting.');

        // Highlight the form (add visual urgency)
        g_form.setLabel('priority', 'Priority *** CRITICAL ***');

    } else {
        // Revert mandatory settings for non-P1
        g_form.setMandatory('assignment_group', false);
        g_form.setMandatory('cmdb_ci', false);
        g_form.setMandatory('description', false);
        g_form.setMandatory('contact_type', false);

        // Clear messages
        g_form.hideFieldMsg('assignment_group');
        g_form.hideFieldMsg('cmdb_ci');
        g_form.hideFieldMsg('description');
        g_form.clearMessages();

        // Reset label
        g_form.setLabel('priority', 'Priority');
    }
}
```

**Verification:**
1. Open any incident form
2. Change Priority to "1 - Critical"
3. Observe: Assignment Group, CI, and Description become mandatory (red asterisk)
4. Info messages appear on those fields and a banner appears at the top
5. Change Priority to "3 - Moderate" — mandatory indicators disappear

---

### Exercise 3.5: Create Client Script — "Auto-populate Contact Info"

When the agent selects a Caller, automatically fetch and display their contact information using GlideAjax.

> **Prerequisite:** This script requires the `UPIAjaxUtils` Script Include from Part 5. Create that first, or use `g_form.getReference()` as a simpler alternative shown in the comments.

**Navigation:** System Definition > Client Scripts > New

| Field | Value |
|---|---|
| Name | NPCI - Auto-populate Contact Info |
| Table | Incident [incident] |
| Type | onChange |
| Field name | Caller |
| Active | true |

**Script:**

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading || newValue === '') {
        return;
    }

    // Clear previous contact info messages
    g_form.hideFieldMsg('caller_id');

    // Option A: Using GlideAjax (preferred — non-blocking, efficient)
    var ga = new GlideAjax('UPIAjaxUtils');
    ga.addParam('sysparm_name', 'getCallerInfo');
    ga.addParam('sysparm_user_id', newValue);
    ga.getXMLAnswer(function(answer) {
        if (!answer) {
            return;
        }

        var callerInfo;
        try {
            callerInfo = JSON.parse(answer);
        } catch (e) {
            console.log('NPCI CS: Failed to parse caller info response');
            return;
        }

        // Display caller information as a field message
        var infoMsg = 'Phone: ' + (callerInfo.phone || 'N/A') +
                      ' | Email: ' + (callerInfo.email || 'N/A') +
                      ' | Location: ' + (callerInfo.location || 'N/A');

        g_form.showFieldMsg('caller_id', infoMsg, 'info');

        // If the caller is VIP, show a prominent warning
        if (callerInfo.vip === 'true') {
            g_form.showFieldMsg('caller_id',
                'VIP CALLER — This incident will receive expedited handling', 'error');

            // Auto-escalate urgency for VIP callers
            var currentUrgency = g_form.getValue('urgency');
            if (currentUrgency > 1) {
                g_form.setValue('urgency', '1');
                g_form.addInfoMessage('Urgency automatically set to High for VIP caller');
            }
        }

        // Auto-set location if available and not already set
        if (callerInfo.location_id && !g_form.getValue('location')) {
            g_form.setValue('location', callerInfo.location_id);
        }
    });

    // Option B: Using getReference (simpler but synchronous in older versions)
    // Uncomment the block below if you haven't created UPIAjaxUtils yet
    /*
    g_form.getReference('caller_id', function(ref) {
        if (!ref) return;

        var infoMsg = 'Phone: ' + (ref.phone || 'N/A') +
                      ' | Email: ' + (ref.email || 'N/A');
        g_form.showFieldMsg('caller_id', infoMsg, 'info');

        if (ref.vip == 'true') {
            g_form.showFieldMsg('caller_id',
                'VIP CALLER — This incident will receive expedited handling', 'error');
        }
    });
    */
}
```

**Verification:**
1. Open a new or existing incident
2. Select a caller from the Caller field
3. Observe the info message under the Caller field showing phone, email, and location
4. Select a VIP caller — observe the VIP warning message and urgency escalation

---

### Exercise 3.6: Create Client Script — "Confirm Before Major State Change"

Prevent accidental resolution or closure by requiring explicit confirmation.

**Navigation:** System Definition > Client Scripts > New

| Field | Value |
|---|---|
| Name | NPCI - Confirm Before Major State Change |
| Table | Incident [incident] |
| Type | onSubmit |
| Active | true |

**Script:**

```javascript
function onSubmit() {

    var state = g_form.getValue('state');
    var originalState = g_form.getOriginalValue('state');

    // Only prompt if state is actually changing
    if (state === originalState) {
        return true;
    }

    // State 6 = Resolved, State 7 = Closed
    if (state == '6' || state == '7') {
        var stateLabel = (state == '6') ? 'Resolved' : 'Closed';
        var incNumber = g_form.getValue('number');
        var priority = g_form.getDisplayValue('priority');

        var message = 'You are about to set incident ' + incNumber + ' to ' + stateLabel + '.\n\n';

        // Additional warnings for P1 incidents
        if (g_form.getValue('priority') == '1') {
            message += 'WARNING: This is a P1 Critical incident.\n';
            message += 'Ensure the following before proceeding:\n';
            message += '  - Root cause has been identified\n';
            message += '  - All affected users have been notified\n';
            message += '  - Close notes contain detailed resolution steps\n';
            message += '  - Major Incident Review has been scheduled\n\n';
        }

        // Check if resolution fields are filled
        if (state == '6') {
            var closeCode = g_form.getValue('close_code');
            var closeNotes = g_form.getValue('close_notes');

            if (!closeCode) {
                g_form.addErrorMessage('Resolution Code is required before resolving the incident.');
                g_form.setMandatory('close_code', true);
                return false;
            }

            if (!closeNotes) {
                g_form.addErrorMessage('Resolution Notes are required before resolving the incident.');
                g_form.setMandatory('close_notes', true);
                return false;
            }
        }

        message += 'Are you sure you want to proceed?';

        // Show confirmation dialog
        var confirmed = confirm(message);

        if (!confirmed) {
            // User cancelled — revert state to original
            g_form.setValue('state', originalState);
            g_form.addInfoMessage('State change cancelled. The incident remains in its current state.');
            return false;
        }
    }

    return true;
}
```

**Verification:**
1. Open an incident in "In Progress" state
2. Change State to "Resolved" without filling Resolution Code — error message appears
3. Fill Resolution Code and Resolution Notes, then change State to "Resolved"
4. A confirmation dialog appears — click "Cancel" and verify state reverts
5. Repeat and click "OK" — the incident should save as Resolved

---

### Exercise 3.7: Create Client Script — "Dynamic Category Subcategory"

When an agent selects the "UPI" category, dynamically populate subcategory choices specific to UPI operations.

**Navigation:** System Definition > Client Scripts > New

| Field | Value |
|---|---|
| Name | NPCI - Dynamic Category Subcategory |
| Table | Incident [incident] |
| Type | onChange |
| Field name | Category |
| Active | true |

**Script:**

```javascript
function onChange(control, oldValue, newValue, isLoading, isTemplate) {
    if (isLoading || newValue === '') {
        return;
    }

    // Define UPI-specific subcategories
    var upiSubcategories = [
        { value: 'transaction',  label: 'Transaction Failure' },
        { value: 'settlement',   label: 'Settlement Processing' },
        { value: 'dispute',      label: 'Dispute / Chargeback' },
        { value: 'merchant',     label: 'Merchant Onboarding' },
        { value: 'monitoring',   label: 'Monitoring / Alerting' },
        { value: 'performance',  label: 'Performance Degradation' },
        { value: 'security',     label: 'Security / Fraud' },
        { value: 'integration',  label: 'Bank Integration' },
        { value: 'compliance',   label: 'Regulatory Compliance' }
    ];

    if (newValue == 'upi') {
        // Clear existing subcategory options
        g_form.clearOptions('subcategory');

        // Add a blank default option
        g_form.addOption('subcategory', '', '-- Select UPI Subcategory --');

        // Add UPI-specific subcategories
        for (var i = 0; i < upiSubcategories.length; i++) {
            g_form.addOption('subcategory',
                upiSubcategories[i].value,
                upiSubcategories[i].label);
        }

        // Show informational message
        g_form.showFieldMsg('subcategory',
            'Select the specific UPI service area affected', 'info');

        // Make subcategory mandatory for UPI incidents
        g_form.setMandatory('subcategory', true);

    } else {
        // For non-UPI categories, restore default subcategory behavior
        // Clear custom options (ServiceNow will repopulate from dictionary)
        g_form.clearOptions('subcategory');
        g_form.hideFieldMsg('subcategory');
        g_form.setMandatory('subcategory', false);

        // Clear subcategory value
        g_form.setValue('subcategory', '');
    }
}
```

**Verification:**
1. Open a new incident form
2. Set Category to "UPI"
3. Click the Subcategory dropdown — you should see the UPI-specific options
4. Select "Transaction Failure" — note the subcategory value
5. Change Category to "Software" — subcategory should clear and show default options

---

## Part 4: UI Policies — Deep Dive

### 4.1 UI Policy vs Client Script

| Aspect | UI Policy | Client Script |
|---|---|---|
| **Code required** | No (mostly configuration) | Yes (JavaScript) |
| **Capabilities** | Mandatory, Visible, Read-only | Everything (setValue, messages, AJAX) |
| **Maintenance** | Easy for non-developers | Requires scripting knowledge |
| **Performance** | Optimized by platform | Can impact if poorly written |
| **Reverse if false** | Built-in toggle | Must code both directions |
| **Best for** | Show/hide/mandatory/read-only | Complex logic, calculations, API calls |

**Rule of thumb:** If you only need to change field visibility, mandatory, or read-only status based on a condition, use a UI Policy. For everything else, use a Client Script.

### 4.2 UI Policy Execution

- UI Policies run **after** Client Scripts
- Multiple UI Policies can apply simultaneously
- **Order** field controls execution priority (lower = first)
- **Reverse if false** automatically undoes actions when condition is no longer met
- **On load** controls whether the policy runs when the form first loads

---

### Exercise 4.3: Create UI Policy — "Show Resolution Fields When Resolved"

**Navigation:** System UI > UI Policies > New

**UI Policy Record:**

| Field | Value |
|---|---|
| Name | NPCI - Show Resolution Fields When Resolved |
| Table | Incident [incident] |
| Active | true |
| Short description | Show resolution fields when incident state is Resolved |
| On load | true |
| Reverse if false | true |
| Order | 100 |

**Conditions:**

| Field | Operator | Value |
|---|---|---|
| State | is | Resolved |

Click **Save** (not Submit) to stay on the record, then scroll down to **UI Policy Actions**.

**UI Policy Actions (click New for each):**

| # | Field Name | Mandatory | Visible | Read Only |
|---|---|---|---|---|
| 1 | Close code | true | true | -- |
| 2 | Close notes | true | true | -- |
| 3 | Resolved by | -- | true | true |
| 4 | Resolution category | -- | true | -- |

> **How "Reverse if false" works:** When the State is NOT Resolved, these fields will automatically be hidden and non-mandatory. You do not need to create separate "hide" logic.

**Verification:**
1. Open an incident in "New" or "In Progress" state
2. Confirm that Close Code, Close Notes, and Resolved By are NOT visible
3. Change State to "Resolved"
4. Observe: Close Code and Close Notes appear and are marked mandatory (red asterisk)
5. Resolved By appears as read-only
6. Change State back to "In Progress" — fields disappear again

---

### Exercise 4.4: Create UI Policy — "Lock Fields After Closure"

Once an incident is closed, prevent any further modifications.

**Navigation:** System UI > UI Policies > New

**UI Policy Record:**

| Field | Value |
|---|---|
| Name | NPCI - Lock Fields After Closure |
| Table | Incident [incident] |
| Active | true |
| Short description | Make all fields read-only when incident is Closed |
| On load | true |
| Reverse if false | true |
| Order | 200 |

**Conditions:**

| Field | Operator | Value |
|---|---|---|
| State | is | Closed |

**UI Policy Actions:**

| # | Field Name | Mandatory | Visible | Read Only |
|---|---|---|---|---|
| 1 | Short description | -- | -- | true |
| 2 | Description | -- | -- | true |
| 3 | Priority | -- | -- | true |
| 4 | Impact | -- | -- | true |
| 5 | Urgency | -- | -- | true |
| 6 | Assignment group | -- | -- | true |
| 7 | Assigned to | -- | -- | true |
| 8 | Category | -- | -- | true |
| 9 | Subcategory | -- | -- | true |
| 10 | Configuration item | -- | -- | true |
| 11 | Contact type | -- | -- | true |
| 12 | State | -- | -- | true |
| 13 | Close code | -- | -- | true |
| 14 | Close notes | -- | -- | true |

> **Note:** You can also achieve this with an ACL (Access Control Rule) or a "read-only" form view. The UI Policy approach is simpler for lab purposes but ACLs are more secure for production.

**Verification:**
1. Open a Closed incident
2. Verify that all major fields are read-only (grayed out, not editable)
3. Reopen the incident (if you have a reopen process) — fields become editable again

---

### Exercise 4.5: Create UI Policy — "Major Incident Fields"

When Priority is set to Critical (P1), show fields specific to Major Incident management.

**Navigation:** System UI > UI Policies > New

**UI Policy Record:**

| Field | Value |
|---|---|
| Name | NPCI - Major Incident Fields |
| Table | Incident [incident] |
| Active | true |
| Short description | Show major incident fields for P1 Critical |
| On load | true |
| Reverse if false | true |
| Order | 150 |

**Conditions:**

| Field | Operator | Value |
|---|---|---|
| Priority | is | 1 - Critical |

**UI Policy Actions:**

| # | Field Name | Mandatory | Visible | Read Only |
|---|---|---|---|---|
| 1 | Major incident state | true | true | -- |
| 2 | Business impact | true | true | -- |
| 3 | Escalation | -- | true | -- |

> **Note:** `Major incident state` and `Business impact` may not exist as fields on your PDI. If not, you can add them via **Table Designer** or use alternative fields like `business_stc` (Business Duration) and a custom "Impact Statement" field.

**Verification:**
1. Open an incident with Priority = "3 - Moderate"
2. Confirm that Major Incident State and Business Impact are not visible
3. Change Priority to "1 - Critical"
4. Major Incident State and Business Impact appear and are mandatory
5. Change Priority back to "3 - Moderate" — fields disappear

---

### Exercise 4.6: Create UI Policy — "UPI-Specific Fields"

When Category = "UPI", show custom fields for UPI-specific information.

> **Prerequisite:** This policy uses custom fields. You will need to add them to the Incident table first.

**Step 1: Add Custom Fields to Incident Table**

Navigate to **System Definition > Tables**, find `incident`, and add these columns:

| Column Label | Column Name | Type | Max Length |
|---|---|---|---|
| UPI Transaction ID | u_upi_transaction_id | String | 40 |
| UPI Error Code | u_upi_error_code | String | 20 |
| Affected Bank | u_affected_bank | String | 100 |
| Transaction Amount | u_transaction_amount | Decimal | -- |
| Merchant ID | u_merchant_id | String | 40 |

**Step 2: Create the UI Policy**

**Navigation:** System UI > UI Policies > New

**UI Policy Record:**

| Field | Value |
|---|---|
| Name | NPCI - UPI-Specific Fields |
| Table | Incident [incident] |
| Active | true |
| Short description | Show UPI-specific fields when category is UPI |
| On load | true |
| Reverse if false | true |
| Order | 100 |

**Conditions:**

| Field | Operator | Value |
|---|---|---|
| Category | is | upi |

**UI Policy Actions:**

| # | Field Name | Mandatory | Visible | Read Only |
|---|---|---|---|---|
| 1 | UPI Transaction ID | -- | true | -- |
| 2 | UPI Error Code | -- | true | -- |
| 3 | Affected Bank | true | true | -- |
| 4 | Transaction Amount | -- | true | -- |
| 5 | Merchant ID | -- | true | -- |

**Verification:**
1. Open a new incident, set Category = "Software" — UPI fields are hidden
2. Change Category to "UPI"
3. UPI Transaction ID, UPI Error Code, Affected Bank, Transaction Amount, and Merchant ID appear
4. Affected Bank is mandatory
5. Change Category back to "Software" — UPI fields disappear

---

## Part 5: Script Includes — Reusable Server Libraries

### 5.1 Script Include Types

| Type | Client-callable | Use Case |
|---|---|---|
| **Classless** | No | Simple utility functions |
| **Class-based** | No | Organized, reusable server-side libraries |
| **Client-callable** | Yes (extends AbstractAjaxProcessor) | GlideAjax target for Client Scripts |

### 5.2 Class-based Pattern

```javascript
var ClassName = Class.create();
ClassName.prototype = {
    initialize: function() {
        // Constructor — runs when instantiated
    },

    myMethod: function(param1, param2) {
        // Your logic here
        return result;
    },

    type: 'ClassName'  // Must match the class name
};
```

---

### Exercise 5.3: Create Script Include — "UPIUtils"

A reusable server-side utility library for UPI-related operations.

**Navigation:** System Definition > Script Includes > New

| Field | Value |
|---|---|
| Name | UPIUtils |
| API Name | global.UPIUtils |
| Client callable | false |
| Active | true |
| Description | Server-side utility class for NPCI UPI operations. Provides methods for recurring incident detection, MTTR calculation, and VIP caller identification. |

**Script:**

```javascript
var UPIUtils = Class.create();
UPIUtils.prototype = {
    initialize: function() {
        this.LOG_PREFIX = 'UPIUtils: ';
    },

    /**
     * Get the count and details of incidents related to a specific CI
     * within a given number of days.
     *
     * @param {string} ciSysId - sys_id of the Configuration Item
     * @param {number} days - Number of days to look back (default: 30)
     * @returns {object} { count: number, incidents: array }
     */
    getRelatedIncidents: function(ciSysId, days) {
        if (!ciSysId) {
            gs.warn(this.LOG_PREFIX + 'getRelatedIncidents called with empty ciSysId');
            return { count: 0, incidents: [] };
        }

        days = days || 30;
        var lookbackDate = new GlideDateTime();
        lookbackDate.addDaysUTC(-days);

        var incidents = [];
        var gr = new GlideRecord('incident');
        gr.addQuery('cmdb_ci', ciSysId);
        gr.addQuery('opened_at', '>=', lookbackDate);
        gr.orderByDesc('opened_at');
        gr.query();

        while (gr.next()) {
            incidents.push({
                sys_id: gr.sys_id.toString(),
                number: gr.number.toString(),
                short_description: gr.short_description.toString(),
                state: gr.state.getDisplayValue(),
                priority: gr.priority.getDisplayValue(),
                opened_at: gr.opened_at.getDisplayValue(),
                resolved_at: gr.resolved_at.getDisplayValue() || '',
                assigned_to: gr.assigned_to.getDisplayValue() || 'Unassigned'
            });
        }

        gs.info(this.LOG_PREFIX + 'Found ' + incidents.length +
                ' incidents for CI ' + ciSysId + ' in last ' + days + ' days');

        return {
            count: incidents.length,
            incidents: incidents
        };
    },

    /**
     * Calculate Mean Time To Resolve (MTTR) for a given CI.
     * Only considers incidents that have been resolved or closed.
     *
     * @param {string} ciSysId - sys_id of the Configuration Item
     * @param {number} days - Number of days to look back (default: 90)
     * @returns {object} { mttr_minutes: number, mttr_display: string, sample_size: number }
     */
    calculateMTTR: function(ciSysId, days) {
        if (!ciSysId) {
            return { mttr_minutes: 0, mttr_display: 'N/A', sample_size: 0 };
        }

        days = days || 90;
        var lookbackDate = new GlideDateTime();
        lookbackDate.addDaysUTC(-days);

        var totalMinutes = 0;
        var count = 0;

        var gr = new GlideRecord('incident');
        gr.addQuery('cmdb_ci', ciSysId);
        gr.addQuery('state', 'IN', '6,7');  // Resolved or Closed
        gr.addQuery('opened_at', '>=', lookbackDate);
        gr.addNotNullQuery('resolved_at');
        gr.query();

        while (gr.next()) {
            var opened = new GlideDateTime(gr.opened_at.toString());
            var resolved = new GlideDateTime(gr.resolved_at.toString());

            var diffMs = resolved.getNumericValue() - opened.getNumericValue();
            if (diffMs > 0) {
                totalMinutes += Math.floor(diffMs / 60000);
                count++;
            }
        }

        if (count === 0) {
            return { mttr_minutes: 0, mttr_display: 'No data', sample_size: 0 };
        }

        var avgMinutes = Math.round(totalMinutes / count);
        var hours = Math.floor(avgMinutes / 60);
        var mins = avgMinutes % 60;

        var display = '';
        if (hours > 0) {
            display = hours + 'h ' + mins + 'm';
        } else {
            display = mins + 'm';
        }

        gs.info(this.LOG_PREFIX + 'MTTR for CI ' + ciSysId + ': ' + display +
                ' (based on ' + count + ' incidents over ' + days + ' days)');

        return {
            mttr_minutes: avgMinutes,
            mttr_display: display,
            sample_size: count
        };
    },

    /**
     * Check if a user is a VIP caller.
     *
     * @param {string} userSysId - sys_id of the user
     * @returns {boolean} true if user is VIP
     */
    isVIPCaller: function(userSysId) {
        if (!userSysId) {
            return false;
        }

        var gr = new GlideRecord('sys_user');
        if (gr.get(userSysId)) {
            return gr.vip.toString() === 'true';
        }

        return false;
    },

    /**
     * Get the support group for a given CI.
     *
     * @param {string} ciSysId - sys_id of the Configuration Item
     * @returns {string} sys_id of the support group, or empty string
     */
    getCISupportGroup: function(ciSysId) {
        if (!ciSysId) {
            return '';
        }

        var gr = new GlideRecord('cmdb_ci');
        if (gr.get(ciSysId)) {
            return gr.support_group.toString() || '';
        }

        return '';
    },

    /**
     * Check if a CI has exceeded the incident threshold and should
     * trigger a Problem investigation.
     *
     * @param {string} ciSysId - sys_id of the CI
     * @param {number} threshold - Minimum number of incidents (default: 3)
     * @param {number} days - Look-back period in days (default: 30)
     * @returns {boolean} true if threshold is exceeded
     */
    isRecurringIssue: function(ciSysId, threshold, days) {
        threshold = threshold || 3;
        days = days || 30;

        var result = this.getRelatedIncidents(ciSysId, days);
        return result.count >= threshold;
    },

    type: 'UPIUtils'
};
```

**Usage in a Business Rule:**

```javascript
// In any Business Rule script:
var utils = new UPIUtils();

// Check for recurring issues
if (utils.isRecurringIssue(current.cmdb_ci, 3, 30)) {
    gs.info('Recurring issue detected on CI: ' + current.cmdb_ci.getDisplayValue());
}

// Calculate MTTR
var mttr = utils.calculateMTTR(current.cmdb_ci);
gs.info('MTTR: ' + mttr.mttr_display);
```

---

### Exercise 5.4: Create Script Include — "UPIAjaxUtils"

A client-callable Script Include that serves as the bridge for GlideAjax calls from Client Scripts.

**Navigation:** System Definition > Script Includes > New

| Field | Value |
|---|---|
| Name | UPIAjaxUtils |
| API Name | global.UPIAjaxUtils |
| Client callable | true (check this box) |
| Active | true |
| Description | Client-callable AJAX processor for NPCI UPI operations. Used by Client Scripts to fetch server-side data via GlideAjax. |

**Script:**

```javascript
var UPIAjaxUtils = Class.create();
UPIAjaxUtils.prototype = Object.extendsObject(AbstractAjaxProcessor, {

    /**
     * Get caller contact information.
     * Called from Client Script via GlideAjax.
     *
     * Client-side usage:
     *   var ga = new GlideAjax('UPIAjaxUtils');
     *   ga.addParam('sysparm_name', 'getCallerInfo');
     *   ga.addParam('sysparm_user_id', callerSysId);
     *   ga.getXMLAnswer(callback);
     *
     * @returns {string} JSON string with phone, email, location, vip status
     */
    getCallerInfo: function() {
        var userId = this.getParameter('sysparm_user_id');

        if (!userId) {
            return JSON.stringify({ error: 'No user ID provided' });
        }

        var gr = new GlideRecord('sys_user');
        if (!gr.get(userId)) {
            return JSON.stringify({ error: 'User not found' });
        }

        var result = {
            name: gr.name.toString(),
            phone: gr.phone.toString() || '',
            mobile_phone: gr.mobile_phone.toString() || '',
            email: gr.email.toString() || '',
            location: gr.location.getDisplayValue() || '',
            location_id: gr.location.toString() || '',
            department: gr.department.getDisplayValue() || '',
            title: gr.title.toString() || '',
            vip: gr.vip.toString(),
            manager: gr.manager.getDisplayValue() || '',
            company: gr.company.getDisplayValue() || ''
        };

        return JSON.stringify(result);
    },

    /**
     * Get CI details including status and related CIs.
     * Called from Client Script via GlideAjax.
     *
     * Client-side usage:
     *   var ga = new GlideAjax('UPIAjaxUtils');
     *   ga.addParam('sysparm_name', 'getCIDetails');
     *   ga.addParam('sysparm_ci_id', ciSysId);
     *   ga.getXMLAnswer(callback);
     *
     * @returns {string} JSON string with CI details
     */
    getCIDetails: function() {
        var ciId = this.getParameter('sysparm_ci_id');

        if (!ciId) {
            return JSON.stringify({ error: 'No CI ID provided' });
        }

        var gr = new GlideRecord('cmdb_ci');
        if (!gr.get(ciId)) {
            return JSON.stringify({ error: 'CI not found' });
        }

        var result = {
            name: gr.name.toString(),
            sys_class_name: gr.sys_class_name.toString(),
            operational_status: gr.operational_status.getDisplayValue(),
            support_group: gr.support_group.getDisplayValue() || '',
            support_group_id: gr.support_group.toString() || '',
            environment: gr.u_environment ? gr.u_environment.toString() : '',
            owned_by: gr.owned_by.getDisplayValue() || '',
            location: gr.location.getDisplayValue() || ''
        };

        // Get recent incident count using UPIUtils
        var utils = new UPIUtils();
        var related = utils.getRelatedIncidents(ciId, 30);
        result.recent_incident_count = related.count;

        // Calculate MTTR
        var mttr = utils.calculateMTTR(ciId, 90);
        result.mttr = mttr.mttr_display;

        // Get related CIs (upstream/downstream)
        result.relationships = [];
        var rel = new GlideRecord('cmdb_rel_ci');
        rel.addQuery('parent', ciId);
        rel.setLimit(10);
        rel.query();

        while (rel.next()) {
            result.relationships.push({
                type: rel.type.getDisplayValue(),
                child_name: rel.child.getDisplayValue(),
                child_id: rel.child.toString()
            });
        }

        return JSON.stringify(result);
    },

    /**
     * Get subcategory options for a given category.
     * Useful for dynamic choice population.
     *
     * @returns {string} JSON array of {value, label} objects
     */
    getSubcategories: function() {
        var category = this.getParameter('sysparm_category');

        if (category !== 'upi') {
            return JSON.stringify([]);
        }

        var subcategories = [
            { value: 'transaction',  label: 'Transaction Failure' },
            { value: 'settlement',   label: 'Settlement Processing' },
            { value: 'dispute',      label: 'Dispute / Chargeback' },
            { value: 'merchant',     label: 'Merchant Onboarding' },
            { value: 'monitoring',   label: 'Monitoring / Alerting' },
            { value: 'performance',  label: 'Performance Degradation' },
            { value: 'security',     label: 'Security / Fraud' },
            { value: 'integration',  label: 'Bank Integration' },
            { value: 'compliance',   label: 'Regulatory Compliance' }
        ];

        return JSON.stringify(subcategories);
    },

    /**
     * Security: Define which methods are accessible from the client.
     * Any method NOT listed here will be blocked.
     */
    isPublic: function() {
        return true;
    },

    type: 'UPIAjaxUtils'
});
```

**Testing the Script Include from Scripts — Background:**

Navigate to **System Definition > Scripts — Background** and run:

```javascript
// Test UPIUtils
var utils = new UPIUtils();

// Test isVIPCaller
var userGr = new GlideRecord('sys_user');
userGr.addQuery('vip', true);
userGr.setLimit(1);
userGr.query();
if (userGr.next()) {
    var isVip = utils.isVIPCaller(userGr.sys_id);
    gs.info('VIP check for ' + userGr.name + ': ' + isVip);
}

// Test MTTR calculation
var ciGr = new GlideRecord('cmdb_ci');
ciGr.addQuery('name', 'UPI Transaction Service');
ciGr.setLimit(1);
ciGr.query();
if (ciGr.next()) {
    var mttr = utils.calculateMTTR(ciGr.sys_id, 90);
    gs.info('MTTR for UPI Transaction Service: ' + mttr.mttr_display +
            ' (sample: ' + mttr.sample_size + ')');
}
```

---

## Part 6: UI Actions

### 6.1 UI Action Types

| Type | Location | Use Case |
|---|---|---|
| **Form button** | Top or bottom of form | Actions on the current record |
| **Form link** | Related links section | Navigation to related pages |
| **Form context menu** | Right-click on form | Quick actions |
| **List button** | Above list view | Bulk actions |
| **List context menu** | Right-click on list row | Row-specific actions |

---

### Exercise 6.2: Create UI Action — "Escalate to P1"

Add a button to the Incident form that escalates the incident to P1 Critical with a single click.

**Navigation:** System Definition > UI Actions > New

| Field | Value |
|---|---|
| Name | Escalate to P1 |
| Table | Incident [incident] |
| Action name | npci_escalate_p1 |
| Active | true |
| Show insert | false |
| Show update | true |
| Form button | true |
| Hint | Escalate this incident to Priority 1 - Critical |
| Order | 50 |
| Condition | `current.priority != 1` |

**Script:**

```javascript
// Server-side script for UI Action
if (typeof window == 'undefined') {
    // SERVER SIDE
    current.impact = 1;
    current.urgency = 1;
    // Priority will auto-calculate to 1 based on Impact x Urgency matrix

    current.work_notes = 'Incident escalated to P1 Critical by ' +
        gs.getUserDisplayName() + ' on ' + new GlideDateTime().getDisplayValue() +
        '.\nReason: Manual escalation via UI Action.';

    // Set the escalation level
    current.escalation = 1;

    // Notify the assignment group
    gs.eventQueue('incident.escalated', current, gs.getUserDisplayName(), '');

    current.update();
    gs.addInfoMessage('Incident ' + current.number + ' has been escalated to P1 Critical.');

    action.setRedirectURL(current);
}
```

**Client-side condition (optional, to add confirmation):**

Check the **Client** checkbox and add:

```javascript
// CLIENT SIDE — runs before server script
function npci_escalate_p1_client() {
    var confirmed = confirm(
        'You are about to escalate this incident to P1 Critical.\n\n' +
        'This will:\n' +
        '  - Set Impact and Urgency to High\n' +
        '  - Notify the assignment group\n' +
        '  - Flag this as a Major Incident\n\n' +
        'Are you sure?'
    );

    if (!confirmed) {
        return false;
    }

    // Prompt for escalation reason
    var reason = prompt('Please provide the reason for escalation:');
    if (!reason || reason.trim() === '') {
        alert('Escalation reason is required.');
        return false;
    }

    // Pass the reason to the server via a hidden field or g_form
    g_form.setValue('work_notes', 'Escalation reason: ' + reason);

    return true;
}
```

**Verification:**
1. Open a Priority 3 or Priority 2 incident
2. Observe the "Escalate to P1" button on the form header
3. Click the button — confirmation dialog appears
4. Enter a reason and confirm
5. The incident refreshes with Priority = 1 - Critical
6. Check Work Notes for the escalation entry
7. Open a P1 incident — the button should NOT appear (condition hides it)

---

### Exercise 6.3: Create UI Action — "Create Problem from Incident"

A link that creates a Problem record pre-populated with the incident's data.

**Navigation:** System Definition > UI Actions > New

| Field | Value |
|---|---|
| Name | Create Problem from Incident |
| Table | Incident [incident] |
| Action name | npci_create_problem |
| Active | true |
| Show insert | false |
| Show update | true |
| Form link | true |
| Hint | Create a Problem record linked to this incident |
| Order | 100 |
| Condition | `current.state != 7 && gs.hasRole('itil')` |

**Script:**

```javascript
if (typeof window == 'undefined') {
    // SERVER SIDE

    // Check if a problem is already linked
    if (!current.problem_id.nil()) {
        gs.addWarningMessage('This incident is already linked to Problem: ' +
            current.problem_id.getDisplayValue());
        action.setRedirectURL(current);
    } else {
        // Create a new Problem record
        var problem = new GlideRecord('problem');
        problem.initialize();
        problem.short_description = 'Problem from Incident: ' + current.short_description;
        problem.description = 'This problem was created from Incident ' + current.number + '.\n\n' +
            'Original Description:\n' + current.description + '\n\n' +
            'Resolution Notes:\n' + (current.close_notes || 'N/A');
        problem.cmdb_ci = current.cmdb_ci;
        problem.category = current.category;
        problem.impact = current.impact;
        problem.urgency = current.urgency;
        problem.assignment_group = current.assignment_group;
        problem.assigned_to = current.assigned_to;

        var problemId = problem.insert();

        if (problemId) {
            // Link the problem back to the incident
            current.problem_id = problemId;
            current.work_notes = 'Problem ' + problem.number +
                ' created from this incident by ' + gs.getUserDisplayName();
            current.update();

            gs.addInfoMessage('Problem ' + problem.number + ' created successfully and linked to this incident.');

            // Redirect to the new Problem record
            action.setRedirectURL(problem);
        } else {
            gs.addErrorMessage('Failed to create Problem record.');
            action.setRedirectURL(current);
        }
    }
}
```

**Verification:**
1. Open an incident (not Closed)
2. Look in the Related Links section for "Create Problem from Incident"
3. Click the link
4. You are redirected to the new Problem record
5. Verify the Problem has the incident's Short Description, CI, Category, and Assignment Group
6. Go back to the incident — check that Problem field is populated and work note was added

---

### Exercise 6.4: Create UI Action — "View CI Dependency Map"

A link that navigates to the CMDB dependency map for the incident's CI.

**Navigation:** System Definition > UI Actions > New

| Field | Value |
|---|---|
| Name | View CI Dependency Map |
| Table | Incident [incident] |
| Action name | npci_view_ci_map |
| Active | true |
| Show insert | false |
| Show update | true |
| Form link | true |
| Hint | View the CMDB dependency map for this CI |
| Order | 200 |
| Condition | `!current.cmdb_ci.nil()` |
| Client | true |

**Script (Client-side):**

```javascript
function npci_view_ci_map() {
    var ciSysId = g_form.getValue('cmdb_ci');

    if (!ciSysId) {
        alert('No Configuration Item is linked to this incident.\nPlease set a CI first.');
        return false;
    }

    var ciName = g_form.getDisplayValue('cmdb_ci');

    // Open the CMDB dependency map in a new window
    var url = '/cmdb_dependency_map.do?sysparm_id=' + ciSysId;
    window.open(url, '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes');

    return false;  // Prevent form submission
}
```

**Verification:**
1. Open an incident that has a CI linked
2. In Related Links, click "View CI Dependency Map"
3. A new window opens showing the CMDB dependency/relationship map for that CI
4. Open an incident WITHOUT a CI — the link should not appear

---

## Part 7: Testing & Debugging

### 7.1 Server-Side Debugging

**System Logs:**

```javascript
// In Business Rules and Script Includes:
gs.info('Informational message');           // Logged as "Info"
gs.warn('Warning message');                 // Logged as "Warning"
gs.error('Error message');                  // Logged as "Error"
gs.debug('Debug message');                  // Only logged when debugging enabled
gs.log('Generic log message', 'MySource'); // Custom source label
```

**View logs:** Navigate to **System Logs > System Log > All**
- Filter by Source to find your messages
- Filter by "Created" to see recent entries

**Script Debugger:**
1. Navigate to **System Diagnostics > Script Debugger**
2. Set a breakpoint on your Business Rule
3. Trigger the Business Rule (e.g., save an incident)
4. Step through the code, inspect variables

### 7.2 Client-Side Debugging

**Browser Console:**

```javascript
// In Client Scripts:
console.log('Debug message');                    // Standard browser console
console.warn('Warning message');
console.error('Error message');
jslog('ServiceNow jslog message');               // ServiceNow-specific logging
```

**Enable JavaScript Debugging:**
1. In the browser, append `&sysparm_debug=true` to the URL
2. Or navigate to **System Diagnostics > Session Debug > Enable All**

**View Client Script Execution:**
1. Open browser Developer Tools (F12)
2. Go to the Console tab
3. Filter for your messages or "ServiceNow"

### 7.3 Common Errors and Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| "Cannot read property of null" | GlideRecord query returned no results | Check `gr.next()` before accessing fields |
| Business Rule not firing | Wrong conditions or table | Verify When/Insert/Update/Delete settings |
| Client Script not firing | Wrong Type (onChange vs onLoad) | Verify Type and Field name |
| GlideAjax returns empty | Script Include not client-callable | Check "Client callable" checkbox |
| "setAbortAction is not a function" | Used in After rule (not Before) | Move abort logic to Before rule |
| UI Policy not reversing | "Reverse if false" not checked | Enable the checkbox |
| Performance slow | Too many GlideRecord queries | Use GlideAggregate, addEncodedQuery, setLimit |

### 7.4 Debugging Checklist

When a script is not working as expected, follow this checklist:

1. **Check the logs:** System Logs > System Log > All (filter by recent)
2. **Verify the record:** Is the Business Rule on the correct table?
3. **Check conditions:** Are the filter conditions matching your test data?
4. **Check timing:** Before vs After vs Async — is the type correct?
5. **Check active:** Is the script/rule/policy set to Active?
6. **Test in isolation:** Use Scripts — Background to test your GlideRecord queries
7. **Check security:** Does the user have the required roles?
8. **Check scope:** Is the script in the correct application scope?
9. **Browser cache:** Clear cache and hard-reload (Ctrl+Shift+R) for client scripts
10. **Review execution order:** Is another Business Rule or UI Policy conflicting?

### 7.5 Testing Your Scripts

**Scripts — Background (Server-side testing):**

Navigate to **System Definition > Scripts — Background** and test your Script Includes:

```javascript
// Test UPIUtils.getRelatedIncidents
var utils = new UPIUtils();

var ciGr = new GlideRecord('cmdb_ci');
ciGr.addQuery('name', 'UPI Transaction Service');
ciGr.setLimit(1);
ciGr.query();

if (ciGr.next()) {
    var result = utils.getRelatedIncidents(ciGr.sys_id, 30);
    gs.info('Found ' + result.count + ' incidents');

    for (var i = 0; i < result.incidents.length; i++) {
        gs.info('  ' + result.incidents[i].number + ' - ' +
                result.incidents[i].short_description);
    }
}
```

**Test Business Rule conditions manually:**

```javascript
// Simulate the condition check for "Auto-create Problem for Recurring Incidents"
var gr = new GlideRecord('incident');
gr.addQuery('state', '6');  // Resolved
gr.addNotNullQuery('cmdb_ci');
gr.setLimit(5);
gr.query();

while (gr.next()) {
    var utils = new UPIUtils();
    var isRecurring = utils.isRecurringIssue(gr.cmdb_ci, 3, 30);
    gs.info(gr.number + ' - CI: ' + gr.cmdb_ci.getDisplayValue() +
            ' - Recurring: ' + isRecurring);
}
```

---

## Practice Exercises

### Exercise A: Auto-set Assignment Group from CI Support Group

**Task:** Write a Business Rule that automatically sets the Assignment Group to the CI's support group when a CI is selected.

**Requirements:**
- Table: Incident
- Type: Before Insert/Update
- Trigger: When cmdb_ci changes and is not empty
- Action: Look up the CI's support_group and set it as the incident's assignment_group

**Solution:**

```javascript
(function executeRule(current, previous /*null when insert*/) {

    // Only run if CI has changed and is not empty
    if (!current.cmdb_ci.changes() || current.cmdb_ci.nil()) {
        return;
    }

    // Look up the CI's support group
    var ciGr = new GlideRecord('cmdb_ci');
    if (ciGr.get(current.cmdb_ci)) {
        var supportGroup = ciGr.support_group.toString();

        if (supportGroup) {
            current.assignment_group = supportGroup;
            gs.info('NPCI Exercise A: Auto-set assignment group to ' +
                    ciGr.support_group.getDisplayValue() +
                    ' based on CI ' + ciGr.name);
        } else {
            gs.info('NPCI Exercise A: CI ' + ciGr.name + ' has no support group defined');
        }
    }

})(current, previous);
```

---

### Exercise B: Show Remaining SLA Time on Form

**Task:** Write a Client Script (onLoad) that displays the remaining SLA time as an info message on the incident form.

**Requirements:**
- Type: onLoad
- Action: Use GlideAjax to query the task_sla table for the active SLA
- Display remaining time as an info message

**Solution (Client Script):**

```javascript
function onLoad() {
    var incSysId = g_form.getUniqueValue();

    if (!incSysId) {
        return;
    }

    var ga = new GlideAjax('UPIAjaxUtils');
    ga.addParam('sysparm_name', 'getSLAInfo');
    ga.addParam('sysparm_task_id', incSysId);
    ga.getXMLAnswer(function(answer) {
        if (!answer) {
            return;
        }

        var slaInfo;
        try {
            slaInfo = JSON.parse(answer);
        } catch (e) {
            return;
        }

        if (slaInfo.has_active_sla) {
            var msg = 'Active SLA: ' + slaInfo.sla_name +
                      ' | Remaining: ' + slaInfo.time_remaining +
                      ' | Stage: ' + slaInfo.stage;

            if (slaInfo.has_breached) {
                g_form.addErrorMessage('SLA BREACHED: ' + slaInfo.sla_name +
                    ' — breached by ' + slaInfo.breach_duration);
            } else {
                g_form.addInfoMessage(msg);
            }
        }
    });
}
```

**Solution (Script Include method to add to UPIAjaxUtils):**

```javascript
getSLAInfo: function() {
    var taskId = this.getParameter('sysparm_task_id');

    if (!taskId) {
        return JSON.stringify({ has_active_sla: false });
    }

    var gr = new GlideRecord('task_sla');
    gr.addQuery('task', taskId);
    gr.addQuery('active', true);
    gr.orderBy('end_time');
    gr.setLimit(1);
    gr.query();

    if (!gr.next()) {
        return JSON.stringify({ has_active_sla: false });
    }

    var now = new GlideDateTime();
    var endTime = new GlideDateTime(gr.end_time.toString());
    var remaining = GlideDateTime.subtract(now, endTime);

    var result = {
        has_active_sla: true,
        sla_name: gr.sla.getDisplayValue(),
        stage: gr.stage.getDisplayValue(),
        has_breached: gr.has_breached.toString() === 'true',
        time_remaining: remaining.getDisplayValue(),
        percentage: gr.percentage.toString(),
        end_time: gr.end_time.getDisplayValue()
    };

    if (result.has_breached) {
        result.breach_duration = remaining.getDisplayValue();
    }

    return JSON.stringify(result);
},
```

---

### Exercise C: Settlement Batch ID UI Policy

**Task:** Create a UI Policy that shows a "Settlement Batch ID" field when Subcategory is "Settlement".

**Requirements:**
- Add a custom field `u_settlement_batch_id` (String, 40) to the Incident table
- Create a UI Policy with condition: Subcategory = Settlement
- Actions: Show and make mandatory the Settlement Batch ID field
- Enable "Reverse if false"

**Solution:**

1. Add the custom field:
   - Navigate to the Incident table definition
   - Add column: Label = "Settlement Batch ID", Name = `u_settlement_batch_id`, Type = String, Length = 40

2. Create the UI Policy:

| Field | Value |
|---|---|
| Name | NPCI - Settlement Batch ID |
| Table | Incident |
| On load | true |
| Reverse if false | true |
| Condition | Subcategory is settlement |

3. Add UI Policy Action:

| Field Name | Mandatory | Visible | Read Only |
|---|---|---|---|
| Settlement Batch ID | true | true | -- |

---

### Exercise D: Change Risk Calculator Script Include

**Task:** Write a Script Include that calculates a risk score for Change Requests based on CI criticality, change type, and timing.

**Solution:**

```javascript
var ChangeRiskCalculator = Class.create();
ChangeRiskCalculator.prototype = {
    initialize: function() {
        this.LOG_PREFIX = 'ChangeRiskCalculator: ';
    },

    /**
     * Calculate the risk score for a change request.
     *
     * @param {GlideRecord} changeGr - The change_request GlideRecord
     * @returns {object} { score: number, level: string, factors: array }
     */
    calculateRisk: function(changeGr) {
        var score = 0;
        var factors = [];

        // Factor 1: Change Type (0-30 points)
        var typeScores = {
            'standard':  5,
            'normal':    15,
            'emergency': 30
        };
        var changeType = changeGr.type.toString().toLowerCase();
        var typeScore = typeScores[changeType] || 15;
        score += typeScore;
        factors.push('Change type (' + changeType + '): +' + typeScore);

        // Factor 2: CI Criticality (0-30 points)
        if (!changeGr.cmdb_ci.nil()) {
            var ciGr = new GlideRecord('cmdb_ci');
            if (ciGr.get(changeGr.cmdb_ci)) {
                var businessCriticality = ciGr.getValue('busines_criticality') || '3';
                var critScores = { '1': 30, '2': 20, '3': 10, '4': 5 };
                var critScore = critScores[businessCriticality] || 10;
                score += critScore;
                factors.push('CI criticality (' + businessCriticality + '): +' + critScore);

                // Check if CI has recent incidents (additional risk)
                var utils = new UPIUtils();
                var related = utils.getRelatedIncidents(changeGr.cmdb_ci, 7);
                if (related.count > 0) {
                    var incidentRisk = Math.min(related.count * 5, 15);
                    score += incidentRisk;
                    factors.push('Recent incidents (' + related.count + ' in 7 days): +' + incidentRisk);
                }
            }
        } else {
            score += 10;
            factors.push('No CI linked (unknown impact): +10');
        }

        // Factor 3: Implementation Window (0-20 points)
        if (!changeGr.start_date.nil()) {
            var startDate = new GlideDateTime(changeGr.start_date.toString());
            var dayOfWeek = startDate.getDayOfWeekLocalTime();
            // Weekend = lower risk, weekday = higher risk
            if (dayOfWeek == 1 || dayOfWeek == 7) {
                score += 5;
                factors.push('Weekend implementation: +5');
            } else {
                score += 15;
                factors.push('Weekday implementation: +15');
            }

            // Business hours = higher risk
            var hour = parseInt(startDate.getLocalTime().toString().substring(0, 2), 10);
            if (hour >= 9 && hour <= 17) {
                score += 10;
                factors.push('During business hours: +10');
            } else {
                score += 3;
                factors.push('Outside business hours: +3');
            }
        }

        // Factor 4: Scope of Impact (0-20 points)
        var impact = parseInt(changeGr.impact, 10) || 3;
        var impactScores = { 1: 20, 2: 12, 3: 5 };
        var impactScore = impactScores[impact] || 5;
        score += impactScore;
        factors.push('Impact level (' + impact + '): +' + impactScore);

        // Determine risk level
        var level;
        if (score >= 70) {
            level = 'High';
        } else if (score >= 40) {
            level = 'Moderate';
        } else {
            level = 'Low';
        }

        gs.info(this.LOG_PREFIX + 'Risk score for ' + changeGr.number +
                ': ' + score + ' (' + level + ')');

        return {
            score: score,
            level: level,
            factors: factors
        };
    },

    type: 'ChangeRiskCalculator'
};
```

---

### Exercise E: "Link to Known Error" UI Action

**Task:** Create a UI Action button that searches the Knowledge Base for articles matching the incident's short description and category.

**Solution:**

**Navigation:** System Definition > UI Actions > New

| Field | Value |
|---|---|
| Name | Link to Known Error |
| Table | Incident [incident] |
| Action name | npci_link_known_error |
| Show update | true |
| Form button | true |
| Client | true |
| Order | 150 |
| Condition | `current.state != 7` |

**Client Script:**

```javascript
function npci_link_known_error() {
    var shortDesc = g_form.getValue('short_description');
    var category = g_form.getValue('category');

    if (!shortDesc) {
        alert('Please enter a Short Description before searching for Known Errors.');
        return false;
    }

    // Build a search query for the Knowledge Base
    var searchTerms = encodeURIComponent(shortDesc);
    var kbUrl = '/kb_find.do?sysparm_search=' + searchTerms;

    if (category) {
        kbUrl += '&sysparm_category=' + category;
    }

    // Open KB search in a new window
    var kbWindow = window.open(kbUrl, 'kb_search',
        'width=1000,height=700,scrollbars=yes,resizable=yes');

    if (kbWindow) {
        kbWindow.focus();
    }

    return false;  // Prevent form submission
}
```

---

## Appendix: Complete Script Reference

Below is a consolidated reference of all scripts created in this lab, organized by type.

### A.1 Business Rules Summary

| # | Name | Type | Table | Trigger |
|---|---|---|---|---|
| 1 | Auto-populate CI from Category | Before | Incident | Insert, Update |
| 2 | Prevent P1 Close Without Root Cause | Before | Incident | Update |
| 3 | Notify VIP Callers | After | Incident | Insert |
| 4 | Calculate Business Duration | After | Incident | Update |
| 5 | Auto-create Problem for Recurring Incidents | Async | Incident | Update |

### A.2 Client Scripts Summary

| # | Name | Type | Field | Table |
|---|---|---|---|---|
| 1 | Mandatory Fields on P1 | onChange | Priority | Incident |
| 2 | Auto-populate Contact Info | onChange | Caller | Incident |
| 3 | Confirm Before Major State Change | onSubmit | -- | Incident |
| 4 | Dynamic Category Subcategory | onChange | Category | Incident |

### A.3 UI Policies Summary

| # | Name | Condition | Reverse if False |
|---|---|---|---|
| 1 | Show Resolution Fields When Resolved | State = Resolved | Yes |
| 2 | Lock Fields After Closure | State = Closed | Yes |
| 3 | Major Incident Fields | Priority = 1 - Critical | Yes |
| 4 | UPI-Specific Fields | Category = UPI | Yes |

### A.4 Script Includes Summary

| # | Name | Client Callable | Methods |
|---|---|---|---|
| 1 | UPIUtils | No | getRelatedIncidents, calculateMTTR, isVIPCaller, getCISupportGroup, isRecurringIssue |
| 2 | UPIAjaxUtils | Yes | getCallerInfo, getCIDetails, getSubcategories |

### A.5 UI Actions Summary

| # | Name | Type | Condition |
|---|---|---|---|
| 1 | Escalate to P1 | Form Button | Priority != 1 |
| 2 | Create Problem from Incident | Form Link | State != Closed, has itil role |
| 3 | View CI Dependency Map | Form Link (Client) | CI is not empty |

### A.6 Custom Fields Added to Incident Table

| Label | Column Name | Type | Length |
|---|---|---|---|
| UPI Transaction ID | u_upi_transaction_id | String | 40 |
| UPI Error Code | u_upi_error_code | String | 20 |
| Affected Bank | u_affected_bank | String | 100 |
| Transaction Amount | u_transaction_amount | Decimal | -- |
| Merchant ID | u_merchant_id | String | 40 |
| Settlement Batch ID | u_settlement_batch_id | String | 40 |

---

## Key Takeaways

1. **Business Rules** enforce server-side logic that cannot be bypassed by the client — use them for data integrity, cascading updates, and automated record creation.

2. **Client Scripts** provide real-time feedback in the browser — use them for UI behavior, confirmations, and dynamic field interactions, but remember they can be bypassed via API or list edits.

3. **UI Policies** are the preferred method for simple field visibility, mandatory, and read-only control — they require no code and are easier to maintain.

4. **Script Includes** keep your code DRY (Don't Repeat Yourself) — write reusable utility classes and extend `AbstractAjaxProcessor` for client-callable methods.

5. **UI Actions** extend the form with custom buttons and links — combine client and server scripts for confirmation dialogs with server-side processing.

6. **Always layer your protections:** Use UI Policies for user guidance, Client Scripts for real-time validation, and Business Rules for enforcement. Never rely solely on client-side validation.

---

## What's Next

In **Lab 22**, you will bring everything together with **Update Sets, Automated Testing (ATF), and Deployment** — packaging all the configurations from Labs 01-21 into a deployable update set, writing automated test cases, and simulating a production deployment pipeline.
