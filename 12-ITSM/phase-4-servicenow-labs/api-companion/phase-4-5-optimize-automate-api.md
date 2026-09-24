# API Companion: Phase 4 (Optimize) & Phase 5 (Automate) — Labs 17-22

This file provides curl REST API commands that replicate what Labs 17-22
do via the ServiceNow UI. Use these to automate, script, or integrate
the Optimize and Automate phases of the NPCI UPI ITSM implementation.

---

## Setup: Credentials and Environment

```bash
export SNOW="https://YOUR-INSTANCE.service-now.com"
export AUTH="admin:YOUR-PASSWORD"

# Helper alias for pretty-printed JSON output
alias snowget='curl -s -u "$AUTH" -H "Accept: application/json"'
alias snowpost='curl -s -u "$AUTH" -H "Content-Type: application/json" -H "Accept: application/json" -X POST'
alias snowpatch='curl -s -u "$AUTH" -H "Content-Type: application/json" -H "Accept: application/json" -X PATCH'
alias snowput='curl -s -u "$AUTH" -H "Content-Type: application/json" -H "Accept: application/json" -X PUT'
alias snowdel='curl -s -u "$AUTH" -X DELETE'
```

---

## Lab 17: Reporting & Performance Analytics

> **UI Equivalent:** Reports > Create New, Performance Analytics > Indicators,
> Self-Service > Dashboards. Lab 17 builds 10+ reports and a dashboard.
> The API cannot render charts, but it CAN query the underlying data that
> powers every report and PA indicator.

### 17.1 Aggregate API — Incidents by Priority (Donut Chart data)

```bash
# UI: Report 2 — "UPI Incidents by Priority" donut chart
# Returns count of active incidents grouped by priority
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=active=true&sysparm_count=true&sysparm_group_by=priority&sysparm_display_value=true" \
  | python3 -m json.tool
```

**Expected response:**

```json
{
  "result": [
    { "groupby_fields": [{"field": "priority", "value": "1 - Critical"}], "stats": {"count": "3"} },
    { "groupby_fields": [{"field": "priority", "value": "2 - High"}], "stats": {"count": "8"} },
    { "groupby_fields": [{"field": "priority", "value": "3 - Moderate"}], "stats": {"count": "15"} },
    { "groupby_fields": [{"field": "priority", "value": "4 - Low"}], "stats": {"count": "22"} }
  ]
}
```

### 17.2 Aggregate API — Incidents by Assignment Group (Horizontal Bar data)

```bash
# UI: Report 3 — "UPI Incidents by Assignment Group" bar chart
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=active=true&sysparm_count=true&sysparm_group_by=assignment_group&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.3 Aggregate API — Average Resolution Time (MTTR Bar Chart data)

```bash
# UI: Report 5 — "UPI MTTR by Priority" bar chart
# Average calendar_duration for resolved incidents, grouped by priority
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=stateIN6,7^resolved_atISNOTEMPTY&sysparm_avg_fields=calendar_duration&sysparm_group_by=priority&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.4 Aggregate API — SLA Compliance (Pivot Table data)

```bash
# UI: Report 4 — "UPI SLA Compliance by Priority" pivot table
# Count of completed task_sla records grouped by has_breached and task priority
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/task_sla?sysparm_query=stage=complete&sysparm_count=true&sysparm_group_by=has_breached&sysparm_display_value=true" \
  | python3 -m json.tool
```

```bash
# SLA breaches by task priority (cross-tab data)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/task_sla?sysparm_query=stage=complete^has_breached=true&sysparm_count=true&sysparm_group_by=task.priority&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.5 Aggregate API — Incidents by Category (Pie Chart data)

```bash
# UI: Report 7 — "UPI Problem Root Cause by Category" pie chart (applied to incidents here)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=active=true&sysparm_count=true&sysparm_group_by=category&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.6 Aggregate API — Incidents by Configuration Item (Top 10 CIs)

```bash
# UI: Report 8 — "UPI Top 10 Impacted CIs" bar chart
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=cmdb_ciISNOTEMPTY&sysparm_count=true&sysparm_group_by=cmdb_ci&sysparm_display_value=true&sysparm_orderby=count&sysparm_top=10" \
  | python3 -m json.tool
```

### 17.7 Aggregate API — Incident Trend Monthly (Line Chart data)

```bash
# UI: Report 1 — "UPI Incident Trend - Monthly" line chart
# Count incidents grouped by creation month for last 90 days
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=sys_created_on>=javascript:gs.daysAgo(90)&sysparm_count=true&sysparm_group_by=sys_created_on&sysparm_group_by_having=GROUPBYTRUNC:month&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.8 Aggregate API — Change Success Rate (Single Score data)

```bash
# UI: Report 6 — "UPI Change Success Rate" single score
# Count of successful changes
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/change_request?sysparm_query=state=-3^close_code=successful&sysparm_count=true" \
  | python3 -m json.tool
```

```bash
# Total completed changes (for calculating percentage)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/change_request?sysparm_query=state=-3&sysparm_count=true" \
  | python3 -m json.tool
```

### 17.9 Aggregate API — Changes by Type (Column Chart data)

```bash
# Count changes grouped by type (Normal, Standard, Emergency)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/change_request?sysparm_count=true&sysparm_group_by=type&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.10 Aggregate API — Problems by State (Donut data)

```bash
# Problem status distribution for dashboard widget
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/problem?sysparm_count=true&sysparm_group_by=state&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.11 Aggregate API — Problems by Category

```bash
# Problem root cause category distribution
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/problem?sysparm_count=true&sysparm_group_by=category&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.12 Aggregate API — Incident Reopen Rate

```bash
# Count of incidents that were reopened (reopen_count > 0)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=reopen_count>0^stateIN6,7&sysparm_count=true" \
  | python3 -m json.tool
```

```bash
# Total resolved/closed incidents (denominator for reopen rate)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=stateIN6,7&sysparm_count=true" \
  | python3 -m json.tool
```

### 17.13 Aggregate API — Incidents by State (for backlog analysis)

```bash
# Current backlog: count of incidents in each state
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_count=true&sysparm_group_by=state&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.14 Aggregate API — Average and Max Resolution Time

```bash
# Average and maximum calendar_duration for resolved incidents
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=stateIN6,7^resolved_atISNOTEMPTY&sysparm_avg_fields=calendar_duration&sysparm_max_fields=calendar_duration&sysparm_min_fields=calendar_duration" \
  | python3 -m json.tool
