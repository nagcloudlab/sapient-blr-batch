# ITIL Practices -- Submission Checklist
## Module 35 | Days 41-42

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Incident: Priority is P1 (High Impact + High Urgency) | [ ] |
| 2 | Incident: Category is "Application > Order > API" | [ ] |
| 3 | Incident: P1 response time is 15 minutes | [ ] |
| 4 | Incident: Assigned to Platform Engineering team | [ ] |
| 5 | Incident: Status flow includes New > In Progress > Resolved > Closed | [ ] |
| 6 | Incident: Related CI is order-service (not email-server) | [ ] |
| 7 | Incident: Communication plan with stakeholders, status page, customer message | [ ] |
| 8 | Change: Type is "Normal" (not Standard) | [ ] |
| 9 | Change: Risk assessment is "Medium" with mitigation plan | [ ] |
| 10 | Change: Implementation plan includes validation/test steps | [ ] |
| 11 | Change: Rollback plan is specific and actionable | [ ] |
| 12 | Change: Scheduled during maintenance window (not peak hours) | [ ] |
| 13 | Change: CAB approval is required and documented | [ ] |
| 14 | Problem: Status is "Known Error" (not Closed) | [ ] |
| 15 | Problem: Lists all 5 related incidents | [ ] |
| 16 | Problem: Complete 5 Whys to actual root cause (missing index) | [ ] |
| 17 | Problem: Workaround is actionable (kill report query) | [ ] |
| 18 | Problem: Permanent fix defined with change request and date | [ ] |
| 19 | Problem: Trend data shows 5 occurrences, weekly pattern | [ ] |
| 20 | SLA: Availability target is 99.9% | [ ] |
| 21 | SLA: P1 resolution time is 4 hours | [ ] |
| 22 | SLA: Monthly measurement period | [ ] |
| 23 | SLA: Financial penalties (service credits) for breach | [ ] |
| 24 | SLA: Weekends NOT excluded from 24x7 service | [ ] |
| 25 | SLA: Monthly reporting frequency | [ ] |

---

## Self-Check Questions

1. **Why P1 and not P4?** Impact=High + Urgency=High = P1. A P4 response would leave ~2,000 customers unable to order for hours.
2. **Why can't a DB schema migration be a Standard change?** Standard changes are pre-authorized, low-risk, repeatable. A schema migration on a 10M-row production table is Medium risk and needs CAB review.
3. **Why stop at 2 Whys?** "Because it broke" is not a root cause. You must dig until you find a systemic cause that can be permanently fixed (the missing index).
4. **Why not exclude weekends from SLA?** A 24x7 service means customers order food on weekends too. Weekend outages absolutely count.
5. **Why are service credits important?** Without financial consequences, there is no accountability for SLA breaches. Service credits align incentives.
