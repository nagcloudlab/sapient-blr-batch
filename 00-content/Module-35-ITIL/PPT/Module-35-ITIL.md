# ITIL Practices
## Module 35 | Sustain Engineering Training | Days 41-42

---

## Agenda -- Day 41 (Half Day)

| # | Topic |
|---|-------|
| 01 | ITIL 4 Practices Overview |
| 02 | Availability Management |
| 03 | Business Analysis |
| 04 | Capacity & Performance Management |
| 05 | Change Control |
| 06 | Incident Management (Deep Dive) |
| 07 | IT Asset Management + Monitoring & Event Management |

---

## Agenda -- Day 42

| # | Topic |
|---|-------|
| 01 | Problem Management |
| 02 | Release Management |
| 03 | Service Catalogue Management |
| 04 | Service Configuration Management |
| 05 | Service Continuity Management |
| 06 | Service Design |
| 07 | Service Desk |
| 08 | Service Level Management |
| 09 | Service Request Management |
| 10 | Service Validation & Testing |
| 11 | Lab: ITIL Practice Templates |
| 12 | ITIL Practices Integration |
| 13 | Module Wrap-up |

---

## ITIL 4: 34 Practices Overview

### Three Categories

```
┌──────────────────────────────────────────────────────┐
│              ITIL 4 Practice Categories              │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  General Management Practices (14)           │   │
│  │  Strategy, Portfolio, Architecture,          │   │
│  │  Risk, Security, Workforce, Supplier,        │   │
│  │  Relationship, Financial, Knowledge,         │   │
│  │  Measurement, Project, Organizational        │   │
│  │  Change, Continual Improvement               │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Service Management Practices (17)           │   │
│  │  Availability, Business Analysis, Capacity,  │   │
│  │  Change Control, Incident, IT Asset,         │   │
│  │  Monitoring, Problem, Release, Service       │   │
│  │  Catalog, Config, Continuity, Design, Desk,  │   │
│  │  Level, Request, Validation & Testing        │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Technical Management Practices (3)          │   │
│  │  Deployment, Infrastructure & Platform,      │   │
│  │  Software Development                        │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

---

## Availability Management

### Ensuring Services Are Available When Needed

**Purpose:** Ensure services deliver agreed levels of availability to meet business needs.

| Concept | Definition | FoodExpress Example |
|---------|-----------|---------------------|
| **Availability** | Ability to perform as agreed | Order platform up 99.9% of the time |
| **Reliability** | How long a service runs without failure | MTBF (Mean Time Between Failures) = 720 hours |
| **Maintainability** | How quickly a service is restored | MTRS (Mean Time to Restore) = 30 minutes |
| **Serviceability** | Contractual obligations of third parties | Payment gateway SLA = 99.95% |

### Availability Formula

```
Availability % = (Agreed Service Time - Downtime) / Agreed Service Time x 100

FoodExpress Order Platform:
  Agreed Service Time = 720 hours/month (24x7)
  Allowed Downtime at 99.9% = 43.8 minutes/month

  "Three nines" = 99.9% = 8.76 hours/year downtime
  "Four nines"  = 99.99% = 52.6 minutes/year downtime
  "Five nines"  = 99.999% = 5.26 minutes/year downtime
