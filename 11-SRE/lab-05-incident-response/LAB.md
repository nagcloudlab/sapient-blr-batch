# Lab 05: Incident Response

## Objective

Practice a structured incident response through a simulated outage.
Learn incident roles, severity levels, communication, and escalation.

---

## Concepts

### Incident Response Lifecycle

```
  DETECT          TRIAGE          RESPOND         MITIGATE        RESOLVE
    |               |               |               |               |
 Monitoring     Assess severity  Assemble team   Stop bleeding   Fix root cause
 alerts fire    Assign roles     Investigate      Restore service Post-mortem
 User reports   Open war room    Communicate      Verify recovery Follow-up items
```

### Incident Severity Levels

| Level | Meaning | Response Time | Example |
|-------|---------|---------------|---------|
| **SEV-1** | Critical -- service down for all users | 5 min | All orders failing, zero revenue |
| **SEV-2** | Major -- key feature broken | 15 min | Payments failing, orders queue up |
| **SEV-3** | Minor -- degraded but functional | 1 hour | Slow responses, some timeouts |
| **SEV-4** | Low -- cosmetic or minor issue | Next business day | Incorrect order count on dashboard |

### Incident Roles

| Role | Responsibility | Communication |
|------|---------------|---------------|
| **Incident Commander (IC)** | Runs the incident. Delegates tasks. Makes decisions. | "I'm the IC. Here's our status." |
| **Operations Lead** | Investigates, diagnoses, implements fixes | "I see X in the logs. Trying Y." |
| **Communications Lead** | Updates stakeholders, status page, customers | "Posting update: ETA 10 min." |
| **Scribe** | Documents the timeline in real-time | "14:23 - Alert fired. 14:25 - IC assigned." |

---

## Part 1: The Simulation Setup

### Scenario

You are the SRE on-call team for FoodExpress. It's **Friday 7:30 PM** (peak dinner time).

**The class will be split into groups of 4, each person taking one role.**

Assign roles within your group:
```
IC:                 _______________
Operations Lead:    _______________
Communications Lead: _______________
Scribe:             _______________
```

---

## Part 2: Incident Simulation

### Timeline of Events (Trainer reads these out one at a time)

**19:30 -- Alert fires**

```
ALERT: Order Service Availability SLI dropped below 99.9%
       Error rate: 15% (was 0.3%)
       Duration: 3 minutes
       Dashboard: http://localhost:3001
```

**Action required:** IC acknowledges the alert and assigns severity.

Questions for the team:
- What severity is this? Why?
- Who do you notify?

---

**19:33 -- Investigation begins**

Operations Lead checks:

```bash
# Check order service health
curl -s http://localhost:3000/health

# Check recent errors in logs
cd ../services && docker compose logs order-service 2>&1 | tail -30

# Check payment service health
curl -s http://localhost:8080/health

# Check payment service logs
cd ../services && docker compose logs payment-service 2>&1 | tail -30
```

**Finding:** Order service is UP, but payment-service is returning 500 errors
at a higher rate than normal.

Questions:
- Is this a SEV-1 or SEV-2?
- What does the Communications Lead post to the status page?

---

**19:36 -- Diagnosis**

Operations Lead digs deeper:

```bash
# Check error patterns
cd ../services && docker compose logs payment-service 2>&1 | grep -c "INTERNAL ERROR"
cd ../services && docker compose logs payment-service 2>&1 | grep -c "completed"

# Check if payment service is overwhelmed
cd ../services && docker compose logs payment-service 2>&1 | grep "SLOW PROCESSING" | tail -10
```

**Root cause identified:** Payment service database connection simulation is
failing more than usual under load.

---

**19:38 -- Mitigation decision**

IC asks: "What are our options?"

```
Option A: Restart payment-service pod
  Pro: Quick fix, clears any bad state
  Con: Brief additional downtime during restart

Option B: Redirect traffic away from payment-service
  Pro: Orders stop failing immediately
  Con: No payments processed

Option C: Scale up payment-service replicas
  Pro: Distribute load
  Con: Takes time, may not fix root cause
```

**Team decides and acts:**

```bash
# If Option A: Restart payment service
cd ../services && docker compose restart payment-service

# Verify recovery
sleep 5
curl -s http://localhost:8080/health
```

---

**19:42 -- Verification**

```bash
# Send test orders
for i in $(seq 1 10); do
  curl -s -X POST http://localhost:3000/orders \
    -H "Content-Type: application/json" \
    -d '{"item": "Naan", "quantity": 2, "price": 60}' | jq .status
done
```

**Check:** Are orders succeeding again? What's the success rate?

---

**19:45 -- All clear**

IC declares: "Incident resolved. Service restored at 19:42.
Total duration: 12 minutes. Moving to post-incident review."

---

## Part 3: Incident Document

### Scribe's document should look like this:

Each group's scribe presents their timeline:

```
INCIDENT REPORT
────────────────────────────────────────────
Incident ID:    INC-2026-0918
Title:          Payment Service Degradation During Dinner Rush
Severity:       ____
Duration:       19:30 - 19:42 (12 minutes)
IC:             ____
Ops Lead:       ____
Comms Lead:     ____
Scribe:         ____

TIMELINE:
19:30 - Alert fired: error rate 15% on order-service
19:31 - IC acknowledged, severity assessed as ____
19:32 - Team assembled in war room (Slack channel)
19:33 - Ops Lead investigating order-service logs
19:34 - Identified: payment-service returning 500s
19:36 - Root cause: ____________________________________
19:38 - Mitigation: decided to ________________________
19:39 - Executing mitigation
19:42 - Service restored, verified with test orders
19:45 - IC declares all clear

IMPACT:
- Users affected: ____
- Orders failed: ____
- Error budget consumed: ____ min of ____ min total
- Estimated revenue impact: ____

FOLLOW-UP:
- [ ] Write post-mortem (due: Monday)
- [ ] Review error budget status
- [ ] Identify automation opportunities
```

---

## Part 4: Discussion -- What Makes Good Incident Response

### Common Anti-Patterns

| Anti-Pattern | Why It's Bad | SRE Best Practice |
|-------------|-------------|-------------------|
| Everyone investigates independently | Chaotic, duplicate work | IC delegates specific tasks |
| No communication to stakeholders | Users panic, flood support | Comms Lead posts every 15 min |
| Jumping to root cause fix during outage | Takes too long, users still affected | Mitigate first, fix root cause later |
| No timeline documented | Can't learn from the incident | Scribe writes everything in real-time |
| "Who broke this?" | Creates blame culture | Focus on what happened, not who |

### The Golden Rule of Incident Response

```
MITIGATE first, ROOT CAUSE later.

During the incident:  STOP THE BLEEDING (restart, rollback, redirect)
After the incident:   FIND THE ROOT CAUSE (post-mortem, next lab!)
```

---

## Key Takeaways

1. **Structured roles** prevent chaos during incidents
2. **Severity levels** determine response urgency and escalation
3. **Mitigate first** -- restore service, then investigate root cause
4. **Communicate proactively** -- silence causes more panic than bad news
5. **Document everything** in real-time -- memory is unreliable under stress

> **Next:** Lab 06 -- After the incident is resolved, write a blameless post-mortem
