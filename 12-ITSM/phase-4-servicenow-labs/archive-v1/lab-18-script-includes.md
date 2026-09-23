# Lab 18: Script Includes & Server-Side Scripting

**Level:** Advanced | **Duration:** 90 minutes | **Prerequisites:** Lab 16-17 completed

---

## Objective

By the end of this lab, you will:
- Create Script Includes for reusable server-side logic
- Understand class inheritance with Object.extendsObject
- Use advanced GlideRecord patterns (encoded queries, aggregates, joins)
- Use GlideSystem (gs) utility methods
- Debug server-side scripts effectively
- Use Background Scripts for testing

---

## Part 1: Script Includes

### What Are Script Includes?

Script Includes are **reusable server-side JavaScript libraries**. They're like utility classes that can be called from:
- Business Rules
- Other Script Includes
- Scheduled Jobs
- Flow Designer scripts
- Client Scripts (via GlideAjax, if client-callable)

### Step 1.1: Create a Utility Script Include

1. Navigate to **System Definition > Script Includes** (or type `sys_script_include.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | IncidentHelper |
   | API Name | global.IncidentHelper |
   | Client callable | Unchecked (server-only for now) |
   | Active | Checked |

4. **Script**:
   ```javascript
   var IncidentHelper = Class.create();
   IncidentHelper.prototype = {
       initialize: function() {
           // Constructor
       },

       /**
        * Get count of open incidents for a specific CI
        * @param {string} ciSysId - sys_id of the Configuration Item
        * @returns {number} count of open incidents
        */
       getOpenIncidentCountForCI: function(ciSysId) {
           var gr = new GlideAggregate('incident');
           gr.addQuery('cmdb_ci', ciSysId);
           gr.addQuery('state', 'NOT IN', '6,7,8');
           gr.addAggregate('COUNT');
           gr.query();
           if (gr.next()) {
               return parseInt(gr.getAggregate('COUNT'));
           }
           return 0;
       },

       /**
        * Get the most common category for incidents in the last N days
        * @param {number} days - number of days to look back
        * @returns {string} the most common category
        */
       getMostCommonCategory: function(days) {
           var gr = new GlideAggregate('incident');
           gr.addQuery('sys_created_on', '>=', gs.daysAgoStart(days));
           gr.addAggregate('COUNT', 'category');
           gr.orderByAggregate('COUNT', 'category');
           gr.query();

           if (gr.next()) {
               return gr.getValue('category');
           }
           return 'unknown';
       },

       /**
        * Check if a user has any overdue incidents assigned to them
        * @param {string} userSysId - sys_id of the user
        * @returns {object} { hasOverdue: boolean, count: number }
        */
       getUserOverdueIncidents: function(userSysId) {
           var gr = new GlideRecord('incident');
           gr.addQuery('assigned_to', userSysId);
           gr.addQuery('state', 'IN', '1,2'); // New or In Progress
           gr.addQuery('sla_due', '<', gs.nowDateTime());
           gr.query();

           return {
               hasOverdue: gr.hasNext(),
               count: gr.getRowCount()
           };
       },

       /**
        * Bulk reassign incidents from one group to another
        * @param {string} fromGroup - source group sys_id
        * @param {string} toGroup - destination group sys_id
        * @param {string} reason - reason for reassignment
        * @returns {number} number of incidents reassigned
        */
       bulkReassign: function(fromGroup, toGroup, reason) {
           var count = 0;
           var gr = new GlideRecord('incident');
           gr.addQuery('assignment_group', fromGroup);
           gr.addQuery('state', 'NOT IN', '6,7,8'); // Open only
           gr.query();

           while (gr.next()) {
               gr.assignment_group = toGroup;
               gr.work_notes = 'Bulk reassigned: ' + reason;
               gr.update();
               count++;
           }

           return count;
       },

       type: 'IncidentHelper'
   };
   ```

5. Click **Submit**

### Step 1.2: Call Script Include from a Business Rule

1. Create a new Business Rule or modify an existing one
2. In the script:
   ```javascript
   (function executeRule(current, previous) {

       var helper = new IncidentHelper();
       var count = helper.getOpenIncidentCountForCI(current.cmdb_ci);

       if (count >= 5) {
           current.work_notes = 'WARNING: ' + count +
               ' open incidents exist for this CI. Consider creating a Problem.';
       }

   })(current, previous);
   ```

---

## Part 2: Client-Callable Script Include

### Step 2.1: Create for GlideAjax

1. Create a new Script Include:

   | Field | Value |
   |---|---|
   | Name | ClientIncidentUtils |
   | Client callable | Checked |

2. **Script** (must extend AbstractAjaxProcessor):
   ```javascript
   var ClientIncidentUtils = Class.create();
   ClientIncidentUtils.prototype = Object.extendsObject(AbstractAjaxProcessor, {

       /**
        * Get incident statistics for a given assignment group
        * Called from Client Scripts via GlideAjax
        */
       getGroupStats: function() {
           var groupSysId = this.getParameter('sysparm_group_id');
           var result = {};

           // Total open
           var gr = new GlideAggregate('incident');
           gr.addQuery('assignment_group', groupSysId);
           gr.addQuery('state', 'NOT IN', '6,7,8');
           gr.addAggregate('COUNT');
           gr.query();
           result.total_open = gr.next() ?
               parseInt(gr.getAggregate('COUNT')) : 0;

           // P1 count
           var p1 = new GlideAggregate('incident');
           p1.addQuery('assignment_group', groupSysId);
           p1.addQuery('priority', 1);
           p1.addQuery('state', 'NOT IN', '6,7,8');
           p1.addAggregate('COUNT');
           p1.query();
           result.p1_count = p1.next() ?
               parseInt(p1.getAggregate('COUNT')) : 0;

           // Return as JSON string
           return JSON.stringify(result);
       },

       /**
        * Validate if a CI is in production
        */
       isCIProduction: function() {
           var ciSysId = this.getParameter('sysparm_ci_id');
           var gr = new GlideRecord('cmdb_ci');
           if (gr.get(ciSysId)) {
               return (gr.getValue('environment') == 'production').toString();
           }
           return 'false';
       },

       type: 'ClientIncidentUtils'
   });
   ```

3. Click **Submit**

### Step 2.2: Call from a Client Script

```javascript
// In a Client Script (onChange on assignment_group)
function onChange(control, oldValue, newValue, isLoading) {
    if (isLoading || newValue == '') return;

    var ga = new GlideAjax('ClientIncidentUtils');
    ga.addParam('sysparm_name', 'getGroupStats');
    ga.addParam('sysparm_group_id', newValue);
    ga.getXMLAnswer(function(answer) {
        var stats = JSON.parse(answer);
        if (stats.total_open > 20) {
            g_form.addWarningMessage('This group has ' +
                stats.total_open + ' open incidents (' +
                stats.p1_count + ' P1). Consider alternate assignment.');
        }
    });
}
```

---

## Part 3: Advanced GlideRecord Patterns

### Step 3.1: GlideAggregate (Counting & Grouping)

```javascript
// Count incidents by priority
var ga = new GlideAggregate('incident');
ga.addQuery('state', 'NOT IN', '6,7,8');
ga.addAggregate('COUNT', 'priority');
ga.groupBy('priority');
ga.query();

while (ga.next()) {
    gs.info('Priority ' + ga.priority + ': ' +
        ga.getAggregate('COUNT', 'priority') + ' incidents');
}

// Get average resolution time
var avgGa = new GlideAggregate('incident');
avgGa.addQuery('state', 6); // Resolved
avgGa.addAggregate('AVG', 'calendar_duration');
avgGa.query();
if (avgGa.next()) {
    gs.info('Average resolution time: ' +
        avgGa.getAggregate('AVG', 'calendar_duration'));
}
```

### Step 3.2: Encoded Queries

```javascript
// Use encoded queries for complex conditions
var gr = new GlideRecord('incident');
gr.addEncodedQuery('priority=1^state=2^assignment_groupISNOTEMPTY^opened_atRELATIVEGE@dayofweek@ago@7');
gr.query();

gs.info('Found ' + gr.getRowCount() + ' matching incidents');
```

### Step 3.3: Dot-Walking (Traversing References)

```javascript
// Access related record fields through references
var gr = new GlideRecord('incident');
gr.addQuery('priority', 1);
gr.query();

while (gr.next()) {
    // Dot-walk through references
    var callerName = gr.caller_id.name;               // User name
    var callerEmail = gr.caller_id.email;              // User email
    var callerDept = gr.caller_id.department.name;     // Department name
    var groupManager = gr.assignment_group.manager.name; // Group manager
    var ciClass = gr.cmdb_ci.sys_class_name;           // CI class

    gs.info(gr.number + ': Caller=' + callerName +
        ' (Dept: ' + callerDept + ')');
}
```

### Step 3.4: GlideRecord Best Practices

```javascript
// DO: Use setLimit() when you only need a few records
var gr = new GlideRecord('incident');
gr.addQuery('priority', 1);
gr.setLimit(10);  // Only get first 10
gr.query();

// DO: Use get() for single record lookups
var user = new GlideRecord('sys_user');
if (user.get('user_name', 'admin')) {
    gs.info('Found: ' + user.name);
}

// DO: Use GlideAggregate for counts instead of getRowCount()
// BAD (loads all records into memory):
var bad = new GlideRecord('incident');
bad.query();
var count = bad.getRowCount(); // Slow for large tables!

// GOOD (uses SQL COUNT):
var good = new GlideAggregate('incident');
good.addAggregate('COUNT');
good.query();
good.next();
var count = good.getAggregate('COUNT'); // Fast!

// DO: Use addEncodedQuery() for complex conditions
// Instead of multiple addQuery() calls for OR logic

// DON'T: Use GlideRecord in Client Scripts
// Use GlideAjax + Script Include instead
```

---

## Part 4: GlideSystem (gs) Utilities

### Step 4.1: Common gs Methods

```javascript
// User context
gs.getUserID();              // Current user's sys_id
gs.getUserName();            // Current user's username
gs.getUserDisplayName();     // Current user's display name
gs.hasRole('admin');         // Check if user has role

// Date/Time
gs.now();                    // Current date/time
gs.nowDateTime();            // Current date/time (formatted)
gs.daysAgo(7);               // DateTime 7 days ago
gs.daysAgoStart(7);          // Start of day 7 days ago
gs.beginningOfLastMonth();   // First day of last month

// Logging
gs.info('Info message');     // Log info
gs.warn('Warning message'); // Log warning
gs.error('Error message');  // Log error
gs.debug('Debug message');  // Log debug (if debug enabled)

// Messages (shown to user)
gs.addInfoMessage('Info');
gs.addErrorMessage('Error');

// Properties
gs.getProperty('property.name');  // Get system property value

// Generate unique IDs
gs.generateGUID();           // Generate a GUID
```

---

## Part 5: Background Scripts (Testing)

### Step 5.1: Access Background Scripts

1. Navigate to **System Definition > Scripts - Background** (or type `sys.scripts.do`)
2. This is a **sandbox** for running server-side scripts interactively

### Step 5.2: Test Your Script Include

```javascript
// Test IncidentHelper
var helper = new IncidentHelper();

// Test getOpenIncidentCountForCI
var ciGr = new GlideRecord('cmdb_ci');
ciGr.setLimit(1);
ciGr.query();
if (ciGr.next()) {
    var count = helper.getOpenIncidentCountForCI(ciGr.sys_id);
    gs.info('Open incidents for ' + ciGr.name + ': ' + count);
}

// Test getMostCommonCategory
var topCategory = helper.getMostCommonCategory(30);
gs.info('Most common category (30 days): ' + topCategory);
```

### Step 5.3: Run Quick Queries

```javascript
// Quick data exploration
var gr = new GlideRecord('incident');
gr.addQuery('priority', 1);
gr.setLimit(5);
gr.query();

while (gr.next()) {
    gs.info(gr.number + ' | ' + gr.short_description +
        ' | ' + gr.state.getDisplayValue());
}
```

### Step 5.4: Background Script Safety

```
WARNING: Background Scripts run as System Admin with no guardrails.
  - There is no undo
  - Changes are immediate and permanent
  - Always test with gs.info() first before making changes
  - Never run DELETE or UPDATE without testing the query first

Safe testing pattern:
  1. First: run a SELECT query to see what records match
  2. Verify the results are correct
  3. Then: run the UPDATE with the same query
```

---

## Part 6: Scheduled Jobs

### Step 6.1: Create a Scheduled Job

Scheduled Jobs run scripts on a recurring schedule.

1. Navigate to **System Definition > Scheduled Jobs** (or type `sysauto_script.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | Auto-close Resolved Incidents (7 days) |
   | Active | Checked |
   | Run | Daily |
   | Time | 02:00:00 (2 AM) |

4. **Script**:
   ```javascript
   // Auto-close incidents that have been in Resolved state for 7+ days
   var gr = new GlideRecord('incident');
   gr.addQuery('state', 6); // Resolved
   gr.addQuery('resolved_at', '<=', gs.daysAgo(7));
   gr.query();

   var count = 0;
   while (gr.next()) {
       gr.state = 7; // Closed
       gr.close_code = 'Solved (Permanently)';
       gr.close_notes = 'Auto-closed after 7 days in Resolved state. ' +
           'No reopening reported.';
       gr.update();
       count++;
   }

   gs.info('Auto-close job: Closed ' + count + ' incidents.');
   ```

5. Click **Submit**

---

## Part 7: Practice Exercises

### Exercise 1: SLA Reporting Script Include

Create a Script Include `SLAReporter` with methods:
1. `getBreachCountByPriority(days)` -- returns breach counts grouped by priority
2. `getAvgResolutionTime(priority, days)` -- returns average resolution time
3. `getTopOffenders(days, limit)` -- returns groups with most SLA breaches

Test each method using Background Scripts.

### Exercise 2: User Onboarding Script Include

Create `UserOnboardingHelper` with methods:
1. `createUser(firstName, lastName, email, department)` -- creates a sys_user record
2. `addToGroup(userSysId, groupName)` -- adds user to a group
3. `assignRole(userSysId, roleName)` -- assigns a role
4. `fullOnboard(userData)` -- calls all three methods in sequence

### Exercise 3: Data Cleanup Scheduled Job

Create a scheduled job that runs weekly:
1. Finds incidents older than 90 days that are still in "New" state
2. Changes them to "Closed" with close code "Closed/Resolved by Caller"
3. Logs the count of closed incidents
4. Sends a summary email to the admin

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created Script Includes | Reusable, testable server-side code |
| Extended AbstractAjaxProcessor | Bridge between client and server |
| Used GlideAggregate | Efficient counting and grouping |
| Mastered advanced GlideRecord | Complex queries, dot-walking, encoded queries |
| Used Background Scripts | Rapid testing and prototyping |
| Created Scheduled Jobs | Automated recurring tasks |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Script Include** | Reusable server-side JavaScript class |
| **AbstractAjaxProcessor** | Base class for client-callable Script Includes |
| **GlideAggregate** | API for COUNT, SUM, AVG, MIN, MAX operations |
| **Dot-walking** | Traversing reference fields (e.g., `caller_id.department.name`) |
| **Encoded Query** | String-based query conditions (e.g., `priority=1^state=2`) |
| **Background Scripts** | Interactive script execution sandbox for admins |
| **Scheduled Job** | Script that runs automatically on a schedule |
| **GlideSystem (gs)** | Utility API for user context, dates, logging |

---

## What's Next

Congratulations -- you've completed the **Advanced** scripting labs! You can now build custom automation with server-side and client-side scripts.

In **Lab 19**, you begin the **Expert** labs with **Reporting & Dashboards** -- building custom reports, charts, and performance analytics.