```

### 17.15 Aggregate API — SLA Breaches by SLA Definition

```bash
# Which SLA definitions are breached most often?
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/task_sla?sysparm_query=has_breached=true&sysparm_count=true&sysparm_group_by=sla&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.16 Aggregate API — Incidents Created Per Day of Week (Heatmap data)

```bash
# Count incidents by day of week (for staffing optimization)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=sys_created_on>=javascript:gs.daysAgo(180)&sysparm_count=true&sysparm_group_by=sys_created_on&sysparm_group_by_having=GROUPBYTRUNC:dayofweek&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 17.17 Query Report Definitions via API

```bash
# UI: Reports > All — list existing reports
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_report?sysparm_query=titleLIKEUPI&sysparm_fields=sys_id,title,table,type,field,user&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### 17.18 Create a Report via API

```bash
# UI: Reports > Create New
# Creates a bar chart report for incidents by priority
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_report" \
  -d '{
    "title": "UPI Incidents by Priority (API Created)",
    "table": "incident",
    "type": "bar",
    "field": "priority",
    "filter": "active=true",
    "description": "Created via REST API - shows active incident distribution by priority"
  }' \
  | python3 -m json.tool
```

**Verification — confirm the report was created:**

```bash
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_report?sysparm_query=titleLIKEAPI Created&sysparm_fields=sys_id,title,table,type&sysparm_limit=5" \
  | python3 -m json.tool
```

---

## Lab 18: Continual Improvement

> **UI Equivalent:** System Definition > Plugins (activate CIM),
> Continual Improvement > Create New, walk records through lifecycle states.
> The CIM plugin creates the `improvement` table.

### 18.1 Check if CIM Plugin is Active

```bash
# Query the plugin registry for CIM
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/v_plugin?sysparm_query=idLIKEcim^ORnameLIKEContinual Improvement&sysparm_fields=id,name,active&sysparm_display_value=true&sysparm_limit=5" \
  | python3 -m json.tool
```

> **Note:** Plugin activation MUST be done via the UI (System Definition > Plugins).
> The REST API does not support plugin activation. If the plugin is not active,
> navigate to System Definition > Plugins, search for "com.sn_cim", and activate it.

### 18.2 Create Improvement Initiative — Reduce P1 MTTR

```bash
# UI: Continual Improvement > Create New
# CIM0001001: Reduce P1 MTTR from 4.2hrs to < 1hr
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/improvement" \
  -d '{
    "short_description": "Reduce P1 MTTR from 4.2hrs to < 1hr",
    "priority": "1",
    "description": "P1 incidents on the UPI Transaction Service currently take an average of 4.2 hours to resolve. For a real-time payment platform processing 14+ billion transactions per month, this is unacceptable. This improvement targets auto-assignment, KB integration, and CI auto-detection to reduce MTTR to under 1 hour.",
    "justification": "UPI platform availability directly impacts national digital payment infrastructure. Reducing P1 MTTR from 4.2 hours to < 1 hour will reduce transaction failure windows by 76%. Conservative estimate: prevents 500K+ failed transactions per incident."
  }' \
  | python3 -m json.tool
```

**Save the returned sys_id for subsequent operations:**

```bash
export CIM_MTTR_ID="<sys_id from response>"
```

### 18.3 Create Improvement Initiative — SLA Compliance

```bash
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/improvement" \
  -d '{
    "short_description": "Improve SLA Compliance from 72% to 95%",
    "priority": "2",
    "description": "SLA compliance across all incident priorities is 72%, meaning nearly 1 in 3 tickets breaches its SLA. Root causes include overly aggressive SLA targets for current process maturity, lack of proactive breach warnings, and insufficient training on SLA expectations.",
    "justification": "SLA breaches erode trust with UPI member banks and internal stakeholders. Improving compliance to 95% demonstrates operational maturity and supports NPCI service level commitments to RBI."
  }' \
  | python3 -m json.tool
```

### 18.4 Create Improvement Initiative — Change Failure Rate

```bash
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/improvement" \
  -d '{
    "short_description": "Reduce Change Failure Rate from 15% to below 5%",
    "priority": "2",
    "description": "15% of changes deployed to the UPI platform result in failures. This initiative addresses mandatory CI impact analysis, automated pre-deployment testing using ATF, comprehensive rollback plans, and peer review for all changes.",
    "justification": "Each failed change risks UPI platform stability. Reducing to < 5% aligns with DORA metrics for elite performers and reduces unplanned work for Platform Engineering."
  }' \
  | python3 -m json.tool
```

### 18.5 Update Improvement Through Lifecycle States

```bash
# Transition CIM0001001 to Analysis state
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/improvement/$CIM_MTTR_ID" \
  -d '{
    "state": "analysis",
    "work_notes": "Analysis complete. Root causes confirmed: 42% of P1 time spent waiting for assignment, 28% searching for runbooks, 18% identifying affected CI, 12% actual investigation and fix. Feasibility: HIGH."
  }' \
  | python3 -m json.tool
```

```bash
# Transition to Approved
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/improvement/$CIM_MTTR_ID" \
  -d '{
    "state": "authorized",
    "work_notes": "Approved by Sanjay Manager in CSI review meeting. Budget: No additional budget required. Resources: Ravi Kumar (20 hrs), Priya Sharma (10 hrs), Admin (10 hrs)."
  }' \
  | python3 -m json.tool
```

```bash
# Transition to Implementation
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/improvement/$CIM_MTTR_ID" \
  -d '{
    "state": "implementation",
    "work_notes": "Implementation started. Week 1: Configure auto-assignment rules and create 5 UPI runbook KB articles. Week 2: CMDB CI auto-detection and escalation rule updates."
  }' \
  | python3 -m json.tool
```

```bash
# Transition to Closed (successful)
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/improvement/$CIM_MTTR_ID" \
  -d '{
    "state": "closed",
    "work_notes": "IMPROVEMENT CLOSED - SUCCESS. P1 MTTR reduced from 4.2 hours to 45 minutes. Auto-assignment, KB integration, and escalation rules are now permanent configurations. Next iteration: Target MTTR < 30 minutes."
  }' \
  | python3 -m json.tool
```

### 18.6 Query All Improvement Records (CSI Register)

