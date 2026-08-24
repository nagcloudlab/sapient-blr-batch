# ITSM Role Play -- P1 Incident Management

**Module:** 36 -- ServiceNow & ITSM
**Context:** FoodExpress Food Delivery Application
**Total Time:** 75 minutes (two rounds + debrief)
**Group Size:** 5 participants per group

---

## Overview

These scenarios apply the ITIL incident management and problem management processes to a realistic, high-pressure situation. Participants experience the full lifecycle: detection, classification, investigation, resolution, and then the deeper problem management process that prevents recurrence. The ServiceNow tooling is the backbone of these processes -- participants should reference ServiceNow at each handoff point.

---

## Scenario Card (distribute before both rounds)

> FoodExpress processes approximately 3,200 orders during the lunch peak (12:00 PM -- 2:00 PM). The payment gateway is provided by a third party (Razorpay). FoodExpress has an SLA with restaurant partners guaranteeing 99.5% payment processing uptime during peak hours. The current ITSM tooling is ServiceNow. All incidents, changes, and problems are tracked in ServiceNow. The P1 response SLA is: acknowledge within 5 minutes, first update within 15 minutes, resolution target 60 minutes.

---

## Round 1: P1 Incident Response

**Duration:** 30 minutes
(22 min role play + 8 min debrief)

### Situation

It is 12:32 PM on a Wednesday. Peak lunch hour. The FoodExpress payment gateway has stopped processing payments. No orders can be completed. Users who attempt to pay see the error: "Payment could not be processed. Please try again." Orders are queuing and failing. The monitoring system has fired a critical alert.

Every minute of downtime is costing the business approximately Rs 85,000 in failed transactions (based on average order value Rs 340 and peak order rate of 250 orders per minute).

### Incident Timeline (read aloud to set the scene before starting)

- 12:29 PM -- Razorpay payment API begins returning HTTP 503 errors.
- 12:31 PM -- FoodExpress payment service error rate reaches 100%. All payment attempts fail.
- 12:32 PM -- Monitoring alert fires. ServiceNow automatically creates incident INC0023847.
- 12:33 PM -- Current time. The role play begins here.

### Roles

**Incident Manager (coordinates the entire response)**
You are the Incident Commander for this P1. Your job is not to fix the technical problem -- it is to coordinate the people who will. You own the ServiceNow incident record. You must:
- Keep a running log of all updates in INC0023847 in ServiceNow (simulate this by keeping notes on paper)
- Ensure the P1 SLA is being met (first update within 15 minutes of detection = by 12:44 PM)
- Drive to resolution within 60 minutes (target: 1:29 PM)
- Decide when to post status page updates
- Chair the war room call

Open the war room immediately. Your first action: assign the incident to L2 Engineering and page L1 Support.

**L1 Support (first response, customer-facing)**
You are monitoring the support queue. At 12:33 PM, you have 23 open support tickets all reporting the same symptom: payment not going through. By 12:38 PM, that number will be 91.

Your job in the role play:
- Confirm the incident is real (not isolated reports) and report this to the Incident Manager.
- Update INC0023847 in ServiceNow with the customer impact data.
- Draft the first customer-facing status page message (you will propose this to the Communications Lead for approval).
- Answer incoming customer contacts with a holding message: "We are aware of a payment processing issue and are working to resolve it. Orders placed in the last 10 minutes have not been charged."

**L2 Engineer (technical investigation)**
You join the war room at 12:34 PM. Your job is to diagnose and fix the problem.

Diagnostic steps to roleplay (do these in sequence, announcing each one to the war room):
1. (12:34 PM) Check FoodExpress payment service logs. Find: Razorpay API returning 503, no connection errors from FoodExpress side.
2. (12:37 PM) Check Razorpay status page (simulate: it shows "Investigating - Payment API degradation" posted at 12:30 PM).
3. (12:39 PM) Call Razorpay technical support. (Trainer plays Razorpay support: "We are aware of the issue. Our payment API is experiencing degraded performance due to a network routing issue. ETA for resolution: 30-45 minutes.")
4. (12:42 PM) Propose workaround: switch to the backup payment gateway (PayU). FoodExpress has a configured but inactive PayU integration. Activating it requires a configuration change and a deploy.
5. Raise the workaround to the Incident Manager. A configuration change = an emergency change. This needs the Change Manager's approval.

