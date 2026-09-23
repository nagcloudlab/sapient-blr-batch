# ServiceNow Labs -- Teaching Plan (Day-wise Mapping)

**Programme:** PSI-2026 Jul Sustain Eng BLR Batch
**Available Time:** 4.5 days (Days 38-42) for ITSM + ITIL + ServiceNow
**ServiceNow Hands-on Time:** ~2.5 days (Day 40 PM + Day 41 + Day 42 AM)
**Total Labs:** 22 | **Total Lab Duration:** ~40 hours
**Strategy:** Core labs in class, remaining as self-study reference

---

## Time Budget

```
Day 38 PM (3 hrs):  ITSM Theory (phase-1-itsm docs + PPT)
Day 39    (7 hrs):  ITIL 4 Practices (phase-2-itil-framework)
Day 40 AM (3 hrs):  ITIL Practices continued
Day 40 PM (3 hrs):  ServiceNow Intro + Labs 01-03 (PDI setup, navigation, lists)
Day 41    (7 hrs):  ServiceNow Labs 04, 07, 12, 13 (Users, CMDB, Deploy Stack, Incidents)
Day 42 AM (3 hrs):  ServiceNow Labs 09, 15 (SLA, Change Management)
Day 42 PM (3 hrs):  ITSM Role Play + Final Project kickoff
Day 43    (7 hrs):  Final Project (participants apply labs independently)
```

---

## Day-wise Lab Plan

### Day 40 PM -- ServiceNow First Touch (3 hours)

| Time | Lab | Title | What Participants Do |
|------|-----|-------|---------------------|
| 13:30-14:00 | -- | Walkthrough: phase-3-servicenow/ docs 17-18 | Instructor demo of ServiceNow platform |
| 14:00-14:30 | Lab 01 | PDI Setup | Everyone gets their Personal Developer Instance |
| 14:30-15:15 | Lab 02 | Platform Navigation | Navigator, menus, search, workspaces |
| 15:15-15:30 | Break | -- | -- |
| 15:30-16:15 | Lab 03 | Lists & Forms | List views, form layout, personalization |
| 16:15-16:30 | -- | Recap + assign Lab 04-06 as homework | Participants complete foundation labs at home |

**Homework:** Labs 04 (Users/Groups/Roles), 05 (Tables/Columns), 06 (Filters/Views) -- use Background Scripts from appendix for quick setup if short on time.

---

### Day 41 -- Core ITSM in ServiceNow (7 hours)

| Time | Lab | Title | What Participants Do |
|------|-----|-------|---------------------|
| 09:00-09:15 | -- | Recap: verify Lab 04-06 homework done | Quick check everyone has users/groups created |
| 09:15-10:30 | Lab 07 | CMDB & Configuration Management | Create 12 UPI CIs, relationships, service map |
| 10:30-10:45 | Break | -- | -- |
| 10:45-11:30 | Lab 07 | CMDB continued | Use Background Script if time-constrained |
| 11:30-12:30 | Lab 12 | Deploy Demo Stack & Event Management | docker compose up, traffic, Prometheus, Grafana |
| 12:30-13:30 | Lunch | -- | -- |
| 13:30-15:00 | Lab 13 | Incident Management -- Full Lifecycle | Chaos injection, auto-incident, SLA, escalation |
| 15:00-15:15 | Break | -- | -- |
| 15:15-16:00 | Lab 14 | Problem Management (walkthrough) | Create problem from recurring incidents, RCA |
| 16:00-16:30 | -- | Recap + assign remaining labs | Point to self-study labs |

**Instructor Note:** Lab 12 requires Docker. If participants don't have Docker, do an instructor-led demo and share the Grafana screenshots. Labs 07 and 13 are the most critical -- don't skip these.

---

### Day 42 AM -- SLA & Change Management (3 hours)

| Time | Lab | Title | What Participants Do |
|------|-----|-------|---------------------|
| 09:00-09:15 | -- | Recap Day 41 | Review incidents, problems created |
| 09:15-10:30 | Lab 09 | SLA, SLO & SLI | Create SLA definitions, schedules, test breach |
| 10:30-10:45 | Break | -- | -- |
| 10:45-12:00 | Lab 15 | Change Management | Normal/Standard/Emergency changes, CAB approval |
| 12:00-12:30 | -- | Wrap-up: The ITIL Lifecycle in ServiceNow | Tie it all together: Incident -> Problem -> Change |

---

### Day 42 PM -- Role Play + Final Project (3 hours)

| Time | Activity |
|------|----------|
| 13:30-15:00 | ITSM Role Play (use docs/ITSM-ROLEPLAY-FACILITATION-GUIDE.md) |
| 15:00-15:15 | Break |
| 15:15-16:30 | Final Project kickoff -- participants choose labs to complete |

