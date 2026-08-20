# JIRA Lab — Level 2: Sprint Planning, Execution & First Bugs

> **Domain**: MTS (Money Transfer System)
> **Time**: ~90 minutes
> **Prerequisite**: Level 1 completed (1 Epic, 2 Stories, 1 Task in backlog)
> **Continues from**: Prioritized backlog with QA-refined stories

---

### Where We Left Off (Level 1)

| Key | Type | Summary | Labels | Status |
|-----|------|---------|--------|--------|
| MTS-1 | Epic | Fund Transfer Module | — | TO DO |
| MTS-4 | Task | Set up MySQL database schema and seed data | `backend`, `database` | TO DO |
| MTS-2 | Story | Transfer money via UPI (5 pts) | `backend` | TO DO |
| MTS-3 | Story | View account balance (3 pts) | `frontend` | TO DO |

- Backlog prioritized: MTS-4 → MTS-2 → MTS-3
- MTS-2 is blocked by MTS-4
- MTS-2 has refined acceptance criteria (from QA review)
- No bugs yet — those come when QA starts testing

---

## Lab 2.1 — Create a Sprint

### What is a Sprint?

- A **time-boxed iteration** — typically 1 to 4 weeks
- The team commits to completing a set of backlog items during the sprint
- At the end of every sprint, the team delivers a **tested, potentially shippable increment**
- Sprints have a **goal** — a one-line statement of what the sprint aims to achieve
- Key Scrum ceremonies around a sprint:
  - **Sprint Planning** — decide what goes into the sprint
  - **Daily Standup** — 15-min sync every day
  - **Sprint Review** — demo what was built
  - **Sprint Retrospective** — what went well, what to improve

### Lab Steps

1. Click **Backlog** in the sidebar
2. At the top of the backlog, click **Create sprint** (or you may see a sprint section already)
3. A new sprint section appears above the backlog
4. Click the sprint name (e.g., "MTS Sprint 1") to edit it:
   - **Name**: `Sprint 1 - Transfer Found` (max 30 characters)
5. Click the **...** menu on the sprint → **Edit sprint**
   - **Goal**: `Set up database and implement UPI transfer API`
   - **Duration**: 2 weeks
   - **Start date**: today
6. Click **Save**

> **Agile connection**: The sprint goal aligns with the BRD objective — "Enable customers to initiate secure domestic money transfers." Sprint 1 lays the foundation (database) and builds the core feature (UPI transfer).

---

## Lab 2.2 — Sprint Planning: Pull Items into Sprint

### What is Sprint Planning?

- The team decides **which backlog items** to pull into the sprint
- Based on: priority, team capacity, dependencies, and sprint goal
- The team should not over-commit — only pull what they can realistically finish
- Rule of thumb: total story points should match the team's **velocity** (past sprint average)
  - First sprint? Estimate conservatively

### The Scenario

The team (you) decides:
- **MTS-4** (DB task) — must go first, blocks everything
- **MTS-2** (UPI transfer, 5 pts) — core feature, aligns with sprint goal
- **MTS-3** (View balance, 3 pts) — supports the transfer flow, fits within capacity
- Total: **8 story points** — reasonable for a first sprint

### Lab Steps

1. In the **Backlog** view, you should see the sprint section at top and backlog items below
2. **Drag MTS-4** (DB task) from the backlog into the sprint section
3. **Drag MTS-2** (UPI transfer) into the sprint
4. **Drag MTS-3** (View balance) into the sprint
5. Verify the sprint section shows:
   - 3 issues
   - Total story points: 8 (5 + 3, task has no points)
6. The backlog below should now be empty

> **Capacity connection**: In a real team, sprint planning considers each member's availability. 8 points for a 2-week sprint is conservative — good for Sprint 1 when velocity is unknown.

---

## Lab 2.3 — Start the Sprint

### Lab Steps

1. In the **Backlog** view, click the **Start sprint** button (top-right of sprint section)
2. A dialog appears — confirm:
   - **Sprint name**: `Sprint 1 - Transfer Found`
   - **Duration**: 2 weeks
   - **Start date**: today
   - **End date**: auto-calculated (today + 14 days)
   - **Sprint goal**: `Set up database and implement UPI transfer API`
