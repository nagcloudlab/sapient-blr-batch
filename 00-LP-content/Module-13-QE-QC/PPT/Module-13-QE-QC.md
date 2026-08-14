# Quality Engineering & Quality Control
## Module 13 | Sustain Engineering Training | Day 14

**1 day | Lecture + MCQ + Role Play (90 min)**

---

## Agenda

| Session | Topics |
|---------|--------|
| First half | Quality Mindset, QA vs QC vs QE, Roles & Responsibilities, Testing Fundamentals |
| Second half | Testing Types (Functional/Non-Functional), Tool Selection, Manual & Automation, Risk-Based Testing |
| Assessment | MCQ (30 min) + Role Play (90 min, 2 rounds) |

> Building a quality-first culture for sustain engineering teams.

---

## Why Quality Matters in Sustain Engineering

### The Cost of Defects

| Stage Found | Cost to Fix | Example |
|-------------|-------------|---------|
| Requirements | $1 | Catch a missing validation rule |
| Development | $10 | Fix during code review |
| Testing | $100 | Bug found in QA environment |
| Production | $1,000+ | Customer-facing outage, data loss |

### FoodExpress Impact
- A payment bug in production: **lost revenue + customer trust**
- A missing null check: **500 errors on 10% of orders**
- Wrong tax calculation: **legal compliance risk**
- Sustain engineers are the **last line of defense** before production

---

## Quality Mindset

### What Is Quality?

- **Conformance to requirements** -- Does it do what was specified?
- **Fitness for use** -- Does it serve the user's actual needs?
- **Customer satisfaction** -- Does it meet or exceed expectations?

### Quality in Sustain Context

| Traditional Development | Sustain Engineering |
|------------------------|---------------------|
| Build new features | Fix bugs in existing code |
| Define quality upfront | Improve quality of inherited code |
| Write tests from scratch | Add tests to untested code |
| Known codebase | Unfamiliar, often undocumented code |
| Greenfield | Legacy systems, technical debt |

### Quality Principles
1. **Prevention over detection** -- Catch defects early
2. **Shift left** -- Move testing earlier in the lifecycle
3. **Everyone owns quality** -- Not just the QA team
4. **Continuous improvement** -- Every bug is a learning opportunity

---

## QA vs QC vs QE

### Definitions

| Term | Full Name | Focus | Nature |
|------|-----------|-------|--------|
| **QA** | Quality Assurance | Process | Preventive |
| **QC** | Quality Control | Product | Detective |
| **QE** | Quality Engineering | System | Proactive |

### QA (Quality Assurance)
- Focuses on **processes** that prevent defects
- Reviews, audits, standards, checklists
- Example: Code review guidelines, branching strategy, CI/CD gates

### QC (Quality Control)
- Focuses on **finding defects** in the product
- Testing, inspection, validation
- Example: Running test cases, verifying bug fixes, regression testing

### QE (Quality Engineering)
- **Engineering approach** to quality at scale
- Builds quality into the system: test automation, observability, chaos engineering
- Example: Automated test pipelines, performance benchmarks, SLO monitoring

---

## QA vs QC Comparison

| Aspect | QA | QC |
|--------|----|----|
| Focus | Process | Product |
| Goal | Prevent defects | Find defects |
| Approach | Proactive | Reactive |
| Scope | Entire lifecycle | Testing phase |
| Activities | Reviews, audits, standards | Test execution, bug reporting |
| Responsibility | Everyone | QC/Testing team |
| Output | Process improvements | Bug reports, test results |

### FoodExpress Example

| QA Activity | QC Activity |
|-------------|-------------|
| Define code review checklist | Execute test cases for order flow |
| Set up CI/CD pipeline with test gates | Verify payment calculation accuracy |
| Create coding standards document | Test API responses for edge cases |
| Establish branching strategy | Regression test after each release |

---

## Roles and Responsibilities

### Quality Roles in a Sustain Team

| Role | Responsibilities | FoodExpress Example |
|------|-----------------|---------------------|
| **QA Lead** | Define test strategy, manage test plan, report metrics | Decide which modules need regression testing |
| **Test Engineer** | Write and execute test cases, report bugs | Test the order placement API endpoint |
| **SDET** | Build test automation frameworks, CI integration | Write Selenium tests for the checkout flow |
| **Performance Engineer** | Load testing, capacity planning, bottleneck analysis | Load test the restaurant search API |
| **Release Manager** | Coordinate releases, gate checks, go/no-go | Approve FoodExpress v2.3 for production |

