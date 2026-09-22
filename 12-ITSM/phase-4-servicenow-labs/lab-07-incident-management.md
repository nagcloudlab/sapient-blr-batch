# Lab 07: Incident Management

**Level:** Intermediate | **Duration:** 90 minutes | **Prerequisites:** Lab 01-06 completed

---

## Objective

By the end of this lab, you will:
- Create incidents through multiple channels
- Manage the full incident lifecycle (New → In Progress → Resolved → Closed)
- Configure the priority matrix (Impact x Urgency)
- Assign and escalate incidents
- Link incidents to CIs, problems, and knowledge articles
- Use incident templates

---

## Part 1: Create Your First Incident

### Step 1.1: Create via the Form

1. Navigate to **Incident > Create New**
2. Fill in the form:

   | Field | Value |
   |---|---|
   | Caller | Abel Tuter (search and select) |
   | Category | Software |
   | Subcategory | Email |
   | Short description | Unable to access email from mobile device |
   | Description | User reports that email on iPhone has stopped syncing after latest update. Tried restarting the device. All other apps work fine. |
   | Impact | 2 - Medium |
   | Urgency | 2 - Medium |
   | Assignment group | Service Desk |
   | Assigned to | Beth Anglin |

3. **Before clicking Submit**, observe:
   - **Priority** is auto-calculated from Impact x Urgency
   - **State** defaults to "New"
   - **Number** will be auto-assigned on submit

4. Click **Submit**
5. Note the incident number (e.g., INC0010001)

### Step 1.2: The Priority Matrix

Priority is calculated automatically:

```
                    Impact
                1-High  2-Medium  3-Low
Urgency  1-High    1        2        3
         2-Medium  2        3        4
         3-Low     3        4        5

Priority values:
  1 = Critical    (Impact:High + Urgency:High)
  2 = High        (High+Medium or Medium+High)
  3 = Moderate    (High+Low, Medium+Medium, Low+High)
  4 = Low         (Medium+Low, Low+Medium)
  5 = Planning    (Low+Low)
```

### Step 1.3: Create a P1 Critical Incident

1. Navigate to **Incident > Create New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Caller | David Loo (or any demo user) |
   | Category | Network |
   | Subcategory | VPN |
   | Short description | VPN service down - all remote users affected |
   | Description | VPN gateway is unreachable. Over 500 remote users cannot connect. Started at 9:00 AM. |
   | Impact | 1 - High |
   | Urgency | 1 - High |
   | Assignment group | Network |
   | Assigned to | (leave empty for now) |

3. Click **Submit**
4. Note: Priority = **1 - Critical** (auto-calculated)
5. Record the number: ___________

### Step 1.4: Create More Incidents

Create these additional incidents for practice:

| # | Caller | Category | Short Description | Impact | Urgency | Group |
|---|---|---|---|---|---|---|
| 3 | Fred Luddy | Hardware | Laptop screen flickering | 3-Low | 2-Med | Hardware |
| 4 | Abel Tuter | Software | Cannot print to network printer | 2-Med | 3-Low | Service Desk |
| 5 | Beth Anglin | Network | WiFi keeps disconnecting in Bldg 2 | 2-Med | 2-Med | Network |

---

## Part 2: Incident Lifecycle

### Step 2.1: Work Through the Lifecycle

Open the P1 incident you created (VPN service down).

**State 1: New → In Progress**
1. Open the incident
2. Change **Assigned to**: select a user (e.g., ITIL User or Beth Anglin)
3. Change **State** to: **In Progress**
4. Add a **Work note**: "Investigating VPN gateway. Checking firewall logs and VPN concentrator status."
5. Click **Update**

**State 2: In Progress (working on it)**
1. Reopen the incident
2. Add another work note: "Root cause identified - VPN concentrator certificate expired. Renewing certificate now."
3. Click **Update**

**State 3: In Progress → Resolved**
1. Reopen the incident
2. Change **State** to: **Resolved**
3. Fill in Resolution fields:
   - **Resolution code**: Solved (Permanently)
   - **Resolution notes**: "VPN concentrator SSL certificate had expired. Renewed the certificate and restarted the VPN service. All remote users can now connect. Monitoring for stability."
