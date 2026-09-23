# Lab 20: Flow Designer & Workflow Automation

**Level:** Advanced | **Duration:** 90 min | **Prerequisites:** Labs 12-19 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand the ITIL 4 guiding principle "Optimize and Automate" and its practical application
- Master the Flow Designer interface: triggers, actions, flow logic, subflows, and data pills
- Build an Incident Auto-Assignment flow based on category and priority
- Build an SLA Breach Escalation flow with email notifications
- Build a Scheduled Flow to auto-close resolved incidents after 5 days
- Build a Catalog Approval Flow for Merchant Onboarding with sequential tasks
- Create reusable Subflows and call them from parent flows
- Build a Weekly ITSM Summary scheduled flow
- Test, debug, and troubleshoot flows using Flow Designer's built-in tools
- Understand when to use Flow Designer vs Legacy Workflows vs Business Rules

---

## Scenario: Automating UPI Platform Operations

```
NPCI's UPI platform generates hundreds of incidents, change requests, and
service catalog requests every week. Manual routing, escalation, and closure
consume significant effort from the Service Desk and Platform Engineering teams.

Sanjay Manager has mandated:
  "Every repetitive process must be automated. No P1 incident should sit
   unassigned for more than 30 seconds. No SLA breach should go unnoticed.
   Resolved incidents must auto-close. Catalog fulfillment must be orchestrated."

Your mission: Build a comprehensive automation layer using Flow Designer
that eliminates manual toil and enforces NPCI's ITSM policies.
```

---

## Part 1: Automation in ITIL 4

### The Guiding Principle: "Optimize and Automate"

```
ITIL 4 Guiding Principles:
  1. Focus on value
  2. Start where you are
  3. Progress iteratively with feedback
  4. Collaborate and promote visibility
  5. Think and work holistically
  6. Keep it simple and practical
  7. OPTIMIZE AND AUTOMATE            <-- This lab's focus

"Resources of all types, particularly human resources, should be used
 to their best effect. Eliminate anything that is truly wasteful and
 use technology to achieve whatever it is capable of."
                                        — ITIL 4 Foundation, Axelos
```

### What Should You Automate?

```
HIGH VALUE AUTOMATION TARGETS:
+----------------------------------+-------------------+------------------+
| Process                          | Manual Effort     | Automation Value |
+----------------------------------+-------------------+------------------+
| Incident assignment/routing      | 2-5 min/incident  | Very High        |
| SLA breach escalation            | Reactive/missed   | Critical         |
| Resolved incident closure        | Daily review task  | High             |
| Catalog request fulfillment      | Multi-step manual | Very High        |
| Notifications and alerts         | Often forgotten   | High             |
| Standard change creation         | Repetitive forms  | Medium           |
| Report generation                | Weekly manual     | Medium           |
| Password resets                  | High volume       | Very High        |
+----------------------------------+-------------------+------------------+

NPCI UPI CONTEXT — What we will automate today:
  1. P1/P2 UPI incidents → auto-assign to correct engineer
  2. SLA breach → auto-escalate to management
  3. Resolved incidents → auto-close after 5 days
  4. Merchant onboarding requests → orchestrated approval + task creation
  5. Weekly summary → automated report to management
```

### Automation Value Chain

```
ITIL 4 Automation Value Chain:

  IDENTIFY          PRIORITIZE         DESIGN            BUILD
  What can be  -->  Which gives   -->  How should   -->  Implement
  automated?        most value?        it work?          in platform

       |                                                     |
       v                                                     v
  MONITOR           DEPLOY             TEST
  Is it working  <--  Roll out     <--  Verify it
  as expected?        to production     works correctly

For each flow we build today, we follow this chain:
  - Identify the manual process
  - Confirm it is high-value
  - Design the logic (trigger + conditions + actions)
  - Build in Flow Designer
  - Test with real records
  - Monitor execution history
```

### Low-Code vs Pro-Code Automation in ServiceNow

```
+-------------------------+----------------------------+----------------------------+
| Approach                | When to Use                | ServiceNow Tools           |
+-------------------------+----------------------------+----------------------------+
| Low-Code (No Script)    | Standard routing,          | Flow Designer              |
|                         | approvals, notifications,  | Workflow Editor            |
|                         | simple record operations   | Assignment Rules           |
+-------------------------+----------------------------+----------------------------+
| Pro-Code (Script)       | Complex logic, external    | Business Rules             |
|                         | API calls, data transform, | Script Includes            |
|                         | performance-critical       | Scheduled Scripts          |
+-------------------------+----------------------------+----------------------------+
| Hybrid                  | Low-code orchestration     | Flow Designer + Custom     |
|                         | with scripted actions      | Script Actions             |
+-------------------------+----------------------------+----------------------------+

NPCI Decision Framework:
  "If Flow Designer can do it → use Flow Designer.
   If it needs script → use a Custom Action inside Flow Designer.
   Only use standalone Business Rules for table-level field logic."
```

### Flow Designer vs Legacy Workflow vs Business Rules

```
COMPARISON MATRIX:
+---------------------+------------------+------------------+------------------+
| Feature             | Flow Designer    | Legacy Workflow  | Business Rules   |
+---------------------+------------------+------------------+------------------+
| Interface           | Visual, modern   | Visual, legacy   | Script-based     |
| Trigger types       | Many             | Limited          | Record ops only  |
| Reusability         | Subflows         | Limited          | Script Includes  |
| Integration Hub     | Yes              | No               | REST manually    |
| Debugging           | Built-in         | Basic            | Debug BR         |
| Future direction    | Strategic        | Deprecated path  | Always relevant  |
| Catalog integration | Native           | Native           | Indirect         |
| Scheduling          | Built-in         | Timer activities  | Scheduled Jobs   |
| Approvals           | Built-in actions | Approval engine  | Not applicable   |
| Recommended for     | New development  | Legacy only      | Field-level ops  |
+---------------------+------------------+------------------+------------------+

ServiceNow's direction: Flow Designer is the strategic automation platform.
Legacy Workflow Editor is in maintenance mode. All new automation should
use Flow Designer.
```

---

## Part 2: Flow Designer Architecture

### Accessing Flow Designer

```
NAVIGATION:
  All > Process Automation > Flow Designer

  OR: Type "Flow Designer" in the Filter Navigator

  This opens Flow Designer in a NEW browser tab/window.
  Flow Designer has its own dedicated interface — it does NOT run
  inside the standard ServiceNow frame.
```

### Interface Walkthrough

```
FLOW DESIGNER HOME SCREEN:
+------------------------------------------------------------------+
|  Flow Designer                                    [+ New] [v]     |
+------------------------------------------------------------------+
|  Flows | Subflows | Actions | Spokes | Execution History         |
+------------------------------------------------------------------+
|                                                                    |
|  My Flows                                                          |
|  +-----------------------------------------------------------+    |
|  | Name            | Status   | Updated      | Application   |    |
|  +-----------------------------------------------------------+    |
|  | (your flows     | Draft/   | Date         | Global/       |    |
|  |  appear here)   | Active)  |              | Scoped App)   |    |
|  +-----------------------------------------------------------+    |
|                                                                    |
|  Recent Executions                                                 |
|  +-----------------------------------------------------------+    |
|  | Flow Name       | Status   | Started      | Duration      |    |
|  +-----------------------------------------------------------+    |
|  | (executions     | Complete/| Date/time    | ms            |    |
|  |  appear here)   | Error)   |              |               |    |
|  +-----------------------------------------------------------+    |
+------------------------------------------------------------------+

TOP-LEVEL TABS:
  Flows       → Main automation sequences (trigger + actions)
  Subflows    → Reusable flow components (no trigger, called by flows)
  Actions     → Individual operations (core, custom, spoke-based)
  Spokes      → Integration Hub connectors (Slack, Teams, JIRA, etc.)
  Execution   → History and debugging of flow runs
  History
```

### Flow Components Deep Dive

```
ANATOMY OF A FLOW:
+------------------------------------------------------------------+
|  FLOW: "UPI Incident Auto-Assignment"                             |
+------------------------------------------------------------------+
|                                                                    |
|  TRIGGER (What starts this flow?)                                  |
|  +--------------------------------------------------------------+ |
|  | Record Created or Updated                                     | |
|  | Table: Incident [incident]                                    | |
|  | Condition: Category = UPI                                     | |
|  +--------------------------------------------------------------+ |
|                                                                    |
|  ACTIONS & FLOW LOGIC (What does the flow do?)                     |
|  +--------------------------------------------------------------+ |
|  | 1. IF Trigger→Incident→Priority = 1 - Critical               | |
|  |    THEN:                                                      | |
|  |      1.1 Update Record: Assignment group = Platform Eng       | |
|  |      1.2 Update Record: Assigned to = Ravi Kumar             | |
|  |      1.3 Add Work Note: "Auto-assigned..."                   | |
|  |    ELSE IF Priority = 2 or 3:                                 | |
|  |      1.4 Update Record: Assignment group = Platform Eng       | |
|  |      1.5 Update Record: Assigned to = Amit Verma             | |
|  |    ELSE:                                                      | |
|  |      1.6 Update Record: Assignment group = Service Desk       | |
|  +--------------------------------------------------------------+ |
|                                                                    |
+------------------------------------------------------------------+
```