### Sustain Engineer's Quality Role
- **You are not just a developer** -- you also own quality
- Review existing tests when fixing bugs
- Add tests for every bug fix (regression prevention)
- Question: "How was this bug missed? What test should exist?"

---

## Testing Fundamentals

### What Is Testing?

- Process of evaluating a system to find differences between **expected** and **actual** behavior
- Testing proves the **presence** of bugs, not their **absence**
- Testing is a **risk reduction** activity, not a guarantee

### Testing Terminology

| Term | Definition |
|------|-----------|
| **Test Case** | A specific set of inputs, execution conditions, and expected results |
| **Test Suite** | A collection of related test cases |
| **Test Plan** | Document describing the testing approach, scope, and schedule |
| **Defect/Bug** | Deviation from expected behavior |
| **Severity** | Impact of the bug (Critical, Major, Minor, Trivial) |
| **Priority** | Urgency of fixing (P1-urgent, P2-high, P3-medium, P4-low) |
| **Regression** | A previously working feature that breaks after a change |

---

## Severity vs Priority Matrix

| | High Priority | Low Priority |
|---|--------------|-------------|
| **High Severity** | Payment fails for all users (fix NOW) | Export to PDF crashes (workaround: use CSV) |
| **Low Severity** | Typo on homepage (CEO noticed) | Color mismatch on admin settings page |

### FoodExpress Examples

| Bug | Severity | Priority | Reasoning |
|-----|----------|----------|-----------|
| Order total calculates wrong tax | Critical | P1 | Financial/legal impact, affects all orders |
| Restaurant search returns 500 | Major | P1 | Core feature broken, customers cannot browse |
| Order history shows wrong timezone | Minor | P3 | Cosmetic, data is correct internally |
| Admin dashboard font is wrong | Trivial | P4 | No functional impact |
| CEO's profile photo does not load | Trivial | P1 | Low severity but CEO escalated |

---

## Testing Types -- Functional

### Functional Testing Categories

| Type | What It Tests | FoodExpress Example |
|------|--------------|---------------------|
| **Unit Testing** | Individual functions/methods | `calculateTotal()` returns correct sum |
| **Integration Testing** | Components working together | Order API saves to database correctly |
| **System Testing** | End-to-end system | Place order -> confirm -> deliver flow |
| **Smoke Testing** | Critical paths after deployment | Can users log in and search restaurants? |
| **Sanity Testing** | Specific fix verification | Bug fix for tax calculation works |
| **Regression Testing** | Previously working features | Old order flow still works after new feature |
| **UAT** | Business requirements | Product owner verifies order flow |

---

## Testing Types -- Functional (continued)

### Unit Testing

```javascript
// FoodExpress: Unit test for calculateTotal
describe('calculateTotal', () => {
  it('should sum item prices correctly', () => {
    const items = [
      { name: 'Pizza', price: 299, qty: 2 },
      { name: 'Coke', price: 49, qty: 1 }
    ];
    expect(calculateTotal(items)).toBe(647);
  });

  it('should return 0 for empty cart', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should handle negative quantities', () => {
    const items = [{ name: 'Pizza', price: 299, qty: -1 }];
    expect(() => calculateTotal(items)).toThrow('Invalid quantity');
  });
});
```

### Integration Testing

```javascript
// FoodExpress: Integration test for order creation
describe('POST /api/orders', () => {
  it('should create order and return 201', async () => {
    const response = await request(app)
      .post('/api/orders')
      .send({ customerId: 1, restaurantId: 2, items: [...] });
    expect(response.status).toBe(201);
    expect(response.body.order_id).toBeDefined();
  });
});
```

---

## Testing Types -- Non-Functional

| Type | What It Tests | FoodExpress Example |
|------|--------------|---------------------|
| **Performance** | Speed, throughput | API responds in < 200ms |
| **Load Testing** | Behavior under expected load | 1000 concurrent users browsing |
| **Stress Testing** | Behavior beyond capacity | 10,000 concurrent orders |
| **Scalability** | Growth handling | Double the restaurants -- still fast? |
| **Security** | Vulnerabilities | SQL injection, auth bypass |
| **Usability** | User experience | Can a user place an order in 3 clicks? |
| **Compatibility** | Cross-platform | Works on Chrome, Safari, mobile |
| **Reliability** | Uptime, failure recovery | Service restarts after crash |
| **Accessibility** | Disability support | Screen reader compatible |

