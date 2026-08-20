# JIRA Lab — Level 3: Dashboards, Confluence & SDLC Role Play

> **Domain**: MTS (Money Transfer System)
> **Time**: ~120 minutes
> **Prerequisite**: Level 1 & 2 completed (Sprint 1 closed, 12 issues)

---

### Where We Left Off (Level 2)

| Metric | Value |
|--------|-------|
| Sprint 1 | Closed — 8 story points completed |
| Issues | 1 Epic, 2 Stories, 1 Task, 6 Sub-tasks, 2 Bugs — all DONE |
| Epic (MTS-1) | Still open — more work in future sprints |
| Velocity | 8 pts/sprint (baseline) |

---

## Part A — JIRA Dashboards

---

## Lab 3.1 — Create a Dashboard

### What is a Dashboard?

- A customizable page with **gadgets** (widgets) showing project data
- Each gadget is powered by a **filter** (JQL query) or built-in report
- Dashboards give stakeholders a **real-time summary** without digging into backlogs
- Different dashboards for different audiences:
  - **Dev team**: sprint progress, open bugs, blockers
  - **QA team**: bugs by priority, test coverage, defect trends
  - **Management**: velocity, release progress, risk areas

### Lab Steps

1. Click **Dashboards** in the top navigation
2. Click **Create dashboard**
3. Fill in:
   - **Name**: `MTS - Project Dashboard`
   - **Description**: `Real-time overview of the MTS project for all team members`
   - **Access**: keep default (private — you can share later)
4. Click **Create**
5. You land on an empty dashboard — ready to add gadgets

---

## Lab 3.2 — Add Gadget: Filter Results

### What is this gadget?

- Displays a **list of issues** matching a JQL filter
- Like a mini issue list embedded in the dashboard
- Useful for: "show me all open bugs" or "my assigned work"

### Lab Steps

1. On your dashboard, click **Add gadget** (top-right)
2. Search for **Filter Results**
3. Click **Add** to place it on the dashboard
4. Configure the gadget:
   - **Saved filter**: Click **Advanced** → enter JQL:
     ```
     project = MTS AND type = Bug
     ```
   - **Number of results**: 10
   - **Columns to display**: Key, Summary, Priority, Status, Assignee
5. Click **Save**
6. The gadget shows your 2 bugs (MTS-11, MTS-12) — both Done

> **Tip**: You can create and save the filter first (like we did in Level 1), then select it from the dropdown instead of entering JQL each time.

---

## Lab 3.3 — Add Gadget: Pie Chart

### What is this gadget?

- Visual breakdown of issues by a field (status, priority, type, assignee, etc.)
- Quick snapshot of distribution — where is the work concentrated?

### Lab Steps

1. Click **Add gadget**
2. Search for **Pie Chart**
3. Click **Add**
4. Configure:
   - **Saved filter / JQL**: `project = MTS`
   - **Statistic Type**: `Issue Type`
5. Click **Save**
6. The pie chart shows distribution: Stories, Tasks, Sub-tasks, Bugs, Epic

### Try Another Pie Chart

1. Click **Add gadget** → **Pie Chart** again
2. Configure:
   - **JQL**: `project = MTS`
   - **Statistic Type**: `Priority`
3. Click **Save**
4. Shows: High vs Medium breakdown

---

## Lab 3.4 — Add Gadget: Sprint Burndown / Sprint Health

### Lab Steps

1. Click **Add gadget**
2. Search for **Sprint Burndown** (or **Sprint Health**)
3. Click **Add**
4. Configure:
   - **Board**: MTS board
   - **Sprint**: Sprint 1 - Transfer Found
5. Click **Save**
6. Shows the burndown chart from Sprint 1 — how quickly work was completed

---

## Lab 3.5 — Add Gadget: Recently Created Issues

### Lab Steps

1. Click **Add gadget**
2. Search for **Created vs Resolved**
3. Click **Add**
4. Configure:
   - **JQL**: `project = MTS`
   - **Period**: Last 30 days
5. Click **Save**
6. Shows how many issues were created vs resolved over time

---

## Lab 3.6 — Arrange the Dashboard Layout

### Lab Steps

