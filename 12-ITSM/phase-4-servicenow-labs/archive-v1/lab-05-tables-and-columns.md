# Lab 05: Tables & Columns

**Level:** Beginner | **Duration:** 60 minutes | **Prerequisites:** Lab 01-04 completed

---

## Objective

By the end of this lab, you will:
- Understand ServiceNow's table structure and hierarchy
- Explore core ITSM tables using the Table schema
- Create a custom table with fields
- Understand field types, reference fields, and table relationships
- Use the Schema Map to visualize table relationships

---

## Part 1: Exploring Existing Tables

### Step 1.1: View Tables List

1. Navigate to **System Definition > Tables** (or type `sys_db_object.list`)
2. You'll see hundreds of tables -- ServiceNow has 4000+ tables out of the box
3. Use the search to find specific tables

### Step 1.2: Explore the Incident Table

1. In the tables list, search for: `incident`
2. Click on the **Incident** table record
3. Observe the table definition:
   ```
   Name:           incident
   Label:          Incident
   Extends:        Task [task]    <-- incident inherits from the task table
   Number prefix:  INC
   Active:         true
   ```

4. Scroll down to the **Columns** related list
5. Browse the columns (fields) that belong to the incident table:

   | Column Name | Type | Reference |
   |---|---|---|
   | number | String | -- |
   | short_description | String | -- |
   | priority | Integer | -- |
   | state | Integer | -- |
   | caller_id | Reference | sys_user |
   | assigned_to | Reference | sys_user |
   | assignment_group | Reference | sys_user_group |
   | cmdb_ci | Reference | cmdb_ci |
   | category | String (choice) | -- |
   | description | String | -- |

### Step 1.3: Understand Table Inheritance

ServiceNow uses table inheritance -- child tables inherit all columns from parent tables.

```
task (Parent table)
  |-- All common fields: number, short_description, assigned_to, state, priority
  |
  |-- incident (extends task)
  |     +-- caller_id, category, subcategory, cause (incident-specific fields)
  |
  |-- problem (extends task)
  |     +-- root_cause, known_error, first_reported (problem-specific fields)
  |
  |-- change_request (extends task)
  |     +-- type, risk, cab_required, rollback_plan (change-specific fields)
  |
  |-- sc_request (extends task)
  |     +-- requested_for, stage (request-specific fields)
  |
  |-- sc_task (extends task)
        +-- request_item, sc_catalog (catalog task-specific fields)
```

**Key insight:** The `task` table is the parent of all work items. This means you can query `task.list` to see ALL incidents, problems, changes, and requests in one list.

### Step 1.4: View the Task Table

1. Type `task.list` in Filter Navigator and press Enter
2. You'll see a combined list of incidents, problems, changes, requests, etc.
3. Notice the "Number" column shows different prefixes: INC, PRB, CHG, REQ, SCTASK
4. This proves they all live in the same table hierarchy

---

## Part 2: Field Types Deep Dive

### Step 2.1: Explore Field Types

Navigate to **System Definition > Tables**, open the `incident` table, and look at the Columns related list. Click on individual columns to see their types.

| Field Type | Description | Example | Storage |
|---|---|---|---|
| **String** | Text up to 255 chars | short_description | VARCHAR |
| **Integer** | Whole number | priority, state | INT |
| **Boolean** | True/False | active, knowledge | BOOLEAN |
| **Date/Time** | Date and time | opened_at, resolved_at | DATETIME |
| **Reference** | Link to another table | caller_id → sys_user | Foreign key (sys_id) |
| **Choice** | Predefined options | category, state | INT or STRING |
| **Journal** | Multi-line, append-only | work_notes, comments | TEXT (separate table) |
| **HTML** | Rich text | description (sometimes) | TEXT |
| **URL** | Web link | Related URL | VARCHAR |
| **Decimal** | Decimal number | Calculated scores | DECIMAL |
| **Currency** | Money value | Cost fields | DECIMAL |
| **Conditions** | Encoded query | Filter conditions | STRING |
| **Document ID** | Cross-table reference | task_ci | VARCHAR |

