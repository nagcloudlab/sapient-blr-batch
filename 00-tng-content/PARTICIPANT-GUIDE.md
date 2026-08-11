# Participant Guide — Sustain Engineering Training
**Publicis Sapient | Bangalore | July 29 – September 26, 2026**
**Trainer: Nagabhushanam | Duration: 43.5 Days**

---

## 1. Welcome

Welcome to the Publicis Sapient Sustain Engineering training programme.

Over the next 43.5 days, you will build the practical skills that a sustain engineering (SRE + ITIL) professional uses every day. The programme spans the full technology stack — from HTML and Java through to Docker, Kubernetes, Ansible, Observability, SRE practices, ITSM, and ITIL — and is structured around a single, real-world scenario that evolves with you as the training progresses.

The incremental project running through this training is **FoodExpress**, a food delivery application. You will inherit an existing codebase, diagnose issues across its services, fix them, and extend the system — exactly what a sustain engineering team does in production.

By the end, you will have hands-on experience across every layer of the stack, a working knowledge of ITIL and ITSM processes, and a portfolio of fixes and enhancements applied to a real, multi-service application.

---

## 2. How This Training Works

### You are the sustain engineering team

FoodExpress is already "live". Your team has been handed the codebase mid-life. There are known bugs, technical debt, and gaps in observability. Your job, module by module, is to stabilise it, improve it, and keep it running.

### Each module follows the same three-step pattern

1. **Learn concepts (slides)** — The trainer walks through the topic using slides. Follow along, ask questions, and take notes. Slides are concept-focused; the project details are in the labs and project exercises.
2. **Fix bugs (labs)** — Each module's starter code has intentional bugs planted in it. You receive a bug list with hints. Your job is to locate each bug, understand why it is wrong, and fix it.
3. **Apply to the project (project exercises)** — After the lab, you apply what you have learned to the FoodExpress project brief for that module.

### The "Fix the Issues" lab pattern

Sustain engineering is overwhelmingly about understanding and fixing existing code, not writing from scratch. The labs reflect this reality:

- Starter code is provided in `Labs/starter-code/` — it runs but has intentional bugs.
- `Labs/lab-exercises.md` gives you a numbered bug list with hints (location, symptom, what to look for).
- You work through the list, fix each bug, and verify using the checkpoints provided.
- Bonus challenges are available for fast finishers.
- Reference solutions are in `Labs/solutions/` — use them only after you have made a genuine attempt.

### Labs build on each other

Each module's starter code is the previous module's solution with new bugs introduced for the current topic. This means your fixes carry forward. Do not skip or shortcut earlier modules; the later labs depend on them being in a clean state.

### Capsule days

Modules 08, 11, 17, 23, and 31 are **capsule days** — integration and project days where you apply everything learned in the preceding modules to a larger FoodExpress scenario. There are no new concept slides on capsule days. The full session is dedicated to project work and review.

---

## 3. How to Use the Materials

All training materials are organised by module folder:

```
Module-XX-TopicName/
    PPT/
        slides.html           -- slide deck for this module
        Module-XX-TopicName.md -- Gamma-importable version of the deck
    Labs/
        lab-exercises.md      -- your bug list and instructions
        starter-code/         -- buggy code to fix
        solutions/            -- reference solutions
    Project/
        BRIEF.md              -- your assignment for this module
        SOLUTION.md           -- trainer reference solution
        CHECKLIST.md          -- submission checklist
```

### Slides

Open `PPT/slides.html` in **Google Chrome**. Use the left and right arrow keys to navigate between slides. No installation required.

### Labs

Start with `Labs/lab-exercises.md`. It tells you exactly which files to open, what to look for, and how to verify your fix. Work through the bugs in order — they are sequenced by difficulty and dependency.

Starter code is in `Labs/starter-code/`. Do not modify files inside `Labs/solutions/` until you have completed your own attempt.

### Project exercises

Read `Project/BRIEF.md` to understand your assignment. Use `Project/CHECKLIST.md` to verify your submission before declaring it complete.

