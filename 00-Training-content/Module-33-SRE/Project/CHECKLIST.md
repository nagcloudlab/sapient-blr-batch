# SRE Automation -- Submission Checklist
## Module 33 | Days 37-38

---

## Submission Checklist

### Lab 1: SLO Definitions
| # | Item | Done? |
|---|------|-------|
| 1 | Order-service SLO changed from 100% to realistic target (e.g., 99.9%) | [ ] |
| 2 | Payment-service SLI changed from "uptime" to user-centric metric | [ ] |
| 3 | All measurement windows changed to 30-day rolling | [ ] |
| 4 | Error budgets calculated for all services | [ ] |
| 5 | Error budget policy defined with actions at each level | [ ] |

### Lab 2: Error Budget Calculator
| # | Item | Done? |
|---|------|-------|
| 6 | Monthly error budgets calculated correctly in minutes | [ ] |
| 7 | Budget consumption tracked for 3 given incidents | [ ] |
| 8 | Remaining budget and percentage calculated | [ ] |
| 9 | Policy actions determined for each service | [ ] |
| 10 | Monthly projection completed | [ ] |

### Lab 3: Toil Assessment
| # | Item | Done? |
|---|------|-------|
| 11 | Monitoring dashboards and architecture reviews classified as NOT toil | [ ] |
| 12 | All genuine toil tasks identified | [ ] |
| 13 | Prioritization matrix completed (frequency x impact) | [ ] |
| 14 | 3-month automation roadmap with effort estimates | [ ] |

### Lab 4: Post-Mortem
| # | Item | Done? |
|---|------|-------|
| 15 | Timeline filled in with minute-by-minute events | [ ] |
| 16 | "What Went Wrong" rewritten to be blameless (systemic focus) | [ ] |
| 17 | All action items have owners and deadlines | [ ] |
| 18 | Lessons learned section completed | [ ] |

### Lab 5: MCQ
| # | Item | Done? |
|---|------|-------|
| 19 | MCQ assessment completed (30 questions) | [ ] |

---

## Self-Check Questions

1. **Why not 100% SLO?** Impossible to achieve; error budget would be zero, blocking all deployments. The cost of each additional "nine" grows exponentially.
2. **What is the difference between SLI and SLO?** SLI is the metric (what you measure); SLO is the target (what you aim for). Example: SLI = availability percentage; SLO = 99.9%.
3. **Why is "blameless" important?** If people fear blame, they hide mistakes. Hidden mistakes prevent learning and lead to repeated failures.
4. **How do you distinguish toil from engineering?** Toil is manual, repetitive, automatable, tactical, and scales linearly. Engineering work creates enduring value and requires judgment.
