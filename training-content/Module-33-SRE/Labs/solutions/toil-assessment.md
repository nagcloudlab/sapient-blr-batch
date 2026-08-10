# FoodExpress Toil Assessment
## SOLUTION

---

## Current Tasks -- Classification

| # | Task | Frequency | Duration | Monthly Hours | Is this Toil? | Explanation |
|---|------|-----------|----------|---------------|---------------|-------------|
| 1 | Restart crashed pods manually | 3x/week | 15 min | 3.0 | YES | Manual, repetitive, automatable (K8s probes) |
| 2 | Scale services for lunch rush | Daily | 10 min | 3.5 | YES | Manual, repetitive, automatable (HPA) |
| 3 | Database backup verification | Daily | 20 min | 7.0 | YES | Manual, repetitive, automatable (script) |
| 4 | Monitoring dashboards | Ongoing | -- | 10.0 | NO | # FIX 1: Engineering work -- builds enduring value, requires judgment |
| 5 | SSL certificate renewal | Quarterly | 2 hrs | 0.67 | YES | Manual, repetitive, automatable (cert-manager) |
| 6 | Deploy to staging manually | 2x/week | 30 min | 4.0 | YES | Manual, repetitive, automatable (Jenkins) |
| 7 | Manually rotate log files | Weekly | 5 min | 0.33 | YES | Manual, repetitive, automatable (logrotate) |
| 8 | Architecture review meetings | Monthly | 2 hrs | 2.0 | NO | # FIX 1: Engineering work -- strategic, requires human judgment |
| 9 | Manually update DNS records | Monthly | 15 min | 0.25 | YES | Manual, repetitive, automatable (Terraform/IaC) |
| 10 | Respond to false alarm alerts | 5x/week | 10 min | 3.3 | YES | Automatable by fixing alert thresholds |

**Total toil:** 22.05 hours/month (tasks 1,2,3,5,6,7,9,10)
**Total engineering:** 12.0 hours/month (tasks 4,8)
**Toil percentage:** 64.7% -- exceeds the 50% SRE target

---

## Prioritization Matrix

# FIX 2: Tasks prioritized by Frequency x Impact

| # | Task | Freq Score (1-5) | Impact Score (1-5) | Priority (F x I) | Automation Effort |
|---|------|------------------|--------------------|-------------------|-------------------|
| 3 | DB backup verification | 5 (daily) | 4 (data safety) | 20 | Low (cron + script) |
| 2 | Scale for lunch rush | 5 (daily) | 4 (performance) | 20 | Low (HPA config) |
| 6 | Deploy to staging | 3 (2x/week) | 4 (velocity) | 12 | Medium (Jenkins pipeline) |
| 10 | False alarm alerts | 4 (5x/week) | 3 (focus) | 12 | Low (fix thresholds) |
| 1 | Restart crashed pods | 3 (3x/week) | 3 (availability) | 9 | Low (liveness probes) |
| 7 | Log rotation | 2 (weekly) | 2 (disk space) | 4 | Low (logrotate config) |
| 5 | SSL cert renewal | 1 (quarterly) | 5 (outage risk) | 5 | Medium (cert-manager) |
| 9 | DNS updates | 1 (monthly) | 2 (low frequency) | 2 | Medium (Terraform) |

---

## 3-Month Automation Roadmap

# FIX 3: Complete roadmap with effort estimates

| Month | Task to Automate | Effort | Expected Toil Reduction |
|-------|-----------------|--------|------------------------|
| Month 1 | K8s liveness probes (task 1) | 2 hours | 3.0 hrs/month |
| Month 1 | HPA configuration (task 2) | 3 hours | 3.5 hrs/month |
| Month 1 | Fix alert thresholds (task 10) | 2 hours | 3.3 hrs/month |
| Month 2 | DB backup cron script (task 3) | 4 hours | 7.0 hrs/month |
| Month 2 | Jenkins staging pipeline (task 6) | 8 hours | 4.0 hrs/month |
| Month 3 | cert-manager setup (task 5) | 4 hours | 0.67 hrs/month |
| Month 3 | logrotate config (task 7) | 1 hour | 0.33 hrs/month |
| Month 3 | Terraform DNS (task 9) | 4 hours | 0.25 hrs/month |

**Current total toil:** 22.05 hours/month
**After Month 1:** 12.25 hours/month (-9.8 hrs, 44.5% reduction)
**After Month 2:** 1.25 hours/month (-11.0 hrs, 94.3% reduction)
**After Month 3:** 0.0 hours/month (all toil automated)
**Total automation effort:** 28 hours (pays for itself in < 2 months)
