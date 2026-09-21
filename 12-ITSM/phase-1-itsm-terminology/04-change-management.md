# Section 4: Change Management

## What is a Change?

The **addition, modification, or removal** of anything that could affect IT services.

Goal: **Ensure changes are done in a controlled way -- minimizing risk, maximizing success.**

---

## UPI Example: The Root Cause from Section 3

Remember the root cause? **Axis Bank deployed a core banking upgrade without telling NPCI.** That uncontrolled change caused a P1 incident.

Change Management exists so this never happens again.

---

## Types of Changes

| Type | What | Approval | UPI Example |
|---|---|---|---|
| **Standard** | Pre-approved, low risk, routine | No CAB needed | Adding a new merchant to UPI |
| **Normal** | Planned, needs review | CAB approval | Upgrading NPCI's transaction engine to v4.2 |
| **Emergency** | Urgent fix for a live incident | Fast-track approval (post-review) | Hotfix for transactions failing at midnight |

---

## The Change Lifecycle

```
Request --> Assess --> Approve --> Plan --> Implement --> Review --> Close
```

### UPI Example: Upgrading Transaction Engine to v4.2

| Step | What happens |
|---|---|
| **Request** | Engineering team submits CHG-20260925-0008: "Upgrade txn engine v4.1 -> v4.2" |
| **Assess** | Risk: Medium. Impact: All 400+ banks. Downtime: 0 (rolling deployment) |
| **Approve** | Goes to CAB (Change Advisory Board) -- reviewed by Ops Lead, Architect, QA |
| **Plan** | Deploy window: Sunday 2 AM - 4 AM. Rollback plan: revert to v4.1 containers |
| **Implement** | Rolling deployment: 10% traffic -> 50% -> 100% over 90 minutes |
| **Review** | Post-Implementation Review: success rate stable at 99.4%, no errors |
| **Close** | CHG closed as successful |

---

## CAB (Change Advisory Board)

A group that **reviews and approves** non-standard changes.

| Role | Who at NPCI |
|---|---|
| CAB Chair | VP of Engineering |
| Members | Platform Lead, Security Lead, QA Lead, Ops Lead |
| Invitees (as needed) | Bank representatives (for high-impact changes) |

**CAB doesn't do the work** -- they evaluate risk and say yes/no/defer.

---

## The Rollback Plan

Every change MUST have a rollback plan. No exceptions.

```
Change: Upgrade transaction engine v4.1 --> v4.2

Rollback trigger:
  - Success rate drops below 98% within 30 min of deployment
  - Error rate exceeds 0.5%
  - Any P1 incident linked to this change

Rollback steps:
  1. Stop rolling deployment
  2. Route traffic back to v4.1 containers
  3. Verify success rate recovers to baseline
  4. Notify all PSPs (PhonePe, GPay, etc.)

Rollback time: < 10 minutes
```

---

## What Happens Without Change Management?

That's exactly what Axis Bank did in Section 3:

```
Without Change Management:
  Axis deploys upgrade --> NPCI not informed --> connection pool exhausted
  --> 2.8 crore users affected --> 19 min outage --> trust damaged

With Change Management:
  Axis submits change request --> NPCI reviews impact --> deploy window agreed
  --> monitoring in place --> rollback ready --> zero user impact
```

---

## Connection to Previous Sections

```
Problem Management finds root cause
        |
        +--> "We need to deploy a fix"
                    |
                    +--> Change Management (controlled deployment)
                              |
                              +--> If change causes issues --> new Incident
                              |
                              +--> If successful --> Problem closed
```

---

## Key Takeaway

> **80% of incidents are caused by changes.**
> Change Management doesn't slow you down -- it keeps you from breaking things.
> Every change needs: **risk assessment, approval, plan, rollback, and review.**
