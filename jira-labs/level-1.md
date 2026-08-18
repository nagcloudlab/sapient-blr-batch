# JIRA Lab — Level 1: Space, Roles & Backlog Setup

> **Domain**: MTS (Money Transfer System)
> **Time**: ~90 minutes
> **Prerequisite**: SDLC & STLC concepts from Day 1

---

### Yesterday's Recap

| Concept | Key Takeaway |
|---------|-------------|
| SDLC | Business Need → Requirements → Design → Development → Testing → Deployment → Maintenance |
| Methodologies | Waterfall (sequential) → V-Model (test-aligned) → Agile (iterative, sprints) |
| STLC | Requirement Analysis → Test Planning → Test Design → Env Setup → Execution → Defect Reporting → Closure |
| Requirements | BRD (WHY) → FRD (WHAT it does) → SRS (WHAT exactly) |
| Agile Requirements | User Stories + Acceptance Criteria replace heavyweight docs |
| Traceability | Every requirement → test case → evidence (RTM) |
| Shift-Left | Find defects early — a conversation in requirements saves a production incident |

> Today we bring all of this to life in **JIRA** — the tool Agile teams use to manage SDLC, track STLC, and deliver software.
>
> You will play **all roles** (PO, Dev, QA, SM) to experience the full workflow end to end.

---

## Lab 1.1 — Log In & Explore the Interface

### What is JIRA?

- Atlassian's project & issue tracking tool — used by most software teams
- Supports Agile frameworks: Scrum (sprints) and Kanban (continuous flow)
- Manages the full SDLC: plan (backlog) → build (sprints) → test (bugs) → release (versions)
- Provides visibility: boards, timelines, reports, dashboards

### Space vs Project — A Naming Clarification

- Atlassian recently renamed **"Project"** to **"Space"** in the top navigation
- However, many places inside JIRA still say "Project":
  - JQL queries use `project = MTS`
  - URLs show `/projects/MTS`
  - Settings page says "Project settings"
- **They are the same thing** — just a naming transition in progress
- This lab uses both terms interchangeably

### Lab Steps

1. Open your browser → go to `https://your-org.atlassian.net`
2. Enter your email → click **Continue**
3. Enter your password → click **Log in**
4. You land on the **Home** page
5. Observe the top navigation bar:
   - **Spaces** — all your team workspaces
   - **Goals** — OKRs and objectives
   - **Teams** — team management
   - **Plans** — cross-team planning
   - **Create** button — quick-create any issue
   - **Search** icon (or press `/`) — global search
   - **Bell** icon — notifications
   - **Your avatar** — profile & settings
6. Click your **avatar** (top-right) → click **Personal settings**
7. Configure:
   - Time zone → `(GMT+05:30) India Standard Time`
   - Language → `English`
   - Theme → your preference
8. Click **Save changes**

---

## Lab 1.2 — Create the MTS Space

### Why?

- Every software project needs a workspace
- The space holds all issues, boards, sprints, and reports
- Choosing **Scrum** gives us sprints, backlog, and velocity tracking — Agile in action

### Lab Steps

1. Click **Spaces** in the top navigation
2. Click **Create space** (top-right)
3. Select the **Scrum** template
4. Fill in:
   - **Name**: `MTS - Money Transfer System`
   - **Key**: `MTS`
   - **Access**: keep default
5. Click **Create**
6. You are now inside the MTS space
7. Explore the **left sidebar** — click each item to preview:

| Sidebar Item | Purpose | Who Uses It |
|-------------|---------|-------------|
| Summary | Space overview, recent activity | Everyone |
| List | Flat table of all issues | PO, SM |
| Board | Visual columns: To Do → In Progress → Done | Dev, QA (daily standup) |
| Backlog | All unplanned work + sprint planning | PO, SM |
| Timeline | Gantt chart — epics and stories as bars | Managers, PO |
| Calendar | Issues plotted by due date | Everyone |
| Reports | Burndown, velocity, cumulative flow | SM, Managers |
| Space settings | Workflows, permissions, issue types | Admin |

> **SDLC connection**: This space is where the team executes the full SDLC. Each sidebar item supports a different stage or role.

---

## Lab 1.3 — Understand Team Roles

### Why?

- In a real project, different people play different roles
- In this lab, **you will play all roles** to experience the full workflow
- Understanding each role helps you see how JIRA connects different SDLC activities

### Roles in a Scrum Team

