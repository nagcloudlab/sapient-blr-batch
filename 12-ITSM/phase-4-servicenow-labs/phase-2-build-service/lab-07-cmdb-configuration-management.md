# Lab 07: CMDB & Configuration Management

**Level:** Intermediate | **Duration:** 90 min | **Prerequisites:** Labs 01-06 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand ITIL 4 Configuration Management practice and the CI lifecycle
- Navigate the ServiceNow CMDB architecture, including CI class hierarchy and relationship types
- Create 12 Configuration Items representing every component of the NPCI UPI Payment Platform
- Build a complete relationship map connecting all CIs with dependency, hosting, and containment relationships
- Visualize the UPI service topology using ServiceNow Service Maps
- Manage CI lifecycle states and understand operational vs. install status
- Assess CMDB health, detect orphan CIs, and apply governance best practices
- Automate CI creation using Background Scripts (GlideRecord)

---

## Scenario

NPCI's UPI Payment Platform processes over 10 billion transactions per month. Before the Platform Engineering team can manage incidents, problems, or changes effectively, every component of the UPI infrastructure must be registered in the CMDB with accurate relationships.

Today, you will build the **complete configuration model** for the UPI Payment Platform:

```
                        UPI Payment Platform (Business Application)
                                       │
                 ┌─────────────────────┼─────────────────────┐
                 │                     │                     │
          UPI Production LB     Monitoring Stack       Databases
          (Load Balancer)             │                     │
           ┌─────┴─────┐      ┌──────┼──────┐       ┌──────┴──────┐
           │           │      │      │      │       │             │
    UPI Txn Svc   UPI Stl Svc  Prom  Graf  Snow   PG Primary  PG Replica
    (port 8081)   (port 8082)                     (port 5432)
        │             │
   App Server 01  App Server 02                  DB Server 01
   (16GB/8CPU)    (16GB/8CPU)                    (64GB/16CPU)
```

Without this configuration model, the NOC team (Priya Sharma) cannot see what depends on what during an outage. The Platform Engineering team (Ravi Kumar, Amit Verma) cannot assess change impact. And Service Level Management has no way to map SLAs to infrastructure components.

---

## Part 1: ITIL 4 Configuration Management Theory

Before touching ServiceNow, you must understand the ITIL 4 foundations that drive every decision in CMDB design.

### 1.1 Practice Definition

**Service Configuration Management** is one of ITIL 4's 34 management practices. Its purpose is to ensure that accurate and reliable information about the configuration of services, and the CIs that support them, is available when and where it is needed.

Key outcomes:
- Every service component is **identified** and **registered**
- Relationships between components are **mapped**
- Changes to configurations are **controlled**
- Configuration data is **accurate** and **trusted**

### 1.2 The CI Lifecycle

Configuration Items go through four stages of management:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  1. IDENTIFICA-  │────►│   2. CONTROL     │────►│  3. STATUS       │────►│  4. VERIFICATION │
│     TION         │     │                  │     │     ACCOUNTING   │     │     & AUDIT      │
├──────────────────┤     ├──────────────────┤     ├──────────────────┤     ├──────────────────┤
│ What CIs exist?  │     │ Who can change   │     │ What is the      │     │ Is the CMDB      │
│ What attributes  │     │ CI data?         │     │ current state    │     │ accurate?        │
│ matter?          │     │ What approval    │     │ of each CI?      │     │ Does it match    │
│ What relation-   │     │ is needed?       │     │ What changed     │     │ reality?         │
│ ships exist?     │     │ What is the      │     │ and when?        │     │ Are there orphan │
│                  │     │ change process?  │     │                  │     │ or duplicate CIs?│
└──────────────────┘     └──────────────────┘     └──────────────────┘     └──────────────────┘
```

**For UPI context:**
1. **Identification:** We identify 12 CIs — 2 app servers, 2 databases, 1 load balancer, 3 physical servers, 3 monitoring tools, and 1 business application
2. **Control:** Only Platform Engineering (Ravi Kumar, Amit Verma) and IT Admin (Vijay Admin) can modify CI records
3. **Status Accounting:** Each CI has an operational status (Operational, In Maintenance, Retired) that reflects its current state
4. **Verification & Audit:** We will use CMDB Health Dashboard and relationship audits to ensure accuracy

### 1.3 Configuration Model vs. Configuration Record

| Concept | Definition | UPI Example |
|---|---|---|
| **Configuration Record** | A single CI entry in the CMDB | "UPI Transaction Service" — one record with name, IP, port, owner |
| **Configuration Model** | The complete set of CIs and their relationships that describe a service | All 12 CIs + all relationships together form the UPI Payment Platform configuration model |
| **Configuration Baseline** | A snapshot of the configuration model at a point in time | The state of all UPI CIs before a major release deployment |

### 1.4 CMDB vs. CMS

```
┌──────────────────────────────────────────────────────────┐
│                  CMS (Configuration Management System)    │
│                                                           │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────────┐ │
│   │  CMDB   │  │ Asset   │  │ License │  │ Discovery │ │
│   │         │  │ Mgmt DB │  │ Mgmt DB │  │ Data      │ │
│   └─────────┘  └─────────┘  └─────────┘  └───────────┘ │
│                                                           │
│   + Knowledge Base + Monitoring Data + Vendor Data        │
└──────────────────────────────────────────────────────────┘
```

- **CMDB** = a single database of CIs and relationships
- **CMS** = the entire ecosystem of tools, data sources, and processes that feed and consume configuration data
- In ServiceNow, the CMDB is the core, but the CMS includes Discovery, Service Mapping, Asset Management, and integrations with external tools (like our Prometheus/Grafana stack)

### 1.5 How CMDB Supports Other ITIL Practices

| Practice | How CMDB Helps | UPI Example |
|---|---|---|
| **Incident Management** | Attach affected CI to incident; see CI's relationships to understand blast radius | Incident on "UPI PostgreSQL Primary" — CMDB shows both Transaction and Settlement services depend on it |
| **Problem Management** | Trace root cause through CI dependency chains | Recurring timeouts in Transaction Service traced to DB connection pool on PostgreSQL Primary |
| **Change Management** | Impact analysis before approving a change | Change to upgrade PostgreSQL — CMDB shows 2 app services, 1 replica, and the entire Payment Platform are impacted |
| **Service Level Management** | Map SLAs to specific CIs and services | P1 SLA (1hr resolve) attached to "UPI Payment Platform" business application |
| **Event Management** | Correlate alerts to CIs for automated incident creation | Prometheus alert for high CPU on upi-txn-01.npci.org.in → maps to "UPI Transaction Service" CI |

---

## Part 2: Understanding ServiceNow CMDB Architecture

### 2.1 The Base CI Table: cmdb_ci

Every Configuration Item in ServiceNow lives in the `cmdb_ci` table or one of its child tables. This is the root of the CI class hierarchy.

Key fields on `cmdb_ci`:

| Field | Column Name | Description |
|---|---|---|
| Name | `name` | Display name of the CI |
| Class | `sys_class_name` | Which child table this CI belongs to |
| Asset tag | `asset_tag` | Unique asset identifier |
| Serial number | `serial_number` | Hardware serial number |
| IP Address | `ip_address` | Network address |
| Operational status | `operational_status` | 1=Operational, 2=Non-Operational, 5=In Maintenance, 6=Retired |
| Install status | `install_status` | 1=Installed, 2=In Maintenance, 3=On Order, 7=Retired |
| Support group | `support_group` | Group responsible for this CI |
| Assigned to | `assigned_to` | Individual responsible |
| Managed by | `managed_by` | Manager of the CI |
| Owned by | `owned_by` | Business owner |
| Department | `department` | Owning department |
| Location | `location` | Physical location |
| Environment | `environment` | Development, Test, Staging, Production |

### 2.2 CI Class Hierarchy

ServiceNow uses table inheritance. Every CI class extends `cmdb_ci`:

```
cmdb_ci (Base Configuration Item)
├── cmdb_ci_business_app          ← "UPI Payment Platform"
├── cmdb_ci_service               ← Business/Technical Services
├── cmdb_ci_appl                  ← Applications (Prometheus, Grafana, Snow Bridge)
├── cmdb_ci_server                ← Physical/Virtual Servers
│   ├── cmdb_ci_linux_server      ← Linux-specific servers
│   └── cmdb_ci_win_server        ← Windows-specific servers
├── cmdb_ci_app_server            ← Application Servers (Tomcat, JBoss, Spring Boot)
│   └── cmdb_ci_app_server_java   ← Java-specific app servers
├── cmdb_ci_db_instance           ← Database Instances (PostgreSQL, MySQL, Oracle)
├── cmdb_ci_lb                    ← Load Balancers (F5, HAProxy, Nginx)
├── cmdb_ci_network_gear          ← Switches, Routers
└── cmdb_ci_storage_device        ← SAN, NAS
```

**Why this matters for UPI:** Each CI class has specialized fields. A `cmdb_ci_db_instance` has fields for database type, port, and version that a generic `cmdb_ci` does not. By choosing the right class, you get the right fields automatically.

### 2.3 CI Classes Used in This Lab

| CI Class | Table Name | UPI Component | Count |
|---|---|---|---|
| Business Application | `cmdb_ci_business_app` | UPI Payment Platform | 1 |
| Application Server | `cmdb_ci_app_server` | UPI Transaction Service, UPI Settlement Service | 2 |
| Database Instance | `cmdb_ci_db_instance` | PostgreSQL Primary, PostgreSQL Replica | 2 |
| Load Balancer | `cmdb_ci_lb` | UPI Production LB | 1 |
| Server | `cmdb_ci_server` | App Server 01, App Server 02, DB Server 01 | 3 |
| Application | `cmdb_ci_appl` | Prometheus, Grafana, Snow Bridge | 3 |
| **Total** | | | **12** |

### 2.4 Relationship Types

CI relationships in ServiceNow use the `cmdb_rel_ci` table. Each relationship has a **type** defined in `cmdb_rel_type`:

| Relationship Type | Parent Label | Child Label | Use Case |
|---|---|---|---|
| `Depends on::Used by` | Depends on | Used by | Service A depends on Database B |
| `Runs on::Runs` | Runs on | Runs | Application runs on Server |
| `Contains::Contained by` | Contains | Contained by | Business App contains Technical Services |
| `Monitors::Monitored by` | Monitors | Monitored by | Prometheus monitors App Server |
| `Cluster of::Cluster` | Cluster of | Cluster | DB Primary clusters with DB Replica |
| `Sends data to::Receives data from` | Sends data to | Receives data from | App sends logs to monitoring |

### 2.5 Discovery vs. Manual Population

| Method | Description | When to Use |
|---|---|---|
| **Manual** | Create CIs by hand through the UI | Lab environments, small deployments, business-level CIs |
| **Discovery** | ServiceNow Discovery scans your network and auto-populates CIs | Production environments with hundreds/thousands of servers |
| **Service Mapping** | Maps application dependencies automatically | Complex microservice architectures |
| **Integration/Import** | Import from CSV, LDAP, or API (e.g., Prometheus service discovery) | When data exists in another system |
| **Background Script** | Programmatic creation using GlideRecord | Bulk setup, lab environments, migration |

In this lab, we will use **manual creation** (Parts 3-4) and provide a **Background Script** (Appendix) for automated creation.

### 2.6 CI Lifecycle States

ServiceNow tracks CI state with two fields:

**Install Status** (`install_status`):
```
On Order (3) ──► Received (6) ──► In Stock (4) ──► Installed (1) ──► In Maintenance (2) ──► Retired (7)
```

**Operational Status** (`operational_status`):
```
Operational (1) ◄──► Non-Operational (2)
       │                      │
       ▼                      ▼