4. Add **Additional comments** (customer-visible): "The VPN service has been restored. Please try connecting again. Contact us if you still experience issues."
5. Click **Update**

**State 4: Resolved → Closed**
1. Reopen the incident
2. Change **State** to: **Closed**
3. Fill in:
   - **Close code**: Solved (Permanently)
   - **Close notes**: "Confirmed VPN is stable. No further reports from users."
4. Click **Update**

### Step 2.2: Review the Activity Stream

1. Open the closed incident
2. Scroll to the **Activity Stream**
3. Review the full timeline:
   ```
   [timestamp] State changed from New to In Progress
   [timestamp] Work note: "Investigating VPN gateway..."
   [timestamp] Work note: "Root cause identified..."
   [timestamp] State changed from In Progress to Resolved
   [timestamp] Resolution notes: "VPN concentrator SSL..."
   [timestamp] Additional comments: "The VPN service has been restored..."
   [timestamp] State changed from Resolved to Closed
   [timestamp] Close notes: "Confirmed VPN is stable..."
   ```
4. This is the complete audit trail -- essential for compliance and review

---

## Part 3: Assignment and Escalation

### Step 3.1: Assignment Rules

Assignment rules auto-assign incidents based on conditions.

1. Navigate to **System Policy > Rules > Assignment** (or type `sysrule_assignment.list`)
2. Click **New**
3. Create a rule:

   | Field | Value |
   |---|---|
   | Name | Auto-assign Network incidents |
   | Table | Incident [incident] |
   | Active | Checked |
   | Conditions | Category is Network |
   | Group | Network |

4. Click **Submit**
5. **Test it:** Create a new incident with Category = Network
6. After submit, open it -- it should be auto-assigned to the Network group

### Step 3.2: Manual Escalation

1. Open an incident that's assigned to Service Desk
2. Change **Assignment group** to: **Network** (escalating to a different team)
3. Add a work note: "Escalating to Network team - this requires network infrastructure expertise"
4. Click **Update**
5. Note: The **Reassignment count** field increments automatically

### Step 3.3: Functional Escalation (L1 → L2 → L3)

Simulate a tiered support escalation:

1. Create a new incident:
   - Short description: "Application timeout errors on internal portal"
   - Assignment group: **Service Desk** (L1)
   - Priority: 2 - High

2. As L1 (Service Desk):
   - Add work note: "Attempted basic troubleshooting. Cleared user cache, verified network. Issue persists. Escalating to L2."
   - Change Assignment group to: **Software** (L2)
   - Click **Update**

3. As L2 (Software):
   - Add work note: "Application logs show database connection pool exhaustion. This is a database issue. Escalating to L3."
   - Change Assignment group to: **Database** (L3, create this group if needed)
   - Click **Update**

4. As L3 (Database):
   - Add work note: "Found deadlock in transaction processing. Killed blocking sessions. Increased connection pool. Issue resolved."
   - Change State to: **Resolved**
   - Add resolution notes
   - Click **Update**

---

## Part 4: Linking Incidents to Other Records

### Step 4.1: Link to a Configuration Item (CI)

1. Open any incident
2. Find the **Configuration item** field (cmdb_ci)
3. Click the magnifying glass and search for a CI (e.g., "Web Server" or any available CI)
4. Select the CI
5. Click **Update**
6. Now this incident is linked to a specific infrastructure component

### Step 4.2: Link to a Problem

1. Open an incident
2. Find the **Problem** field (or look in Related Records tab)
3. Search for an existing problem or create a new one first
4. Link the incident to the problem
5. This creates a relationship: "This incident was caused by this problem"

### Step 4.3: Create a Child Incident

1. Open any incident
2. Look for a **Create Child Incident** button or related link
3. Click it -- a new incident form opens pre-filled with the parent reference
4. Fill in additional details
5. Submit
6. Back on the parent incident, check the **Child Incidents** related list

