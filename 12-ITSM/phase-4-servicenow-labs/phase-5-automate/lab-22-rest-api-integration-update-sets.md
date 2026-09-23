# Lab 22: REST API, Integration Hub & Update Sets

**Level:** Advanced | **Duration:** 90 min | **Prerequisites:** Lab 21 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Master ServiceNow REST API architecture (Table, Aggregate, Import Set, Attachment, CMDB, Scripted REST)
- Create, read, update incidents via inbound REST API using curl and Postman
- Build custom Scripted REST APIs for the UPI platform
- Configure outbound REST integrations with webhooks and external systems
- Use Integration Hub and Action Designer for spoke-based integrations
- Capture all customizations in Update Sets for controlled deployment
- Write and run Automated Test Framework (ATF) tests for regression validation
- Understand the full CI/CD lifecycle for ServiceNow: Dev to Test to Prod

---

## Scenario: Full-Stack Integration for NPCI UPI Platform

```
The NPCI UPI Platform has evolved across 21 labs:
  - CMDB with UPI services and infrastructure CIs
  - Incident, Problem, Change Management workflows
  - SLAs, Business Rules, Client Scripts, Flow Designer automations
  - Snow Bridge (Python Flask) already integrates with ServiceNow REST API

Now we bring it all together:
  1. Deep-dive into every ServiceNow REST API endpoint
  2. Build native Scripted REST APIs inside ServiceNow
  3. Configure outbound webhooks for Slack and Prometheus
  4. Package everything into Update Sets for deployment
  5. Write ATF tests to validate our entire ITSM configuration

This is the capstone lab. Everything connects here.
```

---

## Part 1: ServiceNow REST API Architecture

### 1.1 API Families Overview

ServiceNow exposes a rich set of REST APIs. Every API is available at:

```
https://<instance>.service-now.com/api/<namespace>/<api_name>
```

Here are the core API families you will use:

```
API Family                  Base Path                                  Purpose
--------------------------  -----------------------------------------  --------------------------------
Table API                   /api/now/table/{tableName}                 CRUD on any table
Aggregate API               /api/now/stats/{tableName}                 COUNT, SUM, AVG, MIN, MAX
Import Set API              /api/now/import/{tableName}                Bulk data import via staging
Attachment API              /api/now/attachment                        Upload/download file attachments
CMDB API                    /api/now/cmdb/instance/{className}         CMDB-specific operations
Scripted REST API           /api/{namespace}/{api_id}                  Custom endpoints you build
Service Catalog API         /sn_sc/servicecatalog                      Catalog items & cart operations
Performance Analytics API   /api/now/pa/scorecards                     KPIs and indicators
CSM API                     /api/sn_customerservice                    Customer service management
```

### 1.2 Authentication Methods

```
Method          How It Works                              When to Use
--------------  ----------------------------------------  ----------------------------------
Basic Auth      Username:Password in Authorization        Development, PDI testing
                header (Base64 encoded)

OAuth 2.0       Client Credentials or Authorization       Production integrations
                Code grant. Token endpoint:               Service-to-service communication
                /oauth_token.do

API Key         Custom header with pre-shared key         Simple external integrations
                (configured via Scripted REST API)        Webhook receivers

Mutual TLS      Client certificate authentication         High-security environments
                                                          Financial services (NPCI)
```

#### OAuth 2.0 Setup (Reference)

```
To configure OAuth 2.0 on your PDI:

1. Navigate to: System OAuth > Application Registry
2. Click "New"
3. Select: "Create an OAuth API endpoint for external clients"
4. Fill in:
   - Name:           UPI Integration OAuth
   - Client ID:      (auto-generated)
   - Client Secret:  (auto-generated)
   - Redirect URL:   https://your-app.npci.org.in/callback
   - Token Lifetime: 1800 (30 minutes)
5. Save

To obtain a token:
   POST https://instance.service-now.com/oauth_token.do
   Content-Type: application/x-www-form-urlencoded

   grant_type=password
   &client_id=<client_id>
   &client_secret=<client_secret>
   &username=admin
   &password=<password>

Response:
{
  "access_token": "abc123...",
  "refresh_token": "def456...",
  "scope": "useraccount",
  "token_type": "Bearer",
  "expires_in": 1800
}

Then use:
   Authorization: Bearer abc123...
```

### 1.3 Common Query Parameters

Every Table API call supports these parameters:

```
Parameter               Type      Description                                  Example
----------------------  --------  -------------------------------------------  ---------------------------
sysparm_query           string    Encoded query string                         state=1^priority=1
sysparm_fields          string    Comma-separated field list                   number,short_description
sysparm_limit           integer   Max records to return (default 10000)        10
sysparm_offset          integer   Starting record index for pagination         20
sysparm_display_value   string    Return display values: true, false, all      true
sysparm_exclude_        string    Exclude reference link URLs                  true
  reference_link
sysparm_suppress_       string    Suppress pagination header                   true
  pagination_header
sysparm_view            string    UI view to determine fields                  mobile
sysparm_query_category  string    Query category for filtering                 -
sysparm_query_no_domain string    Ignore domain separation                     true
sysparm_no_count        string    Skip row count for performance               true
```

### 1.4 Encoded Query Syntax

```
Operator    Syntax          Example
----------  --------------  ----------------------------------------
Equals      =               state=1
Not equals  !=              state!=7
Contains    LIKE            short_descriptionLIKEUPI
Starts with STARTSWITH      numberSTARTSWITHINC
Ends with   ENDSWITH        numberENDSWITH001
Less than   <               priority<3
Greater     >               priority>1
AND         ^               state=1^priority=1
OR          ^OR             priority=1^ORpriority=2
Order ASC   ORDERBY         ORDERBYnumber
Order DESC  ORDERBYDESC     ORDERBYDESCsys_created_on
NULL        ISEMPTY         assigned_toISEMPTY
NOT NULL    ISNOTEMPTY      assigned_toISNOTEMPTY
IN list     IN              stateIN1,2,3
Between     BETWEEN         sys_created_onBETWEENjavascript:gs.beginningOfLastMonth()@javascript:gs.endOfLastMonth()
```

### 1.5 Rate Limiting and Best Practices

```
Production Considerations:

1. Rate Limits (ServiceNow default):
   - Inbound REST:  Governed by instance capacity
   - Concurrent:    Typically 10-20 concurrent API sessions
   - Per-user:      Track via System Diagnostics > Stats

2. Performance Best Practices:
   - Always use sysparm_fields to limit returned data
   - Use sysparm_limit with pagination (never pull all records)
   - Use sysparm_no_count=true for large tables
   - Prefer PATCH over PUT (send only changed fields)
   - Use Aggregate API for counts instead of fetching records
   - Implement exponential backoff on 429 responses
   - Cache reference data (assignment groups, categories)

3. Security Best Practices:
   - Use OAuth 2.0 in production (never Basic Auth)
   - Create dedicated integration user accounts
   - Assign minimal ACLs to integration users
   - Log all API access for audit trail
   - Rotate credentials on a schedule
   - Use IP Access Control Lists (ACLs) to restrict source IPs

4. Response Codes:
   200  OK              - Successful GET, PUT, PATCH
   201  Created         - Successful POST
   204  No Content      - Successful DELETE
   400  Bad Request     - Malformed request body
   401  Unauthorized    - Invalid credentials
   403  Forbidden       - Insufficient ACL permissions
   404  Not Found       - Invalid table or sys_id
   405  Method Not      - HTTP method not supported
        Allowed
   429  Too Many        - Rate limit exceeded
        Requests
```

---

## Part 2: Inbound REST API -- CRUD Operations on Incidents

In this section, you will interact with your PDI using curl. Replace `your-instance` with your actual PDI hostname and `admin:password` with your credentials.

### 2.1 GET -- List Incidents

**Retrieve the 5 most recent incidents with selected fields:**

```bash
curl -s -u 'admin:password' \
  -H "Accept: application/json" \
  "https://your-instance.service-now.com/api/now/table/incident?sysparm_limit=5&sysparm_fields=number,short_description,priority,state,assignment_group&sysparm_display_value=true&sysparm_query=ORDERBYDESCsys_created_on" \
  | python3 -m json.tool
```

**Expected Response Structure:**

```json
{
  "result": [
    {
      "number": "INC0010001",
      "short_description": "UPI Transaction Service latency spike",
      "priority": "1 - Critical",
      "state": "New",
      "assignment_group": "Platform Engineering"
    },
    {
      "number": "INC0010002",
      "short_description": "UPI Settlement batch job delayed",
      "priority": "2 - High",
      "state": "In Progress",
      "assignment_group": "Platform Engineering"
    }
  ]
}
```

**Filtered query -- P1 incidents assigned to Platform Engineering:**

```bash
curl -s -u 'admin:password' \
  -H "Accept: application/json" \
  "https://your-instance.service-now.com/api/now/table/incident?sysparm_query=priority=1^assignment_group.name=Platform Engineering^stateIN1,2&sysparm_fields=number,short_description,state,assigned_to,sys_created_on&sysparm_display_value=true&sysparm_limit=10" \
  | python3 -m json.tool
```

### 2.2 GET -- Retrieve Single Incident by sys_id

```bash
curl -s -u 'admin:password' \
  -H "Accept: application/json" \
  "https://your-instance.service-now.com/api/now/table/incident/{sys_id}?sysparm_fields=number,short_description,description,priority,state,impact,urgency,assignment_group,assigned_to,category,subcategory,cmdb_ci,opened_at,resolved_at&sysparm_display_value=all" \
  | python3 -m json.tool
```

When using `sysparm_display_value=all`, each field returns both display and value:

```json
{
  "result": {
    "priority": {
      "display_value": "1 - Critical",
      "value": "1"
    },
    "state": {
      "display_value": "New",
      "value": "1"
    }
  }
}
```

### 2.3 POST -- Create Incident

**Create a UPI-specific incident with full field mapping:**

```bash
curl -s -u 'admin:password' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "https://your-instance.service-now.com/api/now/table/incident" \
  -d '{
    "short_description": "UPI Transaction Service latency spike detected",
    "description": "Prometheus alert: P95 latency exceeded 500ms threshold.\nCurrent value: 1.2s\nAffected service: UPI Transaction Service\nAlert source: Prometheus AlertManager\nDashboard: http://grafana:3000/d/upi-services",
    "category": "Software",
    "subcategory": "Operating System",
    "impact": "2",
    "urgency": "1",
    "assignment_group": "Platform Engineering",
    "caller_id": "ravi.kumar",
    "cmdb_ci": "UPI Transaction Service",
    "work_notes": "[AUTO] Incident created via REST API from monitoring alert. P95 latency: 1.2s (threshold: 500ms)."
  }' \
  | python3 -m json.tool
```

**Expected Response (201 Created):**

```json
{
  "result": {
    "sys_id": "a1b2c3d4e5f6...",
    "number": "INC0010045",
    "short_description": "UPI Transaction Service latency spike detected",
    "state": "1",
    "priority": "1",
    "impact": "2",
    "urgency": "1",
    "assignment_group": {
      "link": "https://instance.service-now.com/api/now/table/sys_user_group/...",
      "value": "abc123..."
    },
    "sys_created_on": "2026-09-23 10:15:00",
    "sys_created_by": "admin"
  }
}
```

