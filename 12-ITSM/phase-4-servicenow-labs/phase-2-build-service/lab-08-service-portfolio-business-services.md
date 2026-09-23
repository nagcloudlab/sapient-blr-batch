# Lab 08: Service Portfolio & Business Services

**Level:** Intermediate | **Duration:** 60 min | **Prerequisites:** Lab 07 completed | **PDI Version:** Zurich

---

## Objective

By the end of this lab, you will:
- Understand ITIL 4 Service Portfolio Management and how it differs from a Service Catalog
- Create Business Services, Technical Services, and Application Services in ServiceNow
- Map the full service hierarchy: Business Service --> Technical Services --> Applications --> Infrastructure CIs
- Configure service relationships and dependencies using CIs created in Lab 07
- Define Service Offerings under Business Services
- Assign service owners, support groups, and escalation contacts
- Build a Service Portfolio Dashboard showing service health and criticality

---

## Scenario

NPCI has completed the CMDB build for the UPI Payment Platform in Lab 07. The following Configuration Items now exist:

```
CMDB (from Lab 07):
  Business Application:
    - UPI Payment Platform

  Application Services:
    - UPI Transaction Service (Spring Boot, port 8081)
    - UPI Settlement Service (Spring Boot, port 8082)

  Database Instances:
    - UPI PostgreSQL Primary
    - UPI PostgreSQL Replica

  Load Balancers:
    - UPI Production LB

  Servers:
    - UPI App Server 01
    - UPI App Server 02
    - UPI DB Server 01

  Monitoring Tools:
    - Prometheus
    - Grafana
    - Snow Bridge
```

The CTO has mandated that before any operational processes (incidents, problems, changes) go live, every technology component must be traceable to a **Business Service** that delivers value to NPCI's stakeholders -- member banks, fintech partners, and end users.

Your task: Build the **Service Portfolio** in ServiceNow so that every CI maps upward to a Business Service, every Business Service has defined ownership and support structure, and Service Offerings describe what consumers actually receive.

---

## Part 1: ITIL 4 Service Portfolio Management -- Theory

Before touching ServiceNow, you must understand the conceptual framework.

### 1.1 What is Service Portfolio Management?

In ITIL 4, **Service Portfolio Management** is the practice that ensures an organization has the right mix of services to meet its business outcomes. It answers:

- What services do we offer today?
- What services are we developing?
- What services have we retired?
- Are our services aligned with business strategy?

The Service Portfolio is the **complete set of services** managed by an organization, regardless of their lifecycle stage.

### 1.2 The Three Zones of the Service Portfolio

```
  SERVICE PORTFOLIO
  ================================================

  1. SERVICE PIPELINE          (Future)
     ┌─────────────────────────────────────┐
     │  Services under development         │
     │  - UPI Credit Line (proposed)       │
     │  - UPI Cross-Border (in design)     │
     │  NOT visible to customers           │
     └─────────────────────────────────────┘
              │
              ▼
  2. SERVICE CATALOG           (Present)
     ┌─────────────────────────────────────┐
     │  Live, operational services         │
     │  - UPI Payment Processing           │
     │  - UPI Merchant Onboarding          │
     │  - UPI Dispute Resolution           │
     │  VISIBLE to customers               │
     └─────────────────────────────────────┘
              │
              ▼
  3. RETIRED SERVICES          (Past)
     ┌─────────────────────────────────────┐
     │  Decommissioned services            │
     │  - UPI USSD Payments (retired 2024) │
     │  - Legacy IMPS Gateway (sunset)     │
     │  NOT visible to customers           │
     └─────────────────────────────────────┘
```

### 1.3 Service Portfolio vs. Service Catalog

This distinction trips up most people:

| Aspect | Service Portfolio | Service Catalog |
|---|---|---|
| **Scope** | ALL services (pipeline + live + retired) | Only LIVE, customer-facing services |
| **Audience** | Internal management, strategy | Customers, end users, support teams |
| **Purpose** | Investment decisions, strategy alignment | Service request, consumption |
| **Visibility** | Restricted (management) | Public (within org or external) |
| **Contains** | Business cases, costs, risks, ROI | Offerings, SLAs, request forms |

**Key insight:** The Service Catalog is a **subset** of the Service Portfolio. Lab 11 will build the Service Catalog items. This lab builds the portfolio structure that contains them.

### 1.4 Service Types in ServiceNow

ServiceNow models services in a class hierarchy:

```
  cmdb_ci_service                     (Base Service class)
    ├── cmdb_ci_service_business      (Business Service)
    ├── cmdb_ci_service_technical     (Technical Service)
    └── cmdb_ci_service_application   (Application Service - auto from APM)

  Business Service:
    - Customer-facing, delivers business value
    - Example: "UPI Payment Processing"
    - Owned by business stakeholder

  Technical Service:
    - Underpins a business service
    - Not visible to end users
    - Example: "UPI Transaction Processing Engine"
    - Owned by technical team

  Application Service:
    - Represents a running application
    - Often discovered automatically
    - Example: "UPI Transaction Service" (the Spring Boot app)
```

### 1.5 Service Relationships and Dependencies

Services do not exist in isolation. The dependency chain for UPI looks like this:

```
  BUSINESS SERVICE LAYER
  ┌──────────────────────────────────────────────────┐
  │  UPI Payment Processing (Business Service)       │
  │    ├── UPI Dispute Resolution (Business Service) │
  │    └── UPI Merchant Onboarding (Business Service)│
  └──────────────┬───────────────────────────────────┘
                 │ depends on
                 ▼
  TECHNICAL SERVICE LAYER
  ┌──────────────────────────────────────────────────┐
  │  UPI Transaction Processing (Technical)          │
  │  UPI Settlement & Reconciliation (Technical)     │
  │  UPI Database Service (Technical)                │
  │  UPI Monitoring & Observability (Technical)      │
  │  UPI Network & Load Balancing (Technical)        │
  └──────────────┬───────────────────────────────────┘
                 │ depends on
                 ▼
  APPLICATION LAYER (CIs from Lab 07)
  ┌──────────────────────────────────────────────────┐
  │  UPI Transaction Service (app, 8081)             │
  │  UPI Settlement Service (app, 8082)              │
  │  UPI Payment Platform (Business Application)     │
  └──────────────┬───────────────────────────────────┘
                 │ runs on / depends on
                 ▼
  INFRASTRUCTURE LAYER (CIs from Lab 07)
  ┌──────────────────────────────────────────────────┐
  │  UPI App Server 01, UPI App Server 02            │
  │  UPI DB Server 01                                │
  │  UPI PostgreSQL Primary, UPI PostgreSQL Replica  │
  │  UPI Production LB                               │
  │  Prometheus, Grafana, Snow Bridge                │
  └──────────────────────────────────────────────────┘
```

### 1.6 Service Roles

| Role | ITIL 4 Definition | UPI Example |
|---|---|---|
| **Service Owner** | Accountable for delivery of a specific service | Sanjay Manager owns "UPI Payment Processing" |
| **Service Manager** | Manages the end-to-end delivery of services | Ravi Kumar manages Technical Services |
| **Process Owner** | Owns the Service Portfolio Management process | Vijay Admin |
| **Relationship Manager** | Manages stakeholder relationships | Sanjay Manager (also interfaces with banks) |

### 1.7 Four Dimensions of Service Management Applied to UPI

ITIL 4 states every service must be considered across four dimensions:

| Dimension | UPI Payment Processing |
|---|---|
| **Organizations & People** | NPCI Platform Engineering, NOC, Service Desk, Member Bank liaisons |
| **Information & Technology** | PostgreSQL, Spring Boot, Prometheus, Grafana, ServiceNow CMDB |
| **Partners & Suppliers** | Member Banks (SBI, HDFC, etc.), Cloud Providers, RBI Compliance |
| **Value Streams & Processes** | Payment initiation --> Authentication --> Debit --> Credit --> Settlement |

---

## Part 2: ServiceNow Service Portfolio Module

### Step 2.1: Navigate to Service Portfolio

1. In the **Filter Navigator** (left sidebar), type: `Service Portfolio`
2. You should see the following menu structure:

```
Service Portfolio
  ├── Services
  │     ├── All Services
  │     ├── Business Services
  │     ├── Technical Services
  │     └── Application Services
  ├── Service Offerings
  └── Service Portfolio Dashboard
```

> **Note:** If you do not see "Service Portfolio" in the navigator, your PDI may require the **IT Service Management** plugin. Navigate to **System Definition > Plugins** and search for `com.snc.service-portfolio`. Activate it if not already active.

### Step 2.2: Understand the Underlying Tables

Open the **All Services** list. Right-click the header bar and select **Configure > List Layout** to verify you are looking at the `cmdb_ci_service` table.

Key tables:

| Table | Label | Description |
|---|---|---|
| `cmdb_ci_service` | Service | Base service table (parent of all service types) |
| `cmdb_ci_service_business` | Business Service | Customer-facing services |
| `cmdb_ci_service_technical` | Technical Service | Infrastructure/platform services |
| `cmdb_ci_service_auto` | Application Service | Auto-discovered application services |
| `service_offering` | Service Offering | Specific offerings under a service |
| `svc_ci_assoc` | Service CI Association | Maps services to CIs |
| `cmdb_rel_ci` | CI Relationship | Relationships between any CIs (including services) |

### Step 2.3: Service Classification and Status Fields

Before creating services, understand the key fields:

**Service Classification** (what type of service):
- Business Service
- Technical Service
- Application Service
- Shared Service

**Service Status** (portfolio lifecycle position):
| Status | Meaning | Portfolio Zone |
|---|---|---|
| Pipeline | Under development, not yet live | Service Pipeline |
| Catalog | Live, available to consumers | Service Catalog |
| Retired | Decommissioned, no longer available | Retired Services |

**Operational Status** (current running state):
| Status | Meaning |
|---|---|
| Operational | Running normally |
| Non-Operational | Down or disabled |
| Repair in Progress | Under maintenance |
| Retired | Permanently shut down |

---

## Part 3: Create Business Services

### Step 3.1: Create "UPI Payment Processing" Business Service

This is the primary Business Service for NPCI's UPI platform.

1. Navigate to **Service Portfolio > Services > Business Services**
2. Click **New**
3. Fill in the following fields:

   | Field | Value |
   |---|---|
   | Name | UPI Payment Processing |
   | Service classification | Business Service |
   | Service status | Catalog |
   | Operational status | Operational |
   | Number | (auto-generated, note it) |

4. Scroll down to the **Details** section:

   | Field | Value |
   |---|---|
   | Description | End-to-end UPI payment processing service handling real-time fund transfers between banks via NPCI's Unified Payments Interface. Processes 10B+ transactions/month across 350+ member banks. Supports P2P, P2M, bill payments, and autopay mandates. Governed by RBI guidelines with 99.95% uptime SLA. |
   | Short description | Core UPI real-time payment processing for member banks and fintech partners |
   | Business criticality | 1 - Most Critical |
   | Used for | Production |

5. Scroll to the **Ownership** section:

   | Field | Value |
   |---|---|
   | Owned by | Sanjay Manager |
   | Managed by | Ravi Kumar |
   | Support group | Platform Engineering |

6. Scroll to the **Stakeholders** section (Related List at the bottom):

   | Field | Value |
   |---|---|
   | Used by | NPCI Operations, Member Banks, Fintech Partners |

7. Click **Submit**

> **Verify:** After submit, navigate back to **Business Services** list. You should see "UPI Payment Processing" with Status = Catalog and Operational Status = Operational.

### Step 3.2: Create "UPI Dispute Resolution" Business Service

1. Navigate to **Service Portfolio > Services > Business Services**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Dispute Resolution |
   | Service classification | Business Service |
   | Service status | Catalog |
   | Operational status | Operational |
   | Description | Handles UPI transaction disputes including failed transactions, unauthorized debits, merchant refunds, and chargeback processing. Interfaces with UDIR (UPI Dispute and Issue Resolution) system as mandated by RBI. Target resolution: 95% within 5 business days. |
   | Short description | UPI dispute handling and resolution for member banks and consumers |
   | Business criticality | 2 - Somewhat Critical |
   | Owned by | Sanjay Manager |
   | Managed by | Ravi Kumar |
   | Support group | Platform Engineering |

4. Click **Submit**

### Step 3.3: Create "UPI Merchant Onboarding" Business Service

1. Navigate to **Service Portfolio > Services > Business Services**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Merchant Onboarding |
   | Service classification | Business Service |
   | Service status | Catalog |
   | Operational status | Operational |
   | Description | End-to-end merchant onboarding service for UPI acceptance. Includes VPA (Virtual Payment Address) creation, QR code generation, settlement account configuration, and merchant category code (MCC) mapping. Onboards 50K+ merchants/month through acquiring banks. |
   | Short description | Merchant registration and activation for UPI payment acceptance |
   | Business criticality | 2 - Somewhat Critical |
   | Owned by | Sanjay Manager |
   | Managed by | Amit Verma |
   | Support group | Platform Engineering |

4. Click **Submit**

### Step 3.4: Verify All Business Services

1. Navigate to **Service Portfolio > Services > Business Services**
2. You should now see three Business Services:

```
┌──────────────────────────────┬──────────┬──────────────┬────────────────────┐
│ Name                         │ Status   │ Op. Status   │ Business Crit.     │
├──────────────────────────────┼──────────┼──────────────┼────────────────────┤
│ UPI Payment Processing       │ Catalog  │ Operational  │ 1 - Most Critical  │
│ UPI Dispute Resolution       │ Catalog  │ Operational  │ 2 - Somewhat Crit. │
│ UPI Merchant Onboarding      │ Catalog  │ Operational  │ 2 - Somewhat Crit. │
└──────────────────────────────┴──────────┴──────────────┴────────────────────┘
```

---

## Part 4: Create Technical Services

Technical Services represent the technology components that underpin Business Services. They are not visible to end users but are critical for service delivery.

### Step 4.1: Create "UPI Transaction Processing" Technical Service

1. Navigate to **Service Portfolio > Services > Technical Services**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Transaction Processing |
   | Service classification | Technical Service |
   | Service status | Catalog |
   | Operational status | Operational |
   | Description | Core transaction processing engine handling UPI payment requests. Performs VPA resolution, payer/payee PSP routing, NPCI switching, transaction signing (PKI), and real-time debit/credit orchestration. Built on Spring Boot microservices with sub-500ms P95 latency requirement. |
   | Short description | Real-time UPI transaction switching and processing engine |
   | Business criticality | 1 - Most Critical |
   | Owned by | Ravi Kumar |
   | Managed by | Amit Verma |
   | Support group | Platform Engineering |

4. Click **Submit**

### Step 4.2: Create "UPI Settlement & Reconciliation" Technical Service

