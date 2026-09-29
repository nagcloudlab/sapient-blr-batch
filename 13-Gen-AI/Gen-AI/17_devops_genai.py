# KEY TAKEAWAY: Gen-AI can automate the most tedious parts of DevOps —
# generating Dockerfiles, K8s manifests, Jenkins pipelines, Ansible playbooks,
# and Terraform configs from a single application description.

import json
from config import banner, section, ask_and_print, ask, pause, teaching_point, openai_client, OPENAI_MODEL

banner(17, "DevOps with Gen-AI: From App to Infrastructure",
       "Describe your app ONCE — AI generates your entire DevOps stack")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: The DevOps boilerplate problem")
print("""
For every microservice you build, you write the SAME boilerplate:

  1. Dockerfile           (multi-stage, non-root, healthcheck)
  2. K8s Deployment        (probes, limits, security context)
  3. K8s Service + Ingress (routing, TLS)
  4. Jenkins pipeline      (build, test, scan, deploy)
  5. Ansible playbook      (provisioning, config management)
  6. Prometheus rules      (alerts, recording rules)
  7. Grafana dashboard     (as JSON/code)

You spent WEEKS learning each of these. The KNOWLEDGE is in your head.
But the TYPING is repetitive. AI handles the typing. You handle the review.

WORKFLOW:
  1. Describe your app ONCE (language, ports, deps, requirements)
  2. AI generates the ENTIRE DevOps stack
  3. You REVIEW each file against your training
  4. You CUSTOMIZE for your specific needs
  5. Commit and ship
""")

pause(tip="Ask: 'How long did it take you to write the DevOps config for your capsule project?'")

# ---------------------------------------------------------------------------
# The application spec — single source of truth
# ---------------------------------------------------------------------------
section("THE APP SPEC: Describe once, generate everything")

APP_SPEC = {
    "name": "return-service",
    "description": "Return & Refund processing microservice",
    "language": "Java 17",
    "framework": "Spring Boot 3.3.4",
    "build_tool": "Maven",
    "artifact": "return-service-1.0.0.jar",
    "port": 8080,
    "health_endpoint": "/actuator/health",
    "metrics_endpoint": "/actuator/prometheus",
    "database": {
        "type": "MongoDB 7",
        "connection": "mongodb://mongo:27017/returnsdb"
    },
    "dependencies": [
        "refund-gateway (external API, port 8081)",
        "notification-service (internal, port 8082)"
    ],
    "environment": {
        "SPRING_PROFILES_ACTIVE": "production",
        "MONGO_MAX_POOL_SIZE": "100",
        "MONGO_MIN_POOL_SIZE": "10",
        "JVM_OPTS": "-Xms256m -Xmx512m"
    },
    "requirements": {
        "replicas": 3,
        "cpu_request": "250m",
        "cpu_limit": "1000m",
        "memory_request": "512Mi",
        "memory_limit": "1Gi",
        "max_image_size": "200MB",
        "sla_p99_latency": "500ms",
        "sla_error_rate": "1%",
        "sla_uptime": "99.9%"
    },
    "team": "sustain-engineering",
    "namespace": "production",
    "registry": "registry.internal.company.com"
}

print("APPLICATION SPEC (single source of truth):\n")
print(json.dumps(APP_SPEC, indent=2))

