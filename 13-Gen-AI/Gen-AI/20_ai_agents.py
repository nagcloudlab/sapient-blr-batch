# KEY TAKEAWAY: AI Agents don't just answer questions — they PURSUE GOALS.
# Given a goal, an agent decides WHAT to do, DOES it, OBSERVES the result,
# and DECIDES what to do next — in a loop until the goal is achieved.

import json
from config import banner, section, ask_and_print, ask, pause, teaching_point, openai_client, OPENAI_MODEL

banner(20, "AI Agents: From Prompts to Autonomous Action",
       "The evolution: Prompts -> Chains -> Agents -> Autonomous SRE")

# ---------------------------------------------------------------------------
# Concept: The evolution
# ---------------------------------------------------------------------------
section("THE EVOLUTION: How we got here")
print("""
Look at your journey TODAY — each module built toward this:

  MODULE 1-7:  SINGLE PROMPT
               Human writes prompt -> AI responds -> done
               "Review this Dockerfile"

  MODULE 9:    PROMPT CHAIN
               Human designs the pipeline -> AI executes each step
               Log -> [AI] -> Root Cause -> [AI] -> Ansible -> [AI] -> K8s

  MODULE 19:   MCP TOOLS
               AI can CALL tools -> but human still orchestrates
               "Check health, then get logs, then create ticket"

  MODULE 20:   AI AGENT
               Human gives a GOAL -> Agent figures out the rest
               "Fix the production incident"

               Agent THINKS: What do I need to know?
               Agent ACTS:   Calls check_health()
               Agent OBSERVES: Pod is in CrashLoopBackOff
               Agent THINKS: I need more context. Let me check logs.
               Agent ACTS:   Calls get_error_logs()
               Agent OBSERVES: MongoDB pool exhaustion
               Agent THINKS: I know the fix. Let me apply it.
               Agent ACTS:   Calls restart_deployment()
               Agent OBSERVES: Pods restarting. Let me verify.
               Agent ACTS:   Calls check_health() again
               Agent OBSERVES: All pods healthy. Error rate dropping.
               Agent CONCLUDES: Incident resolved. Creating ticket.

  This is the THINK -> ACT -> OBSERVE loop.
  The agent decides WHAT to do, WHEN, and HOW MANY TIMES.
""")

pause(tip="Draw the Think->Act->Observe loop on the whiteboard. It's the core concept.")

# ---------------------------------------------------------------------------
# Architecture
# ---------------------------------------------------------------------------
section("AGENT ARCHITECTURE: The ReAct Pattern")
print("""
The most common agent pattern is ReAct (Reasoning + Acting):

  ┌─────────────────────────────────────────────────────┐
  │                                                     │
  │           ┌──────────┐                              │
  │     ┌────>│  THINK   │ What should I do next?       │
  │     │     │(Reasoning)│ What do I know? What's       │
  │     │     └────┬─────┘ missing?                     │
  │     │          │                                    │
  │     │          ▼                                    │
  │     │     ┌──────────┐                              │
  │     │     │   ACT    │ Call a tool, read a resource, │
  │     │     │ (Action) │ generate code, ask user       │
  │     │     └────┬─────┘                              │
  │     │          │                                    │
  │     │          ▼                                    │
  │     │     ┌──────────┐                              │
  │     └─────│ OBSERVE  │ What happened? Did it work?  │
  │           │(Result)  │ Do I need more info?          │
  │           └────┬─────┘                              │
  │                │                                    │
  │                ▼                                    │
  │           Goal achieved?                            │
  │           YES -> Return final answer                │
  │           NO  -> Loop back to THINK                 │
  │                                                     │
  └─────────────────────────────────────────────────────┘

KEY DIFFERENCE FROM CHAINS:
  Chain:  Human designs steps 1,2,3 in advance
  Agent:  AI decides steps DYNAMICALLY based on what it finds
""")

pause()

# ---------------------------------------------------------------------------
# Demo 1: Build an agent from scratch
# ---------------------------------------------------------------------------
section("DEMO 1: Build an SRE Agent from scratch (Python)")
print("""
Let's build a real agent — not a library, not a framework.
Just Python + OpenAI + a Think/Act/Observe loop.
""")