1. Click **Edit layout** (or drag gadgets to rearrange)
2. Arrange gadgets in a logical order:
   - **Top-left**: Pie chart (by Issue Type) — overall composition
   - **Top-right**: Pie chart (by Priority) — risk overview
   - **Middle**: Filter Results (Bugs) — what needs attention
   - **Bottom-left**: Sprint Burndown — sprint health
   - **Bottom-right**: Created vs Resolved — trend
3. Click **Done** when satisfied

### Your Dashboard Summary

| Gadget | Shows | Audience |
|--------|-------|----------|
| Pie Chart (Issue Type) | Story/Task/Bug/Sub-task distribution | Everyone |
| Pie Chart (Priority) | High vs Medium breakdown | PO, Management |
| Filter Results (Bugs) | All bugs with status | QA, Dev |
| Sprint Burndown | How sprint work was completed | SM, Dev |
| Created vs Resolved | Issue creation vs resolution trend | Management |

> **SDLC connection**: Dashboards are how stakeholders get visibility into the project without attending every standup. They answer: "Are we on track? What's the risk? What needs attention?"

---

## Part B — Confluence Integration

---

## Lab 3.7 — What is Confluence?

### Key Concepts

- Confluence is Atlassian's **wiki and documentation** tool
- Tightly integrated with JIRA — link pages to issues, embed JIRA data
- Used for:
  - **Project documentation**: architecture, design decisions, runbooks
  - **Meeting notes**: sprint planning, retrospectives, decision logs
  - **Knowledge base**: onboarding guides, coding standards, FAQs
  - **Agile docs**: product requirements, test plans, release notes

### Confluence vs JIRA

| Aspect | JIRA | Confluence |
|--------|------|-----------|
| Purpose | Track work (issues, sprints, bugs) | Document knowledge (pages, wikis) |
| Content | Short-form: summaries, descriptions, comments | Long-form: documents, diagrams, tables |
| Structure | Issues in a backlog/board | Pages in a space hierarchy |
| Best for | "What are we doing?" | "Why and how are we doing it?" |

---

## Lab 3.8 — Create a Confluence Space for MTS

### Lab Steps

1. Open Confluence: click the **app switcher** (grid icon, top-left) → select **Confluence**
   - Or go to `https://your-org.atlassian.net/wiki`
2. Click **Spaces** → **Create space**
3. Select **Blank space** (or **Team space**)
4. Fill in:
   - **Name**: `MTS - Money Transfer System`
   - **Key**: `MTS`
5. Click **Create**
6. You land on the space home page — ready to add content

---

## Lab 3.9 — Create a Product Requirements Page

### The Scenario

The PO documents the product requirements in Confluence — a living document that the whole team references.

### Lab Steps

1. In the MTS Confluence space, click **Create** (or `+` button)
2. Select **Blank page**
3. Title: `MTS - Product Requirements`
4. Add content:

```
# Product Requirements — Money Transfer System

## Business Objective
Enable customers to initiate secure domestic money transfers via digital channels.

## Functional Requirements

### FR-01: Fund Transfer (UPI)
- User can select source and destination accounts
- Source and destination must be different
- Amount: INR 1.00 to INR 10,00,000.00
- Transfer modes: UPI, NEFT, IMPS, RTGS
- On success: display reference ID
- On failure: display specific error message
- Error cases:
  - Inactive account → "Account is inactive, please contact support"
  - Insufficient balance → "Insufficient balance in account [ACC_NUMBER]"
  - Same account → "Cannot transfer to the same account"

### FR-02: Account Dashboard
- Display all accounts as cards
- Each card: account number, owner, type (SAVINGS/CURRENT), balance (INR)
- Auto-refresh after successful transfer

## Non-Functional Requirements
- Transfer response time < 3 seconds (500 concurrent users)
- Database: MySQL with constraints (balance >= 0, amount > 0)
- API: RESTful, JSON, Spring Boot 3.x
- Frontend: React with Vite

## Out of Scope
- International transfers, forex
- Batch payroll processing
```

5. Click **Publish**

---

## Lab 3.10 — Link Confluence Page to JIRA Issues

### Why Link?

- Creates bidirectional traceability: JIRA issue ↔ Confluence document
- When someone reads the requirement doc, they can jump to the JIRA issue tracking it
- When someone views a JIRA issue, they can access the detailed documentation

### Lab Steps — From JIRA

