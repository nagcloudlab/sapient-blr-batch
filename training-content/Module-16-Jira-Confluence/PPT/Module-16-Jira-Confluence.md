# Confluence & Jira
## Module 16 | Sustain Engineering Training | Day 17

**1 day | Lecture + hands-on + SDLC Role Play**

---

## Agenda

| Session | Topics |
|---------|--------|
| First half | Jira: Agile Concepts, Scrum & Kanban Boards, Projects, Issues, Workflows, Dashboard |
| Second half | Confluence: Collaboration, User Management, Content Creation, Project Wikis |
| Assessment | SDLC Role Play (90 min) |

> Master the tools that sustain engineering teams use daily: Jira for tracking work, Confluence for documentation.

---

## Why Jira & Confluence for Sustain Engineers?

### The Reality of Sustain Work

| Activity | Tool | Frequency |
|----------|------|-----------|
| Tracking bugs and tasks | Jira | Daily |
| Sprint planning and reviews | Jira | Weekly |
| Writing root-cause analysis | Confluence | Per incident |
| Documenting fixes and runbooks | Confluence | Per fix |
| Checking deployment status | Jira + Confluence | Daily |
| Onboarding new team members | Confluence | Per person |

> In sustain engineering, **Jira is your task list** and **Confluence is your knowledge base**.

---

## Jira -- Overview

### What Is Jira?

- **Project management tool** by Atlassian
- Industry standard for Agile software development
- Tracks work items (issues) through customizable workflows
- Supports Scrum, Kanban, and hybrid methodologies

### Key Concepts

| Concept | Description | FoodExpress Example |
|---------|-------------|---------------------|
| **Project** | A collection of issues for a product/team | FOOD (FoodExpress project) |
| **Issue** | A single unit of work | FOOD-156: Fix tax calculation |
| **Board** | Visual representation of work | FoodExpress Sustain Board |
| **Sprint** | Time-boxed iteration | Sprint 23 (Jul 28 - Aug 8) |
| **Backlog** | Prioritized list of work to do | All unfinished issues |
| **Epic** | Large body of work, spans sprints | Payment System Overhaul |
| **Workflow** | States an issue moves through | To Do -> In Progress -> Done |

---

## Jira -- Agile Concepts Refresher

### Scrum in Jira

```
Product Backlog          Sprint Board             Burndown
+-----------+            +-----+-----+-----+      |\
| Epic      |   Sprint   |To Do|In   |Done |      | \
|  Story 1  |  Planning  |     |Prog |     |      |  \
|  Story 2  |  -------> |S1   |S3   |S5   |      |   \
|  Story 3  |            |S2   |S4   |     |      |    \  Ideal
|  Bug 1    |            |     |     |     |      |     \_____
|  Task 1   |            +-----+-----+-----+      |     Actual
+-----------+                                      +----------->
  Prioritized              Visualized               Time
```

### Key Scrum Concepts in Jira

| Concept | Jira Implementation |
|---------|-------------------|
| **Sprint** | Time-boxed container for issues (1-4 weeks) |
| **Velocity** | Average story points completed per sprint |
| **Burndown Chart** | Shows remaining work over time |
| **Sprint Report** | Summary of completed vs incomplete work |
| **Story Points** | Effort estimation (Fibonacci: 1, 2, 3, 5, 8, 13) |

---

## Jira -- Kanban Concepts

### Kanban Board Configuration

```
+----------+-----------+-----------+----------+---------+
| Backlog  | To Do     | In Prog   | Review   | Done    |
| (no WIP) | WIP: 5    | WIP: 3    | WIP: 2   | (no WIP)|
+----------+-----------+-----------+----------+---------+
| FOOD-170 | FOOD-162  | FOOD-160  | FOOD-158 | FOOD-155|
| FOOD-171 | FOOD-163  | FOOD-161  |          | FOOD-156|
| FOOD-172 | FOOD-164  |           |          | FOOD-157|
| FOOD-173 |           |           |          |         |
+----------+-----------+-----------+----------+---------+
```

### Kanban Concepts in Jira