3. Click **Start**
4. JIRA automatically switches to the **Board** view
5. Observe: all 3 issues are in the **TO DO** column

### What just happened?

- The sprint is now **active** — the clock is ticking
- The Board view shows the sprint's work across columns
- Reports (burndown, velocity) start tracking from this moment
- No more items can be added without disrupting the sprint (in real Scrum)

---

## Lab 2.4 — Dev Starts Work: Transition the DB Task

### The Scenario

Wearing the **Developer hat** — you start with the database task since it blocks the UPI story.

### What are Workflow Transitions?

- Each issue moves through states: **TO DO → IN PROGRESS → DONE**
- Transitioning = updating the status as work progresses
- The Board view reflects transitions in real-time — cards move between columns
- Two ways to transition:
  - Drag the card on the Board
  - Click the status dropdown on the issue detail page

### Lab Steps

1. On the **Board**, find **MTS-4** (DB schema task) in the TO DO column
2. **Drag MTS-4** from **TO DO** to **IN PROGRESS**
3. The card moves — status is now IN PROGRESS
4. Open **MTS-4** → add a comment:

```
Starting database setup.
- Creating schema from database/schema.sql
- Tables: users, accounts, transactions
- Will seed with test data after schema is verified.
```

5. Click **Save**

> **SDLC connection**: This is the **Development** stage of SDLC. The developer is implementing the design (schema) that was defined during requirements and design phases.

---

## Lab 2.5 — Dev Completes the DB Task

### The Scenario

The database schema is set up and verified. Time to mark it done.

### Lab Steps

1. On the **Board**, drag **MTS-4** from **IN PROGRESS** to **DONE**
2. Open **MTS-4** → add a comment:

```
Database setup complete.
- All 3 tables created: users, accounts, transactions
- Constraints verified: balance >= 0, amount > 0, from != to
- Seed data: 3 users, 5 accounts inserted
- Application connects successfully
```

3. Click **Save**
4. Check the Board — MTS-4 is in the DONE column

### What just happened?

- The DB task is complete — the blocker for MTS-2 is resolved
- The UPI transfer story can now move to IN PROGRESS
- On the burndown chart, completed work starts appearing

---

## Lab 2.6 — Dev Breaks the UPI Story into Child Issues

### The Scenario

Before starting the UPI transfer story, you (as Dev) break it into smaller, implementable **child issues**. This is like creating a mini work breakdown.

### Why Child Issues?

- A 5-point story is too large to track as a single unit
- Child issues make progress visible — instead of "in progress" for days, you see individual pieces completing
- Each child issue maps to a specific code component
- In the V-Model: child issues = detailed design, each testable individually

### Lab Steps

1. Open **MTS-2** (UPI transfer story)
2. Find the **Child issues** section (or click **Create child issue** / **Create sub-task**)
3. Create the following child issues one by one:

**Child 1:**
- Summary: `Create TransferRequest DTO with validations`
- Priority: High

**Child 2:**
- Summary: `Create TransferResponse DTO`
- Priority: High

**Child 3:**
- Summary: `Implement TransferService.transfer() method`
- Priority: High

**Child 4:**
- Summary: `Implement TransferController POST /api/transfers endpoint`
- Priority: High

**Child 5:**
- Summary: `Build TransferForm.jsx with client-side validation`
- Priority: Medium

**Child 6:**
- Summary: `Write unit tests for TransferService`
- Priority: High

4. After creating all 6, verify they appear under MTS-2's Child issues section
5. Check the **Board** — child issues should appear as sub-items under MTS-2

> **V-Model connection**: Notice child issues 1-4 are the development side (left of V). Child issue 6 is the testing side (right of V). Unit tests verify the detailed design — the V-Model in action within a single story.

---

## Lab 2.7 — Dev Works Through Child Issues

### The Scenario

You (Dev) start implementing the UPI transfer feature, working through child issues one by one.

### Lab Steps

1. Move **MTS-2** (parent story) to **IN PROGRESS** on the Board
2. Open **Child 1** (TransferRequest DTO) → transition to **IN PROGRESS**
3. Add a comment on Child 1:

```
Implementing TransferRequest with Jakarta validations:
- @NotBlank fromAccountNumber, toAccountNumber
- @NotNull @DecimalMin("1.00") @DecimalMax("1000000.00") amount
- @NotNull TransferMode (UPI, NEFT, IMPS, RTGS)
- @Size(max=255) description
```

4. Transition Child 1 to **DONE**
5. Transition **Child 2** (TransferResponse DTO): TO DO → IN PROGRESS → DONE
6. Transition **Child 3** (TransferService): TO DO → IN PROGRESS
7. Add a comment on Child 3:

```
Implementing core transfer logic:
- Validate both accounts exist and are active
- Check sender has sufficient balance
- Debit sender, credit receiver (atomic transaction)
- Generate UUID reference ID
- Return TransferResponse with status
```

8. Transition Child 3 to **DONE**
9. Transition **Child 4** (TransferController): TO DO → IN PROGRESS → DONE

### Check the Board

- MTS-2 should still be IN PROGRESS (parent stays in progress until all children are done)
- 4 child issues should be in DONE
- 2 child issues (TransferForm.jsx, unit tests) still in TO DO

---

## Lab 2.8 — QA Finds the First Bug!

### The Scenario

Switch to the **QA hat**. While the Dev is still working on the remaining child issues, you start testing the completed backend API. You discover a bug.

### What is a Bug?

- A defect — actual behavior doesn't match expected behavior
- Yesterday in STLC: *"When Expected != Actual → Defect"*
- A good bug report includes:
  - **Summary** — what failed, in one line
  - **Steps to Reproduce** — exact actions to trigger it
  - **Expected Result** — what should happen (from acceptance criteria)
  - **Actual Result** — what actually happened
  - **Environment** — where you tested
  - **Severity/Priority** — impact and urgency

### Lab Steps — Create Bug 1

1. Click **Create**
2. Fill in:
   - **Issue Type**: Bug
   - **Summary**: `Transfer succeeds when sender account is inactive`
   - **Description**:
     ```
     Steps to Reproduce:
     1. Use account ACC003 (priya.sharma, is_active = false)
     2. POST /api/transfers with fromAccountNumber=ACC003, toAccountNumber=ACC001, amount=500, transferMode=UPI
     3. Observe the response

     Expected Result:
     - Error response: "Account is inactive, please contact support"
     - Transfer should be rejected

     Actual Result:
     - Transfer succeeds with 200 OK
     - Balance is deducted from inactive account

     Environment: Local dev, Spring Boot 3.x, H2 database
     Severity: Major
     Root Cause: TransferService.transfer() does not check account isActive flag
     ```
   - **Priority**: High
   - **Labels**: `backend`, `bug`
3. Click **Create**
4. Note the issue key

> **STLC connection**: This is **STLC Stage 5 — Test Execution** and **Stage 6 — Defect Reporting**. The bug follows the exact defect report template from yesterday — summary, steps, expected vs actual, environment.

---

## Lab 2.9 — Link the Bug to the Story

### Why Link?

- Traceability: this bug was **caused by** the UPI transfer story implementation
- When Dev opens the story, they see related bugs immediately
- When QA tracks bugs, they can trace back to which requirement was affected

### Lab Steps

1. Open the bug you just created
2. Click **Link**
3. Configure:
   - **Link type**: `is caused by`
   - **Issue**: search for the UPI transfer story → select it
4. Click **Link**
5. Verify the link appears on both issues

---

## Lab 2.10 — QA Finds a Second Bug

### The Scenario

You (QA) continue testing and find another issue — this time on the frontend.

### Lab Steps — Create Bug 2

1. Click **Create**
2. Fill in:
   - **Issue Type**: Bug
   - **Summary**: `Insufficient balance error not displayed on TransferForm`
   - **Description**:
     ```
     Steps to Reproduce:
     1. Open MTS dashboard in browser
     2. Select From: ACC004 (balance: INR 30,000)
     3. Select To: ACC001
     4. Enter amount: 50,000
     5. Select mode: RTGS
     6. Click "Transfer Funds"

     Expected Result:
     - Error message displayed: "Insufficient balance in account ACC004"
     - Transfer should not proceed

     Actual Result:
     - No error message shown on the UI
     - Request sent to backend, backend returns 400 error
     - Frontend silently fails — user sees nothing

     Environment: Chrome 120, React frontend
     Severity: Major
     Root Cause: TransferForm.jsx catch block doesn't extract error message from API response
     ```
   - **Priority**: High
   - **Labels**: `frontend`, `bug`
