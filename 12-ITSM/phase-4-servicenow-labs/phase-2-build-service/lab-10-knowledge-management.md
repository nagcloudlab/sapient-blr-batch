# Lab 10: Knowledge Management

**Level:** Intermediate | **Duration:** 60 min | **Prerequisites:** Labs 07-09 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand ITIL 4 Knowledge Management practice and the DIKW model
- Build a complete Knowledge Base structure for UPI Operations
- Create realistic, production-quality knowledge articles (error code guides, runbooks, KEDB entries)
- Configure article approval workflows (Draft, Review, Published, Retired)
- Integrate Knowledge with Incident Management (suggested articles)
- Establish a Known Error Database (KEDB) linked to Problem records
- Use Knowledge-Centered Service (KCS) principles to embed knowledge into daily operations

---

## Scenario

NPCI's UPI platform team has been operating for several months. Tribal knowledge is scattered across Slack messages, personal notes, and the minds of senior engineers. After a recent P1 incident where a junior NOC engineer could not find the correct restart procedure and escalated unnecessarily, Ravi Kumar (Platform Engineering Lead) has been tasked with building a centralized Knowledge Base in ServiceNow. The goal: every common issue has a documented resolution, every runbook is version-controlled, and every known error has a published workaround.

---

## Part 1: ITIL 4 Knowledge Management Theory

### 1.1 Practice Definition

Knowledge Management is an ITIL 4 general management practice that ensures stakeholders get the right information, in the proper format, at the correct level, and at the right time. Its purpose is to maintain and improve the effective, efficient, and convenient use of information and knowledge across the organization.

In the context of UPI operations, this means that when Priya Sharma in the NOC sees a spike in transaction failures at 2 AM, she should be able to find a relevant runbook in under 60 seconds without waking up a senior engineer.

### 1.2 The DIKW Model

The DIKW model describes the transformation of raw signals into actionable understanding:

```
+------------------------------------------------------------------+
|                        WISDOM                                     |
|   "We should pre-scale UPI services before festival seasons       |
|    because transaction volumes spike 300% and cause timeout       |
|    errors if capacity is not added 48 hours in advance."          |
+------------------------------------------------------------------+
|                       KNOWLEDGE                                   |
|   "UPI timeout errors (U01) increase when transaction volume      |
|    exceeds 80% of provisioned capacity. Restarting the            |
|    transaction service clears the connection pool and restores    |
|    throughput within 5 minutes."                                  |
+------------------------------------------------------------------+
|                      INFORMATION                                  |
|   "Between 10:00-10:15 IST, 847 transactions failed with         |
|    error code U01. The transaction service has been running       |
|    for 14 days without restart. Memory usage is at 94%."          |
+------------------------------------------------------------------+
|                         DATA                                      |
|   error_code=U01, count=847, timestamp=2024-01-15T10:00:00Z,     |
|   service=upi-txn-service, memory_pct=94, uptime_days=14         |
+------------------------------------------------------------------+
```

- **Data:** Raw metrics and logs from Prometheus, Grafana, and application logs
- **Information:** Data organized with context (dashboards, alerts, incident records)
- **Knowledge:** Documented understanding of cause-and-effect (KB articles, runbooks)
- **Wisdom:** Judgment applied over time (architectural decisions, capacity planning)

### 1.3 Types of Knowledge

| Type | Definition | UPI Example |
|------|-----------|-------------|
| **Tacit** | Personal, experience-based, hard to document | Ravi knows that the PostgreSQL failover behaves differently when triggered during peak hours vs. off-peak |
| **Explicit** | Documented, structured, shareable | A step-by-step runbook for database failover published in the Knowledge Base |

The goal of Knowledge Management is to convert as much tacit knowledge as possible into explicit knowledge. When Amit Verma documents his mental model of "how to diagnose a settlement batch failure," that tacit knowledge becomes an explicit KB article that the entire team can use.

### 1.4 Knowledge Lifecycle

```
  +--------+     +--------+     +-----------+     +---------+     +---------+
  | Create | --> | Review | --> | Published | --> | Archive | --> | Retire  |
  +--------+     +--------+     +-----------+     +---------+     +---------+
       |              |                                                 |
       |         (Rejected)                                       (Deleted)
       |              |
       v              v
  +--------+     +--------+
  | Draft  | <-- | Rework |
  +--------+     +--------+
```

- **Create:** Author drafts the article (e.g., Amit writes a new runbook)
- **Review:** Subject matter expert validates accuracy (e.g., Ravi Kumar reviews)
- **Published:** Article is visible to target audience
- **Archive:** Article is no longer actively shown but retained for reference
- **Retire:** Article is removed from the Knowledge Base entirely

### 1.5 Knowledge-Centered Service (KCS)

KCS is a methodology that integrates knowledge creation and maintenance into the daily workflow rather than treating it as a separate activity. Key principles:

1. **Capture in the workflow:** When resolving an incident, document the solution immediately
2. **Evolve with demand:** Articles are improved each time they are used
3. **Develop a knowledge base of collective experience:** Not one person's notes, but the team's shared understanding
4. **Reward learning, collaboration, sharing, and improving:** Recognize contributors

In ServiceNow, KCS is supported by:
- "Create Knowledge" button on the Incident form
- Article feedback and flagging
- Usage analytics (views, helpfulness ratings)
- Integration with the search engine

### 1.6 Knowledge Integration with ITSM Processes

```
+-------------------+     Suggested Articles      +--------------------+
|                   | <--------------------------- |                    |
| Incident Mgmt    |     "Create Knowledge"       | Knowledge Mgmt     |
|                   | ---------------------------> |                    |
+-------------------+                              +--------------------+
                                                          ^    |
+-------------------+     Known Error Articles            |    |
|                   | ----------------------------------->|    |
| Problem Mgmt     |     Workaround Documentation        |    |
|                   | <-----------------------------------|    |
+-------------------+                                          |
                                                               |
+-------------------+     Implementation Plans                 |
|                   | <----------------------------------------+
| Change Mgmt      |     Change Guides
|                   |
+-------------------+
```

- **Incident Management:** Agents search KB for solutions; resolved incidents can generate new KB articles
- **Problem Management:** Known Errors are documented as KB articles in the KEDB
- **Change Management:** Implementation plans and rollback procedures are stored as KB articles

---

## Part 2: ServiceNow Knowledge Base Architecture

### 2.1 Core Tables

| Table | Label | Purpose |
|-------|-------|---------|
| `kb_knowledge_base` | Knowledge Base | Top-level container; controls access, ownership, and settings |
| `kb_category` | Knowledge Category | Folders/sections within a Knowledge Base for organizing articles |
| `kb_knowledge` | Knowledge Article | The individual article with content, state, and metadata |
| `kb_feedback` | Article Feedback | User ratings and comments on articles |
| `kb_use` | Article Usage | Tracks views and usage statistics |

### 2.2 Article States

```
                          Approval
    +-------+   Submit   +--------+   Approve   +-----------+
    | Draft | ---------> | Review | ----------> | Published |
    +-------+            +--------+             +-----------+
        ^                    |                        |
        |               Reject                   Retire
        |                    |                        |
        |                    v                        v
        +<--- Rework ---+--------+             +---------+
                                               | Retired |
                                               +---------+
```

- **Draft (1):** Article is being authored; not visible to end users
- **Review (2):** Article submitted for approval; pending SME review
- **Published (3):** Article is live and visible based on access controls
- **Retired (4):** Article removed from active search results; retained for audit

### 2.3 Article Versioning

ServiceNow supports article versioning. When an author edits a published article:
1. A new version is created in Draft state
2. The published version remains active
3. When the new version is approved and published, it replaces the old version
4. Version history is maintained for audit

### 2.4 Article Templates

Templates provide a consistent structure for articles. Common templates include:
- **How-To:** Step-by-step instructions
- **FAQ:** Question and answer format
- **Known Error:** Symptom, cause, workaround, permanent fix
- **Runbook:** Pre-checks, procedure, post-checks, rollback

---

## Part 3: Create Knowledge Base Structure

### Step 3.1: Create the Knowledge Base

1. Navigate to **Knowledge > Administration > Knowledge Bases**
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |-------|-------|
   | Title | UPI Operations Knowledge Base |
   | Owner | Ravi Kumar |
   | Description | Comprehensive knowledge repository for UPI payment platform operations, troubleshooting, runbooks, and standard operating procedures. Maintained by the Platform Engineering team. |
   | Active | true (checked) |

4. In the **Managers** field, add: **Platform Engineering** group
5. Click **Submit**
6. Note the Knowledge Base `sys_id` for later use

> **Verification:** Navigate to **Knowledge > Homepage**. You should see "UPI Operations Knowledge Base" listed.

### Step 3.2: Create Knowledge Categories

Open the newly created Knowledge Base record, then scroll down to the **Categories** related list.

Create the following categories by clicking **New** in the Categories related list:

| # | Category Name | Parent Category | Description |
|---|--------------|----------------|-------------|
| 1 | UPI Error Codes & Resolution | (none - top level) | Reference documentation for all UPI error codes with diagnostic steps and resolution procedures |
| 2 | Runbooks & Standard Operating Procedures | (none - top level) | Step-by-step operational procedures for routine and emergency operations |
| 3 | Architecture & Design Documents | (none - top level) | System architecture diagrams, design decisions, and integration specifications |
| 4 | Onboarding & Training | (none - top level) | Guides for new team members joining the UPI platform team |
| 5 | Known Issues & Workarounds | (none - top level) | Known Error Database (KEDB) - documented known issues with workarounds and fix status |
| 6 | Change Implementation Guides | (none - top level) | Standard deployment procedures, rollback plans, and change execution guides |
| 7 | Monitoring & Alerting | (none - top level) | Grafana dashboard guides, Prometheus query references, and alert response procedures |

For each category:
1. Click **New** in the Categories related list
2. Set the **Label** to the category name from the table above
3. Set the **Knowledge Base** to "UPI Operations Knowledge Base" (should auto-populate)
4. Add the **Description**
5. Click **Submit**

> **Verification:** Open the Knowledge Base record and confirm all 7 categories appear in the Categories related list.

---

## Part 4: Create Knowledge Articles

We will now create 10 detailed knowledge articles with realistic UPI content. Each article should be created with the full body content provided below.

### Article 1: UPI Error Code Reference Guide

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | UPI Error Codes & Resolution |
   | Short description | UPI Error Code Reference Guide |
   | Author | Amit Verma |

3. In the **Article body**, enter the following content:

```html
<h2>Overview</h2>
<p>This document provides a comprehensive reference for UPI error codes encountered in the NPCI UPI payment platform. Each error code includes a description, common causes, diagnostic steps, and resolution procedures. This guide should be the first reference when investigating transaction failures.</p>

<h2>Error Code Reference Table</h2>
<table border="1" cellpadding="8" cellspacing="0">
<thead>
<tr>
  <th>Error Code</th>
  <th>Description</th>
  <th>Severity</th>
  <th>Common Cause</th>
  <th>Resolution</th>
</tr>
</thead>
<tbody>
<tr>
  <td><strong>U01</strong></td>
  <td>Transaction Timeout</td>
  <td>High</td>
  <td>Backend service latency exceeding 30-second threshold; connection pool exhaustion; database query timeout</td>
  <td>1. Check service health: <code>curl -s http://upi-txn-service:8080/health</code><br/>
      2. Check connection pool: query Prometheus for <code>hikari_connections_active</code><br/>
      3. If connection pool exhausted, restart transaction service (see Runbook: UPI Transaction Service Restart)<br/>
      4. If database slow, check PostgreSQL slow query log</td>
</tr>
<tr>
  <td><strong>U09</strong></td>
  <td>Beneficiary Bank Offline</td>
  <td>Medium</td>
  <td>Downstream bank's UPI gateway is unreachable or returning 5xx errors</td>
  <td>1. Verify bank connectivity: <code>curl -s http://upi-gateway:8080/api/v1/banks/{bank_code}/status</code><br/>
      2. Check NPCI switch dashboard for bank availability<br/>
      3. If bank confirmed offline, enable circuit breaker for affected bank<br/>
      4. Notify affected PSPs via broadcast alert<br/>
      5. Monitor for bank recovery; circuit breaker will auto-close after 3 successful health checks</td>
</tr>
<tr>
  <td><strong>U16</strong></td>
  <td>Risk Threshold Exceeded</td>
  <td>Medium</td>
  <td>Transaction flagged by fraud detection engine; velocity check failure; amount exceeds risk threshold for user profile</td>
  <td>1. Review transaction in fraud dashboard: Grafana > UPI Fraud Monitoring<br/>
      2. Check risk score: <code>GET /api/v1/risk/score/{txn_id}</code><br/>
      3. If false positive, whitelist pattern in risk engine configuration<br/>
      4. If legitimate block, no action required - system working as intended<br/>
      5. Escalate to Risk & Compliance team if pattern suggests new fraud vector</td>
</tr>
<tr>
  <td><strong>U28</strong></td>
  <td>PSP Not Registered</td>
  <td>Low</td>
  <td>Payment Service Provider identifier not found in NPCI registry; expired PSP certificate; PSP onboarding incomplete</td>
  <td>1. Verify PSP registration: <code>SELECT * FROM psp_registry WHERE psp_code = '{psp_code}'</code><br/>
      2. Check certificate expiry: <code>GET /api/v1/psp/{psp_code}/certificate</code><br/>
      3. If PSP not found, escalate to PSP Onboarding team<br/>
      4. If certificate expired, notify PSP to renew and re-register</td>
</tr>
<tr>
  <td><strong>U30</strong></td>
  <td>Debit Failed</td>
  <td>High</td>
  <td>Insufficient funds in remitter account; account frozen; bank-side debit processing failure</td>
  <td>1. This is typically a customer-side issue (insufficient funds)<br/>
      2. If bulk failures from a single bank, check bank connectivity (similar to U09)<br/>
      3. If systematic failures across banks, check UPI debit service health<br/>
      4. Monitor <code>upi_debit_failure_rate</code> metric in Prometheus<br/>
      5. Escalate if failure rate exceeds 5% for more than 10 minutes</td>
</tr>
<tr>
  <td><strong>U48</strong></td>
  <td>Transaction Not Found</td>
  <td>Medium</td>
  <td>Transaction ID not found in the transaction ledger; possible replication lag between primary and replica databases; transaction expired from cache</td>
  <td>1. Check primary database directly: <code>SELECT * FROM txn_ledger WHERE txn_id = '{txn_id}'</code><br/>
      2. Check replication lag: <code>SELECT pg_last_wal_receive_lsn() - pg_last_wal_replay_lsn()</code><br/>
      3. If replication lag > 10 seconds, investigate replica health<br/>
      4. If transaction genuinely missing, check transaction service logs for the original request</td>
</tr>
<tr>
  <td><strong>U66</strong></td>
  <td>Device Fingerprint Mismatch</td>
  <td>High</td>
  <td>Device binding verification failed; user changed device without re-registration; potential account takeover attempt</td>
  <td>1. Verify in device registry: <code>GET /api/v1/device/{vpa}/bindings</code><br/>
      2. If user legitimately changed device, guide through re-registration flow<br/>
      3. If suspicious (multiple VPAs from same new device), escalate to Security team<br/>
      4. Log incident in fraud monitoring system</td>
</tr>
<tr>
  <td><strong>U78</strong></td>
  <td>Remitter PSP Not Registered</td>
  <td>Low</td>
  <td>Similar to U28 but specific to the remitter (sending) side PSP</td>
  <td>1. Follow same procedure as U28<br/>
      2. Additionally verify remitter-side VPA format is valid<br/>
      3. Check if PSP was recently deregistered or suspended</td>
</tr>
</tbody>
</table>

<h2>Escalation Guidelines</h2>
<p>If an error code is causing failure rates above the following thresholds, escalate immediately:</p>
<ul>
  <li><strong>P1 (Critical):</strong> Any single error code causing > 10% overall transaction failure rate</li>
  <li><strong>P2 (High):</strong> Any single error code causing > 5% failure rate for more than 15 minutes</li>
  <li><strong>P3 (Moderate):</strong> Any new/unknown error code appearing in production</li>
</ul>

<h2>Related Resources</h2>
<ul>
  <li>Runbook: UPI Transaction Service Restart Procedure</li>
  <li>Troubleshooting: High Transaction Failure Rate</li>
  <li>Grafana Dashboard: UPI Transaction Monitoring</li>
</ul>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

### Article 2: Runbook - UPI Transaction Service Restart Procedure

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | Runbooks & Standard Operating Procedures |
   | Short description | Runbook: UPI Transaction Service Restart Procedure |
   | Author | Ravi Kumar |

3. In the **Article body**, enter:

```html
<h2>Document Control</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><td><strong>Runbook ID</strong></td><td>RB-UPI-001</td></tr>
<tr><td><strong>Version</strong></td><td>2.1</td></tr>
<tr><td><strong>Last Updated</strong></td><td>2024-01-10</td></tr>
<tr><td><strong>Author</strong></td><td>Ravi Kumar</td></tr>
<tr><td><strong>Approved By</strong></td><td>Platform Engineering Lead</td></tr>
<tr><td><strong>Classification</strong></td><td>Internal - Operations</td></tr>
</table>

<h2>Purpose</h2>
<p>This runbook provides the step-by-step procedure for performing a controlled restart of the UPI Transaction Service. This procedure should be followed when the service exhibits connection pool exhaustion, memory leaks, or elevated error rates that cannot be resolved by other means.</p>

<h2>When to Use This Runbook</h2>
<ul>
  <li>Connection pool utilization exceeds 90% for more than 10 minutes</li>
  <li>Heap memory usage exceeds 85% and is not recovering after GC</li>
  <li>Transaction timeout (U01) rate exceeds 5% for more than 15 minutes</li>
  <li>Service health endpoint returning degraded status</li>
</ul>

<h2>Prerequisites</h2>
<ol>
  <li>SSH access to the UPI application servers (upi-app-01 through upi-app-04)</li>
  <li>Access to Grafana dashboard: "UPI Transaction Monitoring"</li>
  <li>Access to Kubernetes cluster (if running in K8s)</li>
  <li>Notification sent to NOC channel: #upi-noc-alerts</li>
</ol>

<h2>Pre-Restart Checks</h2>
<ol>
  <li><strong>Verify current transaction volume:</strong>
    <pre>curl -s http://upi-txn-service:8080/metrics | grep upi_transactions_per_second</pre>
    <p>Record the current TPS. If TPS > 5000, coordinate with NOC before proceeding.</p>
  </li>
  <li><strong>Check active in-flight transactions:</strong>
    <pre>curl -s http://upi-txn-service:8080/api/v1/admin/inflight-count</pre>
    <p>Wait until in-flight count drops below 100 before proceeding.</p>
  </li>
  <li><strong>Verify other instances are healthy:</strong>
    <pre>for i in 1 2 3 4; do
  echo "upi-app-0$i: $(curl -s http://upi-app-0$i:8080/health | jq -r '.status')"
done</pre>
    <p>At least 3 of 4 instances must be healthy before restarting any one instance.</p>
  </li>
  <li><strong>Notify the team:</strong>
    <p>Post in #upi-noc-alerts: "MAINTENANCE: Restarting UPI Transaction Service on [server]. Expected duration: 5 minutes. Current TPS: [value]."</p>
  </li>
</ol>

<h2>Restart Procedure</h2>

<h3>Option A: Kubernetes Deployment (Preferred)</h3>
<ol>
  <li><strong>Initiate rolling restart:</strong>
    <pre>kubectl rollout restart deployment/upi-txn-service -n upi-production</pre>
  </li>
  <li><strong>Monitor rollout status:</strong>
    <pre>kubectl rollout status deployment/upi-txn-service -n upi-production --timeout=300s</pre>
  </li>
  <li><strong>Verify pod health:</strong>
    <pre>kubectl get pods -n upi-production -l app=upi-txn-service -o wide</pre>
    <p>All pods should show Running status with 1/1 READY.</p>
  </li>
</ol>

<h3>Option B: VM-Based Deployment</h3>
<ol>
  <li><strong>Remove instance from load balancer:</strong>
    <pre>curl -X POST http://upi-lb:8080/api/v1/backend/upi-app-01/disable</pre>
  </li>
  <li><strong>Wait for connections to drain (60 seconds):</strong>
    <pre>sleep 60 && curl -s http://upi-app-01:8080/api/v1/admin/inflight-count</pre>
    <p>Confirm in-flight count is 0.</p>
  </li>
  <li><strong>Restart the service:</strong>
    <pre>sudo systemctl restart upi-transaction-service</pre>
  </li>
  <li><strong>Wait for service to become healthy (typically 30-45 seconds):</strong>
    <pre>until curl -sf http://upi-app-01:8080/health; do sleep 5; done</pre>
  </li>
  <li><strong>Re-enable in load balancer:</strong>
    <pre>curl -X POST http://upi-lb:8080/api/v1/backend/upi-app-01/enable</pre>
  </li>
</ol>

<h2>Post-Restart Validation</h2>
<ol>
  <li><strong>Verify service health:</strong>
    <pre>curl -s http://upi-txn-service:8080/health | jq .</pre>
    <p>Expected: <code>{"status": "UP", "components": {"db": "UP", "redis": "UP", "kafka": "UP"}}</code></p>
  </li>
  <li><strong>Check connection pool:</strong>
    <pre>curl -s http://upi-txn-service:8080/metrics | grep hikari_connections</pre>
    <p>Active connections should be < 20% of max pool size.</p>
  </li>
  <li><strong>Monitor error rate in Grafana:</strong>
    <p>Open Grafana > UPI Transaction Monitoring > Error Rate panel. Confirm error rate returns to baseline (< 0.5%) within 5 minutes.</p>
  </li>
  <li><strong>Verify TPS recovery:</strong>
    <p>Transaction throughput should return to pre-restart levels within 2 minutes.</p>
  </li>
</ol>

<h2>Rollback Procedure</h2>
<p>If the service does not recover after restart:</p>
<ol>
  <li>Check application logs: <code>kubectl logs -f deployment/upi-txn-service -n upi-production --tail=200</code></li>
  <li>If a recent deployment caused the issue, rollback: <code>kubectl rollout undo deployment/upi-txn-service -n upi-production</code></li>
  <li>If infrastructure issue, engage Platform Engineering on-call</li>
</ol>

<h2>Escalation</h2>
<ul>
  <li>If service does not recover within 10 minutes: Escalate to <strong>Platform Engineering On-Call</strong></li>
  <li>If transaction failure rate exceeds 20%: Declare <strong>P1 Major Incident</strong></li>
  <li>If all 4 instances are unhealthy: Invoke <strong>Disaster Recovery Plan</strong></li>
</ul>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

