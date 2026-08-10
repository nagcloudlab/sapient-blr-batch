# FoodExpress -- Master Bug Manifest (TRAINER ONLY)

## Quick Reference: Every Module's Fix/Improve Tasks

---

### Module 01 -- HTML & CSS (Day 0-1, 0.5d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | Menu grid breaks on tablet (missing col-sm-6) | index.html | Easy |
| 2 | BUG | Cart sidebar overlaps on mobile (fixed positioning) | style.css | Medium |
| 3 | BUG | Cart total misaligned on small screens | style.css | Easy |
| 4 | PERF | Food images not lazy loaded | index.html | Easy |
| 5 | ENH | Add "Free Delivery" badge on qualifying items | index.html + style.css | Easy |
| 6 | ENH | Sticky footer with restaurant support contact | index.html + style.css | Medium |
| 7 | ENH | Back to Top button | index.html + style.css + script | Medium |
| 8 | BUG | Order form flexbox misalignment on Safari | style.css | Easy |

---

### Module 02 -- CSS Frameworks (Day 2, 1d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | Navbar toggler doesn't work on mobile (missing data-bs attributes) | index.html | Easy |
| 2 | BUG | Menu cards have inconsistent heights (missing h-100 class) | index.html | Easy |
| 3 | BUG | Modal "Order Placed" doesn't close properly (wrong dismiss attribute) | index.html | Medium |
| 4 | BUG | Restaurant filter dropdown overlaps content on tablet (z-index issue) | style.css | Medium |
| 5 | PERF | Bootstrap loaded via full bundle instead of individual components | index.html | Easy |
| 6 | ENH | Add "Free Delivery" badge using Bootstrap badge component | index.html | Easy |
| 7 | ENH | Make footer sticky using Bootstrap utility classes | index.html | Medium |
| 8 | ENH | Add responsive breakpoint for menu cards (1 col mobile, 2 tablet, 3 desktop) | index.html | Easy |
| 9 | BUG | Carousel for featured restaurants doesn't auto-advance (missing data-bs-ride) | index.html | Easy |
| 10 | BUG | Accordion FAQ section doesn't collapse other items (wrong parent attribute) | index.html | Medium |

---

### Module 03 -- JavaScript (Day 3, 1d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | Add to cart creates duplicate (doesn't increment qty) | app.js | Medium |
| 2 | BUG | Cart total shows NaN (string + number, wrong operator) | app.js | Medium |
| 3 | BUG | Rapid clicking creates ghost entries | app.js | Easy |
| 4 | BUG | Order form submits without validation (missing preventDefault) | checkout.js | Medium |
| 5 | PERF | Cuisine filter re-renders entire page (body.innerHTML) | app.js | Medium |
| 6 | ENH | Disable "Add to Cart" for out-of-stock items | app.js | Easy |
| 7 | DOC | Write debugging guide using DevTools | New file | -- |

---

### Module 04 -- UI Frameworks / React (Day 4-5, 1d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | MenuCard doesn't re-render on stock update (stale useEffect) | MenuCard.jsx | Medium |
| 2 | DOC | Create component map diagram | New file | -- |
| 3 | ENH | Cart count in Header uses local state instead of prop | Header.jsx | Easy |
| 4 | RCA | "Stale menu data" -- missing useEffect dependency | MenuCard.jsx | Medium |

---

### Module 05 -- Java Part 1 (Day 6, 1d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | DOC | Trace POST /orders request flow | All files | -- |
| 2 | BUG | Bulk discount not applied for qty > 10 items | OrderService.java | Easy |
| 3 | BUG | getOrdersByCustomer uses == instead of .equals() | OrderService.java | Medium |
| 4 | PERF | Order history loads all orders into memory | OrderService.java | Medium |
| 5 | ENH | Add PREPARING status + transitions | OrderStatus.java | Medium |
| 6 | BUG | Race condition on concurrent stock check | OrderService.java | Hard |
| 7 | INC | Simulate concurrent order -> stock = -1 | -- | Hard |
| 8 | DOC | Write request flow document | New file | -- |

