# Role Cards -- Print & Cut

Print this file. Cut along the lines. Distribute one card per person (face down).

---

## SCENARIO CARD (1 per group -- read aloud before starting)

> FoodExpress runs a sustain engineering team of 5. The team uses GitHub for version control, follows a trunk-based development workflow, and deploys to production twice a week. Standups are held at 9:30 AM every morning. PRs must be reviewed and approved by at least one peer before merge.

---
---

## ROLE CARD A -- Senior Backend Engineer

**Yesterday:** You completed the fix for a database query that was causing slow load times on the restaurant listing page. You merged PR #341 after getting two approvals.

**Today:** You are starting work on FE-100 (push notification fix for Android 14). You need to read the Firebase documentation before writing any code.

**Blocker:** None currently, but you are waiting on the DevOps team to provision a test Android device on the CI pipeline. You raised this ticket 3 days ago and have not heard back.

**Instructions:** Mention the blocker clearly. Do not go into technical detail about the database fix -- save that for a separate conversation if anyone asks.

---
---

## ROLE CARD B -- Frontend Engineer

**Yesterday:** You were supposed to complete the UI changes for the saved addresses feature (FE-97) but got pulled into an unplanned meeting with the restaurant partner team for 3 hours. You completed only the address list component. The address form component is not started.

**Today:** You will complete the address form component and submit it for review.

**Concern:** You are behind on FE-97. You originally estimated it at 3 days; you are now on Day 3 with one component remaining. You are not technically blocked but you are at risk of missing the sprint commitment.

**Instructions:** Be honest about being behind. Do not over-explain or make excuses. State the situation and what you are doing about it.

---
---

## ROLE CARD C -- QE Engineer

**Yesterday:** You wrote test cases for FE-96 (restaurant open/closed status fix) and executed them. All 12 test cases passed. FE-96 is ready to merge.

**Today:** You are picking up FE-95 (iOS cart crash) for testing. You need a build from the iOS team first.

**Dependency:** You cannot start FE-95 testing until the Developer (Role A or D) gives you a build. Flag this dependency in the standup so it is visible to the Scrum Master.

**Instructions:** Keep it short. You have no blockers of your own but you need to surface the dependency.

---
---

## ROLE CARD D -- Junior Backend Engineer

**Yesterday:** You started work on FE-99 (payment gateway upgrade). You read the Razorpay v2 documentation and discovered that the webhook signature verification has changed. You are not sure how to implement it and spent 2 hours reading without writing code.

**Today:** You plan to pair with the Senior Backend Engineer (Role A) to work through the webhook problem.

**Blocker:** You are effectively blocked on writing code until you understand the webhook change. You feel embarrassed to say you are blocked because it is only your second sprint on this team.

**Instructions:** Say you are blocked. The Scrum Master role is to respond and pair you up -- this is the right outcome. Do not downplay the blocker.

---
---

## ROLE CARD E -- Scrum Master / Tech Lead

You facilitate the standup. Your responsibilities:

1. **Keep the timer.** Each person gets 90 seconds max. The standup must finish in 10 minutes.
2. **After each person speaks**, note any blockers on a paper/whiteboard.
3. **After all team members speak**, do the following:
   - Acknowledge Role D's blocker and propose that Role A pairs with Role D after standup
   - Acknowledge Role A's DevOps dependency and say you will chase that ticket today
   - Acknowledge Role B's risk and ask privately after standup (not in front of the group) whether sprint commitment is at risk
   - Tell Role C you will confirm with the developer when a build will be available

**Instructions:** Cut people off politely at 90 seconds. Do not let the standup become a design discussion. Resolve blockers AFTER the standup, not during it.

---
---

## ROUND 2 ROLES (PR Code Review) -- Assign within groups

### PR Author
You wrote the fix. Walk reviewers through your changes. Explain the bug, where it lived, and how your fix addresses it. Be open to feedback. Do not get defensive. If a reviewer raises something you had not considered, acknowledge it.

### Reviewer 1 (Logic Review)
Verify the fix is correct. Check: does it handle the edge case where `discountPercent` is `0`? Phrase feedback as questions: "Have you considered what happens when..."

### Reviewer 2 (Style & Tests Review)
Check code style and test coverage. Look for: debug logs left in code, missing unit tests, unnecessary complexity, unclear variable names. If there are no tests, the PR should not be merged -- state this clearly but without hostility.
