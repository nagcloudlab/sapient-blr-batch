# Module 15 Solutions -- TRAINER ONLY

## Exercise 1: Sample User Stories

### Story 1: Schedule an Order
```
As a customer,
I want to schedule a food order for a future date and time,
So that I can plan my meals in advance.

Acceptance Criteria:
- Given I am on the checkout page, when I select "Schedule for later" and pick a date/time at least 1 hour in the future, then my order is saved with status "scheduled"
- Given I pick a time less than 30 minutes from now, then I see an error "Schedule time must be at least 30 minutes from now"
- Given I pick a date more than 7 days in the future, then I see an error "Cannot schedule more than 7 days ahead"
```

### Story 2: Edit a Scheduled Order
```
As a customer,
I want to edit my scheduled order before it is processed,
So that I can change items or delivery details.

Acceptance Criteria:
- Given I have a scheduled order with status "scheduled", when I click "Edit", then I can modify items and delivery address
- Given my scheduled order is being prepared (status "processing"), when I try to edit, then I see "Order is already being prepared and cannot be edited"
```

### SRS Excerpt

```
FR-101: Schedule Order for Future Time
  Description: Allow customers to place orders for future delivery
  Input: customer_id, restaurant_id, items[], scheduled_datetime, payment_method
  Process:
    1. Validate scheduled_datetime is 30+ minutes in the future and within 7 days
    2. Validate restaurant will be open at scheduled time
    3. Reserve payment authorization (do not charge yet)
    4. Create order with status "scheduled"
    5. Create scheduler job to process order 30 min before scheduled time
    6. Send confirmation with scheduled details
  Output: order_id, scheduled_datetime, estimated_preparation_start
  Error Cases:
    - E1: scheduled_datetime < now + 30 min -> 400 "Too soon to schedule"
    - E2: scheduled_datetime > now + 7 days -> 400 "Cannot schedule more than 7 days ahead"
    - E3: Restaurant closed at scheduled time -> 400 "Restaurant not available at scheduled time"
    - E4: Payment authorization fails -> 402 "Payment authorization failed"
  Non-Functional:
    - NF1: Schedule creation < 3 seconds
    - NF2: Scheduler job must fire within 1 minute of target time
    - NF3: System must handle 1000 concurrent schedule requests
```

## Exercise 2: Methodology Recommendations

| Project | Methodology | Justification |
|---------|-------------|---------------|
| A (Loyalty program) | **Scrum** | Evolving requirements, PO available for feedback, 3-month timeline fits 6 sprints |
| B (DB migration) | **Waterfall** | Fixed, well-defined scope; sequential steps (schema, data, testing, cutover) |
| C (Production support) | **Kanban** | Ongoing, unpredictable work; continuous flow; WIP limits prevent overload |
| D (Payment gateway) | **Waterfall or V-Model** | Regulated, fixed requirements by bank; V-Model pairs each phase with testing |
| E (AI recommendation) | **Spiral** | High uncertainty, research-oriented; spiral's risk-driven iterations fit exploration |
| F (Platform rewrite) | **Scrum (SAFe)** | Large, complex, evolving; needs scaled agile with multiple teams coordinating |

## Exercise 3: Environment Strategy

| Environment | Purpose | Who Uses It | Data Source | Deploy Method | Monitoring |
|-------------|---------|-------------|-------------|---------------|------------|
| Local | Development, debugging | Individual developer | Mock/seed data | Manual | Console logs |
| Dev | Integration testing | Dev team | Synthetic test data | Auto (CI on merge) | Basic logging |
| QA/Staging | Full testing, regression | QA team | Anonymized prod subset | Auto (CD pipeline) | Full monitoring |
| Pre-Prod | Final validation, UAT | PO, stakeholders | Anonymized prod copy | Manual approval gate | Full + alerting |
| Production | Live users | Everyone | Real customer data | Approved deployment | Full + alerting + on-call |

### Environment Variables

| Variable | Local | Dev | Staging | Production |
|----------|-------|-----|---------|------------|
| DB_HOST | localhost | dev-db.internal | stg-db.internal | prod-db.internal |
| LOG_LEVEL | debug | debug | info | warn |
| API_URL | http://localhost:3000 | https://dev-api.foodexpress.com | https://stg-api.foodexpress.com | https://api.foodexpress.com |
| FEATURE_LOYALTY | true | true | true | false (behind flag) |

### Promotion Rules
1. Code ONLY moves forward (Local -> Dev -> Staging -> Prod), never backward
2. Each environment requires all automated tests to pass before promotion
3. Production deployments require CAB approval and a rollback plan

## Exercise 4: STLC for v2.4

### Test Plan Summary
- **Scope:** Loyalty Points, Scheduled Orders, 5 bug fixes, pagination
- **Out of scope:** Existing stable features not touched by this release
- **Test types:** Unit (developers), Integration (QA), E2E (QA), Performance (load test), Security scan
- **Entry criteria:** All features code-complete, unit tests passing, deployed to staging
- **Exit criteria:** 95%+ pass rate, no Critical bugs, < 3 Major bugs, performance within targets
- **Timeline:** 3 days (Day 1: smoke + integration, Day 2: regression + performance, Day 3: UAT + sign-off)

### Test Summary (Sample)

| Metric | Value |
|--------|-------|
| Total test cases | 85 |
| Executed | 82 |
| Passed | 78 |
| Failed | 4 |
| Blocked | 3 |
| Pass rate | 95.1% |
| Critical bugs found | 0 |
| Major bugs found | 2 |
| Minor bugs found | 5 |
| Test coverage | 84% |

## Exercise 5: Change Request

| Field | Answer |
|-------|--------|
| Change ID | FOOD-CR-042 |
| Title | Fix incorrect tax calculation in order service |
| Description | Tax is being calculated on the post-discount amount instead of pre-discount amount per regulatory requirements |
| Type | Normal |
| Requester | Sustain Engineering Team |
| Impact | Order Service, Payment Service; all new orders will have corrected tax |
| Risk Level | Medium (changes revenue calculation) |
| Affected Services | order-service, payment-service |
| Rollback Plan | Revert to Docker image tag v2.3.5; affected orders can be manually corrected |
| Testing Evidence | 15 unit tests passing, staging verification with 50 test orders, finance team approved calculation |
| Deploy Window | Saturday 02:00-04:00 AM (low traffic) |

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| New tax calculation has edge case bugs | Incorrect charges | Test with 50 edge case scenarios on staging |
| Rollback needed mid-deployment | Service unavailable for 5-10 min | Blue-green deployment; instant rollback |
| Historical orders show different tax | Customer confusion | Add note in order history: "Tax recalculated per regulation" |

## Hints

| Exercise | Level 1 | Level 2 |
|----------|---------|---------|
| #1 | "Follow the As/I want/So that format strictly" | "Acceptance criteria should be testable: Given/When/Then" |
| #2 | "Match the methodology to the nature of requirements" | "Fixed reqs = Waterfall; evolving = Scrum; ongoing = Kanban" |
| #3 | "Each environment needs a clear purpose and audience" | "Data should never flow from lower to higher environments" |
| #4 | "Entry criteria = what must be ready before testing" | "Exit criteria = what must be achieved before release" |
| #5 | "Always include a rollback plan" | "Deploy window should be during low-traffic periods" |
