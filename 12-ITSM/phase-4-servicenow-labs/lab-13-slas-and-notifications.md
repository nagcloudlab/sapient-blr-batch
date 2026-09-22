# Lab 13: SLAs & Notifications

**Level:** Advanced | **Duration:** 90 minutes | **Prerequisites:** Lab 07-12 completed

---

## Objective

By the end of this lab, you will:
- Create SLA definitions with start, pause, and stop conditions
- Configure schedules (business hours, 24x7, holidays)
- Set up SLA breach triggers and escalation actions
- Configure email notifications with variable substitution
- Build an end-to-end automated escalation flow

---

## Part 1: Create Schedules

### Step 1.1: View Existing Schedules

1. Navigate to **System Scheduler > Schedules** (or type `cmn_schedule.list`)
2. Browse existing schedules (e.g., "8-5 weekdays", "24x7")

### Step 1.2: Create a Business Hours Schedule

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | Business Hours India |
   | Time zone | Asia/Kolkata |
   | Type | (leave default or select "Schedule") |

3. Click **Submit**
4. Reopen the schedule
5. In the **Schedule Entries** related list, click **New**:

   | Field | Value |
   |---|---|
   | Name | Weekday Hours |
   | Type | Time range |
   | All day | Unchecked |
   | Start time | 09:00:00 |
   | End time | 18:00:00 |
   | Days of week | Monday, Tuesday, Wednesday, Thursday, Friday |
   | Repeat type | Weekly |

6. Click **Submit**

### Step 1.3: Add Holiday Exclusions

1. On the "Business Hours India" schedule, find the **Child Schedules** or **Exclusions** related list
2. Create a new exclusion schedule: "India Holidays 2026"
3. Add holiday entries:

   | Holiday | Date | Type |
   |---|---|---|
   | Republic Day | Jan 26, 2026 | Exclude |
   | Holi | Mar 17, 2026 | Exclude |
   | Independence Day | Aug 15, 2026 | Exclude |
   | Gandhi Jayanti | Oct 2, 2026 | Exclude |
   | Diwali | Oct 20-21, 2026 | Exclude |
   | Christmas | Dec 25, 2026 | Exclude |

4. Link this exclusion schedule to "Business Hours India"

### Step 1.4: Create a 24x7 Schedule

1. Create a new schedule: **24x7 Operations**
2. Add a schedule entry:
   - All day: Checked
   - Days: All days (Mon-Sun)
   - Repeat: Weekly
3. No exclusions -- 24x7 means ALL the time

---

## Part 2: Create SLA Definitions

### Step 2.1: Navigate to SLA Definitions

1. Navigate to **Service Level Management > SLA > SLA Definitions** (or type `sla_definition.list`)
2. Browse existing SLA definitions

### Step 2.2: Create P1 Incident Response SLA

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | P1 Incident Response |
   | Table | Incident [incident] |
   | Type | SLA |
   | Target type | Duration |
   | Duration | 5 minutes |
   | Schedule | 24x7 Operations |
   | Active | Checked |

3. **Start condition** (when the timer starts):
   ```
   Condition: Priority = 1 - Critical AND State = New
   ```
   Set using the condition builder on the form.

4. **Stop condition** (when the timer stops):
   ```
   Condition: State changes to In Progress OR Assigned to is not empty
   ```

5. Click **Submit**

### Step 2.3: Create P1 Incident Resolution SLA

1. Click **New**:

   | Field | Value |
   |---|---|
   | Name | P1 Incident Resolution |
   | Table | Incident [incident] |
   | Type | SLA |
   | Duration | 30 minutes |
   | Schedule | 24x7 Operations |

2. **Start condition**:
   ```
   Priority = 1 - Critical AND State = In Progress
   ```

3. **Pause condition** (timer pauses):
   ```
   State = On Hold
   ```

4. **Stop condition**:
   ```
   State = Resolved OR State = Closed
   ```

5. **Reset condition** (SLA no longer applies):
   ```
   Priority changes from 1 to anything else
   ```

6. Click **Submit**

### Step 2.4: Create P2 Resolution SLA

| Field | Value |
|---|---|
| Name | P2 Incident Resolution |
| Table | Incident [incident] |
| Duration | 4 hours |
| Schedule | Business Hours India |
| Start | Priority = 2 AND State = In Progress |
| Pause | State = On Hold |
| Stop | State = Resolved OR Closed |

### Step 2.5: Create Service Request SLA

| Field | Value |
|---|---|
| Name | Service Request Fulfillment |
| Table | Request Item [sc_req_item] |
| Duration | 8 hours |
| Schedule | Business Hours India |
| Start | Stage = Fulfillment |
| Stop | Stage = Closed Complete |