**Record the returned sys_id -- you will need it for PUT and PATCH operations.**

### 2.4 PUT -- Full Update of Incident

PUT replaces ALL writable fields. Any field not included is set to its default or emptied. Use PUT when you need to overwrite the entire record.

```bash
curl -s -u 'admin:password' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PUT \
  "https://your-instance.service-now.com/api/now/table/incident/{sys_id}" \
  -d '{
    "state": "2",
    "assigned_to": "ravi.kumar",
    "work_notes": "Investigating latency spike. Checking Grafana dashboards and Prometheus metrics. Initial assessment: possible database connection pool exhaustion.",
    "short_description": "UPI Transaction Service latency spike detected",
    "impact": "2",
    "urgency": "1",
    "category": "Software",
    "assignment_group": "Platform Engineering",
    "caller_id": "ravi.kumar"
  }' \
  | python3 -m json.tool
```

### 2.5 PATCH -- Partial Update of Incident (Preferred)

PATCH only updates the fields you send. This is safer and more efficient than PUT.

```bash
curl -s -u 'admin:password' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X PATCH \
  "https://your-instance.service-now.com/api/now/table/incident/{sys_id}" \
  -d '{
    "state": "2",
    "assigned_to": "ravi.kumar",
    "work_notes": "Root cause identified: connection pool max_size=10 insufficient for current load. Scaling to max_size=50. Monitoring recovery."
  }' \
  | python3 -m json.tool
```

### 2.6 DELETE -- Why It Is Rarely Used

```
In ITSM, records are almost never deleted. Here is why:

1. Audit Trail:  ITIL requires full history of every incident, change, problem
2. Compliance:   Financial regulators (RBI, NPCI) mandate data retention
3. Reporting:    Deleted records break metrics (MTTR, SLA compliance, trend analysis)
4. Referential:  Other records (problems, changes, tasks) reference incidents

Instead, use the SOFT DELETE pattern:
  - Set state to "Closed" or "Canceled"
  - Set active to "false"
  - Records remain queryable but are filtered from active views

If you absolutely must delete (e.g., test data cleanup in PDI):
```

```bash
# WARNING: Destructive operation -- PDI/dev only
curl -s -u 'admin:password' \
  -X DELETE \
  "https://your-instance.service-now.com/api/now/table/incident/{sys_id}"
```

```
Response: 204 No Content (success, no body returned)

In production, DELETE is typically blocked by ACLs for the integration user.
```

### 2.7 Aggregate API -- Get Incident Statistics

Instead of fetching all incidents and counting client-side, use the Aggregate API:

```bash
# Count open incidents by priority
curl -s -u 'admin:password' \
  -H "Accept: application/json" \
  "https://your-instance.service-now.com/api/now/stats/incident?sysparm_query=active=true&sysparm_count=true&sysparm_group_by=priority&sysparm_display_value=true" \
  | python3 -m json.tool
```

**Response:**

```json
{
  "result": [
    {
      "groupby_fields": [
        {
          "field": "priority",
          "value": "1 - Critical"
        }
      ],
      "stats": {
        "count": "3"
      }
    },
    {
      "groupby_fields": [
        {
          "field": "priority",
          "value": "2 - High"
        }
      ],
      "stats": {
        "count": "7"
      }
    }
  ]
}
```

```bash
# Average time to resolution for closed incidents (in seconds)
curl -s -u 'admin:password' \
  -H "Accept: application/json" \
  "https://your-instance.service-now.com/api/now/stats/incident?sysparm_query=state=7&sysparm_avg_fields=calendar_duration&sysparm_display_value=true" \
  | python3 -m json.tool
```

---

## Part 3: Scripted REST API -- Build Custom Endpoints

Scripted REST APIs let you build custom endpoints with full control over request processing, response format, and business logic. This is how you build production-grade integrations natively inside ServiceNow.

### 3.1 Create the API: "UPI Integration API"

```
1. Navigate to: System Web Services > Scripted REST APIs
2. Click "New"
3. Fill in:

   Field           Value
   -------         -----
   Name:           UPI Integration API
   API ID:         x_upi
   API Namespace:  (auto-populated from scope, or use global)
   Protection:     None
   Active:         true

4. Save

The base path will be: /api/x_upi/v1
(Versioning is automatic when you set up resources)
```

### 3.2 Resource 1: GET /api/x_upi/v1/service-health

**Purpose:** Returns health status of all UPI Configuration Items from the CMDB.

```
1. In the UPI Integration API record, scroll to "Resources"
2. Click "New"
3. Fill in:

   Field                Value
   -------              -----
   Name:                Service Health
   HTTP Method:         GET
   Relative path:       /service-health
   Requires auth:       true (checked)
   Requires ACL auth:   false

4. In the Script field, enter the following:
```

**Server-Side Script:**

```javascript
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {

    var services = [];
    var gr = new GlideRecord('cmdb_ci_service');
    gr.addQuery('name', 'CONTAINS', 'UPI');
    gr.query();

    while (gr.next()) {
        var service = {};
        service.sys_id = gr.getUniqueValue();
        service.name = gr.getValue('name');
        service.operational_status = gr.getDisplayValue('operational_status');
        service.environment = gr.getDisplayValue('u_environment') || 'Production';

        // Get last incident for this CI
        var incGR = new GlideRecord('incident');
        incGR.addQuery('cmdb_ci', gr.getUniqueValue());
        incGR.orderByDesc('sys_created_on');
        incGR.setLimit(1);
        incGR.query();

        if (incGR.next()) {
            service.last_incident = {
                number: incGR.getValue('number'),
                short_description: incGR.getValue('short_description'),
                priority: incGR.getDisplayValue('priority'),
                state: incGR.getDisplayValue('state'),
                opened_at: incGR.getValue('opened_at')
            };
        } else {
            service.last_incident = null;
        }

        // Check SLA compliance
        var slaGR = new GlideRecord('task_sla');
        slaGR.addQuery('task.cmdb_ci', gr.getUniqueValue());
        slaGR.addQuery('active', true);
        slaGR.query();

        service.active_slas = slaGR.getRowCount();
        service.sla_breached = false;

        var slaCheck = new GlideRecord('task_sla');
        slaCheck.addQuery('task.cmdb_ci', gr.getUniqueValue());
        slaCheck.addQuery('has_breached', true);
        slaCheck.addQuery('active', true);
        slaCheck.query();
        if (slaCheck.hasNext()) {
            service.sla_breached = true;
        }

        services.push(service);
    }

    var body = {
        status: 'success',
        count: services.length,
        timestamp: new GlideDateTime().getDisplayValue(),
        services: services
    };

    response.setBody(body);
    response.setStatus(200);

})(request, response);
```

**Test with curl:**

```bash
curl -s -u 'admin:password' \
  -H "Accept: application/json" \
  "https://your-instance.service-now.com/api/x_upi/v1/service-health" \
  | python3 -m json.tool
```

**Expected Response:**

```json
{
  "result": {
    "status": "success",
    "count": 4,
    "timestamp": "2026-09-23 10:30:00",
    "services": [
      {
        "sys_id": "abc123...",
        "name": "UPI Transaction Service",
        "operational_status": "Operational",
        "environment": "Production",
        "last_incident": {
          "number": "INC0010045",
          "short_description": "UPI Transaction Service latency spike detected",
          "priority": "1 - Critical",
          "state": "In Progress",
          "opened_at": "2026-09-23 10:15:00"
        },
        "active_slas": 1,
        "sla_breached": false
      },
      {
        "sys_id": "def456...",
        "name": "UPI Settlement Service",
        "operational_status": "Operational",
        "environment": "Production",
        "last_incident": null,
        "active_slas": 0,
        "sla_breached": false
      }
    ]
  }
}
```

### 3.3 Resource 2: POST /api/x_upi/v1/alert

**Purpose:** Accepts Prometheus AlertManager webhook payload and creates or deduplicates incidents. This is the native ServiceNow equivalent of what Snow Bridge does externally.

```
1. In the UPI Integration API record, go to Resources
2. Click "New"
3. Fill in:

   Field                Value
   -------              -----
   Name:                Alert Receiver
   HTTP Method:         POST
   Relative path:       /alert
   Requires auth:       true
```

**Server-Side Script:**

```javascript
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {

    try {
        var body = request.body.data;
        var alerts = body.alerts;

        if (!alerts || !Array.isArray(alerts)) {
            response.setStatus(400);
            response.setBody({
                status: 'error',
                message: 'Invalid payload: expected alerts array'
            });
            return;
        }

        var results = [];
        var severityMap = {
            'critical': { impact: '1', urgency: '1' },
            'warning':  { impact: '2', urgency: '2' },
            'info':     { impact: '3', urgency: '3' }
        };

        for (var i = 0; i < alerts.length; i++) {
            var alert = alerts[i];
            var labels = alert.labels || {};
            var annotations = alert.annotations || {};
            var status = alert.status || 'firing';
            var alertName = labels.alertname || 'Unknown Alert';
            var severity = labels.severity || 'warning';
            var service = labels.application || labels.job || 'unknown';
            var instance = labels.instance || 'unknown';

            if (status === 'firing') {
                // --- DEDUPLICATION CHECK ---
                // Look for active incident with same alert name and CI
                var dedupGR = new GlideRecord('incident');
                dedupGR.addQuery('short_description', 'CONTAINS', alertName);
                dedupGR.addQuery('active', true);

                // Also match on CI if possible
                var ciGR = new GlideRecord('cmdb_ci_service');
                ciGR.addQuery('name', 'CONTAINS', service);
                ciGR.setLimit(1);
                ciGR.query();
                var ciSysId = '';
                if (ciGR.next()) {
                    ciSysId = ciGR.getUniqueValue();
                    dedupGR.addQuery('cmdb_ci', ciSysId);
                }

                dedupGR.setLimit(1);
                dedupGR.query();

                if (dedupGR.next()) {
                    // Duplicate -- add work note to existing incident
                    dedupGR.work_notes = '[AUTO-DEDUP] Alert fired again at ' +
                        (alert.startsAt || 'unknown') +
                        '. Instance: ' + instance +
                        '. Alert is still active.';
                    dedupGR.update();

                    results.push({
                        alert: alertName,
                        action: 'deduplicated',
                        incident: dedupGR.getValue('number'),
                        sys_id: dedupGR.getUniqueValue()
                    });
                    continue;
                }

                // --- CREATE NEW INCIDENT ---
                var priority = severityMap[severity] || severityMap['warning'];
                var summary = annotations.summary || alertName;
                var description = annotations.description || '';
                var runbook = annotations.runbook || '';

                var incGR = new GlideRecord('incident');
                incGR.initialize();
                incGR.short_description = '[AUTO] ' + summary;
                incGR.description =
                    'Alert: ' + alertName + '\n' +
                    'Service: ' + service + '\n' +
                    'Instance: ' + instance + '\n' +
                    'Severity: ' + severity + '\n' +
                    'Fired at: ' + (alert.startsAt || 'unknown') + '\n\n' +
                    '--- Description ---\n' + description;

                if (runbook) {
                    incGR.description += '\n\n--- Runbook ---\n' + runbook;
                }

                incGR.impact = priority.impact;
                incGR.urgency = priority.urgency;
                incGR.category = 'Software';
                incGR.assignment_group.setDisplayValue('Platform Engineering');
                incGR.caller_id.setDisplayValue('admin');

                if (ciSysId) {
                    incGR.cmdb_ci = ciSysId;
                }

                incGR.work_notes = '[AUTO] Incident created by Scripted REST API. ' +
                    'Source: Prometheus AlertManager. Alert: ' + alertName;

                var newSysId = incGR.insert();

                results.push({
                    alert: alertName,
                    action: 'created',
                    incident: incGR.getValue('number'),
                    sys_id: newSysId
                });

            } else if (status === 'resolved') {
                // --- RESOLVE: Add work note to matching incident ---
                var resolveGR = new GlideRecord('incident');
                resolveGR.addQuery('short_description', 'CONTAINS', alertName);
                resolveGR.addQuery('active', true);
                resolveGR.setLimit(1);
                resolveGR.query();

                if (resolveGR.next()) {
                    resolveGR.work_notes = '[AUTO] Alert resolved at ' +
                        (alert.endsAt || 'unknown') +
                        '. Monitoring confirms service has recovered.';
                    resolveGR.update();

                    results.push({
                        alert: alertName,
                        action: 'resolution_noted',
                        incident: resolveGR.getValue('number')
                    });
                } else {
                    results.push({
                        alert: alertName,
                        action: 'no_matching_incident',
                        message: 'No active incident found for resolved alert'
                    });
                }
            }
        }

        response.setStatus(200);
        response.setBody({
            status: 'processed',
            count: results.length,
            results: results
        });

    } catch (ex) {
        gs.error('UPI Alert API error: ' + ex.message);
        response.setStatus(500);
        response.setBody({
            status: 'error',
            message: 'Internal server error: ' + ex.message
        });
    }

})(request, response);
```

