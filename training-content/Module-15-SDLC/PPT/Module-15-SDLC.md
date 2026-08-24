# SDLC Fundamentals
## Module 15 | Sustain Engineering Training | Day 16

**1 day | Lecture + exercises + group discussion**

---

## Agenda

| Session | Topics |
|---------|--------|
| First half | SDLC Overview, Stages, Waterfall, Agile (Scrum, Kanban), DevOps |
| Second half | Requirement Documents (SRS, BRD, FRD), STLC, Application Types, Dev/Test/Prod Environments |

> Understanding how software is built, tested, and delivered -- the lifecycle that sustain engineers support.

---

## What Is SDLC?

### Definition
**Software Development Life Cycle (SDLC)** is a structured process for planning, creating, testing, deploying, and maintaining software applications.

### Why Sustain Engineers Must Understand SDLC
- You inherit code at **any stage** of its lifecycle
- Understanding the original development process helps you:
  - Find documentation and design decisions
  - Understand why code was written a certain way
  - Follow the correct process for making changes
  - Coordinate with QA, ops, and product teams

---

## SDLC Stages

```
+------------+     +---------+     +----------+     +----------+
| 1. Planning| --> | 2.Analysis| --> | 3. Design| --> | 4. Build |
+------------+     +---------+     +----------+     +----------+
                                                         |
+------------+     +---------+     +----------+          |
| 7. Retire  | <-- | 6.Maintain| <-- | 5. Test &| <--------+
+------------+     +---------+     |   Deploy |
                                   +----------+
```

| Stage | Description | FoodExpress Example |
|-------|-------------|---------------------|
| **1. Planning** | Define goals, scope, timeline, budget | "Build a food delivery app for Bangalore" |
| **2. Analysis** | Gather requirements, feasibility study | Interview restaurants, customers, delivery partners |
| **3. Design** | Architecture, UI/UX, database design | Microservices architecture, React frontend |
| **4. Build** | Write code, develop features | Sprint-based development of order service |
| **5. Test & Deploy** | QA testing, staging, production release | Regression testing, blue-green deployment |
| **6. Maintain** | Bug fixes, updates, monitoring | **Sustain engineering!** |
| **7. Retire** | End-of-life, migration, decommission | Replace legacy order system |

---

## Stage 1: Planning

### Activities
- Define project vision and business objectives
- Identify stakeholders
- Estimate timeline and budget
- Risk assessment
- Resource allocation

### Key Outputs

| Document | Purpose |
|----------|---------|
| **Project Charter** | High-level scope, objectives, stakeholders |
| **Project Plan** | Timeline, milestones, resource plan |
| **Risk Register** | Identified risks with mitigation plans |
| **Budget Estimate** | Cost breakdown by phase |

### FoodExpress Planning Example
```
Project: FoodExpress v2.0
Goal: Support 10,000 concurrent users in 3 cities
Timeline: 6 months (Jan - Jun 2026)
Budget: $500,000
Key Risk: Payment gateway integration delays
```

---

## Stage 2: Requirements Analysis

### Types of Requirements

| Type | Description | FoodExpress Example |
|------|-------------|---------------------|
| **Functional** | What the system should DO | "User can search restaurants by cuisine" |
| **Non-Functional** | How the system should PERFORM | "Search results load in < 2 seconds" |
| **Business** | Why the system is needed | "Increase order volume by 30% in Q2" |
| **Technical** | Technical constraints | "Must run on AWS, Node.js backend" |
| **User** | End-user needs | "Customer can track delivery in real-time" |

### Requirements Gathering Techniques

| Technique | Description | When to Use |
|-----------|-------------|-------------|
| **Interviews** | 1-on-1 with stakeholders | Complex requirements, subject matter expertise |
| **Surveys** | Questionnaires to large groups | User preferences, feature prioritization |
| **Workshops** | Group brainstorming sessions | Cross-functional requirements |
| **Prototyping** | Build quick mockups | UI/UX requirements, unclear requirements |
| **Document Analysis** | Review existing systems | Sustain: understanding legacy systems |
| **Observation** | Watch users work | Usability requirements |

