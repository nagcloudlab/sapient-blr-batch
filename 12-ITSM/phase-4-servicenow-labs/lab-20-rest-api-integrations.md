# Lab 20: REST API & Integrations

**Level:** Expert | **Duration:** 90 minutes | **Prerequisites:** Lab 07-19 completed, basic API/JSON knowledge

---

## Objective

By the end of this lab, you will:
- Use the ServiceNow Table API to create, read, update, and delete records
- Test APIs using the REST API Explorer
- Create Scripted REST APIs for custom endpoints
- Use Import Sets to load data from external sources
- Make outbound REST calls from ServiceNow
- Understand authentication methods

---

## Part 1: Table API Basics

### Step 1.1: Understand the Table API

ServiceNow provides a built-in REST API for every table:

```
Base URL: https://devXXXXXX.service-now.com/api/now/table/{tableName}

Methods:
  GET    /api/now/table/incident              → List incidents
  GET    /api/now/table/incident/{sys_id}     → Get one incident
  POST   /api/now/table/incident              → Create incident
  PUT    /api/now/table/incident/{sys_id}     → Update incident
  PATCH  /api/now/table/incident/{sys_id}     → Partial update
  DELETE /api/now/table/incident/{sys_id}     → Delete incident
```

### Step 1.2: Open the REST API Explorer

1. Navigate to **System Web Services > REST > REST API Explorer** (or type `rest_api_explorer`)
2. The REST API Explorer is an interactive tool for testing APIs

### Step 1.3: GET -- List Incidents

1. In REST API Explorer:
   - Namespace: **now**
   - API Name: **Table API**
   - API Version: **latest**
   - Method: **GET**
   - Table name: **incident**

2. Add query parameters:
   | Parameter | Value |
   |---|---|
   | sysparm_query | priority=1^state!=7 |
   | sysparm_limit | 5 |
   | sysparm_fields | number,short_description,priority,state,assigned_to |
   | sysparm_display_value | true |

3. Click **Send**
4. Observe the response:
   ```json
   {
     "result": [
       {
         "number": "INC0010001",
         "short_description": "VPN service down",
         "priority": "1 - Critical",
         "state": "In Progress",
         "assigned_to": "Beth Anglin"
       },
       ...
     ]
   }
   ```

5. Note the generated URL:
   ```
   GET https://devXXXXXX.service-now.com/api/now/table/incident
       ?sysparm_query=priority=1^state!=7
       &sysparm_limit=5
       &sysparm_fields=number,short_description,priority,state,assigned_to
       &sysparm_display_value=true
   ```

### Step 1.4: GET -- Single Record

1. Method: **GET**
2. URL: `/api/now/table/incident/{sys_id}`
3. Replace `{sys_id}` with an actual incident sys_id
4. Click **Send**
5. Response shows all fields for that one record

### Step 1.5: POST -- Create an Incident

1. Method: **POST**
2. Table: **incident**
3. Request body (JSON):
   ```json
   {
     "caller_id": "abel.tuter",
     "short_description": "Created via REST API",
     "description": "This incident was created using the Table API",
     "category": "software",
     "subcategory": "email",
     "impact": "2",
     "urgency": "2",
     "assignment_group": "Service Desk"
   }
   ```
4. Click **Send**
5. Response: 201 Created with the new record details including `sys_id` and `number`

### Step 1.6: PUT/PATCH -- Update an Incident

1. Method: **PATCH** (partial update)
2. URL: `/api/now/table/incident/{sys_id}` (use the sys_id from step 1.5)
3. Request body:
   ```json
   {
     "state": "2",
     "work_notes": "Updated via REST API - assigned and in progress",
     "assigned_to": "beth.anglin"
   }
   ```
4. Click **Send**
5. Response: 200 OK with updated record

### Step 1.7: DELETE -- Delete a Record

1. Method: **DELETE**
2. URL: `/api/now/table/incident/{sys_id}`
3. Click **Send**
4. Response: 204 No Content (record deleted)

**Warning:** Use DELETE with extreme caution. In production, prefer deactivating/closing records.

---

## Part 2: Common API Query Parameters