---

## 4. How to Run Labs by Technology

The following commands apply to the typical setup for each module group. Your lab exercises will include any module-specific variations.

| Modules | Technology | How to Run |
|---------|-----------|------------|
| M01–M03 | HTML / CSS / JavaScript | Open `index.html` in Chrome. Use DevTools (F12) for debugging. |
| M04 | React (UI Frameworks) | `cd frontend && npm install && npm start` |
| M05–M08 | Java / Spring Boot | `cd order-service && mvn spring-boot:run` |
| M09–M11 | Node.js | `npm install && npm start` |
| M12 | Database / SQL | `mysql -u root -p < schema.sql` |
| M13 | QE / QC | `npm test` (frontend) or `mvn test` (backend) |
| M15–M16 | SDLC / Jira | Process exercises — no code to run |
| M19 | Git / GitHub | Git CLI exercises in terminal |
| M20 | Linux | Terminal or SSH exercises |
| M21 | Apache | Edit Apache config files, then restart: `sudo systemctl restart apache2` |
| M24–M26 | Docker | `docker build -t foodexpress .` / `docker-compose up` |
| M28 | Jenkins | Jenkins pipeline via browser UI or Jenkinsfile |
| M29 | Kubernetes | `kubectl apply -f manifests/` |
| M30 | Ansible | `ansible-playbook deploy.yml` |
| M32 | Observability | `docker-compose up` (Prometheus + Grafana stack) |

> **Prerequisite software:** Ensure Node.js (v18+), Java 17+, Maven, MySQL, Docker Desktop, and kubectl are installed before Day 1. Your trainer will confirm the exact versions during onboarding.

---

## 5. FoodExpress Project Overview

FoodExpress is a multi-service food delivery application. Each service is owned by a different technology stack, which is why it is an ideal vehicle for a full-stack sustain engineering programme.

```
                        [ Browser ]
                            |
                     [ Frontend ]
                  HTML / CSS / JS / React
                            |
          +-----------------+-----------------+
          |                 |                 |
  [ Restaurant Service ] [ Cart Service ] [ Order Service ]
    Node.js : 3000         Node.js : 3001   Java : 8080
    MongoDB                MongoDB          MySQL
          |                                   |
          +-----------------------------------+
                            |
                   [ Delivery Service ]
                     Node.js : 3002
                     MongoDB
```

| Service | Port | Runtime | Database |
|---------|------|---------|----------|
| Frontend | — | HTML / CSS / JS / React | — |
| Restaurant Service | 3000 | Node.js | MongoDB |
| Cart Service | 3001 | Node.js | MongoDB |
| Order Service | 8080 | Java (Spring Boot) | MySQL |
| Delivery Service | 3002 | Node.js | MongoDB |

Each module's labs and project exercises will target one or more of these services. By the end of the programme, you will have touched every layer of this architecture.

---

## 6. Day-by-Day Schedule

August 15 (Independence Day) is a national holiday and has been excluded. All other weekdays are training days.