### Trigger Types

```
TRIGGER TYPES IN FLOW DESIGNER:

1. RECORD-BASED TRIGGERS:
   - Created                    → When a new record is inserted
   - Created or Updated         → When a record is inserted or modified
   - Updated                    → When an existing record is modified
   - Deleted                    → When a record is removed

   Configuration options:
     Table:      Select the target table (e.g., Incident [incident])
     Condition:  Optional filter (e.g., Priority = 1 AND Category = UPI)
     Run as:     System or specific user context

   IMPORTANT: Conditions on triggers filter WHICH records activate the flow.
              Conditions in flow logic determine WHAT actions to take.

2. SCHEDULE-BASED TRIGGERS:
   - Daily          → Run once per day at specified time
   - Weekly         → Run on specified day(s) at specified time
   - Monthly        → Run on specified date at specified time
   - Repeat         → Run at interval (every N minutes/hours)

   Configuration options:
     Time zone:  Select appropriate timezone (IST for NPCI)
     Run as:     System or specific user context

3. APPLICATION-BASED TRIGGERS:
   - Service Catalog  → When a catalog item is requested (RITM created)
   - Inbound Email    → When an email is received matching criteria
   - REST/API         → When an external system calls a trigger endpoint
   - MetricBase       → When a metric threshold is crossed

4. FLOW LOGIC TRIGGERS (used in Subflows):
   - Subflows do NOT have triggers — they are called by parent flows
   - They accept INPUT variables defined at design time
```

### Action Types

```
CORE ACTIONS (Built-in):

  Record Operations:
    - Create Record         → Insert a new record in any table
    - Update Record         → Modify fields on an existing record
    - Delete Record         → Remove a record
    - Lookup Record         → Find a single record by conditions
    - Lookup Records        → Find multiple records (returns list)

  Communication:
    - Send Email            → Send email notification
    - Send Notification     → Send via notification channel
    - Create Event          → Create a ServiceNow event

  Task Management:
    - Ask for Approval      → Request approval from user/group
    - Create Task           → Create task record (SCTASK, etc.)
    - Wait for Condition    → Pause flow until condition is met

  Flow Control:
    - Log                   → Write to flow execution log
    - Set Flow Variables    → Store values for later use

FLOW LOGIC ELEMENTS:

  - If / Then / Else        → Conditional branching
  - For Each                → Loop through a list of records
  - Do Until                → Repeat until a condition is true
  - Wait                    → Pause for duration or until condition
  - Parallel                → Execute multiple branches simultaneously

INTEGRATION HUB ACTIONS (require subscription):
  - Slack: Post message, create channel
  - Microsoft Teams: Send message
  - JIRA: Create issue, update issue
  - REST: Make arbitrary HTTP calls
  - PowerShell: Run remote commands
  - SSH: Execute remote commands
  - Ansible: Run playbook
```

### Data Pills and Dot-Walking

```
DATA PILLS — The heart of dynamic data in Flow Designer:

  Data pills are references to values from triggers, actions, or flow variables.
  They appear as colored capsules that you drag into fields.

  Example:
    Trigger: Record Created [Incident]

    Available data pills:
      Trigger → Incident Record → Number        = INC0010042
      Trigger → Incident Record → Short description
      Trigger → Incident Record → Priority
      Trigger → Incident Record → Caller        (reference field)
      Trigger → Incident Record → Assignment group

  DOT-WALKING — Navigate through reference fields:
    Trigger → Incident Record → Caller → Email
    Trigger → Incident Record → Caller → Manager → Name
    Trigger → Incident Record → Assignment group → Manager → Email

    This is equivalent to:
      current.caller_id.email
      current.caller_id.manager.name
      current.assignment_group.manager.email

  Data pills from ACTIONS:
    After a "Lookup Record" action, its output becomes a data pill:
      Step 2 → User Record → Email
      Step 2 → User Record → Name

  VISUAL REPRESENTATION:
    +----------------------------------------------------------+
    | Send Email                                                |
    | To:    [ Trigger→Incident→Caller→Email ]                  |
    | Subject: P1 Incident [ Trigger→Incident→Number ] Opened  |
    | Body:  Dear [ Trigger→Incident→Caller→Name ],            |
    |        A critical incident has been raised...             |
    +----------------------------------------------------------+
    (Items in brackets are data pills — colored capsules in the UI)
```

---

## Part 3: Create Incident Auto-Assignment Flow

### Design

```
FLOW: UPI Incident Auto-Assignment

PURPOSE:  Automatically assign UPI incidents to the correct engineer
          based on category and priority. Eliminates manual triage delay.

TRIGGER:  When an Incident record is CREATED
          Condition: Category = "UPI" OR Category = "Network"

LOGIC:
  IF Category = "UPI" AND Priority = 1 - Critical:
    → Assign to group: Platform Engineering
    → Assign to: Ravi Kumar
    → Work note: "P1 UPI incident auto-assigned to Ravi Kumar (Platform Eng Lead)"

  ELSE IF Category = "UPI" AND Priority = 2 or 3:
    → Assign to group: Platform Engineering
    → Assign to: Amit Verma
    → Work note: "Auto-assigned to Amit Verma (Platform Engineering)"

  ELSE IF Category = "Network":
    → Assign to group: Network Operations
    → Work note: "Auto-assigned to Network Operations based on category"

  ELSE:
    → Assign to group: Service Desk
    → Assign to: Meera Joshi
    → Work note: "Auto-assigned to Service Desk"

EXPECTED OUTCOME:
  Every qualifying incident is assigned within seconds of creation.
  No manual triage needed for UPI and Network incidents.
```

### Step-by-Step Build

```
STEP 1: Open Flow Designer
  Navigation: All > Process Automation > Flow Designer
  → Flow Designer opens in a new tab

STEP 2: Create New Flow
  Click: [+ New] → Flow
  Flow Properties:
    Name:           UPI Incident Auto-Assignment
    Description:    Automatically assigns UPI and Network incidents to the
                    correct team and engineer based on category and priority.
                    Part of NPCI UPI automation initiative.
    Application:    Global
    Protection:     None
    Run As:         System User
  Click: [Submit]

STEP 3: Add Trigger
  Click: [Add a trigger]
  Select: "Created" (under Record)
  Configure:
    Table:          Incident [incident]
    Condition:      [Category] [is one of] [UPI, Network]

  WHY "Created" not "Created or Updated"?
    We only want assignment on initial creation. If we used "Created or Updated",
    every field change would re-trigger assignment, potentially overriding
    manual reassignments made by the team.

STEP 4: Add Flow Logic — First Condition (P1 UPI)
  Click: [Add an Action, Flow Logic, or Subflow]
  Select: Flow Logic → If
  Configure the IF condition:
    Condition Label:  P1 UPI Incident
    Condition:
      [Trigger - Record Created → Incident Record → Category] [is] [UPI]
      AND
      [Trigger - Record Created → Incident Record → Priority] [is] [1 - Critical]

STEP 5: Add Actions Inside the IF Branch
  Inside the "then" section:

  Action 5a: Update Record
    Click: [Add an Action, Flow Logic, or Subflow] (inside the THEN)
    Select: ServiceNow Core → Update Record
    Configure:
      Record:           Drag data pill: Trigger - Record Created → Incident Record
      Fields to update:
        Assignment group:  Platform Engineering
        Assigned to:       Ravi Kumar

  Action 5b: Update Record (Add Work Note)
    Add another action inside the THEN:
    Select: ServiceNow Core → Update Record
    Configure:
      Record:           Drag data pill: Trigger - Record Created → Incident Record
      Fields to update:
        Work notes:     [Auto-Assigned] P1 UPI incident auto-assigned to
                        Ravi Kumar (Platform Engineering Lead) by Flow Designer.
                        Immediate attention required per NPCI P1 SLA.

  NOTE: You can combine both field updates into a single "Update Record"
  action. Set Assignment group, Assigned to, AND Work notes all in one step.
  We show them separately for clarity.

STEP 6: Add Else If — P2/P3 UPI
  Click on the IF block → [Else If]
  Configure:
    Condition Label:  P2/P3 UPI Incident
    Condition:
      [Trigger → Incident Record → Category] [is] [UPI]
      AND
      [Trigger → Incident Record → Priority] [is one of] [2 - High, 3 - Moderate]

  Add Action inside this Else If:
    Select: ServiceNow Core → Update Record
    Configure:
      Record:           Trigger → Incident Record
      Fields to update:
        Assignment group:  Platform Engineering
        Assigned to:       Amit Verma
        Work notes:        [Auto-Assigned] UPI incident auto-assigned to
                           Amit Verma (Platform Engineering) by Flow Designer.

STEP 7: Add Else If — Network Category
  Click on the IF block → [Else If]
  Configure:
    Condition Label:  Network Incident
    Condition:
      [Trigger → Incident Record → Category] [is] [Network]

  Add Action inside this Else If:
    Select: ServiceNow Core → Update Record
    Configure:
      Record:           Trigger → Incident Record
      Fields to update:
        Assignment group:  Network Operations
        Work notes:        [Auto-Assigned] Network incident auto-assigned to
                           Network Operations team by Flow Designer.

STEP 8: Add Else — Default to Service Desk
  Click on the IF block → [Else]

  Add Action inside the Else:
    Select: ServiceNow Core → Update Record
    Configure:
      Record:           Trigger → Incident Record
      Fields to update:
        Assignment group:  Service Desk
        Assigned to:       Meera Joshi
        Work notes:        [Auto-Assigned] Incident auto-assigned to Service Desk
                           (default assignment) by Flow Designer.

STEP 9: Save and Activate
  Click: [Save] (top right)
  Click: [Activate] (top right)
  Confirm activation when prompted.

  STATUS CHANGES: Draft → Active
  The flow is now live and will trigger on every new incident matching
  the trigger condition.
```