Click **Submit**

---

## Part 3: Test SLA Timers

### Step 3.1: Create a P1 Incident and Watch the SLA

1. Create a new incident:
   - Priority: 1 - Critical
   - Short description: "SLA Test - Critical server down"
   - State: New
2. Click **Submit**
3. Immediately reopen the incident
4. Look for the **SLA** section or **Task SLA** related list at the bottom
5. You should see the "P1 Incident Response" SLA timer running:
   ```
   SLA: P1 Incident Response
   Stage: In Progress
   Target: 5 minutes
   Elapsed: 0 minutes
   Has breached: No
   ```

### Step 3.2: Acknowledge the Incident

1. Change **Assigned to** to a user (e.g., Ravi Kumar)
2. Change **State** to **In Progress**
3. Click **Update**
4. Reopen the incident
5. Check the SLA:
   - P1 Incident Response: should be **Achieved** (stopped timer)
   - P1 Incident Resolution: should now be **In Progress** (new timer started)

### Step 3.3: Test Pause

1. Change **State** to **On Hold**
2. Click **Update**
3. Reopen and check: P1 Resolution SLA should show **Paused**
4. Change **State** back to **In Progress**
5. The SLA timer resumes from where it paused

### Step 3.4: Resolve and Check SLA Status

1. Change **State** to **Resolved**
2. Add resolution notes
3. Click **Update**
4. Reopen the incident
5. Check the SLA:
   - P1 Incident Resolution: **Achieved** or **Breached**
   - The **Has breached** field shows true/false
   - **Business elapsed time** shows the actual elapsed time

---

## Part 4: SLA Breach Triggers

### Step 4.1: Navigate to SLA Triggers

Triggers fire actions at specific SLA percentage thresholds.

### Step 4.2: Create a 50% Warning Trigger

1. Open the "P1 Incident Resolution" SLA definition
2. Find the **SLA Percentage Timer** or go to **SLA > SLA Workflows** or add conditions in the SLA definition
3. Alternative: Use **System Policy > Events** to create event-based triggers

