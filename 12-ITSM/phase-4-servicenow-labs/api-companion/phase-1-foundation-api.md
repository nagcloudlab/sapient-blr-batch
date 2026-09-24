# Phase 1: Platform Foundation — API Companion

> Every UI action from Labs 01-06, replicated via ServiceNow REST API.
> Set your credentials below, then run any section.
> Each command includes the UI equivalent so you can map between browser and terminal.

---

## Setup

Set these once per terminal session. Every command below references them.

```bash
export SNOW="https://YOUR-INSTANCE.service-now.com"
export AUTH="admin:YOUR-PASSWORD"
```

Quick helper — pipe any curl output through this for readable JSON:

```bash
alias snjq="python3 -m json.tool"
```

---

## Lab 01 — PDI Setup: Verify Connectivity

> **UI equivalent:** Log in to your PDI, confirm the dashboard loads, check the instance version under System Diagnostics.

### Test API access

```bash
# Equivalent to: successfully loading the ServiceNow login page and seeing the dashboard
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_properties?sysparm_limit=1" | python3 -m json.tool
```

Expected: a JSON object with a `result` array containing one system property. If you get a 401, check your credentials. If you get a connection error, check your instance URL.

### Check instance version

```bash
# Equivalent to: System Diagnostics > Stats > Build tag
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_properties?sysparm_query=name=glide.buildtag&sysparm_fields=value" \
  | python3 -m json.tool
```

Expected: the build tag string (e.g., `glide-vancouver-07-08-2023` or similar).

### Confirm ITSM plugins are active

```bash
# Equivalent to: System Definition > Plugins, then searching for "ITSM"
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/v_plugin?sysparm_query=idLIKEitsm^state=active&sysparm_fields=id,name,state&sysparm_limit=10" \
  | python3 -m json.tool
```

### Verify your user account details

```bash
# Equivalent to: clicking your avatar > Profile
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_user?sysparm_query=user_name=admin&sysparm_fields=user_name,name,email,roles&sysparm_display_value=true" \
  | python3 -m json.tool
```

### Check instance stats (node, memory, sessions)

```bash
# Equivalent to: System Diagnostics > Stats
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_properties?sysparm_query=nameLIKEglide.servlet^ORnameLIKEglide.db&sysparm_fields=name,value&sysparm_limit=10" \
  | python3 -m json.tool
```

---

## Lab 02 — Platform Navigation: Explore Modules

> **UI equivalent:** Using the Filter Navigator (left sidebar) to find and open application menus and modules.

### List all application menus

```bash
# Equivalent to: looking at the top-level entries in the left-hand Application Navigator
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_app_application?sysparm_fields=title,sys_id&sysparm_limit=20&sysparm_query=ORDERBYtitle" \
  | python3 -m json.tool
```

### List modules under the Incident application

```bash
# Equivalent to: expanding "Incident" in the left navigator
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_app_module?sysparm_query=applicationLIKEIncident&sysparm_fields=title,uri,order&sysparm_limit=10&sysparm_query=ORDERBYorder" \
  | python3 -m json.tool
```

### Search for a module by name (like Filter Navigator search)

```bash
# Equivalent to: typing "Create New" in the Filter Navigator
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_app_module?sysparm_query=titleLIKECreate New&sysparm_fields=title,uri,application&sysparm_display_value=true" \
  | python3 -m json.tool
```

### List modules under Problem, Change, and Knowledge

```bash
# Equivalent to: expanding Problem, Change, and Knowledge Base menus
for app in "Problem" "Change" "Knowledge"; do
  echo "=== $app ==="
  curl -s -u "$AUTH" -H "Accept:application/json" \
    "$SNOW/api/now/table/sys_app_module?sysparm_query=applicationLIKE${app}&sysparm_fields=title,uri&sysparm_limit=8" \
    | python3 -c "import sys,json; [print(f\"  {m['title']:30s} {m.get('uri','')}\" ) for m in json.load(sys.stdin)['result']]"
done
```

### List CMDB-related modules

```bash
# Equivalent to: typing "CMDB" in the Filter Navigator
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_app_module?sysparm_query=titleLIKECMDB&sysparm_fields=title,uri&sysparm_limit=10" \
  | python3 -m json.tool
```

### Check favorites (bookmarked modules)

```bash
# Equivalent to: viewing the star/favorites list in the navigator
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_ui_bookmark?sysparm_fields=title,url&sysparm_limit=10&sysparm_display_value=true" \
  | python3 -m json.tool
```

