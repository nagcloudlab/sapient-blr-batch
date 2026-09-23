# Lab 15: Flow Designer & Workflows

**Level:** Advanced | **Duration:** 90 minutes | **Prerequisites:** Lab 07-14 completed

---

## Objective

By the end of this lab, you will:
- Understand Flow Designer vs legacy Workflow Editor
- Create flows with triggers, actions, and conditions
- Build an approval flow for service catalog requests
- Create subflows for reusable logic
- Use Flow Designer actions (create record, update record, send notification)

---

## Part 1: Introduction to Flow Designer

### Step 1.1: Open Flow Designer

1. Navigate to **Process Automation > Flow Designer** (or type `flow_designer` in Filter Navigator)
2. Flow Designer opens in a new tab/window
3. Browse existing flows to see examples

### Step 1.2: Flow Designer vs Workflow Editor

| Feature | Flow Designer (Modern) | Workflow Editor (Legacy) |
|---|---|---|
| Interface | Visual, drag-and-drop | Visual, drag-and-drop |
| Scripting | Optional (low-code) | Often required |
| Reusability | Subflows, actions, spokes | Activities |
| Recommended | Yes -- current standard | Being replaced |
| Where | Process Automation > Flow Designer | Workflow > Workflow Editor |

**Use Flow Designer for all new automation.**

### Step 1.3: Key Components

```
Flow
  ├── Trigger     (WHEN does it start?)
  ├── Actions     (WHAT does it do?)
  ├── Conditions  (IF this, THEN that)
  └── Flow Logic  (for each, wait, do until)

Subflow = A reusable mini-flow called by other flows
Action  = A single operation (create record, send email, update field)
Spoke   = A collection of actions for an integration (Slack, Teams, etc.)
```

---

## Part 2: Create Your First Flow

### Step 2.1: Build an Incident Auto-Assignment Flow

This flow will auto-assign P1 incidents to a specific group.

1. In Flow Designer, click **New > Flow**
2. Fill in:
   | Field | Value |
   |---|---|
   | Flow name | P1 Auto-Assignment |
   | Description | Automatically assigns P1 incidents to the Critical Response team |
   | Application | Global |
   | Run as | System User |

3. Click **Submit**

### Step 2.2: Add a Trigger

1. Click **Add a trigger**
2. Select **Record > Created**
3. Configure:
   | Field | Value |
   |---|---|
   | Table | Incident [incident] |
   | Condition | Priority is 1 - Critical |
4. This flow will trigger whenever a P1 incident is created

### Step 2.3: Add Actions

**Action 1: Update the Incident**

1. Click **Add an Action, Flow Logic, or Subflow**
2. Select **Action > ServiceNow Core > Update Record**
3. Configure:
   | Field | Value |
   |---|---|
   | Record | Trigger > Incident Record (drag from the data panel) |
   | Fields to update | |
   | Assignment group | Network (or your critical response group) |
   | Work notes | Auto-assigned to Critical Response team by Flow Designer (P1 auto-assignment rule) |

**Action 2: Send Email Notification**

1. Click the **+** to add another action after the update
2. Select **Action > ServiceNow Core > Send Email**
3. Configure:
   | Field | Value |
   |---|---|
   | To | (assignment group manager email or a specific email) |
   | Subject | `[P1 AUTO-ASSIGNED] ` + Trigger Record > Number + `: ` + Trigger Record > Short description |
   | Body | A P1 incident has been auto-assigned to your team. Please acknowledge immediately. |

### Step 2.4: Activate and Test

1. Click **Save** (top-right)
2. Click **Activate** (makes the flow live)
3. **Test:** Create a new P1 incident
4. After submit, check:
   - Is the incident assigned to the correct group?
   - Was the work note added?
   - Was the email sent? (Check System Mailboxes > Outbound > Sent)

---

## Part 3: Build an Approval Flow

