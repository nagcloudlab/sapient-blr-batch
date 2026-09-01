# Agile/DevOps Role Play Scenarios

**Module:** 19 -- Git & GitHub
**Context:** FoodExpress Food Delivery Application
**Total Time:** 60 minutes (two rounds + debrief)
**Group Size:** 4-5 participants per group

---

## Overview

These scenarios practise the daily collaboration rituals of a DevOps-oriented engineering team: the standup and the code review. Both are deceptively simple in theory and consistently mishandled in practice. The goal is to develop the habit of concise communication and constructive technical feedback.

---

## Scenario Card (distribute before Round 1)

> FoodExpress runs a sustain engineering team of 5. The team uses GitHub for version control, follows a trunk-based development workflow, and deploys to production twice a week. Standups are held at 9:30 AM every morning. PRs must be reviewed and approved by at least one peer before merge.

---

## Round 1: Daily Standup Simulation

**Duration:** 15 minutes
(10 min role play + 5 min debrief)

### Situation

It is Tuesday, 9:30 AM. The FoodExpress sustain engineering team is running its daily standup. The Scrum Master will keep a timer. Each person has a maximum of 90 seconds. The standup must finish in 10 minutes total. Participants speak in turn using the format: what did I do yesterday, what will I do today, what is blocking me.

### Role Cards (cut and distribute one per participant)

---

**Role Card A -- Senior Backend Engineer**

Yesterday: You completed the fix for a database query that was causing slow load times on the restaurant listing page. You merged PR #341 after getting two approvals.

Today: You are starting work on FE-100 (push notification fix for Android 14). You need to read the Firebase documentation before writing any code.

Blocker: None currently, but you are waiting on the DevOps team to provision a test Android device on the CI pipeline. You raised this ticket 3 days ago and have not heard back.

During the standup, mention the blocker clearly. Do not go into technical detail about the database fix -- save that for a separate conversation if anyone asks.

---

**Role Card B -- Frontend Engineer**

Yesterday: You were supposed to complete the UI changes for the saved addresses feature (FE-97) but got pulled into an unplanned meeting with the restaurant partner team for 3 hours. You completed only the address list component. The address form component is not started.

Today: You will complete the address form component and submit it for review.

Concern: You are behind on FE-97. You originally estimated it at 3 days; you are now on Day 3 with one component remaining. You are not technically blocked but you are at risk of missing the sprint commitment.

During the standup, be honest about being behind. Do not over-explain or make excuses. State the situation and what you are doing about it.

---

**Role Card C -- QE Engineer**

Yesterday: You wrote test cases for FE-96 (restaurant open/closed status fix) and executed them. All 12 test cases passed. FE-96 is ready to merge.

Today: You are picking up FE-95 (iOS cart crash) for testing. You need a build from the iOS team first.

Dependency: You cannot start FE-95 testing until the Developer (Role Card A or D) gives you a build. Flag this dependency in the standup so it is visible to the Scrum Master.

During the standup, keep it short. You have no blockers of your own but you need to surface the dependency.

---

**Role Card D -- Backend Engineer (Junior)**

Yesterday: You started work on FE-99 (payment gateway upgrade). You read the Razorpay v2 documentation and discovered that the webhook signature verification has changed. You are not sure how to implement it and spent 2 hours reading without writing code.

Today: You plan to pair with the Senior Backend Engineer (Role Card A) to work through the webhook problem.

Blocker: You are effectively blocked on writing code until you understand the webhook change. You feel embarrassed to say you are blocked because it is only your second sprint on this team.

During the standup, say you are blocked. The Scrum Master role is to respond and pair you up -- this is the right outcome. Do not downplay the blocker.

---

**Role Card E -- Scrum Master / Tech Lead (use if 5 participants)**

You facilitate the standup. Keep the timer. Cut people off politely at 90 seconds. After each person speaks, note any blockers on a whiteboard or paper.

After all four team members speak, do the following:
- Acknowledge Role D's blocker and propose that Role A pairs with Role D after standup.
- Acknowledge Role A's DevOps dependency and say you will chase that ticket today.
- Acknowledge Role B's risk and ask privately after standup (not in front of the group) whether sprint commitment is at risk.
- Tell Role C you will confirm with the developer when a build will be available.

If there are only 4 participants, the trainer plays the Scrum Master role.

---

### Objectives

By the end of Round 1, the group should have:
- Completed the standup in 10 minutes
- Surfaced all blockers and dependencies
- Avoided turning the standup into a status report or design discussion
- Demonstrated the Scrum Master's role in clearing blockers after the standup

---

### Round 1 Debrief Questions (5 minutes)

1. Was the standup completed within 10 minutes? If not, what caused it to run long?
2. Did Role D raise their blocker? If they downplayed it, why might a junior engineer do that on a real team? What is the cost to the team?
3. What is the difference between a standup and a status meeting? Did this standup feel like one or the other?
4. The Scrum Master resolved blockers after the standup, not during it. Why is this important?
5. Role B is behind on their commitment. Should this have been raised in the standup? How should the Scrum Master follow up?

---

## Round 2: Code Review / PR Review

**Duration:** 25 minutes
(18 min role play + 7 min debrief)

### Situation

