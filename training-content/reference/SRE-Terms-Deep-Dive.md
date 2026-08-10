# SRE Terminology Deep Dive
## FoodExpress Reference Guide

**Audience:** Sustain Engineering trainees
**Programme:** Publicis Sapient Sustain Eng, Bangalore 2026

---

## What is SRE?

**Google's definition (from the SRE Book, 2016):**
"SRE is what happens when a software engineer is tasked with what used to be called operations."

In practice, SRE applies software engineering principles -- automation, measurement, code -- to
infrastructure and operations problems. SREs write code to replace manual operational work.

### SRE vs Traditional Ops

| Dimension | Traditional Ops | SRE |
|---|---|---|
| Goal | Keep systems running, avoid change | Maintain reliability WHILE enabling change |
| Response to failure | Manual intervention, heroics | Alert, runbook, then automate the fix |
| Attitude to toil | Accepted as part of the job | Toil is debt; automate it away |
| Success metric | Uptime / "nothing broke" | Error budget consumed vs features shipped |
| On-call | Paged for everything | Paged only for real customer impact |
| Change | Change is risky, avoid it | Change is necessary; manage it with error budgets |

For FoodExpress, the SRE team is responsible for: reliability of Order, Payment, Restaurant, and
Delivery services; on-call rotations; building observability; and reducing toil through automation.

---

## Core SRE Terms

---

### SLI -- Service Level Indicator

An SLI is a **quantitative measure** of a service behaviour that matters to users.
It is a ratio: good events divided by total events, expressed as a percentage.

**Formula:**
```
SLI = (good events / total events) * 100
```

**FoodExpress SLI Table:**

| SLI Name | What it measures | Formula | PromQL query |
|---|---|---|---|
| Availability | Orders that succeed vs total attempts | successful_requests / total_requests | `sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))` |
| Latency | Fraction of requests faster than threshold | requests_under_500ms / total_requests | `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))` |
| Error rate | Fraction of requests that return 5xx | 1 - availability SLI | `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))` |
| Throughput | Orders processed per second | count(orders_created) per second | `rate(orders_created_total[1m])` |
| Correctness | Orders delivered to correct address | correct_deliveries / total_deliveries | Measured via delivery confirmation events |

---

### SLO -- Service Level Objective

An SLO is a **target value** for an SLI over a rolling time window (typically 28 or 30 days).
SLOs are internal engineering targets -- they define what "good" looks like.

**FoodExpress SLO examples:**

| Service | SLI | SLO Target | Window | Allowed downtime |
|---|---|---|---|---|
| Order Service | Availability | 99.9% | 30 days | 43.2 minutes/month |
| Order Service | P95 latency | < 500ms | 30 days | 0.1% of requests may exceed |
| Payment Service | Availability | 99.95% | 30 days | 21.6 minutes/month |
| Payment Service | P99 latency | < 1000ms | 30 days | 0.01% of requests may exceed |
| Restaurant Service | Availability | 99.9% | 30 days | 43.2 minutes/month |

**Allowed downtime calculation for 99.9% over 30 days:**
```
Total minutes in 30 days = 30 * 24 * 60 = 43,200 minutes
Allowed downtime = 43,200 * (1 - 0.999) = 43,200 * 0.001 = 43.2 minutes
```

---

### SLA -- Service Level Agreement

An SLA is a **formal contract** between the service provider (Publicis Sapient) and the client
(FoodExpress). It is based on SLOs but is looser, leaving a buffer for engineering reality.

```
SLO >= SLA  (always set the internal target higher than the contractual commitment)

Example:
  SLO: 99.95% availability (engineering target -- what we aim for)
  SLA: 99.9%  availability (what we legally commit to -- the floor)

If SLO is breached, the engineering team is concerned and investigates.
If SLA is breached, the client may receive service credits and will demand a root cause report.
```

---

### Error Budget

The error budget is the **allowed amount of unreliability** within an SLO window.
It is what makes SRE different from pure uptime maximization.

**Formula:**
```
Error Budget = 1 - SLO target
```

**FoodExpress Order Service example (SLO = 99.9%, 30-day window):**

```
Error Budget = 100% - 99.9% = 0.1%
In time: 43,200 minutes * 0.001 = 43.2 minutes of downtime allowed per month

Current usage (mid-month):
  - INC0042187 (PaymentService cascade): 28 minutes
  - INC0042190 (Config deploy rollback): 8 minutes
  - Total consumed: 36 minutes

Remaining budget: 43.2 - 36 = 7.2 minutes

Error budget remaining: 7.2 / 43.2 = 16.7%
```

**Error Budget Policy:**
- Budget > 50% remaining: Normal velocity. New features can be deployed freely.
- Budget 10-50% remaining: Caution. Risky changes require additional review.
- Budget < 10% remaining: Feature freeze. Only reliability work and bug fixes.
- Budget exhausted: No new deployments until next measurement window. SRE team focuses
  exclusively on reliability improvements.

**Burn Rate:**
```
Burn Rate = how fast the error budget is being consumed vs the expected rate

Expected rate: consume 1 month of budget in 1 month (burn rate = 1.0)
Burn rate > 1: consuming budget faster than it is being replenished
Burn rate of 14.4: consuming in 2 hours what should last 30 days (P1 alert threshold)
```

---

### Toil

Toil is **manual, repetitive, operational work** that is triggered by running a production
service, that does not provide permanent value, and that scales linearly with service growth.

**The key test for toil:** If you automate it, will it go away? If yes, it is toil.

**FoodExpress toil examples:**

