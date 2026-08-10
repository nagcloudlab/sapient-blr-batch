# DevOps -- The 7 C's Deep Dive
## FoodExpress Reference Guide

**Audience:** Sustain Engineering trainees
**Programme:** Publicis Sapient Sustain Eng, Bangalore 2026

---

## What is DevOps?

DevOps is a culture, a set of practices, and a collection of tools that unifies software
development (Dev) and IT operations (Ops). The goal is to shorten the system development
lifecycle and deliver high-quality software continuously.

DevOps answers the question: **"How do we go from idea to production safely, quickly, and
repeatedly?"**

For FoodExpress, DevOps means:
- A developer's feature branch goes from git push to production deployment in under 30 minutes
- Every merge to main triggers automated build, test, and deploy
- Issues in production feed back into the next development cycle via post-mortems and metrics

---

## The DevOps Infinity Loop

```
          PLAN
         /    \
      CODE      MONITOR
     /                \
   BUILD           OPERATE
     \                /
      TEST       DEPLOY
         \    /
          RELEASE

The loop never stops. Feedback from Monitor -> Plan -> Code is what makes it "DevOps"
rather than just "automated deployment".
```

The 7 C's map onto the phases of this loop:

```
PLAN -> C7 (Continuous Feedback)
CODE -> C1 (Continuous Development)
BUILD + TEST -> C2 (Continuous Integration) + C3 (Continuous Testing)
RELEASE -> C4 (Continuous Delivery)
DEPLOY -> C5 (Continuous Deployment)
OPERATE + MONITOR -> C6 (Continuous Monitoring)
(loop back) -> C7 (Continuous Feedback)
```

---

## C1 -- Continuous Development

**What it means:** Code is developed in small, frequent increments using version control.
Changes are isolated in feature branches, kept short-lived, and merged often.

**Why small commits?**
- Easier to review: a 50-line PR takes 10 minutes; a 2,000-line PR takes days
- Easier to revert: roll back one small change, not a week of work
- Fewer merge conflicts: short-lived branches diverge less from main
- Faster feedback: tests run on small changes give precise failure location

**FoodExpress git workflow:**

```bash
# Developer starts a new feature: "Add estimated delivery time to order confirmation"

git checkout main
git pull origin main
git checkout -b feature/order-eta-display

# Developer makes small, focused commits:
git add src/services/OrderService.js
git commit -m "feat: calculate ETA based on restaurant prep time and distance"

git add src/api/routes/orders.js
git commit -m "feat: include eta field in POST /api/orders response"

git add tests/unit/OrderService.test.js
git commit -m "test: add unit tests for ETA calculation"

# Push and open PR:
git push origin feature/order-eta-display
# Open PR on GitHub -> automated CI pipeline triggers
```

**FoodExpress branching conventions:**

| Branch prefix | Purpose | Example |
|---|---|---|
| `feature/` | New functionality | `feature/order-eta-display` |
| `fix/` | Bug fix | `fix/payment-retry-leak` |
| `hotfix/` | Emergency production fix | `hotfix/sql-injection-menu-search` |
| `chore/` | Config, deps, tooling | `chore/update-mongoose-to-8.0` |
| `release/` | Release candidate branch | `release/v2.4.1` |

---

## C2 -- Continuous Integration

**What it means:** Every push to the shared repository triggers an automated pipeline that
builds the application and runs tests. The goal is to detect integration problems immediately.

**The CI contract:** If you break the build, fixing it is the team's top priority.
No one merges new work on top of a broken build.

**FoodExpress CI pipeline (Jenkins / GitHub Actions):**

```
Trigger: Pull request opened OR push to main branch

Stage 1: Checkout
  - Clone repository at the commit SHA

Stage 2: Install dependencies
  - npm ci              (Node.js services)
  - mvn dependency:go-offline  (Java services)

Stage 3: Lint and code quality
  - ESLint (Node.js)
  - Checkstyle (Java)
  - Fail if any errors (warnings allowed)

Stage 4: Unit tests
  - npm test            (Jest, target: 80% coverage minimum)
  - mvn test            (JUnit)
  - Coverage report published to SonarQube

Stage 5: Build artifact
  - docker build -t foodexpress/order-service:${GIT_SHA} .
  - Push to ECR (Amazon Elastic Container Registry)

Stage 6: Integration tests
  - Spin up test containers (MongoDB, Redis, mock payment gateway)
  - Run integration test suite
  - Tear down test containers

Total pipeline time target: under 8 minutes
```

**What "CI" does NOT mean:** CI does not mean automatic deployment to production.
It means the code is integrated and verified continuously. Deployment decisions are separate.

---

## C3 -- Continuous Testing

**What it means:** Testing is embedded at every stage of the pipeline, not done as a separate
phase at the end. Different test types run at different stages.

**The FoodExpress testing pyramid:**