### Step 2.2: Reference Fields

Reference fields are the most important field type -- they create relationships between tables.

1. Open the `incident` table definition
2. Find the `caller_id` column
3. Click on it to see its properties:
   ```
   Column name:    caller_id
   Type:           Reference
   Reference:      User [sys_user]

   This means: the caller_id field stores the sys_id of a record
   in the sys_user table. On the form, it shows as a search box
   with the user's name.
   ```

4. On an incident form, the caller_id field shows as:
   ```
   Caller: [Abel Tuter 🔍]

   Behind the scenes, it stores: caller_id = "6816f79cc0a8016401c5a33be04be441"
   (that's Abel Tuter's sys_id in the sys_user table)
   ```

### Step 2.3: Choice Fields

Choice fields provide dropdown options.

1. Navigate to **System Definition > Choice Lists** (or type `sys_choice.list`)
2. Filter by: Table = incident, Element = state
3. You'll see the choice values:
   ```
   Value    Label
   1        New
   2        In Progress
   3        On Hold
   6        Resolved
   7        Closed
   8        Canceled
   ```

---

## Part 3: Create a Custom Table

### Step 3.1: Plan the Table

We'll create a table to track **Server Health Checks** -- a common operational task.

```
Table: Server Health Check
Purpose: Track regular health check activities on servers
Fields:
  - Server name (reference to CMDB)
  - Check date (date/time)
  - CPU status (choice: Normal/Warning/Critical)
  - Memory status (choice: Normal/Warning/Critical)
  - Disk status (choice: Normal/Warning/Critical)
  - Overall status (choice: Healthy/Degraded/Critical)
  - Notes (string)
  - Checked by (reference to sys_user)
```

### Step 3.2: Create the Table

1. Navigate to **System Definition > Tables** (or type `sys_db_object.list`)
2. Click **New**
3. Fill in the table form:

   | Field | Value |
   |---|---|
   | Label | Server Health Check |
   | Name | (auto-fills as `u_server_health_check`) |
   | Extends table | Task [task] (select this to inherit task fields) |
   | Add module to menu | Checked |
   | New module group | Server Health Checks |
   | Create access controls | Checked |

   **Note on naming:** Custom tables get the `u_` prefix automatically. This distinguishes custom tables from out-of-box (OOB) tables.

4. Click **Submit**

### Step 3.3: Verify Table Creation

1. Type `u_server_health_check.list` in Filter Navigator
2. You should see an empty list (no records yet)
3. Notice the table inherited fields from `task`: number, short_description, state, priority, etc.
4. Check the Application Navigator -- you should see a new module group "Server Health Checks"

### Step 3.4: Add Custom Fields

1. Open the table definition: **System Definition > Tables**, search for `u_server_health_check`
2. Click on it to open
3. Scroll down to the **Columns** tab/related list
4. Click **New** to add a column

**Field 1: Server**
| Field | Value |
|---|---|
| Type | Reference |
| Column label | Server |
| Column name | (auto-fills as `u_server`) |
| Reference | Configuration Item [cmdb_ci] |
| Mandatory | Checked |

Click **Submit**

**Field 2: Check Date**
| Field | Value |
|---|---|
| Type | Date/Time |
| Column label | Check Date |
| Column name | `u_check_date` |
| Mandatory | Checked |

Click **Submit**

**Field 3: CPU Status**
| Field | Value |
|---|---|
| Type | Choice |
| Column label | CPU Status |
| Column name | `u_cpu_status` |
| Choice values | Normal, Warning, Critical |

Click **Submit**, then add choices:
1. Go to **System Definition > Choice Lists**
2. Add choices for table `u_server_health_check`, element `u_cpu_status`:
   - Value: 1, Label: Normal
   - Value: 2, Label: Warning
   - Value: 3, Label: Critical

