# KEY TAKEAWAY: MCP (Model Context Protocol) lets AI tools talk to YOUR systems.
# Instead of copy-pasting data into prompts, MCP connects AI directly to your
# databases, APIs, monitoring, and internal tools — securely and in real time.

from config import banner, section, pause, teaching_point

banner(19, "MCP: Model Context Protocol",
       "Connect AI directly to YOUR systems — no more copy-pasting")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: The copy-paste problem")
print("""
Today you learned to INJECT context into prompts (RAG, Module 16).
But that requires MANUAL work:

  1. Open Grafana -> copy metrics
  2. Open logs -> copy error traces
  3. Open K8s -> copy manifest
  4. Open ServiceNow -> copy ticket details
  5. Paste ALL of it into a prompt

MCP solves this: AI connects DIRECTLY to your systems.

  ┌──────────────┐     MCP Protocol      ┌──────────────────┐
  │  AI Client   │ <===================> │   MCP Server     │
  │  (ChatGPT,   │    JSON-RPC over      │  (YOUR system)   │
  │   Claude,    │    stdio or HTTP       │                  │
  │   your app)  │                        │  - MongoDB       │
  └──────────────┘                        │  - Prometheus    │
                                          │  - Jenkins       │
                                          │  - ServiceNow    │
                                          │  - Git repos     │
                                          │  - K8s cluster   │
                                          └──────────────────┘

Instead of:  "Here's my log, analyze it"  (copy-paste)
MCP does:    AI asks the server "get me the last 100 error logs"  (direct)

MCP is an OPEN STANDARD by Anthropic, adopted by OpenAI, Google, and others.
Think of it as USB for AI — one protocol to connect everything.
""")

pause(tip="Analogy: 'MCP is like JDBC for AI — a standard way to connect to any data source.'")

# ---------------------------------------------------------------------------
# Architecture
# ---------------------------------------------------------------------------
section("MCP ARCHITECTURE: Client, Server, Tools, Resources")
print("""
MCP has 4 key concepts:

  1. MCP SERVER — Exposes your system's capabilities
     - Written in Python, Node.js, Java, etc.
     - Runs alongside your application
     - Declares TOOLS (actions) and RESOURCES (data)

  2. MCP CLIENT — The AI application that connects to servers
     - Claude Desktop, VS Code Copilot, your custom app
     - Discovers what tools/resources are available
     - Calls them on behalf of the user

  3. TOOLS — Actions the AI can take
     - "get_error_logs(service, last_n_minutes)"
     - "create_incident_ticket(severity, description)"
     - "restart_deployment(namespace, name)"
     - Like API endpoints, but for AI

  4. RESOURCES — Data the AI can read
     - "mongodb://returns/schema" (database schema)
     - "runbook://mongodb-connection-pool" (team docs)
     - "metrics://return-service/error-rate" (live metrics)
     - Like files, but dynamic and real-time

  ┌─────────────────────────────────────────────────────┐
  │                    MCP SERVER                       │
  │                                                     │
  │  TOOLS (actions):           RESOURCES (data):       │
  │  ├─ get_error_logs()       ├─ service://schema     │
  │  ├─ get_metrics()          ├─ runbook://mongodb    │
  │  ├─ create_ticket()        ├─ config://app-spec    │
  │  ├─ restart_pod()          └─ metrics://dashboard  │
  │  └─ run_health_check()                             │
  └─────────────────────────────────────────────────────┘
""")

pause()

# ---------------------------------------------------------------------------
# Demo 1: Build an MCP Server (Python)
# ---------------------------------------------------------------------------
section("DEMO 1: Build an MCP Server for your return-service")
print("""
Let's build an MCP server that exposes your return-service's
operations data to any AI client.

This server connects to your logs, metrics, and runbooks.
""")

