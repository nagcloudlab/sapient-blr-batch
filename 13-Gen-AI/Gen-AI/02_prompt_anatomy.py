# KEY TAKEAWAY: A prompt is an engineering specification, not a conversation.
# Every great prompt has 6 parts: Role, Context, Task, Format, Constraints, Examples.

from config import banner, section, ask_and_print, pause, teaching_point

banner(2, "Anatomy of a Prompt",
       "A prompt is an engineering specification with 6 parts")

# ---------------------------------------------------------------------------
# The 6-Part Framework
# ---------------------------------------------------------------------------
section("THE 6-PART PROMPT FRAMEWORK")
print("""
Every effective prompt has up to 6 parts (not all are always needed):

  1. ROLE        — Who should the AI be? (sets expertise and tone)
  2. CONTEXT     — What does the AI need to know? (background, project details)
  3. TASK        — What exactly should it do? (clear, specific action)
  4. FORMAT      — How should the output look? (JSON, markdown, bullet points)
  5. CONSTRAINTS — What should it NOT do? (boundaries, limitations)
  6. EXAMPLES    — What does good output look like? (few-shot samples)

Think of it like a function signature:

  prompt(role, context, task, format, constraints, examples) -> output
""")

pause(tip="Write these 6 parts on the whiteboard. Students will refer back to them all day.")

# ---------------------------------------------------------------------------
# Demo 1: Task only (what most people do)
# ---------------------------------------------------------------------------
section("DEMO: ATTEMPT 1 — Task only (what most people do)")

k8s_manifest = open("samples/k8s_manifest.yaml").read().split("# PROBLEMS")[0].strip()

task_only = "Review this Kubernetes manifest for issues."
print(f'PROMPT: "{task_only}"\n')

ask_and_print(f"{task_only}\n\n```yaml\n{k8s_manifest}\n```")

teaching_point("""
Generic advice. Inconsistent format. Misses context-specific issues.
Only 1 of the 6 parts used: TASK.
""")

pause(tip="Ask: 'If a senior SRE reviewed this, what would they ask first?' (Answer: What's it for? What traffic? What environment?)")

# ---------------------------------------------------------------------------
# Demo 2: All 6 parts
# ---------------------------------------------------------------------------
section("DEMO: ATTEMPT 2 — Full 6-part prompt")

print("Building the prompt with all 6 parts:\n")
print("  [1] ROLE:        Senior SRE, 10 years experience")
print("  [2] CONTEXT:     Return & Refund service, MongoDB, 500+ req/min, production")
print("  [3] TASK:        Find issues, explain WHY, provide fixes")
print("  [4] FORMAT:      Structured template per issue (severity + impact + fix)")
print("  [5] CONSTRAINTS: K8s only, security first, no app code changes")
print("  [6] EXAMPLES:    (Coming in Module 5 — Few-Shot Prompting)\n")

system_msg = """You are a senior Site Reliability Engineer at Publicis Sapient
with 10 years of experience in Kubernetes production deployments.
You are reviewing code from a junior engineer's capsule project."""  # ROLE

user_msg = f"""CONTEXT:
This is a Kubernetes manifest for a Return & Refund microservice that connects to MongoDB.
It will be deployed in a production namespace serving 500+ requests/minute.
The team uses Helm for templating but this manifest was written manually.

TASK:
Review this manifest and identify all security, reliability, and operational issues.
For each issue, explain WHY it's a problem and provide the corrected YAML snippet.

FORMAT:
For each issue, use this structure:
  **Issue #N: [Title]**
  - Severity: Critical / High / Medium / Low
  - Problem: [1-2 sentences]
  - Impact: [What could go wrong in production]
  - Fix: [corrected YAML snippet]

CONSTRAINTS:
- Do NOT suggest changes to the application code itself
- Focus only on Kubernetes/infrastructure concerns
- Prioritize security issues first, then reliability, then best practices

```yaml
{k8s_manifest}
```"""

ask_and_print(user_msg, system_msg=system_msg)

teaching_point("""
Compare the two outputs:
  Attempt 1: Generic, unstructured, shallow
  Attempt 2: Structured, prioritized, actionable, production-aware

5 of 6 parts used. The only missing part is EXAMPLES (Module 5).
""")

pause()

# ---------------------------------------------------------------------------
# Exercise
# ---------------------------------------------------------------------------
section("STUDENT EXERCISE (2 minutes)")
print("""
Think about a prompt you used in your capsule project.

  1. Which of the 6 parts were present?
  2. Which were missing?
  3. How would you rewrite it using the framework?

The 6 parts again:
  ROLE | CONTEXT | TASK | FORMAT | CONSTRAINTS | EXAMPLES

Next up: System Prompt vs User Prompt — why they're different and
how to use them like a .env file for the AI.
""")

pause()
