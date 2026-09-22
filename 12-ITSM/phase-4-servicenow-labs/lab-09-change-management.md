# Lab 09: Change Management

**Level:** Intermediate | **Duration:** 90 minutes | **Prerequisites:** Lab 07-08 completed

---

## Objective

By the end of this lab, you will:
- Create Normal, Standard, and Emergency change requests
- Navigate the full change lifecycle with state transitions
- Configure and use the CAB Workbench
- Use the Change Calendar and conflict detection
- Create Standard Change templates
- Configure risk assessment

---

## Part 1: Create a Normal Change

### Step 1.1: Open the Change Form

1. Navigate to **Change > Create New** (or type `change_request.do`)
2. Select Type: **Normal**

### Step 1.2: Fill in the Change Request

| Field | Value |
|---|---|
| Type | Normal |
| Short description | Upgrade Mail Server from v3.2 to v3.3 |
| Description | Upgrade mail server software from version 3.2 to 3.3 to fix memory leak (ref: PRB0040001). This is a critical upgrade to prevent recurring email service outages. |
| Category | Software |
| Priority | 2 - High |
| Risk | Moderate |
| Impact | 2 - Medium |
| Assignment group | Software |
| Assigned to | (pick a user, e.g., Ravi Kumar) |
| Configuration item | (search for a CI, e.g., "Mail Server" or any CI) |

### Step 1.3: Fill in the Planning Tab

Navigate to the **Planning** tab/section:

| Field | Value |
|---|---|
| Planned start date | (pick a date next week, 2:00 AM) |
| Planned end date | (same date, 4:00 AM) |
| Justification | Fix memory leak causing weekly email outages. 15 incidents in the last month linked to this issue. Vendor advisory SA-2026-045 confirms the fix in v3.3. |
| Implementation plan | 1. Take mail server backup at 2:00 AM<br>2. Stop mail service at 2:15 AM<br>3. Update software package to v3.3<br>4. Run database migration scripts<br>5. Start mail service<br>6. Run smoke tests (send/receive test emails)<br>7. Monitor memory usage for 30 minutes<br>8. Declare success or initiate rollback |
| Rollback plan | 1. Stop mail service<br>2. Restore from backup taken at step 1<br>3. Revert software package to v3.2<br>4. Start mail service<br>5. Verify service restoration<br>6. Re-enable 12-hour restart workaround |
| Test plan | 1. Tested v3.3 in staging environment for 7 days<br>2. No memory leak observed (stable at 1.2GB vs growing pattern in v3.2)<br>3. All email protocols tested: IMAP, SMTP, ActiveSync<br>4. Load tested with 3000 simulated mailboxes |

### Step 1.4: Fill in the Risk Tab

Navigate to the **Risk Assessment** section:

| Question | Answer |
|---|---|
| Has this type of change been done before? | Yes |
| Is there a backout/rollback plan? | Yes |
| Will there be service downtime? | Yes (2 hours maintenance window) |
| Does it affect production? | Yes |
| How many users are affected? | 2,400 email users |
| Is it scheduled in a maintenance window? | Yes |
| Has it been tested? | Yes (staging for 7 days) |

The risk score auto-calculates based on answers.

### Step 1.5: Submit the Change

1. Click **Submit**
2. Note the change number (e.g., CHG0030001)
3. The change state should be **New**

---

## Part 2: Change Lifecycle -- State Transitions

### Step 2.1: State Flow for Normal Changes

```
New --> Assess --> Authorize --> Scheduled --> Implement --> Review --> Closed
                     |                            |
                  (rejected)                   (failed)
                     |                            |
                     v                            v
                  New (rework)              Review --> Closed (Failed)
```

### Step 2.2: Move Through States

**New → Assess:**
1. Open your change CHG0030001
2. Change State to: **Assess**
3. Add work note: "Submitting for assessment. All planning documents attached."
4. Click **Update**

**Assess → Authorize:**
1. Reopen the change
2. Review that all planning fields are complete
3. Change State to: **Authorize**
4. Add work note: "Assessment complete. Risk: Moderate. Submitting for CAB approval."
5. Click **Update**

### Step 2.3: Approval Process

When a change moves to **Authorize**, it typically requires approval:

1. Open the change
2. Scroll to the **Approvers** related list (or **Approvals** tab)
3. If no approvers are auto-added, click **New** in the Approvers list:
   - Approver: Sanjay Manager (the user with `approver_user` role)
   - State: Requested