| Concept | Jira Implementation | FoodExpress Example |
|---------|-------------------|---------------------|
| **WIP Limits** | Max issues per column | In Progress: max 3 |
| **Swimlanes** | Horizontal groupings | By priority, by assignee |
| **Card Colors** | Visual indicators | Red = bug, Blue = story, Yellow = task |
| **Cumulative Flow** | Chart showing issue distribution | Detect bottlenecks |
| **Lead Time** | Time from creation to completion | Track how fast bugs are fixed |
| **Cycle Time** | Time from start to completion | Track active work time |

---

## Jira -- Projects

### Project Types

| Type | Use Case | FoodExpress Example |
|------|----------|---------------------|
| **Scrum** | Sprint-based feature development | FoodExpress Feature Development |
| **Kanban** | Continuous flow, sustain work | FoodExpress Sustain Engineering |
| **Bug Tracking** | Dedicated bug management | FoodExpress Production Issues |
| **Service Desk** | Customer support tickets | FoodExpress Customer Support |

### Project Configuration

| Setting | Description | Recommendation |
|---------|-------------|----------------|
| **Key** | Short prefix for issues | FOOD |
| **Lead** | Project manager | Sustain Team Lead |
| **Scheme** | Workflow, permissions, notifications | Match team's process |
| **Components** | Sub-areas of the project | Order Service, Payment, Search, Delivery |
| **Versions** | Release tracking | v2.3, v2.4, v2.5 |
| **Categories** | Grouping of projects | Backend, Frontend, Infrastructure |

---

## Jira -- Issue Types

### Standard Issue Types

| Type | Icon | Description | FoodExpress Example |
|------|------|-------------|---------------------|
| **Epic** | Lightning bolt | Large body of work | Payment System Redesign |
| **Story** | Green bookmark | User-facing feature | As a customer, I can track delivery |
| **Task** | Blue checkbox | Technical work item | Set up monitoring for order service |
| **Bug** | Red circle | Defect to fix | Order total shows wrong tax amount |
| **Sub-task** | Gray sub-item | Breakdown of parent | Write unit tests for tax calculation |

### Issue Fields

| Field | Required? | Description | Example |
|-------|-----------|-------------|---------|
| **Summary** | Yes | Short title | "Fix tax calculation on discounted orders" |
| **Description** | Yes | Detailed explanation | Steps to reproduce, expected vs actual |
| **Type** | Yes | Issue type | Bug |
| **Priority** | Yes | Urgency | P1-Critical |
| **Assignee** | No | Who is working on it | Priya Sharma |
| **Reporter** | Auto | Who created it | QA Team |
| **Sprint** | No | Which sprint | Sprint 23 |
| **Story Points** | No | Effort estimate | 5 |
| **Labels** | No | Tags for filtering | "sustain", "payment", "regression" |
| **Component** | No | Which subsystem | Order Service |
| **Fix Version** | No | Target release | v2.4 |

---

## Jira -- Issue Hierarchy

```
Epic: Payment System Redesign (FOOD-100)
|
+-- Story: Implement new tax calculation (FOOD-110)
|   +-- Sub-task: Update tax formula (FOOD-111)
|   +-- Sub-task: Write unit tests (FOOD-112)
|   +-- Sub-task: Update API documentation (FOOD-113)
|
+-- Story: Add payment retry logic (FOOD-120)
|   +-- Sub-task: Implement retry with exponential backoff (FOOD-121)
|   +-- Sub-task: Add circuit breaker (FOOD-122)
|
+-- Bug: Double charge on failed retry (FOOD-130)
|   +-- Sub-task: Add idempotency key (FOOD-131)
|   +-- Sub-task: Write integration test (FOOD-132)
```

### Linking Issues

| Link Type | Meaning | Example |
|-----------|---------|---------|
| **Blocks / Is blocked by** | Dependency | FOOD-110 blocks FOOD-120 |
| **Relates to** | Related work | FOOD-130 relates to FOOD-120 |
| **Duplicates / Is duplicated by** | Same issue reported twice | FOOD-135 duplicates FOOD-130 |
| **Clones / Is cloned by** | Copied issue | Cloned for different environment |

---

## Jira -- Workflows

### Default Workflow

```
+--------+     +-------------+     +--------+
| To Do  | --> | In Progress | --> |  Done  |
+--------+     +-------------+     +--------+
```

### FoodExpress Sustain Workflow

