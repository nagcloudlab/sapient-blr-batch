# KEY TAKEAWAY: Context is everything. The AI knows nothing about YOUR project.

from config import banner, section, ask_and_print, pause, teaching_point

banner(1, "The Gap Between You and the AI",
       "Context is everything — same question, wildly different answers")

# ---------------------------------------------------------------------------
# Demo 1: The vague prompt
# ---------------------------------------------------------------------------
section("DEMO 1: The Vague Prompt — what you've been doing for months")

VAGUE_PROMPT = "Write a Dockerfile for my Spring Boot application."

print(f'PROMPT: "{VAGUE_PROMPT}"')
ask_and_print(VAGUE_PROMPT)

teaching_point("""
Notice what's MISSING from this output:
  - No multi-stage build (image will be 500MB+)
  - Runs as ROOT user (security risk)
  - No HEALTHCHECK (K8s can't probe it)
  - No JVM memory tuning
  - Uses deprecated openjdk base image
This is what you get when you give ZERO context.
""")

pause(tip="Ask students: 'How many of you have typed a prompt like this?'")

# ---------------------------------------------------------------------------
# Demo 2: The engineered prompt
# ---------------------------------------------------------------------------
section("DEMO 2: The Engineered Prompt — same question, 10x better answer")

PRECISE_PROMPT = """Write a production-ready Dockerfile for a Spring Boot 3.3 application with these requirements:

PROJECT CONTEXT:
- Java 17, Maven build, produces a JAR named return-service-1.0.0.jar
- Connects to MongoDB and exposes REST APIs on port 8080
- Will be deployed on Kubernetes with liveness/readiness probes at /actuator/health

REQUIREMENTS:
- Multi-stage build (build stage + runtime stage)
- Use Eclipse Temurin JRE 17 Alpine for the runtime stage
- Run as non-root user (uid 1001)
- Include HEALTHCHECK instruction
- Set JVM memory flags: -Xms512m -Xmx512m
- Add labels: maintainer, version, description
- Ensure the image is under 200MB

CONSTRAINTS:
- Do NOT use openjdk base images (deprecated)
- Do NOT use the 'latest' tag for any base image
- Do NOT copy the entire project — only copy the JAR
"""

print(f"PROMPT:\n{PRECISE_PROMPT}")
ask_and_print(PRECISE_PROMPT)

teaching_point("""
SAME question. DRAMATICALLY better output.
The AI didn't get smarter. YOU got smarter about what to ask.
""")

pause(tip="Ask: 'What changed between Demo 1 and Demo 2? Count the differences.'")

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("KEY LESSON")
print("""
Think of it like filing a Jira ticket:

  BAD TICKET:   "Fix the login bug"
  GOOD TICKET:  "Login fails with 401 when JWT expires during active session.
                 Steps to reproduce: ... Expected: ... Actual: ..."

The AI is like a brilliant contractor who does EXACTLY what you ask.
  - Vague spec  = generic work
  - Precise spec = production-quality work

The engineer's skill is in the SPECIFICATION, not the implementation.

Coming up next: The 6-part framework for writing perfect prompts every time.
""")

pause()