```

---

## Availability Management: Techniques

### Proactive Availability

```
┌──────────────────────────────────────────────────┐
│        Availability Management Techniques        │
│                                                  │
│  REACTIVE                                        │
│  ├── Incident-triggered analysis                │
│  ├── Service outage analysis (SOA)              │
│  └── Expanded incident lifecycle                │
│                                                  │
│  PROACTIVE                                       │
│  ├── Component Failure Impact Analysis (CFIA)    │
│  │   "What if MySQL master goes down?"          │
│  ├── Single Points of Failure (SPOF) analysis   │
│  │   "Is there only one payment gateway?"       │
│  ├── Fault Tree Analysis (FTA)                  │
│  │   "What combination of failures causes       │
│  │    total order platform outage?"              │
│  └── Risk assessment and management             │
│      "What is the probability and impact?"       │
└──────────────────────────────────────────────────┘
```

**FoodExpress SPOF Analysis:**
- Single Redis instance (no replica) -- SPOF
- One payment gateway provider -- SPOF
- Single DNS provider -- SPOF

---

## Business Analysis

### Understanding Business Needs

**Purpose:** Analyze business needs and recommend solutions that deliver value.

```
┌─────────────────────────────────────────────────┐
│         Business Analysis Activities            │
│                                                 │
│  1. UNDERSTAND stakeholder needs                │
│     "FoodExpress wants faster delivery times"   │
│                                                 │
│  2. ANALYZE requirements                        │
│     "Delivery tracking must update every 30s"   │
│                                                 │
│  3. RECOMMEND solutions                         │
│     "Implement WebSocket-based live tracking"   │
│                                                 │
│  4. VALIDATE solutions                          │
│     "Track P95 GPS update latency < 30s"        │
│                                                 │
│  5. MANAGE requirements through lifecycle       │
│     "Requirement traceability matrix"           │
└─────────────────────────────────────────────────┘
```

### FoodExpress Example

| Business Need | IT Requirement | Success Metric |
|--------------|---------------|----------------|
| Reduce order cancellations | Improve payment reliability | < 0.1% payment failures |
| Faster delivery | Optimize rider assignment | Average assignment time < 2 min |
| Better customer experience | Real-time tracking | GPS update every 30s |

---

## Capacity & Performance Management

### Right-Sizing Resources

**Purpose:** Ensure services achieve agreed performance levels, meeting current and future demand.

```
┌──────────────────────────────────────────────────────┐
│       Capacity & Performance Sub-Practices          │
│                                                      │
│  ┌────────────────┐  ┌────────────────────────────┐ │
│  │   Business     │  │  Capacity                  │ │
│  │   Capacity     │  │  Planning                  │ │
│  │                │  │                            │ │
│  │  "Diwali sale  │  │  "Scale order-service      │ │
│  │   = 5x normal  │  │   from 3 to 15 pods        │ │
│  │   traffic"     │  │   by October 15"           │ │
│  └────────────────┘  └────────────────────────────┘ │
│                                                      │
│  ┌────────────────┐  ┌────────────────────────────┐ │
│  │   Service      │  │  Component                 │ │
│  │   Capacity     │  │  Capacity                  │ │
│  │                │  │                            │ │
│  │  "Order API    │  │  "MySQL can handle         │ │
│  │   must handle  │  │   5000 connections,        │ │
│  │   500 req/s"   │  │   currently at 3000"       │ │
│  └────────────────┘  └────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

### Key Metrics

| Resource | Current | Threshold | Action |
|----------|---------|-----------|--------|
| CPU (order pods) | 45% avg | 70% | Scale at 70% |
| Memory (order pods) | 60% avg | 80% | Alert at 80% |
| DB Connections | 3000/5000 | 4000 | Add read replica |
| Disk (logs) | 65% | 85% | Implement log rotation |

---

## Change Control

### Managing Changes Safely

**Purpose:** Maximize successful changes by ensuring risks are properly assessed, changes are authorized, and the change schedule is managed.

```
┌──────────────────────────────────────────────────────┐
│              Change Control Flow                     │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  Request  │─>│  Assess  │─>│ Authorize│          │
│  │  Change   │  │  Risk &  │  │  (CAB or │          │
│  │  (RFC)    │  │  Impact  │  │  Auto)   │          │
│  └──────────┘  └──────────┘  └────┬─────┘          │
│                                    │                 │
│  ┌──────────┐  ┌──────────┐  ┌────▼─────┐          │
│  │  Review  │<─│ Implement│<─│ Schedule │          │
│  │  & Close │  │  & Test  │  │  Change  │          │
│  └──────────┘  └──────────┘  └──────────┘          │
└──────────────────────────────────────────────────────┘
```

### Change Types

| Type | Authorization | Example | Risk |
|------|--------------|---------|------|
| **Standard** | Pre-authorized | Deploy patch to staging | Low |
| **Normal** | CAB approval | Database schema migration | Medium-High |
| **Emergency** | Emergency CAB | Hotfix for payment outage | High (but urgent) |

