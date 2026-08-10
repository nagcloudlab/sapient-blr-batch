# CI/CD with Jenkins
## Module 28 | Sustain Engineering Training | Day 31

---

## Agenda -- Day 31

| # | Topic |
|---|-------|
| 01 | CI/CD Concepts & Why They Matter |
| 02 | Continuous Integration Deep Dive |
| 03 | Continuous Delivery vs Continuous Deployment |
| 04 | Jenkins Architecture & Components |
| 05 | Jenkins Installation & Configuration |
| 06 | Jenkins Plugins Ecosystem |
| 07 | Declarative Pipeline Syntax |
| 08 | Pipeline Stages: Build, Test, Deploy |
| 09 | GitHub Webhooks & Triggers |
| 10 | Lab: Fix the FoodExpress Jenkinsfile |
| 11 | Day Wrap-up & Key Takeaways |

---

## What is CI/CD?

### The Problem Without CI/CD

```
Traditional Development:
Day 1-20:  Developers code in isolation
Day 21:    "Integration Day" -- merge everything
           ├── Merge conflicts everywhere
           ├── Broken builds
           ├── "It worked on my branch!"
           └── 3 days to stabilize
Day 24:    Manual testing begins
Day 28:    Manual deployment to staging
Day 30:    Manual deployment to production
           └── Deployment at 2 AM, fingers crossed
```

> **FoodExpress:** Before CI/CD, deployments took 6 hours and failed 40% of the time. After CI/CD: 15 minutes, 98% success rate.

---

## CI/CD Pipeline Overview

<!--VISUAL:cicd-pipeline-->

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Source   │──▶│  Build   │──▶│  Test    │──▶│  Deploy  │──▶│ Monitor  │
│          │   │          │   │          │   │  Staging │   │          │
│ Git Push │   │ Compile  │   │ Unit     │   │          │   │ Health   │
│ PR Merge │   │ Package  │   │ Integr.  │   │  Prod    │   │ Alerts   │
│          │   │ Lint     │   │ Security │   │          │   │ Metrics  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │              │              │
     └──────────────┴──────────────┴──────────────┴──────────────┘
                    Automated, Repeatable, Fast
```

---

## Continuous Integration (CI)

### Merge and validate code frequently

```
Developer A ──push──▶ ┌─────────────────────────┐
                      │     CI Server             │
Developer B ──push──▶ │                           │
                      │  1. Pull latest code      │
Developer C ──push──▶ │  2. Build application     │
                      │  3. Run unit tests        │
                      │  4. Run linting/SAST      │
                      │  5. Report results        │
                      │                           │
                      │  ✓ Pass → Ready to merge  │
                      │  ✗ Fail → Fix immediately │
                      └─────────────────────────┘
```

### CI Best Practices

| Practice | Why |
|----------|-----|
| Commit frequently (daily minimum) | Smaller changes, easier to debug |
| Automated tests run on every push | Catch regressions immediately |
| Fix broken builds immediately | Team rule: broken build = top priority |
| Keep build fast (< 10 minutes) | Slow builds = developers skip them |

---

## Continuous Delivery vs Continuous Deployment

```
Continuous Integration    Continuous Delivery      Continuous Deployment
┌────────────┐           ┌────────────┐           ┌────────────┐
│ Build      │           │ Build      │           │ Build      │
│ Unit Test  │           │ Unit Test  │           │ Unit Test  │
│ Lint       │           │ Lint       │           │ Lint       │
└─────┬──────┘           │ Int. Test  │           │ Int. Test  │
      │                  │ Stage Deploy│           │ Stage Deploy│
   STOP here             │ Approval   │           │ Prod Deploy │
                         └─────┬──────┘           └────────────┘
                               │                       │
                         Manual button             Fully automatic
                         to deploy                 No human gate
