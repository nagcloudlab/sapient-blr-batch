# Lab 17: Reporting & Performance Analytics

**Level:** Advanced | **Duration:** 90 min | **Prerequisites:** Labs 12-16 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand ITIL 4 Measurement & Reporting practice and how it drives continual improvement
- Master ServiceNow's reporting engine: report types, sources, filters, aggregation, and drill-down
- Build 10+ ITSM reports covering Incidents, Problems, Changes, SLAs, CMDB, and Knowledge
- Configure Performance Analytics (PA) indicators, breakdowns, targets, and thresholds
- Construct an Executive Dashboard: "UPI Service Management Dashboard"
- Schedule automated report delivery to stakeholders
- Manage report sharing, access control, and export options

---

## Scenario: Making ITSM Visible at NPCI

```
NPCI's UPI platform processes 14 billion+ transactions monthly. Over the previous
labs, you have built:

  - CMDB with 12+ Configuration Items (UPI-PSP-Server-01, UPI-TXN-SVC, etc.)
  - Business and Technical Services mapped to CIs
  - SLAs (P1 Resolution: 4hrs, P2: 8hrs, P3: 24hrs, P4: 72hrs)
  - Knowledge Base articles for known errors
  - Service Catalog items for standard requests
  - Incidents across priorities (P1 through P4)
  - Problems with root cause analysis
  - Changes (Normal, Standard, Emergency)
  - Releases for deployment tracking

Sanjay (IT Service Manager) has been asked by the NPCI Board to present:
  1. Are we meeting our SLAs?
  2. What is our Mean Time to Restore for critical incidents?
  3. Are changes succeeding or failing?
  4. Which CIs cause the most incidents?
  5. Is our service improving over time?

You must build the reporting infrastructure to answer these questions —
and automate delivery so leadership sees it every Monday.
```

---

## Part 1: ITIL 4 Measurement & Reporting Theory

### 1.1 The Measurement & Reporting Practice

```
ITIL 4 Practice: Measurement & Reporting

Purpose: Support good decision-making and continual improvement by
         reducing levels of uncertainty through collection of relevant
         data and assessment of that data in an appropriate context.

Key Activities:
  1. Define what to measure (aligned with business objectives)
  2. Determine how to collect data
  3. Process and analyze data
  4. Present information in appropriate formats
  5. Enable decisions and actions based on findings
```

### 1.2 CSFs and KPIs

```
Critical Success Factor (CSF):
  A high-level goal that must be achieved for the service to succeed.

  Example CSF: "UPI transactions must be processed reliably 24x7"

Key Performance Indicator (KPI):
  A measurable value that demonstrates how effectively a CSF is being achieved.

  Example KPIs for above CSF:
    - Platform availability: >= 99.95%
    - P1 incident resolution: <= 4 hours
    - SLA compliance: >= 95%

Relationship:
  Business Objective --> CSF --> KPI --> Metric --> Data Point

  "Reliable UPI" --> "Always Available" --> "Availability %" --> "Uptime/Total Time" --> "Minutes"
```

### 1.3 ITSM Metrics Hierarchy

```
Level 1: STRATEGIC METRICS (Board / CxO)
  +---------------------------------------------------------+
  | Customer Satisfaction Score (CSAT)                       |
  | Overall Service Availability                             |
  | Total Cost of IT Service Delivery                        |
  | IT's Contribution to Business Revenue                    |
  +---------------------------------------------------------+
         |
Level 2: TACTICAL METRICS (IT Service Manager / Process Owner)
  +---------------------------------------------------------+
  | SLA Compliance %                                         |
  | Change Success Rate                                      |
  | Problem Resolution Rate                                  |
  | Mean Time to Restore (MTTR)                              |
  | Mean Time Between Failures (MTBF)                        |
  | First Contact Resolution Rate                            |
  | Cost per Ticket                                          |
  +---------------------------------------------------------+
         |
Level 3: OPERATIONAL METRICS (Team Lead / Analyst)
  +---------------------------------------------------------+
  | Open Incident Count by Priority                          |
  | Incident Backlog Age                                     |
  | Reassignment Count                                       |
  | Average Handle Time                                      |
  | Incident Reopen Rate                                     |
  | Change Backlog                                           |
  | Knowledge Article Usage                                  |
  +---------------------------------------------------------+
```

### 1.4 Key ITSM Metrics — Definitions

```
+-------------------------------+--------------------------------------------------+------------------+
| Metric                        | Formula                                          | NPCI Target      |
+-------------------------------+--------------------------------------------------+------------------+
| MTTR (Mean Time to Restore)   | Sum(Resolved - Opened) / Count of Incidents      | P1: < 4 hrs      |
|                               |                                                  | P2: < 8 hrs      |
+-------------------------------+--------------------------------------------------+------------------+
| MTBF (Mean Time Between       | Total Uptime / Number of Failures                | > 720 hrs        |
| Failures)                     |                                                  | (30 days)        |
+-------------------------------+--------------------------------------------------+------------------+
| Change Success Rate           | (Successful Changes / Total Changes) * 100       | >= 95%           |
+-------------------------------+--------------------------------------------------+------------------+
| SLA Compliance %              | (SLAs Met / Total SLAs) * 100                    | >= 95%           |
+-------------------------------+--------------------------------------------------+------------------+
| First Contact Resolution Rate | (Resolved at L1 / Total L1 Incidents) * 100      | >= 70%           |
+-------------------------------+--------------------------------------------------+------------------+
| Incident Reopen Rate          | (Reopened Incidents / Total Resolved) * 100       | <= 5%            |
+-------------------------------+--------------------------------------------------+------------------+
| Cost per Ticket               | Total Support Cost / Number of Tickets            | Track trend      |
+-------------------------------+--------------------------------------------------+------------------+
| Backlog Aging                 | Count of tickets > X days old                     | 0 tickets > SLA  |
+-------------------------------+--------------------------------------------------+------------------+
```

### 1.5 Balanced Scorecard for IT Services

```
The Balanced Scorecard translates strategic objectives into four perspectives:

  +-----------------------------+     +-----------------------------+
  |    FINANCIAL PERSPECTIVE    |     |    CUSTOMER PERSPECTIVE     |
  |                             |     |                             |
  | - Cost per transaction      |     | - CSAT score                |
  | - IT spend as % of revenue  |     | - SLA compliance            |
  | - Cost per ticket           |     | - Service availability      |
  | - ROI of automation         |     | - First contact resolution  |
  +-----------------------------+     +-----------------------------+

  +-----------------------------+     +-----------------------------+
  | INTERNAL PROCESS PERSPECTIVE|     | LEARNING & GROWTH           |
  |                             |     |                             |
  | - Change success rate       |     | - Staff certifications      |
  | - MTTR / MTBF               |     | - Knowledge articles created|
  | - Incident reopen rate      |     | - Automation ratio          |
  | - Problem closure rate      |     | - Training hours per agent  |
  +-----------------------------+     +-----------------------------+

At NPCI, Sanjay's scorecard might look like:
  Financial:  Cost per UPI transaction incident = INR 2,500 (target: < 3,000)
  Customer:   SLA compliance = 96% (target: >= 95%)
  Process:    Change success rate = 92% (target: >= 95%) -- NEEDS IMPROVEMENT
  Learning:   3 new KB articles this month (target: >= 5) -- NEEDS IMPROVEMENT
```

---

## Part 2: ServiceNow Reporting Engine

### 2.1 Report Types Overview

```
ServiceNow provides 15+ report types. The key ones for ITSM:

+------------------+----------------------------------------------+------------------------------+
| Report Type      | Best For                                     | Example                      |
+------------------+----------------------------------------------+------------------------------+
| List             | Detailed record listing                      | All open P1 incidents        |
| Bar (Vertical)   | Comparing categories                         | Incidents by priority        |
| Bar (Horizontal) | Comparing categories (long labels)           | Incidents by assignment group |
| Pie              | Proportional breakdown                       | Problem by category          |
| Donut            | Proportional breakdown (with center value)   | Incidents by priority        |
| Line             | Trends over time                             | Incident trend monthly       |
| Area             | Volume trends over time                      | Ticket volume by month       |
| Column           | Comparing values (similar to bar)            | Changes by type              |
| Heatmap          | Two-dimensional frequency analysis           | Incidents by day vs hour     |
| Bubble           | Three-variable comparison                    | Priority vs age vs count     |
| Pivot Table      | Cross-tabulation of two dimensions           | SLA breach by priority       |
| Single Score     | One KPI number                               | Total open incidents         |
| Speedometer      | KPI against target                           | SLA compliance gauge         |
| Dial             | Progress toward a goal                       | Change success rate          |
| Trend            | Metric change over time with direction       | Weekly incident count        |
+------------------+----------------------------------------------+------------------------------+
```