```
+--------+     +-----------+     +---------+     +--------+     +--------+
|  Open  | --> | In Review | --> | In Prog | --> | Testing| --> | Deploy |
+--------+     +-----------+     +---------+     +--------+     +---+----+
    |               |                 |               |              |
    v               v                 v               v              v
+--------+     +-----------+     +---------+     +--------+     +--------+
|Rejected|     | More Info |     | Blocked |     | Failed |     |  Done  |
+--------+     +-----------+     +---------+     +--------+     +--------+
```

### Workflow Transitions

| From | To | Condition | Example |
|------|----|-----------|---------|
| Open | In Review | Assigned to someone | QA triages and assigns |
| In Review | In Progress | Reviewer approves | Developer starts work |
| In Progress | Testing | Code committed + PR merged | PR approved, deployed to staging |
| Testing | Deploy | All tests pass | QA signs off |
| Deploy | Done | Deployed to production | Change verified in prod |
| Any | Blocked | External dependency | Waiting for API access |

---

## Jira -- Writing Good Issues

### Bug Report Template

```
**Summary:** [Component] Brief description of the bug

**Environment:** Production / Staging / Dev
**Browser/OS:** Chrome 115 / Windows 11
**Severity:** Critical / Major / Minor / Trivial
**Frequency:** Always / Intermittent / Once

**Steps to Reproduce:**
1. Navigate to https://foodexpress.com/orders
2. Place an order with a 20% discount code
3. View the order summary

**Expected Result:**
Tax should be calculated on the original amount (before discount)

**Actual Result:**
Tax is calculated on the discounted amount, resulting in lower tax

**Evidence:**
- Screenshot: [attached]
- Order ID: 12345
- Expected tax: Rs 89.82, Actual tax: Rs 71.86

**Impact:**
- Affects all orders with discount codes (~15% of orders)
- Revenue impact: ~Rs 50,000/month in under-collected tax
```

---

## Jira -- Boards

### Scrum Board

```
Sprint 23 Board (Jul 28 - Aug 8, 2026)
+----------+-----------+-----------+----------+
| TO DO    | IN PROG   | IN REVIEW | DONE     |
+----------+-----------+-----------+----------+
| FOOD-165 | FOOD-162  | FOOD-160  | FOOD-158 |
| (5 pts)  | (3 pts)   | (8 pts)   | (5 pts)  |
|          |           |           |          |
| FOOD-166 | FOOD-163  |           | FOOD-159 |
| (3 pts)  | (5 pts)   |           | (3 pts)  |
|          |           |           |          |
| FOOD-167 |           |           | FOOD-161 |
| (8 pts)  |           |           | (2 pts)  |
+----------+-----------+-----------+----------+
Sprint Goal: Fix payment bugs and add order tracking
Velocity (avg): 28 pts | Committed: 34 pts
```

### Board Filters (JQL)

```
-- All open bugs assigned to me
project = FOOD AND type = Bug AND assignee = currentUser()
  AND status != Done

-- P1 bugs not yet started
project = FOOD AND type = Bug AND priority = P1
  AND status = "To Do"

-- All issues in current sprint
project = FOOD AND sprint in openSprints()

-- Bugs created in the last 7 days
project = FOOD AND type = Bug
  AND created >= -7d

-- Unresolved issues for v2.4
project = FOOD AND fixVersion = "v2.4"
  AND resolution = Unresolved
```

---

## Jira -- JQL (Jira Query Language)

### JQL Syntax

```
field operator value [AND/OR field operator value]
```

### Common JQL Queries for Sustain Teams

| Purpose | JQL |
|---------|-----|
| My open tasks | `assignee = currentUser() AND status != Done` |
| Overdue issues | `due < now() AND status != Done` |
| Bugs by component | `type = Bug AND component = "Order Service"` |
| High priority unassigned | `priority in (P1, P2) AND assignee = EMPTY` |
| Created this week | `created >= startOfWeek()` |
| Resolved this sprint | `sprint in openSprints() AND status = Done` |
| Blocked issues | `status = Blocked` |
| Aging issues (30+ days) | `created <= -30d AND status != Done` |

### JQL Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equals | `type = Bug` |
| `!=` | Not equals | `status != Done` |
| `in` | In list | `priority in (P1, P2)` |
| `~` | Contains text | `summary ~ "payment"` |
| `>=`, `<=` | Comparison | `created >= "2026-07-01"` |
| `is EMPTY` | No value set | `assignee is EMPTY` |
| `was` | Previously had value | `status was "In Progress"` |

