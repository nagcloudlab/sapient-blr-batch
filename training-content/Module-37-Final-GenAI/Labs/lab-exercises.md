# Final Project + Generative AI -- Lab Exercises
## Module 37 | Days 45-47

---

## Client Email

```
From: meera.patel@foodexpress.in
To: sustain-engineering@team.com
Subject: FINAL PROJECT: Payment Service Incident + AI Integration
Date: 2026-09-13

Team,

This is your final assessment. You will:

1. Handle a complete ITSM lifecycle for a major payment
   service outage (Days 45-46)
2. Fix our AI prompt templates and evaluation harness
   that have bugs (Day 47)

For the ITSM project, refer to the scenario in the
Project Brief. All deliverables must be submitted by
end of Day 46.

For the AI labs, fix the provided templates and demonstrate
responsible AI usage.

-- Meera Patel, CTO, FoodExpress
```

---

## Lab 1: Fix the AI Prompt Templates (6 bugs)

**File:** `starter-code/ai-prompts.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the system prompt for the menu generator | No role is defined | AI gives generic responses, not food-specific |
| 2 | Look at the temperature setting | Temperature is 2.0 (max valid is ~1.0-2.0 but 2.0 is too random) | Output is incoherent gibberish |
| 3 | Check the max_tokens setting | max_tokens is 5000 for a 50-word description | Wasteful and allows excessively long output |
| 4 | Look at the incident analysis prompt | No output format specified | AI gives unstructured wall of text |
| 5 | Check the SQL generation prompt | No constraint against destructive operations | AI could generate DELETE or DROP statements |
| 6 | Look at the security guardrails | No input sanitization rule | Prompt injection vulnerability |

### Verification

For each prompt: Does it have a role, context, task, format, and constraints? Would you trust the output?

---

## Lab 2: Fix the AI Evaluation Harness (6 bugs)

**File:** `starter-code/ai-eval.py`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the API key handling | API key is hardcoded in the source code | Security vulnerability |
| 2 | Look at the error handling | No try/except around API calls | Script crashes on API errors |
| 3 | Check the output validation | No validation of AI response | Potentially harmful content passes through |
| 4 | Look at the rate limiting | No rate limiting on API calls | Could exhaust API quota rapidly |
| 5 | Check the logging | AI responses are not logged | No audit trail for AI-generated content |
| 6 | Look at the PII handling | Customer data included in prompt without redaction | PII sent to external AI service |

### Verification

Run through the evaluation flow mentally: Is the API key secure? Are errors handled? Is output validated? Is there an audit trail?

---

## Lab 3: Fix the "When to Trust AI" Guidelines (5 bugs)

**File:** `starter-code/ai-trust-guidelines.yaml`

### Bug List

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check the trust level for security code | Security code is marked "High Trust" | Dangerous -- security code needs expert review |
| 2 | Look at the trust level for test generation | Test generation is marked "Low Trust" | Overly cautious -- tests are safe to AI-generate |
| 3 | Check the review policy for production deploys | AI code can be deployed without review | No human in the loop for production changes |
| 4 | Look at the data sharing policy | "All data can be shared with AI" | No restrictions on PII or sensitive data |
| 5 | Check the hallucination handling | "If AI output looks correct, trust it" | No verification requirement |

### Verification

Would a security audit approve these guidelines? Would following them lead to safe AI usage?

---

## Lab 4: AI-Assisted Troubleshooting Exercise

### Hands-on (no bugs to fix -- practice exercise)

Given these FoodExpress logs, use AI to help diagnose the issue:

```
2026-09-13 08:15:23 [ERROR] DeliveryService: WebSocket pool exhausted
2026-09-13 08:15:24 [WARN]  GPSHandler: Update queue full (1000/1000)
2026-09-13 08:15:25 [ERROR] DeliveryTracker: Stale GPS data for rider R-4521
2026-09-13 08:15:26 [INFO]  ActiveConnections: 4832 (limit: 5000)
2026-09-13 08:15:27 [WARN]  MemoryMonitor: Heap usage 94% (483MB/512MB)
2026-09-13 08:15:28 [ERROR] DeliveryService: Cannot allocate new WebSocket
2026-09-13 08:15:30 [ERROR] GPSHandler: 47 riders with stale data (>5 min)
```

**Tasks:**
1. Write a prompt for AI to analyze these logs
2. Evaluate the AI's suggested root cause
3. Check if the AI's fix suggestion is correct
4. Identify anything the AI might miss

---

## Lab Submission

| # | Item | Done? |
|---|------|-------|
| 1 | All 6 AI prompt template bugs fixed | [ ] |
| 2 | All 6 AI evaluation harness bugs fixed | [ ] |
| 3 | All 5 AI trust guidelines bugs fixed | [ ] |
| 4 | AI-assisted troubleshooting exercise completed | [ ] |
