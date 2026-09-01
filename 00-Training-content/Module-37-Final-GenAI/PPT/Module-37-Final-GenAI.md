# Final Project + Generative AI
## Module 37 | Sustain Engineering Training | Days 45-47

---

## Agenda -- Day 45

| # | Topic |
|---|-------|
| 01 | Final Project Brief & Team Formation |
| 02 | Project Requirements Review |
| 03 | Final Project Work Session (Part 1) |
| 04 | Final Project Work Session (Part 2) |

---

## Agenda -- Day 46

| # | Topic |
|---|-------|
| 01 | Final Project: Last Work Session |
| 02 | Team Demos & Presentations |
| 03 | Evaluation & Peer Review |
| 04 | Final Project Feedback |
| 05 | Individual Assessments (if needed) |

---

## Agenda -- Day 47 (Half Day)

| # | Topic |
|---|-------|
| 01 | Generative AI: Overview & Landscape |
| 02 | AI in Frontend & Backend Development |
| 03 | Building with OpenAI API |
| 04 | AI Tools for Development |
| 05 | DevOps Automation with AI |
| 06 | Hands-on: AI-Assisted Troubleshooting |
| 07 | Programme Wrap-up & Graduation |

---

## Final Project: Overview

### ITSM + ServiceNow Capstone

```
┌──────────────────────────────────────────────────────┐
│         Final Project: FoodExpress ITSM              │
│                                                      │
│  Build a complete ITSM workflow for FoodExpress      │
│  covering the full incident-to-resolution cycle.     │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Scenario: FoodExpress Payment Outage        │   │
│  │                                              │   │
│  │  The payment service has been experiencing   │   │
│  │  intermittent failures for 3 days. Today it  │   │
│  │  went completely down. You must:             │   │
│  │                                              │   │
│  │  1. Handle the major incident                │   │
│  │  2. Investigate the problem                  │   │
│  │  3. Create a change request for the fix      │   │
│  │  4. Define SLAs and monitoring               │   │
│  │  5. Design a service catalog entry           │   │
│  │  6. Write a post-incident review             │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Duration: 1.5 days | Teams of 3-4                   │
│  Presentation: 15 min per team                       │
└──────────────────────────────────────────────────────┘
```

---

## Final Project: Detailed Requirements

### Deliverables

| # | Deliverable | Description | Points |
|---|------------|-------------|--------|
| 1 | Major Incident Record | Complete INC record: timeline, priority, communication, resolution | 15 |
| 2 | Problem Record | Root cause analysis (5 Whys), known error, permanent fix plan | 12 |
| 3 | Change Request | Full RFC for permanent fix: risk assessment, rollback, implementation plan | 12 |
| 4 | SLA Definition | SLA for payment service with targets, penalties, reporting | 8 |
| 5 | Service Catalog Entry | Payment Processing service entry with dependencies and support model | 8 |
| 6 | Post-Incident Review | Blameless retrospective with timeline, action items, lessons learned | 10 |
| 7 | Monitoring Dashboard | Design for payment service golden signals dashboard | 5 |
| 8 | Presentation | Clear demo, professional communication, Q&A handling | 10 |

**Total Points:** 80

---

## Final Project: Scenario Details

### The Incident

```
Day 1 (Monday):
  08:30  Intermittent payment failures noticed by support team
  09:00  INC-2026-0470 created, Priority P3
  11:00  Workaround: Retry button added to checkout page
  14:00  Failure rate drops to ~2%, considered stable

Day 2 (Tuesday):
  09:00  Payment failures increase to 8%
  10:00  INC-2026-0470 reprioritized to P2
  14:00  Pattern noticed: failures correlate with high order volume
  16:00  Temporary fix: Increase payment service replicas from 3 to 8

Day 3 (Wednesday):
  07:30  Payment service completely down (all pods crash-looping)
  07:35  INC-2026-0475 created, Priority P1 - Major Incident declared
  07:40  War room opened: #inc-0475
  08:00  Root cause: Memory leak in payment retry logic (introduced in v3.1.0)
         Each failed payment retry allocates a new HTTP client without closing
  08:15  Rollback to v3.0.2
  08:30  Payment service restored
  09:00  Incident resolved
```

