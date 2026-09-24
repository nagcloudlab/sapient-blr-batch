# Lab 10: Knowledge Management -- Step-by-Step Quick Guide

> Companion to the full lab doc. Use this during hands-on sessions.
> For theory and background, refer to `lab-10-knowledge-management.md`

---

## Pre-check

- [ ] Labs 07-09 done (users ravi.kumar, amit.verma, priya.sharma, meera.joshi exist)
- [ ] Groups exist: Platform Engineering, NOC, Service Desk
- [ ] Logged into PDI as admin

---

## Step 1: Create the Knowledge Base

Navigate: **Knowledge > Administration > Knowledge Bases** > **New**

| Field | Value |
|-------|-------|
| Title | UPI Operations Knowledge Base |
| Owner | Ravi Kumar |
| Description | Comprehensive knowledge repository for UPI payment platform operations, troubleshooting, runbooks, and standard operating procedures. |
| Active | Checked |

In the **Managers** field, add: **Platform Engineering** group.

> Submit. Verify it appears on **Knowledge > Homepage**.

---

## Step 2: Create 7 Knowledge Categories

Open the Knowledge Base record > scroll to **Categories** related list > click **New** for each:

| # | Label | Description |
|---|-------|-------------|
| 1 | UPI Error Codes & Resolution | Reference documentation for all UPI error codes with diagnostic steps |
| 2 | Runbooks & Standard Operating Procedures | Step-by-step operational procedures for routine and emergency operations |
| 3 | Architecture & Design Documents | System architecture diagrams, design decisions, and integration specs |
| 4 | Onboarding & Training | Guides for new team members joining the UPI platform team |
| 5 | Known Issues & Workarounds | Known Error Database (KEDB) -- documented known issues with workarounds |
| 6 | Change Implementation Guides | Standard deployment procedures, rollback plans, and change execution guides |
| 7 | Monitoring & Alerting | Grafana dashboard guides, Prometheus query references, alert response procedures |

For each: set **Knowledge Base** = UPI Operations Knowledge Base (auto-populated), add **Label** and **Description**, then **Submit**.

---

## Checkpoint A

Open the Knowledge Base record > Categories related list.

Expected: **7 categories**. If any missing, go back and create them.

---

## Step 3: Create 5 Knowledge Articles

Navigate: **Knowledge > Create New** for each article.

### Article 1: UPI Error Code Reference Guide

| Field | Value |
|-------|-------|
| Knowledge Base | UPI Operations Knowledge Base |
| Category | UPI Error Codes & Resolution |
| Short description | UPI Error Code Reference Guide |
| Author | Amit Verma |
| Workflow State | Draft |

**Article body (text field):**

```html
<h2>Overview</h2>
<p>Comprehensive reference for UPI error codes. First reference when investigating transaction failures.</p>
<h2>Error Code Reference</h2>
<table border="1" cellpadding="6"><thead><tr><th>Code</th><th>Description</th><th>Severity</th><th>Resolution</th></tr></thead>
<tbody>
<tr><td><b>U01</b></td><td>Transaction Timeout</td><td>High</td><td>Check service health, connection pool; restart if needed (RB-UPI-001)</td></tr>
<tr><td><b>U09</b></td><td>Beneficiary Bank Offline</td><td>Medium</td><td>Verify bank connectivity, enable circuit breaker</td></tr>
<tr><td><b>U16</b></td><td>Risk Threshold Exceeded</td><td>Medium</td><td>Review risk score in fraud dashboard; whitelist if false positive</td></tr>
<tr><td><b>U28</b></td><td>PSP Not Registered</td><td>Low</td><td>Verify PSP registration and certificate expiry</td></tr>
<tr><td><b>U30</b></td><td>Debit Failed</td><td>High</td><td>Check bank connectivity; monitor upi_debit_failure_rate metric</td></tr>
<tr><td><b>U66</b></td><td>Device Fingerprint Mismatch</td><td>High</td><td>Verify device registry; guide user re-registration if legitimate</td></tr>
</tbody></table>
<h2>Escalation</h2>
<ul><li>P1: Any error code causing > 10% overall failure rate</li>
<li>P2: Any error code causing > 5% failure rate for 15+ minutes</li></ul>
```

> Submit.

---

### Article 2: Runbook -- UPI Transaction Service Restart Procedure