1. Go back to JIRA → open **MTS-2** (UPI transfer story)
2. Find the **Confluence page** section (or click **Link** → **Confluence page**)
3. Search for `MTS - Product Requirements`
4. Select and link it
5. The Confluence page now appears on the JIRA issue

### Lab Steps — From Confluence

1. Go to the `MTS - Product Requirements` page in Confluence
2. In the page content, type `/jira` to insert a JIRA macro
3. Enter JQL: `project = MTS AND type = Story`
4. A live table of MTS stories appears embedded in the Confluence page
5. Click **Publish** to save

> **RTM connection**: This creates a full traceability chain: Confluence (requirements doc) ↔ JIRA (stories/bugs) ↔ Code (implementation). Stakeholders can navigate from business requirement to issue status to code — complete transparency.

---

## Lab 3.11 — Create a Sprint Retrospective Page

### The Scenario

After Sprint 1, the team conducts a **Sprint Retrospective** — documenting what went well, what didn't, and action items for improvement.

### Lab Steps

1. In Confluence MTS space, click **Create** → **Blank page**
2. Title: `Sprint 1 - Retrospective`
3. Add content:

```
# Sprint 1 Retrospective

**Sprint**: Sprint 1 - Transfer Found
**Date**: [today's date]
**Velocity**: 8 story points

## What Went Well
- Database schema set up quickly — unblocked stories early
- QA caught the inactive account bug before release (shift-left in action)
- Acceptance criteria refinement through comments improved story clarity
- All committed stories completed within the sprint

## What Didn't Go Well
- Bug found: TransferService didn't check isActive flag — missing validation
- Frontend error display bug — catch block didn't extract API error messages
- All work assigned to one person — no parallel execution

## Action Items
| Action | Owner | Due |
|--------|-------|-----|
| Add account status validation to all service methods | Dev | Sprint 2 |
| Improve frontend error handling pattern — create reusable error handler | Dev | Sprint 2 |
| Define code review checklist for validation edge cases | QA | Sprint 2 |
| Consider splitting work across team members in Sprint 2 | SM | Sprint 2 Planning |

## Metrics
- Stories completed: 2/2 (100%)
- Tasks completed: 1/1 (100%)
- Bugs found: 2
- Bugs fixed: 2/2 (100%)
- Story points: 8 committed / 8 completed
```

4. Click **Publish**

> **STLC connection**: The retrospective is part of **STLC Stage 7 — Test Closure**. Yesterday: *"Lessons learned — what can we improve in the next cycle?"* This page captures exactly that.

---

## Lab 3.12 — Create a Test Plan Page

### The Scenario

QA documents the test plan for the Fund Transfer Module — what to test, how, and what's in/out of scope.

### Lab Steps

1. Create a new Confluence page
2. Title: `MTS - Test Plan: Fund Transfer Module`
3. Add content:

```
# Test Plan — Fund Transfer Module

## Objective
Verify that the Fund Transfer Module meets all functional and non-functional requirements.

## Scope
### In Scope
- UPI transfer: happy path and error scenarios
- Account validation: active/inactive, existence
- Balance validation: sufficient/insufficient
- Same account check
- Transaction reference ID generation
- Frontend: TransferForm validation and error display
- Dashboard: AccountCard display and refresh

### Out of Scope
- NEFT/IMPS/RTGS (future sprints)
- International transfers
- Performance/load testing (separate cycle)

## Test Scenarios

| ID | Scenario | Type | Priority |
|----|----------|------|----------|
| TS-01 | Valid UPI transfer between active accounts | Functional | P1 |
| TS-02 | Transfer with insufficient balance | Functional | P1 |
| TS-03 | Transfer from inactive account | Functional | P1 |
| TS-04 | Transfer to same account | Functional | P1 |
| TS-05 | Transfer with amount below minimum (< 1) | Functional | P2 |
| TS-06 | Transfer with amount above maximum (> 10L) | Functional | P2 |
| TS-07 | Transfer to non-existent account | Functional | P1 |
| TS-08 | Dashboard displays all accounts correctly | Functional | P1 |
| TS-09 | Dashboard refreshes after transfer | Functional | P2 |
| TS-10 | Error messages display correctly on frontend | Functional | P1 |

## Test Environment
- Backend: Spring Boot 3.x, H2/MySQL
- Frontend: React, Chrome 120+
- API Testing: Postman / curl

## Entry Criteria
- Database schema created and seeded
- Backend API deployed and accessible
- Frontend build successful

## Exit Criteria
- All P1 test scenarios executed
- No open Critical/Major bugs
- Test evidence captured for all scenarios
```