---

## Change Control: The 7 Rs

### Questions to Ask Before Every Change

| R | Question | FoodExpress Example |
|---|---------|---------------------|
| **Raised** | Who raised the change? | Sustain Eng team via Jira CHG-2026-0089 |
| **Reason** | Why is this change needed? | Memory leak causing delivery service restarts |
| **Return** | What is the expected benefit? | Eliminate 3-4 daily pod restarts |
| **Risk** | What are the risks? | WebSocket reconnection during deployment |
| **Resources** | What resources are needed? | 1 engineer, 2-hour maintenance window |
| **Responsible** | Who is responsible for implementation? | Ravi Kumar, Sustain Engineering |
| **Relationship** | What other services are affected? | Delivery tracking, notification service |

---

## Incident Management: Deep Dive

### Beyond the Basics

```
┌──────────────────────────────────────────────────────┐
│           Incident Management Maturity               │
│                                                      │
│  Level 1: REACTIVE                                   │
│  "Users call us when things break"                   │
│  - Manual detection, ad-hoc response                 │
│                                                      │
│  Level 2: RESPONSIVE                                 │
│  "We detect incidents and respond quickly"           │
│  - Monitoring alerts, defined response process       │
│                                                      │
│  Level 3: PROACTIVE                                  │
│  "We prevent incidents before they impact users"     │
│  - Trend analysis, chaos engineering, auto-remediation│
│                                                      │
│  Level 4: PREDICTIVE                                 │
│  "We predict incidents before they happen"           │
│  - ML-based anomaly detection, capacity forecasting  │
│                                                      │
│  FoodExpress is at Level 2, aiming for Level 3       │
└──────────────────────────────────────────────────────┘
```

### Swarming vs Tiered Support

| Approach | How It Works | Best For |
|----------|-------------|----------|
| **Tiered (L1/L2/L3)** | Escalate through tiers | High-volume, routine incidents |
| **Swarming** | Right experts collaborate immediately | Complex, novel incidents |

---

## IT Asset Management

### Tracking What You Own

**Purpose:** Plan and manage the full lifecycle of IT assets to maximize value and control costs.

| Asset Type | FoodExpress Examples | Lifecycle |
|-----------|---------------------|-----------|
| Hardware | Servers, network switches, load balancers | Procure > Deploy > Maintain > Retire |
| Software | Licenses (MySQL Enterprise, Redis, Kong) | Purchase > Install > Patch > Decommission |
| Cloud | AWS EC2, RDS, EKS, S3 | Provision > Monitor > Optimize > Terminate |
| Containers | Docker images, Helm charts | Build > Deploy > Version > Archive |

### CMDB (Configuration Management Database)

```
┌──────────────────────────────────────────────────┐
│                    CMDB                          │
│                                                  │
│  CI: order-service-v2.3.0                       │
│  ├── Type: Microservice                          │
│  ├── Owner: Platform Team                        │
│  ├── Environment: Production                     │
│  ├── Dependencies: MySQL, Redis, RabbitMQ        │
│  ├── Depends On: payment-service, menu-service   │
│  ├── Pods: 5 replicas                            │
│  ├── CPU: 500m request, 1000m limit              │
│  └── Last Change: CHG-2026-0089 (2026-09-03)     │
└──────────────────────────────────────────────────┘
```

---

## Monitoring & Event Management

### From Events to Action

**Purpose:** Systematically observe services and components, recording and reporting events.

```
┌──────────────────────────────────────────────────────┐
│           Event Classification                       │
│                                                      │
│  ┌──────────────┐                                   │
│  │  All Events  │  Thousands per minute              │
│  └──────┬───────┘                                   │
│         │                                            │
│  ┌──────▼───────┐                                   │
│  │Informational │  "Deployment completed"            │
│  │  (log it)    │  "Backup successful"               │
│  └──────┬───────┘                                   │
│         │                                            │
│  ┌──────▼───────┐                                   │
│  │   Warning    │  "CPU at 75%"                      │
│  │  (watch it)  │  "Response time increasing"        │
│  └──────┬───────┘                                   │
│         │                                            │
│  ┌──────▼───────┐                                   │
│  │  Exception   │  "Service DOWN"                    │
│  │  (act on it) │  "Error rate > 1%"                 │
│  └──────────────┘  --> Create Incident               │
└──────────────────────────────────────────────────────┘
```