4. Click **Save**

**Simulate Approval:**
1. Impersonate **Sanjay Manager** (or the approver user)
2. Navigate to **Self-Service > My Approvals** (or type `sysapproval_approver.list`)
3. Find the approval for CHG0030001
4. Open it
5. Click **Approve**
6. Stop impersonating (back to admin)

### Step 2.4: Continue the Lifecycle

**Authorize → Scheduled:**
1. Open the change (it should be approved now)
2. Change State to: **Scheduled**
3. Click **Update**
4. The change now appears on the **Change Calendar**

**Scheduled → Implement:**
1. On the planned start date (or for this exercise, change state now)
2. Change State to: **Implement**
3. Add work note: "Starting implementation. Backup taken at 2:00 AM."
4. Click **Update**

**Implement → Review:**
1. After "implementing" the change:
2. Change State to: **Review**
3. Add work note: "Implementation complete. Mail server upgraded to v3.3. All smoke tests passed. Memory usage stable."
4. Click **Update**

**Review → Closed:**
1. Change State to: **Closed**
2. Set **Close code**: Successful
3. Add close notes: "Change implemented successfully during maintenance window. No incidents reported. Memory monitoring shows stable usage at 1.2GB (previously growing to 8GB+). Workaround scheduled restarts have been removed."
4. Click **Update**

---

## Part 3: Standard Changes

### Step 3.1: Understand Standard Changes

Standard changes are:
- Pre-approved (no CAB review needed)
- Low risk
- Well-documented procedures
- Created from templates

### Step 3.2: Create a Standard Change Template

1. Navigate to **Change > Standard Change Catalog** (or **Change > Standard Change Proposals**)
2. If not available, navigate to **Change > Create New** and set Type to **Standard**
3. Create a change:

   | Field | Value |
   |---|---|
   | Type | Standard |
   | Short description | Add new user to Active Directory |
   | Description | Standard procedure for creating a new Active Directory user account. Pre-approved, low risk. |
   | Category | Software |
   | Risk | Low |
   | Impact | 3 - Low |
   | Assignment group | Service Desk |
   | Implementation plan | 1. Open Active Directory Users and Computers<br>2. Navigate to appropriate OU<br>3. Create user account with standard naming convention<br>4. Add to default security groups<br>5. Set temporary password<br>6. Send credentials to requesting manager |
   | Rollback plan | Disable and delete the created user account |
   | Test plan | Verify user can log in to workstation with temporary password |

4. Click **Submit**

### Step 3.3: Standard Change Lifecycle

Standard changes skip the Authorize (CAB) step:

```
Standard Change: New --> Scheduled --> Implement --> Review --> Closed
                 (no Assess or Authorize -- pre-approved)
```

1. Open the standard change you created
2. Move directly from **New → Scheduled → Implement → Review → Closed**
3. Notice: no approval is required

---

## Part 4: Emergency Changes

### Step 4.1: Create an Emergency Change

Emergency changes are for urgent situations -- a production incident that requires an immediate fix.

1. Navigate to **Change > Create New**
2. Set Type: **Emergency**
3. Fill in:

   | Field | Value |
   |---|---|
   | Type | Emergency |
   | Short description | Emergency hotfix - Payment gateway SSL certificate expired |
   | Description | The SSL certificate on the payment gateway expired at 11:30 PM, causing all payment transactions to fail. An emergency certificate renewal is required immediately. |
   | Category | Network |
   | Risk | High |
   | Impact | 1 - High |
   | Urgency | 1 - High |
   | Assignment group | Network |
   | Justification | Production payment processing is completely down. Revenue loss estimated at $50K per hour. |

4. Click **Submit**

### Step 4.2: Emergency Change Lifecycle

```
Emergency: New --> Authorize --> Implement --> Review --> Closed
           (fast-track: verbal approval, post-implementation CAB review)
```

1. Open the emergency change
2. Add work note: "Verbal approval obtained from VP Engineering (Sanjay) via phone at 11:35 PM"
3. Move State to **Implement**
4. Add work note: "New SSL certificate installed and verified. Payment processing restored at 11:50 PM."
5. Move to **Review**
6. Move to **Closed** with close notes
7. **Important:** An emergency change MUST have a post-implementation review:
   - Was it successful?
   - Could it have been prevented?
   - Should this be a standard change for the future?