---

## Lab 03 — Lists & Forms: Read Data

> **UI equivalent:** Opening list views (incident.list), clicking into a record (form view), and personalizing columns.

### List view: first 10 incidents

```bash
# Equivalent to: navigating to Incident > All, seeing the default list
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_limit=10&sysparm_fields=number,short_description,priority,state,assigned_to&sysparm_display_value=true" \
  | python3 -m json.tool
```

### Form view: open a single incident

```bash
# Equivalent to: clicking on incident INC0000001 to open its form
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=number=INC0000001&sysparm_display_value=true" \
  | python3 -m json.tool
```

### Get form layout / field list for the incident table

```bash
# Equivalent to: right-clicking the form header > Configure > Form Layout
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_dictionary?sysparm_query=name=incident^internal_type!=collection&sysparm_fields=element,column_label,internal_type&sysparm_limit=50" \
  | python3 -m json.tool
```

### Personalize list columns

```bash
# Equivalent to: right-clicking the list header > Personalize List Columns
# Here we select only the columns we want to see
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_fields=number,short_description,priority,state,category,assignment_group&sysparm_display_value=true&sysparm_limit=5" \
  | python3 -m json.tool
```

### Read related records (activity / work notes)

```bash
# Equivalent to: scrolling down on the incident form to the Activity section
# Get journal entries (work notes and comments) for a specific incident
INC_SYS_ID=$(curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=number=INC0000001&sysparm_fields=sys_id" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_journal_field?sysparm_query=element_id=$INC_SYS_ID&sysparm_fields=element,value,sys_created_on,sys_created_by&sysparm_limit=5&sysparm_display_value=true" \
  | python3 -m json.tool
```

### View related lists (like the Related Lists tab on a form)

```bash
# Equivalent to: viewing the "Child Incidents" or "Tasks" related list
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=parent_incident.number=INC0000001&sysparm_fields=number,short_description,state&sysparm_display_value=true" \
  | python3 -m json.tool
```

### Get a record count (like the row count in a list footer)

```bash
# Equivalent to: seeing "Rows 1-20 of 152" at the bottom of the list
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/stats/incident?sysparm_count=true" \
  | python3 -m json.tool
```

---

## Lab 04 — Users, Groups & Roles: CRUD Operations

> **UI equivalent:** User Administration > Users/Groups, assigning roles via the Roles related list.

### READ: Look up an existing user

```bash
# Equivalent to: User Administration > Users, searching for "abel.tuter"
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_user?sysparm_query=user_name=abel.tuter&sysparm_fields=user_name,name,email,title,department&sysparm_display_value=true" \
  | python3 -m json.tool
```

### CREATE: Add a new user (Ravi Kumar)

```bash
# Equivalent to: User Administration > Users > New, filling in the form, clicking Submit
curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
  -X POST "$SNOW/api/now/table/sys_user" \
  -d '{
    "user_name": "ravi.kumar",
    "first_name": "Ravi",
    "last_name": "Kumar",
    "email": "ravi.kumar@example.com",
    "title": "Platform Engineer",
    "department": "IT",
    "active": "true"
  }' | python3 -m json.tool
```

Expected: the full user record with a new `sys_id`.

### CREATE: Batch-create all UPI lab users

```bash
# Equivalent to: repeating the New User form six times
for user in \
  '{"user_name":"priya.sharma","first_name":"Priya","last_name":"Sharma","title":"NOC Operator","email":"priya.sharma@example.com"}' \
  '{"user_name":"amit.verma","first_name":"Amit","last_name":"Verma","title":"Junior Engineer","email":"amit.verma@example.com"}' \
  '{"user_name":"meera.joshi","first_name":"Meera","last_name":"Joshi","title":"Service Desk Lead","email":"meera.joshi@example.com"}' \
  '{"user_name":"vijay.admin","first_name":"Vijay","last_name":"Admin","title":"System Administrator","email":"vijay.admin@example.com"}' \
  '{"user_name":"sanjay.mgr","first_name":"Sanjay","last_name":"Manager","title":"VP Engineering","email":"sanjay.mgr@example.com"}'; do
  curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
    -X POST "$SNOW/api/now/table/sys_user" -d "$user" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"Created: {r['user_name']} ({r['sys_id']})\")"
done
```

### CREATE: Add groups

