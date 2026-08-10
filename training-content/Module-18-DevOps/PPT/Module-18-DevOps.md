# DevOps Fundamentals
## Module 18 | Sustain Engineering Training | Day 19

---

## Agenda

| # | Topic |
|---|-------|
| 01 | Why DevOps? The Problem It Solves |
| 02 | DevOps Mindset & Culture |
| 03 | The 7 C's of DevOps |
| 04 | SCM & Version Control Concepts |
| 05 | CI/CD Pipeline Overview |
| 06 | Automation in DevOps |
| 07 | DevOps Pipeline Deep Dive |
| 08 | WSDL & Web Services in DevOps Context |
| 09 | DevOps Tools Ecosystem |
| 10 | Lab & Wrap-up |

---

## The World Before DevOps

### The "Wall of Confusion"

```
 Development Team          |  WALL  |         Operations Team
                           |        |
 "Here's the code,         |   OF   |    "It doesn't work
  it works on my           |        |     in production!"
  machine!"                |CONFUSN |
                           |        |
 Focus: Features           |        |    Focus: Stability
 Speed of delivery         |        |    Uptime & reliability
```

- Dev and Ops had **conflicting goals**
- Deployments were manual, risky, and infrequent
- Feedback loops were weeks or months long

---

## The Cost of Silos

### Traditional Software Delivery

| Problem | Impact |
|---------|--------|
| Manual deployments | Hours of downtime per release |
| No shared ownership | "Not my problem" culture |
| Infrequent releases | Big-bang deployments with high risk |
| Late testing | Bugs found in production |
| No monitoring feedback | Slow incident response |

**FoodExpress example:** Before DevOps, FoodExpress deployed once a month. Each deployment took 8 hours and caused 30 minutes of downtime. Customer complaints spiked after every release.

---

## What Is DevOps?

### Definition

> **DevOps** is a set of practices, tools, and cultural philosophies that automate and integrate the processes between software development and IT operations teams.

### Key Principles

- **Collaboration** over silos
- **Automation** over manual processes
- **Continuous improvement** over big-bang changes
- **Measurement** over guesswork
- **Sharing** knowledge across teams

---

## DevOps Is NOT Just Tools

```
                DevOps = Culture + Practices + Tools
                ┌─────────────────────────────────┐
                │           CULTURE                │
                │    Collaboration, Trust,          │
                │    Shared Responsibility          │
                │  ┌───────────────────────────┐   │
                │  │       PRACTICES            │   │
                │  │  CI/CD, IaC, Monitoring    │   │
                │  │  ┌─────────────────────┐   │   │
                │  │  │      TOOLS           │   │   │
                │  │  │ Jenkins, Docker, K8s │   │   │
                │  │  └─────────────────────┘   │   │
                │  └───────────────────────────┘   │
                └─────────────────────────────────┘
```

Tools without culture change = expensive shelfware

---

## Why DevOps? Business Value

| Metric | Without DevOps | With DevOps |
|--------|---------------|-------------|
| Deployment frequency | Monthly | Multiple/day |
| Lead time for changes | Months | Hours |
| Change failure rate | 30-50% | 0-15% |
| Mean time to recovery | Days | Minutes |
| Customer satisfaction | Low | High |

*Source: DORA State of DevOps Reports*

**FoodExpress after DevOps:** Deploys 10x daily, MTTR dropped from 4 hours to 15 minutes, customer complaints reduced by 60%.

---

## DevOps Mindset

### Cultural Shift Required

| Traditional Mindset | DevOps Mindset |
|-------------------|---------------|
| "That's not my job" | "We own this together" |
| "Don't change it, it works" | "Continuously improve" |
| "We'll test later" | "Shift left, test early" |
| "Deploy on Friday night" | "Deploy anytime with confidence" |
| "Hide failures" | "Fail fast, learn faster" |
| "Manual is fine" | "Automate everything repeatable" |

---

## The Three Ways of DevOps