AGENT_CODE = '''
# sre_agent.py — A simple SRE agent that diagnoses incidents autonomously
# No frameworks. Just Python + OpenAI + tool loop.

import json
from openai import OpenAI

client = OpenAI()

# ── TOOLS the agent can use ──────────────────────────────
def check_health(service, namespace="production"):
    """Check deployment health in Kubernetes."""
    return json.dumps({
        "service": service,
        "namespace": namespace,
        "replicas": {"desired": 3, "ready": 2},
        "health_status": "DEGRADED",
        "pods": [
            {"name": f"{service}-abc12", "status": "Running", "restarts": 0},
            {"name": f"{service}-def34", "status": "Running", "restarts": 2},
            {"name": f"{service}-ghi56", "status": "CrashLoopBackOff", "restarts": 5},
        ]
    })

def get_error_logs(service, minutes=30):
    """Fetch recent error logs."""
    return """MongoTimeoutException: Timed out after 30000ms waiting for server
    Connection pool exhausted: active=50/50, pending=23
    ReturnService.createReturn failed: Unable to acquire connection
    RefundService.processRefund timeout: 5000ms exceeded
    HikariPool health check failed: Active=50/50, Idle=0, Waiting=23"""

def get_metrics(service):
    """Fetch current Prometheus metrics."""
    return json.dumps({
        "http_5xx_rate": "38.7%",
        "p99_latency_ms": 12450,
        "active_db_connections": "50/50",
        "memory_percent": 87.3,
    })

def get_runbook(topic):
    """Fetch team runbook for a topic."""
    if "mongo" in topic.lower() or "connection" in topic.lower():
        return """RUNBOOK: MongoDB Pool Exhaustion
        STEP 1: kubectl edit configmap return-service-config -n production
                Add: ?maxPoolSize=100&minPoolSize=10
        STEP 2: kubectl rollout restart deployment/return-service -n production
        STEP 3: Verify on Grafana — 5xx should drop below 5% in 5 min
        ESCALATE: P1 -> page DB lead + VP Eng via #incidents"""
    return "No runbook found for: " + topic

def create_incident(severity, title, description):
    """Create ServiceNow incident ticket."""
    return f"CREATED: INC20260928 | {severity} | {title}"

def restart_deployment(service, namespace="production"):
    """Restart a K8s deployment (rolling restart)."""
    return f"Rolling restart initiated: {service} in {namespace}. ETA: 2 minutes."

def notify_slack(channel, message):
    """Post a message to Slack."""
    return f"Posted to {channel}: {message[:80]}..."

# ── Tool registry ────────────────────────────────────────
TOOLS = {
    "check_health": check_health,
    "get_error_logs": get_error_logs,
    "get_metrics": get_metrics,
    "get_runbook": get_runbook,
    "create_incident": create_incident,
    "restart_deployment": restart_deployment,
    "notify_slack": notify_slack,
}

TOOL_SCHEMAS = [
    {"type": "function", "function": {"name": "check_health", "description": "Check K8s deployment health", "parameters": {"type": "object", "properties": {"service": {"type": "string"}, "namespace": {"type": "string", "default": "production"}}, "required": ["service"]}}},
    {"type": "function", "function": {"name": "get_error_logs", "description": "Fetch recent error logs", "parameters": {"type": "object", "properties": {"service": {"type": "string"}, "minutes": {"type": "integer", "default": 30}}, "required": ["service"]}}},
    {"type": "function", "function": {"name": "get_metrics", "description": "Fetch Prometheus metrics", "parameters": {"type": "object", "properties": {"service": {"type": "string"}}, "required": ["service"]}}},
    {"type": "function", "function": {"name": "get_runbook", "description": "Fetch team runbook by topic", "parameters": {"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]}}},
    {"type": "function", "function": {"name": "create_incident", "description": "Create ServiceNow ticket", "parameters": {"type": "object", "properties": {"severity": {"type": "string"}, "title": {"type": "string"}, "description": {"type": "string"}}, "required": ["severity", "title", "description"]}}},
    {"type": "function", "function": {"name": "restart_deployment", "description": "Rolling restart a K8s deployment", "parameters": {"type": "object", "properties": {"service": {"type": "string"}, "namespace": {"type": "string", "default": "production"}}, "required": ["service"]}}},
    {"type": "function", "function": {"name": "notify_slack", "description": "Post message to Slack channel", "parameters": {"type": "object", "properties": {"channel": {"type": "string"}, "message": {"type": "string"}}, "required": ["channel", "message"]}}},
]

# ── THE AGENT LOOP ───────────────────────────────────────
def run_agent(goal, max_steps=10):
    """Run the SRE agent with a goal."""
    messages = [
        {"role": "system", "content": """You are an autonomous SRE agent.
Given a goal, you independently investigate, diagnose, and resolve issues.

RULES:
1. Always gather data BEFORE making conclusions
2. Check health + logs + metrics before diagnosing
3. Consult the runbook before taking action
4. Create an incident ticket for P1/P2 issues
5. Notify Slack after taking any production action
6. Verify your fix worked after applying it
7. Stop when the goal is achieved or you need human approval"""},
        {"role": "user", "content": f"GOAL: {goal}"}
    ]

    for step in range(1, max_steps + 1):
        print(f"\\n{'─'*50}")
        print(f"  AGENT STEP {step}")
        print(f"{'─'*50}")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        msg = response.choices[0].message

        # If agent wants to call tools
        if msg.tool_calls:
            messages.append(msg)
            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                print(f"  THINK -> I need to call: {name}")
                print(f"  ACT   -> {name}({json.dumps(args)})")
                result = TOOLS[name](**args)
                print(f"  OBSERVE -> {str(result)[:120]}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result),
                })
        else:
            # Agent is done — return conclusion
            print(f"  CONCLUDE -> Agent finished\\n")
            return msg.content

    return "Agent reached max steps without concluding."

# ── RUN ──────────────────────────────────────────────────
result = run_agent(
    "return-service has a high error rate alert. "
    "Investigate, diagnose, fix if possible, "
    "and create an incident ticket."
)
print("="*60)
print("  AGENT FINAL REPORT")
print("="*60)
print(result)
'''

