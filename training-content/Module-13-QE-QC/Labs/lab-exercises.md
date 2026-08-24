# Module 13: QE/QC -- Incremental Labs

## Scenario

You just joined the FoodExpress sustain team. The app has been in production for 6 months. The previous developer left. There are **zero tests**, **no documentation**, and **bugs are being found by customers**.

Last night, 340 customers were double-charged. Rs 68,000 lost.

Your job: apply QC, QA, and QE practices to this codebase -- step by step.

## Codebase

```
starter-code/
  src/
    cart.js          -- Shopping cart (add, remove, totals, discount, delivery fee)
    order.js         -- Order creation, validation, status transitions
    restaurant.js    -- Restaurant search, availability, ratings
  test/              -- Empty. You will create test files here.
  package.json
```

## Setup

```
cd Labs/starter-code
npm install
```

---

## Lab 1 -- Be the Customer (QC: Manual Testing)

**Concept:** Quality Control = finding defects in the product.

**Time:** 20 min

You are a FoodExpress customer. No tests exist, so you will test the code manually by reading it and running it in Node.

### Tasks

**1.1** Open `src/cart.js`. Read the `getDeliveryFee()` method. The rule is:
  - Orders Rs 500 and above = free delivery
  - Orders below Rs 500 = Rs 30 delivery fee

Run this in terminal:
```
node -e "const Cart = require('./src/cart'); const c = new Cart(); c.addItem({id:1,price:500,quantity:1}); console.log('Delivery fee:', c.getDeliveryFee())"
```

What do you get? What should you get? Write down the bug.

**1.2** Read the `applyDiscount()` method. The rule is: 10% discount on Rs 750 should give Rs 675.

Run this:
```
node -e "const Cart = require('./src/cart'); const c = new Cart(); c.addItem({id:1,price:250,quantity:3}); console.log('Discounted:', c.applyDiscount(10))"
```

What do you get? What line has the bug?

**1.3** Open `src/order.js`. Read the `validate()` method. The rules are:
  - Minimum order: Rs 99
  - Maximum items: 20

Test the boundaries:
```
node -e "const {Order} = require('./src/order'); console.log('Rs 98:', new Order(1,1,[{id:1,price:98,quantity:1}]).validate())"
node -e "const {Order} = require('./src/order'); console.log('21 items:', new Order(1,1,Array(21).fill({id:1,price:10,quantity:1})).validate())"
```

Both should be rejected. Are they?

**1.4** Read the `cancel()` method in order.js. Can a delivered order be cancelled? Test it:
```
node -e "const {Order} = require('./src/order'); const o = new Order(1,1,[{id:1,price:100,quantity:1}]); o.updateStatus('delivered'); o.cancel(); console.log(o.status)"
```

**1.5** Open `src/restaurant.js`. Run:
```
node -e "const r = require('./src/restaurant'); console.log('Search pizza:', r.searchByName('pizza').length); console.log('All:', r.getAllRestaurants().length)"
```

Search should find "Pizza Corner" but doesn't. Why? And should inactive restaurants appear in the list?

### Deliverable

Write a bug report table:

| # | File | Method | Bug Description | Business Impact |
|---|------|--------|-----------------|-----------------|
| 1 | cart.js | getDeliveryFee | ? | ? |
| ... | | | | |

You should find **at least 8 bugs** across the 3 files.

---

## Lab 2 -- Classify and Prioritize (QC: Defect Management)

**Concept:** Severity = how bad. Priority = how soon. They can differ.

**Time:** 25 min

### Tasks

**2.1** Take your bug list from Lab 1. For each bug, assign:
  - **Severity:** Critical / Major / Minor / Trivial
  - **Priority:** P1 / P2 / P3 / P4

| # | Bug | Severity | Priority | Reasoning |
|---|-----|----------|----------|-----------|
| 1 | Delivery fee at Rs 500 | ? | ? | ? |

**2.2** You have capacity to fix **4 bugs** this sprint. Which 4? Write one sentence justifying each choice.

**2.3** For each selected bug, write:
  - Root cause (what is wrong in the code)
  - Which testing type would have caught it (Unit / Integration / Boundary / Functional)

**2.4** Write a full bug report for the discount bug using this format:

| Field | Value |
|-------|-------|
| Title | ? |
| Severity | ? |
| Priority | ? |
| Steps to Reproduce | 1. ... 2. ... 3. ... |
| Expected Result | ? |
| Actual Result | ? |
| Root Cause | ? |

### Discussion

