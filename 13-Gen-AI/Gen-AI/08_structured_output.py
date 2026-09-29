# KEY TAKEAWAY: AI output must be machine-parseable for real systems.
# Free-text is for humans. JSON is for pipelines.

import json
from config import banner, section, ask_and_print, ask, pause, teaching_point, openai_client, OPENAI_MODEL

banner(8, "Structured Output Engineering",
       "AI output must be machine-parseable — JSON, not prose")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: Why structured output matters")
print("""
When you use ChatGPT in the browser, free-text is fine — you READ it.

But in production systems:
  - Your Jenkins pipeline needs to PARSE the AI's output
  - Your monitoring dashboard needs to CHART it
  - Your ServiceNow integration needs to FILL ticket fields

Free-text = conversations.  JSON = pipelines.

TWO APPROACHES:
  1. Prompt engineering:  "Return ONLY valid JSON matching this schema..."
  2. API feature:         response_format={"type": "json_object"}
""")

pause(tip="Connect to their ServiceNow training — structured data is how systems talk to each other.")

# ---------------------------------------------------------------------------
# Demo 1: Prompt-based JSON
# ---------------------------------------------------------------------------
section("DEMO 1: Prompt-based JSON enforcement")

error_log = open("samples/spring_boot_error.log").read()

prompt = f"""Analyze this error log and return a JSON object matching this EXACT schema.
Return ONLY the JSON — no markdown, no explanation, no code fences.

Schema:
{{
  "incident_id": "auto-generated string",
  "timestamp": "ISO 8601 of first error",
  "service": "affected service name",
  "severity": "P1|P2|P3|P4",
  "root_cause": "one sentence",
  "affected_components": ["list of components"],
  "error_count": number,
  "metrics": {{
    "active_connections": "current/max",
    "pending_requests": number
  }},
  "immediate_action": "one sentence",
  "long_term_fix": "one sentence",
  "servicenow_category": "Infrastructure|Application|Database|Network",
  "servicenow_subcategory": "string"
}}

Error log:
{error_log}"""

print("PROMPT: 'Analyze this log, return ONLY JSON matching this schema...'\n")
result = ask_and_print(prompt, max_tokens=1024, label="Prompt-based JSON")

try:
    parsed = json.loads(result.strip().strip("```json").strip("```").strip())
    print(f"\n  [PASS] Valid JSON with {len(parsed)} fields")
except json.JSONDecodeError as e:
    print(f"\n  [FAIL] NOT valid JSON: {e}")

teaching_point("""
Even with "Return ONLY JSON", models sometimes add markdown fences
or explanations. That's why we strip them in code.
In production, ALWAYS validate the output before using it.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 2: OpenAI native JSON mode
# ---------------------------------------------------------------------------
section("DEMO 2: OpenAI's native JSON mode (API feature)")

print("OpenAI has a built-in response_format parameter that GUARANTEES valid JSON:\n")
print('  response_format={"type": "json_object"}\n')

response = openai_client.chat.completions.create(
    model=OPENAI_MODEL,
    temperature=0.3,
    max_tokens=1024,
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": "You return structured JSON for incident management."},
        {"role": "user", "content": prompt},
    ],
)
native_json = response.choices[0].message.content
print(native_json)

try:
    parsed = json.loads(native_json)
    print(f"\n  [PASS] Native JSON mode: valid JSON, {len(parsed)} fields")
except json.JSONDecodeError as e:
    print(f"\n  [FAIL] {e}")

pause()

# ---------------------------------------------------------------------------
# Demo 3: Using the output programmatically
# ---------------------------------------------------------------------------
section("DEMO 3: Using structured output in a pipeline")

print("Now we USE this data — just like any API response:\n")

try:
    data = json.loads(native_json)
    print("  ServiceNow Ticket Draft (auto-generated):")
    print("  ───────────────────────────────────────────")
    print(f"  Category:     {data.get('servicenow_category', 'N/A')}")
    print(f"  Subcategory:  {data.get('servicenow_subcategory', 'N/A')}")
    print(f"  Severity:     {data.get('severity', 'N/A')}")
    print(f"  Service:      {data.get('service', 'N/A')}")
    print(f"  Root Cause:   {data.get('root_cause', 'N/A')}")
    print(f"  Action:       {data.get('immediate_action', 'N/A')}")
    print(f"  Affected:     {', '.join(data.get('affected_components', []))}")
except Exception as e:
    print(f"  Could not parse: {e}")

teaching_point("""
This is the BRIDGE between AI and your existing systems:

  AI + JSON + ServiceNow API = Auto-generated incident tickets
  AI + JSON + Grafana API    = Auto-annotated dashboards
  AI + JSON + Slack API      = Formatted alert notifications
  AI + JSON + Jenkins API    = Triggered remediation pipelines

THIS is how AI enters your CI/CD pipeline — through structured output.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("PRODUCTION CHECKLIST FOR STRUCTURED OUTPUT")
print("""
  1. Always provide the EXACT schema you expect
  2. Say "Return ONLY JSON" — models love to add explanations
  3. Use native JSON mode when available (response_format)
  4. ALWAYS validate/parse output — never trust raw strings
  5. Use Pydantic or JSON Schema for validation in production
  6. Have a fallback for when parsing fails (retry or default)

Next up: Prompt Chaining — building multi-step AI pipelines,
like microservices for prompts.
""")

pause()