In Maintenance (5) ──► Retired (6)
```

For this lab, all CIs will start with `Install Status = Installed` and `Operational Status = Operational`.

---

## Part 3: Create Configuration Items

We will now create all 12 CIs for the UPI Payment Platform. Follow each step precisely.

### 3.1 Create Business Application: "UPI Payment Platform"

This is the top-level CI that represents the entire UPI service.

1. In the Filter Navigator, type **`cmdb_ci_business_app.list`** and press Enter
2. Click **New** to create a new record
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | UPI Payment Platform |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | NPCI Unified Payments Interface — core payment processing platform handling 10B+ transactions/month |
   | Managed by | Ravi Kumar |
   | Owned by | Sanjay Manager |
   | Support group | Platform Engineering |
   | Environment | Production |
   | Description | The UPI Payment Platform is NPCI's flagship digital payment infrastructure. It consists of a Transaction Service (real-time payment processing), Settlement Service (batch settlement with member banks), PostgreSQL databases (primary + replica), a production load balancer, and a comprehensive monitoring stack (Prometheus, Grafana, AlertManager, Snow Bridge). This business application represents the end-to-end service as seen by NPCI management and regulators. |

4. Click **Submit**
5. Note: The system auto-generates a `sys_id`. Record the name for relationship creation later.

> **Why a Business Application?** In ITIL 4, a "service" is what the customer consumes. The Business Application CI represents the service boundary — everything inside it (app servers, databases, LBs, monitoring) are technical CIs that support this business capability.

### 3.2 Create Application Server: "UPI Transaction Service"

This is the core Spring Boot microservice that processes real-time UPI payments.

1. In the Filter Navigator, type **`cmdb_ci_app_server.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | UPI Transaction Service |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Spring Boot microservice for real-time UPI payment processing (port 8081) |
   | Host name | upi-txn-01.npci.org.in |
   | IP Address | 10.100.1.11 |
   | TCP port | 8081 |
   | Running process | java -jar upi-transaction-service.jar |
   | Running process key | upi-transaction-service |
   | Version | 3.2.1 |
   | Managed by | Ravi Kumar |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Ravi Kumar |
   | Environment | Production |
   | Description | The UPI Transaction Service is the primary payment processing engine. It receives payment initiation requests from PSP (Payment Service Provider) banks, validates them against NPCI rules, routes them to the beneficiary bank, and returns the response. Built on Spring Boot 3.2.1 with Java 21. Exposes REST APIs on port 8081. Metrics endpoint: /actuator/prometheus. Health endpoint: /actuator/health. Handles approximately 4,000 TPS during peak hours. |

4. Click **Submit**
5. Record: CI created — "UPI Transaction Service"

### 3.3 Create Application Server: "UPI Settlement Service"

1. In the Filter Navigator, type **`cmdb_ci_app_server.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | UPI Settlement Service |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Spring Boot microservice for UPI settlement and reconciliation (port 8082) |
   | Host name | upi-stl-01.npci.org.in |
   | IP Address | 10.100.1.12 |
   | TCP port | 8082 |
   | Running process | java -jar upi-settlement-service.jar |
   | Running process key | upi-settlement-service |
   | Version | 3.2.1 |
   | Managed by | Amit Verma |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Amit Verma |
   | Environment | Production |
   | Description | The UPI Settlement Service handles end-of-day settlement between member banks. It processes batch settlement files, calculates net positions for each bank, and generates settlement instructions for RBI (Reserve Bank of India) RTGS. Runs on Spring Boot 3.2.1 with Java 21. Settlement windows: 8:00 AM, 12:00 PM, 4:00 PM, 8:00 PM, 12:00 AM. Metrics endpoint: /actuator/prometheus. Port 8082. |

4. Click **Submit**

### 3.4 Create Database Instance: "UPI PostgreSQL Primary"

1. In the Filter Navigator, type **`cmdb_ci_db_instance.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | UPI PostgreSQL Primary |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Primary PostgreSQL 16 database for UPI transaction and settlement data |
   | Host name | upi-db-01.npci.org.in |
   | IP Address | 10.100.2.11 |
   | TCP port | 5432 |
   | Type | PostgreSQL |
   | Version | 16.2 |
   | Database name | upi_production |
   | Managed by | Amit Verma |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Amit Verma |
   | Environment | Production |
   | Description | Primary PostgreSQL 16.2 database instance hosting the UPI production database. Contains transaction records, settlement batches, member bank configurations, and UPI ID mappings. Configured with streaming replication to upi-db-02.npci.org.in. WAL archiving enabled. Connection pool: max 500 connections via PgBouncer. Storage: 2TB NVMe SSD with RAID 10. Backup schedule: full daily at 02:00 IST, WAL continuous archiving. RPO: 0 (synchronous replication). RTO: 15 minutes. |

4. Click **Submit**

### 3.5 Create Database Instance: "UPI PostgreSQL Replica"

1. In the Filter Navigator, type **`cmdb_ci_db_instance.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | UPI PostgreSQL Replica |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Read replica of UPI PostgreSQL Primary for reporting and failover |
   | Host name | upi-db-02.npci.org.in |
   | IP Address | 10.100.2.12 |
   | TCP port | 5432 |
   | Type | PostgreSQL |
   | Version | 16.2 |
   | Database name | upi_production |
   | Managed by | Amit Verma |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Amit Verma |
   | Environment | Production |
   | Description | Synchronous streaming replica of UPI PostgreSQL Primary (upi-db-01.npci.org.in). Used for read-only reporting queries, settlement reconciliation reports, and as a hot standby for automatic failover. Patroni manages the failover cluster. Replication lag threshold: < 100ms. If primary fails, this replica is promoted automatically within 30 seconds. Read-only connection string used by Settlement Service for report generation. |

4. Click **Submit**

### 3.6 Create Load Balancer: "UPI Production LB"

1. In the Filter Navigator, type **`cmdb_ci_lb.list`** and press Enter

   > **Note:** If `cmdb_ci_lb` does not appear in your PDI, navigate to **Configuration > Load Balancers** in the filter navigator. Alternatively, type `cmdb_ci_lb.list` directly in the URL.

2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | UPI Production LB |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | HAProxy load balancer distributing UPI API traffic across application servers |
   | Host name | upi-lb-01.npci.org.in |
   | IP Address | 10.100.0.10 |
   | Managed by | Ravi Kumar |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Ravi Kumar |
   | Environment | Production |
   | Description | HAProxy 2.8 LTS load balancer serving as the entry point for all UPI API traffic. Configured with round-robin distribution across UPI Transaction Service instances. SSL termination at LB level using NPCI wildcard certificate. Health check: HTTP GET /actuator/health every 5 seconds. Max connections: 50,000 concurrent. Rate limiting: 10,000 req/sec per PSP bank. Frontend ports: 443 (HTTPS), 80 (HTTP redirect). Backend: 10.100.1.11:8081, 10.100.1.12:8082. Stats page: port 8404. |

4. Click **Submit**

### 3.7 Create Server: "UPI App Server 01"

1. In the Filter Navigator, type **`cmdb_ci_server.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | UPI App Server 01 |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Linux application server hosting UPI Transaction Service |
   | Host name | upi-app-01.npci.org.in |
   | IP Address | 10.100.1.11 |
   | OS | Linux |
   | OS Version | Ubuntu 22.04 LTS |
   | RAM (MB) | 16384 |
   | CPU count | 8 |
   | CPU type | Intel Xeon E5-2686 v4 |
   | Disk space (GB) | 500 |
   | Serial number | NPCI-APP-SRV-001 |
   | Asset tag | NPCI-A001 |
   | Managed by | Ravi Kumar |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Ravi Kumar |
   | Environment | Production |
   | Description | Physical server in NPCI Mumbai Data Center, Rack B12, Unit 15. Hosts the UPI Transaction Service (Spring Boot on port 8081). Specifications: 16GB DDR4 ECC RAM, 8-core Intel Xeon E5-2686 v4 @ 2.3GHz, 500GB NVMe SSD. Network: dual 10GbE bonded interfaces. Monitoring agent: Prometheus node_exporter on port 9100. Hardened per NPCI security baseline v4.2. Last patched: 2024-12-15. |

4. Click **Submit**

### 3.8 Create Server: "UPI App Server 02"