```

| Aspect | Continuous Delivery | Continuous Deployment |
|--------|-------------------|---------------------|
| Production deploy | Manual approval | Automatic |
| Risk | Lower (human gate) | Higher (must trust tests) |
| Speed | Slower (wait for approval) | Fastest |
| Maturity | Most companies | Netflix, Etsy, Facebook |
| FoodExpress | Current state | Future goal |

---

## Jenkins -- What Is It?

### The Most Popular CI/CD Server

- Open source (MIT license), started in 2004 as "Hudson"
- Written in Java, runs on any JVM
- 1,800+ plugins for every tool and platform
- Used by 50%+ of organizations for CI/CD
- Highly customizable pipeline engine

```
┌──────────────────────────────────────────────┐
│                 Jenkins Server                 │
│                                                │
│  ┌────────────────────────────────────────┐   │
│  │  Controller (Master)                    │   │
│  │  ├── Web UI (port 8080)                │   │
│  │  ├── Job scheduling                    │   │
│  │  ├── Plugin management                 │   │
│  │  └── Build history & artifacts         │   │
│  └────────────────────────────────────────┘   │
│                    │                           │
│         ┌─────────┼─────────┐                 │
│         ▼         ▼         ▼                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Agent 1  │ │ Agent 2  │ │ Agent 3  │      │
│  │ (Linux)  │ │ (Linux)  │ │ (Docker) │      │
│  │ Java     │ │ Node.js  │ │ Both     │      │
│  └──────────┘ └──────────┘ └──────────┘      │
└──────────────────────────────────────────────┘
```

---

## Jenkins Architecture

### Controller-Agent Model

| Component | Role | Details |
|-----------|------|---------|
| Controller (Master) | Orchestrates pipelines | Schedules builds, serves UI, stores configs |
| Agent (Node) | Executes builds | Runs on separate machines, labeled by capability |
| Executor | Thread within an agent | Each agent can have multiple executors |
| Workspace | Build directory | Where source code is checked out and built |

```
Controller schedules build
        │
        ├──▶ Finds agent with matching label
        │
        ├──▶ Agent clones repo into workspace
        │
        ├──▶ Agent runs pipeline stages
        │
        └──▶ Agent reports results to Controller
```

---

## Jenkins Plugins

### Essential Plugins for FoodExpress

| Plugin | Purpose |
|--------|---------|
| Pipeline | Declarative & Scripted pipeline support |
| Git | Git SCM integration |
| GitHub Integration | Webhooks, PR status checks |
| Docker Pipeline | Build/push Docker images |
| Credentials | Secure secret storage |
| JUnit | Test result reporting |
| SonarQube | Code quality analysis |
| Slack Notification | Build notifications |
| Blue Ocean | Modern pipeline visualization |
| NodeJS | Node.js build tool support |

```bash
# Install plugins via CLI
java -jar jenkins-cli.jar -s http://localhost:8080/ \
  install-plugin docker-workflow git pipeline-utility-steps
```

---

## Jenkins Pipeline Types

### Declarative vs Scripted

```groovy
// DECLARATIVE (Recommended -- structured, readable)
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
    }
}