### 2.2 Report Building Blocks

```
Every ServiceNow report has these components:

  1. SOURCE (Table)
     - Which table to report on
     - Examples: incident, problem, change_request, task_sla, sc_req_item

  2. TYPE
     - Chart visualization type (bar, pie, line, etc.)

  3. GROUP BY
     - The field to group/categorize records
     - Example: Group by "Priority" to see counts per priority

  4. STACK BY (Optional)
     - A second dimension within each group
     - Example: Group by Priority, Stack by State

  5. AGGREGATION
     - How to calculate: Count, Sum, Average, Min, Max
     - Example: Count of incidents, Average resolution time

  6. FILTER / CONDITIONS
     - Which records to include
     - Example: Active = true, Created in last 90 days

  7. OTHER
     - Sort order, top N, trend settings, colors, drill-down
```

### 2.3 Navigating to Reports

```
Step 1: In the Filter Navigator, type "Reports"
Step 2: Click Reports > Create New

  OR

Step 1: Navigate to any list view (e.g., Incident > All)
Step 2: Right-click any column header
Step 3: Select "Bar Chart" or "Pie Chart" -- quick reports from list views
```

### 2.4 Report Drill-Down

```
Drill-down lets users click a chart segment to see underlying records.

Example: Click the "P1 - Critical" bar in "Incidents by Priority"
         --> Opens a list of all P1 incidents

This is enabled by default in most report types. To configure:
  Report > Configure > Style tab > Enable "Click through"
```

---

## Part 3: Create ITSM Reports (Step-by-Step)

We will build 10 reports. Each report includes exact field values.

### Report 1: Incident Trend Report (Line Chart)

**Purpose:** Show how incident volume changes over time to identify trends.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI Incident Trend - Monthly
  Source type:       Table
  Table:            Incident [incident]
  Type:             Line

GROUP BY TAB:
  Group by:         Created
  Group by interval: Monthly

FILTER TAB (Conditions):
  Condition 1:      Created | on | Last 90 days

  (This captures all incidents from the past 3 months)

