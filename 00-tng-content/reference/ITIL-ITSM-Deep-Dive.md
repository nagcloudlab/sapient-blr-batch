# ITIL and ITSM Deep Dive
## FoodExpress Reference Guide

**Audience:** Sustain Engineering trainees
**Programme:** Publicis Sapient Sustain Eng, Bangalore 2026
**Keep this document** -- it is a reference you will return to throughout your career.

---

## The Big Picture

```
Business Need
    |
    v
ITSM (IT Service Management)
    -- the DISCIPLINE: manage IT as a service to the business
    -- answers: HOW do we deliver and support IT services?
    |
    v
ITIL (IT Infrastructure Library)
    -- the FRAMEWORK: best practice guidance for ITSM
    -- answers: WHAT practices should we follow?
    |
    v
ServiceNow
    -- the TOOL: software platform that implements ITIL practices
    -- answers: WHERE do we record, track, and automate those practices?
```

For FoodExpress, this means:

- **Business need:** Customers can place and track food orders 24x7 reliably.
- **ITSM discipline:** The sustain engineering team manages Order, Payment, Restaurant, and
  Delivery services as products with defined quality levels.
- **ITIL practices:** Incident Management, Problem Management, Change Management, and Service
  Level Management govern how the team responds to and improves those services.
- **ServiceNow:** All incidents, problems, and changes are recorded and tracked in ServiceNow,
  giving the client a single system of record.

---

## A Real Incident: FoodExpress Payment Service Goes Down

Walk through this scenario end-to-end to see all ITIL practices in action.

### The scenario

```
2:17 AM IST, Monday 27 July 2026

Grafana fires an alert: PaymentService HTTP 5xx error rate > 5% for 2 minutes.
Simultaneously, the on-call phone rings. A monitoring bot posts in #alerts Slack:
  "[P1 AUTO] PaymentService: error rate 38% | orders failing | threshold 5%"
```

---

## ITIL Practice 1: Incident Management

An **incident** is an unplanned interruption to a service or reduction in service quality.
The goal of Incident Management is to restore normal service as quickly as possible.

### Phase 1: Detection

Sources that detect incidents for FoodExpress:
- Grafana / Prometheus alert rules (automated)
- Customer complaints via support tickets
- Restaurant partner calls to helpdesk
- On-call engineer noticing something in dashboards
- Synthetic monitoring (a bot places a test order every 5 minutes)

At 2:17 AM, Grafana detected the PaymentService issue automatically.

### Phase 2: Logging and Classification

The on-call engineer opens ServiceNow and creates an Incident record:

```
Incident Number : INC0042187
Title           : PaymentService -- elevated 5xx error rate, orders failing
Detected        : 2026-07-27 02:17 IST
Reported by     : Grafana automated alert
Service         : FoodExpress Payment Service
Environment     : Production
Initial Priority: P1 (pending confirmation of scope)
Assigned to     : Sustain Engineering On-Call Team
Status          : New -> In Progress
```

### Priority Matrix

| Priority | Criteria | Response Target | Resolution Target |
|---|---|---|---|
| P1 Critical | All customers affected OR revenue loss occurring OR data breach | 15 minutes | 4 hours |
| P2 High | Significant subset of customers affected OR major feature down | 30 minutes | 8 hours |
| P3 Medium | Minor feature broken OR workaround available OR small user group | 2 hours | 24 hours |
| P4 Low | Cosmetic issue OR enhancement request OR single user affected | 8 hours | 72 hours |

**FoodExpress P1 examples:**
- Order Service completely down (no orders can be placed)
- Payment Service returning 5xx for all payment methods
- Database unreachable
- Production data corruption

**FoodExpress P2 examples:**
- UPI payments failing but card payments working
- Restaurant dashboard down (restaurants cannot update menus)
- Order tracking not updating for customers in one city

**FoodExpress P3 examples:**
- PDF invoice generation failing (workaround: email summary)
- Search results slow (> 3s) for a specific cuisine filter
- Discount code not applying for a specific promo type

**FoodExpress P4 examples:**
- Minor UI misalignment on the restaurant profile page
- A typo in the order confirmation email template
- Enhancement: add a "reorder" button on order history

### Phase 3: Initial Diagnosis and Assignment

The on-call engineer follows the runbook:

```
Step 1: Check Grafana PaymentService dashboard
  -> Error rate: 38%  Latency P99: 14,200ms  (normal: <200ms)

Step 2: Check Kubernetes pod status
  -> kubectl get pods -n foodexpress-prod -l app=payment-service
  -> All 3 pods: Running  (not crashlooping -- service is up but sick)

Step 3: Check application logs
  -> kubectl logs -n foodexpress-prod payment-service-abc123 --tail=100
  -> Heap used: 1.98GB / 2.00GB  (99% memory)
  -> "JavaScript heap out of memory" errors starting at 02:14

Step 4: Root cause hypothesis: memory leak causing GC pressure and slow responses
Step 5: Escalate to Payment Service team lead (wakes up second engineer)
```

