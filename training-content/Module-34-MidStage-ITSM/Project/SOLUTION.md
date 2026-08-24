# Mid-Stage Project + ITSM Introduction -- Trainer Solutions & Hints
## Module 34 | Days 39-40

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Prometheus Alerts | Add `and rate(...) > 0` guard, fix `for:` duration, correct metric names, set proper severities, use production runbook URLs | Students fix severity but miss the division-by-zero guard. Emphasize that PromQL division by zero silently produces NaN | Ask: "What happens to your alert if no requests come in for 5 minutes?" (Division by zero) |
| 2 | Fix Fault Injection | Correct namespace to `foodexpress`, fix comparison direction, change `add` to `del` for rollback, increase sleep to 180s, fix API path and jq parsing | Students fix the namespace but miss the rollback bug (add vs del). The script would make things worse | Ask: "After this script runs, is the latency removed or doubled?" (Doubled -- bug 3) |
| 3 | Fix Incident Template | P1 priority, real user count, chronological timeline, matching resolution to root cause, complete escalation path, prevention actions | Students fix the priority but leave the resolution as "restart server" when the root cause is a code bug. Resolution must match root cause | Ask: "If restarting fixes it temporarily, what happens when the next new customer orders?" (Crash again) |
| 4 | Fix ITSM Process Flow | Move Payment to Application category, P1 for high/high, 15min P1 escalation, swap P1/P5 resolution times, add PagerDuty/phone for P1 | Students fix the priority matrix but miss the swapped SLA targets. Walk through: "Does it make sense that P5 resolves faster than P1?" | Ask: "Would you wait 24 hours to escalate a complete outage?" (No -- 15 minutes max) |
| 5 | Dashboard Design | Golden signals as stat panels at top, time series for trends, heatmap for latency distribution, table for top errors | Students create too many panels. Guide toward the "glance, scan, drill-down" principle | Ask: "If you wake up at 3 AM to an alert, what's the first thing you want to see?" |
| 6 | Runbook | Clear trigger, 5-minute quick diagnosis, common causes table, escalation path, communication template | Students write generic runbooks. Emphasize specificity: exact PromQL queries, exact kubectl commands | Ask: "Could a junior engineer follow this runbook at 3 AM with no prior context?" |

---

## Key Discussion Points

1. Why is alert fatigue dangerous? (Engineers start ignoring alerts, miss real incidents)
2. What is the difference between an incident and a problem? (Incident = symptom, Problem = root cause)
3. Why does chaos engineering require a hypothesis? (Without one, you're just breaking things randomly)
4. How do you decide the right `for:` duration on an alert? (Balance between speed and noise)
5. Why must the resolution in an incident record match the root cause? (Otherwise you haven't actually fixed it)
6. What is a blameless post-incident review? (Focus on system improvements, not individual blame)
