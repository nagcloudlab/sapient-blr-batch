#!/usr/bin/env python3
"""Lab 10: Knowledge Management - Apply full article content to ServiceNow"""

import urllib.request
import json
import ssl
import base64

INSTANCE = "https://dev302242.service-now.com"
AUTH = base64.b64encode(b"admin:1=zjfqMCYT9$").decode()
CTX = ssl.create_default_context()

def api_call(method, endpoint, data=None):
    url = f"{INSTANCE}/api/now/table/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {AUTH}"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    resp = urllib.request.urlopen(req, context=CTX)
    return json.loads(resp.read())["result"]

# Article IDs from existing records
articles = {
    "7e9d97cd93e30710068e718efaba10dc": {
        "short_description": "UPI Error Code Reference Guide",
        "text": """<h2>Overview</h2>
<p>This document provides a comprehensive reference for UPI error codes encountered in the NPCI UPI payment platform. Each error code includes a description, common causes, diagnostic steps, and resolution procedures. This guide should be the first reference when investigating transaction failures.</p>

<h2>Error Code Reference Table</h2>
<table border="1" cellpadding="8" cellspacing="0">
<thead>
<tr><th>Error Code</th><th>Description</th><th>Severity</th><th>Common Cause</th><th>Resolution</th></tr>
</thead>
<tbody>
<tr>
  <td><strong>U01</strong></td><td>Transaction Timeout</td><td>High</td>
  <td>Backend service latency exceeding 30-second threshold; connection pool exhaustion; database query timeout</td>
  <td>1. Check service health: <code>curl -s http://upi-txn-service:8080/health</code><br/>2. Check connection pool: query Prometheus for <code>hikari_connections_active</code><br/>3. If connection pool exhausted, restart transaction service (see Runbook: UPI Transaction Service Restart)<br/>4. If database slow, check PostgreSQL slow query log</td>
</tr>
<tr>
  <td><strong>U09</strong></td><td>Beneficiary Bank Offline</td><td>Medium</td>
  <td>Downstream bank UPI gateway is unreachable or returning 5xx errors</td>
  <td>1. Verify bank connectivity<br/>2. Check NPCI switch dashboard for bank availability<br/>3. If bank confirmed offline, enable circuit breaker for affected bank<br/>4. Notify affected PSPs via broadcast alert<br/>5. Monitor for bank recovery</td>
</tr>
<tr>
  <td><strong>U16</strong></td><td>Risk Threshold Exceeded</td><td>Medium</td>
  <td>Transaction flagged by fraud detection engine; velocity check failure; amount exceeds risk threshold</td>
  <td>1. Review transaction in fraud dashboard<br/>2. Check risk score<br/>3. If false positive, whitelist pattern in risk engine<br/>4. If legitimate block, no action required<br/>5. Escalate to Risk and Compliance team if new fraud vector</td>
</tr>
<tr>
  <td><strong>U28</strong></td><td>PSP Not Registered</td><td>Low</td>
  <td>Payment Service Provider identifier not found in NPCI registry; expired PSP certificate</td>
  <td>1. Verify PSP registration in database<br/>2. Check certificate expiry<br/>3. If PSP not found, escalate to PSP Onboarding team<br/>4. If certificate expired, notify PSP to renew</td>
</tr>
<tr>
  <td><strong>U30</strong></td><td>Debit Failed</td><td>High</td>
  <td>Insufficient funds in remitter account; account frozen; bank-side debit processing failure</td>
  <td>1. Typically customer-side issue (insufficient funds)<br/>2. If bulk failures from single bank, check bank connectivity<br/>3. If systematic failures across banks, check UPI debit service health<br/>4. Monitor <code>upi_debit_failure_rate</code> metric<br/>5. Escalate if failure rate exceeds 5% for more than 10 minutes</td>
</tr>
<tr>
  <td><strong>U48</strong></td><td>Transaction Not Found</td><td>Medium</td>
  <td>Transaction ID not found in ledger; possible replication lag; transaction expired from cache</td>
  <td>1. Check primary database directly<br/>2. Check replication lag<br/>3. If replication lag &gt; 10 seconds, investigate replica health<br/>4. If transaction genuinely missing, check transaction service logs</td>
</tr>
<tr>
  <td><strong>U66</strong></td><td>Device Fingerprint Mismatch</td><td>High</td>
  <td>Device binding verification failed; user changed device without re-registration; potential account takeover</td>
  <td>1. Verify in device registry<br/>2. If user legitimately changed device, guide through re-registration<br/>3. If suspicious, escalate to Security team<br/>4. Log incident in fraud monitoring system</td>
</tr>
<tr>
  <td><strong>U78</strong></td><td>Remitter PSP Not Registered</td><td>Low</td>
  <td>Similar to U28 but specific to the remitter (sending) side PSP</td>
  <td>1. Follow same procedure as U28<br/>2. Additionally verify remitter-side VPA format is valid<br/>3. Check if PSP was recently deregistered or suspended</td>
</tr>
</tbody>
</table>

<h2>Escalation Guidelines</h2>
<ul>
  <li><strong>P1 (Critical):</strong> Any single error code causing &gt; 10% overall transaction failure rate</li>
  <li><strong>P2 (High):</strong> Any single error code causing &gt; 5% failure rate for more than 15 minutes</li>
  <li><strong>P3 (Moderate):</strong> Any new/unknown error code appearing in production</li>
</ul>

<h2>Related Resources</h2>
<ul>
  <li>Runbook: UPI Transaction Service Restart Procedure</li>
  <li>Troubleshooting: High Transaction Failure Rate</li>
  <li>Grafana Dashboard: UPI Transaction Monitoring</li>
</ul>"""
    },

    "079dd7cd93e30710068e718efaba1016": {
        "short_description": "Runbook: UPI Transaction Service Restart Procedure",
        "text": """<h2>Document Control</h2>
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
    <p>Record the current TPS. If TPS &gt; 5000, coordinate with NOC before proceeding.</p>
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
    <p>Post in #upi-noc-alerts: "MAINTENANCE: Restarting UPI Transaction Service on [server]. Expected duration: 5 minutes."</p>
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
  <li><strong>Wait for connections to drain (60 seconds)</strong></li>
  <li><strong>Restart the service:</strong>
    <pre>sudo systemctl restart upi-transaction-service</pre>
  </li>
  <li><strong>Wait for service to become healthy (30-45 seconds)</strong></li>
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
  <li><strong>Check connection pool:</strong> Active connections should be &lt; 20% of max pool size.</li>
  <li><strong>Monitor error rate in Grafana:</strong> Confirm error rate returns to baseline (&lt; 0.5%) within 5 minutes.</li>
  <li><strong>Verify TPS recovery:</strong> Transaction throughput should return to pre-restart levels within 2 minutes.</li>
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
</ul>"""
    },

    "8f9dd7cd93e30710068e718efaba1036": {
        "short_description": "Runbook: UPI Database Failover Procedure",
        "text": """<h2>Document Control</h2>
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
  |   upi-db-primary  |  ======================================&gt; |  upi-db-replica-1 |
  |  (PostgreSQL 15)  |                                        |  (PostgreSQL 15)  |
  |  192.168.1.10:5432 |                                       |  192.168.1.11:5432 |
  +-------------------+                                        +-------------------+
          |
          |            Streaming Replication             +-------------------+
          +============================================&gt; |  upi-db-replica-2 |
                                                        |  (PostgreSQL 15)  |
                                                        |  192.168.1.12:5432 |
                                                        +-------------------+

  Connection String (PgBouncer): Host: upi-pgbouncer.internal:6432 | Database: upi_transactions
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
    <p>Lag should be &lt; 5 seconds for a clean failover.</p>
  </li>
  <li><strong>Notify stakeholders:</strong>
    <p>Post in #upi-noc-alerts and #upi-platform-eng: "DATABASE FAILOVER: Initiating failover from upi-db-primary to upi-db-replica-1. Expected service interruption: 15-30 seconds."</p>
  </li>
</ol>

<h2>Failover Procedure</h2>
<ol>
  <li><strong>Promote the replica to primary:</strong>
    <pre>sudo -u postgres pg_ctl promote -D /var/lib/postgresql/15/main</pre>
  </li>
  <li><strong>Verify promotion was successful:</strong>
    <pre>psql -h upi-db-replica-1 -U upi_admin -c "SELECT pg_is_in_recovery();"</pre>
    <p>Expected result: <code>f</code> (false, meaning it is now the primary).</p>
  </li>
  <li><strong>Update PgBouncer configuration:</strong>
    <pre>sudo systemctl reload pgbouncer</pre>
  </li>
  <li><strong>Reconfigure remaining replica to follow new primary:</strong>
    <pre>sudo systemctl restart postgresql@15-main</pre>
  </li>
</ol>

<h2>Post-Failover Validation</h2>
<ol>
  <li><strong>Verify application connectivity</strong></li>
  <li><strong>Check application error rate:</strong> Should return to baseline within 2 minutes.</li>
  <li><strong>Verify replication from new primary</strong></li>
</ol>

<h2>Post-Incident: Rebuild Old Primary as Replica</h2>
<p>After the incident is resolved, the old primary should be rebuilt as a replica using <code>pg_basebackup</code>. This task should be tracked as a follow-up Problem record.</p>"""
    },

    "33e5a4c193eb8310068e718efaba10e4": {
        "short_description": "Troubleshooting: High Transaction Failure Rate",
        "text": """<h2>Overview</h2>
<p>This troubleshooting guide helps NOC engineers diagnose and resolve elevated transaction failure rates on the UPI platform. A "high" failure rate is defined as any rate above 2% sustained for more than 5 minutes.</p>

<h2>Symptom Identification</h2>
<ul>
  <li><strong>Grafana Alert:</strong> "UPI Transaction Failure Rate High" (triggers at &gt; 2% for 5 min)</li>
  <li><strong>Prometheus Alert:</strong> <code>UPITransactionFailureRateHigh</code> firing in Alertmanager</li>
  <li><strong>NOC Dashboard:</strong> Red indicator on the UPI Health Overview panel</li>
  <li><strong>Customer reports:</strong> Multiple complaints about failed payments</li>
</ul>

<h2>Step 1: Assess the Situation</h2>
<ol>
  <li><strong>Open Grafana Dashboard:</strong> Navigate to UPI Transaction Monitoring
    <ul>
      <li>Check the "Overall Failure Rate" panel</li>
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
  <li>If connection pool &gt; 90%, follow Runbook: UPI Transaction Service Restart</li>
  <li>If database is slow, check PostgreSQL for long-running queries</li>
</ul>

<h3>Scenario B: Dominant error code is U09 (Beneficiary Bank Offline)</h3>
<ul>
  <li>Check which banks are affected</li>
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
  <li>If failure rate &gt; 10% for &gt; 5 minutes: <strong>Declare P1 Major Incident</strong></li>
  <li>If failure rate &gt; 5% for &gt; 15 minutes and root cause not identified: <strong>Escalate to Platform Engineering</strong></li>
  <li>If NPCI switch suspected: <strong>Escalate to NPCI Operations via hotline</strong></li>
</ul>"""
    },

    "439dd7cd93e30710068e718efaba1064": {
        "short_description": "Architecture: UPI Payment Processing Flow",
        "text": """<h2>Overview</h2>
<p>This document describes the end-to-end flow of a UPI payment transaction through the NPCI platform, from initiation on the payer's device to final settlement. Understanding this flow is essential for troubleshooting, capacity planning, and onboarding new team members.</p>

<h2>End-to-End Transaction Flow</h2>
<pre>
  +----------+     +----------+     +-------------+     +----------+     +----------+
  |  Payer   |     |  Payer   |     |    NPCI     |     |  Payee   |     |  Payee   |
  |  Mobile  |----&gt;|  PSP     |----&gt;|    UPI      |----&gt;|  PSP     |----&gt;|  Bank    |
  |  App     |     |  Server  |     |   Switch    |     |  Server  |     |  Server  |
  +----------+     +----------+     +-------------+     +----------+     +----------+
       |                |                  |                  |                |
       | 1. Initiate    | 2. Validate      | 3. Route &amp;       | 7. Credit      | 8. Credit
       |    Payment     |    &amp; Forward     |    Process       |    Request     |    Account
</pre>

<h2>Component Descriptions</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Component</th><th>Description</th><th>Technology</th><th>ServiceNow CI</th></tr>
<tr><td>UPI Gateway Service</td><td>Entry point for all PSP requests; handles authentication, rate limiting, and request validation</td><td>Java 17, Spring Boot 3.x</td><td>upi-gateway-service</td></tr>
<tr><td>UPI Transaction Service</td><td>Core transaction processing engine; orchestrates debit/credit flows</td><td>Java 17, Spring Boot 3.x</td><td>upi-txn-service</td></tr>
<tr><td>UPI Risk Engine</td><td>Real-time fraud detection and risk scoring for all transactions</td><td>Python 3.11, FastAPI</td><td>upi-risk-engine</td></tr>
<tr><td>UPI Settlement Service</td><td>Batch settlement processing; runs every 30 minutes</td><td>Java 17, Spring Batch</td><td>upi-settlement-service</td></tr>
<tr><td>PostgreSQL Cluster</td><td>Primary transaction database; stores transaction ledger</td><td>PostgreSQL 15, Patroni</td><td>upi-db-primary</td></tr>
<tr><td>Redis Cluster</td><td>Session cache, rate limiting counters, and transaction deduplication</td><td>Redis 7.x Cluster</td><td>upi-redis-cluster</td></tr>
<tr><td>Kafka Cluster</td><td>Event streaming for async processing, audit logging, and inter-service communication</td><td>Apache Kafka 3.x</td><td>upi-kafka-cluster</td></tr>
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
  INITIATED --&gt; VALIDATED --&gt; DEBIT_PENDING --&gt; DEBITED --&gt; CREDIT_PENDING --&gt; CREDITED --&gt; SETTLED
       |            |              |                            |
       v            v              v                            v
    REJECTED    VALIDATION     DEBIT_FAILED              CREDIT_FAILED
                _FAILED                                  (Refund Initiated)
</pre>

<h2>Performance Characteristics</h2>
<ul>
  <li><strong>Target TPS:</strong> 10,000 transactions per second at peak</li>
  <li><strong>P99 Latency:</strong> &lt; 2 seconds end-to-end</li>
  <li><strong>Availability Target:</strong> 99.95% (measured monthly)</li>
  <li><strong>Settlement Cycles:</strong> Every 30 minutes, 24x7</li>
</ul>"""
    },

    "cb9dd7cd93e30710068e718efaba106b": {
        "short_description": "Onboarding: New Team Member Guide for UPI Platform",
        "text": """<h2>Welcome to the UPI Platform Team</h2>
<p>Welcome to NPCI's UPI Platform team! This guide will help you get set up with the tools, access, and knowledge you need to be productive. Please work through each section in order during your first week.</p>

<h2>Day 1: Access Requests</h2>
<p>Submit the following access requests through ServiceNow (Self-Service &gt; Service Catalog &gt; Access Requests):</p>
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
      <li>UPI Transaction Monitoring</li>
      <li>UPI Infrastructure Health</li>
      <li>UPI Error Rate Analysis</li>
    </ul>
  </li>
  <li><strong>ServiceNow setup:</strong> Familiarize yourself with Incident Management, Knowledge Base, and CMDB.</li>
</ol>

<h2>Day 2-3: Required Reading</h2>
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
  <li><strong>Monday-Tuesday:</strong> Shadow NOC engineer during morning shift</li>
  <li><strong>Wednesday:</strong> Shadow Platform Engineer during a change deployment</li>
  <li><strong>Thursday:</strong> Participate in weekly Problem Review meeting</li>
  <li><strong>Friday:</strong> Shadow Service Desk for customer-facing ticket handling</li>
</ul>

<h2>30-Day Milestone</h2>
<ul>
  <li>Navigate all Grafana dashboards and interpret key metrics</li>
  <li>Triage P3/P4 incidents independently</li>
  <li>Execute runbooks for standard procedures</li>
  <li>Create and submit KB articles for review</li>
</ul>"""
    },

    "cb9dd7cd93e30710068e718efaba108d": {
        "short_description": "Known Error: Memory Leak in UPI Transaction Service v2.3",
        "text": """<h2>Known Error Record</h2>
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
  <li>JVM heap memory usage increases steadily over 7-10 days from baseline 45% to &gt;85%</li>
  <li>Garbage collection pause times increase from ~50ms to &gt;500ms</li>
  <li>Transaction latency (P99) degrades from 800ms to &gt;3000ms after ~10 days of uptime</li>
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
<p>Perform a scheduled rolling restart of all UPI Transaction Service instances every 5 days.</p>
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
  expr: jvm_memory_used_bytes{job="upi-txn-service", area="heap"} / jvm_memory_max_bytes{job="upi-txn-service", area="heap"} &gt; 0.75
  for: 30m
  labels:
    severity: warning
  annotations:
    summary: "UPI Transaction Service heap usage above 75% - known memory leak (KE-UPI-007)"</pre>

<h2>Permanent Fix Status</h2>
<ul>
  <li><strong>Fix Branch:</strong> <code>fix/txn-correlation-cache-cleanup</code></li>
  <li><strong>Pull Request:</strong> MR-4521 (approved, pending QA)</li>
  <li><strong>Fix Description:</strong> Restored cleanup logic in the finally block; added TTL-based eviction (1 hour) as defense-in-depth</li>
  <li><strong>Target Release:</strong> v2.4.0, scheduled for 2024-02-15</li>
  <li><strong>After Fix Deployed:</strong> Remove recurring restart Change Request; update this KEDB entry to "Resolved"</li>
</ul>"""
    },

    "c39dd7cd93e30710068e718efaba10ae": {
        "short_description": "Change Guide: Deploying UPI Service Updates",
        "text": """<h2>Document Control</h2>
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
<tr><th>#</th><th>Check</th><th>How to Verify</th></tr>
<tr><td>1</td><td>Change Request approved in ServiceNow</td><td>CHG number in "Implement" state</td></tr>
<tr><td>2</td><td>Docker image built and pushed to registry</td><td><code>docker pull registry.internal/upi/{service}:{version}</code></td></tr>
<tr><td>3</td><td>All automated tests passed in CI pipeline</td><td>GitLab CI pipeline green for the release branch</td></tr>
<tr><td>4</td><td>Release notes reviewed by Platform Engineering Lead</td><td>Release notes in GitLab tagged release</td></tr>
<tr><td>5</td><td>Deployment window confirmed (low-traffic period)</td><td>Grafana TPS dashboard shows &lt; 2000 TPS</td></tr>
<tr><td>6</td><td>NOC notified of upcoming deployment</td><td>Message posted in #upi-noc-alerts</td></tr>
<tr><td>7</td><td>Rollback plan documented in Change Request</td><td>Rollback section completed in CHG work notes</td></tr>
<tr><td>8</td><td>Database migration scripts reviewed (if applicable)</td><td>DBA approval on migration PR</td></tr>
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
  <li><strong>Monitor canary for 10 minutes:</strong> Error rate &lt; 1%, latency P99 within 20% of baseline, no new error patterns</li>
</ol>

<h3>Step 3: Rolling Update (Full Fleet)</h3>
<ol>
  <li>If canary metrics are healthy, proceed:
    <pre>kubectl set image deployment/{service} {service}=registry.internal/upi/{service}:{version} -n upi-production</pre>
  </li>
  <li>Monitor rollout:
    <pre>kubectl rollout status deployment/{service} -n upi-production --timeout=600s</pre>
  </li>
</ol>

<h3>Step 4: Post-Deployment Smoke Tests</h3>
<ol>
  <li>Health check, version verification, functional test</li>
  <li>Monitor Grafana for 15 minutes</li>
</ol>

<h2>Rollback Plan</h2>
<p>If error rate increases by &gt; 2%, P99 latency increases by &gt; 50%, or any new critical errors appear:</p>
<pre>kubectl rollout undo deployment/{service} -n upi-production
kubectl rollout status deployment/{service} -n upi-production</pre>

<h3>Post-Rollback Actions</h3>
<ol>
  <li>Update Change Request state to "Failed" with rollback details</li>
  <li>Create an Incident if customer impact occurred</li>
  <li>Create a Problem record to investigate the deployment failure</li>
  <li>Notify #upi-platform-eng with failure analysis</li>
</ol>"""
    },

    "4f9dd7cd93e30710068e718efaba10b5": {
        "short_description": "Monitoring: Grafana Dashboard Guide for UPI Platform",
        "text": """<h2>Overview</h2>
<p>This guide describes the key Grafana dashboards used to monitor the UPI payment platform. Every NOC engineer and platform engineer should be familiar with these dashboards and know how to interpret the key panels.</p>

<h2>Dashboard 1: UPI Transaction Monitoring</h2>
<p><strong>Purpose:</strong> Real-time visibility into transaction processing health</p>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Panel</th><th>Metric</th><th>Normal Range</th><th>Alert Threshold</th></tr>
<tr>
  <td>Transactions Per Second (TPS)</td>
  <td><code>sum(rate(upi_transactions_total[1m]))</code></td>
  <td>2,000-8,000 TPS (varies by time of day)</td>
  <td>&lt; 500 TPS during business hours</td>
</tr>
<tr>
  <td>Overall Failure Rate</td>
  <td><code>sum(rate(upi_transactions_total{status="failed"}[5m])) / sum(rate(upi_transactions_total[5m])) * 100</code></td>
  <td>0.5% - 1.5%</td>
  <td>&gt; 2% for 5 minutes</td>
</tr>
<tr>
  <td>P99 Latency</td>
  <td><code>histogram_quantile(0.99, sum(rate(upi_request_duration_seconds_bucket[5m])) by (le))</code></td>
  <td>500ms - 1200ms</td>
  <td>&gt; 2000ms for 5 minutes</td>
</tr>
<tr>
  <td>Failure Rate by Error Code</td>
  <td><code>sum by (error_code) (rate(upi_transactions_total{status="failed"}[5m]))</code></td>
  <td>Varies</td>
  <td>Any single code &gt; 3%</td>
</tr>
</table>

<h2>Dashboard 2: UPI Infrastructure Health</h2>
<p><strong>Purpose:</strong> Infrastructure-level health of all UPI platform components</p>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Panel</th><th>What to Look For</th><th>Action if Abnormal</th></tr>
<tr><td>Pod Status (Kubernetes)</td><td>All pods in Running state, 1/1 Ready</td><td>Check pod events: <code>kubectl describe pod {pod_name}</code></td></tr>
<tr><td>CPU Usage by Service</td><td>&lt; 70% of request limits</td><td>If sustained &gt; 80%, consider scaling horizontally</td></tr>
<tr><td>JVM Heap Usage</td><td>40-65% after GC</td><td>If &gt; 75%, check for memory leak (see KE-UPI-007)</td></tr>
<tr><td>Database Connections</td><td>Active connections &lt; 50% of pool max</td><td>If &gt; 80%, follow RB-UPI-001</td></tr>
<tr><td>Kafka Consumer Lag</td><td>&lt; 1000 messages lag</td><td>If &gt; 5000, scale consumer group</td></tr>
<tr><td>PostgreSQL Replication Lag</td><td>&lt; 1 second</td><td>If &gt; 10 seconds, investigate replica health</td></tr>
</table>

<h2>Dashboard 3: UPI Error Rate Analysis</h2>
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
sum(rate(upi_transactions_total[5m]))
sum(rate(upi_transactions_total[5m] offset 1d))

# Average transaction amount
sum(rate(upi_transaction_amount_sum[5m])) / sum(rate(upi_transaction_amount_count[5m]))
</pre>"""
    },

    "839dd7cd93e30710068e718efaba10fd": {
        "short_description": "Runbook: UPI Settlement Reconciliation Failure",
        "text": """<h2>Document Control</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><td><strong>Runbook ID</strong></td><td>RB-UPI-003</td></tr>
<tr><td><strong>Version</strong></td><td>1.2</td></tr>
<tr><td><strong>Last Updated</strong></td><td>2024-01-14</td></tr>
<tr><td><strong>Author</strong></td><td>Amit Verma</td></tr>
<tr><td><strong>Classification</strong></td><td>Internal - Operations</td></tr>
</table>

<h2>Purpose</h2>
<p>This runbook covers the investigation and resolution of settlement reconciliation failures. Settlement reconciliation runs every 30 minutes and compares transactions processed by the UPI switch against bank-reported settlement files.</p>

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
      <li><strong>Type 1:</strong> NPCI processed, bank not reported - Transaction exists in our ledger but missing from bank file</li>
      <li><strong>Type 2:</strong> Bank reported, NPCI not processed - Transaction in bank file but not in our ledger</li>
      <li><strong>Type 3:</strong> Amount mismatch - Both sides have the transaction but amounts differ</li>
    </ul>
  </li>
</ol>

<h2>Step 2: Investigation by Mismatch Type</h2>

<h3>Type 1: Transaction Missing from Bank File</h3>
<ol>
  <li>Verify transaction status in our ledger</li>
  <li>Check if the credit instruction was successfully delivered to the bank</li>
  <li>If credit was delivered but bank did not process: Contact bank operations team via hotline</li>
</ol>

<h3>Type 2: Transaction Missing from NPCI Ledger</h3>
<ol>
  <li>This is rare and may indicate data integrity issues</li>
  <li>Check if the transaction was processed during a known outage window</li>
  <li>Search application logs for the transaction ID</li>
  <li>If transaction genuinely missing, escalate to Platform Engineering with all evidence</li>
</ol>

<h3>Type 3: Amount Mismatch</h3>
<ol>
  <li>Compare amounts in settlement_mismatches table</li>
  <li>Check for currency conversion or rounding issues</li>
  <li>Check if a reversal or refund was processed that the bank did not account for</li>
</ol>

<h2>Step 3: Resolution</h2>
<ol>
  <li>For each mismatch, create a settlement adjustment record via the settlement service API</li>
  <li>Adjustments above INR 1,00,000 require approval from the Settlement Manager</li>
  <li>All adjustments must be documented in the Change Request work notes</li>
</ol>

<h2>Escalation</h2>
<ul>
  <li>Mismatches &gt; INR 10,00,000: Escalate to Finance and Settlement Manager immediately</li>
  <li>Recurring mismatches from the same bank: Create a Problem record for root cause investigation</li>
  <li>System-wide reconciliation failure: Escalate to Platform Engineering as P2</li>
</ul>"""
    }
}