**Test with curl (simulating AlertManager payload):**

```bash
curl -s -u 'admin:password' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  "https://your-instance.service-now.com/api/x_upi/v1/alert" \
  -d '{
    "receiver": "snow-bridge",
    "status": "firing",
    "alerts": [
      {
        "status": "firing",
        "labels": {
          "alertname": "HighErrorRate",
          "severity": "critical",
          "application": "upi-transaction-service",
          "instance": "upi-txn:8080"
        },
        "annotations": {
          "summary": "UPI Transaction Service error rate above 5%",
          "description": "Error rate is 12.5% over the last 5 minutes. Threshold: 5%. Affected endpoint: /api/v1/pay",
          "runbook": "https://wiki.npci.org.in/runbooks/upi-high-error-rate"
        },
        "startsAt": "2026-09-23T10:00:00.000Z",
        "generatorURL": "http://prometheus:9090/graph?g0.expr=rate(http_requests_total{status=~\"5..\"}[5m])"
      }
    ],
    "groupLabels": {
      "alertname": "HighErrorRate"
    },
    "commonLabels": {
      "severity": "critical"
    }
  }' \
  | python3 -m json.tool
```

### 3.4 Resource 3: GET /api/x_upi/v1/metrics

**Purpose:** Returns ITSM operational metrics for consumption by external dashboards (Grafana, custom portals).

```
1. Create new Resource in UPI Integration API
2. Name: ITSM Metrics
3. HTTP Method: GET
4. Relative path: /metrics
```

**Server-Side Script:**

```javascript
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {

    var metrics = {};

    // --- Open Incidents by Priority ---
    var priorities = { '1': 0, '2': 0, '3': 0, '4': 0, '5': 0 };
    var incGR = new GlideRecord('incident');
    incGR.addQuery('active', true);
    incGR.query();
    var totalOpen = 0;
    while (incGR.next()) {
        var p = incGR.getValue('priority') || '5';
        if (priorities.hasOwnProperty(p)) {
            priorities[p]++;
        }
        totalOpen++;
    }
    metrics.open_incidents = {
        total: totalOpen,
        by_priority: {
            'P1_Critical': priorities['1'],
            'P2_High': priorities['2'],
            'P3_Moderate': priorities['3'],
            'P4_Low': priorities['4'],
            'P5_Planning': priorities['5']
        }
    };

    // --- MTTR (Mean Time to Resolve) for last 30 days ---
    var resolvedCount = 0;
    var totalDuration = 0;
    var mttrGR = new GlideRecord('incident');
    mttrGR.addQuery('state', '6'); // Resolved
    mttrGR.addQuery('resolved_at', '>', gs.daysAgoStart(30));
    mttrGR.query();
    while (mttrGR.next()) {
        var opened = new GlideDateTime(mttrGR.getValue('opened_at'));
        var resolved = new GlideDateTime(mttrGR.getValue('resolved_at'));
        var duration = GlideDateTime.subtract(opened, resolved);
        totalDuration += parseInt(duration.getNumericValue());
        resolvedCount++;
    }
    metrics.mttr = {
        period: 'last_30_days',
        resolved_count: resolvedCount,
        avg_minutes: resolvedCount > 0
            ? Math.round(totalDuration / resolvedCount / 60000)
            : 0
    };

    // --- SLA Compliance ---
    var slaTotal = 0;
    var slaMet = 0;
    var slaGR = new GlideRecord('task_sla');
    slaGR.addQuery('active', false);
    slaGR.addQuery('sys_updated_on', '>', gs.daysAgoStart(30));
    slaGR.query();
    while (slaGR.next()) {
        slaTotal++;
        if (slaGR.getValue('has_breached') == 'false') {
            slaMet++;
        }
    }
    metrics.sla_compliance = {
        period: 'last_30_days',
        total_slas: slaTotal,
        met: slaMet,
        breached: slaTotal - slaMet,
        compliance_pct: slaTotal > 0
            ? Math.round((slaMet / slaTotal) * 10000) / 100
            : 100
    };

    // --- Open Problems and Changes ---
    var probGR = new GlideAggregate('problem');
    probGR.addQuery('active', true);
    probGR.addAggregate('COUNT');
    probGR.query();
    metrics.open_problems = probGR.next()
        ? parseInt(probGR.getAggregate('COUNT'))
        : 0;

    var chgGR = new GlideAggregate('change_request');
    chgGR.addQuery('active', true);
    chgGR.addAggregate('COUNT');
    chgGR.query();
    metrics.open_changes = chgGR.next()
        ? parseInt(chgGR.getAggregate('COUNT'))
        : 0;

    response.setStatus(200);
    response.setBody({
        status: 'success',
        generated_at: new GlideDateTime().getDisplayValue(),
        metrics: metrics
    });

})(request, response);
```

**Test with curl:**

```bash
curl -s -u 'admin:password' \
  -H "Accept: application/json" \
  "https://your-instance.service-now.com/api/x_upi/v1/metrics" \
  | python3 -m json.tool
```

### 3.5 Error Handling Best Practices for Scripted REST APIs

```javascript
// Pattern: Consistent error response structure
// Use this pattern in all your Scripted REST resources

function sendError(response, statusCode, errorCode, message, detail) {
    response.setStatus(statusCode);
    response.setBody({
        error: {
            code: errorCode,
            message: message,
            detail: detail || '',
            timestamp: new GlideDateTime().getDisplayValue()
        }
    });
}

// Usage examples:
// sendError(response, 400, 'INVALID_PAYLOAD', 'Missing required field: alerts');
// sendError(response, 404, 'CI_NOT_FOUND', 'No CI found with name: ' + ciName);
// sendError(response, 403, 'INSUFFICIENT_ROLE', 'Requires x_upi.api_user role');
// sendError(response, 429, 'RATE_LIMITED', 'Too many requests. Retry after 60s');
// sendError(response, 500, 'INTERNAL_ERROR', 'Unexpected error', ex.message);
```

---

## Part 4: Outbound REST -- Webhooks and External API Calls

Outbound REST Messages allow ServiceNow to call external APIs when events occur.

### 4.1 Create REST Message: "UPI Slack Notification"

```
1. Navigate to: System Web Services > Outbound > REST Message
2. Click "New"
3. Fill in:

   Field                  Value
   -------                -----
   Name:                  UPI Slack Notification
   Endpoint:              https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   Authentication type:   No authentication (Slack webhook does not require it)

4. Save
```

### 4.2 Create HTTP Method: POST Notification

```
1. In the REST Message record, scroll to "HTTP Methods"
2. Click "New"
3. Fill in:

   Field                Value
   -------              -----
   Name:                Post Notification
   HTTP Method:         POST
   Endpoint:            (inherits from parent)

4. In "HTTP Request" tab, add headers:
   - Content-Type: application/json

5. In the "Content" field, enter:
```

**Request Body (with variable substitution):**

```json
{
  "channel": "#upi-incidents",
  "username": "ServiceNow Bot",
  "icon_emoji": ":rotating_light:",
  "attachments": [
    {
      "color": "${color}",
      "title": "${incident_number}: ${short_description}",
      "title_link": "https://your-instance.service-now.com/nav_to.do?uri=incident.do?sys_id=${sys_id}",
      "fields": [
        {
          "title": "Priority",
          "value": "${priority}",
          "short": true
        },
        {
          "title": "State",
          "value": "${state}",
          "short": true
        },
        {
          "title": "Assigned To",
          "value": "${assigned_to}",
          "short": true
        },
        {
          "title": "Assignment Group",
          "value": "${assignment_group}",
          "short": true
        },
        {
          "title": "CI",
          "value": "${cmdb_ci}",
          "short": true
        },
        {
          "title": "Category",
          "value": "${category}",
          "short": true
        }
      ],
      "footer": "ServiceNow ITSM | NPCI UPI Platform",
      "ts": "${epoch_time}"
    }
  ]
}
```

```
6. In "Variable Substitutions", add each variable:
   - incident_number
   - short_description
   - priority
   - state
   - assigned_to
   - assignment_group
   - cmdb_ci
   - category
   - color
   - sys_id
   - epoch_time

7. Save
```

### 4.3 Business Rule to Trigger Slack Notification

**Create a Business Rule that fires the Slack webhook whenever an incident state changes.**

```
1. Navigate to: System Definition > Business Rules
2. Click "New"
3. Fill in:

   Field              Value
   -------            -----
   Name:              UPI Slack Notification on State Change
   Table:             Incident [incident]
   Active:            true
   Advanced:          true (checked)
   When:              after
   Update:            true (checked)
   Filter Conditions: State | changes

4. In the "Script" tab:
```

