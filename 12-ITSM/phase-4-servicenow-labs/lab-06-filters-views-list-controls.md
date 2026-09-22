# Lab 06: Filters, Views & List Controls

**Level:** Beginner | **Duration:** 45 minutes | **Prerequisites:** Lab 01-05 completed

---

## Objective

By the end of this lab, you will:
- Build complex filters using the condition builder
- Save and share filters
- Create custom list views for different purposes
- Use advanced list controls (export, print, visual task boards)
- Understand encoded queries for URL-based filtering

---

## Part 1: Advanced Filtering

### Step 1.1: The Condition Builder

1. Navigate to **Incident > All**
2. Click the **funnel icon** or **Show Filter** to open the condition builder
3. The condition builder looks like:
   ```
   [Field ▼] [Operator ▼] [Value ▼]     [AND ▼] [Run] [Save]
   ```

### Step 1.2: Build a Simple Filter

1. Set: **Priority** | **is** | **1 - Critical**
2. Click **Run**
3. Only P1 incidents appear
4. Note the breadcrumb: `Priority = 1 - Critical`

### Step 1.3: Add Multiple Conditions (AND)

1. Open the filter builder
2. Click **AND** to add another condition row:
   ```
   Priority is 1 - Critical
   AND State is not Resolved
   AND State is not Closed
   ```
3. Click **Run**
4. Only open/active P1 incidents appear

### Step 1.4: Use OR Conditions

1. Clear the filter
2. Build this filter:
   ```
   Priority is 1 - Critical
   OR Priority is 2 - High
   ```
3. To add an OR: click the **AND** dropdown next to a condition row and change it to **OR**
4. Click **Run** -- shows P1 and P2 incidents

### Step 1.5: Nested Conditions (AND/OR Groups)

For complex logic, you can create groups:

```
Goal: Show all P1 incidents that are open, OR all P2 incidents assigned to Service Desk

( Priority is 1 - Critical AND State is Open )
OR
( Priority is 2 - High AND Assignment group is Service Desk )
```

1. In the condition builder, look for the option to add a **group** or **nested condition**
2. Click the arrow next to AND/OR to create groupings
3. Build the above condition
4. Click **Run**

### Step 1.6: Common Filter Operators

| Operator | Use Case | Example |
|---|---|---|
| **is** | Exact match | `state is Open` |
| **is not** | Exclusion | `state is not Closed` |
| **contains** | Partial text | `short_description contains network` |
| **does not contain** | Text exclusion | `short_description does not contain test` |
| **starts with** | Prefix match | `number starts with INC001` |
| **is empty** | No value set | `assigned_to is empty` (unassigned) |
| **is not empty** | Has a value | `assignment_group is not empty` |
| **is one of** | Multiple values | `priority is one of 1,2` |
| **less than** | Comparison | `priority less than 3` |
| **on** | Specific date | `opened_at on 2026-09-15` |
| **before** | Before date | `opened_at before 2026-09-01` |
| **after** | After date | `opened_at after 2026-09-01` |
| **between** | Date range | `opened_at between 2026-09-01 and 2026-09-22` |
| **relative** | Dynamic date | `opened_at on Last 7 days` |

### Step 1.7: Relative Date Filters

Relative dates are dynamic -- they adjust based on today's date:

1. In the condition builder:
   - Field: **Opened**
   - Operator: **on**
   - Value: Click the dropdown and select **Last 7 days**
2. Click **Run**
3. This filter always shows incidents from the last 7 days, regardless of when you run it

Other relative options:
- Today
- Yesterday
- Last 7 days / Last 30 days / Last 90 days
- This week / This month / This quarter / This year
- Last week / Last month / Last quarter

---

## Part 2: Saving and Sharing Filters

### Step 2.1: Save a Personal Filter

1. Build a filter: **Priority is 1 - Critical AND State is not Closed**
2. Click **Save** in the filter area
3. Name: `My Open P1 Incidents`
4. Click **Save**
5. This filter appears under your personal filters

### Step 2.2: Access Saved Filters