1. Navigate to **Service Portfolio > Services > Technical Services**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Settlement & Reconciliation |
   | Service classification | Technical Service |
   | Service status | Catalog |
   | Operational status | Operational |
   | Description | Batch settlement engine that processes end-of-day net settlement positions across member banks. Performs multi-lateral netting, generates NACH (National Automated Clearing House) settlement files, and reconciles transaction logs against bank confirmations. Settlement windows: 4 cycles/day. |
   | Short description | UPI inter-bank settlement and transaction reconciliation engine |
   | Business criticality | 1 - Most Critical |
   | Owned by | Ravi Kumar |
   | Managed by | Amit Verma |
   | Support group | Platform Engineering |

4. Click **Submit**

### Step 4.3: Create "UPI Database Service" Technical Service

1. Navigate to **Service Portfolio > Services > Technical Services**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Database Service |
   | Service classification | Technical Service |
   | Service status | Catalog |
   | Operational status | Operational |
   | Description | PostgreSQL database cluster providing persistent storage for UPI transaction records, merchant registries, VPA mappings, and settlement data. Primary-replica architecture with synchronous replication, point-in-time recovery, and automated failover. Handles 300K+ writes/sec during peak. |
   | Short description | PostgreSQL database cluster for UPI transaction and configuration data |
   | Business criticality | 1 - Most Critical |
   | Owned by | Ravi Kumar |
   | Managed by | Amit Verma |
   | Support group | Platform Engineering |

4. Click **Submit**

### Step 4.4: Create "UPI Monitoring & Observability" Technical Service

1. Navigate to **Service Portfolio > Services > Technical Services**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Monitoring & Observability |
   | Service classification | Technical Service |
   | Service status | Catalog |
   | Operational status | Operational |
   | Description | Full-stack observability platform for the UPI ecosystem. Prometheus collects 10K+ metrics endpoints. Grafana provides real-time dashboards for transaction rates, latency percentiles, error rates, and settlement status. Snow Bridge forwards critical alerts to ServiceNow for automated incident creation. |
   | Short description | Prometheus + Grafana + Snow Bridge monitoring stack for UPI platform |
   | Business criticality | 2 - Somewhat Critical |
   | Owned by | Ravi Kumar |
   | Managed by | Priya Sharma |
   | Support group | Platform Engineering |

4. Click **Submit**

### Step 4.5: Create "UPI Network & Load Balancing" Technical Service

1. Navigate to **Service Portfolio > Services > Technical Services**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Network & Load Balancing |
   | Service classification | Technical Service |
   | Service status | Catalog |
   | Operational status | Operational |
   | Description | Network infrastructure providing Layer 7 load balancing, SSL/TLS termination, rate limiting, and traffic routing for UPI API endpoints. Distributes requests across application server pool using least-connections algorithm. Handles 50K+ concurrent connections with health-check-based failover. |
   | Short description | Load balancer and network services for UPI API traffic distribution |
   | Business criticality | 1 - Most Critical |
   | Owned by | Ravi Kumar |
   | Managed by | Amit Verma |
   | Support group | Platform Engineering |

4. Click **Submit**

### Step 4.6: Verify All Technical Services

1. Navigate to **Service Portfolio > Services > Technical Services**
2. Confirm five Technical Services exist:

```
┌───────────────────────────────────────┬──────────┬──────────────┬────────────────────┐
│ Name                                  │ Status   │ Op. Status   │ Business Crit.     │
├───────────────────────────────────────┼──────────┼──────────────┼────────────────────┤
│ UPI Transaction Processing            │ Catalog  │ Operational  │ 1 - Most Critical  │
│ UPI Settlement & Reconciliation       │ Catalog  │ Operational  │ 1 - Most Critical  │
│ UPI Database Service                  │ Catalog  │ Operational  │ 1 - Most Critical  │
│ UPI Monitoring & Observability        │ Catalog  │ Operational  │ 2 - Somewhat Crit. │
│ UPI Network & Load Balancing          │ Catalog  │ Operational  │ 1 - Most Critical  │
└───────────────────────────────────────┴──────────┴──────────────┴────────────────────┘
```

---

## Part 5: Service Relationships & Dependencies

This is where the Service Portfolio comes alive. You will create relationships that connect Business Services to Technical Services and Technical Services to the CIs built in Lab 07.

### Step 5.1: Link Business Service to Technical Services

For each Technical Service, create a relationship to the parent Business Service.

**Relationship: UPI Payment Processing depends on UPI Transaction Processing**

1. Navigate to **Service Portfolio > Services > Business Services**
2. Open **UPI Payment Processing**
3. Scroll down to the **Related Items** section (or the **Relations** related list)
4. If you see a **Dependencies** or **Depends on** related list, click **New**

   > **Alternative navigation:** If the related list is not visible, scroll to the bottom of the form and look for **CI Relations** or **Related Services**. You can also use the **Dependency Views** related link.

5. Click **New** in the **Depends on::Used by** related list
6. Fill in:

   | Field | Value |
   |---|---|
   | Parent | UPI Payment Processing |
   | Type | Depends on::Used by |
   | Child | UPI Transaction Processing |

7. Click **Submit**

Repeat for all Technical Services:

| Parent (Business Service) | Relationship | Child (Technical Service) |
|---|---|---|
| UPI Payment Processing | Depends on | UPI Transaction Processing |
| UPI Payment Processing | Depends on | UPI Settlement & Reconciliation |
| UPI Payment Processing | Depends on | UPI Database Service |
| UPI Payment Processing | Depends on | UPI Network & Load Balancing |
| UPI Payment Processing | Depends on | UPI Monitoring & Observability |
| UPI Dispute Resolution | Depends on | UPI Transaction Processing |
| UPI Dispute Resolution | Depends on | UPI Database Service |
| UPI Merchant Onboarding | Depends on | UPI Database Service |
| UPI Merchant Onboarding | Depends on | UPI Network & Load Balancing |

### Step 5.2: Link Technical Services to CIs from Lab 07

Now link each Technical Service to the underlying CIs created in Lab 07.

**Relationship: UPI Transaction Processing depends on UPI Transaction Service CI**

1. Open **UPI Transaction Processing** (Technical Service)
2. Go to the **Depends on::Used by** related list
3. Click **New**
4. Set Child to: **UPI Transaction Service** (the application CI from Lab 07)
5. Click **Submit**

Complete mapping for all Technical Services:

| Technical Service | Depends on (CI from Lab 07) |
|---|---|
| UPI Transaction Processing | UPI Transaction Service |
| UPI Transaction Processing | UPI App Server 01 |
| UPI Transaction Processing | UPI App Server 02 |
| UPI Transaction Processing | UPI Production LB |
| UPI Settlement & Reconciliation | UPI Settlement Service |
| UPI Settlement & Reconciliation | UPI App Server 01 |
| UPI Settlement & Reconciliation | UPI App Server 02 |
| UPI Database Service | UPI PostgreSQL Primary |
| UPI Database Service | UPI PostgreSQL Replica |
| UPI Database Service | UPI DB Server 01 |
| UPI Monitoring & Observability | Prometheus |
| UPI Monitoring & Observability | Grafana |
| UPI Monitoring & Observability | Snow Bridge |
| UPI Network & Load Balancing | UPI Production LB |

### Step 5.3: Verify the Service Dependency Map

1. Open **UPI Payment Processing** Business Service
2. Look for the **Service Map** or **Dependency Map** related link
3. Click it to see the visual dependency tree

You should see a hierarchy like this:

```
UPI Payment Processing (Business Service)
  ├── UPI Transaction Processing (Technical)
  │     ├── UPI Transaction Service (Application CI)
  │     ├── UPI App Server 01 (Server CI)
  │     ├── UPI App Server 02 (Server CI)
  │     └── UPI Production LB (Load Balancer CI)
  │
  ├── UPI Settlement & Reconciliation (Technical)
  │     ├── UPI Settlement Service (Application CI)
  │     ├── UPI App Server 01 (Server CI)
  │     └── UPI App Server 02 (Server CI)
  │
  ├── UPI Database Service (Technical)
  │     ├── UPI PostgreSQL Primary (Database CI)
  │     ├── UPI PostgreSQL Replica (Database CI)
  │     └── UPI DB Server 01 (Server CI)
  │
  ├── UPI Monitoring & Observability (Technical)
  │     ├── Prometheus (Application CI)
  │     ├── Grafana (Application CI)
  │     └── Snow Bridge (Application CI)
  │
  └── UPI Network & Load Balancing (Technical)
        └── UPI Production LB (Load Balancer CI)
```

> **Why this matters:** When UPI PostgreSQL Primary goes down, ServiceNow can now trace the impact upward: Database CI --> UPI Database Service (Technical) --> UPI Payment Processing (Business). This is the foundation for impact analysis in Incident, Problem, and Change Management (Labs 13-15).

### Step 5.4: Understanding Relationship Types

ServiceNow supports many relationship types. Here are the most relevant for service mapping:

| Relationship Type | Forward Label | Reverse Label | Use Case |
|---|---|---|---|
| `Depends on::Used by` | Depends on | Used by | Service A depends on Service B |
| `Runs on::Runs` | Runs on | Runs | App runs on Server |
| `Hosted on::Hosts` | Hosted on | Hosts | DB hosted on Server |
| `Members::Member of` | Members | Member of | Cluster membership |
| `Contains::Contained by` | Contains | Contained by | Logical grouping |
| `Provides::Provided by` | Provides | Provided by | Service provides capability |

---

## Part 6: Service Offerings

Service Offerings describe the specific things consumers can request or consume from a Business Service. They are the bridge between the Service Portfolio and the Service Catalog.

### Step 6.1: Navigate to Service Offerings

1. In the Filter Navigator, type: `Service Offering`
2. Navigate to **Service Portfolio > Service Offerings**
3. This shows the `service_offering` table

### Step 6.2: Create Service Offerings for UPI Payment Processing

**Offering 1: Real-time P2P Transfer**

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | Real-time P2P Transfer |
   | Service | UPI Payment Processing |
   | Status | Operational |
   | Description | Person-to-person real-time fund transfer using VPA (Virtual Payment Address) or mobile number. Supports immediate credit to beneficiary account. Maximum transaction limit: INR 1,00,000 per transaction. Available 24x7x365. Settlement within T+0. |
   | Short description | Instant money transfer between individuals via UPI |
   | Availability | 24x7 |

3. Click **Submit**

**Offering 2: Merchant Payment (P2M)**

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | Merchant Payment |
   | Service | UPI Payment Processing |
   | Status | Operational |
   | Description | Person-to-merchant payment via QR code scan, deep link, or intent flow. Supports static QR (merchant-presented) and dynamic QR (amount-embedded). Settlement to merchant account within T+1 business day. MDR as per RBI guidelines. |
   | Short description | Consumer-to-merchant UPI payment for goods and services |
   | Availability | 24x7 |

3. Click **Submit**

**Offering 3: Bill Payment**

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Bill Payment |
   | Service | UPI Payment Processing |
   | Status | Operational |
   | Description | Recurring and on-demand bill payments via UPI. Integrates with BBPS (Bharat Bill Payment System) for utility bills, loan EMIs, insurance premiums, and government fees. Supports scheduled payments and payment reminders. |
   | Short description | Utility and recurring bill payments through UPI and BBPS integration |
   | Availability | 24x7 |

3. Click **Submit**

**Offering 4: UPI Autopay (Recurring Mandates)**

1. Click **New**
2. Fill in:

   | Field | Value |
   |---|---|
   | Name | UPI Autopay |
   | Service | UPI Payment Processing |
   | Status | Operational |
   | Description | Standing instruction / recurring mandate capability for UPI. Allows consumers to authorize automatic debits for subscriptions, EMIs, SIPs, and recurring payments. Mandate limit: INR 1,00,000 per transaction. Pre-debit notification sent 24 hours before execution. |
   | Short description | Recurring payment mandates and standing instructions via UPI |
   | Availability | 24x7 |

3. Click **Submit**

### Step 6.3: Verify Service Offerings

1. Open **UPI Payment Processing** Business Service
2. Scroll down to the **Service Offerings** related list
3. You should see all four offerings listed:

```
┌────────────────────────────┬──────────────┬──────────────┐
│ Name                       │ Status       │ Availability │
├────────────────────────────┼──────────────┼──────────────┤
│ Real-time P2P Transfer     │ Operational  │ 24x7         │
│ Merchant Payment           │ Operational  │ 24x7         │
│ UPI Bill Payment           │ Operational  │ 24x7         │
│ UPI Autopay                │ Operational  │ 24x7         │
└────────────────────────────┴──────────────┴──────────────┘
```

> **Preview for Lab 11:** Each Service Offering will be linked to a Service Catalog Item. For example, "Merchant Payment" will have a catalog item "Request UPI Merchant Onboarding" with an approval workflow.

### Step 6.4: Create Service Offerings for Other Business Services

**UPI Dispute Resolution -- Offerings:**

| Offering Name | Description | Status |
|---|---|---|
| Transaction Dispute Filing | File a dispute for failed, unauthorized, or incorrect UPI transactions. Initiated by consumer's PSP bank. SLA: acknowledgment within 24 hours. | Operational |
| Chargeback Processing | Initiate chargeback against merchant for goods/services not received. Follows NPCI UDIR (UPI Dispute and Issue Resolution) guidelines. Resolution within 5 business days. | Operational |
| Dispute Status Inquiry | Check real-time status of filed disputes. Provides transaction trail, bank response status, and expected resolution timeline. | Operational |

**UPI Merchant Onboarding -- Offerings:**

| Offering Name | Description | Status |
|---|---|---|
| New Merchant Registration | Register a new merchant for UPI acceptance. Includes KYC verification, VPA creation, QR code generation, and settlement account linking. TAT: 2-3 business days. | Operational |
| Merchant QR Code Generation | Generate static or dynamic QR codes for merchant payment acceptance. Supports Bharat QR and UPI QR formats. Bulk generation available for chains. | Operational |
| Merchant Settlement Configuration | Configure settlement account, frequency (T+0, T+1, T+2), and split settlement rules. Requires NACH mandate and bank verification. | Operational |

Create each of these by following the same process as Step 6.2.

---

## Part 7: Service Owner & Support Configuration

### Step 7.1: Verify Service Ownership

Open each Business Service and confirm ownership is correctly set:

| Business Service | Owner | Managed By | Support Group |
|---|---|---|---|
| UPI Payment Processing | Sanjay Manager | Ravi Kumar | Platform Engineering |
| UPI Dispute Resolution | Sanjay Manager | Ravi Kumar | Platform Engineering |
| UPI Merchant Onboarding | Sanjay Manager | Amit Verma | Platform Engineering |

| Technical Service | Owner | Managed By | Support Group |
|---|---|---|---|
| UPI Transaction Processing | Ravi Kumar | Amit Verma | Platform Engineering |
| UPI Settlement & Reconciliation | Ravi Kumar | Amit Verma | Platform Engineering |
| UPI Database Service | Ravi Kumar | Amit Verma | Platform Engineering |
| UPI Monitoring & Observability | Ravi Kumar | Priya Sharma | Platform Engineering |
| UPI Network & Load Balancing | Ravi Kumar | Amit Verma | Platform Engineering |

