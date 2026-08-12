# FoodExpress -- Code Progression Across Modules

This document tracks how the FoodExpress codebase evolves across the training programme. Each module builds on previous work, adding new components and fixing prior bugs.

---

## Frontend Evolution (M01 -> M04)

| Module | What Changes | Key Files |
|--------|-------------|-----------|
| M01 | Raw HTML/CSS homepage -- restaurant cards, cart sidebar, checkout form | index.html, css/style.css |
| M02 | Bootstrap integration -- responsive grid, navbar, modals, accordion | index.html (Bootstrap classes), style.css (overrides) |
| M03 | JavaScript interactivity -- cart logic, validation, filtering, DOM events | js/app.js, js/checkout.js |
| M04 | React components -- MenuCard, Header, Cart as React components | src/components/*.jsx, src/App.jsx |

**M01 bugs fixed in M02:** Grid layout, cart overlap, flexbox alignment, lazy loading
**M02 bugs fixed in M03:** Bootstrap attributes, card heights, modal, carousel, accordion
**M03 bugs fixed in M04:** Cart duplicates, NaN total, ghost entries, missing validation

---

## Java Backend Evolution (M05 -> M08)

| Module | What Changes | Key Files |
|--------|-------------|-----------|
| M05 | Domain classes, Order Service basics, CRUD operations | Order.java, OrderService.java, OrderStatus.java |
| M06 | Exception handling, file I/O, custom exceptions | PaymentService.java, ReportService.java, *Exception.java |
| M07 | Collections, JDBC, database connectivity | OrderRepository.java, DatabaseUtil.java, MenuItem.java |
| M08 | Full API integration -- REST endpoints, team project | All Java files + API documentation |

**M05 bugs fixed in M06:** Discount logic, == vs .equals(), memory loading, race condition
**M06 bugs fixed in M07:** Generic exception catching, unclosed resources, wrong exception types
**M07 bugs fixed in M08:** Wrong collection types, connection leaks, missing equals/hashCode

---

## Node.js Backend Evolution (M09 -> M11)

| Module | What Changes | Key Files |
|--------|-------------|-----------|
| M09 | Node basics -- require, file I/O, async patterns, error handling | server.js, services/menuLoader.js, services/restaurantService.js |
| M10 | Express routes + MongoDB integration -- CRUD APIs | routes/restaurants.js, server.js, services/restaurantService.js |
| M11 | Full service -- async/await, middleware, validation, config | middleware/validateRequest.js, config/index.js, routes + services |

**M09 bugs fixed in M10:** Wrong requires, callback hell, unhandled rejections, path separators
**M10 bugs fixed in M11:** Wrong HTTP method, missing middleware, route order, wrong field names

---

## Database Layer (M12)

| Module | What Changes | Key Files |
|--------|-------------|-----------|
| M12 | SQL schema, seed data, reporting queries, indexes, views, transactions | schema.sql, seed-data.sql, reports.sql |

Builds on: M05-M07 Order Service schema (customers, orders, order_items tables)

---

## Infrastructure & DevOps Evolution (M20 -> M32)

| Module | What Changes | Key Files |
|--------|-------------|-----------|
| M20 | Linux scripts -- deployment, health check, log analysis | deploy.sh, health-check.sh, log analysis commands |
| M21 | Apache configs -- virtual hosts, .htaccess, logging, performance | httpd.conf, .htaccess, sites-available/*.conf |
| M24 | Dockerfile for Order Service (Java) | Dockerfile |
| M25 | Dockerfile for Restaurant Service (Node.js) + MySQL volumes | Dockerfile, run-mysql.sh |
| M26 | docker-compose.yml for full stack + nginx reverse proxy | docker-compose.yml, nginx.conf |
| M28 | Jenkinsfile for CI/CD pipeline | Jenkinsfile |
| M29 | Kubernetes manifests -- deployments, services, HPA | manifests/*.yaml |
| M30 | Ansible playbooks -- deployment automation | playbook.yml, inventory.ini, templates/ |
| M32 | Observability -- Prometheus, Grafana, alerting | prometheus.yml, grafana-dashboard.json, alert-rules.yml |

---

## Process & Quality Layer (M13 -> M19)

| Module | Focus | Deliverables |
|--------|-------|-------------|
| M13 | Testing strategy, test cases, bug triage | Test plan, automation matrix |
| M14 | Infrastructure mapping, HA design, cost optimization | Architecture documents |
| M15 | SDLC methodology, user stories, change management | Process documents |
| M16 | Jira issues, JQL queries, Confluence docs, Kanban board | Tool artifacts |
| M17 | Full-stack bug fixing with process (JIRA, RCA, tests) | Integrated sprint deliverables |
| M18 | DevOps pipeline design, deployment strategy | Pipeline documents |
| M19 | Git workflows, branching, merge conflicts, code review | Git repository artifacts |

---

## Sustain & Operate Layer (M33 -> M37)

| Module | Focus | Deliverables |
|--------|-------|-------------|
| M33 | SLOs, error budgets, toil assessment, post-mortems | SRE documents |
| M34 | War game, fault injection, incident response, ITSM intro | Incident records, dashboards |
| M35 | ITIL practices -- incident, problem, change, SLA | ITIL process documents |
| M36 | ServiceNow configuration -- SLAs, notifications, CMDB | ServiceNow artifacts |
| M37 | Major incident (3-day timeline), GenAI labs | Capstone deliverables |

---

## Technology Stack by Phase

```
Phase 1: Foundation (M01-M13)
  Frontend:  HTML -> CSS -> Bootstrap -> JavaScript -> React
  Backend:   Java (Spring Boot) -> Node.js (Express + MongoDB)
  Database:  MySQL + MongoDB
  Testing:   Jest + JUnit

Phase 2: Process (M14-M23)
  Tools:     Jira, Confluence, Git, Linux, Apache
  Concepts:  SDLC, DevOps, Microservices, API Design

Phase 3: Platform (M24-M32)
  Containers:  Docker -> Docker Compose
  CI/CD:       Jenkins pipelines
  Orchestration: Kubernetes
  Config Mgmt:  Ansible
  Security:     OWASP, DevSecOps
  Monitoring:   Prometheus + Grafana

Phase 4: Sustain (M33-M37)
  SRE:       SLOs, error budgets, toil, post-mortems
  ITSM:      Incident, problem, change management
  ITIL:      ITIL 4 practices
  ServiceNow: Platform configuration
  GenAI:     AI-assisted operations
```