# Now update each article
print(f"Updating {len(articles)} articles with full content...")
success = 0
failed = 0

for sys_id, article_data in articles.items():
    try:
        result = api_call("PATCH", f"kb_knowledge/{sys_id}", {"text": article_data["text"]})
        print(f"  OK: {article_data['short_description']}")
        success += 1
    except Exception as e:
        print(f"  FAIL: {article_data['short_description']} - {e}")
        failed += 1

print(f"\nDone: {success} updated, {failed} failed")

# ---------------------------------------------------------
# Part 5: Publish Article 1 (UPI Error Code Reference Guide)
# ---------------------------------------------------------
print("\n--- Publishing Article 1: UPI Error Code Reference Guide ---")
try:
    result = api_call("PATCH", "kb_knowledge/7e9d97cd93e30710068e718efaba10dc", {"workflow_state": "published"})
    print(f"  State: {result.get('workflow_state', 'unknown')}")
except Exception as e:
    print(f"  Error: {e}")

# ---------------------------------------------------------
# Part 6: Create incident linked to KB for U01 timeout
# ---------------------------------------------------------
print("\n--- Part 6: Creating incident for KB integration ---")
try:
    # Get Priya Sharma's sys_id
    priya_id = "8c0643f093ef4310068e718efaba1024"

    # Get Platform Engineering group
    grp = api_call("GET", "sys_user_group?sysparm_query=name=Platform Engineering&sysparm_fields=sys_id&sysparm_limit=1")
    pe_group_id = grp[0]["sys_id"] if grp else ""

    inc_data = {
        "caller_id": priya_id,
        "category": "Software",
        "short_description": "UPI transactions failing with error code U01 timeout",
        "description": "Multiple UPI transactions are timing out with error code U01. Failure rate has increased to 4% in the last 10 minutes. Grafana shows elevated P99 latency.",
        "impact": "2",
        "urgency": "2",
        "assignment_group": pe_group_id
    }
    inc_result = api_call("POST", "incident", inc_data)
    inc_number = inc_result.get("number", "unknown")
    inc_sys_id = inc_result.get("sys_id", "")
    print(f"  Created incident: {inc_number}")

