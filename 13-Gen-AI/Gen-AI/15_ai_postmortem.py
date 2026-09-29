# KEY TAKEAWAY: AI can draft a blameless post-mortem in minutes,
# connecting your SRE + ITSM + communication training into one deliverable.

import json
from config import banner, section, ask_and_print, ask, pause, teaching_point

banner(15, "AI Post-Mortem Writer",
       "From incident data to blameless post-mortem in 60 seconds")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: The post-mortem nobody wants to write")
print("""
After every P1/P2 incident, you need a post-mortem document.

  THE REALITY:
    - It's 4 AM, incident is resolved
    - Everyone is exhausted
    - The post-mortem gets written 3 days later
    - Half the details are forgotten
    - It reads like "stuff happened, we fixed it"

  THE AI-AUGMENTED REALITY:
    - Feed incident data to AI DURING the incident
    - AI drafts the post-mortem in 60 seconds
    - You review and edit while details are fresh
    - Published within hours, not days

This connects THREE parts of your training:
  - SRE:     Incident response, root cause analysis
  - ITSM:    ServiceNow documentation, change management
  - Comms:   Stakeholder communication, blameless culture
""")

pause(tip="Ask: 'Who has written a post-mortem before? What was the hardest part?'")

# ---------------------------------------------------------------------------
# Demo 1: Generate a complete post-mortem
# ---------------------------------------------------------------------------
section("DEMO 1: Generate a blameless post-mortem")

alert = json.load(open("samples/prometheus_alert.json"))
error_log = open("samples/spring_boot_error.log").read()

POSTMORTEM_SYSTEM = """You are a senior SRE at Publicis Sapient writing an incident post-mortem.
You follow Google's SRE post-mortem guidelines:
- BLAMELESS: Never blame individuals. Focus on systems and processes.
- ACTIONABLE: Every finding must have a specific, assigned action item
- HONEST: Don't downplay the impact or gloss over mistakes
- CONSTRUCTIVE: Focus on what to improve, not what went wrong

Use past tense throughout. Be precise with timestamps."""

POSTMORTEM_PROMPT = f"""Generate a complete incident post-mortem document from this data.

INCIDENT DATA:
  Alert: {alert['labels']['alertname']} on {alert['labels']['service']}
  Severity: {alert['labels']['severity']}
  Started: {alert['startsAt']}
  Duration: ~33 minutes (resolved at 14:55 UTC)
  Impact: {alert['annotations']['description']}

METRICS AT PEAK:
  - HTTP 5xx rate: {alert['relatedMetrics']['http_5xx_rate']}
  - p99 latency: {alert['relatedMetrics']['p99_latency_ms']}ms
  - DB connections: {alert['relatedMetrics']['active_db_connections']}
  - Pending DB requests: {alert['relatedMetrics']['pending_db_requests']}
  - Memory usage: {alert['relatedMetrics']['memory_usage_percent']}%

ERROR LOGS:
{error_log}

RESOLUTION STEPS TAKEN:
  1. 14:25 — Alert received, on-call engineer acknowledged
  2. 14:28 — Identified MongoDB connection pool exhaustion from logs
  3. 14:32 — Increased connection pool from 50 to 100 via ConfigMap update
  4. 14:35 — Rolling restart of return-service pods
  5. 14:42 — Error rate dropped to 5%
  6. 14:48 — Error rate returned to baseline (2%)
  7. 14:55 — Incident declared resolved

DOCUMENT FORMAT:
# Incident Post-Mortem: [Title]

## Summary
(3-4 sentences: what happened, impact, duration, resolution)

## Impact
- User-facing impact
- Business impact
- Data integrity impact

## Timeline (UTC)
(Chronological bullet points with timestamps)

## Root Cause Analysis
(Step-by-step technical explanation, blameless)

## Contributing Factors
(What made the incident worse or delayed detection)

## What Went Well
(What worked during the response)

## What Went Wrong
(Process gaps, not people failures)

## Action Items
(Table format)
| # | Action | Owner | Priority | Due Date | Status |
Each action item must be SPECIFIC and MEASURABLE.

## Lessons Learned
(3-5 bullet points)

## Appendix
- Related metrics and dashboards
- ServiceNow ticket reference"""

print("Generating blameless post-mortem from incident data...\n")
ask_and_print(POSTMORTEM_PROMPT, system_msg=POSTMORTEM_SYSTEM, max_tokens=3000,
              label="INCIDENT POST-MORTEM")

