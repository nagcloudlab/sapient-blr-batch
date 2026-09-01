# Final Project + Generative AI -- Trainer Solutions & Hints
## Module 37 | Days 45-47

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Major Incident Record | Complete 3-day timeline, P1 priority, communication plan with status page, VPs, and customer message, resolution=rollback to v3.0.2 | Students document only Day 3 and miss the 2-day escalation history. The full timeline shows the incident was initially under-prioritized | Ask: "Should the incident have stayed at P3 on Day 1? What signals suggested it would get worse?" |
| 2 | Problem Record | 5 Whys: timeout > OOM > memory leak > unclosed HTTP client > no resource cleanup in retry logic. Workaround: restart pods when memory > 80%. Fix: refactor retry to reuse HTTP client | Students stop the 5 Whys too early ("memory leak" is Why 3, not the root cause). Push to "Why does the memory leak exist?" | Ask: "If you just fix the memory leak but don't change the retry pattern, what happens when a different resource leaks?" |
| 3 | Change Request | Normal change, Medium risk (code change to payment flow), implementation plan with unit tests + integration tests + canary deploy, rollback = revert to v3.0.2, maintenance window | Students mark it as Emergency change. It was an emergency during the incident (rollback was emergency). The permanent fix is a Normal change because the immediate risk is resolved | Ask: "Is the permanent fix urgent? The rollback is already in place. Take time to do it right." |
| 4 | SLA Definition | 99.95% availability for payment (higher than general platform), 4-hour P1 resolution, 24x7 schedule, service credits at 99.9% and 99.5% tiers | Students copy the general platform SLA. Payment is more critical and needs higher availability targets | Ask: "Should the payment SLA be the same as the menu browsing SLA? Which one loses revenue when it's down?" |
| 5 | Service Catalog | Payment Processing entry with dependencies (Razorpay gateway, MySQL, Redis, order-service), 24x7 support, L1 Service Desk / L2 Platform Engineering / L3 Payment Engineering on-call | Students list technical dependencies but forget external dependencies (Razorpay). External dependency failures are common | Ask: "What happens to your payment service if Razorpay goes down?" |
| 6 | Post-Incident Review | Blameless format: timeline reconstruction, contributing factors (missing resource cleanup, no memory alerts, P3 under-prioritization), action items with owners | Students assign blame ("Developer X wrote bad code"). Enforce blameless culture: focus on system improvements | Ask: "Would blaming the developer prevent the next memory leak? What systemic change would?" |
| 7 | Dashboard | Golden signals for payment: latency (histogram), traffic (req/s), errors (5xx rate), saturation (memory, connections). Plus: payment success rate, Razorpay gateway health | Students create generic dashboards. Payment-specific metrics (payment success rate, gateway health) are critical | Ask: "At 3 AM when payment is down, what three numbers do you look at first?" |
| 8 | AI Labs | Prompts: add role, fix temperature/tokens, add format, constrain SQL, add input sanitization. Eval: env var API key, try/except, output validation, rate limit, logging, no PII. Trust: security=low, tests=high, review required, no PII sharing, verify hallucinations | Students fix obvious bugs (API key) but miss subtle ones (PII in prompts, hallucination policy) | Ask: "Your prompt includes a customer's phone number. What happens if the AI model's provider stores all prompts?" |
| 9 | Presentation | Clear structure: Context > Architecture > Incident Timeline > Root Cause > Fix > Prevention > Demo | Teams run out of time because they try to show everything. Guide them to prioritize the story arc | Tip: "Tell it like a story. Start with the 3 AM alert. End with how you made sure it never happens again." |

---

## Post-Incident Review Template (Expected Output)

### Contributing Factors (not "Root Causes")

| # | Factor | Category | Why It Matters |
|---|--------|----------|---------------|
| 1 | No resource cleanup in retry logic | Code quality | Allowed memory leak to exist |
| 2 | No code review for retry pattern | Process | Memory leak not caught before merge |
| 3 | No memory usage alert | Monitoring | Leak grew for 3 days before outage |
| 4 | Initial P3 priority on Day 1 | Prioritization | Delayed investigation when it was easier to fix |
| 5 | No integration test for retry under failure | Testing | Leak only manifests with sustained payment failures |
| 6 | Scaling as a fix (Day 2) | Band-aid fix | Masked the underlying issue, delayed root cause |

### Action Items

| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | Fix memory leak: reuse HTTP client in retry logic | Dev Team | 2026-09-20 | Open |
| 2 | Add memory usage alert at 80% threshold | SRE | 2026-09-17 | Open |
| 3 | Add integration test for payment retry under sustained failure | QE | 2026-09-20 | Open |
| 4 | Mandatory code review for all payment service changes | Process | 2026-09-15 | Open |
| 5 | Add OOM kill alert on all payment pods | SRE | 2026-09-17 | Open |
| 6 | Review prioritization guidelines (when to escalate P3 to P2) | ITSM Lead | 2026-09-22 | Open |

---

## Key Discussion Points

1. Why is blameless post-incident review important? (People hide mistakes in blame cultures; learning stops)
2. When does an incident become a problem? (When patterns emerge or root cause needs investigation)
3. Why is the permanent fix a Normal change, not Emergency? (The rollback solved the immediate issue; Normal gives time for proper testing)
4. How do you decide SLA targets for different services? (Business criticality, revenue impact, user expectations)
5. What is the role of AI in incident response? (Analysis assistant, not decision maker; always verify)
6. What is the single most valuable skill for a sustain engineer? (The ability to learn and adapt -- technology changes constantly)