| Parameter | Description | Example |
|---|---|---|
| `sysparm_query` | Encoded query filter | `priority=1^state=2` |
| `sysparm_limit` | Max records returned | `10` |
| `sysparm_offset` | Pagination offset | `20` (skip first 20) |
| `sysparm_fields` | Comma-separated fields | `number,state,priority` |
| `sysparm_display_value` | Return display values | `true`, `false`, `all` |
| `sysparm_exclude_reference_link` | Exclude ref links | `true` |
| `sysparm_suppress_pagination_header` | Remove pagination header | `true` |
| `sysparm_no_count` | Skip counting total | `true` (faster) |
| `orderby` | Sort ascending | `priority` |
| `orderbydesc` | Sort descending | `opened_at` |

---

## Part 3: Test with External Tools

### Step 3.1: Using curl (Command Line)

```bash
# GET incidents
curl -s \
  -u "admin:YOUR_PASSWORD" \
  -H "Accept: application/json" \
  "https://devXXXXXX.service-now.com/api/now/table/incident?sysparm_limit=3&sysparm_fields=number,short_description"

# POST create incident
curl -s \
  -u "admin:YOUR_PASSWORD" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -X POST \
  -d '{"short_description":"Created via curl","caller_id":"abel.tuter","impact":"3","urgency":"3"}' \
  "https://devXXXXXX.service-now.com/api/now/table/incident"

# PATCH update incident
curl -s \
  -u "admin:YOUR_PASSWORD" \
  -H "Content-Type: application/json" \
  -X PATCH \
  -d '{"state":"2","work_notes":"Updated via curl"}' \
  "https://devXXXXXX.service-now.com/api/now/table/incident/SYS_ID_HERE"
```

### Step 3.2: Using Postman (GUI Tool)

1. Download and install Postman (free)
2. Create a new request:
   - Method: GET
   - URL: `https://devXXXXXX.service-now.com/api/now/table/incident`
   - Auth: Basic Auth (username: admin, password: your_password)
   - Headers: Accept: application/json
   - Params: sysparm_limit=5
3. Click **Send** and view the JSON response

### Step 3.3: Using Python

```python
import requests
import json

instance = "https://devXXXXXX.service-now.com"
user = "admin"
password = "YOUR_PASSWORD"

# GET incidents
url = f"{instance}/api/now/table/incident"
params = {
    "sysparm_query": "priority=1",
    "sysparm_limit": 5,
    "sysparm_fields": "number,short_description,priority,state"
}
response = requests.get(url, auth=(user, password),
                       headers={"Accept": "application/json"},
                       params=params)

incidents = response.json()["result"]
for inc in incidents:
    print(f"{inc['number']}: {inc['short_description']}")

# POST create incident
create_url = f"{instance}/api/now/table/incident"
payload = {
    "short_description": "Created via Python",
    "caller_id": "abel.tuter",
    "impact": "2",
    "urgency": "2"
}
response = requests.post(create_url, auth=(user, password),
                        headers={"Content-Type": "application/json",
                                 "Accept": "application/json"},
                        data=json.dumps(payload))
print(f"Created: {response.json()['result']['number']}")
```

---

## Part 4: Scripted REST APIs

### Step 4.1: What Are Scripted REST APIs?

Custom REST endpoints with your own logic -- beyond the basic Table API.

### Step 4.2: Create a Scripted REST API

