# FoodExpress -- Incremental Capstone Project
## Sustain Engineering Training | 43.5 Days

---

## What Is This?

A module-wise incremental food delivery application used as the capstone for a 43.5-day Sustain Engineering training programme. Each module folder contains:

- **PPT/** -- Presentation slides (HTML slide deck + Gamma markdown)
- **Labs/starter-code/** -- Buggy FoodExpress code for that module's topic
- **Labs/solutions/** -- Fixed, working code
- **Labs/lab-exercises.md** -- Bug hunt list (fix-the-issues format)
- **Project/BRIEF.md** -- Sustain scenario and tasks (what participants see)
- **Project/SOLUTION.md** -- Trainer-only answers and hints
- **Project/CHECKLIST.md** -- Participant submission checklist

---

## How It Works

1. Each module, participants receive THAT module's folder
2. Previous module's bugs are already fixed in the new version
3. New bugs are planted for the current topic
4. Participants fix/improve things as a sustain engineer would
5. Every module is runnable -- participants can see the bugs in action

---

## Architecture (What Participants Are Sustaining)

```
[Frontend HTML/CSS/JS]  -->  [Restaurant Service Node:3000]  -->  [MongoDB]
                        -->  [Cart Service Node:3001]        -->  [MongoDB]
                        -->  [Order Service Java:8080]       -->  [MySQL]
                        -->  [Delivery Service Node:3002]    -->  [MongoDB]
                        -->  [Payment Service Node:3003]     -->  [External Gateway]
```

## Framing

Participants are a **sustain engineering team**. They inherit FoodExpress -- a pre-built food delivery platform handed over by the development team. Every single day of training, they perform real sustain work: fixing bugs, making enhancements, tuning performance, deploying changes, responding to incidents, writing documentation.

> "You are the sustain team. FoodExpress is live. Customers are ordering food. Things break. Restaurants request changes. Your job: keep it running, make it better, respond fast."

---

## Module-by-Module Index

| # | Module | Day(s) | Duration | Runnable? | How to Run |
|---|--------|--------|----------|-----------|-----------|
| 01 | HTML & CSS | 0-1 | 0.5d | Browser | Open index.html |
| 02 | CSS Frameworks | 2 | 1d | Browser | Open index.html |
| 03 | JavaScript Part 1 | 3 | 1d | Browser | Open index.html |
| 04 | UI Frameworks (React) | 4-5 | 1d | npm start | `cd frontend && npm install && npm start` |
| 05 | Java Part 1 | 6 | 1d | Maven | `cd order-service && mvn spring-boot:run` |
| 06 | Java Part 2 | 7 | 1d | Maven | `cd order-service && mvn spring-boot:run` |
| 07 | Java Part 3 | 8 | 1d | Maven | `cd order-service && mvn spring-boot:run` |
| 08 | Java Capsule | 9 | 1d | Maven | Full stack integration |
| 09 | Node.js Part 1 | 10 | 1d | npm start | `npm install && npm start` |
| 10 | Node.js Part 2 | 11 | 0.5d | npm start | `npm install && npm start` |
| 11 | Node.js Capsule | 12 | 1d | npm start | Full service integration |
| 12 | Database & SQL | 13 | 1d | MySQL | `mysql -u root -p < schema.sql` |
| 13 | QE/QC Testing | 14 | 1d | Jest/JUnit | `npm test` / `mvn test` |
| 14 | Infrastructure | 15 | 1d | N/A | Process exercises |
| 15 | SDLC | 16 | 1d | N/A | Process exercises |
| 16 | Jira/Confluence | 17 | 1d | N/A | Tool exercises |
| 17 | Integration Capsule | 18 | 1d | All | Full stack + JIRA |
| 18 | DevOps | 19 | 1d | N/A | Pipeline design |
| 19 | Git/GitHub | 20 | 1d | Git CLI | Git exercises |
| 20 | Linux | 21 | 1d | Shell | Terminal/SSH exercises |
| 21 | Apache | 22 | 1d | Apache | Config + restart |
| 22 | Microservices & API | 23 | 1d | npm/mvn | All services running |
| 23 | Platform Capsule | 24 | 1d | All | Full stack troubleshooting |
| 24 | Docker Part 1 | 25 | 1d | Docker | `docker build` / `docker run` |
| 25 | Docker Part 2 | 26 | 1d | Docker | `docker build` + volumes |
| 26 | Docker Part 3 | 27 | 1d | Docker | `docker-compose up` |
| 27 | Secure Engineering | 28 | 1d | All | Security audit exercises |
| 28 | Jenkins | 29 | 1d | Jenkins | Run pipeline |
| 29 | Kubernetes | 30 | 1d | kubectl | `kubectl apply -f manifests/` |
| 30 | Ansible | 31 | 1d | Ansible | `ansible-playbook deploy.yml` |
| 31 | DevOps Capsule | 32 | 1d | All | Full DevOps pipeline |
| 32 | Observability | 33 | 1d | Docker | Prometheus + Grafana via compose |
| 33 | SRE | 34 | 1d | All | SLO/error budget exercises |
| 34 | MidStage + ITSM | 35-38 | 2d | All | War game + ITSM exercises |
| 35 | ITIL | 39-40 | 1.5d | N/A | ITIL practice exercises |
| 36 | ServiceNow | 41-42 | 1.5d | ServiceNow | Tool exercises |
| 37 | Final + GenAI | 43-44 | 1.5d | All | Capstone + AI labs |

---

## Prerequisites (Full Programme)

- Node.js 18+
- Java 17+ / Maven 3.8+
- MySQL 8.0
- MongoDB 7.0
- Docker + Docker Compose
- kubectl + minikube
- Ansible
- Apache2
- Jenkins
- VS Code (recommended)

---

## Related Documents

- [SETUP.md](../SETUP.md) -- Environment setup guide (install prerequisites)
- [PARTICIPANT-GUIDE.md](../PARTICIPANT-GUIDE.md) -- Participant onboarding guide
- [COURSE-MAP.md](../COURSE-MAP.md) -- Full 37-module course index
- [PROGRESSION.md](PROGRESSION.md) -- Code evolution across modules

## For Trainers

- `BUGS.md` -- Master list of ALL planted bugs, mapped by module (310+ tasks)
- [TRAINER-GUIDE.md](../TRAINER-GUIDE.md) -- Delivery guide with pacing, hints, backup plans
- Each module's `Project/SOLUTION.md` -- Full answers + hints
- Never share SOLUTION.md with participants!

---

## FoodExpress Color Scheme

- Primary Red: #e84c3d
- Dark Blue: #2c3e50
- Success Green: #27ae60
