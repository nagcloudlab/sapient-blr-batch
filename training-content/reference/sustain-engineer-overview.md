# What is a Sustain Engineer?

**Document purpose:** Participant orientation — to be read or discussed on Day 0 before the first module begins.

---

## The Simple Definition

A sustain engineer is an engineer whose primary job is to keep existing software systems healthy, not to build new ones.

That one sentence contains an important distinction. Most software engineering training focuses on creation: how to design a system, how to write features, how to build something from nothing. Sustain engineering is different. The system already exists. Users are already using it. The sustain engineer's job is to make sure it stays working, stays fast, stays secure, and stays improving — reliably, day after day.

The word "sustain" is deliberate. It means to maintain over time, to support under pressure, and to keep going when things go wrong. That is the job.

---

## The House Analogy

A useful way to understand the relationship between different engineering roles is to think about a house.

The **architects and builders** design and construct the house. They choose the layout, pour the foundation, wire the electricity, and hand over the keys. Their job is to create.

Once the house is occupied, a completely different set of professionals take over. The **plumber** fixes the leak under the sink. The **electrician** investigates why a circuit keeps tripping. The **handyman** patches the wall after a shelf bracket fails. When something breaks at 2 AM, these are the people who get the call.

In software:

| Role | Analogy |
|---|---|
| Software Developer | Builder — designs and constructs features |
| Sustain Engineer | Maintenance professional — keeps it working after handover |
| SRE | Building manager — sets the reliability standards and automates maintenance |
| L1 Support | Reception desk — receives reports, logs them, escalates |
| DevOps Engineer | Building systems specialist — manages the pipes, heating, and electrical (infrastructure) |

The sustain engineer is the maintenance professional. They did not design the house. They may not even know everyone who built it. But they are responsible for making sure the lights stay on and the pipes do not burst — and if they do burst, fixing them correctly and making sure it does not happen again.

---

## What Does a Sustain Engineer Actually Do?

Nine activities make up the core of sustain engineering work. Every module in this programme maps to one or more of them.

| Activity | Description | Example on FoodExpress |
|---|---|---|
| Monitor | Watch system metrics, logs, and alerts to detect problems before users do | Check Grafana dashboard for latency spikes on the order placement API |
| Incident Response | Detect, triage, coordinate, and resolve live production problems under time pressure | Payment service is returning 500 errors; restaurants stop receiving orders |
| Bug Fixes | Investigate defects raised by users, monitoring, or QA; apply a targeted fix; verify | Cart total displaying NaN when a coupon is applied to a single item |
| Enhancements | Small, low-risk improvements to existing features within a defined change window | Restaurant search to support partial name matching in addition to exact match |
| Performance | Profile slow endpoints, optimise database queries, reduce response times | Order history page takes 8 seconds to load for users with more than 50 orders |
| Deployment | Push changes through the CI/CD pipeline; manage staging and production releases; handle rollbacks | Deploy the cart fix through Jenkins; verify in staging before promoting to production |
| RCA | Root cause analysis — after an incident closes, document what happened, why, and how to prevent it | Post-mortem: MongoDB connection pool exhausted during Friday evening peak |
| Documentation | Write and maintain runbooks, knowledge base articles, and architecture notes | Runbook: how to restart the delivery service during a pod crash loop |
| SLA Management | Track service level objectives; report breach risk; escalate appropriately | Delivery ETA accuracy is at 94% this week; SLO is 95%; raise with the team |

Notice that none of these activities involve designing and building a new application. They are all about operating, maintaining, and improving what already exists.

---

## Sustain Engineer vs Other Roles

Teams in technology organisations include many different roles. Sustain engineers are often confused with several of them. The distinctions matter.

| Dimension | Developer | Sustain Engineer | SRE | L1 Support | DevOps Engineer |
|---|---|---|---|---|---|
| Primary focus | Create new features | Keep existing system healthy | Define and enforce reliability standards | Receive and log user reports | Build and manage infrastructure and pipelines |
| Typical output | New code merged via PR | Bug fix, runbook, post-mortem | SLO definition, alerting rule, automation | ServiceNow ticket, escalation | Pipeline, Dockerfile, Kubernetes manifest |
| Relationship to production | Infrequent, via CI/CD | Daily — monitors and responds | Governance and automation | No direct system access | Builds and maintains the delivery path |
| Incident role | Often not on-call | First technical responder | Escalation + post-mortem lead | Ticket creator, customer communicator | Infrastructure recovery |
| Coding | Most of the time | Part of the time (fixes, tests, scripts) | Significant (automation, tooling) | Rarely | Significant (infrastructure as code) |
| Typical tools | IDE, Git, Jira | Grafana, logs, Git, ServiceNow, Jenkins | Prometheus, Terraform, Runbooks | ServiceNow, email | Ansible, Docker, Kubernetes, Jenkins |

