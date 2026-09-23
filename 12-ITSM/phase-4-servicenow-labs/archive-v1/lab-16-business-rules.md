# Lab 16: Business Rules

**Level:** Advanced | **Duration:** 90 minutes | **Prerequisites:** Lab 07-15 completed, basic JavaScript knowledge

---

## Objective

By the end of this lab, you will:
- Understand the four types of Business Rules (before, after, async, display)
- Create Business Rules that execute server-side logic
- Use GlideRecord for database queries within Business Rules
- Use `current` and `previous` objects to detect field changes
- Debug Business Rules using logs and script debugger

---

## Part 1: Understanding Business Rules

### What Are Business Rules?

Business Rules are **server-side scripts** that execute when a record is displayed, inserted, updated, or deleted.

```
When to use Business Rules:
  - Validate data before saving
  - Auto-populate fields
  - Prevent certain actions
  - Trigger side effects (create related records, send events)
  - Complex server-side calculations

When NOT to use (use alternatives instead):
  - Simple field visibility → UI Policy
  - Client-side validation → Client Script
  - Automated workflows → Flow Designer
```

### Business Rule Timing

| When | Timing | Use Case |
|---|---|---|
| **before** | Before the record is saved to database | Validate, modify, abort |
| **after** | After the record is saved | Create related records, send notifications |
| **async** | After save, runs in background | Heavy processing, integrations |
| **display** | When form loads (before rendering) | Set g_scratchpad values for client scripts |

```
User clicks "Save"
       |
  [before] Business Rules run
       |-- Can modify `current` (changes are saved)
       |-- Can abort the save (current.setAbortAction(true))
       |
  Record written to database
       |
  [after] Business Rules run
       |-- Record is already saved
       |-- Can read current.sys_id (now has a value for insert)
       |-- Can create related records
       |
  [async] Business Rules run (background)
       |-- Runs in a separate thread
       |-- Good for slow operations
```

---

## Part 2: Create a Before Business Rule

### Step 2.1: Auto-Set Priority Based on Caller

