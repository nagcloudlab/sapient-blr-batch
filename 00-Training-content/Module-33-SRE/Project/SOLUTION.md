# SRE Automation -- Trainer Solutions & Hints
## Module 33 | Days 37-38

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix SLO Definitions | 99.9% (not 100%); user-centric SLI (transactions not uptime); 30-day window; calculate budgets | Students set all SLOs to 99.9%. Different services need different targets based on business impact. Payment needs higher reliability than menu browsing | Ask: "Would you rather have menu browsing down for 1 hour or payment processing down for 1 hour? That's why SLOs differ." |
| 2 | Error Budget Calculator | 43.2 min for 99.9%; payment-service budget nearly exhausted (1.6 min left); policy says freeze | Students forget that 30-day rolling means the window moves. An incident from 31 days ago drops off. Also students miscalculate: 43,200 x 0.001 = 43.2, not 432 | Ask: "Payment-service has 1.6 minutes of budget left. What does your error budget policy say? Can you deploy on Friday?" |
| 3 | Toil Assessment | Monitoring dashboards and architecture reviews are NOT toil. DB backup (7 hrs/mo) is highest-priority automation | Students classify ALL operational work as toil. Clarify: toil is repetitive and automatable. Strategic work, judgment calls, and creative problem-solving are engineering, not toil | Ask: "Can a robot do this task? If yes, it's toil. If it requires human judgment, it's engineering." |
| 4 | Blameless Post-Mortem | Fill timeline minute-by-minute; rewrite blame to systemic causes; add owners and deadlines to all action items | Students rewrite "Rajesh forgot" as "The team forgot." That's still blame! The blameless version is: "No automated renewal system was in place" -- focus on the missing system, not the person | Ask: "If we replace Rajesh with a different engineer, would this incident still happen?" (Yes -- the system is the problem) |
| 5 | MCQ | Answers: D (Alerts is not a pillar), B (43.8 min), B (Systems and processes) | Students confuse SLI (the metric) with SLO (the target). SLI is what you measure; SLO is what you aim for | Ask: "Is 99.9% an SLI or an SLO?" (SLO -- it's a target. The SLI is the measurement itself) |

---

## Key Discussion Points

1. Why not aim for 100% availability? (Impossible; blocks all changes; exponential cost)
2. How do error budgets align dev and ops? (Shared incentive: dev wants to deploy, ops wants stability; error budget is the contract)
3. What makes a good SLI? (User-centric, measurable, actionable)
4. Why is "blameless" critical for learning? (If people fear punishment, they hide mistakes; hiding mistakes prevents learning)
5. How does toil reduction create a virtuous cycle? (Less toil = more engineering time = more automation = even less toil)
6. When is chaos engineering appropriate? (After basic monitoring and reliability practices are in place; not on day one)

---

## MCQ Answer Key (Selected)

1. D (Alerts) -- The three pillars are Logs, Metrics, Traces
2. B (43.8 min) -- 30 days = 43,200 min; 0.1% = 43.2 min (rounding to 43.8 for standard 30.44 days)
3. B (Systems and processes) -- Blameless post-mortems focus on systemic improvements
4. C (rate()) -- Counters need rate() to be useful; without it you see ever-increasing numbers
5. A (SLI) -- SLI is the measurement; SLO is the target value for that measurement
