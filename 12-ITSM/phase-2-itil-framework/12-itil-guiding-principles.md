# Section 12: ITIL 4 Guiding Principles

## What are Guiding Principles?

7 universal recommendations that guide an organization in **all circumstances**, regardless of changes in goals, strategies, or structure.

Think of it as: **"Before you make any ITSM decision, check it against these 7 rules."**

---

## The 7 Principles at a Glance

```
1. Focus on value
2. Start where you are
3. Progress iteratively with feedback
4. Collaborate and promote visibility
5. Think and work holistically
6. Keep it simple and practical
7. Optimize and automate
```

---

## Principle 1: Focus on Value

**Everything you do should map to value for someone.**

If you can't explain how an activity benefits the consumer, question why you're doing it.

| Without this principle | With this principle |
|---|---|
| "We generate 47 reports monthly" | "Which of these 47 reports does anyone actually read?" |
| "We have a 12-step change approval" | "Do all 12 steps reduce risk, or are 5 of them checkbox theater?" |

**UPI Example:**
NPCI's NOC team was sending daily uptime reports to all 400+ banks. Banks complained -- too much noise. Applying "focus on value": NPCI switched to **exception-based reporting** -- only notify when SLA is at risk. Banks happy, NOC team saved 2 hours/day.

---

## Principle 2: Start Where You Are

**Don't throw everything away and start from scratch.** Assess what you already have -- tools, processes, people -- and build on it.

| Without this principle | With this principle |
|---|---|
| "Our incident process is broken, let's buy ServiceNow and redesign everything" | "Let's first understand what works, what doesn't, then improve incrementally" |

**UPI Example:**
When NPCI wanted to improve their CMDB, the instinct was to buy a new tool and rebuild from scratch. Instead, they audited the existing spreadsheet-based asset list -- found it was 70% accurate. They imported that data into ServiceNow CMDB and then improved the remaining 30%. Saved 4 months.

---

## Principle 3: Progress Iteratively with Feedback

**Don't try to do everything at once.** Small steps, measure, get feedback, adjust.

This is **Agile thinking** applied to ITSM -- you already know this from your Agile module.

```
Big bang approach (risky):
  Plan for 6 months --> Build everything --> Launch --> Hope it works

Iterative approach (safe):
  Week 1: Implement incident logging --> feedback --> adjust
  Week 3: Add priority matrix --> feedback --> adjust
  Week 5: Add escalation rules --> feedback --> adjust
```

**UPI Example:**
NPCI didn't launch UPI with 400 banks on day 1. They started with **21 banks** in April 2016. Got feedback. Fixed issues. Scaled to 50, then 100, then 400+. Each iteration brought improvements -- **that's this principle in action.**

---

## Principle 4: Collaborate and Promote Visibility

**Break silos. Share information. Make work visible.**

| Silo behavior | Collaborative behavior |
|---|---|
| NOC fixes incident, doesn't tell dev team | Incident channel in Slack -- everyone sees status |
| Change deployed without telling ops | Change calendar visible to all teams |
| Problem RCA stays in one team's email | RCA published to knowledge base for all |

**UPI Example:**
When Axis Bank's change caused a P1 incident (Section 3), the root cause was **no visibility** -- Axis didn't tell NPCI about their deployment. Fix: NPCI created a **shared change calendar** where all banks register upcoming changes. Visibility prevents surprises.

---

## Principle 5: Think and Work Holistically

**No service, practice, or component stands alone.** Everything is connected -- understand the full picture.

```
Thinking in isolation:
  "Let's optimize the transaction engine for speed"
  (But this increases DB load, which slows settlement)

Thinking holistically:
  "If we speed up the transaction engine, what's the impact on
   DB, Kafka, settlement, and monitoring? Let's check CMDB dependencies."
```

**UPI Example:**
NPCI once upgraded their Kafka cluster for better throughput. Transaction engine got faster. But the settlement engine couldn't keep up with the increased event volume -- settlement started lagging. **They optimized one part without considering the whole system.** Holistic thinking: check the CMDB dependency map (Section 7) before any change.

---

## Principle 6: Keep It Simple and Practical

**If a process doesn't add value, eliminate it.** Use the minimum number of steps to achieve the objective.

| Over-engineered | Simple and practical |
|---|---|
| 5-level approval for a password reset | Auto-approved, self-service |
| 20-page RCA document for a P4 incident | 3-line summary in the ticket |
| Weekly 2-hour CAB meeting for all changes | CAB only for high-risk; standard changes pre-approved |

**UPI Example:**
NPCI initially required CAB approval for adding a new merchant to UPI -- a low-risk, routine task. It took 3 days. Applying this principle: they made merchant onboarding a **Standard Change** (pre-approved). Time reduced from 3 days to 2 hours.

---

## Principle 7: Optimize and Automate

**First optimize the process (remove waste), THEN automate it.** Don't automate a broken process -- you'll just get broken results faster.

```
Wrong order:
  Broken process --> Automate it --> Broken results, faster

Right order:
  Broken process --> Optimize (remove unnecessary steps) -->
  Streamlined process --> Automate --> Fast, correct results
```

**UPI Example:**

```
Before optimization:
  Incident detected --> NOC calls L1 --> L1 logs ticket --> L1 calls L2
  --> L2 investigates --> L2 calls L3 if needed
  (Total: 25 min average for P1)

After optimization:
  Remove: manual NOC call (replace with auto-alert)
  Remove: L1 logging (auto-create ticket from alert)
  Streamline: auto-escalate to L2 if not acknowledged in 3 min

After automation:
  Alert fires --> ticket auto-created --> L2 auto-paged -->
  runbook auto-suggested from KB
  (Total: 8 min average for P1)
```

---

## All 7 Together: One UPI Scenario

NPCI wants to improve their dispute resolution process:

| Principle | Applied as |
|---|---|
| **Focus on value** | "Banks care about resolution speed, not our internal process steps" |
| **Start where you are** | "Current process resolves 80% of disputes -- don't rebuild from scratch" |
| **Progress iteratively** | "First automate simple disputes (wrong amount), then complex ones (fraud)" |
| **Collaborate** | "Banks, PSPs, and NPCI ops team all need visibility into dispute status" |
| **Think holistically** | "Dispute resolution affects settlement, refunds, and bank reconciliation" |
| **Keep it simple** | "Remove the manual review step for disputes under Rs.500 -- auto-resolve" |
| **Optimize and automate** | "First streamline the 8-step process to 5 steps, then automate steps 1-3" |

---

## Key Takeaway

> These 7 principles are not theoretical -- they're **decision filters**.
>
> Before any ITSM initiative, ask:
> - Does this create value? (P1)
> - Are we building on what exists? (P2)
> - Are we doing this in small steps? (P3)
> - Is everyone who needs to know, informed? (P4)
> - Have we considered the full impact? (P5)
> - Is this the simplest way? (P6)
> - Can we optimize first, then automate? (P7)
