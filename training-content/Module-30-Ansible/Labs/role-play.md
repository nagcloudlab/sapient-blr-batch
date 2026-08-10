# Behavioral Role Play -- Incident Escalation

**Module:** 30 -- Ansible & Configuration Management
**Context:** FoodExpress Food Delivery Application
**Total Time:** 70 minutes (two rounds + debrief)
**Group Size:** 4 participants per group

---

## Overview

These scenarios practise the human side of incident management: the escalation decision, the war room dynamic, and the post-incident review. Technical skills alone do not resolve incidents -- communication, judgement under pressure, and structured retrospection do. These are skills sustain engineers use constantly.

---

## Scenario Card (distribute before Round 1)

> FoodExpress runs on AWS across three regions. The Order Service handles approximately 800 orders per hour during peak (6-9 PM). The team uses PagerDuty for on-call alerting, Slack for incident channels, and Confluence for runbooks. The on-call rotation covers the team of 6 engineers. Average MTTR for past incidents is 45 minutes.

---

## Round 1: Escalation Decision

**Duration:** 25 minutes
(18 min role play + 7 min debrief)

### Situation

It is Tuesday, 8:02 PM. Peak dinner hour. The Order Service has been intermittently returning HTTP 500 errors for the past 32 minutes. Monitoring shows that approximately 15% of order creation requests are failing. The on-call engineer received a PagerDuty alert at 7:31 PM and has been investigating alone since then. The error rate has not improved.

The on-call engineer must now decide: escalate, and if so to whom, and what to communicate externally.

### Timeline of Events (read this aloud to the group before starting)

- 7:28 PM -- Monitoring alert fires: Order Service error rate above 5% threshold.
- 7:31 PM -- PagerDuty pages on-call engineer.
- 7:33 PM -- On-call engineer acknowledges alert. Opens incident Slack channel. Begins investigation.
- 7:45 PM -- Error rate now at 15%. On-call engineer checks application logs. Sees "connection pool exhausted" errors in Order Service logs.
- 7:52 PM -- On-call engineer attempts to restart the Order Service pods. Error rate drops to 8% for 3 minutes then climbs back to 15%.
- 8:02 PM -- Current time. 32 minutes since alert. Error rate stable at 15%. Root cause not yet identified.

### Roles

**On-call Engineer**
You have been investigating for 32 minutes. You have found "connection pool exhausted" in the logs but do not yet know why the pool is exhausting -- it could be a leak, a traffic spike, a slow query holding connections, or a database issue upstream. You restarted the pods but the error returned.

You must decide: do you escalate now? You are hesitant because you feel like you are "almost there" and do not want to wake someone up if you can fix it in the next 10 minutes. But the error rate has not improved.

Your escalation options:
- Page the Team Lead (who is senior and can help diagnose)
- Page the Database team (if you believe this is a database issue)
- Open a Major Incident (which triggers manager notification and customer communication)

Trigger the role play by describing your current situation to the group. Let the discussion develop.

**Team Lead**
You are the on-call engineer's escalation point. You are at home. When the on-call engineer calls or messages you, ask three questions before deciding to join:
1. How long has this been going on?
2. What have you tried so far?
3. Is the error rate getting better, worse, or stable?

Based on the answers (32 minutes, pod restart, stable at 15%), decide to escalate to a Major Incident. Guide the on-call engineer through the steps: declare the incident in PagerDuty, open the war room channel, notify the Manager.

**Manager**
You receive a notification that a Major Incident has been declared. Join the war room. Ask for a status summary in 2 minutes. You need to decide: do you send a customer communication? At what point does 15% order failure rate for 30+ minutes require an external status page update? You lean toward communicating early -- the cost of silence is higher than the cost of transparency. Ask the team to draft a status update within 5 minutes.