**FoodExpress Monitoring Stack:**
- **Metrics:** Prometheus + Grafana
- **Logs:** Loki + Grafana
- **Traces:** Jaeger
- **Alerts:** Alertmanager + PagerDuty

---

## Problem Management

### Finding and Eliminating Root Causes

**Purpose:** Reduce the likelihood and impact of incidents by identifying actual and potential causes.

```
┌──────────────────────────────────────────────────────┐
│     Incident vs Problem vs Known Error              │
│                                                      │
│  INCIDENT ──────> PROBLEM ──────> KNOWN ERROR       │
│  "Payment is      "Why does        "Connection pool  │
│   failing"         payment fail     max=10 is too    │
│                    every Tuesday?"  low for Tuesday   │
│                                    traffic spike"    │
│                                         │            │
│                                    CHANGE REQUEST    │
│                                    "Increase pool    │
│                                     to 50"           │
└──────────────────────────────────────────────────────┘
```

### Problem Management Activities

| Activity | Description | FoodExpress Example |
|----------|-----------|---------------------|
| **Problem Identification** | Trend analysis, multiple incidents | 5 payment timeouts this week |
| **Problem Control** | Investigate and document root cause | Connection pool exhaustion under load |
| **Error Control** | Manage known errors, plan fixes | Workaround: restart pod; Fix: increase pool |
| **Proactive Problem Mgmt** | Identify problems before incidents | Chaos testing reveals SPOF in delivery |

---

## Problem Management: Root Cause Analysis

### Techniques

```
┌──────────────────────────────────────────────────────┐
│           5 Whys -- FoodExpress Example              │
│                                                      │
│  Problem: Orders failing every Tuesday evening       │
│                                                      │
│  Why 1: Payment service returns timeout errors       │
│  Why 2: Database queries take > 30 seconds           │
│  Why 3: Table lock contention on orders table        │
│  Why 4: Weekly report job runs full table scan        │
│  Why 5: Report query has no index on date column     │
│                                                      │
│  Root Cause: Missing index on orders.created_at      │
│  Fix: Add index + move report to read replica        │
└──────────────────────────────────────────────────────┘
```

| Technique | When to Use | Duration |
|-----------|------------|----------|
| **5 Whys** | Simple cause-effect chains | 15-30 min |
| **Fishbone (Ishikawa)** | Multiple potential cause categories | 30-60 min |
| **Fault Tree Analysis** | Complex systems with multiple failure modes | 1-2 hours |
| **Pareto Analysis** | Prioritizing which problems to solve first | 30 min |

---

## Release Management

### Deploying Changes Safely

**Purpose:** Make new and changed services available for use.