print(AGENT_CODE)

teaching_point("""
THIS IS A COMPLETE AI AGENT in ~80 lines of core logic.

The key: run_agent() is a LOOP:
  1. Send goal + history to AI
  2. AI decides: call a tool OR conclude
  3. If tool: execute it, add result to history, loop
  4. If conclude: return the final answer

The AI autonomously chose:
  check_health -> get_error_logs -> get_metrics ->
  get_runbook -> restart_deployment -> check_health (verify) ->
  create_incident -> notify_slack

Nobody told it this order. It FIGURED IT OUT from the goal.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 2: Run the agent live
# ---------------------------------------------------------------------------
section("DEMO 2: Watch the agent work (live)")

print("Running the SRE agent with goal:")
print('  "return-service has high error rate. Investigate, diagnose, fix, ticket."\n')

# We'll simulate the agent loop using the actual OpenAI API
messages = [
    {"role": "system", "content": """You are an autonomous SRE agent at Publicis Sapient.
Given a goal, you independently investigate, diagnose, and resolve production issues.

You have these tools available:
1. check_health(service) — returns pod status, replica count, health
2. get_error_logs(service) — returns recent error log entries
3. get_metrics(service) — returns current Prometheus metrics
4. get_runbook(topic) — returns team runbook for a topic
5. create_incident(severity, title, description) — creates ServiceNow ticket
6. restart_deployment(service) — rolling restart in K8s
7. notify_slack(channel, message) — posts to Slack

RULES:
- Always gather data BEFORE concluding (check health + logs + metrics)
- Consult runbook BEFORE taking action
- Create incident ticket for P1/P2
- Notify Slack after any production action
- Verify fix after applying it

Simulate the tool calls by describing what you would do at each step.
Format each step as:

STEP N:
  THINK: [your reasoning]
  ACT: [tool_name(args)]
  OBSERVE: [what you expect to find]

Continue until the incident is resolved. Then give a final summary."""},
    {"role": "user", "content": """GOAL: return-service has a high error rate alert (38.7% 5xx).
Investigate, diagnose, fix if possible, and create an incident ticket.

Available context:
- Service: return-service in production namespace
- Alert: HighErrorRate fired 12 minutes ago
- The team uses MongoDB, Spring Boot, Kubernetes
- You have access to all 7 tools listed above

Show me your COMPLETE thought process, step by step."""}
]

response = ask(messages[1]["content"], system_msg=messages[0]["content"], max_tokens=3000)

print(f"\n{'='*70}")
print(f"  AGENT EXECUTION TRACE")
print(f"{'='*70}\n")
print(response)

teaching_point("""
Watch the agent's REASONING:

  Step 1: "I need to understand the current state" -> check_health
  Step 2: "Health is degraded, I need to know WHY" -> get_error_logs
  Step 3: "Logs show MongoDB issues, let me confirm" -> get_metrics
  Step 4: "Confirmed. What does the runbook say?" -> get_runbook
  Step 5: "Runbook says increase pool + restart" -> restart_deployment
  Step 6: "Applied fix, let me verify" -> check_health (again!)
  Step 7: "Fix confirmed. This is P1" -> create_incident
  Step 8: "Team needs to know" -> notify_slack

The agent REASONED about what to do at each step.
It didn't follow a script. It ADAPTED based on what it found.

What if the logs showed a DIFFERENT root cause (not MongoDB)?
The agent would have followed a DIFFERENT path.
THAT is the power of agents over chains.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 3: Agent vs Chain vs Prompt — side by side
# ---------------------------------------------------------------------------
section("DEMO 3: The evolution — all three approaches compared")
print("""
Let's see the SAME task handled three ways:

TASK: "return-service has high error rate. Diagnose and fix."

  ┌─────────────────────────────────────────────────────────┐
  │  APPROACH 1: SINGLE PROMPT (Modules 1-7)                │
  │                                                         │
  │  Human:  "Here are the logs and metrics. What's wrong?" │
  │  AI:     "Looks like MongoDB pool exhaustion."          │
  │  Human:  "Now write an Ansible playbook to fix it."     │
  │  AI:     [generates playbook]                           │
  │  Human:  "Now create a ServiceNow ticket."              │
  │  AI:     [generates ticket]                             │
  │                                                         │
  │  Steps: Human drives EVERY step                         │
  │  Tools: None (copy-paste data)                          │
  │  Decisions: ALL made by human                           │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │  APPROACH 2: PROMPT CHAIN (Module 9)                    │
  │                                                         │
  │  Human designs pipeline:                                │
  │    Step 1: Log -> Root Cause (JSON)                     │
  │    Step 2: Root Cause -> Ansible Playbook               │
  │    Step 3: Root Cause -> K8s Manifest                   │
  │                                                         │
  │  Steps: Human designs, AI executes each                 │
  │  Tools: None (data passed between steps)                │
  │  Decisions: Pipeline is FIXED — same path every time    │
  └─────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────┐
  │  APPROACH 3: AI AGENT (Module 20)                       │
  │                                                         │
  │  Human: "Fix the production incident."                  │
  │  Agent: [THINK] I need to check health first            │
  │  Agent: [ACT]   check_health("return-service")          │
  │  Agent: [OBSERVE] Pod in CrashLoopBackOff               │
  │  Agent: [THINK] Need logs to understand why             │
  │  Agent: [ACT]   get_error_logs("return-service")        │
  │  Agent: [OBSERVE] MongoDB pool exhaustion               │
  │  Agent: [THINK] Let me check the runbook                │
  │  Agent: [ACT]   get_runbook("mongodb connection pool")  │
  │  Agent: [OBSERVE] Runbook says restart + scale pool     │
  │  Agent: [ACT]   restart_deployment("return-service")    │
  │  Agent: [ACT]   create_incident("P1", ...)              │
  │  Agent: [ACT]   notify_slack("#incidents", ...)         │
  │                                                         │
  │  Steps: Agent decides DYNAMICALLY                       │
  │  Tools: Agent calls them AUTONOMOUSLY                   │
  │  Decisions: Agent adapts based on what it FINDS         │
  └─────────────────────────────────────────────────────────┘
""")

teaching_point("""
THE KEY INSIGHT:

  Prompt:  Human does thinking + typing
  Chain:   Human does thinking, AI does typing
  Agent:   AI does thinking + typing, human SUPERVISES

As you move right, the AI takes on MORE responsibility.
But YOU remain the SUPERVISOR — the one who:
  - Defines the GOAL
  - Sets the RULES (system prompt)
  - Provides the TOOLS
  - Reviews the ACTIONS
  - Approves CRITICAL decisions (restart? create ticket?)
""")

pause()

# ---------------------------------------------------------------------------
# Agent frameworks
# ---------------------------------------------------------------------------
section("AGENT FRAMEWORKS YOU CAN USE")
print("""
You don't have to build agents from scratch. Frameworks exist:

  ┌────────────────────────────────────────────────────────┐
  │  FRAMEWORK           BEST FOR                         │
  │  ─────────────────── ──────────────────────────────── │
  │  OpenAI Assistants   Quick start, hosted by OpenAI    │
  │  Anthropic Agent SDK Claude-based agents, tool use    │
  │  LangChain/LangGraph Complex multi-agent workflows    │
  │  CrewAI              Team of specialized agents       │
  │  AutoGen (Microsoft) Multi-agent conversations        │
  │  Haystack            Production RAG + agents          │
  └────────────────────────────────────────────────────────┘

  FOR YOUR TEAM (recommended starting point):
    1. Start with OpenAI function calling (what we built today)
    2. Add MCP servers for your tools (Module 19)
    3. Wrap in a simple agent loop (this module)
    4. Graduate to LangGraph when you need complex workflows
""")

pause()

# ---------------------------------------------------------------------------
# The complete picture
# ---------------------------------------------------------------------------
section("THE COMPLETE PICTURE: Your 45+1 Day Journey")
print("""
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║   DAYS 1-45: SUSTAIN ENGINEERING                         ║
  ║   ─────────────────────────────────                      ║
  ║   HTML/CSS -> JavaScript -> Java -> Spring Boot          ║
  ║   -> Node.js -> MongoDB -> Docker -> Kubernetes          ║
  ║   -> Jenkins -> Ansible -> Prometheus -> Grafana          ║
  ║   -> ServiceNow -> ITSM -> Capstone Projects             ║
  ║                                                          ║
  ║   = You can BUILD and OPERATE production systems         ║
  ║                                                          ║
  ║                                                          ║
  ║   DAY 46: GEN-AI                                         ║
  ║   ─────────────────                                      ║
  ║   Prompt Engineering -> Few-shot -> CoT                  ║
  ║   -> Structured Output -> Chaining -> RAG                ║
  ║   -> Code Review -> Testing -> Post-Mortems              ║
  ║   -> DevOps Generation -> MCP -> Agents                  ║
  ║                                                          ║
  ║   = You can AMPLIFY everything you build and operate     ║
  ║                                                          ║
  ║                                                          ║
  ║   THE EQUATION:                                          ║
  ║                                                          ║
  ║   45 days of engineering    x   AI amplification         ║
  ║   (the knowledge)              (the speed)               ║
  ║   ─────────────────────────────────────────────          ║
  ║   = Engineer who builds 10x faster                       ║
  ║     with 10x fewer blind spots                           ║
  ║     and 10x better documentation                         ║
  ║                                                          ║
  ║                                                          ║
  ║   AI doesn't replace engineers.                          ║
  ║   AI replaces engineers who don't use AI.                ║
  ║                                                          ║
  ║   You now know BOTH.                                     ║
  ║                                                          ║
  ║   Go build something amazing.                            ║
  ║                                                          ║
  ╚══════════════════════════════════════════════════════════╝
""")
