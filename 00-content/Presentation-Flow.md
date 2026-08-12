# FoodExpress Training Programme — Stakeholder Presentation Flow

**Trainer:** Nagabhushanam
**Programme:** Publicis Sapient Sustain Engineering (SRE + ITIL)
**Duration:** 43.5 days | 37 modules | Bangalore | July 29, 2026

This document is the trainer's presentation script for walking programme stakeholders, delivery leads, or participant managers through the training design. Each section maps to one stakeholder-facing slide. The "Say this:" blocks contain suggested spoken words.

---

## Slide 1 — "Build it, Deploy it, Monitor it, Sustain it"

### The Philosophy

Most engineering training teaches people to build from scratch. This programme is different. The participants joining this track are joining sustain engineering teams. Their daily reality is not greenfield development — it is reading code written by someone else, debugging incidents at 2 AM, filing change requests, and keeping a live system healthy.

So from Day 1, every concept is taught inside that frame: here is something broken, here is your job, fix it.

The programme runs for 43.5 days across 37 modules. Every single module connects to one application: FoodExpress, a food delivery platform that participants build, break, fix, deploy, monitor, and sustain from start to finish.

### Say this:

"This is not a coding bootcamp. This is a sustain engineering programme. The difference matters. A coding bootcamp teaches someone to write an app. This programme teaches someone to keep an app alive — on a Friday evening, when the on-call pager fires, when no one who wrote the original code is available. We achieve that by giving every participant one application for 43 days and framing every topic as a sustain task from the first slide."

---

## Slide 2 — What is Sustain Engineering?

### The Nine Pillars

Sustain engineering is not a single activity. It is a collection of responsibilities that together keep a production system healthy. Each pillar maps directly to modules in this programme.

| Pillar | What it means in practice |
|---|---|
| Monitor | Watch dashboards, set up alerts, catch problems before users do |
| Incident Response | Detect, triage, coordinate, resolve, communicate during live incidents |
| Bug Fixes | Investigate defects reported by users or monitoring; patch and verify |
| Enhancements | Small improvements to existing features within defined change windows |
| Performance | Profile slow endpoints, optimize queries, reduce latency |
| Deployment | Push changes through CI/CD pipelines, manage rollbacks |
| RCA | Root cause analysis — write post-mortems, identify contributing factors |
| Documentation | Knowledge base articles, runbooks, architecture diagrams |
| SLA Management | Track SLOs, report breach risk, escalate appropriately |

None of these activities involve writing a new application from scratch. They all involve working with something that already exists.

### Say this:

"When I ask a sustain engineer what they did today, the answer is never 'I built a new feature.' The answer is: I investigated a latency spike, I merged a bug fix, I updated the runbook after last night's incident, I filed a change request for tomorrow's deployment, and I closed three service desk tickets. That is sustain engineering. Every one of those activities is a module in this programme."

---

## Slide 3 — The Capstone: FoodExpress

### The Application

FoodExpress is a food delivery platform purpose-built for this training. It is not a toy application. It has a real architecture, real bugs, and real operational concerns. Participants do not watch the trainer build it — they maintain it, fix it, and operate it.

**Architecture:**

- Frontend: React single-page application (restaurant browsing, cart, order tracking, real-time delivery status)
- Restaurant Service: Node.js — search, menu, availability
- Order Service: Java (Spring Boot) — order lifecycle, bulk pricing, discount engine
- Cart Service: Node.js — session management, item totals, coupon validation
- Delivery Service: Node.js — driver assignment, ETA calculation, status updates
- Databases: MongoDB (restaurants, menus) and MySQL (orders, users, payments)
- Observability: Prometheus metrics collection + Grafana dashboards
- Containerisation: Docker with Docker Compose for local environments, Kubernetes for production simulation

**Why food delivery?**

The domain is immediately understandable. Every participant has used a food delivery app. That familiarity means cognitive load goes into the engineering concepts, not into understanding what the application is supposed to do. When a bug causes "the cart total to show NaN", every participant immediately understands the business impact.