```bash
# Equivalent to: User Administration > Groups > New
curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
  -X POST "$SNOW/api/now/table/sys_user_group" \
  -d '{"name":"UPI Platform Engineering","description":"L2/L3 platform engineering team for UPI services"}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"Group created: {r['name']} ({r['sys_id']})\")"

curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
  -X POST "$SNOW/api/now/table/sys_user_group" \
  -d '{"name":"UPI NOC","description":"Network Operations Center - 24x7 L1 monitoring for UPI"}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"Group created: {r['name']} ({r['sys_id']})\")"

curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
  -X POST "$SNOW/api/now/table/sys_user_group" \
  -d '{"name":"UPI Service Desk","description":"L1 service desk for UPI incident intake and triage"}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"Group created: {r['name']} ({r['sys_id']})\")"
```

### ADD user to group

```bash
# Equivalent to: opening a group > Group Members related list > Edit > adding a user

# Step 1: Get sys_ids for the user and group
RAVI_ID=$(curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_user?sysparm_query=user_name=ravi.kumar&sysparm_fields=sys_id" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")
echo "Ravi sys_id: $RAVI_ID"

PLAT_ID=$(curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_user_group?sysparm_query=name=UPI Platform Engineering&sysparm_fields=sys_id" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")
echo "Platform Engineering group sys_id: $PLAT_ID"

# Step 2: Create the membership record
curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
  -X POST "$SNOW/api/now/table/sys_user_grmember" \
  -d "{\"user\":\"$RAVI_ID\",\"group\":\"$PLAT_ID\"}" \
  | python3 -m json.tool
```

### ADD multiple users to groups (batch)

```bash
# Add Priya to NOC, Meera to Service Desk, Amit to Platform Engineering
declare -A USER_GROUP_MAP=(
  ["priya.sharma"]="UPI NOC"
  ["meera.joshi"]="UPI Service Desk"
  ["amit.verma"]="UPI Platform Engineering"
)

for uname in "${!USER_GROUP_MAP[@]}"; do
  gname="${USER_GROUP_MAP[$uname]}"
  UID_VAL=$(curl -s -u "$AUTH" -H "Accept:application/json" \
    "$SNOW/api/now/table/sys_user?sysparm_query=user_name=$uname&sysparm_fields=sys_id" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")
  GID_VAL=$(curl -s -u "$AUTH" -H "Accept:application/json" \
    "$SNOW/api/now/table/sys_user_group?sysparm_query=name=$gname&sysparm_fields=sys_id" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")
  curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
    -X POST "$SNOW/api/now/table/sys_user_grmember" \
    -d "{\"user\":\"$UID_VAL\",\"group\":\"$GID_VAL\"}" \
    | python3 -c "import sys,json; print(f'Added {\"$uname\"} to {\"$gname\"}')"
done
```

### ASSIGN role to a user

```bash
# Equivalent to: opening a user record > Roles related list > Edit > adding "itil"

# Get the itil role sys_id
ITIL_ROLE=$(curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_user_role?sysparm_query=name=itil&sysparm_fields=sys_id" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

# Assign itil role to Ravi
curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
  -X POST "$SNOW/api/now/table/sys_user_has_role" \
  -d "{\"user\":\"$RAVI_ID\",\"role\":\"$ITIL_ROLE\"}" \
  | python3 -m json.tool
```

### ASSIGN role to a group (all members inherit it)

```bash
# Equivalent to: opening a group > Roles related list > Edit > adding "itil"
curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
  -X POST "$SNOW/api/now/table/sys_group_has_role" \
  -d "{\"group\":\"$PLAT_ID\",\"role\":\"$ITIL_ROLE\"}" \
  | python3 -m json.tool
```

### UPDATE: Modify a user record

```bash
# Equivalent to: opening the user form, changing the title field, clicking Update
curl -s -u "$AUTH" -H "Content-Type:application/json" -H "Accept:application/json" \
  -X PATCH "$SNOW/api/now/table/sys_user/$RAVI_ID" \
  -d '{"title":"Senior Platform Engineer"}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"Updated: {r['user_name']} — title is now {r['title']}\")"
```

### VERIFY: List all lab users with details

```bash
# Equivalent to: creating a filtered list view of our custom users
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_user?sysparm_query=user_nameINravi.kumar,priya.sharma,amit.verma,meera.joshi,vijay.admin,sanjay.mgr&sysparm_fields=user_name,name,title,active&sysparm_display_value=true" \
  | python3 -m json.tool
```