A PR has been submitted to the FoodExpress GitHub repository to fix a bug: "Cart total shows NaN when a coupon code is applied and then removed." The Author has opened PR #347 and tagged two reviewers. The review session is synchronous (a PR walkthrough call, which some teams do for complex fixes).

### Roles

**Author (PR Submitter)**
You wrote the fix. Walk the reviewers through your changes at the start. Explain what the bug was, where it lived in the code, and how your fix addresses it. Be open to feedback. Do not get defensive. If a reviewer raises a concern you had not considered, acknowledge it and ask how they would approach it.

**Reviewer 1 (Logic Review)**
Your job is to verify that the fix is correct. Read the diff carefully. You will find one intentional issue in the code (described below). Raise it clearly and constructively. Phrase feedback as questions where possible ("Have you considered what happens when...") rather than as commands ("You should..."). Also check: does the fix handle the edge case where the coupon is invalid?

**Reviewer 2 (Style and Tests Review)**
Your job is to check code style and test coverage. Ask: are there unit tests for this fix? If there are no tests, the PR should not be merged -- state this clearly but without hostility. Check that variable names are clear. Check that the fix does not introduce unnecessary complexity. Look for any console.log statements left in the code.

### The Code Diff (provide this on a printed sheet or shared screen)

```
File: src/cart/cartUtils.js
Branch: fix/cart-total-nan-on-coupon-remove
PR #347

--- a/src/cart/cartUtils.js
+++ b/src/cart/cartUtils.js

@@ -12,14 +12,22 @@ function calculateCartTotal(items) {
   return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
 }

-function applyDiscount(total, coupon) {
-  if (coupon && coupon.discountPercent) {
-    return total - (total * coupon.discountPercent / 100);
-  }
-  return total;
+function applyDiscount(total, coupon) {
+  if (!coupon || coupon.discountPercent === undefined) {
+    return total;
+  }
+  const discount = total * coupon.discountPercent / 100;
+  return total - discount;
 }

 function getDisplayTotal(cartState) {
-  const raw = calculateCartTotal(cartState.items);
-  const discounted = applyDiscount(raw, cartState.activeCoupon);
-  return discounted;
+  if (!cartState || !cartState.items) {
+    return 0;
+  }
+  const raw = calculateCartTotal(cartState.items);
+  const discounted = applyDiscount(raw, cartState.activeCoupon);
+  console.log('Cart total calculated:', discounted);
+  return discounted;
 }

+// TODO: add coupon validation
+
 module.exports = { calculateCartTotal, applyDiscount, getDisplayTotal };
```

### What the Reviewers Should Find

**Reviewer 1 (Logic):**
The fix correctly guards against undefined coupon. However, there is an edge case not handled: if `coupon.discountPercent` is `0` (a valid value in some promotional scenarios), the condition `coupon.discountPercent === undefined` will pass, but a 0% discount is meaningless and may indicate a stale or misconfigured coupon. This is not necessarily a bug but is worth raising as a question.

**Reviewer 2 (Style and Tests):**
- The `console.log` statement on line +18 is a debug log that must not be in production code. This is a clear request for change.
- There are no new test cases submitted with this PR. The reviewer should ask: where are the tests? At minimum, a unit test for `getDisplayTotal` with a null `cartState` and a unit test for `applyDiscount` with a valid coupon, null coupon, and zero-discount coupon should be required.
- The `// TODO: add coupon validation` comment is acceptable to flag -- it signals incomplete work. Ask the Author whether this will be addressed in this PR or as a follow-up ticket.

### Objectives

By the end of Round 2, the group should have:
- Completed a structured PR walkthrough
- Identified the console.log issue and raised it as a required change
- Raised the missing test question
- Discussed the 0% discount edge case
- Reached a decision: approve with changes, request changes, or approve

---

### Round 2 Debrief Questions (7 minutes)

1. Was feedback delivered constructively? Were there any moments where phrasing felt like a personal criticism rather than a code observation?
2. Did Reviewer 2 require tests before approval? In your team's actual workflow, would this be enforced or optional? Should it be enforced?
3. The console.log issue is a clear defect in the PR. How did the group handle it? Was the Author defensive or receptive?
4. The TODO comment signals unfinished work. Is it acceptable to merge a PR with a TODO? What is the risk if this becomes a team habit?
5. What is the difference between a blocking comment and a non-blocking comment in a code review? Did the reviewers distinguish between the two?
6. What would a CI/CD pipeline catch automatically that the human reviewers might miss? How does this change the role of a code review?

---

## Facilitator Notes

- Print the code diff and role cards before the session. Do not put them on a shared screen until Round 2 begins.
- For Round 1 with only 4 participants, the trainer takes the Scrum Master role. This is intentional -- it lets the trainer model the correct facilitator behaviour.
- The code in the diff is deliberately simple. The point is not to test JavaScript knowledge but to practise the review conversation. Participants should be told this upfront if they are anxious about the code.
- In Round 2, if the Author becomes defensive when the console.log is raised, let the dynamic play out briefly, then pause and ask the group: "How did that feel? How would you reframe that feedback?"
- After both rounds, connect the scenarios: the standup identified that a PR was waiting for review. The PR review is what unblocked the QE. This end-to-end flow is how a healthy DevOps team operates daily.