### Say this:

"FoodExpress is the thread that runs through every single day of this programme. On Day 1, participants see a broken HTML layout on the restaurant listing page. On Day 43, they run a war game where faults are injected into the live system and they have to detect, triage, and resolve them against the clock using every tool they have learned. Same app, start to finish."

---

## Slide 4 — Phase 1: Foundation (M01–M13, Days 0–14)

### Building the Knowledge Base

Phase 1 covers the technical fundamentals that underpin everything else in the programme. Every topic is taught as a sustain task on the FoodExpress codebase.

| Module | Topic | FoodExpress Sustain Task |
|---|---|---|
| M01 | HTML & CSS | "The mobile layout on the restaurant listing page is broken — fix the CSS" |
| M02 | CSS Frameworks | Bootstrap grid misalignment on the menu card component |
| M03 | JavaScript Part 1 | "The cart total is showing NaN — find and fix the calculation bug" |
| M04 | UI Frameworks | React component state bug causing stale menu prices |
| M05–07 | Java Parts 1–3 | "The bulk discount is not applying correctly on orders over 5 items" |
| M08 | Java Capsule | Project day — integrate all Java fixes into the Order Service |
| M09–10 | Node.js Parts 1–2 | "Restaurant search is case-sensitive — a user searching 'pizza' gets no results for 'Pizza Palace'" |
| M11 | Node.js Capsule | Project day — integrate all Node.js fixes into Cart and Restaurant services |
| M12 | Database SQL | Slow query on order history; missing index on user_id column |
| M13 | QE/QC | Writing tests for the fixed cart calculation and discount engine |

### Capsule Days

M08 and M11 are capsule days. These are integration and assessment days, not teaching days. Participants apply everything from the preceding modules to the FoodExpress project. The trainer observes and evaluates; instruction is minimal.

### Say this:

"By the end of Phase 1, a participant can read the FoodExpress codebase across four languages — HTML, JavaScript, Java, and Node.js. They can identify bugs, fix them, write tests, and query the database. More importantly, they have done all of that on code they did not write, which is the core sustain engineering skill. We have not once asked them to build something new."

---

## Slide 5 — Phase 2: Process and Tools (M14–M23, Days 15–24)

### How Engineering Teams Work

Technical skill alone is not enough for a sustain engineer. Knowing how to fix a bug is only useful if you know how to do it within a change management process, log it in the right tool, get it reviewed, and deploy it safely.

Phase 2 covers the process and tooling layer.

| Module | Topic | Key Skill |
|---|---|---|
| M14 | Infrastructure | Servers, networks, cloud basics — understanding what the app runs on |
| M15 | SDLC | Agile, sprints, release cycles — how changes flow from idea to production |
| M16 | Jira/Confluence | Raising bugs, managing tickets, writing runbooks in Confluence |
| M17 | Integration Capsule | Checkpoint — participants run a mini sustain sprint on FoodExpress |
| M18 | DevOps | CI/CD concepts, pipelines, automated builds |
| M19 | Git/GitHub | Branching, pull requests, code review, hotfix workflow |
| M20 | Linux | Command line, process management, log tailing, file permissions |
| M21 | Apache | Web server configuration, reverse proxy, access logs, error diagnosis |
| M22 | Microservices/API | Service decomposition, REST contracts, API debugging |
| M23 | Platform Capsule | Checkpoint — participants deploy a change through the full process: Jira ticket to Git PR to pipeline |

### Say this:

"A sustain engineer who can fix a bug but does not know how to raise a change request, get it reviewed, and deploy it safely through the pipeline is only half-trained. Phase 2 is where we teach the professional discipline around the technical skill. By Module 23, participants are running their own mini sustain sprints — ticket, branch, fix, review, deploy."

---

## Slide 6 — Phase 3: Platform (M24–M32, Days 25–33)

### The Infrastructure Layer

Modern sustain engineering happens inside containerised, automated infrastructure. Phase 3 teaches participants to work confidently in that environment.

