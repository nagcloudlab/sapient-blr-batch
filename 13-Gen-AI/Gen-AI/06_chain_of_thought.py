# KEY TAKEAWAY: Chain-of-Thought makes AI show its work — like requiring
# engineers to explain their reasoning in a PR, not just the conclusion.

from config import banner, section, ask_and_print, pause, teaching_point

banner(6, "Chain-of-Thought (CoT) Prompting",
       "Make the AI show its work — reasoning before conclusion")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: What is Chain-of-Thought?")
print("""
CHAIN-OF-THOUGHT = Ask the AI to reason step-by-step before answering.

Without CoT:  "What's wrong with this pipeline?"  -> "Missing tests, no scanning"
With CoT:     "Think step by step..."             -> WHY each issue matters,
                                                     HOW they're connected,
                                                     ROOT CAUSE, not just symptoms

ANALOGY:
  Without CoT = A doctor saying "You have a cold"
  With CoT    = A doctor explaining symptoms -> differential diagnosis -> conclusion

WHY IT MATTERS:
  1. CoT catches issues that flat prompts MISS
  2. CoT reveals REASONING so YOU can verify it
  3. CoT produces AUDITABLE answers (critical for SRE post-mortems)
""")

pause(tip="Ask: 'In a PR review, do you want just the verdict, or the reasoning too?'")

# ---------------------------------------------------------------------------
# Demo 1: WITHOUT CoT
# ---------------------------------------------------------------------------
section("DEMO 1: WITHOUT Chain-of-Thought")

jenkins = open("samples/jenkins_pipeline.groovy").read().split("// PROBLEMS")[0].strip()

prompt_no_cot = f"""What are the issues with this Jenkins pipeline?

```groovy
{jenkins}
```"""

print("PROMPT: 'What are the issues with this pipeline?'\n")
ask_and_print(prompt_no_cot, label="WITHOUT CoT — flat list")

teaching_point("""
You get a LIST of issues. Fine for a quick scan.
But: Which issue is most critical? How do they connect?
What's the ROOT CAUSE pattern? You can't tell.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 2: WITH CoT
# ---------------------------------------------------------------------------
section("DEMO 2: WITH Chain-of-Thought — same pipeline")

prompt_with_cot = f"""Analyze this Jenkins pipeline step by step.

For EACH stage in the pipeline, think through:
1. What is this stage doing?
2. What could go wrong in production?
3. What safety nets are missing?
4. How does a failure here cascade to downstream stages?

After analyzing all stages, provide:
- The SINGLE most critical issue (the one that would wake you up at 2 AM)
- The root cause pattern across all issues
- A prioritized remediation plan (fix order matters)

```groovy
{jenkins}
```"""

print("PROMPT: 'Analyze step by step... what could go wrong... how failures cascade...'\n")
ask_and_print(prompt_with_cot, label="WITH CoT — step-by-step analysis")

teaching_point("""
Night and day difference:
  WITHOUT CoT: "Here are 5 issues" (a grocery list)
  WITH CoT:    "Stage 2 skips tests, which means Stage 3 pushes
                untested code, which means Stage 4 deploys it to
                production with no safety net" (a ROOT CAUSE ANALYSIS)

CoT reveals the CASCADE — how one gap leads to the next.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 3: CoT for incident debugging
# ---------------------------------------------------------------------------
section("DEMO 3: CoT for incident root-cause analysis")

error_log = open("samples/spring_boot_error.log").read()

prompt_incident_cot = f"""You are an SRE responding to a production incident at 2 AM.
Analyze these logs step by step:

Step 1: Read each log line and identify what component produced it
Step 2: Establish the TIMELINE — what happened first, second, third?
Step 3: Identify which error is the ROOT CAUSE vs which are SYMPTOMS
Step 4: Explain the cascade — how did the root cause trigger each subsequent error?
Step 5: Suggest the IMMEDIATE fix (stop the bleeding) vs the LONG-TERM fix (prevent recurrence)

```
{error_log}
```"""

print("PROMPT: 'Analyze these production logs step by step...'\n")
ask_and_print(prompt_incident_cot, label="CoT Incident Analysis")

teaching_point("""
THIS is how you use AI for on-call incident response:
  - Step-by-step prevents the AI from jumping to conclusions
  - Separating ROOT CAUSE from SYMPTOMS is critical
  - IMMEDIATE vs LONG-TERM fix = what the manager needs to hear

And because the reasoning is visible, you can AUDIT it.
If Step 3 is wrong, you know the conclusion is wrong too.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("WHEN TO USE CoT")
print("""
USE CoT when:
  - Debugging production incidents (root cause analysis)
  - Reviewing complex code (how components interact)
  - Making architectural decisions (trade-off analysis)
  - Writing post-mortems (timeline + causation)
  - Anything where you need AUDITABLE reasoning

SKIP CoT when:
  - Simple classification tasks (log level, sentiment)
  - Code generation with clear specs
  - Format conversion (JSON to YAML)

CoT MAGIC PHRASES:
  "Think step by step"
  "Analyze each component before concluding"
  "First identify X, then determine Y, finally recommend Z"
  "Separate root cause from symptoms"

Next up: Self-Consistency — what happens when AI gives different
answers to the same question?
""")

pause()
