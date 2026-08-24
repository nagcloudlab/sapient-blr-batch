# CI/CD with Jenkins -- Project Brief
## Module 28 | Day 31

---

## Sustain Context

FoodExpress deploys 5 times a day using Jenkins CI/CD. The Order Service Jenkinsfile has been broken by a developer's changes -- builds succeed but critical stages are missing, credentials are exposed, and no one gets notified about failures. As a sustain engineer, you must fix the pipeline to restore reliable, secure CI/CD.

---

## Client Email

```
From: deepak.patel@foodexpress.in
To: sustain-engineering@team.com
Subject: Jenkins Pipeline Broken -- Deploying Untested Code!
Date: 2026-08-08

Team,

Our CI/CD pipeline is broken. We're deploying untested code because
the test stage was removed. Credentials are hardcoded in the Jenkinsfile.
No one gets notified when builds fail. Fix it urgently.

-- Deepak Patel, Tech Lead, FoodExpress
```

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix Jenkinsfile | Fix 8 bugs: missing test stage, wrong branch, no cleanup, no artifacts, no timeout, hardcoded creds, no failure notification, wrong docker tag | 60 min | 30 |
| 2 | Write Node.js Jenkinsfile | Create Jenkinsfile for Restaurant Service with Install, Lint, Test, Docker Build stages | 30 min | 15 |
| 3 | Bonus: Optimize Pipeline | Add parallel stages, conditional deploy, docker caching | 15 min | 5 |

**Total Points Available:** 50

---

## Deliverables

1. Fixed `Jenkinsfile` for Order Service with all 8 bugs resolved
2. New `Jenkinsfile.restaurant` for Restaurant Service (Node.js)
3. (Bonus) Optimized Jenkinsfile with parallel stages and conditional deploy
