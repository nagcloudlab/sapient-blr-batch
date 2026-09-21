# Section 9: Knowledge Management

## What is Knowledge Management?

Capturing, organizing, and sharing knowledge so that **people don't solve the same problem twice**.

Think of it as: **"If the engineer who fixed it at 3 AM quits tomorrow, can someone else fix it next time?"**

---

## The Problem Without Knowledge Management

```
Monday 2 AM:
  Alert: Settlement engine stuck
  Ravi (senior engineer) fixes it in 10 min -- he's seen this before

Thursday 3 AM:
  Same alert. Ravi is on vacation.
  Priya spends 2 hours figuring it out from scratch.

Next month:
  Same alert. New joiner Amit has no idea. Calls 4 people at 4 AM.
  Takes 3 hours. SLA breached.
```

**The knowledge was in Ravi's head -- not in the system.**

---

## UPI Example: NPCI's Knowledge Base

### Knowledge Article Types

| Type | Purpose | UPI Example |
|---|---|---|
| **Runbook** | Step-by-step procedure for operations | "How to restart the settlement engine" |
| **Known Error Article** | Workaround for a known issue | "Axis Bank timeout -- switch to backup node" |
| **Troubleshooting Guide** | Decision tree for diagnosing issues | "Transaction failing? Check: PSP -> Gateway -> Bank -> DB" |
| **How-To** | Instructions for common requests | "How to onboard a new bank to UPI" |
| **FAQ** | Common questions answered | "What happens if settlement misses the 6 AM window?" |

### Sample Runbook

```
KB-0042: Restarting UPI Settlement Engine
=========================================
Last updated: Sep 15, 2026
Author: Platform Engineering
Related CIs: CI-1005 (Settlement Engine), CI-3012 (Oracle DB)

WHEN TO USE:
  - Settlement batch job stuck for > 30 min
  - Error: "BATCH_TIMEOUT_EXCEEDED" in logs

PRE-CHECKS:
  1. Confirm no active settlement in progress
     $ curl http://settlement-engine:8080/api/status
     Expected: {"state": "IDLE"} or {"state": "STUCK"}

  2. Verify DB connectivity
     $ psql -h settlement-db -c "SELECT 1"

STEPS:
  1. Drain in-flight requests
     $ kubectl scale deployment settlement-engine --replicas=0
     Wait 60 seconds

  2. Clear stuck batch
     $ curl -X POST http://settlement-engine:8080/api/batch/clear

  3. Restart
     $ kubectl scale deployment settlement-engine --replicas=3
     Wait for all pods READY

  4. Verify
     $ curl http://settlement-engine:8080/api/health
     Expected: {"status": "UP", "batchQueue": 0}

  5. Trigger missed settlement
     $ curl -X POST http://settlement-engine:8080/api/batch/run

ROLLBACK:
  If step 3 fails, escalate to L3 (DBA team) -- possible DB lock issue.

RELATED INCIDENTS:
  INC-20260801-0023, INC-20260815-0091, INC-20260902-0017
```

**This runbook turns a 2-hour struggle into a 10-minute procedure for anyone.**

---

## Knowledge Lifecycle

```
Create --> Review --> Publish --> Use --> Update --> Retire
```

| Stage | What happens | UPI Example |
|---|---|---|
| **Create** | Engineer writes article after resolving an incident | Ravi documents settlement restart steps |
| **Review** | Peer or lead validates accuracy | Tech lead verifies the commands work |
| **Publish** | Made available in knowledge base | Added to NPCI internal wiki |
| **Use** | L1/L2 follows it during next incident | Priya uses runbook at 3 AM -- fixes it in 10 min |
| **Update** | Article revised when service changes | Engine upgraded to v4.2 -- new health check endpoint |
| **Retire** | Article removed when no longer relevant | Old v3.x runbook archived |

---

## Knowledge-Centered Service (KCS)

A practice where **solving and documenting happen at the same time**:

```
Traditional:
  Fix incident --> close ticket --> maybe document later (usually never)

KCS:
  Fix incident --> document while fixing --> attach article to ticket --> close
```

| KCS Rule | Meaning |
|---|---|
| **Solve and document together** | Write the KB article AS you fix the issue |
| **Reuse before create** | Search KB first -- don't duplicate |
| **Improve what exists** | Found a KB article but it's outdated? Update it now |
| **Everyone contributes** | Not just seniors -- L1 engineers add articles too |

---

## How Knowledge Connects to Incidents

```
New Incident arrives
       |
       v
Search Knowledge Base
       |
  +----+----+
  |         |
Found     Not found
  |         |
  v         v
Follow    Investigate
runbook   manually
  |         |
  v         v
Resolved  Resolved
  |         |
  |         +--> CREATE new KB article
  |
  +--> Was article accurate?
         |          |
        Yes        No
         |          |
       Close     UPDATE article, then close
```

---

## Measuring Knowledge Management

| Metric | What it measures | Target |
|---|---|---|
| **KB usage rate** | % of incidents where KB article was used | > 50% |
| **First call resolution** | Solved at L1 using KB? | > 60% |
| **Article freshness** | % of articles reviewed in last 6 months | > 80% |
| **Time to resolve (KB vs no KB)** | Faster when KB exists? | KB incidents 3x faster |
| **Contribution rate** | New articles created per month | Every P1/P2 -> mandatory article |

---

## Connection to Previous Sections

```
Knowledge Management captures learnings from:
  |
  +-- Incident (Sec 2): Runbooks for recurring issues
  +-- Problem (Sec 3): RCA findings documented as Known Error articles
  +-- Change (Sec 4): Post-implementation reviews -> lessons learned
  +-- Service Request (Sec 5): How-to guides for common requests
  +-- CMDB (Sec 7): KB articles linked to specific CIs
  +-- SLA (Sec 8): KB usage improves MTTR -> protects SLA
```

---

## Key Takeaway

> Knowledge in one person's head is a **risk**. Knowledge in a shared system is an **asset**.
>
> The goal: **any L1 engineer at 3 AM should be able to resolve what your best L3 engineer solved last month** -- because it's documented, searchable, and current.