---

## Jira -- Dashboards

### FoodExpress Sustain Dashboard

```
+--------------------------------------------+
|        FoodExpress Sustain Dashboard       |
+--------------------------------------------+
|                                            |
| +------------------+ +------------------+ |
| | Open Bugs by     | | Sprint Burndown  | |
| | Priority         | |                  | |
| | P1: 2  [**]      | | \                | |
| | P2: 5  [*****]   | |  \   _           | |
| | P3: 8  [******** | |   \_/ \          | |
| | P4: 3  [***]     | |       \_____     | |
| +------------------+ +------------------+ |
|                                            |
| +------------------+ +------------------+ |
| | Recent Activity  | | Velocity Chart   | |
| |                  | |                  | |
| | FOOD-162 -> Prog | | S20: 24 pts     | |
| | FOOD-160 -> Rev  | | S21: 28 pts     | |
| | FOOD-158 -> Done | | S22: 32 pts     | |
| | FOOD-165 created | | S23: 34 pts     | |
| +------------------+ +------------------+ |
|                                            |
| +------------------+ +------------------+ |
| | Aging Issues     | | Component Health | |
| | > 30 days: 4     | | Order: 5 bugs    | |
| | > 60 days: 1     | | Payment: 2 bugs  | |
| | > 90 days: 0     | | Search: 1 bug    | |
| +------------------+ +------------------+ |
+--------------------------------------------+
```

### Dashboard Gadgets

| Gadget | Purpose | Configuration |
|--------|---------|---------------|
| **Filter Results** | Show issues matching a JQL query | Any JQL query |
| **Pie Chart** | Distribution by field | Priority, status, assignee |
| **Sprint Burndown** | Remaining work over time | Current sprint |
| **Velocity Chart** | Story points per sprint | Last 5-10 sprints |
| **Created vs Resolved** | Bug trends over time | By week or month |
| **Two-Dimensional Filter** | Matrix (e.g., priority x component) | Row/column fields |

---

## Jira -- Sprint Management

### Sprint Lifecycle

```
1. Sprint Planning     2. Sprint Execution     3. Sprint Review
   - Select stories       - Daily standups         - Demo to stakeholders
   - Estimate effort       - Update board           - Collect feedback
   - Set sprint goal       - Remove blockers        - Accept/reject stories

4. Sprint Retrospective
   - What went well?
   - What to improve?
   - Action items
```

### Sprint Metrics

| Metric | Definition | Healthy Range |
|--------|-----------|---------------|
| **Velocity** | Points completed per sprint | Stable +/- 20% |
| **Commitment vs Completion** | Committed vs delivered | > 80% |
| **Scope Change** | Stories added/removed mid-sprint | < 10% |
| **Carry-over** | Incomplete stories from last sprint | < 2 stories |
| **Bug Escape Rate** | Bugs found post-release | < 5% |

---

## Confluence -- Overview

### What Is Confluence?

- **Team collaboration and documentation platform** by Atlassian
- Integrates deeply with Jira
- Wiki-style content creation with rich editor
- Used for: documentation, meeting notes, knowledge bases, runbooks

### Why Confluence for Sustain Engineering?

| Use Case | Importance |
|----------|------------|
| **Runbooks** | Step-by-step guides for common incidents |
| **Root Cause Analysis** | Document incident findings and fixes |
| **Onboarding** | New team member documentation |
| **Architecture Docs** | System design, API docs, data flow |
| **Meeting Notes** | Sprint reviews, retrospectives, standups |
| **Decision Records** | Why decisions were made (ADRs) |
| **Release Notes** | What changed in each release |

---

## Confluence -- Spaces and Pages

### Space Types

| Type | Description | FoodExpress Example |
|------|-------------|---------------------|
| **Team Space** | For a specific team | Sustain Engineering Team |
| **Project Space** | For a specific project | FoodExpress Project |
| **Knowledge Base** | Shared documentation | Engineering Knowledge Base |
| **Personal Space** | Individual notes | Priya's Notes |

### Page Hierarchy

