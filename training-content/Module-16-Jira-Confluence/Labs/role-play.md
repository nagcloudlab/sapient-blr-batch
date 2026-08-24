# SDLC Role Play Scenarios

**Module:** 16 -- SDLC, Jira & Confluence
**Context:** FoodExpress Food Delivery Application
**Total Time:** 65 minutes (two rounds + debrief)
**Group Size:** 5 participants per group

---

## Overview

These scenarios simulate sprint ceremonies that a sustain engineering team runs every two weeks. Participants practise the facilitation skills, estimation disciplines, and retrospective techniques that make Agile work in practice rather than in theory.

---

## Scenario Card (distribute before Round 1)

> FoodExpress engineering team runs two-week sprints. The team uses Jira for backlog management and Confluence for documentation. The current team velocity average is 38 story points per sprint over the last 4 sprints. The team is distributed across Bangalore and Hyderabad.

---

## Round 1: Sprint Planning

**Duration:** 25 minutes
(18 min role play + 7 min debrief)

### Situation

It is the first Monday of a new sprint. The team is running Sprint 14 planning. The Product Owner has groomed the backlog and the top items are ready for estimation. Team capacity for this sprint is 40 story points (two developers are on leave for 2 days each). The Scrum Master must facilitate the team to a committed sprint backlog.

### Roles

**Scrum Master**
You facilitate the planning session. Your job is to keep the meeting on track, ensure all voices are heard, and prevent over-commitment. Watch for stories that do not have clear acceptance criteria -- surface this as a blocker. Time-box discussions: no single story should take more than 3 minutes to discuss.

**Product Owner**
You have prioritised the backlog. Items higher on the list are more important to the business. You want the team to commit to as many high-priority items as possible. You believe the team sometimes under-estimates to protect themselves. Push gently for the team to take on FE-104 (the coupon feature) even if the team is uncertain about it.

**Developer 1 (Backend)**
You own backend estimates. You know that FE-99 (payment gateway upgrade) has a hidden complexity -- the vendor changed their API and documentation is incomplete. Raise this uncertainty when FE-99 comes up. You are confident about FE-97 and FE-100.

**Developer 2 (Frontend)**
You own frontend estimates. You have a dependency on FE-99 for FE-102 (checkout redesign) -- if FE-99 is not done by Day 7, FE-102 cannot be tested. Raise this dependency explicitly. You are also concerned about FE-104 because the designs are not finalised.

**QE**
You own testing effort estimates. Remind the team that every story needs a testing buffer -- you have seen three stories in the last sprint ship without test cases written. Ask about acceptance criteria before agreeing to any estimate. Flag if a story is entering the sprint without a test plan.

### Sprint 14 Backlog (10 items)

The team must select stories totalling no more than 40 points. Not all stories will fit.

| ID | Story | Priority | Dev Estimate | QE Estimate | Notes |
|----|-------|----------|-------------|------------|-------|
| FE-95 | Fix: Cart crashes on iOS 17.4 when adding more than 8 items | P1 | 3 pts | 2 pts | Carried over from Sprint 13. Bug confirmed in prod. |
| FE-96 | Fix: Restaurant open/closed status not refreshing | P2 | 2 pts | 1 pt | Reported by 3 restaurant partners. |
| FE-97 | Feature: Save delivery addresses (up to 5 per user) | P1 | 5 pts | 3 pts | Designs ready, AC defined. |
| FE-98 | Chore: Upgrade Node.js from 16 to 20 (LTS) | P2 | 3 pts | 2 pts | Security: Node 16 EOL next month. |
| FE-99 | Feature: Payment gateway upgrade (Razorpay v2 API) | P1 | 8 pts | 4 pts | Vendor API docs incomplete. High risk. |
| FE-100 | Fix: Push notifications not delivered on Android 14 | P2 | 3 pts | 2 pts | Affects ~12% of Android users. |
| FE-101 | Feature: Order tracking map (real-time driver location) | P1 | 8 pts | 5 pts | Designs ready. Backend API exists. |
| FE-102 | Feature: Checkout flow redesign (depends on FE-99) | P1 | 6 pts | 3 pts | Cannot start until FE-99 backend is done. |
| FE-103 | Chore: Migrate remaining API calls from REST to GraphQL | P3 | 5 pts | 2 pts | Technical debt item. No user impact. |
| FE-104 | Feature: Coupon code entry at checkout | P2 | 5 pts | 3 pts | Designs not finalised. AC incomplete. |

Total available points across all 10 stories: 84 points. Team capacity: 40 points.

### Objectives

By the end of Round 1, the group should have:
- Selected a sprint backlog totalling no more than 40 story points
- Identified and documented at least 2 dependencies or risks
- Flagged any stories with incomplete acceptance criteria
- Agreed on a sprint goal statement (one sentence)

---

### Round 1 Debrief Questions (7 minutes)