```bash
# UI: Continual Improvement > All
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/improvement?sysparm_fields=number,short_description,priority,state,assigned_to,assignment_group&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### 18.7 Link Improvement to Related Incident

```bash
# Find the M2M table linking improvements to tasks/incidents
# The table name may vary by instance: improvement_incident, task_rel_task, etc.
# Query for existing relationships:
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/task_rel_task?sysparm_query=parent=$CIM_MTTR_ID&sysparm_fields=parent,child,type&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

---

## Lab 19: Availability & Capacity Management

> **UI Equivalent:** Calculating availability from incident data per CI,
> CMDB operational status checks, SPOF analysis, capacity projections.
> These queries compute the raw data for availability and capacity metrics.

### 19.1 Query Incidents by CI for Downtime Calculation

```bash
# UI: Incident > All, filter by CI and P1/P2 for availability calculation
# Get all P1/P2 incidents on UPI Transaction Service with opened/resolved timestamps
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=cmdb_ci.nameLIKEUPI Transaction^priorityIN1,2^stateIN6,7^resolved_atISNOTEMPTY&sysparm_fields=number,short_description,priority,opened_at,resolved_at,cmdb_ci,calendar_duration&sysparm_display_value=all&sysparm_limit=50" \
  | python3 -m json.tool
```

### 19.2 MTTR Calculation — Average Resolution Time by CI

```bash
# Average calendar_duration grouped by CI (MTTR per component)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=stateIN6,7^resolved_atISNOTEMPTY^cmdb_ciISNOTEMPTY&sysparm_avg_fields=calendar_duration&sysparm_group_by=cmdb_ci&sysparm_display_value=true" \
  | python3 -m json.tool
```

**Interpreting the result for availability:**

```
For each CI:
  AST = 720 hours (30-day month, 24x7)
  DT  = sum of (resolved_at - opened_at) for all P1/P2 incidents

  Availability % = (AST - DT) / AST * 100

  MTTR = DT / number_of_failures
  MTBF = (AST - DT) / number_of_failures

Example: UPI Transaction Service
  3 failures, total DT = 4.5 hours
  Availability = (720 - 4.5) / 720 * 100 = 99.375%
  MTTR = 4.5 / 3 = 1.5 hours
  MTBF = (720 - 4.5) / 3 = 238.5 hours
```

### 19.3 MTBF Calculation — Count Failures per CI

```bash
# Count of P1/P2 incidents per CI (number of failures)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=priorityIN1,2^stateIN6,7^cmdb_ciISNOTEMPTY&sysparm_count=true&sysparm_group_by=cmdb_ci&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 19.4 Query CI Operational Status from CMDB

```bash
# UI: Configuration > All CIs — check operational_status
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_ci?sysparm_query=nameLIKEUPI&sysparm_fields=name,sys_class_name,operational_status,support_group,busines_criticality&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### 19.5 Simulate Maintenance — Update CI Status

```bash
# UI: Open CI > set Operational Status to "Maintenance"
# First find the CI sys_id
CI_SYS_ID=$(curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_ci?sysparm_query=name=UPI Transaction Service&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

echo "CI sys_id: $CI_SYS_ID"

# Set to Maintenance mode
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/cmdb_ci/$CI_SYS_ID" \
  -d '{
    "operational_status": "6",
    "short_description": "Scheduled maintenance window for patching"
  }' \
  | python3 -m json.tool
```

```bash
# Restore to Operational after maintenance
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/cmdb_ci/$CI_SYS_ID" \
  -d '{
    "operational_status": "1"
  }' \
  | python3 -m json.tool
```

### 19.6 Availability Data from Custom Table (if created in Lab 19)

```bash
# Query the custom availability records table (u_availability_record)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/u_availability_record?sysparm_fields=u_configuration_item,u_ast_hours,u_downtime_hours,u_availability_pct,u_slo_target_pct,u_slo_status,u_failure_count,u_mtbf_hours,u_mtrs_hours&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### 19.7 Capacity Data from Custom Table (if created in Lab 19)

```bash
# Query the custom capacity records table (u_capacity_record)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/u_capacity_record?sysparm_fields=u_configuration_item,u_metric_name,u_current_value,u_warning_threshold,u_critical_threshold,u_unit,u_capacity_status,u_projected_exhaustion,u_growth_rate_pct&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### 19.8 Compute Availability with Shell Math

```bash
# End-to-end availability calculation from API data
# Step 1: Get total downtime hours for a CI in a given period
CI_NAME="UPI Transaction Service"

# Fetch P1/P2 resolved incidents on this CI in the last 30 days
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/incident?sysparm_query=cmdb_ci.name=$CI_NAME^priorityIN1,2^stateIN6,7^opened_at>=javascript:gs.daysAgo(30)&sysparm_fields=number,opened_at,resolved_at,calendar_duration&sysparm_limit=50" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)['result']
total_seconds = 0
for inc in data:
    dur = int(inc.get('calendar_duration', '0') or '0')
    total_seconds += dur
    print(f\"  {inc['number']}: {dur}s ({dur/3600:.2f}h)\")
hours = total_seconds / 3600
ast = 720
avail = (ast - hours) / ast * 100
failures = len(data)
mttr = hours / failures if failures > 0 else 0
mtbf = (ast - hours) / failures if failures > 0 else ast
print(f\"\nTotal downtime: {hours:.2f} hours\")
print(f\"Availability:   {avail:.4f}%\")
print(f\"Failures:       {failures}\")
print(f\"MTTR:           {mttr:.2f} hours\")
print(f\"MTBF:           {mtbf:.2f} hours\")
print(f\"SLO (99.95%):   {'MET' if avail >= 99.95 else 'BREACH'}\")
"
```

---

## Lab 20: Flow Designer & Automation

> **UI Equivalent:** Process Automation > Flow Designer. Flow Designer is a
> UI-only tool -- flows cannot be created or modified via REST API. However,
> we CAN replicate the EFFECTS of flows using Business Rules (sys_script),
> Scheduled Jobs (sysauto_script), and Notifications (sysevent_email_action).

### 20.1 Query Existing Flows