```
FoodExpress Project Space
+-- Home Page
    +-- Architecture
    |   +-- System Overview
    |   +-- API Documentation
    |   +-- Database Schema
    |   +-- Infrastructure Diagram
    +-- Runbooks
    |   +-- Deployment Guide
    |   +-- Incident Response
    |   +-- Database Recovery
    |   +-- Scaling Procedures
    +-- Sprint Documentation
    |   +-- Sprint 23 Planning
    |   +-- Sprint 23 Review
    |   +-- Sprint 23 Retro
    +-- Incidents
    |   +-- INC-001: Payment Outage
    |   +-- INC-002: Database Connection Leak
    +-- Release Notes
        +-- v2.3 Release Notes
        +-- v2.4 Release Notes
```

---

## Confluence -- User Management

### Permissions Model

| Level | Controls | Example |
|-------|----------|---------|
| **Global** | Site-wide settings, groups | Create spaces, manage users |
| **Space** | Who can access a space | Sustain team can view/edit project space |
| **Page** | Who can view/edit specific pages | Only leads can edit runbooks |

### Common Permission Groups

| Group | Permissions | FoodExpress Members |
|-------|------------|---------------------|
| **confluence-administrators** | Full site admin | IT Admin |
| **sustain-engineers** | View + edit project spaces | All sustain team members |
| **leads** | Edit runbooks + approve pages | Team leads |
| **stakeholders** | View-only access to project space | Product Owner, Manager |
| **everyone** | View knowledge base | All employees |

### Best Practices

| Practice | Why |
|----------|-----|
| Use groups, not individual permissions | Easier to manage at scale |
| Restrict edit on critical pages (runbooks) | Prevent accidental changes |
| Grant view access broadly | Knowledge sharing is valuable |
| Review permissions quarterly | Remove departed team members |

---

## Confluence -- Content Creation

### Page Elements

| Element | Use Case | Example |
|---------|----------|---------|
| **Headings** | Structure content | H1 for title, H2 for sections |
| **Tables** | Structured data | API endpoint reference |
| **Code Blocks** | Technical content | SQL queries, config files |
| **Info Panels** | Callouts | Warning, tip, note, info panels |
| **Macros** | Dynamic content | Jira issue list, table of contents |
| **Attachments** | Files and images | Architecture diagrams, screenshots |
| **Labels** | Categorization | "runbook", "architecture", "incident" |
| **Templates** | Standardized pages | RCA template, meeting notes template |

### Useful Macros

| Macro | Description | Example |
|-------|-------------|---------|
| `{jira}` | Embed Jira issues/filters | Show all open bugs on the page |
| `{toc}` | Table of contents | Auto-generated from headings |
| `{code}` | Syntax-highlighted code | Display SQL query |
| `{status}` | Colored status label | GREEN: Completed |
| `{expand}` | Collapsible section | Hide detailed steps |
| `{panel}` | Bordered content area | Highlight important information |
| `{children}` | List child pages | Show all runbooks |
| `{recently-updated}` | Recent changes | Show team activity |

---

## Confluence -- Templates

### Runbook Template

```
# [Service Name] -- [Procedure Name]

## Overview
Brief description of what this runbook covers.

## When to Use
- Trigger condition 1
- Trigger condition 2

## Prerequisites
- Access to [system]
- Permissions: [role]

## Steps
1. Step one with exact commands
   ```
   kubectl get pods -n foodexpress
   ```
2. Step two with expected output
3. Step three with verification

## Rollback
If something goes wrong:
1. Rollback step 1
2. Rollback step 2

## Escalation
If this runbook does not resolve the issue:
- Contact: [name] ([role])
- Slack: #foodexpress-incidents
- PagerDuty: [service name]

## History
| Date | Author | Change |
|------|--------|--------|
| 2026-07-20 | Priya | Created |
| 2026-07-25 | Rahul | Added rollback section |
```

---

## Confluence -- Root Cause Analysis Template