```
┌──────────────────────────────────────────────────────┐
│           Release Pipeline -- FoodExpress            │
│                                                      │
│  Dev ──> Build ──> Test ──> Stage ──> Prod          │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ Release Types                                  │  │
│  │                                                │  │
│  │ Major (v3.0.0)  Feature release, new UI       │  │
│  │ Minor (v2.4.0)  New payment method added      │  │
│  │ Patch (v2.3.1)  Bug fix for discount calc     │  │
│  │ Emergency        Hotfix for prod outage        │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ Deployment Strategies                          │  │
│  │                                                │  │
│  │ Rolling Update   Replace pods one by one       │  │
│  │ Blue-Green       Switch traffic to new version │  │
│  │ Canary           Route 5% traffic to new       │  │
│  │ Feature Flags    Toggle features without deploy│  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## Service Catalogue Management

### Maintaining the Service Catalog

**Purpose:** Provide a single source of consistent information on all services, ensuring it is available to those authorized to access it.

```
┌──────────────────────────────────────────────────────┐
│     FoodExpress Service Catalog Entry               │
│                                                      │
│  Service: Order Platform                             │
│  ─────────────────────────────                       │
│  Description:  End-to-end food ordering system       │
│  Owner:        Platform Team                         │
│  Status:       Live                                  │
│  Hours:        24x7                                  │
│  SLA:          99.9% availability                    │
│  Support:      L1: Service Desk (24x7)              │
│                L2: Platform Team (business hours)    │
│                L3: Engineering (on-call)             │
│                                                      │
│  Dependencies:                                       │
│  ├── Payment Service (internal)                     │
│  ├── Menu Service (internal)                        │
│  ├── MySQL Database (infrastructure)                │
│  ├── Redis Cache (infrastructure)                   │
│  └── Razorpay Gateway (external)                    │
│                                                      │
│  Request Channel: ServiceNow Portal                  │
│  Incident Channel: PagerDuty + #foodexpress-ops      │
└──────────────────────────────────────────────────────┘
```

---

## Service Configuration Management

### Tracking Configuration Items

**Purpose:** Ensure accurate and reliable information about the configuration of services is available when and where needed.

| CI Type | Examples | Attributes |
|---------|---------|------------|
| **Service CI** | Order Service v2.3.0 | Version, owner, environment, dependencies |
| **Infrastructure CI** | MySQL RDS instance | Instance type, storage, backup schedule |
| **Application CI** | Docker image | Image tag, registry, vulnerabilities |
| **Document CI** | Runbook for payment outage | Version, author, last reviewed |

### Configuration Relationships

```
                    Order Service (v2.3.0)
                          │
            ┌─────────────┼─────────────┐
            │             │             │
     payment-service  menu-service  rabbitmq
     (v1.8.2)         (v2.1.0)    (v3.12)
            │             │
        razorpay-gw    mysql-menu-db
        (external)     (RDS r5.large)
```

---

## Service Continuity Management

### Preparing for Disasters

**Purpose:** Ensure service availability and performance are maintained at sufficient levels in case of a disaster.

```
┌──────────────────────────────────────────────────────┐
│        FoodExpress DR Strategy                       │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Tier 1: Critical (Order + Payment)          │   │
│  │  RTO: 1 hour  |  RPO: 5 minutes              │   │
│  │  Strategy: Hot standby in DR region           │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Tier 2: Important (Delivery + Menu)         │   │
│  │  RTO: 4 hours  |  RPO: 1 hour                │   │
│  │  Strategy: Warm standby                       │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Tier 3: Non-critical (Reports + Analytics)  │   │
│  │  RTO: 24 hours  |  RPO: 24 hours             │   │
│  │  Strategy: Backup and restore                 │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  RTO = Recovery Time Objective (how fast)            │
│  RPO = Recovery Point Objective (how much data loss) │
└──────────────────────────────────────────────────────┘
```

---

## Service Design

### Designing Services That Work

**Purpose:** Design products and services that are fit for purpose and fit for use, and that can be delivered by the organization.

### The Four Ps of Service Design

| P | Description | FoodExpress |
|---|-----------|-------------|
| **People** | Skills, roles, responsibilities | SRE team, DevOps, Support |
| **Processes** | Workflows, procedures | Incident process, change process |
| **Products** | Technology and tools | Kubernetes, Prometheus, ServiceNow |
| **Partners** | Suppliers and vendors | AWS, Razorpay, Twilio |

### Design Considerations

```
┌───────────────────────────────────────────────┐
│  Service Design Package (SDP)                 │
│                                               │
│  1. Service requirements (functional & non)   │
│  2. Service architecture                      │
│  3. Technology requirements                   │
│  4. Process requirements                      │
│  5. Measurement and metrics                   │
│  6. Testing requirements                      │
│  7. Transition requirements                   │
│  8. Acceptance criteria                       │
└───────────────────────────────────────────────┘
```

---

## Service Desk

### The Single Point of Contact

**Purpose:** Capture demand for incident resolution and service requests, and be the entry point for all users.

```
┌──────────────────────────────────────────────────────┐
│            FoodExpress Service Desk                  │
│                                                      │
│  Channels:                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │  Portal  │ │  Phone   │ │   Chat   │ │ Email  │ │
│  │ServiceNow│ │  Toll-   │ │  Slack   │ │support@│ │
│  │          │ │  free    │ │  bot     │ │food..  │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └───┬────┘ │
│       └─────────────┼───────────┼────────────┘      │
│                     ▼                                │
│            ┌──────────────┐                          │
│            │  Service     │                          │
│            │  Desk Agent  │                          │
│            └──────┬───────┘                          │
│                   │                                  │
│         ┌─────────┼─────────┐                       │
│         ▼         ▼         ▼                       │
│     Incident   Service    Knowledge                  │
│     Record     Request    Article                    │
│     (INC-)     (RITM-)   (KB-)                      │
└──────────────────────────────────────────────────────┘
```

### Service Desk Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| First Contact Resolution | > 70% | Resolved without escalation |
| Average Handle Time | < 15 min | Time spent per contact |
| Customer Satisfaction | > 4.0/5.0 | Post-interaction survey |
| Abandonment Rate | < 5% | Calls/chats abandoned before answer |

---

## Service Level Management

### Defining and Measuring Service Quality

**Purpose:** Set clear business-based targets for service levels and ensure delivery is properly assessed and managed.

### SLA / OLA / UC Hierarchy

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  Customer ◄────── SLA (Service Level Agreement)     │
│                   "Order platform: 99.9% uptime"     │
│                                                      │
│  Internal ◄────── OLA (Operational Level Agreement)  │
│  Teams            "Database team: 99.95% uptime"     │
│                   "Network team: 99.99% uptime"      │
│                                                      │
│  Suppliers ◄───── UC (Underpinning Contract)         │
│                   "AWS: 99.99% EC2 uptime"           │
│                   "Razorpay: 99.95% gateway uptime"  │
│                                                      │
│  The SLA can only be as strong as the weakest       │
│  OLA or UC beneath it.                               │
└──────────────────────────────────────────────────────┘
```

