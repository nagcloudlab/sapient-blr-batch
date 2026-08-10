# DevOps Capsule Project -- Trainer Solutions & Hints
## Module 31 | Days 34-35

---

## Solution & Hints Table

| # | Sprint | Key Focus | Common Pitfalls | Trainer Hint |
|---|--------|-----------|-----------------|--------------|
| 1 | Docker | Multi-stage build, layer caching (copy pom.xml first), non-root user, HEALTHCHECK | Students copy all files in one COPY command, defeating layer caching. Also forget to create non-root user | Ask: "If you change one line of Java code, which Docker layers need to rebuild?" |
| 2 | Jenkins | Declarative pipeline, build number as image tag, post block for notifications | Students use `latest` tag for Docker images. Also missing test reporting (junit step) | Ask: "If you deploy `latest` and need to rollback, what version do you rollback to?" |
| 3 | K8s | Resource limits on all containers, liveness + readiness probes, Secrets for passwords | Students copy the liveness probe as readiness. Readiness should have shorter initialDelay. Also forget to use Secrets for DB password | Ask: "What happens if readiness probe has 60s initialDelay?" (60s of downtime on each deploy) |
| 4 | Ansible | Playbook with become, Vault for secrets, health check play | Students write a playbook that works once but is not idempotent. Running it twice should produce no changes | Ask: "What happens if you run this playbook again? Will it break anything?" |
| 5 | Integration | End-to-end pipeline test, rollback with `kubectl rollout undo` | Students test the happy path but not the failure path. Demonstrate a failed deployment and rollback | Ask: "How does your pipeline handle a failed deployment?" |

---

## Key Discussion Points

1. Why multi-stage builds? (Smaller images, no build tools in production)
2. Why not use `latest` tag? (Non-deterministic, can't rollback)
3. What is the difference between `depends_on` and health checks? (depends_on only waits for container start, not readiness)
4. Why use build number as image tag? (Traceability: every image maps to a specific build)
5. What is the role of sustain engineers in DevOps? (Maintain pipelines, fix failures, optimize builds)

---

## MCQ Answer Key

1. C (RUN) -- executes during build, not runtime
2. B (Readiness) -- determines traffic routing
3. B (become: yes) -- Ansible privilege escalation