---

## Final Project: Evaluation Criteria

### Scoring Rubric

```
┌──────────────────────────────────────────────────────┐
│  Evaluation Rubric (80 points total)                │
│                                                      │
│  INCIDENT RECORD (15 pts)                           │
│  ├── 5: Complete timeline with all key events       │
│  ├── 3: Correct priority and impact assessment      │
│  ├── 4: Communication plan with stakeholders        │
│  └── 3: Clear resolution and linked records         │
│                                                      │
│  PROBLEM RECORD (12 pts)                            │
│  ├── 4: Complete 5 Whys to root cause               │
│  ├── 3: Actionable workaround documented            │
│  ├── 3: Permanent fix linked to change request      │
│  └── 2: Trend data and related incidents            │
│                                                      │
│  CHANGE REQUEST (12 pts)                            │
│  ├── 3: Correct change type and risk level          │
│  ├── 3: Implementation plan with test steps         │
│  ├── 3: Rollback plan (specific and testable)       │
│  └── 3: Maintenance window with justification       │
│                                                      │
│  SLA + CATALOG + PIR + DASHBOARD (31 pts)           │
│  ├── 8: SLA with realistic targets and penalties    │
│  ├── 8: Service catalog with dependencies           │
│  ├── 10: PIR with action items and owners           │
│  └── 5: Dashboard design covering golden signals    │
│                                                      │
│  PRESENTATION (10 pts)                              │
│  ├── 4: Clear structure and flow                    │
│  ├── 3: Technical accuracy                          │
│  └── 3: Q&A handling                                │
└──────────────────────────────────────────────────────┘
```

---

## Generative AI: Overview

### The AI Landscape in 2026

```
┌──────────────────────────────────────────────────────┐
│           Generative AI Landscape                    │
│                                                      │
│  Large Language Models (LLMs)                        │
│  ├── OpenAI GPT-4 / GPT-4o                         │
│  ├── Anthropic Claude                                │
│  ├── Google Gemini                                   │
│  ├── Meta Llama (open source)                       │
│  └── Mistral (open source)                          │
│                                                      │
│  Code-Specific Models                                │
│  ├── GitHub Copilot (powered by OpenAI)             │
│  ├── Claude Code (Anthropic)                        │
│  ├── Amazon CodeWhisperer / Q Developer             │
│  ├── Cursor / Windsurf                              │
│  └── Google Gemini Code Assist                      │
│                                                      │
│  Enterprise AI Platforms                             │
│  ├── Azure OpenAI Service                           │
│  ├── AWS Bedrock                                    │
│  ├── Google Vertex AI                               │
│  └── Anthropic API                                  │
│                                                      │
│  Key Trend: AI is becoming a development TOOL,      │
│  not a replacement for developers.                   │
└──────────────────────────────────────────────────────┘
```

---

## How LLMs Work (Simplified)

### The Basics

```
┌──────────────────────────────────────────────────────┐
│           How LLMs Generate Text                     │
│                                                      │
│  Input (Prompt):                                     │
│  "Fix the bug in this Python function that           │
│   calculates FoodExpress delivery fee"               │
│        │                                             │
│        ▼                                             │
│  ┌──────────────┐                                   │
│  │  Tokenizer   │  Break text into tokens           │
│  └──────┬───────┘                                   │
│         ▼                                            │
│  ┌──────────────┐                                   │
│  │  Transformer │  Process tokens through            │
│  │  (attention) │  billions of parameters            │
│  └──────┬───────┘                                   │
│         ▼                                            │
│  ┌──────────────┐                                   │
│  │  Output      │  Generate tokens one by one        │
│  │  Sampling    │  (temperature controls randomness) │
│  └──────┬───────┘                                   │
│         ▼                                            │
│  Output (Completion):                                │
│  "The bug is in line 12. The distance variable       │
│   is not converted from meters to kilometers..."     │
└──────────────────────────────────────────────────────┘

Key Concepts:
- Tokens: ~4 characters per token (word fragments)
- Context Window: How much text the model can process (128K+)
- Temperature: 0 = deterministic, 1 = creative
- Hallucination: Model generates plausible but incorrect info
```