```bash
# List all flows in Flow Designer (sys_hub_flow table)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_hub_flow?sysparm_fields=sys_id,name,description,active,status&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### 20.2 Create Business Rule — UPI Auto-Assignment (API equivalent of Flow)

```bash
# UI: System Definition > Business Rules > New
# This replicates the "UPI Incident Auto-Assignment" flow from Lab 20
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_script" \
  -d '{
    "name": "NPCI - UPI Auto-Assignment (API)",
    "collection": "incident",
    "active": "true",
    "when": "before",
    "action_insert": "true",
    "order": "100",
    "filter_condition": "category=upi^ORcategory=network",
    "script": "(function executeRule(current, previous) {\n    if (current.category == \"upi\" && current.priority == 1) {\n        current.assignment_group.setDisplayValue(\"Platform Engineering\");\n        current.work_notes = \"[Auto-Assigned] P1 UPI incident auto-assigned to Platform Engineering by Business Rule.\";\n    } else if (current.category == \"upi\" && (current.priority == 2 || current.priority == 3)) {\n        current.assignment_group.setDisplayValue(\"Platform Engineering\");\n        current.work_notes = \"[Auto-Assigned] UPI incident auto-assigned to Platform Engineering.\";\n    } else if (current.category == \"network\") {\n        current.assignment_group.setDisplayValue(\"Network Operations\");\n        current.work_notes = \"[Auto-Assigned] Network incident auto-assigned to Network Operations.\";\n    } else {\n        current.assignment_group.setDisplayValue(\"Service Desk\");\n        current.work_notes = \"[Auto-Assigned] Incident auto-assigned to Service Desk (default).\";\n    }\n})(current, previous);"
  }' \
  | python3 -m json.tool
```

### 20.3 Create Scheduled Job — Auto-Close Resolved Incidents

```bash
# UI: System Definition > Scheduled Jobs > New
# Replicates the "Auto-Close Resolved Incidents After 5 Days" flow from Lab 20
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sysauto_script" \
  -d '{
    "name": "NPCI - Auto-Close Resolved Incidents (API)",
    "active": "true",
    "run_type": "daily",
    "time": "00:00:00",
    "script": "var gr = new GlideRecord(\"incident\");\ngr.addQuery(\"state\", 6);\nvar dt = new GlideDateTime();\ndt.addDaysLocalTime(-5);\ngr.addQuery(\"resolved_at\", \"<\", dt);\ngr.query();\nvar count = 0;\nwhile (gr.next()) {\n    gr.state = 7;\n    gr.close_code = \"Solved (Permanently)\";\n    gr.close_notes = \"Auto-closed after 5 days in Resolved state per NPCI incident management policy.\";\n    gr.work_notes = \"[AUTO-CLOSE] This incident was automatically closed by scheduled job. 5+ days elapsed since resolution.\";\n    gr.update();\n    count++;\n}\ngs.info(\"NPCI Auto-Close: Closed \" + count + \" resolved incidents.\");"
  }' \
  | python3 -m json.tool
```

### 20.4 Create Email Notification — SLA Breach Alert

```bash
# UI: System Notification > Email > Notifications > New
# Replicates the SLA breach email from Lab 20
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sysevent_email_action" \
  -d '{
    "name": "NPCI - SLA Breach Alert (API)",
    "collection": "task_sla",
    "active": "true",
    "event_name": "sla.breached",
    "subject": "URGENT: SLA BREACHED on ${task.number}",
    "message_html": "<h2>SLA Breach Alert</h2><p>Incident: ${task.number}</p><p>Description: ${task.short_description}</p><p>Priority: ${task.priority}</p><p>SLA: ${sla.name}</p><p>Breach Time: ${breach_time}</p><p>Assigned To: ${task.assigned_to}</p><p>This is an automated notification from the NPCI UPI ITSM Platform.</p>"
  }' \
  | python3 -m json.tool
```

### 20.5 Query Existing Business Rules

```bash
# List all custom business rules on the incident table
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_script?sysparm_query=collection=incident^nameLIKENPCI&sysparm_fields=sys_id,name,when,active,action_insert,action_update,order&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

---

## Lab 21: Business Rules, Client Scripts & UI Policies

> **UI Equivalent:** System Definition > Business Rules / Client Scripts / Script Includes,
> System UI > UI Policies / UI Actions. Lab 21 creates 5 business rules, 4 client scripts,
> 4 UI policies, 2 script includes, and 3 UI actions.

### 21.1 Create Business Rule — Prevent P1 Close Without Root Cause

```bash
# UI: System Definition > Business Rules > New
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_script" \
  -d '{
    "name": "NPCI - Prevent P1 Close Without Root Cause",
    "collection": "incident",
    "active": "true",
    "when": "before",
    "action_update": "true",
    "filter_condition": "priority=1^state=7",
    "order": "200",
    "script": "(function executeRule(current, previous) {\n    if (!current.state.changesTo(7)) return;\n    if (current.priority != 1) return;\n    var errors = [];\n    if (current.close_notes.nil()) errors.push(\"Close Notes are required for P1 incidents\");\n    if (current.close_code.nil()) errors.push(\"Close Code is required for P1 incidents\");\n    if (current.cmdb_ci.nil()) errors.push(\"Configuration Item must be set before closing a P1 incident\");\n    if (!current.close_notes.nil() && current.close_notes.toString().length < 50) errors.push(\"Close Notes must contain at least 50 characters describing the root cause\");\n    if (errors.length > 0) {\n        var message = \"Cannot close P1 incident:\\n\";\n        for (var i = 0; i < errors.length; i++) message += \"- \" + errors[i] + \"\\n\";\n        gs.addErrorMessage(message);\n        current.setAbortAction(true);\n    }\n})(current, previous);"
  }' \
  | python3 -m json.tool
```

### 21.2 Create Business Rule — Auto-populate CI from Category

```bash
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_script" \
  -d '{
    "name": "NPCI - Auto-populate CI from Category",
    "collection": "incident",
    "active": "true",
    "when": "before",
    "action_insert": "true",
    "action_update": "true",
    "filter_condition": "category=upi",
    "order": "100",
    "script": "(function executeRule(current, previous) {\n    var ciMapping = {\n        \"transaction\": \"UPI Transaction Service\",\n        \"settlement\": \"UPI Settlement Service\",\n        \"dispute\": \"UPI Dispute Resolution\",\n        \"merchant\": \"NPCI API Gateway\",\n        \"monitoring\": \"UPI Monitoring Stack\"\n    };\n    var subcategory = current.subcategory.toString().toLowerCase();\n    var ciName = ciMapping[subcategory];\n    if (!ciName) return;\n    var gr = new GlideRecord(\"cmdb_ci\");\n    gr.addQuery(\"name\", ciName);\n    gr.setLimit(1);\n    gr.query();\n    if (gr.next()) {\n        current.cmdb_ci = gr.sys_id;\n        gs.info(\"NPCI BR: Auto-set CI to \" + ciName + \" for \" + current.number);\n    }\n})(current, previous);"
  }' \
  | python3 -m json.tool
```