### Article 3: Runbook - UPI Database Failover Procedure

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | Runbooks & Standard Operating Procedures |
   | Short description | Runbook: UPI Database Failover Procedure |
   | Author | Ravi Kumar |

3. In the **Article body**, enter:

```html
<h2>Document Control</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><td><strong>Runbook ID</strong></td><td>RB-UPI-002</td></tr>
<tr><td><strong>Version</strong></td><td>1.4</td></tr>
<tr><td><strong>Last Updated</strong></td><td>2024-01-08</td></tr>
<tr><td><strong>Author</strong></td><td>Ravi Kumar</td></tr>
<tr><td><strong>Classification</strong></td><td>Internal - Operations - CRITICAL</td></tr>
</table>

<h2>Purpose</h2>
<p>This runbook describes the procedure for performing a PostgreSQL primary-to-replica failover for the UPI transaction database. This is a high-risk operation that should only be performed when the primary database is unresponsive or exhibiting critical performance degradation.</p>

<h2>Architecture Overview</h2>
<pre>
  +-------------------+          Streaming Replication          +-------------------+
  |   upi-db-primary  |  -------------------------------------> |  upi-db-replica-1 |
  |  (PostgreSQL 15)  |  -------------------------------------> |  (PostgreSQL 15)  |
  |  192.168.1.10:5432 |                                       |  192.168.1.11:5432 |
  +-------------------+                                        +-------------------+
          |                                                            |
          |            Streaming Replication             +-------------------+
          +-------------------------------------------> |  upi-db-replica-2 |
                                                        |  (PostgreSQL 15)  |
                                                        |  192.168.1.12:5432 |
                                                        +-------------------+

  Connection String (PgBouncer):
  Host: upi-pgbouncer.internal:6432
  Database: upi_transactions
</pre>

<h2>When to Invoke This Runbook</h2>
<ul>
  <li>Primary database is unreachable for more than 60 seconds</li>
  <li>Primary database replication lag exceeds 30 seconds</li>
  <li>Primary database disk usage exceeds 95%</li>
  <li>Directed by Platform Engineering Lead during a planned maintenance</li>
</ul>

<h2>CRITICAL: Before You Begin</h2>
<p style="color: red; font-weight: bold;">WARNING: Database failover will cause a brief service interruption (typically 15-30 seconds). All in-flight transactions during the switchover will fail. Coordinate with NOC and obtain explicit approval from Platform Engineering Lead before proceeding.</p>

<h2>Pre-Failover Checks</h2>
<ol>
  <li><strong>Confirm primary is truly unhealthy:</strong>
    <pre>pg_isready -h upi-db-primary -p 5432 -U upi_app
psql -h upi-db-primary -U upi_admin -c "SELECT 1;"</pre>
  </li>
  <li><strong>Check replica health and replication lag:</strong>
    <pre>psql -h upi-db-replica-1 -U upi_admin -c "SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn(),
  EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS lag_seconds;"</pre>
    <p>Lag should be < 5 seconds for a clean failover.</p>
  </li>
  <li><strong>Notify stakeholders:</strong>
    <p>Post in #upi-noc-alerts and #upi-platform-eng: "DATABASE FAILOVER: Initiating failover from upi-db-primary to upi-db-replica-1. Expected service interruption: 15-30 seconds."</p>
  </li>
</ol>

<h2>Failover Procedure</h2>
<ol>
  <li><strong>Promote the replica to primary:</strong>
    <pre>sudo -u postgres pg_ctlcluster 15 main promote -D /var/lib/postgresql/15/main</pre>
    <p>Or using pg_ctl:</p>
    <pre>sudo -u postgres pg_ctl promote -D /var/lib/postgresql/15/main</pre>
  </li>
  <li><strong>Verify promotion was successful:</strong>
    <pre>psql -h upi-db-replica-1 -U upi_admin -c "SELECT pg_is_in_recovery();"</pre>
    <p>Expected result: <code>f</code> (false, meaning it is now the primary).</p>
  </li>
  <li><strong>Update PgBouncer configuration:</strong>
    <pre># Edit /etc/pgbouncer/pgbouncer.ini
# Change: upi_transactions = host=upi-db-primary port=5432 dbname=upi_transactions
# To:     upi_transactions = host=upi-db-replica-1 port=5432 dbname=upi_transactions

sudo systemctl reload pgbouncer</pre>
  </li>
  <li><strong>Reconfigure remaining replica to follow new primary:</strong>
    <pre># On upi-db-replica-2, update recovery.conf or postgresql.auto.conf:
# primary_conninfo = 'host=upi-db-replica-1 port=5432 user=replicator'
sudo systemctl restart postgresql@15-main</pre>
  </li>
</ol>

<h2>Post-Failover Validation</h2>
<ol>
  <li><strong>Verify application connectivity:</strong>
    <pre>psql -h upi-pgbouncer.internal -p 6432 -U upi_app -d upi_transactions -c "SELECT count(*) FROM transactions WHERE created_at > now() - interval '5 minutes';"</pre>
  </li>
  <li><strong>Check application error rate:</strong>
    <p>Grafana > UPI Transaction Monitoring > Error Rate. Should return to baseline within 2 minutes.</p>
  </li>
  <li><strong>Verify replication from new primary:</strong>
    <pre>psql -h upi-db-replica-1 -U upi_admin -c "SELECT client_addr, state, sent_lsn, replay_lsn FROM pg_stat_replication;"</pre>
  </li>
</ol>

<h2>Post-Incident: Rebuild Old Primary as Replica</h2>
<p>After the incident is resolved, the old primary should be rebuilt as a replica:</p>
<ol>
  <li>Investigate and fix the root cause on the old primary</li>
  <li>Use <code>pg_basebackup</code> to rebuild it as a replica of the new primary</li>
  <li>This task should be tracked as a follow-up Problem record</li>
</ol>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

### Article 4: Troubleshooting - High Transaction Failure Rate

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | Known Issues & Workarounds |
   | Short description | Troubleshooting: High Transaction Failure Rate |
   | Author | Priya Sharma |

3. In the **Article body**, enter:

```html
<h2>Overview</h2>
<p>This troubleshooting guide helps NOC engineers diagnose and resolve elevated transaction failure rates on the UPI platform. A "high" failure rate is defined as any rate above 2% sustained for more than 5 minutes.</p>

<h2>Symptom Identification</h2>
<p>You may encounter this situation through:</p>
<ul>
  <li><strong>Grafana Alert:</strong> "UPI Transaction Failure Rate High" (triggers at > 2% for 5 min)</li>
  <li><strong>Prometheus Alert:</strong> <code>UPITransactionFailureRateHigh</code> firing in Alertmanager</li>
  <li><strong>NOC Dashboard:</strong> Red indicator on the UPI Health Overview panel</li>
  <li><strong>Customer reports:</strong> Multiple complaints about failed payments</li>
</ul>

<h2>Step 1: Assess the Situation</h2>
<ol>
  <li><strong>Open Grafana Dashboard:</strong> Navigate to UPI Transaction Monitoring
    <ul>
      <li>Check the "Overall Failure Rate" panel - what is the current rate?</li>
      <li>Check the "Failure Rate by Error Code" panel - which error codes are dominant?</li>
      <li>Check the "Failure Rate by Bank" panel - is it isolated to specific banks?</li>
    </ul>
  </li>
  <li><strong>Prometheus Query - Overall failure rate:</strong>
    <pre>sum(rate(upi_transactions_total{status="failed"}[5m])) / sum(rate(upi_transactions_total[5m])) * 100</pre>
  </li>
  <li><strong>Prometheus Query - Failure rate by error code:</strong>
    <pre>topk(5, sum by (error_code) (rate(upi_transactions_total{status="failed"}[5m])))</pre>
  </li>
</ol>

<h2>Step 2: Identify the Root Cause</h2>

<h3>Scenario A: Dominant error code is U01 (Transaction Timeout)</h3>
<ul>
  <li>Check service response times: <code>histogram_quantile(0.99, rate(upi_request_duration_seconds_bucket[5m]))</code></li>
  <li>Check connection pool: <code>hikari_connections_active / hikari_connections_max</code></li>
  <li>If connection pool > 90%, follow Runbook: UPI Transaction Service Restart</li>
  <li>If database is slow, check PostgreSQL: <code>SELECT * FROM pg_stat_activity WHERE state = 'active' AND duration > interval '10 seconds';</code></li>
</ul>

<h3>Scenario B: Dominant error code is U09 (Beneficiary Bank Offline)</h3>
<ul>
  <li>Check which banks are affected: <code>sum by (bank_code) (rate(upi_transactions_total{status="failed", error_code="U09"}[5m]))</code></li>
  <li>Verify bank connectivity from UPI gateway</li>
  <li>Check NPCI bulletin board for scheduled bank maintenance</li>
  <li>If isolated to 1-2 banks: Monitor and wait for bank recovery</li>
  <li>If widespread: Possible NPCI switch issue - escalate to NPCI Operations</li>
</ul>

<h3>Scenario C: Dominant error code is U30 (Debit Failed)</h3>
<ul>
  <li>Check if isolated to specific remitter banks</li>
  <li>If widespread, check UPI debit processing service health</li>
  <li>Verify Kafka consumer lag: <code>kafka_consumer_group_lag{group="upi-debit-processor"}</code></li>
</ul>

<h3>Scenario D: Multiple error codes elevated simultaneously</h3>
<ul>
  <li>This usually indicates an infrastructure-level issue</li>
  <li>Check Kubernetes cluster health: <code>kubectl get nodes</code></li>
  <li>Check network connectivity between services</li>
  <li>Check shared dependencies (Redis, Kafka, PostgreSQL)</li>
</ul>

<h2>Step 3: Resolution Actions</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Root Cause</th><th>Action</th><th>Runbook</th></tr>
<tr><td>Connection pool exhaustion</td><td>Restart transaction service</td><td>RB-UPI-001</td></tr>
<tr><td>Database performance</td><td>Kill long-running queries; consider failover</td><td>RB-UPI-002</td></tr>
<tr><td>Single bank offline</td><td>Enable circuit breaker; monitor</td><td>N/A - standard NOC procedure</td></tr>
<tr><td>Kafka consumer lag</td><td>Scale consumer group; restart consumers</td><td>RB-UPI-005</td></tr>
<tr><td>Kubernetes node failure</td><td>Cordon node; pods reschedule automatically</td><td>RB-INFRA-003</td></tr>
</table>

<h2>Step 4: Escalation Criteria</h2>
<ul>
  <li>If failure rate > 10% for > 5 minutes: <strong>Declare P1 Major Incident</strong></li>
  <li>If failure rate > 5% for > 15 minutes and root cause not identified: <strong>Escalate to Platform Engineering</strong></li>
  <li>If NPCI switch suspected: <strong>Escalate to NPCI Operations via hotline</strong></li>
</ul>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

### Article 5: Architecture - UPI Payment Processing Flow

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | Architecture & Design Documents |
   | Short description | Architecture: UPI Payment Processing Flow |
   | Author | Ravi Kumar |

3. In the **Article body**, enter:

```html
<h2>Overview</h2>
<p>This document describes the end-to-end flow of a UPI payment transaction through the NPCI platform, from initiation on the payer's device to final settlement. Understanding this flow is essential for troubleshooting, capacity planning, and onboarding new team members.</p>

<h2>End-to-End Transaction Flow</h2>
<pre>
  +----------+     +----------+     +-------------+     +----------+     +----------+
  |  Payer   |     |  Payer   |     |    NPCI     |     |  Payee   |     |  Payee   |
  |  Mobile  |---->|  PSP     |---->|    UPI      |---->|  PSP     |---->|  Bank    |
  |  App     |     |  Server  |     |   Switch    |     |  Server  |     |  Server  |
  +----------+     +----------+     +-------------+     +----------+     +----------+
       |                |                  |                  |                |
       | 1. Initiate    | 2. Validate      | 3. Route &       | 7. Credit      | 8. Credit
       |    Payment     |    & Forward     |    Process       |    Request     |    Account
       |                |                  |                  |                |
       |                |                  | 4. Debit Request |                |
       |                |                  |----------------->|                |
       |                |                  |    to Payer Bank |                |
       |                |                  |                  |                |
       |                |                  | 5. Debit         |                |
       |                |                  |    Confirmation  |                |
       |                |                  |<-----------------|                |
       |                |                  |                  |                |
       |                |                  | 6. Credit        |                |
       |                |                  |    Instruction   |                |
       |                |                  |----------------->|                |
       |                |                  |                  |                |
       |                | 9. Response      |                  |                |
       | 10. Payment    |<-----------------|                  |                |
       |     Status     |                  |                  |                |
       |<---------------|                  |                  |                |
</pre>

<h2>Component Descriptions</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Component</th><th>Description</th><th>Technology</th><th>ServiceNow CI</th></tr>
<tr>
  <td>UPI Gateway Service</td>
  <td>Entry point for all PSP requests; handles authentication, rate limiting, and request validation</td>
  <td>Java 17, Spring Boot 3.x</td>
  <td>upi-gateway-service</td>
</tr>
<tr>
  <td>UPI Transaction Service</td>
  <td>Core transaction processing engine; orchestrates debit/credit flows</td>
  <td>Java 17, Spring Boot 3.x</td>
  <td>upi-txn-service</td>
</tr>
<tr>
  <td>UPI Risk Engine</td>
  <td>Real-time fraud detection and risk scoring for all transactions</td>
  <td>Python 3.11, FastAPI</td>
  <td>upi-risk-engine</td>
</tr>
<tr>
  <td>UPI Settlement Service</td>
  <td>Batch settlement processing; runs every 30 minutes</td>
  <td>Java 17, Spring Batch</td>
  <td>upi-settlement-service</td>
</tr>
<tr>
  <td>PostgreSQL Cluster</td>
  <td>Primary transaction database; stores transaction ledger</td>
  <td>PostgreSQL 15, Patroni</td>
  <td>upi-db-primary</td>
</tr>
<tr>
  <td>Redis Cluster</td>
  <td>Session cache, rate limiting counters, and transaction deduplication</td>
  <td>Redis 7.x Cluster</td>
  <td>upi-redis-cluster</td>
</tr>
<tr>
  <td>Kafka Cluster</td>
  <td>Event streaming for async processing, audit logging, and inter-service communication</td>
  <td>Apache Kafka 3.x</td>
  <td>upi-kafka-cluster</td>
</tr>
</table>

<h2>Key Integration Points</h2>
<ol>
  <li><strong>PSP to NPCI Gateway:</strong> REST API over mutual TLS (mTLS); each PSP has unique client certificates</li>
  <li><strong>NPCI to Bank:</strong> ISO 8583 message format over dedicated leased lines</li>
  <li><strong>Internal Services:</strong> gRPC for synchronous calls; Kafka for asynchronous events</li>
  <li><strong>Monitoring:</strong> All services expose Prometheus metrics at <code>/metrics</code> endpoint</li>
</ol>

<h2>Transaction Lifecycle States</h2>
<pre>
  INITIATED --> VALIDATED --> DEBIT_PENDING --> DEBITED --> CREDIT_PENDING --> CREDITED --> SETTLED
       |            |              |                            |
       v            v              v                            v
    REJECTED    VALIDATION     DEBIT_FAILED              CREDIT_FAILED
                _FAILED                                  (Refund Initiated)
</pre>

<h2>Performance Characteristics</h2>
<ul>
  <li><strong>Target TPS:</strong> 10,000 transactions per second at peak</li>
  <li><strong>P99 Latency:</strong> < 2 seconds end-to-end</li>
  <li><strong>Availability Target:</strong> 99.95% (measured monthly)</li>
  <li><strong>Settlement Cycles:</strong> Every 30 minutes, 24x7</li>
</ul>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

### Article 6: Onboarding - New Team Member Guide for UPI Platform

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | Onboarding & Training |
   | Short description | Onboarding: New Team Member Guide for UPI Platform |
   | Author | Meera Joshi |

3. In the **Article body**, enter:

```html
<h2>Welcome to the UPI Platform Team</h2>
<p>Welcome to NPCI's UPI Platform team! This guide will help you get set up with the tools, access, and knowledge you need to be productive. Please work through each section in order during your first week.</p>

<h2>Day 1: Access Requests</h2>
<p>Submit the following access requests through ServiceNow (Self-Service > Service Catalog > Access Requests):</p>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>System</th><th>Access Level</th><th>Approver</th><th>Expected SLA</th></tr>
<tr><td>ServiceNow ITSM</td><td>ITIL User role</td><td>Service Desk Manager</td><td>4 hours</td></tr>
<tr><td>Grafana</td><td>Viewer (Editor after 30 days)</td><td>Platform Engineering Lead</td><td>8 hours</td></tr>
<tr><td>Prometheus</td><td>Read-only</td><td>Platform Engineering Lead</td><td>8 hours</td></tr>
<tr><td>Kubernetes Cluster</td><td>Namespace: upi-production (read-only)</td><td>Platform Engineering Lead</td><td>24 hours</td></tr>
<tr><td>GitLab</td><td>Developer role on upi-* repositories</td><td>Tech Lead</td><td>8 hours</td></tr>
<tr><td>PagerDuty</td><td>Responder (added to on-call after 60 days)</td><td>NOC Manager</td><td>4 hours</td></tr>
<tr><td>Confluence</td><td>UPI Platform space</td><td>Auto-approved</td><td>Immediate</td></tr>
<tr><td>Slack Channels</td><td>#upi-platform-eng, #upi-noc-alerts, #upi-incidents</td><td>Auto-approved</td><td>Immediate</td></tr>
</table>

<h2>Day 1-2: Tool Setup</h2>
<ol>
  <li><strong>kubectl configuration:</strong>
    <pre>aws eks update-kubeconfig --region ap-south-1 --name upi-production-cluster
kubectl config set-context --current --namespace=upi-production
kubectl get pods  # Verify access</pre>
  </li>
  <li><strong>Grafana bookmarks:</strong> Save these dashboards:
    <ul>
      <li>UPI Transaction Monitoring: <code>https://grafana.internal/d/upi-txn-monitor</code></li>
      <li>UPI Infrastructure Health: <code>https://grafana.internal/d/upi-infra-health</code></li>
      <li>UPI Error Rate Analysis: <code>https://grafana.internal/d/upi-error-analysis</code></li>
    </ul>
  </li>
  <li><strong>ServiceNow setup:</strong> Log in to your PDI and familiarize yourself with:
    <ul>
      <li>Incident Management module</li>
      <li>Knowledge Base: "UPI Operations Knowledge Base"</li>
      <li>CMDB: Search for "UPI" to see all Configuration Items</li>
    </ul>
  </li>
</ol>

<h2>Day 2-3: Required Reading</h2>
<p>Read these KB articles in order:</p>
<ol>
  <li>Architecture: UPI Payment Processing Flow</li>
  <li>UPI Error Code Reference Guide</li>
  <li>Runbook: UPI Transaction Service Restart Procedure</li>
  <li>Troubleshooting: High Transaction Failure Rate</li>
</ol>

<h2>Day 3-5: Key Contacts</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Role</th><th>Name</th><th>Contact</th><th>When to Reach Out</th></tr>
<tr><td>Platform Engineering Lead</td><td>Ravi Kumar</td><td>Slack: @ravi.kumar</td><td>Architecture questions, escalations</td></tr>
<tr><td>Senior Platform Engineer</td><td>Amit Verma</td><td>Slack: @amit.verma</td><td>Technical questions, code reviews</td></tr>
<tr><td>NOC Lead</td><td>Priya Sharma</td><td>Slack: @priya.sharma</td><td>Monitoring, alerting, incident triage</td></tr>
<tr><td>Service Desk Lead</td><td>Meera Joshi</td><td>Slack: @meera.joshi</td><td>ServiceNow workflows, user issues</td></tr>
</table>

<h2>Week 2: Shadowing Schedule</h2>
<ul>
  <li><strong>Monday-Tuesday:</strong> Shadow NOC engineer during morning shift (observe incident triage)</li>
  <li><strong>Wednesday:</strong> Shadow Platform Engineer during a change deployment</li>
  <li><strong>Thursday:</strong> Participate in weekly Problem Review meeting</li>
  <li><strong>Friday:</strong> Shadow Service Desk for customer-facing ticket handling</li>
</ul>

<h2>30-Day Milestone</h2>
<p>By the end of your first month, you should be able to:</p>
<ul>
  <li>Navigate all Grafana dashboards and interpret key metrics</li>
  <li>Triage P3/P4 incidents independently</li>
  <li>Execute runbooks for standard procedures (service restart, log collection)</li>
  <li>Create and submit KB articles for review</li>
</ul>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

### Article 7: Known Error - Memory Leak in UPI Transaction Service v2.3

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | Known Issues & Workarounds |
   | Short description | Known Error: Memory Leak in UPI Transaction Service v2.3 |
   | Author | Amit Verma |

3. In the **Article body**, enter:

```html
<h2>Known Error Record</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><td><strong>KEDB ID</strong></td><td>KE-UPI-007</td></tr>
<tr><td><strong>Related Problem</strong></td><td>PRB0042156 - Recurring memory exhaustion on UPI Transaction Service</td></tr>
<tr><td><strong>Affected CI</strong></td><td>upi-txn-service (version 2.3.x)</td></tr>
<tr><td><strong>Date Identified</strong></td><td>2024-01-05</td></tr>
<tr><td><strong>Status</strong></td><td>Workaround Available | Permanent Fix in Development</td></tr>
<tr><td><strong>Fix Target Version</strong></td><td>v2.4.0 (ETA: 2024-02-15)</td></tr>
</table>

<h2>Symptoms</h2>
<ul>
  <li>JVM heap memory usage increases steadily over 7-10 days from baseline 45% to >85%</li>
  <li>Garbage collection pause times increase from ~50ms to >500ms</li>
  <li>Transaction latency (P99) degrades from 800ms to >3000ms after ~10 days of uptime</li>
  <li>Eventually, OutOfMemoryError crashes the service</li>
  <li>Prometheus metric: <code>jvm_memory_used_bytes{area="heap"}</code> shows linear upward trend</li>
</ul>

<h2>Root Cause Analysis</h2>
<p>The memory leak was traced to the transaction correlation cache in <code>TransactionCorrelationService.java</code>. When a transaction completes with certain error codes (U48, U66), the correlation entry is not removed from the in-memory HashMap. Over time, these orphaned entries accumulate and consume heap memory.</p>
<p>The bug was introduced in v2.3.0 when the error handling flow was refactored (commit: <code>a3f7b2c</code>). The <code>finally</code> block that previously cleaned up correlation entries was inadvertently removed during the refactor.</p>

<h2>Impact</h2>
<ul>
  <li><strong>Frequency:</strong> Occurs on every instance of upi-txn-service v2.3.x</li>
  <li><strong>Time to Impact:</strong> Service degradation begins ~7 days after restart; crash occurs ~12-14 days</li>
  <li><strong>Business Impact:</strong> When service crashes, affected instance stops processing transactions until auto-restart completes (typically 45 seconds)</li>
  <li><strong>Incidents Caused:</strong> INC0078234, INC0079001, INC0079456</li>
</ul>

<h2>Workaround</h2>
<p>Perform a scheduled rolling restart of all UPI Transaction Service instances every 5 days. This prevents memory from reaching critical levels.</p>
<ol>
  <li>Create a recurring Change Request (Standard Change, template: CHG-STD-014)</li>
  <li>Schedule restarts during low-traffic window (02:00-04:00 IST)</li>
  <li>Follow Runbook: UPI Transaction Service Restart Procedure (RB-UPI-001)</li>
  <li>Restart one instance at a time with 5-minute gap between instances</li>
  <li>Verify each instance is healthy before proceeding to the next</li>
</ol>

<h2>Monitoring</h2>
<p>A Prometheus alert has been configured to warn before memory reaches critical levels:</p>
<pre>- alert: UPITxnServiceMemoryLeakWarning
  expr: jvm_memory_used_bytes{job="upi-txn-service", area="heap"} / jvm_memory_max_bytes{job="upi-txn-service", area="heap"} > 0.75
  for: 30m
  labels:
    severity: warning
  annotations:
    summary: "UPI Transaction Service heap usage above 75% - known memory leak (KE-UPI-007)"
    runbook: "Follow workaround in KB article: Known Error - Memory Leak in UPI Transaction Service v2.3"</pre>

<h2>Permanent Fix Status</h2>
<ul>
  <li><strong>Fix Branch:</strong> <code>fix/txn-correlation-cache-cleanup</code></li>
  <li><strong>Pull Request:</strong> MR-4521 (approved, pending QA)</li>
  <li><strong>Fix Description:</strong> Restored cleanup logic in the <code>finally</code> block; added TTL-based eviction (1 hour) to the correlation cache as a defense-in-depth measure</li>
  <li><strong>Target Release:</strong> v2.4.0, scheduled for 2024-02-15</li>
  <li><strong>After Fix Deployed:</strong> Remove recurring restart Change Request; update this KEDB entry to "Resolved"</li>
</ul>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

### Article 8: Change Guide - Deploying UPI Service Updates

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | Change Implementation Guides |
   | Short description | Change Guide: Deploying UPI Service Updates |
   | Author | Ravi Kumar |

3. In the **Article body**, enter:

```html
<h2>Document Control</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><td><strong>Guide ID</strong></td><td>CG-UPI-001</td></tr>
<tr><td><strong>Version</strong></td><td>3.0</td></tr>
<tr><td><strong>Last Updated</strong></td><td>2024-01-12</td></tr>
<tr><td><strong>Author</strong></td><td>Ravi Kumar</td></tr>
<tr><td><strong>Applicable To</strong></td><td>All UPI microservices deployed on Kubernetes</td></tr>
</table>

<h2>Overview</h2>
<p>This guide provides the standard procedure for deploying updates to UPI platform services. All deployments must follow this procedure and be executed through an approved Change Request in ServiceNow.</p>

<h2>Pre-Deployment Checklist</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>#</th><th>Check</th><th>How to Verify</th><th>Status</th></tr>
<tr><td>1</td><td>Change Request approved in ServiceNow</td><td>CHG number in "Implement" state</td><td>[ ]</td></tr>
<tr><td>2</td><td>Docker image built and pushed to registry</td><td><code>docker pull registry.internal/upi/{service}:{version}</code></td><td>[ ]</td></tr>
<tr><td>3</td><td>All automated tests passed in CI pipeline</td><td>GitLab CI pipeline green for the release branch</td><td>[ ]</td></tr>
<tr><td>4</td><td>Release notes reviewed by Platform Engineering Lead</td><td>Release notes in GitLab tagged release</td><td>[ ]</td></tr>
<tr><td>5</td><td>Deployment window confirmed (low-traffic period)</td><td>Grafana TPS dashboard shows < 2000 TPS</td><td>[ ]</td></tr>
<tr><td>6</td><td>NOC notified of upcoming deployment</td><td>Message posted in #upi-noc-alerts</td><td>[ ]</td></tr>
<tr><td>7</td><td>Rollback plan documented in Change Request</td><td>Rollback section completed in CHG work notes</td><td>[ ]</td></tr>
<tr><td>8</td><td>Database migration scripts reviewed (if applicable)</td><td>DBA approval on migration PR</td><td>[ ]</td></tr>
</table>

<h2>Deployment Steps</h2>

<h3>Step 1: Begin Change Implementation</h3>
<ol>
  <li>Open the Change Request in ServiceNow</li>
  <li>Move state to "Implement"</li>
  <li>Add work note: "Beginning deployment of {service} v{version}"</li>
</ol>

<h3>Step 2: Deploy to Canary (10% traffic)</h3>
<ol>
  <li><strong>Update canary deployment:</strong>
    <pre>kubectl set image deployment/{service}-canary {service}=registry.internal/upi/{service}:{version} -n upi-production</pre>
  </li>
  <li><strong>Verify canary pod is running:</strong>
    <pre>kubectl get pods -n upi-production -l app={service},track=canary</pre>
  </li>
  <li><strong>Monitor canary for 10 minutes:</strong>
    <ul>
      <li>Error rate on canary instance should be < 1%</li>
      <li>Latency P99 should be within 20% of baseline</li>
      <li>No new error patterns in application logs</li>
    </ul>
  </li>
</ol>

<h3>Step 3: Rolling Update (Full Fleet)</h3>
<ol>
  <li>If canary metrics are healthy after 10 minutes, proceed with full rollout:
    <pre>kubectl set image deployment/{service} {service}=registry.internal/upi/{service}:{version} -n upi-production</pre>
  </li>
  <li>Monitor rollout progress:
    <pre>kubectl rollout status deployment/{service} -n upi-production --timeout=600s</pre>
  </li>
</ol>

<h3>Step 4: Post-Deployment Smoke Tests</h3>
<ol>
  <li><strong>Health check:</strong>
    <pre>curl -s http://{service}:8080/health | jq .
# Expected: {"status": "UP"}</pre>
  </li>
  <li><strong>Version verification:</strong>
    <pre>curl -s http://{service}:8080/info | jq '.build.version'
# Expected: "{version}"</pre>
  </li>
  <li><strong>Functional test (transaction service):</strong>
    <pre>curl -X POST http://upi-gateway:8080/api/v1/test/ping \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
# Expected: HTTP 200 with valid response</pre>
  </li>
  <li><strong>Monitor Grafana for 15 minutes:</strong>
    <ul>
      <li>Overall error rate stable</li>
      <li>No increase in any specific error code</li>
      <li>TPS and latency within normal range</li>
    </ul>
  </li>
</ol>

<h2>Rollback Plan</h2>
<p>If any of the following conditions occur, initiate immediate rollback:</p>
<ul>
  <li>Error rate increases by more than 2% after deployment</li>
  <li>P99 latency increases by more than 50%</li>
  <li>Any new critical error patterns appear</li>
  <li>Service health check returns non-UP status</li>
</ul>

<h3>Rollback Procedure</h3>
<pre># Immediate rollback to previous version
kubectl rollout undo deployment/{service} -n upi-production

# Verify rollback
kubectl rollout status deployment/{service} -n upi-production

# Confirm previous version is running
curl -s http://{service}:8080/info | jq '.build.version'</pre>

<h3>Post-Rollback Actions</h3>
<ol>
  <li>Update Change Request state to "Failed" with rollback details</li>
  <li>Create an Incident if customer impact occurred</li>
  <li>Create a Problem record to investigate the deployment failure</li>
  <li>Notify #upi-platform-eng with failure analysis</li>
</ol>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

### Article 9: Monitoring - Grafana Dashboard Guide for UPI Platform

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | Monitoring & Alerting |
   | Short description | Monitoring: Grafana Dashboard Guide for UPI Platform |
   | Author | Priya Sharma |

3. In the **Article body**, enter:

```html
<h2>Overview</h2>
<p>This guide describes the key Grafana dashboards used to monitor the UPI payment platform. Every NOC engineer and platform engineer should be familiar with these dashboards and know how to interpret the key panels.</p>

<h2>Dashboard 1: UPI Transaction Monitoring</h2>
<p><strong>URL:</strong> <code>https://grafana.internal/d/upi-txn-monitor</code></p>
<p><strong>Purpose:</strong> Real-time visibility into transaction processing health</p>

<h3>Key Panels</h3>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Panel</th><th>Metric</th><th>Normal Range</th><th>Alert Threshold</th></tr>
<tr>
  <td>Transactions Per Second (TPS)</td>
  <td><code>sum(rate(upi_transactions_total[1m]))</code></td>
  <td>2,000-8,000 TPS (varies by time of day)</td>
  <td>< 500 TPS during business hours</td>
</tr>
<tr>
  <td>Overall Failure Rate</td>
  <td><code>sum(rate(upi_transactions_total{status="failed"}[5m])) / sum(rate(upi_transactions_total[5m])) * 100</code></td>
  <td>0.5% - 1.5%</td>
  <td>> 2% for 5 minutes</td>
</tr>
<tr>
  <td>P99 Latency</td>
  <td><code>histogram_quantile(0.99, sum(rate(upi_request_duration_seconds_bucket[5m])) by (le))</code></td>
  <td>500ms - 1200ms</td>
  <td>> 2000ms for 5 minutes</td>
</tr>
<tr>
  <td>Failure Rate by Error Code</td>
  <td><code>sum by (error_code) (rate(upi_transactions_total{status="failed"}[5m]))</code></td>
  <td>Varies</td>
  <td>Any single code > 3%</td>
</tr>
</table>

<h2>Dashboard 2: UPI Infrastructure Health</h2>
<p><strong>URL:</strong> <code>https://grafana.internal/d/upi-infra-health</code></p>
<p><strong>Purpose:</strong> Infrastructure-level health of all UPI platform components</p>

<h3>Key Panels</h3>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Panel</th><th>What to Look For</th><th>Action if Abnormal</th></tr>
<tr>
  <td>Pod Status (Kubernetes)</td>
  <td>All pods in Running state, 1/1 Ready</td>
  <td>Check pod events: <code>kubectl describe pod {pod_name}</code></td>
</tr>
<tr>
  <td>CPU Usage by Service</td>
  <td>< 70% of request limits</td>
  <td>If sustained > 80%, consider scaling horizontally</td>
</tr>
<tr>
  <td>JVM Heap Usage</td>
  <td>40-65% after GC</td>
  <td>If > 75%, check for memory leak (see KE-UPI-007)</td>
</tr>
<tr>
  <td>Database Connections</td>
  <td>Active connections < 50% of pool max</td>
  <td>If > 80%, follow RB-UPI-001 (service restart)</td>
</tr>
<tr>
  <td>Kafka Consumer Lag</td>
  <td>< 1000 messages lag</td>
  <td>If > 5000, scale consumer group</td>
</tr>
<tr>
  <td>PostgreSQL Replication Lag</td>
  <td>< 1 second</td>
  <td>If > 10 seconds, investigate replica health</td>
</tr>
</table>

<h2>Dashboard 3: UPI Error Rate Analysis</h2>
<p><strong>URL:</strong> <code>https://grafana.internal/d/upi-error-analysis</code></p>
<p><strong>Purpose:</strong> Deep-dive into transaction failures by error code, bank, and PSP</p>

<h3>How to Use This Dashboard</h3>
<ol>
  <li>Use the time range selector to focus on the incident window</li>
  <li>Check "Error Code Distribution" pie chart to identify dominant error codes</li>
  <li>Use "Failure Rate by Bank" panel to see if failures are isolated to specific banks</li>
  <li>Use "Failure Heatmap" to identify time-based patterns</li>
  <li>Cross-reference with the UPI Error Code Reference Guide for resolution steps</li>
</ol>

<h2>Useful Prometheus Queries for Ad-Hoc Investigation</h2>
<pre>
# Top 5 error codes in the last hour
topk(5, sum by (error_code) (increase(upi_transactions_total{status="failed"}[1h])))

# Success rate by PSP
sum by (psp_code) (rate(upi_transactions_total{status="success"}[5m])) / sum by (psp_code) (rate(upi_transactions_total[5m])) * 100

# Transaction volume comparison: today vs yesterday
sum(rate(upi_transactions_total[5m]))  # Current
sum(rate(upi_transactions_total[5m] offset 1d))  # Yesterday

# Average transaction amount
sum(rate(upi_transaction_amount_sum[5m])) / sum(rate(upi_transaction_amount_count[5m]))
</pre>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

### Article 10: Runbook - UPI Settlement Reconciliation Failure

1. Navigate to **Knowledge > Create New**
2. Fill in the fields:

   | Field | Value |
   |-------|-------|
   | Knowledge Base | UPI Operations Knowledge Base |
   | Category | Runbooks & Standard Operating Procedures |
   | Short description | Runbook: UPI Settlement Reconciliation Failure |
   | Author | Amit Verma |

3. In the **Article body**, enter:

```html
<h2>Document Control</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><td><strong>Runbook ID</strong></td><td>RB-UPI-003</td></tr>
<tr><td><strong>Version</strong></td><td>1.2</td></tr>
<tr><td><strong>Last Updated</strong></td><td>2024-01-14</td></tr>
<tr><td><strong>Author</strong></td><td>Amit Verma</td></tr>
<tr><td><strong>Classification</strong></td><td>Internal - Operations</td></tr>
</table>

