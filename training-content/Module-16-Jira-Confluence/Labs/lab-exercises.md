# Module 16: Confluence & Jira -- Exercises

## Lab Overview

These exercises combine hands-on Jira and Confluence tasks with SDLC role play. You will create Jira issues, write JQL queries, build Confluence documentation, and simulate a full sprint cycle with your team.

> "Hi Team, we are standardizing our project management and documentation practices. Every sustain engineer needs to be fluent in Jira for tracking work and Confluence for documentation. Complete these exercises to build the skills you will use every day: creating well-structured issues, querying with JQL, writing runbooks, and participating effectively in Agile ceremonies."

---

## Exercise 1: Jira Issue Creation (30 min)

### Scenario
Create the following Jira issues for the FoodExpress project (FOOD). Write them on paper or in a shared document using the proper format.

### Task: Create 6 Issues

**Issue 1: Epic**
- Create an Epic for "Order Experience Improvement"
- Include: summary, description with business justification, priority

**Issue 2: User Story**
- Under the Epic, create a story: "As a customer, I want to re-order my last meal with one click"
- Include: acceptance criteria (3 Given/When/Then), story points estimate, component

**Issue 3: Bug Report**
- Create a bug: "Order confirmation email shows Rs 0.00 total for COD orders"
- Include: steps to reproduce (numbered), expected vs actual, severity, environment, evidence

**Issue 4: Task**
- Create a task: "Set up automated database backup for production MySQL"
- Include: description with specific requirements, acceptance criteria, priority

**Issue 5: Sub-task**
- Under Issue 2, create a sub-task: "Design API endpoint for re-order functionality"
- Include: technical specifications, estimated hours

**Issue 6: Bug with Links**
- Create a bug: "Promo code FLAT100 gives percentage discount instead of flat Rs 100"
- Link it to Issue 3 (Relates to) and note it blocks a hypothetical FOOD-200

---

## Exercise 2: JQL Queries (30 min)

### Task
Write JQL queries for each of the following scenarios. Test them mentally or on a shared board.

| # | Scenario | Your JQL |
|---|----------|----------|
| 1 | All open bugs in the FoodExpress project | ? |
| 2 | P1 bugs that are unassigned | ? |
| 3 | Issues assigned to you that are not done | ? |
| 4 | Bugs created in the last 7 days | ? |
| 5 | All issues in the current sprint | ? |
| 6 | Stories with more than 8 story points | ? |
| 7 | Issues in the "Order Service" component that are blocked | ? |
| 8 | Bugs that were reopened (status was Done and is now not Done) | ? |
| 9 | All issues updated in the last 24 hours | ? |
| 10 | Overdue issues (past due date, not completed) | ? |
| 11 | Issues with the label "regression" | ? |
| 12 | All issues resolved in version v2.4 | ? |

### Bonus: Create a Dashboard
Design a sustain team dashboard with 4 gadgets. For each gadget, specify:
- Gadget type (pie chart, filter results, burndown, etc.)
- JQL query it uses
- What insight it provides

---

## Exercise 3: Confluence Documentation (45 min)

### Task 3A: Write a Runbook (20 min)
Create a runbook for: **"FoodExpress Order Service -- Restart Procedure"**

Use the runbook template and include:
1. Overview (when and why to restart)
2. Prerequisites (access, permissions)
3. Step-by-step instructions with exact commands
4. Verification steps (how to confirm it is working)
5. Rollback steps (what to do if restart fails)
6. Escalation contacts

### Task 3B: Write a Root Cause Analysis (15 min)
Write an RCA for the following incident:

> **Incident:** On July 25, 2026 at 14:30, the FoodExpress order service started returning 503 errors for all requests. The incident lasted 45 minutes and affected ~500 orders. Root cause was a misconfigured environment variable (MONGODB_URI pointed to the wrong database after a staging deployment script accidentally ran against production).

Include: summary table, timeline, root cause, contributing factors, action items, lessons learned.

### Task 3C: Create a Release Notes Page (10 min)
Write release notes for FoodExpress v2.4 including:
- 2 new features (Loyalty Points, Scheduled Orders)
- 5 bug fixes (make up realistic summaries)
- 1 performance improvement
- Known issues
- Upgrade instructions

---

## Exercise 4: Sprint Board Design (20 min)

### Scenario
Design a Kanban board for the FoodExpress Sustain team.

### Tasks
1. Define the **columns** (workflow states) -- at least 5 columns
2. Set **WIP limits** for each column with justification
3. Define **swimlanes** (how to group issues horizontally)
4. Define **card colors** (what each color represents)
5. Create **quick filters** (useful filter buttons) with JQL

### Deliverable Format

| Column | WIP Limit | Justification |
|--------|-----------|---------------|
| Backlog | No limit | ? |
| ? | ? | ? |
| ? | ? | ? |
| Done | No limit | ? |

---

## Exercise 5: SDLC Role Play (90 min)

### Setup
- Form teams of 5-6 people
- Assign roles: PO, SM, Developer, QA, Tech Lead, Release Manager
- Use the backlog from the slides (FOOD-170 to FOOD-181)

### Phase 1: Sprint Planning (30 min)
1. PO presents each backlog item (2 min each)
2. Team estimates story points (planning poker style)
3. Select items for Sprint 24 (velocity: 30 points)
4. Define sprint goal
5. Document selected items and sprint goal

### Phase 2: Sprint Execution (30 min)
1. SM runs daily standup (simulate Day 3)
2. Dev updates issue statuses on the board
3. QA discovers new bug FOOD-182 and writes it up
4. Team decides: add FOOD-182 to sprint or defer?
5. SM addresses blocked issue FOOD-181

### Phase 3: Sprint Review & Retro (30 min)
1. PO accepts/rejects completed items
2. Dev demos fixes (verbal description)
3. SM calculates velocity
4. Retro: each person writes 1 "went well" and 1 "improve"
5. Tech Lead documents the retro in Confluence format

### Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Issue quality (clear, complete, well-structured) | 25% |
| Sprint planning decisions (realistic, justified) | 20% |
| Standup effectiveness (concise, blockers addressed) | 15% |
| Bug report quality (reproducible, evidence-based) | 15% |
| Retro quality (actionable, specific) | 15% |
| Collaboration and communication | 10% |

---

## Checkpoints

### Checkpoint 1 (Morning)
- [ ] Exercise 1: 6 Jira issues created with all required fields
- [ ] Exercise 2: All 12 JQL queries written
- [ ] Exercise 2: Dashboard design with 4 gadgets

### Checkpoint 2 (Afternoon)
- [ ] Exercise 3: Runbook completed with all sections
- [ ] Exercise 3: RCA completed with timeline and action items
- [ ] Exercise 3: Release notes page completed
- [ ] Exercise 4: Kanban board designed with columns, WIP limits, swimlanes
- [ ] Exercise 5: SDLC Role Play completed (all 3 phases)

---

## Bonus Challenges

1. **Automation rules** -- Design 3 Jira automation rules for FoodExpress (e.g., auto-assign, auto-transition, notifications)
2. **Confluence template library** -- Create 3 additional templates the sustain team would use daily (onboarding guide, deployment checklist, weekly status report)
3. **Cross-project reporting** -- Design a JQL query and dashboard that shows metrics across multiple Jira projects (FoodExpress backend, frontend, infra)
4. **Knowledge base architecture** -- Design the full Confluence space structure for FoodExpress with all spaces, page hierarchy, and labels taxonomy
5. **Sprint metrics analysis** -- Given velocity data for 10 sprints (make up data), calculate average velocity, identify trends, and recommend capacity for the next sprint