```javascript
(function executeRule(current, previous /*null when async*/) {

    // Determine color based on priority
    var colorMap = {
        '1': '#FF0000',  // Critical - Red
        '2': '#FF8C00',  // High - Orange
        '3': '#FFD700',  // Moderate - Yellow
        '4': '#4169E1',  // Low - Blue
        '5': '#808080'   // Planning - Gray
    };
    var color = colorMap[current.getValue('priority')] || '#808080';

    try {
        var r = new sn_ws.RESTMessageV2('UPI Slack Notification', 'Post Notification');
        r.setStringParameterNoEscape('incident_number', current.getValue('number'));
        r.setStringParameterNoEscape('short_description', current.getValue('short_description'));
        r.setStringParameterNoEscape('priority', current.getDisplayValue('priority'));
        r.setStringParameterNoEscape('state', current.getDisplayValue('state'));
        r.setStringParameterNoEscape('assigned_to', current.getDisplayValue('assigned_to'));
        r.setStringParameterNoEscape('assignment_group', current.getDisplayValue('assignment_group'));
        r.setStringParameterNoEscape('cmdb_ci', current.getDisplayValue('cmdb_ci'));
        r.setStringParameterNoEscape('category', current.getDisplayValue('category'));
        r.setStringParameterNoEscape('color', color);
        r.setStringParameterNoEscape('sys_id', current.getUniqueValue());
        r.setStringParameterNoEscape('epoch_time', String(Math.floor(new Date().getTime() / 1000)));

        var resp = r.execute();
        var httpStatus = resp.getStatusCode();

        if (httpStatus != 200) {
            gs.error('Slack notification failed. HTTP ' + httpStatus +
                ': ' + resp.getBody());
        } else {
            gs.info('Slack notification sent for ' + current.getValue('number') +
                ' state change to ' + current.getDisplayValue('state'));
        }

    } catch (ex) {
        gs.error('Slack notification error for ' + current.getValue('number') +
            ': ' + ex.message);
    }

})(current, previous);
```

### 4.4 Create REST Message: "Prometheus Query"

**Purpose:** Query Prometheus API from ServiceNow to fetch real-time metrics for a CI.

```
1. Navigate to: System Web Services > Outbound > REST Message
2. Click "New"
3. Fill in:

   Name:                  Prometheus Metric Query
   Endpoint:              http://prometheus:9090/api/v1/query
   Authentication type:   No authentication

4. Create HTTP Method:
   Name:         Query Metric
   HTTP Method:  GET
   Endpoint:     http://prometheus:9090/api/v1/query?query=${promql_query}

5. Variable Substitutions:
   - promql_query (test value: up)

6. Save
```

**Script Include to use this REST Message:**

```
1. Navigate to: System Definition > Script Includes
2. Click "New"
3. Fill in:

   Name:        UPIPrometheusHelper
   API Name:    global.UPIPrometheusHelper
   Client callable: false
   Active:      true
```

```javascript
var UPIPrometheusHelper = Class.create();
UPIPrometheusHelper.prototype = {
    initialize: function() {
    },

    /**
     * Query Prometheus for a specific metric value.
     * @param {string} promqlQuery - PromQL expression (e.g., "rate(http_requests_total[5m])")
     * @returns {object} - { success: bool, value: string, timestamp: string, error: string }
     */
    queryMetric: function(promqlQuery) {
        try {
            var r = new sn_ws.RESTMessageV2('Prometheus Metric Query', 'Query Metric');
            r.setStringParameterNoEscape('promql_query', encodeURIComponent(promqlQuery));

            var resp = r.execute();
            var httpStatus = resp.getStatusCode();
            var body = JSON.parse(resp.getBody());

            if (httpStatus == 200 && body.status === 'success') {
                var result = body.data.result;
                if (result && result.length > 0) {
                    return {
                        success: true,
                        metric: result[0].metric,
                        value: result[0].value[1],
                        timestamp: result[0].value[0]
                    };
                }
                return { success: true, value: null, message: 'No data returned' };
            }

            return { success: false, error: 'HTTP ' + httpStatus + ': ' + body.error };

        } catch (ex) {
            return { success: false, error: ex.message };
        }
    },

    /**
     * Get current error rate for a specific UPI service.
     * @param {string} serviceName - e.g., "upi-transaction-service"
     * @returns {object} - { success: bool, error_rate_pct: number }
     */
    getErrorRate: function(serviceName) {
        var query = 'rate(http_requests_total{application="' + serviceName +
            '",status=~"5.."}[5m]) / rate(http_requests_total{application="' +
            serviceName + '"}[5m]) * 100';
        var result = this.queryMetric(query);
        if (result.success && result.value !== null) {
            result.error_rate_pct = Math.round(parseFloat(result.value) * 100) / 100;
        }
        return result;
    },

    /**
     * Get P95 latency for a specific UPI service.
     * @param {string} serviceName - e.g., "upi-transaction-service"
     * @returns {object} - { success: bool, p95_latency_ms: number }
     */
    getP95Latency: function(serviceName) {
        var query = 'histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{application="' +
            serviceName + '"}[5m])) * 1000';
        var result = this.queryMetric(query);
        if (result.success && result.value !== null) {
            result.p95_latency_ms = Math.round(parseFloat(result.value) * 100) / 100;
        }
        return result;
    },

    type: 'UPIPrometheusHelper'
};
```

**Usage in a Business Rule or Flow:**

```javascript
var prom = new UPIPrometheusHelper();
var errorRate = prom.getErrorRate('upi-transaction-service');
gs.info('Current error rate: ' + errorRate.error_rate_pct + '%');

var latency = prom.getP95Latency('upi-transaction-service');
gs.info('Current P95 latency: ' + latency.p95_latency_ms + 'ms');
```

---

## Part 5: Integration Hub

Integration Hub provides a no-code/low-code framework for building integrations using Spokes and Actions within Flow Designer.

### 5.1 Integration Hub Overview

```
Integration Hub Architecture:

  Flow Designer                Integration Hub
  +-----------------+         +---------------------------+
  | Trigger          |         |  Spokes                   |
  |  (Incident       |-------->|   - Slack Spoke           |
  |   created)       |         |   - Email Spoke           |
  | Actions          |         |   - REST Spoke            |
  |  (Send Slack     |         |   - JDBC Spoke            |
  |   notification)  |         |   - ServiceNow Spoke      |
  +-----------------+         |   - Custom Spokes          |
                               +---------------------------+
                                          |
                                          v
                               +---------------------------+
                               | External Systems           |
                               |  - Slack workspace         |
                               |  - Email server            |
                               |  - REST endpoints          |
                               |  - Databases               |
                               +---------------------------+

Key Concepts:
  Spoke:   A bundle of reusable actions for a specific system (e.g., Slack Spoke)
  Action:  A unit of work within a spoke (e.g., "Send Message to Channel")
  Step:    An individual operation within an action (REST call, script, transform)
```

### 5.2 Available Spokes (Zurich)

```
Spoke               Actions Available                    License Required
------------------  -----------------------------------  ----------------
Slack               Send Message, Create Channel,        IntegrationHub
                    Upload File, Update Message
Email               Send Email, Send with Attachment     Included
REST                REST Step (any HTTP method)          IntegrationHub
JDBC                Execute Query, Execute Statement     IntegrationHub
ServiceNow          Create/Update/Delete Record,         Included
                    Lookup, Approval
Microsoft Teams     Send Message, Create Team            IntegrationHub
Jira                Create Issue, Update Issue            IntegrationHub
```

### 5.3 Build Custom Spoke Action: "Send UPI Alert to Slack"

If the Slack Spoke is not available on your PDI, you can build a custom action using the REST step.

```
Step 1: Create the Action

1. Navigate to: Flow Designer (Process Automation > Flow Designer)
2. Click "New" > "Action"
3. Fill in:
   - Action name:    Send UPI Alert to Slack
   - Application:    Global
   - Description:    Sends a formatted alert notification to the UPI Slack channel
4. Click "Submit"

Step 2: Define Inputs

Click "+ Add Input" and add the following:
  Label              Name              Type       Mandatory
  ----------------   ---------------   --------   ---------
  Incident Number    incident_number   String     Yes
  Short Description  short_desc        String     Yes
  Priority           priority          String     Yes
  State              state             String     Yes
  Assigned To        assigned_to       String     No
  CI Name            ci_name           String     No
  Webhook URL        webhook_url       String     Yes

Step 3: Add REST Step

1. Click "+" to add a step
2. Select "REST" (under Integration Hub or Utilities)
3. Configure:

   Connection:       Define Connection Inline
   Base URL:         (drag "webhook_url" input pill)
   HTTP Method:      POST
   Headers:
     - Content-Type: application/json

   Request Body:     Build with a Script step (see below)

Step 4: Add a Script Step (before REST step) to build the payload

  Script:
```

```javascript
(function execute(inputs, outputs) {

    var colorMap = {
        '1 - Critical': '#FF0000',
        '2 - High': '#FF8C00',
        '3 - Moderate': '#FFD700',
        '4 - Low': '#4169E1',
        '5 - Planning': '#808080'
    };

    var payload = {
        channel: '#upi-incidents',
        username: 'ServiceNow ITSM',
        attachments: [{
            color: colorMap[inputs.priority] || '#808080',
            title: inputs.incident_number + ': ' + inputs.short_desc,
            fields: [
                { title: 'Priority', value: inputs.priority, short: true },
                { title: 'State', value: inputs.state, short: true },
                { title: 'Assigned To', value: inputs.assigned_to || 'Unassigned', short: true },
                { title: 'CI', value: inputs.ci_name || 'N/A', short: true }
            ],
            footer: 'ServiceNow ITSM | NPCI UPI Platform'
        }]
    };

    outputs.slack_payload = JSON.stringify(payload);

})(inputs, outputs);
```

```
   Output Variable:
     Label: Slack Payload    Name: slack_payload    Type: String

Step 5: Wire the Script output into the REST step body
   - In the REST step, set Request Body to the "slack_payload" output from the Script step

Step 6: Define Outputs
   - HTTP Status Code (from REST step)
   - Response Body (from REST step)

Step 7: Publish the Action
   - Click "Publish" in the top right

Step 8: Use in a Flow (from Lab 20 flows)
   - Open any incident flow (e.g., "UPI P1 Incident Response")
   - Add action: "Send UPI Alert to Slack"
   - Map flow data to the action inputs
   - Activate
```

### 5.4 Using the Custom Action in a Flow

```
Example: Add to "UPI Critical Incident Auto-Response" flow (from Lab 20)

Flow:
  Trigger: Record Created [incident] where priority = 1
  Actions:
    1. Lookup Record - Get assignment group details
    2. Send UPI Alert to Slack                              <-- NEW
       - incident_number: Trigger > Incident Record > Number
       - short_desc:      Trigger > Incident Record > Short Description
       - priority:        Trigger > Incident Record > Priority (display)
       - state:           Trigger > Incident Record > State (display)
       - assigned_to:     Trigger > Incident Record > Assigned To (display)
       - ci_name:         Trigger > Incident Record > Configuration Item (display)
       - webhook_url:     https://hooks.slack.com/services/...
    3. Create Task - Create initial investigation task
    4. Send Email - Notify incident commander
```

---

## Part 6: Update Sets -- SDLC for ServiceNow

Update Sets are the primary mechanism for moving configuration changes between ServiceNow instances. They serve as the deployment unit in the ServiceNow development lifecycle.

### 6.1 What Are Update Sets?

