# CI/CD with Jenkins -- Lab Exercises
## Module 28 | Day 31

---

## Client Email

```
From: deepak.patel@foodexpress.in
To: sustain-engineering@team.com
Subject: Jenkins Pipeline Broken -- Order Service Not Deploying
Date: 2026-08-08

Team,

Our Jenkins CI/CD pipeline for the Order Service is broken.
A developer made changes to the Jenkinsfile and now:

1. Builds succeed but no tests run (we're deploying untested code!)
2. It's building from the wrong branch
3. Workspace has stale files causing intermittent failures
4. We can't download build artifacts
5. Builds sometimes hang forever
6. I found hardcoded credentials in the Jenkinsfile (!!!)
7. No one gets notified when builds fail
8. Docker images aren't tagged properly

Fix the Jenkinsfile. This is critical -- we deploy 5 times a day
and every broken build costs us 30 minutes of developer time.

-- Deepak Patel, Tech Lead, FoodExpress
```

---

## Lab 1: Fix the Jenkinsfile (8 bugs)

### Duration: 60 minutes | Points: 30

**File to fix:** `starter-code/Jenkinsfile`

### Bugs to Find and Fix

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Look for a Test stage | Test stage is completely missing | Untested code deployed to production |
| 2 | Check the git branch | Branch is `development` but should be `main` | Building wrong code |
| 3 | Look for workspace cleanup | No `cleanWs()` in post actions | Stale files from previous builds |
| 4 | Check for archiveArtifacts | No artifact archiving | Can't download/roll back builds |
| 5 | Look for timeout | No pipeline timeout set | Builds hang forever if something stalls |
| 6 | Check for hardcoded secrets | Docker Hub password in plain text | Credentials exposed in Git |
| 7 | Look for failure notification | No `post { failure }` block | Team doesn't know when builds break |
| 8 | Check Docker image tag | Tagged as `latest` only | Non-reproducible deployments |

### Verification Checklist

```
[ ] Test stage present with mvn test
[ ] junit test report published
[ ] Git branch is 'main'
[ ] cleanWs() in post { always }
[ ] archiveArtifacts for target/*.jar
[ ] Pipeline timeout set (e.g., 30 minutes)
[ ] credentials() used for Docker login
[ ] post { failure } with notification
[ ] Docker image tagged with build number
```

---

## Lab 2: Write a Jenkinsfile from Scratch (Node.js)

### Duration: 30 minutes | Points: 15

Write a Jenkinsfile for the FoodExpress Restaurant Service (Node.js):

**Requirements:**
- Agent: `node:18-alpine` Docker image
- Stages: Install, Lint, Test, Docker Build
- `npm ci` for dependency installation
- `npm test -- --coverage` for testing
- Test reports published
- Workspace cleaned after build
- Timeout: 20 minutes
- Notify on failure

### Template

```groovy
pipeline {
    agent {
        // TODO: Use node:18-alpine Docker image
    }

    options {
        // TODO: Add timeout
    }

    stages {
        stage('Install Dependencies') {
            steps {
                // TODO: npm ci
            }
        }

        stage('Lint') {
            steps {
                // TODO: npm run lint
            }
        }

        stage('Test') {
            steps {
                // TODO: npm test with coverage
            }
            post {
                always {
                    // TODO: Publish test reports
                }
            }
        }

        stage('Docker Build') {
            steps {
                // TODO: docker build with proper tag
            }
        }
    }

    post {
        // TODO: failure notification, always cleanup
    }
}
```

---

## Lab 3: Pipeline Optimization (Bonus)

### Duration: 15 minutes | Points: 5

Take the Order Service Jenkinsfile and optimize it:

1. **Parallel stages:** Run Unit Tests and Security Scan in parallel
2. **Docker layer caching:** Add `--cache-from` to docker build
3. **Conditional deploy:** Only deploy to staging on `main` branch pushes

```groovy
stage('Tests') {
    parallel {
        stage('Unit Tests') { ... }
        stage('Security Scan') { ... }
    }
}

stage('Deploy to Staging') {
    when {
        branch 'main'
    }
    steps { ... }
}
```

---

## Scoring

| Task | Points |
|------|--------|
| Lab 1: Fix Jenkinsfile (8 bugs) | 30 |
| Lab 2: Write Node.js Jenkinsfile | 15 |
| Lab 3: Bonus pipeline optimization | 5 |
| **Total** | **50** |