MCP_SERVER_CODE = '''
# mcp_server.py — MCP Server for Return Service Operations
# Install: pip install mcp

from mcp.server import Server
from mcp.types import Tool, Resource, TextContent
import json
from datetime import datetime

# Create the MCP server
server = Server("return-service-ops")

# ─────────────────────────────────────────────────────────
# TOOL 1: Get recent error logs
# ─────────────────────────────────────────────────────────
@server.tool()
async def get_error_logs(service: str, minutes: int = 30) -> str:
    """Get recent error logs for a service.

    Args:
        service: Name of the service (e.g., 'return-service')
        minutes: How many minutes of logs to retrieve (default: 30)
    """
    # In production: query Elasticsearch, CloudWatch, or Loki
    # For demo: read from our sample file
    with open("samples/spring_boot_error.log") as f:
        logs = f.read()
    return f"Error logs for {service} (last {minutes} min):\\n{logs}"


# ─────────────────────────────────────────────────────────
# TOOL 2: Get current metrics
# ─────────────────────────────────────────────────────────
@server.tool()
async def get_metrics(service: str) -> str:
    """Get current Prometheus metrics for a service.

    Args:
        service: Name of the service
    """
    # In production: query Prometheus API
    # For demo: read from our sample alert
    with open("samples/prometheus_alert.json") as f:
        alert = json.load(f)
    metrics = alert.get("relatedMetrics", {})
    return json.dumps({
        "service": service,
        "timestamp": datetime.now().isoformat(),
        "http_5xx_rate": metrics.get("http_5xx_rate"),
        "p99_latency_ms": metrics.get("p99_latency_ms"),
        "active_db_connections": metrics.get("active_db_connections"),
        "memory_usage_percent": metrics.get("memory_usage_percent"),
        "cpu_usage_percent": metrics.get("cpu_usage_percent"),
    }, indent=2)


# ─────────────────────────────────────────────────────────
# TOOL 3: Create a ServiceNow incident ticket
# ─────────────────────────────────────────────────────────
@server.tool()
async def create_incident(
    severity: str,
    short_description: str,
    description: str,
    category: str = "Application"
) -> str:
    """Create a ServiceNow incident ticket.

    Args:
        severity: P1, P2, P3, or P4
        short_description: Brief title (max 160 chars)
        description: Full incident description
        category: Infrastructure, Application, Database, or Network
    """
    # In production: call ServiceNow REST API
    ticket = {
        "number": f"INC{datetime.now().strftime('%Y%m%d%H%M')}",
        "severity": severity,
        "short_description": short_description,
        "description": description,
        "category": category,
        "state": "New",
        "created": datetime.now().isoformat(),
    }
    return f"Ticket created: {json.dumps(ticket, indent=2)}"


# ─────────────────────────────────────────────────────────
# TOOL 4: Check deployment health
# ─────────────────────────────────────────────────────────
@server.tool()
async def check_health(service: str, namespace: str = "production") -> str:
    """Check the health status of a deployed service.

    Args:
        service: Name of the K8s deployment
        namespace: Kubernetes namespace (default: production)
    """
    # In production: kubectl get deployment + curl health endpoint
    return json.dumps({
        "service": service,
        "namespace": namespace,
        "replicas": {"desired": 3, "ready": 2, "available": 2},
        "health_endpoint": "/actuator/health",
        "health_status": "DOWN",
        "last_restart": "2026-09-28T14:35:00Z",
        "pod_statuses": [
            {"name": f"{service}-abc12", "status": "Running", "restarts": 0},
            {"name": f"{service}-def34", "status": "Running", "restarts": 2},
            {"name": f"{service}-ghi56", "status": "CrashLoopBackOff", "restarts": 5},
        ]
    }, indent=2)


# ─────────────────────────────────────────────────────────
# RESOURCE 1: Team runbook
# ─────────────────────────────────────────────────────────
@server.resource("runbook://mongodb-connection-pool")
async def get_runbook() -> str:
    """MongoDB Connection Pool Exhaustion runbook."""
    return """RUNBOOK: MongoDB Connection Pool Exhaustion
SEVERITY: P1 if error rate > 20%, P2 if > 10%

STEP 1 - VERIFY:
  kubectl exec -it <pod> -n production -- \\
    curl localhost:8080/actuator/metrics/mongodb.driver.pool.size

STEP 2 - FIX:
  Option A: kubectl edit configmap return-service-config -n production
    Add: ?maxPoolSize=100&minPoolSize=10
  Then: kubectl rollout restart deployment/return-service -n production

  Option B (scale pods): kubectl scale deployment/return-service --replicas=5

STEP 3 - VERIFY:
  Watch Grafana: https://grafana.internal/d/return-service
  5xx rate should drop below 5% within 5 minutes

ESCALATION:
  P1: Page DB team lead + VP Engineering via #incidents
  P2: Slack #db-oncall during business hours"""


# ─────────────────────────────────────────────────────────
# RESOURCE 2: Application config/spec
# ─────────────────────────────────────────────────────────
@server.resource("config://return-service")
async def get_app_config() -> str:
    """Current application configuration and SLAs."""
    return json.dumps({
        "name": "return-service",
        "port": 8080,
        "database": "MongoDB 7",
        "sla": {
            "p99_latency": "500ms",
            "error_rate": "< 1%",
            "uptime": "99.9%"
        },
        "team": "sustain-engineering",
        "oncall_channel": "#sustain-oncall",
        "escalation": "Platform Team Lead -> VP Engineering"
    }, indent=2)


# ─────────────────────────────────────────────────────────
# Run the server
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server

    async def main():
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())

    asyncio.run(main())
'''