<h2>Purpose</h2>
<p>This runbook covers the investigation and resolution of settlement reconciliation failures. Settlement reconciliation runs every 30 minutes and compares transactions processed by the UPI switch against bank-reported settlement files. Mismatches require investigation and manual resolution.</p>

<h2>When to Use This Runbook</h2>
<ul>
  <li>Grafana alert: "UPI Settlement Reconciliation Mismatch Detected"</li>
  <li>Settlement batch job fails or completes with errors</li>
  <li>Bank reports discrepancy in settlement amounts</li>
  <li>End-of-day settlement totals do not balance</li>
</ul>

<h2>Step 1: Identify the Scope of the Mismatch</h2>
<ol>
  <li><strong>Check settlement job status:</strong>
    <pre>curl -s http://upi-settlement-service:8080/api/v1/settlement/batches?status=FAILED | jq .</pre>
  </li>
  <li><strong>Get mismatch details:</strong>
    <pre>curl -s http://upi-settlement-service:8080/api/v1/settlement/mismatches?batch_id={batch_id} | jq .</pre>
  </li>
  <li><strong>Determine mismatch type:</strong>
    <ul>
      <li><strong>Type 1: NPCI processed, bank not reported</strong> - Transaction exists in our ledger but missing from bank file</li>
      <li><strong>Type 2: Bank reported, NPCI not processed</strong> - Transaction in bank file but not in our ledger</li>
      <li><strong>Type 3: Amount mismatch</strong> - Both sides have the transaction but amounts differ</li>
    </ul>
  </li>
</ol>

<h2>Step 2: Investigation by Mismatch Type</h2>

<h3>Type 1: Transaction Missing from Bank File</h3>
<ol>
  <li>Verify transaction status in our ledger:
    <pre>SELECT txn_id, status, amount, bank_code, created_at, updated_at
FROM txn_ledger WHERE txn_id = '{txn_id}';</pre>
  </li>
  <li>Check if the credit instruction was successfully delivered to the bank:
    <pre>SELECT * FROM outbound_messages WHERE txn_id = '{txn_id}' AND message_type = 'CREDIT';</pre>
  </li>
  <li>If credit was delivered but bank did not process:
    <ul>
      <li>Contact bank operations team via the bank hotline</li>
      <li>Provide transaction ID, amount, timestamp</li>
      <li>Bank will confirm if they received and processed the credit</li>
    </ul>
  </li>
</ol>

<h3>Type 2: Transaction Missing from NPCI Ledger</h3>
<ol>
  <li>This is rare and may indicate data integrity issues</li>
  <li>Check if the transaction was processed during a known outage window</li>
  <li>Search application logs for the transaction ID:
    <pre>kubectl logs -l app=upi-txn-service -n upi-production --since=24h | grep '{txn_id}'</pre>
  </li>
  <li>If transaction genuinely missing, escalate to Platform Engineering with all evidence</li>
</ol>

<h3>Type 3: Amount Mismatch</h3>
<ol>
  <li>Compare amounts:
    <pre>SELECT txn_id, amount as npci_amount, bank_reported_amount,
       (amount - bank_reported_amount) as difference
FROM settlement_mismatches WHERE batch_id = '{batch_id}' AND mismatch_type = 'AMOUNT';</pre>
  </li>
  <li>Check for currency conversion or rounding issues</li>
  <li>Check if a reversal or refund was processed that the bank did not account for</li>
</ol>

<h2>Step 3: Resolution</h2>
<ol>
  <li>For each mismatch, create a settlement adjustment record:
    <pre>curl -X POST http://upi-settlement-service:8080/api/v1/settlement/adjustment \
  -H "Content-Type: application/json" \
  -d '{
    "batch_id": "{batch_id}",
    "txn_id": "{txn_id}",
    "adjustment_type": "CREDIT|DEBIT",
    "amount": {amount},
    "reason": "Settlement reconciliation - {description}",
    "approved_by": "{approver}"
  }'</pre>
  </li>
  <li>Adjustments above INR 1,00,000 require approval from the Settlement Manager</li>
  <li>All adjustments must be documented in the Change Request work notes</li>
</ol>

<h2>Escalation</h2>
<ul>
  <li>Mismatches > INR 10,00,000: Escalate to Finance and Settlement Manager immediately</li>
  <li>Recurring mismatches from the same bank: Create a Problem record for root cause investigation</li>
  <li>System-wide reconciliation failure: Escalate to Platform Engineering as P2</li>
</ul>
```

4. Set **Workflow State** to "Draft"
5. Click **Submit**

---

## Part 5: Knowledge Workflow Configuration

### Step 5.1: Understand the Default Knowledge Workflow

ServiceNow includes a default approval workflow for knowledge articles. Let us examine and configure it for our UPI Knowledge Base.

1. Navigate to **Knowledge > Administration > Knowledge Bases**
2. Open "UPI Operations Knowledge Base"
3. Note the **Workflow** field - it should reference the "Knowledge" workflow

### Step 5.2: View the Knowledge Workflow

1. Navigate to **Workflow > Workflow Editor**
2. Search for workflow: **Knowledge**
3. Open the workflow to see the visual flow:

```
+-------+     +-----------+     +----------+     +-----------+
| Draft | --> | Submitted | --> | Review   | --> | Published |
+-------+     +-----------+     +----------+     +-----------+
                                     |
                                     | (Rejected)
                                     v
                                +-----------+
                                |  Draft    |
                                | (Rework)  |
                                +-----------+
```

### Step 5.3: Configure Approval Rules

1. Navigate to **Knowledge > Administration > Knowledge Properties**
2. Set the following properties:

   | Property | Value | Purpose |
   |----------|-------|---------|
   | `glide.knowman.requires_approval` | true | Require approval before publishing |
   | `glide.knowman.approval_type` | Manager | Articles require manager approval |
   | `glide.knowman.block_duplicate_short_descriptions` | true | Prevent duplicate article titles |

### Step 5.4: Walk Through the Approval Process

Let us take one of our articles through the full workflow.

1. Navigate to **Knowledge > Articles > All**
2. Open "UPI Error Code Reference Guide" (currently in Draft state)
3. Click **Submit for Review** (or change Workflow State to "Review")
4. Observe:
   - The article state changes to "Review"
   - An approval request is generated
   - The approver (Ravi Kumar, as KB Manager) receives a notification

5. **As Ravi Kumar** (or impersonating Ravi Kumar):
   - Navigate to **Self-Service > My Approvals**
   - Open the pending approval for the KB article
   - Review the article content
   - Click **Approve**

6. Observe the article state changes to **Published**
7. Navigate to **Knowledge > Homepage** and verify the article appears

### Step 5.5: Test the Rejection Flow

1. Open another Draft article (e.g., "Runbook: UPI Database Failover Procedure")
2. Submit for Review
3. As the approver, click **Reject** and add a comment: "Please add estimated time for each failover step."
4. Observe:
   - The article returns to **Draft** state
   - The rejection comment is visible to the author
   - The author can revise and resubmit

---

## Part 6: Knowledge Integration with Incidents

### Step 6.1: Enable Suggested Knowledge on Incident Form

1. Navigate to **System Definition > Plugins**
2. Verify that the **Knowledge Management - Service Portal (com.snc.knowledge_management.portal)** plugin is active
3. Navigate to **Knowledge > Administration > Knowledge Properties**
4. Ensure the following properties are set:

   | Property | Value |
   |----------|-------|
   | `glide.knowman.show_portal_search` | true |
   | `glide.knowman.search.on_incident` | true |

### Step 6.2: Create an Incident and Observe KB Suggestions

1. Navigate to **Incident > Create New**
2. Fill in the form:

   | Field | Value |
   |-------|-------|
   | Caller | Priya Sharma |
   | Category | Software |
   | Short description | UPI transactions failing with error code U01 timeout |
   | Description | Multiple UPI transactions are timing out with error code U01. Failure rate has increased to 4% in the last 10 minutes. Grafana shows elevated P99 latency. |
   | Impact | 2 - Medium |
   | Urgency | 2 - Medium |
   | Assignment group | Platform Engineering |

3. **Before submitting**, look at the right side of the form or the "Knowledge" related section
4. Observe: ServiceNow suggests relevant KB articles based on the short description keywords
5. You should see suggestions including:
   - "UPI Error Code Reference Guide" (matches "error code U01")
   - "Troubleshooting: High Transaction Failure Rate" (matches "failing", "failure rate")
   - "Runbook: UPI Transaction Service Restart Procedure" (related content)

6. Click on "UPI Error Code Reference Guide" to view it inline
7. Submit the incident

### Step 6.3: Attach a Knowledge Article to an Incident

1. Open the incident you just created
2. Scroll to the **Knowledge** tab or related list
3. Click **Search Knowledge**
4. Search for "UPI Transaction Service Restart"
5. Click on the article to attach it
6. This creates a link between the incident and the KB article

### Step 6.4: Create a Knowledge Article from an Incident

1. While on the incident form, click the **Create Knowledge** button (in the header or related links)
2. This opens a new KB article form pre-populated with:
   - Short description from the incident
   - Incident details in the article body
3. Edit the content to create a proper resolution article
4. Select Knowledge Base: "UPI Operations Knowledge Base"
5. Select Category: "Known Issues & Workarounds"
6. Submit the article

> **Key Insight:** This is KCS in action - knowledge is created as a byproduct of incident resolution, not as a separate task.

---

## Part 7: Known Error Database (KEDB)

### 7.1 Understanding KEDB

The Known Error Database (KEDB) is not a separate system in ServiceNow. It is a **subset of the Knowledge Base** consisting of articles that document Known Errors - issues where the root cause has been identified through Problem Management, and a workaround or permanent fix is documented.

```
+-------------------------------+
|      Knowledge Base           |
|                               |
|  +-------------------------+ |
|  |  General KB Articles    | |
|  |  (How-Tos, Runbooks,    | |
|  |   Architecture, etc.)   | |
|  +-------------------------+ |
|                               |
|  +-------------------------+ |
|  |        KEDB             | |
|  |  (Known Error Articles) | |
|  |  - Linked to Problems   | |
|  |  - Workaround documented| |
|  |  - Fix status tracked   | |
|  +-------------------------+ |
+-------------------------------+
```

### 7.2 KEDB Article Standard Format

Every Known Error article should follow this standard structure:

| Section | Description |
|---------|-------------|
| **Known Error Record** | KEDB ID, related Problem, affected CI, status |
| **Symptoms** | Observable indicators that this known error is occurring |
| **Root Cause Analysis** | Technical explanation of why this issue occurs |
| **Impact** | Business and technical impact assessment |
| **Workaround** | Steps to mitigate the issue until a permanent fix is available |
| **Monitoring** | Alerts or dashboards to detect this issue proactively |
| **Permanent Fix Status** | Status of the permanent resolution, target version/date |

### 7.3 Link a Problem Record to a KB Article

1. Navigate to **Problem > All Problems**
2. Open an existing Problem record (or create one):

   | Field | Value |
   |-------|-------|
   | Short description | Recurring memory exhaustion on UPI Transaction Service |
   | Description | The UPI Transaction Service (v2.3.x) experiences a gradual memory leak that causes service degradation after approximately 7 days of uptime. |
   | Category | Software |
   | Assignment group | Platform Engineering |
   | Assigned to | Amit Verma |
   | State | Known Error |

3. On the Problem form, look for the **Related Articles** or **Knowledge** related list
4. Click **New** or **Search Knowledge**
5. Search for "Known Error: Memory Leak in UPI Transaction Service v2.3"
6. Link the article to the Problem record

> **Result:** The Problem record now references the KEDB article, and the KEDB article references the Problem record. When an incident is created with similar symptoms, agents can find both the Problem and the workaround through knowledge search.

### 7.4 KEDB Workflow in Practice

```
  Problem          Root Cause         Known Error         Workaround          Fix Deployed
  Identified  -->  Analyzed      -->  Created in KB  -->  Communicated   -->  Article Updated
                                                          to NOC              to "Resolved"
      |                |                   |                   |                    |
  (Problem         (Problem            (KB Article        (Incident           (Problem
   Record           Record              Created)           templates            Closed)
   Created)         Updated)                               updated)
