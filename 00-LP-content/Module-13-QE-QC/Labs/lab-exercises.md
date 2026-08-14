# Module 13: QE/QC Testing -- Exercises

## Lab Overview

This module combines written exercises, test case design, and role play activities. There is no code to debug -- instead, you will practice the analytical and communication skills that sustain engineers need for quality work.

> "Hi Team, the FoodExpress platform has been running in production for 6 months now and we have zero automated tests, no test plan, and bugs are being found by customers instead of by us. We need to establish a quality baseline immediately. Today you will create a test strategy, write test cases, triage production bugs, and practice quality communication as a team."

---

## Exercise 1: Test Case Design (45 min)

### Scenario
You are given the FoodExpress **Order Placement** feature. Write comprehensive test cases.

### Feature Specification
- Customer selects a restaurant, adds items to cart, and places an order
- Minimum order amount: Rs 99
- Maximum 20 items per order
- Delivery fee: Rs 30 for orders under Rs 500, free for Rs 500+
- Estimated delivery time: 30-45 minutes
- Payment methods: Cash on Delivery, Credit Card, UPI
- Order confirmation sent via email and push notification

### Tasks
1. Write **15 test cases** in this format:

| TC ID | Category | Scenario | Steps | Expected Result | Priority |
|-------|----------|----------|-------|-----------------|----------|
| TC-01 | Positive | ... | ... | ... | P1 |

2. Ensure coverage of:
   - [ ] Happy path (valid order with all fields)
   - [ ] Boundary values (Rs 99 minimum, Rs 500 delivery threshold, 20 items max)
   - [ ] Negative cases (empty cart, invalid payment, closed restaurant)
   - [ ] Edge cases (exactly 20 items, exactly Rs 99, exactly Rs 500)
   - [ ] Error handling (network timeout, payment failure mid-order)

3. Classify each test case:
   - **Functional** or **Non-functional**
   - **Positive** or **Negative**
   - **P1** (must pass), **P2** (should pass), or **P3** (nice to verify)

---

## Exercise 2: Bug Triage (30 min)

### Scenario
The following 8 bugs were reported in FoodExpress production last week. You have capacity to fix 4 before the next release (Friday). Prioritize them.

| # | Bug Title | Reporter | Frequency | Description |
|---|-----------|----------|-----------|-------------|
| 1 | Double charge on credit card | 12 customers | 2% of orders | Customer is charged twice; refund takes 5-7 days |
| 2 | Search returns closed restaurants | 3 customers | Always for closed ones | Closed restaurants appear in search with "Order Now" button |
| 3 | Delivery tracking shows wrong location | 8 customers | Intermittent | GPS pin is 2-3 blocks off from actual driver location |
| 4 | Push notification not received on Android 14 | 5 customers | All Android 14 | No order confirmations on latest Android |
| 5 | Order history page takes 12 seconds to load | 20 customers | All users with 50+ orders | No pagination, loads all orders at once |
| 6 | Promo code "WELCOME50" gives 50% off instead of Rs 50 off | 1 customer | 100% reproducible | Code interpretation bug: percentage vs flat discount |
| 7 | Restaurant rating shows 0.0 after new review | 2 customers | After first review | Average calculation divides by wrong count |
| 8 | Logo appears stretched on tablet | 1 customer | iPad landscape | CSS aspect-ratio not set |

### Tasks
1. Classify each bug by **Severity** (Critical/Major/Minor/Trivial) and **Priority** (P1/P2/P3/P4)
2. Select the **4 bugs** you would fix first, with justification
3. For each selected bug, write a 2-sentence **root cause hypothesis**
4. Identify which bug should have been caught by which type of testing

### Deliverable Format

| # | Severity | Priority | Fix This Sprint? | Justification |
|---|----------|----------|-----------------|---------------|
| 1 | ? | ? | Yes/No | ... |

---

## Exercise 3: Test Strategy Document (30 min)

### Scenario
You are the QA Lead for FoodExpress. Create a 1-page test strategy for the next release (v2.4) which includes:
- 2 new features: Loyalty Points + Scheduled Orders
- 5 bug fixes from Exercise 2
- 1 performance improvement: order history pagination

### Template
Fill in each section:

1. **Scope:** What is being tested? What is out of scope?
2. **Test Types:** Which types of testing will you perform? (Unit, Integration, E2E, Performance, Security)
3. **Environments:** Where will testing happen? (Local, Dev, Staging, Prod)
4. **Entry Criteria:** What must be true before testing starts?
5. **Exit Criteria:** What must be true before release?
6. **Risks:** What could go wrong? What is the mitigation?
7. **Tools:** Which tools will you use for each test type?
8. **Schedule:** How much time for each testing phase?

---

## Exercise 4: Automation Decision Matrix (20 min)

### Scenario
The FoodExpress team has 200 test cases. They can only automate 80 this quarter. Decide which to automate.

### Test Case Inventory

| Category | Count | Execution Frequency | Stability |
|----------|-------|-------------------|-----------|
| Login/Auth | 15 | Every release | High |
| Restaurant Search | 25 | Every release | High |
| Order Placement | 40 | Every release | Medium |
| Payment Processing | 20 | Every release | Medium |
| User Profile | 15 | Monthly | High |
| Delivery Tracking | 20 | Every release | Low (GPS flaky) |
| Admin Dashboard | 25 | Quarterly | High |
| Notifications | 15 | Every release | Low (device-dependent) |
| Reports/Analytics | 25 | Monthly | Medium |

### Tasks
1. Score each category on: **Frequency** (1-3), **Stability** (1-3), **Business Impact** (1-3)
2. Calculate priority score = Frequency + Stability + Impact
3. Select categories to automate first (total ~80 test cases)
4. Justify why some categories are better left as manual tests

---

## Checkpoints

### Checkpoint 1 (Morning Complete)
- [ ] Exercise 1: 15 test cases written with proper coverage
- [ ] Exercise 2: All 8 bugs classified, 4 selected with justification
- [ ] Both exercises reviewed by a peer

### Checkpoint 2 (Afternoon Complete)
- [ ] Exercise 3: Test strategy document completed
- [ ] Exercise 4: Automation decision matrix completed
- [ ] MCQ assessment completed (30 min)
- [ ] Role Play rounds completed (90 min)

---

## Bonus Challenges

1. **Write a bug report** for Bug #1 (double charge) using the full defect report template from the slides
2. **Create a test data matrix** for the order placement feature -- list all combinations of payment method, delivery fee, promo code, and order size
3. **Design a performance test plan** for the restaurant search API: define load profiles, think times, and success criteria
4. **Map the FoodExpress features** to the testing pyramid: which features need unit tests, integration tests, and E2E tests?
5. **Calculate defect density** if FoodExpress has 50,000 lines of code and 38 known bugs. Is this acceptable?