---

## AI in Frontend Development

### How AI Assists Frontend Work

| Task | AI Approach | FoodExpress Example |
|------|-----------|---------------------|
| **Code Generation** | Describe the component, AI writes it | "Create a React order tracking component" |
| **Bug Fixing** | Paste buggy code, AI identifies issues | Fix CSS layout bug in restaurant card |
| **Testing** | Generate test cases from component code | Create Cypress tests for checkout flow |
| **Accessibility** | Scan for WCAG violations | Identify missing ARIA labels on buttons |
| **Refactoring** | Suggest cleaner patterns | Convert class components to hooks |
| **Documentation** | Generate JSDoc from code | Document the delivery map component |

### Example: AI-Generated Component

```
Prompt: "Create a React component that shows FoodExpress order
status with a progress bar: Placed > Confirmed > Preparing >
On the Way > Delivered"

AI generates: OrderStatusTracker.jsx with:
- Progress bar component
- Status icons for each step
- Active step highlighting
- Estimated time display
- Responsive layout

Human review needed:
- Business logic correctness
- Edge cases (cancelled orders, refunds)
- Accessibility compliance
- Error state handling
```

---

## AI in Backend Development

### Backend AI Use Cases

| Task | AI Tool | FoodExpress Example |
|------|---------|---------------------|
| **API Design** | LLM prompt | Design REST endpoints for delivery tracking |
| **Database Queries** | Natural language to SQL | "Find all orders above Rs 500 in Bangalore last week" |
| **Code Review** | AI code review tools | Detect potential null pointer in payment logic |
| **Log Analysis** | AI-powered log search | "Find the root cause of payment timeouts" |
| **Performance** | AI profiling | Identify slow database queries automatically |
| **Security** | AI vulnerability scanning | Detect SQL injection risks in order API |

### Example: Natural Language to SQL

```
Prompt: "Find the top 10 restaurants in Bangalore with the
highest order volume this month, including average delivery
time and average rating"

AI generates:
SELECT r.name, r.city,
       COUNT(o.id) as order_count,
       AVG(d.delivery_time_minutes) as avg_delivery_min,
       ROUND(AVG(rt.score), 1) as avg_rating
FROM restaurants r
JOIN orders o ON r.id = o.restaurant_id
JOIN deliveries d ON o.id = d.order_id
LEFT JOIN ratings rt ON o.id = rt.order_id
WHERE r.city = 'Bangalore'
  AND o.created_at >= DATE_TRUNC('month', CURRENT_DATE)
GROUP BY r.id, r.name, r.city
ORDER BY order_count DESC
LIMIT 10;

Human review needed:
- Verify JOIN logic (are all joins correct?)
- Check date function syntax for your database
- Validate column names against actual schema
- Test with sample data
```

---

## Building with OpenAI API

### Simple Integration for FoodExpress

```python
import openai
import os

# FoodExpress: AI-powered menu description generator

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_menu_description(item_name, ingredients, cuisine):
    """Generate an appetizing menu description using AI."""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a food copywriter for FoodExpress. "
                    "Write appetizing menu descriptions in 2-3 sentences. "
                    "Do NOT include pricing, health claims, or allergen info. "
                    "Keep it under 50 words."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Item: {item_name}\n"
                    f"Ingredients: {', '.join(ingredients)}\n"
                    f"Cuisine: {cuisine}"
                )
            }
        ],
        max_tokens=100,
        temperature=0.7
    )

    description = response.choices[0].message.content
    return validate_output(description)

def validate_output(text):
    """Ensure AI output meets FoodExpress guidelines."""
    # Check for prohibited content
    prohibited = ["guaranteed", "cure", "heal", "weight loss", "calorie"]
    for word in prohibited:
        if word.lower() in text.lower():
            return "[Description pending review]"
    # Check length
    if len(text.split()) > 60:
        return text[:200] + "..."
    return text
```

---

## Prompt Engineering Best Practices

### Writing Effective Prompts