| Role | Responsibility | JIRA Activities |
|------|----------------|-----------------|
| **Product Owner (PO)** | Owns the backlog, writes stories, defines acceptance criteria, prioritizes | Creates Epics & Stories, orders backlog |
| **Developer (Dev)** | Implements features, writes unit tests, reviews code | Picks up stories, creates child issues, transitions to Done |
| **QA / Test Engineer** | Reviews requirements, writes test cases, tests features, reports bugs | Comments on stories, creates Bug issues, verifies fixes |
| **Scrum Master (SM)** | Facilitates ceremonies, manages sprints, removes blockers | Creates sprints, tracks board, generates reports |

### In This Lab

- You are **one person playing all four roles**
- When the lab says *"PO creates an epic"* — that's you, wearing the PO hat
- When it says *"QA raises a question"* — that's you, switching to QA thinking
- This simulates how the team collaborates in JIRA

---

## Lab 1.4 — PO Creates the First Epic

### The Scenario

You are the **Product Owner**. You've received a business requirement:

> *"Customers should be able to transfer money between accounts."*

Yesterday we learned: one sentence is business intent — not a testable specification. You create an **Epic** to represent this large initiative.

### What is an Epic?

- A large body of work that spans multiple sprints
- Maps to a **BRD-level objective** — high-level business capability
- Contains Stories, Tasks, and Bugs as children
- Owned by the Product Owner

### Lab Steps

1. Click **Create** (blue button, top navigation)
2. Fill in:
   - **Issue Type**: Epic
   - **Summary**: `Fund Transfer Module`
   - **Description**:
     ```
     Business Objective (from BRD):
     Enable customers to initiate secure domestic money transfers.

     Scope:
     - Transfer modes: UPI, NEFT, IMPS, RTGS
     - Validations: balance check, active accounts, different accounts
     - Transaction tracking with unique reference ID
     - Success/failure notifications

     Out of Scope:
     - International transfers, forex
     - Batch payroll processing
     ```
   - **Priority**: High
3. Click **Create**
4. A toast notification appears — note the issue key (e.g., MTS-1)
5. Click the notification to open the epic
6. Observe:
   - **Status**: TO DO
   - **Child issues**: empty (no stories yet)
   - **Activity**: shows the creation event

> **Important**: JIRA auto-generates issue keys (MTS-1, MTS-2, ...) in creation order. Your keys may differ from someone else's — that's normal. Always refer to issues by their **summary name**, not just the key.

> **BRD connection**: This epic represents the BRD objective: *"Enable customers to initiate secure domestic money transfers."* The BRD defines WHY — the epic in JIRA is where the team tracks the execution.

---

## Lab 1.5 — PO Breaks the Epic into Stories

### The Scenario

Still wearing the **PO hat**, you break the epic into **user stories** — each representing a specific user-facing capability with testable **acceptance criteria**.

### What is a Story?

- A user-facing requirement written from the user's perspective
- Format: *"As a [user], I want [capability], so that [value]"*
- The Agile replacement for formal FRD/SRS documents
- Must include **Acceptance Criteria** — the testable conditions that define "done"
- Estimated in **Story Points** — relative effort (Fibonacci: 1, 2, 3, 5, 8, 13)
  - Points measure **complexity**, not hours
  - A 5-point story is roughly 2-3x the effort of a 2-point story

### Lab Steps — Story 1: UPI Transfer

1. Click **Create**
2. Fill in:
   - **Issue Type**: Story
   - **Summary**: `As a user, I want to transfer money via UPI so that I can make instant payments`
   - **Description**:
     ```
     Acceptance Criteria:
     - User can select source and destination accounts from a dropdown
     - Source and destination accounts must be different
     - Amount must be between INR 1.00 and INR 10,00,000.00
     - On success: display transaction reference ID and transferred amount
     - On failure: display a specific, actionable error message
     ```
   - **Parent / Epic Link**: search `Fund Transfer Module` → select it
   - **Story Points**: `5`
   - **Priority**: High
3. Click **Create**
4. Note the issue key from the notification

### Lab Steps — Story 2: View Balance

1. Click **Create**
2. Fill in:
   - **Issue Type**: Story
   - **Summary**: `As a user, I want to view my account balance so that I can check funds before transferring`
   - **Description**:
     ```
     Acceptance Criteria:
     - Dashboard displays all user accounts as cards
     - Each card shows: account number, owner name, account type (SAVINGS/CURRENT), balance in INR
     - Account data refreshes automatically after a successful transfer
     ```
   - **Parent / Epic Link**: `Fund Transfer Module`
   - **Story Points**: `3`
   - **Priority**: High