1. Navigate to **System Definition > Business Rules** (or type `sys_script.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | Auto-set VIP Priority |
   | Table | Incident [incident] |
   | Active | Checked |
   | Advanced | Checked |
   | When | before |
   | Insert | Checked |
   | Update | Checked |

4. **Condition** (optional -- runs for all incidents if blank):
   Leave blank (we'll handle conditions in the script)

5. **Script**:
   ```javascript
   (function executeRule(current, previous /*null when insert*/) {

       // Check if the caller is a VIP (title contains "VP" or "Director" or "CTO")
       if (!current.caller_id.nil()) {
           var caller = current.caller_id.getRefRecord();
           var title = caller.getValue('title') || '';

           if (title.match(/VP|Director|CTO|CEO|CIO/i)) {
               // Boost urgency for VIP callers
               if (current.urgency > 1) {
                   current.urgency = 1; // Set to High
                   current.work_notes = 'VIP caller detected (' + title +
                       '). Urgency automatically elevated to High.';
               }
           }
       }

   })(current, previous);
   ```

6. Click **Submit**

### Step 2.2: Test the Business Rule

1. Create a new incident
2. Set the Caller to a user with "VP" or "Director" in their title
   - (You may need to edit a demo user to add this title first)
3. Set Urgency to 2 - Medium
4. Click **Submit**
5. Open the incident -- Urgency should be 1 - High, with a work note

### Step 2.3: Before Rule -- Prevent Closure Without Resolution

1. Create a new Business Rule:

   | Field | Value |
   |---|---|
   | Name | Require Resolution Notes on Close |
   | Table | Incident [incident] |
   | When | before |
   | Update | Checked |
   | Advanced | Checked |

2. **Script**:
   ```javascript
   (function executeRule(current, previous) {

       // If state is changing to Resolved or Closed
       if (current.state.changesTo(6) || current.state.changesTo(7)) {
           // Check if close_notes or resolution_notes is empty
           if (current.close_notes.nil() && current.resolution_notes.nil()) {
               current.setAbortAction(true);
               gs.addErrorMessage('Resolution notes are required when resolving or closing an incident.');
           }
       }

   })(current, previous);
   ```

3. Click **Submit**
4. **Test:** Try to close an incident without resolution notes -- you should see an error message

---

## Part 3: Create an After Business Rule

### Step 3.1: Auto-Create Problem for Repeated Incidents

1. Create a new Business Rule:

   | Field | Value |
   |---|---|
   | Name | Auto-create Problem for Repeated CI Incidents |
   | Table | Incident [incident] |
   | When | after |
   | Insert | Checked |
   | Advanced | Checked |

2. **Script**:
   ```javascript
   (function executeRule(current, previous) {

       // Only run if a CI is set
       if (current.cmdb_ci.nil()) return;

       // Count open incidents for the same CI in the last 7 days
       var gr = new GlideRecord('incident');
       gr.addQuery('cmdb_ci', current.cmdb_ci);
       gr.addQuery('state', 'NOT IN', '6,7,8'); // Not resolved, closed, canceled
       gr.addQuery('sys_created_on', '>=', gs.daysAgoStart(7));
       gr.query();
       var count = gr.getRowCount();

       // If 3 or more incidents for same CI, auto-create a problem
       if (count >= 3) {
           // Check if a problem already exists for this CI
           var existingPrb = new GlideRecord('problem');
           existingPrb.addQuery('cmdb_ci', current.cmdb_ci);
           existingPrb.addQuery('state', 'NOT IN', '6,7,8');
           existingPrb.query();

           if (!existingPrb.hasNext()) {
               // Create new problem
               var prb = new GlideRecord('problem');
               prb.initialize();
               prb.short_description = 'Recurring incidents for CI: ' +
                   current.cmdb_ci.getDisplayValue();
               prb.description = count + ' incidents reported for ' +
                   current.cmdb_ci.getDisplayValue() +
                   ' in the last 7 days. Investigation required.';
               prb.cmdb_ci = current.cmdb_ci;
               prb.assignment_group = current.assignment_group;
               prb.priority = current.priority;
               var prbId = prb.insert();

               // Link this incident to the new problem
               current.problem_id = prbId;
               current.work_notes = 'Auto-created Problem ' +
                   prb.number + ' due to ' + count +
                   ' incidents for this CI in the last 7 days.';
               current.update();
           }
       }

   })(current, previous);
   ```

3. Click **Submit**

---

## Part 4: Display Business Rule

### Step 4.1: Pass Data to Client Scripts via g_scratchpad

Display Business Rules run when a form loads. They can pass server-side data to client scripts using `g_scratchpad`.

1. Create a new Business Rule:

   | Field | Value |
   |---|---|
   | Name | Load CI Incident Count |
   | Table | Incident [incident] |
   | When | display |
   | Advanced | Checked |

2. **Script**:
   ```javascript
   (function executeRule(current, previous) {

       // Count open incidents for this CI
       if (!current.cmdb_ci.nil()) {
           var gr = new GlideRecord('incident');
           gr.addQuery('cmdb_ci', current.cmdb_ci);
           gr.addQuery('state', 'NOT IN', '6,7,8');
           gr.addQuery('sys_id', '!=', current.sys_id);
           gr.query();
           g_scratchpad.ci_incident_count = gr.getRowCount();
           g_scratchpad.ci_name = current.cmdb_ci.getDisplayValue();
       } else {
           g_scratchpad.ci_incident_count = 0;
       }

   })(current, previous);
   ```

3. Click **Submit**

Now a Client Script (Lab 17) can access `g_scratchpad.ci_incident_count` to display an info message.

---

## Part 5: GlideRecord Deep Dive

### Step 5.1: GlideRecord Basics

GlideRecord is the API for querying and manipulating database records:

```javascript
// Query: Find all P1 open incidents
var gr = new GlideRecord('incident');
gr.addQuery('priority', 1);
gr.addQuery('state', '!=', 7); // not closed
gr.query();

while (gr.next()) {
    gs.info('Incident: ' + gr.number + ' - ' + gr.short_description);
}

// Insert: Create a new record
var newInc = new GlideRecord('incident');
newInc.initialize();
newInc.short_description = 'Auto-generated incident';
newInc.caller_id = gs.getUserID();
newInc.priority = 3;
newInc.insert();

// Update: Modify an existing record
var updInc = new GlideRecord('incident');
if (updInc.get('number', 'INC0010001')) {
    updInc.state = 2; // In Progress
    updInc.work_notes = 'Updated via script';
    updInc.update();
}

// Delete: Remove a record (use with extreme caution!)
var delInc = new GlideRecord('incident');
if (delInc.get('number', 'INC9999999')) {
    delInc.deleteRecord();
}
```

### Step 5.2: Key GlideRecord Methods

| Method | Description | Example |
|---|---|---|
| `addQuery(field, value)` | Add a filter condition | `gr.addQuery('priority', 1)` |
| `addQuery(field, operator, value)` | Filter with operator | `gr.addQuery('state', '!=', 7)` |
| `query()` | Execute the query | `gr.query()` |
| `next()` | Move to next record | `while (gr.next()) {...}` |
| `hasNext()` | Check if more records exist | `if (gr.hasNext()) {...}` |
| `get(field, value)` | Get a single record | `gr.get('number', 'INC001')` |
| `getValue(field)` | Get field value as string | `gr.getValue('priority')` |
| `setValue(field, value)` | Set field value | `gr.setValue('state', 2)` |
| `getRowCount()` | Count matching records | `var count = gr.getRowCount()` |
| `initialize()` | Prepare for insert | `gr.initialize()` |
| `insert()` | Insert new record | `var sysId = gr.insert()` |
| `update()` | Save changes | `gr.update()` |
| `deleteRecord()` | Delete current record | `gr.deleteRecord()` |
| `getDisplayValue()` | Get display value | `gr.caller_id.getDisplayValue()` |
| `nil()` | Check if field is empty | `if (gr.cmdb_ci.nil())` |
| `changesTo(value)` | Check if field changed to value | `current.state.changesTo(6)` |
| `changes()` | Check if field changed at all | `current.priority.changes()` |

### Step 5.3: Using `current` and `previous`

```javascript
// current  = the record being saved (with new values)
// previous = the record before the save (with old values)
//            previous is null on INSERT

// Detect if priority changed
if (current.priority.changes()) {
    gs.info('Priority changed from ' + previous.priority + ' to ' + current.priority);
}

// Detect if state changed to Resolved
if (current.state.changesTo(6)) {
    gs.info('Incident resolved!');
}

// Check if a specific field was modified
if (current.assignment_group.changes()) {
    current.work_notes = 'Reassigned from ' +
        previous.assignment_group.getDisplayValue() + ' to ' +
        current.assignment_group.getDisplayValue();
}
```

---

## Part 6: Debugging Business Rules

### Step 6.1: Using gs.info() for Logging

```javascript
gs.info('Business Rule fired for: ' + current.number);
gs.info('Priority: ' + current.priority + ', State: ' + current.state);
```

View logs at: **System Logs > System Log > All** (or `syslog.list`)

### Step 6.2: Using gs.addInfoMessage / gs.addErrorMessage

```javascript
// Show a blue info banner on the form
gs.addInfoMessage('This is an informational message');

// Show a red error banner
gs.addErrorMessage('Something went wrong!');
```

### Step 6.3: Script Debugger

1. Navigate to **System Diagnostics > Script Debugger**
2. Set breakpoints in your Business Rules
3. Trigger the Business Rule (e.g., save an incident)
4. The debugger pauses at your breakpoint
5. Inspect variables, step through code

### Step 6.4: Business Rule Order

When multiple Business Rules fire on the same table/action, they execute in **Order** number sequence (lowest first).

| Order | Rule Name | Timing |
|---|---|---|
| 100 | Validate Fields | before |
| 200 | Auto-set Priority | before |
| 300 | Send Notification | after |
| 1000 | Heavy Processing | async |

Set the **Order** field on each Business Rule to control execution sequence.

---

## Part 7: Practice Exercises

### Exercise 1: Before Rule -- Auto-set Category

Create a Business Rule that automatically sets the Category based on the Assignment Group:
- If Assignment group = "Network", set Category = "Network"
- If Assignment group = "Hardware", set Category = "Hardware"
- If Assignment group = "Software", set Category = "Software"

### Exercise 2: After Rule -- Notify on Reassignment

Create a Business Rule that:
- Triggers when an incident's assignment_group changes
- Sends an event `incident.reassigned`
- Adds a work note: "Reassigned from [old group] to [new group] by [current user]"

### Exercise 3: Before Rule -- Prevent Reopening

Create a Business Rule that:
- Prevents changing state from Closed back to any other state
- Shows an error message: "Closed incidents cannot be reopened. Please create a new incident."
- Aborts the save action

### Exercise 4: Debug Challenge

1. Create a Business Rule with an intentional bug (e.g., reference a non-existent field)
2. Trigger it by saving a record
3. Find the error in the System Logs
4. Fix the bug and verify

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created before rules | Validate and modify data before it's saved |
| Created after rules | Trigger actions after record is committed |
| Used display rules with g_scratchpad | Pass server data to client scripts |
| Mastered GlideRecord | Query and manipulate any table in ServiceNow |
| Debugged Business Rules | Essential skill for troubleshooting |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Business Rule** | Server-side script triggered on record insert/update/delete/display |
| **before** | Runs before database write -- can modify or abort |
| **after** | Runs after database write -- for side effects |
| **async** | Runs in background after database write |
| **display** | Runs when form loads -- passes data to client via g_scratchpad |
| **GlideRecord** | Server-side API for database CRUD operations |
| **current** | The record being saved (new values) |
| **previous** | The record before changes (old values) |
| **g_scratchpad** | Object to pass data from display rules to client scripts |

---

## What's Next

In **Lab 17**, you'll learn **Client Scripts** -- JavaScript that runs in the user's browser to create dynamic, interactive forms.
