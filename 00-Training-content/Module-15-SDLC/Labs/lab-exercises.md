# Module 15: SDLC Fundamentals -- Exercises

## Lab Overview

These exercises build practical understanding of SDLC concepts through FoodExpress scenarios. You will write requirement documents, compare methodologies, design environment strategies, and map sustain work to SDLC stages.

> "Hi Team, FoodExpress is onboarding new sustain engineers and they need to understand our development process end-to-end. We use Scrum for feature work, Kanban for sustain work, and DevOps for delivery. Complete these exercises so you can effectively participate in sprint planning, write clear requirements, and understand our environment pipeline."

---

## Exercise 1: Requirements Documentation (45 min)

### Scenario
FoodExpress is adding a **Scheduled Orders** feature. Customers can schedule an order for a future date/time (e.g., order at 10 AM for 7 PM dinner delivery).

### Tasks

**Task 1A: Write 5 User Stories** in the format:
```
As a [role], I want to [action], so that [benefit].
Acceptance Criteria:
- Given [context], when [action], then [result]
```

Suggested stories:
1. Schedule an order for a future time
2. Edit a scheduled order before it is processed
3. Cancel a scheduled order
4. Receive a reminder before the scheduled order is processed
5. View all scheduled orders

**Task 1B: Write an SRS excerpt** for the "Schedule Order" feature:
- Functional requirement (FR-XXX format)
- Input, Process, Output
- Error cases (at least 3)
- Non-functional requirements (performance, reliability)

**Task 1C: Create a Requirements Traceability Matrix (RTM)**

| Req ID | Requirement | Test Case ID | Status |
|--------|-------------|-------------|--------|
| FR-101 | Schedule order for future time | TC-201, TC-202 | ? |

---

## Exercise 2: Methodology Selection (30 min)

### Scenario
For each FoodExpress project below, recommend the best SDLC methodology and justify your choice.

| Project | Description | Duration | Requirements | Your Recommendation |
|---------|-------------|----------|-------------|-------------------|
| A | Build new loyalty program from scratch | 3 months | Evolving, PO available | ? |
| B | Migrate database from MySQL to PostgreSQL | 6 weeks | Fixed, well-defined | ? |
| C | Ongoing production support and bug fixes | Ongoing | Ad-hoc, unpredictable | ? |
| D | Build payment gateway integration with bank | 4 months | Fixed by regulation | ? |
| E | Experimental AI-based restaurant recommendation | 2 months | Unknown, research | ? |
| F | Full platform rewrite to microservices | 12 months | Complex, evolving | ? |

### For each recommendation, answer:
1. Which methodology (Waterfall, Scrum, Kanban, DevOps, Spiral)?
2. Why is this the best fit?
3. What is the risk of using the wrong methodology?

---

## Exercise 3: Environment Strategy Design (30 min)

### Scenario
FoodExpress currently has only 2 environments: Local and Production. This has caused 3 production incidents in the past month from untested deployments.

### Tasks

**Task 3A:** Design a proper environment pipeline for FoodExpress. For each environment, specify:

| Environment | Purpose | Who Uses It | Data Source | Deploy Method | Monitoring |
|-------------|---------|-------------|-------------|---------------|------------|
| Local | ? | ? | ? | ? | ? |
| Dev | ? | ? | ? | ? | ? |
| QA/Staging | ? | ? | ? | ? | ? |
| Pre-Prod | ? | ? | ? | ? | ? |
| Production | ? | ? | ? | ? | ? |

**Task 3B:** Define environment variables that differ between environments:

| Variable | Local | Dev | Staging | Production |
|----------|-------|-----|---------|------------|
| DB_HOST | ? | ? | ? | ? |
| LOG_LEVEL | ? | ? | ? | ? |
| API_URL | ? | ? | ? | ? |
| FEATURE_LOYALTY | ? | ? | ? | ? |

**Task 3C:** Write 3 rules for promoting code between environments.

---

## Exercise 4: STLC Application (30 min)

### Scenario
FoodExpress is releasing v2.4 with 2 new features (Loyalty Points + Scheduled Orders) and 5 bug fixes. Apply the STLC stages.

### Tasks

**Task 4A: Requirement Analysis**
- List 5 testable requirements from the features above
- Create a Requirements Traceability Matrix

**Task 4B: Test Planning**
- Define scope (in-scope vs out-of-scope)
- List test types to be performed
- Define entry and exit criteria
- Estimate testing timeline

**Task 4C: Test Case Design**
- Write 5 test cases for Loyalty Points
- Write 5 test cases for Scheduled Orders
- Include boundary values and negative cases

**Task 4D: Test Closure**
- Define 5 metrics you would include in the test summary report
- Write a sample test summary with made-up (but realistic) numbers

---

## Exercise 5: Change Management Simulation (30 min)

### Scenario
You need to deploy a bug fix (FOOD-156: incorrect tax calculation) to production.

### Tasks

**Task 5A:** Fill out a Change Request Form:

| Field | Your Answer |
|-------|-------------|
| Change ID | FOOD-CR-??? |
| Title | ? |
| Description | ? |
| Type (Standard/Normal/Emergency) | ? |
| Requester | ? |
| Impact Assessment | ? |
| Risk Level | ? |
| Affected Services | ? |
| Rollback Plan | ? |
| Testing Evidence | ? |
| Deploy Window | ? |

**Task 5B:** For each change type below, specify the appropriate process:

| Change Type | Example | Approval Needed? | Testing Required? | Deploy Window |
|-------------|---------|------------------|-------------------|---------------|
| Standard | Restart a service | ? | ? | ? |
| Normal | Deploy bug fix | ? | ? | ? |
| Emergency | Critical security patch | ? | ? | ? |

**Task 5C:** What could go wrong with this deployment? List 3 risks and their mitigations.

---

## Checkpoints

### Checkpoint 1 (Morning)
- [ ] Exercise 1: 5 user stories with acceptance criteria written
- [ ] Exercise 1: SRS excerpt completed with error cases
- [ ] Exercise 2: All 6 projects have methodology recommendations with justification

### Checkpoint 2 (Afternoon)
- [ ] Exercise 3: Environment pipeline designed with all 5 environments
- [ ] Exercise 4: STLC applied to FoodExpress v2.4 release
- [ ] Exercise 5: Change request form completed
- [ ] All exercises peer-reviewed

---

## Bonus Challenges

1. **Compare DORA metrics** -- Research the DORA metrics and estimate where FoodExpress currently stands (deployment frequency, lead time, MTTR, change failure rate). What would it take to move from "Medium" to "High" performance?

2. **Write a Definition of Done** -- Create a comprehensive Definition of Done (DoD) checklist for FoodExpress user stories. Include code, testing, documentation, and deployment criteria.

3. **Sprint Planning simulation** -- Given a team velocity of 40 story points, select stories from the FoodExpress backlog for a 2-week sprint. Justify your selection.

4. **Incident to change** -- Write the full lifecycle from a production incident (order totals wrong) through incident management, root cause analysis, change request, deployment, and post-implementation review.

5. **Architecture Decision Record (ADR)** -- Write an ADR for FoodExpress's decision to move from monolith to microservices. Include context, decision, consequences.