1. In the Filter Navigator, type **`cmdb_ci_server.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | UPI App Server 02 |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Linux application server hosting UPI Settlement Service |
   | Host name | upi-app-02.npci.org.in |
   | IP Address | 10.100.1.12 |
   | OS | Linux |
   | OS Version | Ubuntu 22.04 LTS |
   | RAM (MB) | 16384 |
   | CPU count | 8 |
   | CPU type | Intel Xeon E5-2686 v4 |
   | Disk space (GB) | 500 |
   | Serial number | NPCI-APP-SRV-002 |
   | Asset tag | NPCI-A002 |
   | Managed by | Amit Verma |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Amit Verma |
   | Environment | Production |
   | Description | Physical server in NPCI Mumbai Data Center, Rack B12, Unit 16. Hosts the UPI Settlement Service (Spring Boot on port 8082). Specifications: 16GB DDR4 ECC RAM, 8-core Intel Xeon E5-2686 v4 @ 2.3GHz, 500GB NVMe SSD. Network: dual 10GbE bonded interfaces. Monitoring agent: Prometheus node_exporter on port 9100. Hardened per NPCI security baseline v4.2. Last patched: 2024-12-15. |

4. Click **Submit**

### 3.9 Create Server: "UPI DB Server 01"

1. In the Filter Navigator, type **`cmdb_ci_server.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | UPI DB Server 01 |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | High-performance Linux database server hosting PostgreSQL primary and replica |
   | Host name | upi-db-srv-01.npci.org.in |
   | IP Address | 10.100.2.10 |
   | OS | Linux |
   | OS Version | Ubuntu 22.04 LTS |
   | RAM (MB) | 65536 |
   | CPU count | 16 |
   | CPU type | Intel Xeon Gold 6248R |
   | Disk space (GB) | 4000 |
   | Serial number | NPCI-DB-SRV-001 |
   | Asset tag | NPCI-D001 |
   | Managed by | Amit Verma |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Amit Verma |
   | Environment | Production |
   | Description | High-performance database server in NPCI Mumbai Data Center, Rack C08, Unit 1-4 (4U chassis). Hosts both PostgreSQL Primary and Replica instances. Specifications: 64GB DDR4 ECC RAM, 16-core Intel Xeon Gold 6248R @ 3.0GHz, 4TB NVMe SSD in RAID 10 (2TB usable). Dedicated 25GbE network for replication traffic. Battery-backed write cache. UPS-protected with 30-minute battery runtime. Monitoring: node_exporter (9100), postgres_exporter (9187). |

4. Click **Submit**

### 3.10 Create Application: "Prometheus Monitoring"

1. In the Filter Navigator, type **`cmdb_ci_appl.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | Prometheus Monitoring |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Prometheus 2.48 time-series database collecting metrics from all UPI components |
   | Host name | upi-mon-01.npci.org.in |
   | IP Address | 10.100.3.11 |
   | Version | 2.48.1 |
   | Managed by | Ravi Kumar |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Ravi Kumar |
   | Environment | Production |
   | Description | Prometheus 2.48.1 instance responsible for scraping metrics from all UPI platform components. Scrape targets: UPI Transaction Service (/actuator/prometheus on 8081), UPI Settlement Service (/actuator/prometheus on 8082), node_exporter on all servers (9100), postgres_exporter (9187), HAProxy stats (8404). Scrape interval: 15 seconds. Retention: 30 days. Alert rules configured for: high error rate (>1%), high latency (p95 >500ms), service down, disk usage >80%, CPU >90%. AlertManager endpoint: upi-mon-01.npci.org.in:9093. Web UI: port 9090. |

4. Click **Submit**

### 3.11 Create Application: "Grafana Dashboard"

1. In the Filter Navigator, type **`cmdb_ci_appl.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | Grafana Dashboard |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Grafana 10.2 visualization platform for UPI operational dashboards |
   | Host name | upi-mon-01.npci.org.in |
   | IP Address | 10.100.3.11 |
   | Version | 10.2.3 |
   | Managed by | Ravi Kumar |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Priya Sharma |
   | Environment | Production |
   | Description | Grafana 10.2.3 instance providing operational dashboards for the UPI platform. Dashboards: UPI Transaction Overview (TPS, latency, error rate), UPI Settlement Status (batch progress, bank positions), Infrastructure Health (CPU, memory, disk, network), Database Performance (connections, query time, replication lag), Alert History. Data source: Prometheus on localhost:9090. Authentication: LDAP integrated with NPCI Active Directory. NOC team (Priya Sharma) uses this as the primary monitoring interface. Port 3000. |

4. Click **Submit**

### 3.12 Create Application: "Snow Bridge Integration"

1. In the Filter Navigator, type **`cmdb_ci_appl.list`** and press Enter
2. Click **New**
3. Fill in the form:

   | Field | Value |
   |---|---|
   | Name | Snow Bridge Integration |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Custom integration service bridging Prometheus AlertManager alerts to ServiceNow incidents |
   | Host name | upi-mon-01.npci.org.in |
   | IP Address | 10.100.3.11 |
   | Version | 1.0.0 |
   | Managed by | Ravi Kumar |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |
   | Assigned to | Ravi Kumar |
   | Environment | Production |
   | Description | Snow Bridge is a custom Python service that receives webhook alerts from Prometheus AlertManager and creates corresponding incidents in ServiceNow via the REST API (Table API). It maps alert labels to ServiceNow fields: alertname → short_description, severity → impact/urgency, instance → cmdb_ci (CI lookup by hostname). Runs on port 5001. Supports alert grouping, deduplication, and auto-resolution when alerts clear. Configuration: /etc/snow-bridge/config.yaml. Logs: /var/log/snow-bridge/. Retry policy: 3 attempts with exponential backoff. |

4. Click **Submit**

### 3.13 Verify All CIs Created

Before proceeding to relationships, verify that all 12 CIs exist.

1. In the Filter Navigator, type **`cmdb_ci.list`** and press Enter
2. Set the filter:
   - Click the filter icon (funnel)
   - Set: **Support group → is → Platform Engineering**
   - Click **Run**
3. You should see all 12 CIs in the list

Alternatively, verify by class:

| Navigation | Expected CIs |
|---|---|
| Type `cmdb_ci_business_app.list` | UPI Payment Platform |
| Type `cmdb_ci_app_server.list` | UPI Transaction Service, UPI Settlement Service |
| Type `cmdb_ci_db_instance.list` | UPI PostgreSQL Primary, UPI PostgreSQL Replica |
| Type `cmdb_ci_lb.list` | UPI Production LB |
| Type `cmdb_ci_server.list` | UPI App Server 01, UPI App Server 02, UPI DB Server 01 |
| Type `cmdb_ci_appl.list` | Prometheus Monitoring, Grafana Dashboard, Snow Bridge Integration |

> **Checkpoint:** If you are missing any CIs, go back and create them before proceeding. The relationship step depends on all 12 CIs existing.

---

## Part 4: Create CI Relationships

Relationships are what transform a flat list of CIs into a **configuration model**. Without relationships, the CMDB is just an inventory list. With relationships, it becomes a map that shows impact, dependencies, and service topology.

### 4.1 Understanding How to Create Relationships

There are two ways to create relationships in ServiceNow:

**Method A: From the CI Record (Related Items tab)**
1. Open a CI record
2. Scroll down to the **Related Items** section (or click the "Related Items" tab)
3. Look for the **CI Relationships** related list
4. Click **New** in the CI Relationships related list

**Method B: Directly in the Relationship Table**
1. Navigate to **`cmdb_rel_ci.list`** in the filter navigator
2. Click **New**
3. Fill in Parent, Type, and Child

We will use **Method A** for most relationships as it provides better context.

### 4.2 Relationship: UPI Transaction Service → Depends on → UPI PostgreSQL Primary

This is the most critical dependency — if the database goes down, the Transaction Service cannot process payments.

1. In the Filter Navigator, type **`cmdb_ci_app_server.list`** and press Enter
2. Click on **UPI Transaction Service** to open the record
3. Scroll down to the **Related Items** section
4. In the **CI Relationships** related list, click **New**
5. Fill in the relationship form:

   | Field | Value |
   |---|---|
   | Parent | UPI Transaction Service |
   | Type | Depends on::Used by |
   | Child | UPI PostgreSQL Primary |

   > **Reading this relationship:** "UPI Transaction Service **depends on** UPI PostgreSQL Primary." Conversely, "UPI PostgreSQL Primary **is used by** UPI Transaction Service."

6. Click **Submit**
7. You are returned to the UPI Transaction Service record. In the CI Relationships list, you should now see the relationship.

### 4.3 Relationship: UPI Transaction Service → Runs on → UPI App Server 01

1. Still on the **UPI Transaction Service** record (or navigate back to it)
2. In the **CI Relationships** related list, click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Parent | UPI Transaction Service |
   | Type | Runs on::Runs |
   | Child | UPI App Server 01 |

4. Click **Submit**

### 4.4 Relationship: UPI Settlement Service → Depends on → UPI PostgreSQL Primary

1. Navigate to **`cmdb_ci_app_server.list`**
2. Click on **UPI Settlement Service**
3. In **CI Relationships**, click **New**
4. Fill in:

   | Field | Value |
   |---|---|
   | Parent | UPI Settlement Service |
   | Type | Depends on::Used by |
   | Child | UPI PostgreSQL Primary |

5. Click **Submit**

### 4.5 Relationship: UPI Settlement Service → Runs on → UPI App Server 02

1. Still on **UPI Settlement Service**
2. In **CI Relationships**, click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Parent | UPI Settlement Service |
   | Type | Runs on::Runs |
   | Child | UPI App Server 02 |

4. Click **Submit**

### 4.6 Relationship: UPI Production LB → Depends on → UPI Transaction Service

1. Navigate to **`cmdb_ci_lb.list`**
2. Click on **UPI Production LB**
3. In **CI Relationships**, click **New**
4. Fill in:

   | Field | Value |
   |---|---|
   | Parent | UPI Production LB |
   | Type | Depends on::Used by |
   | Child | UPI Transaction Service |

5. Click **Submit**

### 4.7 Relationship: UPI Production LB → Depends on → UPI Settlement Service

1. Still on **UPI Production LB**
2. In **CI Relationships**, click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Parent | UPI Production LB |
   | Type | Depends on::Used by |
   | Child | UPI Settlement Service |

4. Click **Submit**

### 4.8 Relationship: UPI PostgreSQL Replica → Depends on → UPI PostgreSQL Primary