### Step 7.2: Configure Escalation Contacts

For each Business Service, you can add escalation contacts in the **Escalation** or **Watch list** fields.

1. Open **UPI Payment Processing**
2. In the **Watch list** field, add: `Sanjay Manager, Ravi Kumar`
3. If available, set the **Escalation contact** to: `Sanjay Manager`
4. Click **Update**

### Step 7.3: Configure Business Hours / Support Hours

ServiceNow uses **Schedules** to define support hours. For UPI (a 24x7 service), you need to ensure the correct schedule is applied.

1. Navigate to **System Scheduler > Schedules**
2. Check if a **24x7** schedule exists. If not, create one:

   | Field | Value |
   |---|---|
   | Name | 24x7 UPI Support |
   | Time zone | Asia/Kolkata |
   | Type | (leave default) |

3. Add schedule entries for each day of the week:

   | Day | Start | End |
   |---|---|---|
   | Monday | 00:00:00 | 23:59:59 |
   | Tuesday | 00:00:00 | 23:59:59 |
   | Wednesday | 00:00:00 | 23:59:59 |
   | Thursday | 00:00:00 | 23:59:59 |
   | Friday | 00:00:00 | 23:59:59 |
   | Saturday | 00:00:00 | 23:59:59 |
   | Sunday | 00:00:00 | 23:59:59 |

4. Save

> **Note:** This schedule will be referenced in Lab 09 (SLA Management) when you define SLA targets with business-hours-based breach calculations.

### Step 7.4: Support Tier Structure

Document the support model for UPI services:

```
  SUPPORT TIERS FOR UPI PAYMENT PROCESSING
  ==========================================

  L0 - Self-Service
    ├── Knowledge Base articles (Lab 10)
    ├── Service Catalog request forms (Lab 11)
    └── FAQs on UPI status page

  L1 - Service Desk / NOC
    ├── Team: Service Desk (Meera Joshi)
    ├── Team: NOC (Priya Sharma)
    ├── Handles: Password resets, basic troubleshooting, alert triage
    └── Escalation target: L2

  L2 - Platform Engineering
    ├── Team: Platform Engineering (Amit Verma)
    ├── Handles: Application issues, configuration changes, performance tuning
    └── Escalation target: L3

  L3 - Senior Engineering / Vendor
    ├── Team: Platform Engineering (Ravi Kumar)
    ├── Handles: Code fixes, architecture decisions, database recovery
    └── Escalation target: Management (Sanjay Manager)
```

---

## Part 8: Service Portfolio Dashboard

### Step 8.1: View All Services by Status

1. Navigate to **Service Portfolio > Services > All Services**
2. Add a filter: **Service status = Catalog**
3. You should see all 8 services (3 Business + 5 Technical)
4. Group by **Service classification** to see them organized

### Step 8.2: Create a Service Overview Report

1. Navigate to **Reports > Create New**
2. Configure the report:

   | Field | Value |
   |---|---|
   | Name | UPI Service Portfolio - By Classification |
   | Source type | Table |
   | Table | Service [cmdb_ci_service] |
   | Type | Bar |
   | Group by | Service classification |
   | Filter | Name starts with "UPI" |

3. Click **Save** and then **Run**
4. You should see a bar chart showing 3 Business Services and 5 Technical Services

### Step 8.3: Business Criticality Matrix Report

1. Navigate to **Reports > Create New**
2. Configure:

   | Field | Value |
   |---|---|
   | Name | UPI Services - Business Criticality |
   | Source type | Table |
   | Table | Service [cmdb_ci_service] |
   | Type | Pie |
   | Group by | Business criticality |
   | Filter | Name starts with "UPI" |

3. Click **Save** and then **Run**
4. The pie chart should show the distribution of services across criticality levels

### Step 8.4: Service Health Overview

Create a list report showing service health at a glance:

1. Navigate to **Reports > Create New**
2. Configure:

   | Field | Value |
   |---|---|
   | Name | UPI Service Health Status |
   | Source type | Table |
   | Table | Service [cmdb_ci_service] |
   | Type | List |
   | Filter | Name starts with "UPI" |
   | Columns | Name, Service classification, Service status, Operational status, Business criticality, Owned by, Support group |

3. Click **Save** and then **Run**

### Step 8.5: Service Cost (Conceptual)

ServiceNow supports service costing through the **Cost Management** module. While full cost modeling is beyond this lab, here is the conceptual cost structure for UPI:

| Service | Monthly Infrastructure Cost (INR) | Category |
|---|---|---|
| UPI Transaction Processing | 45,00,000 | Compute + Licensing |
| UPI Settlement & Reconciliation | 25,00,000 | Compute + Licensing |
| UPI Database Service | 35,00,000 | Storage + Licensing |
| UPI Monitoring & Observability | 12,00,000 | Compute + OSS |
| UPI Network & Load Balancing | 18,00,000 | Network + Hardware |
| **Total Technical Services** | **1,35,00,000** | |
| **UPI Payment Processing (Business)** | **1,35,00,000 + overhead** | Fully loaded cost |

> **In production:** These costs would be entered in the **Financial Management** module (ITFM) and linked to services for chargeback and showback reporting.

---

## Practice Exercises

### Exercise 1: Create a New Business Service -- "UPI QR Code Payments"

Create a new Business Service with the following details:

| Field | Value |
|---|---|
| Name | UPI QR Code Payments |
| Service classification | Business Service |
| Service status | Catalog |
| Operational status | Operational |
| Description | Dedicated QR code-based payment acceptance service for merchants. Supports Bharat QR (interoperable with Visa/Mastercard/RuPay) and UPI QR (UPI-only) formats. Enables scan-and-pay for both static and dynamic QR codes. Processes 2B+ QR transactions/month. |
| Business criticality | 2 - Somewhat Critical |
| Owned by | Sanjay Manager |
| Support group | Platform Engineering |

**Validation:** Open the Business Services list and confirm 4 Business Services are now visible.

### Exercise 2: Add a Technical Service -- "UPI QR Generation Engine"

1. Create a new Technical Service:

   | Field | Value |
   |---|---|
   | Name | UPI QR Generation Engine |
   | Service classification | Technical Service |
   | Service status | Catalog |
   | Operational status | Operational |
   | Description | QR code generation and validation engine. Generates static QR codes with embedded merchant VPA and dynamic QR codes with transaction amount. Supports EMVCo QR specification. Handles QR decoding, validation, and payment intent creation. |
   | Business criticality | 2 - Somewhat Critical |
   | Owned by | Ravi Kumar |
   | Support group | Platform Engineering |

2. Link it to the "UPI QR Code Payments" Business Service using a "Depends on" relationship
3. Also link it to the "UPI Production LB" CI (from Lab 07)

**Validation:** Open the dependency map for "UPI QR Code Payments" and verify the chain: Business Service --> Technical Service --> CI.

### Exercise 3: Retire a Service

1. Open **UPI Dispute Resolution** Business Service
2. Change **Service status** from `Catalog` to `Retired`
3. Change **Operational status** to `Retired`
4. Click **Update**

**Observe and answer:**
- Does the service disappear from the Business Services list? (Hint: check your list filter)
- Navigate to **All Services** -- can you still see it?
- What happens to the Technical Services that "UPI Dispute Resolution" depends on? Are they also retired?

**Answer:** No, dependent Technical Services are NOT automatically retired. A Technical Service may be shared by multiple Business Services. This is why service dependency mapping is critical -- retiring a Business Service requires impact analysis first.