### Testing the Flow

```
TEST SCENARIO 1: P1 UPI Incident
  Navigation: All > Incident > Create New
  Fill in:
    Caller:             Priya Sharma
    Category:           UPI
    Subcategory:        Transaction Failure
    Short description:  UPI payment gateway completely down - all transactions failing
    Priority:           1 - Critical
  Click: [Submit]

  VERIFY:
    Open the incident you just created.
    Expected:
      Assignment group:  Platform Engineering
      Assigned to:       Ravi Kumar
      Work notes:        Should contain "[Auto-Assigned] P1 UPI incident..."

TEST SCENARIO 2: P2 UPI Incident
  Create New Incident:
    Caller:             Meera Joshi
    Category:           UPI
    Short description:  UPI settlement batch delayed for 3 banks
    Priority:           2 - High
  Submit and verify:
    Assignment group:  Platform Engineering
    Assigned to:       Amit Verma

TEST SCENARIO 3: Network Incident
  Create New Incident:
    Caller:             Amit Verma
    Category:           Network
    Short description:  Network latency spike on UPI backend cluster
    Priority:           3 - Moderate
  Submit and verify:
    Assignment group:  Network Operations

TEST SCENARIO 4: Other Category
  Create New Incident:
    Caller:             Vijay Admin
    Category:           Hardware
    Short description:  Workstation not booting
    Priority:           4 - Low
  Submit and verify:
    Assignment group:  Service Desk
    Assigned to:       Meera Joshi

CHECK FLOW EXECUTION:
  In Flow Designer → Execution History tab
  You should see 4 executions, all with status "Complete"
  Click any execution to see the step-by-step trace:
    - Trigger fired
    - IF condition evaluated (true/false)
    - Action executed
    - Record updated
```

---

## Part 4: Create SLA Breach Escalation Flow

### Design

```
FLOW: UPI SLA Breach Escalation

PURPOSE:  When any Task SLA breaches, automatically escalate based on
          the related incident's priority. Ensures no SLA breach goes
          unnoticed — critical for NPCI's regulatory compliance.

TRIGGER:  When Task SLA [task_sla] record is Updated
          Condition: Has breached changes to true

LOGIC:
  Step 1: Look up the related incident (task_sla.task → incident)

  Step 2: IF incident priority = 1 - Critical:
    → Send email to Sanjay Manager
    → Add work note on incident: "P1 SLA BREACHED — Escalated to VP Engineering"
    → Set incident state to "In Progress" if currently "New"
    → Create Event: "upi.sla.breach.p1"

  Step 3: ELSE IF incident priority = 2 - High:
    → Send email to Ravi Kumar
    → Add work note: "P2 SLA breach — Escalated to Platform Engineering Lead"
    → Create Event: "upi.sla.breach.p2"

  Step 4: ELSE (P3/P4):
    → Add work note: "SLA breach recorded. Review assignment and progress."
    → Create Event: "upi.sla.breach.general"
```

### Step-by-Step Build

```
STEP 1: Create New Flow
  Flow Designer → [+ New] → Flow
  Properties:
    Name:           UPI SLA Breach Escalation
    Description:    Escalates SLA breaches based on incident priority.
                    P1 → VP notification. P2 → Team lead notification.
    Application:    Global
    Run As:         System User
  Click: [Submit]

STEP 2: Add Trigger
  Click: [Add a trigger]
  Select: "Updated" (under Record)
  Configure:
    Table:          Task SLA [task_sla]
    Condition:      [Has breached] [changes to] [true]

  NOTE: The Task SLA table tracks SLA progress for each task.
  The "has_breached" field flips to true when the SLA timer expires.
  This trigger catches that exact moment.

STEP 3: Look Up the Related Incident
  Add Action: ServiceNow Core → Lookup Record
  Configure:
    Table:          Incident [incident]
    Condition:      [Sys ID] [is] [Trigger → Task SLA Record → Task]

  NOTE: The Task SLA's "Task" field is a reference to the task (incident).
  We look up the full incident record so we can read its priority,
  assigned to, and other fields.

  OUTPUT: This action produces a data pill "Step 3 - Lookup Record → Incident Record"

STEP 4: Add IF — P1 Priority
  Add Flow Logic: If
  Configure:
    Condition Label:  P1 Critical Incident
    Condition:
      [Step 3 → Incident Record → Priority] [is] [1 - Critical]

  Inside THEN:

  Action 4a: Send Email
    Add Action: ServiceNow Core → Send Email
    Configure:
      To:       Search for "Sanjay Manager" (or use sys_id)
      Subject:  URGENT: P1 SLA BREACHED — [Step 3 → Incident Record → Number]
      Body:
        CRITICAL SLA BREACH ALERT

        Incident: [Step 3 → Incident Record → Number]
        Short Description: [Step 3 → Incident Record → Short description]
        Priority: 1 - Critical
        Assigned To: [Step 3 → Incident Record → Assigned to → Name]
        Assignment Group: [Step 3 → Incident Record → Assignment group → Name]
        SLA: [Trigger → Task SLA Record → SLA definition → Name]

        The SLA for this P1 incident has BREACHED.
        Immediate VP-level escalation is required per NPCI policy.

        This is an automated notification from Flow Designer.

  Action 4b: Update Record (Work Note)
    Add Action: ServiceNow Core → Update Record
    Configure:
      Record:     Step 3 → Incident Record
      Fields:
        Work notes:   *** P1 SLA BREACHED ***
                      SLA Definition: [Trigger → Task SLA Record → SLA definition → Name]
                      Breach Time: [Trigger → Task SLA Record → Breach time]
                      Action Taken: Escalated to VP Engineering (Sanjay Manager)
                      This escalation was performed automatically by Flow Designer.

  Action 4c: Update Record (State change — conditional)
    We need to check if the incident is still "New" before changing state.
    Add Flow Logic: If (nested inside the P1 THEN)
    Condition:
      [Step 3 → Incident Record → State] [is] [New]
    Then:
      Add Action: ServiceNow Core → Update Record
      Record:     Step 3 → Incident Record
      Fields:
        State:    In Progress
        Work notes: State changed from New to In Progress due to SLA breach.
                    A P1 incident must not remain in New state.

  Action 4d: Create Event
    Add Action: ServiceNow Core → Create Event
    Configure:
      Event name:     upi.sla.breach.p1
      Table:          incident
      Record:         Step 3 → Incident Record
      Param1:         P1 SLA Breach
      Param2:         [Step 3 → Incident Record → Number]

STEP 5: Add Else If — P2 Priority
  Click on the IF block → [Else If]
  Configure:
    Condition Label:  P2 High Priority Incident
    Condition:
      [Step 3 → Incident Record → Priority] [is] [2 - High]

  Inside this Else If:

  Action 5a: Send Email
    To:       Ravi Kumar
    Subject:  SLA Breach Alert: P2 Incident [Step 3 → Incident Record → Number]
    Body:
      SLA BREACH NOTIFICATION

      Incident: [Step 3 → Incident Record → Number]
      Short Description: [Step 3 → Incident Record → Short description]
      Priority: 2 - High
      Current Assignment: [Step 3 → Incident Record → Assigned to → Name]

      The SLA for this P2 incident has breached.
      As Platform Engineering Lead, please review and ensure resolution.

  Action 5b: Update Record
    Record:     Step 3 → Incident Record
    Fields:
      Work notes:   ** P2 SLA BREACH **
                    SLA: [Trigger → Task SLA Record → SLA definition → Name]
                    Escalated to: Ravi Kumar (Platform Engineering Lead)
                    Automated escalation by Flow Designer.

  Action 5c: Create Event
    Event name:     upi.sla.breach.p2
    Table:          incident
    Record:         Step 3 → Incident Record

STEP 6: Add Else — P3/P4
  Click on the IF block → [Else]

  Action 6a: Update Record
    Record:     Step 3 → Incident Record
    Fields:
      Work notes:   SLA breach recorded for this incident.
                    SLA: [Trigger → Task SLA Record → SLA definition → Name]
                    No escalation triggered (P3/P4 level).
                    Please review assignment and update progress.

  Action 6b: Create Event
    Event name:     upi.sla.breach.general
    Table:          incident
    Record:         Step 3 → Incident Record

STEP 7: Save and Activate
  Click: [Save] → [Activate]
```