```
┌──────────────────────────────────────────────────────┐
│        Prompt Engineering Framework                  │
│                                                      │
│  1. ROLE: Define who the AI is                       │
│     "You are a senior SRE at FoodExpress"            │
│                                                      │
│  2. CONTEXT: Provide background                      │
│     "Our order service uses Spring Boot, MySQL,      │
│      and runs on Kubernetes"                         │
│                                                      │
│  3. TASK: State what you want                        │
│     "Analyze this error log and identify the         │
│      root cause"                                     │
│                                                      │
│  4. FORMAT: Specify output format                    │
│     "Respond with: Root Cause, Impact, Fix,          │
│      Prevention"                                     │
│                                                      │
│  5. CONSTRAINTS: Set boundaries                      │
│     "Do not suggest rewriting the entire service.    │
│      Focus on minimal, targeted fixes."              │
│                                                      │
│  6. EXAMPLES: Show expected output (few-shot)        │
│     "Example: 'Root Cause: Connection pool           │
│      exhaustion due to unclosed connections...'"     │
└──────────────────────────────────────────────────────┘
```

---

## AI Tools for Development

### The Modern AI Toolkit

| Tool | Category | Use Case | FoodExpress Example |
|------|----------|----------|---------------------|
| **GitHub Copilot** | Code completion | Real-time code suggestions | Complete payment validation logic |
| **Claude Code** | CLI agent | Code analysis, refactoring, debugging | Fix bugs across multiple files |
| **ChatGPT / Claude** | Chat interface | Design decisions, learning, documentation | Explain circuit breaker pattern |
| **Cursor** | AI IDE | Full-file editing, multi-file changes | Refactor order service architecture |
| **SonarQube + AI** | Code quality | AI-enhanced code review | Detect security vulnerabilities |
| **Snyk** | Security | AI vulnerability detection | Find CVEs in container images |
| **Datadog AI** | Observability | AI-powered anomaly detection | Detect unusual order patterns |
| **PagerDuty AIOps** | Incident mgmt | AI incident correlation | Group related payment alerts |

### When to Trust AI Output

```
┌──────────────────────────────────────────────────────┐
│  When to Trust AI (and When NOT To)                  │
│                                                      │
│  HIGH TRUST (verify, then use):                      │
│  ✓ Boilerplate code (CRUD, REST endpoints)          │
│  ✓ Test case generation                              │
│  ✓ Documentation drafts                              │
│  ✓ Code formatting and refactoring                   │
│  ✓ Explaining concepts                               │
│                                                      │
│  MEDIUM TRUST (always review carefully):             │
│  ~ Business logic implementation                     │
│  ~ Database queries (verify against schema)          │
│  ~ Configuration files (test in staging)             │
│  ~ Architecture suggestions                          │
│                                                      │
│  LOW TRUST (use as starting point only):             │
│  ✗ Security-critical code                            │
│  ✗ Financial calculations                            │
│  ✗ Compliance and legal advice                       │
│  ✗ Production incident diagnosis (verify first!)     │
│  ✗ Performance claims without benchmarks             │
└──────────────────────────────────────────────────────┘
```

---

## DevOps Automation with AI

### AI-Enhanced DevOps Workflows

```
┌──────────────────────────────────────────────────────┐
│          AI in the DevOps Pipeline                   │
│                                                      │
│  CODE ──────> BUILD ──────> TEST ──────> DEPLOY     │
│    │            │            │             │         │
│    ▼            ▼            ▼             ▼         │
│  Copilot    AI code       AI test      AI canary    │
│  suggests   quality       generation   analysis     │
│  code       analysis      & review     & rollback   │
│                                                      │
│  MONITOR ──> DETECT ──────> RESPOND ──> IMPROVE     │
│    │            │              │           │         │
│    ▼            ▼              ▼           ▼         │
│  AI anomaly  AI alert       AI runbook  AI post-    │
│  detection   correlation   suggestion  incident     │
│              & noise       & auto-     analysis     │
│              reduction     remediation              │
└──────────────────────────────────────────────────────┘
```

### AI for Incident Response