---

## Requirement Documents

### BRD -- Business Requirements Document

| Section | Content | FoodExpress Example |
|---------|---------|---------------------|
| **Business Objectives** | Why this project exists | Expand to 3 new cities by Q3 |
| **Scope** | What is included/excluded | Order management, NOT delivery fleet management |
| **Stakeholders** | Who is involved | Product, Engineering, Ops, Restaurant Partners |
| **Success Criteria** | How to measure success | 10,000 daily orders, < 2% error rate |
| **Constraints** | Limitations | Budget: $500K, Timeline: 6 months |
| **Assumptions** | What we assume to be true | Restaurants have internet connectivity |

### BRD vs SRS vs FRD

| Document | Audience | Detail Level | Focus |
|----------|----------|-------------|-------|
| **BRD** | Business stakeholders | High-level | WHY and WHAT (business) |
| **SRS** | Technical team | Detailed | WHAT (system behavior) |
| **FRD** | Developers | Very detailed | HOW (functional specs) |

---

## SRS -- Software Requirements Specification

### Structure

| Section | Content |
|---------|---------|
| **1. Introduction** | Purpose, scope, definitions |
| **2. Overall Description** | Product perspective, user characteristics, constraints |
| **3. Functional Requirements** | Detailed feature descriptions with inputs/outputs |
| **4. Non-Functional Requirements** | Performance, security, availability targets |
| **5. Interface Requirements** | UI, API, hardware, software interfaces |
| **6. Data Requirements** | Database schema, data flow, data retention |

### FoodExpress SRS Example (Excerpt)

```
FR-001: Place Order
  Description: Customer can place a food order from a restaurant
  Input: customer_id, restaurant_id, items[], payment_method
  Process:
    1. Validate customer and restaurant exist and are active
    2. Validate all items are available
    3. Calculate total (items + tax + delivery fee)
    4. Process payment
    5. Create order record
    6. Send confirmation notification
  Output: order_id, estimated_delivery_time
  Error Cases:
    - E1: Restaurant is closed -> Error 400
    - E2: Item out of stock -> Error 400
    - E3: Payment fails -> Error 402
```

---

## FRD -- Functional Requirements Document

### FoodExpress FRD Example

| Req ID | Feature | Description | Acceptance Criteria | Priority |
|--------|---------|-------------|---------------------|----------|
| FRD-001 | Restaurant Search | Search by name, cuisine, rating | Returns results in < 2s, supports pagination | P1 |
| FRD-002 | Menu Display | Show restaurant menu with prices | Grouped by category, shows availability | P1 |
| FRD-003 | Cart Management | Add/remove items, update quantities | Persists across sessions, max 20 items | P1 |
| FRD-004 | Order Placement | Submit order with payment | Atomic transaction, confirmation sent | P1 |
| FRD-005 | Order Tracking | Real-time delivery status | GPS tracking, ETA updates every 30s | P2 |
| FRD-006 | Order History | View past orders, re-order | Paginated, filterable by date/status | P2 |
| FRD-007 | Rating/Review | Rate restaurant and delivery | 1-5 stars, optional text, one per order | P3 |

---

## SDLC Methodologies

### Overview

| Methodology | Approach | Feedback Loop | Best For |
|-------------|----------|---------------|----------|
| **Waterfall** | Sequential phases | End of project | Fixed requirements, regulated industries |
| **Agile (Scrum)** | Iterative sprints | Every 2-4 weeks | Evolving requirements, fast delivery |
| **Agile (Kanban)** | Continuous flow | Continuous | Operations, sustain work, support |
| **DevOps** | Dev + Ops integration | Continuous | Rapid deployment, high reliability |
| **Spiral** | Risk-driven iterations | Each iteration | High-risk, complex projects |
| **V-Model** | Verification & validation | Each phase paired | Safety-critical systems |

---

## Waterfall Model

```
+------------------+
| 1. Requirements  |
+--------+---------+
         |
+--------v---------+
| 2. System Design |
+--------+---------+
         |
+--------v---------+
| 3. Implementation|
+--------+---------+
         |
+--------v---------+
| 4. Testing       |
+--------+---------+
         |
+--------v---------+
| 5. Deployment    |
+--------+---------+
         |
+--------v---------+
| 6. Maintenance   |
+------------------+
```

