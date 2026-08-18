# JIRA Lab — Kanban: Continuous Flow with WIP Limits

> **Domain**: MTS (Money Transfer System)
> **Time**: ~30 minutes
> **Project**: MTSK (MTS Kanban)
> **Board Type**: Kanban
> **Prerequisite**: Atlassian account with JIRA access

---

## Scrum vs Kanban — When to Use What?

| Aspect | Scrum | Kanban |
|--------|-------|--------|
| **Cadence** | Fixed sprints (1–4 weeks) | Continuous flow — no time-boxes |
| **Planning** | Sprint planning — commit to a set of items | No planning ceremony — pull when ready |
| **WIP Limits** | Implicitly limited by sprint capacity | Explicitly set per column |
| **Roles** | PO, Scrum Master, Dev Team | No prescribed roles |
| **Change** | Discouraged mid-sprint | Welcome anytime — reprioritize freely |
| **Best for** | Feature development with regular releases | Support, bug fixes, ops, continuous delivery |
| **Metrics** | Velocity, Burndown | Lead time, Cycle time, Throughput |

**Rule of thumb**: Use Scrum when you ship in planned releases. Use Kanban when work arrives unpredictably and must flow continuously.

---

## Lab Setup — Create a Kanban Project

### Via JIRA UI

1. Click **Projects** → **Create project**
2. Select **Kanban** template
3. Configure:
   - **Name**: `MTS Kanban`
   - **Key**: `MTSK`
4. Click **Create**
5. JIRA creates a board with default columns:
   - **Backlog** → **Selected for Development** → **In Progress** → **Done**

### Via CLI (REST API)

```bash
curl -s -u "$EMAIL:$API_TOKEN" \
  -X POST -H "Content-Type: application/json" \
  "https://<your-domain>.atlassian.net/rest/api/3/project" \
  -d '{
    "key": "MTSK",
    "name": "MTS Kanban",
    "projectTypeKey": "software",
    "leadAccountId": "<your-account-id>",
    "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-kanban-classic"
  }'
```

---

## Lab K.1 — Create Work Items

### The Scenario

The team maintains the MTS platform. Work arrives continuously — new features, bug reports, and tech debt. There are no sprints; items are pulled as capacity allows.

### Work Items

| # | Type | Summary |
|---|------|---------|
| MTSK-1 | Task | Set up transaction history table |
| MTSK-2 | Story | View transaction history for an account |
| MTSK-3 | Bug | Transaction date shows UTC instead of IST |
| MTSK-4 | Task | Add pagination to transaction list API |

### Lab Steps (UI)

1. Click **Create** for each item above
2. Set the **Issue Type**, **Summary**
3. After creation, all 4 items appear in the **Backlog** column

### Lab Steps (CLI)

```bash
jira issue create -p MTSK -t Task -s "Set up transaction history table" --no-input
jira issue create -p MTSK -t Story -s "View transaction history for an account" --no-input
jira issue create -p MTSK -t Bug -s "Transaction date shows UTC instead of IST" --no-input
jira issue create -p MTSK -t Task -s "Add pagination to transaction list API" --no-input
```

> **Kanban principle**: Unlike Scrum, there is no sprint backlog. Items sit in the Backlog column until someone pulls them. New items can be added at any time without disrupting ongoing work.

---

## Lab K.2 — Set WIP Limits

### What are WIP Limits?

- **WIP = Work In Progress** — the number of items allowed in a column at any time
- WIP limits prevent overloading the team — "Stop starting, start finishing"
- If a column is at its WIP limit, no new items can be pulled in until one moves out
- Typical WIP limit for a small team: **2–3 items** in the In Progress column

### Lab Steps

1. Go to **Board settings** (gear icon on the board)
2. Click **Columns**
3. Set the following WIP limits:
   - **Selected for Development**: `3`
   - **In Progress**: `2`
4. Click **Save**

> **Why WIP limits matter**: Without limits, teams start too many things and finish nothing. A WIP limit of 2 means: "finish something before starting something new." This reduces context switching and improves cycle time.

---

## Lab K.3 — Pull and Flow: The Kanban Way

### Key Concept: Pull System

In Kanban, work is **pulled** not pushed. A developer pulls the next highest-priority item only when they have capacity. This is the opposite of Scrum where work is assigned during sprint planning.

### Step 1 — Select Items for Development

**Scenario**: The team reviews the backlog and selects the most important items.

1. Drag **MTSK-1** (DB table setup) → **Selected for Development**
2. Drag **MTSK-3** (Bug — UTC date) → **Selected for Development**
   - Bugs often get priority in Kanban — no need to wait for next sprint!

**Board state:**

```
Backlog                 Selected for Dev        In Progress     Done
───────                 ────────────────        ───────────     ────
MTSK-2 (Story)          MTSK-1 (Task)
MTSK-4 (Task)           MTSK-3 (Bug)
```

