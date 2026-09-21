# Section 13: Service Value System (SVS)

## What is the SVS?

The complete picture of how an organization takes **demand** (opportunities and needs) and converts it into **value**.

Think of it as: **"The operating model for your entire IT organization -- from 'someone needs something' to 'value delivered'."**

---

## SVS Components

```
+------------------------------------------------------------------+
|                  Service Value System (SVS)                        |
|                                                                    |
|  INPUTS                                                  OUTPUT    |
|  (Opportunity/  +---------------------------------+     (Value)   |
|   Demand)       |                                 |               |
|      ---------->|   Service Value Chain (Sec 14)  |----------->   |
|                 |                                 |               |
|                 +---------------------------------+               |
|                          |          |                              |
|                 Governed by:        Enabled by:                    |
|                 - Governance        - Guiding Principles (Sec 12) |
|                 - Practices (Sec 15)                              |
|                 - Continual Improvement (Sec 10)                  |
+------------------------------------------------------------------+
```

---

## 1. Opportunity / Demand (Input)

Every action in ITSM starts with either:

| Input | Meaning | UPI Example |
|---|---|---|
| **Opportunity** | A chance to add value or improve | "RBI wants UPI to support international payments" |
| **Demand** | A need from a consumer | "HDFC Bank reports transactions timing out" |

```
Opportunity --> proactive work (new features, improvements)
Demand      --> reactive work (incidents, requests, fixes)
```

---

## 2. Value (Output)

The end result -- perceived by the **consumer**, not the provider.

```
NPCI thinks: "We processed 14 billion transactions this month"
Bank thinks: "Our customers could pay seamlessly -- that's value"
End user thinks: "I sent money in 2 seconds -- that's value"
```

Value is **not** what you produce. It's what the **consumer perceives as beneficial**.

---

## 3. Guiding Principles

The 7 principles (Section 12) apply to **everything** in the SVS. They're the guardrails.

---

## 4. Governance

**Who makes decisions? How are they made? Who is accountable?**

| Governance Question | UPI Example |
|---|---|
| Who approves major changes? | CAB chaired by VP Engineering |
| Who sets SLA targets? | NPCI board + RBI regulatory requirements |
| Who owns each service? | Service owners defined for every IT service |
| How are risks managed? | Risk register reviewed quarterly |
| How is compliance ensured? | RBI audit requirements, PCI-DSS for payments |

Governance ensures the SVS doesn't run wild -- it operates within **policies, rules, and accountability structures**.

---

## 5. Service Value Chain

The core engine. Six activities that transform demand into value. Covered in detail in **Section 14**.

---

## 6. Practices

The 34 ITIL practices -- Incident Management, Change Management, etc. -- are **resources** that the Value Chain activities draw upon. Covered in **Sections 15-16**.

---

## 7. Continual Improvement

Applies to **the entire SVS** -- not just services, but governance, practices, and the value chain itself. Already covered in **Section 10**.

---

## How SVS Works -- End to End UPI Example

### Scenario

```
DEMAND: "PhonePe reports UPI Lite (small payments under Rs.500)
         has 15% failure rate -- needs to be below 2%"
```

### Step 1: Demand enters the SVS

```
Input: Demand from PhonePe (service consumer)
Type: Service degradation -- needs improvement
```

### Step 2: Governance checks

```
- Is this within our SLA? No -- SLA says 99.5%, we're at 85%
- Priority: HIGH -- regulatory risk (RBI monitors UPI Lite adoption)
- Budget: Approved from reliability improvement fund
- Owner: Platform Engineering team
```

### Step 3: Guiding Principles applied

```
- Focus on value: PhonePe users need fast small payments
- Start where you are: UPI Lite works -- just failing on 3 bank integrations
- Progress iteratively: Fix worst bank first, then next two
- Collaborate: Involve PhonePe, failing banks, and NPCI platform team
- Think holistically: UPI Lite shares infra with full UPI -- don't degrade full UPI
- Keep it simple: Don't redesign UPI Lite, fix the specific failure points
- Optimize and automate: Add circuit breakers, auto-retry
```

### Step 4: Service Value Chain processes the work

```
Plan -> Design -> Build -> Test -> Deploy -> Operate -> Monitor
(Details in Section 14)
```

### Step 5: Practices are used

```
- Incident Management: Track ongoing failures
- Problem Management: RCA on the 3 failing banks
- Change Management: Deploy fixes through CAB
- Service Level Management: Monitor SLI improvement
- Knowledge Management: Document new retry logic
```

### Step 6: Value delivered

```
OUTPUT: UPI Lite failure rate drops from 15% to 1.2%
VALUE perceived by:
  - PhonePe: "Our users can buy tea without failures"
  - Banks: "Fewer dispute tickets"
  - End users: "UPI Lite just works now"
  - RBI: "UPI Lite adoption target achievable"
```

### Step 7: Continual Improvement

```
- Log in CSI register: "Apply same circuit breaker pattern to full UPI"
- Update SLO: Tighten from 98% to 99.5% for UPI Lite
- Next PDCA cycle begins
```

---

## SVS vs the Old ITIL v3 Lifecycle

| ITIL v3 (Linear) | ITIL 4 SVS (Flexible) |
|---|---|
| Strategy -> Design -> Transition -> Operation -> CSI | All activities can happen in any order |
| Sequential phases | Interconnected, iterative |
| "First design, then build, then operate" | "Plan, engage, build, deliver -- as needed, in any sequence" |

```
ITIL v3:  Strategy --> Design --> Transition --> Operation --> CSI
          (waterfall-like, one direction)

ITIL 4:   Plan <--> Improve <--> Engage <--> Design <--> Obtain <--> Deliver
          (flexible, any path through the value chain)
```

---

## Connection to Previous Sections

```
SVS is the CONTAINER for everything we've learned:

  Guiding Principles (Sec 12) --> how we think
  Service Value Chain (Sec 14) --> how we work
  Practices (Sec 1-10, 15-16) --> what we do
  Governance --> who decides
  Continual Improvement (Sec 10) --> how we get better
```

---

## Key Takeaway

> The SVS is not a process -- it's the **operating model** for your IT organization.
>
> It answers: "When someone needs something from IT, what's the complete system that ensures value gets delivered -- reliably, governed, and always improving?"
