# DevOps Capsule Project
## Module 31 | Sustain Engineering Training | Days 34-35

---

## Agenda -- Day 34

| # | Topic |
|---|-------|
| 01 | Project Brief & Architecture Overview |
| 02 | Sprint Planning & Task Allocation |
| 03 | Sprint 1: Containerize FoodExpress Services |
| 04 | Sprint 2: CI/CD Pipeline with Jenkins |
| 05 | Sprint 3: Kubernetes Deployment |
| 06 | Day 34 Checkpoint & Progress Review |

---

## Agenda -- Day 35

| # | Topic |
|---|-------|
| 01 | Sprint 4: Ansible Configuration & Integration |
| 02 | Sprint 5: End-to-End Testing & Polish |
| 03 | Team Presentations (15 min each) |
| 04 | Peer Review & Feedback |
| 05 | Evaluation & MCQ Assessment |
| 06 | Retrospective & Lessons Learned |
| 07 | Days 34-35 Wrap-up |

---

## Project Overview

### Build a Complete DevOps Pipeline for FoodExpress

```
┌──────┐    ┌──────────┐    ┌─────────┐    ┌──────┐    ┌──────┐
│ Git  │───>│ Jenkins  │───>│ Docker  │───>│  K8s │───>│Ansible│
│Push  │    │ Pipeline │    │ Build   │    │Deploy│    │Config │
└──────┘    └──────────┘    └─────────┘    └──────┘    └──────┘
                │                              │
                ▼                              ▼
         ┌──────────┐                   ┌──────────┐
         │  Tests   │                   │ Health   │
         │  (unit,  │                   │ Checks   │
         │  lint)   │                   └──────────┘
         └──────────┘
```

**Goal:** Take FoodExpress from source code to a running Kubernetes deployment with automated CI/CD and configuration management.

---

## Team Structure

### Teams of 3-4 people

| Role | Responsibility |
|------|---------------|
| **DevOps Lead** | Pipeline design, Jenkins configuration, integration |
| **Container Engineer** | Dockerfiles, docker-compose, image optimization |
| **K8s Engineer** | K8s manifests, services, probes, scaling |
| **Config Engineer** | Ansible playbooks, templates, secrets management |

> In a team of 3, the DevOps Lead also handles Ansible tasks.

---

## Architecture: What You Will Build

