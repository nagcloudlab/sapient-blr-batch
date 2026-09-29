# KEY TAKEAWAY: Complex tasks = pipeline of focused prompts, like microservices for AI.
# Each prompt does ONE thing well. Output of one feeds input of the next.

import json
from config import banner, section, ask_and_print, ask, pause, teaching_point, OPENAI_MODEL_MINI

banner(9, "Prompt Chaining",
       "Complex tasks = pipeline of focused prompts, like microservices")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: Why chain prompts?")
print("""
You learned microservices: each service does ONE thing well.
Prompt chaining applies the SAME principle to AI:

  MONOLITH PROMPT (bad):
    "Analyze this log, find root cause, write Ansible playbook,
     generate K8s rollback, AND create a ServiceNow ticket"
    -> Overwhelming. Low quality. Hard to debug.

  CHAINED PROMPTS (good):
    Chain 1: Log  ->  Root Cause (JSON)
    Chain 2: Root Cause  ->  Ansible Playbook
    Chain 3: Root Cause  ->  K8s Rollback Manifest

  WHY CHAINING IS BETTER:
    - Each prompt is simpler = higher quality output
    - You can VERIFY intermediate results
    - You can RETRY a single step without redoing everything
    - You can use DIFFERENT models for different steps
    - It's testable, debuggable, composable
""")

pause(tip="Analogy: 'Would you write one giant function or break it into focused methods?'")

# ---------------------------------------------------------------------------
# Chain 1: Log -> Root Cause (JSON)
# ---------------------------------------------------------------------------
section("CHAIN 1: Error Log -> Root Cause Analysis (JSON)")

error_log = open("samples/spring_boot_error.log").read()

chain1_prompt = f"""Analyze this Spring Boot error log and extract the root cause.
Return ONLY a JSON object:
{{
  "root_cause": "one sentence description",
  "affected_service": "service name",
  "affected_component": "specific component (e.g., connection pool, scheduler)",
  "error_type": "resource_exhaustion|timeout|crash|config_error",
  "immediate_fix": "one sentence",
  "related_services": ["list of other affected services"]
}}

```
{error_log}
```"""

print("CHAIN 1: Log -> Root Cause (structured extraction)\n")
chain1_result = ask_and_print(chain1_prompt, max_tokens=512, label="CHAIN 1 OUTPUT")

try:
    root_cause = json.loads(chain1_result.strip().strip("```json").strip("```").strip())
    print(f"\n  [PASS] Chain 1 parsed — root cause: {root_cause['root_cause']}")
except json.JSONDecodeError:
    root_cause = {
        "root_cause": "MongoDB connection pool exhaustion",
        "affected_service": "return-service",
        "affected_component": "MongoDB connection pool",
        "error_type": "resource_exhaustion",
        "immediate_fix": "Increase MongoDB connection pool size from 50 to 100",
        "related_services": ["refund-service", "return-expiry-job"]
    }
    print(f"\n  [FALLBACK] Using pre-defined root cause for demo continuity")

teaching_point("""
Chain 1 converts UNSTRUCTURED logs into STRUCTURED data.
This JSON is now the CONTRACT between chains — like an API response.
""")

pause()

# ---------------------------------------------------------------------------
# Chain 2: Root Cause -> Ansible Playbook
# ---------------------------------------------------------------------------
section("CHAIN 2: Root Cause -> Ansible Remediation Playbook")

chain2_prompt = f"""Based on this root cause analysis, generate an Ansible playbook
to remediate the issue on a Kubernetes cluster.

Root Cause Analysis:
{json.dumps(root_cause, indent=2)}

Requirements:
- Target the MongoDB StatefulSet in the 'production' namespace
- Update the connection pool configuration
- Perform a rolling restart to apply changes
- Verify the fix with a health check
- Include proper error handling with block/rescue

Return ONLY the Ansible playbook YAML — no explanation."""

print(f"CHAIN 2: Root Cause JSON -> Ansible Playbook\n")
print(f"  Input:  \"{root_cause['root_cause']}\"")
print(f"  Output: Ansible playbook to fix it\n")

ask_and_print(chain2_prompt, max_tokens=1500, label="CHAIN 2 OUTPUT")

pause()

# ---------------------------------------------------------------------------
# Chain 3: Root Cause -> K8s Rollback
# ---------------------------------------------------------------------------
section("CHAIN 3: Root Cause -> K8s Rollback Manifest")

chain3_prompt = f"""Based on this root cause analysis, generate a Kubernetes manifest
to safely rollback the affected deployment and apply resource fixes.

Root Cause Analysis:
{json.dumps(root_cause, indent=2)}

Generate:
1. A kubectl rollback command (as a comment)
2. An updated Deployment manifest with:
   - Resource limits (CPU and memory)
   - Readiness probe checking /actuator/health
   - Liveness probe checking /actuator/health
   - Environment variables for tuned connection pool settings
   - Security context (runAsNonRoot, readOnlyRootFilesystem)

Return ONLY the YAML manifest — no explanation."""

print(f"CHAIN 3: Root Cause JSON -> K8s Rollback Manifest\n")
print(f"  Input:  Same root cause JSON from Chain 1")
print(f"  Output: Production-ready K8s manifest\n")

ask_and_print(chain3_prompt, max_tokens=1500, label="CHAIN 3 OUTPUT")

teaching_point("""
Three chains, one incident:

  Error Log ──> [Chain 1] ──> Root Cause JSON
                                    │
                  ┌─────────────────┤
                  │                 │
            [Chain 2]         [Chain 3]
                  │                 │
          Ansible Playbook   K8s Manifest

Each chain is independent, testable, and retryable.
The JSON intermediate is the CONTRACT — like a REST API.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("CHAINING = MICROSERVICES FOR AI")
print("""
MICROSERVICES PATTERN         PROMPT CHAINING PATTERN
─────────────────────         ──────────────────────────
Each service = 1 job          Each prompt = 1 task
REST API = contract           JSON = contract between chains
Swap implementations          Swap models per chain
Independent scaling           Independent retry/debug
Compose into pipelines        Compose into workflows

IN PRODUCTION, this becomes:
  - A Python pipeline with error handling + retries
  - Intermediate results logged for observability
  - Each chain validated before the next runs
  - Different models for different chains (GPT-4o for analysis,
    GPT-4o-mini for code generation = cost optimization)

Next up: Putting it ALL together — a real SRE incident response pipeline.
""")

pause()