### Testing SLA Breach Flow

```
TESTING APPROACH:
  To test an SLA breach, you need an incident with an active SLA that breaches.

OPTION A: Create a Short SLA for Testing
  1. Navigate: All > SLA > SLA Definitions
  2. Create a new SLA Definition:
     Name:           Test - 2 Minute Resolution
     Type:           SLA
     Table:          Incident [incident]
     Duration type:  User specified
     Duration:       0 days, 0 hours, 2 minutes
     Start condition: State = New
     Stop condition:  State = Resolved OR State = Closed
     Condition:      Priority = 1 - Critical
  3. Save

  4. Create a P1 Incident:
     Category: UPI, Priority: 1, Short description: "SLA breach test"

  5. Wait 2+ minutes without resolving

  6. Check:
     - The Task SLA record should show has_breached = true
     - The flow should have triggered
     - Check Flow Designer → Execution History for the run
     - Check the incident for work notes
     - Check Sanjay Manager's email

OPTION B: Manually Update Task SLA (faster)
  1. Create a P1 UPI incident
  2. Navigate: All > Task SLA > Task SLAs
  3. Find the Task SLA for your incident
  4. Manually set "Has breached" to true
  5. Save — this triggers the flow immediately

  IMPORTANT: After testing, deactivate the test SLA definition
  to avoid interference with real SLAs.
```

---

## Part 5: Create Auto-Close Resolved Incidents Flow

### Design

```
FLOW: Auto-Close Resolved Incidents After 5 Days

PURPOSE:  NPCI policy requires that incidents resolved for 5 or more
          days without reopening should be automatically closed.
          This reduces the backlog of Resolved-but-not-Closed incidents.

TRIGGER:  Scheduled — Daily at midnight (00:00 IST)

LOGIC:
  Step 1: Look up all incidents WHERE:
    - State = Resolved (6)
    - Resolved at < (now - 5 days)

  Step 2: For Each incident in the result:
    - Set State = Closed (7)
    - Set Close code = "Solved (Permanently)"
    - Set Close notes = "Auto-closed after 5 days in Resolved state
                         per NPCI incident management policy."
    - Add Work note: "This incident was auto-closed by Flow Designer.
                      5 days elapsed since resolution with no reopening."

  Step 3: Log count of closed incidents
```

### Step-by-Step Build

```
STEP 1: Create New Flow
  Flow Designer → [+ New] → Flow
  Properties:
    Name:           Auto-Close Resolved Incidents
    Description:    Automatically closes incidents that have been in Resolved
                    state for 5+ days. Runs daily at midnight per NPCI policy.
    Application:    Global
    Run As:         System User
  Click: [Submit]

STEP 2: Add Trigger — Schedule
  Click: [Add a trigger]
  Select: "Daily" (under Schedule)
  Configure:
    Time:       00:00
    Time zone:  Asia/Kolkata (IST)

  NOTE: Scheduled triggers do NOT have a record context.
  You must explicitly query for records in your flow logic.

STEP 3: Look Up Resolved Incidents
  Add Action: ServiceNow Core → Lookup Records (plural — returns a list)
  Configure:
    Table:          Incident [incident]
    Conditions:
      [State] [is] [Resolved]
      AND
      [Resolved] [before] [5 days ago]

  HOW TO SET "5 days ago":
    In the condition builder:
      Field:    Resolved
      Operator: before
      Value:    Use relative date → "5" "Days" "ago"

    This translates to: resolved_at < (now() - 5 days)

  OUTPUT: This action returns a LIST of incident records.

STEP 4: Add For Each Loop
  Add Flow Logic: For Each
  Configure:
    Items: Step 3 → Lookup Records → Incident Records (the list output)

  This creates a loop that iterates over every matching incident.
  Inside the loop, you get a data pill: "For Each → Incident Record"

STEP 5: Add Actions Inside the Loop
  Inside the For Each:

  Action 5a: Update Record
    Add Action: ServiceNow Core → Update Record
    Configure:
      Record:     For Each → Incident Record
      Fields:
        State:        Closed
        Close code:   Solved (Permanently)
        Close notes:  Auto-closed after 5 days in Resolved state per NPCI
                      incident management policy. No further action was taken
                      by the caller or resolver within the 5-day window.
                      Automated by Flow Designer.
        Work notes:   [AUTO-CLOSE] This incident was automatically closed by
                      Flow Designer. The incident was in Resolved state for
                      5+ days without being reopened. Per NPCI policy, resolved
                      incidents are auto-closed after 5 business days.
                      If this incident needs to be reopened, please create a
                      new incident referencing this record number.

STEP 6: Add Logging (After the For Each)
  After the For Each loop ends, add:
  Add Action: Flow Logic → Log
  Configure:
    Message:    Auto-Close Flow completed. Processed incidents from
                Resolved to Closed state. Check execution details for count.

STEP 7: Save and Activate
  Click: [Save] → [Activate]
```

### Testing Auto-Close Flow

```
TESTING — Since this is a scheduled flow, you test it manually:

STEP 1: Create a Test Incident
  Create New Incident:
    Caller:             Priya Sharma
    Category:           UPI
    Short description:  Test auto-close - old resolved incident
    Priority:           3 - Moderate
  Submit.

STEP 2: Resolve the Incident
  Open the incident → Set State = Resolved
  Add resolution notes: "Test resolution"
  Save.

STEP 3: Backdate the Resolved Date
  To simulate 5 days passing, update the resolved date:
  Navigate: All > System Definition > Scripts - Background

  Run:
    var gr = new GlideRecord('incident');
    gr.addQuery('short_description', 'Test auto-close - old resolved incident');
    gr.query();
    if (gr.next()) {
        var dt = new GlideDateTime();
        dt.addDaysLocalTime(-6);  // 6 days ago
        gr.setValue('resolved_at', dt.toString());
        gr.update();
        gs.info('Updated resolved_at to: ' + gr.getValue('resolved_at'));
    }

STEP 4: Manually Run the Flow
  In Flow Designer:
    Open "Auto-Close Resolved Incidents"
    Click: [Test]
    The flow runs immediately (ignoring the schedule)

STEP 5: Verify
  Open the test incident:
    Expected:
      State:        Closed
      Close code:   Solved (Permanently)
      Close notes:  Contains "Auto-closed after 5 days..."
      Work notes:   Contains "[AUTO-CLOSE]..."

  Check Flow Designer → Execution History:
    The execution should show status "Complete"
    Expand the For Each to see each iteration
```

---

## Part 6: Create Catalog Approval Flow

### Design

```
FLOW: Merchant Onboarding Approval Flow

PURPOSE:  When a user requests "Merchant Onboarding" from the Service Catalog,
          orchestrate the full lifecycle:
            1. Get approval from management
            2. If approved → create sequential fulfillment tasks
            3. Wait for each task to complete before creating the next
            4. Notify requester on completion or rejection

TRIGGER:  Service Catalog trigger — when RITM is created for
          "Request Merchant Onboarding" catalog item

LOGIC:
  Step 1: Ask for Approval from Sanjay Manager
  Step 2: IF Approved:
    2a. Create SCTASK: "Verify Merchant Documents" → Meera Joshi
    2b. Wait for SCTASK to close
    2c. Create SCTASK: "Configure Merchant in UPI" → Ravi Kumar
    2d. Wait for SCTASK to close
    2e. Close RITM as Complete
    2f. Send completion email to requester
  Step 3: IF Rejected:
    3a. Close RITM as Incomplete
    3b. Send rejection email to requester

THIS IS THE MOST COMPLEX FLOW IN THIS LAB.
It demonstrates: approvals, sequential task creation, wait conditions,
and request lifecycle management.
```

