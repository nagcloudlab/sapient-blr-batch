# Day 12 Teaching Plan -- QE/QC Testing (Activity-First Approach)
## Thu Aug 13, 2026 | Office Day 12 | Module 13

**Events:** Assessment 5 (MCQ+Coding) | QE/QC Role Play | Learning Checkpoint 3 & 4

---

## Core Philosophy: Experience First, Label Second

DO NOT open slides at 8:15. Instead, throw participants into real quality problems.
They experience the pain, THEN you give them the vocabulary.

**The flow:**
1. Break something -> feel the pain -> learn the concept
2. Argue about bugs -> disagree -> learn severity vs priority
3. Read bad tests -> find bugs in tests themselves -> learn testing types
4. Triage under pressure -> learn risk-based thinking

---

## At a Glance

| Time | Block | What They DO (not what you lecture) | Duration |
|------|-------|-------------------------------------|----------|
| 08:00-08:15 | Opener | Recap + "Production is on fire" simulation | 15 min |
| 08:15-09:00 | Activity 1 | LIVE: Run buggy tests, watch them fail | 45 min |
| 09:00-09:30 | Debrief 1 | Theory: Testing types, test isolation, regression | 30 min |
| 09:30-10:15 | Activity 2 | "You are QA Lead" -- classify 8 production bugs | 45 min |
| 10:15-10:30 | | BREAK | 15 min |
| 10:30-11:00 | Debrief 2 | Theory: Severity vs Priority, Defect Lifecycle | 30 min |
| 11:00-11:45 | Activity 3 | Write 15 test cases for Order Placement | 45 min |
| 11:45-12:15 | Debrief 3 | Theory: QA vs QC vs QE, Quality Mindset | 30 min |
| 12:15-12:30 | Transition | Prep for Learning Checkpoints | 15 min |
| 12:30-13:00 | Checkpoint | Learning Checkpoint 3 & 4 | 30 min |
| 13:00-13:30 | | LUNCH | 30 min |
| 13:30-14:15 | Activity 4 | LIVE: Run Jest on FoodExpress, write 3 new tests | 45 min |
| 14:15-14:45 | Debrief 4 | Theory: Automation Pyramid, Non-Functional, Tools | 30 min |
| 14:45-15:15 | Activity 5 | Automation Decision Matrix -- which 80 of 200 to automate? | 30 min |
| 15:15-15:30 | | BREAK (send quiz to Chandana) | 15 min |
| 15:30-16:00 | Assessment | Assessment 5: MCQ + Coding | 30 min |
| 16:00-17:00 | Role Play | 2 rounds: Test Plan Defense + Bug Triage | 60 min |

---

## Detailed Plan

---

### 08:00-08:15 -- "PRODUCTION IS ON FIRE" (15 min)

Skip the normal recap. Start with urgency.

**Walk in and say (in character):**

> "Good morning. I have bad news. Last night at 11 PM, 340 customers were double-charged
> on FoodExpress. Rs 68,000 in revenue lost. The CEO is on a call in 2 hours wanting answers.
> Our test coverage is 0%. We have no test plan. We have no idea what else is broken.
> Today, we fix this. You are the sustain engineering team. Let's go."

Write on whiteboard:
```
SITUATION REPORT -- FoodExpress
- 340 double-charge incidents (last 2 hours)
- 0% test coverage
- No test plan
- CEO call in 2 hours
- YOUR JOB: Find what's broken. Fix it. Make sure it never happens again.
```

Quick recap of yesterday (2 min): "Before we dive in -- quick SQL check. What SQL command would
you use to find all double-charged orders?" (Answer: GROUP BY + HAVING COUNT > 1)

**Bridge:** "Now let's look at the actual code."

---

### 08:15-09:00 -- ACTIVITY 1: Run Buggy Tests Live (45 min)

**This is the hook. This is where they get engaged.**

#### Setup (5 min)
- Every participant opens their terminal
- Navigate to `training-content/Module-13-QE-QC/Labs/starter-code/`
- Run: `npm install` (package.json already has jest)
- Run: `npx jest`