### Principles from "The Phoenix Project"

```
Way 1: Flow (Left to Right)
Dev ──────────────────────────────> Ops ──────> Customer
     Fast flow of work from dev to production

Way 2: Feedback (Right to Left)
Dev <────────────────────────────── Ops <────── Customer
     Fast and constant feedback at all stages

Way 3: Continuous Learning
     ┌──────────────────────────────┐
     │  Experimentation & Learning  │
     │  Risk-taking & Repetition    │
     └──────────────────────────────┘
```

---

## CALMS Framework

| Letter | Meaning | Description |
|--------|---------|-------------|
| **C** | Culture | Shared responsibility, no blame |
| **A** | Automation | Automate builds, tests, deploys |
| **L** | Lean | Eliminate waste, small batches |
| **M** | Measurement | Metrics-driven decisions |
| **S** | Sharing | Knowledge sharing across teams |

**FoodExpress example:** The team shares post-incident reviews openly. Every outage becomes a learning opportunity, not a blame session.

---

## The 7 C's of DevOps

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  1. Continuous    2. Continuous    3. Continuous            │
│     Development      Integration     Testing               │
│        │                │               │                   │
│        ▼                ▼               ▼                   │
│  4. Continuous    5. Continuous    6. Continuous            │
│     Deployment       Monitoring      Feedback              │
│        │                │               │                   │
│        ▼                ▼               ▼                   │
│              7. Continuous Operations                       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 7 C's: Continuous Development

### Plan & Code

- Agile planning: user stories, sprint planning
- Version control: Git for all code and config
- IDE integration: linting, formatting, pre-commit hooks

```
FoodExpress Example:
├── Jira board with sprint backlog
├── Feature branches per user story
├── Code standards enforced by ESLint/Checkstyle
└── Pre-commit hooks run tests before push
```

**Tools:** Jira, Git, VS Code, IntelliJ IDEA

---

## 7 C's: Continuous Integration (CI)

### Build & Merge Frequently

- Developers merge code to main branch **multiple times per day**
- Each merge triggers an automated build
- Automated tests run on every build
- Broken builds are fixed **immediately**

```
Developer commits ──> Build triggered ──> Tests run ──> Results
     │                     │                  │            │
     │                     │                  │          Pass ✓
     │                     │                  │          Fail ✗
     │                     │                  │            │
     └─────────────────────┴──────────────────┴── Feedback
```

**FoodExpress:** Every push to `main` triggers Jenkins build + 500 unit tests in 3 minutes.

---

## 7 C's: Continuous Testing

### Test at Every Stage

| Test Type | When | Duration | Scope |
|-----------|------|----------|-------|
| Unit tests | Every commit | Seconds | Functions |
| Integration tests | Every build | Minutes | Components |
| API tests | Every build | Minutes | Endpoints |
| UI tests | Nightly | Hours | Full flows |
| Performance tests | Weekly | Hours | Load/stress |
| Security tests | Weekly | Hours | Vulnerabilities |

**Shift Left:** Find bugs earlier when they are cheaper to fix.

---

## 7 C's: Continuous Deployment

### Automated Release to Production

```
Code ──> Build ──> Test ──> Stage ──> Approve ──> Production
  │        │        │        │          │            │
  Auto     Auto     Auto     Auto    Manual/Auto    Auto
```

- **Continuous Delivery:** Automated up to staging, manual approval for production
- **Continuous Deployment:** Fully automated, every passing build goes to production

**FoodExpress:** Uses Continuous Delivery with manual approval gate for production. Feature flags control rollout.

---

## 7 C's: Continuous Monitoring

### Observe Everything in Production

- **Infrastructure:** CPU, memory, disk, network
- **Application:** Response time, error rate, throughput
- **Business:** Orders/hour, cart abandonment, revenue
- **User experience:** Page load time, bounce rate