---

## Performance Testing Deep Dive

### Key Metrics

| Metric | Definition | FoodExpress Target |
|--------|-----------|-------------------|
| **Response Time** | Time from request to response | < 200ms (P95) |
| **Throughput** | Requests per second | > 500 RPS |
| **Error Rate** | % of failed requests | < 0.1% |
| **Concurrent Users** | Simultaneous active users | 1000+ |
| **Latency P99** | 99th percentile response time | < 1 second |

### Load Testing Progression

```
Step 1: Baseline     (10 users,    5 min)  --> Measure normal performance
Step 2: Load Test    (100 users,   15 min) --> Expected production load
Step 3: Stress Test  (500 users,   10 min) --> Find breaking point
Step 4: Spike Test   (1000 users,  1 min)  --> Sudden traffic burst
Step 5: Soak Test    (100 users,   4 hrs)  --> Memory leaks, degradation
```

---

## Tool Selection

### Testing Tools by Category

| Category | Tools | Use Case |
|----------|-------|----------|
| **Unit Testing** | Jest, JUnit, Mocha, pytest | Function-level testing |
| **API Testing** | Postman, REST Assured, Supertest | HTTP endpoint testing |
| **UI Automation** | Selenium, Cypress, Playwright | Browser-based testing |
| **Performance** | JMeter, Gatling, k6, Locust | Load and stress testing |
| **Security** | OWASP ZAP, Burp Suite, SonarQube | Vulnerability scanning |
| **Mobile** | Appium, Espresso, XCTest | Mobile app testing |
| **CI Integration** | Jenkins, GitHub Actions, GitLab CI | Automated test execution |

### Tool Selection Criteria

| Criteria | Questions to Ask |
|----------|-----------------|
| **Tech stack** | What language/framework is the app built with? |
| **Team skills** | What tools does the team already know? |
| **Budget** | Open source vs commercial? |
| **Integration** | Does it integrate with CI/CD pipeline? |
| **Reporting** | Does it generate useful test reports? |
| **Maintenance** | How much effort to maintain the test suite? |

---

## Manual vs Automation Testing

### When to Use Each

| Use Manual Testing When | Use Automation When |
|------------------------|---------------------|
| Exploratory testing | Regression testing |
| Usability testing | Smoke/sanity testing |
| One-time tests | Repetitive test execution |
| Complex visual validation | Data-driven testing |
| Ad-hoc bug investigation | CI/CD pipeline gates |
| New feature validation | Performance testing |

### Automation Pyramid

```
           /\
          /  \         UI Tests (few, slow, expensive)
         /    \        - Selenium, Cypress
        /------\
       /        \      Integration Tests (moderate)
      /          \     - API tests, service tests
     /------------\
    /              \   Unit Tests (many, fast, cheap)
   /                \  - Jest, JUnit
  /------------------\
```

### Rule of Thumb
- **70%** unit tests
- **20%** integration tests
- **10%** UI/E2E tests

---

## Test Case Design

### FoodExpress: Order Placement Test Cases

| ID | Scenario | Input | Expected Result | Priority |
|----|----------|-------|-----------------|----------|
| TC-01 | Place valid order | Valid customer, restaurant, items | Order created, 201 | P1 |
| TC-02 | Empty cart | No items | Error 400: "Cart is empty" | P1 |
| TC-03 | Invalid customer ID | Non-existent customer_id | Error 404: "Customer not found" | P1 |
| TC-04 | Closed restaurant | Restaurant with is_active=false | Error 400: "Restaurant closed" | P2 |
| TC-05 | Negative quantity | Item with qty = -1 | Error 400: "Invalid quantity" | P2 |
| TC-06 | Very large order | 100 items | Order created successfully | P3 |
| TC-07 | Special characters | Item name with emojis/unicode | Handled correctly | P3 |
| TC-08 | Concurrent orders | 50 simultaneous order requests | All succeed, no duplicates | P2 |

---

## Risk-Based Testing

### What Is Risk-Based Testing?

- Prioritize testing based on **risk** = probability x impact
- Focus limited testing time on the most critical areas
- Sustain teams often have limited time -- risk-based approach is essential

### Risk Assessment Matrix

| | High Impact | Low Impact |
|---|-----------|-----------|
| **High Probability** | Test extensively | Test moderately |
| **Low Probability** | Test moderately | Test minimally |