A sustain engineer sits between the developer and the SRE. They do write code — but targeted fixes, not features. They do use infrastructure tools — but to operate a system, not to architect one. They are the first technical contact when something goes wrong in production.

---

## Why Do Companies Need Sustain Engineers?

A software product does not stop requiring engineering attention once it is built and launched. In many ways, the engineering work intensifies after launch.

**Production traffic reveals problems that testing never found.** Edge cases, load patterns, third-party dependency failures, and user behaviour that no one anticipated all appear only in production. Someone has to catch them and fix them.

**Systems require updates.** Security patches, dependency upgrades, compliance changes, and evolving business rules all require changes to existing systems. Making those changes safely — without introducing new bugs, without causing downtime — is skilled work.

**Users report bugs continuously.** A popular application with tens of thousands of daily users will generate a stream of defect reports. Triaging them, reproducing them, fixing them, and closing them is a full-time engineering activity.

**Incidents happen regardless of how well a system is built.** External services fail. Databases fill up. Deployments go wrong. Traffic spikes unexpectedly. When incidents happen, someone with engineering skill and production knowledge needs to respond immediately.

**The original developers move on.** Systems outlive their creators. The team that built an application is rarely the same team operating it two years later. The sustain engineer has to read, understand, and modify code written by people they have never met.

For all these reasons, large engineering organisations — including Publicis Sapient's delivery and sustain practices — maintain dedicated sustain engineering teams alongside development teams. The development team builds new capabilities. The sustain team keeps the existing system healthy while those new capabilities are being built.

---

## The Publicis Sapient Context

At Publicis Sapient, sustain engineering is a recognised career track and a billable service offering. Clients engage Publicis Sapient not only to build digital products but to operate and sustain them after go-live.

A sustain engineer at Publicis Sapient is accountable to the client for the health of their production systems. This means:

- Responding to incidents according to agreed SLAs (P1 within 15 minutes, P2 within 2 hours, and so on)
- Managing changes through formal change control processes (ITIL-aligned)
- Reporting on system health, incident trends, and SLO performance to client stakeholders
- Following the client's tooling: usually Jira for project tracking, ServiceNow for ITSM, and Confluence for knowledge management
- Working within defined change windows — production deployments do not happen at arbitrary times

This is professional services engineering. The client can see the ticket, the SLA, and the post-mortem. Quality of work is directly visible to the client in a way that internal development work often is not.

This programme prepares you for exactly that context. Every lab, every war game, every ServiceNow ticket you raise during this training is modelled on the way sustain work is delivered at Publicis Sapient.

---

## A Day in the Life — FoodExpress Sustain Engineer

This is a representative day for a sustain engineer on the FoodExpress account. It is not every day — some days are quieter, some are much more intense. But it illustrates the range of activities across a single shift.

**09:00 — Check the Grafana dashboard**

You open the FoodExpress observability dashboard that your team maintains. You scan the key panels: order success rate, p95 latency on the Restaurant Service, cart abandonment rate, delivery ETA accuracy, and payment gateway response time. Everything is within SLO thresholds. You note that the restaurant search latency has crept up slightly since yesterday — not a breach yet, but worth watching.

**09:30 — Check application logs**

You tail the logs from the previous night. There is a cluster of MongoDB connection timeout errors between 02:15 and 02:22. The service recovered on its own, but the errors are there. You note the timestamps and the error message: `MongoNetworkTimeoutError: connection timed out after 30000ms`. This is worth investigating.

**10:00 — Log the incident in ServiceNow**

Even though the system recovered, you raise a problem record in ServiceNow. The timeout cluster is a recurring pattern — this is the third time in two weeks you have seen it at the same time of night. You attach the relevant log lines, link to the Grafana panel showing the connection pool metric, and assign the problem to yourself for investigation.

**11:00 — Fix the slow query and write a test**

The search latency you noticed this morning traces to a missing index on the `cuisine` field in MongoDB. Orders that filter by cuisine type are doing full collection scans instead of index lookups. You check the current index definitions, confirm the gap, write the index creation migration, and add a unit test that verifies query execution uses the index. You push the change to a feature branch and raise a pull request.

**13:00 — Change request for tomorrow's deployment**

The pull request has been reviewed and approved. You raise a change request in ServiceNow for tomorrow's deployment window (Tuesday 22:00–23:00 local). You fill in the risk assessment, the rollback plan (drop the index if latency worsens), and the verification steps (check Grafana search latency panel 10 minutes after deployment). The change request goes to the client's change advisory board for approval.

**14:00 — Deploy the fix via Jenkins**

The change request is approved. You trigger the Jenkins pipeline for the FoodExpress staging environment. The pipeline runs the test suite (all passing), builds the Docker image, and deploys to staging. You run a manual smoke test: search for "burgers" and confirm the response time is under 100ms. You verify the Grafana staging dashboard shows no latency anomaly. Deployment to production is scheduled for tonight.