Compare your severity/priority with a partner. Where you disagree, explain your reasoning. There is no single right answer.

---

## Lab 3 -- Write Unit Tests (QA: Test Case Design)

**Concept:** Quality Assurance = creating processes to prevent defects. Writing tests is QA.

**Time:** 35 min

You will create test files to catch the bugs you found manually.

### Tasks

**3.1** Create file `test/cart.test.js`. Write tests for the Cart class:

| Test # | What to Test | Expected Behavior |
|--------|-------------|-------------------|
| 1 | Add item to empty cart | Cart has 1 item, correct quantity |
| 2 | Add same item twice | Quantity increases, still 1 line item |
| 3 | Remove item | Item no longer in cart |
| 4 | Subtotal calculation | 2 items at Rs 250 x qty 2 = Rs 1000 |
| 5 | Delivery fee below Rs 500 | Returns 30 |
| 6 | Delivery fee at exactly Rs 500 | Returns 0 (THIS WILL FAIL -- the bug!) |
| 7 | Delivery fee above Rs 500 | Returns 0 |
| 8 | Apply 10% discount on Rs 750 | Returns 675 (THIS WILL FAIL -- the bug!) |
| 9 | Apply 0% discount | Returns original total |
| 10 | Empty cart total | Returns 0 |

Run: `npx jest test/cart.test.js --verbose`

Tests 6 and 8 should FAIL. That proves your tests caught the bugs.

**3.2** Create file `test/order.test.js`. Write tests for the Order class:

| Test # | What to Test | Expected Behavior |
|--------|-------------|-------------------|
| 1 | Valid order passes validation | Returns empty error array |
| 2 | Empty cart fails validation | Returns error "Cart is empty" |
| 3 | Rs 98 order fails validation | Returns minimum order error (WILL FAIL -- bug!) |
| 4 | Rs 99 order passes validation | Returns empty error array |
| 5 | 20 items passes validation | Returns empty error array |
| 6 | 21 items fails validation | Returns max items error (WILL FAIL -- bug!) |
| 7 | Cancel placed order | Status changes to "cancelled" |
| 8 | Cancel delivered order | Should throw error (WILL FAIL -- bug!) |

Run: `npx jest test/order.test.js --verbose`

Tests 3, 6, and 8 should FAIL.

**3.3** Create file `test/restaurant.test.js`. Write tests for restaurant.js:

| Test # | What to Test | Expected Behavior |
|--------|-------------|-------------------|
| 1 | getAllRestaurants returns only active | Should NOT include Dragon Wok or Taco Town (WILL FAIL) |
| 2 | searchByName is case-insensitive | "pizza" should find "Pizza Corner" (WILL FAIL) |
| 3 | searchByCuisine excludes inactive | Chinese cuisine returns empty (Dragon Wok inactive) (WILL FAIL) |
| 4 | getTopRated excludes inactive | Top 3 should not include inactive restaurants (WILL FAIL) |
| 5 | addReview averages, not overwrites | Rating 4.5 + review 3.0 should not become 3.0 (WILL FAIL) |

Run: `npx jest test/restaurant.test.js --verbose`

All 5 should FAIL. Good -- your tests caught 5 more bugs.

### Checkpoint

Run `npx jest --verbose`. You should see:
- Multiple tests FAILING (proving bugs exist)
- Some tests PASSING (proving correct behavior)
- This is exactly how a sustain engineer discovers inherited bugs

---

## Lab 4 -- Fix the Bugs (QC + QA: Test-Driven Fixing)

**Concept:** Fix the code. Re-run tests. Green = fixed. This is regression prevention.

**Time:** 25 min

### Tasks

Fix bugs one at a time. After each fix, run `npx jest` to confirm.

**4.1** Fix `cart.js` -- `getDeliveryFee()`:
  - Change `>` to `>=` so Rs 500 exact gets free delivery
  - Run tests. The delivery fee boundary test should now PASS.

**4.2** Fix `cart.js` -- `applyDiscount()`:
  - Change `percent / 1000` to `percent / 100`
  - Run tests. The discount test should now PASS.

**4.3** Fix `order.js` -- `validate()` minimum order:
  - Fix the condition so Rs 98 is rejected and Rs 99 is accepted
  - Run tests.

**4.4** Fix `order.js` -- `validate()` max items:
  - Fix the condition so 21 items is rejected and 20 is accepted
  - Run tests.

**4.5** Fix `order.js` -- `cancel()`:
  - Add a check: only allow cancel if status is `placed` or `confirmed`
  - Throw an error for other statuses
  - Run tests.

