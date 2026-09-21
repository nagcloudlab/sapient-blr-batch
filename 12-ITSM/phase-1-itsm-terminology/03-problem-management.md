# Section 3: Problem Management

## What is a Problem?

The **unknown root cause** of one or more incidents.

**Incident** = the symptom. **Problem** = the disease.

| | Incident | Problem |
|---|---|---|
| **Goal** | Restore service NOW | Prevent it from happening AGAIN |
| **Timeframe** | Minutes to hours | Days to weeks |
| **Question** | "How do we fix it?" | "Why did it happen?" |

---

## UPI Example: Continuing from Section 2

Remember? Axis Bank transactions failed at 12:03 PM. The **incident** was resolved in 19 minutes by routing traffic to a backup node.

But **why** did it fail? That's a **Problem**.

### Problem Record

| Field | Value |
|---|---|
| Problem ID | PRB-20260921-0012 |
| Related Incidents | INC-20260921-0047 (+ 3 similar from last month) |
| Affected Service | UPI Transaction Processing |
| Status | Under Investigation |

---

## Root Cause Analysis (RCA) -- 5 Whys

```
Why did transactions fail?
  --> Axis Bank PSP node stopped responding

Why did the node stop responding?
  --> Connection pool was exhausted (0 available connections)

Why was the pool exhausted?
  --> Axis Bank's core banking system started responding slowly (8s vs normal 200ms)

Why was it responding slowly?
  --> Axis deployed a core banking upgrade at 11:45 AM without informing NPCI

Why wasn't NPCI informed?
  --> No formal change notification process exists between Axis and NPCI
```

### Root Cause

**Axis Bank deployed a change without coordinating with NPCI. No inter-org change communication protocol exists.**

---

## Known Error

Once root cause is identified but a permanent fix isn't ready yet, it becomes a **Known Error**:

```
Problem --> (RCA done) --> Known Error --> (fix deployed) --> Closed
```

| Field | Value |
|---|---|
| Known Error ID | KE-20260921-0012 |
| Workaround | Route through backup node if Axis primary latency > 2s |
| Permanent Fix | Implement inter-org change notification API + auto-circuit-breaker |

---

## Two Flavors of Problem Management

| Type | Trigger | UPI Example |
|---|---|---|
| **Reactive** | After incidents happen | "Axis failed 3 times this month -- investigate" |
| **Proactive** | Before incidents happen | "SBI node latency trending up 5% weekly -- investigate before it breaks" |

---

## Connection to Previous Sections

```
[Incident Occurs] ---> Incident Management (restore service)
       |
       +---> Problem Management (find root cause)
                    |
                    +---> Known Error (workaround documented)
                    |
                    +---> Change Management (permanent fix) <-- next section
```

---

## Key Takeaway

> Incident = **put out the fire**
> Problem = **find out why fires keep starting in that building**
> Known Error = **we know why, here's the workaround until we fix it permanently**
