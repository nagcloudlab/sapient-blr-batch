# Phase 3: Operate -- REST API Companion (Labs 12-16)

Every UI action from Labs 12-16 expressed as a curl command against the
ServiceNow Table API. Run these sequentially; later commands reference
sys_ids captured from earlier responses.

---

## Setup -- Credentials and Environment

```bash
export SNOW="https://YOUR-INSTANCE.service-now.com"
export AUTH="admin:YOUR-PASSWORD"

# Shorthand for common headers
alias snowget='curl -s -u "$AUTH" -H "Accept: application/json"'
alias snowpost='curl -s -u "$AUTH" -H "Content-Type: application/json" -H "Accept: application/json"'
alias snowpatch='curl -s -u "$AUTH" -H "Content-Type: application/json" -H "Accept: application/json" -X PATCH'
alias snowdelete='curl -s -u "$AUTH" -X DELETE'
```

> **Tip:** Pipe any command through `| python3 -m json.tool` for pretty output,
> or `| jq .` if jq is installed.

---

## Lab 12: Deploy Demo Stack and Event Management

The demo stack itself runs in Docker (Prometheus, Grafana, AlertManager,
Snow Bridge, UPI services). The API companion focuses on the ServiceNow
side -- verifying incidents created by the pipeline, testing the webhook
manually, and working with the event management table.

### 12.1 Verify the Snow Bridge webhook is reachable

```bash
# UI equivalent: Open http://localhost:5005/health in browser
curl -s http://localhost:5005/health | python3 -m json.tool
```

### 12.2 Test Snow Bridge -- create a test incident via webhook

```bash
# UI equivalent: Snow Bridge receives AlertManager webhook and creates
#                an incident in ServiceNow automatically.
# Here we call the test-incident endpoint directly.

curl -s -X POST http://localhost:5005/test-incident \
  -H "Content-Type: application/json" \
  -d '{
    "severity": "critical",
    "summary": "UPI Gateway Down - Manual API Test"
  }' | python3 -m json.tool
```

### 12.3 Check active alerts tracked by Snow Bridge

```bash
# UI equivalent: View AlertManager UI at http://localhost:9093
curl -s http://localhost:5005/active-alerts | python3 -m json.tool
```

### 12.4 Query auto-created incidents in ServiceNow

```bash
# UI equivalent: Incident > All, filter Short description contains "[AUTO]"
snowget "$SNOW/api/now/table/incident?sysparm_query=short_descriptionLIKE%5BAUTO%5D&sysparm_fields=number,short_description,priority,state,assignment_group.name,sys_created_on&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 12.5 Create an event record via REST API

```bash
# UI equivalent: Event Management > Create Event (em_event table)
# If em_event is not available on your PDI, skip this step.

snowpost -X POST "$SNOW/api/now/table/em_event" \
  -d '{
    "source": "Prometheus",
    "node": "upi-transaction-service",
    "type": "UPI High Failure Rate",
    "severity": "1",
    "description": "Transaction failure rate exceeded 50% on UPI Transaction Service. Detected by Prometheus alert UpiHighTransactionFailureRate.",
    "additional_info": "{\"alert\":\"UpiHighTransactionFailureRate\",\"current_value\":\"82%\",\"threshold\":\"50%\",\"service\":\"upi-transaction-service:8081\"}"
  }' | python3 -m json.tool

# Capture the sys_id
export EVENT_ID=$(snowpost -X POST "$SNOW/api/now/table/em_event" \
  -d '{
    "source": "Prometheus",
    "node": "upi-settlement-service",
    "type": "UPI Settlement Failures",
    "severity": "3",
    "description": "Settlement service recording failures downstream of transaction service."
  }' | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")
echo "Event sys_id: $EVENT_ID"
```

### 12.6 Query event management table

```bash
# UI equivalent: Event Management > All Events
snowget "$SNOW/api/now/table/em_event?sysparm_query=sourceLIKEPrometheus&sysparm_fields=number,source,node,type,severity,description&sysparm_limit=10" \
  | python3 -m json.tool
```

### 12.7 Verify Prometheus alert-to-incident mapping

```bash
# After chaos injection, verify the pipeline worked end-to-end.
# Check for the critical alert incident.

snowget "$SNOW/api/now/table/incident?sysparm_query=short_descriptionLIKEtransaction%20failure%20rate&sysparm_fields=number,short_description,priority,impact,urgency,state,assignment_group.name&sysparm_display_value=true&sysparm_limit=5" \
  | python3 -m json.tool
```

### 12.8 Cleanup -- close test incidents

```bash
# Find and close any test incidents created by the webhook test
snowget "$SNOW/api/now/table/incident?sysparm_query=short_descriptionLIKEManual%20API%20Test&sysparm_fields=sys_id,number" \
  | python3 -m json.tool

# Close a specific test incident (replace SYS_ID)
# snowpatch "$SNOW/api/now/table/incident/SYS_ID" \
#   -d '{"state":"7","close_code":"Solved (Permanently)","close_notes":"Test incident from API companion."}'
```

---

## Lab 13: Incident Management -- Full Lifecycle

This is the most detailed section. It replicates every UI action from
Lab 13 (referenced as Lab 07 in the phase-3-operate directory).

### 13.1 Ensure required groups exist

```bash
# UI equivalent: User Administration > Groups > New
# Create groups used across all incidents

for GROUP in "Service Desk" "Network" "Hardware" "Software" "Database" "Platform Engineering"; do
  snowpost -X POST "$SNOW/api/now/table/sys_user_group" \
    -d "{\"name\":\"$GROUP\",\"active\":\"true\"}" 2>/dev/null
done