**Change Manager (approves the emergency change)**
You receive a request for an Emergency Change (CHNG0008341) at approximately 12:43 PM to activate the PayU payment gateway as a fallback.

Evaluate the change:
- Risk: switching payment gateways during peak hour could cause order duplication if a request is in-flight during the switch.
- Mitigation proposed by L2: deploy the change to 10% of traffic first, verify, then roll out fully.
- The change will take approximately 8 minutes to deploy (2 minutes for config, 6 minutes for deploy pipeline).

Approve the change with conditions: phased rollout (10% first), L2 must confirm clean traffic before full rollout. Update CHNG0008341 in ServiceNow with the approval and conditions. (Simulate on paper.)

**Communications Lead (stakeholder updates)**
You own external and internal communications during the incident. You are not technical -- your job is to translate technical status into clear, honest communication.

Your tasks:
- At 12:38 PM: draft the first public status page update. (Propose to Incident Manager for approval before posting.)
- At 12:50 PM: draft an internal update to the FoodExpress CEO and Head of Operations.
- At 1:05 PM (after PayU goes live and payments resume): draft the resolution notice.
- At 12:45 PM: the CEO sends a Slack message asking "what is happening." Route this to the Incident Manager. Do not answer directly. Propose a format for regular updates to the CEO (every 10 minutes during a P1).

### Draft Communications (Communications Lead uses these as templates)

**First status page update (12:38 PM)**
> We are currently experiencing an issue with payment processing on the FoodExpress platform. Users may be unable to complete orders. Our team is actively investigating. We will provide an update within 15 minutes. Orders placed before 12:29 PM have been successfully processed.

**Internal update to CEO (12:50 PM)**
> As of 12:50 PM, the FoodExpress payment gateway has been down for 21 minutes. Root cause: Razorpay payment API is experiencing a network routing issue on their infrastructure. We have raised a P1 with Razorpay (ticket: RZP-98331). Our engineering team is deploying a workaround to switch to our backup payment gateway (PayU). Estimated restoration of service: 1:05 PM. Current estimated revenue impact: Rs 17.85 lakhs. Customer communication has been posted on status page. We will update again at 1:00 PM.

**Resolution notice (after PayU goes live)**
> Payment processing has been restored on FoodExpress as of [time]. We have switched to our backup payment provider while our primary provider resolves their infrastructure issue. All orders placed after [time] are processing normally. If you experienced a failed payment, please retry your order -- you were not charged for failed transactions. We apologise for the disruption during lunch hour.

### Incident Resolution Sequence (to complete the role play)

- 12:43 PM -- L2 proposes PayU emergency change.
- 12:45 PM -- Change Manager approves with phased rollout condition.
- 12:47 PM -- L2 begins deploy. 10% traffic routed to PayU.
- 12:52 PM -- L2 confirms 10% traffic clean (zero errors on PayU).
- 12:54 PM -- Full traffic switched to PayU.
- 12:57 PM -- Payment error rate drops to 0%. Incident resolved.
- Total downtime: 28 minutes. Failed transactions: approximately 7,000.

### Objectives

By the end of Round 1, the group should have:
- Followed the ITIL incident management phases: Detection, Classification, Investigation, Resolution, Communication
- Updated INC0023847 with a complete audit trail (simulated on paper)
- Approved and executed an emergency change
- Posted at least 2 external communications
- Closed the incident in ServiceNow with a resolution note

---

### Round 1 Debrief Questions (8 minutes)

1. Was the ITIL incident process followed in sequence? Were any phases skipped or out of order?
2. The P1 SLA requires a first update within 15 minutes of detection (by 12:44 PM). Did the group meet this? If not, what delayed it?
3. The Change Manager added conditions to the emergency change approval (phased rollout). Was this appropriate given the urgency? What is the risk of adding conditions to an emergency change under time pressure?
4. The Communications Lead was communicating to three different audiences: customers, the CEO, and the engineering war room. Were the messages appropriately tailored to each audience?
5. The incident was caused by a third-party (Razorpay) failure, not a FoodExpress engineering failure. How does this change the incident process? Does the RCA responsibility change?
6. ServiceNow was referenced throughout. List three specific points in this incident where an action should have generated a ServiceNow record update.

