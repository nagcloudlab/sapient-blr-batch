# ITSM Role Play -- Major Incident War Room + Change Advisory Board

**Date:** Fri Sep 25, 2026 | **Day 42** | **Duration:** 90 min (including scoring)
**Context:** NPCI UPI -- Production Incident & Change Management (ties into ITSM/ITIL modules)
**Batch:** 26 participants (Pavan Jadhav has left) | **Groups:** 6 (4-5 per group)

---

## QUICK OVERVIEW (Read this first)

Two rounds back-to-back:
1. **Round 1 -- Major Incident Management (War Room)** (35-40 min) -- UPI transaction success rate drops to 40% during evening peak. Multiple banks affected. Settlement at risk. Groups must detect, classify, escalate, communicate, restore service.
2. **Round 2 -- Change Advisory Board (CAB) Meeting** (35-40 min) -- Three change requests for the next maintenance window. One risky database migration, one standard merchant onboarding, one emergency security patch. Groups must review, assess risk, approve/reject/defer with reasoning.

Then a **combined debrief + scoring** (15 min).

**Key learning:** ITSM processes are not bureaucracy -- they are structured decision-making frameworks that protect production systems. Incident Management saves you when things break. Change Management prevents them from breaking.

---

## GROUP ASSIGNMENTS (6 Groups of 4-5)

> Groups reshuffled from all previous role plays (Agile, Combined QE+SDLC, Behavioural) so participants work with different teammates. All 26 are active participants -- no facilitator/observer roles.

### Round 1: Major Incident War Room (5 roles per group)

#### Group 1 (5 members)
| Role | Participant |
|------|------------|
| Incident Commander | Sridhar Govindu |
| NOC Lead | Sinchana M K |
| Platform Engineer | Pappu Tejvardhan |
| Bank Liaison | Vedha Mateti |
| Service Desk Lead | Anirudh M |

#### Group 2 (4 members)
| Role | Participant |
|------|------------|
| Incident Commander | Aravind Anandhakumar |
| NOC Lead | Dega Dheepakkh |
| Platform Engineer | Tanuja K C |
| Bank Liaison / Service Desk Lead | Sai Ganesh |

#### Group 3 (5 members)
| Role | Participant |
|------|------------|
| Incident Commander | Riya Vengurlekar |
| NOC Lead | Sugesh K G |
| Platform Engineer | Pranav Sourya |
| Bank Liaison | Honna Reddy G |
| Service Desk Lead | Devanagouda |

#### Group 4 (4 members)
| Role | Participant |
|------|------------|
| Incident Commander | Dheeraj Naik |
| NOC Lead | Banashankari Anegundi |
| Platform Engineer | Surya Kausthub |
| Bank Liaison / Service Desk Lead | Eeshaan Bharadwaj |

#### Group 5 (4 members)
| Role | Participant |
|------|------------|
| Incident Commander | Yashas Sawai |
| NOC Lead | Dorai Sai Charan |
| Platform Engineer | Ridham Mishra |
| Bank Liaison / Service Desk Lead | Piyush Sidharth |

#### Group 6 (4 members)
| Role | Participant |
|------|------------|
| Incident Commander | Sushmitha G |
| NOC Lead | Sagar Sajjan |
| Platform Engineer | Hithesh S A |
| Bank Liaison / Service Desk Lead | Rahul S |

---

### Round 2: Change Advisory Board (roles rotate within same groups)

#### Group 1 (5 members)
| Role | Participant |
|------|------------|
| CAB Chair | Anirudh M |
| Change Requester | Sridhar Govindu |
| Risk Assessor | Vedha Mateti |
| Ops Lead | Sinchana M K |
| QA Lead | Pappu Tejvardhan |

#### Group 2 (4 members)
| Role | Participant |
|------|------------|
| CAB Chair | Sai Ganesh |
| Change Requester | Aravind Anandhakumar |
| Risk Assessor | Dega Dheepakkh |
| Ops Lead / QA Lead | Tanuja K C |

#### Group 3 (5 members)
| Role | Participant |
|------|------------|
| CAB Chair | Devanagouda |
| Change Requester | Riya Vengurlekar |
| Risk Assessor | Sugesh K G |
| Ops Lead | Pranav Sourya |
| QA Lead | Honna Reddy G |

