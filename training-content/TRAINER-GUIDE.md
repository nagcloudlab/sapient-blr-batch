# Trainer Guide — Sustain Engineering Programme
## FoodExpress | Publicis Sapient | Bangalore | 43.5 Days

---

## 1. Training Overview

**Duration:** 43.5 days (starts July 29, 2026)
**Trainer:** Nagabhushanam
**Participants:** Sustain Engineering / SRE+ITIL track
**Incremental Project:** FoodExpress — a food delivery web application built and maintained progressively across all 37 modules

### The Core Philosophy

This is a sustain engineering programme, not a greenfield development course. Everything is framed around maintaining, debugging, and improving existing systems. The FoodExpress application starts on Day 1 and grows with every module. By the final day, participants have worked on the same codebase end-to-end — front-end to infrastructure to incident response.

### Lab Pattern: Fix the Issues

Every lab session follows the same pattern: participants receive intentionally broken starter code and a list of bugs to find and fix. This is deliberate. Sustain engineers spend most of their working lives reading code they did not write and fixing problems they did not cause. The labs simulate that reality from Day 1.

Each bug has three attributes:
- A hint describing where to look
- A description of the impact if left unfixed
- Guidance on the correct fix

Solutions are available in `Labs/solutions/` but should not be shared until after the lab session closes.

### Four Phases

| Phase | Modules | Days | Focus |
|---|---|---|---|
| Foundation | M01-M13 | 1-15 | Web, Java, Node.js, Databases, Testing |
| Process | M14-M23 | 16-26 | SDLC, Jira, DevOps, Git, Linux, Apache, Microservices |
| Platform | M24-M32 | 27-36 | Docker, Security, Jenkins, Kubernetes, Ansible |
| Sustain | M33-M37 | 37-43.5 | Observability, SRE, ITSM, ITIL, ServiceNow, GenAI, Final |

---

## 2. Daily Rhythm

### Standard Day

| Time | Activity |
|---|---|
| 09:00-09:15 | Recap / standup — what did we cover yesterday, any blockers |
| 09:15-10:30 | Slide deck walkthrough with discussion |
| 10:30-10:45 | Break |
| 10:45-12:30 | Lab exercises — bug fixing session |
| 12:30-13:30 | Lunch |
| 13:30-14:30 | Continue labs or project work |
| 14:30-15:30 | Role play or group activity (where applicable) |
| 15:30-15:45 | Break |
| 15:45-16:30 | Project time and day wrap-up |

### Capsule Days (M08, M11, M17, M28, M34, M37)

Capsule days are project integration days. Reduce slide time to a minimum (15-20 minutes max for context-setting). The rest of the day is hands-on project work and assessment. These are evaluation opportunities, not teaching days. Observe how participants apply what they have learned across modules, not just the current one.

### Standup Format

Keep the standup tight. Three questions:
1. What did you fix or build yesterday?
2. What are you working on today?
3. Is anything blocked?

Do not let this run past 09:15. It sets the tone for disciplined time management.

---

## 3. Pacing Guide per Phase

### Phase 1: Foundation (M01-M13, Days 1-15)

Go slower than you think you need to. Most participants come in with uneven backgrounds. Some will know CSS well and struggle with Java. Some will know Java but have never touched the terminal. The first two weeks are about building confidence and establishing a shared baseline.

- **Demo everything** before asking participants to attempt it themselves. Even obvious things. Show the browser dev tools. Show the error message before fixing it.
- **Let them struggle with bugs before giving hints.** The discomfort of not knowing is the point. The hint system (Section 5) governs when to intervene.
- **JavaScript and async** (M03) is where the first major friction point appears. Budget extra time. Many participants will not have encountered callbacks or Promises before.
- **Java Spring Boot** (M05-M07) is dense. M06 in particular is code-heavy. Walk through annotations slowly. Use the FoodExpress domain to make abstractions concrete (a `@RestController` that returns restaurant listings is easier to grasp than abstract examples).
- **Capsule days (M08, M11)** are the first integration check. Treat them as low-stakes rehearsals for the later formal assessments.

### Phase 2: Process (M14-M23, Days 16-26)

The balance shifts from pure technical content to process and collaboration. Concepts like SDLC, change management, and incident classification can feel abstract. The role plays are what make them real.

- **Do not skip role plays.** This is the most common mistake in process-heavy modules. Participants who sit through a lecture on incident management will forget it. Participants who have played the role of an incident commander in a simulated outage will not.
- **Jira/Confluence (M16):** Have a live Jira project open during the session. Walk through creating an actual ticket for a FoodExpress bug. Making it tangible is more effective than any slide.
- **Git (M19):** Merge conflicts are the sticking point. Create a real conflict during the demo. Resolve it live, narrating each step. Do this twice.
- **Linux (M20):** File permissions trip up almost everyone the first time. Use the analogy of a building with rooms — owner, group, and everyone else. Then demo, then lab.