// SCRIPTED (Flexible -- full Groovy power)
node {
    stage('Build') {
        sh 'mvn clean package'
    }
    stage('Test') {
        sh 'mvn test'
    }
}
```

| Feature | Declarative | Scripted |
|---------|-----------|---------|
| Syntax | Structured, opinionated | Free-form Groovy |
| Learning curve | Easier | Steeper |
| Validation | Pipeline syntax check | Runtime errors |
| Recommended | Yes (for most cases) | For complex logic |

---

## Declarative Pipeline Structure

```groovy
pipeline {
    agent any                        // Where to run

    environment {                    // Environment variables
        DOCKER_REGISTRY = 'ecr.aws/foodexpress'
        APP_NAME = 'order-service'
    }

    options {                        // Pipeline options
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {                         // Build stages
        stage('Checkout') { ... }
        stage('Build') { ... }
        stage('Test') { ... }
        stage('Docker') { ... }
        stage('Deploy') { ... }
    }

    post {                           // Post-build actions
        success { ... }
        failure { ... }
        always { ... }
    }
}
```

---

## FoodExpress Order Service -- Jenkinsfile

```groovy
pipeline {
    agent any

    tools {
        maven 'Maven-3.9'
        jdk 'JDK-17'
    }

    environment {
        DOCKER_REGISTRY = credentials('docker-registry-url')
        APP_NAME = 'order-service'
        APP_VERSION = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/foodexpress/order-service.git'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }

        stage('Code Quality') {
            steps {
                sh 'mvn sonar:sonar'
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_REGISTRY}/${APP_NAME}:${APP_VERSION} ."
            }
        }

        stage('Docker Push') {
            steps {
                sh "docker push ${DOCKER_REGISTRY}/${APP_NAME}:${APP_VERSION}"
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh """
                    ssh deploy@staging 'docker pull ${DOCKER_REGISTRY}/${APP_NAME}:${APP_VERSION}'
                    ssh deploy@staging 'docker compose -f /opt/foodexpress/docker-compose.yml up -d order-service'
                """
            }
        }
    }

    post {
        success {
            slackSend channel: '#deployments',
                      message: "Order Service ${APP_VERSION} deployed to staging"
        }
        failure {
            slackSend channel: '#deployments',
                      color: 'danger',
                      message: "Order Service build FAILED: ${env.BUILD_URL}"
        }
        always {
            cleanWs()
        }
    }
}
```

---

## Pipeline Stages Explained

```
Checkout ──▶ Build ──▶ Test ──▶ Quality ──▶ Docker ──▶ Deploy

│ Clone     │ Compile  │ Run     │ SonarQube │ Build   │ Pull &
│ repo      │ code     │ unit    │ analysis  │ image   │ restart
│ from Git  │ into JAR │ tests   │           │ Push to │ on
│           │          │ Report  │           │ registry│ staging
│           │          │ results │           │         │
```

### Stage Dependencies
- Build must pass before Test
- Test must pass before Docker Build
- Each stage can have its own `post` actions
- Pipeline fails fast on first stage failure

---

## Credentials Management

### Storing Secrets Safely in Jenkins

```groovy
pipeline {
    environment {
        // Bind Jenkins credentials to env variables
        DOCKER_CREDS = credentials('docker-hub-credentials')  // username:password
        DB_PASSWORD = credentials('production-db-password')     // secret text
        SSH_KEY = credentials('staging-ssh-key')                // SSH key file
    }

    stages {
        stage('Docker Login') {
            steps {
                sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin'
            }
        }
    }
}
```

| Credential Type | Jenkins Kind | Usage |
|----------------|-------------|-------|
| Username/Password | `usernamePassword` | Docker Hub, Git HTTPS |
| Secret Text | `string` | API keys, tokens |
| SSH Key | `sshUserPrivateKey` | Git SSH, server access |
| Certificate | `certificate` | TLS/SSL |
| File | `secretFile` | Config files, keystores |

---

## GitHub Webhooks

### Automatic Build Trigger on Push

```
Developer pushes code
        │
        ▼
┌──────────────┐    webhook     ┌──────────────┐
│   GitHub     │ ──────────────▶│   Jenkins    │
│              │  POST /github  │              │
│ repository   │  -webhook/     │  Triggers    │
│ push event   │                │  pipeline    │
└──────────────┘                └──────────────┘
```

### Jenkins Configuration

```groovy
pipeline {
    triggers {
        // Poll SCM every 5 minutes (fallback)
        pollSCM('H/5 * * * *')

        // OR: GitHub webhook (preferred -- instant)
        githubPush()
    }
}
```

### GitHub Webhook Setup
1. Go to repo Settings > Webhooks
2. URL: `https://jenkins.foodexpress.in/github-webhook/`
3. Content type: `application/json`
4. Events: Push, Pull Request

---

## Build Triggers