#### Group 4 (4 members)
| Role | Participant |
|------|------------|
| CAB Chair | Eeshaan Bharadwaj |
| Change Requester | Dheeraj Naik |
| Risk Assessor | Banashankari Anegundi |
| Ops Lead / QA Lead | Surya Kausthub |

#### Group 5 (4 members)
| Role | Participant |
|------|------------|
| CAB Chair | Piyush Sidharth |
| Change Requester | Yashas Sawai |
| Risk Assessor | Dorai Sai Charan |
| Ops Lead / QA Lead | Ridham Mishra |

#### Group 6 (4 members)
| Role | Participant |
|------|------------|
| CAB Chair | Rahul S |
| Change Requester | Sushmitha G |
| Risk Assessor | Sagar Sajjan |
| Ops Lead / QA Lead | Hithesh S A |

---

## STEP-BY-STEP FACILITATION

### BEFORE YOU START (5 min) -- 15:00 to 15:05

1. **Rearrange seating** -- push tables together so each group sits in a circle
2. **Project the Scenario Card** on screen (or print 6 copies)
3. **Set expectations** (say this aloud):

> "Two rounds today. Round 1 -- it is Thursday, 7:02 PM during evening peak. UPI transaction success rate has crashed to 40%. Multiple banks are affected. Settlement processing is at risk. You are in the War Room. Detect, classify, escalate, communicate, restore."

> "Round 2 -- it is the following Tuesday. You are in the Change Advisory Board meeting. Three change requests are on the table. One is risky. One is routine. One is urgent. You must review each, assess risk, and decide: approve, reject, or defer."

> "Round 1 tests how you respond when things break. Round 2 tests how you prevent them from breaking. Together, they are the core of ITSM."

---

### ROUND 1: MAJOR INCIDENT WAR ROOM (35-40 min) -- 15:05 to 15:45

#### Your Script (say this):
> "Read your role card silently. You have 2 minutes."

**[2 min silent reading]**

> "It is Thursday, 7:02 PM. Peak evening hours. UPI transaction success rate has dropped to 40%. NPCI operations centre is lighting up. Multiple banks are reporting failures. The settlement batch for today runs at 11 PM and cannot be delayed. Go."

#### Scenario Card: NPCI UPI Major Incident (project on screen or print 6 copies)

```
----------------------------------------------------------------------
SCENARIO: UPI TRANSACTION SUCCESS RATE CRASH

Date: Thursday | Time: 7:02 PM IST (Peak Evening Hours)

SITUATION:
- UPI transaction success rate dropped from 99.2% to 40% at 6:47 PM
- Approximately 12 lakh transactions failing per hour
- Affected banks: SBI, HDFC, ICICI, Axis, Kotak (5 of top 10 by volume)
- Error pattern: "TIMEOUT" on UPI switch for inter-bank transactions
- Intra-bank transactions (same bank sender/receiver) working normally
- NPCI helpdesk receiving calls from 15+ bank operations teams
- Social media trending: #UPIDown (4,200 tweets in 30 minutes)
- Today's settlement batch runs at 11:00 PM -- cannot be delayed
- Estimated financial impact: Rs 180 crore/hour in failed transactions

KNOWN FACTS (from NOC monitoring):
- CBS (Central Banking Switch) latency spiked from 12ms to 4,200ms at 6:45 PM
- A scheduled config change was deployed to the CBS routing layer at 6:40 PM
  (CHG-4892: "Update routing weights for new bank onboarding")
- The config change passed pre-deployment validation
- No other changes were deployed today
- CBS cluster CPU at 94%, memory at 78%
- Transaction queue depth: 2.4 million (normal: <50,000)

YOUR TASK (15 minutes):
1. Classify this incident (P1/P2/P3?) and justify
2. Define the war room structure: who is in, who is notified, who leads
3. Decide: rollback the config change or investigate further?
4. Draft a communication to member banks (2-3 sentences)
5. Draft a public status page update (2-3 sentences)
6. Create a timeline of actions with owners and ETAs
----------------------------------------------------------------------
```

#### What YOU Do During Round 1

Walk between groups. **Listen for these specific things:**