### Step 3.1: Create Catalog Item Approval Flow

1. In Flow Designer, click **New > Flow**
2. Name: `Database Access Approval Flow`
3. Click **Submit**

### Step 3.2: Add Trigger

1. Click **Add a trigger**
2. Select **Application > Service Catalog > Catalog Item Requested**
3. Configure:
   | Field | Value |
   |---|---|
   | Catalog Item | Database Access Request (from Lab 10) |

### Step 3.3: Add Approval Action

1. Click **Add an Action**
2. Select **Flow Logic > Ask for Approval**
3. Configure:

   **Approval type:** Anyone Approves (or Everyone Must Approve)

   **Approvers:**
   | Rule | Value |
   |---|---|
   | Approval type | Group |
   | Group | IT Management |

   Or for sequential approval:
   ```
   Step 1: Manager approval (requested_for's manager)
   Step 2: DBA team lead approval
   ```

### Step 3.4: Add Conditional Logic

After the approval step:

1. Click **Add Flow Logic > If**
2. Condition: Approval = **Approved**
3. **Then branch (Approved):**
   - Action: **Update Record** (update the RITM stage to "Fulfillment")
   - Action: **Create Task** (create SCTASK for DBA team)
   - Action: **Send Email** (notify requester of approval)

4. Click **Add Flow Logic > Else**
5. **Else branch (Rejected):**
   - Action: **Update Record** (update RITM stage to "Closed Incomplete")
   - Action: **Send Email** (notify requester of rejection with reason)

### Step 3.5: Complete Flow Diagram

```
Trigger: Catalog Item "Database Access Request" requested
  |
  v
Ask for Approval (Manager + DBA Lead)
  |
  ├── IF Approved:
  |     ├── Update RITM: stage = Fulfillment
  |     ├── Create SCTASK: assigned to DBA team
  |     └── Send Email: "Your request has been approved"
  |
  └── ELSE (Rejected):
        ├── Update RITM: stage = Closed Incomplete
        └── Send Email: "Your request has been rejected"
```

### Step 3.6: Save, Activate, and Test

1. **Save** the flow
2. **Activate** it
3. Go to the Service Catalog and order a "Database Access Request"
4. Impersonate the approver -- approve or reject
5. Verify the correct branch executes

---

## Part 4: Flow Logic Elements

### Step 4.1: For Each Loop

Process multiple records:

1. Add **Flow Logic > For Each**
2. Configure:
   - Record list: Use a **Look Up Records** action first to get a list
3. Inside the loop, add actions that execute for each record

Example: "For each open P1 incident, send a reminder email to the assigned user"

```
Look Up Records: incident where priority=1 AND state=In Progress
  |
  v
For Each incident:
  └── Send Email to incident.assigned_to: "Reminder: P1 incident still open"
```

### Step 4.2: Wait For Condition

Pause the flow until a condition is met:

1. Add **Flow Logic > Wait for Condition**
2. Configure:
   - Table: Incident
   - Condition: State changes to Resolved
3. The flow pauses until the condition is satisfied, then continues

Example: After creating a change, wait until it's approved, then proceed.

### Step 4.3: Do Until

Loop until a condition is met:

1. Add **Flow Logic > Do Until**
2. Configure the exit condition
3. Add actions inside the loop

### Step 4.4: Parallel Flow

Run multiple action branches simultaneously:

1. Add **Flow Logic > Parallel**
2. Add actions to each parallel branch
3. All branches run at the same time

---

## Part 5: Subflows

### Step 5.1: Create a Reusable Subflow

Subflows are reusable pieces of logic that can be called from multiple flows.

1. In Flow Designer, click **New > Subflow**
2. Name: `Send Escalation Notification`
3. Click **Submit**

### Step 5.2: Define Inputs

1. Click **Inputs** in the subflow
2. Add input variables:
   | Name | Type | Mandatory |
   |---|---|---|
   | incident_record | Reference (Incident) | Yes |
   | escalation_level | String | Yes |
   | notify_user | Reference (User) | Yes |