STYLE TAB:
  Title:            UPI Incident Trend - Last 90 Days
  Show data labels: Yes
  Chart color:      Blue (#0056B3)

Click "Save" then "Run"
```

**What to verify:**
- Line chart shows monthly created incident counts
- Each data point is labeled with the count
- Clicking a point drills down to that month's incidents

---

### Report 2: Incidents by Priority (Donut Chart)

**Purpose:** Visualize the distribution of incidents across priority levels.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI Incidents by Priority
  Source type:       Table
  Table:            Incident [incident]
  Type:             Donut

GROUP BY TAB:
  Group by:         Priority

FILTER TAB:
  Condition 1:      Active | is | true

  OR for historical view:
  Condition 1:      Created | on | Last 90 days

STYLE TAB:
  Title:            Active Incidents by Priority
  Show legend:      Yes (right side)
  Show percentages: Yes
  Custom colors:
    1 - Critical:   #FF0000 (Red)
    2 - High:       #FF8C00 (Orange)
    3 - Moderate:   #FFD700 (Gold)
    4 - Low:        #008000 (Green)

Click "Save" then "Run"
```

**What to verify:**
- Donut center shows total count
- Each segment shows percentage
- Colors match priority severity (red for critical, green for low)

---

### Report 3: Incidents by Assignment Group (Horizontal Bar)

**Purpose:** Show workload distribution across support teams.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI Incidents by Assignment Group
  Source type:       Table
  Table:            Incident [incident]
  Type:             Horizontal bar

GROUP BY TAB:
  Group by:         Assignment group

FILTER TAB:
  Condition 1:      State | is not | Closed
  Condition 2:      State | is not | Canceled

STYLE TAB:
  Title:            Open Incidents by Team
  Sort by:          Count (descending)
  Show data labels: Yes
  Chart color:      Teal (#009688)

Click "Save" then "Run"
```

**Expected Results:**

```
If your data from previous labs is present:

  UPI-Platform-Engineering  ████████████  (highest - they handle P1/P2)
  UPI-NOC                   ████████      (monitoring team)
  Service Desk              ████          (L1 support)
```

---

### Report 4: SLA Compliance (Pivot Table)

**Purpose:** Cross-tabulate SLA breaches by priority to identify compliance gaps.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI SLA Compliance by Priority
  Source type:       Table
  Table:            Task SLA [task_sla]
  Type:             Pivot table

GROUP BY TAB:
  Group by (Rows):    Task.Priority
  Stack by (Columns): Has breached

AGGREGATION:
  Aggregate:        Count

FILTER TAB:
  Condition 1:      Stage | is | Complete

  (Only count completed SLAs for accurate metrics)

STYLE TAB:
  Title:            SLA Compliance Matrix

Click "Save" then "Run"
```

**Expected Output:**

```
+----------+---------------+------------------+-------+
| Priority | Not Breached  | Breached (true)  | Total |
+----------+---------------+------------------+-------+
| 1 - Crit |      3        |       1          |   4   |
| 2 - High |      5        |       2          |   7   |
| 3 - Mod  |      8        |       1          |   9   |
| 4 - Low  |     10        |       0          |  10   |
+----------+---------------+------------------+-------+
| Total    |     26        |       4          |  30   |
+----------+---------------+------------------+-------+

SLA Compliance = 26/30 = 86.7%  --> BELOW 95% TARGET (needs attention!)
```

---

### Report 5: MTTR by Priority (Bar Chart)

**Purpose:** Show average resolution time per priority level.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI MTTR by Priority
  Source type:       Table
  Table:            Incident [incident]
  Type:             Bar

GROUP BY TAB:
  Group by:         Priority

AGGREGATION:
  Aggregate:        Average
  Aggregate field:  Business resolve time

  NOTE: "Business resolve time" is calculated as (Resolved - Opened).
  If this field is not visible, use "Calendar duration" (business_duration).

  Alternative: Use duration field "Resolve time" if available in your PDI.

FILTER TAB:
  Condition 1:      State | is | Resolved OR Closed
  Condition 2:      Resolved | is not empty

STYLE TAB:
  Title:            Mean Time to Restore by Priority
  Display values as: Duration (hours)
  Show data labels:  Yes
  Custom colors:
    1 - Critical:   #FF0000
    2 - High:       #FF8C00
    3 - Moderate:   #2196F3
    4 - Low:        #4CAF50

Click "Save" then "Run"
```

**Interpreting Results:**

```
Target vs Actual:

  Priority 1:  Target = 4 hrs  |  Actual = 3.5 hrs   PASS
  Priority 2:  Target = 8 hrs  |  Actual = 9.2 hrs   FAIL  <-- needs investigation
  Priority 3:  Target = 24 hrs |  Actual = 18.6 hrs   PASS
  Priority 4:  Target = 72 hrs |  Actual = 48.0 hrs   PASS
```

---

### Report 6: Change Success Rate (Single Score)

**Purpose:** Display the percentage of successful changes as a single KPI.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI Change Success Rate
  Source type:       Table
  Table:            Change Request [change_request]
  Type:             Single Score (or Dial / Speedometer)

AGGREGATION:
  Aggregate:        Count

  NOTE: Single Score reports in ServiceNow show a count or calculated value.
  For a percentage, we need two reports or use Performance Analytics.

  Approach A - Two Single Score reports:
    Report 6a: Count where Close code = "Successful"
    Report 6b: Count of all completed changes
    Display: 6a / 6b * 100 on dashboard

  Approach B - Use a Speedometer:
    This is better handled via Performance Analytics (Part 4).
    For now, create a basic count:

FILTER TAB (for Successful count):
  Condition 1:      State | is | Closed
  Condition 2:      Close code | is | Successful

STYLE TAB:
  Title:            Successful Changes (Last 90 Days)
  Display:          Large number format
  Color:            Green (#4CAF50)

Click "Save" then "Run"
```

**Create the companion report for Total Changes:**

```
Name:             UPI Total Completed Changes
Table:            Change Request [change_request]
Type:             Single Score
Filter:           State = Closed
```

**Manual Calculation:**

```
Change Success Rate = (Successful Changes / Total Completed Changes) * 100

Example: 19 successful / 20 total = 95%

This will be automated in Part 4 using Performance Analytics.
```

---

### Report 7: Problem Root Cause Analysis (Pie Chart)

**Purpose:** Identify which categories generate the most problems.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI Problem Root Cause by Category
  Source type:       Table
  Table:            Problem [problem]
  Type:             Pie

GROUP BY TAB:
  Group by:         Category

FILTER TAB:
  (No filter - include all problems for full picture)

  Optional: Condition 1: State | is | Closed (Root Cause Identified)

STYLE TAB:
  Title:            Problems by Category
  Show legend:      Yes
  Show percentages: Yes

Click "Save" then "Run"
```

**Expected distribution from previous labs:**

```
  Software        45%   (UPI Transaction Service bugs, API errors)
  Network         25%   (Connectivity issues between PSP servers)
  Hardware        15%   (Server hardware failures)
  Database        10%   (MongoDB/PostgreSQL issues)
  Other            5%   (Process/People issues)
```

---

### Report 8: Top 10 Impacted CIs (Bar Chart)

**Purpose:** Identify the Configuration Items that cause the most incidents.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI Top 10 Impacted CIs
  Source type:       Table
  Table:            Incident [incident]
  Type:             Bar

GROUP BY TAB:
  Group by:         Configuration item

AGGREGATION:
  Aggregate:        Count

FILTER TAB:
  Condition 1:      Configuration item | is not empty
  Condition 2:      Created | on | Last 180 days

STYLE TAB:
  Title:            Top 10 Configuration Items by Incident Count
  Sort by:          Count (descending)
  Display:          Top 10 only (set in "Other" tab or chart settings)
  Show data labels: Yes
  Chart color:      Red (#E53935)

Click "Save" then "Run"
```

**Expected Results from CMDB (Lab 12):**

```
  UPI-TXN-SVC             ████████████████  16
  UPI-PSP-Server-01       ████████████      12
  UPI-API-Gateway          ████████          8
  UPI-Settlement-Engine    ██████            6
  UPI-PSP-Server-02        █████            5
  UPI-MongoDB-Primary      ████             4
  UPI-Load-Balancer         ███             3
  UPI-Kafka-Cluster          ██             2
  UPI-DNS-Primary            ██             2
  UPI-Monitoring-Server       █             1
```

**Insight:** UPI-TXN-SVC has the highest incident count. This CI should be
prioritized for Problem Management investigation and proactive maintenance.

---

### Report 9: Knowledge Article Usage (Line Chart)

**Purpose:** Track how often Knowledge Base articles are being viewed over time.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI Knowledge Article Usage Trend
  Source type:       Table
  Table:            KB Use [kb_use]
  Type:             Line

  NOTE: The kb_use table tracks every view/use of a KB article.
  If this table is empty in your PDI, you can use:
    Table: Knowledge [kb_knowledge]
    Aggregate: Sum of "View count" (sys_view_count)

GROUP BY TAB:
  Group by:         Viewed at (or Created)
  Group by interval: Weekly

FILTER TAB:
  Condition 1:      Created | on | Last 90 days

STYLE TAB:
  Title:            Knowledge Base Usage - Weekly Trend
  Show data labels: Yes
  Chart color:      Purple (#7B1FA2)

Click "Save" then "Run"
```

**Alternative if kb_use table is empty:**

```
Create a List report instead:

  Name:             UPI Knowledge Articles by Usage
  Table:            Knowledge [kb_knowledge]
  Type:             Bar
  Group by:         Short description
  Aggregate:        Sum of Sys view count
  Sort:             Descending
  Display:          Top 10
```

---

### Report 10: Service Request Fulfillment Time (Bar Chart)

**Purpose:** Measure average fulfillment time for catalog requests by category.

```
Navigation: Reports > Create New

REPORT TAB:
  Name:             UPI Request Fulfillment Time by Category
  Source type:       Table
  Table:            Requested Item [sc_req_item]
  Type:             Bar

GROUP BY TAB:
  Group by:         Category (or Catalog item)

AGGREGATION:
  Aggregate:        Average
  Aggregate field:  Calendar duration (or Business duration)

FILTER TAB:
  Condition 1:      Stage | is | Complete (or State = Closed Complete)

STYLE TAB:
  Title:            Average Fulfillment Time by Request Category
  Display values as: Duration (hours or days)
  Show data labels:  Yes
  Sort by:           Value (descending)
  Chart color:       Orange (#FF9800)

Click "Save" then "Run"
```

**Interpreting Results:**

```
Category                     Avg Fulfillment Time    Target    Status
-----------------------------------------------------------------------
New VPA Onboarding           2.3 days                3 days    PASS
Access Provisioning          1.1 days                1 day     FAIL
Server Certificate Renewal   0.5 days                2 days    PASS
Firewall Rule Change         4.2 days                5 days    PASS
```

---

## Part 4: Performance Analytics (PA)

### 4.1 What is Performance Analytics?

```
Performance Analytics (PA) goes beyond basic reporting:

  Basic Reporting:
    - Point-in-time snapshots
    - "How many P1 incidents are open RIGHT NOW?"

  Performance Analytics:
    - Historical trend data collected over time
    - "How has our P1 count changed over the last 6 months?"
    - Forecasting: "At this rate, what will next month look like?"
    - Targets & thresholds with red/yellow/green indicators
    - Automated data collection (daily/weekly/monthly)

PA Components:
  +-- Indicator (What to measure) -----> "Open P1 Incidents"
  |     +-- Data Source (Where)  -----> Incident table, Priority=1, Active=true
  |     +-- Frequency (When)    -----> Daily at midnight
  |     +-- Direction (Better)  -----> Minimize (fewer is better)
  |
  +-- Breakdown (How to slice)  -----> By Priority, By Assignment Group
  |
  +-- Target (What to aim for)  -----> < 5 open P1 incidents
  |     +-- Thresholds          -----> Green: 0-2, Yellow: 3-5, Red: 6+
  |
  +-- Widget (How to display)   -----> Scorecard, Speedometer, Trendline
```

### 4.2 Enable PA Data Collection

```
Step 1: Navigate to Performance Analytics > Data Collector > Jobs

Step 2: Verify these collection jobs exist and are active:
  - Incident (pa_incidents)
  - Problem (pa_problems)
  - Change Request (pa_changes)
  - Task SLA

Step 3: If not active, click the job and set:
  Active: true
  Run: Daily

Step 4: To populate historical data, click "Execute Now" on each job
  This will create initial data snapshots

NOTE: In a PDI, PA may have limited historical data. The background
script in the Appendix creates sample data for demonstration.
```

### 4.3 Create PA Indicators

#### Indicator 1: Open P1 Incidents

```
Navigation: Performance Analytics > Indicators > Create New

INDICATOR TAB:
  Name:             Open P1 Incidents - UPI
  Description:      Count of active Priority 1 incidents for UPI platform

  Type:             Collect (snapshot at each collection point)
  Direction:        Minimize (lower is better)
  Unit:             Integer

SOURCE TAB:
  Table:            Incident [incident]
  Aggregate:        Count

  Conditions (Filter):
    Priority | is | 1 - Critical
    Active   | is | true

COLLECTION TAB:
  Frequency:        Daily

  (PA will take a daily snapshot of the count of open P1 incidents)

Click "Save"
```

```
After saving, click "Collect Data" (related link) to generate the first data point.

To see results:
  Performance Analytics > Indicators > Open P1 Incidents - UPI
  Click the "Analytics" related link or view in a PA Widget
```

#### Indicator 2: Average Resolution Time

```
Navigation: Performance Analytics > Indicators > Create New

INDICATOR TAB:
  Name:             Average Resolution Time - UPI
  Description:      Mean time to resolve incidents (all priorities)

  Type:             Collect
  Direction:        Minimize
  Unit:             Duration (hours)

SOURCE TAB:
  Table:            Incident [incident]
  Aggregate:        Average
  Field:            Business resolve time

  Conditions:
    State | is | Resolved
    Resolved | on | Last 7 days

COLLECTION TAB:
  Frequency:        Weekly (every Monday)

Click "Save" then "Collect Data"
```

#### Indicator 3: SLA Breach Rate

```
Navigation: Performance Analytics > Indicators > Create New

INDICATOR TAB:
  Name:             SLA Breach Rate - UPI
  Description:      Percentage of SLAs that have been breached

  Type:             Formula
  Direction:        Minimize
  Unit:             Percentage (%)

FORMULA:
  To create a percentage indicator, we need two base indicators:

  Base Indicator A: "Breached SLAs Count"
    Table:          Task SLA [task_sla]
    Aggregate:      Count
    Conditions:     Has breached = true, Stage = Complete
    Frequency:      Daily

  Base Indicator B: "Total Completed SLAs"
    Table:          Task SLA [task_sla]
    Aggregate:      Count
    Conditions:     Stage = Complete
    Frequency:      Daily

  Formula Indicator:
    Name:           SLA Breach Rate - UPI
    Formula:        (A / B) * 100
    Direction:      Minimize

Click "Save"
```

#### Indicator 4: Change Failure Rate

```
Navigation: Performance Analytics > Indicators > Create New

INDICATOR TAB:
  Name:             Change Failure Rate - UPI
  Description:      Percentage of changes that failed or were backed out

  Type:             Formula
  Direction:        Minimize
  Unit:             Percentage (%)

FORMULA:
  Base Indicator A: "Failed Changes Count"
    Table:          Change Request [change_request]
    Aggregate:      Count
    Conditions:     State = Closed, Close code IN (Unsuccessful, Incomplete)
    Frequency:      Weekly

  Base Indicator B: "Total Completed Changes"
    Table:          Change Request [change_request]
    Aggregate:      Count
    Conditions:     State = Closed
    Frequency:      Weekly

  Formula:          (A / B) * 100
  Direction:        Minimize

Click "Save"
```

### 4.4 PA Breakdowns

```
Breakdowns allow you to slice indicator data by different dimensions.

Navigation: Performance Analytics > Breakdowns > Create New

Breakdown 1: By Priority
  Name:             Breakdown by Priority
  Table:            Incident [incident]
  Field:            Priority

Breakdown 2: By Assignment Group
  Name:             Breakdown by Assignment Group
  Table:            Incident [incident]
  Field:            Assignment group

Breakdown 3: By Service
  Name:             Breakdown by Business Service
  Table:            Incident [incident]
  Field:            Business service

After creating breakdowns, associate them with indicators:
  1. Open indicator "Open P1 Incidents - UPI"
  2. Go to Related Lists > Breakdown Sources
  3. Click "New"
  4. Select the breakdown (e.g., "By Assignment Group")
  5. Save

Now the indicator can show:
  "Open P1 Incidents broken down by Assignment Group"

  UPI-Platform-Engineering:  3
  UPI-NOC:                   1
  Service Desk:              0
```

### 4.5 Targets and Thresholds

```
Navigation: Performance Analytics > Targets > Create New

Target 1: Open P1 Target
  Name:             P1 Incident Target
  Indicator:        Open P1 Incidents - UPI
  Target value:     5
  Direction:        Below (we want to be below 5)

  Thresholds:
    Green:          0 - 2   (Excellent)
    Yellow:         3 - 5   (Warning)
    Red:            6+      (Critical - escalate)

Target 2: SLA Breach Rate Target
  Name:             SLA Compliance Target
  Indicator:        SLA Breach Rate - UPI
  Target value:     5   (5% breach rate = 95% compliance)
  Direction:        Below

  Thresholds:
    Green:          0 - 3%   (Exceeding target)
    Yellow:         3 - 5%   (Meeting target)
    Red:            5%+      (Failing)

Target 3: Change Failure Rate Target
  Name:             Change Success Target
  Indicator:        Change Failure Rate - UPI
  Target value:     5   (5% failure = 95% success)
  Direction:        Below

  Thresholds:
    Green:          0 - 3%
    Yellow:         3 - 5%
    Red:            5%+
```

### 4.6 PA Widgets

```
PA Widgets display indicator data in dashboards. Types include:

  +-------------------+--------------------------------------------+
  | Widget Type       | Shows                                      |
  +-------------------+--------------------------------------------+
  | Scorecard         | Current value with trend arrow              |
  | Speedometer       | Gauge with green/yellow/red zones           |
  | Dial              | Circular gauge                              |
  | Time Series       | Line chart of indicator over time           |
  | Breakdown         | Bar chart by breakdown dimension            |
  | Column            | Comparison of indicator values              |
  +-------------------+--------------------------------------------+

To add PA widgets to a dashboard (covered in Part 5):
  1. Edit dashboard
  2. Add widget > Performance Analytics
  3. Select indicator
  4. Choose visualization type
  5. Configure time range and breakdown
```

### 4.7 Trend Analysis and Forecasting

```
Performance Analytics can project future values based on historical data:

  Navigation: Performance Analytics > Indicators > [Select Indicator]
  Click "Analytics" tab

  In the analytics view:
    1. Set time range: Last 6 months
    2. Enable "Trend line" (linear regression)
    3. Enable "Forecast" (projects 1-3 months ahead)

  Example forecast for "Open P1 Incidents":

  Month          Actual    Trend Line    Forecast
  -----------------------------------------------
  April 2024       8          7.8          --
  May 2024         6          7.2          --
  June 2024        7          6.6          --
  July 2024        5          6.0          --
  August 2024      4          5.4          --
  September 2024   --         4.8         4.8
  October 2024     --         4.2         4.2

  Interpretation: P1 incidents trending downward. If trend continues,
  we will be consistently below target (5) by October. Our Problem
  Management and Change processes are having a positive impact.
```

---

## Part 5: Build an Executive Dashboard

### 5.1 Dashboard Layout Design

```
Dashboard: "UPI Service Management Dashboard"

+-------------------------------------------------------------------+
| ROW 1: Key Performance Indicators                                  |
+---------------------+---------------------+-----------------------+
| P1 Open Incidents   | MTTR (Avg Hours)    | SLA Compliance %      |
| Single Score / Red  | Speedometer / Green | Speedometer / Yellow  |
|       "4"           |     "3.5 hrs"       |      "92%"            |
+---------------------+---------------------+-----------------------+
| ROW 2: Trends & Rates                                              |
+-----------------------------------+-------------------------------+
| Incident Trend - Monthly          | Change Success Rate           |
| Line Chart                        | Dial / Single Score           |
| (last 6 months)                   |     "95%"                     |
+-----------------------------------+-------------------------------+
| ROW 3: Operational Details                                         |
+-----------------------------------+-------------------------------+
| Top 10 Impacted CIs               | Problem Status                |
| Horizontal Bar                    | Donut Chart                   |
| (by incident count)               | (by state)                    |
+-----------------------------------+-------------------------------+
```

### 5.2 Create the Dashboard

```
Step 1: Navigate to Self-Service > Dashboards
        OR type "Dashboards" in Filter Navigator

Step 2: Click "New" (+ icon at top)

Step 3: Configure Dashboard Properties
  Name:          UPI Service Management Dashboard
  Category:      IT Service Management
  Owner:         System Administrator (you)

Step 4: Click "Save"

You now see an empty dashboard canvas.
```

### 5.3 Add Widgets — Row 1

```
--- Widget 1: P1 Open Incidents ---

Step 1: Click "Add Widget" (or the + icon on the dashboard)
Step 2: Select "Reports" from widget types
Step 3: Search for "UPI" and select your "Open P1 Incidents" report
        (or if using PA, select "Performance Analytics" widget type
         and choose the "Open P1 Incidents - UPI" indicator)
Step 4: Place in Row 1, Column 1
Step 5: Resize to 1/3 width

--- Widget 2: MTTR Gauge ---

Step 1: Click "Add Widget"
Step 2: Select "Reports"
Step 3: Select "UPI MTTR by Priority" report
Step 4: Place in Row 1, Column 2

For a speedometer:
  If using PA:
  Step 1: Add Widget > Performance Analytics
  Step 2: Select "Average Resolution Time - UPI" indicator
  Step 3: Visualization: Speedometer
  Step 4: Configure thresholds: Green < 4hrs, Yellow 4-6hrs, Red > 6hrs

--- Widget 3: SLA Compliance Gauge ---

Step 1: Click "Add Widget"
Step 2: If PA indicator exists, select PA widget with "SLA Breach Rate - UPI"
Step 3: Visualization: Speedometer (inverted - show compliance not breach)
Step 4: Configure: Green >= 95%, Yellow 90-95%, Red < 90%
Step 5: Place in Row 1, Column 3
```

### 5.4 Add Widgets — Row 2

```
--- Widget 4: Incident Trend ---

Step 1: Click "Add Widget"
Step 2: Select "Reports"
Step 3: Select "UPI Incident Trend - Monthly"
Step 4: Place in Row 2, left half (span 2 columns)

--- Widget 5: Change Success Rate ---

Step 1: Click "Add Widget"
Step 2: Select "Reports"
Step 3: Select "UPI Change Success Rate" (or use PA dial widget)
Step 4: Place in Row 2, right column
```

### 5.5 Add Widgets — Row 3

```
--- Widget 6: Top Impacted CIs ---

Step 1: Click "Add Widget"
Step 2: Select "Reports"
Step 3: Select "UPI Top 10 Impacted CIs"
Step 4: Place in Row 3, left half

--- Widget 7: Problem Status ---

Step 1: Click "Add Widget"
Step 2: We need a new quick report for Problem Status

  Create Report:
    Name:       UPI Problem Status Distribution
    Table:      Problem [problem]
    Type:       Donut
    Group by:   State
    Colors:
      New = Blue
      Open = Orange
      Work In Progress = Yellow
      Closed = Green

Step 3: Save the report
Step 4: Return to dashboard, add this report as widget
Step 5: Place in Row 3, right column
```

### 5.6 Finalize the Dashboard

```
Step 1: Arrange all 7 widgets in the layout described above
        Use drag-and-drop to reposition
        Use resize handles to adjust width

Step 2: Set auto-refresh:
        Dashboard Settings (gear icon) > Auto-refresh: 5 minutes

Step 3: Click "Save"

Step 4: Preview the dashboard
        Verify all charts render correctly
        Click chart elements to test drill-down

Step 5: Set as your homepage (optional):
        User Menu (top right) > Set as Homepage
```

---

## Part 6: Scheduled Reports

### 6.1 Schedule Weekly ITSM Summary

```
Purpose: Automatically email a weekly ITSM summary to management every Monday.

Navigation: Reports > View/Run (select a report to schedule)

Step 1: Open report "UPI Incident Trend - Monthly"
Step 2: Click the "Sharing" icon (or right-click > Schedule)

  OR

Step 1: Navigate to Reports > Scheduled Reports
Step 2: Click "New"
```

### 6.2 Configure the Schedule

```
SCHEDULED REPORT FORM:

  Name:             Weekly UPI ITSM Summary
  Report:           UPI Incident Trend - Monthly

  TYPE:
    Type:           Once per period
    Run:            Weekly
    Day of week:    Monday
    Time:           08:00 (IST / your timezone)

  DELIVERY:
    Send to:
      Users:        Sanjay Kumar (IT Service Manager)
                    Ravi Kumar (Platform Engineering Lead)
      Groups:       UPI-Management (if group exists)

    Subject:        [NPCI-UPI] Weekly ITSM Summary - {{date}}

    Message body:
      Dear Team,

      Please find attached the weekly UPI ITSM summary report.

      Key highlights will be included in the attached PDF.

      For the full interactive dashboard, please visit:
      [link to UPI Service Management Dashboard]

      Regards,
      ServiceNow Automated Reports

    Format:         PDF

    Include link to report: Yes

Click "Save"
```

### 6.3 Schedule Multiple Reports

```
Repeat the scheduling for other key reports:

Report                           Frequency    Recipients           Format
---------------------------------------------------------------------------
UPI Incidents by Priority        Weekly       Sanjay, Ravi         PDF
UPI SLA Compliance by Priority   Weekly       Sanjay               PDF
UPI Change Success Rate          Monthly      Sanjay, Board Dist   PDF
UPI MTTR by Priority             Monthly      Platform Eng Team    PDF
UPI Top 10 Impacted CIs          Monthly      Sanjay, NOC Lead     Excel

To create each:
  1. Open the report
  2. Click Schedule
  3. Set frequency and recipients
  4. Save
```

### 6.4 Verify Scheduled Reports

```
Navigation: Reports > Scheduled Reports

You should see a list of all scheduled reports:

  Name                                Next Run           Active
  ------------------------------------------------------------------
  Weekly UPI ITSM Summary             Next Monday 08:00  Yes
  Weekly UPI Incidents by Priority    Next Monday 08:00  Yes
  Weekly UPI SLA Compliance           Next Monday 08:00  Yes
  Monthly UPI Change Success Rate     First of Month     Yes
  Monthly UPI MTTR by Priority        First of Month     Yes
  Monthly UPI Top 10 Impacted CIs     First of Month     Yes

To test: Click a scheduled report > Click "Execute Now"
Check your email for the PDF attachment.
```

---

## Part 7: Report Sharing & Access Control

### 7.1 Share Dashboard with Groups

```
Step 1: Open "UPI Service Management Dashboard"
Step 2: Click the "Share" icon (or gear > Sharing)

SHARING OPTIONS:
  Share with:
    Groups:     UPI-Platform-Engineering
                UPI-NOC
                UPI-Management

    Users:      Sanjay Kumar
                Ravi Kumar

    Roles:      itil (all ITIL users)

  Permission:   View only (they can view but not edit)

Step 3: Click "Share" / "Save"

Result: Members of these groups will see the dashboard in their
        Self-Service > Dashboards list.
```

### 7.2 Publish to Homepage

```
Making the dashboard appear on user homepages:

Method 1: System Administrator sets default homepage
  Navigation: System UI > Homepage Admin

  1. Select the user's role or group
  2. Add "UPI Service Management Dashboard" as a tab
  3. Save

Method 2: Users self-select
  Users can navigate to:
    Self-Service > Dashboards > UPI Service Management Dashboard
    Click "Set as Homepage"

Method 3: Content Block on Service Portal
  For Service Portal users:
    1. Navigate to Service Portal > Pages
    2. Edit the homepage
    3. Add a "Dashboard" widget
    4. Configure it to show the ITSM dashboard
```

### 7.3 Report ACLs (Access Control Lists)

```
Reports in ServiceNow respect table-level ACLs:

  - If a user cannot read the Incident table, they cannot see incident reports
  - If a user has row-level ACLs (e.g., only their group's incidents),
    the report only shows data they can access

Additional report-level controls:

  Navigation: Reports > [Open any report] > Sharing tab

  Owner:           System Administrator
  Visible to:      Everyone / Groups / Roles / Owner only
  Editable by:     Owner only / Specific groups

Best Practices for NPCI:
  +---------------------------+------------------------------------+
  | Audience                  | Access Level                       |
  +---------------------------+------------------------------------+
  | Board / C-Level           | Executive Dashboard (view only)    |
  | IT Service Manager        | All ITSM reports (view + create)   |
  | Team Leads                | Team-specific reports (view only)  |
  | Service Desk Agents       | Operational reports only           |
  | End Users (Service Portal)| No report access (use portal KPIs)|
  +---------------------------+------------------------------------+
```

### 7.4 Export Options

```
Every report can be exported in multiple formats:

Step 1: Open any report (e.g., "UPI Incidents by Priority")
Step 2: Click the context menu (hamburger icon or right-click)
Step 3: Select "Export"

Available formats:
  +--------+----------------------------------------------------+
  | Format | Use Case                                           |
  +--------+----------------------------------------------------+
  | PDF    | Formal reports for management, email attachments    |
  | PNG    | Images for presentations                           |
  | Excel  | Further analysis, pivot tables, custom calculations |
  | CSV    | Data import to other tools, large datasets          |
  +--------+----------------------------------------------------+

Bulk export:
  For the executive dashboard, you can:
  1. Open the dashboard
  2. Click "Export" (if available at dashboard level)
  3. Each widget exports individually via its menu

Tip: For board presentations, export charts as PNG and embed in PowerPoint.
```

---

## Practice Exercises

### Exercise 1: Incident Heatmap (Day of Week vs Hour of Day)

```
OBJECTIVE: Identify when incidents occur most frequently to optimize staffing.

Step 1: Navigate to Reports > Create New

Step 2: Configure:
  Name:             UPI Incident Heatmap - Day vs Hour
  Source type:       Table
  Table:            Incident [incident]
  Type:             Heatmap

Step 3: Group By tab:
  Group by:         Created (Day of week)
  Stack by:         Created (Hour of day)

Step 4: Aggregation:
  Aggregate:        Count

Step 5: Filter:
  Condition 1:      Created | on | Last 180 days

Step 6: Style:
  Title:            When Do Incidents Occur? (Day x Hour Heatmap)
  Color scheme:     Green (low) to Red (high)

Step 7: Save and Run

EXPECTED INSIGHT:
  +-------+--00--01--02--03--...--09--10--11--12--...--17--18--19--+
  | Mon   |   1   0   0   1        5   8  12  10        6   3   2  |
  | Tue   |   0   1   0   0        4   9  11   8        7   2   1  |
  | Wed   |   1   0   1   0        6  10  14  11        5   3   1  |
  | Thu   |   0   0   0   1        5   8  10   9        6   2   2  |
  | Fri   |   2   1   0   0        7  11  15  12        8   4   1  |
  | Sat   |   0   0   0   0        2   3   4   3        2   1   0  |
  | Sun   |   0   0   0   0        1   2   2   2        1   0   0  |
  +-------+--------------------------------------------------------+

  INSIGHT: Peak incident time = Wednesday-Friday, 10AM-12PM
  RECOMMENDATION: Ensure full L2 staffing during this window.
  Weekend incidents are minimal - consider on-call model.
```

---

### Exercise 2: PA Indicator — Incident Reopen Rate

```
OBJECTIVE: Track the percentage of incidents that are reopened after resolution.

Step 1: Create Base Indicator A - "Reopened Incidents"
  Navigation:       Performance Analytics > Indicators > New
  Name:             Reopened Incidents Count - UPI
  Table:            Incident [incident]
  Aggregate:        Count
  Conditions:       Reopen count | greater than | 0
                    Resolved | on | Last 30 days
  Frequency:        Weekly

Step 2: Create Base Indicator B - "Total Resolved Incidents"
  Name:             Total Resolved Incidents - UPI
  Table:            Incident [incident]
  Aggregate:        Count
  Conditions:       State | is | Resolved
                    Resolved | on | Last 30 days
  Frequency:        Weekly

Step 3: Create Formula Indicator
  Name:             Incident Reopen Rate - UPI
  Type:             Formula
  Formula:          (A / B) * 100
  Direction:        Minimize
  Unit:             Percentage

Step 4: Set Target
  Target value:     5 (%)
  Thresholds:       Green: 0-3%, Yellow: 3-5%, Red: 5%+

Step 5: Collect data and verify

EXPECTED: If 2 out of 40 resolved incidents were reopened:
  Reopen Rate = (2/40) * 100 = 5% --> YELLOW (at threshold)
```

---

### Exercise 3: Monthly UPI Service Health Summary

```
OBJECTIVE: Create a comprehensive management report combining multiple metrics.

This is a COMPOSITE REPORT using a dashboard approach:

Step 1: Create a new dashboard
  Name:             Monthly UPI Service Health Summary
  Category:         Management Reports

Step 2: Add the following widgets in order:

  Section 1: "Executive Summary" (Text widget)
    Content:
    "UPI Platform Service Health - {{current_month}} {{current_year}}
     Report generated for NPCI IT Service Management
     Prepared by: IT Service Manager"

  Section 2: KPI Row
    Widget 1:       Open P1 Incidents (Single Score)
    Widget 2:       SLA Compliance % (Speedometer)
    Widget 3:       Change Success Rate (Dial)
    Widget 4:       MTTR P1 (Single Score, hours)

  Section 3: Trends
    Widget 5:       Incident Trend - Monthly (Line, 6 months)
    Widget 6:       Problem Closure Trend (Line, 6 months)

  Section 4: Details
    Widget 7:       Top 10 Impacted CIs (Bar)
    Widget 8:       SLA Compliance Matrix (Pivot Table)

  Section 5: Action Items (Text widget)
    Content:
    "Open Actions:
     1. Investigate P2 SLA breaches - assigned to Platform Engineering
     2. Review UPI-TXN-SVC incident frequency - Problem ticket PRB0040002
     3. Schedule preventive maintenance for UPI-PSP-Server-01
     4. Increase Knowledge Base coverage for top 5 incident categories"

Step 3: Schedule as PDF
  Frequency:        Monthly (First Monday of month)
  Recipients:       Sanjay Kumar, CTO Distribution List
  Format:           PDF
```

---

### Exercise 4: Month-over-Month Comparison Report

```
OBJECTIVE: Compare this month's incident count with last month's.

Method 1: Two-Series Line Chart

Step 1: Navigate to Reports > Create New
  Name:             UPI Incident Comparison - Current vs Previous Month
  Table:            Incident [incident]
  Type:             Bar

Step 2: Create two reports and overlay:

  Report A: "Current Month Incidents"
    Filter:         Created | on | This month
    Group by:       Priority
    Aggregate:      Count

  Report B: "Previous Month Incidents"
    Filter:         Created | on | Last month
    Group by:       Priority
    Aggregate:      Count

Step 3: Add both to a dashboard side by side

  +----------------------------------+----------------------------------+
  | Current Month (September 2024)   | Previous Month (August 2024)     |
  | P1: 3                            | P1: 5                            |
  | P2: 8                            | P2: 12                           |
  | P3: 15                           | P3: 18                           |
  | P4: 22                           | P4: 25                           |
  | Total: 48                        | Total: 60                        |
  +----------------------------------+----------------------------------+

  INSIGHT: 20% reduction in total incidents month-over-month
  P1 incidents reduced by 40% - Problem Management is effective!

Method 2: PA Time Series with Two Periods

Step 1: Open any PA indicator (e.g., "Open P1 Incidents")
Step 2: In Analytics view, select:
  Primary period:    This month
  Comparison period: Last month
Step 3: The chart overlays both periods for visual comparison
```

---

### Exercise 5: Custom Homepage with Executive Dashboard

```
OBJECTIVE: Create a custom landing page that shows the executive dashboard.

Step 1: Navigate to Self-Service > Homepage
        OR System UI > Homepages

Step 2: Click "New Tab" or create a new homepage:
  Name:             UPI ITSM Overview

Step 3: Add content:

  Layout:           3-column (Top), 2-column (Middle), Full-width (Bottom)

  Top Row:
    Column 1:       PA Scorecard - Open P1 Incidents
    Column 2:       PA Scorecard - SLA Compliance %
    Column 3:       PA Scorecard - Change Success Rate

  Middle Row:
    Left:           Report - Incident Trend (Line chart)
    Right:          Report - Problem Status (Donut)

  Bottom Row:
    Full width:     Report - Top 10 Impacted CIs (Horizontal Bar)

Step 4: Set as default homepage:
  Click your user profile (top right)
  Preferences > Homepage > Select "UPI ITSM Overview"

  OR for all ITIL users:
  System Properties > Homepage > Default homepage for role "itil"
  Set to: "UPI ITSM Overview"

Step 5: Verify by logging out and back in
  The dashboard should appear immediately upon login.
```

---

## Appendix A: Background Script — Generate Sample Data for Reports

This script creates sample data across Incidents, Problems, and Changes to make your reports meaningful.

**WARNING:** Only run on a Personal Developer Instance (PDI). Never on production.

```
Navigation: System Definition > Scripts - Background
```

### Script 1: Create 50 Sample Incidents

```javascript
// ============================================================
// SAMPLE DATA GENERATOR: 50 Incidents for UPI Platform
// Run in: System Definition > Scripts - Background
// PDI ONLY - Never run on production!
// ============================================================

var priorities = [1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4];
var categories = ['Software', 'Software', 'Network', 'Hardware', 'Database', 'Software'];
var states = [1, 2, 6, 7]; // New, In Progress, Resolved, Closed

var shortDescriptions = [
    'UPI Transaction timeout during peak hours',
    'PSP connectivity failure - Bank of Baroda',
    'API Gateway returning 503 errors',
    'MongoDB replication lag exceeding threshold',
    'SSL certificate expiry warning on UPI-TXN-SVC',
    'Memory leak detected on UPI-PSP-Server-01',
    'Kafka consumer lag increasing on payment queue',
    'DNS resolution failure for UPI merchant endpoints',
    'Load balancer health check failures',
    'Settlement batch job failed - EOD processing',
    'UPI QR code generation service unresponsive',
    'Transaction reversal not processing for HDFC',
    'Monitoring alerts not triggering for P1 conditions',
    'Firewall blocking legitimate UPI callbacks',
    'Database connection pool exhausted',
    'UPI mandate registration failing intermittently',
    'CDN cache invalidation not working',
    'Audit log rotation failure - disk space warning',
    'Backup job failed on MongoDB secondary',
    'High CPU utilization on UPI-PSP-Server-02',
    'VPA validation service returning incorrect results',
    'Transaction status API returning stale data',
    'Dispute management portal login failure',
    'Bulk payout processing stuck in queue',
    'IMPS fallback not triggering during UPI downtime',
    'Rate limiting not enforced on merchant API',
    'Duplicate transaction IDs generated',
    'Reconciliation mismatch for SBI transactions',
    'Payment confirmation SMS delay exceeding 5 minutes',
    'Merchant onboarding workflow stuck at approval',
    'UPI LITE balance not updating after transaction',
    'AutoPay mandate execution failure',
    'Collect request notification not delivered',
    'Transaction history API pagination broken',
    'UPI PIN change not reflecting in real-time',
    'Interoperability failure with RuPay network',
    'Server certificate chain incomplete on API GW',
    'Connection timeout to NPCI switching server',
    'Batch file transfer to RBI delayed',
    'UPI International transaction routing failure',
    'Performance degradation during month-end processing',
    'Webhook delivery failure to merchant endpoints',
    'JWT token validation failing intermittently',
    'Service mesh sidecar proxy crashing',
    'Configuration drift detected on production servers',
    'Incident auto-assignment rule not working',
    'Knowledge base search returning no results',
    'SLA timer not starting for P2 incidents',
    'Email notifications going to spam folder',
    'Dashboard widgets not loading for NOC team'
];

// Get assignment groups
var platformEng = '';
var noc = '';
var serviceDesk = '';

var grpGR = new GlideRecord('sys_user_group');
grpGR.addQuery('name', 'CONTAINS', 'Platform');
grpGR.query();
if (grpGR.next()) platformEng = grpGR.sys_id;

grpGR.initialize();
grpGR.addQuery('name', 'CONTAINS', 'NOC');
grpGR.query();
if (grpGR.next()) noc = grpGR.sys_id;

grpGR.initialize();
grpGR.addQuery('name', 'CONTAINS', 'Service Desk');
grpGR.query();
if (grpGR.next()) serviceDesk = grpGR.sys_id;

var groups = [platformEng, noc, serviceDesk];
var validGroups = groups.filter(function(g) { return g !== ''; });
if (validGroups.length === 0) {
    gs.info('No matching groups found. Incidents will be created without assignment group.');
}

// Get CI sys_ids
var ciNames = [
    'UPI-TXN-SVC', 'UPI-PSP-Server-01', 'UPI-API-Gateway',
    'UPI-Settlement-Engine', 'UPI-PSP-Server-02', 'UPI-MongoDB-Primary',
    'UPI-Load-Balancer', 'UPI-Kafka-Cluster'
];
var ciMap = {};
for (var c = 0; c < ciNames.length; c++) {
    var ciGR = new GlideRecord('cmdb_ci');
    ciGR.addQuery('name', ciNames[c]);
    ciGR.query();
    if (ciGR.next()) {
        ciMap[ciNames[c]] = ciGR.sys_id.toString();
    }
}
var ciKeys = Object.keys(ciMap);

var count = 0;
for (var i = 0; i < 50; i++) {
    var inc = new GlideRecord('incident');
    inc.initialize();

    inc.short_description = shortDescriptions[i % shortDescriptions.length];
    inc.description = 'Auto-generated sample incident for reporting lab. ' +
                      shortDescriptions[i % shortDescriptions.length];
    inc.priority = priorities[i % priorities.length];
    inc.category = categories[i % categories.length];

    // Set state (mix of open and resolved/closed)
    var stateIndex = i % states.length;
    inc.state = states[stateIndex];

    // Set created date spread over last 90 days
    var daysAgo = Math.floor(Math.random() * 90);
    var createdDate = new GlideDateTime();
    createdDate.addDaysLocalTime(-daysAgo);
    inc.setValue('opened_at', createdDate.toString());

    // Set resolved date for resolved/closed incidents
    if (states[stateIndex] == 6 || states[stateIndex] == 7) {
        var resolvedDate = new GlideDateTime(createdDate);
        var resolutionHours = 0;

        // Resolution time based on priority
        switch (parseInt(priorities[i % priorities.length])) {
            case 1: resolutionHours = 2 + Math.floor(Math.random() * 6); break;  // 2-8 hrs
            case 2: resolutionHours = 4 + Math.floor(Math.random() * 12); break;  // 4-16 hrs
            case 3: resolutionHours = 8 + Math.floor(Math.random() * 40); break;  // 8-48 hrs
            case 4: resolutionHours = 24 + Math.floor(Math.random() * 96); break; // 24-120 hrs
        }
        resolvedDate.addSeconds(resolutionHours * 3600);
        inc.setValue('resolved_at', resolvedDate.toString());

        if (states[stateIndex] == 7) {
            inc.setValue('closed_at', resolvedDate.toString());
            inc.close_code = 'Solved (Permanently)';
            inc.close_notes = 'Issue resolved. Root cause identified and fix applied.';
        }
    }

    // Assign group
    if (validGroups.length > 0) {
        if (priorities[i % priorities.length] <= 2) {
            inc.assignment_group = validGroups[0]; // Platform Eng for P1/P2
        } else {
            inc.assignment_group = validGroups[i % validGroups.length];
        }
    }

    // Assign CI
    if (ciKeys.length > 0) {
        var ciIndex = i % ciKeys.length;
        // Weight toward UPI-TXN-SVC (index 0) for realistic distribution
        if (i % 3 === 0 && ciMap['UPI-TXN-SVC']) {
            inc.cmdb_ci = ciMap['UPI-TXN-SVC'];
        } else {
            inc.cmdb_ci = ciMap[ciKeys[ciIndex]];
        }
    }

    inc.insert();
    count++;
}

gs.info('Created ' + count + ' sample incidents for reporting lab.');
```

### Script 2: Create 20 Sample Changes

```javascript
// ============================================================
// SAMPLE DATA GENERATOR: 20 Change Requests for UPI Platform
// Run in: System Definition > Scripts - Background
// PDI ONLY - Never run on production!
// ============================================================

var changeDescriptions = [
    'Deploy UPI Transaction Service v2.4.1 - circuit breaker implementation',
    'Upgrade MongoDB cluster to version 7.0',
    'Add new PSP bank integration - Federal Bank',
    'Update firewall rules for UPI callback endpoints',
    'SSL certificate renewal for all UPI services',
    'Scale out UPI-PSP-Server fleet from 4 to 6 nodes',
    'Implement rate limiting on merchant API gateway',
    'Deploy Kafka cluster upgrade to 3.6',
    'Update DNS configuration for disaster recovery',
    'Patch Linux kernel on all UPI production servers',
    'Enable TLS 1.3 on API Gateway',
    'Migrate settlement engine to containerized deployment',
    'Add monitoring probes for UPI LITE service',
    'Update load balancer health check configuration',
    'Deploy new fraud detection rules engine',
    'Upgrade Java runtime to OpenJDK 21 LTS',
    'Implement automated backup verification',
    'Add new UPI merchant VPA whitelist entries',
    'Deploy CDN edge cache configuration update',
    'Network switch firmware upgrade in DC-1'
];

var changeTypes = ['Normal', 'Normal', 'Normal', 'Standard', 'Emergency'];
var closeCodes = ['Successful', 'Successful', 'Successful', 'Successful', 'Unsuccessful'];
// 80% success rate to make reports interesting

var count = 0;
for (var i = 0; i < 20; i++) {
    var chg = new GlideRecord('change_request');
    chg.initialize();

    chg.short_description = changeDescriptions[i];
    chg.description = 'Sample change request for reporting lab. ' + changeDescriptions[i];
    chg.type = changeTypes[i % changeTypes.length].toLowerCase();
    chg.priority = (i % 4) + 1;
    chg.risk = ['High', 'Moderate', 'Low', 'Low'][i % 4];
    chg.category = ['Software', 'Hardware', 'Network', 'Software'][i % 4];

    // Set dates spread over last 90 days
    var daysAgo = Math.floor(Math.random() * 90);
    var createdDate = new GlideDateTime();
    createdDate.addDaysLocalTime(-daysAgo);
    chg.setValue('opened_at', createdDate.toString());

    // Most changes are closed
    if (i < 18) {
        chg.state = -3; // Closed state for change_request
        chg.close_code = closeCodes[i % closeCodes.length];
        chg.close_notes = 'Change completed. ' +
            (closeCodes[i % closeCodes.length] === 'Successful' ?
             'All validation checks passed.' :
             'Rollback executed due to unexpected issues.');

        var closedDate = new GlideDateTime(createdDate);
        closedDate.addDaysLocalTime(Math.floor(Math.random() * 7) + 1);
        chg.setValue('closed_at', closedDate.toString());
    } else {
        chg.state = -1; // New
    }

    chg.insert();
    count++;
}

gs.info('Created ' + count + ' sample change requests for reporting lab.');
```

### Script 3: Create 10 Sample Problems

```javascript
// ============================================================
// SAMPLE DATA GENERATOR: 10 Problems for UPI Platform
// Run in: System Definition > Scripts - Background
// PDI ONLY - Never run on production!
// ============================================================

var problemDescriptions = [
    'Recurring transaction timeouts on UPI-TXN-SVC during peak hours',
    'Intermittent PSP connectivity failures affecting Bank of Baroda',
    'Memory leak in UPI API Gateway causing periodic 503 errors',
    'MongoDB replication lag causing stale read data',
    'Kafka consumer group rebalancing causing message processing delays',
    'DNS TTL misconfiguration causing intermittent resolution failures',
    'Load balancer session persistence not working for WebSocket connections',
    'Settlement batch job failure due to race condition in parallel processing',
    'Monitoring false positives from misconfigured health check thresholds',
    'Configuration drift between production servers causing inconsistent behavior'
];

var problemCategories = [
    'Software', 'Network', 'Software', 'Database', 'Software',
    'Network', 'Hardware', 'Software', 'Software', 'Software'
];

var problemStates = [1, 2, 3, 4, 4]; // New, Open, Known Error, Closed, Closed

var count = 0;
for (var i = 0; i < 10; i++) {
    var prb = new GlideRecord('problem');
    prb.initialize();

    prb.short_description = problemDescriptions[i];
    prb.description = 'Sample problem for reporting lab. ' + problemDescriptions[i];
    prb.category = problemCategories[i];
    prb.priority = (i % 3) + 1; // P1, P2, P3

    var stateVal = problemStates[i % problemStates.length];
    prb.state = stateVal;

    // Set dates
    var daysAgo = Math.floor(Math.random() * 120) + 30;
    var createdDate = new GlideDateTime();
    createdDate.addDaysLocalTime(-daysAgo);
    prb.setValue('opened_at', createdDate.toString());

    // Closed problems get root cause
    if (stateVal == 4) {
        prb.cause_notes = 'Root cause identified: ' + problemDescriptions[i];
        prb.fix_notes = 'Permanent fix applied and verified in production.';
        var closedDate = new GlideDateTime(createdDate);
        closedDate.addDaysLocalTime(Math.floor(Math.random() * 30) + 7);
        prb.setValue('closed_at', closedDate.toString());
    }

    // Known errors get workaround
    if (stateVal == 3) {
        prb.workaround = 'Temporary workaround in place: Restart affected service ' +
                         'and monitor for recurrence. Permanent fix in development.';
    }

    prb.insert();
    count++;
}

gs.info('Created ' + count + ' sample problems for reporting lab.');
```

### Script 4: Verify Data Counts

```javascript
// ============================================================
// VERIFICATION SCRIPT: Count records for reporting
// Run after the above scripts to confirm data exists
// ============================================================

var tables = ['incident', 'problem', 'change_request', 'task_sla',
              'sc_req_item', 'kb_knowledge', 'cmdb_ci'];

for (var t = 0; t < tables.length; t++) {
    var gr = new GlideRecord(tables[t]);
    gr.query();
    gs.info(tables[t] + ': ' + gr.getRowCount() + ' records');
}

// Incident breakdown by priority
gs.info('--- Incidents by Priority ---');
for (var p = 1; p <= 4; p++) {
    var incGR = new GlideRecord('incident');
    incGR.addQuery('priority', p);
    incGR.query();
    gs.info('  Priority ' + p + ': ' + incGR.getRowCount());
}

// Change breakdown by close code
gs.info('--- Changes by Close Code ---');
var codes = ['Successful', 'Unsuccessful', 'Incomplete'];
for (var c = 0; c < codes.length; c++) {
    var chgGR = new GlideRecord('change_request');
    chgGR.addQuery('close_code', codes[c]);
    chgGR.query();
    gs.info('  ' + codes[c] + ': ' + chgGR.getRowCount());
}
```

---

## Appendix B: Quick Reference — Report Building Cheat Sheet

```
+--------------------------------------------+-------------------------------+
| I want to see...                           | Use this report type          |
+--------------------------------------------+-------------------------------+
| How many incidents per priority            | Bar or Donut chart            |
| Incident volume trend over months          | Line chart (Group by: Month)  |
| When incidents happen (day/time)           | Heatmap                       |
| SLA breach breakdown                       | Pivot Table                   |
| One KPI number (e.g., open count)          | Single Score                  |
| KPI against target                         | Speedometer or Dial           |
| Workload across teams                      | Horizontal Bar                |
| Category distribution                      | Pie or Donut                  |
| Detailed list of records                   | List report                   |
| Two metrics compared side by side          | Column chart with Stack By    |
| KPI trend over time with forecast          | PA Time Series widget         |
| Multiple KPIs in one view                  | Dashboard with PA Scorecards  |
+--------------------------------------------+-------------------------------+
```

---

## Appendix C: Common Troubleshooting

```
ISSUE: Report shows "No data to display"
FIX:   1. Check your filter conditions - they may be too restrictive
       2. Verify the table has data (navigate to the list view)
       3. Run the sample data scripts from Appendix A
       4. Check ACLs - your user may not have access to all records

ISSUE: Performance Analytics indicators show no data
FIX:   1. Run the data collector: PA > Data Collector > Jobs > Execute Now
       2. Wait 2-3 minutes for collection to complete
       3. Verify the indicator's source filter matches existing records
       4. Check that the PA plugin is active: Plugins > Performance Analytics

ISSUE: Scheduled report not sending emails
FIX:   1. Verify email is configured: System Mailboxes > Outbound
       2. Check the scheduled report is Active = true
       3. Verify recipient email addresses are valid
       4. Check System Logs > Emails for delivery errors
       5. In PDI, email may be disabled by default - enable SMTP

ISSUE: Dashboard widgets not loading
FIX:   1. Clear browser cache and refresh
       2. Verify the underlying reports still exist
       3. Check for JavaScript errors in browser console
       4. Try a different browser
       5. Verify your role has access to the report tables

ISSUE: PA forecast not showing
FIX:   1. Forecasting requires minimum 3 data collection points
       2. Run data collection multiple times with different dates
       3. Ensure the indicator has "Enable forecasting" checked
```

---

## Lab Checklist

Before marking this lab complete, verify:

```
[ ] Understand ITIL 4 Measurement & Reporting practice
[ ] Can explain CSFs, KPIs, and the metrics hierarchy
[ ] Know the difference between basic reporting and Performance Analytics

Reports Created:
[ ] Report 1:  Incident Trend (Line chart)
[ ] Report 2:  Incidents by Priority (Donut)
[ ] Report 3:  Incidents by Assignment Group (Horizontal Bar)
[ ] Report 4:  SLA Compliance (Pivot Table)
[ ] Report 5:  MTTR by Priority (Bar chart)
[ ] Report 6:  Change Success Rate (Single Score)
[ ] Report 7:  Problem Root Cause (Pie chart)
[ ] Report 8:  Top 10 Impacted CIs (Bar chart)
[ ] Report 9:  Knowledge Article Usage (Line chart)
[ ] Report 10: Request Fulfillment Time (Bar chart)

Performance Analytics:
[ ] PA data collection enabled
[ ] Indicator: Open P1 Incidents
[ ] Indicator: Average Resolution Time
[ ] Indicator: SLA Breach Rate
[ ] Indicator: Change Failure Rate
[ ] Breakdowns configured (by priority, group, service)
[ ] Targets and thresholds set (green/yellow/red)

Dashboard & Delivery:
[ ] Executive Dashboard built with 7 widgets
[ ] Scheduled weekly report configured
[ ] Dashboard shared with appropriate groups
[ ] Export tested (PDF and Excel)

Practice Exercises:
[ ] Heatmap: Incidents by Day x Hour
[ ] PA Indicator: Reopen Rate
[ ] Monthly Service Health Summary
[ ] Month-over-month comparison
[ ] Custom homepage configured
```

---

## What's Next?

```
Lab 18 will cover Continual Service Improvement (CSI), where we use these
reports and analytics to:

  1. Identify improvement opportunities from the data
  2. Create CSI registers
  3. Prioritize improvements using business value
  4. Implement changes and measure their impact
  5. Close the Deming cycle: Plan-Do-Check-Act

The reports and dashboards from Lab 17 become the INPUT to Lab 18's
improvement initiatives.

  Data (Lab 17) --> Insight (Lab 18) --> Action (Lab 18) --> Measurement (Lab 17)

This is the engine of Continual Improvement.
```

---

*Lab 17 Complete — Reporting & Performance Analytics for NPCI UPI Platform*