### FoodExpress Risk Assessment

| Feature | Probability of Failure | Impact | Risk Level | Testing Effort |
|---------|----------------------|--------|------------|----------------|
| Payment processing | Medium | Critical | HIGH | Extensive |
| Order placement | High (complex logic) | Critical | HIGH | Extensive |
| Restaurant search | Low | Major | MEDIUM | Moderate |
| User profile update | Low | Minor | LOW | Minimal |
| Admin dashboard | Low | Minor | LOW | Minimal |

---

## Defect Lifecycle

```
+--------+    +----------+    +--------+    +----------+
|  New   | -> | Assigned | -> | Fixed  | -> | Verified |
+--------+    +----------+    +--------+    +----------+
    |              |                              |
    v              v                              v
+--------+    +----------+                  +--------+
|Rejected|    |Deferred  |                  | Closed |
+--------+    +----------+                  +--------+
                                                |
                                                v
                                          +----------+
                                          | Reopened |
                                          +----------+
```

### Defect Report Template

| Field | Example |
|-------|---------|
| **Title** | Order total incorrect when discount applied |
| **Severity** | Major |
| **Priority** | P1 |
| **Steps to Reproduce** | 1. Add item (Rs 500) 2. Apply 20% discount 3. View total |
| **Expected** | Total = Rs 400 |
| **Actual** | Total = Rs 500 (discount not applied) |
| **Environment** | Staging, Chrome 114, API v2.3 |
| **Attachments** | Screenshot, API response JSON |

---

## Test Metrics

### Key Metrics for Sustain Teams

| Metric | Formula | Target |
|--------|---------|--------|
| **Defect Density** | Defects / KLOC | < 5 per KLOC |
| **Defect Leakage** | Prod bugs / Total bugs found | < 10% |
| **Test Coverage** | Lines covered / Total lines | > 80% |
| **Test Pass Rate** | Passed / Total executed | > 95% |
| **MTTR** | Mean time to resolve defects | < 4 hours (P1) |
| **Automation Rate** | Automated / Total test cases | > 60% |
| **Regression Rate** | Regressions / Total bugs | < 5% |

### FoodExpress Dashboard

```
+---------------------------------------------+
|  FoodExpress Quality Dashboard              |
+---------------------------------------------+
| Open Bugs: 12  | Critical: 2 | Major: 5    |
| Test Coverage: 72%  | Pass Rate: 94%       |
| Automation Rate: 45% | Defect Leakage: 8%  |
| MTTR (P1): 3.2 hrs  | Regression Rate: 3% |
+---------------------------------------------+
```

---

## Shift-Left Testing

### Traditional vs Shift-Left

```
Traditional:
Requirements -> Design -> Code -> Test -> Deploy
                                  ^^^^
                          Testing happens late

Shift-Left:
Requirements -> Design -> Code -> Test -> Deploy
^^^^^^^^^^^^    ^^^^^^    ^^^^
Testing starts early at every stage
```

### Shift-Left Activities

| Stage | Testing Activity |
|-------|-----------------|
| **Requirements** | Review requirements for testability, ambiguity |
| **Design** | Review architecture for test hooks, observability |
| **Code** | Unit tests (TDD), code review, static analysis |
| **Build** | Automated tests in CI pipeline |
| **Deploy** | Smoke tests, canary deployments |
| **Production** | Monitoring, alerting, chaos testing |

---

## MCQ Assessment Topics

| Topic | Key Concepts |
|-------|-------------|
| Quality Mindset | Prevention vs detection, cost of defects |
| QA vs QC vs QE | Definitions, focus, activities |
| Testing Types | Functional vs non-functional, when to use each |
| Test Design | Test cases, boundary values, equivalence partitioning |
| Severity vs Priority | Matrix, examples, when they differ |
| Manual vs Automation | When to use each, automation pyramid |
| Risk-Based Testing | Risk matrix, prioritization |
| Defect Lifecycle | States, transitions, report format |
| Test Metrics | Coverage, pass rate, defect density |

---

## Role Play -- Overview (90 minutes)

### Format
- **2 rounds**, 45 minutes each
- Teams of 4-5 people
- Each round has a different FoodExpress scenario
- Roles rotate between rounds

### Roles
| Role | Responsibility |
|------|---------------|
| **Product Owner** | Describes the feature/bug, accepts/rejects fixes |
| **QA Lead** | Creates test plan, assigns test cases |
| **Test Engineer** | Writes test cases, executes tests, reports bugs |
| **Developer** | Fixes bugs, explains root cause |
| **Scrum Master** | Facilitates discussion, manages time |