For a simpler approach, create a **Business Rule** or **Flow** (we'll use a notification approach):

1. Navigate to **System Notification > Email > Notifications** (or type `sysevent_email_action.list`)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | P1 SLA 50% Warning |
   | Table | Task SLA [task_sla] |
   | Active | Checked |

4. **When to send** tab:
   - Send when: Record updated
   - Conditions: `sla.name = P1 Incident Resolution AND percentage >= 50 AND percentage < 75 AND stage = In Progress`

5. **Who will receive** tab:
   - Users: (select assignment group manager)
   - Or Groups: Platform Engineering

6. **What it will contain** tab:
   - Subject: `[SLA WARNING] ${task.number}: ${task.short_description} - 50% elapsed`
   - Body:
     ```
     SLA Warning: P1 Incident Resolution

     Incident: ${task.number}
     Description: ${task.short_description}
     Priority: ${task.priority}
     Assigned to: ${task.assigned_to}
     Assignment group: ${task.assignment_group}

     SLA Status: 50% of time elapsed
     Time remaining: ${time_left}
     Target: 30 minutes

     Please ensure this incident is being actively worked on.
     ```

7. Click **Submit**

### Step 4.3: Create a 75% Escalation Trigger

Create another notification:

| Field | Value |
|---|---|
| Name | P1 SLA 75% Escalation |
| Condition | percentage >= 75 AND percentage < 100 |
| Recipients | VP Engineering (Sanjay Manager) |
| Subject | `[SLA CRITICAL] ${task.number} - Auto-escalation at 75%` |

### Step 4.4: Create a Breach Notification

| Field | Value |
|---|---|
| Name | P1 SLA Breached |
| Condition | has_breached = true |
| Recipients | CTO, service owner |
| Subject | `[SLA BREACHED] ${task.number}: ${task.short_description}` |

---

## Part 5: Email Notifications

### Step 5.1: View Existing Notifications

1. Navigate to **System Notification > Email > Notifications** (or type `sysevent_email_action.list`)
2. Browse existing notifications
3. Click any notification to see its configuration

### Step 5.2: Create Incident Assignment Notification

1. Click **New**
2. Fill in:

   **When to send:**
   | Field | Value |
   |---|---|
   | Name | Incident Assigned to Me |
   | Table | Incident [incident] |
   | Send when | Record updated |
   | Conditions | Assigned to changes |
   | Event name | (leave blank or use incident.assigned) |

   **Who will receive:**
   | Field | Value |
   |---|---|
   | Users/Groups | Event Parm 1 user (or configure "Assigned to" field) |
   | Send to event creator | No |

   **What it will contain:**
   | Field | Value |
   |---|---|
   | Subject | `Incident ${number} assigned to you: ${short_description}` |
   | Body | (see below) |

   Email body:
   ```html
   Hello ${assigned_to.first_name},

   An incident has been assigned to you:

   Number: ${number}
   Priority: ${priority}
   Short description: ${short_description}
   Caller: ${caller_id.name}
   Assignment group: ${assignment_group.name}

   Description:
   ${description}

   SLA Target: ${sla_due}

   Click here to view: ${URI_REF}

   Please acknowledge and begin working on this incident.
   ```

3. Click **Submit**

### Step 5.3: Variable Substitution Reference

| Variable | Description | Example Output |
|---|---|---|
| `${number}` | Record number | INC0010001 |
| `${short_description}` | Short description | VPN down |
| `${priority}` | Priority value | 1 - Critical |
| `${assigned_to.name}` | Assigned user's name | Ravi Kumar |
| `${caller_id.email}` | Caller's email | abel@example.com |
| `${assignment_group.name}` | Group name | Platform Engineering |
| `${URI}` | Full URL to record | https://dev.../incident.do?... |
| `${URI_REF}` | Clickable link | HTML link to the record |
| `${sla_due}` | SLA due date/time | 2026-09-22 09:30:00 |

### Step 5.4: Test Email Notifications

1. Navigate to **System Mailboxes > Outbound > Sent** (or type `sys_email.list`)
2. This shows all emails sent by the system
3. Create or update an incident to trigger your notification
4. Check the Sent mailbox -- your notification should appear
5. Click on the email to verify the content, subject, and recipients

---

## Part 6: Inbound Email (Bonus)

### Step 6.1: Configure Inbound Email to Create Incidents

1. Navigate to **System Mailboxes > Inbound > Email Actions** (or type `sysevent_email_action_inbound.list`)
2. View existing inbound email actions
3. ServiceNow can be configured to:
   - Create incidents from incoming emails
   - Update incidents when users reply to notification emails
   - Route to specific groups based on email subject/content

---

## Part 7: Practice Exercises

### Exercise 1: Complete SLA Setup

Create SLA definitions for all priority levels:

| SLA Name | Target | Schedule |
|---|---|---|
| P1 Response | 5 min | 24x7 |
| P1 Resolution | 30 min | 24x7 |
| P2 Response | 15 min | 24x7 |
| P2 Resolution | 4 hours | Business Hours |
| P3 Response | 1 hour | Business Hours |
| P3 Resolution | 24 hours | Business Hours |
| P4 Resolution | 72 hours | Business Hours |

### Exercise 2: End-to-End Escalation Test

1. Create a P1 incident
2. DON'T assign it -- wait and watch the response SLA timer
3. Assign it after a couple of minutes -- check if SLA was met
4. Don't resolve it -- watch the resolution SLA timer approach 50%, 75%
5. Check if notifications are generated at each threshold
6. Resolve before or after breach -- document the SLA status

### Exercise 3: Notification Matrix

Create notifications for these scenarios:

| Event | Recipients | Priority |
|---|---|---|
| P1 incident created | On-call group, NOC manager | Immediate |
| Incident reassigned | New assignee | Normal |
| Change approved | Change requester | Normal |
| Change rejected | Change requester + manager | Normal |
| SLA at 75% | Assignment group manager | High |
| SLA breached | VP Engineering | Critical |

---

## Lab Summary

| What You Did | Why It Matters |
|---|---|
| Created schedules with exclusions | SLA timers respect business hours and holidays |
| Built SLA definitions | Measurable targets for service performance |
| Tested SLA start/pause/stop | Understanding timer behavior for accurate tracking |
| Created breach triggers | Automated escalation prevents SLA violations |
| Configured notifications | Right people informed at the right time |

---

## Key Concepts

| Concept | Definition |
|---|---|
| **SLA Definition** | A timer configuration with start, pause, stop, and reset conditions |
| **Schedule** | Defines when SLA time counts (business hours, 24x7, custom) |
| **Exclusion** | Holidays/exceptions when SLA time doesn't count |
| **SLA Percentage** | How much of the target time has elapsed |
| **Breach** | When 100% of SLA target time has elapsed without meeting the stop condition |
| **Notification** | Automated email triggered by system events or conditions |
| **Variable Substitution** | `${field_name}` syntax to inject dynamic data into notifications |

---

## What's Next

In **Lab 14**, you'll configure **UI Policies & UI Actions** -- making forms dynamic with conditional field visibility, mandatory fields, and custom buttons.