### Characteristics

| Aspect | Description |
|--------|-------------|
| **Flow** | Linear, sequential -- each phase completes before next starts |
| **Requirements** | Must be fully defined upfront |
| **Changes** | Expensive and difficult after phase completion |
| **Documentation** | Heavy -- each phase produces documents |
| **Testing** | Happens after development is complete |
| **Delivery** | Single release at the end |

### When to Use Waterfall
- Requirements are well-understood and unlikely to change
- Regulatory/compliance environments (medical, aviation)
- Short projects with fixed scope
- Contracts with fixed deliverables

---

## Agile -- Scrum

### Scrum Framework

```
Product        Sprint        Sprint       Sprint      Potentially
Backlog   -->  Planning  --> Backlog  --> Execution -->  Shippable
(all work)     (select)     (sprint)    (2-4 weeks)    Increment
                                             |
                                      Daily Standup
                                      (15 min/day)
                                             |
                                      Sprint Review
                                      Sprint Retro
```

### Scrum Roles

| Role | Responsibility | FoodExpress Example |
|------|---------------|---------------------|
| **Product Owner** | Prioritizes backlog, defines acceptance criteria | Decides next features for FoodExpress |
| **Scrum Master** | Facilitates process, removes blockers | Ensures team follows sprint commitments |
| **Development Team** | Builds the product increment | Developers, testers, designers (3-9 people) |

### Scrum Events

| Event | Duration | Purpose |
|-------|----------|---------|
| **Sprint Planning** | 2-4 hours | Select stories for the sprint |
| **Daily Standup** | 15 minutes | What did I do? What will I do? Any blockers? |
| **Sprint Review** | 1-2 hours | Demo completed work to stakeholders |
| **Sprint Retrospective** | 1-1.5 hours | What went well? What to improve? |

---

## Agile -- Scrum Artifacts

### Product Backlog

| Priority | Story | Points | Status |
|----------|-------|--------|--------|
| P1 | As a customer, I can search restaurants by cuisine | 5 | Done |
| P1 | As a customer, I can place an order | 8 | In Sprint |
| P2 | As a customer, I can track my delivery | 13 | Backlog |
| P2 | As a restaurant, I can update my menu | 5 | Backlog |
| P3 | As a customer, I can rate my order | 3 | Backlog |

### User Story Format

```
As a [role],
I want to [action],
So that [benefit].

Acceptance Criteria:
- Given [context], when [action], then [result]
- Given [context], when [action], then [result]
```

### FoodExpress User Story Example

```
As a hungry customer,
I want to search restaurants by cuisine type,
So that I can quickly find what I want to eat.

Acceptance Criteria:
- Given I am on the search page, when I select "Indian",
  then I see only Indian restaurants
- Given I search for "Italian", when no Italian restaurants
  exist in my area, then I see "No restaurants found"
- Given search results load, they must appear within 2 seconds
```

---

## Agile -- Kanban

### Kanban Board

```
+----------+-----------+-----------+----------+---------+
| Backlog  | To Do     | In Prog   | Review   | Done    |
+----------+-----------+-----------+----------+---------+
| Story 8  | Story 5   | Story 3   | Story 2  | Story 1 |
| Story 9  | Story 6   | Story 4   |          |         |
| Story 10 |           |           |          |         |
| Story 11 |           |           |          |         |
+----------+-----------+-----------+----------+---------+
                        WIP Limit=2  WIP Limit=1
```

### Kanban Principles

| Principle | Description |
|-----------|-------------|
| **Visualize work** | Board shows all work items and their status |
| **Limit WIP** | Cap work-in-progress to prevent overload |
| **Manage flow** | Optimize for smooth, continuous delivery |
| **Make policies explicit** | Define "done", WIP limits, priority rules |
| **Continuous improvement** | Regularly review and optimize the process |

### Kanban vs Scrum