1. On the Incident list, look for a **filter dropdown** or **My Filters** section
2. Click on `My Open P1 Incidents`
3. The filter is applied instantly

### Step 2.3: Create a Module from a Filter

You can create a navigator module that opens a pre-filtered list:

1. Navigate to **System Definition > Application Menus** (or `sys_app_module.list`)
2. Click **New**
3. Fill in:
   | Field | Value |
   |---|---|
   | Title | Open P1 Incidents |
   | Application menu | Incident |
   | Order | 200 |
   | Filter | Priority = 1 AND State != Closed |
   | Table | incident |
4. Click **Submit**
5. Check the Application Navigator -- under Incident, you should see "Open P1 Incidents"

---

## Part 3: Custom List Views

### Step 3.1: What Are Views?

A **view** is a saved configuration of which columns appear in a list. Different views show different columns for different purposes.

```
Same table (incident), different views:

Default View:        Number | Short desc | Priority | State | Assigned to
Manager View:        Number | Short desc | Priority | SLA status | Assignment group | Age
SLA Tracking View:   Number | Priority | SLA due | Has breached | Time left
Security View:       Number | Short desc | Category | Caller | CI | State
```

### Step 3.2: Create a Custom View

1. Navigate to **Incident > All**
2. Right-click any column header
3. Select **Configure > List Layout**
4. At the top of the dialog, you'll see a **View** dropdown
5. Type a new view name: `manager_view`
6. Configure the columns for this view:
   - Number
   - Short description
   - Priority
   - State
   - Assignment group
   - Assigned to
   - Opened
   - Category
7. Click **Save**

### Step 3.3: Switch Between Views

1. On the Incident list, look for a **View** selector (might be in the list menu ≡)
2. Or append to the URL: `?sysparm_view=manager_view`
3. Type in Filter Navigator: `incident.list?sysparm_view=manager_view`
4. The list now shows your custom column layout

### Step 3.4: Create an SLA Tracking View

1. On the Incident list, go to **Configure > List Layout**
2. Create a new view: `sla_view`
3. Select columns:
   - Number
   - Short description
   - Priority
   - State
   - Made SLA (if available)
   - Reassignment count
   - Assigned to
   - Assignment group
4. Click **Save**

---

## Part 4: List Controls

### Step 4.1: List Context Menu

1. On the Incident list, right-click on any **record row**
2. You'll see a context menu:
   ```
   Open
   Open in new tab
   Copy sys_id
   Copy URL
   Assign to me
   Show matching
   Filter out
   Add to Visual Task Board
   ```

3. Try **Copy URL** -- this copies a direct link to that specific record

### Step 4.2: Export List Data

1. On the Incident list, click the **list menu** (≡) or look for an Export option
2. Select **Export**
3. Choose a format:
   | Format | Use Case |
   |---|---|
   | **CSV** | Open in Excel, import into other tools |
   | **Excel** | Formatted spreadsheet |
   | **PDF** | Printable report |
   | **XML** | System integrations |
4. Select **CSV** and download the file
5. Open it in a text editor or spreadsheet -- verify the data matches the list

### Step 4.3: List Calculations

1. On the Incident list, right-click on the **Priority** column header
2. Select **Show Column Totals** or **Bar Chart** (options vary by version)
3. If available, you can see:
   - Count of records per priority
   - Sum, average, or count for numeric fields
4. Some columns support inline charts/bars showing distribution

### Step 4.4: Visual Task Board

1. On the Incident list, click the **list menu** (≡)
2. Select **Visual Task Board** (or look for a kanban icon)
3. A kanban-style board appears:
   ```
   | New         | In Progress  | On Hold      | Resolved     |
   |-------------|-------------|-------------|-------------|
   | INC0001    | INC0002     |             | INC0005     |
   | INC0003    | INC0004     |             | INC0008     |
   | INC0006    |             |             |             |
   ```
4. You can drag cards between columns to change the state
5. This is a visual way to manage work items

---

## Part 5: Encoded Queries

