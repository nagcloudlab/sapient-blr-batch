# QA vs QC vs QE — Explained with FoodExpress Demo

## The FoodExpress Scenario

We built a **FoodExpress order module** with a deliberately planted bug:

> When a customer applies a 20% discount coupon (SAVE20), the discount amount is **calculated but never subtracted** from the total.
>
> **Expected:** Rs 500 + Rs 25 (tax) - Rs 100 (discount) = **Rs 425**
> **Actual:** Rs 500 + Rs 25 (tax) = **Rs 525** (discount ignored!)

This single bug helps us understand three different quality approaches.

---

## QC — Quality Control

> **"Is there a bug in the product?"**

| Attribute | Detail |
|-----------|--------|
| **Full Name** | Quality Control |
| **Focus** | Product |
| **Nature** | Detective & Reactive |
| **Goal** | Find defects that already exist |

### QC in Our Demo

| Activity | What Happened |
|----------|---------------|
| Run `npm test` | TC-09 **failed** — caught the discount bug |
| Manual testing | Applied SAVE20 coupon, noticed total was wrong |
| Test execution | Ran 27 test cases, verified expected vs actual |
| Bug reporting | Wrote a defect report with severity, priority, steps to reproduce |

### QC Artifacts Produced

```
Test Case ID : TC-09
Title        : Total should subtract discount
Input        : 1x Pizza (Rs 500), 20% discount
Expected     : Rs 425
Actual       : Rs 525
Result       : FAIL
```

### Defect Report

| Field | Value |
|-------|-------|
| **Title** | Order total does not subtract discount amount |
| **Severity** | Critical — financial impact, every discounted order is wrong |
| **Priority** | P1 — must fix immediately |
| **Steps** | 1. Add item (Rs 500) → 2. Apply SAVE20 → 3. View total |
| **Expected** | Total = Rs 425 |
| **Actual** | Total = Rs 525 (discount not applied) |
| **Root Cause** | Line 42: `total = subtotal + tax` (missing `- discount`) |

> **QC Summary:** We tested the product, found the bug, and reported it.

---

## QA — Quality Assurance

> **"What process would have prevented this bug?"**

| Attribute | Detail |
|-----------|--------|
| **Full Name** | Quality Assurance |
| **Focus** | Process |
| **Nature** | Preventive & Proactive |
| **Goal** | Prevent defects from being introduced |

### QA Processes That Would Have Caught This Bug

| QA Process | How It Prevents the Bug |
|------------|------------------------|
| **Code Review Checklist** | Reviewer checks: "Is every calculated value used?" — `discount` is computed but never subtracted |
| **Pair Programming** | Second pair of eyes would question why `discount` variable exists but isn't in the total formula |
| **Definition of Done** | Rule: "Every function must have unit tests covering all code paths" |
| **Test-Driven Development** | Writing the test FIRST (TC-09) would have caught the bug BEFORE the code was committed |
| **Static Analysis** | Linter rule for unused variables would flag `discount` not being used in the return |

### QA Checklist Example

```
Code Review Checklist — FoodExpress
------------------------------------
[ ] All calculated values are used in the output
[ ] Business logic matches requirements document
[ ] Edge cases handled (zero, negative, boundary values)
[ ] Unit tests cover positive, negative, and edge cases
[ ] No hardcoded values — use constants
[ ] Error messages are user-friendly
```

> **QA Summary:** We define processes and standards that prevent bugs from entering the codebase in the first place.

---

## QE — Quality Engineering

> **"How do we automate and scale quality across the system?"**

| Attribute | Detail |
|-----------|--------|
| **Full Name** | Quality Engineering |
| **Focus** | System |
| **Nature** | Systemic & Proactive |
| **Goal** | Build quality into the engineering pipeline |

### QE in Our Demo

| QE Practice | Implementation |
|-------------|---------------|
| **Test Automation Framework** | Jest + React Testing Library — tests run in seconds, not hours |
| **Coverage Metrics** | `npm run test:coverage` — tracks % of code tested automatically |
| **Automation Pyramid** | 13 unit tests (fast, cheap) + 14 component tests (moderate) |
| **CI/CD Quality Gates** | Tests must pass before code can be merged or deployed |
| **Quality Thresholds** | "Build fails if coverage drops below 80%" |

### CI/CD Pipeline with Quality Gates

```
Code Commit
    │
    ▼
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│ Lint +       │ ──► │ Unit Tests  │ ──► │ Component    │
│ Static       │     │ (13 tests)  │     │ Tests        │
│ Analysis     │     │ < 1 sec     │     │ (14 tests)   │
└─────────────┘     └─────────────┘     └──────────────┘
                                              │
                          ┌───────────────────┘
                          ▼
                    ┌─────────────┐     ┌──────────────┐
                    │ Coverage    │ ──► │ Deploy to    │
                    │ Check ≥80%  │     │ Staging      │
                    └─────────────┘     └──────────────┘
```

### Coverage Report from Our Demo

```
--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |   78.57 |    82.22 |      75 |   84.93 |
 components/        |   72.13 |    73.07 |   71.42 |   80.39 |
  OrderForm.jsx     |   72.13 |    73.07 |   71.42 |   80.39 |
 utils/             |   95.65 |    94.73 |     100 |   95.45 |
  calculateTotal.js |   95.65 |    94.73 |     100 |   95.45 |
--------------------|---------|----------|---------|---------|
```

> **QE Summary:** We build automated systems that enforce quality at every stage, making it nearly impossible for bugs to reach production.

---

## Side-by-Side Comparison

| Aspect | QC | QA | QE |
|--------|----|----|-----|
| **Question** | Is there a bug? | How do we prevent bugs? | How do we automate quality? |
| **Focus** | Product | Process | System |
| **Nature** | Reactive | Preventive | Systemic |
| **When** | After code is written | Before/during development | Across the entire lifecycle |
| **Who** | Testers | Everyone | Engineering team |
| **In our demo** | TC-09 catches the bug | Code review checklist would prevent it | Jest + CI pipeline enforces it at scale |

---

## The Bug's Journey Through QC → QA → QE

```
WITHOUT quality practices:
  Developer writes bug ──► Bug reaches production ──► Customer loses money

WITH QC only:
  Developer writes bug ──► Tester finds it ──► Bug fixed before release

WITH QA + QC:
  Code review catches it ──► Bug never enters codebase

WITH QE + QA + QC:
  CI pipeline auto-rejects ──► Coverage gate blocks merge ──► Bug impossible to deploy
```

---

## Key Takeaway

```
QC  = "We found the bug"         (detective)
QA  = "We prevented the bug"     (process guardian)
QE  = "We made bugs impossible"  (system builder)
```

**All three work together.** QE builds the automated safety nets, QA defines the processes, and QC verifies the product. In sustain engineering, you need all three — because you're the last line of defense before production.

---

## Try It Yourself

```bash
cd foodexpress-qe-demo

# See the bug in action (QC - finding defects)
npm test

# See quality metrics (QE - automated measurement)
npm run test:coverage

# Fix the bug: src/utils/calculateTotal.js, line 42
# Change:  const total = subtotal + tax;
# To:      const total = subtotal + tax - discount;

# Verify the fix (QC - defect lifecycle: Fixed → Verified → Closed)
npm test
```