```python
# FoodExpress: AI-assisted incident analysis

def ai_analyze_incident(logs, metrics, traces):
    """Use AI to analyze incident data and suggest root cause."""

    prompt = f"""
    You are an SRE at FoodExpress analyzing a production incident.

    Recent error logs:
    {logs[-50:]}  # Last 50 log entries

    Key metrics (last 30 min):
    - Error rate: {metrics['error_rate']}%
    - P95 latency: {metrics['p95_latency']}ms
    - CPU usage: {metrics['cpu']}%
    - Memory usage: {metrics['memory']}%
    - DB connections: {metrics['db_connections']}/{metrics['db_max']}

    Recent traces showing errors:
    {traces[:5]}  # 5 error traces

    Analyze and respond with:
    1. Most likely root cause
    2. Confidence level (High/Medium/Low)
    3. Immediate mitigation steps
    4. Verification steps

    Do NOT speculate beyond what the data shows.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3  # Low temperature for factual analysis
    )

    return response.choices[0].message.content
```

---

## AI for Runbook Generation

### Automating Documentation

```
Prompt: "Generate an incident runbook for FoodExpress payment
service returning HTTP 503 errors. Include:
- Alert trigger conditions
- Quick diagnosis steps (5 min)
- Common causes with specific commands to check
- Escalation path
- Verification after fix"

AI Output (then HUMAN REVIEWED):

# Runbook: Payment Service 503 Errors

## Trigger
Alert: PaymentServiceErrors (> 1% 5xx for 5 min)
Dashboard: https://grafana.foodexpress.in/d/payment

## Quick Diagnosis (first 5 minutes)
1. Check pod status:
   kubectl get pods -n foodexpress -l app=payment-service
2. Check recent deployments:
   kubectl rollout history deploy/payment-service
3. Check dependent services:
   curl -s http://payment-service:8080/actuator/health
4. Check database:
   kubectl exec -it mysql-0 -- mysql -e "SHOW PROCESSLIST"

## Common Causes
| Cause | Check Command | Fix |
|-------|--------------|-----|
| OOM Kill | kubectl describe pod <name> | Increase memory limits |
| DB connection pool | Check metrics dashboard | Restart pod / increase pool |
| Bad deployment | Check rollout history | kubectl rollout undo |
| Gateway timeout | Check Razorpay status page | Enable circuit breaker |

CRITICAL: This runbook was AI-generated.
Verify all commands against current infrastructure before use.
```

---

## AI Guardrails and Safety

### Responsible AI Use at FoodExpress

```
┌──────────────────────────────────────────────────────┐
│         AI Safety Guidelines                         │
│                                                      │
│  1. NEVER send sensitive data to AI models           │
│     ✗ Customer PII (names, addresses, phone)        │
│     ✗ Payment information (card numbers, UPI)       │
│     ✗ API keys, passwords, tokens                   │
│     ✗ Internal business metrics                      │
│                                                      │
│  2. ALWAYS review AI-generated code                  │
│     - Check for security vulnerabilities             │
│     - Verify business logic correctness              │
│     - Test edge cases (AI often misses them)         │
│     - Ensure it matches your coding standards        │
│                                                      │
│  3. NEVER deploy AI output directly to production    │
│     - Code review required                           │
│     - Test in staging first                          │
│     - Follow standard change process                 │
│                                                      │
│  4. DOCUMENT AI usage                                │
│     - Note when AI was used in commit messages       │
│     - Track AI-generated vs human-written code       │
│     - Report hallucinations for team learning        │
│                                                      │
│  5. UNDERSTAND limitations                           │
│     - AI can hallucinate (confidently wrong)         │
│     - AI has training data cutoff                    │
│     - AI may suggest deprecated APIs/patterns        │
│     - AI cannot understand your system's context     │
│       without being told                              │
└──────────────────────────────────────────────────────┘
```

---

## Hands-on: AI-Assisted Troubleshooting

### Exercise