Incident is updated in ServiceNow:
```
Priority confirmed: P1
Category: Application -- Memory / Performance
Assigned team: Payment Service Sustain Squad
Bridge call opened: Zoom link posted in #inc-0042187 Slack channel
```

### Phase 4: Investigation and Diagnosis

Two engineers on the bridge call:

- Engineer A: captures heap dump before restart (`kill -USR2 <pid>` on Node.js)
- Engineer B: prepares to do a rolling restart of pods to restore service

Timeline:
```
02:17 - Alert fires, on-call engineer paged
02:22 - Bridge call started, P1 confirmed
02:28 - Root cause hypothesis: unbounded retryQueue array (memory leak)
02:31 - Heap dump captured for post-incident analysis
02:33 - Rolling restart initiated (kubectl rollout restart deployment/payment-service)
02:37 - All pods restarted, error rate drops to 0%
02:40 - Monitoring for 5 minutes to confirm stability
02:45 - Service confirmed stable, P1 downgraded to monitoring
```

### Phase 5: Resolution and Recovery

```
Resolution: Rolling restart of PaymentService pods cleared in-memory state.
Workaround applied: retryQueue processing temporarily disabled via feature flag.
Orders that failed during the window: 847 orders -- reprocessed from dead letter queue.
Customer communications: Stakeholder email sent at 03:00.
```

ServiceNow updated:
```
Status: Resolved
Resolution code: Service restart / workaround applied
Resolution notes: Memory leak in retry handler. Permanent fix tracked as Problem PRB0008821.
Resolved at: 02:45 IST
Total duration: 28 minutes
```

### Phase 6: Closure

After 24 hours with no recurrence:
```
Status: Closed
Post-mortem scheduled: 2026-07-29 10:00 IST
Problem record created: PRB0008821
Action items: 5 items logged, owners assigned
```

---

## ITIL Practice 2: Problem Management

A **problem** is the underlying cause of one or more incidents. Problem Management aims to
prevent incidents by finding and eliminating root causes.

### Reactive Problem Management

After the PaymentService incident, a Problem record is created:

```
Problem Number  : PRB0008821
Title           : PaymentService memory leak in retry handler
Related Incidents: INC0042187 (and 3 previous incidents over 6 weeks)
Root Cause      : retryQueue array grows unbounded -- no eviction or size cap
Known Error     : Yes -- root cause identified, fix not yet deployed
Workaround      : Disable retry queue processing via feature flag PAYMENT_RETRY_ENABLED=false
Fix plan        : Add MAX_RETRY_QUEUE_SIZE=1000 with LRU eviction, add heap monitoring alert
Fix owner       : Payment Service dev team
Target fix date : 2026-08-03
```

A **Known Error** is a problem with a documented root cause AND a workaround. Known errors are
stored in the Known Error Database (KEDB) so future incidents can be resolved faster.

### Proactive Problem Management: 5 Whys

Another recurring issue: "Order Service crashes every Monday morning around 9 AM."

Apply the 5 Whys technique to find the root cause:

```
Symptom: Order Service pods crash every Monday between 09:00 and 09:30 IST

Why 1: The pods run out of memory and are OOMKilled by Kubernetes.
Why 2: Memory usage spikes to 4GB (limit) every Monday morning.
Why 3: A weekly batch job runs at 09:00 that loads the full restaurant catalogue into memory.
Why 4: The batch job was written to use in-memory processing rather than streaming/pagination.
Why 5: No memory budget review was done when the batch job was originally developed because
       the restaurant catalogue had only 200 entries. It now has 18,000 entries.

ROOT CAUSE: Batch job design does not scale with data volume growth.
FIX: Rewrite batch job to use cursor-based pagination (process 500 restaurants at a time).
IMMEDIATE WORKAROUND: Schedule batch job to run at 03:00 when traffic is low.
```

---

## ITIL Practice 3: Change Management

A **change** is the addition, modification, or removal of anything that could affect IT services.
Change Management controls the risk of changes causing new incidents.

### Three Change Types

**Standard Change**
- Pre-approved, low-risk, well-understood procedure
- No CAB (Change Advisory Board) approval needed
- Examples for FoodExpress:
  - Update restaurant banner image in CMS
  - Add a new city to the delivery zone configuration file
  - Rotate an expiring SSL certificate using the standard runbook
  - Increase pod replica count from 3 to 4 (within documented scaling range)