1. Navigate to **`cmdb_ci_db_instance.list`**
2. Click on **UPI PostgreSQL Replica**
3. In **CI Relationships**, click **New**
4. Fill in:

   | Field | Value |
   |---|---|
   | Parent | UPI PostgreSQL Replica |
   | Type | Depends on::Used by |
   | Child | UPI PostgreSQL Primary |

5. Click **Submit**

### 4.9 Relationship: Prometheus → Monitors → UPI Transaction Service

1. Navigate to **`cmdb_ci_appl.list`**
2. Click on **Prometheus Monitoring**
3. In **CI Relationships**, click **New**
4. Fill in:

   | Field | Value |
   |---|---|
   | Parent | Prometheus Monitoring |
   | Type | Monitors::Monitored by |
   | Child | UPI Transaction Service |

   > **Note:** If "Monitors::Monitored by" is not available in your PDI, use "Depends on::Used by" as an alternative. The relationship type list varies by PDI version and installed plugins.

5. Click **Submit**

### 4.10 Relationship: Prometheus → Monitors → UPI Settlement Service

1. Still on **Prometheus Monitoring**
2. In **CI Relationships**, click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Parent | Prometheus Monitoring |
   | Type | Monitors::Monitored by |
   | Child | UPI Settlement Service |

4. Click **Submit**

### 4.11 Relationship: Snow Bridge → Depends on → Prometheus

1. Navigate to **`cmdb_ci_appl.list`**
2. Click on **Snow Bridge Integration**
3. In **CI Relationships**, click **New**
4. Fill in:

   | Field | Value |
   |---|---|
   | Parent | Snow Bridge Integration |
   | Type | Depends on::Used by |
   | Child | Prometheus Monitoring |

5. Click **Submit**

### 4.12 Containment Relationships: UPI Payment Platform Contains All CIs

The Business Application "UPI Payment Platform" should contain all technical CIs. This establishes the service boundary.

1. Navigate to **`cmdb_ci_business_app.list`**
2. Click on **UPI Payment Platform**
3. For **each** of the following CIs, create a "Contains::Contained by" relationship:

   | # | Relationship to Create |
   |---|---|
   | 1 | UPI Payment Platform **Contains** UPI Transaction Service |
   | 2 | UPI Payment Platform **Contains** UPI Settlement Service |
   | 3 | UPI Payment Platform **Contains** UPI PostgreSQL Primary |
   | 4 | UPI Payment Platform **Contains** UPI PostgreSQL Replica |
   | 5 | UPI Payment Platform **Contains** UPI Production LB |
   | 6 | UPI Payment Platform **Contains** UPI App Server 01 |
   | 7 | UPI Payment Platform **Contains** UPI App Server 02 |
   | 8 | UPI Payment Platform **Contains** UPI DB Server 01 |
   | 9 | UPI Payment Platform **Contains** Prometheus Monitoring |
   | 10 | UPI Payment Platform **Contains** Grafana Dashboard |
   | 11 | UPI Payment Platform **Contains** Snow Bridge Integration |

   For each one:
   - In the **CI Relationships** related list, click **New**
   - Set **Parent** = UPI Payment Platform
   - Set **Type** = Contains::Contained by
   - Set **Child** = (the CI from the table above)
   - Click **Submit**
   - Repeat for all 11 CIs

4. After all 11 containment relationships are created, the UPI Payment Platform record should show 11 entries in its CI Relationships list.

### 4.13 Complete Relationship Map

You have now created the following relationships:

```
                    ┌─────────────────────────────────┐
                    │     UPI Payment Platform         │
                    │     (Business Application)       │
                    │     Contains all CIs below       │
                    └──────────────┬──────────────────┘
                                   │ Contains
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
   ┌──────────────┐    ┌────────────────────┐    ┌──────────────┐
   │ UPI Prod LB  │    │  Monitoring Stack  │    │  Databases   │
   │ (Load Bal.)  │    │                    │    │              │
   └──────┬───────┘    │ ┌──────────────┐   │    │ ┌──────────┐│
          │            │ │ Snow Bridge  │   │    │ │ PG       ││
          │ Depends on │ │ Integration  │   │    │ │ Primary  ││
    ┌─────┴─────┐      │ └──────┬───────┘   │    │ │(5432)   ││
    │           │      │        │Depends on  │    │ └─────┬────┘│
    ▼           ▼      │        ▼            │    │       │     │
┌────────┐ ┌────────┐  │ ┌──────────────┐   │    │  ┌────▼───┐ │
│UPI Txn │ │UPI Stl │  │ │ Prometheus   │   │    │  │ PG     │ │
│Service │ │Service │  │ │ Monitoring   │───┼────┼──│Replica │ │
│(8081)  │ │(8082)  │  │ └──────┬───────┘   │    │  │        │ │
└───┬────┘ └───┬────┘  │       │Monitors    │    │  └────────┘ │
    │          │       │       ▼            │    └──────────────┘
    │Depends   │Dep.   │ ┌──────────────┐   │           ▲
    │on        │on     │ │ Grafana      │   │           │
    │   ┌──────┘       │ │ Dashboard    │   │    Used by│
    │   │              │ └──────────────┘   │    (Depends on)
    ▼   ▼              └────────────────────┘           │
┌────────────────┐                              ┌───────┴───────┐
│ UPI PostgreSQL │◄─────────────────────────────┤               │
│ Primary (5432) │                              │  Both app     │
└────────────────┘                              │  services     │
    │Runs on           │Runs on                 │  depend on    │
    ▼                  ▼                        │  this DB      │
┌────────────┐  ┌────────────┐                  └───────────────┘
│UPI App     │  │UPI App     │
│Server 01   │  │Server 02   │
│16GB/8CPU   │  │16GB/8CPU   │
└────────────┘  └────────────┘

                ┌────────────┐
                │UPI DB      │
                │Server 01   │
                │64GB/16CPU  │
                └────────────┘
```

**Relationship Summary:**

| # | Parent CI | Relationship Type | Child CI |
|---|---|---|---|
| 1 | UPI Transaction Service | Depends on | UPI PostgreSQL Primary |
| 2 | UPI Transaction Service | Runs on | UPI App Server 01 |
| 3 | UPI Settlement Service | Depends on | UPI PostgreSQL Primary |
| 4 | UPI Settlement Service | Runs on | UPI App Server 02 |
| 5 | UPI Production LB | Depends on | UPI Transaction Service |
| 6 | UPI Production LB | Depends on | UPI Settlement Service |
| 7 | UPI PostgreSQL Replica | Depends on | UPI PostgreSQL Primary |
| 8 | Prometheus Monitoring | Monitors | UPI Transaction Service |
| 9 | Prometheus Monitoring | Monitors | UPI Settlement Service |
| 10 | Snow Bridge Integration | Depends on | Prometheus Monitoring |
| 11-21 | UPI Payment Platform | Contains | (all 11 technical CIs) |

**Total relationships created: 21**

---

## Part 5: Service Mapping & Visualization

Now that all CIs and relationships are created, let us explore how ServiceNow visualizes the configuration model.

### 5.1 View the Service Map from a CI Record

1. Navigate to **`cmdb_ci_app_server.list`**
2. Click on **UPI Transaction Service**
3. In the CI record, look for the **View Map** button or the **Dependency Views** related link
   - In Zurich, click the **hamburger menu** (three lines) at the top-left of the form
   - Select **View Map** or **Dependency Map**
4. The Service Map viewer opens, showing:
   - **UPI Transaction Service** at the center
   - **UPI PostgreSQL Primary** below it (depends on)
   - **UPI App Server 01** below it (runs on)
   - **UPI Production LB** above it (used by)
   - **Prometheus Monitoring** connected (monitored by)

5. Explore the map controls:
   - **Zoom in/out** using the scroll wheel or +/- buttons
   - **Pan** by clicking and dragging the background
   - **Click on a CI** in the map to see its details in a side panel
   - **Expand nodes** to see deeper relationships

### 5.2 View the Service Map from the Business Application

1. Navigate to **`cmdb_ci_business_app.list`**
2. Click on **UPI Payment Platform**
3. Click **View Map**
4. This shows the **complete service topology** — all 12 CIs and their relationships in one view
5. This is the view that Sanjay Manager and NOC team (Priya Sharma) would use during a major incident to understand the full blast radius

### 5.3 Upstream and Downstream Impact Analysis

From any CI in the map, you can analyze impact in two directions:

**Upstream (What uses this CI?):**
- Starting from **UPI PostgreSQL Primary**, go upstream:
  - UPI Transaction Service uses it (Depends on)
  - UPI Settlement Service uses it (Depends on)
  - UPI PostgreSQL Replica depends on it
  - Going further upstream: UPI Production LB depends on both app services
  - The entire UPI Payment Platform contains it

**Downstream (What does this CI depend on?):**
- Starting from **UPI Production LB**, go downstream:
  - Depends on UPI Transaction Service
  - Depends on UPI Settlement Service
  - Transaction Service depends on PostgreSQL Primary
  - Transaction Service runs on App Server 01
  - Settlement Service depends on PostgreSQL Primary
  - Settlement Service runs on App Server 02

**Impact scenario:** If UPI PostgreSQL Primary goes down:
```
UPI PostgreSQL Primary (DOWN)
    ▲ Used by
    ├── UPI Transaction Service (IMPACTED - cannot process payments)
    │       ▲ Used by
    │       └── UPI Production LB (IMPACTED - backend unavailable)
    ├── UPI Settlement Service (IMPACTED - cannot run settlements)
    │       ▲ Used by
    │       └── UPI Production LB (IMPACTED - backend unavailable)
    └── UPI PostgreSQL Replica (IMPACTED - replication source gone)

Result: TOTAL SERVICE OUTAGE — UPI Payment Platform is fully down
        All PSP banks cannot process UPI transactions
        This is a P1 Critical Incident
```

### 5.4 Navigate the Dependency Views Module

1. In the Filter Navigator, type **`Dependency Views`** and press Enter
2. This opens the graphical dependency explorer
3. In the search box, type **UPI Transaction Service** and select it
4. The dependency graph renders showing all related CIs
5. Use the **Filter** options to show only specific relationship types:
   - Toggle **Depends on** to see only dependency relationships
   - Toggle **Runs on** to see only hosting relationships
   - Toggle **Contains** to see containment relationships