4. Click **Publish**

> **STLC connection**: This covers **STLC Stage 2 (Test Planning)** and **Stage 3 (Test Design)**. The test plan defines scope, scenarios, and entry/exit criteria — exactly what we discussed yesterday.

---

## Part C — Sprint 2 Planning & SDLC Role Play Prep

---

## Lab 3.13 — PO Adds New Stories for Sprint 2

### The Scenario

Based on Sprint 1 learnings and remaining scope, the PO creates new stories for the next sprint.

### Lab Steps — Create Story: Transaction History

1. Click **Create** in JIRA
2. Fill in:
   - **Issue Type**: Story
   - **Summary**: `As a user, I want to view my transaction history so that I can track past transfers`
   - **Description**:
     ```
     Acceptance Criteria:
     - List recent transactions for selected account
     - Each row: reference ID, from/to accounts, amount, mode (UPI/NEFT/IMPS/RTGS), status, timestamp
     - Status color coding: SUCCESS (green), FAILED (red), PENDING (yellow), REVERSED (gray)
     - Pagination or infinite scroll for large lists
     ```
   - **Parent Epic**: `Fund Transfer Module`
   - **Story Points**: `5`
   - **Priority**: Medium
3. Click **Create**

### Lab Steps — Create Story: Transfer Notifications

1. Click **Create**
2. Fill in:
   - **Issue Type**: Story
   - **Summary**: `As a user, I want to receive a notification after a transfer`
   - **Description**:
     ```
     Acceptance Criteria:
     - Notification sent via Node.js notification service
     - Includes: reference ID, amount, from/to accounts, status
     - Both sender and receiver notified
     - Notification delivered within 5 seconds of transfer completion
     ```
   - **Parent Epic**: `Fund Transfer Module`
   - **Story Points**: `3`
   - **Priority**: Low
3. Click **Create**

---

## Lab 3.14 — Create Sprint 2

### Lab Steps

1. Click **Backlog** in the sidebar
2. The new stories should appear in the backlog
3. Click **Create sprint**
4. Name: `Sprint 2 - History & Notif` (max 30 chars)
5. Goal: `Transaction history and notification service`
6. Drag the 2 new stories into Sprint 2
7. **Do not start yet** — this is ready for the next iteration

---

## Part D — SDLC Role Play Preparation

---

## Lab 3.15 — Understand the Role Play

### Format

- Teams of 4-5 people
- Each person plays a specific role
- Simulate a complete SDLC cycle using JIRA and Confluence

### Roles

| Role | Responsibilities in Role Play |
|------|-------------------------------|
| **Product Owner** | Present the feature, write user story with acceptance criteria in JIRA |
| **Developer** | Break story into child issues, estimate, ask clarifying questions |
| **QA Engineer** | Review acceptance criteria, write test scenarios in Confluence, find bugs |
| **Scrum Master** | Create sprint, facilitate planning, track board, manage time |

### Scenario for Role Play

> "MTS needs a new feature: **Transfer Limits**. Each account should have a daily transfer limit. Transfers exceeding the limit should be rejected with a clear error message."

### What Each Role Does

**PO (5 min):**
1. Create a Story in JIRA:
   - `As a user, I want daily transfer limits enforced so that my account is protected from unauthorized large transfers`
2. Write acceptance criteria
3. Set priority and story points

**Developer (10 min):**
1. Review the story and ask questions via JIRA comments
2. Create child issues (sub-tasks) for implementation
3. Identify dependencies and link them

**QA (10 min):**
1. Review acceptance criteria — ask clarifying questions via comments
2. Create a test scenarios page in Confluence
3. Think about edge cases:
   - What IS the daily limit? Per user or per account?
   - What timezone defines "daily"?
   - Is the limit inclusive? (Limit = 50,000 — does 50,000 succeed?)
   - When does the limit reset?

**Scrum Master (5 min):**
1. Create a sprint in JIRA
2. Pull the story and child issues into the sprint
3. Present the sprint plan to the team

### Evaluation Criteria

