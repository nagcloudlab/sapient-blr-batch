# QE/QC Role Play Scenarios

**Module:** 13 -- Quality Engineering & Quality Control
**Context:** FoodExpress Food Delivery Application
**Total Time:** 70 minutes (two rounds + debrief)
**Group Size:** 4 participants per group

---

## Overview

These scenarios simulate real-world QE/QC situations that sustain engineering teams encounter. Participants take on defined roles and must make decisions under realistic constraints. The goal is to practise the communication, prioritisation, and analytical skills that quality engineers use daily.

---

## Scenario Card (distribute before Round 1)

> FoodExpress has 2.4 million monthly active users across 12 cities. The engineering team runs two-week sprints. The QE team of 4 is shared across 3 product squads. The current sprint is Sprint 21.

---

## Round 1: Test Plan Defense

**Duration:** 25 minutes
(15 min role play + 10 min debrief)

### Situation

FoodExpress is launching a "Loyalty Rewards" feature in Sprint 22. Users earn points for every order and can redeem them for discounts. The QE Lead must present the test plan to the stakeholder group before sign-off is granted. The stakeholders have concerns about timeline, coverage, and risk.

### Roles

**QE Lead**
You are presenting the test plan. Your goal is to get sign-off. Be prepared to defend your coverage decisions and timeline estimates. You have planned 5 days of testing across functional, regression, performance, and edge cases.

**Developer**
You built the Loyalty Rewards backend. You believe the unit tests you wrote are sufficient and that the QE team is duplicating effort. Challenge the test coverage on areas where you have unit tests. Ask why integration testing is needed if each component is already tested in isolation.

**Product Owner**
You are under pressure to ship this feature before a competitor does. Your priority is speed. Push back on the 5-day testing window. Ask whether 3 days is possible. Ask specifically about what can be descoped from the test plan without adding significant risk.

**Stakeholder (Head of Operations)**
You were burned by a past production incident where a points calculation bug gave customers 10x rewards, costing the company money. Ask hard questions about how edge cases are being handled. Ask what happens if the redemption service goes down mid-order. Focus on business risk.

### Test Plan Summary (QE Lead reference)

The QE Lead should verbally present the following plan:

**Functional Testing (2 days)**
- Points earn on order completion
- Points calculation accuracy (1 point per Rs 10 spent)
- Redemption flow (minimum 100 points to redeem)
- Points expiry (points expire after 90 days of inactivity)
- Account merge (if user has two accounts, points should consolidate)

**Regression Testing (1 day)**
- Checkout flow (redemption touches payment)
- Order history (points earned should appear in history)
- User profile (points balance display)

**Performance Testing (1 day)**
- Points calculation under 5000 concurrent orders
- Redemption service response time under load

**Edge Cases (1 day)**
- Order cancelled after points awarded -- rollback
- Partial redemption (user redeems more than available balance)
- Negative points scenario (refund on an order that earned points)
- Points awarded for fraudulent orders

### Objectives

By the end of Round 1, the group should have:
- Negotiated a final test scope and timeline
- Identified at least 2 areas of genuine risk
- Reached a conditional or full sign-off decision

---

### Round 1 Debrief Questions (10 minutes)

1. Was the test plan comprehensive? What testing types were missing entirely?
2. Which stakeholder challenge was hardest to respond to? Why?
3. When the Developer pushed back on integration testing, how did the QE Lead justify it? Was the justification sound?
4. Did the group reach a sign-off? If conditions were attached, were they reasonable?
5. What would happen in a real project if testing was cut from 5 days to 3 days for this feature?
6. Name one edge case that was not in the plan but should have been.

---

## Round 2: Production Bug Triage

**Duration:** 25 minutes
(15 min role play + 10 min debrief)

### Situation

It is Friday, 4:30 PM. The QE Lead has just received a dump of 8 production bugs reported by the support team and monitoring alerts. The team must triage all 8 bugs, assign severity and priority, and decide which 4 will be fixed in the current sprint (which ends Sunday). The remaining bugs go to the backlog.

