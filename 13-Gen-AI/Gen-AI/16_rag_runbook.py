# KEY TAKEAWAY: RAG = Retrieval-Augmented Generation.
# Instead of hoping the AI knows your docs, you INJECT them into the prompt.
# Your runbooks, your standards, your knowledge — fed directly to the AI.

import json
from config import banner, section, ask_and_print, ask, pause, teaching_point

banner(16, "RAG: Teach AI Your Team's Knowledge",
       "Don't hope the AI knows your docs — INJECT them into the prompt")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: The problem with AI's knowledge")
print("""
AI was trained on PUBLIC internet data up to a cutoff date.

It does NOT know:
  - Your team's runbooks
  - Your company's coding standards
  - Your production architecture
  - Your ServiceNow categories
  - Your on-call escalation policy
  - Your deployment procedures
  - Anything written AFTER its training cutoff

THE FIX: RAG — Retrieval-Augmented Generation

  STEP 1: RETRIEVE relevant docs from your knowledge base
  STEP 2: INJECT them into the prompt as context
  STEP 3: AI GENERATES answers grounded in YOUR docs

  Without RAG:  AI guesses based on generic internet knowledge
  With RAG:     AI answers based on YOUR team's actual documentation

It's like the difference between:
  - Asking a stranger for directions (they guess)
  - Asking a stranger for directions AND handing them your map
""")

pause(tip="Ask: 'Has the AI ever given you advice that contradicted your team's way of doing things?'")

# ---------------------------------------------------------------------------
# Build a team knowledge base (simulated)
# ---------------------------------------------------------------------------
section("BUILDING YOUR TEAM'S KNOWLEDGE BASE")

# Simulated knowledge base — in production this would come from Confluence/Notion/Git
TEAM_RUNBOOKS = {
    "mongodb-connection-pool": """
RUNBOOK: MongoDB Connection Pool Exhaustion
Last updated: 2026-09-15
Owner: Sustain Engineering Team

SYMPTOMS:
- MongoTimeoutException in logs
- Connection pool active count equals max
- HTTP 5xx rate spike
- Pending request queue growing

SEVERITY: P1 if error rate > 20%, P2 if > 10%, P3 otherwise

STEP 1: VERIFY (2 min)
  kubectl exec -it <pod> -n production -- curl localhost:8080/actuator/metrics/mongodb.driver.pool.size
  Expected: checkedOut should be < maxSize

STEP 2: IMMEDIATE FIX (5 min)
  Option A — Scale pool (preferred):
    kubectl edit configmap return-service-config -n production
    Change: spring.data.mongodb.uri connection params
    Add: ?maxPoolSize=100&minPoolSize=10&maxIdleTimeMS=30000
    Then: kubectl rollout restart deployment/return-service -n production

  Option B — Scale pods (if pool scaling insufficient):
    kubectl scale deployment/return-service -n production --replicas=5

  Option C — Nuclear (last resort):
    kubectl rollout undo deployment/return-service -n production

STEP 3: VERIFY FIX (5 min)
  Watch error rate in Grafana: https://grafana.internal/d/return-service
  Expected: 5xx rate should drop below 5% within 5 minutes
  If not: Escalate to Database Team (Slack: #db-oncall)

ESCALATION:
  P1: Page Database Team lead + notify VP Engineering via Slack #incidents
  P2: Slack #db-oncall during business hours
  P3: Create Jira ticket, fix in next sprint

POST-INCIDENT:
  1. Create ServiceNow incident ticket (category: Database, subcategory: Connection Pool)
  2. Write post-mortem within 24 hours
  3. Schedule review meeting within 48 hours
""",

    "deployment-standards": """
STANDARD: Production Deployment Checklist
Last updated: 2026-09-20
Owner: Sustain Engineering Team

PRE-DEPLOYMENT:
  [ ] All unit tests pass (JUnit 5, >80% coverage)
  [ ] Integration tests pass against staging MongoDB
  [ ] SonarQube quality gate passed (0 critical, 0 blocker)
  [ ] Trivy container scan: 0 critical vulnerabilities
  [ ] SBOM generated and stored in artifact registry
  [ ] Docker image tagged with git SHA (never use :latest)
  [ ] K8s manifest has resource limits, probes, security context
  [ ] Change request approved in ServiceNow
  [ ] Rollback plan documented and tested

DEPLOYMENT SEQUENCE:
  1. Deploy to staging namespace
  2. Run smoke tests (health check + core API endpoints)
  3. Wait 15 minutes, monitor error rate
  4. If staging OK: Deploy to production (canary 10%)
  5. Wait 10 minutes, compare canary metrics vs stable
  6. If canary OK: Roll out to 100%
  7. Monitor for 30 minutes post-deploy
  8. Update ServiceNow change request to "Implemented"

ROLLBACK CRITERIA:
  - Error rate > 5% for 3 minutes -> automatic rollback
  - p99 latency > 2x baseline -> manual review, likely rollback
  - Any data integrity issue -> immediate rollback + page DBA

NEVER:
  - Deploy on Friday after 3 PM
  - Deploy without a rollback plan
  - Skip staging
  - Use kubectl apply directly (use Jenkins pipeline)
""",

    "coding-standards": """
STANDARD: Spring Boot Coding Standards
Last updated: 2026-09-18
Owner: Sustain Engineering Team

ARCHITECTURE:
  - Controller -> Service -> Repository (3-layer)
  - Controllers: ONLY handle HTTP concerns (request/response mapping)
  - Services: ALL business logic (never in controllers)
  - Repository: Data access only (no business logic)

EXCEPTION HANDLING:
  - Use @ControllerAdvice for global exception handling
  - Custom exceptions: ResourceNotFoundException, ValidationException, ServiceException
  - NEVER return stack traces to the client
  - Log the full exception server-side, return sanitized message to client
  - HTTP status codes: 400 for validation, 404 for not found, 500 for server errors

NAMING:
  - Classes: PascalCase (ReturnService, not returnService)
  - Methods: camelCase, verb-first (createReturn, not returnCreate)
  - REST endpoints: kebab-case plural (/api/returns, not /api/Return)
  - Constants: UPPER_SNAKE_CASE

DEPENDENCY INJECTION:
  - Constructor injection ONLY (never @Autowired on fields)
  - Use @RequiredArgsConstructor from Lombok

VALIDATION:
  - @Valid on all @RequestBody parameters
  - Custom validators for business rules
  - Validate at controller level, not service level

MONGODB:
  - Use MongoRepository interface, not MongoTemplate (unless complex queries)
  - Index frequently queried fields
  - Use Instant for timestamps (not Date)
  - Use enum for status fields (not String)
"""
}