---

## Service Level Management: SLA Definition

### FoodExpress SLA Template

```yaml
sla:
  name: "FoodExpress Order Platform SLA"
  version: "2.0"
  effective_date: "2026-07-01"
  review_date: "2026-12-31"

  service_hours: "24x7x365"

  availability:
    target: 99.9%
    measurement: "Monthly, excluding planned maintenance"
    exclusions:
      - "Planned maintenance (max 4 hours/month, announced 48h ahead)"
      - "Force majeure events"

  performance:
    order_api_p95_latency: "< 2 seconds"
    payment_api_p95_latency: "< 3 seconds"
    menu_api_p95_latency: "< 500 milliseconds"

  incident_response:
    P1: { response: "15 min", resolution: "4 hours" }
    P2: { response: "30 min", resolution: "8 hours" }
    P3: { response: "2 hours", resolution: "24 hours" }
    P4: { response: "4 hours", resolution: "48 hours" }

  penalties:
    below_99_9: "5% service credit"
    below_99_5: "10% service credit"
    below_99_0: "20% service credit"

  reporting:
    frequency: "Monthly"
    metrics: ["Availability %", "P95 Latency", "Incident count by priority", "SLA compliance %"]
```

---

## Service Request Management

### Handling Standard User Requests

**Purpose:** Support the agreed quality of a service by handling all predefined, user-initiated service requests.

| Request Type | Example | Fulfillment Time |
|-------------|---------|-----------------|
| **Access** | New team member needs Grafana access | 4 hours |
| **Information** | "What is the API rate limit?" | 2 hours |
| **Provision** | New staging environment needed | 2 business days |
| **Standard Change** | Deploy to staging | 1 hour (automated) |

### Request Fulfillment Flow

```
User submits ──> Auto-categorize ──> Approve (if needed) ──> Fulfill ──> Close
   request          & route              (manager)          (auto/manual)
```

**FoodExpress Examples:**
- "I need read-only access to production Grafana" -- auto-approved, provisioned via ServiceNow
- "Please create a new namespace for load testing" -- manager approval, then automated
- "We need a new API key for restaurant partner ABC" -- security team approval required

