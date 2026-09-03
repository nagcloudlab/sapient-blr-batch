# DevOps Fundamentals -- Lab Exercises
## Module 18 | Day 19

---

## Client Email

```
From: rajesh.kumar@foodexpress.in
To: sustain-engineering@team.com
Subject: DevOps Pipeline Review -- Issues Found
Date: 2026-07-29

Team,

Our DevOps pipeline for the FoodExpress Order Service has several
issues that are causing deployment delays and quality problems. I need
you to review the pipeline configuration, CI/CD setup, and deployment
strategy documents and fix the issues.

The pipeline hasn't been updated since initial setup, and it's
causing problems:
- Builds are slow and unreliable
- Tests are being skipped
- Deployments are risky (no rollback strategy)
- Monitoring is not integrated

Please fix the pipeline configuration and documentation.

-- Rajesh Kumar, DevOps Lead, FoodExpress
```

---

## Lab 1: Fix the Jenkinsfile (6 bugs)

### Buggy Jenkinsfile

Review the following Jenkinsfile for the FoodExpress Order Service. It has 6 bugs that cause build failures, skipped tests, and unsafe deployments.

```groovy
// Jenkinsfile for FoodExpress Order Service
pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io/foodexpress'
        APP_NAME = 'order-service'
        // Bug 1: Hardcoded credentials in pipeline
        DB_PASSWORD = 'FoodExpr3ss2026!'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/foodexpress/order-service'
            }
        }

        stage('Build') {
            steps {
                // Bug 2: Skipping tests during build
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
            // Bug 3: Missing post block to publish test results
        }

        stage('Docker Build') {
            steps {
                // Bug 4: Using 'latest' tag instead of build-specific tag
                sh 'docker build -t ${DOCKER_REGISTRY}/${APP_NAME}:latest .'
            }
        }

        stage('Deploy to Production') {
            steps {
                // Bug 5: No approval gate before production deployment
                sh 'kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:latest'
            }
        }
    }

    // Bug 6: No post-build actions (no notifications, no cleanup)
}
```

### Bugs to Find and Fix

| # | Hint | Impact |
|---|------|--------|
| 1 | Database password is hardcoded in the pipeline file, visible to anyone with repo access | Security vulnerability -- credentials exposed in version control |
| 2 | Tests are skipped during the build stage with `-DskipTests`, then run separately. But if build fails, test stage still runs wastefully | Wasted CI time; build artifacts may have compilation errors |
| 3 | Test results are not published as JUnit XML reports, so Jenkins dashboard shows no test trends | No visibility into test health over time |
| 4 | Using `latest` tag for Docker images makes it impossible to track which version is deployed | Cannot rollback to a specific version; no audit trail |
| 5 | Production deployment has no approval gate -- any passing build goes straight to prod | Risky deployments; no human verification before production |
| 6 | No post-build actions: no Slack/email notifications, no workspace cleanup, no artifact archiving | Team unaware of build status; workspace fills up over time |

### Fixed Jenkinsfile (Reference)

```groovy
pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'docker.io/foodexpress'
        APP_NAME = 'order-service'
        // Fix 1: Use Jenkins credentials store
        DB_PASSWORD = credentials('foodexpress-db-password')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/foodexpress/order-service'
            }
        }

        stage('Build') {
            steps {
                // Fix 2: Run tests during build (don't skip)
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
            // Fix 3: Publish test results
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                // Fix 4: Use build number for versioning
                sh 'docker build -t ${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER} .'
                sh 'docker tag ${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER} ${DOCKER_REGISTRY}/${APP_NAME}:latest'
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh 'kubectl set image deployment/${APP_NAME}-staging ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER} -n staging'
            }
        }

        stage('Approval') {
            steps {
                // Fix 5: Manual approval before production
                input message: 'Deploy to production?', ok: 'Approve'
            }
        }

        stage('Deploy to Production') {
            steps {
                sh 'kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER} -n production'
            }
        }
    }

    // Fix 6: Post-build actions
    post {
        success {
            slackSend channel: '#deployments', message: "SUCCESS: ${APP_NAME} build #${BUILD_NUMBER}"
        }
        failure {
            slackSend channel: '#deployments', message: "FAILED: ${APP_NAME} build #${BUILD_NUMBER}"
        }
        always {
            cleanWs()
        }
    }
}
```