### Step-by-Step Build

```
STEP 1: Create New Flow
  Flow Designer → [+ New] → Flow
  Properties:
    Name:           Merchant Onboarding Approval Flow
    Description:    Orchestrates the merchant onboarding process including
                    management approval and sequential fulfillment tasks.
    Application:    Global
    Run As:         System User
  Click: [Submit]

STEP 2: Add Trigger — Service Catalog
  Click: [Add a trigger]
  Select: "Service Catalog" (under Application)
  Configure:
    Catalog Item:   Request Merchant Onboarding
                    (Select the catalog item created in a previous lab.
                     If you haven't created it, see the note below.)

  NOTE: If you don't have this catalog item from a previous lab,
  create one quickly:
    Navigation: All > Service Catalog > Catalog Definitions > Maintain Items
    Click: [New]
      Name:         Request Merchant Onboarding
      Category:     UPI Services (or any category)
      Short description: Request onboarding of a new merchant to the UPI platform
    Save.
    Add variables:
      - merchant_name (String, Mandatory)
      - merchant_id (String, Mandatory)
      - merchant_category (Choice: Retail, Food, Travel, Other)
    Save.

STEP 3: Ask for Approval
  Add Action: ServiceNow Core → Ask for Approval
  Configure:
    Record:             Trigger → Requested Item Record
    Approval rules:
      Anyone approves:  (select this radio button)
    Approvers:
      Users:            Sanjay Manager

  NOTE: The "Ask for Approval" action PAUSES the flow execution until
  the approval is approved or rejected. The flow sits in "Waiting"
  state in the execution history.

  OUTPUT: This action produces an output data pill:
    Step 3 → Approval State (Approved / Rejected)

STEP 4: Add IF — Approval Decision
  Add Flow Logic: If
  Configure:
    Condition Label:  Approved
    Condition:
      [Step 3 → Ask for Approval → Approval State] [is] [Approved]

STEP 5: Approved Branch — Create First Task
  Inside the THEN:

  Action 5a: Create Record (SCTASK 1)
    Add Action: ServiceNow Core → Create Record
    Configure:
      Table:          Catalog Task [sc_task]
      Fields:
        Request item:     Trigger → Requested Item Record
        Short description: Verify Merchant Documents — [Trigger → RITM → Variables → merchant_name]
        Description:      Verify the following documents for merchant onboarding:
                          1. Business registration certificate
                          2. PAN card / GST registration
                          3. Bank account details for settlement
                          4. Authorized signatory documentation

                          Merchant Name: [Trigger → RITM → Variables → merchant_name]
                          Merchant ID: [Trigger → RITM → Variables → merchant_id]
                          Merchant Category: [Trigger → RITM → Variables → merchant_category]
        Assignment group: Service Desk
        Assigned to:      Meera Joshi
        Priority:         3 - Moderate

    OUTPUT: Step 5a → Catalog Task Record

  Action 5b: Update RITM Work Notes
    Add Action: ServiceNow Core → Update Record
    Configure:
      Record:     Trigger → Requested Item Record
      Fields:
        Work notes:   Merchant onboarding APPROVED by Sanjay Manager.
                      Task 1 created: "Verify Merchant Documents" assigned to Meera Joshi.

STEP 6: Wait for First Task to Complete
  Add Action: Flow Logic → Wait for Condition
  Configure:
    Record:         Step 5a → Catalog Task Record
    Wait until:     [State] [is] [Closed Complete]
    Timeout:        5 days (optional — prevents indefinite waiting)

  NOTE: The flow PAUSES here until Meera Joshi closes the task.
  In the execution history, the flow shows "Waiting" status.

STEP 7: Create Second Task (after first completes)
  Action 7a: Create Record (SCTASK 2)
    Add Action: ServiceNow Core → Create Record
    Configure:
      Table:          Catalog Task [sc_task]
      Fields:
        Request item:     Trigger → Requested Item Record
        Short description: Configure Merchant in UPI Platform — [Trigger → RITM → Variables → merchant_name]
        Description:      Documents verified. Proceed with UPI platform configuration:
                          1. Create merchant VPA (Virtual Payment Address)
                          2. Configure settlement account
                          3. Set transaction limits per merchant category
                          4. Enable merchant in UPI switch
                          5. Run test transaction

                          Merchant Name: [Trigger → RITM → Variables → merchant_name]
                          Merchant ID: [Trigger → RITM → Variables → merchant_id]
        Assignment group: Platform Engineering
        Assigned to:      Ravi Kumar
        Priority:         3 - Moderate

  Action 7b: Update RITM Work Notes
    Update Record on Trigger → Requested Item Record:
      Work notes:   Task 1 (Document Verification) completed by Meera Joshi.
                    Task 2 created: "Configure Merchant in UPI Platform" assigned to Ravi Kumar.

STEP 8: Wait for Second Task to Complete
  Add Action: Flow Logic → Wait for Condition
  Configure:
    Record:         Step 7a → Catalog Task Record
    Wait until:     [State] [is] [Closed Complete]
    Timeout:        5 days

STEP 9: Close RITM as Complete
  Action 9a: Update Record
    Record:     Trigger → Requested Item Record
    Fields:
      State:        Closed Complete
      Work notes:   All fulfillment tasks completed successfully.
                    Merchant "[Trigger → RITM → Variables → merchant_name]"
                    has been onboarded to the UPI platform.
                    This request is now closed.

  Action 9b: Send Email — Completion Notification
    Add Action: ServiceNow Core → Send Email
    Configure:
      To:       Trigger → Requested Item Record → Request → Requested for → Email
      Subject:  Merchant Onboarding Complete — [Trigger → RITM → Variables → merchant_name]
      Body:
        Dear [Trigger → RITM → Request → Requested for → Name],

        Your merchant onboarding request has been completed successfully.

        Merchant Details:
          Name:     [Trigger → RITM → Variables → merchant_name]
          ID:       [Trigger → RITM → Variables → merchant_id]
          Category: [Trigger → RITM → Variables → merchant_category]

        The merchant is now active on the UPI platform.

        Request Number: [Trigger → RITM → Number]
        Completion Date: [current date/time]

        Thank you,
        NPCI UPI Service Desk

STEP 10: Rejected Branch
  Click on the IF block → [Else]
  (This handles the case where Sanjay Manager rejects the request)

  Action 10a: Update RITM
    Record:     Trigger → Requested Item Record
    Fields:
      State:        Closed Incomplete
      Work notes:   Merchant onboarding request REJECTED by management.
                    No fulfillment tasks will be created.
                    Requester has been notified.

  Action 10b: Send Email — Rejection Notification
    To:       Trigger → RITM → Request → Requested for → Email
    Subject:  Merchant Onboarding Request Rejected — [Trigger → RITM → Variables → merchant_name]
    Body:
      Dear [Trigger → RITM → Request → Requested for → Name],

      Your merchant onboarding request has been rejected.

      Merchant: [Trigger → RITM → Variables → merchant_name]
      Request: [Trigger → RITM → Number]

      Reason: The approver determined that this request cannot be
      fulfilled at this time. Please contact your manager for details
      or submit a new request with additional justification.

      Thank you,
      NPCI UPI Service Desk

STEP 11: Save and Activate
  Click: [Save] → [Activate]
```

### Testing Catalog Approval Flow

```
TESTING:

STEP 1: Submit the Catalog Request
  Navigate: Self-Service > Service Catalog
  Find: "Request Merchant Onboarding"
  Fill in:
    Merchant Name:     PhonePe Foods
    Merchant ID:       MERCH-2026-0451
    Merchant Category: Food
  Click: [Order Now] / [Submit]

  Note the RITM number (e.g., RITM0010001)

STEP 2: Check Flow Status
  Flow Designer → Execution History
  Find the "Merchant Onboarding Approval Flow" execution
  Status should be: "Waiting" (waiting for approval)

STEP 3: Approve the Request
  Log in as Sanjay Manager (or impersonate)
  Navigate: Self-Service > My Approvals
  Find the approval for RITM0010001
  Click: [Approve]

STEP 4: Check Flow Progresses
  Flow Designer → Execution History
  Status should now be: "Waiting" (waiting for SCTASK 1 to close)

  Check the RITM: Should have work notes about approval and Task 1 creation
  Check Catalog Tasks: SCTASK assigned to Meera Joshi should exist

STEP 5: Complete Task 1
  Log in as Meera Joshi (or impersonate)
  Open the SCTASK: "Verify Merchant Documents"
  Set State: Closed Complete
  Save

STEP 6: Check Flow Creates Task 2
  Flow Designer → Execution History
  Status: "Waiting" (waiting for SCTASK 2)

  Check Catalog Tasks: New SCTASK "Configure Merchant in UPI Platform"
  assigned to Ravi Kumar should exist

STEP 7: Complete Task 2
  Log in as Ravi Kumar (or impersonate)
  Open the SCTASK: "Configure Merchant in UPI Platform"
  Set State: Closed Complete
  Save

STEP 8: Verify Completion
  Flow Designer → Execution History → Status: "Complete"
  RITM: State = Closed Complete, work notes show full history
  Email: Requester should have received completion email

TEST REJECTION SCENARIO:
  Repeat steps 1-2, but in step 3 select [Reject] instead of [Approve]
  Verify: RITM closes as Incomplete, rejection email sent
```