After observing, **revert the change**: Set status back to Catalog / Operational.

### Exercise 4: Create a Service Offering -- "International Remittance"

1. Navigate to **Service Portfolio > Service Offerings**
2. Click **New**
3. Fill in:

   | Field | Value |
   |---|---|
   | Name | International Remittance |
   | Service | UPI Payment Processing |
   | Status | Pipeline |
   | Description | Cross-border remittance capability for UPI. Enables Indian consumers to send money internationally using UPI to participating countries (Singapore, UAE, France under UPI-PayNow, UPI-NECS linkages). Currently in pilot phase with select banks. Expected GA: Q2 2027. |
   | Short description | Cross-border money transfer via UPI international linkages |

4. Click **Submit**

**Observation:** Note that the status is **Pipeline**, not Operational. This represents a service in the Service Pipeline zone of the portfolio -- under development but not yet available to consumers.

### Exercise 5: Generate a Service Report

Create a report that shows all Business Services with their Technical Service count:

1. Navigate to **Reports > Create New**
2. Configure:

   | Field | Value |
   |---|---|
   | Name | Business Services with Dependency Count |
   | Source type | Table |
   | Table | CI Relationship [cmdb_rel_ci] |
   | Type | Bar |
   | Group by | Parent |
   | Aggregation | Count |
   | Filter | Parent.service classification = Business Service AND Type = Depends on::Used by |

3. Click **Run**

> **Alternative approach:** If the filter is complex, use the **Service Portfolio > Services > All Services** list, add the "Downstream Relationships" count column, and export to Excel.

**Expected result:** UPI Payment Processing should show 5 dependencies (the 5 Technical Services).

---

## Lab Summary

In this lab, you built the **Service Portfolio** for NPCI's UPI Payment Platform:

| What You Built | Count | Details |
|---|---|---|
| Business Services | 3 | UPI Payment Processing, Dispute Resolution, Merchant Onboarding |
| Technical Services | 5 | Transaction Processing, Settlement, Database, Monitoring, Network |
| Service Relationships | 23 | Business-to-Technical and Technical-to-CI mappings |
| Service Offerings | 10 | P2P, P2M, Bill Pay, Autopay, Disputes, Merchant services |
| Reports | 3 | Classification, Criticality, Health Status |

### Service Hierarchy Built

```
  PORTFOLIO LAYER (This Lab)
  ================================================================
  Business Services:
    UPI Payment Processing ──────────── Owner: Sanjay Manager
    UPI Dispute Resolution ──────────── Owner: Sanjay Manager
    UPI Merchant Onboarding ─────────── Owner: Sanjay Manager
                    │
                    ▼
  Technical Services:
    UPI Transaction Processing ──────── Owner: Ravi Kumar
    UPI Settlement & Reconciliation ─── Owner: Ravi Kumar
    UPI Database Service ────────────── Owner: Ravi Kumar
    UPI Monitoring & Observability ──── Owner: Ravi Kumar
    UPI Network & Load Balancing ────── Owner: Ravi Kumar
                    │
                    ▼
  CMDB LAYER (Lab 07)
  ================================================================
  Applications:
    UPI Transaction Service, UPI Settlement Service
  Infrastructure:
    App Servers, DB Server, Load Balancer, PostgreSQL, Monitoring
```

---

## Key Concepts

| Concept | Definition | UPI Example |
|---|---|---|
| **Service Portfolio** | Complete inventory of all services (pipeline + catalog + retired) | All 8 UPI services including future International Remittance |
| **Service Catalog** | Subset of portfolio: only live, consumable services | The 7 operational UPI services visible to banks |
| **Business Service** | Customer-facing service delivering business value | UPI Payment Processing |
| **Technical Service** | Technology service underpinning a Business Service | UPI Transaction Processing |
| **Service Offering** | Specific consumable capability within a service | Real-time P2P Transfer |
| **Service Owner** | Person accountable for service delivery | Sanjay Manager |
| **Depends on / Used by** | Relationship type showing service dependencies | Payment Processing depends on Transaction Processing |
| **Impact Analysis** | Tracing CI failures up to Business Service impact | PostgreSQL down --> Database Service --> Payment Processing impacted |
| **Service Status** | Portfolio lifecycle: Pipeline, Catalog, Retired | International Remittance is in Pipeline status |
| **Business Criticality** | How critical the service is to the organization | 1 - Most Critical for Payment Processing |

---

## What's Next

| Next Lab | What You Will Build | How It Uses This Lab |
|---|---|---|
| **Lab 09: SLA, SLO & SLI** | SLA definitions, SLO targets, SLI metrics | SLAs are attached to Business Services created here. P1 incidents against "UPI Payment Processing" will have a 1-hour resolution SLA. |
| **Lab 10: Knowledge Management** | KB articles and troubleshooting runbooks | KB articles reference Business and Technical Services. "UPI Transaction Processing troubleshooting" article links to the Technical Service. |
| **Lab 11: Service Catalog** | Catalog items and request workflows | Service Offerings from this lab become Catalog Items. "Request Merchant Onboarding" links to the "UPI Merchant Onboarding" service. |
| **Lab 13: Incident Management** | Full incident lifecycle with CMDB context | When a CI fails, the incident auto-populates the Business Service field using the dependency chain built in this lab. |
| **Lab 15: Change Management** | Change requests with impact analysis | Change impact is assessed by traversing the service hierarchy: which Business Services are affected by a change to a Technical Service? |

---

## Appendix: Background Script

If you want to create all Business Services, Technical Services, Service Offerings, and relationships programmatically, use this background script.

> **Navigation:** System Definition > Scripts - Background

> **WARNING:** Run this script only ONCE. Running it multiple times will create duplicate records. Verify Lab 07 CIs exist before running.

