# FoodExpress Toil Assessment
## STARTER CODE -- Contains misclassifications to fix

---

## Current Tasks Inventory

| # | Task | Frequency | Duration | Monthly Hours | Is this Toil? |
|---|------|-----------|----------|---------------|---------------|
| 1 | Restart crashed pods manually | 3x/week | 15 min | 3.0 | TODO |
| 2 | Scale services for lunch rush | Daily | 10 min | 3.5 | TODO |
| 3 | Database backup verification | Daily | 20 min | 7.0 | TODO |
| # BUG 1: Monitoring dashboards is engineering work, NOT toil |
| 4 | Monitoring dashboards | Ongoing | -- | 10.0 | Toil? |
| 5 | SSL certificate renewal | Quarterly | 2 hrs | 0.67 | TODO |
| 6 | Deploy to staging manually | 2x/week | 30 min | 4.0 | TODO |
| 7 | Manually rotate log files | Weekly | 5 min | 0.33 | TODO |
| # BUG 1: Architecture review is engineering work, NOT toil |
| 8 | Architecture review meetings | Monthly | 2 hrs | 2.0 | Toil? |
| 9 | Manually update DNS records | Monthly | 15 min | 0.25 | TODO |
| 10 | Respond to false alarm alerts | 5x/week | 10 min | 3.3 | TODO |

---

## Classification Guide

A task is TOIL if it is:
- [ ] Manual (requires human intervention)
- [ ] Repetitive (done the same way each time)
- [ ] Automatable (a script/tool could do it)
- [ ] Tactical (reactive, not proactive)
- [ ] No enduring value (doesn't improve the system)
- [ ] Scales linearly (more traffic = more work)

---

## Prioritization Matrix

# BUG 2: Tasks not prioritized -- complete this matrix

| # | Task | Frequency Score (1-5) | Impact Score (1-5) | Priority (F x I) | Automation Effort |
|---|------|-----------------------|--------------------|-------------------|-------------------|
| TODO | TODO | TODO | TODO | TODO | TODO |

---

## 3-Month Automation Roadmap

# BUG 3: No effort estimates -- complete this roadmap

| Month | Task to Automate | Effort | Expected Toil Reduction |
|-------|-----------------|--------|------------------------|
| Month 1 | TODO | TODO | TODO hours/month |
| Month 2 | TODO | TODO | TODO hours/month |
| Month 3 | TODO | TODO | TODO hours/month |

**Current total toil:** TODO hours/month
**Target after 3 months:** < 5 hours/month
