# KEY TAKEAWAY: Few-shot = teaching by example, like pair programming with AI.
# Provide 2-3 examples and the AI mimics YOUR pattern.

from config import banner, section, ask_and_print, pause, teaching_point

banner(5, "Few-Shot Prompting",
       "Teach the AI by example — like pair programming")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: What is Few-Shot?")
print("""
FEW-SHOT = Provide 2-3 examples of input -> output pairs BEFORE the actual task.
The AI learns YOUR PATTERN from the examples and applies it.

  Zero-shot:  "Review this code"
  Few-shot:   "Here are 2 examples of how WE review code. Now review this one."

It's the difference between:
  - Telling a new joiner "review PRs" and walking away (zero-shot)
  - Pair programming with them for 2 reviews, THEN letting them solo (few-shot)

WHY IT WORKS: LLMs are extreme pattern matchers.
Show your pattern, and they replicate it precisely.
""")

pause(tip="Analogy: Few-shot is like training a new team member by showing them examples of good work.")

# ---------------------------------------------------------------------------
# Demo: Few-shot Dockerfile review
# ---------------------------------------------------------------------------
section("DEMO: Few-shot Dockerfile review — YOUR team's standards")

system_msg = "You are a senior SRE at Publicis Sapient reviewing Dockerfiles."

user_msg = """Here are examples of how our team reviews Dockerfiles:

EXAMPLE 1:
Input: `FROM node:18`
Review:
| Issue | Severity | Finding | Fix |
|-------|----------|---------|-----|
| Base Image | HIGH | Using full Node image (~900MB). Use slim variant. | `FROM node:18-slim` |
| Image Tag | MEDIUM | Tag `18` is a rolling tag. Pin to specific version. | `FROM node:18.19.0-slim` |

EXAMPLE 2:
Input: `COPY . .`
Review:
| Issue | Severity | Finding | Fix |
|-------|----------|---------|-----|
| Build Context | HIGH | Copies entire directory including node_modules, .git, .env files. | Add `.dockerignore` and use `COPY package*.json ./` first |
| Layer Cache | MEDIUM | Invalidates Docker layer cache on ANY file change. | Copy dependency files first, install, then copy source |

EXAMPLE 3:
Input: `CMD ["npm", "start"]`
Review:
| Issue | Severity | Finding | Fix |
|-------|----------|---------|-----|
| Signal Handling | MEDIUM | npm does not forward SIGTERM to child process. Container won't gracefully shutdown in K8s. | `CMD ["node", "server.js"]` |
| Health Check | HIGH | No HEALTHCHECK instruction. K8s liveness probe has no Docker-level fallback. | Add `HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1` |

---

Now review this Dockerfile using the SAME format and standards:

```dockerfile
FROM openjdk:17
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```"""

print("PROMPT: 3 examples of OUR team's review format, then a new Dockerfile\n")
ask_and_print(user_msg, system_msg=system_msg)

teaching_point("""
Compare this with Module 04's zero-shot review:

  ZERO-SHOT: Generic advice, inconsistent format, missed team standards
  FEW-SHOT:  Matched our table format, used our severity levels,
             found issues aligned with YOUR training

We didn't teach the AI about Docker security.
We showed it HOW OUR TEAM talks about Docker security.
The AI matched our PATTERN — format, tone, severity scale.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("FEW-SHOT PATTERNS FOR YOUR WORK")
print("""
Where can YOU use few-shot in your projects?

  Code review bot:     3 examples of your team's PR feedback style
  Incident reports:    2 examples of your ServiceNow ticket format
  Test cases:          3 examples of your JUnit test structure
  Documentation:       2 examples of your README format
  Commit messages:     2 examples of your team's commit style

RULES OF THUMB:
  - 2-3 examples is the sweet spot
  - More than 5 = diminishing returns + wasted tokens (and money)
  - Examples should cover DIFFERENT scenarios (not 3 of the same thing)
  - The AI will match your FORMAT, TONE, and DEPTH

Next up: Chain-of-Thought — making the AI show its reasoning.
""")

pause()