---

### Module 06 -- Java Part 2 (Day 7, 1d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | Exception handling -- catching generic Exception hides root cause | OrderService.java | Medium |
| 2 | BUG | File I/O -- unclosed resource in CSV export | ReportService.java | Medium |
| 3 | BUG | Wrong exception type thrown in payment validation | PaymentService.java | Easy |
| 4 | ENH | Add custom FoodExpressException hierarchy | Exception classes | Medium |

---

### Module 07 -- Java Part 3 (Day 8, 1d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | Collections -- using wrong collection type for order lookup | OrderRepository.java | Medium |
| 2 | BUG | JDBC connection leak -- not closing in finally block | DatabaseUtil.java | Medium |
| 3 | BUG | HashMap key without equals/hashCode override | MenuItem.java | Medium |
| 4 | PERF | ArrayList used where LinkedList would be better for queue | OrderQueue.java | Easy |
| 5 | ENH | Implement Comparable for order sorting | Order.java | Easy |

---

### Module 08 -- Java Capsule (Day 9, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | API bug fixes -- integration of M05-07 concepts | Medium |
| 2 | ENH | Feature tickets -- new endpoints | Medium |
| 3 | DOC | API documentation | -- |
| 4 | PRES | Team presentation + demo | -- |

---

### Module 09 -- Node.js Part 1 (Day 10, 1d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | Missing or wrong require() calls crash on startup | server.js, utils/logger.js | Easy |
| 2 | BUG | Callback hell in menu loader -- unreadable and error-prone | services/menuLoader.js | Medium |
| 3 | BUG | Unhandled promise rejection crashes the process | services/restaurantService.js | Medium |
| 4 | BUG | File path uses hardcoded `\` separator -- fails on Linux | services/menuLoader.js | Easy |
| 5 | ENH | List all restaurants from data/restaurants.json | services/restaurantService.js | Easy |
| 6 | ENH | Read menu for a restaurant from data/menus/{id}.json | services/menuLoader.js | Easy |

---

### Module 10 -- Node.js Part 2 (Day 11, 0.5d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | POST /restaurants mapped as GET -- creates nothing | routes/restaurants.js | Easy |
| 2 | BUG | Missing express.json() middleware -- req.body is undefined | server.js | Easy |
| 3 | BUG | Catch-all route defined before specific routes -- everything 404s | server.js | Medium |
| 4 | BUG | MongoDB find uses wrong field name (status vs isActive) | services/restaurantService.js | Easy |
| 5 | BUG | MongoDB updateOne uses $push instead of $set | services/restaurantService.js | Easy |
| 6 | ENH | Add Express API routes for restaurant CRUD | routes/restaurants.js | Medium |
| 7 | ENH | Add MongoDB index on cuisine field | db/setup.js | Easy |

---

### Module 11 -- Node.js Capsule (Day 12, 1d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | GET /restaurants 500 -- async/await missing on service call | routes/restaurants.js | Medium |
| 2 | BUG | Async errors bypass error handler -- no try/catch | routes/restaurants.js | Medium |
| 3 | BUG | POST /restaurants saves nothing -- parameter name mismatch | services/restaurantService.js | Easy |
| 4 | BUG | Validation middleware doesn't block -- missing return | middleware/validateRequest.js | Easy |
| 5 | BUG | dotenv loaded too late -- env vars undefined at startup | config/index.js, server.js | Easy |
| 6 | FEATURE | Add DELETE /api/restaurants/:id soft-delete | routes + services | Medium |
| 7 | FEATURE | Add GET /api/restaurants/:id/menu with category filter | routes + services | Medium |

---

### Module 12 -- Database & SQL (Day 13, 1d)
| # | Type | Bug/Task | File | Difficulty |
|---|------|----------|------|-----------|
| 1 | BUG | Revenue report 3x actual -- Cartesian product, missing JOIN ON | reports.sql | Medium |
| 2 | BUG | Customer loyalty report excludes zero-order customers -- needs LEFT JOIN | reports.sql | Medium |
| 3 | BUG | Cancellation rate crashes -- division by zero | reports.sql | Medium |
| 4 | BUG | Top customer query fails -- WHERE instead of HAVING | reports.sql | Easy |
| 5 | BUG | NULL phone query returns no rows -- = NULL vs IS NULL | reports.sql | Easy |
| 6 | PERF | Monthly revenue ignores index -- YEAR() prevents index usage | reports.sql | Medium |
| 7 | PERF | Missing index on order_items.order_id FK | Schema | Easy |
| 8 | ENH | Create v_order_details view for reporting | Schema | Medium |
| 9 | ENH | Write atomic transaction for order placement | Schema | Medium |

---

### Module 13 -- QE/QC (Day 14, 1d)
| # | Type | Task | Difficulty |
|---|------|------|-----------|
| 1 | EXERCISE | Write 15 test cases for Order Placement feature | Medium |
| 2 | EXERCISE | Triage 8 production bugs -- classify and select 4 to fix | Medium |
| 3 | EXERCISE | Create test strategy document for FoodExpress v2.4 | Medium |
| 4 | EXERCISE | Build automation decision matrix for 200 test cases | Medium |
| 5 | ROLE PLAY | Test plan defense for loyalty rewards feature | -- |
| 6 | ROLE PLAY | Production bug triage simulation | -- |

---

### Module 14 -- Infrastructure (Day 15, 1d)
| # | Type | Task | Difficulty |
|---|------|------|-----------|
| 1 | EXERCISE | Map FoodExpress components to infrastructure layers/service models | Medium |
| 2 | EXERCISE | Cloud vs On-Prem decision matrix for 6 services | Medium |
| 3 | EXERCISE | Calculate system availability; design HA architecture | Hard |
| 4 | EXERCISE | Identify 5+ cost optimization opportunities from $15K bill | Medium |
| 5 | EXERCISE | Analyze 2 production incidents (DB pool, cert expiry) | Medium |

---

### Module 15 -- SDLC (Day 16, 1d)
| # | Type | Task | Difficulty |
|---|------|------|-----------|
| 1 | EXERCISE | Write 5 user stories + SRS excerpt + RTM for Scheduled Orders | Medium |
| 2 | EXERCISE | Select SDLC methodology for 6 FoodExpress projects | Medium |
| 3 | EXERCISE | Design 5-environment pipeline for FoodExpress | Medium |
| 4 | EXERCISE | Apply STLC stages to FoodExpress v2.4 release | Medium |
| 5 | EXERCISE | Complete change management simulation for FOOD-156 | Medium |

---

### Module 16 -- Jira/Confluence (Day 17, 1d)
| # | Type | Task | Difficulty |
|---|------|------|-----------|
| 1 | EXERCISE | Create 6 Jira issues (epic, story, bugs, task, sub-task) | Medium |
| 2 | EXERCISE | Write 12 JQL queries for sustain scenarios | Medium |
| 3 | EXERCISE | Write Confluence runbook, RCA, and release notes | Medium |
| 4 | EXERCISE | Design Kanban board with WIP limits and swimlanes | Easy |
| 5 | ROLE PLAY | Sprint planning -- select stories from backlog | -- |
| 6 | ROLE PLAY | Sprint execution -- standup, bug, blocker resolution | -- |
| 7 | ROLE PLAY | Sprint review + retro -- demo, velocity, action items | -- |

---

### Module 17 -- Integration Capsule (Day 18, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Price NaN -- currency symbol in API response (full stack) | P1 |
| 2 | BUG | Search special characters -- SQL injection vulnerability | P2 |
| 3 | BUG | Order history -- missing pagination, sorting, and index | P2 |
| 4 | BUG | Rating 500 error -- type mismatch across all layers | P3 |
| 5 | ENH | Write 2 unit tests per bug fix | Required |
| 6 | DOC | Write 5 Whys RCA documents for each bug | Required |
| 7 | PROCESS | Update JIRA board with comments and RCA | Required |
| 8 | PRES | 15-minute team presentation with demo | Required |

---

### Module 18 -- DevOps (Day 19, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 6 bugs in Jenkinsfile CI/CD pipeline | Medium |
| 2 | BUG | Fix 5 issues in deployment strategy document | Medium |
| 3 | EXERCISE | Design complete DevOps pipeline for Menu Service | Medium |
| 4 | EXERCISE | Map FoodExpress pipeline to 7 C's framework | Easy |
| 5 | EXERCISE | DevOps maturity assessment (Levels 1-5) | Easy |

---

### Module 19 -- Git/GitHub (Day 20, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 6 .gitignore issues (missing ignores, secrets exposure) | Medium |
| 2 | BUG | Rewrite 5 bad commit messages following convention | Easy |
| 3 | BUG | Resolve 4 merge conflicts combining both developers' intent | Medium |
| 4 | BUG | Rename 5 branches to follow naming conventions | Easy |
| 5 | ROLE PLAY | Agile sprint simulation using Git + GitHub | -- |

---

### Module 20 -- Linux (Day 21, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 6 buggy log analysis commands (grep, awk, cut, sort) | Medium |
| 2 | BUG | Fix 8 bugs in deployment shell script | Medium |
| 3 | BUG | Fix 5 disk space commands + create crontab | Easy |
| 4 | BUG | Fix 6 bugs in health check script | Medium |
| 5 | ENH | Write complete log rotation script | Medium |

---

### Module 21 -- Apache (Day 22, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 7 bugs in virtual host config (paths, proxy, security) | Medium |
| 2 | BUG | Fix 6 bugs in .htaccess (rewrite, CORS, caching) | Medium |
| 3 | BUG | Fix 5 logging configuration issues | Easy |
| 4 | BUG | Fix 4 performance issues (KeepAlive, MPM, compression) | Medium |
| 5 | ENH | Configure 3 virtual hosts (name-based + port-based) | Medium |

---

### Module 22 -- Microservices & API (Day 23, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 8 REST controller bugs (versioning, HTTP methods, pagination) | Medium |
| 2 | BUG | Fix 6 API gateway bugs (routing, auth, rate limiting) | Medium |
| 3 | BUG | Fix 5 inter-service communication bugs (timeouts, circuit breaker) | Hard |
| 4 | BUG | Fix 5 LLM security bugs (API key exposure, prompt injection) | Medium |
| 5 | EXERCISE | Design service boundaries (6+ bounded contexts) | Medium |
| 6 | ENH | Design standard error response JSON schema | Easy |

---

### Module 23 -- Platform Capsule (Day 24, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 6 bugs in Order Service startup script + application.yml | Medium |
| 2 | BUG | Fix 5 bugs in disk & log rotation configuration | Medium |
| 3 | BUG | Fix 5 bugs in API timeout chain (sync reads, missing timeouts) | Hard |
| 4 | DOC | Write P1 incident post-mortem document | Medium |

---

### Module 24 -- Docker Part 1 (Day 25, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 7 Dockerfile bugs (base image, WORKDIR, COPY, EXPOSE, USER, CMD, HEALTHCHECK) | Medium |
| 2 | EXERCISE | Docker commands -- pull, run, inspect, cleanup | Easy |
| 3 | ENH | Write Dockerfile from scratch for NGINX landing page | Easy |

---

### Module 25 -- Docker Part 2 (Day 26, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 8 Restaurant Service Dockerfile bugs (tag, COPY, npm ci, USER, CMD) | Medium |
| 2 | BUG | Fix 5 MySQL volume config bugs (path, restart, password, init) | Medium |
| 3 | ENH | Create multi-stage Dockerfile for Order Service | Medium |

---

### Module 26 -- Docker Part 3 (Day 27, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 10 docker-compose.yml bugs (networks, ports, depends_on, volumes, env) | Hard |
| 2 | EXERCISE | Networking exploration -- DNS, isolation, port mapping | Easy |
| 3 | ENH | Write nginx.conf reverse proxy for all services | Medium |

---

### Module 27 -- Secure Engineering (Day 28, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 8 security vulnerabilities (SQL injection, XSS, hardcoded secrets, IDOR, weak hashing) | Hard |
| 2 | ENH | Move all hardcoded secrets to .env | Easy |
| 3 | ENH | Run container vulnerability scan, document findings | Medium |

---

### Module 28 -- Jenkins (Day 29, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 8 Jenkinsfile bugs (missing stages, wrong branch, hardcoded creds, no cleanup) | Medium |
| 2 | ENH | Write Node.js Jenkinsfile (Install, Lint, Test, Docker Build) | Medium |
| 3 | ENH | Optimize pipeline (parallel stages, conditional deploy, caching) | Hard |

---

### Module 29 -- Kubernetes (Day 30, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 4 Order Deployment bugs (probe path, port, resources, startup) | Medium |
| 2 | BUG | Fix 3 Order Service bugs (selector, targetPort, nodePort) | Medium |
| 3 | BUG | Fix 3 Payment Deployment bugs (image, readiness, hardcoded secret) | Medium |
| 4 | BUG | Fix 2 Namespace config bugs (unrealistic quota, inverted limits) | Easy |
| 5 | ENH | Design HPA manifest for order-service | Medium |
| 6 | ENH | Write NetworkPolicy restricting inter-service traffic | Hard |

---

### Module 30 -- Ansible (Day 31, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 4 deployment playbook bugs (module, become, variable, handler) | Medium |
| 2 | BUG | Fix 2 inventory bugs (wrong groups, wrong SSH user) | Easy |
| 3 | BUG | Fix 2 Nginx template bugs (Jinja2 group, upstream) | Easy |
| 4 | ROLE PLAY | Incident escalation scenario -- Order Service down at 2 AM | -- |
| 5 | ENH | Add post-deployment health check using uri module | Easy |
| 6 | ENH | Create proper Ansible role from playbook | Medium |

---

### Module 31 -- DevOps Capsule (Day 32, 1d)
| # | Type | Task | Difficulty |
|---|------|------|-----------|
| 1 | PROJECT | Containerize services (multi-stage Dockerfiles, compose) | Hard |
| 2 | PROJECT | CI/CD pipeline (Jenkinsfile with full stages) | Hard |
| 3 | PROJECT | K8s deployment (pods, services, probes, HPA) | Hard |
| 4 | PROJECT | Ansible configuration (playbooks, inventory, vault) | Medium |
| 5 | PROJECT | Integration testing + rollback + documentation | Medium |
| 6 | PRES | Architecture demo + Q&A | -- |

---

### Module 32 -- Observability (Day 33, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 3 Prometheus config bugs (wrong target, missing job, wrong path) | Easy |
| 2 | BUG | Fix 3 Grafana dashboard bugs (missing rate(), wrong math, avg vs p99) | Medium |
| 3 | BUG | Fix 3 alert rule bugs (wrong threshold, missing for, too sensitive) | Medium |
| 4 | ENH | Write 3 PromQL queries for golden signals | Medium |
| 5 | ENH | Design runbook for HighErrorRate alert | Easy |
| 6 | ENH | Configure Alertmanager routing (critical vs warning) | Medium |

---

### Module 33 -- SRE (Day 34, 1d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 4 SLO definition issues (impossible target, wrong SLI, short window) | Medium |
| 2 | EXERCISE | Error budget calculator -- track consumption, determine policy | Medium |
| 3 | EXERCISE | Toil assessment -- classify, prioritize, automation roadmap | Medium |
| 4 | BUG | Fix 3 post-mortem issues (missing timeline, blame language, no owners) | Easy |
| 5 | ENH | Create risk register with mitigation strategies | Medium |

---

### Module 34 -- MidStage + ITSM (Day 35-38, 2d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 8 Prometheus alert rule bugs (thresholds, severity, metric names) | Medium |
| 2 | BUG | Fix 6 fault injection script bugs (namespace, rollback, API path) | Medium |
| 3 | BUG | Fix 6 incident template bugs (priority, timeline, escalation) | Easy |
| 4 | BUG | Fix 5 ITSM process flow bugs (categories, SLA targets, notifications) | Medium |
| 5 | EXERCISE | Design Grafana dashboard for FoodExpress operations | Easy |
| 6 | ENH | Write complete runbook for order service 500 errors | Medium |

---

### Module 35 -- ITIL (Day 39-40, 1.5d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 7 incident record bugs (priority, SLA, status flow, CI) | Medium |
| 2 | BUG | Fix 6 change request bugs (type, risk, rollback, CAB) | Medium |
| 3 | BUG | Fix 6 problem record bugs (status, 5 Whys, workaround) | Medium |
| 4 | BUG | Fix 6 SLA definition bugs (availability, resolution, penalties) | Medium |
| 5 | EXERCISE | Map 8 FoodExpress scenarios to ITIL practices | Easy |
| 6 | ENH | Trace one issue through Incident > Problem > Change > Release | Medium |

---

### Module 36 -- ServiceNow (Day 41-42, 1.5d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | BUG | Fix 7 SLA policy bugs (start condition, duration, schedule) | Medium |
| 2 | BUG | Fix 6 email notification bugs (subject, recipients, routing) | Medium |
| 3 | BUG | Fix 6 instance config bugs (password, ACLs, session timeout) | Medium |
| 4 | ROLE PLAY | P1 incident response + Change/Problem management | -- |

---

### Module 37 -- Final + GenAI (Day 43-44, 1.5d)
| # | Type | Bug/Task | Difficulty |
|---|------|----------|-----------|
| 1 | PROJECT | Complete Major Incident Record (INC-2026-0475) with full timeline | Hard |
| 2 | PROJECT | Problem Record (PRB-2026-0030) with 5 Whys analysis | Hard |
| 3 | PROJECT | Change Request (CHG-2026-0095) -- memory leak fix with risk assessment | Medium |
| 4 | PROJECT | SLA Definition for Payment Processing service | Medium |
| 5 | PROJECT | Service Catalog entry with dependencies and support model | Easy |
| 6 | PROJECT | Blameless Post-Incident Review with action items | Medium |
| 7 | PROJECT | Payment service monitoring dashboard design | Easy |
| 8 | AI | Fix AI prompt templates (6 bugs), evaluation harness (6 bugs), trust guidelines (5 bugs) | Medium |
| 9 | PRES | 15-minute team demo covering all deliverables | -- |

---

## Total Counts (All 37 Modules)

| Type | Count |
|------|-------|
| BUG | 180+ |
| ENH/FEATURE | 45+ |
| PERF | 10+ |
| EXERCISE | 35+ |
| PROJECT | 15+ |
| ROLE PLAY | 10 |
| DOC/PRES | 15+ |
| **TOTAL** | **310+ tasks** |

### By Phase

| Phase | Modules | Bug/Fix Tasks | Exercise Tasks | Role Plays |
|-------|---------|---------------|----------------|------------|
| Foundation | M01-M13 | ~100 | ~15 | 3 |
| Process & Tools | M14-M23 | ~65 | ~20 | 4 |
| Platform | M24-M32 | ~75 | ~10 | 1 |
| Sustain & Operate | M33-M37 | ~50 | ~10 | 2 |
