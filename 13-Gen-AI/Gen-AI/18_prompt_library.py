# KEY TAKEAWAY: Walk away with a ready-to-use prompt library.
# Copy-paste prompts for every task you'll face as a sustain engineer.

from config import banner, section, ask_and_print, pause, teaching_point

banner(18, "Your Prompt Library: The Engineer's Toolkit",
       "Walk away with copy-paste prompts for every task you'll face")

# ---------------------------------------------------------------------------
# Intro
# ---------------------------------------------------------------------------
section("YOUR TAKEAWAY: A prompt library you can use TOMORROW")
print("""
This is your cheat sheet — battle-tested prompt templates
for every task you'll face as a sustain engineer.

Each template uses the techniques from today:
  - 6-part anatomy (Module 2)
  - System prompts (Module 3)
  - Few-shot examples (Module 5)
  - Chain-of-Thought (Module 6)
  - Structured output (Module 8)
  - RAG context injection (Module 16)

I'll demo each one live so you see the output quality.
Save these. Customize them. Build on them.
""")

pause()

# ===================================================================
# CATEGORY 1: CODE REVIEW
# ===================================================================
section("TEMPLATE 1: Code Review (any language)")

CODE_REVIEW_TEMPLATE = """SYSTEM PROMPT:
You are a senior engineer reviewing code for production readiness.
Follow these standards: [PASTE YOUR TEAM'S CODING STANDARDS HERE]

USER PROMPT:
Review this code for:
1. Security vulnerabilities (OWASP Top 10)
2. Error handling gaps (missing try/catch, unchecked nulls)
3. Performance issues (N+1 queries, unnecessary allocations)
4. Naming and readability
5. Missing edge cases

For each issue found:
  - Severity: CRITICAL / HIGH / MEDIUM / LOW
  - Line: [reference the specific line]
  - Problem: [1 sentence]
  - Fix: [show corrected code]

After the review, give an overall score out of 10 and
list the TOP 3 things to fix first.

```[language]
[PASTE CODE HERE]
```"""

print(CODE_REVIEW_TEMPLATE)

pause(tip="This is the template. Now let's see it in action.")

# Live demo
print("\nLive demo with a real example:\n")

demo_code = """```java
@Service
public class RefundService {
    @Autowired
    MongoTemplate mongo;

    public void processRefund(String orderId, double amount) {
        Order order = mongo.findById(orderId, Order.class);
        order.setStatus("REFUNDED");
        order.setRefundAmount(amount);
        mongo.save(order);

        String cmd = "notify-customer.sh " + order.getEmail();
        Runtime.getRuntime().exec(cmd);
    }
}
```"""

ask_and_print(f"""Review this code for:
1. Security vulnerabilities (OWASP Top 10)
2. Error handling gaps
3. Performance issues
4. Naming and readability
5. Missing edge cases

For each issue: Severity, Line, Problem, Fix (corrected code).
Overall score out of 10 and TOP 3 fixes.

{demo_code}""",
    system_msg="You are a senior engineer reviewing Java code for production readiness.",
    max_tokens=2000, label="CODE REVIEW OUTPUT")

pause()

# ===================================================================
# CATEGORY 2: DEBUGGING
# ===================================================================
section("TEMPLATE 2: Debugging / Error Analysis")

DEBUGGING_TEMPLATE = """SYSTEM PROMPT:
You are a senior debugger specializing in [Spring Boot / Node.js / etc.].
You think step by step and distinguish ROOT CAUSE from SYMPTOMS.

USER PROMPT:
I'm seeing this error in [production/staging/local]:

```
[PASTE ERROR / STACK TRACE HERE]
```

CONTEXT:
- Application: [name, framework, version]
- Recent changes: [what changed recently]
- Frequency: [always / intermittent / first time]
- Environment: [K8s / Docker / local]

Analyze step by step:
1. What is the IMMEDIATE cause of this error?
2. What is the ROOT CAUSE (why did the immediate cause happen)?
3. Is this a SYMPTOM of a deeper issue?
4. What is the QUICK FIX (stop the bleeding)?
5. What is the PROPER FIX (prevent recurrence)?
6. What TESTS should I add to catch this in CI?"""

print(DEBUGGING_TEMPLATE)

pause(tip="Now a live demo with their common error.")

# Live demo
error = """```
org.springframework.dao.DataAccessResourceFailureException: Unable to acquire connection
    at org.springframework.data.mongodb.core.MongoTemplate.execute(MongoTemplate.java:578)
Caused by: com.mongodb.MongoTimeoutException: Timed out after 30000 ms while waiting
    for a server that matches ReadPreferenceServerSelector{readPreference=primary}
```"""