**Field 4: Memory Status** (same pattern as CPU Status)
| Field | Value |
|---|---|
| Type | Choice |
| Column label | Memory Status |
| Column name | `u_memory_status` |
| Choice values | Normal, Warning, Critical |

**Field 5: Disk Status** (same pattern)
| Field | Value |
|---|---|
| Type | Choice |
| Column label | Disk Status |
| Column name | `u_disk_status` |
| Choice values | Normal, Warning, Critical |

**Field 6: Overall Status**
| Field | Value |
|---|---|
| Type | Choice |
| Column label | Overall Status |
| Column name | `u_overall_status` |
| Choice values | Healthy, Degraded, Critical |

**Field 7: Checked By**
| Field | Value |
|---|---|
| Type | Reference |
| Column label | Checked By |
| Column name | `u_checked_by` |
| Reference | User [sys_user] |

### Step 3.5: Alternative -- Add Fields via Form Designer

A faster way to add fields:
1. Navigate to `u_server_health_check.do` (opens a blank form)
2. Click the **hamburger menu** (≡) at the top of the form
3. Select **Configure > Form Layout** (or **Form Designer**)
4. In the Form Designer, you can drag and drop fields onto the form
5. To create a new field, type a label in the "New field" section, select a type, and drag it to the form

---

## Part 4: Configure the Form Layout

### Step 4.1: Open Form Layout

1. Navigate to `u_server_health_check.do` (new form)
2. Right-click the form header
3. Select **Configure > Form Layout**

### Step 4.2: Arrange Fields

In the Form Layout dialog, arrange the fields:

```
Section 1: (default section)
  Row 1: Number          | State
  Row 2: Server          | Checked By
  Row 3: Check Date      | Overall Status
  Row 4: Short description (full width)

Section 2: "Status Details"
  Row 1: CPU Status      | Memory Status
  Row 2: Disk Status     |

Section 3: "Notes" (inherited from task)
  Work notes
  Additional comments
```

Move fields between Available and Selected, reorder them, and click **Save**.

### Step 4.3: Create a Test Record

1. Navigate to `u_server_health_check.do`
2. Fill in the form:

   | Field | Value |
   |---|---|
   | Short description | Monthly health check - Web Server 01 |
   | Server | (search for any CI, or type "Web Server") |
   | Check Date | Today's date |
   | Checked By | Ravi Kumar |
   | CPU Status | Normal |
   | Memory Status | Warning |
   | Disk Status | Normal |
   | Overall Status | Degraded |

3. Click **Submit**
4. Navigate to `u_server_health_check.list` -- you should see your record

---

## Part 5: Schema Map

### Step 5.1: View the Schema Map

1. Navigate to **System Definition > Tables**
2. Open the `incident` table
3. Look for a **Schema Map** related link or button
4. Alternatively, type `schema_map.do` in Filter Navigator
5. The Schema Map shows a visual diagram of table relationships:

```
                    task
                     |
        +------------+------------+
        |            |            |
    incident     problem    change_request
        |
   caller_id ----> sys_user
   cmdb_ci ------> cmdb_ci
   assignment_group -> sys_user_group
```

### Step 5.2: Explore Relationships

1. In the Schema Map, click on any table to expand its relationships
2. Note how many tables reference `sys_user` (users are referenced everywhere)
3. Note how `cmdb_ci` is referenced by incidents, problems, and changes

---

## Part 6: Practice Exercises

### Exercise 1: Table Investigation

Answer these questions by exploring table definitions:

1. What table does `problem` extend? → ___________
2. What is the number prefix for change_request? → ___________
3. How many columns does the `incident` table have? → ___________
4. What table does the `assignment_group` field reference? → ___________
5. Is the `state` field a String or Integer type? → ___________

