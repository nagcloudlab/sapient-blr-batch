# Lab 03: Lists and Forms

**Level:** Beginner | **Duration:** 60 minutes | **Prerequisites:** Lab 01-02 completed

---

## Objective

By the end of this lab, you will:
- Navigate and customize list views (columns, sorting, grouping)
- Understand form layout, sections, and field types
- Use the Activity Stream and work notes
- Personalize list and form views
- Perform list editing (inline and bulk)

---

## Part 1: Working with Lists

### Step 1.1: Open an Incident List

1. Log in to your PDI
2. Navigate to **Incident > All** (type `incident` in Filter Navigator)
3. You should see a list of demo incidents

### Step 1.2: Understand List Anatomy

```
+------------------------------------------------------------------+
| Incidents                                            [≡ List Menu] |
+------------------------------------------------------------------+
| Breadcrumb:  Incident > All                                        |
+------------------------------------------------------------------+
| [Search] [New] [Show/Hide Filter]                                  |
+------+----------+-----+-----------+--------+--------+------+------+
| ☐    | Number   | ▼   | Short desc| Priority|State  |Assign|Opened|
+------+----------+-----+-----------+--------+--------+------+------+
| ☐    | INC00001 |     | Can't ... | 1-Crit | Open   | Abel | Sep 1|
| ☐    | INC00002 |     | Email ... | 2-High | In Prog| Beth | Sep 2|
| ☐    | INC00003 |     | Slow ... | 3-Med  | Open   | Abel | Sep 3|
+------+----------+-----+-----------+--------+--------+------+------+
| Records 1-20 of 156                       [< Prev] [Next >]       |
+------------------------------------------------------------------+
```

**Key Elements:**
| Element | Location | Purpose |
|---|---|---|
| Column headers | Top of list | Click to sort, right-click for options |
| Checkboxes | Left column | Select records for bulk actions |
| Record links | Number column | Click to open the full record |
| Pagination | Bottom | Navigate through pages of records |
| List menu (≡) | Top-right | List configuration options |

### Step 1.3: Sort Records

1. Click the **Number** column header -- records sort ascending (▲)
2. Click again -- records sort descending (▼)
3. Click the **Priority** column header to sort by priority
4. **Multi-sort:** Hold **Shift** and click another column to add a secondary sort

### Step 1.4: Configure List Columns

1. Right-click any column header (e.g., "Number")
2. Select **Configure > List Layout** (or go to the List menu ≡ > List Layout)
3. You'll see a column configuration dialog:
   ```
   Available columns (left):        Selected columns (right):
   +---------------------+          +---------------------+
   | Actual end          |          | Number              |
   | Active              |          | Short description   |
   | Activity due        |          | Priority            |
   | Assigned to         |          | State               |
   | Assignment group    |   >>     | Assigned to         |
   | Business service    |   <<     | Opened              |
   | ...                 |          | ...                 |
   +---------------------+          +---------------------+
   ```
4. Add **Assignment group** to the Selected list (select it, click >>)
5. Add **Category** to the Selected list
6. Remove **Opened** (select it, click <<)
7. Reorder: select a column and use **Up/Down** arrows
8. Click **Save**
9. The list now shows your customized columns

### Step 1.5: Group By

1. Right-click the **Priority** column header
2. Select **Group By** Priority
3. The list now groups incidents by priority level:
   ```
   ▼ Priority: 1 - Critical (3 records)
     INC00001  Can't access email...
     INC00045  Server down...
     ...
   ▼ Priority: 2 - High (8 records)
     INC00002  Slow network...
     ...
   ▼ Priority: 3 - Moderate (15 records)
     ...
   ```
4. Click the **group header** to collapse/expand each group
5. To remove grouping: right-click any column > **Group By > None**

### Step 1.6: List Search

1. At the top of the list, find the **Search** bar
2. Click the dropdown next to the search box -- you can search by specific field:
   - Number
   - Short description
   - Assigned to
   - etc.
3. Select **Short description** and type: `email`
4. Press **Enter** -- the list filters to incidents containing "email" in the description
5. Click the **X** to clear the search

---

## Part 2: Filters and Breadcrumbs

### Step 2.1: Show the Condition Builder

1. On the Incident list, click the **funnel icon** (Show/Hide Filter) or look for the filter area above the list
2. The condition builder appears:
   ```
   [Priority] [is] [1 - Critical]     [AND]
   ```
3. Set the condition: **Priority is 1 - Critical**
4. Click **Run** -- the list shows only P1 incidents

### Step 2.2: Build Complex Filters

1. Open the filter builder
2. Add conditions:
   ```
   Priority is 1 - Critical
   AND State is Open
   AND Assignment group is Service Desk
   ```
