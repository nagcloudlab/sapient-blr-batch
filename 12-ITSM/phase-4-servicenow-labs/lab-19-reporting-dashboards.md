# Lab 19: Reporting & Dashboards

**Level:** Expert | **Duration:** 90 minutes | **Prerequisites:** Lab 07-18 completed (need data from earlier labs)

---

## Objective

By the end of this lab, you will:
- Create reports (bar, pie, line, list, pivot table)
- Schedule and share reports
- Build custom dashboards with multiple widgets
- Use Performance Analytics indicators and breakdowns
- Create executive-level ITSM dashboards

---

## Part 1: Create Reports

### Step 1.1: Navigate to Reports

1. Navigate to **Reports > Create New** (or type `sys_report.do`)
2. The Report Designer opens

### Step 1.2: Bar Chart -- Incidents by Priority

1. In the Report Designer:

   | Field | Value |
   |---|---|
   | Report name | Open Incidents by Priority |
   | Source type | Table |
   | Table | Incident [incident] |
   | Type | Bar |

2. **Configure** tab:
   - Group by: **Priority**
   - Aggregation: **Count**
   - Filter: State is not Closed AND State is not Canceled

3. **Style** tab:
   - Title: Open Incidents by Priority
   - Show data labels: Checked
   - Color scheme: (choose one you like)

4. Click **Save**
5. Click **Run** to see the chart

### Step 1.3: Pie Chart -- Incidents by Category

1. Create a new report:

   | Field | Value |
   |---|---|
   | Report name | Incidents by Category |
   | Table | Incident |
   | Type | Pie |
   | Group by | Category |
   | Filter | Opened in Last 30 days |

2. Save and Run

### Step 1.4: Line Chart -- Incident Trend

1. Create:

   | Field | Value |
   |---|---|
   | Report name | Incident Trend - Last 12 Weeks |
   | Table | Incident |
   | Type | Line |
   | Group by | Opened (by week) |
   | Aggregation | Count |
   | Trend by | Opened |
   | Filter | Opened in Last 90 days |

2. Save and Run
3. This shows weekly incident volume trends

### Step 1.5: Donut Chart -- Incidents by State

1. Create:

   | Field | Value |
   |---|---|
   | Report name | Incident Distribution by State |
   | Table | Incident |
   | Type | Donut |
   | Group by | State |

### Step 1.6: List Report -- Open P1/P2 Incidents

1. Create:

   | Field | Value |
   |---|---|
   | Report name | Open Critical/High Incidents |
   | Table | Incident |
   | Type | List |
   | Columns | Number, Short description, Priority, State, Assigned to, Assignment group, SLA due |
   | Filter | Priority in (1,2) AND State not in (Resolved, Closed, Canceled) |
   | Sort by | Priority ascending, then SLA due ascending |

### Step 1.7: Pivot Table -- Incidents by Priority and Category

1. Create:

   | Field | Value |
   |---|---|
   | Report name | Priority vs Category Matrix |
   | Table | Incident |
   | Type | Pivot Table |
   | Group by (rows) | Category |
   | Stack by (columns) | Priority |
   | Aggregation | Count |

---

## Part 2: Schedule and Share Reports

### Step 2.1: Schedule a Report

1. Open any saved report
2. Click the **Share** or **Schedule** button
3. Configure:

   | Field | Value |
   |---|---|
   | Run | Daily / Weekly / Monthly |
   | Time | 08:00 AM |
   | Send to | (select users or groups) |
   | Format | PDF |
   | Subject | Daily ITSM Report: Open Incidents by Priority |

4. Save the schedule

### Step 2.2: Share a Report

1. Open a report
2. Click **Share**
3. Options:
   - Share with specific users or groups
   - Make it available on a dashboard
   - Publish to a specific module

### Step 2.3: Export Reports

1. Open a report
2. Click **Export**:
   - PDF -- formatted document
   - Excel -- spreadsheet with data
   - Image -- PNG/JPG of the chart

---

## Part 3: Build Dashboards

### Step 3.1: Create a New Dashboard

1. Navigate to **Self-Service > Dashboards** (or type `$pa_dashboard.do`)
2. Click **New** or the **+** icon to create a new dashboard
3. Name: **ITSM Operations Dashboard**
4. Click **Create**

### Step 3.2: Add Widgets

A dashboard is made of **widgets** (reports, gauges, lists, counters).

**Widget 1: Single Score -- Open Incident Count**
1. Click **Add Widget** (or the + icon on the dashboard canvas)
2. Select **Reports** tab
3. Find "Open Incidents by Priority" (your report from Part 1)
4. Drag it to the dashboard

**Widget 2: Create a Gauge**
1. Add another widget
2. Type: **Gauge** or **Dial**
3. Configure:
   - Label: SLA Compliance Rate
   - Data source: (configure to show percentage of SLAs met)

**Widget 3: Add a List Widget**
1. Add widget type: **List**
2. Table: Incident
3. Filter: Priority = 1 AND State = Open
4. Title: "Active P1 Incidents"

**Widget 4: Trend Chart**
1. Add your "Incident Trend" line chart

### Step 3.3: Arrange the Dashboard

```
+---------------------------+---------------------------+
| Open Incidents by Priority| Incidents by Category     |
| (Bar Chart)               | (Pie Chart)               |
+---------------------------+---------------------------+
| Incident Trend            | SLA Compliance            |
| (Line Chart)              | (Gauge/Dial)              |
+---------------------------+---------------------------+
| Active P1 Incidents (List)                            |
|                                                        |
| INC001 | Server down | P1 | In Progress | Ravi       |
| INC002 | VPN outage  | P1 | New         | Unassigned |
+---------------------------+---------------------------+
```