```

---

## Practice Exercises

### Exercise 1: Create a Runbook Article

Create a new KB article with the following details:

| Field | Value |
|-------|-------|
| Knowledge Base | UPI Operations Knowledge Base |
| Category | Runbooks & Standard Operating Procedures |
| Short description | Runbook: UPI Settlement Batch Processing |
| Author | Amit Verma |

**Content requirements:**
- Include document control table (Runbook ID: RB-UPI-004)
- Document the settlement batch schedule (every 30 minutes)
- Pre-checks before running a manual settlement batch
- Steps to trigger a manual settlement run
- How to verify settlement completion
- Troubleshooting steps if a batch fails
- Escalation criteria

### Exercise 2: Full Workflow Walkthrough

1. Create a new Draft article: "FAQ: Common UPI Transaction Questions for Service Desk"
2. Submit the article for Review
3. Approve the article (as KB Manager)
4. Verify it appears on the Knowledge Homepage as Published
5. Note the version number

### Exercise 3: Retire an Article

1. Open Article 7 (Known Error: Memory Leak in UPI Transaction Service v2.3)
2. Assume the permanent fix (v2.4.0) has been deployed
3. Change the article state to **Retired**
4. Observe:
   - The article no longer appears in standard search results
   - The article is still accessible via direct URL or admin view
   - The linked Problem record is not affected

**Questions to answer:**
- Can end users still find retired articles through search?
- What happens to incidents that reference a retired article?
- When should you retire vs. update an article?

### Exercise 4: Incident-to-Knowledge Flow

1. Create a new incident:

   | Field | Value |
   |-------|-------|
   | Short description | UPI QR code payments failing with U66 device fingerprint mismatch |
   | Description | Multiple users reporting QR code payment failures. Error code U66 returned. Appears to affect users who recently updated their mobile app. |
   | Impact | 2 - Medium |
   | Urgency | 1 - High |

2. Use Knowledge Search from the incident to find relevant articles
3. Verify that "UPI Error Code Reference Guide" appears in suggestions
4. Use the article to identify that U66 relates to device fingerprint mismatch
5. Add work notes describing the resolution based on the KB article

### Exercise 5: Create a KEDB Article

Create a new Known Error article:

| Field | Value |
|-------|-------|
| Knowledge Base | UPI Operations Knowledge Base |
| Category | Known Issues & Workarounds |
| Short description | Known Error: QR Code Payment Failure After App Update v4.2 |

**Content requirements (use the KEDB standard format):**
- KEDB ID: KE-UPI-008
- Symptom: Users who updated to UPI mobile app v4.2 experience U66 errors on QR code payments
- Root Cause: The app update changed the device fingerprint generation algorithm, causing mismatch with registered fingerprints
- Workaround: Users must de-register and re-register their device through the app settings
- Permanent Fix: App v4.2.1 patch to maintain backward compatibility with existing fingerprints (ETA: 1 week)
- Create a Problem record and link it to this KEDB article

---

## Appendix A: Background Script - Automated Setup

The following background script creates the complete Knowledge Base structure and all articles from this lab. This is useful for quickly setting up a demo environment or resetting after testing.

Navigate to **System Definition > Scripts - Background** and run:

```javascript
// ============================================================
// Lab 10: Knowledge Management - Automated Setup Script
// Creates KB, Categories, and Articles for UPI Operations
// ============================================================