3. Click **Create**
4. Note the issue key

### Verify the Epic-Story Relationship

1. Click **Backlog** in the sidebar
2. Toggle the **Epic Panel** (left side) → click `Fund Transfer Module`
3. Both stories should appear under this epic
4. Alternatively: open the Epic → scroll to **Child issues** → verify both stories are listed

> **FRD connection**: Yesterday's FRD requirement: *"System shall validate sender account is active and has sufficient balance before processing."* Today: that same requirement lives as acceptance criteria in the UPI transfer story.

---

## Lab 1.6 — Dev Raises a Need: Add a Technical Task

### The Scenario

Now switch to the **Developer hat**. You realize:

> *"We can't build the transfer feature without the database. We need the schema and seed data first."*

This is technical/infrastructure work — not user-facing. It's a **Task**, not a Story.

### What is a Task?

- A work item for technical, internal, or non-functional work
- Does not use the "As a user..." format — it's not user-facing
- Examples: database setup, CI/CD pipeline, environment config, documentation
- Still needs clear **done criteria**

### Lab Steps

1. Click **Create**
2. Fill in:
   - **Issue Type**: Task
   - **Summary**: `Set up MySQL database schema and seed data`
   - **Description**:
     ```
     Done Criteria:
     - Tables created: users, accounts, transactions
     - Constraints added: balance >= 0, amount > 0, from_account != to_account
     - Seed data inserted: 3 users (ravi.kumar, priya.sharma, amit.patel), 5 accounts
     - Verified: application connects and runs queries successfully
     - Reference: database/schema.sql
     ```
   - **Parent / Epic Link**: `Fund Transfer Module`
   - **Priority**: High
3. Click **Create**
4. Note the issue key

> **STLC connection**: This task maps to **STLC Stage 4 — Test Environment Setup**. Yesterday: *"The most carefully written test case produces meaningless results if the environment is wrong."* Without the database, no feature can be built or tested.

---

## Lab 1.7 — Link Dependencies Between Issues

### The Scenario

The UPI transfer story **cannot start** until the database task is done — the API needs tables to read from and write to. You capture this as an **issue link**.

### What is Issue Linking?

- Creates explicit **relationships** between issues
- Makes dependencies visible to the entire team
- Prevents confusion during sprint planning
- Implements **traceability** — the RTM concept from yesterday

### Common Link Types

| Link Type | Meaning | Example |
|-----------|---------|---------|
| blocks / is blocked by | Must be done first | DB task blocks UPI story |
| is caused by / causes | Bug traced to a story | Bug caused by transfer implementation |
| relates to | General relationship | Two stories sharing a component |

### Lab Steps

1. Open the **UPI transfer story** (find it in Backlog or List → click to open)
2. Click **Link** (in the toolbar or under the `...` menu)
3. In the dialog:
   - **Link type**: `is blocked by`
   - **Issue**: type `database` or `schema` → select the database task
4. Click **Link**
5. Verify on the UPI transfer story:
   - Linked Issues shows: *is blocked by — Set up MySQL database schema...*
6. Open the **database task** → verify:
   - Linked Issues shows: *blocks — As a user, I want to transfer money via UPI...*

> **RTM connection**: Yesterday: *"Every requirement links forward to evidence. Every test links back to a requirement."* Issue links create this traceability chain in JIRA.

---

## Lab 1.8 — Add Labels & Dates

### Why?

- **Labels** are tags for categorizing and filtering issues (e.g., `backend`, `frontend`)
- **Dates** enable timeline and calendar views, and help track deadlines
- These metadata fields become powerful when combined with JQL search

### Lab Steps — Add Labels

1. Open the **UPI transfer story** → Labels field → type `backend` → press Enter
2. Open the **View balance story** → Labels → add `frontend`
3. Open the **database task** → Labels → add `backend`, `database`

### Lab Steps — Set Due Date

The database task starts first (it blocks everything else):

1. Open the **database task**
2. **Due date** → select 2 days from now

> **Tip**: The Start date field may not be available in all project types. Due date is always available and is the key field for Timeline and Calendar views.

---

## Lab 1.9 — Prioritize the Backlog

### What is the Backlog?

- The **ordered list of all work** in the space
- Items at the top are highest priority — pulled into sprints first
- The **Product Owner** owns the priority order
- Risk-based thinking: high impact + high probability = top priority