| Toil Task | Frequency | Time per occurrence | Automatable? |
|---|---|---|---|
| Manual restart of Order Service pods when memory climbs | Every Monday | 15 minutes | Yes -- auto-restart on memory threshold |
| Manually reprocessing failed orders from dead letter queue | 3x per week | 30 minutes | Yes -- automated DLQ consumer |
| Manually deploying config changes by SSH to servers | Per change | 45 minutes | Yes -- Ansible / Helm values |
| Manual log review to find errors after each deploy | Per deploy | 20 minutes | Yes -- Grafana alert rules |
| Manually sending "order stuck" reports to restaurants | Daily | 60 minutes | Yes -- automated notification job |
| Reviewing on-call tickets that fired but resolved themselves | Weekly | 30 minutes | Partial -- alert tuning |

**SRE target:** Keep toil below 50% of the team's working time. The other 50% must go to
engineering work that reduces future toil (automation, tooling, reliability improvements).

---

### Post-Mortem (Blameless)

A post-mortem is a structured retrospective written after an incident, focused on learning and
systemic improvement, not on assigning fault to individuals.

**Core principle:** Systems fail, not people. When an engineer made a mistake, ask why the
system allowed that mistake to cause an outage.

**Standard FoodExpress post-mortem template:**

```
INCIDENT POST-MORTEM
--------------------
Incident ID      : INC0042187
Title            : PaymentService memory leak -- 28-minute P1 outage
Date             : 2026-07-27
Duration         : 28 minutes (02:17 to 02:45 IST)
Author           : [on-call lead name]
Review date      : 2026-07-29

IMPACT
  - 847 orders failed during the window
  - Estimated revenue impact: [calculate]
  - Customer-facing error rate: 38% of payment attempts

TIMELINE
  02:14  Memory leak began causing GC pressure (not yet alerting)
  02:17  Grafana alert fires: error rate > 5%
  02:22  Bridge call opened, P1 confirmed
  02:28  Root cause identified: retryQueue unbounded growth
  02:31  Heap dump captured
  02:33  Rolling restart initiated
  02:37  Service restored, error rate 0%
  02:45  Monitoring confirmed stable, P1 closed

ROOT CAUSE
  The retry handler in PaymentService appended the full request payload to an in-memory
  retryQueue array on each failed transaction. No size cap or eviction policy existed.
  After 3 hours of elevated error rate, the Node.js heap (2GB limit) was exhausted.

5 WHYS
  1. Why did the service crash? Heap exhausted.
  2. Why did the heap exhaust? retryQueue grew to 1.98GB.
  3. Why did it grow so large? No eviction policy -- array only appended, never trimmed.
  4. Why was there no eviction policy? The original developer did not anticipate high error rates.
  5. Why was this not caught? No memory profiling in CI and no heap size alert existed.

WHAT WENT WELL
  - Automated alerting detected the issue quickly (3-minute lag from first error)
  - Runbook for pod restart was clear and followed correctly
  - Heap dump was captured before restart, enabling root cause analysis

WHAT WENT WRONG
  - No alert for heap usage > 80% (gap in observability)
  - retryQueue had no size guard (code review gap)
  - No memory load test in the CI pipeline

ACTION ITEMS
  1. Add heap usage alert: memory > 80% for 5 minutes -> PagerDuty P2  [Owner] [Due 2026-08-03]
  2. Fix retryQueue: add MAX_SIZE=1000, evict oldest on overflow                [Due 2026-08-03]
  3. Add memory profiling step to CI pipeline using Node.js --max-old-space-size  [Due 2026-08-10]
  4. Add retryQueue size to Grafana dashboard                                    [Due 2026-08-03]
  5. Review all other services for similar unbounded array patterns             [Due 2026-08-17]
```

---

### The Four Golden Signals

Google SRE defines four signals that, if monitored, provide a complete picture of service health.

| Signal | What it measures | FoodExpress example metric |
|---|---|---|
| Latency | Time to serve a request (distinguish success vs error latency) | P95 order creation response time |
| Traffic | Demand on the system | Orders per second, API requests per minute |
| Errors | Rate of failed requests (explicit 5xx, implicit wrong data) | HTTP 5xx rate, failed payment rate |
| Saturation | How "full" the service is (CPU, memory, queue depth, pool size) | DB connection pool usage %, heap % |

**FoodExpress Grafana dashboard panels (one per signal):**

```
Panel 1 -- Latency
  Metric: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{service="order-service"}[5m]))
  Alert: P95 > 500ms for 2 minutes

Panel 2 -- Traffic
  Metric: sum(rate(http_requests_total{service="order-service"}[1m]))
  Use: detect traffic spikes (lunch peak, dinner peak, flash sales)

Panel 3 -- Errors
  Metric: sum(rate(http_requests_total{service="order-service",status=~"5.."}[5m])) /
          sum(rate(http_requests_total{service="order-service"}[5m]))
  Alert: error rate > 1% for 2 minutes (warning), > 5% for 1 minute (critical/P1)

Panel 4 -- Saturation
  Metric: mongodb_connection_pool_active / mongodb_connection_pool_max
  Alert: pool usage > 90% for 2 minutes
```

---

## Quick Reference

```
SLI  = the measurement  (what did we actually achieve?)
SLO  = the target       (what are we aiming for internally?)
SLA  = the contract     (what did we promise the client?)
Error Budget = 1 - SLO  (how much unreliability is allowed?)

SLO >= SLA  -- always keep internal target stricter than contractual commitment
Toil < 50% of team time -- the rest must be engineering work
Blameless postmortem -- systems fail, not people; find the systemic fix

Golden Signals: Latency, Traffic, Errors, Saturation
```

---

*Reference document for Publicis Sapient Sustain Engineering Training, Bangalore 2026.*
*Module 31 (Observability) and Module 32 (SRE).*