```
An Update Set is a container that captures configuration changes as "customer updates."
When you modify a Business Rule, Client Script, UI Policy, Flow, or any configuration
record while an Update Set is active, that change is recorded in the Update Set.

Think of Update Sets as:
  - Git commits:       Each captures a set of related changes
  - Deployment package: Can be exported and imported to another instance
  - Audit trail:       Records who changed what, and when

Development Lifecycle:
  +-----------+        +-----------+        +-----------+
  |    DEV    |------->|   TEST    |------->|   PROD    |
  | Instance  | Export | Instance  | Export | Instance  |
  | (PDI)     | XML    | (QA/UAT)  | XML    | (Live)    |
  +-----------+        +-----------+        +-----------+
      Create &           Preview &            Preview &
      Complete           Commit               Commit
      Update Set         Update Set           Update Set
```

### 6.2 What Update Sets Capture vs. Do Not Capture

```
CAPTURED in Update Sets:
  - Business Rules, Client Scripts, Script Includes
  - UI Policies, UI Actions, UI Pages
  - Flows, Subflows, Actions (Flow Designer)
  - SLA Definitions, OLA Definitions
  - Notifications (Email templates, events)
  - Form layouts, List layouts, Related Lists
  - Catalog Items, Variables, Variable Sets
  - System Properties
  - ACLs (Access Control Rules)
  - Scheduled Jobs (sys_trigger)
  - Scripted REST APIs, REST Messages
  - Reports, Dashboards, Homepage configurations
  - Application Menus, Modules
  - Transform Maps, Import Sets (definitions)
  - Dictionary changes (new fields, modified fields)

NOT CAPTURED in Update Sets:
  - Data records (incidents, users, CI records, groups)
  - Attachment file content (by default)
  - LDAP/SSO configuration
  - Instance-specific properties (instance URL, SMTP server)
  - Some Scheduled Job execution data
  - User preferences and personal favorites
```

### 6.3 Step-by-Step: Create and Manage Update Sets

#### Step 6.3.1: Create Update Set

```
1. Navigate to: System Update Sets > Local Update Sets
   (or type: sys_update_set.list in the navigator filter)
2. Click "New"
3. Fill in:

   Field              Value
   -------            -----
   Name:              UPI ITSM Configuration v1.0
   Description:       Contains all ITSM customizations for NPCI UPI Platform:
                      - Business Rules (incident auto-assignment, P1 validations)
                      - Client Scripts (priority color coding, mandatory fields)
                      - UI Policies (field visibility rules)
                      - Flows (P1 auto-response, SLA breach notification)
                      - Scripted REST APIs (UPI Integration API)
                      - REST Messages (Slack notification, Prometheus query)
                      - SLA Definitions (P1-P5 resolution and response SLAs)
                      - Notifications (incident email templates)
   State:             In Progress
   Application:       Global

4. Click "Submit"
```

#### Step 6.3.2: Make It the Current Update Set

```
1. Look at the top-right of the ServiceNow banner
2. Click on the current Update Set name (shows "Default [Global]")
3. From the picker, select "UPI ITSM Configuration v1.0"
4. The banner now shows: "UPI ITSM Configuration v1.0"

All configuration changes you make from this point forward will be
captured in this Update Set.
```

#### Step 6.3.3: Create a Business Rule (Captured in Update Set)

```
1. Navigate to: System Definition > Business Rules
2. Click "New"
3. Fill in:

   Name:      UPI Auto-Categorize from CI
   Table:     Incident [incident]
   Active:    true
   Advanced:  true
   When:      before
   Insert:    true
   Update:    true

4. Filter Conditions: Configuration item | is not empty

5. Script:
```

```javascript
(function executeRule(current, previous /*null when async*/) {

    // Auto-categorize based on CI name
    var ciName = current.cmdb_ci.getDisplayValue();

    if (ciName && ciName.indexOf('UPI') >= 0) {
        current.category = 'Software';

        if (ciName.indexOf('Transaction') >= 0) {
            current.subcategory = 'Operating System';
            gs.info('Auto-categorized incident for UPI Transaction Service');
        } else if (ciName.indexOf('Settlement') >= 0) {
            current.subcategory = 'Operating System';
            gs.info('Auto-categorized incident for UPI Settlement Service');
        } else if (ciName.indexOf('Database') >= 0 || ciName.indexOf('DB') >= 0) {
            current.category = 'Database';
            current.subcategory = 'DB2';
            gs.info('Auto-categorized incident for UPI Database CI');
        }
    }

})(current, previous);
```

```
6. Click "Submit"

This Business Rule is now captured in the "UPI ITSM Configuration v1.0" Update Set.
```

#### Step 6.3.4: Create a UI Policy (Captured in Update Set)

```
1. Navigate to: System UI > UI Policies
2. Click "New"
3. Fill in:

   Table:              Incident [incident]
   Short description:  Require justification for P1 downgrade
   Active:             true
   On load:            false
   Reverse if false:   true
   Order:              200

4. Conditions:
   Priority | changes to | 2 - High
   AND
   Priority | was | 1 - Critical

5. UI Policy Actions:
   Field:      Work notes
   Mandatory:  true

6. Click "Submit"

This UI Policy is now captured in the same Update Set.
```

#### Step 6.3.5: Verify Captured Changes

```
1. Navigate to: System Update Sets > Local Update Sets
2. Open "UPI ITSM Configuration v1.0"
3. Scroll down to the "Customer Updates" related list
4. You should see entries for:
   - sys_script (Business Rule: UPI Auto-Categorize from CI)
   - sys_ui_policy (UI Policy: Require justification for P1 downgrade)
   - sys_ui_policy_action (UI Policy Action for the work notes field)

Each entry shows:
  - Name: the configuration record name
  - Type: the table it belongs to
  - Action: Insert or Update
  - Target name: human-readable identifier
```

#### Step 6.3.6: Complete the Update Set

```
1. Open "UPI ITSM Configuration v1.0"
2. Change the State from "In Progress" to "Complete"
3. Click "Update"

IMPORTANT:
  - Once completed, no more changes are captured in this Update Set
  - You cannot reopen a completed Update Set
  - If you need more changes, create a new Update Set (v1.1)
  - The current Update Set reverts to "Default"
```

#### Step 6.3.7: Export as XML

```
1. Open the completed "UPI ITSM Configuration v1.0"
2. Right-click the header bar
3. Select "Export > XML" (or use Related Links > "Export to XML")
4. The browser downloads: sys_remote_update_set_XXXXX.xml

This XML file contains ALL customer updates captured in the Update Set.
You can import this file on another instance.
```

#### Step 6.3.8: Import on Target Instance (Reference)

```
On the TARGET instance (Test or Production):

1. Navigate to: System Update Sets > Retrieved Update Sets
2. Click "Import Update Set from XML"
3. Choose the exported XML file
4. Click "Upload"
5. The Update Set appears with state "Loaded"
6. Open the Update Set
7. Click "Preview Update Set"
   - ServiceNow checks for conflicts:
     - Does the target have the same record?
     - Version conflicts?
     - Missing dependencies?
8. Review the Preview results:
   - Green: Safe to commit
   - Yellow: Warning (review recommended)
   - Red: Error (must resolve before commit)
9. Resolve any conflicts:
   - "Accept remote" (use incoming change)
   - "Reject" (keep current version)
10. Click "Commit Update Set"
11. All changes are applied to the target instance

ROLLBACK:
  If something goes wrong after commit:
  1. Navigate to the committed Update Set
  2. Click "Back Out Update Set" (Related Links)
  3. ServiceNow reverts all changes from this Update Set
  4. Verify the rollback in System Logs
```

### 6.4 Merge Update Sets

```
When you have multiple related Update Sets that should be deployed together:

1. Navigate to: System Update Sets > Merge Update Sets
2. Click "New Merge"
3. Fill in:
   Name:        UPI ITSM Complete Package Q3 2026
   Description: Merged package containing all UPI ITSM customizations

4. In the "Update Sets to Merge" related list, add:
   - UPI ITSM Configuration v1.0
   - UPI Flow Designer Automations v1.0
   - UPI SLA and Notifications v1.0

5. Click "Merge"

The result is a single Update Set containing all changes from the
component Update Sets. Export and deploy this merged set.
```

---

## Part 7: Automated Test Framework (ATF)

ATF lets you write and run automated tests against your ServiceNow configurations. Tests validate that Business Rules, Client Scripts, Flows, and other customizations work correctly after deployment.

### 7.1 ATF Overview

```
ATF Components:

  Test:          A single test case with steps and assertions
  Test Step:     An individual action (create record, impersonate user, assert)
  Test Suite:    A group of tests run together
  Test Runner:   Executes tests (browser-based for client-side tests)

Test Types:
  - Server-side:  Test Business Rules, Script Includes, Flows
  - Client-side:  Test Client Scripts, UI Policies, UI Actions (requires ATF Runner)
  - Record-based: Create/update/query records and assert outcomes

Navigation: System Diagnostics > Automated Test Framework (ATF)
```

### 7.2 Test 1: "Test: Incident Auto-Assignment"

**Validates that incidents with UPI-related CIs are auto-assigned to Platform Engineering.**

```
1. Navigate to: Automated Test Framework > Tests
2. Click "New"
3. Fill in:
   Name:         Test: Incident Auto-Assignment
   Description:  Validates that UPI incidents are auto-assigned to
                 Platform Engineering group and Ravi Kumar
   Active:       true

4. Click "Submit" to save, then open the test
```

**Add Test Steps:**

```
Step 1: Set up - Record the assignment group sys_id

  Step type:      Server Side Script
  Description:    Get Platform Engineering group sys_id
  Script:

    var gr = new GlideRecord('sys_user_group');
    gr.addQuery('name', 'Platform Engineering');
    gr.query();
    if (gr.next()) {
        outputs.group_sys_id = gr.getUniqueValue();
        stepResult.setOutputMessage('Found Platform Engineering: ' + gr.getUniqueValue());
        stepResult.setSuccess(true);
    } else {
        stepResult.setOutputMessage('Platform Engineering group not found');
        stepResult.setFailed('Group not found - prerequisite missing');
    }

Step 2: Create a test incident

  Step type:      Create a Record
  Table:          Incident [incident]
  Field values:
    Short description:   [ATF] Test UPI auto-assignment
    Category:            Software
    Impact:              1 - High
    Urgency:             1 - High
    Configuration item:  UPI Transaction Service
    Caller:              admin

  (Record variable name: test_incident)

Step 3: Assert assignment group

  Step type:       Assert Field Value
  Record:          ${test_incident}
  Table:           Incident [incident]
  Field:           Assignment group
  Operator:        is
  Expected value:  Platform Engineering

Step 4: Assert assigned to

  Step type:       Assert Field Value
  Record:          ${test_incident}
  Table:           Incident [incident]
  Field:           Assigned to
  Operator:        is
  Expected value:  Ravi Kumar

Step 5: Cleanup - delete test record

  Step type:      Delete Record
  Table:          Incident [incident]
  Record:         ${test_incident}
```

### 7.3 Test 2: "Test: SLA Attachment"

**Validates that creating a P1 incident automatically attaches the correct SLA.**

```
1. Create new test:
   Name:         Test: SLA Attachment on P1 Incident
   Description:  Verifies that P1 incidents get the correct Task SLA record attached
```