```
# Incident: [INC-XXX] [Brief Title]

## Summary
| Field | Value |
|-------|-------|
| Incident ID | INC-XXX |
| Date | YYYY-MM-DD |
| Duration | X hours Y minutes |
| Severity | SEV-1 / SEV-2 / SEV-3 |
| Impact | X users affected, Y orders failed |
| Resolved By | [Name] |

## Timeline
| Time | Event |
|------|-------|
| HH:MM | First alert triggered |
| HH:MM | Engineer begins investigation |
| HH:MM | Root cause identified |
| HH:MM | Fix applied |
| HH:MM | Service restored |

## Root Cause
[Detailed technical explanation]

## Contributing Factors
1. [Factor 1]
2. [Factor 2]

## Resolution
[What was done to fix it]

## Action Items
| # | Action | Owner | Due Date | Status |
|---|--------|-------|----------|--------|
| 1 | Add monitoring for X | Priya | 2026-08-01 | {status:In Progress} |
| 2 | Add automated test for Y | Rahul | 2026-08-05 | {status:To Do} |

## Lessons Learned
- [Lesson 1]
- [Lesson 2]
```

---

## Confluence -- Project Wiki Best Practices

### Knowledge Organization

| Category | Content | Update Frequency |
|----------|---------|-----------------|
| **Architecture** | System diagrams, API docs, data flow | Per major change |
| **Runbooks** | Operational procedures, incident response | Per incident learning |
| **Onboarding** | Setup guide, tool access, team norms | Per quarter |
| **Decisions** | Architecture Decision Records (ADRs) | Per decision |
| **Releases** | Release notes, changelog | Per release |
| **Meetings** | Sprint reviews, retros, standups | Per meeting |
| **Incidents** | RCA, postmortems | Per incident |

### Writing Tips

| Tip | Why |
|-----|-----|
| Use headings and tables | Scannable content is read more |
| Keep pages focused | One topic per page |
| Use templates | Consistency across the team |
| Link to Jira issues | Traceability between docs and work |
| Add labels | Findable via search |
| Review regularly | Remove outdated content |
| Use @mentions | Notify relevant people |

---

## Jira + Confluence Integration

### How They Work Together

```
Jira Issue (FOOD-156)              Confluence Page (RCA)
+-----------------------+          +-------------------------+
| Bug: Tax calculation  |          | Incident: INC-042       |
| wrong                 |   link   | Root Cause: Tax formula  |
| Status: Done          | <------> | uses wrong base amount   |
| Fix Version: v2.4     |          | Action Items:            |
+-----------------------+          | - FOOD-157: Add tests    |
                                   +-------------------------+
```

### Integration Features

| Feature | How to Use |
|---------|-----------|
| **Jira macro in Confluence** | Embed issue details or filter results in a Confluence page |
| **Confluence link in Jira** | Attach Confluence page to a Jira issue |
| **Smart links** | Paste a Jira/Confluence URL and it auto-formats |
| **Sprint notes** | Create Confluence page linked to sprint in Jira |
| **Release notes** | Auto-generate from Jira fix version |

---

## SDLC Role Play -- Overview (90 min)

### Format
- **Teams of 5-6 people**
- Simulate a complete sprint cycle using Jira and Confluence
- Each team member plays a different SDLC role
- 90 minutes, 3 phases

### Roles

| Role | SDLC Responsibility | Jira/Confluence Tasks |
|------|---------------------|----------------------|
| **Product Owner** | Define and prioritize requirements | Create and prioritize Jira stories |
| **Scrum Master** | Facilitate ceremonies, remove blockers | Manage sprint board, run standup |
| **Developer** | Build and fix code | Update issue status, log time |
| **QA Engineer** | Test and verify | Create bug reports, verify fixes |
| **Tech Lead** | Architecture decisions, code review | Write Confluence docs, review PRs |
| **Release Manager** | Coordinate deployment | Create release notes, manage versions |

---

## SDLC Role Play -- Phase 1: Sprint Planning (30 min)

### Scenario
FoodExpress Sprint 24 starts today. The Product Owner has 12 items in the backlog. Team velocity is 30 story points. Select items for the sprint.

### Backlog

| ID | Type | Summary | Points | Priority |
|----|------|---------|--------|----------|
| FOOD-170 | Bug | Payment timeout not handled | 5 | P1 |
| FOOD-171 | Bug | Search returns inactive restaurants | 3 | P1 |
| FOOD-172 | Story | Add order tracking page | 13 | P2 |
| FOOD-173 | Bug | Email notifications delayed | 3 | P2 |
| FOOD-174 | Story | Restaurant dashboard v2 | 8 | P2 |
| FOOD-175 | Task | Upgrade Node.js to v20 | 5 | P3 |
| FOOD-176 | Bug | Profile photo upload fails | 2 | P3 |
| FOOD-177 | Story | Scheduled orders feature | 13 | P2 |
| FOOD-178 | Task | Add monitoring for order service | 3 | P2 |
| FOOD-179 | Bug | Delivery ETA negative after delivery | 2 | P3 |
| FOOD-180 | Story | Customer loyalty points | 8 | P3 |
| FOOD-181 | Task | Database backup automation | 5 | P2 |