### Checkpoint
- [ ] All 6 bugs identified and explained
- [ ] Credentials removed from pipeline file
- [ ] Test results published to Jenkins
- [ ] Docker images tagged with build number
- [ ] Approval gate added before production deployment
- [ ] Post-build notifications configured

---

## Lab 2: Fix the Deployment Strategy Document (5 bugs)

### Buggy Deployment Strategy

```markdown
# FoodExpress Deployment Strategy

## Current Approach
We use a "big bang" deployment strategy where we:
1. Stop all running instances                    // Bug 1
2. Deploy the new version to all servers
3. Start all instances
4. Hope everything works                         // Bug 2

## Rollback Plan
If something goes wrong:
1. SSH into each server manually                 // Bug 3
2. Download the previous JAR from "somewhere"
3. Restart the application

## Monitoring
We check if the app is working by:
1. Opening the homepage in a browser             // Bug 4
2. If it loads, deployment is successful

## Schedule
Deployments happen every Friday at 5 PM          // Bug 5
```

### Bugs to Find and Fix

| # | Hint | Impact |
|---|------|--------|
| 1 | Stopping all instances causes complete downtime during deployment | Customers cannot place orders during deployment window |
| 2 | "Hope everything works" is not a verification strategy | No automated smoke tests or health checks |
| 3 | Manual SSH rollback is slow and error-prone | MTTR measured in hours instead of minutes |
| 4 | Manually checking the homepage is not a real health check | Deep issues (DB connection, API errors) won't be caught |
| 5 | Friday 5 PM is the worst time to deploy -- team leaves for weekend | Incidents discovered on Saturday with no one to fix them |

### Checkpoint
- [ ] Identified all 5 deployment strategy problems
- [ ] Proposed rolling or blue-green deployment strategy
- [ ] Wrote automated rollback procedure
- [ ] Defined proper health check endpoints
- [ ] Suggested better deployment schedule (e.g., Tuesday morning)

---

## Lab 3: DevOps Pipeline Design Exercise

### Task

Design a complete DevOps pipeline for the FoodExpress Menu Service (Node.js/Express). Create a document that includes:

1. **Pipeline stages** (at least 7 stages)
2. **Tool selection** for each stage with justification
3. **Testing strategy** (types of tests at each stage)
4. **Deployment strategy** (blue-green, canary, or rolling -- justify your choice)
5. **Monitoring and alerting** plan
6. **Rollback procedure** (automated)

### Requirements

- Pipeline must support at least 5 deployments per day
- Zero-downtime deployments required
- Automated rollback if error rate exceeds 1%
- All secrets managed securely (no hardcoding)
- Test coverage must be above 80%

### Checkpoint
- [ ] Pipeline has at least 7 stages defined
- [ ] Each stage has a tool and justification
- [ ] Testing strategy covers unit, integration, and E2E
- [ ] Deployment strategy chosen with pros/cons analysis
- [ ] Monitoring plan includes metrics, alerts, and dashboards
- [ ] Rollback is automated, not manual

---

## Bonus Challenge

Map the FoodExpress DevOps pipeline to the 7 C's framework:

| C | Pipeline Stage | Tool | FoodExpress Example |
|---|---------------|------|---------------------|
| Continuous Development | ? | ? | ? |
| Continuous Integration | ? | ? | ? |
| Continuous Testing | ? | ? | ? |
| Continuous Deployment | ? | ? | ? |
| Continuous Monitoring | ? | ? | ? |
| Continuous Feedback | ? | ? | ? |
| Continuous Operations | ? | ? | ? |