```
         /\
        /  \
       / E2E \         <-- Few, slow, expensive, high confidence
      /--------\
     / Integration \   <-- More, moderate speed, test component boundaries
    /--------------\
   /   Unit Tests   \  <-- Many, fast, cheap, test individual functions
  /------------------\
```

**FoodExpress test types and examples:**

| Test type | What it tests | Tool | When it runs | Example |
|---|---|---|---|---|
| Unit | Single function or class | Jest (Node.js), JUnit (Java) | Every push, CI Stage 4 | calculateOrderTotal() returns correct sum |
| Integration | Service + database | Jest + testcontainers | Every push, CI Stage 6 | POST /api/orders actually writes to MongoDB |
| Contract | API contract between services | Pact | PR to main | OrderService calls PaymentService with correct schema |
| E2E | Full user journey in browser | Cypress | Pre-release | Customer places order -> receives confirmation email |
| Performance | Latency under load | k6, Gatling | Nightly | Order API handles 500 req/s within SLO |
| Security | Known vulnerability patterns | OWASP ZAP, npm audit | Weekly | No SQL injection, no outdated dependencies with CVEs |

**Example FoodExpress unit test:**

```javascript
// tests/unit/OrderService.test.js
describe('OrderService.calculateTotal()', () => {
  it('sums item prices multiplied by quantity', () => {
    const items = [
      { price: 120, quantity: 2 },  // 240
      { price: 80,  quantity: 1 }   // 80
    ];
    expect(OrderService.calculateTotal(items)).toBe(320);
  });

  it('returns 0 for empty cart', () => {
    expect(OrderService.calculateTotal([])).toBe(0);
  });

  it('applies delivery fee when order is below minimum', () => {
    const items = [{ price: 50, quantity: 1 }];
    expect(OrderService.calculateTotal(items, { minOrder: 100, deliveryFee: 40 })).toBe(90);
  });
});
```

---

## C4 -- Continuous Delivery

**What it means:** Code is ALWAYS in a state where it COULD be deployed to production.
The decision to deploy is a business decision, not a technical one. Deployment requires a
human approval step.

**Key distinction:** Continuous Delivery != Continuous Deployment.

```
Continuous Delivery:
  Code -> CI Pipeline -> Staging Deploy (auto) -> [HUMAN APPROVES] -> Production Deploy

Continuous Deployment:
  Code -> CI Pipeline -> Staging Deploy (auto) -> Production Deploy (auto, no human gate)
```

**FoodExpress Continuous Delivery practices:**

1. The main branch is always deployable. No work-in-progress code merges without passing CI.
2. Feature flags: incomplete features are merged behind a flag (off in production until ready).
3. Staging environment mirrors production: same Kubernetes config, same database schema.
4. Every artifact is tagged with the git SHA: `foodexpress/payment-service:a3f9c21`
5. Rollback is a one-command operation: `kubectl rollout undo deployment/payment-service`

**FoodExpress feature flag example:**

```javascript
// PaymentService - new retry strategy behind a flag
const PAYMENT_RETRY_V2_ENABLED = process.env.PAYMENT_RETRY_V2_ENABLED === 'true';

async function processPayment(order) {
  if (PAYMENT_RETRY_V2_ENABLED) {
    return processPaymentWithBoundedRetry(order);  // new, safe implementation
  }
  return processPaymentLegacy(order);              // existing behaviour
}
```

---

## C5 -- Continuous Deployment

**What it means:** Every change that passes all automated checks is deployed to production
automatically, without human intervention. This is the most advanced stage and requires
extremely high confidence in the test suite.

**FoodExpress Jenkins deployment pipeline:**

```groovy
pipeline {
  agent any
  stages {
    stage('Build and Test') {
      steps {
        sh 'npm ci && npm test'
        sh 'docker build -t foodexpress/order-service:${GIT_COMMIT} .'
        sh 'docker push foodexpress/order-service:${GIT_COMMIT}'
      }
    }

    stage('Deploy to Staging') {
      steps {
        sh '''
          helm upgrade --install order-service ./helm/order-service \
            --namespace foodexpress-staging \
            --set image.tag=${GIT_COMMIT}
        '''
        sh 'npm run test:integration:staging'
      }
    }

    stage('Deploy to Production') {
      // Canary: deploy to 10% of pods first
      steps {
        sh '''
          kubectl set image deployment/order-service \
            order-service=foodexpress/order-service:${GIT_COMMIT} \
            --namespace foodexpress-prod
        '''
        sh 'sleep 300'  // wait 5 minutes, Grafana watches error rate
        // If error rate stays below 1%, rollout continues automatically
      }
    }
  }

  post {
    failure {
      slackSend channel: '#deployments',
        message: "FAILED: order-service ${GIT_COMMIT} -- check Jenkins: ${env.BUILD_URL}"
    }
  }
}
```

**Deployment strategies used at FoodExpress:**

