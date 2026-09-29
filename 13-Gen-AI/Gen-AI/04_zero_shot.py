# KEY TAKEAWAY: Zero-shot is direct instruction without examples.
# It works for well-defined tasks but fails when YOUR standards matter.

from config import banner, section, ask_and_print, pause, teaching_point

banner(4, "Zero-Shot Prompting",
       "Direct instruction without examples — simple but limited")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: What is Zero-Shot?")
print("""
ZERO-SHOT = Give the AI a task with NO examples of desired output.
You rely entirely on the AI's pre-trained knowledge.

  "Translate this to French: Hello"        <- Zero-shot (works great)
  "Classify this log as error/warn/info"   <- Zero-shot (works great)
  "Review this code for OUR team's style"  <- Zero-shot (fails! AI doesn't know YOUR style)

It's called "zero-shot" because you give ZERO examples.

  WORKS WELL FOR:   Universal tasks with clear right/wrong answers
  FAILS FOR:        Tasks needing YOUR domain knowledge, YOUR conventions
""")

pause(tip="Ask: 'Can you think of a task where zero-shot would fail?'")

# ---------------------------------------------------------------------------
# Demo 1: Zero-shot SUCCESS
# ---------------------------------------------------------------------------
section("DEMO 1: Zero-shot SUCCESS — well-defined task")

prompt1 = """Classify each log line as ERROR, WARN, or INFO:

1. 2026-09-28 Failed to acquire connection from pool
2. 2026-09-28 Application started on port 8080
3. 2026-09-28 Connection pool health check failed, Active: 50/50
4. 2026-09-28 MongoDB health check FAILED — connection pool exhausted
5. 2026-09-28 Scheduled cleanup completed successfully

Return ONLY the line number and classification, one per line."""

print(f"PROMPT:\n{prompt1}\n")
ask_and_print(prompt1)

teaching_point("""
Perfect output. Why?
  - Task is well-defined (classify as ERROR/WARN/INFO)
  - Universal knowledge (log levels are standard)
  - Clear output format specified
  - No domain-specific judgment needed
""")

pause()

# ---------------------------------------------------------------------------
# Demo 2: Zero-shot FAILURE
# ---------------------------------------------------------------------------
section("DEMO 2: Zero-shot FAILURE — needs YOUR team's standards")

jenkins_pipeline = open("samples/jenkins_pipeline.groovy").read().split("// PROBLEMS")[0].strip()

prompt2 = f"""Rate this Jenkins pipeline as PRODUCTION-READY, NEEDS-WORK, or NOT-READY.
Explain your rating in one paragraph.

```groovy
{jenkins_pipeline}
```"""

print(f"PROMPT:\n{prompt2[:200]}...\n")
ask_and_print(prompt2)

teaching_point("""
The AI might say "NEEDS-WORK" — but does it catch what YOU know?

YOUR team's definition of production-ready includes:
  - SonarQube code quality scanning
  - Trivy container vulnerability scanning
  - SBOM generation
  - Staging environment before production
  - Approval gates before deploy
  - Slack notifications on failure

The AI doesn't know YOUR bar. It uses a GENERIC bar.
To fix this, we need to TEACH it with examples.
That's NEXT — Few-Shot Prompting.
""")

pause()