---

## Role Play -- Round 1: New Feature Testing

### Scenario

> "FoodExpress is launching a **loyalty rewards program**. Customers earn 1 point per Rs 100 spent. At 500 points, they get Rs 200 off their next order. The feature is ready for testing."

### Tasks
1. **Product Owner:** Present the feature requirements (5 min)
2. **QA Lead:** Create a test plan -- what needs to be tested? (10 min)
3. **Test Engineer:** Write 10 test cases covering positive, negative, and edge cases (15 min)
4. **Developer:** Review test cases and identify gaps (5 min)
5. **Team:** Prioritize test cases using risk-based approach (10 min)

### Expected Test Cases
- Points calculated correctly for exact amounts
- Points for amounts not divisible by 100 (e.g., Rs 350 = 3 points)
- Redemption at exactly 500 points
- Redemption with more than 500 points (e.g., 600 points)
- Attempt to redeem with less than 500 points
- Points after cancelled order (should they be reversed?)
- Concurrent point additions

---

## Role Play -- Round 2: Production Bug Triage

### Scenario

> "FoodExpress production has 5 open bugs reported by customers. The team has capacity to fix only 3 before the weekend. Prioritize and create a fix plan."

### Bug List
| # | Bug | Reported By |
|---|-----|-------------|
| 1 | Payment charged twice for some orders | 15 customers |
| 2 | Restaurant search shows closed restaurants | 3 customers |
| 3 | Order confirmation email has wrong total | 8 customers |
| 4 | Profile photo upload fails on iOS | 2 customers |
| 5 | Delivery ETA shows negative time after delivery | 5 customers |

### Tasks
1. **QA Lead:** Classify each bug by severity and priority (10 min)
2. **Developer:** Estimate fix effort for each bug (10 min)
3. **Product Owner:** Decide which 3 bugs to fix first with justification (10 min)
4. **Scrum Master:** Create a sprint plan for the fixes (10 min)
5. **Team:** Present triage decisions to the class (5 min)

---

## Role Play -- Evaluation Criteria

| Criteria | Weight | What Evaluators Look For |
|----------|--------|------------------------|
| Test case quality | 25% | Coverage, edge cases, clear expected results |
| Prioritization logic | 25% | Risk-based, data-driven, justified decisions |
| Communication | 20% | Clear explanations, active listening, consensus building |
| Role adherence | 15% | Staying in character, fulfilling role responsibilities |
| Time management | 15% | Completing tasks within time boxes |

---

## Quality in CI/CD Pipeline

### FoodExpress Quality Gates

```
Code Commit
    |
    v
+-----------+     +-----------+     +------------+
| Lint +    | --> | Unit      | --> | Integration|
| Static    |     | Tests     |     | Tests      |
| Analysis  |     | (< 2 min) |     | (< 10 min) |
+-----------+     +-----------+     +------------+
                                         |
                                         v
                                   +------------+     +-----------+
                                   | Security   | --> | Deploy to |
                                   | Scan       |     | Staging   |
                                   +------------+     +-----------+
                                                           |
                                                           v
                                                     +-----------+
                                                     | Smoke     |
                                                     | Tests     |
                                                     +-----------+
                                                           |
                                                           v
                                                     +-----------+
                                                     | Deploy to |
                                                     | Production|
                                                     +-----------+
```

---

## Key Takeaways

| Concept | Key Lesson |
|---------|------------|
| Quality Mindset | Prevention is cheaper than detection; shift testing left |
| QA vs QC vs QE | QA = process/preventive, QC = product/detective, QE = systemic/proactive |
| Testing Types | Functional (unit, integration, E2E) + Non-functional (perf, security, usability) |
| Automation Pyramid | 70% unit, 20% integration, 10% UI -- fast feedback at the base |
| Severity vs Priority | Severity = impact, Priority = urgency -- they can differ |
| Risk-Based Testing | Focus testing effort where probability x impact is highest |
| Defect Management | Clear lifecycle, good bug reports, track metrics |
| Tool Selection | Match tools to tech stack, team skills, and CI/CD integration |
| Sustain Quality | Every bug fix needs a test; question why the bug was missed |

> **Next: Module 14 -- Infrastructure Fundamentals: Understanding IT infrastructure, cloud vs traditional, and resilience.**
