# Module 14: Infrastructure Fundamentals -- Exercises

## Lab Overview

This module focuses on understanding IT infrastructure through analysis exercises, architecture review, and a stage gate exit assessment. You will evaluate FoodExpress infrastructure decisions, design resilience strategies, and calculate availability targets.

> "Hi Team, the FoodExpress platform is growing fast and we need to review our infrastructure decisions. We are running on a mix of on-prem and cloud, our costs are climbing, and we had two outages last month. Before we move to the DevOps modules, we need everyone to understand infrastructure fundamentals deeply. Complete these exercises and pass the stage gate assessment."

---

## Exercise 1: Infrastructure Component Mapping (30 min)

### Scenario
Map each FoodExpress component to the correct infrastructure layer and service model.

### Task
Fill in the table:

| FoodExpress Component | Infra Layer | Service Model | Managed By |
|----------------------|-------------|---------------|------------|
| Node.js API servers | ? | ? | ? |
| MySQL database | ? | ? | ? |
| Restaurant images storage | ? | ? | ? |
| Monitoring dashboards (Datadog) | ? | ? | ? |
| Docker containers | ? | ? | ? |
| SSL certificates | ? | ? | ? |
| DNS (api.foodexpress.com) | ? | ? | ? |
| CI/CD pipeline (Jenkins) | ? | ? | ? |
| Load balancer | ? | ? | ? |
| Developer laptops | ? | ? | ? |

### Infra Layers: Compute, Storage, Network, Security, Monitoring, Development
### Service Models: IaaS, PaaS, SaaS, On-Prem
### Managed By: Team, Cloud Provider, Third-Party

---

## Exercise 2: Cloud vs On-Prem Decision Matrix (30 min)

### Scenario
FoodExpress is deciding where to host each service. Evaluate the trade-offs.

### Task
For each service, recommend Cloud or On-Prem with justification:

| Service | Data Sensitivity | Traffic Pattern | Latency Need | Your Recommendation | Justification |
|---------|-----------------|-----------------|-------------- |-------------------|---------------|
| Payment processing | Very High (PCI) | Steady | Low | ? | ? |
| Restaurant search API | Low | Spiky (meal times) | Medium | ? | ? |
| Order database | High | Steady | Low | ? | ? |
| Image CDN | Low | Variable | Medium | ? | ? |
| Analytics/reporting | Medium | Batch (nightly) | High (OK) | ? | ? |
| Real-time delivery tracking | Medium | Spiky | Very Low | ? | ? |

---

## Exercise 3: Availability Calculation (30 min)

### Scenario
Calculate availability and design an HA architecture for FoodExpress.

### Task 1: Calculate System Availability
If each component has the following individual availability:

| Component | Availability |
|-----------|-------------|
| Load Balancer | 99.99% |
| App Server | 99.9% |
| Database | 99.95% |
| Cache (Redis) | 99.9% |

**Question 1:** What is the overall system availability if all components are in series (all must work)?
Formula: A_total = A1 x A2 x A3 x A4

**Question 2:** If you add a second app server in active-active, what is the app layer availability?
Formula: A_redundant = 1 - (1 - A)^2

**Question 3:** With the redundant app layer, what is the new overall availability?

### Task 2: Design HA Architecture
Draw (on paper or describe) an architecture for FoodExpress that achieves 99.95% availability. Include:
- Number of app servers and their configuration
- Database setup (primary + replicas)
- Load balancer configuration
- Which components are in which availability zone

---

## Exercise 4: Cost Optimization (30 min)

### Scenario
The FoodExpress cloud bill is $15,000/month. Find savings.

### Current Infrastructure

| Resource | Type | Monthly Cost | Avg CPU Usage | Notes |
|----------|------|-------------|---------------|-------|
| app-server-1 | m5.xlarge (4 vCPU, 16GB) | $1,200 | 25% | Production |
| app-server-2 | m5.xlarge (4 vCPU, 16GB) | $1,200 | 20% | Production |
| app-server-3 | m5.xlarge (4 vCPU, 16GB) | $1,200 | 15% | Production |
| staging-server | m5.xlarge (4 vCPU, 16GB) | $1,200 | 5% | Runs 24/7 |
| dev-server | m5.large (2 vCPU, 8GB) | $600 | 3% | Runs 24/7 |
| db-primary | r5.2xlarge (8 vCPU, 64GB) | $3,500 | 40% | Production |
| db-replica | r5.2xlarge (8 vCPU, 64GB) | $3,500 | 10% | Read replica |
| S3 storage | Standard | $500 | N/A | 5TB, includes 2TB of old logs |
| Unused EBS volumes | gp3 | $300 | N/A | Orphaned from terminated instances |
| Elastic IPs | 3 unattached | $30 | N/A | Not assigned to any instance |

### Tasks
1. Identify at least **5 cost savings opportunities**
2. Calculate the estimated monthly savings for each
3. Classify each as: Quick Win (do this week), Medium Term (this month), or Long Term (this quarter)
4. What is the total estimated savings?

---

## Exercise 5: Incident Analysis (30 min)

### Scenario
FoodExpress experienced two outages last month. Analyze the incidents.

### Incident 1: Database Connection Pool Exhaustion
- **Duration:** 45 minutes
- **Impact:** 100% of orders failed
- **Timeline:**
  - 14:00 -- Deployment of new feature that opens DB connection per request without closing
  - 14:15 -- Connection pool (max 100) exhausted
  - 14:20 -- All new requests start failing with "too many connections"
  - 14:30 -- Alert fired (30 min delay due to misconfigured threshold)
  - 14:35 -- Engineer investigates, identifies connection leak
  - 14:40 -- Rolled back deployment
  - 14:45 -- Service recovered

### Tasks for Incident 1
1. What was the root cause?
2. What was the detection gap? (How could it be detected faster?)
3. What was the recovery action?
4. List 3 preventive measures to avoid recurrence

### Incident 2: Certificate Expiration
- **Duration:** 2 hours
- **Impact:** All HTTPS traffic failed; HTTP traffic redirected to HTTPS (also failed)
- **Timeline:**
  - 02:00 -- SSL certificate expired
  - 06:00 -- First customer complaint (4 hours later!)
  - 06:15 -- Engineer notified, starts investigation
  - 06:30 -- Identifies expired certificate
  - 07:00 -- New certificate installed, propagation takes 1 hour
  - 08:00 -- Service fully restored

### Tasks for Incident 2
1. What was the root cause?
2. Why was detection so slow (4 hours)?
3. List 3 preventive measures

---

## Checkpoints

### Checkpoint 1 (Morning)
- [ ] Exercise 1: All 10 components mapped correctly
- [ ] Exercise 2: Cloud vs On-Prem recommendations with justifications
- [ ] Exercise 3: Availability calculations completed

### Checkpoint 2 (Afternoon)
- [ ] Exercise 4: At least 5 cost savings identified with estimates
- [ ] Exercise 5: Both incidents analyzed with root cause and preventive measures
- [ ] Stage Gate Exit Assessment completed

---

## Bonus Challenges

1. **Design a DR plan** for FoodExpress: define RPO and RTO for each service, choose a DR strategy, and estimate the cost
2. **Network diagram** -- Draw the complete FoodExpress network including VPC, subnets, security groups, and traffic flow
3. **IaC exercise** -- Write pseudo-Terraform for the FoodExpress infrastructure (VPC, subnets, EC2 instances, RDS, S3)
4. **Security audit** -- List 10 security checks you would perform on the FoodExpress infrastructure
5. **Capacity planning** -- If FoodExpress order volume doubles in 6 months, what infrastructure changes are needed?