### Step 5.3: Add Subflow Actions

1. **Action: Send Email**
   - To: `notify_user.email`
   - Subject: `[ESCALATION - ${escalation_level}] ${incident_record.number}: ${incident_record.short_description}`
   - Body: Escalation notification with incident details

2. **Action: Update Record**
   - Record: incident_record
   - Work notes: `Escalated to ${escalation_level}. Notification sent to ${notify_user.name}.`

3. **Save** and **Publish** the subflow

### Step 5.4: Call Subflow from a Flow

1. Open your "P1 Auto-Assignment" flow
2. Add an action: **Subflow > Send Escalation Notification**
3. Map the inputs:
   - incident_record: Trigger record
   - escalation_level: "L2"
   - notify_user: (the group manager)

---

## Part 6: Flow Execution and Debugging

### Step 6.1: View Flow Execution History

1. In Flow Designer, click **Executions** (top navigation)
2. You'll see a list of all flow executions
3. Click any execution to see:
   - Which trigger fired
   - Each action that ran
   - Success or failure status
   - Runtime data (values at each step)

### Step 6.2: Debug a Flow

1. Open a flow
2. Click **Test** (top-right)
3. Provide test input (e.g., select an incident record)
4. Click **Run Test**
5. The flow executes and shows step-by-step results
6. Check each step for:
   - Did it execute?
   - What values were used?
   - Any errors?

### Step 6.3: Common Flow Errors

| Error | Cause | Fix |
|---|---|---|
| "No records found" | Look Up Records returned empty | Check query conditions |
| "Approval not configured" | Missing approver group | Add approval rules |
| "Email not sent" | Email property disabled | Check sys_properties for email settings |
| Flow doesn't trigger | Trigger condition not met | Verify condition matches test data |
| Flow deactivated | Someone deactivated it | Check flow status, reactivate |

---

## Part 7: Practice Exercises

### Exercise 1: Change Approval Flow

Build a flow:
- Trigger: Change Request created with Type = Normal
- Actions:
  1. If Risk = High, require 2 approvals (Manager + VP)
  2. If Risk = Low or Medium, require 1 approval (Manager only)
  3. On approval: update state to Scheduled, send notification
  4. On rejection: update state to Canceled, send notification with reason

### Exercise 2: Incident Auto-Closure Flow

Build a flow:
- Trigger: Incident updated
- Condition: State = Resolved AND Resolved more than 3 days ago
- Actions:
  1. Update state to Closed
  2. Add close notes: "Auto-closed after 3 days in Resolved state"
  3. Send notification to caller

### Exercise 3: Onboarding Subflow

Create a subflow: "New Employee IT Setup"
- Inputs: employee_name, department, role
- Actions:
  1. Create catalog request for laptop
  2. Create catalog request for email account
  3. Create catalog request for VPN access
  4. Send welcome email to employee's manager

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created flows with triggers and actions | Automated business processes without code |
| Built approval flows | Governance and authorization automation |
| Used conditional logic | Dynamic behavior based on data |
| Created reusable subflows | DRY principle -- don't repeat yourself |
| Debugged flow executions | Troubleshooting and verification |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **Flow** | An automated process with a trigger, actions, and logic |
| **Trigger** | The event that starts a flow (record created, updated, scheduled, etc.) |
| **Action** | A single operation in a flow (create record, send email, etc.) |
| **Flow Logic** | Control structures: If/Else, For Each, Wait, Parallel |
| **Subflow** | A reusable mini-flow that can be called from other flows |
| **Spoke** | A collection of actions for integrating with external services |
| **Execution** | A single run of a flow, with full audit trail |

---

## What's Next

In **Lab 16**, you'll dive into **Business Rules** -- server-side scripts that execute when records are created, updated, or deleted.
