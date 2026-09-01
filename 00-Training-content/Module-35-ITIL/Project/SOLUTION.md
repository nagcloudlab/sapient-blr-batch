# ITIL Practices -- Trainer Solutions & Hints
## Module 35 | Days 41-42

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Incident Record | P1 priority (High/High), correct category path, 15-min response, Platform Engineering assignment, full status flow, correct CI, communication plan | Students fix priority but forget the communication plan. In a real P1, stakeholder communication is critical | Ask: "If the VP of Engineering finds out about a P1 outage from Twitter instead of your team, what happens?" |
| 2 | Fix Change Request | Normal type (not Standard), Medium risk with mitigation, validation steps in plan, rollback plan, maintenance window, CAB approval required | Students add a rollback plan but make it vague ("roll back changes"). Push for specific commands | Ask: "It's 3 AM and the migration failed. Can a junior DBA follow your rollback plan?" |
| 3 | Fix Problem Record | Known Error status, list 5 incidents, complete 5 Whys to root cause, actionable workaround, permanent fix with CHG, accurate trend | Students stop at 3 Whys. The real root cause (missing index) only emerges at Why 5 | Ask: "Why 2 says 'because it broke.' Does that help you fix anything?" |
| 4 | Fix SLA Definition | 99.9% availability, 4-hour P1 resolution, monthly measurement, service credits, remove weekend exclusion, monthly reports | Students set 99.99% (too ambitious). Discuss what 99.9% vs 99.99% means in downtime minutes | Ask: "Can FoodExpress really guarantee 52.6 minutes of downtime per YEAR? Be realistic." |
| 5 | Practice Mapping | 1: Incident, 2: Problem, 3: Service Request, 4: Change+Release, 5: Capacity, 6: Service Catalog+Request, 7: IT Asset+Change, 8: Service Level | Students confuse incidents and service requests. Emphasize: incident = unplanned disruption, request = standard fulfillment | Ask: "Is 'I need Grafana access' an incident or a request?" (Request) |
| 6 | Integration | INC > PRB > CHG > Release flow showing how practices connect | Students treat practices as isolated. The integration exercise shows the feedback loop | Ask: "If you skip Problem Management, what happens to this incident next Tuesday?" (It recurs) |

---

## Practice Mapping Answers

| # | Scenario | Practice(s) |
|---|---------|-------------|
| 1 | Customer cannot place an order | **Incident Management** (unplanned disruption) |
| 2 | Payment failures every Tuesday | **Problem Management** (pattern detection, root cause) |
| 3 | Developer requests prod log access | **Service Request Management** (standard request) |
| 4 | Upgrade MySQL 8.0 to 8.2 | **Change Control** + **Release Management** |
| 5 | Diwali 5x traffic planning | **Capacity & Performance Management** |
| 6 | New restaurant onboarding | **Service Catalogue Management** + **Service Request Management** |
| 7 | Container image CVE | **IT Asset Management** + **Change Control** (security patch) |
| 8 | SLA shows 99.7% (below 99.9%) | **Service Level Management** (SLA breach review) |

---

## Key Discussion Points

1. What is the difference between an incident and a service request? (Incident = unplanned disruption; Request = predefined standard fulfillment)
2. Why does Problem Management matter for sustain engineering? (Without it, the same incidents repeat forever)
3. When should a change skip the CAB? (Only Standard changes and true Emergencies)
4. Why is "yearly" SLA measurement dangerous? (Hides bad months; customers care about each month)
5. What makes a good workaround? (Specific, tested, time-bounded, with clear steps)
6. How do ITIL and DevOps complement each other? (ITIL provides process governance; DevOps provides speed and automation)