**4.6** Fix `restaurant.js` -- `getAllRestaurants()`:
  - Filter to return only active restaurants
  - Run tests.

**4.7** Fix `restaurant.js` -- `searchByName()`:
  - Make search case-insensitive
  - Run tests.

**4.8** Fix `restaurant.js` -- `getTopRated()`:
  - Filter out inactive restaurants before sorting
  - Run tests.

**4.9** Fix `restaurant.js` -- `addReview()`:
  - Store a review count and calculate the running average instead of overwriting
  - Run tests.

### Checkpoint

Run `npx jest --verbose`. ALL tests should now PASS.

This is the power of tests: you fixed 9 bugs, and after each fix you can verify nothing else broke. That is **regression prevention**.

---

## Lab 5 -- Measure and Improve (QE: Coverage and Metrics)

**Concept:** Quality Engineering = building quality into the system with metrics and automation.

**Time:** 20 min

### Tasks

**5.1** Run test coverage:
```
npx jest --coverage
```

Look at the output. It shows:
- % Statements covered
- % Branches covered
- % Functions covered
- % Lines covered

Write down the coverage for each file. Is it above 80%?

**5.2** Find uncovered branches. The coverage report highlights lines in red that your tests don't exercise. Add tests to cover:
  - `cart.js`: `updateQuantity()` method (not tested yet)
  - `cart.js`: `clear()` method (not tested yet)
  - `order.js`: `getTotal()` method
  - `order.js`: `updateStatus()` with invalid status
  - `restaurant.js`: `getById()` with non-existent ID
  - `restaurant.js`: `isOpen()` method

**5.3** Re-run `npx jest --coverage`. Did your coverage go up?

**5.4** Fill in this metrics table for your test suite:

| Metric | Value |
|--------|-------|
| Total tests | ? |
| Passing | ? |
| Failing | ? |
| Pass rate | ? % |
| Statement coverage | ? % |
| Branch coverage | ? % |
| Bugs found by tests | ? |
| Bugs fixed | ? |

---

## Lab 6 -- Test Strategy and Automation Plan (QE: Planning)

**Concept:** QE decides what to test, what to automate, and what to measure.

**Time:** 20 min

### Part A: Test Strategy

FoodExpress v2.4 is releasing next week with:
- 2 new features: Loyalty Points + Scheduled Orders
- 9 bug fixes (the ones you fixed in Lab 4)
- 1 performance fix: order history pagination

Fill in the test plan template in `starter-code/test-plan.md`:
- Scope (in/out)
- Test types (Unit, Integration, E2E, Performance)
- Entry criteria (what must be true before testing)
- Exit criteria (what must be true before release)
- Risks and mitigations

### Part B: Automation Decision

You have 200 test cases across 9 categories but budget to automate only 80 this quarter.

| Category | Count | Frequency | Stability | Impact |
|----------|-------|-----------|-----------|--------|
| Login/Auth | 15 | Every release | High | High |
| Restaurant Search | 25 | Every release | High | Medium |
| Order Placement | 40 | Every release | Medium | High |
| Payment | 20 | Every release | Medium | High |
| User Profile | 15 | Monthly | High | Low |
| Delivery Tracking | 20 | Every release | Low (GPS) | Medium |
| Notifications | 15 | Every release | Low (device) | Low |
| Admin Dashboard | 25 | Quarterly | High | Low |
| Reports | 25 | Monthly | Medium | Medium |

Score each 1-3 on Frequency, Stability, Impact. Pick categories totaling ~80 tests. Justify why some stay manual.

---

## Summary: What You Applied

| Lab | What You Did | QE/QC Concept |
|-----|-------------|---------------|
| Lab 1 | Read code, ran it manually, found bugs | **QC** -- Manual testing, exploratory testing |
| Lab 2 | Classified bugs, wrote bug reports | **QC** -- Severity vs priority, defect lifecycle |
| Lab 3 | Wrote Jest tests that caught bugs | **QA** -- Test case design, boundary testing |
| Lab 4 | Fixed bugs, verified with tests | **QA/QC** -- Regression prevention, test-driven fixing |
| Lab 5 | Measured coverage, filled gaps | **QE** -- Test metrics, coverage analysis |
| Lab 6 | Created test strategy, planned automation | **QE** -- Risk-based testing, automation planning |

You started with a codebase that had **0 tests, 0 documentation, 9+ bugs**.

You ended with **tested code, documented bugs, a test strategy, and an automation plan**.

That is what a sustain engineer does on Day 1.