3. Click **Create**
4. Link this bug: **is caused by** → UPI transfer story

---

## Lab 2.11 — Dev Fixes the Bug and QA Verifies

### The Scenario

Switch to **Dev hat** → fix the bug. Then switch to **QA hat** → verify the fix.

### Lab Steps — Dev Fixes Bug 1

1. Open **Bug 1** (inactive account transfer)
2. Transition: **TO DO → IN PROGRESS**
3. Add a comment:

```
Fix: Added isActive check in TransferService.transfer()

if (!fromAccount.getIsActive()) {
    throw new AccountInactiveException("Account is inactive, please contact support");
}

Added before balance validation. Unit test added.
```

4. Transition: **IN PROGRESS → DONE**

### Lab Steps — QA Verifies Bug 1

1. Open **Bug 1** again
2. Add a comment (as QA):

```
Verification Result: PASSED

Tested with:
- ACC003 (inactive) → correctly returns error "Account is inactive, please contact support"
- ACC001 (active) → transfer succeeds as expected

Bug is verified and closed.
```

### The Defect Lifecycle in Action

```
TO DO → IN PROGRESS (Dev fixing) → DONE (Dev fixed) → Verified by QA via comment
```

> **STLC connection**: This is the full **defect lifecycle** from yesterday: New → Triaged → In Progress → Fixed → Verified → Closed. In JIRA, workflow transitions + comments capture this entire flow.

---

## Lab 2.12 — Dev Finishes Remaining Child Issues

### Lab Steps

1. Transition **Child 5** (TransferForm.jsx): TO DO → IN PROGRESS → DONE
2. Transition **Child 6** (Unit tests): TO DO → IN PROGRESS → DONE
3. Add a comment on Child 6:

```
Unit tests implemented:
- testTransferSuccess() - valid transfer between active accounts
- testTransferInsufficientBalance() - reject when balance too low
- testTransferInactiveAccount() - reject when sender inactive
- testTransferSameAccount() - reject when from == to
- All 4 tests passing
```

4. All 6 child issues are now DONE
5. Transition **MTS-2** (parent story) to **DONE**

---

## Lab 2.13 — Complete the View Balance Story

### Lab Steps

1. Transition **MTS-3** (View balance) to **IN PROGRESS**
2. Add a comment:

```
Implementing Dashboard with AccountCard components.
- Fetching accounts from GET /api/accounts
- Rendering AccountCard for each account
- Auto-refresh after transfer via refreshTrigger state
```

3. Transition **MTS-3** to **DONE**

---

## Lab 2.14 — Complete the Sprint

### The Scenario

All planned items are done. Time to close the sprint.

### Lab Steps

1. Click **Board** in the sidebar
2. Verify all issues are in the **DONE** column:
   - MTS-4 (Task: DB schema) — DONE
   - MTS-2 (Story: UPI transfer) — DONE
   - MTS-3 (Story: View balance) — DONE
   - Bugs should also be in DONE
3. Click **Complete sprint** button (top-right of board)
4. A dialog appears showing:
   - Completed issues count
   - Any incomplete issues (should be none)
   - Option to move incomplete issues to backlog or next sprint
5. Click **Complete**

---

## Lab 2.15 — Review Sprint Reports

### Why Reports?

- Reports give visibility into team performance
- Used during **Sprint Retrospective** to discuss what went well and what to improve
- Help calibrate future sprint capacity (velocity)

### Lab Steps

1. Click **Reports** in the sidebar
2. Explore each report:

**Burndown Chart:**
1. Select the completed sprint
2. Observe:
   - X-axis: days of the sprint
   - Y-axis: remaining story points (or issue count)
   - Ideal line: straight diagonal from total to zero
   - Actual line: how work was actually completed