---

## Round 2: Problem Management

**Duration:** 25 minutes
(18 min role play + 7 min debrief)

### Situation

It is the following Monday, 10:00 AM. This was the third payment gateway outage in two months:
- Outage 1 (5 weeks ago): 19 minutes, Razorpay API timeout during a deployment on their end.
- Outage 2 (3 weeks ago): 12 minutes, Razorpay certificate renewal caused a brief authentication failure.
- Outage 3 (this week, Round 1): 28 minutes, Razorpay network routing issue.

Each incident was treated as isolated. Each was resolved with a workaround. No Problem Record was created after the first two.

Management has escalated. The Head of Technology has asked the Problem Management team to conduct a formal Problem Management review. A Problem Record has been created in ServiceNow: PRB0001293.

The team must use the 5-Why technique to find the true root cause and propose a permanent fix.

### Roles

**Problem Manager (facilitates the review)**
You own PRB0001293. Your job is to guide the group through the 5-Why analysis and ensure the output is a Problem Record with a documented root cause, a Known Error (if applicable), and a permanent fix plan with owners and dates.

Keep the group honest: push back on answers to "Why?" that are too shallow. If someone says "because Razorpay had a failure," ask "why were we impacted by Razorpay's failure?" That is the next Why.

**Engineer 1 (presents technical analysis)**
You have analysed all three outages. The common thread: FoodExpress has no automatic failover from Razorpay to PayU. Each time Razorpay fails, manual intervention is required. In the first two outages, the manual failover was not even attempted because the incidents resolved before a decision was made. This time it took 14 minutes from detection to emergency change approval.

You believe the permanent fix is: implement automatic failover. When Razorpay error rate exceeds 20% for more than 2 minutes, automatically route to PayU without human intervention. This is a backend engineering task estimated at 15 story points.

**Engineer 2 / Change Manager (evaluates the permanent fix)**
You review proposed changes for risk and feasibility. The automatic failover proposal (Engineer 1) is technically sound but has risks:
- If the failover triggers incorrectly (a false positive), PayU may not be able to handle full FoodExpress load without prior warm-up.
- PayU charges a higher transaction fee (0.8% vs Razorpay 0.5%). Automatic failover without approval means the business is making a cost decision automatically.
- Propose a modification: the automatic failover should alert the on-call engineer and provide a 60-second window to cancel before triggering. This preserves human oversight while reducing MTTR.

**Service Owner (approves the permanent fix plan)**
You are accountable for the payment service. You have two concerns:
1. Business concern: three outages in two months is not acceptable for a payment service. The SLA with restaurant partners is at risk. You need a fix that is permanent, not another workaround.
2. Commercial concern: Razorpay provides better pricing. If FoodExpress runs on PayU for extended periods, the cost difference is significant. You want the automatic failover to also include an automatic failback to Razorpay once Razorpay returns to healthy state.

You will approve the permanent fix plan if it includes: automatic failover, human notification with cancel window, and automatic failback.

### The 5-Why Analysis (Problem Manager leads this)

The facilitator should guide the group through these questions. Each answer leads to the next Why:

**Problem Statement:** FoodExpress payment gateway is unavailable for 28 minutes, causing 7,000 failed orders.

**Why 1:** Why was the payment gateway unavailable?
Answer: Razorpay, our primary payment provider, experienced a network routing failure.

**Why 2:** Why did Razorpay's failure cause FoodExpress to have zero payment capability?
Answer: FoodExpress has no automatic failover to the backup payment gateway (PayU).

**Why 3:** Why is there no automatic failover?
Answer: The PayU integration was built as a manual backup. Automatic failover was not prioritised during the original build.

**Why 4:** Why was automatic failover not prioritised?
Answer: The original architecture assumed a single payment gateway. Resilience requirements were not defined in the initial technical specification.

**Why 5:** Why were resilience requirements not defined?
Answer: The team did not have a formal process for defining availability and resilience requirements for critical third-party integrations. (This is the systemic root cause.)

**Root Cause Statement (the Problem Manager should help the group construct this):**
FoodExpress lacks a formal process for assessing and designing resilience requirements for critical third-party service integrations. As a result, the payment service was built with a single point of failure and no automatic recovery capability, making every Razorpay outage a full payment service outage.