### Phase 3: Platform (M24-M32, Days 27-36)

This is the most environment-dependent phase. Docker, Kubernetes, and Jenkins require working infrastructure. Failures here derail entire sessions.

- **Verify all environments before class starts** (see Section 9). Do not assume tools installed last week still work.
- **Docker (M24-M26):** Layer caching and build context cause the most confusion. Spend time on the `docker build` output — teach participants to read it, not just run it.
- **Kubernetes (M27):** YAML indentation errors are universal. Consider having participants write their first manifest in a linting-aware editor with the Kubernetes schema enabled. Debugging pods with `kubectl describe` and `kubectl logs` should become muscle memory.
- **Ansible (M31):** The jump from imperative to declarative thinking is harder than it looks. Start with a simple playbook that does something visible (install nginx, start it, check a webpage). Build complexity from there.
- **Jenkins (M29):** Walk through a full pipeline run for FoodExpress before any lab. Participants need to see the pipeline succeed once before they can diagnose why it fails.

### Phase 4: Sustain (M33-M37, Days 37-43.5)

This phase is about integration and application under pressure. Shift from teacher to facilitator. The participants should be doing most of the talking, debugging, and deciding.

- **War games and incident simulations** are the primary delivery mechanism. Inject a failure scenario into the FoodExpress environment and let teams respond.
- **SRE (M34):** Error budgets and SLO calculations work best when tied to actual FoodExpress metrics. Use the observability dashboards from M33.
- **ITIL and ServiceNow (M35-M36):** Participants often find these modules dry after the intensity of Platform. Keep sessions short and scenario-driven. Process classification exercises beat lectures every time.
- **Final assessment (M37):** The final day is not a teaching day. Set expectations clearly at the start of the programme that Day 43.5 is a demonstration of competency, not another lab session.

---

## 4. Common Participant Struggles

### CSS
- **Specificity confusion:** Participants override styles and cannot understand why their changes have no effect. Use browser dev tools to show the specificity chain live.
- **Flexbox vs grid:** A common question is "which one do I use?" The working answer: flexbox for one-dimensional layout (a nav bar, a row of cards), grid for two-dimensional layout (the full page). Then show both on FoodExpress.
- **Responsive breakpoints:** Participants write mobile styles but test only on desktop, or vice versa. Make it a habit to toggle device mode in dev tools at the end of every CSS change.

### JavaScript
- **Async/await:** The single most common point of confusion in the entire Foundation phase. The mistake is thinking `await` blocks globally. Use a concrete FoodExpress example: fetching restaurant data while the page continues to render.
- **Closures:** Abstract definitions do not land. Use a counter function example first, then show the same concept in a FoodExpress event handler.
- **DOM manipulation:** Participants query elements before the DOM is ready. Demonstrate the difference between placing a script tag in `<head>` vs end of `<body>`, and when to use `DOMContentLoaded`.
- **Event bubbling:** Show the problem by clicking a nested element and watching the parent handler fire. Then show `stopPropagation()`. This is a "show don't tell" moment.

### Java
- **Exception handling:** Participants either catch everything with a bare `catch (Exception e)` or handle nothing. Walk through the FoodExpress order placement flow and identify where each specific exception should be caught.
- **Spring Boot annotations:** The magic of `@Autowired` and `@Component` is opaque until you show what happens when you remove them. Deliberately break a Spring Boot app during the demo, then fix it.
- **Maven dependency issues:** Version conflicts are common. Teach participants to read the `mvn dependency:tree` output early.

### Node.js
- **Callback hell:** Show a real deeply nested callback, then refactor it to Promises, then to async/await. All three versions doing the same thing side by side is the clearest way to show the progression.
- **Middleware order:** Express middleware runs in declaration order. Participants put error handlers in the wrong place. Demo the effect of order by swapping middleware positions.
- **MongoDB connection errors:** Usually a connection string issue or a network/auth problem. Have a connection test script ready that prints a clear success or failure message.

### SQL
- **JOINs (LEFT vs INNER):** Use a Venn diagram and then immediately run both queries on the FoodExpress orders table. Seeing the difference in row counts is more effective than any explanation.
- **GROUP BY with HAVING:** Participants confuse WHERE and HAVING. The rule: WHERE filters rows before grouping, HAVING filters groups after. Show both failing and then show the fix.
- **Subqueries:** When a subquery returns multiple rows where one is expected, the error is confusing. Teach participants to run the inner query first and check its output before nesting it.

### Docker
- **Build context:** Participants wonder why files are missing inside the container. Explain that only what is in the build context is available, and show the `.dockerignore` file.
- **Layer caching:** A `COPY package.json` before `RUN npm install` is not cargo-culting — explain why the order matters for cache efficiency.
- **Port mapping:** `-p 3000:3000` confuses host vs container ports. Draw it as two machines connected by a pipe.
- **Volume mounts:** Participants expect files created inside a container to persist. Show that they do not without a volume, then show that they do with one.