### 21.3 Create Business Rule — Auto-create Problem for Recurring Incidents

```bash
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_script" \
  -d '{
    "name": "NPCI - Auto-create Problem for Recurring Incidents",
    "collection": "incident",
    "active": "true",
    "when": "async",
    "action_update": "true",
    "filter_condition": "state=6",
    "order": "500",
    "script": "(function executeRule(current, previous) {\n    if (current.cmdb_ci.nil()) return;\n    var ciSysId = current.cmdb_ci.toString();\n    var ciName = current.cmdb_ci.getDisplayValue();\n    var lookbackDate = new GlideDateTime();\n    lookbackDate.addDaysUTC(-30);\n    var ga = new GlideAggregate(\"incident\");\n    ga.addQuery(\"cmdb_ci\", ciSysId);\n    ga.addQuery(\"state\", \"IN\", \"6,7\");\n    ga.addQuery(\"opened_at\", \">=\", lookbackDate);\n    ga.addAggregate(\"COUNT\");\n    ga.query();\n    var incidentCount = 0;\n    if (ga.next()) incidentCount = parseInt(ga.getAggregate(\"COUNT\"), 10);\n    if (incidentCount < 3) return;\n    var existing = new GlideRecord(\"problem\");\n    existing.addQuery(\"cmdb_ci\", ciSysId);\n    existing.addQuery(\"state\", \"NOT IN\", \"4,7\");\n    existing.addQuery(\"short_description\", \"CONTAINS\", \"Recurring\");\n    existing.setLimit(1);\n    existing.query();\n    if (existing.next()) {\n        existing.work_notes = \"Additional recurring incident: \" + current.number;\n        existing.update();\n        return;\n    }\n    var problem = new GlideRecord(\"problem\");\n    problem.initialize();\n    problem.short_description = \"Recurring incidents on CI: \" + ciName;\n    problem.description = \"Auto-created. CI \" + ciName + \" has \" + incidentCount + \" incidents in 30 days.\";\n    problem.cmdb_ci = ciSysId;\n    problem.category = current.category.toString();\n    problem.assignment_group = current.assignment_group;\n    problem.insert();\n    gs.info(\"NPCI BR: Created Problem \" + problem.number + \" for recurring incidents on \" + ciName);\n})(current, previous);"
  }' \
  | python3 -m json.tool
```

### 21.4 Create UI Policy — Show Resolution Fields When Resolved

```bash
# UI: System UI > UI Policies > New
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_ui_policy" \
  -d '{
    "table": "incident",
    "short_description": "NPCI - Show Resolution Fields When Resolved",
    "active": "true",
    "conditions": "state=6",
    "on_load": "true",
    "reverse_if_false": "true",
    "order": "100"
  }' \
  | python3 -m json.tool
```

**Save the sys_id, then add UI Policy Actions:**

```bash
export UI_POLICY_ID="<sys_id from above>"

# Action 1: Make Close Code mandatory and visible
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_ui_policy_action" \
  -d '{
    "ui_policy": "'"$UI_POLICY_ID"'",
    "field": "close_code",
    "mandatory": "true",
    "visible": "true"
  }' \
  | python3 -m json.tool

# Action 2: Make Close Notes mandatory and visible
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_ui_policy_action" \
  -d '{
    "ui_policy": "'"$UI_POLICY_ID"'",
    "field": "close_notes",
    "mandatory": "true",
    "visible": "true"
  }' \
  | python3 -m json.tool
```

### 21.5 Create Client Script — Mandatory Fields on P1

```bash
# UI: System Definition > Client Scripts > New
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_script_client" \
  -d '{
    "name": "NPCI - Mandatory Fields on P1",
    "table": "incident",
    "type": "onChange",
    "fieldname": "priority",
    "active": "true",
    "script": "function onChange(control, oldValue, newValue, isLoading, isTemplate) {\n    if (isLoading || newValue === \"\") return;\n    if (newValue == \"1\") {\n        g_form.setMandatory(\"assignment_group\", true);\n        g_form.setMandatory(\"cmdb_ci\", true);\n        g_form.setMandatory(\"description\", true);\n        g_form.setMandatory(\"contact_type\", true);\n        g_form.addInfoMessage(\"P1 CRITICAL INCIDENT: Assignment Group, Configuration Item, Description, and Contact Type are required.\");\n    } else {\n        g_form.setMandatory(\"assignment_group\", false);\n        g_form.setMandatory(\"cmdb_ci\", false);\n        g_form.setMandatory(\"description\", false);\n        g_form.setMandatory(\"contact_type\", false);\n        g_form.clearMessages();\n    }\n}"
  }' \
  | python3 -m json.tool
```

### 21.6 Create Script Include — UPIUtils