### Exercise 2: Create Another Custom Table

Create a table called **Application Deployment** to track deployments:
- Extends: Task
- Fields to add:
  - Application Name (String, mandatory)
  - Environment (Choice: Dev, Staging, Production)
  - Version (String)
  - Deployed By (Reference: sys_user)
  - Deployment Date (Date/Time)
  - Deployment Status (Choice: Planned, In Progress, Completed, Failed, Rolled Back)
  - Rollback Plan (String, multi-line)

### Exercise 3: Create Records

1. Create 3 Server Health Check records with different status values
2. Navigate to the list view and confirm all 3 appear
3. Sort by Overall Status
4. Filter to show only records where Overall Status = Critical or Degraded

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Explored table structure | Everything in ServiceNow is a table -- understanding tables is fundamental |
| Understood inheritance | task → incident/problem/change: shared fields, efficient design |
| Created a custom table | Extend ServiceNow for your organization's unique needs |
| Added custom fields | Define the data your process needs to capture |
| Used Schema Map | Visualize how tables connect -- crucial for reporting and integration |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Table** | A database table storing records (rows) with fields (columns) |
| **Table Inheritance** | Child tables inherit all fields from parent tables |
| **sys_id** | Unique 32-character identifier for every record in ServiceNow |
| **Reference Field** | A field that links to a record in another table (foreign key) |
| **Choice Field** | A field with predefined dropdown options |
| **u_ prefix** | Custom tables and fields get this prefix automatically |
| **Schema Map** | Visual diagram showing table relationships |
| **Number Prefix** | Auto-generated prefix for record numbers (INC, PRB, CHG) |

---

## What's Next

In **Lab 06**, you'll master filters, views, and list controls -- essential for working efficiently with data in ServiceNow.

---

## Appendix: Bulk Setup via Background Script

> **Shortcut:** Instead of performing Parts 3-4 manually through the UI, you can run this single background script to create the custom table, add all fields, set up choice lists, and insert a test record.

### How to Run

1. Navigate to **System Definition > Scripts - Background** (or type `scripts` in Filter Navigator)
2. Paste the entire script below and click **Run script**
3. Check the output pane for confirmation messages
4. After running, verify by navigating to `u_server_health_check.list`

### What This Script Covers

| Manual Steps | What the Script Does |
|---|---|
| Step 3.2 | Creates the `u_server_health_check` table (extends Task) |
| Steps 3.4 | Adds all 7 custom columns (Server, Check Date, CPU/Memory/Disk/Overall Status, Checked By) |
| Steps 3.4 (choices) | Creates all choice list values for status fields |
| Step 4.3 | Inserts a test record |
| Exercise 2 | Creates the `u_application_deployment` table with all fields and choices |
| Exercise 3 | Inserts 3 sample Server Health Check records |

### The Script