### Kubernetes
- **YAML indentation:** One wrong space can produce a cryptic error. Recommend using a YAML linter or IDE plugin from the first session.
- **Service discovery:** Participants try to use IP addresses instead of service names. Demonstrate DNS-based service resolution within the cluster.
- **Debugging pods:** Teach `kubectl describe pod`, `kubectl logs`, and `kubectl exec -it` as the standard three-step debugging sequence. Make them do it repeatedly until it is automatic.

### Linux
- **File permissions:** `chmod 755` feels like magic numbers. Teach the binary breakdown (owner/group/other, read/write/execute) before introducing the numeric shorthand.
- **systemctl:** Participants start a service and then cannot find where its logs are. Show `journalctl -u servicename -f` immediately after any `systemctl start`.
- **Piping commands:** Start with simple pipes (one `|`) and build up. The mental model of output flowing from left to right through filters takes time to solidify.

### Git
- **Merge conflicts:** Do not just explain them — create one live. Have two participants make conflicting changes to the same FoodExpress file and then attempt to merge.
- **Rebase vs merge:** The practical guidance: use merge for integrating feature branches into main, use rebase for cleaning up your own commit history before a PR. Keep it that simple initially.
- **Detached HEAD:** Show participants how they got there (checking out a commit hash) and how to get out (`git switch -` or `git checkout main`).

### ITSM
- **Incident vs problem:** Participants conflate the two. The one-line distinction: an incident restores service, a problem finds the root cause. A restaurant order system going down is an incident. Finding out that a memory leak causes it every Monday is a problem.
- **SLA calculation:** Business hours vs calendar hours trips people up. Use a concrete FoodExpress SLA scenario with specific open and close hours.

---

## 5. Hint System

When a participant is stuck on a lab bug, do not give the answer immediately. Use the graduated hint system:

**Level 1 Hint** — Point to location
Give the file name and approximate line range. Nothing more.
Example: "Take a look at lines 45-60 in `style.css`."

**Level 2 Hint** — Describe the problem
Tell the participant what type of issue they are looking for without naming the fix.
Example: "The `position` property is set to a value that does not behave correctly inside a scrolling container on mobile."

**Level 3 Hint** — Give the fix
State exactly what needs to change.
Example: "Change `position: fixed` to `position: relative` inside the media query at the bottom of the file."

**Timing Rule:**
- Wait 10 minutes after a participant first reports being stuck before giving Level 1.
- Wait 5 more minutes before escalating to Level 2.
- Wait 5 more minutes before escalating to Level 3.

Enforce this across the room, not just per individual. If one participant gets Level 3 early, others will expect the same and stop trying. If the majority of participants are stuck on the same bug after Level 1, give Level 2 to the whole room. This is the only exception to individual timing.

---

## 6. How to Run Role Plays

Role plays appear primarily in the Process and Sustain phases (SDLC, ITSM, ITIL, incident simulation).

**Setup**
- Assign roles randomly using a name randomizer. Do not let participants choose their own roles. Self-selection leads to participants picking comfortable roles and avoiding stretch.
- Distribute printed or shared role cards. Each card describes the character, their goal in the scenario, and one piece of information only they know.
- Give 5 minutes of silent prep time. No discussion between participants during prep.

**Running the Scenario**
- Use a visible countdown timer. Project it on screen or use a physical timer.
- Do not intervene unless the scenario has completely derailed. Let imperfect role plays run. Awkward moments are learning moments.
- Take notes on specific things to raise in the debrief.

**Debrief**
Start the debrief immediately after the scenario ends. Ask specific questions, not general ones.

Good debrief questions:
- "What was the first decision made, and what information drove it?"
- "At what point did the incident commander lose track of the situation? What caused that?"
- "What would have changed if the SLA clock had been 1 hour instead of 4 hours?"
- "What did the team do that was textbook correct? What was textbook wrong?"

Avoid: "How did that go?" or "What did you think?" These produce vague answers.

**Rotation**
Run at least two rounds of any role play scenario. Rotate roles between rounds so that participants experience different perspectives (e.g., a participant who played the incident commander in round one becomes a stakeholder in round two).

---

## 7. Assessment Guidelines

### Labs
- Check that bugs are actually fixed — not commented out, not worked around, not hidden. A commented-out failing assertion is not a fix.
- Run the solution against the same criteria as the starter code to verify parity.
- Use the bug list in `lab-exercises.md` as the marking checklist. Each bug is either fixed or it is not.