**15:00 — Verify on Grafana after deployment**

You monitor the production Grafana dashboard for 20 minutes after the deployment window closes. Search latency has dropped from a p95 of 340ms to 45ms. You update the ServiceNow change request: implementation complete, verified, closed successfully.

**16:00 — Write the knowledge base article**

You write a short Confluence article: "FoodExpress MongoDB — Adding indexes for cuisine and location search fields." You include the symptoms that prompted the investigation, the index commands used, the expected performance improvement, and a link to the Jenkins pipeline run. The next time a team member sees search latency creeping up, they have a starting point.

**End of shift — Handover notes**

You write three lines in the team handover document: the MongoDB timeout problem record is open and under investigation; the search latency fix is deployed and verified; the overnight on-call engineer should watch the MongoDB connection pool metric between 02:00 and 03:00.

That is a sustain engineer's day. No new features were built. Three production issues were addressed: one proactively (latency), one reactively (timeout pattern), one preventively (knowledge article). The system is healthier at 17:00 than it was at 09:00.

---

## How This Programme Maps to Sustain Skills

Every module in this training directly develops one or more of the nine sustain engineering activities listed above.

| Module | Topic | Sustain Skills Developed |
|---|---|---|
| M01 | HTML & CSS | Bug Fixes — read and repair a frontend layout defect |
| M02 | CSS Frameworks | Bug Fixes, Enhancements — fix responsive layout issues in Bootstrap |
| M03 | JavaScript | Bug Fixes — trace and correct a calculation error in client-side code |
| M04 | UI Frameworks | Bug Fixes, Enhancements — debug React component state and props |
| M05–07 | Java Parts 1–3 | Bug Fixes — read, trace, and repair Java service logic |
| M08 | Java Capsule | Bug Fixes, Deployment — integrate fixes across a service boundary |
| M09–10 | Node.js Parts 1–2 | Bug Fixes — repair Node.js service behaviour and API responses |
| M11 | Node.js Capsule | Bug Fixes, Deployment — integrate Node.js service fixes |
| M12 | Database SQL | Performance — identify and fix slow queries; design missing indexes |
| M13 | QE/QC | Bug Fixes — write tests that verify a fix and prevent regression |
| M14 | Infrastructure | Monitor, Incident Response — understand the environment the application runs in |
| M15 | SDLC | Deployment, SLA Management — understand how changes flow to production |
| M16 | Jira/Confluence | Documentation, SLA Management — raise bugs, write runbooks |
| M17 | Integration Capsule | All nine — mini sustain sprint across the full ticket-to-deploy cycle |
| M18 | DevOps | Deployment — CI/CD pipelines, automated quality gates |
| M19 | Git/GitHub | Bug Fixes, Deployment — branching, PRs, hotfix workflow |
| M20 | Linux | Monitor, Incident Response — command-line log tailing, process management |
| M21 | Apache | Monitor, Incident Response — web server logs, reverse proxy configuration |
| M22 | Microservices/API | Bug Fixes, Incident Response — trace failures across service boundaries |
| M23 | Platform Capsule | Deployment — full end-to-end change from ticket to production |
| M24–26 | Docker | Deployment — containerise services, debug container failures |
| M27 | Secure Engineering | Bug Fixes — identify and remediate security misconfigurations |
| M28 | Jenkins | Deployment — build and maintain CI pipelines |
| M29 | Kubernetes | Deployment, Incident Response — scale services, recover from pod failures |
| M30 | Ansible | Deployment — automate environment provisioning and configuration |
| M31 | DevOps Capsule | Deployment — full pipeline from Git to Kubernetes |
| M32 | Observability | Monitor — instrument services, build dashboards, configure alerts |
| M33 | SRE | SLA Management, Monitor — define SLOs, calculate error budgets |
| M34 | Mid-Stage War Game + ITSM | Incident Response, SLA Management — live incident simulation under ITSM process |
| M35 | ITIL | Incident Response, RCA, Documentation, SLA Management — ITIL 4 practice framework |
| M36 | ServiceNow | All nine — raise incidents, changes, problems, and knowledge articles |
| M37 | Final War Game + GenAI | All nine — full production simulation with AI-assisted tooling |

By the end of Module 37, you will have practised every sustain engineering activity, repeatedly, on the same application, using the same tools that Publicis Sapient uses on client engagements.

---

*This document is part of the FoodExpress Training Programme — Sustain Engineering (SRE + ITIL).*
*Trainer: Nagabhushanam | Publicis Sapient | Bangalore | July 29, 2026*
*See also: `TRAINER-GUIDE.md`, `COURSE-MAP.md`, `Presentation-Flow.md`*