```javascript
// ============================================================
// Lab 05 - Full Setup: Tables, Columns, Choices, Test Records
// Run in: System Definition > Scripts - Background
// Idempotent -- safe to run multiple times
// ============================================================

// --- Helper: Create a table ---
function createTable(label, name, extendsTable) {
  var gr = new GlideRecord('sys_db_object');
  gr.addQuery('name', name);
  gr.query();
  if (gr.next()) {
    gs.info('Table already exists: ' + name);
    return gr.sys_id.toString();
  }
  gr.initialize();
  gr.label = label;
  gr.name = name;
  gr.super_class = getTableSysId(extendsTable);
  gr.is_extendable = true;
  gr.create_access_controls = true;
  var sysId = gr.insert();
  gs.info('Created table: ' + name);
  return sysId;
}

// --- Helper: Get table sys_id ---
function getTableSysId(tableName) {
  var gr = new GlideRecord('sys_db_object');
  gr.addQuery('name', tableName);
  gr.query();
  if (gr.next()) return gr.sys_id.toString();
  return null;
}

// --- Helper: Add a column to a table ---
function addColumn(tableName, columnLabel, columnName, columnType, reference, mandatory) {
  var gr = new GlideRecord('sys_dictionary');
  gr.addQuery('name', tableName);
  gr.addQuery('element', columnName);
  gr.query();
  if (gr.next()) {
    gs.info('  Column already exists: ' + tableName + '.' + columnName);
    return;
  }
  gr.initialize();
  gr.name = tableName;
  gr.element = columnName;
  gr.column_label = columnLabel;
  gr.internal_type = columnType;
  if (reference) gr.reference = getTableSysId(reference);
  if (mandatory) gr.mandatory = true;
  gr.insert();
  gs.info('  Added column: ' + tableName + '.' + columnName + ' (' + columnType + ')');
}

// --- Helper: Add a choice value ---
function addChoice(tableName, element, value, label, sequence) {
  var gr = new GlideRecord('sys_choice');
  gr.addQuery('name', tableName);
  gr.addQuery('element', element);
  gr.addQuery('value', value);
  gr.query();
  if (gr.next()) {
    gs.info('    Choice already exists: ' + element + ' = ' + label);
    return;
  }
  gr.initialize();
  gr.name = tableName;
  gr.element = element;
  gr.value = value;
  gr.label = label;
  gr.sequence = sequence || 0;
  gr.language = 'en';
  gr.insert();
  gs.info('    Added choice: ' + element + ' = ' + label);
}

// --- Helper: Get user sys_id ---
function getUserSysId(userName) {
  var gr = new GlideRecord('sys_user');
  gr.addQuery('user_name', userName);
  gr.query();
  if (gr.next()) return gr.sys_id.toString();
  return null;
}

// ============================================================
// PART A: Server Health Check Table (Steps 3.2 - 3.4)
// ============================================================

gs.info('--- Creating Server Health Check table ---');
createTable('Server Health Check', 'u_server_health_check', 'task');

// Add custom columns
addColumn('u_server_health_check', 'Server',         'u_server',         'reference',  'cmdb_ci',  true);
addColumn('u_server_health_check', 'Check Date',     'u_check_date',     'glide_date_time', null,  true);
addColumn('u_server_health_check', 'CPU Status',     'u_cpu_status',     'choice',     null,       false);
addColumn('u_server_health_check', 'Memory Status',  'u_memory_status',  'choice',     null,       false);
addColumn('u_server_health_check', 'Disk Status',    'u_disk_status',    'choice',     null,       false);
addColumn('u_server_health_check', 'Overall Status', 'u_overall_status', 'choice',     null,       false);
addColumn('u_server_health_check', 'Checked By',     'u_checked_by',     'reference',  'sys_user', false);

// Add choices for CPU / Memory / Disk Status
var statusFields = ['u_cpu_status', 'u_memory_status', 'u_disk_status'];
for (var s = 0; s < statusFields.length; s++) {
  addChoice('u_server_health_check', statusFields[s], '1', 'Normal',   100);
  addChoice('u_server_health_check', statusFields[s], '2', 'Warning',  200);
  addChoice('u_server_health_check', statusFields[s], '3', 'Critical', 300);
}

// Add choices for Overall Status
addChoice('u_server_health_check', 'u_overall_status', '1', 'Healthy',  100);
addChoice('u_server_health_check', 'u_overall_status', '2', 'Degraded', 200);
addChoice('u_server_health_check', 'u_overall_status', '3', 'Critical', 300);

// ============================================================
// PART B: Insert Test Records (Step 4.3 + Exercise 3)
// ============================================================

gs.info('--- Creating test records ---');

var testRecords = [
  {
    short_description: 'Monthly health check - Web Server 01',
    u_check_date:      gs.nowDateTime(),
    u_checked_by:      getUserSysId('ravi.kumar'),
    u_cpu_status:      '1',  // Normal
    u_memory_status:   '2',  // Warning
    u_disk_status:     '1',  // Normal
    u_overall_status:  '2'   // Degraded
  },
  {
    short_description: 'Monthly health check - DB Server 01',
    u_check_date:      gs.nowDateTime(),
    u_checked_by:      getUserSysId('priya.sharma'),
    u_cpu_status:      '3',  // Critical
    u_memory_status:   '3',  // Critical
    u_disk_status:     '2',  // Warning
    u_overall_status:  '3'   // Critical
  },
  {
    short_description: 'Monthly health check - App Server 01',
    u_check_date:      gs.nowDateTime(),
    u_checked_by:      getUserSysId('amit.verma'),
    u_cpu_status:      '1',  // Normal
    u_memory_status:   '1',  // Normal
    u_disk_status:     '1',  // Normal
    u_overall_status:  '1'   // Healthy
  }
];

for (var t = 0; t < testRecords.length; t++) {
  var rec = testRecords[t];
  // Check if record already exists
  var rCheck = new GlideRecord('u_server_health_check');
  rCheck.addQuery('short_description', rec.short_description);
  rCheck.query();
  if (rCheck.next()) {
    gs.info('  Record already exists: ' + rec.short_description);
    continue;
  }
  var rGr = new GlideRecord('u_server_health_check');
  rGr.initialize();
  rGr.short_description = rec.short_description;
  rGr.u_check_date      = rec.u_check_date;
  rGr.u_checked_by      = rec.u_checked_by;
  rGr.u_cpu_status      = rec.u_cpu_status;
  rGr.u_memory_status   = rec.u_memory_status;
  rGr.u_disk_status     = rec.u_disk_status;
  rGr.u_overall_status  = rec.u_overall_status;
  rGr.insert();
  gs.info('  Created record: ' + rec.short_description);
}

// ============================================================
// PART C: Application Deployment Table (Exercise 2)
// ============================================================

gs.info('--- Creating Application Deployment table ---');
createTable('Application Deployment', 'u_application_deployment', 'task');

// Add custom columns
addColumn('u_application_deployment', 'Application Name',   'u_application_name',   'string',         null,       true);
addColumn('u_application_deployment', 'Environment',        'u_environment',        'choice',         null,       false);
addColumn('u_application_deployment', 'Version',            'u_version',            'string',         null,       false);
addColumn('u_application_deployment', 'Deployed By',        'u_deployed_by',        'reference',      'sys_user', false);
addColumn('u_application_deployment', 'Deployment Date',    'u_deployment_date',    'glide_date_time', null,      false);
addColumn('u_application_deployment', 'Deployment Status',  'u_deployment_status',  'choice',         null,       false);
addColumn('u_application_deployment', 'Rollback Plan',      'u_rollback_plan',      'string',         null,       false);

// Add choices for Environment
addChoice('u_application_deployment', 'u_environment', '1', 'Dev',        100);
addChoice('u_application_deployment', 'u_environment', '2', 'Staging',    200);
addChoice('u_application_deployment', 'u_environment', '3', 'Production', 300);

// Add choices for Deployment Status
addChoice('u_application_deployment', 'u_deployment_status', '1', 'Planned',     100);
addChoice('u_application_deployment', 'u_deployment_status', '2', 'In Progress', 200);
addChoice('u_application_deployment', 'u_deployment_status', '3', 'Completed',   300);
addChoice('u_application_deployment', 'u_deployment_status', '4', 'Failed',      400);
addChoice('u_application_deployment', 'u_deployment_status', '5', 'Rolled Back', 500);

gs.info('=== Lab 05 setup complete! ===');
```

> **Note:** This script is idempotent -- you can run it multiple times safely. After running, you still need to do **Part 4 (Form Layout)** manually through the UI, as form layout configuration requires the Form Designer. Also explore **Parts 1-2** manually to understand table inheritance and field types -- those are learning exercises, not setup tasks.