| Trigger | When | Use Case |
|---------|------|----------|
| `githubPush()` | On Git push (webhook) | Main build trigger |
| `pollSCM('H/5 * * * *')` | Check Git every 5 min | Fallback when webhook fails |
| `cron('0 2 * * *')` | Scheduled (daily 2 AM) | Nightly builds, security scans |
| `upstream('other-job')` | After another job | Dependency chains |
| Manual | Click "Build Now" | Emergency deployments |

---

## Artifacts & Test Reports

```groovy
stage('Build') {
    steps {
        sh 'mvn clean package -DskipTests'
    }
    post {
        success {
            // Archive the JAR for download
            archiveArtifacts artifacts: 'target/*.jar',
                             fingerprint: true
        }
    }
}

stage('Test') {
    steps {
        sh 'mvn test'
    }
    post {
        always {
            // Publish test results
            junit '**/target/surefire-reports/*.xml'

            // Publish code coverage
            jacoco execPattern: 'target/jacoco.exec'
        }
    }
}
```

---

## Pipeline Best Practices

| Practice | Why | How |
|----------|-----|-----|
| Keep pipelines fast | Slow = developers skip | Parallelize stages, cache dependencies |
| Fail fast | Don't wait for Docker build if tests fail | Stage order matters |
| Archive artifacts | Download builds without rebuilding | `archiveArtifacts` |
| Clean workspace | Prevent stale files | `cleanWs()` in post/always |
| Use credentials plugin | Never hardcode secrets | `credentials()` function |
| Test reports | Track test health over time | `junit` step |
| Notifications | Team awareness | Slack, email on failure |
| Timeout | Prevent stuck builds | `timeout(time: 30, unit: 'MINUTES')` |

---

## Parallel Stages

### Run Tests in Parallel for Speed

```groovy
stage('Tests') {
    parallel {
        stage('Unit Tests') {
            steps {
                sh 'mvn test -pl order-service'
            }
        }
        stage('Integration Tests') {
            steps {
                sh 'mvn verify -pl order-service -Pintegration'
            }
        }
        stage('Security Scan') {
            steps {
                sh 'trivy fs --severity HIGH,CRITICAL .'
            }
        }
    }
}
```

```
                    ┌── Unit Tests ──────────┐
                    │                        │
Tests ──parallel──▶ ├── Integration Tests ───┤──▶ Next Stage
                    │                        │
                    └── Security Scan ───────┘

Serial: 15 min     Parallel: 5 min (only as slow as slowest)
```

---

## FoodExpress CI/CD Architecture

