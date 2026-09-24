# Lab 13: Incident Management — Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-13-incident-management.md`

---

## Pre-check

- [ ] Labs 01-12 done (users, groups, CIs exist)
- [ ] Groups exist: Service Desk, Network, Hardware, Software, Platform Engineering
- [ ] Logged into PDI as admin

---

## Step 1: Create Incident #1 — P3 (Medium/Medium)

Navigate: **Incident > Create New** (or type `incident.do`)

| Field | Value |
|-------|-------|
| Caller | Abel Tuter |
| Category | Software |
| Subcategory | Email |
| Short description | Unable to access email from mobile device |
| Description | User reports email on iPhone stopped syncing after latest update. Tried restarting. All other apps work fine. |
| Impact | 2 - Medium |
| Urgency | 2 - Medium |
| Assignment group | Service Desk |
| Assigned to | Beth Anglin |
| Configuration item | (leave blank or select any CI) |

> Before clicking Submit, observe: Priority auto-calculated as **3 - Moderate**. State defaults to **New**.

Click **Submit**. Record number: INC________

---

## Step 2: Create Incident #2 — P1 (High/High)

Navigate: **Incident > Create New**

| Field | Value |
|-------|-------|
| Caller | David Loo |
| Category | Network |
| Subcategory | VPN |
| Short description | VPN service down - all remote users affected |
| Description | VPN gateway unreachable. 500+ remote users cannot connect. Started at 9:00 AM. |
| Impact | 1 - High |
| Urgency | 1 - High |
| Assignment group | Network |
| Assigned to | (leave empty) |
| Configuration item | UPI Production LB (if available) |

Click **Submit**. Priority = **1 - Critical**. Record number: INC________

---

## Step 3: Create Incident #3 — P4 (Low/Medium)

Navigate: **Incident > Create New**

| Field | Value |
|-------|-------|
| Caller | Fred Luddy |
| Category | Hardware |
| Short description | Laptop screen flickering |
| Description | User reports screen flickers intermittently during video calls. Started 2 days ago. |
| Impact | 3 - Low |
| Urgency | 2 - Medium |
| Assignment group | Hardware |
| Configuration item | (leave blank) |

Click **Submit**. Priority = **4 - Low**. Record number: INC________

---

## Step 4: Create Incident #4 — P4 (Medium/Low)

Navigate: **Incident > Create New**

| Field | Value |
|-------|-------|
| Caller | Abel Tuter |
| Category | Software |
| Short description | Cannot print to network printer |
| Description | Print jobs sent to 3rd floor network printer queue but never print. Other printers work. |
| Impact | 2 - Medium |
| Urgency | 3 - Low |
| Assignment group | Service Desk |
| Configuration item | (leave blank) |

Click **Submit**. Priority = **4 - Low**. Record number: INC________

---

## Step 5: Create Incident #5 — P2 (High/Medium)

Navigate: **Incident > Create New**

| Field | Value |
|-------|-------|
| Caller | Beth Anglin |
| Category | Network |
| Short description | Core switch failure affecting Building 2 network |
| Description | Core network switch in Building 2 MDF failed. All users in Building 2 have no network access. Approximately 200 users affected. |
| Impact | 1 - High |
| Urgency | 2 - Medium |
| Assignment group | Network |
| Configuration item | (leave blank) |

Click **Submit**. Priority = **2 - High**. Record number: INC________

---

## Step 6: Create Incident #6 — P5 (Low/Low)

Navigate: **Incident > Create New**

| Field | Value |
|-------|-------|
| Caller | Fred Luddy |
| Category | Hardware |
| Short description | Request for ergonomic keyboard replacement |
| Description | User requests replacement of standard keyboard with ergonomic model. No urgency, current keyboard works. |
| Impact | 3 - Low |
| Urgency | 3 - Low |
| Assignment group | Service Desk |
| Configuration item | (leave blank) |

Click **Submit**. Priority = **5 - Planning**. Record number: INC________

---

## Checkpoint

Navigate: `incident.list` > sort by **Created** descending.

Expected: **6 new incidents** covering all priorities:

| Priority | Count | Incident |
|----------|-------|----------|
| P1 - Critical | 1 | VPN service down |
| P2 - High | 1 | Core switch failure |
| P3 - Moderate | 1 | Email access |
| P4 - Low | 2 | Laptop screen, Printer |
| P5 - Planning | 1 | Keyboard replacement |

If any are missing, go back and create them.

---

## Priority Matrix Reference

```
                    Impact
                1-High  2-Medium  3-Low
Urgency  1-High    1        2        3
         2-Medium  2        3        4
         3-Low     3        4        5
```

---

## Step 7: Full Incident Lifecycle — VPN Incident (P1)

Open the P1 VPN incident (from Step 2).

### 7a: New --> In Progress

1. Set **Assigned to**: Beth Anglin (or any ITIL user)
2. Change **State** to: **In Progress**
3. Add **Work note**: "Investigating VPN gateway. Checking firewall logs and VPN concentrator status."
4. Click **Update**

### 7b: In Progress (add investigation notes)

1. Reopen the incident
2. Add **Work note**: "Root cause identified - VPN concentrator certificate expired. Renewing certificate now."
3. Click **Update**

### 7c: In Progress --> On Hold

1. Reopen the incident
2. Change **State** to: **On Hold**
3. Set **On hold reason**: Awaiting Vendor
4. Add **Work note**: "Waiting for certificate authority to issue new SSL certificate. ETA 2 hours."
5. Click **Update**