#### What happens (they see this):
```
FAIL  test/cart.test.js
  Cart
    + adds an item to the cart                    PASS
    + increases quantity when same item added      PASS
    + removes an item from the cart                PASS
    + calculates total correctly                   PASS
    - returns cart summary                         FAIL
    + fetches delivery fee for Bangalore pincode   PASS  <-- THIS IS SUSPICIOUS
    - applies 10% discount correctly               FAIL

FAIL  test/order.test.js
  Order Service
    + creates order with placed status             PASS
    + calculates subtotal from items               PASS
    + calculates total with delivery fee           PASS  <-- PASSES BY ACCIDENT
    + cancels a placed order                       PASS
    + confirms a placed order                      PASS
    + throws when confirming a non-placed order    PASS
    NOTE: "testCancelDeliveredOrderThrows" never ran!
```

#### Bug Hunt Challenge (25 min)

Put this on the whiteboard:

```
BUG HUNT -- Find 6 bugs across 2 test files
===========================================
Rules:
- Work in pairs
- You have 25 minutes
- For each bug: (1) What's wrong? (2) Why is it dangerous? (3) How to fix it?

Hints:
- 4 bugs in cart.test.js
- 2 bugs in order.test.js
- Some bugs make tests FAIL (obvious)
- Some bugs make tests PASS when they shouldn't (DANGEROUS)
- One test NEVER RUNS AT ALL (MOST DANGEROUS)
```

**Walk around the room.** Give hints to stuck pairs after 10 minutes:
- "Look at line 61 of cart.test.js. Where is the cart created? What happens between tests?"
- "The delivery fee test passes. But should it? What does fetchDeliveryFee return?"
- "In order.test.js, count the test() calls. Now count the functions. See the mismatch?"

#### Class Discussion (15 min)

Go through each bug together. **Let participants explain, not you.**

| Bug | File | Line | What's Wrong | Why It's Dangerous |
|-----|------|------|--------------|--------------------|
| 1 | cart.test.js | 61 | `const cart = new Cart()` outside describe, no beforeEach | Tests leak state -- pass in isolation, fail in sequence |
| 2 | cart.test.js | 92 | `toBe` on objects (reference equality) | Test fails even when code is correct |
| 3 | cart.test.js | 98 | Missing `await` on async function | Test ALWAYS passes -- never actually checks the value |
| 4 | cart.test.js | 34 | `percent/1000` instead of `percent/100` | Regression bug -- discount is 10x too small |
| 5 | order.test.js | 78 | `function testCancel...()` not wrapped in `test()` | Test exists in file but Jest never runs it -- silent gap |
| 6 | order.test.js | 72 | `expect(450).toBe(order.getTotal())` -- args swapped | Passes by coincidence, confusing failure messages |

**Key teaching moments to drop during discussion:**

After Bug 1: *"This is why test ISOLATION matters. This is the #1 beginner mistake."*

After Bug 3: *"This is the scariest bug in testing -- a test that always passes.
You think you're safe. You're not. This is called a FALSE POSITIVE.
How many tests in real production codebases do you think have this problem?"*

After Bug 5: *"This test was WRITTEN. Someone wrote it. But it NEVER RUNS.
The code coverage tool shows 0% for that code path. But the file looks complete.
This is why you review tests, not just code."*

---

### 09:00-09:30 -- DEBRIEF 1: Testing Concepts (30 min)

**NOW open slides** -- but only to label what they already experienced.

"Let's put names to what you just saw."

1. **Testing Types (10 min)** -- slides from Module-13-QE-QC.md
   - "Bug 4 (discount regression) -- that's a **regression bug**. A working feature broke after a code change."
   - "Running cart.test.js is a **unit test**. Testing one class in isolation."
   - "If we tested the cart talking to a real database, that's an **integration test**."
   - "If we tested the full order flow from UI to database, that's an **E2E/system test**."
   - Quick table on whiteboard:

   | Type | What You Test | Speed | Cost | Example from Today |
   |------|--------------|-------|------|-------------------|
   | Unit | One function | Fast | Cheap | `calculateTotal()` |
   | Integration | Components together | Medium | Medium | Cart + Database |
   | E2E | Full user flow | Slow | Expensive | Place order end-to-end |
   | Smoke | "Does it start?" | Fast | Cheap | Can the app load? |
   | Regression | "Did we break old stuff?" | Varies | Critical | Bug 4 -- discount broke |

