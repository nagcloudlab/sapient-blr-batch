# SRE Automation
## Module 33 | Sustain Engineering Training | Days 37-38

---

## Agenda -- Day 37

| # | Topic |
|---|-------|
| 01 | What is Site Reliability Engineering? |
| 02 | SLIs: Service Level Indicators |
| 03 | SLOs: Service Level Objectives |
| 04 | Error Budgets |
| 05 | Toil and Toil Reduction |
| 06 | Risk Quantification |
| 07 | Lab: Define SLOs & Error Budgets for FoodExpress |
| 08 | SRE vs DevOps vs Traditional Ops |
| 09 | Observability + SRE MCQ Review |
| 10 | Day 37 Wrap-up |

---

## Agenda -- Day 38

| # | Topic |
|---|-------|
| 01 | SRE Automation Tools & Practices |
| 02 | Learning from Failure |
| 03 | Anti-fragility: Chaos Engineering |
| 04 | Incident Response Framework |
| 05 | Blameless Post-Mortems |
| 06 | Lab: Write a Post-Mortem |
| 07 | Toil Assessment & Automation Prioritization |
| 08 | Observability + SRE MCQ Assessment |
| 09 | Module Recap & Discussion |
| 10 | Days 37-38 Wrap-up |

---

## What is Site Reliability Engineering?

### SRE = Software Engineering applied to Operations

> "SRE is what happens when you ask a software engineer to design an operations team." -- Ben Treynor, Google

```
Traditional Ops              SRE
─────────────                ─────
Manual processes     →       Automation
"Keep it running"    →       "Make it reliable AND fast to change"
Separate from dev    →       Shared ownership with dev
Avoid all change     →       Managed risk through error budgets
Heroics at 3 AM      →       Automated remediation
```

