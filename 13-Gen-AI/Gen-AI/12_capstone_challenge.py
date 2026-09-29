# KEY TAKEAWAY: The engineer's skill is in the QUESTION, not the answer.
# This challenge scores YOUR prompts, not the AI's output.

from config import banner, section, ask_and_print, pause, teaching_point

banner(12, "Capstone Challenge: Incident Response",
       "Your skill is in the QUESTION — craft the perfect prompts")

# ---------------------------------------------------------------------------
# The Scenario
# ---------------------------------------------------------------------------
section("THE SCENARIO: Production is on fire")

print("""
It's 2:47 AM. You're on-call. Your phone buzzes:

  CRITICAL: return-service error rate 38.7% (threshold: 25%)
  Duration: 12 minutes and counting
  Namespace: production
  Team: sustain-engineering

Your monitoring dashboard shows:
  - MongoDB connections: 50/50 (maxed out)
  - Pending requests: 23 and growing
  - Memory usage: 87.3%
  - Pod restarts: 0 (not crashing — STUCK)
  - p99 latency: 12.4 seconds (normal: 200ms)

Your manager pings: "What's the status? The client is asking."

You have AI to help — but the AI is only as good as YOUR prompts.

CHALLENGE: Write prompts for 3 phases of incident response.
The quality of YOUR prompts determines the quality of help you get.
""")

pause(tip="Give students 1 minute to absorb the scenario. Ask: 'What would you do first?'")

# ---------------------------------------------------------------------------
# Phase 1: Diagnosis
# ---------------------------------------------------------------------------
section("PHASE 1: DIAGNOSE — What's the root cause? (3 minutes)")

print("""
WRITE A PROMPT to diagnose the root cause.

Available data:
  - Prometheus alert (samples/prometheus_alert.json)
  - Application logs (samples/spring_boot_error.log)
  - K8s manifest (samples/k8s_manifest.yaml)

SCORING RUBRIC (10 points):
  [2 pts] System prompt with SRE persona and context?
  [2 pts] ALL relevant data provided (alert + logs + manifest)?
  [2 pts] Step-by-step reasoning requested (CoT)?
  [2 pts] Structured output (JSON) requested?
  [2 pts] Constraints set (scope, priorities)?

EXAMPLE — BAD PROMPT (2/10):
  "What's wrong with my service?"

EXAMPLE — GOOD PROMPT (8/10):
  [System] "You are a senior SRE with Spring Boot + MongoDB + K8s expertise..."
  [User]   "Given this alert, logs, and manifest, analyze step by step:
            1. Timeline of events
            2. Root cause vs symptoms
            3. Blast radius
            Return JSON with severity, root_cause, affected_components..."

Take 3 minutes. Write your prompt.
""")

pause(tip="Walk around and look at what students write. Pick a good and bad example to discuss.")

# ---------------------------------------------------------------------------
# Reference solution Phase 1
# ---------------------------------------------------------------------------
section("REFERENCE SOLUTION: Phase 1")

alert_data = open("samples/prometheus_alert.json").read()
error_log = open("samples/spring_boot_error.log").read()
k8s_manifest = open("samples/k8s_manifest.yaml").read().split("# PROBLEMS")[0].strip()

diag_system = """You are a senior SRE at Publicis Sapient with deep expertise in:
- Spring Boot 3.x microservices with MongoDB
- Kubernetes production operations
- Prometheus/Grafana monitoring stack
You are responding to a P1 incident at 2:47 AM. Be precise and actionable."""

diag_user = f"""A critical alert has fired. Perform a step-by-step root cause analysis.

STEP 1: Read the alert and establish what threshold was breached
STEP 2: Read the logs chronologically — what happened first?
STEP 3: Cross-reference the K8s manifest — are there missing safeguards?
STEP 4: Identify ROOT CAUSE vs SYMPTOMS (they are different!)
STEP 5: Determine blast radius — who is affected and how badly?

PROMETHEUS ALERT:
{alert_data}

APPLICATION LOGS:
{error_log}

KUBERNETES MANIFEST:
```yaml
{k8s_manifest}
```

After your analysis, return JSON:
{{
  "severity": "P1|P2|P3|P4",
  "root_cause": "one sentence",
  "symptoms": ["list of symptoms that are NOT the root cause"],
  "blast_radius": "who is affected",
  "timeline": ["event 1 at time X", "event 2 at time Y"],
  "contributing_factors": ["K8s misconfigurations that made it worse"]
}}"""

print("Reference prompt uses:")
print("  [1] ROLE:        Senior SRE persona (system prompt)")
print("  [2] CONTEXT:     All 3 data sources")
print("  [3] TASK:        5-step CoT framework")
print("  [4] FORMAT:      Explicit JSON schema")
print("  [5] CONSTRAINTS: ROOT CAUSE vs SYMPTOMS separation\n")

ask_and_print(diag_user, system_msg=diag_system, max_tokens=2048, label="REFERENCE DIAGNOSIS")

pause()

# ---------------------------------------------------------------------------
# Phase 2: Mitigation
# ---------------------------------------------------------------------------
section("PHASE 2: MITIGATE — Stop the bleeding (3 minutes)")