```bash
# UI: System Definition > Script Includes > New
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_script_include" \
  -d '{
    "name": "UPIUtils",
    "api_name": "global.UPIUtils",
    "client_callable": "false",
    "active": "true",
    "description": "Server-side utility class for NPCI UPI operations. Provides methods for recurring incident detection, MTTR calculation, and VIP caller identification.",
    "script": "var UPIUtils = Class.create();\nUPIUtils.prototype = {\n    initialize: function() {\n        this.LOG_PREFIX = \"UPIUtils: \";\n    },\n    getRelatedIncidents: function(ciSysId, days) {\n        if (!ciSysId) return { count: 0, incidents: [] };\n        days = days || 30;\n        var lookbackDate = new GlideDateTime();\n        lookbackDate.addDaysUTC(-days);\n        var incidents = [];\n        var gr = new GlideRecord(\"incident\");\n        gr.addQuery(\"cmdb_ci\", ciSysId);\n        gr.addQuery(\"opened_at\", \">=\", lookbackDate);\n        gr.orderByDesc(\"opened_at\");\n        gr.query();\n        while (gr.next()) {\n            incidents.push({ number: gr.number.toString(), short_description: gr.short_description.toString() });\n        }\n        return { count: incidents.length, incidents: incidents };\n    },\n    calculateMTTR: function(ciSysId, days) {\n        if (!ciSysId) return { mttr_minutes: 0, mttr_display: \"N/A\", sample_size: 0 };\n        days = days || 90;\n        var lookbackDate = new GlideDateTime();\n        lookbackDate.addDaysUTC(-days);\n        var totalMinutes = 0;\n        var count = 0;\n        var gr = new GlideRecord(\"incident\");\n        gr.addQuery(\"cmdb_ci\", ciSysId);\n        gr.addQuery(\"state\", \"IN\", \"6,7\");\n        gr.addQuery(\"opened_at\", \">=\", lookbackDate);\n        gr.addNotNullQuery(\"resolved_at\");\n        gr.query();\n        while (gr.next()) {\n            var opened = new GlideDateTime(gr.opened_at.toString());\n            var resolved = new GlideDateTime(gr.resolved_at.toString());\n            var diffMs = resolved.getNumericValue() - opened.getNumericValue();\n            if (diffMs > 0) { totalMinutes += Math.floor(diffMs / 60000); count++; }\n        }\n        if (count === 0) return { mttr_minutes: 0, mttr_display: \"No data\", sample_size: 0 };\n        var avgMinutes = Math.round(totalMinutes / count);\n        var hours = Math.floor(avgMinutes / 60);\n        var mins = avgMinutes % 60;\n        return { mttr_minutes: avgMinutes, mttr_display: hours + \"h \" + mins + \"m\", sample_size: count };\n    },\n    isVIPCaller: function(userSysId) {\n        if (!userSysId) return false;\n        var gr = new GlideRecord(\"sys_user\");\n        if (gr.get(userSysId)) return gr.vip.toString() === \"true\";\n        return false;\n    },\n    isRecurringIssue: function(ciSysId, threshold, days) {\n        threshold = threshold || 3;\n        days = days || 30;\n        var result = this.getRelatedIncidents(ciSysId, days);\n        return result.count >= threshold;\n    },\n    type: \"UPIUtils\"\n};"
  }' \
  | python3 -m json.tool
```

### 21.7 Create UI Action — Escalate to P1

```bash
# UI: System Definition > UI Actions > New
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_ui_action" \
  -d '{
    "name": "Escalate to P1",
    "table": "incident",
    "action_name": "npci_escalate_p1",
    "active": "true",
    "show_insert": "false",
    "show_update": "true",
    "form_button": "true",
    "hint": "Escalate this incident to Priority 1 - Critical",
    "order": "50",
    "condition": "current.priority != 1",
    "script": "if (typeof window == \"undefined\") {\n    current.impact = 1;\n    current.urgency = 1;\n    current.work_notes = \"Incident escalated to P1 Critical by \" + gs.getUserDisplayName() + \". Manual escalation via UI Action.\";\n    current.escalation = 1;\n    current.update();\n    gs.addInfoMessage(\"Incident \" + current.number + \" has been escalated to P1 Critical.\");\n    action.setRedirectURL(current);\n}"
  }' \
  | python3 -m json.tool
```

### 21.8 Query Existing Client Scripts on Incident Table

```bash
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_script_client?sysparm_query=table=incident^nameLIKENPCI&sysparm_fields=sys_id,name,type,fieldname,active&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### 21.9 Query Existing UI Policies on Incident Table

```bash
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_ui_policy?sysparm_query=table=incident^short_descriptionLIKENPCI&sysparm_fields=sys_id,short_description,active,conditions,reverse_if_false&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

---

## Lab 22: REST API, Integration Hub & Update Sets

> **UI Equivalent:** This IS the API lab. Lab 22 covers inbound/outbound REST,
> Scripted REST APIs, Attachment API, CMDB API, Update Sets, and ATF.
> Below is the complete API lifecycle.

### 22.1 Full CRUD Lifecycle — Incident

#### Create (POST)

```bash
# UI: Incident > Create New
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/incident" \
  -d '{
    "short_description": "UPI Payment Gateway connection timeout — merchant transactions failing",
    "description": "Prometheus alert fired: UPI Payment Gateway returning HTTP 504 for 80% of transactions.\nAffected merchants: PhonePe, Google Pay, Paytm.\nAlert source: AlertManager via Snow Bridge.\nDashboard: http://grafana:3000/d/upi-gateway",
    "category": "Software",
    "impact": "1",
    "urgency": "1",
    "assignment_group": "Platform Engineering",
    "caller_id": "admin",
    "cmdb_ci": "UPI Transaction Service",
    "work_notes": "[API] Incident created via REST API from monitoring integration."
  }' \
  | python3 -m json.tool
```

```bash
# Save the sys_id for subsequent operations
export INC_SYS_ID="<sys_id from the POST response>"
```

#### Read (GET) — Single Record

```bash
# UI: Open incident form
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/incident/$INC_SYS_ID?sysparm_fields=number,short_description,description,priority,state,impact,urgency,assignment_group,assigned_to,category,cmdb_ci,opened_at,work_notes&sysparm_display_value=all" \
  | python3 -m json.tool
```

#### Full Update (PUT)

```bash
# UI: Open incident > modify ALL fields > save
# WARNING: PUT replaces the record — any unset field reverts to default
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PUT \
  "$SNOW/api/now/table/incident/$INC_SYS_ID" \
  -d '{
    "short_description": "UPI Payment Gateway connection timeout — merchant transactions failing",
    "description": "Prometheus alert fired: UPI Payment Gateway returning HTTP 504 for 80% of transactions.",
    "state": "2",
    "assigned_to": "admin",
    "category": "Software",
    "impact": "1",
    "urgency": "1",
    "assignment_group": "Platform Engineering",
    "caller_id": "admin",
    "cmdb_ci": "UPI Transaction Service",
    "work_notes": "Investigation started. Checking Payment Gateway connection pool and upstream PSP connectivity."
  }' \
  | python3 -m json.tool
```

#### Partial Update (PATCH) — Preferred

```bash
# UI: Open incident > modify specific fields > save
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/incident/$INC_SYS_ID" \
  -d '{
    "state": "6",
    "close_code": "Solved (Permanently)",
    "close_notes": "Root cause: Payment Gateway connection pool max_size was set to 10. Under peak UPI traffic (2000+ TPS), pool exhausted within seconds. Fix: Increased max_size to 100 and added connection keepalive. Verified recovery via Grafana — P95 latency back to 120ms.",
    "work_notes": "Incident resolved. Connection pool scaled from 10 to 100. Monitoring confirms stable performance. Post-incident review scheduled for tomorrow."
  }' \
  | python3 -m json.tool
```

