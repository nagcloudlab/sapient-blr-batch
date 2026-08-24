# ServiceNow -- Lab Exercises
## Module 36 | Days 43-44

---

## Client Email

```
From: amit.shah@foodexpress.in
To: sustain-engineering@team.com
Subject: ServiceNow Configuration Issues
Date: 2026-09-10

Team,

We recently set up ServiceNow for FoodExpress but the
configuration has several problems:

1. The SLA policy definitions have wrong conditions and timers
2. The email notification templates have broken variables and
   incorrect routing
3. The ServiceNow instance configuration YAML has security
   and access control issues

Please review and fix these configurations.

Also, prepare for the ITSM MCQ assessment and role play
exercises on Day 44.

-- Amit Shah, Engineering Lead, FoodExpress
```

---

## Lab 1: Fix the SLA Policy Configuration (7 bugs)

**File:** `starter-code/sla-policies.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check P1 start condition | Start condition checks Priority = 5 (Planning) | SLA attaches to wrong incidents |
| 2 | Look at P1 duration | Duration is set to 240 hours (10 days) | P1 SLA is far too lenient |
| 3 | Check the stop condition | Stop condition is "State = New" | SLA stops immediately after starting |
| 4 | Look at the pause condition | Pause when "State = In Progress" | SLA pauses during active investigation |
| 5 | Check P2 schedule | Schedule is "Business Hours" for a P2 critical service | P2 should use 24x7 schedule |
| 6 | Look at the breach notification | Notification is sent at 100% (already breached) | No warning before SLA breaches |
| 7 | Check the SLA target name | Name says "Email Service" but it's for incidents | Confusing for engineers and reports |

### Verification

Trace a P1 incident through: creation, investigation, pending, resolution. Does the SLA timer behave correctly at each stage?

---

## Lab 2: Fix the Email Notification Templates (6 bugs)

**File:** `starter-code/email-notifications.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the P1 notification subject | Subject line is blank | Engineers don't know what the email is about |
| 2 | Look at the variable syntax | Uses `{number}` instead of `${number}` | Variables not resolved, literal text shown |
| 3 | Check who receives the P1 notification | Recipients list is empty | Nobody receives the critical notification |
| 4 | Look at the SLA breach notification condition | Condition checks for `priority = 5` | Only P5 (Planning) SLA breaches trigger email |
| 5 | Check the change approval notification | Sent to the requester instead of the approver | Wrong person asked to approve |
| 6 | Look at the email reply action | Reply action is "Delete incident" | Replying to email deletes the incident record |

### Verification

For each notification: Who gets it? When? Does the content make sense? Would you know what to do after reading it?

---

## Lab 3: Fix the ServiceNow Instance Configuration (6 bugs)

**File:** `starter-code/instance-config.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the admin password | Password is "admin123" | Trivial password, security risk |
| 2 | Look at the ACL setting | ACLs are disabled ("acl_enabled: false") | No access control; everyone can see everything |
| 3 | Check the session timeout | Session timeout is 0 (never expires) | Abandoned sessions stay active forever |
| 4 | Look at the update set name | Working in "Default" update set | Changes not tracked, cannot promote to production |
| 5 | Check the CMDB auto-discovery | Auto-discovery is pointed at wrong IP range | Discovering devices in wrong network |
| 6 | Look at the integration credentials | API credentials stored in plain text | Credentials exposed in configuration file |

### Verification

Would a security audit pass this configuration? Check each setting against ServiceNow best practices.

---

## Lab 4: ITSM MCQ Practice (Sample Questions)

Answer these sample questions to prepare for the assessment:

### Sample Questions

**Q1:** An incident is defined as:
- a) A planned change to a service
- b) An unplanned interruption to a service or reduction in quality
- c) A request for information
- d) A root cause of multiple events

**Q2:** In the priority matrix, Impact=High and Urgency=Medium results in:
- a) P1
- b) P2
- c) P3
- d) P4

**Q3:** Which ServiceNow table is the base table for incidents, problems, and changes?
- a) sys_user
- b) cmdb_ci
- c) task
- d) sys_audit

**Q4:** What is the purpose of an Update Set in ServiceNow?
- a) Update the ServiceNow version
- b) Track and move configuration changes between instances
- c) Set up automatic updates for users
- d) Update SLA definitions

**Q5:** In ITIL 4, which guiding principle says "Don't build something new if you can use what exists"?
- a) Focus on value
- b) Start where you are
- c) Keep it simple and practical
- d) Progress iteratively with feedback

**Answers:** Q1: b, Q2: b, Q3: c, Q4: b, Q5: b

---

## Lab 5: Role Play Preparation

### Prepare for the ITSM Role Play by reviewing these materials:

**Round 1 Preparation: Major Incident**
1. Review the incident priority matrix
2. Know your escalation contacts and timeframes
3. Prepare a stakeholder communication template
4. Review the FoodExpress architecture diagram (which services depend on what)

**Round 2 Preparation: Change + Problem**
1. Review the 7 Rs of Change Management
2. Prepare a change request template
3. Know the CAB approval criteria
4. Review risk assessment format

### Role Play Evaluation Criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| Process Adherence | 30% | Did you follow ITIL incident/change process? |
| Communication | 25% | Clear, timely updates to stakeholders? |
| Technical Accuracy | 20% | Correct diagnosis and resolution approach? |
| Teamwork | 15% | Effective collaboration within the team? |
| Time Management | 10% | Actions taken within SLA timeframes? |

---

## Lab Submission

| # | Item | Done? |
|---|------|-------|
| 1 | All 7 SLA policy bugs fixed | [ ] |
| 2 | All 6 email notification bugs fixed | [ ] |
| 3 | All 6 instance configuration bugs fixed | [ ] |
| 4 | MCQ practice questions reviewed | [ ] |
| 5 | Role play preparation materials reviewed | [ ] |