| Field | Value |
|-------|-------|
| Knowledge Base | UPI Operations Knowledge Base |
| Category | Runbooks & Standard Operating Procedures |
| Short description | Runbook: UPI Transaction Service Restart Procedure |
| Author | Ravi Kumar |
| Workflow State | Draft |

**Article body:**

```html
<h2>Document Control</h2>
<p>Runbook ID: RB-UPI-001 | Version: 2.1 | Author: Ravi Kumar</p>
<h2>When to Use</h2>
<ul><li>Connection pool utilization > 90% for 10+ min</li>
<li>Heap memory > 85% not recovering after GC</li>
<li>U01 timeout rate > 5% for 15+ min</li></ul>
<h2>Pre-Restart Checks</h2>
<ol><li>Verify TPS: <code>curl -s http://upi-txn-service:8080/metrics</code></li>
<li>Check in-flight count (wait until < 100)</li>
<li>Confirm at least 3 of 4 instances healthy</li>
<li>Notify #upi-noc-alerts</li></ol>
<h2>Restart (Kubernetes)</h2>
<pre>kubectl rollout restart deployment/upi-txn-service -n upi-production</pre>
<h2>Post-Restart Validation</h2>
<ol><li>Health check returns UP</li><li>Connection pool < 20% max</li>
<li>Error rate returns to baseline within 5 min</li></ol>
```

> Submit.

---

### Article 3: Troubleshooting -- High Transaction Failure Rate

| Field | Value |
|-------|-------|
| Knowledge Base | UPI Operations Knowledge Base |
| Category | Known Issues & Workarounds |
| Short description | Troubleshooting: High Transaction Failure Rate |
| Author | Priya Sharma |
| Workflow State | Draft |

**Article body:**

```html
<h2>Overview</h2>
<p>Guide for NOC engineers to diagnose elevated transaction failure rates (above 2% for 5+ min).</p>
<h2>Step 1: Assess</h2>
<p>Open Grafana > UPI Transaction Monitoring. Check overall failure rate, failure by error code, failure by bank.</p>
<h2>Step 2: Identify Root Cause</h2>
<ul><li><b>U01 dominant:</b> Check connection pool; follow RB-UPI-001</li>
<li><b>U09 dominant:</b> Check bank connectivity; enable circuit breaker</li>
<li><b>U30 dominant:</b> Check UPI debit service; verify Kafka consumer lag</li>
<li><b>Multiple codes:</b> Infrastructure issue -- check K8s nodes, shared dependencies</li></ul>
<h2>Escalation</h2>
<p>Failure > 10% for 5 min: Declare P1. Failure > 5% for 15 min: Escalate to Platform Engineering.</p>
```

> Submit.

---

### Article 4: Architecture -- UPI Payment Processing Flow

| Field | Value |
|-------|-------|
| Knowledge Base | UPI Operations Knowledge Base |
| Category | Architecture & Design Documents |
| Short description | Architecture: UPI Payment Processing Flow |
| Author | Ravi Kumar |
| Workflow State | Draft |

**Article body:**

```html
<h2>Overview</h2>
<p>End-to-end flow of a UPI payment transaction through the NPCI platform.</p>
<h2>Transaction Flow</h2>
<p>Payer Mobile App -> Payer PSP -> NPCI UPI Switch -> Payee PSP -> Payee Bank</p>
<h2>Key Components</h2>
<table border="1" cellpadding="6"><tr><th>Component</th><th>Technology</th></tr>
<tr><td>UPI Gateway Service</td><td>Java 17, Spring Boot 3.x</td></tr>
<tr><td>UPI Transaction Service</td><td>Java 17, Spring Boot 3.x</td></tr>
<tr><td>UPI Risk Engine</td><td>Python 3.11, FastAPI</td></tr>
<tr><td>UPI Settlement Service</td><td>Java 17, Spring Batch</td></tr>
<tr><td>PostgreSQL Cluster</td><td>PostgreSQL 15, Patroni</td></tr></table>
<h2>Performance Targets</h2>
<ul><li>TPS: 10,000 peak</li><li>P99 Latency: < 2 seconds</li>
<li>Availability: 99.95%</li></ul>
```

> Submit.

---

### Article 5: Known Error -- Memory Leak in UPI Transaction Service v2.3