1. Drag widgets to rearrange
2. Resize widgets by dragging edges
3. Click **Save** when done

### Step 3.4: Create a Change Management Dashboard

Build a second dashboard: **Change Management Dashboard**

Add these widgets:
1. **Changes by Type** (pie: Normal, Standard, Emergency)
2. **Change Calendar** (calendar widget showing scheduled changes)
3. **Changes by State** (bar: New, Assess, Authorize, Scheduled, etc.)
4. **Failed Changes - Last 30 Days** (list report)
5. **Change Success Rate** (single score/gauge)

---

## Part 4: Performance Analytics (PA)

### Step 4.1: What is PA?

Performance Analytics provides real-time KPI tracking, trends, and analytics. It goes beyond basic reports.

```
Reports = "What happened?" (snapshot)
PA      = "How are we trending?" (over time, with targets)
```

### Step 4.2: View PA Indicators

1. Navigate to **Performance Analytics > Indicators** (or type `pa_indicators.list`)
2. Browse existing indicators:
   - Number of open incidents
   - Mean time to resolve
   - SLA compliance percentage
   - Change success rate

### Step 4.3: Create a Custom Indicator

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | P1 Mean Time to Resolve (MTTR) |
   | Direction | Minimize (lower is better) |
   | Unit | Minutes |
   | Aggregation | Average |
   | Table | Incident |
   | Conditions | Priority = 1 AND State = Resolved |
   | Field | Calendar duration |
   | Frequency | Daily |

3. Click **Submit**

### Step 4.4: Create a PA Dashboard Widget

1. On your ITSM Operations Dashboard, add a PA widget:
   - Widget type: **Performance Analytics > Scorecard**
   - Indicator: P1 Mean Time to Resolve
   - Period: Last 30 days
   - Show trend line: Yes
   - Show target: Yes (e.g., target = 30 minutes)

### Step 4.5: Breakdowns

Breakdowns slice an indicator by a dimension:

1. Navigate to **Performance Analytics > Breakdowns**
2. Create: "Incidents by Assignment Group"
3. Apply to your P1 MTTR indicator
4. Now you can see MTTR for each team individually

---

## Part 5: Executive Dashboard

### Step 5.1: Build an Executive ITSM Dashboard

Create a dashboard: **Executive ITSM Summary**

Layout:
```
+------------------+------------------+------------------+
| Total Open       | P1 Count         | SLA Compliance   |
| Incidents        | (Red if > 0)     | % (Gauge)        |
| [  156  ]        | [   3   ]        | [  94.2%  ]      |
+------------------+------------------+------------------+
| Incident Trend (12 weeks)          | Changes This Month|
| (Line chart with P1,P2,P3 lines)  | (Pie: N/S/E)      |
+------------------------------------+-------------------+
| Top 5 Problem Areas               | MTTR Trend         |
| (Bar: by category)                | (Line: weekly avg) |
+------------------------------------+-------------------+
| Open P1/P2 Incidents (List)                            |
+--------------------------------------------------------+
```

### Step 5.2: Add Data from Multiple Modules

Your executive dashboard should include:
1. Incident metrics (count, MTTR, SLA compliance)
2. Problem metrics (open problems, known errors)
3. Change metrics (success rate, emergency change %)
4. Service request metrics (fulfillment time, backlog)

---

## Part 6: Practice Exercises

### Exercise 1: Monthly ITSM Report

Create a set of reports for a monthly ITSM review:
1. Incidents opened/closed this month (comparison bar chart)
2. MTTR by priority (grouped bar chart)
3. SLA breach analysis (which SLAs breached most?)
4. Top 10 CIs with most incidents (horizontal bar)
5. Change success rate trend (line chart, 6 months)

### Exercise 2: Team Dashboard

Create a dashboard for a specific team (e.g., Platform Engineering):
1. My team's open incidents (filtered by assignment group)
2. Aging incidents (bar chart by age: <1 day, 1-3 days, >3 days)
3. Team workload (incidents per team member)
4. SLA compliance for the team

### Exercise 3: Automated Report Distribution

Schedule these reports for automatic email delivery:
1. Daily: Open P1/P2 list → NOC team
2. Weekly: Incident summary → IT Manager
3. Monthly: Full ITSM report → VP Engineering

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created various report types | Visualize ITSM data for insights |
| Scheduled and shared reports | Automated distribution to stakeholders |
| Built custom dashboards | Single-pane-of-glass view of operations |
| Used Performance Analytics | KPI tracking with trends and targets |
| Created executive dashboards | Management visibility into IT performance |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Report** | A visualization (chart, list, pivot) based on table data |
| **Dashboard** | A collection of widgets providing an operational overview |
| **Widget** | A single component on a dashboard (report, gauge, list, etc.) |
| **Performance Analytics** | Advanced analytics with indicators, trends, and targets |
| **Indicator** | A KPI measured over time (e.g., MTTR, SLA compliance) |
| **Breakdown** | A dimension to slice an indicator (by group, priority, etc.) |
| **Scorecard** | PA widget showing indicator value, trend, and target |

---

## What's Next

In **Lab 20**, you'll learn **REST API & Integrations** -- accessing ServiceNow data via APIs, building integrations, and using Import Sets.