### VERIFY: List group memberships

```bash
# Equivalent to: opening each group and checking the Members related list
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_user_grmember?sysparm_query=group.nameLIKEUPI&sysparm_fields=user,group&sysparm_display_value=true" \
  | python3 -m json.tool
```

---

## Lab 05 — Tables & Columns: Explore Schema

> **UI equivalent:** System Definition > Tables, clicking into table records, viewing columns, exploring the schema map.

### List key ITSM tables

```bash
# Equivalent to: System Definition > Tables, filtering for ITSM table names
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_db_object?sysparm_query=nameINincident,problem,change_request,cmdb_ci,kb_knowledge,task,sc_request,sla_definition&sysparm_fields=name,label,super_class&sysparm_display_value=true" \
  | python3 -m json.tool
```

### View table hierarchy (incident extends task)

```bash
# Equivalent to: opening the incident table record and seeing "Extends: Task"
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_db_object?sysparm_query=name=incident&sysparm_fields=name,label,super_class&sysparm_display_value=true" \
  | python3 -m json.tool
```

### List all child tables of Task

```bash
# Equivalent to: opening the Task table > looking at the "Extensions" related list
TASK_ID=$(curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_db_object?sysparm_query=name=task&sysparm_fields=sys_id" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_db_object?sysparm_query=super_class=$TASK_ID&sysparm_fields=name,label&sysparm_limit=20" \
  | python3 -m json.tool
```

### List columns on the incident table

```bash
# Equivalent to: System Definition > Tables > incident > Columns tab
# Shows field name, label, type, length, and whether it is mandatory
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_dictionary?sysparm_query=name=incident^internal_type!=collection&sysparm_fields=element,column_label,internal_type,max_length,mandatory&sysparm_limit=30" \
  | python3 -m json.tool
```

### Search for a specific column across tables

```bash
# Equivalent to: System Definition > Dictionary, searching for "priority"
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_dictionary?sysparm_query=element=priority^nameINincident,problem,change_request&sysparm_fields=name,element,column_label,internal_type" \
  | python3 -m json.tool
```

### Explore CMDB table hierarchy

```bash
# Equivalent to: navigating CMDB > CI Class Manager and viewing the tree
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_db_object?sysparm_query=nameLIKEcmdb_ci&sysparm_fields=name,label,super_class&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### View reference fields on the incident table

```bash
# Equivalent to: checking which fields on the incident form are reference dropdowns
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_dictionary?sysparm_query=name=incident^internal_type=reference&sysparm_fields=element,column_label,reference" \
  | python3 -m json.tool
```

### View choice list values for a field (e.g., incident priority)

```bash
# Equivalent to: right-clicking a choice field > Show Choice List
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_choice?sysparm_query=name=incident^element=priority&sysparm_fields=label,value,sequence&sysparm_orderby=sequence" \
  | python3 -m json.tool
```

### View choice values for incident state

```bash
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_choice?sysparm_query=name=incident^element=state&sysparm_fields=label,value,sequence&sysparm_orderby=sequence" \
  | python3 -m json.tool
```

---

## Lab 06 — Filters, Views & Encoded Queries

> **UI equivalent:** Using the condition builder (funnel icon) on any list, applying dot-walking, breadcrumb filters, and saving personal/global filters.

### Simple filter: Priority = 1 (Critical)

```bash
# Equivalent to: opening Incident list > adding filter "Priority is Critical"
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=priority=1&sysparm_fields=number,short_description,priority&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

### Multiple AND conditions: P1 AND state = New

```bash
# Equivalent to: Priority is Critical AND State is New
# Encoded query uses ^ as the AND separator
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=priority=1^state=1&sysparm_fields=number,short_description,priority,state&sysparm_display_value=true" \
  | python3 -m json.tool
```

### OR condition: P1 OR P2

```bash
# Equivalent to: Priority is Critical OR Priority is High
# Encoded query uses ^OR as the OR separator
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=priority=1^ORpriority=2&sysparm_fields=number,priority&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

### LIKE filter: description contains "UPI"

```bash
# Equivalent to: Short description contains "UPI"
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=short_descriptionLIKEUPI&sysparm_fields=number,short_description&sysparm_limit=10" \
  | python3 -m json.tool
```

### NOT IN filter: exclude P4 and P5

```bash
# Equivalent to: Priority is not 4 - Low AND Priority is not 5 - Planning
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=priorityNOT IN4,5&sysparm_fields=number,priority&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