### Lab Steps

1. Click **Backlog** in the sidebar
2. You should see all issues listed
3. **Drag and drop** to reorder:

| Priority | Issue | Reasoning |
|----------|-------|-----------|
| 1st | DB schema task | Foundation — everything depends on it |
| 2nd | UPI transfer story | Core business feature, highest value |
| 3rd | View balance story | Supports the transfer flow, not blocking |

4. Toggle the **Epic Panel** (left side) → click `Fund Transfer Module` to filter
5. Try the **Only My Issues** filter

> **Agile connection**: This is the Scrum **Product Backlog** — an ordered, living list of everything the product needs. The PO refines it continuously.

---

## Lab 1.10 — QA Reviews Requirements (Shift-Left)

### The Scenario

Switch to the **QA hat**. You review the UPI transfer story **before the sprint starts** and find gaps in the acceptance criteria.

### Why This Matters

- This is **STLC Stage 1: Requirement Analysis** happening in JIRA
- Yesterday: *"Six questions QA asks — Clear? Complete? Consistent? Feasible? Testable? Error paths?"*
- Catching ambiguity **now** costs a conversation — catching it in production costs an incident

### Lab Steps

1. Open the **UPI transfer story**
2. Scroll to **Activity** → click **Comments** tab
3. Type:

```
QA Review — Questions before writing test cases:

1. What happens if the sender's account is INACTIVE?
   Should we show a specific error message?

2. Should "insufficient balance" and "account inactive" show
   DIFFERENT error messages? Or a generic one?

3. What if someone tries to transfer to their OWN account
   (same source and destination)?

4. What is the expected response time? Needed for
   performance test cases. (NFR)

These must be clarified before sprint starts.
```

4. Click **Save**

---

## Lab 1.11 — PO Refines the Story Based on QA Feedback

### The Scenario

Switch back to the **PO hat**. You respond to the QA questions and update the story with refined acceptance criteria.

### Lab Steps — Reply to the Comment

1. On the UPI transfer story, scroll to the QA comment → click **Reply**
2. Type:

```
Answers to QA review:

1. Inactive sender → error: "Account is inactive, please contact support"
2. Yes — different error messages for each failure case
3. Same account → error: "Cannot transfer to the same account"
4. NFR: Transfer must complete within 3 seconds under normal load
   (up to 500 concurrent users)

Updating acceptance criteria now.
```

3. Click **Save**

### Lab Steps — Update the Story Description

1. Click the **Description** field to edit
2. Add at the bottom of existing acceptance criteria:

```
Refined Criteria (from QA review):
- Inactive sender account → error: "Account is inactive, please contact support"
- Insufficient balance → error: "Insufficient balance in account [ACC_NUMBER]"
- Same account transfer → error: "Cannot transfer to the same account"
- Transfer completes within 3 seconds under normal load (500 concurrent users) [NFR]
```

3. Click **Save**

### What Just Happened?

- You played both PO and QA — simulating real team collaboration
- The story now has **functional** (what it does) and **non-functional** (how fast) criteria
- In Waterfall, this would be a formal change request. In Agile, it's a comment + description update.

---

## Lab 1.12 — Explore Different Views

### Why Multiple Views?

Different views serve different roles and purposes — same data, presented differently.

### Lab Steps