| Field | Value |
|-------|-------|
| Knowledge Base | UPI Operations Knowledge Base |
| Category | Known Issues & Workarounds |
| Short description | Known Error: Memory Leak in UPI Transaction Service v2.3 |
| Author | Amit Verma |
| Workflow State | Draft |

**Article body:**

```html
<h2>Known Error Record</h2>
<p>KEDB ID: KE-UPI-007 | Related Problem: PRB0042156 | Affected CI: upi-txn-service v2.3.x | Status: Workaround Available</p>
<h2>Symptoms</h2>
<ul><li>JVM heap memory increases steadily over 7-10 days</li>
<li>GC pause times increase from ~50ms to >500ms</li>
<li>P99 latency degrades from 800ms to >3000ms after ~10 days uptime</li>
<li>Eventually OutOfMemoryError crashes the service</li></ul>
<h2>Root Cause</h2>
<p>Memory leak in TransactionCorrelationService.java -- orphaned correlation entries not cleaned up for error codes U48 and U66. Bug introduced in v2.3.0 refactor.</p>
<h2>Workaround</h2>
<p>Scheduled rolling restart every 5 days during 02:00-04:00 IST. Follow Runbook RB-UPI-001.</p>
<h2>Permanent Fix</h2>
<p>Fix branch: fix/txn-correlation-cache-cleanup. Target release: v2.4.0.</p>
```

> Submit.

---

## Checkpoint B

Navigate: **Knowledge > Articles > All** > filter by **Knowledge Base = UPI Operations Knowledge Base**

Expected: **5 articles**, all in **Draft** state.

---

## Step 4: Publish Articles

For each of the 5 articles, open the article and change **Workflow State** from **Draft** to **Published**.

> If approval workflow is enabled, click **Submit for Review** instead, then impersonate **Ravi Kumar** > **Self-Service > My Approvals** > **Approve** each article.

After publishing, verify:
1. Navigate to **Knowledge > Homepage**
2. Click into "UPI Operations Knowledge Base"
3. Confirm all 5 articles appear and are accessible

---

## Step 5: Test -- KB Integration with Incidents

### 5.1: Create an Incident

Navigate: **Incident > Create New**

| Field | Value |
|-------|-------|
| Caller | Priya Sharma |
| Category | Software |
| Short description | UPI transactions failing with error code U01 timeout |
| Description | Multiple UPI transactions are timing out with error code U01. Failure rate has increased to 4% in the last 10 minutes. |
| Impact | 2 - Medium |
| Urgency | 2 - Medium |
| Assignment group | Platform Engineering |

### 5.2: Verify KB Suggestions

Before submitting, look at the right side of the form or the **Knowledge** section.

Expected suggestions:
- "UPI Error Code Reference Guide" (matches "error code U01")
- "Troubleshooting: High Transaction Failure Rate" (matches "failing", "failure rate")

Click on a suggested article to view it inline.

### 5.3: Submit and Attach

1. Submit the incident
2. Reopen it > scroll to the **Knowledge** tab
3. Click **Search Knowledge** > search for "UPI Transaction Service Restart"
4. Attach the article to the incident

---

## Step 6: Verify KB Structure

Navigate: **Knowledge > Administration > Knowledge Bases** > open "UPI Operations Knowledge Base"

Verify:
- [ ] Knowledge Base record exists with Owner = Ravi Kumar
- [ ] 7 categories listed in the Categories related list
- [ ] 5 articles exist (filter on **Knowledge > Articles > All**)
- [ ] At least 1 article in **Published** state
- [ ] Incident shows KB suggestions when short description contains UPI keywords
- [ ] At least 1 article attached to an incident

---

## Quick Verification Checklist

- [ ] 1 Knowledge Base created (UPI Operations Knowledge Base)
- [ ] 7 categories created across the KB
- [ ] 5 articles created with realistic UPI content
- [ ] Articles published (workflow_state = published)
- [ ] Incident created and KB article suggested
- [ ] KB article attached to incident
- [ ] KB Homepage shows published articles

---

## Shortcut: Background Script

If running behind, go to **System Definition > Scripts - Background** and run the script from Appendix A in `lab-10-knowledge-management.md`. Creates 1 KB + 7 categories + 10 articles in ~1 minute.

---

*For detailed ITIL theory, full article HTML content, KEDB workflow, exercises, and background script code, see the full lab doc.*