3. Click **Run**
4. Notice the **breadcrumb** at the top updates to show your active filter:
   ```
   Incident > Priority = 1 - Critical ^ State = Open ^ Assignment group = Service Desk
   ```
5. You can click individual breadcrumb items to remove that filter condition

### Step 2.3: Save a Filter

1. Build a filter: **Priority is 1 - Critical AND State is not Closed**
2. Click **Save** (in the filter area)
3. Name it: `My P1 Open Incidents`
4. Click **Save**
5. This filter now appears in the left navigator under **Incident > My Filters** or as a saved filter
6. You can access it anytime without rebuilding

### Step 2.4: Filter Operators

| Operator | Usage | Example |
|---|---|---|
| **is** | Exact match | Priority is 1 - Critical |
| **is not** | Exclude | State is not Closed |
| **contains** | Partial text match | Short description contains "email" |
| **starts with** | Text prefix | Number starts with "INC001" |
| **is empty** | Field has no value | Assigned to is empty |
| **is not empty** | Field has a value | Assignment group is not empty |
| **less than** | Numeric/date comparison | Priority less than 3 |
| **between** | Date range | Opened between "2026-09-01" and "2026-09-22" |
| **in** | Multiple values | Priority in 1 - Critical, 2 - High |

---

## Part 3: Working with Forms

### Step 3.1: Open a Record

1. Navigate to **Incident > All**
2. Click on any incident number (e.g., **INC0000001**)
3. The form opens showing all fields for that record

### Step 3.2: Understand Form Layout