| What to Watch | Good Sign | Red Flag |
|--------------|-----------|----------|
| Incident classification | "P1 -- national payment infrastructure, revenue impact Rs 180 crore/hr" | Classifying as P2 or debating severity vs priority for too long |
| Correlation with change | "Config change at 6:40, incident at 6:47 -- 7 min gap, likely related" | Not connecting the change to the incident |
| Rollback decision | Clear decision with rationale (rollback first, investigate later) | Paralysis -- "let's investigate before rolling back" while service is down |
| War room structure | IC assigns roles, sets communication cadence (every 10 min updates) | No structure, everyone talking over each other |
| Bank communication | Professional, factual, includes ETA and next update time | Vague ("we are looking into it"), no ETA, no next update time |
| Public communication | Honest, no over-promising, includes workaround if possible | Ignoring public comms or saying "resolved" prematurely |
| Settlement awareness | "Settlement batch at 11 PM -- we have 4 hours, but need buffer for reprocessing" | Forgetting about settlement entirely |
| Service Desk coordination | Tracking ticket volume, prepared FAQ for frontline agents | Service Desk ignored or sidelined |

**[15 min war room activity]**

#### Round 1 Presentations (15-20 min) -- each group presents for 2-3 min:

Each group shares:
1. How they classified the incident and why
2. Their rollback/investigate decision and reasoning
3. Their bank communication message (read aloud)
4. Their public status page update (read aloud)
5. Their action timeline with owners

#### Round 1 Debrief (5 min) -- ask the whole class:

1. "How many groups classified this as P1? What criteria did you use?" (Should be all groups -- national payment infrastructure, multi-bank, revenue > Rs 100 crore/hr)
2. "How many groups decided to rollback immediately vs investigate first?" (Best practice: rollback first. A config change 7 minutes before the incident is the most likely cause. Investigating while service is down costs Rs 3 crore per minute.)
3. "Read your bank communication. Does it include: (a) what happened, (b) current status, (c) next update time? All three are mandatory."
4. "Who remembered the 11 PM settlement batch? What happens if UPI is down past 10 PM?" (Settlement delay affects all banks' end-of-day reconciliation. RBI reporting implications.)
5. "In ITIL terms, what process did you just execute?" (Major Incident Management -- distinct from normal Incident Management in escalation path, communication cadence, and war room structure.)

---

### ROUND 2: CHANGE ADVISORY BOARD MEETING (35-40 min) -- 15:45 to 16:25

#### Your Script:
> "New round. Same groups, new roles. Pick up your new role card. It is now the following Tuesday, 10:00 AM. You are in the weekly CAB meeting. Three change requests are on the table for Saturday's maintenance window (10 PM to 2 AM). Review each one. Decide: approve, reject, or defer. Every decision needs a rationale."

#### The Three Change Requests (project on screen or print 6 copies)

```
----------------------------------------------------------------------
CHANGE REQUEST 1: DATABASE MIGRATION (HIGH RISK)

CHG-5102 | Requested by: Platform Engineering
Type: Normal Change | Priority: High

DESCRIPTION:
Migrate UPI transaction database from Oracle 19c to PostgreSQL 16.
- 4.2 billion transaction records
- Estimated migration time: 3.5 hours
- Requires 45-minute full UPI service downtime for cutover
- Dual-write has been running for 2 weeks (PostgreSQL shadow copy in sync)
- Performance testing shows 15% improvement in query latency on PostgreSQL

RISK ASSESSMENT (submitted by requester):
- Risk: HIGH
- Rollback plan: Switch DNS back to Oracle (estimated 10 min)
- Testing: 3 rounds of UAT completed. Load testing at 2x peak volume passed.
- Impact if deferred: Oracle license renewal due in 45 days (Rs 2.8 crore annual)
- Dependencies: All 280 member banks notified of maintenance window

CONCERNS:
- Last database migration (2024) caused 6-hour unplanned outage
- Festival season (Navratri) starts in 12 days -- transaction volumes 3x normal
- Rollback plan assumes Oracle stays warm during migration -- not tested under load
----------------------------------------------------------------------

----------------------------------------------------------------------
CHANGE REQUEST 2: MERCHANT ONBOARDING (STANDARD)

CHG-5103 | Requested by: Business Operations
Type: Standard Change (pre-approved template) | Priority: Medium

DESCRIPTION:
Onboard 340 new merchants (Swiggy Instamart stores) to UPI Collect.
- Standard API integration, same template used 14 times before
- No schema changes, no infrastructure changes
- Estimated time: 20 minutes (automated script)
- Merchant go-live: Monday 9 AM

RISK ASSESSMENT (submitted by requester):
- Risk: LOW
- Rollback plan: Disable merchant IDs via admin console (2 min)
- Testing: Sandbox testing completed by merchant integration team
- Impact if deferred: Contractual go-live penalty of Rs 15 lakh/week
----------------------------------------------------------------------

----------------------------------------------------------------------
CHANGE REQUEST 3: EMERGENCY SECURITY PATCH (URGENT)

CHG-5104 | Requested by: Information Security
Type: Emergency Change | Priority: Critical

DESCRIPTION:
Patch CVE-2026-31847 on UPI authentication gateway (Apache Tomcat RCE).
- Critical vulnerability (CVSS 9.8) disclosed 48 hours ago
- Exploit code is publicly available on GitHub
- NPCI authentication gateway runs affected Tomcat version
- RBI CISO advisory received: "Patch within 72 hours or submit exception report"
- Patch has been tested on staging environment -- no issues found
- Requires rolling restart of 12 auth gateway nodes (2 min downtime per node)

RISK ASSESSMENT (submitted by requester):
- Risk: MEDIUM (patch itself is low risk, but auth gateway is critical path)
- Rollback plan: Revert to previous Tomcat version via Ansible playbook (5 min)
- Testing: Staging environment tested. No regression in auth flows.
- Impact if deferred: RBI compliance violation. Active exploit in the wild.
- Window requested: TONIGHT (Tuesday) -- cannot wait until Saturday
----------------------------------------------------------------------
```

#### CAB Meeting Context Card (project on screen)

```
----------------------------------------------------------------------
CAB MEETING CONTEXT

Maintenance Window: Saturday 10:00 PM to 2:00 AM (4 hours)
Upcoming Events:
  - Navratri festival starts: Oct 7 (12 days away) -- 3x normal volume
  - RBI audit scheduled: Oct 15
  - Quarter-end reconciliation: Sep 30 (5 days away)

Change Freeze: Oct 5 to Oct 20 (festival season freeze)

Recent Incidents:
  - Last week's P1 (CHG-4892 caused UPI outage) -- config change related
  - 2024 database migration caused 6-hour outage
  - Zero security incidents in last 180 days

CAB Members Present: CAB Chair, Change Requester (presents all 3),
  Risk Assessor, Ops Lead, QA Lead

YOUR TASK (15 minutes):
For each change request, decide:
  APPROVE -- proceed as planned in the requested window
  APPROVE WITH CONDITIONS -- proceed with additional safeguards
  DEFER -- postpone to a later window (specify when)
  REJECT -- decline with rationale

Document your rationale for each decision.
----------------------------------------------------------------------
```

#### What YOU Do During Round 2

Walk between groups. **Listen for these specific things:**

| What to Watch | Good Sign | Red Flag |
|--------------|-----------|----------|
| CHG-5102 (DB migration) risk discussion | "Festival in 12 days, last migration failed, defer to post-freeze" | Approving without discussing festival season or past failure |
| CHG-5102 rollback scrutiny | "Rollback plan not tested under load -- that's a gap" | Accepting rollback plan at face value |
| CHG-5103 (merchant onboarding) standard change handling | "Standard template, done 14 times, low risk -- approve" | Over-analysing a standard change or rejecting it unnecessarily |
| CHG-5104 (security patch) urgency recognition | "RBI mandate, active exploit, cannot wait -- approve tonight" | Deferring to Saturday or rejecting |
| Calendar conflict awareness | "DB migration + merchant onboarding in same window -- sequence them" | Not checking for conflicts between changes |
| Change freeze consideration | "DB migration should be post-freeze, not pre-freeze" | Ignoring the upcoming change freeze |
| Lessons from last week | "Last week's P1 was change-related -- we need extra scrutiny" | No reference to recent incident history |
| QA Lead involvement | "Has regression testing been done? What's the test coverage?" | QA silent throughout the meeting |

**[15 min CAB activity]**

#### Round 2 Presentations (15-20 min) -- each group presents for 2-3 min:

Each group shares their three decisions with rationale:
1. CHG-5102 (DB migration): approve / approve with conditions / defer / reject -- and why
2. CHG-5103 (merchant onboarding): approve / approve with conditions / defer / reject -- and why
3. CHG-5104 (security patch): approve / approve with conditions / defer / reject -- and why

#### Round 2 Debrief (5 min) -- ask the whole class:

1. "How many groups approved the database migration for Saturday?" (Best practice: DEFER. Festival season in 12 days, last migration failed, change freeze starts Oct 5. Schedule for post-freeze window in late October.)
2. "Anyone who approved it -- what conditions did you add?" (Good conditions: extended rollback window, full team on standby, 2-hour canary period with dual-read)
3. "CHG-5103 is a standard change. How long did your group spend on it?" (Should be quick -- standard changes have pre-approved templates. Spending 5 min on a standard change is a process smell.)
4. "How many groups approved the security patch for tonight instead of Saturday?" (Should be all. CVSS 9.8, exploit public, RBI mandate. Emergency changes bypass normal CAB flow -- that's by design.)
5. "What is the difference between a Normal, Standard, and Emergency change?" (Normal: full CAB review. Standard: pre-approved, low risk. Emergency: expedited approval for critical/urgent fixes.)
6. "After last week's P1 caused by a config change, should CAB be more cautious or more efficient?" (Both -- more cautious on high-risk changes, more efficient on standard/emergency changes. The goal is risk-appropriate governance, not blanket slowness.)

---

### FINAL CONNECTION (say this) -- 16:25 to 16:30

> "Notice the thread between these two rounds. In Round 1, a change that was approved caused a major incident. In Round 2, you sat in the CAB that approves those changes. The quality of your CAB decisions directly determines how many P1 incidents you will face."

> "Three ITSM principles you practised today:"
> "1. Incident Management is about speed AND structure. A war room without an Incident Commander is just a group chat."
> "2. Change Management is about risk-appropriate governance. Not every change needs the same scrutiny. Standard changes are fast-tracked. Emergency changes bypass normal process. High-risk changes get extra scrutiny."
> "3. The feedback loop between Incident and Change Management is what makes ITSM work. Every P1 should feed back into how CAB reviews future changes."

> "In ServiceNow, every step you discussed today -- incident classification, war room notes, change requests, CAB approvals, risk assessments -- is a record. That traceability is what separates professional operations from ad-hoc firefighting."

---

## ROLE CARDS (Print & Cut -- 1 set per group)

### Round 1 Role Cards

---

**ROUND 1: INCIDENT COMMANDER**

You are the most senior technical leader in the war room. You OWN this incident.

Your responsibilities:
1. Classify the incident (P1/P2/P3) within the first 2 minutes
2. Assign tasks to war room members -- do NOT do everything yourself
3. Set a communication cadence: "Status updates every 10 minutes"
4. Make the rollback decision: the config change at 6:40 PM is the prime suspect
5. Ensure someone drafts bank communication AND public status page update
6. Track the 11 PM settlement deadline -- you have ~4 hours

Start the role play by calling the war room to order: "This is IC [your name]. I am declaring this a [P-level] incident. Here is how we will work."

---

**ROUND 1: NOC LEAD**

You are the first line of defence. Your monitoring dashboards are on fire.

You have the data:
- Success rate dropped from 99.2% to 40% at 6:47 PM
- CBS latency spiked from 12ms to 4,200ms at 6:45 PM
- A config change (CHG-4892) was deployed at 6:40 PM
- CBS cluster CPU at 94%, transaction queue depth at 2.4 million
- 5 of top 10 banks by volume are affected
- Intra-bank transactions (same bank) are working fine

Present this data clearly when the IC asks. Recommend rollback of CHG-4892 as the first action. Monitor dashboards and report changes in real-time.

---

**ROUND 1: PLATFORM ENGINEER**

You are the person who will execute the fix. You know the CBS routing layer.

Key facts you know:
- CHG-4892 updated routing weights for new bank onboarding
- The change passed pre-deployment validation (but validation only checks syntax, not load behaviour)
- Rollback is possible: you have the previous config backed up
- Rollback will take approximately 8 minutes (deploy + restart CBS nodes)
- BUT: rolling back will also undo the new bank onboarding that went live today
- Alternative: you could adjust the routing weights manually (15 min, riskier)

Present these options when asked. Recommend the safest path. You lean toward full rollback -- fix the outage first, re-onboard the bank tomorrow.

---

**ROUND 1: BANK LIAISON**

You are the interface between NPCI and 280+ member banks. Your phone is ringing non-stop.

You have received calls from:
- SBI Operations: "Our UPI payments are failing. What is happening?"
- HDFC Treasury: "We have settlement concerns. Will tonight's batch run?"
- ICICI Digital: "Our customers are complaining on social media. We need a statement."
- RBI (Payment Systems): "We are monitoring the situation. Please send a status report by 8 PM."

You need the IC to give you: (a) a 2-3 sentence bank communication, (b) an ETA for resolution, (c) confirmation on settlement batch status. Push for clear answers. Banks need facts, not hope.

---

**ROUND 1: SERVICE DESK LEAD**

You manage the frontline support team. Your ticket queue is exploding.

Your data:
- 847 tickets opened in the last 15 minutes
- Top complaint: "UPI payment failed, money debited but not credited"
- 23% of tickets involve stuck transactions (money left sender, not reached receiver)
- Your agents are using last month's outage FAQ, which is outdated
- You need an updated FAQ/script for agents within 10 minutes
- Merchant partners (PhonePe, Google Pay, Paytm) are escalating through their dedicated channels

Share this data in the war room. Ask for: (a) an agent FAQ/script, (b) guidance on stuck transactions (will they auto-reverse?), (c) a public status page update. Stuck transactions are a regulatory concern -- flag this clearly.

---

### Round 2 Role Cards

---

**ROUND 2: CAB CHAIR**

You chair the Change Advisory Board meeting. You control the agenda and the clock.

Your responsibilities:
1. Call the meeting to order. State the maintenance window (Saturday 10 PM - 2 AM)
2. Remind the board of context: Navratri in 12 days, change freeze Oct 5-20, quarter-end Sep 30, last week's P1 was change-related
3. For each change request, follow this flow:
   - Change Requester presents (2 min)
   - Risk Assessor reviews (2 min)
   - Ops Lead and QA Lead comment (2 min)
   - You call for a decision: Approve / Approve with Conditions / Defer / Reject
4. Ensure every decision has a documented rationale
5. CHG-5104 (security patch) requests TONIGHT, not Saturday -- handle this as an emergency change

Keep the meeting moving. You have 15 minutes for 3 change requests.

---

**ROUND 2: CHANGE REQUESTER**

You present ALL THREE change requests to the CAB. You are advocating for approval, but you must be honest about risks.

For CHG-5102 (DB migration): You believe in the technical readiness. Dual-write is working. UAT passed. But you know the last migration failed, and festival season is coming. Present honestly.

For CHG-5103 (merchant onboarding): This is straightforward. Same template used 14 times. Low risk. But there is a contractual penalty if deferred.

For CHG-5104 (security patch): This is urgent. CVSS 9.8. Exploit is public. RBI wants it patched within 72 hours. You want approval for TONIGHT.

Present each change clearly: what, why, risk, rollback plan, impact of deferral.

---

**ROUND 2: RISK ASSESSOR**

You are the sceptic. Your job is to find what can go wrong.

For CHG-5102 (DB migration):
- Last migration caused a 6-hour outage. What's different this time?
- Festival season starts in 12 days. If this fails, recovery could bleed into high-volume period.
- Rollback plan says "switch DNS back to Oracle in 10 min" -- has this been tested under production load?
- The change freeze starts Oct 5. If migration fails, there is no window to retry.
- 4.2 billion records. What if dual-write has silent data drift?

For CHG-5103 (merchant onboarding): Low risk. Confirm rollback exists. Approve.

For CHG-5104 (security patch): The patch itself is low risk, but the auth gateway is critical path. What if the rolling restart causes auth failures during the restart window? Is there a canary deployment plan?

---

**ROUND 2: OPS LEAD**

You own the production environment. You care about stability, capacity, and operational readiness.

Your concerns:
- Saturday's maintenance window is 4 hours. DB migration alone is estimated at 3.5 hours. That leaves 30 minutes of buffer. Not enough.
- Your on-call team is already stretched after last week's P1 incident
- If DB migration is approved, you need: full team on standby (not just on-call), pre-staged rollback, and a go/no-go checkpoint at the 2-hour mark
- For the security patch tonight: you can support a rolling restart. Minimal impact if done correctly. You have done this before.
- Quarter-end reconciliation is Sep 30. A failed migration could affect reconciliation data.

Speak up about operational feasibility. You are the voice of "can we actually do this safely?"

---

**ROUND 2: QA LEAD**

You own testing and validation. Your job is to ensure every change has been adequately tested before production.

Your questions for each change:
- CHG-5102: "UAT passed, but was rollback tested under production load? Was a chaos test done (kill a node mid-migration)? What is the data validation plan post-migration -- how do we know 4.2 billion records migrated correctly?"
- CHG-5103: "Standard template, 14 prior executions. Test report looks clean. No concerns."
- CHG-5104: "Staging test passed. But staging has 2 nodes, production has 12. Was the rolling restart sequence tested at scale? What is the automated regression suite coverage on auth flows?"

Push for evidence, not assurances. "We tested it" is not the same as "here is the test report."

---

## SCORING RUBRIC

### Individual Score Card (per participant, per round)

| # | Parameter | Max | How to Score |
|---|-----------|-----|-------------|
| 1 | Effective Demonstration | 15 | 15=exceptional role play, 12=solid, 9=adequate, 6=weak |
| 2 | Enthusiasm for the Position | 15 | Engagement, energy, ownership of the role |
| 3 | Knowledge on the Position | 10 | Understanding of ITSM concepts and role responsibilities |
| 4 | Communication Skills | 15 | Clarity, conciseness, data-driven arguments |
| 5 | Teambuilding / Interpersonal Skills | 10 | Listening, building on others, collaboration |
| 6 | Initiative | 10 | Proactive contributions, didn't wait to be asked |
| 7 | Time Management | 15 | Stayed within time, moved discussion forward |
| 8 | Customer Service Skills | 10 | Empathy, stakeholder-first thinking (banks, merchants, public) |
| | **Total** | **100** | |

> Same rubric as Behavioural role play for consistency across all role plays.

### Grading Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 85-100 | A | Excellent -- ready for ITSM operations |
| 70-84 | B | Good -- understands intent, needs practice |
| 55-69 | C | Developing -- grasps basics, needs coaching |
| < 55 | D | Needs significant improvement |

---

## PRINTABLE SCORING SHEET

Use one sheet per group. Score each participant across both rounds (average the two rounds for final score).

```
GROUP: ___  |  Date: Sep 25, 2026

                              ROUND 1 (War Room)                    ROUND 2 (CAB)
Participant Name          | R1 Role         | P1 P2 P3 P4 P5 P6 P7 P8 | R1 Total | R2 Role          | P1 P2 P3 P4 P5 P6 P7 P8 | R2 Total | AVG
--------------------------|-----------------|--------------------------|----------|------------------|--------------------------|----------|----
_________________________ | _______________ | __ __ __ __ __ __ __ __ | ___/100  | ________________ | __ __ __ __ __ __ __ __ | ___/100  | ___
_________________________ | _______________ | __ __ __ __ __ __ __ __ | ___/100  | ________________ | __ __ __ __ __ __ __ __ | ___/100  | ___
_________________________ | _______________ | __ __ __ __ __ __ __ __ | ___/100  | ________________ | __ __ __ __ __ __ __ __ | ___/100  | ___
_________________________ | _______________ | __ __ __ __ __ __ __ __ | ___/100  | ________________ | __ __ __ __ __ __ __ __ | ___/100  | ___
_________________________ | _______________ | __ __ __ __ __ __ __ __ | ___/100  | ________________ | __ __ __ __ __ __ __ __ | ___/100  | ___

P1=Effective Demo  P2=Enthusiasm  P3=Knowledge  P4=Communication
P5=Teambuilding    P6=Initiative  P7=Time Mgmt  P8=Customer Service

Group Observations:
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
```

---

## MATERIALS CHECKLIST (Prepare Before Session)

| Item | Copies | Status |
|------|--------|--------|
| Round 1 Scenario Card (UPI outage) | Project on screen or 6 copies | [ ] |
| Round 1 Role Cards (IC, NOC Lead, Platform Eng, Bank Liaison, Service Desk Lead) | 6 sets (print & cut) | [ ] |
| Round 2 Change Requests (3 CHGs) | Project on screen or 6 copies | [ ] |
| Round 2 CAB Context Card | Project on screen or 6 copies | [ ] |
| Round 2 Role Cards (CAB Chair, Change Requester, Risk Assessor, Ops Lead, QA Lead) | 6 sets (print & cut) | [ ] |
| Scoring Sheets (blank, from above) | 6 copies | [ ] |
| Timer (phone/watch) | 1 | [ ] |
| Whiteboard markers | For debrief notes | [ ] |

---

## IF THINGS GO WRONG

| Problem | What To Do |
|---------|-----------|
| Group classifies the UPI outage as P2 | Pause. Ask: "12 lakh transactions failing per hour, Rs 180 crore/hr impact, RBI is calling. What is your P1 threshold if not this?" |
| Group wants to investigate before rolling back | Let it play for 2 min, then ask the Bank Liaison: "SBI is on the phone. HDFC is on the phone. RBI wants a status report by 8 PM. How long will investigation take?" |
| Group forgets settlement batch deadline | Ask at the 10-min mark: "What time is the settlement batch? What happens if UPI is still down at 10:30 PM?" |
| CAB approves DB migration without discussing festival season | Ask the Risk Assessor: "Navratri starts in 12 days. What happens if this migration fails and you need a recovery window?" |
| CAB defers the security patch to Saturday | Ask: "The exploit code is public on GitHub. Your auth gateway is vulnerable for 4 more days. What is the risk of waiting?" |
| Group spends too long on CHG-5103 (standard change) | Pause. Say: "This is a Standard Change. It has been done 14 times with the same template. How long should a CAB spend on a Standard Change?" |
| 4-person group struggles with combined Bank Liaison / Service Desk role | Tell them: "In a real war room, one person often covers both. Focus on data: ticket volume and bank calls. You are the voice of external stakeholders." |
| A group finishes early | Curveball for Round 1: "CERT-In just called. They are seeing a DDoS signature on the CBS traffic. Is this an attack or an outage?" Curveball for Round 2: "A fourth CHG just arrived -- hot-fix for the stuck transactions from last week's P1. It changes the settlement reconciliation logic. Approve tonight?" |

---

## TIMELINE SUMMARY

| Time | Activity | Duration |
|------|----------|----------|
| 15:00 | Setup, seating, distribute materials | 5 min |
| 15:05 | Round 1: Major Incident War Room (15 min activity + 20 min presentations/debrief) | 35-40 min |
| 15:45 | Round 2: CAB Meeting (15 min activity + 20 min presentations/debrief) | 35-40 min |
| 16:25 | Final connection + ITSM tie-in | 5 min |
| 16:30 | Score tabulation + individual feedback | 10 min |
| 16:40 | Submit scores | 5 min |
| **Total** | | **~100 min** |

> Note: If running tight on time, reduce presentation time to 2 min per group (12 min total per round instead of 15-20 min). This brings total to ~85 min.

---

## EMAIL TEMPLATE (Send to all participants before the session)

**Subject:** ITSM Role Play -- Major Incident War Room + CAB Meeting | Fri Sep 25, 3:00 PM

Hi team,

We have our **ITSM Role Play** scheduled for **Friday Sep 25, 3:00 - 4:45 PM**.

**What:** Two rounds simulating real ITSM processes at NPCI (UPI):
- Round 1: UPI transaction success rate crashes to 40% during peak hours. You are in the War Room. Classify, escalate, communicate, restore.
- Round 2: Three change requests on the CAB table. One risky, one standard, one emergency. Approve, defer, or reject -- with rationale.

**Preparation:** No preparation needed. Role cards will be distributed at the start. Everything you need is in the scenario handout.

**Groups:** You will be in new groups (reshuffled from previous role plays). Group assignments will be shared at the start.

**What is being evaluated:** Incident classification and escalation, structured war room communication, risk-based change decisions, ITIL process awareness, stakeholder management.

See you there.

Best,
Nagabhushanam