```
FoodExpress Monitoring Dashboard:
┌──────────────────────────────────────┐
│ Orders/min: 245  │  Errors: 0.1%    │
│ Avg response: 120ms │ CPU: 45%      │
│ Active users: 1,200 │ Memory: 62%   │
└──────────────────────────────────────┘
```

**Tools:** Prometheus, Grafana, ELK Stack, Datadog

---

## 7 C's: Continuous Feedback

### Close the Loop

- Monitoring alerts feed back to development
- Customer feedback drives feature priorities
- Post-incident reviews improve processes
- Metrics inform architecture decisions

```
Production Alert ──> On-Call Engineer ──> Incident Channel
       │                    │                    │
       │              Investigate            Collaborate
       │                    │                    │
       └──> Root Cause ──> Fix ──> Deploy ──> Verify
```

---

## 7 C's: Continuous Operations

### Zero Downtime, Always Available

- Blue-green deployments
- Rolling updates
- Canary releases
- Feature flags
- Automated scaling

**FoodExpress:** Uses rolling updates in Kubernetes. New versions are deployed to 10% of pods first, monitored for 15 minutes, then rolled to 100%.

---

## SCM: Software Configuration Management

### What Is SCM?

> Managing and tracking changes to software code, configurations, and documentation throughout the development lifecycle.

### SCM Components

| Component | Purpose | Example |
|-----------|---------|---------|
| Version Control | Track code changes | Git |
| Build Management | Compile and package | Maven, npm |
| Environment Config | Manage env-specific settings | .env files, ConfigMaps |
| Release Management | Track what's deployed where | Tags, release notes |
| Change Management | Control and approve changes | PRs, JIRA workflow |

---

## Version Control: Why It Matters

### Without Version Control

```
project/
├── app_v1.js
├── app_v2.js
├── app_v2_final.js
├── app_v2_final_REAL.js
├── app_v2_final_REAL_fixed.js
└── app_v2_final_REAL_fixed_FINAL.js   ← Which one is in production?
```

### With Version Control (Git)

```
commit a1b2c3d  Fix: Price display NaN bug (FE-001)
commit d4e5f6a  Feature: Add combo meal support
commit g7h8i9j  Refactor: Extract price formatter utility
commit k0l1m2n  Initial commit
```

Every change tracked, reversible, and attributable.

---

## CI/CD Pipeline: The Assembly Line

### End-to-End Pipeline

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  CODE   │──>│  BUILD  │──>│  TEST   │──>│  STAGE  │──>│ DEPLOY  │
│         │   │         │   │         │   │         │   │         │
│ Git     │   │ Maven   │   │ JUnit   │   │ Docker  │   │ K8s     │
│ Branch  │   │ npm     │   │ Jest    │   │ Compose │   │ Helm    │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
     │              │             │              │             │
     └──────────────┴─────────────┴──────────────┴─────────────┘
                        Jenkins / GitHub Actions
```

---

## CI/CD Pipeline Example: FoodExpress

```groovy
// Jenkinsfile for FoodExpress Order Service
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/foodexpress/order-service'
            }
        }
        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker build -t foodexpress/order-service:${BUILD_NUMBER} .'
            }
        }
        stage('Deploy to Staging') {
            steps {
                sh 'kubectl apply -f k8s/staging/'
            }
        }
    }
}
```

---

## Automation in DevOps

### What to Automate

| Category | What | Tool |
|----------|------|------|
| Code quality | Linting, formatting | ESLint, Checkstyle |
| Build | Compile, package | Maven, npm, Gradle |
| Testing | Unit, integration, E2E | JUnit, Jest, Selenium |
| Security | Vulnerability scanning | SonarQube, Snyk |
| Infrastructure | Server provisioning | Terraform, Ansible |
| Deployment | Release to production | Jenkins, ArgoCD |
| Monitoring | Alerts and dashboards | Prometheus, Grafana |
| Incident | Auto-scaling, self-healing | Kubernetes |

---

## Automation: The ROI Calculation

### Should You Automate It?

```
Time saved per occurrence x Frequency = Total time saved