---

## Part 7: Create a Reusable Subflow

### What is a Subflow?

```
SUBFLOW = A reusable flow component with NO trigger.
  - Called by other flows (parent flows)
  - Accepts INPUT variables
  - Can return OUTPUT variables
  - Think of it like a function in programming

WHY USE SUBFLOWS?
  - DRY principle (Don't Repeat Yourself)
  - Consistent behavior across multiple flows
  - Easier maintenance — update once, applies everywhere
  - Modular design
```

### Build: "Send UPI Alert Notification" Subflow

```
STEP 1: Create New Subflow
  Flow Designer → [+ New] → Subflow
  Properties:
    Name:           Send UPI Alert Notification
    Description:    Reusable subflow to send alert notifications.
                    Sends email to specified recipient, adds work note
                    to related record, and escalates to management if critical.
    Application:    Global
  Click: [Submit]

STEP 2: Define Inputs
  Click: [+ Add Input]

  Input 1:
    Label:          Recipient
    Name:           recipient
    Type:           Reference → User [sys_user]
    Mandatory:      Yes

  Input 2:
    Label:          Subject
    Name:           subject
    Type:           String
    Mandatory:      Yes

  Input 3:
    Label:          Message
    Name:           message
    Type:           String
    Mandatory:      Yes

  Input 4:
    Label:          Priority Level
    Name:           priority_level
    Type:           String
    Mandatory:      Yes
    (Expected values: "Critical", "High", "Medium", "Low")

  Input 5:
    Label:          Related Record
    Name:           related_record
    Type:           Reference → Task [task]
    Mandatory:      No
    (Optional — if provided, a work note is added)

STEP 3: Build the Subflow Logic

  Action 3a: Send Email to Recipient
    Add Action: ServiceNow Core → Send Email
    Configure:
      To:       Inputs → Recipient → Email
      Subject:  [UPI Alert] [Inputs → Subject]
      Body:
        UPI Platform Alert Notification
        ================================

        Priority: [Inputs → Priority Level]

        [Inputs → Message]

        --------------------------------
        This is an automated alert from the NPCI UPI ITSM Platform.
        Please take appropriate action based on the priority level.

        For Critical alerts: Immediate action required.
        For High alerts: Action required within 1 hour.
        For Medium/Low alerts: Review at next available opportunity.

  Action 3b: Add Work Note (if related record provided)
    Add Flow Logic: If
    Condition:
      [Inputs → Related Record] [is not empty]
    Then:
      Add Action: ServiceNow Core → Update Record
      Record:     Inputs → Related Record
      Fields:
        Work notes:   [UPI Alert Sent]
                      Notification sent to: [Inputs → Recipient → Name]
                      Subject: [Inputs → Subject]
                      Priority: [Inputs → Priority Level]
                      Automated by Flow Designer subflow.

  Action 3c: Escalate to Management if Critical
    Add Flow Logic: If
    Condition:
      [Inputs → Priority Level] [is] [Critical]
    Then:
      Add Action: ServiceNow Core → Send Email
      To:       Sanjay Manager
      Subject:  [ESCALATION] [Inputs → Subject]
      Body:
        CRITICAL ALERT ESCALATION
        ==========================

        A critical alert has been generated and sent to
        [Inputs → Recipient → Name].

        Details:
        [Inputs → Message]

        As VP Engineering, you are being notified per NPCI
        escalation policy for all Critical-level alerts.

        Original Recipient: [Inputs → Recipient → Name]
        ([Inputs → Recipient → Email])

STEP 4: Save and Publish
  Click: [Save] → [Publish]

  NOTE: Subflows must be PUBLISHED (not just Activated) to be
  available for use in other flows.
```

### Using the Subflow in Other Flows

```
EXAMPLE: Using "Send UPI Alert Notification" in the SLA Breach Flow

Instead of manually configuring email + work note + escalation in every flow,
you can call the subflow:

  Add Action: Subflow → Send UPI Alert Notification
  Configure Inputs:
    Recipient:       Ravi Kumar
    Subject:         P2 SLA Breach on [Incident Number]
    Message:         The SLA for incident [Number] has breached.
                     Short description: [Short description]
                     Current assignment: [Assigned to]
    Priority Level:  High
    Related Record:  [The incident record]

This replaces multiple individual actions with a single subflow call.
Any future changes to the notification format only need to be made
in one place — the subflow.
```

---

## Part 8: Scheduled Flow — Weekly ITSM Summary Report

### Design

```
FLOW: Weekly UPI ITSM Summary

PURPOSE:  Every Monday at 8:00 AM IST, generate a summary of
          the past week's ITSM activity and email it to Management.

TRIGGER:  Weekly — Monday at 08:00 IST

LOGIC:
  Step 1: Count open P1 incidents
  Step 2: Count SLA breaches this week
  Step 3: Count changes completed this week
  Step 4: Count new problems created this week
  Step 5: Count catalog requests fulfilled this week
  Step 6: Compose and send summary email to Management group
```

### Step-by-Step Build

```
STEP 1: Create New Flow
  Flow Designer → [+ New] → Flow
  Properties:
    Name:           Weekly UPI ITSM Summary
    Description:    Generates and emails a weekly summary of ITSM metrics
                    to the Management group every Monday at 8 AM IST.
    Application:    Global
    Run As:         System User
  Click: [Submit]

STEP 2: Add Trigger — Weekly Schedule
  Click: [Add a trigger]
  Select: "Weekly" (under Schedule)
  Configure:
    Day:        Monday
    Time:       08:00
    Time zone:  Asia/Kolkata (IST)

STEP 3: Count Open P1 Incidents
  Add Action: ServiceNow Core → Lookup Records
  Configure:
    Table:      Incident [incident]
    Conditions:
      [Priority] [is] [1 - Critical]
      AND
      [State] [is not] [Closed]
      AND
      [State] [is not] [Resolved]

  Label this step: "Open P1 Incidents"

STEP 4: Count SLA Breaches This Week
  Add Action: ServiceNow Core → Lookup Records
  Configure:
    Table:      Task SLA [task_sla]
    Conditions:
      [Has breached] [is] [true]
      AND
      [Breach time] [on or after] [7 days ago] (relative)

  Label this step: "SLA Breaches This Week"

STEP 5: Count Changes Completed This Week
  Add Action: ServiceNow Core → Lookup Records
  Configure:
    Table:      Change Request [change_request]
    Conditions:
      [State] [is] [Closed]
      AND
      [Closed at] [on or after] [7 days ago]

  Label this step: "Changes Completed"

STEP 6: Count New Problems This Week
  Add Action: ServiceNow Core → Lookup Records
  Configure:
    Table:      Problem [problem]
    Conditions:
      [Opened at] [on or after] [7 days ago]

  Label this step: "New Problems"

STEP 7: Count Catalog Requests Fulfilled
  Add Action: ServiceNow Core → Lookup Records
  Configure:
    Table:      Requested Item [sc_req_item]
    Conditions:
      [State] [is] [Closed Complete]
      AND
      [Closed at] [on or after] [7 days ago]

  Label this step: "Fulfilled Requests"

STEP 8: Send Summary Email
  Add Action: ServiceNow Core → Send Email
  Configure:
    To:       Sanjay Manager (or the Management group email)
    Subject:  Weekly UPI ITSM Summary — Week of [current date]
    Body:
      ================================================================
      NPCI UPI Platform — Weekly ITSM Summary Report
      Generated: [current date/time]
      ================================================================

      KEY METRICS (Last 7 Days):
      ----------------------------------------------------------------
      Open P1 Incidents:        [Step 3 → Record Count]
      SLA Breaches:             [Step 4 → Record Count]
      Changes Completed:        [Step 5 → Record Count]
      New Problems:             [Step 6 → Record Count]
      Catalog Requests Fulfilled: [Step 7 → Record Count]
      ----------------------------------------------------------------

      ATTENTION ITEMS:
      - Open P1 incidents require immediate review if count > 0
      - SLA breaches indicate potential capacity or process issues
      - Review new problems for trending patterns

      ACTION REQUIRED:
      - Review the ITSM Dashboard for detailed breakdowns
      - Address any open P1 incidents in the daily standup
      - Ensure all SLA breaches have corrective action plans

      ================================================================
      This report was generated automatically by Flow Designer.
      For detailed data, visit the ITSM Dashboard in ServiceNow.
      ================================================================

  NOTE ON RECORD COUNTS:
    Flow Designer's Lookup Records action returns a list.
    The "Record Count" data pill gives you the number of records found.
    If your version does not expose a count pill, you can use a
    For Each loop with a counter variable, or use a Script action:

    Add Action: ServiceNow Core → Script
    Script:
      var count = 0;
      // Access the list from previous step and count
      // This depends on your exact Flow Designer version

STEP 9: Save and Activate
  Click: [Save] → [Activate]
```