| Aspect | Scrum | Kanban |
|--------|-------|--------|
| **Cadence** | Fixed sprints (2-4 weeks) | Continuous flow |
| **Roles** | PO, SM, Dev Team | No prescribed roles |
| **Planning** | Sprint planning every sprint | Continuous replenishment |
| **Changes** | Avoid mid-sprint changes | Changes welcome anytime |
| **Best for** | Feature development | Sustain, support, ops |

---

## DevOps

### What Is DevOps?

> DevOps is a **culture and set of practices** that brings Development and Operations together to deliver software faster, more reliably, and with higher quality.

### DevOps Infinity Loop

```
        PLAN --> CODE --> BUILD --> TEST
       /                                \
MONITOR                                 RELEASE
       \                                /
        OPERATE <-- DEPLOY <-- (gate)
```

### DevOps Principles

| Principle | Description | FoodExpress Example |
|-----------|-------------|---------------------|
| **Culture** | Dev + Ops collaborate, shared responsibility | Developers on-call for their services |
| **Automation** | Automate everything repeatable | CI/CD pipeline, infrastructure as code |
| **Measurement** | Data-driven decisions | Deployment frequency, lead time, MTTR |
| **Sharing** | Share knowledge, tools, responsibilities | Shared runbooks, post-incident reviews |
| **Continuous Improvement** | Always getting better | Blameless postmortems, action items |

---

## DevOps Practices

| Practice | Description | FoodExpress Example |
|----------|-------------|---------------------|
| **CI** | Merge code frequently, auto-build and test | Every PR triggers build + unit tests |
| **CD** | Auto-deploy to staging/production | Merged code deploys to staging in 10 min |
| **IaC** | Infrastructure defined in code | Terraform for AWS resources |
| **Monitoring** | Observe system health continuously | Datadog dashboards, PagerDuty alerts |
| **Containerization** | Package apps in containers | Docker for all microservices |
| **Orchestration** | Manage containers at scale | Kubernetes cluster |
| **ChatOps** | Operations via chat tools | Slack bot for deployments, alerts |
| **Feature Flags** | Toggle features without deployment | Enable loyalty program for 10% of users |

### DORA Metrics

| Metric | Definition | Elite Level |
|--------|-----------|-------------|
| **Deployment Frequency** | How often you deploy | Multiple per day |
| **Lead Time** | Code commit to production | < 1 hour |
| **Change Failure Rate** | % of deployments causing failure | < 5% |
| **MTTR** | Time to recover from failure | < 1 hour |

---

## STLC -- Software Testing Life Cycle

```
+-------------------+
| 1. Requirement    |
|    Analysis       |
+---------+---------+
          |
+---------v---------+
| 2. Test Planning  |
+---------+---------+
          |
+---------v---------+
| 3. Test Case      |
|    Design         |
+---------+---------+
          |
+---------v---------+
| 4. Environment    |
|    Setup          |
+---------+---------+
          |
+---------v---------+
| 5. Test           |
|    Execution      |
+---------+---------+
          |
+---------v---------+
| 6. Test Closure   |
+-------------------+
```

### STLC Stages

| Stage | Activities | Outputs |
|-------|-----------|---------|
| **Requirement Analysis** | Review SRS/FRD, identify testable requirements | Requirements Traceability Matrix (RTM) |
| **Test Planning** | Define scope, strategy, resources, schedule | Test Plan document |
| **Test Case Design** | Write test cases, prepare test data | Test cases, test scripts |
| **Environment Setup** | Configure test environments, tools | Ready test environment |
| **Test Execution** | Run tests, log results, report defects | Test results, defect reports |
| **Test Closure** | Evaluate exit criteria, lessons learned | Test summary report, metrics |

---

## Application Types

### Types and Characteristics

| Type | Description | FoodExpress Example |
|------|-------------|---------------------|
| **Web Application** | Browser-based, client-server | Customer-facing ordering website |
| **Mobile App** | Native or hybrid mobile | iOS/Android ordering app |
| **API/Microservice** | Backend service with API | Order Service, Restaurant Service |
| **Single Page App (SPA)** | Client-side rendered web app | React-based restaurant dashboard |
| **Desktop Application** | Installed on user's computer | Restaurant POS system |
| **Batch Application** | Scheduled processing | Nightly revenue report generation |
| **Real-time Application** | Live data processing | Delivery tracking, live chat |