---

## Part 5: Change Calendar

### Step 5.1: View the Change Calendar

1. Navigate to **Change > Change Calendar** (or type `change_calendar` in Filter Navigator)
2. You'll see a calendar view showing all scheduled changes:
   ```
   +--------+--------+--------+--------+--------+--------+--------+
   | Mon    | Tue    | Wed    | Thu    | Fri    | Sat    | Sun    |
   +--------+--------+--------+--------+--------+--------+--------+
   |        | CHG001 |        |        |        |        | CHG002 |
   |        | 10-11AM|        |        |        |        | 2-4 AM |
   +--------+--------+--------+--------+--------+--------+--------+
   ```
3. Click on any change to see its details
4. Use this to identify potential scheduling conflicts

### Step 5.2: Conflict Detection

1. Create a new change with a planned start/end date that overlaps with an existing change
2. If both changes affect the same CI, ServiceNow should flag a **conflict**
3. The conflict appears as a warning on the change form

### Step 5.3: Blackout Windows

Blackout windows define periods when no changes are allowed:

1. Navigate to **Change > Change Blackout** (or type `change_blackout.list`)
2. Click **New**
3. Create a blackout:
   | Field | Value |
   |---|---|
   | Name | Holiday Freeze - Year End |
   | Start | Dec 20, 2026 |
   | End | Jan 3, 2027 |
   | Description | No changes during year-end holiday freeze |
4. Click **Submit**
5. Now, if someone schedules a change during this period, they get a warning

---

## Part 6: CAB Workbench

### Step 6.1: Access CAB Workbench

1. Navigate to **Change > CAB Workbench** (or type `cab_workbench`)
2. The CAB Workbench shows:
   - Changes pending approval
   - Upcoming changes
   - Change calendar integration
   - Approval status

### Step 6.2: CAB Review Process

1. As admin, open the CAB Workbench
2. View the list of changes pending CAB review
3. For each change, the CAB can:
   - **Approve** -- proceed with implementation
   - **Reject** -- send back for rework
   - **Request More Info** -- ask the requester for details
   - **Defer** -- postpone to next CAB meeting
4. Practice approving one change from the workbench

---

## Part 7: Practice Exercises

### Exercise 1: End-to-End Normal Change

Create a Normal Change for: "Upgrade database server from PostgreSQL 14 to PostgreSQL 16"
1. Fill in ALL tabs: Planning, Risk, Schedule
2. Add an approver
3. Get it approved (impersonate the approver)
4. Walk it through all states: New → Assess → Authorize → Scheduled → Implement → Review → Closed
5. Close as Successful

### Exercise 2: Failed Change

1. Create a Normal Change for: "Migrate application to new server"
2. Walk it through to the Implement state
3. Simulate a failure: during implementation, something goes wrong
4. Execute the rollback plan (document in work notes)
5. Move to Review
6. Close as **Unsuccessful** with detailed notes on what went wrong

### Exercise 3: Change Analysis

Create a set of 5-6 changes with different types and states:
- 2 Normal (1 approved, 1 pending)
- 2 Standard (both closed)
- 1 Emergency (closed)
- 1 Normal (rejected)

This data will be useful for the Reporting lab (Lab 19).

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created Normal changes with full planning | Structured process reduces change failure |
| Walked through complete lifecycle | Understanding state flow is critical for operations |
| Created Standard change templates | Pre-approved changes speed up routine operations |
| Created Emergency changes | Fast-track process for critical production issues |
| Used Change Calendar | Prevents scheduling conflicts |
| Used CAB Workbench | Centralized approval management |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Normal Change** | Requires full assessment and CAB approval |
| **Standard Change** | Pre-approved from a template, low risk |
| **Emergency Change** | Fast-track for critical situations, post-approval |
| **CAB** | Change Advisory Board -- reviews and approves changes |
| **Change Calendar** | Visual view of all scheduled changes |
| **Blackout Window** | Period when no changes are permitted |
| **Conflict Detection** | Auto-detection of overlapping changes on same CI |
| **Risk Assessment** | Questionnaire that auto-calculates change risk score |

---

## What's Next

In **Lab 10**, you'll build a **Service Catalog** -- creating catalog items, variables, approval workflows, and tracking requests through REQ/RITM/SCTASK.