**Test Steps:**

```
Step 1: Create P1 incident

  Step type:      Create a Record
  Table:          Incident [incident]
  Field values:
    Short description:   [ATF] Test SLA attachment
    Impact:              1 - High
    Urgency:             1 - High
    Category:            Software
    Caller:              admin

  (Record variable name: p1_incident)

Step 2: Wait for SLA engine (important)

  Step type:      Server Side Script
  Description:    Brief pause for SLA engine to process
  Script:

    // SLA engine runs async; give it a moment
    gs.sleep(2000);
    stepResult.setSuccess(true);
    stepResult.setOutputMessage('Waited for SLA engine');

Step 3: Assert Task SLA record exists

  Step type:      Server Side Script
  Description:    Verify Task SLA was created
  Script:

    var slaGR = new GlideRecord('task_sla');
    slaGR.addQuery('task', inputs.p1_incident.sys_id);
    slaGR.query();

    if (slaGR.getRowCount() > 0) {
        stepResult.setSuccess(true);
        stepResult.setOutputMessage('Found ' + slaGR.getRowCount() +
            ' Task SLA record(s) for the P1 incident');

        // Store for next assertion
        slaGR.next();
        outputs.sla_name = slaGR.sla.getDisplayValue();
    } else {
        stepResult.setFailed('No Task SLA records found for P1 incident');
    }

Step 4: Assert SLA definition name

  Step type:      Server Side Script
  Description:    Verify correct SLA definition was attached
  Script:

    var slaGR = new GlideRecord('task_sla');
    slaGR.addQuery('task', inputs.p1_incident.sys_id);
    slaGR.query();

    var found = false;
    while (slaGR.next()) {
        var slaName = slaGR.sla.getDisplayValue();
        if (slaName.indexOf('P1') >= 0 || slaName.indexOf('Critical') >= 0) {
            found = true;
            stepResult.setOutputMessage('Correct SLA attached: ' + slaName);
            break;
        }
    }

    if (found) {
        stepResult.setSuccess(true);
    } else {
        stepResult.setFailed('Expected P1/Critical SLA definition not found');
    }

Step 5: Cleanup

  Step type:      Delete Record
  Table:          Incident [incident]
  Record:         ${p1_incident}
```

### 7.4 Test 3: "Test: Business Rule -- Prevent P1 Close Without Root Cause"

**Validates that P1 incidents cannot be closed without close_notes (root cause documentation).**

```
1. Create new test:
   Name:         Test: P1 Close Requires Root Cause
   Description:  Ensures Business Rule prevents closing P1 without close notes
```

**Test Steps:**

```
Step 1: Create P1 incident

  Step type:      Create a Record
  Table:          Incident [incident]
  Field values:
    Short description:   [ATF] Test P1 close validation
    Impact:              1 - High
    Urgency:             1 - High
    Category:            Software
    Caller:              admin
    State:               In Progress
    Assigned to:         admin

  (Record variable name: p1_close_test)

Step 2: Attempt to close without close_notes

  Step type:      Server Side Script
  Description:    Try closing P1 without close notes - expect failure
  Script:

    var gr = new GlideRecord('incident');
    gr.get(inputs.p1_close_test.sys_id);
    gr.state = 7;  // Closed
    gr.close_code = 'Solved (Permanently)';
    // Intentionally NOT setting close_notes

    var result = gr.update();

    // Check if the record was actually updated to Closed
    gr.get(inputs.p1_close_test.sys_id);
    var currentState = gr.getValue('state');

    if (currentState != '7') {
        stepResult.setSuccess(true);
        stepResult.setOutputMessage(
            'Business Rule correctly prevented closing P1 without close notes. ' +
            'Current state: ' + gr.getDisplayValue('state'));
    } else {
        stepResult.setFailed(
            'ERROR: P1 incident was closed without close notes. ' +
            'Business Rule validation is missing or inactive.');
    }

Step 3: Close with close_notes - expect success

  Step type:      Server Side Script
  Description:    Close P1 with close notes - should succeed
  Script:

    var gr = new GlideRecord('incident');
    gr.get(inputs.p1_close_test.sys_id);
    gr.state = 6;  // Resolved first
    gr.close_code = 'Solved (Permanently)';
    gr.close_notes = 'Root Cause: Connection pool exhaustion due to ' +
        'unclosed database connections. Fix: Increased pool size from ' +
        '10 to 50 and added connection timeout of 30s.';
    gr.update();

    // Now close
    gr.get(inputs.p1_close_test.sys_id);
    gr.state = 7; // Closed
    gr.update();

    gr.get(inputs.p1_close_test.sys_id);
    var currentState = gr.getValue('state');

    if (currentState == '6' || currentState == '7') {
        stepResult.setSuccess(true);
        stepResult.setOutputMessage(
            'P1 incident successfully resolved/closed with close notes. ' +
            'State: ' + gr.getDisplayValue('state'));
    } else {
        stepResult.setFailed(
            'Failed to close P1 even with close notes. State: ' +
            gr.getDisplayValue('state'));
    }

Step 4: Cleanup

  Step type:      Delete Record
  Table:          Incident [incident]
  Record:         ${p1_close_test}
```

### 7.5 Test Suite: "UPI ITSM Regression"

```
1. Navigate to: Automated Test Framework > Suites
2. Click "New"
3. Fill in:
   Name:         UPI ITSM Regression Suite
   Description:  Comprehensive regression tests for all NPCI UPI ITSM customizations.
                 Run after every Update Set deployment.
   Active:       true

4. In the "Tests" related list, add:
   - Test: Incident Auto-Assignment
   - Test: SLA Attachment on P1 Incident
   - Test: P1 Close Requires Root Cause

5. Click "Save"
```

### 7.6 Running Tests and Viewing Results

```
Running a Single Test:
1. Open the test record
2. Click "Run Test" (button in header or Related Links)
3. Wait for execution to complete
4. View the "Test Result" record:
   - Status: Success / Failure
   - Each step shows Pass/Fail with output messages
   - Duration of execution
   - Stack trace on failure

Running a Test Suite:
1. Open the Test Suite record
2. Click "Run Test Suite"
3. All tests execute in sequence
4. View "Test Suite Results":
   - Overall: Pass/Fail
   - Individual test results
   - Total duration
   - Failure details

Best Practices:
  - Run the regression suite after every Update Set commit
  - Include ATF tests IN the Update Set (they are configuration)
  - Name tests with clear prefix: "Test: <what it validates>"
  - Always include cleanup steps to remove test data
  - Use impersonation steps to test role-based behavior
  - Test both positive (should work) and negative (should fail) cases
```

---

## Part 8: ServiceNow CI/CD with Update Sets

### 8.1 Development Workflow

```
The standard ServiceNow SDLC follows a three-instance model:

+------------------+     +------------------+     +------------------+
|   DEVELOPMENT    |     |      TEST        |     |   PRODUCTION     |
|   (PDI / Dev)    |     |   (QA / UAT)     |     |   (Live)         |
+------------------+     +------------------+     +------------------+
| - Build configs  |     | - Import Update  |     | - Import Update  |
| - Write scripts  |     |   Sets           |     |   Sets           |
| - Create flows   | --> | - Preview &      | --> | - Preview &      |
| - Test locally   |     |   resolve        |     |   resolve        |
| - Complete       |     |   conflicts      |     |   conflicts      |
|   Update Set     |     | - Commit         |     | - Commit         |
| - Export XML     |     | - Run ATF tests  |     | - Smoke test     |
|                  |     | - UAT sign-off   |     | - Monitor        |
+------------------+     +------------------+     +------------------+

Environments at NPCI might look like:
  DEV:   devXXXXXX.service-now.com    (PDI or dev instance)
  TEST:  npcitest.service-now.com     (QA / UAT)
  PROD:  npci.service-now.com         (Production)
```

### 8.2 Update Set Naming Conventions

```
Follow a consistent naming convention across teams:

Pattern:  <Project>_<Component>_<Version>_<Date>

Examples:
  UPI_ITSM_IncidentRules_v1.0_20260923
  UPI_ITSM_FlowDesigner_v1.0_20260923
  UPI_ITSM_ScriptedRESTAPI_v1.0_20260923
  UPI_ITSM_SLAConfig_v1.0_20260923
  UPI_ITSM_MergedRelease_v1.0_20260923

Rules:
  - Never use spaces in names (use underscores)
  - Always include version number
  - Include date for traceability
  - Prefix with project/team name
  - Use "HOTFIX" prefix for emergency changes:
    HOTFIX_UPI_P1CloseValidation_v1.1_20260923
```

### 8.3 Batch Parent Update Sets

```
Parent Update Sets group related child Update Sets into a single deployable unit.

1. Navigate to: System Update Sets > Local Update Sets
2. Click "New"
3. Fill in:
   Name:    UPI ITSM Release 1.0 [PARENT]
   State:   In Progress
   Is batch: true (checked)

4. Create child Update Sets:
   - UPI ITSM Business Rules v1.0
     Parent: UPI ITSM Release 1.0 [PARENT]
   - UPI ITSM UI Policies v1.0
     Parent: UPI ITSM Release 1.0 [PARENT]
   - UPI ITSM Scripted REST API v1.0
     Parent: UPI ITSM Release 1.0 [PARENT]

5. Work in individual child Update Sets for different workstreams
6. Complete all children, then complete the parent
7. Export the parent -- it includes all children

Benefits:
  - Different developers work on different child Update Sets
  - Deploy as a single unit (parent)
  - Rollback is also a single operation
```

### 8.4 Source Control Integration

```
ServiceNow supports Git integration for version control:

Setup (Reference - requires Team Development license):
1. Navigate to: System Applications > Studio
2. Open your scoped application
3. Click "Source Control" > "Link to Source Control"
4. Configure:
   - URL:      https://github.com/npci/servicenow-upi-itsm.git
   - Branch:   main
   - Username: <git-username>
   - Password: <personal-access-token>

Workflow with Git:
  1. Developer creates a branch in Studio
  2. Makes changes (captured in Update Set AND versioned in Git)
  3. Commits to Git from Studio
  4. Opens Pull Request for review
  5. Merged to main branch
  6. CI/CD pipeline deploys via Update Set or App Repository

Benefits over Update Sets alone:
  - Full commit history with diffs
  - Code review via Pull Requests
  - Branch-based development
  - Merge conflict resolution with Git tooling
  - Automated testing in CI pipeline
```

### 8.5 App Repository

```
For scoped applications, ServiceNow provides an App Repository:

1. Publish your scoped app to the App Repository (System Applications > Studio)
2. Install on target instances from the App Repository
3. Version management is built in
4. Dependency tracking between apps

This is the preferred approach for:
  - Scoped applications (not global scope)
  - ISV/partner-developed applications
  - Applications shared across multiple instances
```

---

## Practice Exercises

### Exercise 1: Bulk Incident Creation via REST API

**Use curl to create 5 incidents with different priorities and categories:**

