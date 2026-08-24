# Module 18: DevOps -- Lab Setup

## Prerequisites

- No runtime tools required for the core lab (document + config review).
- Optional: a text editor with YAML highlighting (VS Code with the YAML extension).
- Optional: Jenkins (Docker or native) for pipeline validation.

## Running the Starter Code

This lab focuses on reviewing and fixing configuration files. There is no application to start.

1. Read `Project/BRIEF.md` for the full exercise instructions.
2. Open `Labs/starter-code/Jenkinsfile` and the deployment docs in a text editor.
3. Work through each issue listed in `lab-exercises.md`.

## Verifying Your Fixes

**Jenkinsfile syntax check (optional but recommended):**
If you have Jenkins running via Docker:
```bash
docker run --rm -v $(pwd)/Labs/starter-code:/workspace \
  jenkins/jenkins:lts \
  java -jar /usr/share/jenkins/jenkins.war --httpPort=-1 \
  --jsonapi http://localhost:8080 2>/dev/null
```
Or paste the Jenkinsfile into the "Pipeline Syntax" validator in the Jenkins UI.

Compare your fixed pipeline design against `Project/CHECKLIST.md`:
- All required stages present (checkout, build, test, package, deploy).
- Environment variables used instead of hard-coded credentials.
- Post-build notifications configured.

## Expected Behavior

- Jenkinsfile parses without syntax errors.
- Pipeline stages are in the correct order: build before test, test before deploy.
- No credentials or secrets are hard-coded in the Jenkinsfile.
- Deployment documentation covers rollback procedure.

## Troubleshooting

**Jenkinsfile YAML/Groovy confusion:** Jenkinsfiles use Groovy DSL, not YAML. Indentation matters for
readability but not for syntax -- look for missing braces `{}` or mismatched `stage()` blocks.

**Hard-coded secrets not obvious:** Search for IP addresses, passwords, and API keys using `grep -r`
across all files in `starter-code/`. Any literal credential is a bug.