print(MCP_SERVER_CODE)

teaching_point("""
This is a COMPLETE MCP server in ~100 lines of Python.

4 TOOLS the AI can call:
  get_error_logs()    — fetch logs from your logging system
  get_metrics()       — fetch metrics from Prometheus
  create_incident()   — create a ServiceNow ticket
  check_health()      — check K8s deployment status

2 RESOURCES the AI can read:
  runbook://mongodb   — your team's runbook (RAG, but automatic!)
  config://return     — app config and SLAs

In production, replace the mock data with:
  - Elasticsearch/Loki queries for logs
  - Prometheus API for metrics
  - ServiceNow REST API for tickets
  - kubectl commands for health checks
""")

pause()

# ---------------------------------------------------------------------------
# Demo 2: Build an MCP Client
# ---------------------------------------------------------------------------
section("DEMO 2: Build an MCP Client — AI that uses your tools")
print("""
Now let's build the CLIENT that connects to this server.
The client gives the AI access to the tools and resources.
""")

MCP_CLIENT_CODE = '''
# mcp_client.py — AI assistant that uses MCP tools
# Install: pip install mcp openai

from mcp.client import Client
from mcp.client.stdio import stdio_client
from openai import OpenAI
import json, asyncio

openai = OpenAI()

async def run_assistant():
    # Connect to our MCP server
    async with stdio_client("python", "mcp_server.py") as (read, write):
        async with Client("incident-assistant", read, write) as client:

            # Discover available tools
            tools = await client.list_tools()
            print(f"Connected! {len(tools)} tools available:")
            for tool in tools:
                print(f"  - {tool.name}: {tool.description[:60]}")

            # Convert MCP tools to OpenAI function format
            openai_tools = []
            for tool in tools:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema,
                    }
                })

            # User asks a question
            user_question = """
            return-service seems to be having issues.
            Check its health, get the error logs, and tell me
            what's wrong. If it's a P1, create an incident ticket.
            """

            print(f"\\nUser: {user_question.strip()}")
            print("\\nAI is working (calling tools automatically)...\\n")

            # Send to OpenAI with tools
            messages = [
                {"role": "system", "content": """You are an SRE assistant
                    with access to production monitoring tools.
                    Use the tools to gather data before making conclusions.
                    Always check health and logs before diagnosing."""},
                {"role": "user", "content": user_question}
            ]

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=openai_tools,
            )

            # Process tool calls
            while response.choices[0].message.tool_calls:
                msg = response.choices[0].message
                messages.append(msg)

                for tool_call in msg.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    print(f"  [TOOL CALL] {name}({args})")

                    # Execute the tool via MCP
                    result = await client.call_tool(name, args)
                    tool_output = result.content[0].text
                    print(f"  [TOOL RESULT] {tool_output[:100]}...")

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_output,
                    })

                # Let AI process tool results and decide next action
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    tools=openai_tools,
                )

            # Final answer
            print(f"\\n{'='*60}")
            print(f"  AI DIAGNOSIS (grounded in real data)")
            print(f"{'='*60}\\n")
            print(response.choices[0].message.content)

asyncio.run(run_assistant())
'''