teaching_point("""
In 60 seconds, we got a post-mortem that would take 2-3 hours to write.

KEY THINGS TO VERIFY:
  1. Is the timeline accurate? (AI might reorder events)
  2. Are the action items realistic? (AI might suggest impractical fixes)
  3. Is it truly BLAMELESS? (AI sometimes slips into blame language)
  4. Are the "lessons learned" specific to YOUR team?
  5. Does the root cause analysis match your understanding?

The AI drafts it. You make it YOURS.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 2: Generate action items with SMART criteria
# ---------------------------------------------------------------------------
section("DEMO 2: AI-generated SMART action items")

actions_prompt = f"""Based on this incident (MongoDB connection pool exhaustion in return-service),
generate 8 follow-up action items using SMART criteria:
  S - Specific (exactly what to do)
  M - Measurable (how to know it's done)
  A - Assignable (which team/role)
  R - Relevant (directly prevents recurrence)
  T - Time-bound (specific deadline)

Categorize each as:
  - PREVENT:  Stops this exact incident from recurring
  - DETECT:   Catches it faster next time
  - RESPOND:  Improves response process
  - IMPROVE:  General reliability improvement

Format as a table:
| # | Category | Action | Measurable Outcome | Owner | Deadline |"""

print("Generating SMART action items...\n")
ask_and_print(actions_prompt, max_tokens=1500, label="SMART ACTION ITEMS")

teaching_point("""
Action items are the MOST IMPORTANT part of a post-mortem.

BAD action item:  "Improve monitoring"
  - Not specific, not measurable, no owner, no deadline

GOOD action item: "Add Grafana alert for MongoDB connection pool
  utilization > 80%, targeting production namespace, assigned to
  Platform team, due by Oct 5, verified by triggering test alert"
  - Specific, measurable, assigned, relevant, time-bound

The AI generates the structure. YOU verify relevance and assign owners.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 3: Generate a stakeholder summary from the post-mortem
# ---------------------------------------------------------------------------
section("DEMO 3: Executive summary for leadership")

exec_prompt = """Convert this incident post-mortem into a 100-word executive summary
for the VP of Engineering who doesn't know what MongoDB or Kubernetes means.

INCIDENT FACTS:
- Return & Refund processing was partially unavailable for 33 minutes
- ~39% of refund requests failed during the window
- No data was lost; all failed requests can be retried
- Root cause: database capacity was undersized for current traffic
- Fix: increased capacity and added monitoring
- 8 action items assigned to prevent recurrence

FORMAT:
  Subject line + 3 short paragraphs:
    1. What happened (business impact)
    2. What we did (resolution)
    3. What we're doing to prevent it (action items summary)

RULES:
  - Zero technical jargon
  - Acknowledge the impact honestly
  - Show confidence in prevention plan
  - Include timeline for completion of fixes"""

print("Converting technical post-mortem to executive summary...\n")
ask_and_print(exec_prompt, max_tokens=500, label="EXECUTIVE SUMMARY")

teaching_point("""
THREE AUDIENCES, THREE DOCUMENTS, ONE INCIDENT:

  1. Technical post-mortem  -> Engineering team (root cause, fixes, code)
  2. SMART action items     -> Project manager (tracking, deadlines)
  3. Executive summary      -> VP/Client (business impact, confidence)

AI generated all three from the SAME incident data.
You just changed the SYSTEM PROMPT and CONSTRAINTS.

This is Module 3 (System Prompts) applied to real SRE work.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 4: ServiceNow change request from action items
# ---------------------------------------------------------------------------
section("DEMO 4: Auto-generate ServiceNow change request")

change_prompt = """Based on the post-mortem action item "Increase MongoDB connection pool
from 50 to 100 and add connection utilization monitoring", generate a
ServiceNow Change Request in JSON format:

{
  "short_description": "max 160 chars",
  "description": "detailed description of the change",
  "type": "Standard|Normal|Emergency",
  "category": "Infrastructure|Application|Database",
  "risk": "High|Medium|Low",
  "impact": "High|Medium|Low",
  "implementation_plan": "step-by-step plan",
  "backout_plan": "rollback steps if change fails",
  "test_plan": "how to verify the change worked",
  "change_window": "suggested maintenance window",
  "approvals_needed": ["list of approvers"]
}

Return ONLY the JSON."""

print("Generating ServiceNow change request from action item...\n")
result = ask_and_print(change_prompt, temperature=0, max_tokens=1024, label="CHANGE REQUEST")

try:
    cr = json.loads(result.strip().strip("```json").strip("```").strip())
    print(f"\n  Change Request Preview:")
    print(f"  ───────────────────────────")
    print(f"  Title:    {cr.get('short_description', 'N/A')}")
    print(f"  Type:     {cr.get('type', 'N/A')}")
    print(f"  Risk:     {cr.get('risk', 'N/A')}")
    print(f"  Window:   {cr.get('change_window', 'N/A')}")
except Exception:
    print("  (JSON preview unavailable)")

teaching_point("""
FULL INCIDENT LIFECYCLE powered by AI:

  Prometheus Alert
    -> AI Triage (Module 10)
      -> AI Post-Mortem (this module)
        -> AI Action Items (SMART)
          -> AI Change Request (ServiceNow)
            -> AI Executive Summary (stakeholders)

Each step uses a DIFFERENT prompt technique:
  Triage:     Few-shot + CoT + structured output
  Post-mortem: System prompt (blameless culture) + format template
  Actions:    Constraints (SMART criteria)
  Change req: Structured output (JSON schema)
  Exec summary: Constraints (no jargon, 100 words)

Your 45-day training gave you the JUDGMENT to verify each output.
AI gave you the SPEED to produce them in minutes instead of days.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("THE COMPLETE PICTURE")
print("""
Over 15 modules, you've learned to:

  TECHNIQUES (Modules 1-9):
    Context, Anatomy, System Prompts, Zero/Few-Shot,
    Chain-of-Thought, Self-Consistency, Structured Output, Chaining

  APPLICATIONS (Modules 10-15):
    Incident Response, Hallucination Detection, Prompt Challenges,
    Code Review, Test Generation, Post-Mortem Writing

  THE THREAD: Every module builds on the previous.
    Module 2's 6-part framework appears in EVERY subsequent module.
    Module 3's system prompts power EVERY persona.
    Module 8's structured output enables EVERY integration.

  THE THESIS: AI is the most powerful tool you'll ever use.
    But a tool is only as good as the engineer wielding it.
    Your 45-day training is your competitive advantage.

    AI generates. You verify. That is the engineer's role.
""")

pause()
