# KEY TAKEAWAY: AI is probabilistic. Same prompt, different answers.
# Production systems need verification.

from config import banner, section, ask_and_print, ask, pause, teaching_point

banner(7, "Self-Consistency: Trust but Verify",
       "AI is probabilistic — same prompt, different answers each time")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: Why does AI give different answers?")
print("""
LLMs are PROBABILISTIC — they sample from a distribution of possible tokens.

Temperature controls randomness:
  temperature=0.0  -> Nearly deterministic (always picks most likely)
  temperature=0.3  -> Slight variation (good for code & analysis)
  temperature=0.7  -> More creative (good for brainstorming)
  temperature=1.0  -> Maximum randomness (often incoherent)

SELF-CONSISTENCY = Run the same prompt N times, then check:
  All agree?     -> HIGH confidence, trust the answer
  They disagree? -> LOW confidence, investigate manually

It's like asking 3 on-call engineers the same question.
""")

pause(tip="This is a mind-blowing concept for most devs — AI isn't deterministic like code.")

# ---------------------------------------------------------------------------
# Demo 1: temperature=0.7 (3 runs)
# ---------------------------------------------------------------------------
section("DEMO 1: Same prompt, 3 runs at temperature=0.7")

error_log = open("samples/spring_boot_error.log").read()

prompt = f"""Analyze this production error log. Identify:
1. The root cause (one sentence)
2. Severity (P1/P2/P3/P4)
3. Immediate action (one sentence)

Be concise — max 3 lines total.

```
{error_log}
```"""

print("Running the EXACT same prompt 3 times (temperature=0.7)...\n")

for run in range(1, 4):
    print(f"{'='*70}")
    print(f"  RUN {run} of 3  (temperature=0.7)")
    print(f"{'='*70}\n")
    print(ask(prompt, temperature=0.7, max_tokens=300))
    print()

teaching_point("""
Look at the 3 outputs:
  - Do they agree on root cause? (probably yes — MongoDB pool)
  - Do they agree on severity? (maybe P1 vs P2 — watch for variation)
  - Do they use the same wording? (unlikely — it's sampling)

Agreement = confidence. Disagreement = the AI is uncertain.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 2: temperature=0 (3 runs)
# ---------------------------------------------------------------------------
section("DEMO 2: Same prompt, 3 runs at temperature=0 (deterministic)")

print("Running the EXACT same prompt 3 times (temperature=0)...\n")

for run in range(1, 4):
    print(f"{'='*70}")
    print(f"  RUN {run} of 3  (temperature=0)")
    print(f"{'='*70}\n")
    print(ask(prompt, temperature=0, max_tokens=300))
    print()

teaching_point("""
At temperature=0:
  - Outputs are nearly IDENTICAL
  - This is what you want for automated pipelines
  - Predictable, reproducible, testable
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("PRODUCTION RULES FOR TEMPERATURE")
print("""
  USE CASE                          TEMPERATURE
  ──────────────────────────────    ───────────
  Automated CI/CD pipeline          0
  Code generation                   0 - 0.2
  Code review / analysis            0.2 - 0.3
  Human-in-the-loop tools           0.3
  Technical writing                 0.3 - 0.5
  Brainstorming / exploration       0.7
  Creative writing                  0.8 - 1.0

SELF-CONSISTENCY PATTERN (for critical decisions):
  1. Run the prompt 3 times at temperature=0.3
  2. If all 3 agree -> proceed with confidence
  3. If they disagree -> the problem is ambiguous, investigate manually
  4. NEVER trust a single run for critical production decisions

Next up: Structured Output — making AI return JSON, not prose.
""")

pause()