ask_and_print(f"""I'm seeing this error in production:

{error}

CONTEXT:
- Application: return-service, Spring Boot 3.3, Java 17
- Recent changes: Deployed new refund feature 2 hours ago
- Frequency: Intermittent, increasing over last 30 minutes
- Environment: Kubernetes (3 pods, production namespace)

Analyze step by step:
1. IMMEDIATE cause?
2. ROOT CAUSE?
3. Deeper issue?
4. QUICK FIX?
5. PROPER FIX?
6. What TESTS to add?""",
    system_msg="You are a senior debugger specializing in Spring Boot + MongoDB on Kubernetes.",
    max_tokens=1500, label="DEBUGGING OUTPUT")

pause()

# ===================================================================
# CATEGORY 3: GENERATE TESTS
# ===================================================================
section("TEMPLATE 3: Test Generation")

TEST_TEMPLATE = """SYSTEM PROMPT:
You are a QE engineer writing JUnit 5 tests for Spring Boot.
Every test has: Arrange (setup) / Act (execute) / Assert (verify).
Method names: should_[expected]_when_[condition].

USER PROMPT:
Generate tests for this method/class:

```[language]
[PASTE CODE HERE]
```

Generate:
1. Happy path tests (valid inputs, expected outputs)
2. Edge cases (null, empty, boundary values, special characters)
3. Error cases (exceptions, invalid state, timeouts)
4. For each test, add a comment: // WHAT: ... WHY: ...

Use:
- @MockBean for dependencies
- assertThat (AssertJ) for assertions
- @DisplayName for readable test names"""

print(TEST_TEMPLATE)
pause()

# ===================================================================
# CATEGORY 4: INCIDENT RESPONSE
# ===================================================================
section("TEMPLATE 4: Incident Response (on-call)")

INCIDENT_TEMPLATE = """SYSTEM PROMPT:
You are an SRE on-call. Follow the DETECT-TRIAGE-DIAGNOSE-MITIGATE-RESOLVE
framework. Be precise and actionable. Time is critical.

USER PROMPT:
INCIDENT:
  Alert: [alert name]
  Service: [service name]
  Impact: [error rate / latency / downtime]
  Duration: [how long]
  Namespace: [K8s namespace]

AVAILABLE DATA:
  [PASTE: logs, metrics, alert JSON, manifest — whatever you have]

INSTRUCTIONS:
  Step 1: Establish timeline from the data
  Step 2: Identify root cause vs symptoms
  Step 3: Determine blast radius (who is affected?)
  Step 4: Provide IMMEDIATE mitigation (exact commands)
  Step 5: Provide PERMANENT fix (this week)

Return JSON:
{
  "severity": "P1-P4",
  "root_cause": "one sentence",
  "blast_radius": "description",
  "immediate_commands": ["kubectl ...", "curl ..."],
  "permanent_fix": "description",
  "escalation": "who to notify"
}"""

print(INCIDENT_TEMPLATE)
pause()

# ===================================================================
# CATEGORY 5: DEVOPS GENERATION
# ===================================================================
section("TEMPLATE 5: DevOps Config Generation")

DEVOPS_TEMPLATE = """SYSTEM PROMPT:
You are a senior DevOps engineer. Generate production-grade configs.
Standards: non-root containers, health checks, resource limits,
security contexts, no :latest tags, no hardcoded secrets.

USER PROMPT:
Generate a [Dockerfile / K8s manifest / Jenkinsfile / Ansible playbook]
for this application:

  Name: [service name]
  Language: [Java 17 / Node 18 / Python 3.11]
  Framework: [Spring Boot 3.3 / Express.js / FastAPI]
  Port: [8080]
  Health: [/actuator/health]
  Database: [MongoDB / PostgreSQL / Redis]
  Build: [Maven / Gradle / npm]

Requirements:
  [LIST SPECIFIC REQUIREMENTS — multi-stage, non-root, probes, etc.]

Constraints:
  [LIST WHAT NOT TO DO — no :latest, no root, no secrets in image]

Return ONLY the config file — no explanation."""

print(DEVOPS_TEMPLATE)
pause()

# ===================================================================
# CATEGORY 6: DOCUMENTATION
# ===================================================================
section("TEMPLATE 6: Documentation & Communication")

