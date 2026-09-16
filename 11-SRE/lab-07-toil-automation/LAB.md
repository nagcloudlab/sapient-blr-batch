# Lab 07: Toil & Automation

## Objective

Identify toil in operations work, quantify it, prioritize what to automate,
and write a real automation script that eliminates a toil task.

---

## Concepts

### What is Toil?

```
Toil is work that:
  [x] Manual        -- a human has to do it
  [x] Repetitive    -- you do it over and over
  [x] Automatable   -- a machine could do it
  [x] Tactical      -- reactive, not strategic
  [x] No lasting value -- doesn't improve the system permanently
  [x] Scales linearly -- grows as the service grows

Toil is NOT:
  [ ] Writing automation scripts (this REDUCES future toil)
  [ ] Architecture design
  [ ] Code reviews
  [ ] Capacity planning
  [ ] Post-mortem analysis
```

### Google's Rule

> **SRE teams should spend no more than 50% of their time on toil.**
> The other 50% should be engineering work that reduces future toil.

```
If toil > 50%:
  Team becomes an ops team, not an SRE team.
  No time to automate = toil keeps growing.
  Team burns out and attrition increases.
```

---

## Part 1: Identify Toil

### Exercise: Classify Each Task

For each task, mark whether it's TOIL or ENGINEERING work:

```
+----+--------------------------------------------+-------+-------------+
| #  | Task                                       | Toil? | Why?        |
+----+--------------------------------------------+-------+-------------+
| 1  | Manually restarting crashed pods            |       |             |
| 2  | Writing a Kubernetes liveness probe config  |       |             |
| 3  | Scaling up replicas before lunch rush daily |       |             |
| 4  | Configuring HPA (auto-scaling)             |       |             |
| 5  | Manually rotating SSL certificates          |       |             |
| 6  | Setting up cert-manager for auto-renewal    |       |             |
| 7  | Running database backups manually each day  |       |             |
| 8  | Copying logs from servers for investigation |       |             |
| 9  | Building a Grafana dashboard                |       |             |
| 10 | Manually checking if backups succeeded      |       |             |
| 11 | Responding to "disk full" alerts            |       |             |
| 12 | Writing a capacity planning document        |       |             |
+----+--------------------------------------------+-------+-------------+
```

<details>
<summary>Answers</summary>

| # | Task | Toil? | Reasoning |
|---|------|-------|-----------|
| 1 | Manually restarting crashed pods | TOIL | Manual, repetitive, automatable |
| 2 | Writing liveness probe config | ENGINEERING | Reduces future toil (auto-restart) |
| 3 | Scaling up before lunch rush | TOIL | Manual, repetitive, predictable |
| 4 | Configuring HPA | ENGINEERING | One-time work that eliminates scaling toil |
| 5 | Manually rotating SSL certs | TOIL | Manual, repetitive, automatable |
| 6 | Setting up cert-manager | ENGINEERING | Eliminates cert rotation toil |
| 7 | Running DB backups manually | TOIL | Manual, repetitive, scriptable |
| 8 | Copying logs from servers | TOIL | Manual, should use centralized logging |
| 9 | Building Grafana dashboard | ENGINEERING | Creates lasting value |
| 10 | Manually checking backups | TOIL | Automatable with a verification script |
| 11 | Responding to disk full alerts | TOIL | Should have auto-cleanup or auto-expand |
| 12 | Capacity planning | ENGINEERING | Strategic, lasting value |

</details>

---

## Part 2: Quantify and Prioritize Toil

### Exercise: FoodExpress Toil Register

Fill in the monthly cost and prioritize using the Impact/Frequency matrix:

```
+----+------------------------------+-----------+----------+--------+-----------+
| #  | Toil Task                    | Frequency | Duration | Monthly| Automation|
|    |                              |           | (each)   | Hours  | Candidate |
+----+------------------------------+-----------+----------+--------+-----------+
| 1  | Restart crashed pods         | 4x/week   | 15 min   |        |           |
| 2  | Scale for lunch rush         | Daily     | 10 min   |        |           |
| 3  | DB backup + verify           | Daily     | 25 min   |        |           |
| 4  | SSL cert renewal             | Quarterly | 2 hours  |        |           |
| 5  | Deploy to staging            | 3x/week   | 20 min   |        |           |
| 6  | Log cleanup on servers       | Weekly    | 10 min   |        |           |
| 7  | Manually send incident email | ~2x/month | 15 min   |        |           |
| 8  | Rotate API keys              | Monthly   | 30 min   |        |           |
+----+------------------------------+-----------+----------+--------+-----------+
| TOTAL                                                    |        |           |
+----+------------------------------+-----------+----------+--------+-----------+
```

### Prioritization Matrix

```
                    HIGH FREQUENCY
                         |
          AUTOMATE       |       AUTOMATE
          LATER          |       FIRST
     (high effort,       |    (high value,
      low frequency)     |     quick win)
                         |
    LOW IMPACT ──────────+────────── HIGH IMPACT
                         |
          IGNORE         |       AUTOMATE
          (not worth     |       SECOND
           the effort)   |    (meaningful but
                         |     less urgent)
                         |
                    LOW FREQUENCY
```

### Exercise: Place Each Toil Task in the Matrix

```
Which tasks go in "AUTOMATE FIRST"?   _______________
Which tasks go in "AUTOMATE SECOND"?  _______________
Which tasks go in "AUTOMATE LATER"?   _______________
Which tasks can you IGNORE?           _______________
```

---

## Part 3: Write a Real Automation Script

Let's automate one of the most common toil tasks: **health check + auto-restart**.

### Scenario

Currently, someone manually checks if services are healthy and restarts
them if they're not. Let's automate this.

### Create the health check script

A pre-built script is provided at `lab-07-toil-automation/health-check.sh`. Read through it
to understand how it works, then test it:

```bash
cd lab-07-toil-automation

# Test with services running (should show all OK)
./health-check.sh

# Simulate a failure: stop payment-service
cd ../services && docker compose stop payment-service && cd -

# Run health check again (should detect failure and restart)
./health-check.sh

# Verify the log
cat health-check.log

# Bring payment-service back
cd ../services && docker compose start payment-service && cd -
```

### Toil Reduction Calculation

```
BEFORE automation:
  Manual health checks: 4x/week x 15 min = 4 hours/month
  Manual restarts: included in above

AFTER automation:
  Script runs via cron every 5 minutes
  Human time: ~0 (only if script alerts for manual intervention)

TOIL REDUCED: 4 hours/month
AUTOMATION EFFORT: 30 minutes (one-time)
ROI: Pays for itself in the first week
```

---

## Part 4: Build a 3-Month Automation Roadmap (Optional)

### Exercise

Based on your prioritization, create a roadmap:

```
MONTH 1 ("AUTOMATE FIRST"):
  Week 1-2: ________________________________________
  Week 3-4: ________________________________________
  Expected toil reduction: ____ hours/month

MONTH 2 ("AUTOMATE SECOND"):
  Week 1-2: ________________________________________
  Week 3-4: ________________________________________
  Expected toil reduction: ____ hours/month

MONTH 3 ("AUTOMATE LATER"):
  Week 1-2: ________________________________________
  Week 3-4: ________________________________________
  Expected toil reduction: ____ hours/month

TOTAL TOIL BEFORE: ____ hours/month
TOTAL TOIL AFTER:  ____ hours/month
REDUCTION:         ____%
```

---

## Key Takeaways

1. **Toil is the enemy of SRE** -- it's the work that scales linearly and has no lasting value
2. **50% rule** -- if toil exceeds 50%, the team can't improve systems
3. **Quantify toil** in hours/month to make the case for automation
4. **Prioritize by impact x frequency** -- automate the biggest time sinks first
5. **Every automation script is a one-time cost that saves recurring time**
6. **ROI matters** -- don't spend 2 weeks automating a 5 min/quarter task

> **Next:** Lab 08 -- Chaos Engineering: deliberately break things to build confidence