# Capture group sys_ids for later use
export GRP_SVCDESK=$(snowget "$SNOW/api/now/table/sys_user_group?sysparm_query=name=Service%20Desk&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

export GRP_NETWORK=$(snowget "$SNOW/api/now/table/sys_user_group?sysparm_query=name=Network&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

export GRP_HARDWARE=$(snowget "$SNOW/api/now/table/sys_user_group?sysparm_query=name=Hardware&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

export GRP_SOFTWARE=$(snowget "$SNOW/api/now/table/sys_user_group?sysparm_query=name=Software&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

export GRP_DATABASE=$(snowget "$SNOW/api/now/table/sys_user_group?sysparm_query=name=Database&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

export GRP_PLATFORM=$(snowget "$SNOW/api/now/table/sys_user_group?sysparm_query=name=Platform%20Engineering&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['sys_id'])")

echo "Service Desk: $GRP_SVCDESK"
echo "Network:      $GRP_NETWORK"
echo "Hardware:     $GRP_HARDWARE"
echo "Software:     $GRP_SOFTWARE"
echo "Database:     $GRP_DATABASE"
echo "Platform Eng: $GRP_PLATFORM"
```

### 13.2 Look up demo user sys_ids

```bash
# UI equivalent: Searching for a user in the Caller field
export USER_ABEL=$(snowget "$SNOW/api/now/table/sys_user?sysparm_query=nameLIKEAbel%20Tuter&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['sys_id'] if r else '')")

export USER_BETH=$(snowget "$SNOW/api/now/table/sys_user?sysparm_query=nameLIKEBeth%20Anglin&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['sys_id'] if r else '')")

export USER_DAVID=$(snowget "$SNOW/api/now/table/sys_user?sysparm_query=nameLIKEDavid%20Loo&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['sys_id'] if r else '')")

export USER_FRED=$(snowget "$SNOW/api/now/table/sys_user?sysparm_query=nameLIKEFred%20Luddy&sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['sys_id'] if r else '')")

echo "Abel:  $USER_ABEL"
echo "Beth:  $USER_BETH"
echo "David: $USER_DAVID"
echo "Fred:  $USER_FRED"
```

---

### 13.3 COMPLETE INCIDENT LIFECYCLE (9-step walkthrough)

#### Step 1: CREATE incident

```bash
# UI equivalent: Incident > Create New, fill form, click Submit
export INC1_ID=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"caller_id\": \"$USER_ABEL\",
    \"category\": \"software\",
    \"subcategory\": \"email\",
    \"short_description\": \"Unable to access email from mobile device\",
    \"description\": \"User reports that email on iPhone has stopped syncing after latest update. Tried restarting the device. All other apps work fine.\",
    \"impact\": \"2\",
    \"urgency\": \"2\",
    \"assignment_group\": \"$GRP_SVCDESK\",
    \"assigned_to\": \"$USER_BETH\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['sys_id'])")

export INC1_NUM=$(snowget "$SNOW/api/now/table/incident/$INC1_ID?sysparm_fields=number" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['number'])")

echo "Created incident: $INC1_NUM (sys_id: $INC1_ID)"
```

#### Step 2: READ incident back

```bash
# UI equivalent: Open the incident form to view all fields
snowget "$SNOW/api/now/table/incident/$INC1_ID?sysparm_display_value=true&sysparm_fields=number,short_description,state,priority,impact,urgency,category,subcategory,caller_id,assignment_group,assigned_to,sys_created_on" \
  | python3 -m json.tool
```

#### Step 3: UPDATE state to In Progress

```bash
# UI equivalent: Change State dropdown from "New" to "In Progress", click Update
snowpatch "$SNOW/api/now/table/incident/$INC1_ID" \
  -d '{"state":"2"}' | python3 -m json.tool
```

#### Step 4: ADD work notes

```bash
# UI equivalent: Type in the Activity / Work notes field, click Update
snowpatch "$SNOW/api/now/table/incident/$INC1_ID" \
  -d '{"work_notes":"Investigating email sync issue on user mobile device. Checking Exchange ActiveSync connectivity and certificate status."}' \
  | python3 -c "import sys,json; print('Work note added to', json.load(sys.stdin)['result']['number'])"

# Add a second work note
snowpatch "$SNOW/api/now/table/incident/$INC1_ID" \
  -d '{"work_notes":"Root cause found: Exchange ActiveSync profile corrupted after iOS update. Recreating the mail profile."}' \
  | python3 -c "import sys,json; print('Second work note added to', json.load(sys.stdin)['result']['number'])"
```

#### Step 5: ASSIGN to group and user

```bash
# UI equivalent: Change Assignment group and Assigned to fields
snowpatch "$SNOW/api/now/table/incident/$INC1_ID" \
  -d "{
    \"assignment_group\": \"$GRP_SOFTWARE\",
    \"assigned_to\": \"$USER_BETH\",
    \"work_notes\": \"Reassigning to Software team -- requires Exchange server-side investigation.\"
  }" | python3 -c "import sys,json; print('Reassigned', json.load(sys.stdin)['result']['number'])"
```

#### Step 6: ESCALATE priority (P3 to P1)

```bash
# UI equivalent: Change Impact to 1-High, Urgency to 1-High
# Priority auto-calculates: Impact 1 x Urgency 1 = Priority 1 (Critical)
snowpatch "$SNOW/api/now/table/incident/$INC1_ID" \
  -d '{
    "impact": "1",
    "urgency": "1",
    "work_notes": "Escalating to P1 -- multiple users now reporting same email sync failure. Affects entire department."
  }' | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f'Priority now: {r[\"priority\"]}')"
```

#### Step 7: LINK to Configuration Item

```bash
# UI equivalent: Click magnifying glass on Configuration item field, select a CI
# First, find a CI to link to
export CI_ID=$(snowget "$SNOW/api/now/table/cmdb_ci?sysparm_query=nameLIKEEmail%20Server&sysparm_fields=sys_id,name&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['sys_id'] if r else '')")

# If no Email Server CI exists, search for any available CI
if [ -z "$CI_ID" ]; then
  export CI_ID=$(snowget "$SNOW/api/now/table/cmdb_ci?sysparm_fields=sys_id,name&sysparm_limit=1" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['sys_id'] if r else '')")
fi

snowpatch "$SNOW/api/now/table/incident/$INC1_ID" \
  -d "{\"cmdb_ci\": \"$CI_ID\"}" \
  | python3 -c "import sys,json; print('CI linked to', json.load(sys.stdin)['result']['number'])"
```

#### Step 8: RESOLVE incident

```bash
# UI equivalent: Change State to Resolved, fill Resolution code and notes
snowpatch "$SNOW/api/now/table/incident/$INC1_ID" \
  -d '{
    "state": "6",
    "close_code": "Solved (Permanently)",
    "close_notes": "Exchange ActiveSync profile was corrupted after iOS 17.5 update. Deleted and recreated the mail profile on user device. Email syncing normally. Applied Exchange server-side workaround to prevent recurrence on other devices.",
    "work_notes": "Incident resolved. Applied permanent fix on Exchange server."
  }' | python3 -c "import sys,json; print('Resolved:', json.load(sys.stdin)['result']['number'])"
```

#### Step 9: CLOSE incident

```bash
# UI equivalent: Change State to Closed
snowpatch "$SNOW/api/now/table/incident/$INC1_ID" \
  -d '{
    "state": "7",
    "close_notes": "Confirmed email is syncing normally. No further reports from users. Closing."
  }' | python3 -c "import sys,json; print('Closed:', json.load(sys.stdin)['result']['number'])"
```

---

### 13.4 Create a P1 Critical Incident (VPN outage)

```bash
# UI equivalent: Incident > Create New with Impact=1-High, Urgency=1-High
export INC_VPN_ID=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"caller_id\": \"$USER_DAVID\",
    \"category\": \"network\",
    \"subcategory\": \"vpn\",
    \"short_description\": \"VPN service down - all remote users affected\",
    \"description\": \"VPN gateway is unreachable. Over 500 remote users cannot connect. Started at 9:00 AM.\",
    \"impact\": \"1\",
    \"urgency\": \"1\",
    \"assignment_group\": \"$GRP_NETWORK\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['sys_id'])")

echo "VPN Incident: $INC_VPN_ID"
```

---

### 13.5 Create 6 realistic UPI incidents across all priorities

```bash
# UI equivalent: Create New incident for each, with different Impact/Urgency combos

# --- INC-UPI-1: P1 Critical (Impact=1, Urgency=1) ---
export INC_UPI1=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"UPI payment gateway unreachable - all transactions failing\",
    \"description\": \"NPCI UPI switch is returning connection refused on port 443. No transactions processing. Estimated 500+ TPS impacted. All 350+ member banks affected.\",
    \"category\": \"network\",
    \"impact\": \"1\",
    \"urgency\": \"1\",
    \"assignment_group\": \"$GRP_PLATFORM\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['sys_id'])")
echo "P1 UPI Incident (gateway down): $INC_UPI1"

# --- INC-UPI-2: P2 High (Impact=1, Urgency=2) ---
export INC_UPI2=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"UPI settlement batch job stuck - end-of-day reconciliation delayed\",
    \"description\": \"Nightly settlement batch has been running for 4 hours (normal: 45 min). 12 million transactions pending reconciliation. Member banks awaiting settlement confirmation.\",
    \"category\": \"software\",
    \"impact\": \"1\",
    \"urgency\": \"2\",
    \"assignment_group\": \"$GRP_PLATFORM\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['sys_id'])")
echo "P2 UPI Incident (settlement stuck): $INC_UPI2"

# --- INC-UPI-3: P3 Moderate (Impact=2, Urgency=2) ---
export INC_UPI3=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"UPI collect requests showing 30-second delay for HDFC Bank VPAs\",
    \"description\": \"Collect payment requests initiated by HDFC Bank VPAs are experiencing 30s+ latency. P2P and P2M payments from other banks unaffected. Approx 50K users impacted.\",
    \"category\": \"software\",
    \"impact\": \"2\",
    \"urgency\": \"2\",
    \"assignment_group\": \"$GRP_PLATFORM\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['sys_id'])")
echo "P3 UPI Incident (HDFC delay): $INC_UPI3"

# --- INC-UPI-4: P3 Moderate (Impact=3, Urgency=1) ---
export INC_UPI4=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"UPI QR code generation returning blurred images on merchant app\",
    \"description\": \"Merchants using UPI QR code generation API v2 are seeing low-resolution QR codes that fail to scan on older phone cameras. New API version available but merchant adoption is low.\",
    \"category\": \"software\",
    \"impact\": \"3\",
    \"urgency\": \"1\",
    \"assignment_group\": \"$GRP_SOFTWARE\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['sys_id'])")
echo "P3 UPI Incident (QR blurred): $INC_UPI4"

# --- INC-UPI-5: P4 Low (Impact=2, Urgency=3) ---
export INC_UPI5=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"UPI transaction history API returning stale data for last 24h\",
    \"description\": \"The /api/upi/history endpoint returns cached results from yesterday. Users see outdated transaction list. Payments themselves are processing correctly.\",
    \"category\": \"software\",
    \"impact\": \"2\",
    \"urgency\": \"3\",
    \"assignment_group\": \"$GRP_SOFTWARE\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['sys_id'])")
echo "P4 UPI Incident (stale history): $INC_UPI5"

# --- INC-UPI-6: P5 Planning (Impact=3, Urgency=3) ---
export INC_UPI6=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"UPI merchant dashboard CSV export truncates at 10000 rows\",
    \"description\": \"Large merchants with 10K+ daily transactions cannot export full transaction reports. Pagination not implemented in CSV export. Workaround: use date range filters to reduce rows.\",
    \"category\": \"software\",
    \"impact\": \"3\",
    \"urgency\": \"3\",
    \"assignment_group\": \"$GRP_SOFTWARE\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['sys_id'])")
echo "P5 UPI Incident (CSV export): $INC_UPI6"
```

### 13.6 Priority matrix demonstration

```bash
# The priority matrix: Impact x Urgency = Priority
# P1=Critical, P2=High, P3=Moderate, P4=Low, P5=Planning
#
#                     Impact
#                 1-High  2-Medium  3-Low
# Urgency 1-High    1        2        3
#         2-Medium  2        3        4
#         3-Low     3        4        5

# Verify the priority was calculated correctly for each incident
echo "=== Priority Matrix Verification ==="
for INC_ID in $INC_UPI1 $INC_UPI2 $INC_UPI3 $INC_UPI4 $INC_UPI5 $INC_UPI6; do
  snowget "$SNOW/api/now/table/incident/$INC_ID?sysparm_fields=number,short_description,impact,urgency,priority&sysparm_display_value=true" \
    | python3 -c "
