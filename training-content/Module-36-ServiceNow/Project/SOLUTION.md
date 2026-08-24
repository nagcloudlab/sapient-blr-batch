# ServiceNow -- Trainer Solutions & Hints
## Module 36 | Days 43-44

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix SLA Policies | Priority=1 (not 5), 4h duration, stop on Resolved/Closed, pause on Pending, 24x7 for P2, warnings at 50% and 75%, correct name | Students fix the priority but miss the pause condition. Pausing during "In Progress" means the timer stops while someone is actively working -- that defeats the purpose | Ask: "When should the SLA timer pause? When YOU are working, or when you're waiting for the CUSTOMER?" |
| 2 | Fix Email Notifications | Add subject line, use ${} syntax, add recipients, remove priority=5 filter, send approval to approver not requester, reply adds work notes | Students fix the variable syntax but miss the reply action. "Delete incident" on email reply would be catastrophic | Ask: "What happens if a VP replies 'thanks for the update' and it deletes the P1 incident record?" |
| 3 | Fix Instance Config | Strong password/SSO, enable ACLs, 30-min session timeout, named update set, correct IP range, vault references for secrets | Students change the password but leave it in the config file. Emphasize: credentials should NEVER be in config files | Ask: "If this YAML file is accidentally committed to Git, what credentials are now exposed?" |
| 4 | MCQ Assessment | Cover all three sections; common mistakes on incident vs request, change types, table inheritance | Students confuse Standard and Normal changes. Standard = pre-authorized template. Normal = needs CAB | Ask: "A routine monthly patching -- Standard or Normal change?" (Standard, if it's templated and pre-approved) |
| 5 | Role Play | Follow incident lifecycle; communicate clearly; document in real time; apply change process | Teams often skip the communication role -- they focus on fixing but forget to update stakeholders | Ask after: "How did the business stakeholder feel? Were they informed or left in the dark?" |

---

## Role Play Evaluation Notes

### Round 1: Major Incident

| Criteria | Excellent | Adequate | Needs Improvement |
|----------|-----------|----------|-------------------|
| Process | Followed incident lifecycle, correct priority, SLA tracked | Most steps followed, minor gaps | Skipped steps, no priority assignment |
| Communication | Regular updates every 15 min, status page updated, stakeholder informed | Some updates, stakeholder partially informed | No updates, stakeholder learned from outside |
| Technical | Correct diagnosis approach, used monitoring tools | Reasonable approach, some missteps | Random troubleshooting, no method |
| Teamwork | Clear role assignment, collaboration, no confusion | Roles somewhat clear, some overlap | Role confusion, duplication of effort |

### Round 2: Change + Problem

| Criteria | Excellent | Adequate | Needs Improvement |
|----------|-----------|----------|-------------------|
| Problem Record | Complete 5 Whys, workaround documented, permanent fix planned | Partial analysis, basic workaround | Superficial analysis, no workaround |
| Change Request | All 7 Rs answered, rollback plan, implementation steps with validation | Most fields complete, basic rollback | Incomplete, no rollback plan |
| CAB Presentation | Clear, confident, answered questions well | Adequate, struggled with some questions | Unprepared, could not answer CAB questions |

---

## Key Discussion Points

1. Why can't you work in the "Default" update set? (Changes are not tracked and cannot be promoted between instances)
2. What is the risk of storing API keys in config files? (Anyone with file access has system access; Git commits are permanent)
3. Why should SLA timers pause during "Pending" but not "In Progress"? (Pending = waiting for external input you can't control; In Progress = you are working)
4. Why is the reply action "Delete incident" dangerous? (Accidental deletion of active incident records; no recovery without audit)
5. How do you handle a journalist asking about an outage? (Communications Lead role; prepared statement; don't speculate on root cause publicly)
