# Lab 06: Blameless Post-Mortems

## Objective

Write a blameless post-mortem for a real incident, learn to distinguish
blame-focused vs system-focused language, and create actionable follow-ups.

---

## Concepts

### Blameless Culture

```
BLAME CULTURE                       BLAMELESS CULTURE
──────────────                      ─────────────────
"Ravi forgot to renew the cert"     "The system lacked automated cert renewal"
"QA missed this bug"                "Our test suite didn't cover this path"
"DevOps should have caught this"    "Monitoring didn't alert on this condition"

Result: People hide mistakes        Result: People share learnings
        Fear of punishment                  Continuous improvement
        Same incidents repeat               Root causes get fixed
```

### The 5 Whys

```
Problem: Delivery tracking went down for 37 minutes

Why 1: Why did it go down?
  -> TLS certificate expired

Why 2: Why did the certificate expire?
  -> Nobody renewed it before expiry

Why 3: Why didn't anyone renew it?
  -> The warning email went to a shared inbox nobody monitors

Why 4: Why doesn't anyone monitor that inbox?
  -> No process or ownership for certificate lifecycle

Why 5: Why is there no process?
  -> Certificate management was never formalized; it was done ad-hoc

ROOT CAUSE: No automated certificate lifecycle management
ACTION:     Implement cert-manager for auto-renewal + monitoring
```

---

## Part 1: Spot the Blame

### Exercise: Rewrite These Statements

Convert blame-focused language to system-focused language:

```
ORIGINAL (Blame-focused):
1. "Priya pushed the deployment without testing it properly."
2. "The on-call engineer took 15 minutes to respond because he was at dinner."
3. "The junior developer wrote a query that brought down the database."
4. "DevOps forgot to update the monitoring configuration."
5. "The team lead should have reviewed the change more carefully."

REWRITE (System-focused):
1. _______________________________________________________________
2. _______________________________________________________________
3. _______________________________________________________________
4. _______________________________________________________________
5. _______________________________________________________________
```

<details>
<summary>Example rewrites</summary>

1. "The deployment pipeline lacked automated integration tests that would have caught this regression."
2. "The alerting system did not have a secondary escalation path for after-hours incidents."
3. "The database lacked query guardrails (query timeout, row limit) to prevent resource-intensive queries from affecting production."
4. "The monitoring configuration was not managed as code, so changes could be missed during updates."
5. "The change review process did not include a checklist for high-risk database migrations."

</details>

---

## Part 2: Write a Post-Mortem

### Incident Scenario

Read this incident summary and write a complete post-mortem:

```
INCIDENT: FoodExpress Delivery Tracking Outage
DATE:     Friday, September 5, 2026
TIME:     20:15 - 20:52 IST (37 minutes)
SEVERITY: SEV-2

FACTS:
- At 20:15, the delivery-tracking service became unreachable
- Root cause: TLS certificate on delivery-tracking service expired
- A certificate expiry warning email was sent 14 days prior to a
  shared ops@foodexpress.in inbox -- nobody actioned it
- 12,000 customers could not see their delivery status
- Drivers could still deliver but customers called support
- On-call engineer Arun received PagerDuty alert at 20:18
- Arun acknowledged at 20:27 (was at a family dinner)
- Arun started investigating at 20:30
- Identified expired cert at 20:38
- Manually renewed certificate at 20:48
- Service verified healthy at 20:52
- Customer support received 340 calls during the outage
- The same certificate had expired 6 months ago (same fix applied)

SLO CONTEXT:
- Delivery tracking SLO: 99.9% availability (43.2 min/month budget)
- This incident consumed: 37 min = 85.6% of monthly budget
- Budget remaining: 6.2 min for the rest of the month
```

### Post-Mortem Template

Fill in every section:

```
POST-MORTEM: Delivery Tracking Outage
═══════════════════════════════════════════════════════════════

Date of post-mortem:  _______________
Incident date:        September 5, 2026
Author:               _______________
Attendees:            _______________

---

1. SUMMARY (2-3 sentences)
   _______________________________________________________________
   _______________________________________________________________

---

2. IMPACT
   Duration:          _______________
   Users affected:    _______________
   Support calls:     _______________
   Revenue impact:    _______________
   Error budget:      _______________
   SLO status:        _______________

---

3. TIMELINE (fill in minute by minute)
   20:15  _______________________________________________
   20:18  _______________________________________________
   20:27  _______________________________________________
   20:30  _______________________________________________
   20:38  _______________________________________________
   20:48  _______________________________________________
   20:52  _______________________________________________

---

4. ROOT CAUSE ANALYSIS (use 5 Whys)
   Why 1: ________________________________________________
   Why 2: ________________________________________________
   Why 3: ________________________________________________
   Why 4: ________________________________________________
   Why 5: ________________________________________________

   Root cause: ___________________________________________

---

5. WHAT WENT WELL
   - ____________________________________________________
   - ____________________________________________________
   - ____________________________________________________

---

6. WHAT WENT WRONG
   - ____________________________________________________
   - ____________________________________________________
   - ____________________________________________________
   - ____________________________________________________

---

7. WHERE WE GOT LUCKY
   - ____________________________________________________
   - ____________________________________________________

---

8. ACTION ITEMS
   +----+----------------------------------+----------+-----------+--------+
   | #  | Action                           | Owner    | Deadline  | Status |
   +----+----------------------------------+----------+-----------+--------+
   | 1  |                                  |          |           |        |
   | 2  |                                  |          |           |        |
   | 3  |                                  |          |           |        |
   | 4  |                                  |          |           |        |
   | 5  |                                  |          |           |        |
   +----+----------------------------------+----------+-----------+--------+

---

9. LESSONS LEARNED
   - ____________________________________________________
   - ____________________________________________________
   - ____________________________________________________
```

---

## Part 3: Peer Review

### Swap post-mortems with another group and review:

Checklist:
```
[ ] Is the language blameless throughout?
    (No person named as the cause, only systems/processes)
[ ] Is the timeline complete? (No gaps > 5 minutes)
[ ] Does the root cause go deep enough? (Not just "cert expired")
[ ] Are action items specific? (Not "improve monitoring")
[ ] Do action items have owners AND deadlines?
[ ] Is there at least one action to prevent recurrence?
[ ] Is there a "Where We Got Lucky" section?
    (This catches near-misses that won't be lucky next time)
```

---

## Key Takeaways

1. **Blameless != Accountable-less** -- we still assign action items with owners
2. **Systems fail, not people** -- if a human can make a mistake, the system should prevent it
3. **5 Whys** gets you past symptoms to root causes
4. **"Where We Got Lucky"** catches risks that didn't cause damage THIS time
5. **Repeat incidents** (like this cert expiry) mean prior action items weren't completed
6. Every post-mortem should reduce the chance of the SAME incident recurring

> **Next:** Lab 07 -- The cert renewal in this incident was toil. Let's learn to identify and eliminate toil.