import sys,json
r=json.load(sys.stdin)['result']
print(f\"{r['number']}  Impact={r['impact']}  Urgency={r['urgency']}  => Priority={r['priority']}\")
print(f\"  {r['short_description'][:70]}\")
"
done
```

### 13.7 Query incidents by various filters

```bash
# UI equivalent: Incident > All, then use filter builder

# --- All open P1 incidents ---
echo "=== Open P1 Incidents ==="
snowget "$SNOW/api/now/table/incident?sysparm_query=priority=1^stateNOT%20IN6,7&sysparm_fields=number,short_description,state,assignment_group&sysparm_display_value=true" \
  | python3 -m json.tool

# --- All incidents for Platform Engineering group ---
echo "=== Platform Engineering Incidents ==="
snowget "$SNOW/api/now/table/incident?sysparm_query=assignment_group=$GRP_PLATFORM&sysparm_fields=number,short_description,priority,state&sysparm_display_value=true" \
  | python3 -m json.tool

# --- Incidents with UPI in description ---
echo "=== UPI-related Incidents ==="
snowget "$SNOW/api/now/table/incident?sysparm_query=short_descriptionLIKEUPI&sysparm_fields=number,short_description,priority,state&sysparm_display_value=true" \
  | python3 -m json.tool

# --- Unassigned incidents (no assigned_to) ---
echo "=== Unassigned Incidents ==="
snowget "$SNOW/api/now/table/incident?sysparm_query=assigned_toISEMPTY^stateNOT%20IN6,7&sysparm_fields=number,short_description,priority,assignment_group&sysparm_display_value=true" \
  | python3 -m json.tool

# --- Incidents created today ---
echo "=== Incidents Created Today ==="
snowget "$SNOW/api/now/table/incident?sysparm_query=sys_created_onONToday@javascript:gs.beginningOfToday()@javascript:gs.endOfToday()&sysparm_fields=number,short_description,priority&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 13.8 Aggregate queries -- count by priority, state, assignment group

```bash
# UI equivalent: Incident > Overview -- counts and charts

# --- Count incidents by priority ---
echo "=== Incidents by Priority ==="
snowget "$SNOW/api/now/stats/incident?sysparm_count=true&sysparm_group_by=priority&sysparm_display_value=true" \
  | python3 -c "
import sys,json
for g in json.load(sys.stdin)['result']:
    print(f\"  {g['groupby_fields'][0]['display_value']}: {g['stats']['count']}\")
"

# --- Count incidents by state ---
echo "=== Incidents by State ==="
snowget "$SNOW/api/now/stats/incident?sysparm_count=true&sysparm_group_by=state&sysparm_display_value=true" \
  | python3 -c "
import sys,json
for g in json.load(sys.stdin)['result']:
    print(f\"  {g['groupby_fields'][0]['display_value']}: {g['stats']['count']}\")
"

# --- Count incidents by assignment group ---
echo "=== Incidents by Assignment Group ==="
snowget "$SNOW/api/now/stats/incident?sysparm_count=true&sysparm_group_by=assignment_group&sysparm_display_value=true" \
  | python3 -c "
import sys,json
for g in json.load(sys.stdin)['result']:
    print(f\"  {g['groupby_fields'][0]['display_value']}: {g['stats']['count']}\")
"
```

### 13.9 SLA verification -- check task_sla records

```bash
# UI equivalent: Open incident > SLA tab / Related Lists > Task SLAs
# After an incident is created, the SLA engine attaches task_sla records.

echo "=== SLA Records for P1 UPI Incident ==="
snowget "$SNOW/api/now/table/task_sla?sysparm_query=task=$INC_UPI1&sysparm_fields=sla,stage,has_breached,business_percentage,start_time,end_time&sysparm_display_value=true" \
  | python3 -m json.tool

# Check SLAs across all our UPI incidents
echo "=== SLA Breach Status (all UPI incidents) ==="
for INC_ID in $INC_UPI1 $INC_UPI2 $INC_UPI3 $INC_UPI4 $INC_UPI5 $INC_UPI6; do
  INC_NUM=$(snowget "$SNOW/api/now/table/incident/$INC_ID?sysparm_fields=number" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['number'])")
  SLAS=$(snowget "$SNOW/api/now/table/task_sla?sysparm_query=task=$INC_ID&sysparm_fields=sla,has_breached,business_percentage&sysparm_display_value=true" \
    | python3 -c "
import sys,json
for s in json.load(sys.stdin)['result']:
    print(f\"    SLA: {s['sla']}  Breached: {s['has_breached']}  Progress: {s['business_percentage']}%\")
" 2>/dev/null)
  echo "$INC_NUM:"
  echo "${SLAS:-    (no SLAs attached)}"
done
```

### 13.10 Bulk operations -- update multiple incidents at once

```bash
# UI equivalent: Select multiple incidents in list view > Actions > Update Selected

# Put all open UPI incidents to In Progress state in one loop
echo "=== Bulk Update: Move UPI incidents to In Progress ==="
for INC_ID in $INC_UPI1 $INC_UPI2 $INC_UPI3 $INC_UPI4 $INC_UPI5 $INC_UPI6; do
  snowpatch "$SNOW/api/now/table/incident/$INC_ID" \
    -d '{"state":"2","work_notes":"Bulk update via API -- moving to In Progress for triage."}' \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  {r['number']}: state -> In Progress\")"
done

# Bulk assign all P3+ UPI incidents to Platform Engineering
echo "=== Bulk Assign: All UPI incidents to Platform Engineering ==="
for INC_ID in $INC_UPI1 $INC_UPI2 $INC_UPI3 $INC_UPI4 $INC_UPI5 $INC_UPI6; do
  snowpatch "$SNOW/api/now/table/incident/$INC_ID" \
    -d "{\"assignment_group\":\"$GRP_PLATFORM\"}" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  {r['number']}: assigned to Platform Engineering\")"
done
```

### 13.11 Functional escalation simulation (L1 -> L2 -> L3)

```bash
# UI equivalent: Reassign incident from Service Desk -> Software -> Database

export INC_ESCALATE=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"Application timeout errors on internal portal\",
    \"description\": \"Users experiencing frequent timeout errors on the internal company portal. Issue affects multiple departments.\",
    \"category\": \"software\",
    \"impact\": \"2\",
    \"urgency\": \"1\",
    \"assignment_group\": \"$GRP_SVCDESK\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

# L1 triage and escalate to L2
snowpatch "$SNOW/api/now/table/incident/$INC_ESCALATE" \
  -d "{
    \"state\": \"2\",
    \"assignment_group\": \"$GRP_SOFTWARE\",
    \"work_notes\": \"L1 (Service Desk): Basic troubleshooting done. Cleared cache, verified network. Issue persists. Escalating to L2 Software team.\"
  }" | python3 -c "import sys,json; print('Escalated to L2:', json.load(sys.stdin)['result']['number'])"

# L2 investigation and escalate to L3
snowpatch "$SNOW/api/now/table/incident/$INC_ESCALATE" \
  -d "{
    \"assignment_group\": \"$GRP_DATABASE\",
    \"work_notes\": \"L2 (Software): App logs show database connection pool exhaustion. This is a database issue. Escalating to L3 DBA team.\"
  }" | python3 -c "import sys,json; print('Escalated to L3:', json.load(sys.stdin)['result']['number'])"

# L3 resolves
snowpatch "$SNOW/api/now/table/incident/$INC_ESCALATE" \
  -d '{
    "state": "6",
    "close_code": "Solved (Permanently)",
    "close_notes": "Found deadlock in transaction processing. Killed blocking sessions. Increased connection pool from 50 to 100. Issue resolved.",
    "work_notes": "L3 (Database): Deadlock resolved. Connection pool increased. Monitoring for stability."
  }' | python3 -c "import sys,json; print('Resolved by L3:', json.load(sys.stdin)['result']['number'])"
```

### 13.12 Verification -- read full activity log

```bash
# UI equivalent: Open incident > scroll to Activity Stream
# The journal fields (work_notes, comments) are in sys_journal_field

snowget "$SNOW/api/now/table/sys_journal_field?sysparm_query=element_id=$INC_ESCALATE^element=work_notes&sysparm_fields=value,sys_created_on,sys_created_by&sysparm_display_value=true" \
  | python3 -c "
import sys,json
for entry in json.load(sys.stdin)['result']:
    print(f\"[{entry['sys_created_on']}] {entry['sys_created_by']}\")
    print(f\"  {entry['value'][:120]}\")
    print()
"
```

### 13.13 Cleanup -- close all lab incidents

```bash
# Resolve and close all open UPI incidents
echo "=== Cleanup: Closing all UPI lab incidents ==="
for INC_ID in $INC_UPI1 $INC_UPI2 $INC_UPI3 $INC_UPI4 $INC_UPI5 $INC_UPI6 $INC_VPN_ID $INC_ESCALATE; do
  snowpatch "$SNOW/api/now/table/incident/$INC_ID" \
    -d '{"state":"7","close_code":"Solved (Permanently)","close_notes":"Closed by API companion cleanup."}' \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  Closed {r['number']}\")" 2>/dev/null
done
```

---

## Lab 14: Problem Management

Replicates the full problem management lifecycle from Lab 14 (referenced
as Lab 08 in the phase-3-operate directory). Uses the UPI incidents
created above.

### 14.1 CREATE problem from recurring incidents

```bash
# UI equivalent: Problem > Create New, fill form, click Submit

export PRB_ID=$(snowpost -X POST "$SNOW/api/now/table/problem" \
  -d "{
    \"short_description\": \"UPI Transaction Service recurring failures causing payment disruptions\",
    \"description\": \"Multiple incidents reported within a short time window indicating UPI Transaction Service instability:\\n- Transaction failure rate exceeded 50%\\n- Settlement service failures (downstream impact)\\n- HTTP 5xx errors on /api/upi/pay endpoint\\n- Complete service outage detected\\n\\nImpact: All UPI payment processing affected -- estimated 500+ transactions/minute.\\nDetected by: Prometheus + AlertManager monitoring stack.\\nAffected Services: UPI Transaction Service, UPI Settlement Service.\",
    \"category\": \"software\",
    \"impact\": \"1\",
    \"urgency\": \"1\",
    \"assignment_group\": \"$GRP_PLATFORM\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export PRB_NUM=$(snowget "$SNOW/api/now/table/problem/$PRB_ID?sysparm_fields=number" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['number'])")

echo "Created Problem: $PRB_NUM (sys_id: $PRB_ID)"
```

### 14.2 LINK incidents to problem

```bash
# UI equivalent: Open each incident, set Problem field to PRB number

echo "=== Linking UPI incidents to Problem $PRB_NUM ==="

# Link the auto-created monitoring incidents (if they exist)
AUTO_INC_IDS=$(snowget "$SNOW/api/now/table/incident?sysparm_query=short_descriptionLIKE%5BAUTO%5D&sysparm_fields=sys_id,number" \
  | python3 -c "
import sys,json
for r in json.load(sys.stdin)['result']:
    print(r['sys_id'])
")

for INC_ID in $AUTO_INC_IDS; do
  snowpatch "$SNOW/api/now/table/incident/$INC_ID" \
    -d "{\"problem_id\": \"$PRB_ID\"}" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  Linked {r['number']} to $PRB_NUM\")"
done

# Also link the UPI incidents we created in section 13.5
for INC_ID in $INC_UPI1 $INC_UPI2 $INC_UPI3; do
  snowpatch "$SNOW/api/now/table/incident/$INC_ID" \
    -d "{\"problem_id\": \"$PRB_ID\"}" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  Linked {r['number']} to $PRB_NUM\")" 2>/dev/null
done
```

### 14.3 Verify linked incidents

```bash
# UI equivalent: Open Problem > scroll to Related Incidents list
snowget "$SNOW/api/now/table/incident?sysparm_query=problem_id=$PRB_ID&sysparm_fields=number,short_description,priority,state&sysparm_display_value=true" \
  | python3 -c "
import sys,json
incidents = json.load(sys.stdin)['result']
print(f'Incidents linked to $PRB_NUM: {len(incidents)}')
for i in incidents:
    print(f\"  {i['number']}  P{i['priority'][0]}  {i['state']}  {i['short_description'][:60]}\")
"
```

### 14.4 UPDATE problem state through lifecycle

```bash
# UI equivalent: Click Assess button or change State dropdown

# --- New -> Assess ---
snowpatch "$SNOW/api/now/table/problem/$PRB_ID" \
  -d '{
    "state": "2",
    "work_notes": "Starting RCA for UPI Transaction Service failures.\n\nInvestigation plan:\n1. Review Prometheus metrics and Grafana dashboards at time of incident\n2. Analyze application logs from upi-transaction-service container\n3. Check for recent deployments or configuration changes\n4. Review service architecture for single points of failure"
  }' | python3 -c "import sys,json; print('State -> Assess')"

# --- Add investigation work notes ---
snowpatch "$SNOW/api/now/table/problem/$PRB_ID" \
  -d '{
    "work_notes": "Metrics analysis:\n- upi_transactions_total{status=\"failed\"} spiked from 0% to 80% instantaneously\n- Rate of change was not gradual -- something toggled failure state\n- Settlement failures cascaded within 30 seconds\n- P95 latency remained normal -- only error rate changed\n- JVM heap at 45% -- not resource exhaustion\n- No deployment recorded in change calendar\n\nConclusion: External trigger toggled service into failure state."
  }' | python3 -c "import sys,json; print('Work note added: metrics analysis')"

snowpatch "$SNOW/api/now/table/problem/$PRB_ID" \
  -d '{
    "work_notes": "Code review findings:\n- Service exposes /chaos/enable, /chaos/down, /chaos/latency endpoints\n- NO authentication or authorization on these endpoints\n- Any network-reachable client can trigger a production outage\n- Settlement Service has no circuit breaker -- failures cascade with no fallback"
  }' | python3 -c "import sys,json; print('Work note added: code review findings')"
```

### 14.5 ADD root cause analysis (cause_notes)

```bash
# UI equivalent: Click Analysis Information tab, fill in Cause notes, Fix notes, Workaround

snowpatch "$SNOW/api/now/table/problem/$PRB_ID" \
  -d '{
    "cause_notes": "ROOT CAUSE: Unprotected chaos engineering endpoints + missing circuit breaker\n\n1. The UPI Transaction Service exposes /chaos/* endpoints without any authentication or authorization. These endpoints can inject failures, latency, or complete outages into the production service.\n\n2. No circuit breaker pattern exists between the UPI Settlement Service and Transaction Service. When transactions fail, settlement requests cascade-fail with no fallback, timeout, or bulkhead isolation.\n\n3. No network segmentation prevents internal services from reaching the chaos endpoints.",
    "fix_notes": "Permanent fix (requires Change Request):\n1. SECURITY: Add Spring Security to /chaos/* endpoints -- require admin JWT token\n2. RESILIENCE: Add Resilience4j circuit breaker in Settlement Service\n3. RATE LIMITING: Add rate limiter on /api/upi/pay\n4. MONITORING: Add circuit breaker state change alerts\n5. NETWORK: Restrict /chaos/* to management network only",
    "workaround": "Immediate workaround (restores service within 30 seconds):\n1. Disable chaos: curl -X POST http://upi-transaction-service:8081/chaos/disable\n2. Verify recovery on Grafana (failure rate drops to 0%)\n3. If unresponsive: docker compose restart upi-transaction-service\n4. Monitor 15 minutes for stability"
  }' | python3 -c "import sys,json; print('RCA, workaround, and fix notes documented')"
```

### 14.6 CREATE known error

```bash
# UI equivalent: On Problem form, set known_error = true
# In Zurich PDI, known errors may be tracked via Knowledge articles.
# Here we set the known_error flag on the problem record.

snowpatch "$SNOW/api/now/table/problem/$PRB_ID" \
  -d '{
    "known_error": "true",
    "work_notes": "Marked as Known Error. Root cause identified, workaround documented. Permanent fix requires Change Request for Spring Security + Resilience4j implementation."
  }' | python3 -c "import sys,json; print('Problem marked as Known Error')"

# Verify known error status
snowget "$SNOW/api/now/table/problem/$PRB_ID?sysparm_fields=number,known_error,cause_notes,workaround&sysparm_display_value=true" \
  | python3 -c "
import sys,json
r=json.load(sys.stdin)['result']
print(f\"Problem: {r['number']}\")
print(f\"Known Error: {r['known_error']}\")
print(f\"Cause: {r['cause_notes'][:80]}...\")
print(f\"Workaround: {r['workaround'][:80]}...\")
"
```

### 14.7 Create exercise problems -- UPI QR Code problem

```bash
# --- Create 3 QR-related incidents ---
export INC_QR1=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"UPI QR code scan timeout on merchant POS terminals\",
    \"category\": \"software\",
    \"impact\": \"2\",
    \"urgency\": \"1\",
    \"assignment_group\": \"$GRP_PLATFORM\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export INC_QR2=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"QR code payment confirmation delayed by 60+ seconds\",
    \"category\": \"software\",
    \"impact\": \"2\",
    \"urgency\": \"2\",
    \"assignment_group\": \"$GRP_PLATFORM\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export INC_QR3=$(snowpost -X POST "$SNOW/api/now/table/incident" \
  -d "{
    \"short_description\": \"Merchant settlement report missing QR transactions\",
    \"category\": \"software\",
    \"impact\": \"2\",
    \"urgency\": \"2\",
    \"assignment_group\": \"$GRP_PLATFORM\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

# --- Create QR Code Problem ---
export PRB_QR_ID=$(snowpost -X POST "$SNOW/api/now/table/problem" \
  -d "{
    \"short_description\": \"UPI QR Code payment processing delays across merchant network\",
    \"description\": \"Multiple incidents related to QR code payment delays -- scan timeouts, confirmation delays, and missing transactions in settlement reports.\",
    \"category\": \"software\",
    \"impact\": \"2\",
    \"urgency\": \"1\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"cause_notes\": \"QR code validation service DNS resolver configured with expired upstream nameserver, causing 60-second timeout fallback on every DNS lookup.\",
    \"workaround\": \"Manually update /etc/resolv.conf on QR validation pods to use secondary DNS (10.0.1.53).\",
    \"known_error\": \"true\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

echo "QR Problem: $PRB_QR_ID"

# --- Link QR incidents to QR problem ---
for INC_ID in $INC_QR1 $INC_QR2 $INC_QR3; do
  snowpatch "$SNOW/api/now/table/incident/$INC_ID" \
    -d "{\"problem_id\": \"$PRB_QR_ID\"}" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  Linked {r['number']} to QR problem\")"
done
```

### 14.8 Create proactive problem (no incidents yet)

```bash
# UI equivalent: Problem > Create New for a risk identified proactively
export PRB_PROACTIVE=$(snowpost -X POST "$SNOW/api/now/table/problem" \
  -d "{
    \"short_description\": \"UPI Settlement Service single point of failure -- no redundancy\",
    \"description\": \"The settlement service runs as a single container with no redundancy. If it crashes, all UPI settlements halt. Architecture review recommends minimum 2 replicas with health-check failover.\",
    \"category\": \"software\",
    \"impact\": \"1\",
    \"urgency\": \"3\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"fix_notes\": \"Deploy with 2+ replicas behind load balancer. Add health-check based failover. Configure auto-scaling for peak transaction periods.\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"Proactive Problem: {r['number']}\")")
```

### 14.9 RESOLVE and CLOSE problem

```bash
# UI equivalent: Change State to Resolved, fill Close code and Close notes

snowpatch "$SNOW/api/now/table/problem/$PRB_ID" \
  -d '{
    "state": "4",
    "close_code": "Fix Applied",
    "close_notes": "Permanent fix deployed via Change Request. Chaos endpoints secured with Spring Security (JWT auth required). Circuit breaker added between Settlement and Transaction services. Monitoring confirms zero recurrence over 72 hours.",
    "work_notes": "Problem resolved. Fix verified in production. Closing."
  }' | python3 -c "import sys,json; print('Problem resolved and closed')"

# Verify final state
snowget "$SNOW/api/now/table/problem/$PRB_ID?sysparm_fields=number,state,known_error,close_code,close_notes&sysparm_display_value=true" \
  | python3 -m json.tool
```

### 14.10 Cleanup

```bash
# Close QR incidents and problems
for INC_ID in $INC_QR1 $INC_QR2 $INC_QR3; do
  snowpatch "$SNOW/api/now/table/incident/$INC_ID" \
    -d '{"state":"7","close_code":"Solved (Permanently)","close_notes":"Closed via API companion cleanup."}' 2>/dev/null
done

snowpatch "$SNOW/api/now/table/problem/$PRB_QR_ID" \
  -d '{"state":"4","close_code":"Fix Applied","close_notes":"DNS configuration corrected. QR payments processing normally."}' 2>/dev/null
```

---

## Lab 15: Change Management

Replicates the full change management lifecycle from Lab 15 (referenced
as Lab 09 in the phase-3-operate directory). Three change types: Normal,
Standard, and Emergency.

### 15.1 CREATE Normal Change Request

```bash
# UI equivalent: Change > Create New, Type = Normal

export CHG_NORMAL_ID=$(snowpost -X POST "$SNOW/api/now/table/change_request" \
  -d "{
    \"type\": \"normal\",
    \"short_description\": \"Secure UPI Transaction Service chaos endpoints and add circuit breaker\",
    \"description\": \"Implement security controls on chaos engineering endpoints and add Resilience4j circuit breaker to prevent cascading failures between UPI Settlement and Transaction services.\\n\\nRoot cause from Problem $PRB_NUM:\\n- Unprotected /chaos/* endpoints allow unauthorized service degradation\\n- No circuit breaker between Settlement and Transaction services\\n\\nChanges:\\n1. Spring Security on /chaos/* endpoints (admin JWT required)\\n2. Resilience4j circuit breaker in Settlement Service\\n3. Rate limiting on /api/upi/pay\\n4. Circuit breaker state change alerts in Prometheus\",
    \"category\": \"Software\",
    \"risk\": \"moderate\",
    \"impact\": \"1\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"justification\": \"Fix root cause of 4 P1/P3 incidents ($PRB_NUM). Unprotected chaos endpoints allowed unauthorized service degradation. Missing circuit breaker caused cascading settlement failures.\",
    \"implementation_plan\": \"1. Pre-implementation: Notify ops, take config backup, verify staging tests\\n2. Deploy Transaction Service v2.1 with Spring Security on /chaos/*\\n3. Deploy Settlement Service v2.1 with Resilience4j circuit breaker\\n4. Smoke test: 100 test UPI transactions\\n5. Chaos test: verify /chaos/* returns 401 without auth\\n6. Monitor 90 minutes on Grafana dashboard\",
    \"backout_plan\": \"1. Stop both services\\n2. Revert to v2.0 Docker images\\n3. Restart services and verify health\\n4. Re-apply manual workaround (monitor and disable chaos if triggered)\\n5. Notify ops of rollback\",
    \"test_plan\": \"1. Tested in staging for 5 days with production-equivalent traffic\\n2. Spring Security blocks /chaos/* without valid admin JWT\\n3. Circuit breaker opens after 5 failures, half-opens after 30s\\n4. Failed settlements queued and retried on recovery\\n5. No performance impact -- P95 latency unchanged\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export CHG_NORMAL_NUM=$(snowget "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID?sysparm_fields=number" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['number'])")

echo "Normal Change: $CHG_NORMAL_NUM (sys_id: $CHG_NORMAL_ID)"
```

### 15.2 CREATE Standard Change

```bash
# UI equivalent: Change > Create New, Type = Standard
# Standard changes are pre-approved, low-risk, routine

export CHG_STD_ID=$(snowpost -X POST "$SNOW/api/now/table/change_request" \
  -d "{
    \"type\": \"standard\",
    \"short_description\": \"Add new merchant VPA to UPI whitelist -- BigBasket\",
    \"description\": \"Standard procedure: Add merchant VPA bigbasket@hdfcbank to the UPI payment whitelist. Pre-approved, low risk.\",
    \"category\": \"Software\",
    \"risk\": \"low\",
    \"impact\": \"3\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"implementation_plan\": \"1. Add VPA entry to merchant whitelist configuration\\n2. Reload configuration: curl -X POST http://upi-transaction-service:8081/actuator/refresh\\n3. Verify merchant can receive test UPI payment\\n4. Confirm in merchant portal\",
    \"backout_plan\": \"Remove VPA entry from whitelist, reload configuration\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export CHG_STD_NUM=$(snowget "$SNOW/api/now/table/change_request/$CHG_STD_ID?sysparm_fields=number" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['number'])")

echo "Standard Change: $CHG_STD_NUM (sys_id: $CHG_STD_ID)"
```

### 15.3 CREATE Emergency Change

```bash
# UI equivalent: Change > Create New, Type = Emergency
# Emergency changes fast-track for critical production issues

export CHG_EMERG_ID=$(snowpost -X POST "$SNOW/api/now/table/change_request" \
  -d "{
    \"type\": \"emergency\",
    \"short_description\": \"EMERGENCY: UPI payment gateway SSL certificate expired -- all transactions failing\",
    \"description\": \"SSL certificate on UPI payment gateway expired at 11:30 PM IST. All UPI transactions returning SSL handshake failures. Impact: 500+ transactions/minute failing. Revenue loss: significant.\",
    \"category\": \"Network\",
    \"risk\": \"high\",
    \"impact\": \"1\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"justification\": \"Production UPI payment processing is completely down. Immediate certificate renewal required. Verbal approval obtained from VP Engineering at 11:35 PM.\",
    \"implementation_plan\": \"1. Obtain new SSL certificate from CA (wildcard *.npci-upi.internal)\\n2. Install certificate on payment gateway\\n3. Restart gateway service\\n4. Verify transaction processing restored\",
    \"backout_plan\": \"Restore previous certificate from backup if new cert causes issues\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export CHG_EMERG_NUM=$(snowget "$SNOW/api/now/table/change_request/$CHG_EMERG_ID?sysparm_fields=number" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['number'])")

echo "Emergency Change: $CHG_EMERG_NUM (sys_id: $CHG_EMERG_ID)"
```

### 15.4 UPDATE Normal Change through complete state lifecycle

```bash
# Normal Change flow: New -> Assess -> Authorize -> Scheduled -> Implement -> Review -> Closed

# --- State: New -> Assess ---
# UI equivalent: Click "Assess" button on change form
snowpatch "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID" \
  -d '{
    "state": "-4",
    "work_notes": "All planning documents complete. Implementation, rollback, and test plans verified. Submitting for CAB review."
  }' | python3 -c "import sys,json; print('Normal Change -> Assess')"

# --- State: Assess -> Authorize ---
# UI equivalent: Click "Authorize" button
snowpatch "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID" \
  -d '{
    "state": "-3",
    "work_notes": "Assessment complete. Risk: Moderate. Impact: High. Submitting for CAB approval."
  }' | python3 -c "import sys,json; print('Normal Change -> Authorize')"

# --- State: Authorize -> Scheduled ---
# UI equivalent: After approval, move to Scheduled
snowpatch "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID" \
  -d '{
    "state": "-2",
    "work_notes": "CAB approved. Change scheduled for Sunday 02:00-05:00 AM IST maintenance window."
  }' | python3 -c "import sys,json; print('Normal Change -> Scheduled')"

# --- State: Scheduled -> Implement ---
# UI equivalent: Click "Implement" button at start of maintenance window
snowpatch "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID" \
  -d '{
    "state": "-1",
    "work_notes": "2:00 AM - Pre-implementation started. Operations team notified. Configuration backup taken. Staging test results verified."
  }' | python3 -c "import sys,json; print('Normal Change -> Implement')"

# Add implementation work notes
snowpatch "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID" \
  -d '{
    "work_notes": "2:15 AM - Deploying UPI Transaction Service v2.1\n- New Docker image pulled\n- Rolling restart completed\n- /chaos/status returns 401 without auth token\n- /api/upi/pay still works without auth (public endpoint)"
  }' | python3 -c "import sys,json; print('Implementation note 1 added')"

snowpatch "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID" \
  -d '{
    "work_notes": "2:45 AM - Deploying UPI Settlement Service v2.1\n- Resilience4j circuit breaker active\n- Circuit breaker state: CLOSED (healthy)\n- Metrics visible in Prometheus"
  }' | python3 -c "import sys,json; print('Implementation note 2 added')"

snowpatch "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID" \
  -d '{
    "work_notes": "3:00 AM - Smoke test: 100 transactions, 100% success rate\n3:15 AM - Chaos test: /chaos/enable returns 401 Unauthorized\n3:30 AM - Monitoring phase started. Grafana shows green."
  }' | python3 -c "import sys,json; print('Implementation note 3 added')"

# --- State: Implement -> Review ---
snowpatch "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID" \
  -d '{
    "state": "0",
    "work_notes": "5:00 AM - Monitoring phase complete. 90 minutes stable operation. Zero errors. Circuit breaker CLOSED. JVM heap stable at 42%. Change declared SUCCESSFUL."
  }' | python3 -c "import sys,json; print('Normal Change -> Review')"

# --- State: Review -> Closed ---
snowpatch "$SNOW/api/now/table/change_request/$CHG_NORMAL_ID" \
  -d '{
    "state": "3",
    "close_code": "successful",
    "close_notes": "Change implemented successfully during maintenance window (2:00-5:00 AM).\n- Chaos endpoints secured with Spring Security (JWT auth required)\n- Circuit breaker added between Settlement and Transaction services\n- Smoke and chaos tests passed\n- 90-minute monitoring period: zero issues\n- Workaround (manual /chaos/disable) no longer needed\n- Problem can now be closed"
  }' | python3 -c "import sys,json; print('Normal Change -> Closed (Successful)')"
```

### 15.5 UPDATE Standard Change through lifecycle (shortened flow)

```bash
# Standard flow: New -> Scheduled -> Implement -> Review -> Closed
# (No Assess or Authorize -- pre-approved)

snowpatch "$SNOW/api/now/table/change_request/$CHG_STD_ID" \
  -d '{"state":"-2","work_notes":"Standard change -- pre-approved. Scheduling for next available window."}' \
  | python3 -c "import sys,json; print('Standard Change -> Scheduled')"

snowpatch "$SNOW/api/now/table/change_request/$CHG_STD_ID" \
  -d '{"state":"-1","work_notes":"Adding bigbasket@hdfcbank to merchant whitelist. Reloading config."}' \
  | python3 -c "import sys,json; print('Standard Change -> Implement')"

snowpatch "$SNOW/api/now/table/change_request/$CHG_STD_ID" \
  -d '{"state":"0","work_notes":"Merchant VPA added. Test payment confirmed. Merchant portal shows active."}' \
  | python3 -c "import sys,json; print('Standard Change -> Review')"

snowpatch "$SNOW/api/now/table/change_request/$CHG_STD_ID" \
  -d '{"state":"3","close_code":"successful","close_notes":"Merchant VPA bigbasket@hdfcbank added successfully. Test payment confirmed."}' \
  | python3 -c "import sys,json; print('Standard Change -> Closed (Successful)')"
```

### 15.6 UPDATE Emergency Change through lifecycle

```bash
# Emergency flow: New -> Authorize -> Implement -> Review -> Closed
# (Verbal approval, post-implementation CAB review)

snowpatch "$SNOW/api/now/table/change_request/$CHG_EMERG_ID" \
  -d '{"state":"-3","work_notes":"Verbal approval from VP Engineering (Sanjay) at 11:35 PM. Proceeding with emergency certificate renewal."}' \
  | python3 -c "import sys,json; print('Emergency Change -> Authorize')"

snowpatch "$SNOW/api/now/table/change_request/$CHG_EMERG_ID" \
  -d '{
    "state": "-1",
    "work_notes": "11:45 PM - Emergency implementation\n- New SSL certificate obtained from CA (wildcard *.npci-upi.internal)\n- Certificate installed on payment gateway\n- UPI transaction processing restored at 11:50 PM\n- Monitoring confirms 100% success rate"
  }' | python3 -c "import sys,json; print('Emergency Change -> Implement')"

snowpatch "$SNOW/api/now/table/change_request/$CHG_EMERG_ID" \
  -d '{
    "state": "0",
    "work_notes": "Post-implementation review:\n- Root cause: Certificate expiry was not monitored (no alert for cert expiry)\n- Action item: Add SSL certificate expiry monitoring (alert 30 days before)\n- Action item: Create Standard Change template for SSL renewal\n- This should become a proactive Problem (certificate monitoring gap)"
  }' | python3 -c "import sys,json; print('Emergency Change -> Review')"

snowpatch "$SNOW/api/now/table/change_request/$CHG_EMERG_ID" \
  -d '{"state":"3","close_code":"successful","close_notes":"SSL certificate renewed. UPI transactions restored within 20 minutes of detection. Post-implementation review completed."}' \
  | python3 -c "import sys,json; print('Emergency Change -> Closed (Successful)')"
```

### 15.7 ADD CI impact (affected CIs)

```bash
# UI equivalent: Open change > Affected CIs related list > Edit > Add CIs
# Link CIs to the normal change using the task_ci M2M table

# Find available CIs
snowget "$SNOW/api/now/table/cmdb_ci?sysparm_fields=sys_id,name,sys_class_name&sysparm_limit=5&sysparm_display_value=true" \
  | python3 -c "
import sys,json
print('Available CIs:')
for ci in json.load(sys.stdin)['result']:
    print(f\"  {ci['sys_id'][:12]}...  {ci['name']}  ({ci['sys_class_name']})\")
"

# Link a CI to the change (if a CI was found)
CI_FOR_CHG=$(snowget "$SNOW/api/now/table/cmdb_ci?sysparm_fields=sys_id&sysparm_limit=1" \
  | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['sys_id'] if r else '')")

if [ -n "$CI_FOR_CHG" ]; then
  snowpost -X POST "$SNOW/api/now/table/task_ci" \
    -d "{\"task\":\"$CHG_NORMAL_ID\",\"ci_item\":\"$CI_FOR_CHG\"}" \
    | python3 -c "import sys,json; print('CI linked to change')"
fi
```

### 15.8 Approval simulation

```bash
# UI equivalent: Impersonate approver > My Approvals > Approve
# Create an approval record for the normal change

snowpost -X POST "$SNOW/api/now/table/sysapproval_approver" \
  -d "{
    \"sysapproval\": \"$CHG_NORMAL_ID\",
    \"approver\": \"$USER_ABEL\",
    \"state\": \"approved\",
    \"comments\": \"CAB approval granted. Implementation plan is thorough. Rollback plan tested. Risk accepted.\"
  }" | python3 -c "import sys,json; print('Approval record created: approved')"

# To simulate a rejection instead (on a different change):
# snowpost -X POST "$SNOW/api/now/table/sysapproval_approver" \
#   -d "{\"sysapproval\":\"CHANGE_SYS_ID\",\"approver\":\"$USER_ABEL\",\"state\":\"rejected\",\"comments\":\"Need more testing data before approval.\"}"
```

### 15.9 LINK change to problem

```bash
# UI equivalent: Open Problem > Change Requests related list > Edit > Add
# The problem record has a related list for change requests.
# We can also set it from the change side if a field exists.

snowpatch "$SNOW/api/now/table/problem/$PRB_ID" \
  -d "{
    \"work_notes\": \"Change Request $CHG_NORMAL_NUM created for permanent fix. CAB approved. Deployment scheduled.\"
  }" | python3 -c "import sys,json; print('Problem updated with change reference')"
```

### 15.10 Change conflict detection -- query overlapping changes

```bash
# UI equivalent: Change > Change Calendar -- look for overlapping windows
# Query for changes scheduled in the same maintenance window

echo "=== Changes scheduled this month ==="
snowget "$SNOW/api/now/table/change_request?sysparm_query=stateIN-2,-1&sysparm_fields=number,short_description,type,risk,state&sysparm_display_value=true" \
  | python3 -c "
import sys,json
changes = json.load(sys.stdin)['result']
print(f'Active/Scheduled changes: {len(changes)}')
for c in changes:
    print(f\"  {c['number']}  Type={c['type']}  Risk={c['risk']}  State={c['state']}\")
    print(f\"    {c['short_description'][:70]}\")
"

# Check for blackout schedules
echo "=== Change Blackout Schedules ==="
snowget "$SNOW/api/now/table/change_blackout?sysparm_fields=name,type,start_date,end_date&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

### 15.11 Create additional changes for reporting data

```bash
# UI equivalent: Create 6 more changes with varied types for later reporting

REPORT_CHANGES=(
  '{"type":"normal","short_description":"Add rate limiting to UPI /api/upi/pay endpoint","category":"Software","risk":"moderate","impact":"2"}'
  '{"type":"normal","short_description":"Migrate UPI logs to centralized ELK stack","category":"Software","risk":"moderate","impact":"2"}'
  '{"type":"standard","short_description":"Rotate UPI API authentication keys -- quarterly","category":"Software","risk":"low","impact":"3"}'
  '{"type":"standard","short_description":"Update UPI transaction daily limit from 1L to 2L","category":"Software","risk":"low","impact":"2"}'
  '{"type":"emergency","short_description":"Hotfix: UPI duplicate transaction detection bypass","category":"Software","risk":"high","impact":"1"}'
  '{"type":"normal","short_description":"Upgrade Spring Boot from 3.2 to 3.3 across UPI services","category":"Software","risk":"moderate","impact":"2"}'
)

echo "=== Creating reporting data changes ==="
for CHG_DATA in "${REPORT_CHANGES[@]}"; do
  # Add assignment_group to each
  FULL_DATA=$(echo "$CHG_DATA" | python3 -c "
import sys,json
d=json.load(sys.stdin)
d['assignment_group']='$GRP_PLATFORM'
print(json.dumps(d))
")
  snowpost -X POST "$SNOW/api/now/table/change_request" \
    -d "$FULL_DATA" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  {r['number']}: {r['short_description']}\")"
done
```

### 15.12 Failed change with rollback (Exercise)

```bash
# Create a change that will be marked as unsuccessful
export CHG_FAIL_ID=$(snowpost -X POST "$SNOW/api/now/table/change_request" \
  -d "{
    \"type\": \"normal\",
    \"short_description\": \"Upgrade UPI Settlement Service database from PostgreSQL 14 to 16\",
    \"description\": \"Database upgrade for improved performance and security patches.\",
    \"category\": \"Software\",
    \"risk\": \"high\",
    \"impact\": \"1\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"implementation_plan\": \"1. Full database backup\\n2. Stop settlement service\\n3. Run pg_upgrade from 14 to 16\\n4. Run migration scripts\\n5. Start settlement service\\n6. Verify settlements processing\",
    \"backout_plan\": \"1. Stop settlement service\\n2. Restore PostgreSQL 14 from backup\\n3. Restart settlement service\\n4. Verify data integrity\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

# Walk it through to failure
snowpatch "$SNOW/api/now/table/change_request/$CHG_FAIL_ID" \
  -d '{"state":"-1","work_notes":"Starting database upgrade. Full backup completed."}' 2>/dev/null

snowpatch "$SNOW/api/now/table/change_request/$CHG_FAIL_ID" \
  -d '{"work_notes":"FAILURE: Database migration script failed at step 3. Foreign key constraint violation on settlement_transactions table. Initiating rollback."}' 2>/dev/null

snowpatch "$SNOW/api/now/table/change_request/$CHG_FAIL_ID" \
  -d '{"work_notes":"Rollback complete. PostgreSQL 14 restored from backup. All settlements processing normally. Time to rollback: 18 minutes."}' 2>/dev/null

snowpatch "$SNOW/api/now/table/change_request/$CHG_FAIL_ID" \
  -d '{"state":"0","work_notes":"Post-mortem: Migration script incompatible with settlement_transactions partitioning. Need to update migration for partitioned tables."}' 2>/dev/null

snowpatch "$SNOW/api/now/table/change_request/$CHG_FAIL_ID" \
  -d '{"state":"3","close_code":"unsuccessful","close_notes":"Database migration failed due to foreign key constraint on partitioned tables. Rolled back successfully. No data loss. Remediation: update migration scripts for partitioned table support and retest in staging."}' \
  | python3 -c "import sys,json; print('Failed change closed as Unsuccessful')"
```

### 15.13 Verification and cleanup

```bash
# Verify all changes
echo "=== All Change Requests ==="
snowget "$SNOW/api/now/table/change_request?sysparm_query=assignment_group=$GRP_PLATFORM&sysparm_fields=number,type,short_description,state,close_code&sysparm_display_value=true&sysparm_limit=20" \
  | python3 -c "
import sys,json
for c in json.load(sys.stdin)['result']:
    print(f\"{c['number']}  {c['type']:<10}  {c['state']:<12}  {c.get('close_code',''):<14}  {c['short_description'][:50]}\")
"
```

---

## Lab 16: Release and Deployment Management

Replicates the release management lifecycle from Lab 16. Creates a
release record, links changes, defines phases, creates deployment
tasks, and closes with a post-implementation review.

> **Note:** The release_project, release_phase, and release_task tables
> require the Release Management plugin (`com.snc.release_management`)
> to be activated. If these tables are not available, the commands will
> return errors. Check with:
> `snowget "$SNOW/api/now/table/release_project?sysparm_limit=1"`

### 16.1 CREATE release record

```bash
# UI equivalent: Release > Create New

export REL_ID=$(snowpost -X POST "$SNOW/api/now/table/release_project" \
  -d "{
    \"short_description\": \"UPI Platform v3.2.0 -- September Release\",
    \"description\": \"UPI Platform v3.2.0 -- September Major Release\\n\\nSCOPE:\\n1. Circuit Breaker Implementation (from Problem $PRB_NUM)\\n2. Settlement Batch Processing Optimization\\n3. New Merchant Onboarding API Endpoint\\n4. PostgreSQL Upgrade from 14.x to 15.x\\n\\nDEPLOYMENT STRATEGY:\\n- Canary deployment for Transaction Service\\n- Blue-green deployment for Settlement Service\\n- Rolling restart for API endpoints\\n\\nMAINTENANCE WINDOW: Sunday 02:00 - 06:00 IST\",
    \"type\": \"major\",
    \"state\": \"draft\",
    \"priority\": \"2\",
    \"risk\": \"high\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export REL_NUM=$(snowget "$SNOW/api/now/table/release_project/$REL_ID?sysparm_fields=number" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['number'])")

echo "Created Release: $REL_NUM (sys_id: $REL_ID)"
```

### 16.2 CREATE change requests for the release

```bash
# Create 4 changes that will be bundled in this release

export CHG_CB_ID=$(snowpost -X POST "$SNOW/api/now/table/change_request" \
  -d "{
    \"type\": \"normal\",
    \"short_description\": \"Implement circuit breaker pattern in UPI Transaction Service\",
    \"category\": \"Software\",
    \"priority\": \"2\",
    \"risk\": \"moderate\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"justification\": \"Prevent cascading failures identified in Problem $PRB_NUM\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export CHG_SETTLE_ID=$(snowpost -X POST "$SNOW/api/now/table/change_request" \
  -d "{
    \"type\": \"normal\",
    \"short_description\": \"Optimize settlement batch processing\",
    \"category\": \"Software\",
    \"priority\": \"3\",
    \"risk\": \"low\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"justification\": \"Reduce batch processing time by 40%, eliminate DB lock contention\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export CHG_MERCHANT_ID=$(snowpost -X POST "$SNOW/api/now/table/change_request" \
  -d "{
    \"type\": \"normal\",
    \"short_description\": \"Deploy new merchant onboarding API endpoint\",
    \"category\": \"Software\",
    \"priority\": \"3\",
    \"risk\": \"low\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"justification\": \"Replace manual CSV-based merchant registration with REST API\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

export CHG_PG_ID=$(snowpost -X POST "$SNOW/api/now/table/change_request" \
  -d "{
    \"type\": \"normal\",
    \"short_description\": \"Upgrade PostgreSQL from 14.x to 15.x\",
    \"category\": \"Hardware\",
    \"priority\": \"2\",
    \"risk\": \"high\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"justification\": \"Security patches, performance improvements, replication enhancements\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

echo "Changes for release:"
echo "  Circuit Breaker:  $CHG_CB_ID"
echo "  Settlement Opt:   $CHG_SETTLE_ID"
echo "  Merchant API:     $CHG_MERCHANT_ID"
echo "  PostgreSQL Upgr:  $CHG_PG_ID"
```

### 16.3 LINK changes to release

```bash
# UI equivalent: Open Release > Change Requests related list > Edit > Add
# Link each change to the release by setting the release field on the change

for CHG_ID in $CHG_CB_ID $CHG_SETTLE_ID $CHG_MERCHANT_ID $CHG_PG_ID; do
  snowpatch "$SNOW/api/now/table/change_request/$CHG_ID" \
    -d "{\"release\": \"$REL_ID\"}" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  Linked {r['number']} to release $REL_NUM\")"
done

# Verify linked changes
echo "=== Changes linked to $REL_NUM ==="
snowget "$SNOW/api/now/table/change_request?sysparm_query=release=$REL_ID&sysparm_fields=number,short_description,type,risk&sysparm_display_value=true" \
  | python3 -c "
import sys,json
for c in json.load(sys.stdin)['result']:
    print(f\"  {c['number']}  Risk={c['risk']}  {c['short_description'][:55]}\")
"
```

### 16.4 CREATE release phases

```bash
# UI equivalent: Open Release > Release Phases related list > New

PHASES=(
  '{"short_description":"Phase 1: Planning & Design","order":"100","state":"1","description":"Architecture review, resource allocation, risk assessment. Gate: CAB approval required before proceeding to Build phase."}'
  '{"short_description":"Phase 2: Build & Integration Testing","order":"200","state":"-5","description":"Code freeze, merge feature branches, CI/CD pipeline, integration tests. Gate: All tests pass, zero critical defects, code coverage above 80%."}'
  '{"short_description":"Phase 3: UAT & Performance Testing","order":"300","state":"-5","description":"User acceptance testing in staging. Load test: 50,000 TPS sustained 30 min. Security scan: OWASP Top 10. Gate: UAT sign-off, p99 latency < 200ms."}'
  '{"short_description":"Phase 4: Production Deployment","order":"400","state":"-5","description":"Execute deployment plan within Sunday 02:00-06:00 IST window. Canary deployment with traffic ramp-up. NOC monitoring throughout. Gate: Smoke tests pass, error rate < 0.01%."}'
  '{"short_description":"Phase 5: Post-Deployment Verification","order":"500","state":"-5","description":"24-hour soak period. Monitor all transaction types, settlement processing, merchant onboarding. Conduct PIR. Gate: PIR completed, stakeholder sign-off."}'
)

PHASE_IDS=()
echo "=== Creating Release Phases ==="
for PHASE_DATA in "${PHASES[@]}"; do
  FULL_DATA=$(echo "$PHASE_DATA" | python3 -c "
import sys,json
d=json.load(sys.stdin)
d['release']='$REL_ID'
print(json.dumps(d))
")
  PHASE_ID=$(snowpost -X POST "$SNOW/api/now/table/release_phase" \
    -d "$FULL_DATA" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['sys_id'])")
  PHASE_IDS+=("$PHASE_ID")
  echo "  Created: $(echo $PHASE_DATA | python3 -c "import sys,json; print(json.load(sys.stdin)['short_description'])")"
done

# Save Phase 4 sys_id for deployment tasks
export PHASE4_ID="${PHASE_IDS[3]}"
echo "Phase 4 sys_id (for deployment tasks): $PHASE4_ID"
```

### 16.5 CREATE deployment tasks (under Phase 4)

```bash
# UI equivalent: Open Phase 4 > Deployment Tasks related list > New

TASKS=(
  '{"short_description":"Pre-deployment: Verify staging matches production","order":"10","description":"Confirm staging deployment healthy. Verify artifacts staged. Check rollback scripts tested. Confirm NOC team online. Est: 15 min."}'
  '{"short_description":"Create full PostgreSQL backup (primary + replica)","order":"20","description":"pg_dump full backup of production database. Verify backup integrity with checksum. Store in S3 with 30-day retention. Est: 20 min."}'
  '{"short_description":"Execute PostgreSQL upgrade 14.x to 15.x","order":"30","description":"Stop replication. Upgrade primary via pg_upgrade. Run optimizer statistics. Verify data integrity (row counts, checksums). Restart replication. Est: 30 min."}'
  '{"short_description":"Deploy backend services with rolling restart","order":"40","description":"Deploy Transaction Service with circuit breaker (canary -- 1 server first). Deploy Settlement Service with batch optimization (blue-green). Est: 20 min."}'
  '{"short_description":"Deploy merchant onboarding API endpoint","order":"50","description":"Deploy new API endpoint alongside existing services. Additive change -- does not modify existing functionality. Est: 10 min."}'
  '{"short_description":"Update load balancer for canary traffic split","order":"60","description":"Configure LB to route 5% traffic to canary (v3.2.0) server. Health check auto-removes canary if error rate > 1%. Est: 10 min."}'
  '{"short_description":"Execute production smoke test suite","order":"70","description":"Automated smoke tests: UPI P2P, P2M, settlement batch, merchant API, DB query performance. All must pass. Est: 15 min."}'
  '{"short_description":"Canary traffic ramp-up: 5% to 25% to 50% to 100%","order":"80","description":"Gradually increase traffic to v3.2.0 servers. Monitor 10 min at each stage. GREEN=proceed, YELLOW=hold, RED=rollback. Est: 40 min."}'
  '{"short_description":"Full rollout complete -- final verification","order":"90","description":"All servers running v3.2.0. Final verification. Confirm NOC dashboards green. Update release state. Send completion notification. Est: 10 min."}'
)

echo "=== Creating Deployment Tasks ==="
for TASK_DATA in "${TASKS[@]}"; do
  FULL_DATA=$(echo "$TASK_DATA" | python3 -c "
import sys,json
d=json.load(sys.stdin)
d['parent']='$PHASE4_ID'
d['state']='-5'
print(json.dumps(d))
")
  snowpost -X POST "$SNOW/api/now/table/release_task" \
    -d "$FULL_DATA" \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  Task {r.get('order','?')}: {r['short_description'][:60]}\")"
done
```

### 16.6 UPDATE release state through lifecycle

```bash
# Release flow: Draft -> Planning -> Build -> Test -> Deploy -> Review -> Closed

echo "=== Walking release through lifecycle ==="

# Draft -> Planning
snowpatch "$SNOW/api/now/table/release_project/$REL_ID" \
  -d '{"state":"planning","work_notes":"Release scope finalized. 4 changes linked. Resource allocation complete. Proceeding to planning phase."}' \
  | python3 -c "import sys,json; print('Release -> Planning')"

# Planning -> Build
snowpatch "$SNOW/api/now/table/release_project/$REL_ID" \
  -d '{"state":"build","work_notes":"CAB approval received for all 4 changes. Feature branches merged. CI/CD pipeline initiated."}' \
  | python3 -c "import sys,json; print('Release -> Build')"

# Build -> Test
snowpatch "$SNOW/api/now/table/release_project/$REL_ID" \
  -d '{"state":"test","work_notes":"Build artifacts created and staged. All integration tests pass. Code coverage: 87%. Proceeding to UAT and performance testing."}' \
  | python3 -c "import sys,json; print('Release -> Test')"

# Test -> Deploy
snowpatch "$SNOW/api/now/table/release_project/$REL_ID" \
  -d '{"state":"deploy","work_notes":"UAT sign-off received. Load test: 50K TPS sustained for 30 min. p99 latency: 185ms (below 200ms threshold). Security scan clean. Proceeding to production deployment."}' \
  | python3 -c "import sys,json; print('Release -> Deploy')"

# Deploy -> Review
snowpatch "$SNOW/api/now/table/release_project/$REL_ID" \
  -d '{"state":"review","work_notes":"Deployment completed at 05:15 IST (25-min overrun due to PostgreSQL optimizer stats rebuild). All smoke tests passed. Canary ramp-up successful. No rollback required. Entering 24-hour soak period."}' \
  | python3 -c "import sys,json; print('Release -> Review')"
```

### 16.7 Post-Implementation Review and Close

```bash
# UI equivalent: Fill in PIR section, change state to Closed

snowpatch "$SNOW/api/now/table/release_project/$REL_ID" \
  -d '{
    "state": "closed",
    "close_notes": "POST-IMPLEMENTATION REVIEW: UPI Platform v3.2.0\n\nDEPLOYMENT RESULTS:\n  PostgreSQL Upgrade:    SUCCESS (with 25-min delay)\n  Circuit Breaker:       SUCCESS\n  Settlement Batch Opt:  SUCCESS\n  Merchant API:          SUCCESS\n  Overall:               SUCCESSFUL -- No rollback required\n\nMETRICS COMPARISON:\n  Avg transaction latency:  145ms -> 128ms  (-12%)\n  p99 transaction latency:  280ms -> 195ms  (-30%)\n  Settlement batch time:    47min -> 29min  (-38%)\n  Error rate:               0.008% -> 0.005% (-37%)\n\nLESSONS LEARNED:\n  1. Database upgrade time: Add 50% buffer for production data volume\n  2. Health check thresholds: Create separate deployment-mode alert profiles\n  3. Stakeholder updates every 30 min worked well -- formalize as standard\n\nSIGN-OFF: Release Manager (Sanjay) -- APPROVED"
  }' | python3 -c "import sys,json; print('Release -> Closed (PIR completed)')"

# Verify final release state
snowget "$SNOW/api/now/table/release_project/$REL_ID?sysparm_fields=number,short_description,state,close_notes&sysparm_display_value=true" \
  | python3 -c "
import sys,json
r=json.load(sys.stdin)['result']
print(f\"Release: {r['number']}\")
print(f\"State: {r['state']}\")
print(f\"Description: {r['short_description']}\")
print(f\"Close notes (first 200 chars): {r['close_notes'][:200]}...\")
"
```

### 16.8 Query release calendar

```bash
# UI equivalent: Release > Release Calendar

echo "=== All Releases ==="
snowget "$SNOW/api/now/table/release_project?sysparm_fields=number,short_description,type,state,release_date,risk,priority&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -c "
import sys,json
for r in json.load(sys.stdin)['result']:
    print(f\"{r['number']}  {r['type']:<10}  {r['state']:<10}  Risk={r['risk']}  {r['short_description'][:50]}\")
"

# Query phases for our release
echo "=== Phases for $REL_NUM ==="
snowget "$SNOW/api/now/table/release_phase?sysparm_query=release=$REL_ID&sysparm_fields=short_description,order,state&sysparm_display_value=true&sysparm_order_by=order" \
  | python3 -c "
import sys,json
for p in json.load(sys.stdin)['result']:
    print(f\"  {p['order']}  {p['state']:<10}  {p['short_description']}\")
"

# Query deployment tasks
echo "=== Deployment Tasks ==="
snowget "$SNOW/api/now/table/release_task?sysparm_query=parent=$PHASE4_ID&sysparm_fields=short_description,order,state&sysparm_display_value=true&sysparm_order_by=order" \
  | python3 -c "
import sys,json
for t in json.load(sys.stdin)['result']:
    print(f\"  Task {t['order']}  {t['state']:<10}  {t['short_description'][:55]}\")
"
```

### 16.9 Create an emergency hotfix release

```bash
# Exercise: Minor release for circuit breaker threshold fix

export REL_HOTFIX_ID=$(snowpost -X POST "$SNOW/api/now/table/release_project" \
  -d "{
    \"short_description\": \"UPI Platform v3.2.1 -- Hotfix: Circuit breaker threshold adjustment\",
    \"description\": \"Emergency release to adjust circuit breaker threshold from 50% to 80% failure rate. Original threshold was based on staging traffic patterns. Production traffic is burstier, causing premature circuit opens during normal peak hours.\",
    \"type\": \"emergency\",
    \"state\": \"deploy\",
    \"priority\": \"1\",
    \"risk\": \"low\"
  }" | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"Hotfix Release: {r['number']}\")")

# Create the emergency change for the hotfix
export CHG_HOTFIX_ID=$(snowpost -X POST "$SNOW/api/now/table/change_request" \
  -d "{
    \"type\": \"emergency\",
    \"short_description\": \"Adjust circuit breaker threshold from 50% to 80% failure rate\",
    \"description\": \"Circuit breaker opens prematurely during peak traffic. Threshold of 50% too aggressive for production burstiness.\",
    \"category\": \"Software\",
    \"risk\": \"low\",
    \"impact\": \"2\",
    \"assignment_group\": \"$GRP_PLATFORM\",
    \"release\": \"$REL_HOTFIX_ID\"
  }" | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['sys_id'])")

echo "Hotfix change linked to release: $CHG_HOTFIX_ID"
```

### 16.10 Cleanup

```bash
echo "=== Cleanup: Closing all lab release records ==="

# Close all open changes created in this lab
for CHG_ID in $CHG_CB_ID $CHG_SETTLE_ID $CHG_MERCHANT_ID $CHG_PG_ID $CHG_HOTFIX_ID; do
  snowpatch "$SNOW/api/now/table/change_request/$CHG_ID" \
    -d '{"state":"3","close_code":"successful","close_notes":"Closed by API companion cleanup."}' 2>/dev/null \
    | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(f\"  Closed {r['number']}\")" 2>/dev/null
done

# Note: Release records, phases, and tasks are typically not deleted.
# To delete a release record (use with caution):
# snowdelete "$SNOW/api/now/table/release_project/$REL_ID"
```

---

## Quick Reference -- Table and Field Names

| Table | API Path | Key Fields |
|---|---|---|
| Incident | `/api/now/table/incident` | number, state, priority, impact, urgency, category, assignment_group, assigned_to, cmdb_ci, problem_id, close_code, close_notes, work_notes |
| Problem | `/api/now/table/problem` | number, state, known_error, cause_notes, fix_notes, workaround, close_code |
| Change Request | `/api/now/table/change_request` | number, type, state, risk, impact, category, implementation_plan, backout_plan, test_plan, close_code |
| Release | `/api/now/table/release_project` | number, type, state, priority, risk, release_date, close_notes |
| Release Phase | `/api/now/table/release_phase` | release, short_description, order, state |
| Release Task | `/api/now/table/release_task` | parent, short_description, order, state |
| Event | `/api/now/table/em_event` | source, node, type, severity, description |
| Task SLA | `/api/now/table/task_sla` | task, sla, stage, has_breached, business_percentage |
| Approval | `/api/now/table/sysapproval_approver` | sysapproval, approver, state, comments |
| User Group | `/api/now/table/sys_user_group` | name, active |
| CI | `/api/now/table/cmdb_ci` | name, sys_class_name |
| Journal | `/api/now/table/sys_journal_field` | element_id, element, value |

## State Values Reference

**Incident states:** 1=New, 2=In Progress, 3=On Hold, 6=Resolved, 7=Closed

**Problem states:** 1=New, 2=Assess (Open), 3=Root Cause Analysis, 4=Resolved/Closed

**Change Request states:** -5=New, -4=Assess, -3=Authorize, -2=Scheduled, -1=Implement, 0=Review, 3=Closed, 4=Cancelled

**Release states:** draft, planning, build, test, deploy, review, closed

**Change types:** normal, standard, emergency

**Change close codes:** successful, unsuccessful, incomplete

---

## Aggregate API Reference

```bash
# Generic pattern for aggregate (stats) queries:
# GET /api/now/stats/{table}?sysparm_count=true&sysparm_group_by={field}

# Count incidents by priority
snowget "$SNOW/api/now/stats/incident?sysparm_count=true&sysparm_group_by=priority&sysparm_display_value=true"

# Count changes by type
snowget "$SNOW/api/now/stats/change_request?sysparm_count=true&sysparm_group_by=type&sysparm_display_value=true"

# Count problems by known_error status
snowget "$SNOW/api/now/stats/problem?sysparm_count=true&sysparm_group_by=known_error&sysparm_display_value=true"

# Average resolution time for incidents
snowget "$SNOW/api/now/stats/incident?sysparm_avg_fields=calendar_duration&sysparm_group_by=priority&sysparm_query=state=7&sysparm_display_value=true"
```