print(MCP_CLIENT_CODE)

teaching_point("""
What just happened:

  1. Client CONNECTS to MCP server (discovers 4 tools)
  2. User asks: "What's wrong with return-service?"
  3. AI DECIDES which tools to call (check_health, get_error_logs)
  4. MCP server EXECUTES the tools (queries your systems)
  5. AI ANALYZES the real data and diagnoses
  6. If P1: AI calls create_incident() to open a ticket

The AI doesn't just GUESS — it CHECKS your actual systems.
No copy-pasting. No stale data. Real-time, automated.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 3: Simulate the flow
# ---------------------------------------------------------------------------
section("DEMO 3: Simulated MCP flow (what it looks like in action)")

from config import ask_and_print

# Simulate what the AI sees after calling tools
error_log = open("samples/spring_boot_error.log").read()
alert = open("samples/prometheus_alert.json").read()

simulated_tool_results = f"""I called the following MCP tools and got these results:

[TOOL: check_health("return-service", "production")]
RESULT:
{{
  "replicas": {{"desired": 3, "ready": 2, "available": 2}},
  "health_status": "DOWN",
  "pod_statuses": [
    {{"name": "return-service-abc12", "status": "Running", "restarts": 0}},
    {{"name": "return-service-def34", "status": "Running", "restarts": 2}},
    {{"name": "return-service-ghi56", "status": "CrashLoopBackOff", "restarts": 5}}
  ]
}}

[TOOL: get_error_logs("return-service", 30)]
RESULT:
{error_log}

[TOOL: get_metrics("return-service")]
RESULT:
{alert}

[RESOURCE: runbook://mongodb-connection-pool]
RESULT: Team runbook loaded (MongoDB pool exhaustion procedures)

Based on ALL the data gathered from tools, provide:
1. Diagnosis (what's wrong and why)
2. Severity (using the runbook's criteria)
3. Immediate action (exact commands from the runbook)
4. Whether to create an incident ticket (if P1/P2, call create_incident)
"""

ask_and_print(simulated_tool_results,
    system_msg="""You are an SRE assistant connected to production systems via MCP.
You have real-time access to health checks, logs, metrics, and runbooks.
Base your diagnosis ONLY on the tool results — never guess.
If severity is P1 or P2, recommend creating an incident ticket.""",
    max_tokens=2000, label="MCP-POWERED AI DIAGNOSIS")

teaching_point("""
Compare this with Module 10 (Incident Responder):

  MODULE 10: You manually pasted logs + alert + manifest into the prompt
  MODULE 19: MCP tools AUTOMATICALLY fetched the data

  MODULE 10: Runbook was copy-pasted (RAG style)
  MODULE 19: Runbook was a RESOURCE the AI reads on demand

  MODULE 10: ServiceNow ticket was generated as JSON text
  MODULE 19: AI would CALL create_incident() to actually create it

MCP = RAG + Automation + Real-time data + Actions
""")

pause()

# ---------------------------------------------------------------------------
# Real-world MCP ecosystem
# ---------------------------------------------------------------------------
section("THE MCP ECOSYSTEM: What's already available")
print("""
MCP SERVERS THAT EXIST TODAY:
  ┌─────────────────────────────────────────────────────┐
  │  DATABASES                                          │
  │  ├── PostgreSQL — query, schema, explain plans      │
  │  ├── MongoDB — query, aggregations, indexes         │
  │  ├── Redis — get/set, cache management              │
  │  └── Elasticsearch — search, index management       │
  │                                                     │
  │  DEVOPS                                             │
  │  ├── Docker — list containers, logs, exec           │
  │  ├── Kubernetes — pods, deployments, logs, exec     │
  │  ├── GitHub — PRs, issues, code search, actions     │
  │  └── Jenkins — trigger builds, get status           │
  │                                                     │
  │  MONITORING                                         │
  │  ├── Prometheus — query metrics, alert rules        │
  │  ├── Grafana — dashboards, annotations              │
  │  ├── PagerDuty — incidents, on-call schedules       │
  │  └── Datadog — metrics, logs, traces                │
  │                                                     │
  │  PRODUCTIVITY                                       │
  │  ├── Slack — messages, channels, search              │
  │  ├── Jira — issues, boards, sprints                 │
  │  ├── Confluence — pages, search, create             │
  │  ├── Notion — pages, databases, search              │
  │  └── Google Drive — docs, sheets, search            │
  │                                                     │
  │  FILE SYSTEMS                                       │
  │  ├── Local filesystem — read, write, search         │
  │  ├── Git — diff, log, blame, branch                 │
  │  └── S3 — list, read, upload                        │
  └─────────────────────────────────────────────────────┘

You don't have to build everything from scratch.
Many MCP servers are open-source and ready to use.
""")

pause()

# ---------------------------------------------------------------------------
# How it connects to their work
# ---------------------------------------------------------------------------
section("MCP FOR YOUR SUSTAIN ENGINEERING TEAM")
print("""
Imagine your team's AI assistant with these MCP servers connected:

  ┌──────────────────────────────────────────────────────┐
  │                                                      │
  │  "Hey AI, return-service is slow. What's happening?" │
  │                                                      │
  │  AI thinks: I need data. Let me check...             │
  │                                                      │
  │  1. [MCP: K8s]         -> check pod health           │
  │  2. [MCP: Prometheus]  -> check error rate + latency │
  │  3. [MCP: Elasticsearch] -> get recent error logs    │
  │  4. [MCP: Confluence]  -> fetch relevant runbook     │
  │  5. [MCP: Git]         -> check recent deploys       │
  │                                                      │
  │  AI: "Based on my investigation:                     │
  │   - Pod ghi56 is in CrashLoopBackOff (5 restarts)   │
  │   - MongoDB connections are at 50/50 (exhausted)     │
  │   - Error started 12 min after last deploy (commit   │
  │     a1b2c3 added new retry logic without pool limit) │
  │   - Runbook says: increase pool to 100, restart      │
  │                                                      │
  │   Should I create a P1 incident ticket and           │
  │   restart the deployment?"                           │
  │                                                      │
  │  You: "Yes, do it."                                  │
  │                                                      │
  │  6. [MCP: ServiceNow]  -> creates INC20260928       │
  │  7. [MCP: K8s]         -> kubectl rollout restart    │
  │  8. [MCP: Slack]       -> posts update to #incidents │
  │                                                      │
  └──────────────────────────────────────────────────────┘

This is the FUTURE of SRE. And you're learning it TODAY.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("MCP: FROM PROMPTS TO PRODUCTION AI")
print("""
THE JOURNEY (what you learned today):

  Module 1-7:   Prompt Engineering  — HOW to talk to AI
  Module 8-9:   Structured Output   — AI output for pipelines
  Module 10:    Incident Response    — All techniques combined
  Module 11:    Hallucinations       — When AI fails
  Module 12:    Capstone             — Prove your skills
  Module 13-15: Daily Work           — Code review, testing, post-mortems
  Module 16:    RAG                  — Inject YOUR knowledge
  Module 17:    DevOps               — Generate infra from specs
  Module 18:    Prompt Library       — Templates for daily use
  Module 19:    MCP                  — Connect AI to YOUR systems

THE EVOLUTION:
  Copy-paste    -> Prompt Engineering -> RAG -> MCP
  (manual)         (better questions)    (your docs)  (live systems)

  Each step REDUCES manual work and INCREASES AI's usefulness.

MCP is where prompt engineering meets PRODUCTION SYSTEMS.
Your prompting skills + MCP tools = AI-augmented SRE.

  ╔══════════════════════════════════════════════════════╗
  ║  AI doesn't replace engineers.                      ║
  ║  AI replaces engineers who don't use AI.            ║
  ║                                                      ║
  ║  You now know HOW to use AI.                        ║
  ║  Go build something amazing.                        ║
  ╚══════════════════════════════════════════════════════╝
""")

pause()