Example: FoodExpress deployment
- Manual deployment time: 2 hours
- Frequency: 10 deployments/week
- Manual cost: 20 hours/week

Automated deployment:
- Pipeline setup: 40 hours (one-time)
- Automated deployment time: 15 minutes
- Automated cost: 2.5 hours/week

Break-even: 40 / (20 - 2.5) = 2.3 weeks
Annual savings: 17.5 hours/week x 50 weeks = 875 hours
```

---

## Infrastructure as Code (IaC)

### Treat Infrastructure Like Application Code

```yaml
# Terraform: FoodExpress infrastructure
resource "aws_instance" "order_service" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.medium"

  tags = {
    Name        = "foodexpress-order-service"
    Environment = "production"
    Team        = "sustain-engineering"
  }
}

resource "aws_db_instance" "foodexpress_db" {
  engine         = "mysql"
  engine_version = "8.0"
  instance_class = "db.t3.medium"
  allocated_storage = 100
}
```

**Benefits:** Version controlled, repeatable, reviewable, auditable

---

## DevOps Pipeline Deep Dive

### Pipeline Stages in Detail

| Stage | Actions | Failure Action |
|-------|---------|----------------|
| **Source** | Pull code from Git, resolve dependencies | Alert developer |
| **Build** | Compile, resolve dependencies, create artifact | Fail pipeline, notify team |
| **Unit Test** | Run unit tests, code coverage check | Fail pipeline, show report |
| **Static Analysis** | SonarQube scan, security check | Warn or fail based on severity |
| **Package** | Create Docker image, push to registry | Fail pipeline |
| **Deploy Staging** | Deploy to staging environment | Rollback, notify team |
| **Integration Test** | Run E2E tests against staging | Fail pipeline |
| **Approval Gate** | Manual or automated approval | Hold until approved |
| **Deploy Production** | Rolling update to production | Auto-rollback |
| **Smoke Test** | Verify critical paths in production | Auto-rollback |

---

## Deployment Strategies

### Blue-Green Deployment

```
              Load Balancer
                   │
          ┌────────┴────────┐
          │                 │
    ┌─────▼─────┐   ┌──────▼────┐
    │   BLUE    │   │   GREEN   │
    │ (Current) │   │  (New)    │
    │  v1.0     │   │  v1.1     │
    └───────────┘   └───────────┘

Step 1: Deploy v1.1 to Green
Step 2: Test Green
Step 3: Switch traffic to Green
Step 4: Blue becomes standby
```

---

## Deployment Strategies

### Canary Release

```
              Load Balancer
                   │
          ┌────────┴────────┐
          │ 90%             │ 10%
    ┌─────▼─────┐   ┌──────▼────┐
    │  Stable   │   │  Canary   │
    │  v1.0     │   │  v1.1     │
    │ (90%)     │   │ (10%)     │
    └───────────┘   └───────────┘

Step 1: Deploy v1.1 to 10% of instances
Step 2: Monitor error rate, latency
Step 3: Gradually increase to 100%
Step 4: Rollback if metrics degrade
```

**FoodExpress:** Uses canary for payment service changes (high risk).

---

## WSDL & Web Services

### Web Services Description Language

- XML-based language for describing web service interfaces
- Defines **operations**, **messages**, and **bindings**
- Used primarily with SOAP-based web services
- Being replaced by REST + OpenAPI in modern systems

```xml
<!-- WSDL Example: FoodExpress Order Service -->
<definitions name="OrderService"
  targetNamespace="http://foodexpress.com/orders">

  <message name="CreateOrderRequest">
    <part name="customerId" type="xsd:long"/>
    <part name="items" type="tns:ItemList"/>
  </message>

  <message name="CreateOrderResponse">
    <part name="orderId" type="xsd:long"/>
    <part name="status" type="xsd:string"/>
  </message>

  <portType name="OrderPortType">
    <operation name="createOrder">
      <input message="tns:CreateOrderRequest"/>
      <output message="tns:CreateOrderResponse"/>
    </operation>
  </portType>
