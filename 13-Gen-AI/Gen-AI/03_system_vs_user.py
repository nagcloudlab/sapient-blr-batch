# KEY TAKEAWAY: System prompt = configuration. User prompt = input.
# Same user message, different system prompts → completely different outputs.

from config import banner, section, ask_and_print, pause, teaching_point

banner(3, "System Prompt vs User Prompt",
       "System prompt is like a .env file — it configures the AI's behavior")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: Two types of messages")
print("""
Every API call has TWO types of messages:

  SYSTEM PROMPT — Sets behavior, persona, rules (invisible to the "user")
                  Like configuring an application via environment variables.
                  Persistent across the conversation.

  USER PROMPT   — The actual question or task.
                  Like a request hitting your API endpoint.

  system_prompt = "You are a code reviewer"   # .env / application.yml
  user_prompt   = "Review this Dockerfile"     # HTTP request body

Key insight: When you type into ChatGPT, you're ONLY writing user prompts.
The system prompt is hidden and generic.
When you use the API, YOU control BOTH.
""")

pause(tip="This is the 'aha' moment — they've never controlled the system prompt before.")

# ---------------------------------------------------------------------------
# Demo: Same Dockerfile, 3 different system prompts
# ---------------------------------------------------------------------------
dockerfile = open("samples/broken_dockerfile").read().split("# PROBLEMS")[0].strip()
USER_MSG = f"Review this Dockerfile:\n\n```dockerfile\n{dockerfile}\n```"

# --- Persona 1: Security Auditor ---
section("PERSONA 1: Security Auditor")
sys1 = """You are a container security auditor performing a compliance review.
Your job is to identify security vulnerabilities and CIS benchmark violations.
Rate each finding as CRITICAL, HIGH, MEDIUM, or LOW.
You only care about security — ignore performance and best practices."""

print(f"SYSTEM PROMPT:\n  {sys1}\n")
print(f"USER PROMPT:\n  Review this Dockerfile (same for all 3 personas)\n")

ask_and_print(USER_MSG, system_msg=sys1, label="PERSONA 1: Security Auditor")

teaching_point("""
Notice: The AI ONLY talks about security.
It ignores image size, build speed, everything else.
The system prompt CONSTRAINED its perspective.
""")

pause(tip="Ask: 'What did the security auditor focus on? What did it ignore?'")

# --- Persona 2: Performance Engineer ---
section("PERSONA 2: Performance Engineer")
sys2 = """You are a performance engineer optimizing Docker images for a Kubernetes cluster
with limited resources. Your only concern is image size, build speed, and runtime efficiency.
You do NOT care about security — only performance and resource usage.
Suggest specific size reduction techniques with estimated savings."""

print(f"SYSTEM PROMPT:\n  {sys2}\n")
print("USER PROMPT: Same Dockerfile!\n")

ask_and_print(USER_MSG, system_msg=sys2, label="PERSONA 2: Performance Engineer")

teaching_point("""
SAME Dockerfile, COMPLETELY different review.
Now it talks about image size, Alpine, multi-stage builds.
Zero mention of security.
""")

pause(tip="Ask: 'Same Dockerfile — why is the review totally different?'")

# --- Persona 3: Junior Developer Mentor ---
section("PERSONA 3: Mentor for Junior Developers")
sys3 = """You are a patient senior developer mentoring a junior engineer on their first
Dockerfile. Explain issues in simple terms with analogies. Don't overwhelm them —
pick the TOP 3 most important issues only. For each issue, explain:
1. What's wrong (in plain English, no jargon)
2. Why it matters (use a real-world analogy)
3. How to fix it (show the corrected code)"""

print(f"SYSTEM PROMPT:\n  {sys3}\n")
print("USER PROMPT: Same Dockerfile!\n")

ask_and_print(USER_MSG, system_msg=sys3, label="PERSONA 3: Junior Mentor")

teaching_point("""
Now it's gentle, uses analogies, limits to 3 issues.
The TONE changed because the PERSONA changed.
Same AI. Same Dockerfile. Three completely different reviews.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("KEY LESSON: The System Prompt is Your Superpower")
print("""
Three personas, one Dockerfile:

  Security Auditor     -> CIS violations, root user, no USER instruction
  Performance Engineer -> Image bloat, no multi-stage, JDK vs JRE, ~300MB savings
  Junior Mentor        -> Top 3 only, analogies, gentle tone

It's not about WHAT you ask — it's about WHO you configure the AI to be.

REAL-WORLD APPLICATIONS:
  - Code review bot:     System prompt = your team's coding standards
  - Incident assistant:  System prompt = your runbook + escalation policy
  - Doc generator:       System prompt = your company's documentation format
  - Onboarding buddy:    System prompt = your tech stack + team conventions

The system prompt is the most UNDERUSED feature in AI.
Most people never touch it. Now you know better.
""")

pause()
