# Module 13 Solutions -- TRAINER ONLY

## Exercise 1: Sample Test Cases (Order Placement)

| TC ID | Category | Scenario | Expected Result | Priority |
|-------|----------|----------|-----------------|----------|
| TC-01 | Positive | Place order with 3 items, COD payment | Order created, confirmation shown | P1 |
| TC-02 | Positive | Place order Rs 500+ | Free delivery (Rs 0 delivery fee) | P1 |
| TC-03 | Positive | Place order Rs 499 | Delivery fee Rs 30 applied | P1 |
| TC-04 | Boundary | Place order exactly Rs 99 | Order accepted (minimum met) | P1 |
| TC-05 | Boundary | Place order Rs 98 | Error: "Minimum order Rs 99" | P1 |
| TC-06 | Boundary | Add exactly 20 items | Order accepted | P2 |
| TC-07 | Boundary | Add 21st item | Error: "Maximum 20 items" | P2 |
| TC-08 | Boundary | Place order exactly Rs 500 | Free delivery | P2 |
| TC-09 | Negative | Place order with empty cart | Error: "Cart is empty" | P1 |
| TC-10 | Negative | Order from closed restaurant | Error: "Restaurant is closed" | P1 |
| TC-11 | Negative | Invalid credit card number | Error: "Payment failed" | P1 |
| TC-12 | Negative | Order with network timeout | Error shown, order not double-created | P2 |
| TC-13 | Edge | Place order at midnight (date change) | Correct date on order | P3 |
| TC-14 | Edge | Two users order last item simultaneously | One succeeds, one gets "item unavailable" | P2 |
| TC-15 | Non-func | Place order under load (100 concurrent) | All orders complete < 2 seconds | P2 |

## Exercise 2: Bug Triage Answers

| # | Severity | Priority | Fix This Sprint? | Justification |
|---|----------|----------|-----------------|---------------|
| 1 | Critical | P1 | YES | Financial impact, legal liability, affects 2% of all orders |
| 2 | Major | P2 | YES | Misleading UX, customer tries to order from closed restaurant |
| 3 | Minor | P3 | No | Approximate location still useful; GPS accuracy is external dependency |
| 4 | Major | P2 | No | Affects specific OS version; workaround: check email for confirmation |
| 5 | Major | P2 | YES | Affects all power users; simple fix (add pagination) |
| 6 | Critical | P1 | YES | Financial loss per use; easy fix but high impact |
| 7 | Minor | P3 | No | Low frequency, cosmetic after first review; auto-corrects on second review |
| 8 | Trivial | P4 | No | Single device/orientation; cosmetic only |

**Selected 4:** #1 (double charge), #6 (promo code), #5 (order history), #2 (closed restaurants)

**Rationale:** #1 and #6 are financial impact bugs (must fix). #5 affects all power users and is a simple pagination fix. #2 is a data integrity issue leading to failed orders.

### Which testing would have caught each bug?

| Bug | Testing Type That Would Catch It |
|-----|----------------------------------|
| #1 | Integration testing (payment + order service) |
| #2 | Functional testing (search filters) |
| #3 | Non-functional testing (GPS accuracy validation) |
| #4 | Compatibility testing (Android 14 testing) |
| #5 | Performance testing (load test with large datasets) |
| #6 | Unit testing (discount calculation logic) |
| #7 | Unit testing (average calculation edge case) |
| #8 | Compatibility testing (tablet responsive testing) |

## Exercise 3: Test Strategy Key Points

**Scope:**
- In scope: Loyalty Points, Scheduled Orders, 5 bug fixes, pagination
- Out of scope: Existing stable features (unless regression risk)

**Entry Criteria:**
- All features code-complete and deployed to staging
- Unit tests passing with > 80% coverage
- No Critical or Major bugs open from previous release

**Exit Criteria:**
- All P1 test cases passing
- > 95% overall pass rate
- No open Critical bugs, < 3 open Major bugs
- Performance: API response < 200ms P95

## Exercise 4: Automation Priority

| Category | Frequency | Stability | Impact | Score | Automate? |
|----------|-----------|-----------|--------|-------|-----------|
| Login/Auth | 3 | 3 | 3 | 9 | YES (15) |
| Order Placement | 3 | 2 | 3 | 8 | YES (40) |
| Payment | 3 | 2 | 3 | 8 | YES (20) |
| Restaurant Search | 3 | 3 | 2 | 8 | Partial (5 of 25) |
| Delivery Tracking | 3 | 1 | 2 | 6 | NO (flaky) |
| Notifications | 3 | 1 | 1 | 5 | NO (device-dependent) |
| User Profile | 1 | 3 | 1 | 5 | NO (low frequency) |
| Admin Dashboard | 1 | 3 | 1 | 5 | NO (low frequency) |
| Reports | 1 | 2 | 2 | 5 | NO (low frequency) |

**Automated: 80 tests** = Login (15) + Order (40) + Payment (20) + Search (5)

## Hints

| Exercise | Level 1 | Level 2 |
|----------|---------|---------|
| #1 | "Think about boundary values: what are the limits?" | "Test at Rs 98, Rs 99, Rs 100, Rs 499, Rs 500, Rs 501, 19 items, 20, 21" |
| #2 | "Which bugs cause financial loss?" | "Double charge and promo code bug are both P1 -- financial impact" |
| #3 | "What must be true BEFORE testing and AFTER testing?" | "Entry: code complete + unit tests. Exit: > 95% pass rate + no criticals" |
| #4 | "High frequency + high stability + high impact = automate first" | "Login, Order, Payment are the top 3 categories to automate" |