#### Delete

```bash
# WARNING: Rarely used in ITSM. Use state=Closed instead.
# Only for test data cleanup on PDI.
curl -s -u "$AUTH" \
  -X DELETE \
  "$SNOW/api/now/table/incident/$INC_SYS_ID"

# Expected: 204 No Content (no response body)
```

### 22.2 Aggregate API — Comprehensive Statistics

```bash
# Count incidents grouped by priority (for dashboard KPIs)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=active=true&sysparm_count=true&sysparm_group_by=priority&sysparm_display_value=true" \
  | python3 -m json.tool
```

```bash
# Average and max resolution time
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_query=stateIN6,7&sysparm_avg_fields=calendar_duration&sysparm_max_fields=calendar_duration&sysparm_count=true" \
  | python3 -m json.tool
```

```bash
# Count incidents with two groupby dimensions (priority + state)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_count=true&sysparm_group_by=priority,state&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 22.3 Attachment API — Upload and Download

```bash
# Upload a file to an incident
curl -s -u "$AUTH" \
  -H "Content-Type: text/plain" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/attachment/file?table_name=incident&table_sys_id=$INC_SYS_ID&file_name=upi-gateway-error-log.txt" \
  --data-binary @/tmp/error-log.txt \
  | python3 -m json.tool
```

```bash
# List attachments on a record
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/attachment?sysparm_query=table_name=incident^table_sys_id=$INC_SYS_ID&sysparm_fields=sys_id,file_name,content_type,size_bytes" \
  | python3 -m json.tool
```

```bash
# Download an attachment
export ATTACH_SYS_ID="<sys_id of the attachment>"
curl -s -u "$AUTH" \
  -H "Accept: */*" \
  "$SNOW/api/now/attachment/$ATTACH_SYS_ID/file" \
  -o downloaded-file.txt
```

### 22.4 CMDB API — Query Configuration Items

```bash
# List all servers in CMDB
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/cmdb/instance/cmdb_ci_server?sysparm_fields=name,operational_status,os,ip_address,support_group&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

```bash
# Query all CIs with name containing "UPI"
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_ci?sysparm_query=nameLIKEUPI&sysparm_fields=name,sys_class_name,operational_status,support_group,busines_criticality&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

```bash
# Get CI relationships (dependencies)
CI_SYS_ID=$(curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_ci?sysparm_query=name=UPI Transaction Service&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/cmdb_rel_ci?sysparm_query=parent=$CI_SYS_ID&sysparm_fields=parent,child,type&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### 22.5 Update Sets — Create, Manage, and Export

```bash
# UI: System Update Sets > Local Update Sets
# List existing update sets
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_update_set?sysparm_fields=name,state,description,application&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

```bash
# Create a new update set
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_update_set" \
  -d '{
    "name": "NPCI UPI ITSM Configuration v1.0",
    "description": "Contains all Business Rules, Client Scripts, UI Policies, Script Includes, and UI Actions from Labs 17-22 for the NPCI UPI Platform ITSM implementation.",
    "state": "in progress"
  }' \
  | python3 -m json.tool
```

```bash
export UPDATE_SET_ID="<sys_id from response>"
```

```bash
# Make this the current update set (so new changes are captured in it)
# This is done by setting it on the user preference — typically done via UI
# but you can PATCH the sys_update_set record state:
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/sys_update_set/$UPDATE_SET_ID" \
  -d '{"state": "in progress"}' \
  | python3 -m json.tool
```

```bash
# Query customer updates captured in the update set
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_update_xml?sysparm_query=update_set=$UPDATE_SET_ID&sysparm_fields=name,type,target_name,action&sysparm_display_value=true&sysparm_limit=50" \
  | python3 -m json.tool
```

```bash
# Complete (close) the update set
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/sys_update_set/$UPDATE_SET_ID" \
  -d '{"state": "complete"}' \
  | python3 -m json.tool
```

> **Note:** Update Set XML export is a UI-only operation. Navigate to
> System Update Sets > Local Update Sets > open the set > Related Links >
> "Export to XML" to download the XML file for importing into another instance.

### 22.6 Scripted REST API — Query and Create

```bash
# Query existing Scripted REST APIs
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_ws_definition?sysparm_fields=sys_id,name,api_id,active&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

```bash
# Create a new Scripted REST API definition
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_ws_definition" \
  -d '{
    "name": "UPI Integration API",
    "api_id": "upi_integration",
    "active": "true",
    "short_description": "Custom REST API for NPCI UPI platform integrations — health check, incident summary, and CI status endpoints."
  }' \
  | python3 -m json.tool
```

```bash
# Query Scripted REST API resources (endpoints)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_ws_operation?sysparm_fields=sys_id,name,http_method,relative_path,web_service_definition&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

### 22.7 ATF — Automated Test Framework

```bash
# Query ATF test suites
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_atf_test_suite?sysparm_fields=sys_id,name,description,active&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -m json.tool
```

```bash
# Query ATF test results (most recent)
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_atf_test_result?sysparm_fields=test,status,start_time,end_time,duration&sysparm_display_value=true&sysparm_query=ORDERBYDESCstart_time&sysparm_limit=20" \
  | python3 -m json.tool
```

```bash
# Run an ATF test suite via API (if supported on your instance)
# Note: Not all instances support ATF execution via REST.
# The standard approach is: ATF > Tests > Run
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/sys_atf_test_suite_run" \
  -d '{
    "test_suite": "<test_suite_sys_id>"
  }' \
  | python3 -m json.tool 2>/dev/null || echo "ATF suite execution via API may not be available on this instance. Use the ATF UI instead."
```

### 22.8 Full Integration Scenario — Monitoring to Incident to Resolution

```bash
#!/bin/bash
# ============================================================
# End-to-end integration scenario: Alert -> Incident -> Resolve
# Simulates what Snow Bridge does when Prometheus fires an alert
# ============================================================

echo "=== Step 1: Create incident from monitoring alert ==="
RESPONSE=$(curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "$SNOW/api/now/table/incident" \
  -d '{
    "short_description": "UPI Transaction Service P95 latency > 500ms",
    "description": "AlertManager: upi_latency_high\nCurrent P95: 823ms\nThreshold: 500ms\nDuration: 5m\nSource: prometheus/alertmanager",
    "category": "Software",
    "impact": "2",
    "urgency": "1",
    "assignment_group": "Platform Engineering",
    "caller_id": "admin",
    "cmdb_ci": "UPI Transaction Service",
    "work_notes": "[ALERT] Auto-created from Prometheus AlertManager via REST API."
  }')

