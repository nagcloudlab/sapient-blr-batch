# Final Project + Generative AI -- Submission Checklist
## Module 37 | Days 45-47

---

## ITSM Final Project Checklist

### Major Incident Record (INC-2026-0475)

| # | Item | Done? |
|---|------|-------|
| 1 | Complete timeline covering all 3 days (Monday through Wednesday) | [ ] |
| 2 | Correct priority: P1 - Critical (Major Incident) | [ ] |
| 3 | Impact assessment: number of affected users, revenue impact | [ ] |
| 4 | Communication plan: stakeholders, status page, customer message | [ ] |
| 5 | Resolution: rollback to v3.0.2 | [ ] |
| 6 | Linked to Problem Record PRB-2026-0030 | [ ] |
| 7 | Linked to initial incidents INC-2026-0470 (P3) and escalation history | [ ] |

### Problem Record (PRB-2026-0030)

| # | Item | Done? |
|---|------|-------|
| 8 | Complete 5 Whys analysis to actual root cause | [ ] |
| 9 | Root cause: unclosed HTTP client in retry logic | [ ] |
| 10 | Actionable workaround documented (restart when memory > 80%) | [ ] |
| 11 | Permanent fix linked to change request CHG-2026-0095 | [ ] |
| 12 | Related incidents listed (INC-0470, INC-0475) | [ ] |
| 13 | Trend data: pattern over 3 days, correlated with load | [ ] |

### Change Request (CHG-2026-0095)

| # | Item | Done? |
|---|------|-------|
| 14 | Change type: Normal (not Emergency -- rollback already in place) | [ ] |
| 15 | Risk assessment: Medium, with mitigation plan | [ ] |
| 16 | Implementation plan with test steps (unit, integration, canary) | [ ] |
| 17 | Rollback plan: revert to v3.0.2 | [ ] |
| 18 | Maintenance window: low-traffic period | [ ] |
| 19 | CAB approval documented | [ ] |

### SLA Definition

| # | Item | Done? |
|---|------|-------|
| 20 | Availability target appropriate for payment service (>= 99.95%) | [ ] |
| 21 | 24x7 schedule (no weekend exclusions) | [ ] |
| 22 | P1 resolution time: 4 hours | [ ] |
| 23 | Service credits for SLA breach | [ ] |
| 24 | Monthly measurement and reporting | [ ] |

### Service Catalog Entry

| # | Item | Done? |
|---|------|-------|
| 25 | Service description, owner, status | [ ] |
| 26 | Internal dependencies (MySQL, Redis, order-service) | [ ] |
| 27 | External dependencies (Razorpay gateway) | [ ] |
| 28 | Support model (L1/L2/L3 with groups) | [ ] |

### Post-Incident Review

| # | Item | Done? |
|---|------|-------|
| 29 | Blameless format (no individual blame) | [ ] |
| 30 | Timeline reconstruction for all 3 days | [ ] |
| 31 | Contributing factors identified (code, process, monitoring, prioritization) | [ ] |
| 32 | Action items with owners and deadlines | [ ] |

### Dashboard & Presentation

| # | Item | Done? |
|---|------|-------|
| 33 | Dashboard covers golden signals for payment service | [ ] |
| 34 | Presentation: clear structure, technical accuracy, Q&A handled | [ ] |

---

## GenAI Labs Checklist

| # | Item | Done? |
|---|------|-------|
| 35 | AI Prompts: Role defined in system prompt | [ ] |
| 36 | AI Prompts: Temperature set to reasonable value (0.3-0.7) | [ ] |
| 37 | AI Prompts: max_tokens appropriate for output length | [ ] |
| 38 | AI Prompts: Output format specified for incident analysis | [ ] |
| 39 | AI Prompts: SQL generator prohibits destructive operations | [ ] |
| 40 | AI Prompts: Input sanitization for prompt injection defense | [ ] |
| 41 | AI Eval: API key from environment variable | [ ] |
| 42 | AI Eval: Error handling around API calls | [ ] |
| 43 | AI Eval: Output validation before returning | [ ] |
| 44 | AI Eval: Rate limiting between API calls | [ ] |
| 45 | AI Eval: AI responses logged for audit | [ ] |
| 46 | AI Eval: No PII in prompts | [ ] |
| 47 | AI Trust: Security code is LOW trust | [ ] |
| 48 | AI Trust: Test generation is HIGH trust | [ ] |
| 49 | AI Trust: Production deploy requires code review | [ ] |
| 50 | AI Trust: PII and secrets excluded from AI sharing | [ ] |
| 51 | AI Trust: Hallucinations require verification | [ ] |

---

## Self-Check Questions

1. **Why document all 3 days in the incident record?** The escalation pattern (P3 > P2 > P1) reveals a systemic issue: the initial incident was under-prioritized. This is a key learning for the PIR.
2. **Why is the permanent fix a Normal change, not Emergency?** The rollback resolved the immediate crisis. The permanent fix can follow normal CAB approval to ensure proper testing.
3. **Why does the payment service need a higher SLA than the menu service?** Payment failures directly block revenue. Menu slowness is annoying but customers can still browse. Business criticality determines SLA targets.
4. **Why should AI-generated security code be LOW trust?** AI can introduce subtle security vulnerabilities (race conditions, injection flaws, weak crypto). Security code needs expert human review.
5. **Why must PIR be blameless?** In blame cultures, people hide mistakes. In blameless cultures, people share openly, enabling systemic improvements. The goal is fixing the system, not punishing individuals.