### Project Work
- Use the module's `Project/CHECKLIST.md` as the rubric. Each checklist item maps to a specific requirement.
- Look for understanding, not just passing output. Ask a participant to explain one of their fixes. If they cannot, it is not assessed as complete.

### Capsule Days
- Evaluate integration across modules, not just the work done that day. A clean fix that breaks something introduced in a previous module is a failure of integration thinking.
- Observe collaboration. Who is helping others? Who is stuck but not asking? Both are worth noting.

### Role Plays
- Assess on two dimensions: participation (did they engage?) and reasoning (did their decisions follow from the information they had?). Participants should not be penalised for outcomes if their reasoning was sound given what they knew.

### MidStage Checkpoint (M34)
- This is a formal competency gate. All participants should be able to demonstrate:
  - Basic debugging across the FoodExpress stack (front-end to back-end)
  - Running and reading a CI/CD pipeline
  - Responding to a simulated incident using ITSM process
  - Navigating the Linux environment and reading logs
- Participants who cannot meet this threshold need a recovery plan before the final assessment.

### Final Assessment (M37)
- Comprehensive. Covers the full FoodExpress stack and all four phases.
- Participants should be given the scenario the morning of the final day and work through it independently (or in pairs, depending on cohort size).
- Use the final module's `Project/CHECKLIST.md` as the scoring rubric.

---

## 8. Backup Plans

### Docker or Kubernetes not available
Use screenshots of container output and dry-run YAML exercises. For Kubernetes, walk through manifests line by line and trace what would happen at each step. Ask participants to predict the outcome before revealing it. This is less effective than live execution but preserves the conceptual content.

### MySQL not installed
Use SQLite for all SQL labs. The syntax differences are minimal for the queries used in this programme. Alternatively, use an online SQL playground such as sqliteonline.com — all FoodExpress schema and seed data can be pasted in.

### Network down
- All slides are offline HTML files (`PPT/slides.html`) and require no internet connection.
- All lab starter code is local (`Labs/starter-code/`).
- Solutions are local (`Labs/solutions/`).
- The FoodExpress application does not depend on any external APIs.
- The only gap is ServiceNow (M36), which is SaaS-based. Substitute with offline screenshots and a process walk-through exercise.

### Participants are ahead of schedule
Every lab has bonus challenges at the end of `lab-exercises.md`. Direct fast finishers there. Additionally, ask them to write up what they fixed and why — this reinforces understanding and produces useful documentation for slower participants later.

### Participants are behind schedule
- Identify the critical bugs in the current lab (bugs that would prevent the next module's starter code from working) and focus there.
- Skip enhancement tasks entirely.
- Do not skip capsule days to recover time — they are integration checks and cannot be deferred without losing visibility into participant progress.
- If an entire cohort is consistently behind, review pacing. The most common cause is spending too long on JavaScript async or Java Spring Boot in the Foundation phase.

---

## 9. Environment Checklist

Run through this before the start of every module. Do not rely on checks done the previous day.

### Universal (every module)
- [ ] `PPT/slides.html` opens correctly in Chrome or Firefox without errors
- [ ] Lab starter code is in place in `Labs/starter-code/`
- [ ] Solutions are available locally in `Labs/solutions/` (trainer only — not shared with participants)
- [ ] Module `Project/BRIEF.md`, `SOLUTION.md`, and `CHECKLIST.md` are accessible

### Foundation Phase (M01-M13)
- [ ] Node.js installed and `node --version` returns expected version
- [ ] Java JDK installed and `javac --version` returns expected version
- [ ] Maven installed and `mvn --version` returns expected version
- [ ] MySQL running and FoodExpress schema loaded
- [ ] Browser dev tools accessible (demo at least once on Day 1)

### Process Phase (M14-M23)
- [ ] Jira project exists and is accessible
- [ ] Confluence space exists and is accessible
- [ ] Git installed and `git --version` returns expected version
- [ ] A test repository with intentional merge conflict exists for Git demo
- [ ] Linux VM or WSL accessible for Linux module

### Platform Phase (M24-M32)
- [ ] Docker installed, daemon running, and `docker ps` returns without error
- [ ] Docker Hub accessible (or local registry if network is restricted)
- [ ] FoodExpress Docker images build successfully from `Labs/starter-code/`
- [ ] Kubernetes cluster accessible (`kubectl get nodes` returns ready nodes)
- [ ] Jenkins instance running and accessible via browser
- [ ] Ansible installed and control node can reach managed hosts

### Sustain Phase (M33-M37)
- [ ] Prometheus and Grafana running with FoodExpress metrics flowing
- [ ] At least one alerting rule configured and triggering correctly on test data
- [ ] ServiceNow developer instance accessible (or backup plan confirmed)
- [ ] Incident simulation environment ready (FoodExpress with injected failure)
- [ ] Final assessment scenario prepared and not visible to participants

---

*Last updated: 2026-07-27*
