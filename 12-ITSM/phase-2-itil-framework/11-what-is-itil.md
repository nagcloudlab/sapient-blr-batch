# Section 11: What is ITIL?

## Definition

**ITIL** = Information Technology Infrastructure Library -- a **globally accepted framework** of best practices for ITSM.

Think of it as: **"ITSM tells you WHAT to do. ITIL tells you HOW to do it well."**

---

## ITSM vs ITIL -- What's the Difference?

| | ITSM | ITIL |
|---|---|---|
| **What** | The discipline/practice | The framework/guidebook |
| **Analogy** | "Cooking" | "A recipe book" |
| **Scope** | Managing IT services | Best practices for managing IT services |
| **Owned by** | No one -- it's a concept | Axelos / PeopleCert |
| **Versions** | N/A | ITIL v1, v2, v3, **ITIL 4** (current) |

You can do ITSM without ITIL, but it's like cooking without recipes -- possible, but inconsistent.

---

## ITIL Evolution

```
ITIL v1 (1989)    40+ books, government IT (UK)
     |
ITIL v2 (2001)    Simplified to processes (Incident, Change, Problem...)
     |
ITIL v3 (2007)    Service Lifecycle: Strategy -> Design -> Transition -> Operation -> CSI
     |
ITIL 4 (2019)     Modern: Value co-creation, Agile/DevOps friendly, flexible
```

**We focus on ITIL 4** -- it's current and aligns with Agile/DevOps/SRE practices you've already learned.

---

## ITIL v3 vs ITIL 4: The Shift

| ITIL v3 | ITIL 4 |
|---|---|
| **Lifecycle** (linear stages) | **Value System** (flexible, interconnected) |
| 26 Processes | 34 Practices |
| Waterfall-friendly | Agile/DevOps-friendly |
| Prescriptive ("do it this way") | Adaptive ("adopt what works") |
| Service provider delivers TO consumer | Value **co-created** WITH consumer |

### UPI Example of the Shift

```
ITIL v3 thinking:
  "NPCI delivers UPI service TO banks. Banks are passive consumers."

ITIL 4 thinking:
  "NPCI and banks CO-CREATE value. Banks provide APIs, feedback,
   transaction data. Both sides contribute to making UPI work."
```

PhonePe doesn't just "consume" UPI -- they build features on top, report bugs, suggest improvements. That's **co-creation**.

---

## ITIL 4 Big Picture (Preview)

ITIL 4 has three core components:

```
+------------------------------------------------------------------+
|                    ITIL 4 Framework                                |
|                                                                    |
|  1. Guiding Principles (Sec 12)                                   |
|     "How should we think and behave?"                              |
|                                                                    |
|  2. Service Value System (Sec 13)                                  |
|     "How does value flow through the organization?"                |
|                                                                    |
|  3. Practices (Sec 15-16)                                          |
|     "What specific activities do we perform?"                      |
|     (This is where Incident, Change, Problem etc. live)           |
+------------------------------------------------------------------+
```

**Everything from Phase 1 (Sections 1-10) maps into ITIL 4 Practices.** ITIL 4 just adds structure, principles, and a value system around them.

---

## Other Frameworks (For Context)

ITIL is not the only framework. Others you may encounter:

| Framework | Focus | Used by |
|---|---|---|
| **ITIL 4** | Comprehensive IT service management | Most enterprises globally |
| **COBIT** | IT governance and compliance | Finance, audit-heavy orgs |
| **ISO 20000** | Certifiable ITSM standard | Orgs needing formal certification |
| **MOF** | Microsoft Operations Framework | Microsoft-centric shops |
| **DevOps/SRE** | Speed + reliability | Tech-forward companies |

ITIL 4 explicitly embraces DevOps and SRE -- they're complementary, not competing.

---

## Key Takeaway

> ITIL is not a standard you "comply with" -- it's a **library of best practices you adopt and adapt**.
>
> You don't implement ALL of ITIL. You pick what makes sense for your organization and maturity level.
> NPCI doesn't follow ITIL because they have to -- they follow it because at 14B+ transactions/month, they can't afford chaos.