INC_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")
INC_NUM=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['number'])")
echo "Created: $INC_NUM (sys_id: $INC_ID)"

echo ""
echo "=== Step 2: Assign and acknowledge ==="
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/incident/$INC_ID" \
  -d '{
    "state": "2",
    "assigned_to": "admin",
    "work_notes": "Acknowledged. Checking Grafana dashboard for latency patterns."
  }' | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f'State: {r[\"state\"]}, Assigned: {r[\"assigned_to\"]}')"

echo ""
echo "=== Step 3: Add diagnostic work notes ==="
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/incident/$INC_ID" \
  -d '{
    "work_notes": "Diagnostics: DB connection pool at 95% capacity. Query execution time spiked from 5ms to 200ms. Root cause: long-running settlement query holding connections."
  }' > /dev/null

echo "Work notes added."

echo ""
echo "=== Step 4: Resolve incident ==="
curl -s -u "$AUTH" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "$SNOW/api/now/table/incident/$INC_ID" \
  -d '{
    "state": "6",
    "close_code": "Solved (Permanently)",
    "close_notes": "Root cause: Long-running settlement reconciliation query (45s) holding DB connections. Fixed by adding query timeout of 10s and optimizing the settlement query with proper indexing. P95 latency recovered to 120ms within 2 minutes of fix deployment.",
    "work_notes": "[RESOLVED] Latency recovered. P95 back to 120ms. Settlement query optimized."
  }' | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f'State: {r[\"state\"]}, Close Code: {r.get(\"close_code\",\"N/A\")}')"

echo ""
echo "=== Step 5: Verify the incident ==="
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/incident/$INC_ID?sysparm_fields=number,short_description,state,priority,close_code,close_notes,assignment_group,assigned_to&sysparm_display_value=true" \
  | python3 -m json.tool

echo ""
echo "=== Integration scenario complete ==="
```

### 22.9 Verification Queries — Confirm All Lab Artifacts

```bash
echo "=== Verification: Business Rules ==="
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/sys_script?sysparm_query=nameLIKENPCI^active=true&sysparm_count=true" \
  | python3 -c "import sys,json; print('Active NPCI Business Rules:', json.load(sys.stdin)['result']['stats']['count'])"

echo ""
echo "=== Verification: Client Scripts ==="
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/sys_script_client?sysparm_query=nameLIKENPCI^active=true&sysparm_count=true" \
  | python3 -c "import sys,json; print('Active NPCI Client Scripts:', json.load(sys.stdin)['result']['stats']['count'])"

echo ""
echo "=== Verification: UI Policies ==="
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/sys_ui_policy?sysparm_query=short_descriptionLIKENPCI^active=true&sysparm_count=true" \
  | python3 -c "import sys,json; print('Active NPCI UI Policies:', json.load(sys.stdin)['result']['stats']['count'])"

echo ""
echo "=== Verification: Script Includes ==="
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/sys_script_include?sysparm_query=nameLIKEUPI^active=true&sysparm_count=true" \
  | python3 -c "import sys,json; print('Active UPI Script Includes:', json.load(sys.stdin)['result']['stats']['count'])"

echo ""
echo "=== Verification: UI Actions ==="
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/sys_ui_action?sysparm_query=nameLIKENPCI^ORnameLIKEEscalate^active=true&sysparm_count=true" \
  | python3 -c "import sys,json; print('Active NPCI UI Actions:', json.load(sys.stdin)['result']['stats']['count'])"

echo ""
echo "=== Verification: Update Sets ==="
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/sys_update_set?sysparm_query=nameLIKENPCI&sysparm_fields=name,state&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool

echo ""
echo "=== Verification: Improvement Records ==="
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/table/improvement?sysparm_fields=number,short_description,state,priority&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool

echo ""
echo "=== Verification: Incident Statistics ==="
curl -s -u "$AUTH" \
  -H "Accept: application/json" \
  "$SNOW/api/now/stats/incident?sysparm_count=true&sysparm_group_by=state&sysparm_display_value=true" \
  | python3 -m json.tool
```

---

## Quick Reference: API Endpoints Used

```
Table API (CRUD):
  GET    /api/now/table/{table}              List records
  GET    /api/now/table/{table}/{sys_id}     Get single record
  POST   /api/now/table/{table}              Create record
  PUT    /api/now/table/{table}/{sys_id}     Full update
  PATCH  /api/now/table/{table}/{sys_id}     Partial update
  DELETE /api/now/table/{table}/{sys_id}     Delete record

Aggregate API (Statistics):
  GET    /api/now/stats/{table}              Count, Avg, Min, Max, Sum

Attachment API:
  POST   /api/now/attachment/file            Upload file
  GET    /api/now/attachment/{sys_id}/file   Download file
  GET    /api/now/attachment                 List attachments

CMDB API:
  GET    /api/now/cmdb/instance/{class}      Query CIs by class

Key Tables Used in This Companion:
  incident              Incident Management
  problem               Problem Management
  change_request        Change Management
  task_sla              SLA tracking per task
  cmdb_ci               Configuration Items
  cmdb_rel_ci           CI relationships
  improvement           Continual Improvement (CIM plugin)
  sys_report            Report definitions
  sys_script            Business Rules
  sys_script_client     Client Scripts
  sys_script_include    Script Includes
  sys_ui_policy         UI Policies
  sys_ui_policy_action  UI Policy Actions
  sys_ui_action         UI Actions (buttons/links)
  sys_update_set        Update Sets
  sys_update_xml        Customer updates in update sets
  sys_hub_flow          Flow Designer flows
  sys_ws_definition     Scripted REST API definitions
  sys_ws_operation      Scripted REST API resources
  sysauto_script        Scheduled Jobs
  sysevent_email_action Email Notifications
  sys_atf_test_suite    ATF Test Suites
  sys_atf_test_result   ATF Test Results
  v_plugin              Plugin registry
  u_availability_record Custom availability table (Lab 19)
  u_capacity_record     Custom capacity table (Lab 19)
```

---

*API Companion for Phase 4 (Optimize) & Phase 5 (Automate) — Labs 17-22*
*NPCI UPI Platform ITSM Implementation*