---

## Service Validation & Testing

### Ensuring Quality Before Release

**Purpose:** Ensure new or changed products and services meet defined requirements.

```
┌──────────────────────────────────────────────────────┐
│         Testing Pyramid for FoodExpress              │
│                                                      │
│                    ▲                                  │
│                   / \     E2E Tests                   │
│                  /   \    (Selenium, Cypress)         │
│                 /     \   "Order flow works"          │
│                /───────\                              │
│               / Integr. \  API & Integration Tests   │
│              /  Tests    \ "Services communicate"    │
│             /─────────────\                          │
│            /   Unit Tests  \  Component Tests        │
│           /                 \ "Discount calc is      │
│          /                   \  correct"             │
│         /─────────────────────\                      │
│                                                      │
│  Also:                                               │
│  - Performance testing (k6, JMeter)                  │
│  - Security testing (OWASP ZAP, SonarQube)          │
│  - Chaos testing (fault injection)                   │
│  - Smoke testing (post-deployment health checks)     │
└──────────────────────────────────────────────────────┘
```

---

## ITIL Practices Integration

### How Practices Work Together

```
Customer reports slow orders
         │
    ┌────▼─────┐
    │ Incident │  INC-2026-0460: "Orders taking 30+ seconds"
    │ Mgmt     │  Priority: P2
    └────┬─────┘
         │ Pattern detected: 5 similar incidents this week
    ┌────▼─────┐
    │ Problem  │  PRB-2026-0025: "Recurring order latency"
    │ Mgmt     │  Root cause: Missing DB index
    └────┬─────┘
         │ Fix identified
    ┌────▼─────┐
    │ Change   │  CHG-2026-0092: "Add index on orders.created_at"
    │ Control  │  Type: Normal, Risk: Low
    └────┬─────┘
         │ Approved by CAB
    ┌────▼─────┐
    │ Release  │  Released in v2.3.2 via canary deployment
    │ Mgmt     │  Validated with performance tests
    └────┬─────┘
         │ Service updated
    ┌────▼─────┐
    │ Service  │  Update CMDB: order-service v2.3.2
    │ Config   │  Update service catalog entry
    └────┬─────┘
         │ Verify improvement
    ┌────▼─────┐
    │ Service  │  SLA compliance improved from 92% to 98%
    │ Level    │  P95 latency reduced from 8s to 400ms
    └──────────┘
```

---

## ITIL Practices: Quick Reference Card

### Cheat Sheet for Sustain Engineers

| Situation | Practice | First Action |
|-----------|---------|-------------|
| Service is down | Incident Management | Create INC, set priority, assign |
| Same incident keeps recurring | Problem Management | Create PRB, do root cause analysis |
| Need to deploy a fix | Change Control | Create CHG, assess risk, get approval |
| Customer requests access | Service Request | Create RITM, route for fulfillment |
| Planning for Diwali traffic | Capacity Management | Forecast demand, plan scaling |
| New service launching | Service Design | Create SDP, define SLA, update catalog |
| Certificate expiring next week | IT Asset Management | Track expiry, plan renewal change |
| Alerts firing but no impact | Monitoring & Event | Classify as Warning, tune threshold |

---

## Continual Improvement: The CSI Approach

### Always Getting Better

```
┌──────────────────────────────────────────────────────┐
│        Continual Service Improvement                 │
│                                                      │
│  ┌──────────────────────────────────┐               │
│  │  What is the vision?            │  Business      │
│  │  (Be the #1 food delivery app)  │  alignment     │
│  └────────────┬─────────────────────┘               │
│               ▼                                      │
│  ┌──────────────────────────────────┐               │
│  │  Where are we now?              │  Baseline      │
│  │  (99.7% availability, P1 MTTR   │  assessment    │
│  │   = 2.5 hours)                  │                │
│  └────────────┬─────────────────────┘               │
│               ▼                                      │
│  ┌──────────────────────────────────┐               │
│  │  Where do we want to be?        │  Measurable    │
│  │  (99.9% availability, P1 MTTR   │  targets       │
│  │   < 1 hour)                     │                │
│  └────────────┬─────────────────────┘               │
│               ▼                                      │
│  ┌──────────────────────────────────┐               │
│  │  How do we get there?           │  Improvement   │
│  │  (Auto-remediation, better      │  plan          │
│  │   alerting, chaos testing)      │                │
│  └────────────┬─────────────────────┘               │
│               ▼                                      │
│  ┌──────────────────────────────────┐               │
│  │  Did we get there?              │  Metrics       │
│  │  (Monthly SLA review)           │  & feedback    │
│  └──────────────────────────────────┘               │
└──────────────────────────────────────────────────────┘
```