print("""
WRITE A PROMPT to get IMMEDIATE mitigation steps.
You need something executable in the NEXT 5 MINUTES.

SCORING RUBRIC (10 points):
  [2 pts] Provided the diagnosis from Phase 1 as context?
  [2 pts] Specified urgency (immediate, not long-term)?
  [2 pts] Asked for executable commands (not just advice)?
  [2 pts] Included rollback as an option?
  [2 pts] Requested risk assessment for each action?

Take 3 minutes. Write your prompt.
""")

pause(tip="Remind them: 'Your manager is waiting. The client is asking. Be specific.'")

section("REFERENCE SOLUTION: Phase 2")

mit_prompt = """Based on this diagnosis:
- Root cause: MongoDB connection pool exhaustion (50/50 connections, 23 pending)
- Service: return-service in production namespace
- Impact: 38.7% error rate, refund processing failing
- Duration: 12+ minutes

I need IMMEDIATE mitigation steps I can execute in the next 5 minutes.
For EACH step, provide:
1. The exact kubectl/shell command to run
2. What it does in plain English
3. Risk level (safe/moderate/risky)
4. Rollback command if something goes wrong

Prioritize: stop the bleeding FIRST, then stabilize.
Do NOT include long-term fixes — only immediate actions.
Include a "nuclear option" (full rollback) as the last resort."""

ask_and_print(mit_prompt, system_msg=diag_system, max_tokens=2048, label="REFERENCE MITIGATION")

pause()

# ---------------------------------------------------------------------------
# Phase 3: Communication
# ---------------------------------------------------------------------------
section("PHASE 3: COMMUNICATE — Update stakeholders (3 minutes)")

print("""
Your manager asked: "What's the status? The client is asking."

WRITE A PROMPT to generate a stakeholder update.

SCORING RUBRIC (10 points):
  [2 pts] Specified audience (non-technical management)?
  [2 pts] Included timeline, impact, status, next steps?
  [2 pts] Set format (Subject + structured body)?
  [2 pts] Constrained jargon (no MongoDB, no pods, no K8s)?
  [2 pts] Set word limit and tone?

This is the MOST IMPORTANT prompt in production:
  Engineers fix systems. COMMUNICATION fixes trust.

Take 3 minutes. Write your prompt.
""")

pause()

section("REFERENCE SOLUTION: Phase 3")

comm_prompt = """Write a concise incident status update for non-technical stakeholders.

INCIDENT FACTS:
- Service: Return & Refund processing system
- Started: 2:22 AM UTC, September 28
- Current time: 2:55 AM UTC
- Impact: ~39% of return/refund requests are failing
- Root cause: Database connection capacity exceeded
- Status: Mitigation in progress (scaling connection pool)
- No data loss has occurred
- Users see "Service temporarily unavailable" when affected

FORMAT:
  Subject: [P1] Return Service Incident — Status Update #1
  Body:
    Impact: (1 sentence, business terms, no jargon)
    Timeline: (bullet points, simple language)
    Current Status: (what we're doing NOW)
    ETA: (when we expect resolution)
    Next Update: (when they'll hear from us again)

CONSTRAINTS:
  - NO technical jargon (no "MongoDB", "connection pool", "pods")
  - Write for a VP who doesn't know what Kubernetes is
  - Be honest about uncertainty in ETA
  - Maximum 150 words"""

ask_and_print(comm_prompt, max_tokens=512, label="REFERENCE COMMUNICATION")

pause()

# ---------------------------------------------------------------------------
# Final scoring and wrap-up
# ---------------------------------------------------------------------------
section("FINAL SCORING & WRAP-UP")

print("""
Total: 30 points across 3 phases

  Phase 1 — Diagnose:     /10  (CoT + structured + all data)
  Phase 2 — Mitigate:     /10  (executable + rollback + risk)
  Phase 3 — Communicate:  /10  (audience + no jargon + format)
                         ─────
  Your Total:             /30

  25-30:  Ready to build AI-augmented SRE tools
  18-24:  Solid understanding — practice the 6-part framework
  10-17:  Review Modules 2 and 6 — they're your foundation
   0-9:   Re-run the demos, focus on the 6-part framework


THE FINAL MESSAGE:

  The AI gave the SAME model to everyone in this room.
  The difference in output quality came from YOUR PROMPTS.

  Modules 1-9 gave you the TECHNIQUES:
    Context, Anatomy, System Prompts, Zero-shot, Few-shot,
    Chain-of-Thought, Self-Consistency, Structured Output, Chaining

  Module 10 showed you the INTEGRATION:
    All techniques combined into a real SRE workflow

  Module 11 showed you the DANGER:
    AI hallucinates. AI fabricates. AI lies with confidence.

  Module 12 proved the THESIS:
    The engineer's skill is in the QUESTION, not the answer.

  Your 45-day training + today's session = your competitive edge.

  AI is the most powerful tool you'll ever use.
  But a tool is only as good as the engineer wielding it.

  Welcome to the age of AI-augmented engineering.
""")