### Architecture Patterns

| Pattern | Description | Pros | Cons |
|---------|-------------|------|------|
| **Monolith** | Single deployable unit | Simple, easy to develop | Hard to scale, tight coupling |
| **Microservices** | Independent services | Scalable, independent deployment | Complex, distributed systems |
| **Serverless** | Function-based | No server management, auto-scale | Cold starts, vendor lock-in |
| **Event-Driven** | Async message processing | Loose coupling, scalable | Eventually consistent, debugging hard |

---

## Development Environments

### Environment Pipeline

```
+--------+     +--------+     +---------+     +-----------+     +------+
|  Local | --> |  Dev   | --> | Staging | --> | Pre-Prod  | --> | Prod |
+--------+     +--------+     +---------+     +-----------+     +------+
Developer's    Shared dev     Mirrors          Final              Live
machine        environment    production       validation         users
```

### Environment Comparison

| Aspect | Local | Dev | Staging | Pre-Prod | Production |
|--------|-------|-----|---------|----------|------------|
| **Purpose** | Development | Integration | Testing | Final check | Live users |
| **Data** | Mock/seed | Synthetic | Subset of prod | Anonymized prod | Real data |
| **Users** | Developer | Dev team | QA team | Stakeholders | Everyone |
| **Infra** | Laptop | Shared server | Prod-like | Identical to prod | Full scale |
| **Deployment** | Manual | Auto (CI) | Auto (CD) | Manual gate | Approved only |
| **Monitoring** | Console logs | Basic | Full | Full | Full + alerting |

---

## Environment Details

### Local Development Environment

```
Developer's Laptop:
+----------------------------+
| IDE (VS Code / IntelliJ)   |
| Node.js / Java runtime     |
| Docker Desktop             |
|  +--------+ +--------+    |
|  | MySQL  | | MongoDB|    |
|  |(Docker)| |(Docker)|    |
|  +--------+ +--------+    |
| Git, npm, Postman          |
+----------------------------+
```

### Staging Environment

```
Staging (mirrors production):
- Same cloud provider (AWS)
- Same architecture (load balancer + 2 app servers + DB)
- Smaller instance sizes (cost savings)
- Synthetic test data (not real customer data)
- Full monitoring and logging
- Used by QA team for integration and regression testing
```

### Production Environment

```
Production:
- Full-scale infrastructure
- Real customer data (encrypted, access-controlled)
- Full monitoring, alerting, on-call rotation
- Change management process for all deployments
- Backup and disaster recovery configured
- Performance-tuned and load-tested
```

---

## Environment Management Best Practices

| Practice | Why | How |
|----------|-----|-----|
| **Parity** | Reduce "works on my machine" issues | Use containers, IaC to match environments |
| **Data isolation** | Prevent test data in production | Separate databases, never share |
| **Access control** | Limit who can change what | RBAC: developers can deploy to dev, only ops deploys to prod |
| **Configuration** | Same code, different config per env | Environment variables, config files |
| **Promotion** | Code moves up, never down | Local -> Dev -> Staging -> Prod |
| **Refresh** | Keep staging data realistic | Periodically refresh staging from anonymized prod data |

### Environment Variables Example

```javascript
// Same code, different config per environment
// .env.development
DB_HOST=localhost
DB_NAME=foodexpress_dev
LOG_LEVEL=debug

// .env.staging
DB_HOST=staging-db.internal
DB_NAME=foodexpress_staging
LOG_LEVEL=info

// .env.production
DB_HOST=prod-db.internal
DB_NAME=foodexpress
LOG_LEVEL=warn
```

---

## SDLC in Sustain Engineering Context

### Where Sustain Fits

```
SDLC Stages:
Plan -> Analyze -> Design -> Build -> Test -> Deploy -> MAINTAIN -> Retire
                                                        ^^^^^^^^
                                                     YOU ARE HERE
```