**Board** (sidebar → Board):
1. Observe columns: **TO DO | IN PROGRESS | DONE**
2. All issues should be in TO DO
3. Drag the database task to IN PROGRESS — status updates automatically
4. Drag it back to TO DO (we'll start properly in Level 2)
5. *Use case*: Daily standup — team walks the board right to left

**List** (sidebar → List):
1. See all issues in a spreadsheet-style table
2. Try **Group by** → Epic — issues nest under "Fund Transfer Module"
3. Try **Sort by** → Priority — highest first
4. *Use case*: PO reviewing backlog, bulk editing

**Timeline** (sidebar → Timeline):
1. Epic displayed as a bar with child stories nested below
2. Database task shows its start/due date range
3. Drag bar edges to adjust dates visually
4. *Use case*: Release planning, dependency visualization

**Calendar** (sidebar → Calendar):
1. Database task appears on its due date
2. Switch between Month and Week views
3. *Use case*: Deadline tracking, sprint boundary planning

---

## Lab 1.13 — Search with Keywords & JQL

### What is JQL?

- **Jira Query Language** — SQL-like syntax for searching issues
- Format: `field operator value [AND/OR] field operator value [ORDER BY field]`
- Powers filters, dashboards, and reports
- Note: JQL uses `project` (not `space`) — part of the naming transition

### Lab Steps — Basic Search

1. Press `/` (or click the Search icon)
2. Type: `transfer`
3. The UPI transfer story appears in results
4. Click to open it

### Lab Steps — JQL Queries

1. Click Search → switch to **Advanced** / JQL mode
2. Try each query:

| Query | What It Returns |
|-------|----------------|
| `project = MTS` | All issues in MTS |
| `project = MTS AND type = Story` | Only stories |
| `project = MTS AND type = Task` | Only tasks |
| `project = MTS AND type = Epic` | Only epics |
| `project = MTS AND priority = High` | High priority items |
| `project = MTS AND labels = "backend"` | Backend-labeled issues |
| `project = MTS AND summary ~ "transfer"` | Issues with "transfer" in title |
| `project = MTS AND created >= startOfDay()` | Issues created today |

### Lab Steps — Save a Filter

1. Run: `project = MTS AND type = Story`
2. Click **Save as**
3. Name: `MTS - All Stories`
4. Click **Save**
5. Access anytime: top nav → **Filters** → **My Filters**

> Saved filters are reusable — they power dashboards, notifications, and team reports.

---

## Summary — What We Built

### Issues Created

| Type | Summary | Labels | Status |
|------|---------|--------|--------|
| Epic | Fund Transfer Module | — | TO DO |
| Story | Transfer money via UPI | `backend` | TO DO |
| Story | View account balance | `frontend` | TO DO |
| Task | Set up MySQL schema & seed data | `backend`, `database` | TO DO |

### What We Also Did

- Understood team roles: PO, Dev, QA, Scrum Master
- Linked dependency: UPI story **is blocked by** DB task
- Prioritized backlog: DB task → UPI story → Balance story
- QA reviewed acceptance criteria and raised questions (shift-left)
- PO refined the story with additional criteria + NFR
- Explored 4 views: Board, List, Timeline, Calendar
- Wrote JQL queries and saved a filter
- **No bugs yet** — those naturally appear in Level 2 when QA starts testing

---

## JIRA ↔ Yesterday's Concepts

| What We Did in JIRA | SDLC/STLC Concept |
|---------------------|-------------------|
| Created a Scrum space | Agile methodology — iterative, sprint-based delivery |
| Understood team roles | SDLC roles — PO, Dev, QA, Scrum Master |
| Created an Epic | BRD — high-level business objective |
| Wrote Stories with Acceptance Criteria | FRD → User Stories — functional requirements in Agile |
| Added NFR to story description | SRS — non-functional requirements (response time < 3s) |
| QA commented with questions | STLC Stage 1 — Requirement Analysis |
| PO updated story from QA feedback | Shift-Left — catching defects early saves cost |
| Created a Task for DB setup | STLC Stage 4 — Test Environment Setup |
| Linked "is blocked by" | RTM — Requirements Traceability Matrix |
| Prioritized backlog | Risk-based prioritization (impact × probability) |
| Saved a JQL filter | Reusable query for tracking requirements |

---

## Checklist

- [ ] Logged in and explored JIRA navigation
- [ ] Understood Space = Project (naming transition)
- [ ] Created Scrum space: `MTS`
- [ ] Understood team roles: PO, Dev, QA, SM
- [ ] (As PO) Created 1 Epic: Fund Transfer Module
- [ ] (As PO) Created 2 Stories with acceptance criteria and story points
- [ ] (As Dev) Created 1 Task with done criteria
- [ ] Linked dependency: UPI story blocked by DB task
- [ ] Added labels: `backend`, `frontend`, `database`
- [ ] Set start/due dates on the database task
- [ ] Prioritized backlog via drag-and-drop
- [ ] (As QA) Reviewed requirements via comments — shift-left
- [ ] (As PO) Refined story with clearer criteria + NFR
- [ ] Explored Board, List, Timeline, Calendar views
- [ ] Ran JQL queries and saved a filter

---

## What's Next?

**Level 2** — Sprint Planning & Execution:
- Create a sprint and pull items from backlog
- Start the sprint
- Break stories into child issues
- Transition work: TO DO → IN PROGRESS → DONE
- QA tests and finds the first bugs
- Defect reporting and linking
- Sprint completion and reports (burndown, velocity)