| Strategy | How it works | When to use |
|---|---|---|
| Rolling update | Replace pods one by one | Standard deployments, minimal risk |
| Canary | Deploy to 10% of pods, monitor, then expand | Features with uncertain impact |
| Blue/Green | Run two full environments, switch traffic | Major releases, instant rollback needed |
| Feature flag | Deploy code to all pods but disable in config | Incomplete features, A/B testing |

---

## C6 -- Continuous Monitoring

**What it means:** The production system is monitored at all times. Metrics, logs, and traces
are collected continuously. Alerts fire automatically. The team does not wait for customers to
report problems.

**FoodExpress observability stack:**

| Tool | Role | What it monitors for FoodExpress |
|---|---|---|
| Prometheus | Metrics collection and storage | HTTP rates, latency, error rates, pod CPU/memory |
| Grafana | Metrics visualization and alerting | Dashboards per service, SLO burn rate dashboard |
| Loki | Log aggregation | Application logs from all Kubernetes pods |
| Jaeger | Distributed tracing | Request traces across Order -> Payment -> Restaurant services |
| PagerDuty | Alert routing and on-call management | Routes P1/P2 alerts to on-call engineer's phone |
| Synthetic monitoring | Proactive availability check | Places a test order every 5 minutes from 3 regions |

**FoodExpress alert runbook (what gets paged):**

```
P1 page (immediate wake-up):
  - Order Service error rate > 5% for 1 minute
  - Payment Service error rate > 1% for 1 minute
  - Any service: 0 healthy pods
  - Heap / memory usage > 95% for 2 minutes

P2 page (page within 30 minutes):
  - Order Service P95 latency > 1000ms for 5 minutes
  - DB connection pool > 90% for 2 minutes
  - Error budget burn rate > 5x for 1 hour

Warning (Slack only, no page):
  - Order Service P95 latency > 500ms
  - DB connection pool > 70%
  - Error budget burn rate > 2x
```

**Grafana dashboard checklist (what every FoodExpress service dashboard must have):**
- The four golden signals panel: latency, traffic, errors, saturation
- Pod health panel: restarts, OOMKills, pending pods
- SLO burn rate panel: error budget remaining and burn rate
- Deployment marker: vertical line showing when each deploy happened
- Database / cache connection panel: pool usage, query time

---

## C7 -- Continuous Feedback

**What it means:** Learnings from production flow back into planning and development.
Feedback comes from: post-mortems, retros, customer reports, metrics trends, and SLO reviews.

**FoodExpress feedback loops:**

| Feedback source | Cadence | Who reviews | Output |
|---|---|---|---|
| Blameless post-mortem | After every P1/P2 | Full sustain team | Action items in Jira, runbook updates |
| Sprint retrospective | Every 2 weeks | Development team | Process improvements for next sprint |
| SLO review | Monthly | Team lead + client | Service credit decisions, reliability roadmap |
| Error budget report | Monthly | SRE + product team | Feature freeze decision or risk acceptance |
| Customer satisfaction (CSAT) | Monthly | Product owner | Prioritization of UX fixes |
| Alert noise review | Weekly | On-call lead | Alert tuning, reduce false positives |
| Dependency vulnerability scan | Weekly (automated) | Sustain team | Security patches prioritized in backlog |

**The feedback principle:** Every outage, every slow query, every user complaint is data.
The DevOps team collects it, analyses it, and uses it to make the next iteration more reliable.

**Example feedback cycle for FoodExpress:**

```
1. MONITOR: Grafana shows Order Service P95 latency climbing every Sunday evening
2. FEEDBACK: SRE engineer creates Jira ticket "Investigate Sunday latency spike"
3. PLAN: Team reviews metrics -- spikes correlate with weekly menu update batch job
4. CODE: Developer rewrites batch job to use streaming instead of in-memory load
5. CI: Tests pass including a new load test that simulates the batch job during traffic
6. DEPLOY: Fix deployed via Jenkins pipeline
7. MONITOR: Sunday latency spike no longer appears in Grafana
8. POSTMORTEM: Brief write-up: root cause, fix, validation -- shared with client
```

---

## 7 C's Summary

```
C1 Continuous Development  -- small commits, feature branches, git workflow
C2 Continuous Integration  -- auto-build + auto-test on every push
C3 Continuous Testing      -- unit + integration + E2E + performance at each stage
C4 Continuous Delivery     -- code is always READY; deploy is a business decision
C5 Continuous Deployment   -- code goes to production automatically after tests pass
C6 Continuous Monitoring   -- Prometheus + Grafana + alerts + on-call
C7 Continuous Feedback     -- postmortems + retros + SLO reviews feed back to C1
```

The 7 C's form a closed loop. Without C7 feeding back into C1, the other six simply automate
what was already being done. Feedback is what makes DevOps improve over time.

---

*Reference document for Publicis Sapient Sustain Engineering Training, Bangalore 2026.*
*Module 18 (DevOps), Module 19 (Git/GitHub), Module 25 (Jenkins), Module 27 (Kubernetes).*