| Module | Topic | FoodExpress Context |
|---|---|---|
| M24–26 | Docker Parts 1–3 | Containerise every FoodExpress service; write and debug Docker Compose files |
| M27 | Secure Engineering | Identify secrets in environment files; fix CORS misconfigurations on the API |
| M28 | Jenkins | Build a CI pipeline that runs tests and lints on every PR to FoodExpress |
| M29 | Kubernetes | Deploy FoodExpress to a local K8s cluster; scale the Restaurant Service |
| M30 | Ansible | Automate environment provisioning with Ansible playbooks |
| M31 | DevOps Capsule | Checkpoint — participants deploy FoodExpress end-to-end: Git to Jenkins to Docker to K8s |
| M32 | Observability | Instrument FoodExpress with Prometheus; build a Grafana dashboard |

### Say this:

"By the end of Phase 3, participants are deploying FoodExpress to Kubernetes through a Jenkins pipeline. They have instrumented it with Prometheus and can read the Grafana dashboard to spot anomalies. That is the platform layer that underpins modern sustain engineering. Phase 4 is where we put all of it under pressure."

---

## Slide 7 — Phase 4: Sustain and Operate (M33–M37, Days 34–44)

### The Proving Ground

Phase 4 is where the programme culminates. Every concept from every earlier phase comes together in simulated production operation.

| Module | Topic | What Happens |
|---|---|---|
| M33 | SRE | Error budgets, SLOs, SLAs — measuring reliability of FoodExpress in numbers |
| M34 | Mid-Stage War Game + ITSM | Live fault injection exercise. Participants operate FoodExpress under simulated incidents while following ITSM process |
| M35 | ITIL | ITIL 4 framework: incident, problem, change, and knowledge management |
| M36 | ServiceNow | Raise and manage incidents and change requests in ServiceNow |
| M37 | Final War Game + GenAI | Full-scale final exercise with P1 incident simulation, plus AI-assisted sustain tooling |

### The Outcome

A participant who completes all 37 modules has:
- Maintained one application across 43 days
- Fixed bugs in HTML, CSS, JavaScript, Java, and Node.js
- Deployed changes through a Jenkins pipeline to Kubernetes
- Monitored the application with Prometheus and Grafana
- Responded to simulated production incidents using ITIL process and ServiceNow
- Written RCA documents and post-mortems
- Used GenAI to assist log analysis and code review

### Say this:

"Phase 4 is the test. The war games are not optional enrichment — they are the assessment. If a participant cannot detect a fault, triage it, raise the right ticket, communicate with stakeholders, fix it, and verify the fix, they have not completed the programme. Phase 4 is where we find that out while there is still time to address it."

---

## Slide 8 — The War Games

### How They Work

The programme includes two war game exercises: the Mid-Stage War Game on Day 35 (M34) and the Final War Game on Day 43–44 (M37).

**Mechanics:**

Faults are injected into the running FoodExpress environment using the `inject-faults-wargame.sh` script. Participants do not know when faults will be injected or what kind. The trainer controls the script.

**Mid-Stage War Game fault schedule (Day 35):**

| Time | Fault | Expected Detection Method |
|---|---|---|
| 09:30 | MongoDB text index dropped — search becomes slow | Grafana latency spike + user report |
| 11:00 | Cart service memory leak activated | Container memory graph in Grafana |
| 13:30 | Network delay added to Delivery Service | Increased order ETA response times |
| 15:00 | MySQL sleep injected into Order Service query | Slow query log + latency dashboard |

**Final War Game fault schedule (Days 43–44):**

A P1 incident is triggered on Day 43. The payment gateway is blocked for all orders. Participants must: detect the fault via monitoring, raise a P1 in ServiceNow, follow the ITIL incident management process, communicate a customer-facing status update, investigate root cause, apply the fix, verify recovery, write the post-mortem, and raise the problem record.

**What the trainer observes:**

- Time to detection (how long before anyone notices?)
- Quality of the ServiceNow ticket (correct category, priority, description?)
- Communication — does the team update stakeholders proactively?
- Fix quality — do they verify before closing the incident?
- Post-mortem — is the RCA accurate and the remediation actionable?