### EMPTY / NOT EMPTY checks

```bash
# Equivalent to: "Assigned to is empty" — find unassigned incidents
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=assigned_toISEMPTY&sysparm_fields=number,short_description,assigned_to&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool

# Equivalent to: "Assignment group is not empty"
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=assignment_groupISNOTEMPTY&sysparm_fields=number,assignment_group&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

### Date filter: created in the last 7 days

```bash
# Equivalent to: Created on is after 7 days ago (using relative date)
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=sys_created_on>=javascript:gs.daysAgoStart(7)&sysparm_fields=number,sys_created_on,short_description&sysparm_limit=10" \
  | python3 -m json.tool
```

### Date filter: created this month

```bash
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=sys_created_on>=javascript:gs.beginningOfThisMonth()&sysparm_fields=number,sys_created_on&sysparm_limit=10" \
  | python3 -m json.tool
```

### Date filter: between two specific dates

```bash
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=sys_created_on>=2024-01-01^sys_created_on<=2024-12-31&sysparm_fields=number,sys_created_on&sysparm_limit=10" \
  | python3 -m json.tool
```

### Sort: oldest first (ascending)

```bash
# Equivalent to: clicking the "Created" column header to sort ascending
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=ORDERBYsys_created_on&sysparm_fields=number,sys_created_on&sysparm_limit=5" \
  | python3 -m json.tool
```

### Sort: newest first (descending)

```bash
# Equivalent to: clicking the "Created" column header twice to sort descending
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=ORDERBYDESCsys_created_on&sysparm_fields=number,sys_created_on&sysparm_limit=5" \
  | python3 -m json.tool
```

### Multi-column sort: priority ascending, then created descending

```bash
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=ORDERBYpriority^ORDERBYDESCsys_created_on&sysparm_fields=number,priority,sys_created_on&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

### Dot-walking: filter by a related record's field

```bash
# Equivalent to: "Assignment group > Name is Network"
# Dot-walking lets you filter on fields from referenced tables
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=assignment_group.nameLIKENetwork&sysparm_fields=number,assignment_group&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool

# Dot-walk deeper: "Caller > Department > Name is IT"
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=caller_id.department.nameLIKEIT&sysparm_fields=number,caller_id&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

### Aggregate: count incidents by priority

```bash
# Equivalent to: right-clicking the Priority column > Group By, or a report bar chart
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=active=true&sysparm_group_by=priority&sysparm_count=true" \
  | python3 -m json.tool
```

### Aggregate: count incidents by state

```bash
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/stats/incident?sysparm_group_by=state&sysparm_count=true&sysparm_display_value=true" \
  | python3 -m json.tool
```

### Aggregate: average resolution time

```bash
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=state=7&sysparm_avg_fields=calendar_duration&sysparm_display_value=true" \
  | python3 -m json.tool
```

### Pagination: simulate scrolling through a long list

```bash
# Page 1 (records 1-10)
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_limit=10&sysparm_offset=0&sysparm_fields=number,short_description"

# Page 2 (records 11-20)
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_limit=10&sysparm_offset=10&sysparm_fields=number,short_description"

# Page 3 (records 21-30)
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_limit=10&sysparm_offset=20&sysparm_fields=number,short_description"
```

### Complex combined query (real-world example)

```bash
# "Show me all P1 or P2 incidents assigned to a group with 'Network' in the name,
#  created in the last 30 days, sorted by newest first"
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=priority<=2^assignment_group.nameLIKENetwork^sys_created_on>=javascript:gs.daysAgoStart(30)^ORDERBYDESCsys_created_on&sysparm_fields=number,short_description,priority,assignment_group,sys_created_on&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

### Export encoded query (for saving/sharing filters)