| Day | Date | Module | Topic | Duration |
|-----|------|--------|-------|----------|
| 0–1 | Tue 29 Jul | M01 | HTML & CSS | 0.5d |
| 2 | Wed 30 Jul | M02 | CSS Frameworks | 1d |
| 3 | Thu 31 Jul | M03 | JavaScript Part 1 | 1d |
| 4–5 | Fri 1 Aug | M04 | UI Frameworks (React) | 1d |
| 6 | Mon 4 Aug | M05 | Java Part 1 | 1d |
| 7 | Tue 5 Aug | M06 | Java Part 2 | 1d |
| 8 | Wed 6 Aug | M07 | Java Part 3 | 1d |
| 9 | Thu 7 Aug | M08 | Java Capsule | 1d |
| 10 | Fri 8 Aug | M09 | NodeJS Part 1 | 1d |
| 11 | Mon 11 Aug | M10 | NodeJS Part 2 | 0.5d |
| 12 | Tue 12 Aug | M11 | NodeJS Capsule | 1d |
| 13 | Wed 13 Aug | M12 | Database SQL | 1d |
| 14 | Thu 14 Aug | M13 | QE / QC | 1d |
| — | Fri 15 Aug | — | Independence Day (Holiday) | — |
| 15 | Mon 18 Aug | M14 | Infrastructure | 1d |
| 16 | Tue 19 Aug | M15 | SDLC | 1d |
| 17 | Wed 20 Aug | M16 | Jira / Confluence | 1d |
| 18 | Thu 21 Aug | M17 | Integration Capsule | 1d |
| 19 | Fri 22 Aug | M18 | DevOps | 1d |
| 20 | Mon 25 Aug | M19 | Git / GitHub | 1d |
| 21 | Tue 26 Aug | M20 | Linux | 1d |
| 22 | Wed 27 Aug | M21 | Apache | 1d |
| 23 | Thu 28 Aug | M22 | Microservices / API | 1d |
| 24 | Fri 29 Aug | M23 | Platform Capsule | 1d |
| 25 | Mon 1 Sep | M24 | Docker Part 1 | 1d |
| 26 | Tue 2 Sep | M25 | Docker Part 2 | 1d |
| 27 | Wed 3 Sep | M26 | Docker Part 3 | 1d |
| 28 | Thu 4 Sep | M27 | Secure Engineering | 1d |
| 29 | Fri 5 Sep | M28 | Jenkins | 1d |
| 30 | Mon 8 Sep | M29 | Kubernetes | 1d |
| 31 | Tue 9 Sep | M30 | Ansible | 1d |
| 32 | Wed 10 Sep | M31 | DevOps Capsule | 1d |
| 33 | Thu 11 Sep | M32 | Observability | 1d |
| 34 | Fri 12 Sep | M33 | SRE | 1d |
| 35–38 | Mon–Thu 15–18 Sep | M34 | MidStage + ITSM | 2d |
| 39–40 | Fri 19 Sep, Mon 22 Sep | M35 | ITIL | 1.5d |
| 41–42 | Tue–Wed 23–24 Sep | M36 | ServiceNow | 1.5d |
| 43–44 | Thu–Fri 25–26 Sep | M37 | Final Presentations + GenAI | 1.5d |

**Programme end date: Friday, 26 September 2026.**

---

## 7. Tips for Success

**Always attempt the bug before looking at the solution.**
The value is in the diagnostic process, not the answer. If you look up the solution immediately, you lose the opportunity to build the muscle memory that makes you effective in production incidents.

**Use Chrome DevTools (F12) extensively.**
For frontend labs, DevTools is your primary debugging tool. Get comfortable with the Console, Elements, Network, and Sources panels. Sustain engineers live in DevTools.

**Keep a personal fix log.**
After each lab, note the bug, the symptom, and how you found it. A one-line entry per bug is enough. Over 43 days, this log becomes a personal reference you will actually use on the job.

**Take screenshots of your fixes.**
Capture the broken state and the fixed state for each lab. This gives you evidence for your portfolio and makes the CHECKLIST.md submissions straightforward.

**Do not skip the project exercises.**
The project brief is where concepts are applied in a realistic context. The labs teach you the technique; the project brief teaches you the judgement.

**Ask questions during role plays and walkthroughs.**
The trainer-led walkthroughs are your best opportunity to ask "why does this fail in this specific way?" and get an expert answer. Use that time.

**Stay current with the codebase state.**
Because each module's starter code builds on the previous module's solution, falling behind creates compound debt. If you are struggling with a module, flag it early so the trainer can help you get back to a clean baseline before the next session.

**Capsule days are assessments in practice.**
On M08, M11, M17, M23, and M31, there are no new slides. The entire day is project work. Come prepared: review your notes from the preceding modules the evening before.

---

*Publicis Sapient Sustain Engineering Training | Bangalore 2026 | Trainer: Nagabhushanam*