2. **Test Isolation (5 min)**
   - "Bug 1 taught us: each test must start fresh. `beforeEach` exists for this reason."
   - "In Java/JUnit: `@BeforeEach`. In Jest: `beforeEach()`. Same concept."

3. **False Positives (5 min)**
   - "Bug 3 and Bug 5 taught us: a passing test is NOT proof of correctness."
   - "A test that never fails is either perfect or broken. Usually broken."
   - Introduce: **Mutation testing** concept (if you flip the logic and the test still passes, the test is useless)

4. **Smoke vs Sanity vs Regression (10 min)**
   - Draw sequence on whiteboard:
   ```
   Deploy --> Smoke ("does it start?") --> Sanity ("does my fix work?")
         --> Regression ("did I break anything else?") --> UAT ("business happy?")
   ```
   - "After you fix the discount bug and deploy, which tests do you run? ALL of these. In that order."

---

### 09:30-10:15 -- ACTIVITY 2: "You Are QA Lead" -- Bug Triage (45 min)

**Setup (5 min):**
Distribute Exercise 2 from lab-exercises.md (the 8 production bugs) OR project on screen.

> "It's Friday, 4:30 PM. You just got this dump from the support team.
> You have capacity to fix 4 bugs before Monday. Which 4?
> You have 15 minutes. Work ALONE first."

#### Individual Work (15 min)
Each participant fills in:

| # | Severity (Critical/Major/Minor/Trivial) | Priority (P1/P2/P3/P4) | Fix this sprint? | Why? |
|---|----------------------------------------|------------------------|-----------------|------|

**Do NOT teach severity vs priority definitions yet.** Let them use their gut instinct.

#### Pair Debate (15 min)
Pair up. Compare answers. Rules:
- Where you disagree, you must ARGUE YOUR CASE
- If you change your mind, write down WHY

**Walk around and listen.** You'll hear the exact confusions you need to address:
- "Is the double charge a P1 because it's bad, or because it needs to be fixed now?" (BOTH, but for different reasons)
- "The promo code bug is only 1 customer!" "But it's Rs 1000 per use!" (frequency vs impact)
- "The slow page is annoying but not broken" vs "20 customers complained!" (severity vs priority split)

#### Class Vote (10 min)
Go through each bug on whiteboard. Ask for a show of hands:
- "Who rated Bug #1 as Critical?" "Who said Major?"
- "Who would fix Bug #5 this sprint?" "Who would defer?"

**Capture the disagreements.** These are GOLD. Don't resolve them yet.

---

### 10:15-10:30 -- BREAK

---

### 10:30-11:00 -- DEBRIEF 2: Severity, Priority, and the Defect Lifecycle (30 min)

Now resolve the disagreements from Activity 2.

1. **Severity vs Priority Definitions (10 min)**
   - "You just argued about these. Now let me give you the official definitions."
   - Severity = **technical impact** (how bad is the damage to the system/user?)
   - Priority = **business urgency** (how soon must we fix it?)
   - They CAN differ:
     - CEO's photo broken = Trivial severity, P1 priority (because CEO)
     - PDF export crashes = Critical severity, P3 priority (has CSV workaround)
   - "In your triage, did anyone rate a bug as high severity but low priority? That's CORRECT and that's the nuance."