```
+------------------------------------------------------------------+
| INC0000001                                                         |
+------------------------------------------------------------------+
| [Save] [Update] [Insert] [Insert and Stay]  | [Attachments] [📋] |
+------------------------------------------------------------------+
|                                                                    |
| Number:          INC0000001         State:      [Open ▼]          |
| Caller:          [Abel Tuter  🔍]   Priority:   [1-Critical ▼]   |
| Category:        [Software ▼]      Subcategory: [Email ▼]        |
| Assignment Group:[Service Desk 🔍]  Assigned to: [Beth Anglin 🔍] |
|                                                                    |
| Short description: [Can't access email from mobile device       ] |
|                                                                    |
| +--- Description ---+                                              |
| | User reports that email on iPhone has stopped syncing.          |
| | Started after the latest iOS update. Tried restarting.          |
| +-------------------+                                              |
|                                                                    |
| +--- Tabs: Notes | Related Records | Resolution | Closure ---+   |
| |                                                               |  |
| | Activity Stream:                                              |  |
| | [Work notes] [Additional comments] [Activities filter]        |  |
| |                                                               |  |
| | Sep 3  Beth Anglin (work note):                               |  |
| |   "Checked Exchange server. User profile looks clean."        |  |
| |                                                               |  |
| | Sep 2  Abel Tuter (comment):                                  |  |
| |   "Still can't access email. Please help."                    |  |
| +---------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

### Step 3.3: Field Types on Forms

| Field Type | Visual Indicator | Example |
|---|---|---|
| **String** | Plain text box | Short description |
| **Choice/Dropdown** | Dropdown arrow (▼) | Priority, State, Category |
| **Reference** | Magnifying glass (🔍) | Caller, Assigned to, Assignment group |
| **Date/Time** | Calendar icon (📅) | Opened, Resolved |
| **Journal** | Multi-line text in Activity | Work notes, Additional comments |
| **Boolean** | Checkbox | Knowledge, Active |
| **Integer** | Number input | Severity, Impact, Urgency |
| **HTML** | Rich text editor | Description (sometimes) |

### Step 3.4: Edit a Record

1. Open incident **INC0000001** (or any incident)
2. Change the **State** dropdown to **In Progress**
3. In the **Work notes** field (under Notes tab), type:
   ```
   Lab exercise: investigating the reported issue.
   ```
4. Click **Update** (top-left or bottom of form)
5. The record saves and you return to the list
6. Open the incident again -- verify your changes are saved

### Step 3.5: Activity Stream

The Activity Stream shows the chronological history of all changes to a record.

1. Open any incident
2. Scroll down to the **Activity** section (or click the **Notes** tab)
3. You'll see:
   - **Work notes** (internal, visible only to IT staff) -- yellow background
   - **Additional comments** (visible to the caller/customer) -- white background
   - **Field changes** (automatic entries when fields are modified)
4. Add a **Work note**: type "Testing activity stream" and click **Update**
5. Reopen the incident -- your work note appears in the activity stream

### Step 3.6: Form Context Menu (Right-Click)

1. Open any incident form
2. Right-click on the **form header** (the gray bar with the record number)
3. You'll see options like:
   - **Save** -- save without leaving
   - **Insert** -- create a copy as a new record
   - **Copy sys_id** -- copy the unique record ID
   - **Show XML** -- view the record as XML
   - **Reload form** -- refresh
4. Right-click on any **field label** (e.g., "Priority"):
   - **Show - Priority** -- shows the field's technical name, type, and value
   - **Configure Dictionary** -- edit the field definition (admin)
   - **Configure Label** -- change the display label
5. Try right-clicking on the "Priority" label and selecting **Show - Priority** to see its internal name: `priority`

---

## Part 4: Form Sections and Related Lists

### Step 4.1: Form Sections

Forms are organized into sections (tabs at the bottom or collapsible sections):

1. Open any incident
2. Look for tabs or sections:
   - **Notes** -- work notes, additional comments, activity stream
   - **Related Records** -- related problems, changes, child incidents
   - **Resolution Information** -- resolution code, resolution notes
   - **Closure Information** -- close code, close notes

### Step 4.2: Related Lists

Below the form, you'll see **Related Lists** -- lists of records related to this incident:

```
+-- Related Lists ------------------------------------------+
|                                                            |
| ▼ Child Incidents (0)                                      |
|   (no records)                                             |
|                                                            |
| ▼ Problem (0)                                              |
|   (no records)                                             |
|                                                            |
| ▼ Change Requests (0)                                      |
|   (no records)                                             |
|                                                            |
| ▼ Tasks (SLA) (1)                                          |
|   TASK0000001 | P1 Resolution SLA | In Progress           |
+------------------------------------------------------------+
```

### Step 4.3: Customize Related Lists

1. Right-click on the form header
2. Select **Configure > Related Lists**
3. Add or remove related lists:
   - Add: **Approvals**
   - Add: **Attachments**
   - Remove any you don't need
4. Click **Save**

---

## Part 5: List Editing

### Step 5.1: Inline List Editing

1. Navigate to **Incident > All**
2. **Double-click** on any cell in the list (e.g., the "State" cell of an incident)
3. The cell becomes editable -- you can change the value
4. Press **Enter** or click away to save
5. A green check appears briefly to confirm the save

### Step 5.2: Bulk Update (Multiple Records)

1. On the Incident list, check the **checkboxes** next to 3-4 incidents
2. At the bottom of the list (or in a dropdown), you'll see actions:
   ```
   Actions on selected rows:
   [Delete] [Update Selected] [Add to Update Set]
   ```
3. Click **Update Selected** (or right-click > Update Selected)
4. A form appears where you can change fields for ALL selected records:
   - Change **Assignment group** to "Hardware"
   - Add a work note: "Bulk reassignment for lab exercise"
5. Click **Update**
6. All selected incidents are updated simultaneously

**Warning:** Be careful with bulk updates in production -- there's no undo!

---

## Part 6: Practice Exercises

### Exercise 1: List Customization

1. Open the Incident list
2. Add these columns: Number, Short description, Priority, State, Category, Assignment group, Assigned to, Opened
3. Sort by Priority (ascending), then by Opened (descending)
4. Group by Assignment group
5. Save a filter: "Open High Priority" = Priority in (1-Critical, 2-High) AND State is not Resolved AND State is not Closed

### Exercise 2: Form Navigation

1. Open incident INC0000001
2. Find the following information:
   - Who is the Caller? → ___________
   - What is the Priority? → ___________
   - Who is it Assigned to? → ___________
   - What is the Short description? → ___________
3. Right-click on the "Assigned to" label -- what is the field's internal name? → ___________
4. Check the Activity Stream -- how many work notes exist? → ___________

### Exercise 3: Edit and Track

1. Open any incident
2. Change the **Category** to "Hardware"
3. Add a work note: "Category changed to Hardware for lab exercise"
4. Click **Update**
5. Reopen the incident
6. In the Activity Stream, verify both changes appear (field change + work note)
7. Right-click the form header > **Show XML** -- observe the XML structure

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Customized list columns | See the data that matters for your role |
| Built and saved filters | Quickly access specific record sets |
| Explored form layout | Understand how data is entered and displayed |
| Used the Activity Stream | Track all changes and communication |
| Performed inline and bulk edits | Efficient data management |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **List View** | Tabular view showing multiple records from a table |
| **Form View** | Detailed view of a single record with all its fields |
| **Condition Builder** | Visual filter tool to build query conditions |
| **Breadcrumb** | Shows active filter conditions, clickable to modify |
| **Activity Stream** | Chronological log of all changes and notes on a record |
| **Work Notes** | Internal notes visible only to IT staff (yellow) |
| **Additional Comments** | Customer-visible notes (white) |
| **Related Lists** | Lists of records linked to the current record |
| **Inline Editing** | Double-click a cell in list view to edit directly |

---

## What's Next

In **Lab 04**, you'll create users, groups, and roles -- the foundation of access control in ServiceNow.