**Customer Support Lead**
You have been receiving escalating support tickets and calls since 7:45 PM. At 8:02 PM, you have 47 open tickets related to order failures. You join the war room and provide this data. You need to know: when can you tell customers something? What is the message? Can affected customers be given a refund or voucher? Push the manager for a decision on customer communication and compensation.

### Decision Points (the group must reach a conclusion on each)

1. When should the on-call engineer have escalated? (At what point -- time elapsed, error rate, failed remediation attempts -- does escalation become mandatory?)
2. Who declares the Major Incident and what does that trigger?
3. What is the customer communication message? (Draft a 2-sentence external status update for the group to agree on.)
4. Is the Customer Support Lead authorised to offer vouchers to affected customers now, or must that wait for resolution?

### Objectives

By the end of Round 1, the group should have:
- Declared the incident and identified the incident commander
- Agreed on the escalation trigger criteria
- Drafted a customer communication message
- Made a decision on customer compensation approach

---

### Round 1 Debrief Questions (7 minutes)

1. The on-call engineer waited 32 minutes before escalating. Was that too long? What is the cost of escalating too early versus too late?
2. The team lead asked three diagnostic questions before deciding to escalate further. Why does this matter? What happens if a manager joins a war room without this context?
3. What is the difference between declaring a Major Incident and simply investigating an incident? What does the declaration trigger?
4. Did the group agree on a customer communication? Read it aloud. Is it honest? Is it specific enough? Does it over-promise a resolution time?
5. Was the Customer Support Lead included in the war room at the right time, or too late? What information did they bring that changed the picture?
6. If you had a runbook for this exact scenario (connection pool exhaustion), what three steps would be in it?

---

## Round 2: Post-Incident Review

**Duration:** 25 minutes
(18 min role play + 7 min debrief)

### Situation

It is Thursday, 10:00 AM. The incident from Round 1 has been resolved. Root cause was confirmed: a database connection pool was configured with a maximum of 20 connections. During peak hours, a new feature (restaurant analytics) was running expensive queries that held connections open for 4-6 seconds each. Under load, the pool exhausted within minutes of peak hour starting.

The fix applied was: increase the connection pool size from 20 to 100 (emergency change). The permanent fix (query optimisation for the analytics feature) is scheduled for Sprint 22.

The team is now running a Post-Incident Review (PIR). The format is: Timeline, Root Cause, Contributing Factors, Action Items. The goal is to be blameless.

### Roles

**Incident Commander (facilitates the PIR)**
You facilitated the war room during the incident. Now you facilitate the PIR. Your job: guide the group through the four sections in 18 minutes. Keep the tone blameless. If anyone uses language that assigns blame to an individual, redirect to the system. ("The process did not catch this" rather than "you should have caught this.") Ensure action items are concrete and owned.

**Engineer (presents timeline and technical analysis)**
You investigated the incident. You have the timeline from the runbook you wrote after the incident. Walk the group through what happened technically. Be precise about the connection pool configuration. Explain why the restaurant analytics feature caused this -- it was added in Sprint 19 without a load test. Own that gap without self-flagellating.

**QE (identifies the testing gap)**
The restaurant analytics feature went to production without a performance test. Your team's test plan for Sprint 19 did not include a load test because the feature was considered "low risk" (read-only queries). Raise this as a process gap. Propose a change to the definition of done: all features that touch shared database connections must include a connection pool stress test. Make this a concrete action item.

**Manager (discusses prevention and cost)**
You have data: the incident lasted 54 minutes. Based on Order Service metrics, approximately 720 failed orders. Average order value Rs 340. Estimated revenue impact: Rs 245,000. Reputational cost is harder to quantify. You want action items that prevent recurrence -- specifically, you want to know why monitoring did not alert on connection pool exhaustion (only the downstream effect, the 500 errors, was alerted). Propose adding a connection pool utilisation alert at 70% as an action item.

### PIR Structure (Incident Commander should follow this)