### Tasks
1. **PO:** Present each item, answer questions
2. **Team:** Estimate (if points seem wrong, re-estimate)
3. **SM:** Facilitate selection -- velocity is 30 points
4. **All:** Agree on sprint goal
5. **SM:** Create sprint in Jira (simulated on paper/whiteboard)

---

## SDLC Role Play -- Phase 2: Sprint Execution Simulation (30 min)

### Scenario
Mid-sprint: 3 days have passed. Simulate daily standup and issue progression.

### Day 3 Status

| Issue | Assignee | Status | Update |
|-------|----------|--------|--------|
| FOOD-170 | Dev | In Progress | Found root cause, fix in PR |
| FOOD-171 | Dev | In Review | PR submitted, awaiting review |
| FOOD-173 | Dev | To Do | Not started yet |
| FOOD-178 | Dev | Done | Monitoring dashboard live |
| FOOD-181 | Dev | Blocked | Waiting for AWS access |

### Tasks
1. **SM:** Run 15-minute standup (each person: done/doing/blocked)
2. **Dev:** Move issues on the board
3. **QA:** Report new bug found during testing:
   - "While testing FOOD-171 fix, discovered that search also shows restaurants from other cities"
   - Create a new bug (FOOD-182) in Jira format
4. **Tech Lead:** Decide if FOOD-182 should be added to current sprint
5. **SM:** Address the blocker on FOOD-181 (who to escalate to?)

---

## SDLC Role Play -- Phase 3: Sprint Review & Retro (30 min)

### Sprint Review (15 min)

### Scenario
Sprint 24 is complete. Present results to stakeholders.

| Issue | Status | Notes |
|-------|--------|-------|
| FOOD-170 | Done | Payment timeout now shows user-friendly error |
| FOOD-171 | Done | Search correctly filters inactive restaurants |
| FOOD-173 | Done | Email delay reduced from 5 min to 30 sec |
| FOOD-178 | Done | Monitoring dashboard live for order service |
| FOOD-181 | Carry-over | AWS access still pending |
| FOOD-182 | Done | Cross-city search bug fixed (added mid-sprint) |

### Tasks
1. **PO:** Accept/reject each completed item
2. **Dev:** Demo the fixes (describe what was done)
3. **QA:** Report test results and any remaining concerns
4. **SM:** Calculate velocity: completed = ? points

### Sprint Retrospective (15 min)

| Category | Discussion Points |
|----------|------------------|
| **What went well?** | Quick bug fixes, good collaboration |
| **What to improve?** | AWS access process too slow, scope change mid-sprint |
| **Action items** | Pre-request access for next sprint, define scope change policy |

### Tasks
1. Each team member writes 1 item for each category
2. **SM:** Facilitates discussion and captures action items
3. **Tech Lead:** Write a Confluence page for the retro (use template)

---

## Key Takeaways

| Concept | Key Lesson |
|---------|------------|
| Jira Basics | Projects, issues (epic/story/bug/task), boards (Scrum/Kanban) |
| Scrum in Jira | Sprints, velocity, burndown charts, sprint reports |
| Kanban in Jira | WIP limits, continuous flow, lead time, cycle time |
| JQL | Query language for finding issues: `type = Bug AND priority = P1` |
| Dashboards | Visualize team health: open bugs, velocity, aging issues |
| Workflows | Customize issue states to match your team's process |
| Confluence Basics | Spaces, pages, templates, macros, permissions |
| Documentation | Runbooks, RCA templates, release notes, architecture docs |
| Integration | Jira issues embedded in Confluence; Confluence pages linked from Jira |
| SDLC in Practice | Sprint planning -> execution -> review -> retro -- the continuous cycle |

> **Next: Module 17 -- Linux Fundamentals: Command line skills for managing servers and troubleshooting production systems.**