### Step 2 — Dev Pulls into In Progress

**Scenario**: Dev has capacity. Pulls the top 2 items (WIP limit = 2).

1. Drag **MTSK-1** → **In Progress**
2. Drag **MTSK-3** → **In Progress**

**Board state:**

```
Backlog                 Selected for Dev        In Progress     Done
───────                 ────────────────        ───────────     ────
MTSK-2 (Story)                                  MTSK-1 (Task)
MTSK-4 (Task)                                   MTSK-3 (Bug)
```

> **WIP limit enforced**: In Progress has 2 items — the column is full. No more items can be pulled until one moves to Done.

### Step 3 — Bug Fixed, Pull Next

**Scenario**: The bug fix is quick (timezone config change). Dev finishes it first.

1. Drag **MTSK-3** → **Done**
   - WIP slot freed! Dev can pull the next item.
2. Drag **MTSK-1** → **Done**
   - DB table is set up.

**Board state:**

```
Backlog                 Selected for Dev        In Progress     Done
───────                 ────────────────        ───────────     ────
MTSK-2 (Story)                                                  MTSK-1 (Task)
MTSK-4 (Task)                                                   MTSK-3 (Bug)
```

### Step 4 — Pull Remaining Items

**Scenario**: Both In Progress slots are free. Dev pulls the next items.

1. Drag **MTSK-2** → **Selected for Development** → **In Progress**
2. Drag **MTSK-4** → **Selected for Development** → **In Progress**

### Step 5 — Complete All Work

1. Drag **MTSK-4** → **Done**
2. Drag **MTSK-2** → **Done**

**Final board state:**

```
Backlog                 Selected for Dev        In Progress     Done
───────                 ────────────────        ───────────     ────
                                                                MTSK-1 (Task)
                                                                MTSK-2 (Story)
                                                                MTSK-3 (Bug)
                                                                MTSK-4 (Task)
```

---

## Lab K.4 — Kanban Metrics

### Cumulative Flow Diagram (CFD)

1. Go to **Reports** → **Cumulative Flow Diagram**
2. Observe:
   - X-axis: time
   - Y-axis: number of issues
   - Each color band represents a column (Backlog, In Progress, Done)
   - The **width** of a band = how long items stay in that state
   - A widening "In Progress" band = bottleneck (work piling up)

### Control Chart

1. Go to **Reports** → **Control Chart**
2. Shows **cycle time** for each issue — how long from In Progress to Done
3. Look for:
   - **Average cycle time** — your team's typical delivery speed
   - **Outliers** — items that took unusually long (investigate why)

> **Kanban metrics focus on flow**, not velocity. The goal is to reduce cycle time and increase throughput — deliver more, faster, with less waste.

---

## Summary — Scrum vs Kanban in Practice

| What We Did | Scrum (Level 2) | Kanban (This Lab) |
|-------------|-----------------|-------------------|
| **Created work items** | Before sprint planning | Anytime — continuous |
| **Planned work** | Sprint planning ceremony | No ceremony — just prioritize the backlog |
| **Started work** | "Start Sprint" button | Pull from backlog when ready |
| **Managed flow** | Sprint scope is fixed | WIP limits control flow |
| **Handled bugs** | Added to sprint (mid-sprint disruption) | Pulled immediately — bugs jump the queue |
| **Completed work** | "Complete Sprint" — batch | Continuous — each item flows to Done independently |
| **Measured performance** | Velocity, Burndown chart | Cycle time, Cumulative Flow Diagram |

---

## Checklist

- [ ] Created a Kanban project (MTSK)
- [ ] Understood the Kanban board columns: Backlog → Selected for Dev → In Progress → Done
- [ ] Created 4 work items (1 Story, 1 Bug, 2 Tasks)
- [ ] Set WIP limit of 2 on In Progress column
- [ ] Pulled items from Backlog → Selected → In Progress (pull system)
- [ ] Respected WIP limits — finished items before pulling new ones
- [ ] Completed all items through continuous flow
- [ ] Reviewed Cumulative Flow Diagram
- [ ] Reviewed Control Chart
- [ ] Understood Scrum vs Kanban differences

---

## Key Takeaways

1. **No sprints** — Kanban is a continuous flow. Work is delivered as it's completed, not in batches.
2. **WIP limits are the core mechanism** — they prevent overload and force focus.
3. **Pull, don't push** — developers pull work when they have capacity.
4. **Bugs get fast-tracked** — no waiting for the next sprint to fix critical issues.
5. **Measure flow, not velocity** — cycle time and throughput tell you how efficient your process is.
6. **Both work** — Scrum and Kanban are tools. Pick the one that fits your team's work pattern.