---

## Part 6: CI Lifecycle Management

CIs are not static — they go through maintenance, upgrades, and eventually retirement. This part covers managing CI state changes.

### 6.1 Change CI Status: Simulate Maintenance Window

**Scenario:** The Platform Engineering team needs to perform a PostgreSQL minor version upgrade on the replica database. The replica must be taken out of service temporarily.

1. Navigate to **`cmdb_ci_db_instance.list`**
2. Click on **UPI PostgreSQL Replica**
3. Change the following fields:

   | Field | Old Value | New Value |
   |---|---|---|
   | Operational status | Operational | In Maintenance |
   | Install status | Installed | In Maintenance |

4. In the **Additional comments** or **Work notes** field, add:
   ```
   Maintenance window: Upgrading PostgreSQL from 16.2 to 16.3.
   Approved change: CHG0010001.
   Expected duration: 30 minutes.
   Impact: Read-only reporting queries will fail during maintenance.
   Settlement Service report generation will be temporarily unavailable.
   Primary database and all write operations are unaffected.
   ```
5. Click **Update**

### 6.2 Verify Maintenance Status

1. Navigate back to **`cmdb_ci_db_instance.list`**
2. Notice that "UPI PostgreSQL Replica" now shows operational status as "In Maintenance"
3. Open the record and scroll to the **Activity** section to see the work note you added

### 6.3 Return CI to Operational Status

After the maintenance window completes:

1. Open **UPI PostgreSQL Replica**
2. Change:

   | Field | Old Value | New Value |
   |---|---|---|
   | Operational status | In Maintenance | Operational |
   | Install status | In Maintenance | Installed |
   | Version | 16.2 | 16.3 |

3. Add a work note:
   ```
   Maintenance complete. PostgreSQL upgraded from 16.2 to 16.3 successfully.
   Replication lag recovered to <50ms within 2 minutes.
   Read-only queries restored. Settlement Service reports verified functional.
   Change CHG0010001 closed successful.
   ```
4. Click **Update**

### 6.4 Audit Trail: View CI Change History

Every change to a CI record is logged in the audit trail.

1. Open **UPI PostgreSQL Replica**
2. Right-click the header bar and select **History** (or click the **History** icon)
3. You will see a list of all changes made to this CI:
   - Initial creation (all fields set)
   - Status changed to In Maintenance
   - Status changed back to Operational
   - Version changed from 16.2 to 16.3
4. Each entry shows: **Who** changed it, **When**, and **What** the old and new values were

> **ITIL Connection:** This is **Status Accounting** — the third stage of the CI lifecycle. The audit trail provides a complete history of every configuration change, which is essential for compliance, root cause analysis, and change verification.

### 6.5 Understanding Operational Status vs. Install Status

These two fields serve different purposes:

| Field | Purpose | Values | Who Updates |
|---|---|---|---|
| **Install Status** | Tracks where the CI is in its physical lifecycle | On Order, Received, In Stock, Installed, In Maintenance, Retired | Asset Management, IT Admin |
| **Operational Status** | Tracks whether the CI is currently functioning | Operational, Non-Operational, In Maintenance, Retired | Operations team, monitoring automation |

**Example scenario:**
- A server is **Installed** (Install Status) but **Non-Operational** (Operational Status) = the hardware is racked and cabled, but the OS has not been configured yet
- A server is **Installed** and **In Maintenance** = the server is live in production but currently undergoing a maintenance window
- A server is **Retired** (both fields) = the server has been decommissioned and removed from service

---

## Part 7: CMDB Health & Best Practices

A CMDB is only valuable if its data is accurate and trusted. This section covers CMDB governance and health monitoring.

### 7.1 CMDB Health Dashboard

1. In the Filter Navigator, type **`CMDB Health`** and press Enter
2. If the CMDB Health Dashboard is available in your PDI, you will see:
   - **Completeness Score:** Are all required fields populated?
   - **Compliance Score:** Do CIs follow naming conventions and governance rules?
   - **Relationship Score:** Do CIs have appropriate relationships?
   - **Staleness Score:** Are CIs being updated regularly?

> **Note:** The CMDB Health Dashboard may not be fully functional in all PDI versions. If it is not available, you can perform manual health checks as described below.

### 7.2 Find Orphan CIs (No Relationships)

An "orphan CI" is a CI with no relationships — it exists in isolation, which usually means it is either misconfigured or no longer relevant.

1. In the Filter Navigator, type **`cmdb_ci.list`** and press Enter
2. Set the filter:
   - **Support group → is → Platform Engineering**
3. Click **Run**
4. For each CI in the list, check whether it appears in the `cmdb_rel_ci` table:

   **Quick method using a report:**
   1. Navigate to **`cmdb_rel_ci.list`**
   2. Count the unique CIs that appear as either Parent or Child
   3. Compare with your total CI count (12)

   **Script method (run in Scripts - Background):**
   ```javascript
   // Find orphan CIs in Platform Engineering support group
   var orphans = [];
   var ci = new GlideRecord('cmdb_ci');
   ci.addQuery('support_group.name', 'Platform Engineering');
   ci.query();
   while (ci.next()) {
       var rel = new GlideAggregate('cmdb_rel_ci');
       rel.addQuery('parent', ci.sys_id)
          .addOrCondition('child', ci.sys_id);
       rel.addAggregate('COUNT');
       rel.query();
       rel.next();
       if (rel.getAggregate('COUNT') == 0) {
           orphans.push(ci.name.toString());
       }
   }
   gs.info('Orphan CIs: ' + (orphans.length > 0 ? orphans.join(', ') : 'None found'));
   ```

If you created all relationships in Part 4, there should be **zero orphan CIs**.

### 7.3 Duplicate Detection

Duplicate CIs create confusion — which record is the "real" one? Check for duplicates by name:

1. Navigate to **`cmdb_ci.list`**
2. Set the filter: **Support group → is → Platform Engineering**
3. Click the **Name** column header to sort alphabetically
4. Scan for duplicate names
5. If you accidentally created a CI twice, delete the duplicate:
   - Open the duplicate record
   - Click **Delete** from the hamburger menu
   - Confirm deletion

### 7.4 Data Quality Checklist

For each CI in your CMDB, verify the following data quality indicators:

| Quality Check | What to Verify | Why It Matters |
|---|---|---|
| **Name is meaningful** | "UPI Transaction Service" not "Server 1" | Incident responders need to quickly identify the CI |
| **Support group is set** | Every CI has a support group | Assignment rules route incidents based on CI support group |
| **Operational status is current** | Reflects actual state | NOC dashboard filters on operational CIs |
| **Environment is set** | Production, Development, Test | Prevents changes meant for Dev from being applied to Prod CIs |
| **Relationships exist** | At least one relationship per CI | Impact analysis requires relationships |
| **IP/Hostname populated** | For infrastructure CIs | Discovery and monitoring correlation depends on these fields |
| **Description is detailed** | Contains enough context for first-time responder | Reduces resolution time during incidents |
| **Owner and manager set** | Business and technical ownership clear | Escalation paths are clear |

### 7.5 CMDB Governance Best Practices

| Practice | Description | UPI Application |
|---|---|---|
| **Single Source of Truth** | The CMDB is the authoritative source for CI data | All teams reference ServiceNow CMDB, not spreadsheets or wiki pages |
| **Federated Data** | Some CI attributes are mastered in external systems | Prometheus service discovery feeds CI hostnames; ServiceNow masters ownership and relationships |
| **Regular Audits** | Quarterly review of all CIs for accuracy | Platform Engineering reviews all 12 UPI CIs every quarter |
| **Automated Discovery** | Use Discovery or integrations to keep CMDB current | Prometheus node_exporter data could feed server CI attributes (CPU, RAM, disk) |
| **Change-Driven Updates** | Every change request should update affected CIs | PostgreSQL upgrade from 16.2 to 16.3 updates the version field on the CI |
| **Retirement Process** | Retired CIs are not deleted but marked as Retired | When a server is decommissioned, set Install Status = Retired, do not delete the record |
| **Naming Convention** | Consistent naming standard for all CIs | Pattern: "UPI [Component Name]" — enforced by Platform Engineering |

---

## Practice Exercises

### Exercise 1: Add a New CI — "UPI Dispute Service"

NPCI is launching a new Dispute Resolution Service for handling UPI transaction disputes (chargebacks, refunds, escalations).

**Task:** Create this CI and set up proper relationships.

1. Navigate to **`cmdb_ci_app_server.list`**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Dispute Service |
   | Operational status | Operational |
   | Install status | Installed |
   | Short description | Spring Boot microservice for UPI dispute resolution and chargeback management (port 8083) |
   | Host name | upi-dsp-01.npci.org.in |
   | IP Address | 10.100.1.13 |
   | TCP port | 8083 |
   | Running process | java -jar upi-dispute-service.jar |
   | Version | 1.0.0 |
   | Managed by | Amit Verma |
   | Support group | Platform Engineering |
   | Environment | Production |

4. Click **Submit**
5. Create these relationships:
   - UPI Dispute Service **Depends on** UPI PostgreSQL Primary
   - UPI Dispute Service **Runs on** UPI App Server 02 (shared hosting)
   - UPI Production LB **Depends on** UPI Dispute Service
   - UPI Payment Platform **Contains** UPI Dispute Service
   - Prometheus Monitoring **Monitors** UPI Dispute Service

### Exercise 2: Mark "UPI PostgreSQL Replica" as "In Maintenance" and Observe Impact

1. Open **UPI PostgreSQL Replica**
2. Set Operational Status to **In Maintenance**
3. Add work note: "Emergency patching for CVE-2024-XXXX PostgreSQL vulnerability"
4. Click **Update**
5. Now open the **Service Map** for UPI Payment Platform
6. **Question:** Which CIs show as impacted? Why?
7. **Answer:** The replica being in maintenance does not directly impact Transaction or Settlement services because they depend on the Primary, not the Replica. However, settlement **reporting** queries that use read replicas will be affected. This demonstrates that impact analysis depends on which CI is affected and the direction of relationships.
8. After observing, restore the status to **Operational**

### Exercise 3: Create a Custom CI Attribute — "Compliance Status"