| Criteria | Weight | What to Look For |
|----------|--------|-----------------|
| Story quality | 25% | Clear summary, testable acceptance criteria, proper format |
| QA analysis | 25% | Edge cases identified, test scenarios documented, shift-left questions |
| Dev breakdown | 25% | Logical child issues, dependencies identified, effort estimated |
| Collaboration | 25% | Comments in JIRA, questions asked, refinement happened |

---

## Summary — What We Built in Level 3

### JIRA Dashboard
- Created `MTS - Project Dashboard` with 5 gadgets
- Pie charts (issue type, priority), bug filter, burndown, created vs resolved

### Confluence Pages
- `MTS - Product Requirements` — functional + non-functional requirements
- `Sprint 1 - Retrospective` — what went well, action items
- `MTS - Test Plan: Fund Transfer Module` — test scenarios, entry/exit criteria

### Sprint 2 Prep
- 2 new stories in backlog (Transaction History, Notifications)
- Sprint 2 created and ready

### SDLC Role Play
- Scenario: Transfer Limits feature
- Roles defined: PO, Dev, QA, SM
- Evaluation criteria clear

---

## JIRA ↔ SDLC/STLC Concepts (Full Picture)

| JIRA / Confluence Activity | SDLC/STLC Stage |
|---------------------------|------------------|
| Confluence: Product Requirements page | Requirements phase — BRD/FRD/SRS |
| JIRA: Epics | SDLC: Business Need / Planning |
| JIRA: Stories with Acceptance Criteria | SDLC: Requirements → Agile User Stories |
| JIRA: Child issues / Sub-tasks | SDLC: Design → Development |
| JIRA: Sprint creation & planning | Agile: Sprint Planning ceremony |
| JIRA: Board transitions (To Do → Done) | SDLC: Development → Testing → Deployment |
| JIRA: Bug with steps/expected/actual | STLC: Test Execution + Defect Reporting |
| JIRA: Issue links (blocks, caused by) | STLC: Requirements Traceability (RTM) |
| Confluence: Test Plan | STLC: Test Planning + Test Design |
| JIRA: Sprint burndown & velocity | Agile: Sprint Review + Metrics |
| Confluence: Retrospective | Agile: Sprint Retrospective |
| JIRA: Dashboard with gadgets | SDLC: Project Monitoring & Visibility |
| Confluence ↔ JIRA linking | Full traceability: Requirements → Issues → Evidence |
| SDLC Role Play | End-to-end SDLC simulation with all roles |

---

## Checklist

### Part A — Dashboards
- [ ] Created `MTS - Project Dashboard`
- [ ] Added Pie Chart gadget (by Issue Type)
- [ ] Added Pie Chart gadget (by Priority)
- [ ] Added Filter Results gadget (Bugs)
- [ ] Added Sprint Burndown gadget
- [ ] Added Created vs Resolved gadget
- [ ] Arranged dashboard layout

### Part B — Confluence
- [ ] Created MTS Confluence space
- [ ] Created Product Requirements page
- [ ] Linked Confluence page to JIRA issue
- [ ] Embedded JIRA issues in Confluence page (JIRA macro)
- [ ] Created Sprint 1 Retrospective page
- [ ] Created Test Plan page with scenarios and entry/exit criteria

### Part C — Sprint 2 Prep
- [ ] (As PO) Created 2 new stories: Transaction History, Notifications
- [ ] Created Sprint 2, added stories

### Part D — Role Play
- [ ] Understood the Transfer Limits scenario
- [ ] Know your role and responsibilities
- [ ] Ready to execute PO → Dev → QA → SM workflow in JIRA

---

## Lab Complete!

You've now experienced the **full JIRA + Confluence workflow** from project setup to sprint delivery to documentation:

```
Level 1: Space → Epic → Stories → Task → Links → Backlog → QA Review
Level 2: Sprint → Transitions → Child Issues → Bugs → Fix → Verify → Close Sprint → Reports
Level 3: Dashboard → Confluence Docs → Sprint 2 Prep → SDLC Role Play
```

This maps directly to the complete SDLC:
```
Business Need → Requirements → Design → Development → Testing → Deployment → Maintenance
     ↑                                                                          |
     └──────────── Feedback loop (retrospective, new requirements) ─────────────┘
```
