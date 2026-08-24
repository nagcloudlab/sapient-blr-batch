# FoodExpress CI/CD Pipeline Design Exercise

## Instructions
Design a complete CI/CD pipeline for FoodExpress. Fill in each section.

---

## 1. Pipeline Overview

### Pipeline Stages
Draw or describe the pipeline stages in order:

```
TODO: Define your pipeline stages
Example: Code Commit -> ? -> ? -> ? -> ? -> Production
```

### Trigger Strategy
- **What triggers the pipeline?** TODO (push, PR merge, schedule, manual)
- **Which branches trigger which environments?** TODO
- **How are hotfixes handled?** TODO

---

## 2. Stage Details

### Stage 1: Source Control
- **Tool:** TODO (Git, SVN)
- **Branching Strategy:** TODO (GitFlow, trunk-based, etc.)
- **Code Review:** TODO (required before merge? how many approvals?)

### Stage 2: Build
- **Build Tool:** TODO (Maven, Gradle, npm)
- **Build Steps:** TODO
- **Artifact Output:** TODO (JAR, WAR, Docker image)

### Stage 3: Unit Tests
- **Framework:** TODO (JUnit, Jest, pytest)
- **Coverage Threshold:** TODO (e.g., 80% minimum)
- **What happens if tests fail?** TODO

### Stage 4: Code Quality
- **Tool:** TODO (SonarQube, ESLint, Checkstyle)
- **Quality Gate Criteria:** TODO
- **What happens if quality gate fails?** TODO

### Stage 5: Security Scan
- **SAST Tool:** TODO (SonarQube, Fortify, Snyk)
- **Dependency Scan:** TODO (OWASP Dependency Check, npm audit)
- **Container Scan:** TODO (Trivy, Clair)

### Stage 6: Deploy to Staging
- **Deployment Method:** TODO (rolling, blue-green, canary)
- **Smoke Tests:** TODO (what do you check?)
- **Approval Required?** TODO

### Stage 7: Integration/E2E Tests
- **Framework:** TODO (Selenium, Cypress, Postman)
- **Test Scope:** TODO
- **What happens if tests fail?** TODO

### Stage 8: Deploy to Production
- **Deployment Method:** TODO
- **Approval Process:** TODO
- **Rollback Plan:** TODO

---

## 3. Environment Strategy

| Environment | Purpose | Deployed From | Auto/Manual |
|------------|---------|---------------|-------------|
| DEV        | TODO    | TODO          | TODO        |
| SIT        | TODO    | TODO          | TODO        |
| UAT        | TODO    | TODO          | TODO        |
| STAGING    | TODO    | TODO          | TODO        |
| PROD       | TODO    | TODO          | TODO        |

---

## 4. Monitoring and Feedback

- **Build Notifications:** TODO (Slack, email, Teams)
- **Deployment Dashboard:** TODO
- **Metrics Tracked:** TODO (build time, deploy frequency, failure rate)

---

## 5. Rollback Strategy

- **How do you roll back a bad deployment?** TODO
- **How quickly can you roll back?** TODO (target: < 5 minutes)
- **Who can trigger a rollback?** TODO