### Say this:

"The war game is the closest we can get to a real production incident without actual production risk. Everything runs in Docker on a local environment. Every fault is reversible in seconds. But from the participants' perspective, FoodExpress is down, customers cannot order food, and they need to fix it. We inject a fault every 90 minutes and watch how the team responds. By the end of Day 38, we know exactly which participants are ready for a sustain engineering seat and which ones need more time."

---

## Slide 9 — GenAI in Sustain Engineering

### The Role of AI

Module 37 includes a dedicated GenAI section. The framing is deliberate: AI is a tool that assists sustain work, not a replacement for engineering judgment.

**How participants use AI in the programme:**

| Task | AI Assistance |
|---|---|
| Log analysis | Paste a wall of application logs; ask AI to identify the anomaly pattern |
| Code review | Ask AI to explain a block of unfamiliar Java or Node.js code |
| RCA writing | Draft the initial post-mortem structure; human fills in the specifics |
| Communication | Draft a customer-facing incident update for review and approval |
| Query optimisation | Ask AI to suggest index strategies; validate the suggestion manually |

**The non-negotiable principle:**

AI provides a starting point. The sustain engineer validates, challenges, and decides. A wrong AI suggestion acted on without validation can make an incident worse. Participants are taught to treat AI output the same way they treat a suggestion from a junior colleague: useful input, requires verification.

The module slogan is: "AI assists, humans decide."

### Say this:

"GenAI is already in the tools that sustain engineers use every day. Ignoring it would be dishonest. But teaching participants to blindly trust it would be dangerous. Module 37 teaches them to use it the way a professional should: to accelerate the boring parts of the job — drafting, log triage, code explanation — while keeping their own judgment in the loop for every decision that matters."

---

## Slide 10 — Delivery Methodology

### How Each Day is Structured

Every standard training day follows the same rhythm. Participants quickly learn what to expect, which reduces the cognitive overhead of the format and lets them focus on the content.

| Time Block | Activity |
|---|---|
| 09:00 – 09:15 | Morning recap and standup — what did we cover yesterday, any blockers |
| 09:15 – 10:30 | Concept teaching with slides and live demo |
| 10:30 – 10:45 | Break |
| 10:45 – 12:30 | Hands-on lab — bug hunting in FoodExpress starter code |
| 12:30 – 13:30 | Lunch |
| 13:30 – 14:30 | Lab continuation or group project work |
| 14:30 – 15:30 | Role play or group scenario activity |
| 15:30 – 15:45 | Break |
| 15:45 – 16:30 | Project time and day wrap-up |

**Instructional model: I Do, We Do, You Do**

- I Do: Trainer demonstrates the concept on FoodExpress with a running system
- We Do: Trainer and participants work through the first bug together
- You Do: Participants complete the remaining bugs independently or in pairs

This model means no participant sits passively through an entire session. Within 30 minutes of any new concept being introduced, they are applying it.

### Say this:

"The I Do, We Do, You Do model is non-negotiable. If I am the only one doing anything for more than 30 minutes, something has gone wrong. The goal of the teaching portion is to give participants just enough context to attack the lab. The real learning happens in the lab, not the slides. The slides are the map; the lab is the territory."

---

## Slide 11 — Supporting Struggling Participants

### Early Detection

Falling behind in a 43-day programme is easy to miss until it is too late to address. This programme uses three early detection mechanisms:

- **Quiz scores:** Short knowledge checks at the end of each module flag gaps immediately
- **Lab completion:** Participants who do not complete the minimum bug fixes by end of day are flagged
- **Participation:** Silence during the I Do phase or repeated questions on the same concept signal a participant who is not following

### Graduated Intervention