```bash
# Incident 1: P1 Critical - UPI Transaction Service down
curl -s -u 'admin:password' \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -X POST "https://your-instance.service-now.com/api/now/table/incident" \
  -d '{
    "short_description": "UPI Transaction Service completely unresponsive",
    "impact": "1", "urgency": "1",
    "category": "Software",
    "assignment_group": "Platform Engineering",
    "caller_id": "admin",
    "description": "All UPI transaction endpoints returning 503. No transactions processing."
  }' | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['number'], r['priority'])"

# Incident 2: P2 High - Settlement batch delayed
curl -s -u 'admin:password' \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -X POST "https://your-instance.service-now.com/api/now/table/incident" \
  -d '{
    "short_description": "UPI Settlement batch processing delayed by 2 hours",
    "impact": "2", "urgency": "2",
    "category": "Software",
    "assignment_group": "Platform Engineering",
    "caller_id": "admin",
    "description": "Nightly settlement batch started 2 hours late. Banks awaiting settlement files."
  }' | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['number'], r['priority'])"

# Incident 3: P3 Moderate - Dashboard loading slowly
curl -s -u 'admin:password' \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -X POST "https://your-instance.service-now.com/api/now/table/incident" \
  -d '{
    "short_description": "UPI Monitoring Dashboard loading slowly in Grafana",
    "impact": "2", "urgency": "3",
    "category": "Software",
    "assignment_group": "Platform Engineering",
    "caller_id": "admin",
    "description": "Grafana dashboards for UPI services taking >30s to load. Prometheus queries timing out."
  }' | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['number'], r['priority'])"

# Incident 4: P4 Low - Certificate expiry warning
curl -s -u 'admin:password' \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -X POST "https://your-instance.service-now.com/api/now/table/incident" \
  -d '{
    "short_description": "UPI API Gateway SSL certificate expiring in 30 days",
    "impact": "3", "urgency": "3",
    "category": "Network",
    "assignment_group": "Platform Engineering",
    "caller_id": "admin",
    "description": "SSL certificate for api.npci.org.in expires on 2026-10-23. Renewal required."
  }' | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['number'], r['priority'])"

# Incident 5: P5 Planning - Capacity planning request
curl -s -u 'admin:password' \
  -H "Content-Type: application/json" -H "Accept: application/json" \
  -X POST "https://your-instance.service-now.com/api/now/table/incident" \
  -d '{
    "short_description": "Plan UPI infrastructure capacity for Diwali peak season",
    "impact": "3", "urgency": "3",
    "category": "Hardware",
    "assignment_group": "Platform Engineering",
    "caller_id": "admin",
    "description": "Annual capacity planning for Diwali peak. Expected 3x normal transaction volume."
  }' | python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r['number'], r['priority'])"
```

### Exercise 2: Scripted REST API -- CI Lookup

**Build a Scripted REST API endpoint: GET /api/x_upi/v1/ci/{name}**

```
Requirements:
1. Accept CI name as path parameter
2. Query cmdb_ci_service for matching CI
3. Return:
   - CI details (name, operational_status, environment, sys_class_name)
   - Upstream dependencies (parent CIs)
   - Downstream dependencies (child CIs)
   - Active incidents for this CI
   - Active changes for this CI
4. Return 404 if CI not found

Resource configuration:
  Name:           CI Lookup
  HTTP Method:    GET
  Relative path:  /ci/{name}
```

**Server-Side Script:**

```javascript
(function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {

    var ciName = request.pathParams.name;

    if (!ciName) {
        response.setStatus(400);
        response.setBody({ error: 'CI name is required' });
        return;
    }

    // Decode URL-encoded name
    ciName = decodeURIComponent(ciName);

    // Find the CI
    var ciGR = new GlideRecord('cmdb_ci');
    ciGR.addQuery('name', ciName);
    ciGR.setLimit(1);
    ciGR.query();

    if (!ciGR.next()) {
        response.setStatus(404);
        response.setBody({
            error: 'CI not found',
            name: ciName,
            suggestion: 'Use /api/x_upi/v1/service-health to list all UPI CIs'
        });
        return;
    }

    var result = {
        sys_id: ciGR.getUniqueValue(),
        name: ciGR.getValue('name'),
        sys_class_name: ciGR.getValue('sys_class_name'),
        operational_status: ciGR.getDisplayValue('operational_status'),
        environment: ciGR.getDisplayValue('u_environment') || 'Not set',
        category: ciGR.getDisplayValue('category'),
        subcategory: ciGR.getDisplayValue('subcategory'),
        managed_by: ciGR.getDisplayValue('managed_by'),
        support_group: ciGR.getDisplayValue('support_group')
    };

    // --- Upstream (parent) relationships ---
    result.upstream = [];
    var upGR = new GlideRecord('cmdb_rel_ci');
    upGR.addQuery('child', ciGR.getUniqueValue());
    upGR.query();
    while (upGR.next()) {
        result.upstream.push({
            ci_name: upGR.parent.getDisplayValue(),
            relationship: upGR.type.getDisplayValue(),
            sys_id: upGR.getValue('parent')
        });
    }

    // --- Downstream (child) relationships ---
    result.downstream = [];
    var downGR = new GlideRecord('cmdb_rel_ci');
    downGR.addQuery('parent', ciGR.getUniqueValue());
    downGR.query();
    while (downGR.next()) {
        result.downstream.push({
            ci_name: downGR.child.getDisplayValue(),
            relationship: downGR.type.getDisplayValue(),
            sys_id: downGR.getValue('child')
        });
    }

    // --- Active Incidents ---
    result.active_incidents = [];
    var incGR = new GlideRecord('incident');
    incGR.addQuery('cmdb_ci', ciGR.getUniqueValue());
    incGR.addQuery('active', true);
    incGR.orderByDesc('priority');
    incGR.query();
    while (incGR.next()) {
        result.active_incidents.push({
            number: incGR.getValue('number'),
            short_description: incGR.getValue('short_description'),
            priority: incGR.getDisplayValue('priority'),
            state: incGR.getDisplayValue('state'),
            assigned_to: incGR.getDisplayValue('assigned_to')
        });
    }

    // --- Active Changes ---
    result.active_changes = [];
    var chgGR = new GlideRecord('change_request');
    chgGR.addQuery('cmdb_ci', ciGR.getUniqueValue());
    chgGR.addQuery('active', true);
    chgGR.query();
    while (chgGR.next()) {
        result.active_changes.push({
            number: chgGR.getValue('number'),
            short_description: chgGR.getValue('short_description'),
            type: chgGR.getDisplayValue('type'),
            state: chgGR.getDisplayValue('state'),
            planned_start: chgGR.getValue('start_date')
        });
    }

    response.setStatus(200);
    response.setBody({
        status: 'success',
        ci: result
    });

})(request, response);
```

**Test:**

```bash
curl -s -u 'admin:password' \
  -H "Accept: application/json" \
  "https://your-instance.service-now.com/api/x_upi/v1/ci/UPI%20Transaction%20Service" \
  | python3 -m json.tool
```

### Exercise 3: Outbound REST -- Webhook on Change Approval

```
Build an outbound REST integration that posts to a webhook when a Change Request
is approved (state changes to "Scheduled").

1. Create REST Message:
   Name:     UPI Change Approval Webhook
   Endpoint: https://your-webhook-endpoint.example.com/change-approved

2. Create HTTP Method:
   Name:     Post Approval
   Method:   POST
   Body:     JSON with change number, description, type, planned start/end,
             approved by, risk, CI affected

3. Create Business Rule:
   Table:    Change Request [change_request]
   When:     After Update
   Filter:   State changes to "Scheduled"
   Script:   Use sn_ws.RESTMessageV2 to send the webhook
```

### Exercise 4: Update Set for Labs 20-21

```
Create a comprehensive Update Set containing all customizations from Labs 20-21:

1. Create Update Set: "UPI_ITSM_Labs20-21_v1.0_YYYYMMDD"
2. Set as current
3. Recreate or modify each customization (they will be captured):
   - Business Rules from Lab 21
   - Client Scripts from Lab 21
   - UI Policies from Lab 21
   - Flows from Lab 20
   - Script Includes
   - SLA Definitions
   - Notifications
4. Review the Customer Updates list
5. Complete the Update Set
6. Export as XML
7. Document the Update Set contents in a manifest
```

### Exercise 5: ATF Tests for Lab 21 Business Rules

```
Write 3 additional ATF tests:

Test A: "Test: Auto-Priority Calculation"
  - Create incident with Impact=1, Urgency=2
  - Assert: Priority = 2 (High)
  - Create incident with Impact=2, Urgency=2
  - Assert: Priority = 3 (Moderate)

Test B: "Test: UPI Category Auto-Set from CI"
  - Create incident with cmdb_ci = "UPI Transaction Service"
  - Assert: Category = Software
  - Assert: Subcategory is set appropriately

Test C: "Test: Work Notes Mandatory on Reassignment"
  - Create incident assigned to Group A
  - Reassign to Group B without work notes
  - Assert: Prevented (or warning displayed)
  - Reassign with work notes
  - Assert: Success

Add all 3 tests to the "UPI ITSM Regression Suite"
```

---

## Appendix A: Snow Bridge Code Walkthrough

The Snow Bridge application (`demo-e2e-incident/services/snow-bridge/app.py`) is a Python Flask application that bridges Prometheus AlertManager with ServiceNow. Here is a detailed walkthrough of how it uses the ServiceNow REST API.

### A.1 Architecture

```
+-------------------+     +-----------------+     +-------------------+
| Prometheus        |     | Snow Bridge     |     | ServiceNow        |
| AlertManager      |     | (Flask App)     |     | Instance          |
+-------------------+     +-----------------+     +-------------------+
|                   |     |                 |     |                   |
| Alert fires       |---->| POST /webhook   |     |                   |
|                   |     |   Parse alert   |     |                   |
|                   |     |   Map fields    |---->| POST /api/now/    |
|                   |     |   Dedup check   |     |   table/incident  |
|                   |     |   Create INC    |     |   (Create)        |
|                   |     |                 |     |                   |
| Alert resolves    |---->| POST /webhook   |     |                   |
|                   |     |   Find INC      |---->| GET /api/now/     |
|                   |     |   Add work note |     |   table/incident  |
|                   |     |                 |---->| PATCH /api/now/   |
|                   |     |                 |     |   table/incident/ |
|                   |     |                 |     |   {sys_id}        |
+-------------------+     +-----------------+     +-------------------+
                          | GET /health     |
                          | GET /active-    |
                          |   alerts        |
                          | POST /test-     |
                          |   incident      |
                          +-----------------+
```

### A.2 Configuration (Lines 17-21)

```python
SNOW_INSTANCE = os.environ.get('SNOW_INSTANCE', 'https://devXXXXXX.service-now.com').rstrip('/')
SNOW_USER = os.environ.get('SNOW_USER', 'admin')
SNOW_PASSWORD = os.environ.get('SNOW_PASSWORD', 'password')
SNOW_ENABLED = os.environ.get('SNOW_ENABLED', 'true').lower() == 'true'
```

```
Key Points:
  - All configuration is via environment variables (12-factor app pattern)
  - SNOW_ENABLED flag allows dry-run mode (logs API calls but does not make them)
  - Instance URL has .rstrip('/') to normalize trailing slashes
  - In Docker Compose, these are set via .env file or environment section
```