---

## Part 9: Testing & Debugging Flows

### Flow Designer Test Mode

```
TESTING A FLOW:

Option 1: Test Button (for any flow)
  Open the flow in Flow Designer
  Click: [Test] (top right)

  For record-triggered flows:
    You will be prompted to select or create a record
    The flow runs immediately against that record

  For scheduled flows:
    The flow runs immediately (ignoring the schedule)
    Useful for testing without waiting for the schedule

  For catalog-triggered flows:
    You will be prompted to select a RITM

Option 2: Create a Real Record
  Create an incident/request/etc. that matches the trigger conditions
  The flow triggers automatically
  Check Execution History for the run

Option 3: REST API Trigger (for advanced testing)
  Some flows can be triggered via REST API
  Useful for integration testing
```

### Viewing Execution History

```
EXECUTION HISTORY:

Navigation: Flow Designer → Execution History tab

EXECUTION LIST VIEW:
+------------------------------------------------------------------------+
| Flow Name                    | Status    | Started       | Duration    |
+------------------------------------------------------------------------+
| UPI Incident Auto-Assignment | Complete  | 2026-09-23... | 234 ms      |
| SLA Breach Escalation        | Complete  | 2026-09-23... | 1,204 ms    |
| Merchant Onboarding          | Waiting   | 2026-09-22... | (ongoing)   |
| Auto-Close Resolved          | Complete  | 2026-09-23... | 5,432 ms    |
| Weekly ITSM Summary          | Error     | 2026-09-22... | 102 ms      |
+------------------------------------------------------------------------+

EXECUTION STATUSES:
  Complete     → Flow finished successfully (green)
  Waiting      → Flow is paused (approval, wait condition) (blue)
  In Progress  → Flow is currently executing (blue spinner)
  Error        → Flow encountered an error (red)
  Cancelled    → Flow was manually cancelled (grey)

EXECUTION DETAIL VIEW:
  Click any execution to see the step-by-step trace:

  +----------------------------------------------------------+
  | Execution Detail: UPI Incident Auto-Assignment            |
  +----------------------------------------------------------+
  | Trigger: Record Created                                    |
  |   Record: INC0010042                                       |
  |   Time: 2026-09-23 14:32:01                                |
  |   Status: OK                                               |
  +----------------------------------------------------------+
  | Step 1: If (P1 UPI Incident)                               |
  |   Condition evaluated: TRUE                                |
  |   Category = UPI: true                                     |
  |   Priority = 1: true                                       |
  +----------------------------------------------------------+
  | Step 1.1: Update Record                                    |
  |   Record: INC0010042                                       |
  |   Assignment group: Platform Engineering                   |
  |   Assigned to: Ravi Kumar                                  |
  |   Work notes: [Auto-Assigned]...                           |
  |   Status: OK                                               |
  +----------------------------------------------------------+

  Each step shows:
    - Input values (what data pills resolved to)
    - Output values (what the action produced)
    - Status (OK or Error)
    - Duration (milliseconds)
```

### Debugging Common Errors

```
COMMON FLOW ERRORS AND FIXES:

1. "Record not found"
   Cause:   Lookup Record returned no results, and the next action
            tried to use the empty data pill
   Fix:     Add an IF condition after Lookup to check if record exists
            before proceeding

   Example:
     Step 2: Lookup Record (Incident)
     Step 3: IF [Step 2 → Incident Record] [is not empty]
               THEN: proceed with actions
               ELSE: Log "No record found, skipping"

2. "Insufficient rights"
   Cause:   Flow running as a user without permissions on the table
   Fix:     Change "Run As" to System User in flow properties
            Or grant the necessary roles to the user

3. "Invalid reference"
   Cause:   Data pill references a record that was deleted or
            a reference field that is empty
   Fix:     Add null checks before dot-walking through references

4. "Flow not triggering"
   Possible causes:
     a. Flow is in Draft state (not Activated)
     b. Trigger conditions don't match the record
     c. Another Business Rule changes the record before the flow processes
     d. Flow is deactivated

   Debug steps:
     - Verify flow status is "Active"
     - Check trigger conditions match your test data exactly
     - Check System Logs: All > System Logs > System Log > All
     - Look for flow-related errors in the log

5. "Wait condition never resolves"
   Cause:   The condition can never become true (wrong field/value)
   Fix:     Review the Wait for Condition configuration
            Set a timeout to prevent indefinite waiting
            Check if the expected record update is actually happening

6. "Duplicate actions / flow running twice"
   Cause:   "Created or Updated" trigger firing on both insert and
            the subsequent auto-update by the flow itself
   Fix:     Use "Created" trigger (not "Created or Updated")
            OR add condition: [Updated by] [is not] [system]
            OR add "Run once per record" option if available

7. "Email not sending"
   Cause:   Email properties not configured on PDI
   Fix:     Check: System Properties > Email Properties
            Ensure outbound email is enabled
            On PDI: emails may be captured in the email log
            rather than actually sent
            Check: All > System Mailboxes > Outbound > Sent
```

### Performance Considerations

```
PERFORMANCE BEST PRACTICES:

1. TRIGGER CONDITIONS — Filter early
   BAD:   Trigger on ALL incident creates, then use IF to check category
   GOOD:  Trigger on incidents WHERE Category = UPI (filter in trigger)
   WHY:   Trigger conditions are evaluated efficiently by the platform.
          Flow logic runs inside the flow engine — more overhead.

2. LOOKUP RECORDS — Be specific
   BAD:   Lookup all incidents, then For Each to find the right one
   GOOD:  Lookup records with precise conditions
   WHY:   Database queries are faster than iteration in flow logic.

3. FOR EACH — Avoid large loops
   CAUTION: For Each loops over thousands of records can time out
   LIMIT:   Use conditions to narrow the result set
   BATCH:   For large operations, consider Scheduled Scripts instead

4. UPDATE RECORD — Minimize updates
   BAD:   5 separate Update Record actions on the same record
   GOOD:  1 Update Record action setting all 5 fields
   WHY:   Each Update Record triggers Business Rules, which adds overhead.

5. SUBFLOWS — Use for repeated patterns
   If you find the same 3-4 actions repeated in multiple flows,
   extract them into a subflow. Reduces maintenance and improves
   consistency.

6. WAIT CONDITIONS — Set timeouts
   Always set a timeout on Wait for Condition actions.
   Without a timeout, a flow can remain in "Waiting" state indefinitely,
   consuming resources.

7. TESTING — Always test in sub-production
   Test flows in your PDI or dev instance before activating in production.
   Use the Test button rather than creating real records when possible.
```

---

## Part 10: Migrating Legacy Workflows to Flow Designer

```
WHY MIGRATE?
  - Legacy Workflow Editor is in maintenance mode
  - Flow Designer is ServiceNow's strategic automation platform
  - Flow Designer has better debugging, subflows, and Integration Hub
  - New features are only added to Flow Designer

MIGRATION APPROACH:

Step 1: Inventory Legacy Workflows
  Navigation: All > Workflow > Workflow Editor
  List all active workflows
  Categorize by:
    - Complexity (simple / medium / complex)
    - Table (incident, change, sc_req_item, etc.)
    - Usage frequency

Step 2: Prioritize Migration
  Start with:
    - Simple workflows (approval + notification)
    - High-frequency workflows
    - Workflows with known issues

  Defer:
    - Complex workflows with many conditions
    - Rarely-used workflows
    - Workflows with custom script activities

Step 3: Rebuild in Flow Designer
  For each workflow:
    a. Document the trigger, conditions, and actions
    b. Recreate in Flow Designer
    c. Test thoroughly
    d. Run both in parallel briefly (if possible)
    e. Deactivate the legacy workflow
    f. Monitor Flow Designer version for issues

Step 4: Mapping Legacy to Flow Designer
  +---------------------------+-------------------------------+
  | Legacy Workflow           | Flow Designer Equivalent      |
  +---------------------------+-------------------------------+
  | Workflow trigger          | Flow trigger                  |
  | If activity               | If flow logic                 |
  | Approval activity         | Ask for Approval action       |
  | Notification activity     | Send Email action             |
  | Create Task activity      | Create Record action          |
  | Timer activity            | Wait flow logic               |
  | Run Script activity       | Script action (custom)        |
  | Catalog task activity     | Create Record (sc_task)       |
  | Set Values activity       | Update Record action          |
  +---------------------------+-------------------------------+

IMPORTANT: Do NOT delete legacy workflows immediately.
  Keep them deactivated for 30 days as rollback insurance.
```