```
Scenario: FoodExpress delivery tracking service is showing
stale GPS locations (not updating for 5+ minutes).

Step 1: Use AI to analyze these logs
  [ERROR] WebSocketHandler: Connection pool exhausted
  [WARN]  GPS update rejected: queue full (max: 1000)
  [ERROR] DeliveryTracker: Timeout waiting for GPS update
  [INFO]  Active WebSocket connections: 4,832
  [WARN]  Memory usage: 92% of 512MB limit

Step 2: Ask AI to suggest root cause
  Prompt: "Given these logs, what is the most likely root
  cause of stale GPS data?"

Step 3: Ask AI to suggest a fix
  Prompt: "Suggest a fix for WebSocket connection pool
  exhaustion in a Spring Boot delivery tracking service"

Step 4: CRITICALLY EVALUATE the AI response
  - Does the suggested fix make sense?
  - Are there edge cases the AI missed?
  - Would you deploy this fix as-is?
  - What additional testing would you do?
```

---

## AI for Log Analysis

### Real-World Application

```python
# FoodExpress: AI-powered log analysis for faster MTTR

def analyze_logs_with_ai(log_entries, context):
    """Send structured log data to AI for pattern analysis."""

    # Redact PII before sending to AI
    sanitized_logs = redact_pii(log_entries)

    prompt = f"""
    Context: {context}

    Analyze these application logs and identify:
    1. Error patterns (recurring errors, frequency)
    2. Correlation between events (what triggered what)
    3. Most likely root cause
    4. Recommended investigation steps

    Logs (most recent first):
    {sanitized_logs}

    Format your response as:
    PATTERN: [description]
    CORRELATION: [event A] -> [event B]
    ROOT CAUSE: [most likely cause]
    INVESTIGATE: [step 1], [step 2], [step 3]
    """

    # Call AI with low temperature for factual analysis
    response = call_ai(prompt, temperature=0.2, max_tokens=400)

    # Log the analysis for audit
    log_ai_analysis(response, log_entries)

    return response
```

**Important:** AI log analysis is an ASSISTANT, not a replacement for human investigation.

---

## AI Limitations: What AI Cannot Do

### Know the Boundaries

```
┌──────────────────────────────────────────────────────┐
│  What AI CANNOT Do (Today)                          │
│                                                      │
│  ✗ Understand your system's runtime state           │
│    (It only sees what you paste into the prompt)     │
│                                                      │
│  ✗ Access your monitoring dashboards                │
│    (Unless integrated via API)                       │
│                                                      │
│  ✗ Know about recent changes you didn't mention     │
│    (It has no memory of your deployment history)     │
│                                                      │
│  ✗ Guarantee correctness                            │
│    (It generates statistically likely text)          │
│                                                      │
│  ✗ Replace domain expertise                         │
│    (It doesn't know your business rules)             │
│                                                      │
│  ✗ Make decisions under uncertainty                  │
│    (It gives plausible answers, not necessarily      │
│     the RIGHT answer for YOUR situation)             │
│                                                      │
│  Bottom line: AI is a powerful tool.                │
│  You are the engineer. You make the decisions.      │
└──────────────────────────────────────────────────────┘
```

---

## AI-Assisted Code Review

### Using AI to Review FoodExpress Code

```
Prompt: "Review this FoodExpress payment retry logic for:
1. Resource management issues
2. Error handling gaps
3. Performance concerns
4. Security vulnerabilities"

def process_payment(order_id, amount):
    for attempt in range(3):
        client = HttpClient()     # AI catches: new client each retry
        try:
            response = client.post(
                PAYMENT_URL,
                json={"order_id": order_id, "amount": amount}
            )
            if response.status_code == 200:
                return response.json()
        except Exception:         # AI catches: too broad exception
            time.sleep(1)
    return None                   # AI catches: silent failure

AI identifies:
1. Resource leak: HttpClient created but never closed
2. Too-broad exception catching (hides real errors)
3. Silent failure (returns None instead of raising)
4. No exponential backoff between retries
5. Credentials might be in PAYMENT_URL

Human adds context:
- This is the exact bug that caused the 3-day outage!
- AI correctly identified the resource leak pattern
```

---

## AI Ethics for Engineers

### Responsible AI Principles

| Principle | What It Means | FoodExpress Policy |
|-----------|-------------|-------------------|
| **Transparency** | Users know when AI is involved | "AI-generated" label on menu descriptions |
| **Accountability** | Humans are responsible for AI output | Engineer who deploys AI code owns it |
| **Fairness** | AI doesn't discriminate | Menu recommendations don't exclude cuisines |
| **Privacy** | User data protected | No customer PII in AI prompts |
| **Safety** | AI doesn't cause harm | Output validation on all AI responses |
| **Reliability** | Fallback when AI fails | Default descriptions if AI is unavailable |