</definitions>
```

---

## WSDL vs REST/OpenAPI

| Feature | WSDL/SOAP | REST/OpenAPI |
|---------|-----------|-------------|
| Protocol | SOAP (XML) | HTTP (JSON) |
| Description | WSDL (XML) | OpenAPI (YAML/JSON) |
| Complexity | High | Low |
| Performance | Slower (XML parsing) | Faster (JSON) |
| Error handling | SOAP Faults | HTTP status codes |
| Tooling | Heavy (generated clients) | Light (curl, Postman) |
| Use case | Enterprise, legacy | Modern APIs, microservices |

**FoodExpress context:** Legacy payment gateway uses SOAP/WSDL. New services use REST. Sustain engineers must handle both.

---

## DevOps Tools Ecosystem

### Categorized Tool Landscape

| Category | Tools |
|----------|-------|
| **Source Control** | Git, GitHub, GitLab, Bitbucket |
| **CI/CD** | Jenkins, GitHub Actions, GitLab CI, CircleCI |
| **Containerization** | Docker, Podman |
| **Orchestration** | Kubernetes, Docker Swarm |
| **Config Management** | Ansible, Chef, Puppet |
| **IaC** | Terraform, CloudFormation, Pulumi |
| **Monitoring** | Prometheus, Grafana, Datadog, New Relic |
| **Logging** | ELK Stack, Splunk, Loki |
| **Security** | SonarQube, Snyk, Trivy |
| **Collaboration** | Slack, Teams, PagerDuty |

---

## DevOps in Sustain Engineering

### Why DevOps Matters for Sustain Teams

| Sustain Activity | DevOps Practice |
|-----------------|-----------------|
| Bug fixes | CI/CD for rapid, safe deployment |
| Production incidents | Monitoring + alerting + runbooks |
| Performance issues | Observability + auto-scaling |
| Security patches | Automated vulnerability scanning |
| Configuration changes | IaC + version control |
| Knowledge transfer | Documentation as code |

**FoodExpress sustain team uses:** Jenkins for CI/CD, Docker for containers, Kubernetes for orchestration, Prometheus/Grafana for monitoring.

---

## DevOps Maturity Model

| Level | Description | FoodExpress Status |
|-------|-------------|-------------------|
| **Level 1: Initial** | Manual processes, no CI/CD | Was here 2 years ago |
| **Level 2: Managed** | Basic CI, some automation | Passed this stage |
| **Level 3: Defined** | CI/CD pipeline, IaC, monitoring | Currently here |
| **Level 4: Measured** | Metrics-driven, SLOs, error budgets | Working toward |
| **Level 5: Optimized** | Self-healing, chaos engineering | Future goal |

---

## DevOps Anti-Patterns

| Anti-Pattern | Description | Fix |
|-------------|-------------|-----|
| "DevOps Team" | Creating a separate DevOps silo | Embed practices in all teams |
| Tool obsession | Buying tools without culture change | Start with culture, then tools |
| Automation theater | Automating bad processes | Fix the process first |
| Metric gaming | Optimizing metrics, not outcomes | Align metrics with business goals |
| "Works on my machine" | No environment parity | Use containers + IaC |

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Why DevOps | Breaks down silos, enables fast, reliable delivery |
| DevOps Mindset | Culture of collaboration, shared ownership, continuous improvement |
| 7 C's | Continuous Development, Integration, Testing, Deployment, Monitoring, Feedback, Operations |
| CI/CD | Automated pipeline from code to production |
| Automation | Automate everything repeatable; calculate ROI |
| IaC | Infrastructure as version-controlled code |
| WSDL | Legacy web service description; modern = REST + OpenAPI |
| Sustain relevance | DevOps practices enable rapid, safe production changes |

> **Next: Module 19 -- Git & GitHub**
