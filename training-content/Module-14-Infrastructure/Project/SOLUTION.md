# Module 14 Solutions -- TRAINER ONLY

## Exercise 1: Infrastructure Component Mapping

| FoodExpress Component | Infra Layer | Service Model | Managed By |
|----------------------|-------------|---------------|------------|
| Node.js API servers | Compute | IaaS (EC2) or PaaS (Beanstalk) | Team (IaaS) / Provider (PaaS) |
| MySQL database | Storage/Compute | IaaS (self-managed) or PaaS (RDS) | Team or Provider |
| Restaurant images storage | Storage | IaaS/PaaS (S3) | Cloud Provider |
| Monitoring dashboards (Datadog) | Monitoring | SaaS | Third-Party |
| Docker containers | Compute | IaaS (self-managed) or PaaS (ECS) | Team or Provider |
| SSL certificates | Security | SaaS (ACM) | Cloud Provider |
| DNS (api.foodexpress.com) | Network | SaaS (Route 53) | Cloud Provider |
| CI/CD pipeline (Jenkins) | Development | IaaS (self-hosted) or SaaS (GitHub Actions) | Team or Third-Party |
| Load balancer | Network | PaaS (ALB) | Cloud Provider |
| Developer laptops | Compute | On-Prem | Team |

## Exercise 2: Cloud vs On-Prem Recommendations

| Service | Recommendation | Justification |
|---------|---------------|---------------|
| Payment processing | Hybrid (On-Prem + Cloud) | PCI compliance requires strict data control; use on-prem for sensitive data, cloud for processing |
| Restaurant search API | Cloud | Spiky traffic during meal times; auto-scaling is essential; data is not sensitive |
| Order database | Cloud (managed RDS) | Steady traffic + managed backups/failover; data encrypted at rest and in transit |
| Image CDN | Cloud (CloudFront/S3) | Content delivery needs global edge presence; low sensitivity; variable traffic |
| Analytics/reporting | Cloud | Batch processing benefits from elastic compute; spin up large instances only when needed |
| Real-time delivery tracking | Cloud | Very spiky traffic; needs low-latency websockets; auto-scaling critical |

## Exercise 3: Availability Calculations

**Question 1:** Series availability
```
A_total = 0.9999 x 0.999 x 0.9995 x 0.999
A_total = 0.9974 = 99.74%
Annual downtime = 365 x 24 x (1 - 0.9974) = 22.8 hours
```

**Question 2:** Redundant app server
```
A_single = 0.999
A_redundant = 1 - (1 - 0.999)^2 = 1 - (0.001)^2 = 1 - 0.000001 = 0.999999 = 99.9999%
```

**Question 3:** New overall availability
```
A_total = 0.9999 x 0.999999 x 0.9995 x 0.999
A_total = 0.9984 = 99.84%
Annual downtime = 365 x 24 x (1 - 0.9984) = 14.0 hours
Improvement: 8.8 hours less downtime per year
```

## Exercise 4: Cost Optimization Answers

| # | Opportunity | Current Cost | Savings | Timeline |
|---|-------------|-------------|---------|----------|
| 1 | Right-size app servers (m5.xlarge -> m5.large at 25% CPU) | $3,600 | $1,800/mo | Quick Win |
| 2 | Shut down staging/dev outside business hours (12 hrs/day) | $1,800 | $900/mo | Quick Win |
| 3 | Delete orphaned EBS volumes + unattached Elastic IPs | $330 | $330/mo | Quick Win |
| 4 | Move 2TB old logs to S3 Glacier | $200 (of $500) | $180/mo | Medium Term |
| 5 | Right-size DB replica (r5.2xlarge -> r5.xlarge at 10% CPU) | $3,500 | $1,750/mo | Medium Term |
| 6 | Reserve DB primary (1-year reserved instance) | $3,500 | $1,050/mo (30%) | Long Term |
| 7 | Use spot instances for staging server | $1,200 | $960/mo (80%) | Medium Term |
| **Total** | | | **$6,970/mo (46%)** | |

## Exercise 5: Incident Analysis Answers

### Incident 1: DB Connection Pool Exhaustion

**Root Cause:** New code opened a database connection per request without closing it. After ~100 requests, the connection pool (max 100) was exhausted, blocking all subsequent requests.

**Detection Gap:** Alert threshold was set at 95% pool usage but only checked every 30 minutes. Should be checked every 1 minute with alert at 80%.

**Preventive Measures:**
1. Code review gate: check for connection management in all DB-touching PRs
2. Load test new features before deployment to catch resource leaks
3. Set monitoring alerts on connection pool usage at 80% with 1-minute intervals
4. Implement connection pooling with automatic timeout and cleanup
5. Canary deployment: deploy to 10% of traffic first to catch issues early

### Incident 2: Certificate Expiration

**Root Cause:** SSL certificate had a fixed expiry date and no automated renewal was configured. No monitoring alert was set for certificate expiry.

**Detection Gap:** No synthetic monitoring (health checks from outside). Internal monitoring did not check certificate validity. First detection was a customer complaint at 6 AM (4 hours after expiry at 2 AM).

**Preventive Measures:**
1. Use auto-renewing certificates (Let's Encrypt or AWS ACM)
2. Add certificate expiry monitoring with alert 30, 14, and 7 days before expiry
3. Set up external synthetic monitoring that checks HTTPS connectivity every minute
4. Document all certificates with expiry dates in a central inventory
5. Run quarterly certificate audits

## Hints

| Exercise | Level 1 | Level 2 |
|----------|---------|---------|
| #1 | "Is the component hardware, software, or a service?" | "S3 is PaaS/IaaS managed by provider; Datadog is SaaS managed by third-party" |
| #2 | "Consider data sensitivity and traffic pattern" | "Spiky traffic = cloud (auto-scale); sensitive data = on-prem or hybrid" |
| #3 | "Series: multiply. Redundant: 1 - (1-A)^N" | "Two servers at 99.9% each = 1 - (0.001)^2 = 99.9999%" |
| #4 | "Look for low CPU usage and always-on non-production servers" | "App servers at 25% CPU can be halved; staging runs 24/7 but used 8 hrs" |
| #5 | "What changed right before the incident?" | "Incident 1: deployment introduced connection leak; Incident 2: no change, just time passing" |