### A.3 Severity Mapping (Lines 24-28)

```python
SEVERITY_MAP = {
    'critical': {'impact': '1', 'urgency': '1'},  # P1 Critical
    'warning':  {'impact': '2', 'urgency': '2'},   # P3 Moderate
    'info':     {'impact': '3', 'urgency': '3'},   # P5 Planning
}
```

```
This maps Prometheus alert severity labels to ServiceNow Impact/Urgency values.
ServiceNow calculates Priority from the Impact/Urgency matrix:

  Prometheus Severity    ServiceNow Impact   ServiceNow Urgency   Resulting Priority
  -------------------    -----------------   ------------------   ------------------
  critical               1 - High            1 - High             1 - Critical
  warning                2 - Medium          2 - Medium           3 - Moderate
  info                   3 - Low             3 - Low              5 - Planning
```

### A.4 Incident Creation (Lines 40-122)

```
The create_snow_incident() function:

1. EXTRACT: Pulls labels and annotations from the AlertManager payload
   - alertname, severity, application, instance from labels
   - summary, description, runbook from annotations

2. MAP: Transforms monitoring data to ITSM fields
   - short_description: "[AUTO] " + summary (truncated to 160 chars)
   - description: Formatted multi-line with all alert context
   - impact/urgency: From SEVERITY_MAP
   - category: From CATEGORY_MAP (service name to ITSM category)
   - assignment_group: "Platform Engineering" (hardcoded for UPI)

3. DEDUP: Checks in-memory dict (active_alerts) for existing alert
   - Key: "{alertname}_{service}_{instance}"
   - If found, returns existing incident number (no duplicate created)

4. DRY RUN: If SNOW_ENABLED=false, logs the payload and returns fake INC number

5. API CALL: POST to /api/now/table/incident
   - Auth: Basic Auth (SNOW_USER:SNOW_PASSWORD)
   - Headers: Content-Type: application/json, Accept: application/json
   - Body: JSON incident_data dict
   - Timeout: 30 seconds
   - Parses response for number and sys_id
   - Stores in active_alerts for dedup tracking

6. ERROR HANDLING: Catches requests.exceptions.RequestException
   - Logs error, returns None (incident not created)
   - Does NOT retry (could be enhanced with exponential backoff)
```

### A.5 Alert Resolution (Lines 125-168)

```
The resolve_snow_incident() function:

1. Constructs the alert_key and looks up the incident number in active_alerts
2. Removes it from active_alerts (pop)
3. If no matching incident found, logs and returns
4. If DRY RUN, logs the resolution and returns

5. Two API calls to ServiceNow:
   a. GET /api/now/table/incident?sysparm_query=number={inc_number}&sysparm_limit=1
      - Finds the incident by number to get its sys_id
      - This is necessary because we stored the number, not the sys_id

   b. PATCH /api/now/table/incident/{sys_id}
      - Adds a work_notes entry: "[AUTO] Alert resolved at {timestamp}"
      - Does NOT change the state (leaves that for human operators)
      - This is intentional: auto-resolution without human verification
        could mask recurring issues
```

### A.6 Webhook Endpoint (Lines 171-193)

```
POST /webhook receives the AlertManager payload format:

{
  "receiver": "snow-bridge",
  "status": "firing",           <-- overall status
  "alerts": [                   <-- array of individual alerts
    {
      "status": "firing",       <-- per-alert status
      "labels": { ... },
      "annotations": { ... },
      "startsAt": "...",
      "endsAt": "...",
      "generatorURL": "..."
    }
  ],
  "groupLabels": { ... },
  "commonLabels": { ... },
  "externalURL": "..."
}

Processing:
  - Iterates over each alert in the array
  - Routes to create_snow_incident() or resolve_snow_incident() based on status
  - Returns JSON summary of actions taken
  - Always returns 200 (even if individual incidents fail)
    This prevents AlertManager from retrying the entire batch
```

### A.7 Utility Endpoints (Lines 196-232)

```
GET /health
  Returns service status, SNOW_ENABLED flag, instance URL, active alert count.
  Used by Docker healthcheck and monitoring.

GET /active-alerts
  Returns the in-memory alert-to-incident mapping.
  Useful for debugging and verifying deduplication.

POST /test-incident
  Creates a manual test incident (bypasses AlertManager format).
  Accepts optional JSON body with alertname, severity, service, summary, description.
  Used during demos and initial setup verification.
```

### A.8 Limitations and Production Enhancements

```
Current Limitations:
  1. In-memory dedup: Lost on container restart (should use Redis or DB)
  2. No retry logic: Failed API calls are not retried
  3. No OAuth: Uses Basic Auth (acceptable for PDI, not production)
  4. No rate limiting: Could overwhelm ServiceNow if alert storm occurs
  5. Single-threaded: Flask dev server (should use gunicorn in production)
  6. No TLS verification: Should verify ServiceNow SSL certificate
  7. Hardcoded assignment: Always assigns to "Platform Engineering"

Production Enhancements:
  1. Use Redis for dedup state (survives restarts, shared across replicas)
  2. Implement exponential backoff with jitter for retries
  3. Switch to OAuth 2.0 client credentials flow
  4. Add rate limiting (token bucket algorithm)
  5. Deploy with gunicorn + multiple workers
  6. Add Prometheus metrics endpoint (/metrics) for self-monitoring
  7. Make assignment group configurable per service
  8. Add circuit breaker (stop calling ServiceNow if it is down)
  9. Queue alerts in RabbitMQ/Kafka for reliable delivery
  10. Add structured logging (JSON) for log aggregation
```

---

## Appendix B: Quick Reference -- API Endpoint Cheat Sheet

```
ACTION                                  METHOD   ENDPOINT
--------------------------------------  ------   ----------------------------------------
List incidents                          GET      /api/now/table/incident
Get single incident                     GET      /api/now/table/incident/{sys_id}
Create incident                         POST     /api/now/table/incident
Full update incident                    PUT      /api/now/table/incident/{sys_id}
Partial update incident                 PATCH    /api/now/table/incident/{sys_id}
Delete incident                         DELETE   /api/now/table/incident/{sys_id}

List CIs                                GET      /api/now/table/cmdb_ci
Get CI by class                         GET      /api/now/cmdb/instance/{className}
Get CI relationships                    GET      /api/now/table/cmdb_rel_ci

Incident stats                          GET      /api/now/stats/incident
Problem stats                           GET      /api/now/stats/problem
Change stats                            GET      /api/now/stats/change_request

Upload attachment                       POST     /api/now/attachment/file
List attachments                        GET      /api/now/attachment
Download attachment                     GET      /api/now/attachment/{sys_id}/file

Import set load                         POST     /api/now/import/{staging_table}
Transform import set                    POST     /api/now/import/{staging_table}/{sys_id}

Create change request                   POST     /api/now/table/change_request
Create problem                          POST     /api/now/table/problem
Create catalog request                  POST     /sn_sc/servicecatalog/items/{sys_id}/order_now

Custom: Service health                  GET      /api/x_upi/v1/service-health
Custom: Alert receiver                  POST     /api/x_upi/v1/alert
Custom: ITSM metrics                    GET      /api/x_upi/v1/metrics
Custom: CI lookup                       GET      /api/x_upi/v1/ci/{name}
```

---

## Appendix C: Postman Collection Structure

```
If you prefer Postman over curl, organize your collection as follows:

Collection: NPCI UPI ServiceNow API
  |
  +-- Folder: Authentication
  |   +-- Get OAuth Token
  |   +-- Refresh Token
  |
  +-- Folder: Incident Management
  |   +-- GET List Incidents
  |   +-- GET Single Incident
  |   +-- POST Create Incident (UPI Latency)
  |   +-- POST Create Incident (UPI Error Rate)
  |   +-- PATCH Update State
  |   +-- PATCH Add Work Notes
  |   +-- PATCH Resolve Incident
  |
  +-- Folder: CMDB
  |   +-- GET List CIs
  |   +-- GET CI by Name
  |   +-- GET CI Relationships
  |
  +-- Folder: Aggregate / Stats
  |   +-- GET Incident Count by Priority
  |   +-- GET Incident Count by State
  |   +-- GET Average Resolution Time
  |
  +-- Folder: Custom UPI API
  |   +-- GET Service Health
  |   +-- POST Alert (Prometheus format)
  |   +-- GET ITSM Metrics
  |   +-- GET CI Lookup
  |
  +-- Folder: Change Management
  |   +-- POST Create Normal Change
  |   +-- PATCH Approve Change
  |   +-- GET Change Schedule
  |
  +-- Folder: Attachments
      +-- POST Upload File
      +-- GET Download File

Environment Variables (Postman):
  instance_url:   https://devXXXXXX.service-now.com
  username:       admin
  password:       ********
  oauth_token:    (set by pre-request script)
```

---

## Summary and Key Takeaways

```
What You Built in This Lab:

  REST API Mastery:
    - GET, POST, PUT, PATCH, DELETE on incident table
    - Aggregate API for statistics
    - Query parameters, encoded queries, pagination
    - Authentication methods (Basic, OAuth)

  Scripted REST APIs:
    - /service-health  -- CI health status from CMDB
    - /alert           -- AlertManager webhook receiver (native)
    - /metrics         -- ITSM KPIs for external dashboards
    - /ci/{name}       -- CI details with relationships

  Outbound Integrations:
    - Slack webhook notification on incident state change
    - Prometheus query from ServiceNow
    - UPIPrometheusHelper Script Include

  Integration Hub:
    - Custom "Send UPI Alert to Slack" action
    - Integration with Flow Designer flows

  Update Sets:
    - Created, captured changes, completed, exported
    - Naming conventions and batch parent sets
    - Import, preview, commit, back-out workflow
    - Source control integration concepts

  ATF Testing:
    - Incident auto-assignment test
    - SLA attachment test
    - P1 close validation test
    - Regression test suite

  Snow Bridge Walkthrough:
    - Complete code analysis of Python-to-ServiceNow integration
    - Production enhancement recommendations

This lab connects all 21 previous labs into a deployable, testable,
integrated ITSM platform for NPCI UPI.
```

---

## What Comes Next

```
With Lab 22 complete, you have built a full ITSM platform:

  Phase 1 (Labs 1-6):    Foundation -- PDI, navigation, tables, users
  Phase 2 (Labs 7-11):   Build -- Service portfolio, CMDB, catalog
  Phase 3 (Labs 12-15):  Operate -- Incident, Problem, Change management
  Phase 4 (Labs 16-21):  Customize -- Rules, scripts, flows, SLAs, dashboards
  Phase 5 (Lab 22):      Automate -- APIs, integration, deployment, testing

You are now equipped to:
  - Build end-to-end monitoring-to-incident automation
  - Create custom APIs for any external system integration
  - Package and deploy configurations across instances
  - Write automated tests for regression validation
  - Operate a production-grade ITSM platform for critical financial infrastructure
```

---

*Lab 22 of 22 | NPCI UPI Platform ITSM Series | Phase 5: Automate*