1. What stories made it into the sprint? What was left out? Was the cut logical?
2. Did the team over-commit or stay within capacity? If they over-committed, why did it happen?
3. Was the dependency between FE-99 and FE-102 surfaced and addressed? What is the risk if it was not?
4. How did the team handle FE-99 given the incomplete vendor documentation? Did they spike it, buffer it, or ignore the uncertainty?
5. Did QE get adequate time to review stories before committing? What happens when QE is not involved in estimation?
6. What was the sprint goal the team agreed on? Is it specific enough to use as a "definition of done" for the sprint?

---

## Round 2: Sprint Retrospective

**Duration:** 20 minutes
(13 min role play + 7 min debrief)

### Situation

Sprint 13 has ended. The team is running a retrospective. Two stories were not completed (carried over to Sprint 14). There was one production incident on Day 9 (a botched deploy that caused the search service to return empty results for 40 minutes). However, the NPS score from the last customer survey went up by 4 points, and the restaurant partner onboarding flow that shipped in Sprint 12 is receiving positive feedback.

The Scrum Master must facilitate the retrospective in 13 minutes. The format is: What Went Well / What Did Not Go Well / Action Items.

### Roles

**Scrum Master**
You facilitate. Timebox each section: 4 minutes for What Went Well, 4 minutes for What Did Not Go Well, 5 minutes for Action Items. Keep the tone blameless. If anyone uses the words "you should have" or "why didn't you," redirect them. The goal is systemic improvement, not personal accountability.

**Team Member 1 (Backend Developer)**
The two stories that were not completed are yours. FE-88 (payment reconciliation report) was blocked because the finance team did not provide the spec until Day 6. FE-89 (restaurant analytics dashboard) was underestimated -- it turned out to need a data warehouse query that you had not anticipated. Be honest but not defensive.

**Team Member 2 (Frontend Developer)**
You are frustrated about the production incident. You feel the deploy process is too loose -- there is no staging environment that mirrors production. You want to raise this as a systemic issue. Be constructive but firm. You also want to acknowledge that the team's pair programming sessions this sprint helped catch two bugs early.

**Team Member 3 (QE)**
You have data from Sprint 13: 14 bugs found in QE, 3 bugs found in production. You want to raise the fact that two stories were handed to QE on Day 9 (the last day before sprint end) with no time for proper testing. You want an action item around definition of ready for QE handover. Avoid blaming developers -- frame it as a process gap.

**Team Member 4 (Product Owner)**
You are pleased about the NPS improvement and want to make sure the team recognises what drove it. You are concerned about the two carry-over stories -- they were both promised to external stakeholders. You want to discuss whether the team's velocity forecasting is accurate enough. Avoid assigning blame for the incidents.

### Expected Retrospective Output

The facilitator should guide the group to produce:

**What Went Well (examples the team might raise)**
- NPS improvement (customer satisfaction trending positive)
- Pair programming sessions caught bugs early
- Restaurant partner onboarding feedback positive

**What Did Not Go Well (examples the team might raise)**
- Two stories carried over
- Production incident from deploy
- Stories handed to QE too late
- External dependency (finance team) not flagged early enough

**Action Items (must be specific and owned)**
Each action item needs: what will be done, who owns it, by when.

Example format: "QE will be included in story kick-off on Day 1 of each story. QE Lead owns this. Starting Sprint 14."

### Objectives

By the end of Round 2, the group should have:
- Identified at least 3 What Went Well items
- Identified at least 3 What Did Not Go Well items
- Agreed on at least 3 action items, each with an owner and a due date

---

### Round 2 Debrief Questions (7 minutes)

1. Were the action items specific and actionable? An action item like "improve communication" is not actionable. What would make it actionable?
2. Was blame avoided? Were there any moments where the discussion became personal rather than systemic?
3. The production incident was caused by a missing staging environment. Is the action item to "fix the deploy process" sufficient? What would a better action item look like?
4. Did the team acknowledge what went well genuinely, or did it feel perfunctory? Why does the "what went well" section matter?
5. The Product Owner raised velocity forecasting accuracy. Is this a valid retrospective topic, or is it a planning concern? Where is the line?
6. Which action item from your list is most likely to actually be followed up on? Which is most at risk of being forgotten?

---

## Facilitator Notes

- For Round 1, print the backlog table and give one copy per group. Participants can use sticky notes or a whiteboard to sort stories.
- For Round 2, write "What Went Well / What Did Not Go Well / Action Items" on a whiteboard with three columns before the session starts.
- The Scrum Master role in Round 1 is the most demanding. If the group is junior, brief that participant in advance.
- If groups finish Round 1 early, introduce a late-breaking item: the CTO has just asked whether the team can also take on a P0 hotfix (FE-94: login failure on Samsung Galaxy) which is estimated at 5 points. How does the team accommodate it?
- Remind participants that these ceremonies feel mechanical in training but become natural with repetition. The goal is to experience the friction and learn to resolve it.