**Normal Change**
- Requires assessment, planning, and CAB approval
- Scheduled in advance with test and rollback plans
- Examples for FoodExpress:
  - Deploy new version of PaymentService with retry logic rewrite
  - Add a new database index to the orders collection (requires maintenance window)
  - Migrate MongoDB Atlas cluster to a new tier
  - Introduce a new microservice (DeliveryOptimizationService)

**Emergency Change**
- Urgently needed to resolve a P1/P2 incident or prevent one
- Streamlined approval (e-CAB or designated approver, not full board)
- Must be retroactively documented after the fact
- Examples for FoodExpress:
  - Deploy hotfix for SQL injection vulnerability found in production
  - Roll back PaymentService deployment that caused the memory leak incident
  - Apply OS security patch for a zero-day vulnerability on production nodes
  - Temporarily disable a feature flag to stop an ongoing outage

### Normal Change Lifecycle (FoodExpress example)

```
Change request submitted in ServiceNow:
  CHG0019443 -- PaymentService v2.4.1 -- Fix unbounded retryQueue (PRB0008821)

Fields required:
  - Description of change and business justification
  - Risk assessment (Low / Medium / High / Critical)
  - Impact assessment (which services/customers affected during change)
  - Test plan (what was tested in staging)
  - Rollback plan (how to revert if change causes issues)
  - Maintenance window: 2026-08-03 02:00-04:00 IST (low traffic window)
  - Approvers: Change Manager + Service Owner + On-call Lead

CAB review: 2026-08-01
Approval: Granted with condition -- rollback must be tested in staging first

Deployment:
  - 02:00: Change window opens, monitoring intensified
  - 02:05: Deploy v2.4.1 to 1 of 3 pods (canary)
  - 02:15: Error rate nominal, memory stable -- proceed
  - 02:20: Deploy to remaining 2 pods
  - 02:35: All pods stable, memory well within bounds
  - 02:40: Change window closes, CHG closed as Successful

Post-implementation review: Confirm PRB0008821 resolved after 1 week observation.
```

---

## ITIL Practice 4: Service Level Management

Service Level Management defines, agrees, monitors, and reports on service quality commitments.

### Key Terms

**SLA (Service Level Agreement):** Formal contract between the client and the service provider.
Breach has financial or contractual consequences.

**SLO (Service Level Objective):** Internal target the engineering team aims to meet or exceed.
Usually stricter than the SLA to give a safety margin.

**SLI (Service Level Indicator):** The actual measured metric (availability %, latency ms, etc.).

### FoodExpress Service Level Definitions

| Service | SLI Measured | SLO Target | SLA Commitment |
|---|---|---|---|
| Order Service | Availability (successful requests / total) | 99.95% | 99.9% |
| Order Service | P95 response latency | < 500ms | < 1000ms |
| Payment Service | Availability | 99.99% | 99.95% |
| Payment Service | P99 transaction latency | < 1000ms | < 2000ms |
| Restaurant Service | Availability | 99.9% | 99.5% |
| Delivery Tracking | WebSocket uptime | 99.9% | 99.5% |
| Overall Platform | End-to-end order success rate | 99.5% | 99.0% |

### SLA Breach Consequences (example)

```
If Payment Service availability drops below 99.95% in any calendar month:
  - Client receives a service credit of 10% of monthly fee
  - Root cause report due within 5 business days
  - Remediation plan due within 10 business days

Measurement: Calculated from Prometheus metrics, reviewed monthly.
Exclusions: Planned maintenance windows approved in advance, force majeure.
```

### Monthly SLA Reporting (what sustain engineers produce)

A monthly service report includes:
- Actual SLI values vs SLO targets vs SLA commitments
- List of incidents that caused SLA risk or breach
- Trend analysis (is availability improving or degrading?)
- Planned improvements for the next month

---

## Quick Reference Card

```
INCIDENT  = unplanned disruption       -> restore service FAST
PROBLEM   = root cause of incidents    -> eliminate permanently
CHANGE    = controlled modification    -> introduce safely
SLA/SLO   = quality commitments        -> measure and report honestly

P1 -> 15 min response, 4 hr resolution, wake everyone up
P2 -> 30 min response, 8 hr resolution, escalate if needed
P3 -> 2 hr response, 24 hr resolution, normal working hours
P4 -> 8 hr response, 72 hr resolution, queue it

Standard Change  -> pre-approved, no CAB needed
Normal Change    -> planned, CAB approved, scheduled window
Emergency Change -> now, e-CAB or designated approver, document later

Known Error      -> root cause known + workaround documented = KEDB entry
Post-Mortem      -> blameless, timeline + 5 Whys + action items
```

---

*Reference document for Publicis Sapient Sustain Engineering Training, Bangalore 2026.*
*Module 35 (ITSM/ITIL) and Module 36 (ServiceNow).*
