# KEY TAKEAWAY: AI is a force multiplier for SRE workflows.
# This combines everything: system prompts, few-shot, CoT, structured output, chaining.

import json
from config import banner, section, ask_and_print, ask, pause, teaching_point

banner(10, "Real-World SRE: AI Incident Responder",
       "Combining ALL techniques into a production-grade SRE tool")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: Putting it ALL together")
print("""
This module combines EVERYTHING from Modules 1-9:

  Module 1 (Context)        -> Rich incident context provided
  Module 2 (Anatomy)        -> Role + Context + Task + Format + Constraints
  Module 3 (System prompt)  -> SRE persona with runbook knowledge
  Module 5 (Few-shot)       -> Past incidents as examples
  Module 6 (CoT)            -> Step-by-step root cause analysis
  Module 8 (Structured)     -> JSON output for ServiceNow
  Module 9 (Chaining)       -> Multi-step pipeline

We'll build a mini incident response assistant in ~50 lines of Python.
""")

pause(tip="This is the climax — everything connects here. Go slower on this one.")

# ---------------------------------------------------------------------------
# Step 1: The alert fires
# ---------------------------------------------------------------------------
section("STEP 1: Prometheus alert fires at 2:22 AM")

alert = json.load(open("samples/prometheus_alert.json"))
error_log = open("samples/spring_boot_error.log").read()

print(f"  Alert:    {alert['labels']['alertname']}")
print(f"  Service:  {alert['labels']['service']}")
print(f"  Severity: {alert['labels']['severity']}")
print(f"  Summary:  {alert['annotations']['summary']}")
print(f"  Started:  {alert['startsAt']}")
print(f"  5xx Rate: {alert['relatedMetrics']['http_5xx_rate']}")
print(f"  DB Conns: {alert['relatedMetrics']['active_db_connections']}")
print(f"  Memory:   {alert['relatedMetrics']['memory_usage_percent']}%")

teaching_point("""
This is a REAL scenario from your training:
  - Spring Boot service hitting MongoDB
  - Connection pool maxed out
  - Error rate spiking
  - 2 AM. You're on call. Manager is pinging.
""")

pause()

# ---------------------------------------------------------------------------
# Step 2: AI-powered triage
# ---------------------------------------------------------------------------
section("STEP 2: AI-powered triage (few-shot + CoT + JSON)")

SYSTEM_PROMPT = """You are a senior SRE on-call at Publicis Sapient. You have 5 years of
experience with Spring Boot microservices on Kubernetes.

You follow this incident response framework:
1. DETECT: What triggered the alert?
2. TRIAGE: What's the blast radius? Which users are affected?
3. DIAGNOSE: What's the root cause? (use step-by-step reasoning)
4. MITIGATE: What's the immediate fix to stop the bleeding?
5. RESOLVE: What's the permanent fix to prevent recurrence?"""

TRIAGE_PROMPT = f"""A Prometheus alert has fired. Here are two past incidents for reference:

PAST INCIDENT 1:
  Alert: HighErrorRate on payment-service (32% 5xx)
  Root cause: Redis connection pool exhausted due to connection leak in retry logic
  Blast radius: All payment transactions failing, ~2000 users affected
  Immediate fix: Restart payment-service pods (kubectl rollout restart)
  Permanent fix: Added connection pool monitoring + fixed retry logic

PAST INCIDENT 2:
  Alert: HighLatency on order-service (p99 > 10s)
  Root cause: Missing database index on orders.created_at column
  Blast radius: Order listing slow for all users, but no data loss
  Immediate fix: Added index via direct SQL
  Permanent fix: Added index to migration scripts + query monitoring

---

NOW: A new alert has fired. Analyze step by step using the 5-step framework.

ALERT:
{json.dumps(alert, indent=2)}

RECENT LOGS:
{error_log}

After your step-by-step analysis, return a JSON object:
{{
  "incident_severity": "P1|P2|P3|P4",
  "blast_radius": "description of impact",
  "affected_users_estimate": "number or range",
  "root_cause": "one sentence",
  "root_cause_reasoning": ["step 1", "step 2", "step 3"],
  "immediate_mitigation": "what to do RIGHT NOW",
  "permanent_resolution": "what to do THIS WEEK",
  "estimated_recovery_time": "minutes",
  "escalation_needed": true/false
}}

First show your analysis, THEN the JSON."""