```
┌─────────────────────────────────────────────────────────┐
│  FoodExpress CI/CD Pipeline                              │
│                                                          │
│  GitHub ──webhook──▶ Jenkins Controller                  │
│                           │                              │
│                     ┌─────┼─────┐                       │
│                     ▼     ▼     ▼                       │
│               ┌──────┐ ┌──────┐ ┌──────┐                │
│               │Build │ │Build │ │Build │                │
│               │Agent │ │Agent │ │Agent │                │
│               │Java  │ │Node  │ │Docker│                │
│               └──┬───┘ └──┬───┘ └──┬───┘                │
│                  │        │        │                     │
│                  ▼        ▼        ▼                     │
│             ┌──────────────────────────┐                │
│             │     AWS ECR (Registry)    │                │
│             └────────────┬─────────────┘                │
│                          │                              │
│               ┌──────────┼──────────┐                   │
│               ▼                     ▼                   │
│          ┌──────────┐         ┌──────────┐              │
│          │ Staging  │         │Production│              │
│          │ Auto     │         │ Manual   │              │
│          │ Deploy   │         │ Approval │              │
│          └──────────┘         └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

---

## Jenkinsfile for Node.js (Restaurant Service)

```groovy
pipeline {
    agent {
        docker {
            image 'node:18-alpine'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    stages {
        stage('Install') {
            steps {
                sh 'npm ci'
            }
        }

        stage('Lint') {
            steps {
                sh 'npm run lint'
            }
        }

        stage('Test') {
            steps {
                sh 'npm test -- --coverage'
            }
            post {
                always {
                    junit 'test-results/*.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t foodexpress/restaurant-service:${BUILD_NUMBER} ."
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
```

---

## MCQ -- Quick Check 1

**Question:** What is the main difference between Continuous Delivery and Continuous Deployment?

A) Delivery uses Jenkins; Deployment uses GitHub Actions
B) Delivery requires manual approval for production; Deployment is fully automatic
C) Delivery only builds; Deployment also tests
D) They are the same thing

> **Answer:** B -- Continuous Delivery automates everything up to production but requires a manual approval gate. Continuous Deployment automatically deploys to production after all tests pass.

---

## MCQ -- Quick Check 2

**Question:** In a Declarative Jenkins Pipeline, what does `agent any` mean?

A) The pipeline won't run
B) The pipeline runs on any available Jenkins agent
C) The pipeline runs on the controller only
D) The pipeline requires a Docker agent

> **Answer:** B -- `agent any` means Jenkins will schedule the pipeline on whichever agent (node) has an available executor.

---

## MCQ -- Quick Check 3

**Question:** You have this in your Jenkinsfile:
```groovy
post {
    always {
        junit '**/surefire-reports/*.xml'
        cleanWs()
    }
}
```
When does this block execute?

A) Only when the build succeeds
B) Only when the build fails
C) Every time, regardless of success or failure
D) Only on the first build

> **Answer:** C -- The `always` block in `post` runs on every build, whether it succeeds, fails, or is unstable. This ensures test reports are published and workspace is cleaned.

---

## MCQ -- Quick Check 4

**Question:** Why should you use `credentials('my-secret')` instead of hardcoding secrets in the Jenkinsfile?

A) It's faster
B) Jenkinsfiles are stored in Git -- secrets would be exposed in version control
C) Jenkins can't read hardcoded strings
D) Credentials are easier to type

> **Answer:** B -- Jenkinsfiles are code stored in your Git repository. Hardcoded secrets would be visible to anyone with repo access. The credentials plugin stores secrets encrypted in Jenkins.

---

## MCQ -- Quick Check 5

**Question:** A build is triggered but the workspace contains files from the previous build. What should you add?

A) `deleteDir()` at the start
B) `cleanWs()` in the `post { always }` block
C) `git clean -fdx` in the checkout stage
D) Any of the above would work

> **Answer:** D -- All three approaches clean the workspace. `cleanWs()` in `post { always }` is the most common pattern as it runs after every build, including failures.

---

## Lab Preview: Fix the FoodExpress Jenkinsfile

### What You'll Fix

The Order Service Jenkinsfile has **8 bugs** that prevent the CI/CD pipeline from working correctly:

1. Missing test stage -- builds but never tests
2. Wrong Git branch -- builds from wrong branch
3. No workspace cleanup -- stale files cause failures
4. Artifacts not archived -- builds can't be downloaded
5. No timeout -- builds hang forever
6. Hardcoded credentials -- secrets in Git
7. Missing post-failure notification
8. Docker image not tagged properly

> File: `Labs/starter-code/Jenkinsfile`

---

## Key Takeaways

| # | Takeaway |
|---|----------|
| 1 | CI/CD automates build, test, and deploy -- reducing manual errors and deployment time |
| 2 | Continuous Integration = merge frequently + automated tests on every push |
| 3 | Continuous Delivery = automated pipeline + manual production approval gate |
| 4 | Jenkins uses Controller-Agent architecture with 1,800+ plugins |
| 5 | Declarative Pipeline is preferred: structured, readable, validated |
| 6 | Always include test stage, artifact archiving, workspace cleanup, and notifications |
| 7 | Use Jenkins credentials plugin -- never hardcode secrets in Jenkinsfiles |
| 8 | GitHub webhooks trigger builds instantly on push |

> **Next: Module 29 -- Kubernetes (Container Orchestration)**