```
The Golden Rule of AI in Production:

  A human must be able to understand, verify,
  and override any AI-generated output before
  it affects users or systems.

  AI augments human judgment.
  AI does not replace human judgment.
```

---

## The AI-Augmented Sustain Engineer

### Your Competitive Advantage

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  Sustain Engineer WITHOUT AI:                        │
│  - Manually reads 500 log lines                     │
│  - Takes 30 min to write a runbook                  │
│  - Writes boilerplate code from scratch             │
│  - Searches documentation manually                   │
│                                                      │
│  Sustain Engineer WITH AI:                           │
│  - AI highlights the 5 most relevant log lines      │
│  - AI drafts runbook in 2 min, you refine for 10   │
│  - AI generates boilerplate, you add business logic │
│  - AI summarizes relevant docs, you verify          │
│                                                      │
│  The difference is not AI replacing you.             │
│  The difference is AI making you faster              │
│  so you can focus on what ONLY humans can do:        │
│                                                      │
│  - Understanding business context                    │
│  - Making judgment calls under pressure              │
│  - Building relationships with stakeholders          │
│  - Designing systems that serve real people          │
└──────────────────────────────────────────────────────┘
```

---

## Programme Recap: The Journey

### 47 Days of Sustain Engineering

```
┌──────────────────────────────────────────────────────┐
│  Week 1-2: Foundations                               │
│  HTML/CSS, CSS Frameworks, JavaScript, UI Frameworks │
│                                                      │
│  Week 3-4: Backend                                   │
│  Java, Node.js, Databases                            │
│                                                      │
│  Week 5: QE & Process                                │
│  QE/QC, SDLC, Jira, Integration Project             │
│                                                      │
│  Week 6: DevOps Foundations                          │
│  Git/GitHub, Linux, Apache/Nginx                     │
│                                                      │
│  Week 7: Cloud & Containers                          │
│  Microservices, API, Docker                          │
│                                                      │
│  Week 8: CI/CD & Orchestration                       │
│  Jenkins, Kubernetes, Ansible                        │
│                                                      │
│  Week 9: Observability & SRE                         │
│  Monitoring, SRE Practices, Mid-Stage Project        │
│                                                      │
│  Week 10: ITSM & Completion                          │
│  ITIL, ServiceNow, Final Project, Generative AI      │
└──────────────────────────────────────────────────────┘
```

---

## Programme Recap: Skills Acquired

### From Code to Operations

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  DEVELOPMENT                                         │
│  ☑ HTML/CSS/JS fundamentals                         │
│  ☑ React/Angular frameworks                         │
│  ☑ Java (Spring Boot) backend                       │
│  ☑ Node.js (Express) backend                        │
│  ☑ SQL databases                                    │
│  ☑ REST API design                                  │
│  ☑ Microservices architecture                       │
│                                                      │
│  DEVOPS                                              │
│  ☑ Git version control                              │
│  ☑ Linux system administration                      │
│  ☑ Docker containerization                          │
│  ☑ Kubernetes orchestration                         │
│  ☑ Jenkins CI/CD pipelines                          │
│  ☑ Ansible configuration management                 │
│                                                      │
│  SRE & ITSM                                         │
│  ☑ Prometheus/Grafana monitoring                    │
│  ☑ SLI/SLO/SLA management                          │
│  ☑ Incident/Problem/Change management               │
│  ☑ ServiceNow administration                        │
│  ☑ ITIL 4 practices                                 │
│  ☑ Chaos engineering                                │
│                                                      │
│  AI & MODERN TOOLS                                   │
│  ☑ AI-assisted development                          │
│  ☑ LLM API integration                              │
│  ☑ Responsible AI practices                          │
└──────────────────────────────────────────────────────┘
```

---

## What Makes a Great Sustain Engineer