```
┌─────────────────────────────────────────────────────────┐
│                    FoodExpress DevOps                    │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │                  Git Repository                   │  │
│  │  ├── order-service/                               │  │
│  │  │   ├── src/                                     │  │
│  │  │   ├── Dockerfile                               │  │
│  │  │   └── pom.xml                                  │  │
│  │  ├── menu-service/                                │  │
│  │  │   ├── src/                                     │  │
│  │  │   └── Dockerfile                               │  │
│  │  ├── k8s/                                         │  │
│  │  │   ├── order-deployment.yaml                    │  │
│  │  │   ├── order-service.yaml                       │  │
│  │  │   ├── menu-deployment.yaml                     │  │
│  │  │   └── menu-service.yaml                        │  │
│  │  ├── ansible/                                     │  │
│  │  │   ├── deploy.yml                               │  │
│  │  │   └── inventory/                               │  │
│  │  └── Jenkinsfile                                  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## Sprint 1: Containerize Services (2.5 hours)

### Tasks

| # | Task | Deliverable | Points |
|---|------|-------------|--------|
| 1.1 | Write Dockerfile for order-service | Multi-stage Dockerfile | 5 |
| 1.2 | Write Dockerfile for menu-service | Multi-stage Dockerfile | 5 |
| 1.3 | Create docker-compose.yml | Local dev environment with both services + MySQL | 5 |
| 1.4 | Optimize images | Final images under 200MB, non-root user | 3 |
| 1.5 | Test locally | Both services start and respond to health checks | 2 |

### Requirements

```dockerfile
# Multi-stage build pattern
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:resolve
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:17-jre-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=build /app/target/*.jar app.jar
USER appuser
EXPOSE 8080
HEALTHCHECK CMD wget -qO- http://localhost:8080/actuator/health || exit 1
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## Sprint 2: CI/CD Pipeline (1.5 hours)

### Tasks

| # | Task | Deliverable | Points |
|---|------|-------------|--------|
| 2.1 | Write Jenkinsfile | Declarative pipeline with stages | 5 |
| 2.2 | Build stage | Compile code and run unit tests | 3 |
| 2.3 | Docker stage | Build and tag images | 3 |
| 2.4 | Push stage | Push to container registry | 2 |
| 2.5 | Deploy stage | Trigger K8s deployment | 2 |

### Jenkinsfile Structure

```groovy
pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = 'registry.foodexpress.in'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    stages {
        stage('Checkout')  { ... }
        stage('Build')     { ... }
        stage('Test')      { ... }
        stage('Docker')    { ... }
        stage('Deploy')    { ... }
    }
    post {
        failure { ... }
        success { ... }
    }
}
```

---

## Sprint 3: Kubernetes Deployment (1.5 hours)

### Tasks

| # | Task | Deliverable | Points |
|---|------|-------------|--------|
| 3.1 | Write Deployment manifests | order-service, menu-service with resource limits | 5 |
| 3.2 | Write Service manifests | ClusterIP for internal, LoadBalancer for API | 3 |
| 3.3 | Add health probes | Liveness + readiness probes on all deployments | 3 |
| 3.4 | ConfigMap & Secrets | Externalize configuration, use Secrets for passwords | 3 |
| 3.5 | HPA | Auto-scaling for order-service | 2 |

### Namespace Strategy

```
foodexpress-dev    → Development (relaxed quotas)
foodexpress-stg    → Staging (prod-like quotas)
foodexpress-prod   → Production (strict quotas + RBAC)
```

---

## Sprint 4: Ansible Configuration (1 hour)

### Tasks

| # | Task | Deliverable | Points |
|---|------|-------------|--------|
| 4.1 | Write deployment playbook | Install prerequisites, deploy to K8s | 3 |
| 4.2 | Create inventory | Dev, staging, prod hosts | 2 |
| 4.3 | Templates | nginx reverse proxy config | 2 |
| 4.4 | Vault | Encrypt secrets with Ansible Vault | 2 |
| 4.5 | Health check play | Post-deploy verification | 1 |

---

## Sprint 5: Integration & Testing (1 hour)

### Tasks

| # | Task | Deliverable | Points |
|---|------|-------------|--------|
| 5.1 | End-to-end test | Full pipeline runs: Git push → K8s deployment | 5 |
| 5.2 | Rollback test | Demonstrate rollback on failure | 3 |
| 5.3 | Documentation | Architecture diagram, runbook | 2 |

### Definition of Done

- [ ] Code pushed to Git repository
- [ ] Jenkins pipeline runs without errors
- [ ] Docker images built and tagged
- [ ] Services running in Kubernetes with health checks passing
- [ ] Ansible playbook configures and deploys successfully
- [ ] Rollback demonstrated successfully

---

## Evaluation Rubric

### Technical (70 points)

| Category | Criteria | Points |
|----------|----------|--------|
| **Docker** | Multi-stage build, optimized image, non-root, health check | 20 |
| **Jenkins** | Pipeline with build, test, docker, deploy stages | 15 |
| **Kubernetes** | Deployments, services, probes, resources, HPA | 16 |
| **Ansible** | Playbook, inventory, templates, vault | 10 |
| **Integration** | End-to-end pipeline works, rollback tested | 9 |

### Presentation (20 points)

| Criteria | Points |
|----------|--------|
| Architecture explanation | 5 |
| Live demo (pipeline run) | 5 |
| Problem-solving narrative | 5 |
| Q&A handling | 5 |

### Collaboration (10 points)

| Criteria | Points |
|----------|--------|
| Task distribution | 3 |
| Git workflow (branches, PRs) | 4 |
| Peer review feedback | 3 |

**Total: 100 points**

---

## Presentation Guidelines

### 15 minutes per team

| Time | Content |
|------|---------|
| 0-3 min | Architecture overview and design decisions |
| 3-8 min | Live demo: trigger pipeline, show deployment |
| 8-11 min | Challenges faced and how you solved them |
| 11-13 min | What you would improve with more time |
| 13-15 min | Q&A from other teams and trainer |

### Demo checklist:
1. Show Git repository structure
2. Trigger Jenkins pipeline
3. Show Docker image build
4. Show K8s pods running with `kubectl get pods`
5. Hit a health check endpoint
6. Show Ansible playbook execution (or recording)

---

## MCQ Assessment

### 30 questions, 30 minutes

| Topic | Questions | Modules Covered |
|-------|-----------|-----------------|
| Docker & Containers | 8 | Modules 26-27 |
| CI/CD & Jenkins | 6 | Module 28 |
| Kubernetes | 8 | Module 29 |
| Ansible | 5 | Module 30 |
| Git & DevOps | 3 | Modules 18-19 |

### Sample Questions

1. Which Dockerfile instruction runs during image build but NOT during container start?
   - A) CMD  B) ENTRYPOINT  C) RUN  D) EXPOSE

2. In Kubernetes, which probe determines if a pod should receive traffic?
   - A) Liveness  B) Readiness  C) Startup  D) Health

3. In Ansible, which directive enables running tasks with sudo?
   - A) sudo: yes  B) become: yes  C) privilege: yes  D) escalate: yes

---

## Peer Review Template

### Each team reviews one other team

| Dimension | Score (1-5) | Comments |
|-----------|-------------|----------|
| Code quality (Dockerfiles, manifests, playbooks) | | |
| Pipeline completeness (all stages present) | | |
| K8s best practices (probes, resources, secrets) | | |
| Documentation clarity | | |
| Demo effectiveness | | |

**One thing they did well:**

**One thing they could improve:**

---

## Retrospective

### What went well? What could be improved?

| Category | Went Well | Could Improve |
|----------|-----------|---------------|
| **Docker** | | |
| **Jenkins** | | |
| **Kubernetes** | | |
| **Ansible** | | |
| **Teamwork** | | |

### Action items for real-world application:
1. Practice writing Dockerfiles for your project
2. Set up a personal Jenkins/GitHub Actions pipeline
3. Deploy a sample app to Minikube
4. Write Ansible playbooks for your dev environment setup

---

## Grading Scale

| Grade | Points | Description |
|-------|--------|-------------|
| **A** | 90-100 | Exceptional: all components working, clean code, excellent presentation |
| **B** | 75-89 | Proficient: most components working, minor issues, good presentation |
| **C** | 60-74 | Developing: core components work, some gaps, adequate presentation |
| **D** | 45-59 | Beginning: significant gaps, partial implementations |
| **F** | < 45 | Incomplete: major components missing |

---

## Key Takeaways

| Concept | Key Point |
|---------|-----------|
| DevOps Pipeline | Git -> Build -> Test -> Docker -> Deploy (automated) |
| Docker | Multi-stage builds, non-root users, health checks |
| Jenkins | Declarative pipelines, stage-based, post actions |
| Kubernetes | Deployments, Services, Probes, Resources, HPA |
| Ansible | Agentless config management, playbooks, templates |
| Integration | All tools work together in a cohesive pipeline |
| Sustain Role | Maintain, fix, and improve existing pipelines |

> **Next:** Module 32 -- Observability (Monitoring, Logging, Tracing)