### Step 5.1: What Are Encoded Queries?

Behind every filter, ServiceNow generates an **encoded query** -- a string representation of the filter conditions.

```
Filter:              Priority is 1 - Critical AND State is Open
Encoded query:       priority=1^state=1
URL:                 incident.list?sysparm_query=priority=1^state=1
```

### Step 5.2: Find the Encoded Query

1. Build any filter on the Incident list
2. Right-click the **breadcrumb** (the filter summary at the top)
3. Select **Copy query** or **Copy encoded query**
4. Paste it in a text editor -- you'll see something like:
   ```
   priority=1^stateNOT IN6,7,8^assignment_group=<sys_id>
   ```

### Step 5.3: Encoded Query Syntax

| Condition | Encoded Query |
|---|---|
| Priority is 1 | `priority=1` |
| State is not Closed | `state!=7` |
| AND | `^` |
| OR | `^OR` |
| Short desc contains email | `short_descriptionLIKEemail` |
| Assigned to is empty | `assigned_toISEMPTY` |
| Opened in last 7 days | `opened_atRELATIVEGE@dayofweek@ago@7` |
| Priority in (1,2) | `priorityIN1,2` |
| Order by priority | `^ORDERBYpriority` |
| Order by descending | `^ORDERBYDESCpriority` |

### Step 5.4: Use Encoded Queries in URLs

1. In your browser, navigate to:
   ```
   https://devXXXXXX.service-now.com/nav_to.do?uri=incident.list?sysparm_query=priority=1^state!=7
   ```
2. This opens the incident list pre-filtered to "P1, not closed"
3. Bookmark this URL for quick access

### Step 5.5: Practice Encoded Queries

Build these filters using the condition builder, then copy the encoded query:

1. All P1 and P2 incidents that are open:
   - Expected: `priorityIN1,2^state=1`

2. Incidents assigned to Service Desk, opened in the last 30 days:
   - Build it, copy the encoded query, verify it works in a URL

3. Unassigned incidents (assigned_to is empty) ordered by priority:
   - Expected: `assigned_toISEMPTY^ORDERBYpriority`

---

## Part 6: Practice Exercises

### Exercise 1: Filter Challenge

Build and save these filters on the Incident list:

1. **"Unassigned Critical"**: Priority = 1 AND Assigned to is empty
2. **"My Team's Work"**: Assignment group = Platform Engineering AND State is not Closed
3. **"Aging Incidents"**: State = In Progress AND Opened before 30 days ago
4. **"Recent P1/P2"**: Priority in (1,2) AND Opened in Last 7 days

### Exercise 2: View Challenge

Create these custom views for the Incident list:

1. **Executive View**: Number, Short description, Priority, State, SLA, Assignment group
2. **Technician View**: Number, Short description, Category, Subcategory, CI, Work notes

### Exercise 3: Export and Analyze

1. Filter incidents to show only P1 and P2
2. Export to CSV
3. Open in a spreadsheet
4. Count: How many P1 vs P2? How many per assignment group?

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Built complex filters | Find exactly the records you need |
| Saved and shared filters | Reusable queries for daily work |
| Created custom views | Different views for different roles |
| Used list controls | Export, kanban boards, calculations |
| Learned encoded queries | URL-based filtering, API queries, automation |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Condition Builder** | Visual tool to build filter conditions |
| **Encoded Query** | String representation of a filter (e.g., `priority=1^state=1`) |
| **View** | A saved list column configuration |
| **Breadcrumb** | Visual display of active filter, clickable to modify |
| **Relative Dates** | Dynamic date filters (e.g., "Last 7 days") |
| **Visual Task Board** | Kanban-style board for managing work items |
| **List Export** | Download list data as CSV, Excel, PDF, or XML |

---

## What's Next

Congratulations -- you've completed the **Beginner** labs! You now have a solid foundation in ServiceNow navigation, administration, and data management.

In **Lab 07**, you begin the **Intermediate** labs, starting with **Incident Management** -- you'll create, manage, escalate, and resolve incidents through the full lifecycle.