### 7d: On Hold --> In Progress

1. Reopen the incident
2. Change **State** to: **In Progress**
3. Add **Work note**: "New certificate received from CA. Installing on VPN concentrator now."
4. Click **Update**

### 7e: In Progress --> Resolved

1. Reopen the incident
2. Change **State** to: **Resolved**
3. Fill in:
   - **Resolution code**: Solved (Permanently)
   - **Resolution notes**: "VPN concentrator SSL certificate renewed and installed. VPN service restored. All remote users can connect. Monitoring for stability."
4. Add **Additional comments** (customer-visible): "The VPN service has been restored. Please try connecting again."
5. Click **Update**

### 7f: Resolved --> Closed

1. Reopen the incident
2. Change **State** to: **Closed**
3. Fill in:
   - **Close code**: Solved (Permanently)
   - **Close notes**: "Confirmed VPN stable for 24 hours. No further reports from users."
4. Click **Update**

---

## Checkpoint

Open the closed VPN incident. Scroll to **Activity Stream**. Verify the full timeline:

```
State: New --> In Progress
Work note: "Investigating VPN gateway..."
Work note: "Root cause identified..."
State: In Progress --> On Hold (Awaiting Vendor)
Work note: "Waiting for certificate authority..."
State: On Hold --> In Progress
Work note: "New certificate received..."
State: In Progress --> Resolved
Resolution notes: "VPN concentrator SSL certificate..."
Additional comments: "The VPN service has been restored..."
State: Resolved --> Closed
Close notes: "Confirmed VPN stable..."
```

All state transitions and notes visible? This is the complete audit trail.

---

## Step 8: Verify SLA Auto-Attachment

1. Open any P1 incident (VPN incident)
2. Scroll down to **Task SLA** related list (or look for SLA-related tabs)
   - If not visible: right-click header > **Configure > Related Lists** > add **Task SLA** > Save
3. Check if any SLA records are attached:

| Field to Look For | What It Shows |
|-------------------|--------------|
| SLA Definition | Which SLA applies (e.g., Priority 1 Resolution) |
| Stage | In Progress, Paused, or Completed |
| Has breached | Whether the SLA was breached (true/false) |
| Business elapsed | Time counted toward SLA |

> Note: SLAs auto-attach based on SLA Definitions configured in your PDI. If no Task SLA records appear, your PDI may not have SLA definitions active for incidents.

---

## Step 9: Check Task SLA Records

Navigate: `task_sla.list`

1. Filter: **Task** | **is** | your P1 VPN incident number
2. Review the SLA records:
   - **Start time**: When the SLA clock started
   - **Planned end time**: When the SLA would breach
   - **Actual end time**: When the task reached the target stage
   - **Has breached**: true/false
3. If no records exist, navigate to **SLA > SLA Definitions** (`sla.list`) and verify definitions are active

---

## Step 10: Escalation Practice

### 10a: Manual Escalation (Reassignment)

1. Open the printer incident (Step 4)
2. Change **Assignment group** to: **Network**
3. Add **Work note**: "Escalating to Network team — this appears to be a network printer connectivity issue, not a software problem."
4. Click **Update**
5. Check: **Reassignment count** field should show **1**

### 10b: Functional Escalation (L1 --> L2 --> L3)

Create a new incident:

| Field | Value |
|-------|-------|
| Short description | Application timeout errors on internal portal |
| Category | Software |
| Impact | 2 - Medium |
| Urgency | 1 - High |
| Assignment group | Service Desk |

Click **Submit**.

**L1 (Service Desk):**
1. Open the incident
2. Add work note: "Basic troubleshooting done. Cleared cache, verified network. Issue persists. Escalating to L2."
3. Change **Assignment group** to: **Software**
4. Click **Update**

**L2 (Software):**
1. Reopen the incident
2. Add work note: "App logs show database connection pool exhaustion. This is a DB issue. Escalating to L3."
3. Change **Assignment group** to: **Database** (create group if needed via `sys_user_group.do`)
4. Click **Update**

**L3 (Database):**
1. Reopen the incident
2. Add work note: "Found deadlock in transaction processing. Killed blocking sessions. Increased connection pool."
3. Change **State** to: **Resolved**
4. Resolution code: Solved (Permanently)
5. Resolution notes: "Database deadlock resolved. Connection pool increased from 50 to 100."
6. Click **Update**

---

## Quick Verification Checklist

- [ ] 6 incidents created covering P1 through P5
- [ ] VPN incident walked through full lifecycle: New > In Progress > On Hold > In Progress > Resolved > Closed
- [ ] Activity stream shows complete audit trail with all state transitions
- [ ] Priority auto-calculated correctly from Impact x Urgency for all 6 incidents
- [ ] Task SLA related list checked on P1 incident
- [ ] Manual escalation done (reassignment count incremented)
- [ ] L1 > L2 > L3 functional escalation completed on portal timeout incident
- [ ] On Hold reason set to "Awaiting Vendor" during hold state

---

## Shortcut: Background Script

If running behind, go to **System Definition > Scripts - Background** and run the script from the Appendix in `lab-13-incident-management.md`. Creates all incidents, assignment rules, and templates. The lifecycle walkthrough (Step 7), SLA check (Steps 8-9), and escalation practice (Step 10) must be done manually through the UI.

---

*For priority matrix theory, incident templates, reporting exercises, and background script code, see the full lab doc.*