```javascript
// ============================================================
// Lab 08: Service Portfolio & Business Services - Background Script
// Creates: Business Services, Technical Services, Service Offerings,
//          and all relationships
// Prerequisites: Lab 07 CIs must exist in CMDB
// ============================================================

// Helper: Find a CI by name
function findCI(name) {
    var gr = new GlideRecord('cmdb_ci');
    gr.addQuery('name', name);
    gr.query();
    if (gr.next()) {
        return gr.sys_id.toString();
    }
    gs.warn('Lab 08: CI not found: ' + name);
    return null;
}

// Helper: Find a user by name (last_name or user_name)
function findUser(name) {
    var gr = new GlideRecord('sys_user');
    gr.addQuery('name', name);
    gr.query();
    if (gr.next()) {
        return gr.sys_id.toString();
    }
    gs.warn('Lab 08: User not found: ' + name);
    return null;
}

// Helper: Find a group by name
function findGroup(name) {
    var gr = new GlideRecord('sys_user_group');
    gr.addQuery('name', name);
    gr.query();
    if (gr.next()) {
        return gr.sys_id.toString();
    }
    gs.warn('Lab 08: Group not found: ' + name);
    return null;
}

// Helper: Find the "Depends on::Used by" relationship type
function findRelType() {
    var gr = new GlideRecord('cmdb_rel_type');
    gr.addQuery('parent_descriptor', 'Depends on');
    gr.addQuery('child_descriptor', 'Used by');
    gr.query();
    if (gr.next()) {
        return gr.sys_id.toString();
    }
    gs.warn('Lab 08: Relationship type "Depends on::Used by" not found');
    return null;
}

// Helper: Create a relationship between two CIs
function createRelationship(parentSysId, childSysId, relTypeSysId) {
    if (!parentSysId || !childSysId || !relTypeSysId) {
        gs.warn('Lab 08: Skipping relationship - missing sys_id');
        return;
    }
    var gr = new GlideRecord('cmdb_rel_ci');
    gr.addQuery('parent', parentSysId);
    gr.addQuery('child', childSysId);
    gr.addQuery('type', relTypeSysId);
    gr.query();
    if (gr.next()) {
        gs.info('Lab 08: Relationship already exists, skipping');
        return;
    }
    gr.initialize();
    gr.parent = parentSysId;
    gr.child = childSysId;
    gr.type = relTypeSysId;
    gr.insert();
    gs.info('Lab 08: Created relationship');
}

// Lookup users and groups
var sanjayManager = findUser('Sanjay Manager');
var raviKumar = findUser('Ravi Kumar');
var amitVerma = findUser('Amit Verma');
var priyaSharma = findUser('Priya Sharma');
var platformEng = findGroup('Platform Engineering');

// ============================================================
// PART 1: CREATE BUSINESS SERVICES
// ============================================================

var businessServices = [
    {
        name: 'UPI Payment Processing',
        description: 'End-to-end UPI payment processing service handling real-time fund transfers between banks via NPCI\'s Unified Payments Interface. Processes 10B+ transactions/month across 350+ member banks.',
        short_description: 'Core UPI real-time payment processing for member banks and fintech partners',
        busines_criticality: '1 - Most Critical',
        owned_by: sanjayManager,
        managed_by: raviKumar,
        support_group: platformEng
    },
    {
        name: 'UPI Dispute Resolution',
        description: 'Handles UPI transaction disputes including failed transactions, unauthorized debits, merchant refunds, and chargeback processing. Interfaces with UDIR system as mandated by RBI.',
        short_description: 'UPI dispute handling and resolution for member banks and consumers',
        busines_criticality: '2 - Somewhat Critical',
        owned_by: sanjayManager,
        managed_by: raviKumar,
        support_group: platformEng
    },
    {
        name: 'UPI Merchant Onboarding',
        description: 'End-to-end merchant onboarding service for UPI acceptance. Includes VPA creation, QR code generation, settlement account configuration, and MCC mapping.',
        short_description: 'Merchant registration and activation for UPI payment acceptance',
        busines_criticality: '2 - Somewhat Critical',
        owned_by: sanjayManager,
        managed_by: amitVerma,
        support_group: platformEng
    }
];

var bsMap = {}; // Store sys_ids for later use

for (var b = 0; b < businessServices.length; b++) {
    var bs = businessServices[b];

    // Check if already exists
    var check = new GlideRecord('cmdb_ci_service_business');
    check.addQuery('name', bs.name);
    check.query();
    if (check.next()) {
        gs.info('Lab 08: Business Service already exists: ' + bs.name);
        bsMap[bs.name] = check.sys_id.toString();
        continue;
    }

    var gr = new GlideRecord('cmdb_ci_service_business');
    gr.initialize();
    gr.name = bs.name;
    gr.service_classification = 'Business Service';
    gr.service_status = 'catalog';
    gr.operational_status = 1; // Operational
    gr.short_description = bs.short_description;
    gr.description = bs.description;
    gr.busines_criticality = bs.busines_criticality;
    gr.owned_by = bs.owned_by;
    gr.managed_by = bs.managed_by;
    gr.support_group = bs.support_group;
    gr.used_for = 'Production';
    var sysId = gr.insert();
    bsMap[bs.name] = sysId;
    gs.info('Lab 08: Created Business Service: ' + bs.name + ' (' + sysId + ')');
}

// ============================================================
// PART 2: CREATE TECHNICAL SERVICES
// ============================================================

var technicalServices = [
    {
        name: 'UPI Transaction Processing',
        description: 'Core transaction processing engine handling UPI payment requests. Performs VPA resolution, payer/payee PSP routing, NPCI switching, and real-time debit/credit orchestration.',
        short_description: 'Real-time UPI transaction switching and processing engine',
        busines_criticality: '1 - Most Critical',
        owned_by: raviKumar,
        managed_by: amitVerma,
        support_group: platformEng
    },
    {
        name: 'UPI Settlement & Reconciliation',
        description: 'Batch settlement engine that processes end-of-day net settlement positions across member banks. Performs multi-lateral netting and generates NACH settlement files.',
        short_description: 'UPI inter-bank settlement and transaction reconciliation engine',
        busines_criticality: '1 - Most Critical',
        owned_by: raviKumar,
        managed_by: amitVerma,
        support_group: platformEng
    },
    {
        name: 'UPI Database Service',
        description: 'PostgreSQL database cluster providing persistent storage for UPI transaction records, merchant registries, VPA mappings, and settlement data. Primary-replica architecture with synchronous replication.',
        short_description: 'PostgreSQL database cluster for UPI transaction and configuration data',
        busines_criticality: '1 - Most Critical',
        owned_by: raviKumar,
        managed_by: amitVerma,
        support_group: platformEng
    },
    {
        name: 'UPI Monitoring & Observability',
        description: 'Full-stack observability platform. Prometheus collects 10K+ metrics endpoints. Grafana provides real-time dashboards. Snow Bridge forwards critical alerts to ServiceNow.',
        short_description: 'Prometheus + Grafana + Snow Bridge monitoring stack for UPI platform',
        busines_criticality: '2 - Somewhat Critical',
        owned_by: raviKumar,
        managed_by: priyaSharma,
        support_group: platformEng
    },
    {
        name: 'UPI Network & Load Balancing',
        description: 'Network infrastructure providing Layer 7 load balancing, SSL/TLS termination, rate limiting, and traffic routing for UPI API endpoints.',
        short_description: 'Load balancer and network services for UPI API traffic distribution',
        busines_criticality: '1 - Most Critical',
        owned_by: raviKumar,
        managed_by: amitVerma,
        support_group: platformEng
    }
];

var tsMap = {}; // Store sys_ids

for (var t = 0; t < technicalServices.length; t++) {
    var ts = technicalServices[t];

    var check2 = new GlideRecord('cmdb_ci_service_technical');
    check2.addQuery('name', ts.name);
    check2.query();
    if (check2.next()) {
        gs.info('Lab 08: Technical Service already exists: ' + ts.name);
        tsMap[ts.name] = check2.sys_id.toString();
        continue;
    }

    var gr2 = new GlideRecord('cmdb_ci_service_technical');
    gr2.initialize();
    gr2.name = ts.name;
    gr2.service_classification = 'Technical Service';
    gr2.service_status = 'catalog';
    gr2.operational_status = 1; // Operational
    gr2.short_description = ts.short_description;
    gr2.description = ts.description;
    gr2.busines_criticality = ts.busines_criticality;
    gr2.owned_by = ts.owned_by;
    gr2.managed_by = ts.managed_by;
    gr2.support_group = ts.support_group;
    gr2.used_for = 'Production';
    var sysId2 = gr2.insert();
    tsMap[ts.name] = sysId2;
    gs.info('Lab 08: Created Technical Service: ' + ts.name + ' (' + sysId2 + ')');
}

// ============================================================
// PART 3: CREATE RELATIONSHIPS - Business to Technical
// ============================================================

var relType = findRelType();

// UPI Payment Processing depends on all 5 Technical Services
var paymentProcessing = bsMap['UPI Payment Processing'];
createRelationship(paymentProcessing, tsMap['UPI Transaction Processing'], relType);
createRelationship(paymentProcessing, tsMap['UPI Settlement & Reconciliation'], relType);
createRelationship(paymentProcessing, tsMap['UPI Database Service'], relType);
createRelationship(paymentProcessing, tsMap['UPI Network & Load Balancing'], relType);
createRelationship(paymentProcessing, tsMap['UPI Monitoring & Observability'], relType);

// UPI Dispute Resolution depends on Transaction Processing + Database
var disputeResolution = bsMap['UPI Dispute Resolution'];
createRelationship(disputeResolution, tsMap['UPI Transaction Processing'], relType);
createRelationship(disputeResolution, tsMap['UPI Database Service'], relType);

// UPI Merchant Onboarding depends on Database + Network
var merchantOnboarding = bsMap['UPI Merchant Onboarding'];
createRelationship(merchantOnboarding, tsMap['UPI Database Service'], relType);
createRelationship(merchantOnboarding, tsMap['UPI Network & Load Balancing'], relType);

gs.info('Lab 08: Business-to-Technical relationships created');

// ============================================================
// PART 4: CREATE RELATIONSHIPS - Technical to CIs (from Lab 07)
// ============================================================

// UPI Transaction Processing depends on CIs
var txnProcessing = tsMap['UPI Transaction Processing'];
createRelationship(txnProcessing, findCI('UPI Transaction Service'), relType);
createRelationship(txnProcessing, findCI('UPI App Server 01'), relType);
createRelationship(txnProcessing, findCI('UPI App Server 02'), relType);
createRelationship(txnProcessing, findCI('UPI Production LB'), relType);

// UPI Settlement & Reconciliation depends on CIs
var settlement = tsMap['UPI Settlement & Reconciliation'];
createRelationship(settlement, findCI('UPI Settlement Service'), relType);
createRelationship(settlement, findCI('UPI App Server 01'), relType);
createRelationship(settlement, findCI('UPI App Server 02'), relType);

// UPI Database Service depends on CIs
var dbService = tsMap['UPI Database Service'];
createRelationship(dbService, findCI('UPI PostgreSQL Primary'), relType);
createRelationship(dbService, findCI('UPI PostgreSQL Replica'), relType);
createRelationship(dbService, findCI('UPI DB Server 01'), relType);

// UPI Monitoring & Observability depends on CIs
var monitoring = tsMap['UPI Monitoring & Observability'];
createRelationship(monitoring, findCI('Prometheus'), relType);
createRelationship(monitoring, findCI('Grafana'), relType);
createRelationship(monitoring, findCI('Snow Bridge'), relType);

// UPI Network & Load Balancing depends on CIs
var network = tsMap['UPI Network & Load Balancing'];
createRelationship(network, findCI('UPI Production LB'), relType);

gs.info('Lab 08: Technical-to-CI relationships created');

// ============================================================
// PART 5: CREATE SERVICE OFFERINGS
// ============================================================

var offerings = [
    // UPI Payment Processing offerings
    {
        name: 'Real-time P2P Transfer',
        service: paymentProcessing,
        status: 'operational',
        description: 'Person-to-person real-time fund transfer using VPA or mobile number. Maximum limit: INR 1,00,000. Available 24x7x365.',
        short_description: 'Instant money transfer between individuals via UPI'
    },
    {
        name: 'Merchant Payment',
        service: paymentProcessing,
        status: 'operational',
        description: 'Person-to-merchant payment via QR code scan, deep link, or intent flow. Supports static and dynamic QR. Settlement within T+1.',
        short_description: 'Consumer-to-merchant UPI payment for goods and services'
    },
    {
        name: 'UPI Bill Payment',
        service: paymentProcessing,
        status: 'operational',
        description: 'Recurring and on-demand bill payments via UPI. Integrates with BBPS for utility bills, loan EMIs, and insurance premiums.',
        short_description: 'Utility and recurring bill payments through UPI and BBPS'
    },
    {
        name: 'UPI Autopay',
        service: paymentProcessing,
        status: 'operational',
        description: 'Standing instruction / recurring mandate capability for UPI. Mandate limit: INR 1,00,000. Pre-debit notification sent 24 hours before execution.',
        short_description: 'Recurring payment mandates and standing instructions via UPI'
    },
    // UPI Dispute Resolution offerings
    {
        name: 'Transaction Dispute Filing',
        service: disputeResolution,
        status: 'operational',
        description: 'File a dispute for failed, unauthorized, or incorrect UPI transactions. SLA: acknowledgment within 24 hours.',
        short_description: 'File UPI transaction disputes'
    },
    {
        name: 'Chargeback Processing',
        service: disputeResolution,
        status: 'operational',
        description: 'Initiate chargeback against merchant. Follows NPCI UDIR guidelines. Resolution within 5 business days.',
        short_description: 'Merchant chargeback processing for UPI disputes'
    },
    {
        name: 'Dispute Status Inquiry',
        service: disputeResolution,
        status: 'operational',
        description: 'Check real-time status of filed disputes. Provides transaction trail and expected resolution timeline.',
        short_description: 'Real-time UPI dispute status tracking'
    },
    // UPI Merchant Onboarding offerings
    {
        name: 'New Merchant Registration',
        service: merchantOnboarding,
        status: 'operational',
        description: 'Register new merchant for UPI acceptance. Includes KYC, VPA creation, QR generation, and settlement account linking. TAT: 2-3 business days.',
        short_description: 'New merchant onboarding for UPI payment acceptance'
    },
    {
        name: 'Merchant QR Code Generation',
        service: merchantOnboarding,
        status: 'operational',
        description: 'Generate static or dynamic QR codes. Supports Bharat QR and UPI QR formats. Bulk generation available.',
        short_description: 'QR code generation for merchant payment acceptance'
    },
    {
        name: 'Merchant Settlement Configuration',
        service: merchantOnboarding,
        status: 'operational',
        description: 'Configure settlement account, frequency (T+0, T+1, T+2), and split settlement rules. Requires NACH mandate.',
        short_description: 'Merchant settlement account and frequency configuration'
    }
];

for (var o = 0; o < offerings.length; o++) {
    var off = offerings[o];

    // Check if already exists
    var check3 = new GlideRecord('service_offering');
    check3.addQuery('name', off.name);
    check3.query();
    if (check3.next()) {
        gs.info('Lab 08: Service Offering already exists: ' + off.name);
        continue;
    }

    var gr3 = new GlideRecord('service_offering');
    gr3.initialize();
    gr3.name = off.name;
    gr3.parent = off.service;
    gr3.status = off.status;
    gr3.description = off.description;
    gr3.short_description = off.short_description;
    gr3.insert();
    gs.info('Lab 08: Created Service Offering: ' + off.name);
}

// ============================================================
// SUMMARY
// ============================================================
gs.info('');
gs.info('============================================================');
gs.info('Lab 08: Service Portfolio Setup Complete');
gs.info('============================================================');
gs.info('Business Services created: ' + businessServices.length);
gs.info('Technical Services created: ' + technicalServices.length);
gs.info('Service Offerings created: ' + offerings.length);
gs.info('Relationships created: Business-to-Technical + Technical-to-CI');
gs.info('');
gs.info('Next steps:');
gs.info('  1. Verify in Service Portfolio > Services > All Services');
gs.info('  2. Open UPI Payment Processing and check the dependency map');
gs.info('  3. Proceed to Lab 09: SLA, SLO & SLI');
gs.info('============================================================');
```

> **To run:** Copy the entire script above, navigate to **System Definition > Scripts - Background**, paste it in, and click **Run script**. Check the output log for any warnings about missing CIs or users (which would indicate Lab 07 or Lab 04 data is not in place).

---

**End of Lab 08**