### Core SRE principles:
1. Embrace risk (don't aim for 100% uptime)
2. Eliminate toil through automation
3. Measure everything with SLIs/SLOs
4. Use error budgets to balance reliability vs velocity

---

## SRE vs DevOps vs Traditional Ops

| Aspect | Traditional Ops | DevOps | SRE |
|--------|----------------|--------|-----|
| **Focus** | Stability | Collaboration | Reliability |
| **Change** | Resist change | Embrace change | Managed risk |
| **Measurement** | Uptime (binary) | Deployment frequency | SLIs/SLOs |
| **Failure** | Blame someone | Blameless | Error budgets |
| **Automation** | Ad-hoc scripts | CI/CD pipeline | Eliminate toil |
| **Ownership** | Ops owns prod | Shared ownership | SRE + Dev teams |
| **Scaling** | Add more people | Add more tools | Automate away work |

DevOps is the philosophy. SRE is a concrete implementation.

---

## Service Level Indicators (SLIs)

### Quantitative measures of service health

```
SLI = A carefully chosen metric that represents
      the user experience of your service.
```

| SLI | Formula | FoodExpress Example |
|-----|---------|---------------------|
| **Availability** | Successful requests / Total requests | 99.9% of order API calls succeed |
| **Latency** | Requests below threshold / Total requests | 95% of orders placed in < 500ms |
| **Throughput** | Successful operations / Time period | 200 orders/minute during peak |
| **Error Rate** | Failed requests / Total requests | < 0.1% of payments fail |
| **Freshness** | Data age < threshold / Total queries | 99% of menu prices updated within 5 min |

### Good SLIs are:
- Measurable from the user's perspective
- Directly tied to user happiness
- Aggregatable and comparable over time

---

## SLI Specification for FoodExpress

### Order Service SLIs

```
SLI: Availability
  - Good events: HTTP responses with status < 500
  - Total events: All HTTP requests
  - Measurement: Prometheus counter http_requests_total

SLI: Latency
  - Good events: Requests completed in < 500ms
  - Total events: All HTTP requests
  - Measurement: Prometheus histogram http_request_duration_seconds

SLI: Correctness
  - Good events: Orders where items + prices match menu
  - Total events: All completed orders
  - Measurement: Business metric validation check
```

**Key:** SLIs are fractions: good events / total events, expressed as a percentage.

---

## Service Level Objectives (SLOs)

### Target values for SLIs

```
SLO = "We aim for this SLI to be at least X% over Y period"
```

| Service | SLI | SLO Target | Measurement Window |
|---------|-----|------------|-------------------|
| Order API | Availability | 99.9% | 30-day rolling |
| Order API | Latency (p99) | 99% < 500ms | 30-day rolling |
| Payment API | Availability | 99.95% | 30-day rolling |
| Menu API | Availability | 99.5% | 30-day rolling |
| Delivery Tracking | Freshness | 99% < 30s old | 30-day rolling |

### Why not 100%?
- 100% is impossible (physics, network, hardware)
- 100% prevents all changes (any deploy risks downtime)
- Users can't tell the difference between 99.99% and 100%
- The cost increases exponentially as you approach 100%

---

## The Reliability Pyramid

<!--VISUAL:sre-reliability-pyramid-->

```
                    ▲
                   ╱ ╲
                  ╱   ╲
                 ╱99.999╲     $$$$$  (5 nines = 5 min/year downtime)
                ╱─────────╲
               ╱  99.99%   ╲   $$$$  (4 nines = 52 min/year)
              ╱─────────────╲
             ╱    99.9%      ╲  $$$   (3 nines = 8.7 hrs/year)
            ╱─────────────────╲
           ╱      99%         ╲ $$    (2 nines = 3.65 days/year)
          ╱─────────────────────╲
         ╱        90%           ╲ $    (1 nine = 36.5 days/year)
        ╱─────────────────────────╲
```

| Target | Downtime/Year | Downtime/Month | FoodExpress Service |
|--------|---------------|----------------|---------------------|
| 99% | 3.65 days | 7.3 hours | Internal tools |
| 99.9% | 8.76 hours | 43.8 min | Menu service |
| 99.95% | 4.38 hours | 21.9 min | Payment service |
| 99.99% | 52.6 min | 4.38 min | (Not needed for FoodExpress) |

---

## Error Budgets

<!--VISUAL:sre-error-budget-->

### The bridge between reliability and velocity

```
Error Budget = 1 - SLO

If SLO = 99.9% availability:
  Error Budget = 0.1% = 43.8 minutes/month of downtime allowed

If SLO = 99.5%:
  Error Budget = 0.5% = 3.65 hours/month
```

### How error budgets work:

```
Month starts:  Error Budget = 43.8 minutes

Week 1: Deploy broke for 5 min     → Remaining: 38.8 min
Week 2: Payment gateway outage 10 min → Remaining: 28.8 min
Week 3: No incidents                → Remaining: 28.8 min
Week 4: Budget healthy              → Ship more features!

vs.

Week 1: Major outage 30 min        → Remaining: 13.8 min
Week 2: Another outage 10 min      → Remaining: 3.8 min  ⚠️
         FREEZE: No more deployments until budget replenishes
         Focus on: reliability improvements, testing, automation
```

---

## Error Budget Policy

### What happens when budget is consumed

```
┌────────────────────────────────────────────────────────┐
│              ERROR BUDGET POLICY                       │
│                                                         │
│  Budget > 50% remaining:                                │
│    ✓ Deploy freely                                     │
│    ✓ Run experiments                                   │
│    ✓ Take calculated risks                             │
│                                                         │
│  Budget 20-50% remaining:                               │
│    ⚠ Deploy with extra testing                         │
│    ⚠ No risky experiments                              │
│    ⚠ Review recent incidents                           │
│                                                         │
│  Budget < 20% remaining:                                │
│    ✗ Feature freeze                                    │
│    ✗ Focus on reliability improvements only            │
│    ✗ Post-mortem all recent incidents                  │
│                                                         │
│  Budget exhausted (0%):                                 │
│    ✗ Complete deployment freeze                        │
│    ✗ All hands on reliability                          │
│    ✗ Escalate to leadership                            │
└────────────────────────────────────────────────────────┘
```

---

## Toil

### Repetitive, manual, automatable work

> "Toil is the kind of work tied to running a production service that tends to be manual, repetitive, automatable, tactical, devoid of enduring value, and that scales linearly as a service grows." -- Google SRE Book

### Toil vs Non-Toil

| Toil (Automate This!) | Not Toil (Engineering Work) |
|------------------------|-----------------------------|
| Restarting a crashed service manually | Writing auto-restart logic |
| Manually scaling during peak hours | Configuring HPA |
| Running database migrations by hand | Building migration pipeline |
| Copying logs to investigate incidents | Setting up centralized logging |
| Manually rotating certificates | Automating cert renewal (cert-manager) |

### Google's SRE rule: **Spend no more than 50% of time on toil.** The other 50% should be engineering work that reduces future toil.

---

## Toil Assessment

### How to quantify toil

```
FoodExpress Toil Assessment:

Task: Manually restart crashed pods
  Frequency: 3x/week
  Duration: 15 min each
  Monthly cost: 3 hours
  Automatable? YES → Kubernetes liveness probes

Task: Manually scale during lunch rush
  Frequency: Daily
  Duration: 10 min
  Monthly cost: 3.5 hours
  Automatable? YES → HPA configuration

Task: Database backup verification
  Frequency: Daily
  Duration: 20 min
  Monthly cost: 7 hours
  Automatable? YES → Automated backup + verification script

Task: SSL certificate renewal
  Frequency: Quarterly
  Duration: 2 hours
  Monthly cost: 0.67 hours
  Automatable? YES → cert-manager

TOTAL TOIL: 14.17 hours/month → Target: < 5 hours/month
```

---

## Risk Quantification

### Measure risk in terms of impact and probability

```
Risk Score = Likelihood x Impact x Detection Difficulty

Scale: 1 (low) to 5 (high)
```

| Risk | Likelihood | Impact | Detection | Score | Mitigation |
|------|-----------|--------|-----------|-------|------------|
| Payment gateway outage | 3 | 5 | 2 | 30 | Circuit breaker, fallback queue |
| Database corruption | 1 | 5 | 3 | 15 | Automated backups, replication |
| DDoS attack | 2 | 4 | 2 | 16 | Rate limiting, CDN, WAF |
| Config drift | 4 | 3 | 4 | 48 | Ansible, GitOps, drift detection |
| Memory leak in order-service | 3 | 3 | 3 | 27 | Resource limits, memory profiling |

**Priority:** Address highest-score risks first. Config drift (48) > Payment outage (30) > Memory leak (27).

---

## SRE vs DevOps: Complementary Approaches

```
┌─────────────────────────────────────────────────┐
│                                                  │
│   DevOps (Culture & Philosophy)                 │
│   ┌──────────────────────────────────────────┐  │
│   │  - Break down silos                      │  │
│   │  - Automate everything                   │  │
│   │  - Continuous delivery                   │  │
│   │  - Shared ownership                      │  │
│   │                                          │  │
│   │   SRE (Concrete Implementation)          │  │
│   │   ┌──────────────────────────────────┐   │  │
│   │   │  - SLIs, SLOs, Error Budgets    │   │  │
│   │   │  - Toil reduction (< 50%)       │   │  │
│   │   │  - Blameless post-mortems       │   │  │
│   │   │  - Chaos engineering            │   │  │
│   │   │  - On-call rotations            │   │  │
│   │   └──────────────────────────────────┘   │  │
│   └──────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## SRE Automation Tools

### Automate repetitive reliability tasks

| Category | Tool | Purpose |
|----------|------|---------|
| **Infrastructure as Code** | Terraform, Pulumi | Provision cloud resources |
| **Configuration Management** | Ansible, Puppet | Consistent server config |
| **Container Orchestration** | Kubernetes | Automated deployment & scaling |
| **CI/CD** | Jenkins, GitHub Actions | Automated build & deploy |
| **Monitoring** | Prometheus, Grafana | Metrics & alerting |
| **Incident Management** | PagerDuty, OpsGenie | On-call rotation & escalation |
| **Chaos Engineering** | Chaos Monkey, Litmus | Test failure resilience |
| **Runbook Automation** | Rundeck, StackStorm | Automated incident response |

---

## Learning from Failure

### Failure is inevitable; learning is optional

```
FoodExpress Incident Timeline:
─────────────────────────────

14:23  Alert: Error rate > 5% on order-service
14:25  On-call engineer acknowledges
14:28  Investigation: payment-service returning 500s
14:35  Root cause: database connection pool exhausted
14:38  Mitigation: increase pool size, restart payment pods
14:42  Service restored
14:45  Monitoring confirms error rate < 0.1%

Total impact: 19 minutes downtime
Error budget consumed: 19 / 43.8 = 43%

What did we learn?
  1. Connection pool had no monitoring
  2. No auto-scaling for DB connections
  3. Alert fired 2 min after users were affected
```

---

## Anti-fragility & Chaos Engineering

### Systems that get stronger under stress

```
FRAGILE          ROBUST           ANTI-FRAGILE
─────────        ──────           ────────────
Breaks under     Survives         Gets STRONGER
stress           stress           under stress

Glass            Rock             Muscle
Manual ops       Redundancy       Chaos engineering
No testing       Disaster drills  Game days
```

### Chaos Engineering Principles:
1. **Define steady state** (normal metrics)
2. **Hypothesize** that steady state will continue during experiment
3. **Introduce failure** (kill pods, add latency, corrupt data)
4. **Observe** if hypothesis holds
5. **Learn** and improve

### Tools: Chaos Monkey, Litmus Chaos, Gremlin

---

## Chaos Engineering: FoodExpress Examples

| Experiment | What | Hypothesis | Outcome |
|-----------|------|------------|---------|
| Kill order-service pod | `kubectl delete pod order-service-xyz` | K8s recreates pod; traffic routes to other replicas; no user impact | Validated: pod recreated in 8s, no errors |
| Add 500ms latency to payment | Inject network delay | Circuit breaker activates; orders queued; no timeouts | Found bug: circuit breaker threshold too high |
| MySQL failover | Kill primary database | Replica promotes automatically; < 30s downtime | Discovered: app didn't reconnect automatically |
| DNS failure | Block DNS for 5 min | Services use cached connections; degrade gracefully | Found: no DNS caching, all services failed |

---

## Incident Response Framework

### Structured approach to handling incidents

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  DETECT  │───>│ RESPOND  │───>│ MITIGATE │───>│  LEARN   │
│          │    │          │    │          │    │          │
│ Alerts   │    │ Assemble │    │ Fix or   │    │ Post-    │
│ Monitor  │    │ team     │    │ rollback │    │ mortem   │
│ Reports  │    │ Assign   │    │ Verify   │    │ Actions  │
│          │    │ roles    │    │ recovery │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### Incident Roles

| Role | Responsibility |
|------|---------------|
| **Incident Commander (IC)** | Coordinates response; makes decisions |
| **Operations Lead** | Investigates and implements fixes |
| **Communications Lead** | Updates stakeholders, status page |
| **Scribe** | Documents timeline and actions |

---

## Incident Severity Levels

| Level | Impact | Response | FoodExpress Example |
|-------|--------|----------|---------------------|
| **SEV-1** | Service down for all users | All hands, 5 min response | All orders failing |
| **SEV-2** | Major feature degraded | On-call team, 15 min | Payments failing, orders queueing |
| **SEV-3** | Minor feature affected | On-call, next business hour | Rating system down |
| **SEV-4** | Low impact, workaround exists | Ticket, within sprint | Menu images not loading |

### Escalation timeline:
```
SEV-1: 5 min → IC assigned
       15 min → Engineering manager notified
       30 min → VP Engineering notified
       60 min → Executive team notified
```

---

## Blameless Post-Mortems

### Focus on systems, not individuals

```
┌─────────────────────────────────────────────────────┐
│                 POST-MORTEM TEMPLATE                 │
│                                                      │
│  Title: Payment Service Outage - Sept 8, 2026       │
│  Duration: 14:23 - 14:42 (19 minutes)               │
│  Severity: SEV-2                                     │
│  Author: Sustain Engineering Team                    │
│  Date: Sept 9, 2026                                  │
│                                                      │
│  Sections:                                           │
│  1. Summary (2 sentences)                           │
│  2. Impact (users affected, error budget consumed)  │
│  3. Timeline (minute-by-minute)                     │
│  4. Root Cause Analysis                             │
│  5. What Went Well                                  │
│  6. What Went Wrong                                 │
│  7. Action Items (with owners and deadlines)        │
│  8. Lessons Learned                                 │
└─────────────────────────────────────────────────────┘
```

**Blameless:** "The system allowed this to happen" not "Person X caused this."

---

## Post-Mortem: Example

### FoodExpress Payment Service Outage

**Summary:** Payment service became unavailable for 19 minutes due to database connection pool exhaustion, causing order placement failures for ~2,300 customers.

**Impact:**
- 2,300 customers experienced failed orders
- Estimated revenue loss: INR 3,45,000
- Error budget consumed: 43% of monthly budget

**Root Cause:** A slow database query (missing index on `orders.created_at`) held connections for 30+ seconds. During lunch rush, all 20 connection pool slots were occupied by slow queries, causing new requests to timeout.

**Action Items:**

| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | Add index on orders.created_at | DB Team | Sept 10 | Done |
| 2 | Increase connection pool to 50 | Platform | Sept 10 | Done |
| 3 | Add connection pool monitoring | SRE | Sept 12 | In Progress |
| 4 | Add circuit breaker on DB calls | Dev Team | Sept 15 | To Do |
| 5 | Load test with Diwali traffic levels | QE | Sept 20 | To Do |

---

## Post-Mortem: What Went Well vs Wrong

### Payment Service Outage Post-Mortem (continued)

| What Went Well | What Went Wrong |
|---------------|-----------------|
| Alert fired within 2 minutes of impact | No connection pool monitoring -- could have detected earlier |
| On-call responded in 3 minutes | Root cause took 10 minutes to identify (too long) |
| Rollback procedure worked correctly | No runbook for "connection pool exhaustion" scenario |
| Communication to stakeholders was timely | Missing index was known issue but never prioritized |

### Lessons Learned:
1. Monitor resource pools (connections, threads, file descriptors), not just CPU/memory
2. Create runbooks for common database failure modes
3. Prioritize known technical debt before it becomes an incident
4. Load test with realistic traffic patterns (lunch rush simulation)

---

## Toil Assessment Framework

### Prioritize what to automate

```
                    HIGH IMPACT
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        │  Automate     │  Automate     │
        │  LATER        │  FIRST        │
        │  (high effort)│  (high value) │
        │               │               │
  LOW ──┼───────────────┼───────────────┼── HIGH
FREQUENCY               │               FREQUENCY
        │               │               │
        │  IGNORE       │  Automate     │
        │  (not worth)  │  SECOND       │
        │               │  (quick wins) │
        │               │               │
        └───────────────┼───────────────┘
                        │
                    LOW IMPACT
```

---

## FoodExpress Toil Assessment

| Task | Frequency | Duration | Monthly Hours | Automatable | Priority |
|------|-----------|----------|---------------|-------------|----------|
| Restart crashed pods | 3x/week | 15 min | 3.0 | K8s liveness probes | FIRST |
| Scale for lunch rush | Daily | 10 min | 3.5 | HPA | FIRST |
| DB backup verification | Daily | 20 min | 7.0 | Cron + script | FIRST |
| SSL cert renewal | Quarterly | 2 hrs | 0.67 | cert-manager | SECOND |
| Log rotation | Weekly | 5 min | 0.33 | logrotate config | SECOND |
| Deploy to staging | 2x/week | 30 min | 4.0 | Jenkins pipeline | FIRST |
| Incident war room setup | Monthly | 15 min | 0.25 | PagerDuty automation | LATER |
| **TOTAL** | | | **18.75** | Target: < 5 hrs | |

---

## Observability + SRE MCQ

### 30 questions, 30 minutes

| Topic | Questions |
|-------|-----------|
| Observability (Three Pillars) | 5 |
| Prometheus & PromQL | 5 |
| Grafana & Alerting | 4 |
| SLIs & SLOs | 5 |
| Error Budgets | 4 |
| Toil & Automation | 3 |
| Incident Response & Post-Mortems | 4 |

### Sample Questions

1. Which is NOT one of the three pillars of observability?
   - A) Logs  B) Metrics  C) Traces  D) Alerts

2. An SLO of 99.9% availability allows how much downtime per month?
   - A) 4.38 min  B) 43.8 min  C) 438 min  D) 8.76 hrs

3. In a blameless post-mortem, the focus is on:
   - A) Who made the mistake  B) Systems and processes  C) Punishment  D) Blame

---

## Lab: SLO & Error Budget Worksheet

### Define SLOs for FoodExpress services

Complete the worksheet in `Labs/lab-exercises.md`:
1. Define SLIs for 3 FoodExpress services
2. Set SLO targets with justification
3. Calculate error budgets (monthly)
4. Write an error budget policy
5. Assess toil and prioritize automation

---

## Lab: Write a Post-Mortem

### Scenario

At 20:15 on a Friday, FoodExpress delivery tracking went down. Customers couldn't see their delivery status. The service was restored at 20:52. Write a blameless post-mortem using the template provided.

### Given facts:
- Root cause: Expired TLS certificate on delivery-service
- 12,000 customers affected
- Delivery service was unreachable for 37 minutes
- On-call engineer was at dinner, responded in 12 minutes
- Fix: manually renewed certificate

---

## Key Takeaways

| Concept | Key Point |
|---------|-----------|
| SRE | Software engineering applied to operations; embrace managed risk |
| SLI | Quantitative measure of user experience (good events / total events) |
| SLO | Target for SLI (e.g., 99.9% availability over 30 days) |
| Error Budget | 1 - SLO; budget for allowed failures; balances reliability vs velocity |
| Toil | Repetitive, automatable work; keep under 50% of time |
| Chaos Engineering | Intentionally inject failures to build anti-fragile systems |
| Incident Response | Structured roles (IC, Ops Lead, Comms Lead, Scribe) |
| Blameless Post-Mortem | Focus on systems/processes, not individuals; actionable items |

> **Next:** Module 34 -- ITSM & ServiceNow