| Level | Trigger | Response |
|---|---|---|
| Level 1 — Monitor | One missed lab completion | Trainer checks in at lunch or end of day |
| Level 2 — Assist | Two consecutive incomplete labs | Pair the participant with a stronger peer; trainer gives 10-min individual session |
| Level 3 — Escalate | Quiz score below threshold two modules in a row | Notify programme manager; offer optional evening review session |
| Level 4 — Formal Review | Consistent underperformance across a phase | Structured catch-up plan; assess whether participant is on the right track |

### Tiered Lab Design

Every lab in the programme has three tiers:

- **Core bugs (required):** The minimum set that every participant must fix to pass the lab. These cover the primary learning objective.
- **Extended bugs (recommended):** Additional bugs for participants who complete the core set early. These go deeper into the same concept.
- **Bonus challenges (optional):** Open-ended enhancements for fast finishers. These are not assessed.

This means a struggling participant always has a clear minimum target, and a fast participant is never sitting idle.

### Say this:

"I have run enough training programmes to know that a participant who is lost on Day 3 and says nothing will be completely overwhelmed by Day 10. The tiered lab design and the observation checkpoints let me catch that on Day 3. A quiet participant in a hands-on session is almost always a participant who does not know where to start. I watch for that."

---

## Slide 12 — Why This Works

### The Design Principles That Make It Effective

**One application for 43 days.**

Every module touches FoodExpress. There is no context-switching overhead. Participants do not have to learn a new codebase for each topic. By Week 2, they know the FoodExpress code well enough to navigate it without guidance. By Week 6, they have fixed things in it that would appear in real production systems.

**Sustain framing from Day 1.**

The first lab is not "build a webpage." It is "this webpage is broken, fix it." That framing never changes. Participants never develop the expectation that their job is to create something new. They are sustain engineers from the first minute.

**Every topic has a task.**

There are no theory-only modules. Every module ends with a lab that requires participants to do something on FoodExpress. Observability is not just slides about Prometheus — it is "here is a FoodExpress service that has no metrics; instrument it and build a dashboard."

**Progressive layering.**

HTML skills learned in M01 are needed when reading the React templates in M04. Database skills from M12 are needed during the slow query lab in M32. Kubernetes knowledge from M29 is needed during the war game in M34. Everything builds on everything else.

**The war game proves readiness.**

Assessment in most training programmes is a written test. This programme's assessment is a live incident. A participant who can perform under a war game scenario — detecting a fault, following process, communicating clearly, fixing correctly — is demonstrably ready for a sustain engineering seat.

### FAQ: "Is this realistic for 43 days?"

The question gets asked. The answer is: yes, because the scope is sustain, not greenfield. Participants are not building FoodExpress from scratch — they are maintaining a system that already exists. Maintaining a system is faster to learn than building one, because every task has a concrete, bounded scope. Fix this. Deploy that. Monitor this endpoint.

The breadth of 37 modules across 43 days is achievable because each module is taught at the level of a sustain engineer, not at the level of a specialist. A sustain engineer does not need to know how to design a Kubernetes cluster from scratch. They need to know how to read a pod crash log, scale a deployment, and restart a failing service. That is 1 day of content, not 5.

### FAQ: "How do you keep engagement?"

Three things:

First, the application is always running. Participants can always see FoodExpress in a browser. Abstract concepts become concrete the moment you can point at a real endpoint and say "this is the one that is slow."

Second, bugs are satisfying to fix. There is a specific pleasure in seeing a broken page become a working page. The lab format generates that feeling multiple times per day.

Third, the war games create genuine stakes. When faults are injected and participants know they are being observed, engagement is not a problem. The challenge becomes keeping them calm, not keeping them interested.

### Say this:

"I have seen training programmes where participants check out by Week 2 because they have been watching slide decks and doing isolated exercises with no connection to each other. That does not happen here, because every single day connects to the same story: FoodExpress is running in production, it has problems, and your team's job is to keep it healthy. That story does not get boring."

---

*End of Presentation Flow*

*For the full module-by-module schedule, see `COURSE-MAP.md`.
For daily timing and trainer notes, see `TRAINER-GUIDE.md`.
For war game fault details, see `war-game-scripts/inject-faults-wargame.sh`.*