Sprint capacity remaining: approximately 2 developer-days.

### Roles

**QE Lead**
You facilitate the triage meeting. Your job is to drive the group to a decision within 15 minutes. Keep the discussion focused. Document severity (S1-S4) and priority (P1-P4) for each bug. Ensure the team commits to exactly 4 bugs for this sprint.

**Dev Lead**
You estimate the effort for each fix. You know the codebase. Give realistic effort estimates (in hours). Push back if the team is trying to squeeze in too much. Remind the group that a complex fix done badly creates more bugs.

**Product Owner**
You represent the business. You are the voice of revenue impact and customer experience. You want the payment bug fixed immediately but are less concerned about cosmetic issues. You also know that a major food critic is reviewing the app this weekend -- you want the app to look polished.

**Ops Lead**
You are reporting real-time impact from monitoring dashboards. You know which bugs are actively affecting users right now. You have data: error rates, affected user counts, geographic spread. Use the impact data below when speaking.

### The 8 Bugs

| # | Bug | Ops Impact Data | Dev Effort Estimate |
|---|-----|-----------------|---------------------|
| B1 | Payment failure on orders above Rs 2000 | 340 failed transactions in last 2 hours. Rs 68,000 revenue lost. Affects all cities. | 3 hours |
| B2 | Delivery ETA shows incorrect time (always 15 min regardless of distance) | Affects 100% of active orders. No direct failure but high complaint volume. | 4 hours |
| B3 | Menu images broken on restaurant pages (404 errors) | Affects 23 restaurants. Images hosted on old CDN endpoint. | 1 hour |
| B4 | Search returns stale results (cached for too long) | Results 40 min stale. Two restaurants show as open when they are closed. | 5 hours |
| B5 | Cart does not update quantity when user taps +/- button | Workaround: remove and re-add item. Affects mobile app only. | 6 hours |
| B6 | Email order confirmation delayed by 45-90 minutes | Email queue backlog. No order loss. Users are calling support thinking order failed. | 2 hours |
| B7 | Rating not saving when submitted from order history | Silent failure -- no error shown. Affects restaurant ratings accuracy over time. | 3 hours |
| B8 | Order history shows wrong restaurant name for 3 orders | Data mapping bug introduced in last deploy. Affects ~60 users. | 2 hours |

Total dev capacity: approximately 16 hours (2 developer-days).
The team must pick 4 bugs whose combined effort fits within capacity and justifies the selection with clear criteria.

### Objectives

By the end of Round 2, the group should have:
- Assigned severity and priority to all 8 bugs
- Selected exactly 4 bugs for immediate fix with justification
- Documented the rationale for what was deferred
- Agreed on whether any deferred bugs need a customer communication

---

### Round 2 Debrief Questions (10 minutes)

1. How did the group approach prioritisation? Did they use a framework or go by instinct?
2. Did anyone confuse severity with priority? (Severity = how bad is it. Priority = how soon must it be fixed.) Give an example from the discussion.
3. B2 (wrong ETA) affects 100% of users but does not cause a transaction failure. B1 (payment failure) affects fewer users but causes direct revenue loss. How did the group weigh these two?
4. Was the Product Owner's concern about the food critic review a legitimate prioritisation input or a distraction?
5. Which bugs were deferred? Do any of the deferred bugs have a ticking clock (i.e., will they get worse over time)?
6. Were any customer communications recommended for deferred bugs? Should there have been?

---

## Facilitator Notes

- Print role cards separately so participants only see their own role instructions.
- For Round 2, write the 8 bugs on a whiteboard or shared screen so the full group can see them during triage.
- Encourage the Ops Lead to volunteer impact data proactively rather than waiting to be asked -- this is realistic.
- If the group finishes early, introduce a complication: a ninth bug arrives mid-triage (e.g., the app crashes on login for users on Android 12).
- The goal is not to reach the "right" answer. The goal is to practise the process and language of QE triage.
