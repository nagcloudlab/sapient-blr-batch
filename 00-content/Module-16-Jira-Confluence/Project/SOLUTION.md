# Module 16 Solutions -- TRAINER ONLY

## Exercise 1: Sample Jira Issues

### Issue 2: User Story (Sample Answer)

```
Summary: Re-order last meal with one click
Type: Story
Priority: P2
Component: Order Service
Story Points: 5
Epic Link: FOOD-EPK-01 (Order Experience Improvement)

Description:
As a customer,
I want to re-order my last meal with one click,
So that I can save time when ordering my favorites.

Acceptance Criteria:
1. Given I am on the order history page, when I click "Re-order"
   on a past order, then my cart is populated with the same items
   from that order.
2. Given the original restaurant is now closed/inactive, when I
   click "Re-order", then I see "Restaurant is currently unavailable".
3. Given an item from the original order is no longer on the menu,
   when I click "Re-order", then I see a warning listing unavailable
   items and the remaining items are added to the cart.
```

### Issue 3: Bug Report (Sample Answer)

```
Summary: [Order Service] Confirmation email shows Rs 0.00 for COD orders
Type: Bug
Priority: P2 (Major)
Component: Notification Service
Labels: sustain, payment, regression
Fix Version: v2.4

Environment: Production
Browser/OS: All (email rendering)
Frequency: 100% for COD orders

Steps to Reproduce:
1. Log in as customer (test account: priya@test.com)
2. Add items to cart totaling Rs 549
3. Select "Cash on Delivery" as payment method
4. Place the order
5. Check the confirmation email

Expected Result:
Email shows "Total: Rs 549.00"

Actual Result:
Email shows "Total: Rs 0.00"

Root Cause Hypothesis:
The email template reads the `charged_amount` field, which is Rs 0
for COD orders since no payment is charged upfront. It should read
the `total_amount` field instead.

Impact:
- All COD orders (~40% of total) show Rs 0 in confirmation email
- Customers confused and calling support
```

### Issue 6: Bug with Links

```
Summary: [Payment] Promo code FLAT100 gives percentage discount instead of flat Rs 100
Type: Bug
Priority: P1 (Critical)
Component: Payment Service
Labels: sustain, promo, financial-impact

Links:
- Relates to: FOOD-XXX (COD email bug -- both are payment display issues)
- Blocks: FOOD-200 (Launch of new promo campaign)

Description:
The promo code "FLAT100" is configured as a flat Rs 100 discount but
the system interprets it as 100% discount, making orders free.

Steps to Reproduce:
1. Add any item to cart
2. Apply promo code "FLAT100"
3. View total

Expected: Total reduced by Rs 100
Actual: Total reduced by 100% (becomes Rs 0)
```

## Exercise 2: JQL Answers

| # | Scenario | JQL |
|---|----------|-----|
| 1 | All open bugs | `project = FOOD AND type = Bug AND status != Done` |
| 2 | P1 bugs unassigned | `project = FOOD AND type = Bug AND priority = P1 AND assignee is EMPTY` |
| 3 | My issues not done | `project = FOOD AND assignee = currentUser() AND status != Done` |
| 4 | Bugs created last 7 days | `project = FOOD AND type = Bug AND created >= -7d` |
| 5 | Current sprint | `project = FOOD AND sprint in openSprints()` |
| 6 | Stories > 8 points | `project = FOOD AND type = Story AND "Story Points" > 8` |
| 7 | Order Service blocked | `project = FOOD AND component = "Order Service" AND status = Blocked` |
| 8 | Reopened bugs | `project = FOOD AND type = Bug AND status was Done AND status != Done` |
| 9 | Updated last 24 hours | `project = FOOD AND updated >= -1d` |
| 10 | Overdue | `project = FOOD AND due < now() AND status != Done` |
| 11 | Regression label | `project = FOOD AND labels = "regression"` |
| 12 | Resolved in v2.4 | `project = FOOD AND fixVersion = "v2.4" AND status = Done` |

### Dashboard Design (Sample)

| # | Gadget | JQL / Config | Insight |
|---|--------|-------------|---------|
| 1 | Pie Chart (Priority) | `project = FOOD AND type = Bug AND status != Done` | Bug distribution by priority -- shows if P1s are piling up |
| 2 | Filter Results | `project = FOOD AND priority = P1 AND status != Done` | List of all open P1 issues -- immediate attention needed |
| 3 | Sprint Burndown | Current sprint | Is the team on track to complete sprint commitment? |
| 4 | Created vs Resolved | `project = FOOD AND type = Bug` (by week) | Are we fixing bugs faster than they are created? |

## Exercise 3: Confluence Answers

### Runbook Key Points
- Must include exact commands (not "restart the service" but `sudo systemctl restart foodexpress-order`)
- Must include verification (how to check it is actually running after restart)
- Must include rollback (what if restart makes things worse)
- Must include escalation with names and contact methods

### RCA Key Points
**Timeline:**
| Time | Event |
|------|-------|
| 14:20 | Staging deployment script runs |
| 14:25 | Script accidentally targets production (wrong MONGODB_URI) |
| 14:30 | Production MONGODB_URI now points to staging DB |
| 14:30 | First 503 errors appear |
| 14:45 | Alert fires (15 min delay) |
| 15:00 | Engineer identifies wrong MONGODB_URI in production config |
| 15:10 | MONGODB_URI corrected, service restarted |
| 15:15 | Service restored |

**Root Cause:** Staging deployment script modified the production environment variable MONGODB_URI because the script used a shared config file without environment isolation.

**Contributing Factors:**
1. No environment isolation in deployment scripts
2. No config change alerts/approval for production
3. Alert delay of 15 minutes

**Action Items:**
1. Separate staging and production deployment scripts completely
2. Add config change detection and alert (alert on any env var change in production)
3. Require approval for production config changes via change management
4. Reduce alert threshold from 15 min to 2 min for 503 errors

## Exercise 4: Kanban Board Design

| Column | WIP Limit | Justification |
|--------|-----------|---------------|
| Backlog | No limit | Queue for incoming work |
| Triaged | 10 | Limit to prevent too much analysis-without-action |
| In Progress | 3 | Focus: prevent context switching; team of 5, but max 3 active |
| Code Review | 2 | Keep reviews moving; if full, reviewers prioritize |
| Testing | 2 | QA capacity limit; prevents testing backlog |
| Deploying | 1 | One deployment at a time for safety |
| Done | No limit | Completed work |

**Swimlanes:** By priority (P1 on top, P2-P4 below)
**Card Colors:** Red = Bug, Blue = Story, Green = Task, Yellow = Sub-task
**Quick Filters:** "My Issues", "P1 Only", "Bugs Only", "This Week"

## Hints

| Exercise | Level 1 | Level 2 |
|----------|---------|---------|
| #1 | "A good bug report must be reproducible" | "Include: steps, expected, actual, environment, evidence" |
| #2 | "JQL format: field operator value" | "Use currentUser(), openSprints(), now(), -7d for dynamic values" |
| #3 | "A runbook should be followable by someone unfamiliar with the system" | "Include exact commands, expected output, and what to do if output differs" |
| #4 | "WIP limits prevent overload and make bottlenecks visible" | "If a column is always at its limit, that is the bottleneck to address" |
| #5 | "Sprint goal should be a sentence, not a list of issues" | "Example: 'Stabilize payment flow and add order tracking for mobile'" |