(function() {
    gs.info('=== Lab 10: Knowledge Management Setup - START ===');

    // ---------------------------------------------------------
    // Step 1: Create the Knowledge Base
    // ---------------------------------------------------------
    var kb = new GlideRecord('kb_knowledge_base');
    kb.addQuery('title', 'UPI Operations Knowledge Base');
    kb.query();

    if (!kb.hasNext()) {
        kb.initialize();
        kb.setValue('title', 'UPI Operations Knowledge Base');
        kb.setValue('description', 'Comprehensive knowledge repository for UPI payment platform operations, troubleshooting, runbooks, and standard operating procedures. Maintained by the Platform Engineering team.');
        kb.setValue('active', true);

        // Set owner to Ravi Kumar
        var owner = new GlideRecord('sys_user');
        owner.addQuery('first_name', 'Ravi');
        owner.addQuery('last_name', 'Kumar');
        owner.query();
        if (owner.next()) {
            kb.setValue('owner', owner.sys_id);
        }

        kb.insert();
        gs.info('Created Knowledge Base: UPI Operations Knowledge Base');
    } else {
        kb.next();
        gs.info('Knowledge Base already exists, using existing record');
    }

    var kbSysId = kb.sys_id;

    // ---------------------------------------------------------
    // Step 2: Create Categories
    // ---------------------------------------------------------
    var categories = [
        { label: 'UPI Error Codes & Resolution', description: 'Reference documentation for all UPI error codes with diagnostic steps and resolution procedures' },
        { label: 'Runbooks & Standard Operating Procedures', description: 'Step-by-step operational procedures for routine and emergency operations' },
        { label: 'Architecture & Design Documents', description: 'System architecture diagrams, design decisions, and integration specifications' },
        { label: 'Onboarding & Training', description: 'Guides for new team members joining the UPI platform team' },
        { label: 'Known Issues & Workarounds', description: 'Known Error Database (KEDB) - documented known issues with workarounds and fix status' },
        { label: 'Change Implementation Guides', description: 'Standard deployment procedures, rollback plans, and change execution guides' },
        { label: 'Monitoring & Alerting', description: 'Grafana dashboard guides, Prometheus query references, and alert response procedures' }
    ];

    var categorySysIds = {};

    categories.forEach(function(cat) {
        var catGR = new GlideRecord('kb_category');
        catGR.addQuery('label', cat.label);
        catGR.addQuery('kb_knowledge_base', kbSysId);
        catGR.query();

        if (!catGR.hasNext()) {
            catGR.initialize();
            catGR.setValue('label', cat.label);
            catGR.setValue('kb_knowledge_base', kbSysId);
            catGR.setValue('description', cat.description);
            catGR.insert();
            gs.info('Created category: ' + cat.label);
        } else {
            catGR.next();
            gs.info('Category already exists: ' + cat.label);
        }

        categorySysIds[cat.label] = catGR.sys_id;
    });

    // ---------------------------------------------------------
    // Step 3: Helper function to create articles
    // ---------------------------------------------------------
    function createArticle(shortDesc, categoryLabel, authorFirst, authorLast, body) {
        var art = new GlideRecord('kb_knowledge');
        art.addQuery('short_description', shortDesc);
        art.query();

        if (!art.hasNext()) {
            art.initialize();
            art.setValue('short_description', shortDesc);
            art.setValue('kb_knowledge_base', kbSysId);
            art.setValue('kb_category', categorySysIds[categoryLabel]);
            art.setValue('text', body);
            art.setValue('workflow_state', 'draft');

            // Set author
            var author = new GlideRecord('sys_user');
            author.addQuery('first_name', authorFirst);
            author.addQuery('last_name', authorLast);
            author.query();
            if (author.next()) {
                art.setValue('author', author.sys_id);
            }

            art.insert();
            gs.info('Created article: ' + shortDesc);
        } else {
            gs.info('Article already exists: ' + shortDesc);
        }
    }

    // ---------------------------------------------------------
    // Step 4: Create Articles
    // ---------------------------------------------------------

    // Article 1: UPI Error Code Reference Guide
    createArticle(
        'UPI Error Code Reference Guide',
        'UPI Error Codes & Resolution',
        'Amit', 'Verma',
        '<h2>Overview</h2><p>This document provides a comprehensive reference for UPI error codes encountered in the NPCI UPI payment platform.</p>' +
        '<h2>Error Code Reference Table</h2>' +
        '<table border="1" cellpadding="8"><thead><tr><th>Error Code</th><th>Description</th><th>Severity</th><th>Common Cause</th><th>Resolution</th></tr></thead><tbody>' +
        '<tr><td><b>U01</b></td><td>Transaction Timeout</td><td>High</td><td>Backend service latency exceeding 30-second threshold</td><td>Check service health, connection pool, restart if needed</td></tr>' +
        '<tr><td><b>U09</b></td><td>Beneficiary Bank Offline</td><td>Medium</td><td>Downstream bank gateway unreachable</td><td>Verify bank connectivity, enable circuit breaker</td></tr>' +
        '<tr><td><b>U16</b></td><td>Risk Threshold Exceeded</td><td>Medium</td><td>Transaction flagged by fraud detection</td><td>Review risk score, whitelist if false positive</td></tr>' +
        '<tr><td><b>U28</b></td><td>PSP Not Registered</td><td>Low</td><td>PSP identifier not found in registry</td><td>Verify PSP registration, check certificate</td></tr>' +
        '<tr><td><b>U30</b></td><td>Debit Failed</td><td>High</td><td>Insufficient funds or bank-side failure</td><td>Check bank connectivity, monitor failure rate</td></tr>' +
        '<tr><td><b>U48</b></td><td>Transaction Not Found</td><td>Medium</td><td>Replication lag or expired cache</td><td>Check primary DB, verify replication lag</td></tr>' +
        '<tr><td><b>U66</b></td><td>Device Fingerprint Mismatch</td><td>High</td><td>Device binding verification failed</td><td>Verify device registry, guide re-registration</td></tr>' +
        '<tr><td><b>U78</b></td><td>Remitter PSP Not Registered</td><td>Low</td><td>Remitter-side PSP not found</td><td>Follow U28 procedure for remitter side</td></tr>' +
        '</tbody></table>'
    );

    // Article 2: Transaction Service Restart
    createArticle(
        'Runbook: UPI Transaction Service Restart Procedure',
        'Runbooks & Standard Operating Procedures',
        'Ravi', 'Kumar',
        '<h2>Document Control</h2><p>Runbook ID: RB-UPI-001 | Version: 2.1</p>' +
        '<h2>Purpose</h2><p>Step-by-step procedure for performing a controlled restart of the UPI Transaction Service.</p>' +
        '<h2>Pre-Restart Checks</h2><ol><li>Verify current transaction volume</li><li>Check active in-flight transactions</li><li>Verify other instances are healthy</li><li>Notify the team</li></ol>' +
        '<h2>Restart Procedure</h2><p>Option A: kubectl rollout restart deployment/upi-txn-service -n upi-production</p><p>Option B: VM-based - remove from LB, restart, re-add to LB</p>' +
        '<h2>Post-Restart Validation</h2><ol><li>Verify service health</li><li>Check connection pool</li><li>Monitor error rate in Grafana</li><li>Verify TPS recovery</li></ol>'
    );

    // Article 3: Database Failover
    createArticle(
        'Runbook: UPI Database Failover Procedure',
        'Runbooks & Standard Operating Procedures',
        'Ravi', 'Kumar',
        '<h2>Document Control</h2><p>Runbook ID: RB-UPI-002 | Version: 1.4</p>' +
        '<h2>Purpose</h2><p>Procedure for performing a PostgreSQL primary-to-replica failover for the UPI transaction database.</p>' +
        '<h2>Pre-Failover Checks</h2><ol><li>Confirm primary is truly unhealthy</li><li>Check replica health and replication lag</li><li>Notify stakeholders</li></ol>' +
        '<h2>Failover Procedure</h2><ol><li>Promote the replica</li><li>Verify promotion</li><li>Update PgBouncer configuration</li><li>Reconfigure remaining replicas</li></ol>' +
        '<h2>Post-Failover Validation</h2><ol><li>Verify application connectivity</li><li>Check error rate</li><li>Verify replication from new primary</li></ol>'
    );

    // Article 4: Troubleshooting High Failure Rate
    createArticle(
        'Troubleshooting: High Transaction Failure Rate',
        'Known Issues & Workarounds',
        'Priya', 'Sharma',
        '<h2>Overview</h2><p>Guide for diagnosing and resolving elevated transaction failure rates on the UPI platform.</p>' +
        '<h2>Step 1: Assess the Situation</h2><p>Open Grafana Dashboard: UPI Transaction Monitoring. Check failure rate, error code distribution, and bank-specific failures.</p>' +
        '<h2>Step 2: Identify Root Cause</h2><p>Scenario A: U01 Timeout - check connection pool. Scenario B: U09 Bank Offline - check bank connectivity. Scenario C: U30 Debit Failed - check debit service. Scenario D: Multiple codes - check infrastructure.</p>' +
        '<h2>Step 3: Resolution</h2><p>Follow the appropriate runbook based on identified root cause.</p>' +
        '<h2>Escalation</h2><p>Failure rate > 10% for 5 min: Declare P1. Failure rate > 5% for 15 min: Escalate to Platform Engineering.</p>'
    );

    // Article 5: Architecture
    createArticle(
        'Architecture: UPI Payment Processing Flow',
        'Architecture & Design Documents',
        'Ravi', 'Kumar',
        '<h2>Overview</h2><p>End-to-end flow of a UPI payment transaction through the NPCI platform.</p>' +
        '<h2>Transaction Flow</h2><p>Payer Mobile App -> Payer PSP -> NPCI UPI Switch -> Payee PSP -> Payee Bank</p>' +
        '<h2>Components</h2><p>UPI Gateway Service (Java 17), UPI Transaction Service (Java 17), UPI Risk Engine (Python 3.11), UPI Settlement Service (Java 17), PostgreSQL 15, Redis 7.x, Kafka 3.x</p>' +
        '<h2>Performance</h2><p>Target TPS: 10,000. P99 Latency: < 2s. Availability: 99.95%.</p>'
    );

    // Article 6: Onboarding
    createArticle(
        'Onboarding: New Team Member Guide for UPI Platform',
        'Onboarding & Training',
        'Meera', 'Joshi',
        '<h2>Welcome</h2><p>Welcome to NPCI UPI Platform team! This guide covers your first week.</p>' +
        '<h2>Day 1: Access Requests</h2><p>Submit requests for: ServiceNow, Grafana, Prometheus, Kubernetes, GitLab, PagerDuty, Confluence, Slack channels.</p>' +
        '<h2>Day 1-2: Tool Setup</h2><p>Configure kubectl, bookmark Grafana dashboards, set up ServiceNow.</p>' +
        '<h2>Key Contacts</h2><p>Ravi Kumar (Platform Lead), Amit Verma (Sr. Engineer), Priya Sharma (NOC Lead), Meera Joshi (Service Desk Lead).</p>'
    );

    // Article 7: Known Error - Memory Leak
    createArticle(
        'Known Error: Memory Leak in UPI Transaction Service v2.3',
        'Known Issues & Workarounds',
        'Amit', 'Verma',
        '<h2>Known Error Record</h2><p>KEDB ID: KE-UPI-007 | Related Problem: PRB0042156 | Affected CI: upi-txn-service v2.3.x | Status: Workaround Available</p>' +
        '<h2>Symptoms</h2><p>JVM heap memory increases steadily over 7-10 days. GC pause times increase. P99 latency degrades. Eventually OOM crash.</p>' +
        '<h2>Root Cause</h2><p>Memory leak in TransactionCorrelationService.java - orphaned correlation entries not cleaned up for error codes U48 and U66.</p>' +
        '<h2>Workaround</h2><p>Perform scheduled rolling restart every 5 days during low-traffic window (02:00-04:00 IST).</p>' +
        '<h2>Permanent Fix</h2><p>Fix branch: fix/txn-correlation-cache-cleanup. Target release: v2.4.0 (ETA: 2024-02-15).</p>'
    );

    // Article 8: Change Guide - Deploying Updates
    createArticle(
        'Change Guide: Deploying UPI Service Updates',
        'Change Implementation Guides',
        'Ravi', 'Kumar',
        '<h2>Document Control</h2><p>Guide ID: CG-UPI-001 | Version: 3.0</p>' +
        '<h2>Pre-Deployment Checklist</h2><p>1. CHG approved 2. Docker image built 3. Tests passed 4. Release notes reviewed 5. Low-traffic window 6. NOC notified 7. Rollback plan documented 8. DB migrations reviewed</p>' +
        '<h2>Deployment Steps</h2><p>Step 1: Deploy to canary (10% traffic). Step 2: Monitor for 10 min. Step 3: Rolling update to full fleet. Step 4: Post-deployment smoke tests.</p>' +
        '<h2>Rollback Plan</h2><p>kubectl rollout undo deployment/{service} -n upi-production</p>'
    );

    // Article 9: Monitoring Guide
    createArticle(
        'Monitoring: Grafana Dashboard Guide for UPI Platform',
        'Monitoring & Alerting',
        'Priya', 'Sharma',
        '<h2>Dashboard 1: UPI Transaction Monitoring</h2><p>Key panels: TPS (2000-8000 normal), Failure Rate (0.5-1.5% normal), P99 Latency (500-1200ms normal).</p>' +
        '<h2>Dashboard 2: UPI Infrastructure Health</h2><p>Key panels: Pod status, CPU usage, JVM Heap, DB connections, Kafka consumer lag, PostgreSQL replication lag.</p>' +
        '<h2>Dashboard 3: UPI Error Rate Analysis</h2><p>Deep-dive into failures by error code, bank, and PSP.</p>' +
        '<h2>Useful Prometheus Queries</h2><p>Top 5 error codes, success rate by PSP, volume comparison today vs yesterday.</p>'
    );

    // Article 10: Settlement Reconciliation
    createArticle(
        'Runbook: UPI Settlement Reconciliation Failure',
        'Runbooks & Standard Operating Procedures',
        'Amit', 'Verma',
        '<h2>Document Control</h2><p>Runbook ID: RB-UPI-003 | Version: 1.2</p>' +
        '<h2>Purpose</h2><p>Investigation and resolution of settlement reconciliation failures.</p>' +
        '<h2>Step 1: Identify Scope</h2><p>Check batch status, get mismatch details, determine type (NPCI-only, Bank-only, Amount mismatch).</p>' +
        '<h2>Step 2: Investigation</h2><p>Type 1: Check credit delivery. Type 2: Search application logs. Type 3: Compare amounts, check for reversals.</p>' +
        '<h2>Step 3: Resolution</h2><p>Create settlement adjustment record. Adjustments > INR 1,00,000 require Settlement Manager approval.</p>'
    );

    gs.info('=== Lab 10: Knowledge Management Setup - COMPLETE ===');
    gs.info('Created: 1 Knowledge Base, 7 Categories, 10 Articles');

})();
```

---

## Appendix B: Verification Checklist

After completing this lab, verify the following:

| # | Check | How to Verify | Status |
|---|-------|--------------|--------|
| 1 | Knowledge Base exists | Knowledge > Administration > Knowledge Bases | [ ] |
| 2 | 7 categories created | Open KB record > Categories related list | [ ] |
| 3 | 10 articles created | Knowledge > Articles > All, filter by KB | [ ] |
| 4 | At least 1 article Published | Filter articles by Workflow State = Published | [ ] |
| 5 | At least 1 article Retired | Filter articles by Workflow State = Retired | [ ] |
| 6 | Incident linked to KB article | Open incident > Knowledge related list | [ ] |
| 7 | Problem linked to KEDB article | Open Problem > Related Articles | [ ] |
| 8 | KB search returns results on incident form | Create new incident with UPI keywords | [ ] |

---

## Key Takeaways

1. **Knowledge Management is not optional** - it is the difference between a 5-minute resolution and a 2-hour escalation at 2 AM
2. **DIKW model** helps structure what goes into the KB - not raw data, but analyzed knowledge with context
3. **KCS methodology** embeds knowledge creation into daily work rather than making it a separate burden
4. **KEDB** is a subset of the KB specifically for known errors linked to Problem records
5. **Knowledge workflow** (Draft, Review, Published, Retired) ensures quality control through peer review
6. **Integration with Incidents** means agents find answers faster, reducing MTTR
7. **Article versioning** allows updates without disrupting the published version

---

## What's Next

In **Lab 11**, we will configure the **Service Catalog** to create request-based workflows for the UPI platform, including access provisioning, change requests, and standard service offerings that leverage the knowledge articles created in this lab.

---

*Lab 10 of 22 | NPCI UPI Payment Platform - ITIL 4 ServiceNow Lab Series*
