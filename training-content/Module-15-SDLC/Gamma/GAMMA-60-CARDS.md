# SDLC Fundamentals

From idea to production—and the sustain engineer’s role at every stage.

**Module 15 · Sustain Engineering Training · 17 August 2026**

> Gamma direction: Full-bleed image using `assets/01-sdlc-journey.png`. Dark navy theme, white title, electric-blue accent.

---

# Today’s challenge

A production defect is reported at 9:00 AM.

**What must happen before a safe fix reaches customers?**

> Gamma direction: Minimal question card. Large type, amber accent, no additional image.

---

# What you will be able to do

- Map the complete software lifecycle
- Choose an appropriate delivery method
- Read BRD, SRS, and FRD documents
- Connect SDLC with testing and environments
- Plan a controlled sustain change

---

# SDLC in one sentence

The Software Development Life Cycle is a structured way to **plan, build, verify, release, operate, and retire software**.

---

# Why structure matters

Without a lifecycle, teams optimize for speed today and create incidents tomorrow.

**Structure makes change repeatable, visible, and safer.**

---

# The lifecycle at a glance

Plan → Analyze → Design → Build → Test → Deploy → Maintain → Retire

> Gamma direction: Full-width `assets/01-sdlc-journey.png`; overlay only the lifecycle line.

---

# Stage 1: Planning

Decide **why** the work matters, **what** success means, and **whether** it is feasible.

---

# Planning outputs

- Project charter
- Scope and milestones
- Budget and resources
- Risk register
- Success measures

---

# Stage 2: Analysis

Turn business intent into clear, testable requirements.

**The key question: What must the system do—and how well?**

---

# Functional requirements

Describe system behavior.

Example: “A customer can search restaurants by cuisine.”

---

# Non-functional requirements

Describe quality and constraints.

Example: “Search results appear within two seconds for 95% of requests.”

---

# A requirement must be testable

Weak: “The app should be fast.”

Strong: “Checkout completes within three seconds at 2,000 concurrent users.”

---

# Stage 3: Design

Translate requirements into a technical solution before writing production code.

---

# Design decisions

- Architecture and service boundaries
- Data model
- APIs and integrations
- Security controls
- Failure handling
- User experience

---

# Design for failure

Reliable systems ask early:

**What happens when payment, inventory, or notification services are unavailable?**

---

# Stage 4: Build

Develop the solution in small, reviewable, testable changes.

---

# Stage 5: Test

Testing does not prove perfection.

It provides evidence that the system behaves as expected under known conditions.

---

# Stage 6: Deploy

Release a verified change through a controlled, observable, reversible process.

---

# A safe deployment has four parts

1. Approved change
2. Verified artifact
3. Health checks
4. Rollback plan

---

# Stage 7: Maintain

Monitor, support, repair, improve, and protect the live service.

**This is the sustain engineer’s home ground.**

---

# Maintenance still uses the lifecycle

A production fix still requires analysis, design, build, test, and deployment.

**Maintenance is not a shortcut around engineering discipline.**

---

# Stage 8: Retire

End-of-life is a planned engineering activity—not simply switching a server off.

---

# Checkpoint: trace the defect

In pairs, trace a checkout defect through every lifecycle stage.

**What evidence is produced at each stage?**

---

# Delivery methods

The lifecycle describes **what must happen**.

A methodology describes **how the team organizes that work**.

> Gamma direction: Use `assets/02-methodologies.png` as a wide visual.

---

# Waterfall

Work moves through defined sequential phases, with formal handoffs and approvals.

---

# When Waterfall fits

- Stable scope
- Strong regulatory controls
- Fixed contractual deliverables
- Expensive late-stage change

---

# Waterfall trade-off

Predictability is high when assumptions are correct.

Feedback arrives late when assumptions are wrong.

---

# Agile

Deliver value in small increments, learn from feedback, and adapt the plan.

---

# Scrum

Scrum organizes work into time-boxed sprints that produce a usable increment.

---

# Scrum roles

- Product Owner: value and priority
- Scrum Master: flow and facilitation
- Developers: create the increment

---

# Scrum events

Sprint Planning → Daily Scrum → Sprint Review → Retrospective

---

# Scrum artifacts

- Product Backlog
- Sprint Backlog
- Increment
- Definition of Done

---

# Kanban

Visualize work, limit work in progress, and improve continuous flow.

---

# Why Kanban fits sustain work

Incidents, defects, service requests, and improvements arrive continuously—not neatly at sprint boundaries.

---

# WIP limits reveal bottlenecks

Starting less work helps teams finish more work.

**If testing is full, stop starting and help finish.**

---

# DevOps

DevOps combines culture, automation, measurement, and shared ownership to improve delivery and reliability.

---

# DevOps is not a tool

CI/CD, containers, and cloud platforms enable DevOps.

They do not replace collaboration or accountability.

---

# CALMS

Culture · Automation · Lean · Measurement · Sharing

---

# Choose by context

Waterfall for controlled sequence. Scrum for iterative product work. Kanban for continuous flow. DevOps for shared delivery and operations.

**Real organizations often combine them.**

---

# Decision activity

Choose a method for each:

- Banking regulation change
- New loyalty feature
- Production support queue
- Daily cloud deployment

---

# Requirements create alignment

Good documents preserve the reasoning between business intent and system behavior.

> Gamma direction: Full-width `assets/03-requirements-to-release.png`.

---

# BRD: the business view

The Business Requirements Document explains **why the initiative exists and what outcome matters**.

---

# BRD contents

- Business objective
- Scope
- Stakeholders
- Success criteria
- Constraints and assumptions

---

# SRS: the system view

The Software Requirements Specification defines **what the system must do and how well it must perform**.

---

# SRS contents

- Functional requirements
- Non-functional requirements
- Interfaces
- Data requirements
- Constraints
- Error behavior

---

# FRD: the functional detail

The Functional Requirements Document describes detailed workflows, rules, inputs, outputs, and exceptions.

---

# BRD vs SRS vs FRD

BRD = business **why**

SRS = system **what**

FRD = functional **how**

---

# Traceability

Every requirement should connect to design, code, tests, release evidence, and operational monitoring.

---

# STLC

The Software Testing Life Cycle structures quality work from requirement analysis through test closure.

---

# STLC phases

Analyze → Plan → Design tests → Prepare environment → Execute → Close

---

# Shift left

Find ambiguity and risk before code is expensive to change.

**The earliest useful test is a test of the requirement.**

---

# Application type changes the test strategy

Web, mobile, API, batch, and real-time systems fail in different ways.

---

# Environments protect customers

Changes gain confidence as they move through isolated environments toward production.

> Gamma direction: Full-width `assets/04-environments.png`.

---

# Local and Development

Fast feedback, synthetic data, verbose logs, and frequent change.

**Optimized for learning—not customer traffic.**

---

# Test and Staging

Integrated services, realistic configuration, controlled test data, and release validation.

---

# Production

Real users, protected data, strict access, monitoring, backups, and formal change control.

---

# Environment parity

Keep environments similar enough that testing predicts production behavior.

**Same artifact; environment-specific configuration.**

---

# Production incident scenario

Checkout totals are wrong for discounted orders.

The team must diagnose, fix, verify, approve, deploy, monitor, and document the outcome.

> Gamma direction: Use `assets/05-sustain-response.png`; keep copy in the dark left-side negative space.

---

# The safe sustain loop

Observe → Triage → Analyze → Fix → Test → Approve → Deploy → Verify → Learn

---

# Final takeaway

**Speed is valuable only when the change remains understandable, testable, observable, and reversible.**

Next: Jira and Confluence—turning the lifecycle into visible team execution.