teaching_point("""
ONE spec describes the entire application.
From this, we'll generate 5 DevOps artifacts.
In a real team, this spec lives in your repo as app-spec.json.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 1: Generate production Dockerfile
# ---------------------------------------------------------------------------
section("DEMO 1: App Spec -> Production Dockerfile")

DEVOPS_SYSTEM = """You are a senior DevOps engineer at Publicis Sapient.
You follow these production standards:
- Multi-stage Docker builds (build + runtime stages)
- Non-root user (UID 1001)
- HEALTHCHECK instruction mandatory
- Specific version tags (never :latest)
- Labels for maintainer, version, description
- .dockerignore awareness
- Minimal final image (JRE, not JDK)
- Security: no secrets in image, no package managers in final stage
Generate production-grade configs. No shortcuts. No TODOs."""

dockerfile_prompt = f"""Generate a production-ready Dockerfile for this application:

{json.dumps(APP_SPEC, indent=2)}

Requirements:
- Multi-stage build: Maven build stage + Eclipse Temurin JRE 17 Alpine runtime
- Non-root user with UID 1001
- HEALTHCHECK using the health endpoint
- JVM memory flags from the spec
- Labels: maintainer, version, description, team
- Final image must be under {APP_SPEC['requirements']['max_image_size']}
- Copy ONLY the JAR file to the runtime stage

Return ONLY the Dockerfile — no explanation."""

print(f"Generating Dockerfile from app spec...\n")
dockerfile_result = ask_and_print(dockerfile_prompt, system_msg=DEVOPS_SYSTEM,
                                   max_tokens=1500, label="GENERATED DOCKERFILE")

teaching_point("""
CHECK against your Docker training:
  [x] Multi-stage build?
  [x] Non-root user (UID 1001)?
  [x] HEALTHCHECK instruction?
  [x] JVM flags (-Xms256m -Xmx512m)?
  [x] Specific base image tags (not :latest)?
  [x] Only JRE in final stage (not JDK)?
  [x] Labels present?

If ANY of these are missing, the AI failed YOUR standards.
Your Docker training is the verification layer.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 2: Generate K8s manifests
# ---------------------------------------------------------------------------
section("DEMO 2: App Spec -> Kubernetes Manifests")

k8s_prompt = f"""Generate production-ready Kubernetes manifests for this application:

{json.dumps(APP_SPEC, indent=2)}

Generate ALL of these as a single YAML file (separated by ---):

1. Namespace (if not exists)
2. ConfigMap (environment variables from spec)
3. Secret placeholder (for database credentials)
4. Deployment with:
   - Replicas from spec
   - Resource requests/limits from spec
   - Liveness probe (health endpoint, initial delay 30s, period 10s)
   - Readiness probe (health endpoint, initial delay 10s, period 5s)
   - Security context (runAsNonRoot, readOnlyRootFilesystem, drop ALL capabilities)
   - Image pull policy: IfNotPresent
   - Graceful shutdown (terminationGracePeriodSeconds: 30)
5. Service (ClusterIP)
6. HorizontalPodAutoscaler (min 3, max 10, target CPU 70%)

Return ONLY the YAML — no explanation."""

print(f"Generating K8s manifests from app spec...\n")
k8s_result = ask_and_print(k8s_prompt, system_msg=DEVOPS_SYSTEM,
                            max_tokens=3000, label="GENERATED K8S MANIFESTS")

teaching_point("""
CHECK against your K8s training:
  [x] Resource requests AND limits set?
  [x] Both liveness AND readiness probes?
  [x] Security context (runAsNonRoot, readOnly, drop caps)?
  [x] HPA for autoscaling?
  [x] ConfigMap for env vars (not hardcoded)?
  [x] Secret for credentials (not plain text)?
  [x] Correct label selectors matching?

Remember the capsule review feedback:
  "Most students forgot readiness probes"
  "Only Sinchana had HEALTHCHECK on every Dockerfile"
  "Nobody dropped ALL capabilities"

Now AI generates it. You VERIFY it.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 3: Generate Jenkins pipeline
# ---------------------------------------------------------------------------
section("DEMO 3: App Spec -> Jenkins CI/CD Pipeline")

jenkins_prompt = f"""Generate a production-grade Jenkins pipeline for this application:

{json.dumps(APP_SPEC, indent=2)}

The pipeline must include ALL of these stages:

1. Checkout (git)
2. Build (Maven, DO NOT skip tests)
3. Unit Tests (JUnit 5, publish results)
4. Code Quality (SonarQube analysis with quality gate)
5. Security Scan (Trivy container vulnerability scan)
6. SBOM Generation (generate and archive software bill of materials)
7. Docker Build (multi-stage, tag with git SHA, push to registry)
8. Deploy to Staging (kubectl apply to staging namespace)
9. Smoke Tests (curl health endpoint, wait for 200)
10. Approval Gate (manual approval before production)
11. Deploy to Production (canary 10%, then full rollout)
12. Post-deploy Verification (check error rate < 1% for 5 minutes)

Also include:
- post block: always notify Slack (success or failure)
- post block: publish test results and coverage
- Rollback stage on failure
- Environment variables for registry, image name, K8s namespace
- withCredentials for registry auth and kubeconfig

Return ONLY the Jenkinsfile — no explanation."""

print(f"Generating Jenkins pipeline from app spec...\n")
jenkins_result = ask_and_print(jenkins_prompt, system_msg=DEVOPS_SYSTEM,
                                max_tokens=3000, label="GENERATED JENKINSFILE")

teaching_point("""
Compare this with the BROKEN pipeline from samples/jenkins_pipeline.groovy:

  BROKEN PIPELINE:          GENERATED PIPELINE:
  - Skips tests             + Tests run
  - No quality gate         + SonarQube with quality gate
  - No security scan        + Trivy scan
  - No SBOM                 + SBOM generation
  - Deploys to prod direct  + Staging -> approval -> canary -> full
  - No rollback             + Rollback on failure
  - No notifications        + Slack notifications
  - No credentials mgmt    + withCredentials blocks
  - :latest tag             + Git SHA tag

EVERY issue from Module 4 (zero-shot Jenkins review) is now FIXED.
The AI knows best practices. But YOU know to verify it.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 4: Generate Ansible playbook
# ---------------------------------------------------------------------------
section("DEMO 4: App Spec -> Ansible Deployment Playbook")

ansible_prompt = f"""Generate an Ansible playbook to deploy and configure this application
on a Kubernetes cluster:

{json.dumps(APP_SPEC, indent=2)}

The playbook must:
1. Verify cluster connectivity (kubectl cluster-info)
2. Create namespace if not exists
3. Apply ConfigMap and Secrets from templates
4. Deploy the application using K8s manifests
5. Wait for rollout to complete (timeout 300s)
6. Run health check verification (curl health endpoint)
7. Configure Prometheus ServiceMonitor for metrics scraping
8. Send deployment notification to Slack

Include:
- Proper use of roles (deploy, verify, notify)
- Variables file (vars/main.yml) with defaults from the spec
- Error handling with block/rescue/always
- Tags for selective execution (deploy, verify, notify)
- Idempotent design (safe to run multiple times)

Return ONLY the playbook YAML — no explanation."""

print(f"Generating Ansible playbook from app spec...\n")
ansible_result = ask_and_print(ansible_prompt, system_msg=DEVOPS_SYSTEM,
                                max_tokens=3000, label="GENERATED ANSIBLE PLAYBOOK")

teaching_point("""
CHECK against your Ansible training:
  [x] Roles structure (not one giant playbook)?
  [x] Variables with defaults?
  [x] block/rescue/always for error handling?
  [x] Tags for selective runs?
  [x] Idempotent tasks (safe to re-run)?
  [x] Health verification after deploy?

Capsule review feedback said:
  "Most students had shallow Ansible playbooks"
  "Missing error handling and verification steps"

AI generates the COMPLETE playbook. You verify the LOGIC.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 5: Generate Prometheus alert rules
# ---------------------------------------------------------------------------
section("DEMO 5: App Spec -> Prometheus Alert Rules + Grafana Dashboard")

monitoring_prompt = f"""Generate Prometheus alerting rules and a Grafana dashboard config
for this application:

{json.dumps(APP_SPEC, indent=2)}

PROMETHEUS ALERT RULES (YAML):
Generate alerts for:
1. HighErrorRate: HTTP 5xx rate > {APP_SPEC['requirements']['sla_error_rate']} for 5 min
2. HighLatency: p99 latency > {APP_SPEC['requirements']['sla_p99_latency']} for 5 min
3. PodRestarting: restart count > 3 in 10 min
4. HighMemoryUsage: memory > 85% of limit for 5 min
5. MongoConnectionPoolExhaustion: active connections > 80% of max for 3 min
6. DeploymentUnavailable: available replicas < desired for 5 min

Each alert must have:
- severity label (critical/warning)
- summary annotation with service name
- description annotation with current value
- runbook_url annotation

GRAFANA DASHBOARD (JSON):
Generate a simple dashboard with panels for:
1. Request rate (req/s)
2. Error rate (%)
3. p99 latency (ms)
4. MongoDB connection pool usage
5. CPU and Memory usage
6. Pod count (desired vs available)

Return the Prometheus rules YAML first, then the Grafana dashboard JSON."""

print(f"Generating monitoring config from app spec...\n")
ask_and_print(monitoring_prompt, system_msg=DEVOPS_SYSTEM,
              max_tokens=4000, label="GENERATED MONITORING CONFIG")

teaching_point("""
Notice the alert thresholds come from YOUR app spec SLAs:
  - Error rate > 1% (from sla_error_rate)
  - p99 > 500ms (from sla_p99_latency)

And alert #5 (MongoConnectionPoolExhaustion) is EXACTLY the alert
that triggered the incident in Modules 10 and 15.

In production, these alerts PREVENT the incidents you've been
diagnosing all day. Full circle.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 6: One-shot full stack generation
# ---------------------------------------------------------------------------
section("DEMO 6: THE GRAND FINALE — Generate everything at once")

oneshot_prompt = f"""Given this application spec, list ALL the files that need to be created
for a complete production deployment, organized by directory:

{json.dumps(APP_SPEC, indent=2)}

For each file, provide:
  - Full file path
  - One-line description of what it contains
  - Which team is responsible for maintaining it

Organize by:
  docker/
  k8s/
  jenkins/
  ansible/
  monitoring/
  docs/

Also include files that are commonly FORGOTTEN:
  - .dockerignore
  - .gitignore
  - CODEOWNERS
  - CHANGELOG.md
  - Architecture Decision Records

Return as a structured file tree with descriptions."""

print("Generating the COMPLETE file tree for production deployment...\n")
ask_and_print(oneshot_prompt, max_tokens=2000, label="COMPLETE DEVOPS FILE TREE")

teaching_point("""
From ONE app spec, the AI planned your entire DevOps file structure.

In your capsule projects, many of you were missing:
  - .dockerignore (huge images!)
  - K8s Secrets (hardcoded passwords!)
  - Monitoring configs (no alerts!)
  - SBOM generation (compliance gap!)
  - Rollback plans (no safety net!)

AI helps you REMEMBER what you know but might forget under pressure.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("DEVOPS + GEN-AI: THE WORKFLOW")
print("""
THE NEW DEVOPS WORKFLOW:

  1. DEFINE    — Write app-spec.json (10 minutes of thinking)
  2. GENERATE  — AI creates Dockerfile, K8s, Jenkins, Ansible, Monitoring
  3. REVIEW    — You verify against YOUR training and standards
  4. CUSTOMIZE — Adjust for your specific infrastructure
  5. TEST      — Run in staging, verify everything works
  6. COMMIT    — Ship it

TIME COMPARISON:
  Manual DevOps setup:  2-3 days of boilerplate
  AI-augmented setup:   2-3 hours (generate + review + customize)

BUT REMEMBER:
  - AI generates GENERIC best practices
  - YOU add TEAM-SPECIFIC customizations
  - AI doesn't know your network topology
  - AI doesn't know your registry URLs
  - AI doesn't know your team's Slack channels
  - Combine with RAG (Module 16) for team-specific generation

THE COMPLETE PICTURE:
  Modules 1-9:   HOW to prompt (techniques)
  Modules 10-12: WHEN AI fails (trust & verify)
  Modules 13-15: AI for daily work (review, test, post-mortem)
  Module 16:     AI + YOUR knowledge (RAG)
  Module 17:     AI for DevOps (generate entire infra stack)

  Prompt Engineering + RAG + DevOps Automation
  = The AI-augmented engineer

  Your 45-day training taught you WHAT to build.
  Today taught you HOW to build it 10x faster.

  Go build something amazing.
""")

pause()