NPCI must track regulatory compliance status for each CI (RBI and NPCI security standards).

1. Navigate to **System Definition > Dictionary** (or type `sys_dictionary.list` in the filter navigator)
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Table | Configuration Item [cmdb_ci] |
   | Type | Choice |
   | Column label | Compliance Status |
   | Column name | u_compliance_status |
   | Max length | 40 |

4. Click **Submit**
5. Now add the choice values:
   - Navigate to **System Definition > Choices** (or `sys_choice.list`)
   - Create three choices for the `cmdb_ci` table, field `u_compliance_status`:

     | Label | Value | Sequence |
     |---|---|---|
     | Compliant | compliant | 100 |
     | Non-Compliant | non_compliant | 200 |
     | Pending Review | pending | 300 |

6. Now open any CI (e.g., **UPI Transaction Service**) and verify that the "Compliance Status" field appears on the form
7. Set it to **Compliant** and click **Update**

> **Note:** You may need to add the field to the form layout. Right-click the form header, select **Configure > Form Layout**, and add `u_compliance_status` to the form.

### Exercise 4: Trace All Dependencies of UPI Transaction Service

Using the Dependency Views or Service Map:

1. Open **UPI Transaction Service**
2. Click **View Map** or navigate to **Dependency Views**
3. Document the complete dependency chain:

   **Direct dependencies (1 hop):**
   - Depends on: UPI PostgreSQL Primary
   - Runs on: UPI App Server 01
   - Used by: UPI Production LB
   - Monitored by: Prometheus Monitoring
   - Contained by: UPI Payment Platform

   **Transitive dependencies (2 hops):**
   - UPI PostgreSQL Primary is Used by: UPI Settlement Service, UPI PostgreSQL Replica
   - UPI Production LB has no further upstream dependencies
   - Prometheus Monitoring is Used by: Snow Bridge Integration

4. **Question:** How many CIs are within 2 hops of UPI Transaction Service?
5. **Answer:** 8 CIs — PostgreSQL Primary, App Server 01, Production LB, Prometheus, UPI Payment Platform, Settlement Service, PostgreSQL Replica, Snow Bridge Integration

### Exercise 5: Impact Analysis — UPI App Server 01 Failure

**Scenario:** UPI App Server 01 suffers a hardware failure (motherboard failure, server is completely down).

**Task:** Using the CMDB, determine all impacted CIs and services.

1. Open **UPI App Server 01**
2. View the Service Map
3. Trace upstream:

   ```
   UPI App Server 01 (DOWN - hardware failure)
       ▲ Runs
       └── UPI Transaction Service (IMPACTED - no hosting server)
               ▲ Used by
               ├── UPI Production LB (IMPACTED - lost one backend)
               ▲ Monitored by
               └── Prometheus Monitoring (will report "target down")
                       ▲ Used by
                       └── Snow Bridge Integration (will create incident)
   ```

4. **Impact Assessment:**

   | CI | Impact | Severity |
   |---|---|---|
   | UPI App Server 01 | DOWN — hardware failure | Critical |
   | UPI Transaction Service | DOWN — hosting server unavailable | Critical |
   | UPI Production LB | DEGRADED — lost 50% backend capacity | High |
   | Prometheus Monitoring | ALERTING — target unreachable | Low |
   | Snow Bridge Integration | ACTIVE — creating incident automatically | Low |
   | UPI Settlement Service | NOT IMPACTED — runs on App Server 02 | None |
   | UPI PostgreSQL Primary | NOT IMPACTED — independent infrastructure | None |

5. **Conclusion:** This is a **P1 Critical Incident** because the UPI Transaction Service (real-time payments) is completely down. However, settlements can still run because the Settlement Service is on a separate server. This demonstrates the value of infrastructure redundancy and proper CMDB modeling.

---

## Lab Summary

| What You Did | ITIL 4 Concept | Why It Matters |
|---|---|---|
| Learned CI lifecycle stages | Configuration Management practice — Identification, Control, Status Accounting, Verification | Provides the framework for managing CIs systematically |
| Understood CMDB architecture | CI class hierarchy, table inheritance | Ensures CIs are stored in the right tables with the right fields |
| Created 12 Configuration Items | Configuration Record creation | Every component of the UPI platform is registered and trackable |
| Built 21 relationships | Configuration Model, dependency mapping | Enables impact analysis, blast radius assessment, and service mapping |
| Viewed Service Maps | Service topology visualization | NOC team and management can see how everything connects |
| Managed CI lifecycle state | Status Accounting, audit trail | Track maintenance windows, upgrades, and retirements with full history |
| Checked CMDB health | Verification & Audit | Ensures CMDB data is accurate, complete, and trustworthy |
| Applied governance practices | CMDB governance, data quality | Maintains CMDB as a trusted single source of truth |

---

## Key Concepts

| ITIL Term | Definition | UPI Example |
|---|---|---|
| **Configuration Item (CI)** | Any component that needs to be managed to deliver a service | "UPI Transaction Service" — an application server CI |
| **CMDB** | Configuration Management Database — a repository of CI records and relationships | The ServiceNow CMDB containing all 12 UPI CIs |
| **Configuration Management System (CMS)** | The complete set of tools and data supporting configuration management | CMDB + Discovery + Prometheus integration + Asset Management |
| **Configuration Model** | The set of CIs and relationships that describe a service | All 12 CIs + 21 relationships = the UPI Payment Platform configuration model |
| **Configuration Baseline** | A snapshot of a configuration model at a specific point in time | State of all UPI CIs before a major release deployment |
| **CI Type (Class)** | The category of CI, determining which table stores it | cmdb_ci_app_server, cmdb_ci_db_instance, cmdb_ci_server |
| **CI Relationship** | A defined connection between two CIs | "UPI Transaction Service Depends on UPI PostgreSQL Primary" |
| **Dependency** | A relationship where one CI requires another to function | Transaction Service depends on PostgreSQL — no DB means no transactions |
| **Impact Analysis** | Determining what is affected when a CI fails or changes | PostgreSQL Primary down = both app services impacted = total outage |
| **Service Map** | A visual representation of CI relationships and dependencies | The graphical view showing all UPI components and their connections |
| **Orphan CI** | A CI with no relationships to any other CI | A CI that was created but never connected — indicates a data quality issue |
| **Operational Status** | Whether a CI is currently functioning | Operational, In Maintenance, Non-Operational, Retired |
| **Install Status** | Where a CI is in its physical lifecycle | On Order, Installed, In Maintenance, Retired |
| **Discovery** | Automated scanning to identify and populate CIs | ServiceNow Discovery scanning NPCI network to find servers |
| **Federated Data** | CI data sourced from multiple systems | Hostname from Discovery, ownership from ServiceNow, metrics from Prometheus |

---

## What's Next

In **Lab 08: Service Portfolio & Business Services**, you will:
- Create the **"UPI Payment Processing" Business Service** in ServiceNow
- Define **Technical Services** underneath it
- Assign **Service Owners** and **Support Groups** to services
- Map services to the CIs you created in this lab (service-to-CI relationships)
- Build the **Service Portfolio** showing all NPCI services
- Understand the ITIL 4 **Service Portfolio Management** and **Relationship Management** practices

The CMDB you built in this lab is the foundation for everything that follows. Lab 08 adds the **service layer** on top of the infrastructure layer. Labs 09-11 then attach SLAs, Knowledge articles, and Service Catalog items to these services and CIs.

```
Lab 07 (CMDB)           Lab 08 (Services)        Lab 09 (SLAs)
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│ 12 CIs       │───────►│ Business     │───────►│ SLA: P1 1hr  │
│ 21 Relations │        │ Service +    │        │ SLO: 99.9%   │
│ Service Map  │        │ Tech Services│        │ SLI: Latency │
└──────────────┘        └──────────────┘        └──────────────┘
```

---

## Appendix: Background Script — Automated CI and Relationship Creation

The following script creates all 12 CIs and all 21 relationships programmatically. Use this if you want to skip manual creation or to reset your CMDB data.

**How to run:**
1. Navigate to **System Definition > Scripts - Background** (or type `scripts_background` in the filter navigator)
2. Paste the entire script below
3. Click **Run script**
4. Review the output log for confirmation

> **WARNING:** Run this script only once. Running it multiple times will create duplicate CIs. If you already created CIs manually in Parts 3-4, do NOT run this script unless you first delete those manual CIs.