print("Simulated knowledge base loaded with 3 documents:\n")
for key, doc in TEAM_RUNBOOKS.items():
    lines = [l.strip() for l in doc.strip().split("\n") if l.strip()]
    print(f"  [{key}]")
    print(f"    Title: {lines[0]}")
    print(f"    Lines: {len(doc.strip().split(chr(10)))}")
    print()

teaching_point("""
In production, this knowledge base would live in:
  - Confluence/Notion pages
  - Git repos (markdown runbooks)
  - ServiceNow knowledge articles
  - Team wikis

RAG systems use VECTOR SEARCH to find relevant docs.
Today we'll simulate it by manually selecting the right doc.
The PRINCIPLE is the same — inject context, get better answers.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 1: WITHOUT runbook (AI guesses)
# ---------------------------------------------------------------------------
section("DEMO 1: WITHOUT your runbook — AI guesses generic steps")

alert = json.load(open("samples/prometheus_alert.json"))

prompt_no_rag = f"""A Prometheus alert fired:
  Alert: {alert['labels']['alertname']}
  Service: {alert['labels']['service']}
  Error rate: {alert['relatedMetrics']['http_5xx_rate']}
  DB connections: {alert['relatedMetrics']['active_db_connections']}

What should I do? Give me step-by-step mitigation."""

print("PROMPT: Alert details only. No runbook. AI must guess.\n")
ask_and_print(prompt_no_rag, label="WITHOUT RAG — generic advice")

teaching_point("""
The AI gives GENERIC advice:
  - "Check your connection pool settings"
  - "Consider scaling up"
  - "Monitor the logs"

Useless at 2 AM. Where are the kubectl commands?
Where's the Grafana dashboard URL? The escalation path?
The AI doesn't know YOUR infrastructure.
""")

pause(tip="Ask: 'Would you trust these steps at 2 AM? What's missing?'")

# ---------------------------------------------------------------------------
# Demo 2: WITH runbook injected (RAG)
# ---------------------------------------------------------------------------
section("DEMO 2: WITH your runbook injected — AI follows YOUR procedures")

# Simulate RAG: retrieve the relevant runbook
retrieved_doc = TEAM_RUNBOOKS["mongodb-connection-pool"]

prompt_with_rag = f"""A Prometheus alert fired. Use the team runbook below to guide your response.

ALERT:
  Alert: {alert['labels']['alertname']}
  Service: {alert['labels']['service']}
  Error rate: {alert['relatedMetrics']['http_5xx_rate']}
  DB connections: {alert['relatedMetrics']['active_db_connections']}
  Pending requests: {alert['relatedMetrics']['pending_db_requests']}
  Memory: {alert['relatedMetrics']['memory_usage_percent']}%

TEAM RUNBOOK:
{retrieved_doc}

Based on the alert data AND the runbook:
1. What severity is this incident? (use the runbook's criteria)
2. Which step should I execute FIRST? (give me the exact command)
3. What's the verification step? (exact URL/command)
4. Who do I escalate to? (use the runbook's escalation path)

Be specific — use commands and URLs from the runbook, not generic advice."""

SYSTEM = """You are an SRE assistant that ONLY gives advice based on the team's
runbooks and documentation. If the runbook doesn't cover something, say
'Not covered in runbook — escalate to team lead.' NEVER make up procedures."""

print("PROMPT: Same alert + team runbook injected as context\n")
print("SYSTEM: 'Only give advice based on the runbook. Never make up procedures.'\n")
ask_and_print(prompt_with_rag, system_msg=SYSTEM, label="WITH RAG — runbook-grounded response")

teaching_point("""
NIGHT AND DAY difference:
  - Specific kubectl commands from YOUR runbook
  - YOUR Grafana dashboard URL
  - YOUR escalation path (#db-oncall, VP Engineering)
  - YOUR severity criteria (>20% = P1)
  - YOUR ServiceNow categorization

The AI didn't learn anything new. We INJECTED the knowledge.
Same model. Same prompt structure. Better context = better answer.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 3: RAG with coding standards — code review
# ---------------------------------------------------------------------------
section("DEMO 3: RAG for code review — YOUR coding standards")

retrieved_standards = TEAM_RUNBOOKS["coding-standards"]

code_to_review = """```java
@RestController
@RequestMapping("/api/Return")
public class returnController {

    @Autowired
    ReturnService returnService;

    @PostMapping
    public Return returnCreate(@RequestBody ReturnRequest req) {
        try {
            Return r = returnService.createReturn(req);
            return r;
        } catch (Exception e) {
            e.printStackTrace();
            throw e;
        }
    }

    @GetMapping("/{id}")
    public Return getreturn(@PathVariable String id) {
        Return r = returnService.getReturn(id);
        return r;
    }
}
```"""

review_prompt = f"""Review this code against our team's coding standards.
For each violation, cite the SPECIFIC standard being violated.

TEAM CODING STANDARDS:
{retrieved_standards}

CODE TO REVIEW:
{code_to_review}

Format each violation as:
  VIOLATION: [what's wrong]
  STANDARD: [exact quote from the standards document]
  FIX: [corrected code]"""

print("PROMPT: Code + team standards injected. Review against YOUR rules.\n")
ask_and_print(review_prompt, max_tokens=2000, label="RAG CODE REVIEW — team standards enforced")

teaching_point("""
The AI found violations against YOUR SPECIFIC standards:
  - "returnController" -> PascalCase required (YOUR standard)
  - "/api/Return" -> kebab-case plural required (YOUR standard)
  - @Autowired on field -> constructor injection only (YOUR standard)
  - No @Valid -> required on @RequestBody (YOUR standard)
  - e.printStackTrace() -> use @ControllerAdvice (YOUR standard)
  - "returnCreate" -> verb-first camelCase (YOUR standard)

Without RAG: "This code has some naming issues"
With RAG:    "This violates Section 'NAMING': Classes must be PascalCase"

The AI CITES your standards. That's the power of RAG.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 4: RAG with deployment checklist — pre-deploy validation
# ---------------------------------------------------------------------------
section("DEMO 4: RAG for deployment validation")

deploy_standards = TEAM_RUNBOOKS["deployment-standards"]

deploy_prompt = f"""I'm about to deploy return-service to production. Today is Friday at 4:30 PM.

Here's what I've done:
  - Unit tests pass (82% coverage)
  - Docker image built and tagged as return-service:latest
  - K8s manifest ready (no resource limits yet, will add later)
  - SonarQube: 0 critical, 2 blockers
  - Trivy scan: not run yet
  - Change request: not created yet
  - Planning to kubectl apply directly to production

Check my deployment against the team's standards and tell me what's BLOCKING.

TEAM DEPLOYMENT STANDARDS:
{deploy_standards}

For each blocker:
  1. What standard is violated (quote it)
  2. Why it matters
  3. What I need to do before deploying"""

print("SCENARIO: Friday 4:30 PM deploy with multiple violations...\n")
ask_and_print(deploy_prompt, max_tokens=2000, label="DEPLOYMENT GATE — RAG validation")

teaching_point("""
The AI caught EVERY violation against YOUR standards:
  - Friday after 3 PM -> "NEVER deploy on Friday after 3 PM"
  - :latest tag -> "Docker image tagged with git SHA (never use :latest)"
  - No resource limits -> "K8s manifest has resource limits"
  - 2 SonarQube blockers -> "0 critical, 0 blocker"
  - No Trivy scan -> "Trivy container scan: 0 critical"
  - No change request -> "Change request approved in ServiceNow"
  - kubectl apply directly -> "use Jenkins pipeline"

This could be a PRE-DEPLOY BOT in your CI/CD pipeline:
  1. Collect deployment metadata
  2. Inject deployment standards (RAG)
  3. AI validates against standards
  4. Block deploy if violations found
  5. All automated. Zero human effort to enforce.
""")

pause()

# ---------------------------------------------------------------------------
# How RAG works in production
# ---------------------------------------------------------------------------
section("HOW RAG WORKS IN PRODUCTION")
print("""
What we did today (SIMULATED RAG):
  1. Manually selected the right document
  2. Injected the full text into the prompt
  3. AI answered based on the document

What PRODUCTION RAG looks like:

  USER QUERY
      │
      ▼
  EMBEDDING MODEL ──> Convert query to vector
      │
      ▼
  VECTOR DATABASE ──> Search for similar docs
  (Pinecone, Weaviate,    (cosine similarity)
   ChromaDB, pgvector)
      │
      ▼
  TOP-K DOCUMENTS ──> Retrieve most relevant docs
      │
      ▼
  PROMPT = User Query + Retrieved Docs
      │
      ▼
  LLM (GPT-4o) ──> Answer grounded in YOUR docs


  TOOLS FOR BUILDING RAG:
    - LangChain (Python framework for RAG pipelines)
    - LlamaIndex (document indexing + retrieval)
    - ChromaDB (lightweight vector database)
    - OpenAI Embeddings (text-embedding-3-small)
    - pgvector (PostgreSQL extension for vectors)

  YOUR KNOWLEDGE SOURCES:
    - Confluence runbooks
    - Git repo READMEs
    - ServiceNow knowledge articles
    - Slack thread archives
    - Post-mortem documents
    - Architecture decision records (ADRs)
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("RAG: THE KEY TO ENTERPRISE AI")
print("""
RAG is what makes AI USEFUL in a real company:

  WITHOUT RAG: AI is a smart stranger who guesses
  WITH RAG:    AI is a team member who reads your docs

USE CASES FOR YOUR TEAM:
  1. ON-CALL ASSISTANT:  Inject runbooks -> step-by-step mitigation
  2. CODE REVIEW BOT:    Inject standards -> enforce team conventions
  3. DEPLOY GATE:        Inject checklist -> block bad deployments
  4. ONBOARDING BUDDY:   Inject team wiki -> answer new joiner questions
  5. INCIDENT HELPER:    Inject past post-mortems -> pattern recognition

THE EQUATION:
  AI + YOUR KNOWLEDGE = AI THAT WORKS FOR YOUR TEAM

  Prompt Engineering = HOW you talk to AI (Modules 1-12)
  RAG = WHAT knowledge you give it (Module 16)
  Together = Enterprise-grade AI applications

This is the foundation of every AI product you'll build in your career.
""")

pause()