### Sustain Engineer's SDLC Activities

| SDLC Stage | Sustain Activity |
|------------|-----------------|
| **Planning** | Sprint planning for bug fixes and enhancements |
| **Analysis** | Read requirements docs to understand expected behavior |
| **Design** | Review architecture docs, understand dependencies |
| **Build** | Fix bugs, add small features, refactor |
| **Test** | Add regression tests, verify fixes |
| **Deploy** | Follow change management, deploy fixes |
| **Maintain** | Monitor, respond to incidents, performance tune |

### Sustain Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|-------------|---------|-----------------|
| "Quick fix" without understanding | Introduces new bugs | Read the code, understand the system |
| No documentation | Knowledge lost when team changes | Document every fix and its root cause |
| Skip testing | Regression bugs | Add a test for every bug fix |
| Direct production fix | Untracked changes | Always go through Dev -> Staging -> Prod |
| Ignore monitoring | Miss early warnings | Set up alerts, check dashboards daily |

---

## Change Management in Sustain

### Change Types

| Type | Description | Example | Approval |
|------|-------------|---------|----------|
| **Standard** | Pre-approved, low-risk | Config change, restart | No approval needed |
| **Normal** | Planned, moderate risk | Bug fix deployment | CAB approval |
| **Emergency** | Urgent, production impact | Critical security patch | Emergency CAB |

### Change Process

```
1. Request  --> 2. Assess  --> 3. Approve  --> 4. Implement
(RFC)           (Impact,        (CAB vote)      (Deploy)
                Risk,
                Rollback plan)

5. Review   --> 6. Close
(Post-impl      (Document
verification)   outcome)
```

### FoodExpress Change Example

```
Change Request: FOOD-CR-042
Type: Normal
Description: Fix order total calculation (Bug FOOD-156)
Impact: Order service, payment service
Risk: Medium (affects revenue calculation)
Rollback Plan: Revert to previous Docker image
Testing: Unit tests + staging verification
Approval: CAB approved on 2026-07-25
Deploy Window: 2026-07-27, 02:00-04:00 AM
```

---

## Methodologies Comparison Summary

| Aspect | Waterfall | Scrum | Kanban | DevOps |
|--------|-----------|-------|--------|--------|
| **Approach** | Sequential | Iterative | Continuous | Continuous |
| **Planning** | Upfront, detailed | Sprint-level | Just-in-time | Continuous |
| **Changes** | Difficult | Between sprints | Anytime | Anytime |
| **Delivery** | End of project | End of sprint | Continuous | Continuous |
| **Feedback** | Late | Every 2-4 weeks | Real-time | Real-time |
| **Documentation** | Heavy | Light | Minimal | As needed |
| **Team Size** | Large | 3-9 | Any | Cross-functional |
| **Best For** | Fixed scope | New features | Sustain/ops | High velocity |
| **Risk** | Late discovery | Scope creep | No deadlines | Complexity |

---

## Key Takeaways

| Concept | Key Lesson |
|---------|------------|
| SDLC Stages | Plan -> Analyze -> Design -> Build -> Test -> Deploy -> Maintain -> Retire |
| Waterfall | Sequential, heavy documentation, fixed scope -- good for regulated environments |
| Scrum | Iterative sprints (2-4 weeks), roles (PO, SM, Team), ceremonies (standup, review, retro) |
| Kanban | Continuous flow, WIP limits, visualize work -- ideal for sustain and ops work |
| DevOps | Culture + automation + measurement + sharing; CI/CD, IaC, monitoring |
| BRD/SRS/FRD | BRD = business why, SRS = system what, FRD = functional how |
| STLC | Parallel to SDLC: requirement analysis -> test planning -> design -> execute -> close |
| Environments | Local -> Dev -> Staging -> Pre-Prod -> Prod; maintain parity, isolate data |
| Application Types | Web, mobile, API, SPA, batch, real-time -- each has different testing needs |
| Sustain Context | You work in the Maintain phase; follow change management, add tests, document everything |

> **Next: Module 16 -- Confluence & Jira: Project management, agile boards, and team collaboration tools.**