---

## Practice Exercises

### Exercise 1: Auto-Assign Problems Based on Category

```
BUILD: "UPI Problem Auto-Assignment"

Requirements:
  - Trigger: When a Problem record is Created
  - IF Category = "UPI":
    → Assign to Platform Engineering, Assigned to Ravi Kumar
  - IF Category = "Network":
    → Assign to Network Operations
  - ELSE:
    → Assign to Service Desk
  - Always add a work note indicating auto-assignment

Test:
  Create problems with different categories and verify assignment.

HINTS:
  - This is very similar to the Incident Auto-Assignment flow
  - Table is Problem [problem] instead of Incident [incident]
  - Problem priorities work differently — consider using Impact/Urgency
```

### Exercise 2: CI Status Change Creates Incident

```
BUILD: "CI Non-Operational Alert"

Requirements:
  - Trigger: When a CMDB CI [cmdb_ci] record is Updated
  - Condition: Operational Status changes to "Non-Operational"
  - Actions:
    1. Create Incident:
       Caller:             System (or Vijay Admin)
       Category:           UPI (or based on CI class)
       Short description:  CI [CI Name] is Non-Operational
       Description:        The CI [CI Name] (Class: [CI Class]) has been
                           marked as Non-Operational. Automatic incident
                           created for investigation.
                           CI Sys ID: [CI sys_id]
                           Previous Status: [previous operational status]
       Priority:           2 - High
       Assignment group:   Platform Engineering
    2. Send email to Ravi Kumar about the new incident
    3. Add work note on the CI record: "Incident [INC number] created
       due to Non-Operational status change"

Test:
  Find a CI in the CMDB, change its Operational Status to Non-Operational.
  Verify the incident is created with correct details.

HINTS:
  - Use the "Updated" trigger with condition on Operational Status
  - After Create Record (incident), the output gives you the INC number
  - Use that INC number data pill in the work note on the CI
```

### Exercise 3: Standard Change from Template Subflow

```
BUILD SUBFLOW: "Create Standard Change from Template"

Inputs:
  - template_name (String) — name of the standard change template
  - requested_by (Reference: sys_user)
  - scheduled_start (Date/Time)
  - scheduled_end (Date/Time)

Logic:
  1. Lookup the Standard Change Template by name
  2. IF template found:
     - Create Change Request:
       Type:              Standard
       Short description: [Template short description]
       Description:       [Template description]
       Category:          [Template category]
       Requested by:      [Input: requested_by]
       Scheduled start:   [Input: scheduled_start]
       Scheduled end:     [Input: scheduled_end]
       Assignment group:  [Template assignment group]
       State:             Scheduled (standard changes skip approval)
     - Return the Change Request record as output
  3. IF template NOT found:
     - Log error: "Template not found: [template_name]"
     - Return empty

Outputs:
  - change_record (Reference: change_request) — the created change

Test:
  Create a parent flow that calls this subflow with a known template name.
  Verify the change request is created correctly.
```

### Exercise 4: Expiring SLA Warning Flow

```
BUILD: "Daily SLA Expiration Warning"

Requirements:
  - Trigger: Scheduled — Daily at 07:00 IST
  - Logic:
    1. Lookup all Task SLAs WHERE:
       - Has breached = false
       - Percentage >= 75
       - Stage = In Progress
    2. For Each Task SLA:
       - Lookup the related incident
       - Send email to the Assigned to user:
         Subject: "SLA Warning: 75%+ elapsed on [INC number]"
         Body: Include SLA name, percentage, time remaining
       - Add work note on incident:
         "SLA Warning: [SLA Name] is [percentage]% elapsed.
          Remaining time: [time remaining].
          Please prioritize resolution."

Test:
  Create an incident with a short SLA
  Wait until it passes 75% but not 100%
  Run the flow manually via Test button
  Verify warning email and work note

HINTS:
  - The Task SLA table has a "percentage" field
  - Use Lookup Records with percentage >= 75
  - Dot-walk from Task SLA → Task to get the incident
```

### Exercise 5: Emergency Change Approval Flow

```
BUILD: "Emergency Change Auto-Approval Flow"

Requirements:
  - Trigger: When Change Request is Created
  - Condition: Type = Emergency
  - Logic:
    1. Check who submitted the change:
       IF Requested by → is member of → Platform Engineering group:
         → Auto-approve:
           - Set Approval = Approved
           - Set State = Implement
           - Add work note: "Emergency change auto-approved.
             Submitted by Platform Engineering member [name].
             Per NPCI policy, Platform Engineering emergency changes
             are auto-approved with post-implementation review."
         → Send email to Sanjay Manager:
           "FYI: Emergency change [CHG number] auto-approved for
            Platform Engineering. Post-implementation review required."
       ELSE:
         → Request approval from Sanjay Manager (Ask for Approval)
         → IF Approved:
           - Set State = Implement
           - Add work note: "Emergency change approved by VP Engineering"
         → IF Rejected:
           - Set State = Closed
           - Add work note: "Emergency change rejected by VP Engineering.
             Reason: [approval comments]"
           - Send email to requester with rejection details

Test:
  Scenario A: Create emergency change as Ravi Kumar (Platform Eng)
    → Should auto-approve
  Scenario B: Create emergency change as Meera Joshi (Service Desk)
    → Should require Sanjay Manager approval

HINTS:
  - To check group membership, use Lookup Record on sys_user_grmember table
    Condition: User = [requested by] AND Group = [Platform Engineering]
  - If the lookup returns a record → user is a member
  - If empty → user is not a member
```

---

## Summary and Key Takeaways

```
FLOWS BUILT IN THIS LAB:
+----+--------------------------------------+-------------+------------------+
| #  | Flow Name                            | Trigger     | Type             |
+----+--------------------------------------+-------------+------------------+
| 1  | UPI Incident Auto-Assignment         | Record      | Assignment       |
| 2  | UPI SLA Breach Escalation            | Record      | Escalation       |
| 3  | Auto-Close Resolved Incidents        | Schedule    | Lifecycle mgmt   |
| 4  | Merchant Onboarding Approval Flow    | Catalog     | Fulfillment      |
| 5  | Send UPI Alert Notification          | (Subflow)   | Reusable         |
| 6  | Weekly UPI ITSM Summary              | Schedule    | Reporting        |
+----+--------------------------------------+-------------+------------------+

KEY CONCEPTS MASTERED:
  - ITIL 4 "Optimize and Automate" principle applied to real ITSM processes
  - Flow Designer components: Triggers, Actions, Flow Logic, Subflows
  - Data pills and dot-walking for dynamic data
  - Record triggers vs Schedule triggers vs Catalog triggers
  - Conditional logic: If/Then/Else If/Else
  - Loops: For Each for batch processing
  - Wait conditions for sequential task orchestration
  - Approval actions for request management
  - Subflows for reusable automation components
  - Testing with Test button and Execution History
  - Debugging with step-by-step execution traces
  - Performance best practices
  - Migration path from Legacy Workflows

AUTOMATION IMPACT AT NPCI:
  Before:
    - P1 incidents sat unassigned for 5-10 minutes
    - SLA breaches discovered hours after the fact
    - Resolved incidents lingered for weeks
    - Catalog fulfillment required manual coordination
    - Weekly reports compiled manually every Monday morning

  After:
    - P1 incidents assigned in < 1 second
    - SLA breaches escalated instantly
    - Resolved incidents auto-closed per policy
    - Catalog fulfillment fully orchestrated
    - Weekly reports delivered automatically at 8 AM
```

---

## What's Next

```
Lab 21: Reporting & Performance Analytics
  - Build ITSM dashboards with real-time metrics
  - Create KPI indicators for incident, problem, and change
  - Performance Analytics widgets and trend analysis
  - Executive reporting for NPCI management

Lab 22: Integration & REST APIs
  - Integrate ServiceNow with external systems
  - Build REST API endpoints
  - Integration Hub spokes
  - Webhook-based event processing
```

---

**End of Lab 20**
