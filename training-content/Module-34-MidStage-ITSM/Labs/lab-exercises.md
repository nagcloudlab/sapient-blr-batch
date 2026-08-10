# Mid-Stage Project + ITSM Introduction -- Lab Exercises
## Module 34 | Days 39-40

---

## Client Email

```
From: ananya.rao@foodexpress.in
To: sustain-engineering@team.com
Subject: Observability Gaps & Incident Response Issues
Date: 2026-09-05

Team,

Our FoodExpress platform has been experiencing issues that take
too long to detect and resolve:

1. The Prometheus alerting rules have bugs -- some alerts never
   fire, others fire too often
2. The fault injection script has errors that prevent proper
   chaos experiments
3. Our incident response template is incomplete and missing
   key fields
4. The ITSM process flow has incorrect categorization

Please fix these issues so we can improve our incident response
times and build confidence in our monitoring stack.

-- Ananya Rao, Platform Lead, FoodExpress
```

---

## Lab 1: Fix the Prometheus Alerting Rules (8 bugs)

**File:** `starter-code/prometheus-alerts.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Look at the error rate calculation | Division by zero possible when no requests | Alert crashes Prometheus evaluation |
| 2 | Check the `for` duration on HighErrorRate | Duration is 0s -- alert fires on any transient spike | Alert fatigue from false positives |
| 3 | Look at PaymentServiceDown `expr` | Wrong metric name used | Alert never fires when payment is actually down |
| 4 | Check HighLatency threshold | Threshold set to 0.001 seconds (1ms) | Every request triggers this alert |
| 5 | Look at DiskSpaceLow percentage direction | Alert fires when disk is MORE than 20% free | Alert logic is inverted |
| 6 | Check the severity labels | All alerts have severity: info | Critical alerts not routed to PagerDuty |
| 7 | Look at HighMemoryUsage expr | Missing container label filter | Alert matches system containers, not app |
| 8 | Check the runbook URLs | Runbook URLs point to localhost | Runbooks unreachable in production |

### Verification

After fixing, validate with `promtool check rules prometheus-alerts.yaml` (or manually review).

---

## Lab 2: Fix the Fault Injection Script (6 bugs)

**File:** `starter-code/fault-injection.sh`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the namespace variable | Namespace is hardcoded to `default` instead of `foodexpress` | Fault injected in wrong namespace |
| 2 | Look at the steady state check | Threshold comparison is inverted (`<` instead of `>=`) | PASS/FAIL logic is backwards |
| 3 | Check the rollback command | Missing `tc qdisc del` -- uses `add` again | Latency doubled instead of removed |
| 4 | Look at the sleep duration | Sleep is 5 seconds instead of 180 | Not enough observation time |
| 5 | Check the curl command for Prometheus | Missing `-s` flag and wrong API path | Script errors out on metric query |
| 6 | Look at the jq parsing | Wrong JSON path for extracting value | Always returns null |

### Verification

Read through the fixed script end-to-end. Each step should: record baseline, inject fault, wait, observe, and cleanly rollback.

---

## Lab 3: Fix the Incident Response Template (6 bugs)

**File:** `starter-code/incident-template.md`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the Priority field | Priority is set to P5 for a production outage | Incident not escalated properly |
| 2 | Look at the Affected Users count | Shows "0 users" for a platform-wide outage | Business impact underreported |
| 3 | Check the Timeline section | Events are in random order, not chronological | Confusing during post-incident review |
| 4 | Look at the Resolution field | Resolution says "Restart the server" but the root cause is a code bug | Resolution doesn't match root cause |
| 5 | Check the Escalation section | No escalation contacts or timeframes listed | Engineers don't know who to call |
| 6 | Look at the Prevention section | Prevention section is empty | Same incident will recur |

### Verification

The completed template should tell a clear story: what happened, when, what was done, and how to prevent recurrence.

---

## Lab 4: Fix the ITSM Process Flow (5 bugs)

**File:** `starter-code/itsm-process-flow.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the incident categories | "Payment" is categorized under "Infrastructure" | Misrouted to wrong team |
| 2 | Look at the priority matrix | Impact "High" + Urgency "High" maps to P3 | Critical incidents treated as medium |
| 3 | Check the escalation timers | P1 escalation time is 24 hours | Major outages not escalated quickly enough |
| 4 | Look at the SLA targets | Resolution time for P1 is longer than P5 | SLA values are swapped |
| 5 | Check the notification rules | Critical incidents only notify via email | No pager/phone for critical outages |

### Verification

Walk through a sample P1 incident from detection to resolution and confirm each step follows the corrected process.

---

## Bonus Challenge: Design a Runbook

Design a complete runbook for the following FoodExpress scenario:

**Scenario:** The order service is returning HTTP 500 errors at a rate above 5% for the last 10 minutes.

Your runbook should include:
1. Alert trigger conditions
2. Quick diagnosis steps (first 5 minutes)
3. Common causes table with checks and fixes
4. Escalation path with timeframes
5. Communication template for stakeholders
6. Post-resolution verification steps

---

## Lab Submission

| # | Item | Done? |
|---|------|-------|
| 1 | All 8 Prometheus alert bugs fixed | [ ] |
| 2 | All 6 fault injection script bugs fixed | [ ] |
| 3 | All 6 incident template bugs fixed | [ ] |
| 4 | All 5 ITSM process flow bugs fixed | [ ] |
| 5 | (Bonus) Complete runbook designed | [ ] |