1. Navigate to **System Web Services > Scripted REST APIs** (or type `sys_ws_definition.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | IT Operations API |
   | API ID | it_operations |
   | API namespace | custom |
   | Active | Checked |

4. Click **Submit**

### Step 4.3: Add API Resources (Endpoints)

1. Open your "IT Operations API"
2. In the **Resources** related list, click **New**
3. Create:

   | Field | Value |
   |---|---|
   | Name | Get Incident Summary |
   | HTTP method | GET |
   | Relative path | /incident-summary |

4. **Script**:
   ```javascript
   (function process(/*RESTAPIRequest*/ request, /*RESTAPIResponse*/ response) {

       var result = {};

       // Count open incidents by priority
       var priorities = [1, 2, 3, 4, 5];
       result.by_priority = {};

       for (var i = 0; i < priorities.length; i++) {
           var ga = new GlideAggregate('incident');
           ga.addQuery('priority', priorities[i]);
           ga.addQuery('state', 'NOT IN', '6,7,8');
           ga.addAggregate('COUNT');
           ga.query();
           if (ga.next()) {
               result.by_priority['P' + priorities[i]] =
                   parseInt(ga.getAggregate('COUNT'));
           }
       }

       // Total open
       var total = new GlideAggregate('incident');
       total.addQuery('state', 'NOT IN', '6,7,8');
       total.addAggregate('COUNT');
       total.query();
       result.total_open = total.next() ?
           parseInt(total.getAggregate('COUNT')) : 0;

       // P1 incidents detail
       result.p1_incidents = [];
       var p1 = new GlideRecord('incident');
       p1.addQuery('priority', 1);
       p1.addQuery('state', 'NOT IN', '6,7,8');
       p1.query();
       while (p1.next()) {
           result.p1_incidents.push({
               number: p1.getValue('number'),
               short_description: p1.getValue('short_description'),
               state: p1.state.getDisplayValue(),
               assigned_to: p1.assigned_to.getDisplayValue()
           });
       }

       response.setBody(result);

   })(request, response);
   ```

5. Click **Submit**

### Step 4.4: Test Your Custom API

Call your custom endpoint:
```
GET https://devXXXXXX.service-now.com/api/custom/it_operations/incident-summary
```

Response:
```json
{
  "by_priority": {
    "P1": 3,
    "P2": 12,
    "P3": 45,
    "P4": 28,
    "P5": 15
  },
  "total_open": 103,
  "p1_incidents": [
    {
      "number": "INC0010001",
      "short_description": "VPN service down",
      "state": "In Progress",
      "assigned_to": "Beth Anglin"
    }
  ]
}
```

### Step 4.5: POST Endpoint -- Create Incident with Validation

Add another resource:

| Field | Value |
|---|---|
| Name | Create Validated Incident |
| HTTP method | POST |
| Relative path | /create-incident |

Script:
```javascript
(function process(request, response) {

    var body = request.body.data;

    // Validate required fields
    var required = ['short_description', 'caller_id', 'impact', 'urgency'];
    var missing = [];
    for (var i = 0; i < required.length; i++) {
        if (!body[required[i]]) {
            missing.push(required[i]);
        }
    }

    if (missing.length > 0) {
        response.setStatus(400);
        response.setBody({
            error: 'Missing required fields: ' + missing.join(', ')
        });
        return;
    }

    // Create the incident
    var gr = new GlideRecord('incident');
    gr.initialize();
    gr.short_description = body.short_description;
    gr.caller_id.setDisplayValue(body.caller_id);
    gr.impact = body.impact;
    gr.urgency = body.urgency;
    gr.description = body.description || '';
    gr.category = body.category || '';
    var sysId = gr.insert();

    response.setStatus(201);
    response.setBody({
        success: true,
        sys_id: sysId,
        number: gr.getValue('number')
    });

})(request, response);
```

---

## Part 5: Import Sets

### Step 5.1: What Are Import Sets?

Import Sets let you bulk-import data from external sources (CSV, Excel, JDBC, etc.) into ServiceNow tables.

```
External Data (CSV) → Import Set Table (staging) → Transform Map → Target Table
```

### Step 5.2: Import Users from CSV

1. Create a CSV file (`users.csv`):
   ```csv
   first_name,last_name,email,department,title
   Rahul,Patel,rahul.patel@example.com,Engineering,Senior Engineer
   Sneha,Reddy,sneha.reddy@example.com,Engineering,DevOps Lead
   Karthik,Iyer,karthik.iyer@example.com,Operations,SRE Manager
   Anita,Das,anita.das@example.com,Security,Security Analyst
   ```

2. Navigate to **System Import Sets > Load Data** (or type `sys_import_set_row`)
3. Select:
   - Table: **Create new table** (or use an existing import set table)
   - Source: **File** → upload your CSV
4. Click **Load**
5. ServiceNow creates an **Import Set Table** with your data

### Step 5.3: Create a Transform Map

1. After loading, click **Create Transform Map**
2. Map source columns to target table fields:

   | Source Column | Target Table | Target Field |
   |---|---|---|
   | first_name | sys_user | First name |
   | last_name | sys_user | Last name |
   | email | sys_user | Email |
   | department | sys_user | Department |
   | title | sys_user | Title |

3. Set **Coalesce** on the `email` field (prevents duplicates -- if email already exists, update instead of insert)
4. Click **Save**

### Step 5.4: Run the Transform

1. Click **Transform**
2. ServiceNow processes each row:
   - Matches against existing records (coalesce)
   - Inserts new records
   - Updates existing records
3. Review the results: how many inserted, updated, errors

### Step 5.5: Scheduled Import

You can schedule imports to run automatically:
1. Navigate to **System Import Sets > Scheduled Imports**
2. Configure a data source (JDBC, REST, LDAP, etc.)
3. Set the schedule (daily, hourly, etc.)
4. The import runs automatically and keeps ServiceNow in sync

---

## Part 6: Outbound REST (Calling External APIs)

### Step 6.1: Create a REST Message

1. Navigate to **System Web Services > Outbound > REST Message** (or type `sys_rest_message.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | External Monitoring API |
   | Endpoint | `https://api.example.com/v1` (use a test API) |
   | Authentication type | Basic |

4. Click **Submit**

### Step 6.2: Add HTTP Methods

1. Open your REST Message
2. In the **HTTP Methods** related list, click **New**
3. Create a GET method:

   | Field | Value |
   |---|---|
   | Name | Get Server Status |
   | HTTP method | GET |
   | Endpoint | `https://api.example.com/v1/servers/${server_id}/status` |

4. Click **Submit**

### Step 6.3: Call from a Script

```javascript
// In a Business Rule or Script Include
try {
    var sm = new sn_ws.RESTMessageV2('External Monitoring API', 'Get Server Status');
    sm.setStringParameterNoEscape('server_id', 'web-server-01');
    var response = sm.execute();

    var httpStatus = response.getStatusCode();
    var body = response.getBody();

    if (httpStatus == 200) {
        var data = JSON.parse(body);
        gs.info('Server status: ' + data.status);
    } else {
        gs.error('API call failed with status: ' + httpStatus);
    }
} catch (ex) {
    gs.error('REST call exception: ' + ex.getMessage());
}
```

---

## Part 7: Authentication

| Method | Use Case | How |
|---|---|---|
| **Basic Auth** | Simple, testing | Username + password in header |
| **OAuth 2.0** | Production integrations | Token-based, more secure |
| **API Key** | External service access | Key in header or query param |
| **Mutual TLS** | High-security | Certificate-based |

---

## Part 8: Practice Exercises

### Exercise 1: Build a Monitoring Integration

1. Create a Scripted REST API endpoint: `/api/custom/monitoring/create-alert`
2. It receives POST requests with: `server`, `severity`, `message`
3. Based on severity, it creates an incident with appropriate priority
4. Return the incident number in the response

### Exercise 2: Bulk Import

1. Create a CSV of 20 configuration items
2. Import them via Import Set into the cmdb_ci table
3. Verify all CIs were created correctly
4. Create a scheduled import that could run daily

### Exercise 3: External Dashboard Data

1. Create a Scripted REST API: `/api/custom/dashboard/metrics`
2. Return JSON with:
   - Open incidents (by priority)
   - Pending changes
   - SLA compliance percentage
   - Top 5 CIs by incident count
3. Test with curl or Postman

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Used Table API (CRUD) | Programmatic access to ServiceNow data |
| Built Scripted REST APIs | Custom endpoints for integration |
| Imported data via Import Sets | Bulk data migration and synchronization |
| Made outbound REST calls | Integrate with external systems |
| Tested with curl/Postman/Python | Real-world API interaction patterns |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Table API** | Built-in REST API for CRUD on any table |
| **Scripted REST API** | Custom REST endpoints with server-side logic |
| **Import Set** | Staging table for bulk data imports |
| **Transform Map** | Rules mapping import data to target table fields |
| **Coalesce** | Field used to match existing records (prevent duplicates) |
| **REST Message** | Configuration for outbound REST API calls |
| **OAuth** | Token-based authentication for secure API access |

---

## What's Next

In **Lab 21** (final lab), you'll learn **Update Sets, ATF & Deployment** -- capturing configurations for migration between instances and automated testing.