```bash
# The sysparm_query value IS the encoded query.
# You can copy it from the UI: right-click breadcrumb > Copy query
# Example encoded query:
#   priority<=2^stateNOT IN6,7^assignment_groupISNOTEMPTY
# Use it directly:
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=priority<=2^stateNOT IN6,7^assignment_groupISNOTEMPTY&sysparm_fields=number,priority,state,assignment_group&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

---

## Cleanup — Remove Lab Test Data

> Run these commands to delete all users, groups, and memberships created during Lab 04.
> **WARNING:** These are destructive operations. Only run in your PDI, never in production.

### Delete lab users

```bash
# Delete each user created in Lab 04
for uname in ravi.kumar priya.sharma amit.verma meera.joshi vijay.admin sanjay.mgr; do
  SID=$(curl -s -u "$AUTH" -H "Accept:application/json" \
    "$SNOW/api/now/table/sys_user?sysparm_query=user_name=$uname&sysparm_fields=sys_id" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
  if [ "$SID" != "NOT_FOUND" ]; then
    curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/sys_user/$SID"
    echo "Deleted user: $uname ($SID)"
  else
    echo "User not found: $uname (skipped)"
  fi
done
```

### Delete lab groups

```bash
# Delete each group created in Lab 04
for gname in "UPI Platform Engineering" "UPI NOC" "UPI Service Desk"; do
  GID=$(curl -s -u "$AUTH" -H "Accept:application/json" \
    "$SNOW/api/now/table/sys_user_group?sysparm_query=name=$gname&sysparm_fields=sys_id" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['sys_id'] if r else 'NOT_FOUND')")
  if [ "$GID" != "NOT_FOUND" ]; then
    # Group memberships and role assignments are auto-deleted when the group is removed
    curl -s -u "$AUTH" -X DELETE "$SNOW/api/now/table/sys_user_group/$GID"
    echo "Deleted group: $gname ($GID)"
  else
    echo "Group not found: $gname (skipped)"
  fi
done
```

### Verify cleanup

```bash
# Confirm no lab users remain
echo "=== Remaining lab users (should be empty) ==="
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_user?sysparm_query=user_nameINravi.kumar,priya.sharma,amit.verma,meera.joshi,vijay.admin,sanjay.mgr&sysparm_fields=user_name" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print('None found - cleanup complete' if not r else [u['user_name'] for u in r])"

# Confirm no lab groups remain
echo "=== Remaining lab groups (should be empty) ==="
curl -s -u "$AUTH" -H "Accept:application/json" \
  "$SNOW/api/now/table/sys_user_group?sysparm_query=nameLIKEUPI&sysparm_fields=name" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print('None found - cleanup complete' if not r else [g['name'] for g in r])"
```

---

## Quick Reference — Encoded Query Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equals | `priority=1` |
| `!=` | Not equals | `state!=7` |
| `<` | Less than | `priority<3` |
| `<=` | Less than or equal | `priority<=2` |
| `>` | Greater than | `impact>2` |
| `>=` | Greater than or equal | `sys_created_on>=2024-01-01` |
| `LIKE` | Contains | `short_descriptionLIKEUPI` |
| `STARTSWITH` | Starts with | `numberSTARTSWITHINC` |
| `ENDSWITH` | Ends with | `emailENDSWITH@example.com` |
| `IN` | In list | `priorityIN1,2,3` |
| `NOT IN` | Not in list | `priorityNOT IN4,5` |
| `ISEMPTY` | Is empty/null | `assigned_toISEMPTY` |
| `ISNOTEMPTY` | Is not empty | `assignment_groupISNOTEMPTY` |
| `^` | AND | `priority=1^state=1` |
| `^OR` | OR | `priority=1^ORpriority=2` |
| `ORDERBY` | Sort ascending | `ORDERBYsys_created_on` |
| `ORDERBYDESC` | Sort descending | `ORDERBYDESCsys_created_on` |
| `BETWEEN` | Between values | `priorityBETWEEN1@3` |
| `INSTANCEOF` | Table hierarchy | `sys_class_nameINSTANCEOFtask` |

## Quick Reference — Common sysparm Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `sysparm_limit` | Max records to return | `sysparm_limit=10` |
| `sysparm_offset` | Skip N records (pagination) | `sysparm_offset=20` |
| `sysparm_fields` | Comma-separated field list | `sysparm_fields=number,state` |
| `sysparm_query` | Encoded query string | `sysparm_query=priority=1` |
| `sysparm_display_value` | Return labels instead of values | `sysparm_display_value=true` |
| `sysparm_exclude_reference_link` | Omit reference URLs | `sysparm_exclude_reference_link=true` |
| `sysparm_count` | Return count only (stats API) | `sysparm_count=true` |
| `sysparm_group_by` | Group results (stats API) | `sysparm_group_by=priority` |
| `sysparm_avg_fields` | Average a numeric field | `sysparm_avg_fields=calendar_duration` |
| `sysparm_sum_fields` | Sum a numeric field | `sysparm_sum_fields=calendar_duration` |

---

*End of Phase 1 API Companion. Proceed to Phase 2 for Incident, Problem, Change, and CMDB API operations.*