except Exception as e:
    print(f"  Error creating incident: {e}")

# ---------------------------------------------------------
# Part 7: Create Problem record for KEDB
# ---------------------------------------------------------
print("\n--- Part 7: Creating Problem record for KEDB ---")
try:
    amit_id = "cc0643f093ef4310068e718efaba1027"

    prb_data = {
        "short_description": "Recurring memory exhaustion on UPI Transaction Service",
        "description": "The UPI Transaction Service (v2.3.x) experiences a gradual memory leak that causes service degradation after approximately 7 days of uptime. Root cause traced to TransactionCorrelationService.java - orphaned correlation entries for error codes U48 and U66.",
        "category": "Software",
        "assignment_group": pe_group_id,
        "assigned_to": amit_id,
        "problem_state": "4"  # Known Error
    }
    prb_result = api_call("POST", "problem", prb_data)
    prb_number = prb_result.get("number", "unknown")
    print(f"  Created problem: {prb_number} (Known Error state)")

except Exception as e:
    print(f"  Error creating problem: {e}")

# ---------------------------------------------------------
# Clean up duplicate categories
# ---------------------------------------------------------
print("\n--- Cleaning up duplicate categories ---")
# Keep the ones with & (proper names), delete the old ones with "and"
duplicates_to_delete = [
    "07e5a4c193eb8310068e718efaba1071",  # Monitoring and Alerting (dup)
    "1ae5a4c193eb8310068e718efaba1023",  # Onboarding and Training (dup)
    "35e564c193eb8310068e718efaba10c7",  # Architecture and Design (dup)
    "61e564c193eb8310068e718efaba10c2",  # Runbooks and SOPs (dup)
    "d1e564c193eb8310068e718efaba10a1",  # UPI Error Codes and Resolution (dup)
    "eae5a4c193eb8310068e718efaba1028",  # Known Issues and Workarounds (dup)
]

for cat_id in duplicates_to_delete:
    try:
        url = f"{INSTANCE}/api/now/table/kb_category/{cat_id}"
        req = urllib.request.Request(url, method="DELETE", headers={
            "Accept": "application/json",
            "Authorization": f"Basic {AUTH}"
        })
        urllib.request.urlopen(req, context=CTX)
        print(f"  Deleted duplicate category: {cat_id}")
    except Exception as e:
        print(f"  Could not delete {cat_id}: {e}")

print("\n=== Lab 10: Knowledge Management - COMPLETE ===")