```javascript
// ============================================================================
// Lab 07: CMDB & Configuration Management — Background Script
// Creates all 12 UPI Payment Platform CIs and 21 relationships
// Organization: NPCI | Platform: UPI | Environment: Production
// ============================================================================

// Helper function: lookup user sys_id by user_name
function getUserSysId(username) {
    var user = new GlideRecord('sys_user');
    user.addQuery('user_name', username);
    user.query();
    if (user.next()) {
        return user.sys_id.toString();
    }
    gs.warn('User not found: ' + username);
    return '';
}

// Helper function: lookup group sys_id by name
function getGroupSysId(groupName) {
    var grp = new GlideRecord('sys_user_group');
    grp.addQuery('name', groupName);
    grp.query();
    if (grp.next()) {
        return grp.sys_id.toString();
    }
    gs.warn('Group not found: ' + groupName);
    return '';
}

// Helper function: lookup relationship type sys_id
function getRelTypeSysId(parentDescriptor) {
    var relType = new GlideRecord('cmdb_rel_type');
    relType.addQuery('parent_descriptor', parentDescriptor);
    relType.query();
    if (relType.next()) {
        return relType.sys_id.toString();
    }
    gs.warn('Relationship type not found: ' + parentDescriptor);
    return '';
}

// Helper function: create a CI relationship
function createRelationship(parentSysId, childSysId, relTypeSysId, desc) {
    var rel = new GlideRecord('cmdb_rel_ci');
    rel.initialize();
    rel.parent = parentSysId;
    rel.child = childSysId;
    rel.type = relTypeSysId;
    var relSysId = rel.insert();
    if (relSysId) {
        gs.info('  Relationship created: ' + desc);
    } else {
        gs.error('  FAILED to create relationship: ' + desc);
    }
    return relSysId;
}

// ============================================================================
// STEP 1: Lookup users and groups
// ============================================================================
gs.info('========================================');
gs.info('Lab 07: CMDB Background Script - START');
gs.info('========================================');

var raviId = getUserSysId('ravi.kumar');
var amitId = getUserSysId('amit.verma');
var priyaId = getUserSysId('priya.sharma');
var sanjayId = getUserSysId('sanjay.mgr');
var platEngId = getGroupSysId('Platform Engineering');

gs.info('Users resolved: ravi=' + raviId + ', amit=' + amitId +
        ', priya=' + priyaId + ', sanjay=' + sanjayId);
gs.info('Group resolved: Platform Engineering=' + platEngId);

// ============================================================================
// STEP 2: Lookup relationship types
// ============================================================================
var dependsOnType = getRelTypeSysId('Depends on');
var runsOnType = getRelTypeSysId('Runs on');
var containsType = getRelTypeSysId('Contains');

// Try "Monitors" — may not exist in all PDIs
var monitorsType = getRelTypeSysId('Monitors');
if (!monitorsType) {
    gs.info('Monitors relationship type not found. Using Depends on instead.');
    monitorsType = dependsOnType;
}

gs.info('Relationship types: dependsOn=' + dependsOnType +
        ', runsOn=' + runsOnType + ', contains=' + containsType +
        ', monitors=' + monitorsType);

// ============================================================================
// STEP 3: Create Configuration Items
// ============================================================================
var ciSysIds = {};

// --- CI 1: UPI Payment Platform (Business Application) ---
gs.info('');
gs.info('--- Creating CIs ---');

var ci1 = new GlideRecord('cmdb_ci_business_app');
ci1.initialize();
ci1.name = 'UPI Payment Platform';
ci1.operational_status = 1; // Operational
ci1.install_status = 1;     // Installed
ci1.short_description = 'NPCI Unified Payments Interface — core payment processing platform handling 10B+ transactions/month';
ci1.managed_by = raviId;
ci1.owned_by = sanjayId;
ci1.support_group = platEngId;
ci1.environment = 'Production';
ci1.comments = 'The UPI Payment Platform is NPCI flagship digital payment infrastructure. It consists of a Transaction Service, Settlement Service, PostgreSQL databases, load balancer, and monitoring stack.';
ciSysIds['upi_platform'] = ci1.insert();
gs.info('CI created: UPI Payment Platform (' + ciSysIds['upi_platform'] + ')');

// --- CI 2: UPI Transaction Service (App Server) ---
var ci2 = new GlideRecord('cmdb_ci_app_server');
ci2.initialize();
ci2.name = 'UPI Transaction Service';
ci2.operational_status = 1;
ci2.install_status = 1;
ci2.short_description = 'Spring Boot microservice for real-time UPI payment processing (port 8081)';
ci2.host_name = 'upi-txn-01.npci.org.in';
ci2.ip_address = '10.100.1.11';
ci2.tcp_port = '8081';
ci2.running_process = 'java -jar upi-transaction-service.jar';
ci2.running_process_key = 'upi-transaction-service';
ci2.version = '3.2.1';
ci2.managed_by = raviId;
ci2.owned_by = raviId;
ci2.support_group = platEngId;
ci2.assigned_to = raviId;
ci2.environment = 'Production';
ci2.comments = 'Primary payment processing engine. Receives payment initiation requests from PSP banks, validates, routes to beneficiary bank. REST APIs on port 8081. Handles ~4000 TPS peak.';
ciSysIds['txn_service'] = ci2.insert();
gs.info('CI created: UPI Transaction Service (' + ciSysIds['txn_service'] + ')');

// --- CI 3: UPI Settlement Service (App Server) ---
var ci3 = new GlideRecord('cmdb_ci_app_server');
ci3.initialize();
ci3.name = 'UPI Settlement Service';
ci3.operational_status = 1;
ci3.install_status = 1;
ci3.short_description = 'Spring Boot microservice for UPI settlement and reconciliation (port 8082)';
ci3.host_name = 'upi-stl-01.npci.org.in';
ci3.ip_address = '10.100.1.12';
ci3.tcp_port = '8082';
ci3.running_process = 'java -jar upi-settlement-service.jar';
ci3.running_process_key = 'upi-settlement-service';
ci3.version = '3.2.1';
ci3.managed_by = amitId;
ci3.owned_by = raviId;
ci3.support_group = platEngId;
ci3.assigned_to = amitId;
ci3.environment = 'Production';
ci3.comments = 'Handles end-of-day settlement between member banks. Settlement windows: 8AM, 12PM, 4PM, 8PM, 12AM. Port 8082.';
ciSysIds['stl_service'] = ci3.insert();
gs.info('CI created: UPI Settlement Service (' + ciSysIds['stl_service'] + ')');

// --- CI 4: UPI PostgreSQL Primary (DB Instance) ---
var ci4 = new GlideRecord('cmdb_ci_db_instance');
ci4.initialize();
ci4.name = 'UPI PostgreSQL Primary';
ci4.operational_status = 1;
ci4.install_status = 1;
ci4.short_description = 'Primary PostgreSQL 16 database for UPI transaction and settlement data';
ci4.host_name = 'upi-db-01.npci.org.in';
ci4.ip_address = '10.100.2.11';
ci4.tcp_port = '5432';
ci4.type = 'PostgreSQL';
ci4.version = '16.2';
ci4.database_name = 'upi_production';
ci4.managed_by = amitId;
ci4.owned_by = raviId;
ci4.support_group = platEngId;
ci4.assigned_to = amitId;
ci4.environment = 'Production';
ci4.comments = 'Primary PostgreSQL 16.2 with streaming replication. Max 500 connections via PgBouncer. 2TB NVMe RAID 10. RPO: 0, RTO: 15min.';
ciSysIds['pg_primary'] = ci4.insert();
gs.info('CI created: UPI PostgreSQL Primary (' + ciSysIds['pg_primary'] + ')');

// --- CI 5: UPI PostgreSQL Replica (DB Instance) ---
var ci5 = new GlideRecord('cmdb_ci_db_instance');
ci5.initialize();
ci5.name = 'UPI PostgreSQL Replica';
ci5.operational_status = 1;
ci5.install_status = 1;
ci5.short_description = 'Read replica of UPI PostgreSQL Primary for reporting and failover';
ci5.host_name = 'upi-db-02.npci.org.in';
ci5.ip_address = '10.100.2.12';
ci5.tcp_port = '5432';
ci5.type = 'PostgreSQL';
ci5.version = '16.2';
ci5.database_name = 'upi_production';
ci5.managed_by = amitId;
ci5.owned_by = raviId;
ci5.support_group = platEngId;
ci5.assigned_to = amitId;
ci5.environment = 'Production';
ci5.comments = 'Synchronous streaming replica. Read-only reporting. Hot standby with Patroni. Failover <30 seconds. Replication lag <100ms.';
ciSysIds['pg_replica'] = ci5.insert();
gs.info('CI created: UPI PostgreSQL Replica (' + ciSysIds['pg_replica'] + ')');

// --- CI 6: UPI Production LB (Load Balancer) ---
var ci6 = new GlideRecord('cmdb_ci_lb');
ci6.initialize();
ci6.name = 'UPI Production LB';
ci6.operational_status = 1;
ci6.install_status = 1;
ci6.short_description = 'HAProxy load balancer distributing UPI API traffic across application servers';
ci6.host_name = 'upi-lb-01.npci.org.in';
ci6.ip_address = '10.100.0.10';
ci6.managed_by = raviId;
ci6.owned_by = raviId;
ci6.support_group = platEngId;
ci6.assigned_to = raviId;
ci6.environment = 'Production';
ci6.comments = 'HAProxy 2.8 LTS. SSL termination. Round-robin. 50K concurrent connections. Rate limit: 10K req/sec per PSP. Ports: 443, 80, stats 8404.';
ciSysIds['lb'] = ci6.insert();
gs.info('CI created: UPI Production LB (' + ciSysIds['lb'] + ')');

// --- CI 7: UPI App Server 01 (Server) ---
var ci7 = new GlideRecord('cmdb_ci_server');
ci7.initialize();
ci7.name = 'UPI App Server 01';
ci7.operational_status = 1;
ci7.install_status = 1;
ci7.short_description = 'Linux application server hosting UPI Transaction Service';
ci7.host_name = 'upi-app-01.npci.org.in';
ci7.ip_address = '10.100.1.11';
ci7.os = 'Linux';
ci7.os_version = 'Ubuntu 22.04 LTS';
ci7.ram = 16384;
ci7.cpu_count = 8;
ci7.cpu_type = 'Intel Xeon E5-2686 v4';
ci7.disk_space = 500;
ci7.serial_number = 'NPCI-APP-SRV-001';
ci7.asset_tag = 'NPCI-A001';
ci7.managed_by = raviId;
ci7.owned_by = raviId;
ci7.support_group = platEngId;
ci7.assigned_to = raviId;
ci7.environment = 'Production';
ci7.comments = 'Mumbai DC, Rack B12, Unit 15. 16GB DDR4 ECC, 8-core Xeon, 500GB NVMe. Dual 10GbE. node_exporter on 9100.';
ciSysIds['app_srv_01'] = ci7.insert();
gs.info('CI created: UPI App Server 01 (' + ciSysIds['app_srv_01'] + ')');

// --- CI 8: UPI App Server 02 (Server) ---
var ci8 = new GlideRecord('cmdb_ci_server');
ci8.initialize();
ci8.name = 'UPI App Server 02';
ci8.operational_status = 1;
ci8.install_status = 1;
ci8.short_description = 'Linux application server hosting UPI Settlement Service';
ci8.host_name = 'upi-app-02.npci.org.in';
ci8.ip_address = '10.100.1.12';
ci8.os = 'Linux';
ci8.os_version = 'Ubuntu 22.04 LTS';
ci8.ram = 16384;
ci8.cpu_count = 8;
ci8.cpu_type = 'Intel Xeon E5-2686 v4';
ci8.disk_space = 500;
ci8.serial_number = 'NPCI-APP-SRV-002';
ci8.asset_tag = 'NPCI-A002';
ci8.managed_by = amitId;
ci8.owned_by = raviId;
ci8.support_group = platEngId;
ci8.assigned_to = amitId;
ci8.environment = 'Production';
ci8.comments = 'Mumbai DC, Rack B12, Unit 16. 16GB DDR4 ECC, 8-core Xeon, 500GB NVMe. Dual 10GbE. node_exporter on 9100.';
ciSysIds['app_srv_02'] = ci8.insert();
gs.info('CI created: UPI App Server 02 (' + ciSysIds['app_srv_02'] + ')');

// --- CI 9: UPI DB Server 01 (Server) ---
var ci9 = new GlideRecord('cmdb_ci_server');
ci9.initialize();
ci9.name = 'UPI DB Server 01';
ci9.operational_status = 1;
ci9.install_status = 1;
ci9.short_description = 'High-performance Linux database server hosting PostgreSQL primary and replica';
ci9.host_name = 'upi-db-srv-01.npci.org.in';
ci9.ip_address = '10.100.2.10';
ci9.os = 'Linux';
ci9.os_version = 'Ubuntu 22.04 LTS';
ci9.ram = 65536;
ci9.cpu_count = 16;
ci9.cpu_type = 'Intel Xeon Gold 6248R';
ci9.disk_space = 4000;
ci9.serial_number = 'NPCI-DB-SRV-001';
ci9.asset_tag = 'NPCI-D001';
ci9.managed_by = amitId;
ci9.owned_by = raviId;
ci9.support_group = platEngId;
ci9.assigned_to = amitId;
ci9.environment = 'Production';
ci9.comments = 'Mumbai DC, Rack C08, Unit 1-4 (4U). 64GB DDR4 ECC, 16-core Xeon Gold, 4TB NVMe RAID 10. 25GbE replication. Battery-backed cache. UPS 30min.';
ciSysIds['db_srv_01'] = ci9.insert();
gs.info('CI created: UPI DB Server 01 (' + ciSysIds['db_srv_01'] + ')');

// --- CI 10: Prometheus Monitoring (Application) ---
var ci10 = new GlideRecord('cmdb_ci_appl');
ci10.initialize();
ci10.name = 'Prometheus Monitoring';
ci10.operational_status = 1;
ci10.install_status = 1;
ci10.short_description = 'Prometheus 2.48 time-series database collecting metrics from all UPI components';
ci10.host_name = 'upi-mon-01.npci.org.in';
ci10.ip_address = '10.100.3.11';
ci10.version = '2.48.1';
ci10.managed_by = raviId;
ci10.owned_by = raviId;
ci10.support_group = platEngId;
ci10.assigned_to = raviId;
ci10.environment = 'Production';
ci10.comments = 'Scrape interval 15s. Retention 30d. Alert rules: error rate >1%, p95 >500ms, service down, disk >80%, CPU >90%. Port 9090.';
ciSysIds['prometheus'] = ci10.insert();
gs.info('CI created: Prometheus Monitoring (' + ciSysIds['prometheus'] + ')');

// --- CI 11: Grafana Dashboard (Application) ---
var ci11 = new GlideRecord('cmdb_ci_appl');
ci11.initialize();
ci11.name = 'Grafana Dashboard';
ci11.operational_status = 1;
ci11.install_status = 1;
ci11.short_description = 'Grafana 10.2 visualization platform for UPI operational dashboards';
ci11.host_name = 'upi-mon-01.npci.org.in';
ci11.ip_address = '10.100.3.11';
ci11.version = '10.2.3';
ci11.managed_by = raviId;
ci11.owned_by = raviId;
ci11.support_group = platEngId;
ci11.assigned_to = priyaId;
ci11.environment = 'Production';
ci11.comments = 'Dashboards: UPI Transaction Overview, Settlement Status, Infra Health, DB Performance, Alert History. Data source: Prometheus. LDAP auth. Port 3000.';
ciSysIds['grafana'] = ci11.insert();
gs.info('CI created: Grafana Dashboard (' + ciSysIds['grafana'] + ')');

// --- CI 12: Snow Bridge Integration (Application) ---
var ci12 = new GlideRecord('cmdb_ci_appl');
ci12.initialize();
ci12.name = 'Snow Bridge Integration';
ci12.operational_status = 1;
ci12.install_status = 1;
ci12.short_description = 'Custom integration service bridging Prometheus AlertManager alerts to ServiceNow incidents';
ci12.host_name = 'upi-mon-01.npci.org.in';
ci12.ip_address = '10.100.3.11';
ci12.version = '1.0.0';
ci12.managed_by = raviId;
ci12.owned_by = raviId;
ci12.support_group = platEngId;
ci12.assigned_to = raviId;
ci12.environment = 'Production';
ci12.comments = 'Python service receiving AlertManager webhooks, creating ServiceNow incidents via REST API. Port 5001. Deduplication, auto-resolve. Config: /etc/snow-bridge/config.yaml.';
ciSysIds['snow_bridge'] = ci12.insert();
gs.info('CI created: Snow Bridge Integration (' + ciSysIds['snow_bridge'] + ')');

gs.info('');
gs.info('All 12 CIs created successfully.');
gs.info('');

// ============================================================================
// STEP 4: Create Relationships
// ============================================================================
gs.info('--- Creating Relationships ---');
gs.info('');

// Dependency relationships
createRelationship(ciSysIds['txn_service'], ciSysIds['pg_primary'], dependsOnType,
    'UPI Transaction Service --Depends on--> UPI PostgreSQL Primary');

createRelationship(ciSysIds['stl_service'], ciSysIds['pg_primary'], dependsOnType,
    'UPI Settlement Service --Depends on--> UPI PostgreSQL Primary');

createRelationship(ciSysIds['lb'], ciSysIds['txn_service'], dependsOnType,
    'UPI Production LB --Depends on--> UPI Transaction Service');

createRelationship(ciSysIds['lb'], ciSysIds['stl_service'], dependsOnType,
    'UPI Production LB --Depends on--> UPI Settlement Service');

createRelationship(ciSysIds['pg_replica'], ciSysIds['pg_primary'], dependsOnType,
    'UPI PostgreSQL Replica --Depends on--> UPI PostgreSQL Primary');

createRelationship(ciSysIds['snow_bridge'], ciSysIds['prometheus'], dependsOnType,
    'Snow Bridge Integration --Depends on--> Prometheus Monitoring');

// Runs on relationships
createRelationship(ciSysIds['txn_service'], ciSysIds['app_srv_01'], runsOnType,
    'UPI Transaction Service --Runs on--> UPI App Server 01');

createRelationship(ciSysIds['stl_service'], ciSysIds['app_srv_02'], runsOnType,
    'UPI Settlement Service --Runs on--> UPI App Server 02');

// Monitors relationships
createRelationship(ciSysIds['prometheus'], ciSysIds['txn_service'], monitorsType,
    'Prometheus Monitoring --Monitors--> UPI Transaction Service');

createRelationship(ciSysIds['prometheus'], ciSysIds['stl_service'], monitorsType,
    'Prometheus Monitoring --Monitors--> UPI Settlement Service');

// Containment relationships (UPI Payment Platform contains all technical CIs)
var technicalCIs = [
    { key: 'txn_service',  name: 'UPI Transaction Service' },
    { key: 'stl_service',  name: 'UPI Settlement Service' },
    { key: 'pg_primary',   name: 'UPI PostgreSQL Primary' },
    { key: 'pg_replica',   name: 'UPI PostgreSQL Replica' },
    { key: 'lb',           name: 'UPI Production LB' },
    { key: 'app_srv_01',   name: 'UPI App Server 01' },
    { key: 'app_srv_02',   name: 'UPI App Server 02' },
    { key: 'db_srv_01',    name: 'UPI DB Server 01' },
    { key: 'prometheus',   name: 'Prometheus Monitoring' },
    { key: 'grafana',      name: 'Grafana Dashboard' },
    { key: 'snow_bridge',  name: 'Snow Bridge Integration' }
];

for (var i = 0; i < technicalCIs.length; i++) {
    createRelationship(ciSysIds['upi_platform'], ciSysIds[technicalCIs[i].key], containsType,
        'UPI Payment Platform --Contains--> ' + technicalCIs[i].name);
}

// ============================================================================
// STEP 5: Summary
// ============================================================================
gs.info('');
gs.info('========================================');
gs.info('Lab 07: CMDB Background Script - COMPLETE');
gs.info('========================================');
gs.info('CIs created: 12');
gs.info('Relationships created: 21');
gs.info('  - Depends on: 6');
gs.info('  - Runs on: 2');
gs.info('  - Monitors: 2');
gs.info('  - Contains: 11');
gs.info('');
gs.info('Next step: Open a CI and click View Map to see the service topology.');
gs.info('========================================');
```