### Step 4.4: Link to a Knowledge Article

1. Open an incident
2. Look for a **Knowledge** section or search icon
3. Search for relevant KB articles
4. If you find one, attach it to the incident
5. This helps future agents who encounter the same issue

---

## Part 5: Incident Templates

### Step 5.1: Create an Incident Template

1. Navigate to **Incident > Create New**
2. Fill in common fields for a recurring incident type:

   | Field | Value |
   |---|---|
   | Category | Network |
   | Subcategory | VPN |
   | Impact | 1 - High |
   | Urgency | 1 - High |
   | Assignment group | Network |
   | Short description | VPN service disruption - [LOCATION] |

3. Right-click the form header
4. Select **Save as Template** (or **Insert and Stay** > then Template)
5. Or navigate to **System Templates > Templates** (`sys_template.list`)
6. Click **New**:
   - Name: `VPN Outage P1`
   - Table: Incident
   - Template fields: set the pre-filled values
7. Click **Submit**

### Step 5.2: Use the Template

1. Navigate to **Incident > Create New**
2. Look for a **Template** bar or icon at the top of the form
3. Search for "VPN Outage P1"
4. Select it -- the form auto-fills with the template values
5. Fill in the remaining fields (caller, specific details)
6. Click **Submit**

---

## Part 6: Incident Reports (Quick Look)

### Step 6.1: View Incident Overview

1. Navigate to **Incident > Overview** (or type `incident_overview` in Filter Navigator)
2. If an overview page exists, you'll see:
   - Open incidents by priority
   - Incidents opened today
   - Average resolution time
   - Top categories

### Step 6.2: Quick Count

1. Navigate to **Incident > All**
2. Build filters and note the record count:
   - All open incidents: ___
   - Open P1 incidents: ___
   - Unassigned incidents: ___
   - Incidents opened this week: ___

---

## Part 7: Practice Exercises

### Exercise 1: Full Lifecycle

Create an incident and take it through every state:
1. New → In Progress → On Hold → In Progress → Resolved → Closed
2. At each state change, add appropriate work notes
3. When putting On Hold, set the **On hold reason** (e.g., "Awaiting Vendor")
4. Review the Activity Stream at the end -- it should show the complete history

### Exercise 2: Major Incident Simulation

1. Create a P1 incident: "Payment processing system down - all transactions failing"
2. Create 3 child incidents:
   - "Payment gateway not responding"
   - "Database replication lag detected"
   - "Load balancer health check failing"
3. Assign each child to a different group
4. Resolve child incidents one by one
5. Resolve the parent incident last
6. Add a "Cause" reference linking to a change request (if any exist)

### Exercise 3: Reporting Data

Create at least 10 incidents with varied:
- Priorities (mix of P1, P2, P3, P4)
- Categories (Network, Software, Hardware)
- Assignment groups
- States (some Open, some In Progress, some Resolved)

This data will be used in later labs for reporting and dashboards.

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created incidents through forms | Standard incident creation process |
| Managed full lifecycle | New → In Progress → Resolved → Closed |
| Configured priority matrix | Impact x Urgency = consistent prioritization |
| Escalated incidents (L1→L2→L3) | Functional escalation when expertise needed |
| Linked incidents to CIs, problems, KB | Relationships enable root cause analysis |
| Created templates | Speed and consistency for recurring incident types |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Incident** | An unplanned interruption or reduction in quality of an IT service |
| **Priority Matrix** | Impact x Urgency determines priority (auto-calculated) |
| **Lifecycle States** | New → In Progress → On Hold → Resolved → Closed |
| **Escalation** | Moving an incident to a higher-skill team (L1→L2→L3) |
| **Child Incident** | A sub-incident linked to a parent (for major incidents) |
| **Assignment Rule** | Auto-assigns incidents based on conditions |
| **Template** | Pre-filled form for recurring incident types |

---

## What's Next

In **Lab 08**, you'll work with **Problem Management** -- creating problems from recurring incidents, performing root cause analysis, and documenting known errors.