**Section 1 -- Timeline (4 minutes)**
The Engineer walks through the timeline from Round 1 plus:
- 8:15 PM -- Database team joins war room. Confirms connection pool exhaustion.
- 8:19 PM -- Emergency change submitted: increase pool size from 20 to 100.
- 8:22 PM -- Emergency change approved (Change Manager).
- 8:25 PM -- Pool size updated via Ansible playbook. Pods restarted.
- 8:27 PM -- Error rate drops to 0%. Incident resolved.
- Total duration: 59 minutes (7:28 PM alert to 8:27 PM resolution).

**Section 2 -- Root Cause (4 minutes)**
Root cause: database connection pool configured at 20 connections (default, never reviewed). Restaurant analytics feature introduced in Sprint 19 holds connections for 4-6 seconds per query. Under peak load (800 orders/hour), connections exhaust within minutes.

**Section 3 -- Contributing Factors (5 minutes)**
The group must identify at least 3 contributing factors (not the root cause itself, but conditions that allowed it to happen):
- Suggested: connection pool size was never reviewed post-initial deployment
- Suggested: restaurant analytics feature had no performance test before go-live
- Suggested: monitoring alerted on the effect (500 errors) not the cause (pool exhaustion)
- Suggested: no documented runbook for connection pool exhaustion prior to this incident

**Section 4 -- Action Items (5 minutes)**
Each action item needs: what, who owns it, by when.
The group should produce at least 4 action items. Examples:
- Add connection pool utilisation monitoring alert at 70%. Owner: DevOps. By: end of Sprint 22.
- Add connection pool stress test to definition of done for any database-touching feature. Owner: QE Lead. By: Sprint 22 planning.
- Optimise restaurant analytics queries (target: under 500ms, no held connections). Owner: Backend Engineer. By: Sprint 22 completion.
- Document runbook for connection pool exhaustion in Confluence. Owner: Engineer. By: end of this week.

### Objectives

By the end of Round 2, the group should have:
- Completed all four PIR sections
- Produced a blameless analysis with at least 3 contributing factors
- Agreed on at least 4 concrete action items with owners and dates
- Identified the monitoring gap as a separate action item

---

### Round 2 Debrief Questions (7 minutes)

1. Was the review blameless? Were there moments where the language shifted toward individual blame? How did the facilitator handle it?
2. The root cause was a misconfigured connection pool that had been in production since launch. No one was "at fault" in the incident -- but the contributing factors reveal process gaps. What process change would have caught this before the incident?
3. The emergency fix (increase pool size to 100) solved the symptom. Is it a good permanent fix? What are the risks of leaving the pool at 100 without also fixing the slow queries?
4. Review the action items the group produced. Are they specific? Are they owned? What is the likelihood each one will actually be completed? What follow-up mechanism ensures they are?
5. The monitoring only alerted on the downstream effect (500 errors), not the upstream cause (connection pool exhaustion). Why does this matter for MTTR? How much time was lost because the alert was indirect?
6. The PIR took 18 minutes in the simulation. In real life, PIRs for a 1-hour P1 incident might take 60-90 minutes. What makes them take longer, and is that time well spent?

---

## Facilitator Notes

- Round 1 is deliberately tense. The on-call engineer role is designed with hesitation built in ("I feel like I am almost there"). Let the hesitation play out for 2-3 minutes before the Team Lead asks the three questions. The tension is the learning.
- Round 2 should feel calmer and more structured than Round 1. The contrast is intentional.
- If a participant in Round 2 says something like "the engineer should have noticed this when they added the feature," pause the role play and point out: this is a blame statement. Ask the group to reframe it as a system statement.
- The timeline in Round 2 can be projected or written on a whiteboard. Participants find it easier to discuss a written timeline than a verbal one.
- Connect these two rounds to the Ansible module content: the fix applied (increasing the pool size) was deployed via an Ansible playbook. The fact that it could be applied in under 3 minutes (8:22 PM approval to 8:25 PM applied) is a direct benefit of infrastructure-as-code. The facilitator should call this out explicitly in the final debrief.