### Script Cleanup (Optional)

If you need to remove all CIs created by this script and start over, use this cleanup script:

```javascript
// ============================================================================
// CLEANUP SCRIPT — Removes all UPI CIs and their relationships
// WARNING: This deletes data permanently. Use with caution.
// ============================================================================

var ciNames = [
    'UPI Payment Platform',
    'UPI Transaction Service',
    'UPI Settlement Service',
    'UPI PostgreSQL Primary',
    'UPI PostgreSQL Replica',
    'UPI Production LB',
    'UPI App Server 01',
    'UPI App Server 02',
    'UPI DB Server 01',
    'Prometheus Monitoring',
    'Grafana Dashboard',
    'Snow Bridge Integration'
];

var deletedCIs = 0;
var deletedRels = 0;

for (var i = 0; i < ciNames.length; i++) {
    var ci = new GlideRecord('cmdb_ci');
    ci.addQuery('name', ciNames[i]);
    ci.query();
    while (ci.next()) {
        // Delete relationships first
        var rel = new GlideRecord('cmdb_rel_ci');
        rel.addQuery('parent', ci.sys_id)
           .addOrCondition('child', ci.sys_id);
        rel.query();
        while (rel.next()) {
            rel.deleteRecord();
            deletedRels++;
        }
        // Then delete the CI
        ci.deleteRecord();
        deletedCIs++;
        gs.info('Deleted CI: ' + ciNames[i]);
    }
}

gs.info('Cleanup complete. Deleted ' + deletedCIs + ' CIs and ' + deletedRels + ' relationships.');
```

---

**End of Lab 07**