print("Sending: alert + logs + 2 past incidents (few-shot) + 5-step framework (CoT)\n")
print("Techniques used:")
print("  [System prompt]    SRE persona with framework")
print("  [Few-shot]         2 past incidents as examples")
print("  [Chain-of-Thought] 5-step DETECT-TRIAGE-DIAGNOSE-MITIGATE-RESOLVE")
print("  [Structured]       JSON output at the end\n")

ask_and_print(TRIAGE_PROMPT, system_msg=SYSTEM_PROMPT, max_tokens=2048, label="AI INCIDENT ANALYSIS")

teaching_point("""
Look at what happened:
  1. The AI used PAST INCIDENTS to calibrate its analysis (few-shot)
  2. It followed the 5-STEP FRAMEWORK (CoT from system prompt)
  3. It produced STRUCTURED JSON (for automation)
  4. All from a SINGLE well-crafted prompt

This took 5 seconds. A manual analysis takes 15-30 minutes.
""")

pause()

# ---------------------------------------------------------------------------
# Step 3: Auto-generate ServiceNow ticket
# ---------------------------------------------------------------------------
section("STEP 3: Auto-generate ServiceNow ticket (prompt chaining)")

TICKET_PROMPT = """Based on this incident analysis, generate a ServiceNow incident ticket.

Analysis:
  Root cause: MongoDB connection pool exhaustion in return-service
  Severity: P1 — 38.7% error rate affecting return/refund processing
  Immediate fix: Scale MongoDB connection pool from 50 to 100

Generate the ticket as JSON matching this ServiceNow schema:
{
  "short_description": "max 160 chars",
  "description": "detailed description with timeline",
  "urgency": "1-high|2-medium|3-low",
  "impact": "1-high|2-medium|3-low",
  "category": "Infrastructure|Application|Database",
  "subcategory": "string",
  "assignment_group": "team name",
  "configuration_item": "service name",
  "work_notes": "initial investigation notes with timeline"
}

Return ONLY the JSON."""

print("Chaining: Taking analysis output -> generating ServiceNow ticket\n")
ticket_json = ask_and_print(TICKET_PROMPT, temperature=0, max_tokens=1024, label="SERVICENOW TICKET")

try:
    ticket = json.loads(ticket_json.strip().strip("```json").strip("```").strip())
    print(f"\n  Ticket Preview:")
    print(f"  ─────────────────────────────")
    print(f"  Title:    {ticket.get('short_description', 'N/A')}")
    print(f"  Urgency:  {ticket.get('urgency', 'N/A')}")
    print(f"  Impact:   {ticket.get('impact', 'N/A')}")
    print(f"  Category: {ticket.get('category', 'N/A')}")
    print(f"  Assigned: {ticket.get('assignment_group', 'N/A')}")
except Exception:
    print("  (Could not parse ticket JSON)")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("KEY LESSON: AI-Augmented SRE")
print("""
In ~50 lines of Python, we built a pipeline that:

  1. Reads a Prometheus alert           (real monitoring data)
  2. Correlates with error logs          (real application logs)
  3. References past incidents           (few-shot learning)
  4. Performs step-by-step diagnosis      (chain-of-thought)
  5. Produces structured analysis        (JSON for automation)
  6. Generates a ServiceNow ticket       (prompt chaining)

This is NOT science fiction. This is achievable TODAY.

BUT REMEMBER (next module!):
  - The AI's analysis needs HUMAN VERIFICATION
  - Use this to AUGMENT your on-call engineers, not REPLACE them
  - AI reduces MTTR by drafting the analysis
  - The HUMAN approves, adjusts, and executes

YOUR 45-DAY TRAINING is what qualifies you to VERIFY the AI's output.
  - You know what good Dockerfiles look like
  - You know what K8s manifests need
  - You know how Jenkins pipelines should be structured
  - You know how ServiceNow tickets should be categorized

  AI generates. YOU verify. THAT is the engineer's role.

Next up: The Dark Side — when AI fails spectacularly.
""")

pause()