2. **Reveal the "Correct" Answers (10 min)**
   - Show solution from SOLUTION.md
   - Walk through reasoning for each bug
   - Key: **financial impact bugs are always P1** (#1 double charge, #6 promo code)
   - Key: "How many customers" matters less than "what's the damage per incident"

3. **Defect Lifecycle + Bug Report (10 min)**
   - Draw lifecycle on whiteboard: New -> Assigned -> Fixed -> Verified -> Closed / Reopened
   - Write a live bug report for Bug #1 (double charge):
     ```
     Title:     Payment charged twice for orders above Rs 2000
     Severity:  Critical
     Priority:  P1
     Steps:     1. Add items totaling Rs 2500
                2. Select Credit Card payment
                3. Click "Place Order"
                4. Check bank statement
     Expected:  Single charge of Rs 2500
     Actual:    Two charges of Rs 2500 each
     Env:       Production, all payment gateways
     Impact:    340 customers, Rs 68,000 revenue loss
     ```
   - "This is what a real bug report looks like. Notice: steps are specific, expected vs actual is clear, impact is quantified."

---

### 11:00-11:45 -- ACTIVITY 3: Write 15 Test Cases (45 min)

**Exercise 1 from lab-exercises.md**

Read the spec aloud:
> "FoodExpress Order Placement:
> - Min order Rs 99, Max 20 items
> - Delivery: Rs 30 under Rs 500, free above Rs 500
> - Payment: COD, Credit Card, UPI
> - Confirmation: email + push notification
> - Delivery time: 30-45 minutes"

#### Setup (5 min)
- Project the test case template on screen
- Give one example:
  ```
  TC-01 | Positive | Place order with 3 items, COD | 1. Select restaurant
  2. Add 3 items (total Rs 450) 3. Select COD 4. Place order |
  Order confirmed, delivery fee Rs 30 | P1
  ```

#### Individual Work (25 min)
- Each participant writes 15 test cases
- Must include: at least 3 boundary values, 3 negative cases, 2 edge cases
- Walk around. Common mistakes to watch for:
  - Vague steps ("add items" -- WHICH items? HOW MANY?)
  - Missing boundary: Rs 98 vs Rs 99 vs Rs 100
  - Missing boundary: Rs 499 vs Rs 500 vs Rs 501
  - Missing boundary: 19 items vs 20 vs 21
  - Forgetting: what if restaurant is closed? what if payment fails mid-order?

#### Peer Review (10 min)
- Swap test cases with neighbor
- Reviewer checks: "Could I execute this test without asking any questions?"
- Reviewer marks any test case that's too vague or missing expected result

#### Quick Share (5 min)
- Ask 2-3 participants to share their most creative edge case test
- Celebrate good ones: concurrent orders, midnight date boundary, unicode in item names

---

### 11:45-12:15 -- DEBRIEF 3: QA vs QC vs QE, Quality Mindset (30 min)

**This is where the "big picture" concepts land -- after they've DONE the work.**

1. **QA vs QC vs QE (15 min)**
   - "Everything you did today falls into one of three categories."
   - QA (Quality Assurance) = **Process, Preventive** -- the rules that prevent defects
     - "Writing a test plan (Activity 3) is QA. You're setting up a process."
     - Restaurant analogy: recipe standards, hygiene rules, chef training
   - QC (Quality Control) = **Product, Detective** -- finding defects in the product
     - "Running the buggy tests (Activity 1) is QC. You found defects."
     - Restaurant analogy: taste-testing each dish before serving
   - QE (Quality Engineering) = **System, Proactive** -- engineering quality at scale
     - "Building an automated test pipeline is QE. Quality is built into the system."
     - Restaurant analogy: automated temperature sensors, kitchen workflow optimization

   - Quick classification exercise (participants call out answers):
     - "Setting up a linting rule that blocks console.log" -- QA
     - "Running 50 test cases on checkout" -- QC
     - "Building a CI pipeline that runs tests on every PR" -- QE
     - "Code review with a checklist" -- QA
     - "Monitoring production error rates" -- QE
     - "Manually verifying a bug fix in staging" -- QC

2. **Quality Mindset for Sustain Engineers (10 min)**
   - Show the cost-of-defects table: $1 at requirements -> $1000+ in production
   - "You're sustain engineers. You inherit code with technical debt. Your job is:"
     1. Every bug fix gets a test (so it never comes back)
     2. Ask "How was this missed?" (improve the process)
     3. Check test coverage before changing code
     4. Prevention over detection -- shift left
   - "The bugs you found in Activity 1 (cart.test.js) -- those bugs in TESTS
     are arguably worse than bugs in code. Because they give you false confidence."

3. **Quality in Sustain vs Greenfield (5 min)**
   - Quick comparison:
     | Greenfield | Sustain |
     |-----------|---------|
     | Write tests from scratch | Add tests to untested code |
     | Known codebase | Unfamiliar, undocumented code |
     | Define quality upfront | Improve quality of inherited code |
   - "You will never have the luxury of 100% coverage on Day 1. Use risk-based testing to decide where to start."

---

### 12:15-12:30 -- Transition (15 min)
- Quick recap: "We've done 3 activities. What did we learn?"
- Cold call 3 participants for one takeaway each
- Prep for learning checkpoints

### 12:30-13:00 -- Learning Checkpoint 3 & 4 (30 min)
- Client-format pulse checks on prior modules
- Participants eat while completing

### 13:00-13:30 -- LUNCH

---

### 13:30-14:15 -- ACTIVITY 4: Write Real Jest Tests for FoodExpress (45 min)

**This is the hands-on coding activity that makes the day feel practical.**

#### The Challenge (on whiteboard):

```
CHALLENGE: Write 3 New Tests
=============================
Open: Labs/starter-code/test/cart.test.js

STEP 1: Fix all 4 bugs (10 min)
  - Fix the shared state bug (add beforeEach)
  - Fix toBe -> toEqual
  - Fix missing await
  - Fix the discount regression (percent/100)

STEP 2: Run tests -- all should PASS (2 min)
  $ npx jest

STEP 3: Write 3 NEW test cases (20 min)
  Pick any 3:
  a) Test getTotal with empty cart (should return 0)
  b) Test addItem with quantity 0 (what should happen?)
  c) Test removeItem for non-existent item (should not crash)
  d) Test applyDiscount with 0% (should return original total)
  e) Test applyDiscount with 100% (should return 0)
  f) Test applyDiscount with negative percent (what should happen?)
  g) Test fetchDeliveryFee for non-Bangalore pincode (should be 50)
  h) Test addItem then removeItem -- cart should be empty

STEP 4: Run tests -- all should PASS (3 min)

BONUS: Write a test that INTENTIONALLY fails. Then fix the code to make it pass.
This is TDD (Test-Driven Development) in action.
```

#### Walk around during this (15 min)
- Help participants who are stuck on Jest syntax
- Highlight good test cases to the class
- Common struggle: testing for exceptions (`expect(() => ...).toThrow()`)

#### Also fix order.test.js (10 min)
- Faster -- only 2 bugs
- Bug 1: wrap `function testCancelDeliveredOrderThrows()` in `test()`
- Bug 2: swap `expect(450).toBe(order.getTotal())` to `expect(order.getTotal()).toBe(450)`

#### Show-and-Tell (5 min)
- Ask 2 volunteers to share a test they wrote
- Highlight any creative edge cases

---

### 14:15-14:45 -- DEBRIEF 4: Automation, Non-Functional Testing, Tools (30 min)

**Now the theory lands because they've written real tests.**

1. **Automation Pyramid (10 min)**
   - "You just wrote unit tests. They run in milliseconds. They're cheap to write."
   - Draw the pyramid:
     ```
            /\        UI/E2E tests (10%)
           /  \       Slow, expensive, brittle
          /----\
         /      \     Integration tests (20%)
        /--------\    API tests, service tests
       /          \
      /            \  Unit tests (70%)
     /--------------\ Fast, cheap, reliable <-- YOU WERE HERE
     ```
   - Anti-pattern: The Ice Cream Cone (everything is manual/UI tests)
   - "FoodExpress has 0 tests today. If you could only write 10 tests, where would you put them?" (Answer: unit tests for payment and order total calculation)

2. **Non-Functional Testing Types (10 min)**
   - "We've been doing functional testing. But what about..."
   - Performance: "The app is slow" -- how do you prove it? Response time, throughput, P95/P99
   - Load: 1000 concurrent users ordering at lunch peak
   - Security: SQL injection in search, auth bypass (covered deeper in Module 27)
   - Show the Load Testing Progression: Baseline -> Load -> Stress -> Spike -> Soak
   - Key for sustain: "Your client will say 'it's slow'. You need NUMBERS, not feelings."

3. **Tools Map (5 min)**
   - Quick table -- focus only on tools they've already touched:
     | What | Tool | You Used It In |
     |------|------|----------------|
     | Unit tests (JS) | Jest | Today, Module 9-10 |
     | Unit tests (Java) | JUnit | Module 5-7 |
     | API testing | Postman/Supertest | Module 10 |
     | UI automation | Selenium/Cypress | Coming in capstone |
     | Performance | JMeter/k6 | Conceptual today |

4. **Shift-Left + Metrics (5 min)**
   - "Don't wait until the end to test. Test at every stage."
   - Key metrics their manager will ask about:
     - Test coverage > 80%
     - Defect leakage < 10%
     - Pass rate > 95%
     - MTTR (P1) < 4 hours

---

### 14:45-15:15 -- ACTIVITY 5: Automation Decision Matrix (30 min)

**Exercise 4 from lab-exercises.md** -- simplified, fast version.

> "FoodExpress has 200 test cases. Budget to automate 80 this quarter. Which ones?"

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

**Task (15 min):** Score each 1-3 on Frequency, Stability, Impact. Total = sum. Pick top categories adding up to ~80 tests.

**Class discussion (10 min):**
- Reveal answer: Login (15) + Order (40) + Payment (20) + Search partial (5) = 80
- Key insight: "Delivery tracking is HIGH frequency but LOW stability (GPS is flaky). Flaky automated tests are WORSE than no automation -- they erode trust."
- "Admin dashboard is stable but runs quarterly. Not worth automating yet."

**Quick callout (5 min):**
- "Manual testing isn't bad. Exploratory testing, usability testing, one-time tests -- those stay manual."
- "Automate what's repetitive, stable, and high-impact."

---

### 15:15-15:30 -- BREAK
*Send daily quiz questions to Chandana during this break.*

---

### 15:30-16:00 -- Assessment 5: MCQ + Coding (30 min)

- Covers: Database (yesterday) + QE/QC (today)
- Files: `assessments/02-module-mcq/mcq-05-database-qeqc.xlsx` + `assessments/03-coding/assessment-05/`
- Individual, timed, closed-book

---

### 16:00-17:00 -- QE/QC Role Play (60 min)

**Reference:** `Labs/role-play.md`

#### Setup (5 min)
- Form groups of 4 (27 participants = 6 groups of 4 + 1 group of 3)
- Hand out ROLE CARDS face down. Each person gets ONLY their role.
- Project the scenario card on screen.

#### Round 1: Test Plan Defense (25 min)

**Scenario:** FoodExpress launching Loyalty Rewards. QE Lead presents test plan. Others challenge.

| Role | Secret Agenda |
|------|--------------|
| **QE Lead** | Defend the 5-day test plan. Get sign-off. |
| **Developer** | "My unit tests are enough. Why do we need 5 days?" |
| **Product Owner** | "Competitor ships next week. Can we do 3 days?" |
| **Head of Operations** | "Last time a points bug gave 10x rewards. I need guarantees." |

**Your job as trainer:**
- Walk around, listen to 2-3 groups
- If a group finishes early or goes flat, inject a curveball:
  *"Breaking news: the dev just found that points calculation uses floating point. Rs 99.99 rounds differently on different systems."*

**Debrief (10 min):**
- "Which group got sign-off? What conditions were attached?"
- "Developer said unit tests are enough. QE Lead, how did you respond?"
  (Expected: unit tests test components in isolation, integration tests catch the gaps between them)
- "Product Owner pushed for 3 days. Is that ever acceptable?"
  (Expected: yes, if you descope regression to automated-only and cut edge cases to post-release)

#### Round 2: Production Bug Triage (25 min)

**Scenario:** Friday 4:30 PM. 8 bugs. Fix only 4 by Sunday. 16 hours of dev capacity.

| Role | Focus |
|------|-------|
| **QE Lead** | Facilitate triage. Drive to a decision in 15 min. |
| **Dev Lead** | Estimate effort. Push back on overcommitting. |
| **Product Owner** | Revenue impact. Food critic reviewing the app this weekend. |
| **Ops Lead** | Real-time monitoring data. 340 payment failures, 100% wrong ETA. |

Write the 8 bugs on whiteboard (from role-play.md):
```
B1: Payment failure > Rs 2000      (3 hrs, 340 failures, Rs 68K lost)
B2: ETA always shows 15 min        (4 hrs, affects ALL orders)
B3: Menu images broken (404)       (1 hr, 23 restaurants)
B4: Search results 40 min stale    (5 hrs, 2 restaurants show as open)
B5: Cart +/- button broken         (6 hrs, mobile only, has workaround)
B6: Email confirmation delayed     (2 hrs, no data loss)
B7: Rating not saving              (3 hrs, silent failure)
B8: Wrong restaurant name          (2 hrs, ~60 users)
```

**Debrief (10 min):**
- "Which 4 did your group pick? What's the total hours?"
- Expected best answer: B1 (3h) + B3 (1h) + B6 (2h) + B8 (2h) = 8 hours
  OR: B1 (3h) + B2 (4h) + B3 (1h) + B6 (2h) = 10 hours
- "Did anyone pick B5? Why/why not?" (6 hours is half your capacity for a bug with a workaround)
- "B2 affects 100% of users but no revenue loss. B1 affects fewer users but loses money. How did you weigh that?"
- "Did anyone recommend customer communication for deferred bugs?"

#### Wrap-up (5 min)
- "Quality is a team sport. The role play showed you that QE decisions involve business, engineering, AND operations."
- "As sustain engineers, you will sit in these triage meetings weekly. Today you practiced."
- Preview: "Tomorrow -- Infrastructure Fundamentals. We move from code quality to system quality."

---

## Preparation Checklist (Tonight)

### Must-Do
- [ ] Verify `npm install` and `npx jest` work in `Labs/starter-code/` on training room machines
- [ ] Print role play cards -- 4 separate cards per group, cut so each person sees ONLY their role
- [ ] Have `Labs/solutions/` test files ready but NOT shared until after Activity 4
- [ ] Load Assessment 5 files
- [ ] Prepare Learning Checkpoint 3 & 4 materials
- [ ] Draft 6-7 daily quiz questions for Chandana (due by 3 PM)

### Whiteboard Prep (draw before class)
- "SITUATION REPORT" for the opening
- Bug Triage table template (8 rows)
- Keep space for: Testing Pyramid, Defect Lifecycle, Severity/Priority matrix (draw during debriefs)

### Materials to Project
- `cart.test.js` (buggy) -- for Activity 1
- Exercise 2 bug list -- for Activity 2
- Test case template -- for Activity 3
- Automation matrix table -- for Activity 5

---

## Why This Approach Works

| Traditional QE/QC Teaching | This Activity-First Approach |
|---------------------------|------------------------------|
| Slides first, exercises later | Exercises first, theory labels what they experienced |
| "QA means Quality Assurance..." | "You just found 6 bugs. The process of finding them? That's QC." |
| Severity vs Priority definitions | "You just argued about which bugs to fix. That argument IS severity vs priority." |
| "Write test cases" (cold) | "340 customers were double-charged. Write test cases so it never happens again." (urgent) |
| Role play feels like homework | Role play is the climax -- they have ALL the vocabulary and experience by then |

**The key insight:** By the time you show a slide, participants should already KNOW the concept from experience. The slide just gives it a name.

---

## Timing Safety Valves

If running **behind:**
- Activity 5 (Automation Matrix) can be cut -- cover verbally in 5 min
- Debrief 3 (QA/QC/QE) can be shortened to 15 min -- they'll get it fast after 3 activities

If running **ahead:**
- Extend Activity 4: participants also fix `order.test.js` and write 2 more tests
- Add Exercise 3 (Test Strategy Document) as a 20-min bonus
- Calculate defect density: FoodExpress has 50,000 LOC and 38 bugs. Is 0.76/KLOC acceptable? (Yes, industry average is 1-5/KLOC)

---

## Key Phrases to Use Throughout the Day

| Moment | Say This |
|--------|----------|
| When a participant finds a bug in tests | "This is QC -- you just found a defect in the product" |
| When discussing what tests to write | "This is QA -- you're creating a process to prevent defects" |
| When they automate tests | "This is QE -- you're engineering quality into the system" |
| When they argue about priority | "This is exactly what happens in a real triage meeting" |
| When a test passes that shouldn't | "False positive. The most dangerous kind of bug." |
| When they ask "is this the right answer?" | "In QE, the answer depends on business context. Defend your reasoning." |
| After fixing the discount bug | "You just prevented Rs 68,000 in lost revenue. That's the value of testing." |