DOC_TEMPLATE = """--- POST-MORTEM ---
SYSTEM: You write blameless post-mortems following Google SRE guidelines.
USER:   Given [incident data], generate a post-mortem with:
        Summary, Impact, Timeline, Root Cause, Action Items (SMART), Lessons Learned.

--- STAKEHOLDER UPDATE ---
SYSTEM: You write incident updates for non-technical stakeholders.
USER:   Given [incident facts], write a 150-word update with:
        Impact (business terms), Status, ETA, Next Update.
        NO technical jargon.

--- PR DESCRIPTION ---
SYSTEM: You write clear, concise PR descriptions.
USER:   Given this diff: [PASTE DIFF]
        Generate: Title (< 70 chars), Summary (3 bullets), Test Plan.

--- ARCHITECTURE DECISION RECORD ---
SYSTEM: You write ADRs following the Nygard template.
USER:   Decision: [what we decided]
        Context: [why we needed to decide]
        Generate: Status, Context, Decision, Consequences (pros/cons).

--- RUNBOOK ---
SYSTEM: You write SRE runbooks that can be followed at 2 AM.
USER:   Service: [name], Alert: [what triggers it]
        Generate: Symptoms, Severity Criteria, Step-by-step Mitigation
        (with exact commands), Verification, Escalation path."""

print(DOC_TEMPLATE)
pause()

# ===================================================================
# CATEGORY 7: LEARNING & GROWTH
# ===================================================================
section("TEMPLATE 7: Learning & Skill Building")

LEARNING_TEMPLATE = """--- EXPLAIN LIKE I'M A JUNIOR ---
"Explain [concept] as if I'm a junior developer who knows Java but
not [specific technology]. Use analogies from everyday life.
Give me 1 example I can run locally in 5 minutes."

--- COMPARE TECHNOLOGIES ---
"Compare [X] vs [Y] for [use case]. Create a table with:
Feature | X | Y | Winner | Why
Include: performance, learning curve, ecosystem, team adoption cost."

--- INTERVIEW PREP ---
"I'm interviewing for a [role]. Ask me 5 progressively harder questions
about [topic]. After each answer, score me and explain what a
perfect answer includes."

--- CODE KATA ---
"Give me a coding challenge related to [topic] at [difficulty] level.
After I solve it, review my solution and suggest optimizations.
Then give me a harder variant."

--- CONCEPT MAP ---
"Create a concept map for [topic] showing how these concepts connect:
[list concepts]. For each connection, explain WHY they're related
with a one-sentence explanation." """

print(LEARNING_TEMPLATE)
pause()

# ===================================================================
# Quick Reference Card
# ===================================================================
section("QUICK REFERENCE: The 6-Part Framework")
print("""
Copy this to your desk. Use it EVERY TIME you write a prompt.

  ┌─────────────────────────────────────────────────────┐
  │           THE 6-PART PROMPT FRAMEWORK               │
  │                                                     │
  │  1. ROLE        Who should the AI be?               │
  │                 "You are a senior SRE..."           │
  │                                                     │
  │  2. CONTEXT     What background does it need?       │
  │                 "This is a Spring Boot service..."  │
  │                                                     │
  │  3. TASK        What exactly should it do?          │
  │                 "Review for security issues..."     │
  │                                                     │
  │  4. FORMAT      How should output look?             │
  │                 "Return JSON with severity, fix..." │
  │                                                     │
  │  5. CONSTRAINTS What should it NOT do?              │
  │                 "No jargon, max 200 words..."       │
  │                                                     │
  │  6. EXAMPLES    What does good output look like?    │
  │                 "Here are 2 examples of our style.."│
  │                                                     │
  │  BONUS TECHNIQUES:                                  │
  │  - "Think step by step" (Chain-of-Thought)          │
  │  - "Return ONLY JSON" (Structured Output)           │
  │  - temperature=0 for consistency                    │
  │  - Inject your docs for team context (RAG)          │
  └─────────────────────────────────────────────────────┘
""")

pause()

# ===================================================================
# Final wrap-up
# ===================================================================
section("FINAL MESSAGE")
print("""
  ╔══════════════════════════════════════════════════════╗
  ║                                                      ║
  ║   YOU NOW HAVE:                                      ║
  ║                                                      ║
  ║   17 modules of prompt engineering techniques        ║
  ║   7 ready-to-use prompt templates                    ║
  ║   A 6-part framework for ANY prompt                  ║
  ║   45 days of knowledge to VERIFY AI output           ║
  ║                                                      ║
  ║   THE EQUATION:                                      ║
  ║                                                      ║
  ║   Your Training  +  Prompt Engineering  =  10x       ║
  ║   (the judgment)    (the speed)            (you)     ║
  ║                                                      ║
  ║   AI doesn't replace engineers.                      ║
  ║   AI replaces engineers who don't use AI.            ║
  ║                                                      ║
  ║   Go build something amazing.                        ║
  ║                                                      ║
  ╚══════════════════════════════════════════════════════╝

  Templates are in this file: 18_prompt_library.py
  Copy them, customize them, make them yours.

  Thank you for 45 incredible days.
  This is just the beginning.
""")