### Known Error and Workaround

The Problem Manager should document in PRB0001293:
- **Known Error:** FoodExpress payment service has no automatic failover from Razorpay to PayU.
- **Workaround:** Manual emergency change to activate PayU integration (requires Change Manager approval, takes approximately 14 minutes from incident detection to service restoration).
- **Permanent Fix:** Implement automatic failover with human notification window and automatic failback (see action items).

### Action Items from the Problem Review

Each item needs: what, who owns it, by when.

The group should produce these (or equivalents):

1. Implement automatic payment gateway failover (Razorpay to PayU) with 60-second human cancel window. Owner: Backend Engineering Lead. Target: Sprint 23 (3 weeks).
2. Implement automatic failback from PayU to Razorpay when Razorpay returns to healthy state. Owner: Backend Engineering Lead. Target: Sprint 23.
3. Define and document resilience requirements for all critical third-party integrations (payment, SMS, maps, push notifications). Owner: Service Owner + Architecture Team. Target: 6 weeks.
4. Add payment gateway availability to the monitoring dashboard with a dedicated alert (separate from the general error rate alert). Owner: DevOps. Target: 1 week.
5. Add PRB0001293 Known Error and workaround to the on-call runbook so future engineers can activate the PayU failover in under 5 minutes without needing a Change Manager approval for an already-approved Known Error workaround. Owner: L2 Engineer. Target: this week.

### Objectives

By the end of Round 2, the group should have:
- Completed the 5-Why analysis and identified the systemic root cause
- Distinguished between the root cause (no resilience requirements process) and the immediate cause (no automatic failover)
- Documented a Known Error with a workaround in PRB0001293
- Agreed on a permanent fix plan with at least 4 concrete action items
- Connected the Problem Record to the three Incident Records in ServiceNow (simulate by noting INC numbers in PRB record)

---

### Round 2 Debrief Questions (7 minutes)

1. The 5-Why analysis revealed that the root cause is not "Razorpay had a failure" but "we have no resilience requirements process." Is this distinction meaningful? How does it change the action items?
2. Did the group go deep enough on the Whys? Was there a temptation to stop at Why 2 ("no automatic failover") and call that the root cause? Why is Why 2 not sufficient?
3. The Change Manager proposed a modification to the automatic failover (60-second cancel window). Was this a useful risk mitigation or an unnecessary complication? How did the group decide?
4. The Known Error entry means: next time this happens, the on-call engineer does not need emergency change approval for the PayU failover. Why does this matter for MTTR in future incidents?
5. Three incidents occurred before a Problem Record was created. ITIL guidance says a Problem Record should be created after a major incident or after a pattern of related incidents. Was waiting until the third incident acceptable? What is the cost of that delay?
6. Review the action items. Which one addresses the root cause? Which ones address contributing factors? Is there an action item that treats only the symptom? Should it stay in the list?

---

## Facilitator Notes

- Round 1 is the most complex scenario in this collection. With 5 roles running simultaneously, the Incident Manager role is critical -- if that participant is weak, the session loses structure. Consider briefing that participant in advance or taking that role yourself for the first run.
- The timeline in Round 1 is designed to move quickly. Print it and give each participant a copy so they know what is coming next. The L2 Engineer especially needs the diagnostic sequence in hand.
- For the ServiceNow simulation: participants do not need access to actual ServiceNow. Have them maintain a paper log with these fields: Incident Number, State, Priority, Assigned To, Last Update, Resolution Notes. This mirrors ServiceNow's incident record structure.
- For Round 2, the 5-Why is the core technique. If the group tries to jump to solutions before completing the analysis, redirect them. The value of 5-Why is in the discipline of asking the next question, not in reaching the answer quickly.
- After Round 2, point out explicitly: if a Problem Record had been created after Outage 1, the Known Error workaround would have been documented, and Outages 2 and 3 would have been resolved in under 5 minutes instead of 12-28 minutes. This is the business case for Problem Management, stated in plain terms the trainees will remember.
- These two rounds together span the entire ITIL lifecycle for a single problem. That end-to-end view -- from a P1 incident to the problem management review that prevents the next one -- is the key learning for this module.