---

## ITIL 4: The Four Dimensions

### A Holistic View of Service Management

```
┌──────────────────────────────────────────────────────┐
│           Four Dimensions of ITIL 4                  │
│                                                      │
│        Organizations                                 │
│        & People                                      │
│           ▲                                          │
│           │                                          │
│  Information   ◄──── VALUE ────►  Partners           │
│  & Technology        (center)     & Suppliers        │
│           │                                          │
│           ▼                                          │
│        Value Streams                                 │
│        & Processes                                   │
│                                                      │
│  FoodExpress Examples:                               │
│  1. Orgs & People: SRE team structure, on-call rota │
│  2. Info & Tech: Prometheus, Kubernetes, ServiceNow │
│  3. Partners: AWS, Razorpay, Twilio                 │
│  4. Value Streams: Incident → Problem → Change      │
└──────────────────────────────────────────────────────┘
```

---

## ITIL and DevOps: Better Together

### Complementary, Not Competing

| ITIL Strength | DevOps Strength | Combined Benefit |
|--------------|----------------|-----------------|
| Process governance | Automation | Automated change approval for low-risk |
| Risk management | Continuous delivery | Safe, fast deployments |
| Stakeholder communication | Monitoring & feedback | Data-driven service reviews |
| Knowledge management | Infrastructure as Code | Self-documenting infrastructure |
| Service design | Microservices | Well-designed, independently deployable |

```
┌──────────────────────────────────────────────────┐
│  FoodExpress: ITIL + DevOps Integration          │
│                                                  │
│  Standard Change + CI/CD = Auto-deploy patches  │
│  Incident Mgmt + PagerDuty = Fast response      │
│  Problem Mgmt + Chaos Eng = Proactive fixes     │
│  Service Level + SLO Dashboards = Real-time SLA │
│  CMDB + Terraform = Auto-updated inventory      │
└──────────────────────────────────────────────────┘
```

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Availability Management | Measure with MTBF, MTRS; proactively eliminate SPOFs |
| Business Analysis | Translate business needs into IT requirements with measurable success criteria |
| Capacity & Performance | Plan for peak demand (Diwali traffic); monitor CPU, memory, connections, disk |
| Change Control | Three types (Standard, Normal, Emergency); use the 7 Rs before every change |
| Incident Management | Maturity levels: Reactive > Responsive > Proactive > Predictive |
| IT Asset Management | Track full lifecycle in CMDB; know your dependencies |
| Monitoring & Event | Classify events: Informational, Warning, Exception; only exceptions create incidents |
| Problem Management | Incident = symptom, Problem = root cause; use 5 Whys, Fishbone diagrams |
| Release Management | Semantic versioning; deployment strategies: rolling, blue-green, canary |
| Service Catalog | Single source of truth for all services, SLAs, owners, and dependencies |
| Service Configuration | Track CIs and their relationships; critical for impact analysis |
| Service Continuity | DR tiers based on criticality; define RTO and RPO for each service |
| Service Design | Four Ps: People, Processes, Products, Partners |
| Service Desk | Single point of contact; measure FCR, AHT, CSAT |
| Service Level Management | SLA > OLA > UC hierarchy; SLA only as strong as weakest link |
| Service Request | Pre-defined, user-initiated requests; automate where possible |
| Validation & Testing | Testing pyramid; include performance, security, and chaos testing |

> **Next: Module 36 -- ServiceNow**