---

### Day 43 -- Final Project (7 hours)

Participants work independently or in teams on their ServiceNow PDI. They can:
- Complete remaining labs from the self-study list
- Build the full ITIL lifecycle: CMDB -> Services -> SLAs -> Incident -> Problem -> Change
- Create reports and dashboards (Lab 17)
- Demo their configured ServiceNow instance

---

## Lab Classification

### Must-Do in Class (Core)

| Lab | Title | Duration | Why It's Essential |
|-----|-------|----------|-------------------|
| 01 | PDI Setup | 30 min | Can't do anything without it |
| 02 | Platform Navigation | 30 min | Foundation for all other labs |
| 03 | Lists & Forms | 45 min | Core UI skills |
| 07 | CMDB & Configuration Management | 90 min | Foundation for all ITIL practices |
| 09 | SLA, SLO & SLI | 90 min | Core ITSM metric -- maps to SRE (M33) |
| 12 | Deploy Demo Stack | 60 min | Live monitoring -> ServiceNow pipeline |
| 13 | Incident Management | 90 min | Most important ITSM process |
| 15 | Change Management | 90 min | Critical ITIL practice |

**Total Core:** ~8.5 hours (fits in 2.5 days with demos and breaks)

### Homework (Assign Day 40 evening)

| Lab | Title | Duration | Notes |
|-----|-------|----------|-------|
| 04 | Users, Groups & Roles | 60 min | Setup for all subsequent labs |
| 05 | Tables & Columns | 60 min | Understanding data model |
| 06 | Filters, Views & Queries | 45 min | Efficient navigation |

### Instructor Walkthrough (Demo, not hands-on)

| Lab | Title | Duration | Notes |
|-----|-------|----------|-------|
| 08 | Service Portfolio | 60 min | Show concepts, skip hands-on |
| 14 | Problem Management | 75 min | Walk through RCA process |
| 16 | Release Management | 60 min | Show release calendar concept |

### Self-Study Reference (Post-training)

| Lab | Title | Duration | Notes |
|-----|-------|----------|-------|
| 10 | Knowledge Management | 60 min | Can explore independently |
| 11 | Service Catalog | 90 min | Advanced -- good for motivated learners |
| 17 | Reporting & Analytics | 90 min | Great for final project |
| 18 | Continual Improvement | 60 min | Conceptual, easy to self-study |
| 19 | Availability & Capacity | 60 min | Ties to SRE M33 concepts |
| 20 | Flow Designer | 90 min | Advanced automation |
| 21 | Business Rules & Scripts | 90 min | Advanced development |
| 22 | REST API & Update Sets | 90 min | Advanced integration |

---

## Quick Setup for Time-Constrained Sessions

If a session is running behind, use the **Background Scripts** (Appendix in each lab) to bulk-create data:

```
Lab 04: Run background script to create all 6 UPI users + groups + roles    (~2 min)
Lab 07: Run background script to create all 12 CIs + relationships          (~2 min)
Lab 09: Run background script to create all 7 SLA definitions + schedules   (~2 min)
Lab 17: Run background script to create 50 incidents + 20 changes for reports (~2 min)
```

This lets you skip the manual creation steps and focus on the **concepts and exploration**.

---

## Cross-Reference with sustain-engineering-training

| sustain-eng Module | 12-ITSM Content | Relationship |
|--------------------|-----------------|-------------|
| Module 34 (ITSM labs) | phase-1-itsm + phase-2-itil | Theory foundation |
| Module 35 (ITIL practices) | phase-2-itil-framework | ITIL 4 deep dive |
| Module 36 (ServiceNow) | phase-4-servicenow-labs | Hands-on labs |
| Module 36 bug-fix labs | archive-v1 style | Complementary (fix bugs vs build) |
| mcq-10-itsm-itil-servicenow | phase-2 HTML quizzes | Assessment |
| war-game-scripts | demo-e2e-incident/chaos | Chaos engineering |
| itil-templates | docs/ + KB articles in Lab 10 | Reference templates |

---

## Final Project Ideas (Day 43)

Participants can choose one:

1. **Full ITIL Lifecycle Demo** -- Build CMDB, create incident from chaos, escalate to problem, raise change, deploy fix, create report
2. **Service Catalog Builder** -- Create 5 catalog items with approval workflows for UPI services
3. **Monitoring Dashboard** -- Build executive dashboard with MTTR, SLA compliance, change success rate
4. **Automation Challenge** -- Create 3 Flow Designer flows for auto-assignment, escalation, auto-close
5. **API Integration** -- Use REST API to create incidents programmatically and build a custom Scripted REST endpoint
