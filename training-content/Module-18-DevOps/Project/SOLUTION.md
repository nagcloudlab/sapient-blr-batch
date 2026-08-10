# DevOps Fundamentals -- Trainer Solutions & Hints
## Module 18 | Day 19

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Jenkinsfile | Use credentials store, build-number tags, approval gates, post-build actions | Students miss the credential exposure issue -- they focus on functional bugs first | Ask: "What happens if this Jenkinsfile is in a public repo?" |
| 2 | Fix Deployment Strategy | Replace big-bang with rolling/blue-green, add automated health checks, change schedule | Students propose complex strategies but forget the basics: health checks and rollback | Ask: "How long can FoodExpress afford to be down during a deployment?" |
| 3 | Design Pipeline | 7+ stages with proper tool selection, testing at every stage, automated rollback | Students design ideal pipelines without considering cost/complexity tradeoffs | Ask: "What's the minimum viable pipeline you could ship this week?" |
| 4 | 7 C's Mapping | Each C maps to specific pipeline stages and tools | Students confuse Continuous Delivery with Continuous Deployment | Clarify: "Delivery = can deploy anytime. Deployment = every change auto-deploys." |
| 5 | DevOps Maturity | FoodExpress is Level 3 (Defined), needs metrics and SLOs for Level 4 | Students rate too high (Level 4-5) without evidence of metrics-driven decisions | Ask: "What metrics does FoodExpress currently track? Are decisions based on them?" |

---

## Key Discussion Points

1. Why is "Friday 5 PM" a terrible deployment time? (No one available for incidents over weekend)
2. What is the difference between Continuous Delivery and Continuous Deployment?
3. Why should Docker images NOT use the `latest` tag?
4. How does IaC relate to DevOps? (Reproducibility, auditability, version control)
5. When would you use SOAP/WSDL vs REST/OpenAPI? (Legacy integration vs new services)