3. If all work was done quickly, the actual line drops steeply — shows the team finished early

**Velocity Chart:**
1. Shows story points completed per sprint
2. Sprint 1: 8 points completed
3. Over time, this chart shows if the team is getting faster, slower, or staying consistent
4. Used to forecast future sprints — "we can do ~8 points per sprint"

**Sprint Report:**
1. Shows completed vs not completed issues
2. Lists all issues with their final status
3. Shows story points committed vs completed

> **Agile connection**: Velocity is the team's average story points per sprint. After 3-4 sprints, velocity stabilizes and becomes a reliable forecasting tool. Sprint 1 velocity = 8 points.

---

## Summary — What We Built in Level 2

### Sprint 1 Results

| Metric | Value |
|--------|-------|
| Sprint Name | Sprint 1 - Transfer Found |
| Duration | 2 weeks |
| Stories Completed | 2 (UPI transfer + View balance) |
| Tasks Completed | 1 (DB schema) |
| Story Points Committed | 8 |
| Story Points Completed | 8 |
| Bugs Found | 2 |
| Bugs Fixed | 1 (inactive account), 1 (open — frontend error display) |
| Velocity | 8 pts/sprint |

### All Issues

| Key | Type | Summary | Status |
|-----|------|---------|--------|
| MTS-1 | Epic | Fund Transfer Module | TO DO (epic stays open — more work in future sprints) |
| MTS-2 | Story | Transfer money via UPI | DONE |
| MTS-3 | Story | View account balance | DONE |
| MTS-4 | Task | DB schema & seed data | DONE |
| MTS-5+ | Sub-tasks | 6 child issues under MTS-2 | DONE |
| MTS-X | Bug | Transfer succeeds with inactive account | DONE |
| MTS-Y | Bug | Insufficient balance error not displayed | DONE |

---

## JIRA ↔ SDLC/STLC Concepts

| What We Did in Level 2 | SDLC/STLC Concept |
|-------------------------|-------------------|
| Created a sprint with a goal | Agile Scrum — time-boxed iteration |
| Sprint planning: pulled items from backlog | Sprint Planning ceremony |
| Started sprint | Development phase begins |
| Transitioned TO DO → IN PROGRESS → DONE | SDLC: Development → Testing → Deployment |
| Created child issues under a story | V-Model: Detailed Design → Unit Tests |
| QA found bugs during sprint | STLC Stage 5: Test Execution |
| Created bug with steps/expected/actual | STLC Stage 6: Defect Reporting |
| Linked bug "is caused by" story | RTM: Traceability — defect traced to requirement |
| Dev fixed bug, QA verified | Defect Lifecycle: New → In Progress → Fixed → Verified |
| Completed sprint | Sprint Review — deliver working increment |
| Reviewed burndown & velocity | Sprint Retrospective — measure and improve |

---

## Checklist

- [ ] Created Sprint 1 with name, goal, and duration
- [ ] (As PO) Pulled 3 items into the sprint from backlog
- [ ] Started the sprint
- [ ] (As Dev) Transitioned DB task: TO DO → IN PROGRESS → DONE
- [ ] (As Dev) Created 6 child issues under UPI transfer story
- [ ] (As Dev) Worked through child issues with transitions and comments
- [ ] (As QA) Found and reported Bug 1 (inactive account) with proper defect format
- [ ] (As QA) Found and reported Bug 2 (frontend error display)
- [ ] Linked both bugs to the UPI transfer story
- [ ] (As Dev) Fixed Bug 1 with code comment
- [ ] (As QA) Verified Bug 1 fix with test evidence
- [ ] Completed all stories and tasks
- [ ] Completed the sprint
- [ ] Reviewed Burndown Chart
- [ ] Reviewed Velocity Chart
- [ ] Reviewed Sprint Report

---

## What's Next?

**Level 3** — Dashboards, Confluence Integration & SDLC Role Play:
- Create a JIRA Dashboard with gadgets (filter results, pie charts, sprint health)
- Connect JIRA to Confluence for project documentation
- Full SDLC Role Play — simulate a complete feature delivery as a team
