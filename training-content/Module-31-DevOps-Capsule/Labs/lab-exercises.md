# DevOps Capsule Project -- Lab Exercises
## Module 31 | Days 34-35

---

## Project Lab Overview

This is a 2-day capsule project. There are no individual bug-fix labs. Instead, teams work through 5 sprints to build a complete DevOps pipeline for FoodExpress.

---

## Sprint 1: Containerize FoodExpress (2.5 hours)

### Task 1.1: Write Dockerfile for order-service

Create a multi-stage Dockerfile that:
- Uses `maven:3.9-eclipse-temurin-17` as build stage
- Uses `eclipse-temurin:17-jre-alpine` as runtime stage
- Runs as a non-root user
- Exposes port 8080
- Includes a HEALTHCHECK instruction

### Task 1.2: Write Dockerfile for menu-service

Same requirements as order-service but for the menu microservice.

### Task 1.3: Create docker-compose.yml

Create a docker-compose file with:
- order-service (port 8081:8080)
- menu-service (port 8082:8080)
- MySQL database (port 3306)
- Shared network
- Volume for MySQL data persistence
- Health checks on all services

### Task 1.4: Optimize images

- Final images must be under 200MB
- Use `.dockerignore` to exclude unnecessary files
- Layer caching: copy pom.xml before source code

### Task 1.5: Test locally

```bash
docker-compose up -d
curl http://localhost:8081/actuator/health
curl http://localhost:8082/actuator/health
```

---

## Sprint 2: CI/CD Pipeline (1.5 hours)

### Task 2.1: Write Jenkinsfile

Create a declarative pipeline with stages: Checkout, Build, Test, Docker Build, Deploy.

### Task 2.2-2.5: Pipeline stages

Each stage should have proper error handling and post-build actions (email on failure, Slack notification on success).

---

## Sprint 3: Kubernetes Deployment (1.5 hours)

### Task 3.1-3.5: K8s Manifests

Write deployment and service manifests for both services. Include probes, resource limits, ConfigMaps, Secrets, and HPA.

---

## Sprint 4: Ansible Configuration (1 hour)

### Task 4.1-4.5: Ansible Automation

Write playbooks for deploying FoodExpress to the K8s cluster with post-deployment health checks.

---

## Sprint 5: Integration (1 hour)

### Task 5.1-5.3: End-to-End Testing

Run the full pipeline. Test rollback. Document the architecture.

---

## Starter Code

The `starter-code/` directory contains skeleton files with TODO comments for each sprint. Use these as starting points.