### The Sustain Engineering Mindset

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  1. EMPATHY FOR THE USER                             │
│     "Every incident is a person who can't order      │
│      their food"                                     │
│                                                      │
│  2. CURIOSITY ABOUT ROOT CAUSES                      │
│     "Don't just fix the symptom -- find the why"     │
│                                                      │
│  3. DISCIPLINE IN PROCESS                            │
│     "Follow the incident process even at 3 AM"       │
│                                                      │
│  4. COURAGE TO ESCALATE                              │
│     "If you don't know, ask. If it's big, escalate"  │
│                                                      │
│  5. OWNERSHIP OF OUTCOMES                            │
│     "The incident isn't over until the post-mortem   │
│      actions are complete"                            │
│                                                      │
│  6. CONTINUOUS LEARNING                              │
│     "Technology changes; the ability to learn         │
│      and adapt is your most valuable skill"           │
│                                                      │
│  You are not just fixing code.                       │
│  You are keeping a business running.                 │
│  Real people depend on the systems you sustain.      │
└──────────────────────────────────────────────────────┘
```

---

## Career Growth Paths

### Where Sustain Engineering Leads

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  Sustain Engineer (you are here)                     │
│       │                                              │
│       ├──> Senior Sustain Engineer                   │
│       │    └──> Technical Lead                       │
│       │         └──> Engineering Manager             │
│       │                                              │
│       ├──> Site Reliability Engineer (SRE)           │
│       │    └──> Senior SRE                           │
│       │         └──> SRE Manager / Director          │
│       │                                              │
│       ├──> DevOps Engineer                           │
│       │    └──> Platform Engineer                    │
│       │         └──> Cloud Architect                 │
│       │                                              │
│       ├──> Full-Stack Developer                      │
│       │    └──> Senior Developer                     │
│       │         └──> Principal Engineer              │
│       │                                              │
│       └──> ITSM Consultant                           │
│            └──> Service Management Lead              │
│                 └──> VP of IT Operations             │
│                                                      │
│  Key: The breadth of skills you've learned opens     │
│  multiple career paths. Choose what excites you.     │
└──────────────────────────────────────────────────────┘
```

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Final Project | Full ITSM lifecycle: Incident > Problem > Change > SLA > Service Catalog > PIR |
| Generative AI | LLMs generate text by predicting next tokens; useful but can hallucinate |
| AI in Frontend | Code generation, bug fixing, testing, accessibility; always review AI output |
| AI in Backend | SQL generation, log analysis, code review, security scanning; verify against schema |
| OpenAI API | System prompt sets behavior; max_tokens controls length; temperature controls creativity |
| Prompt Engineering | Role + Context + Task + Format + Constraints + Examples = effective prompts |
| AI Dev Tools | Copilot, Claude Code, Cursor, ChatGPT; know when each tool is appropriate |
| DevOps + AI | AI for anomaly detection, alert correlation, runbook generation, incident analysis |
| AI Safety | Never send PII to AI; always review output; follow change process for AI-generated code |
| Trust Levels | High trust for boilerplate; low trust for security, finance, compliance code |
| Sustain Mindset | Empathy, curiosity, discipline, courage, ownership, continuous learning |
| Career Paths | Sustain Engineering opens doors to SRE, DevOps, Platform, Full-Stack, ITSM leadership |

---

## Programme Wrap-up

| Week | Topics Covered | Key Achievement |
|------|---------------|-----------------|
| 1-2 | HTML, CSS, JavaScript, UI Frameworks | Built FoodExpress frontend |
| 3-4 | Java, Node.js, Database | Built FoodExpress backend services |
| 5 | QE, SDLC, Jira, Integration | First integration project |
| 6 | Git, Linux, Apache | Infrastructure fundamentals |
| 7 | Microservices, API, Docker | Containerized FoodExpress |
| 8 | Jenkins, Kubernetes, Ansible | CI/CD pipeline and orchestration |
| 9 | Observability, SRE, Mid-Stage | Monitoring and chaos engineering |
| 10 | ITIL, ServiceNow, GenAI, Final | ITSM processes and AI tools |

> **Congratulations! You have completed the Publicis Sapient Sustain Engineering Training Programme. You are now equipped with the skills to maintain, monitor, and improve production systems. Go make an impact!**
