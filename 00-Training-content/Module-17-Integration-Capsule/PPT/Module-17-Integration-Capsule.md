# Integration Capsule Project
## Module 17 | Sustain Engineering Training | Day 18

---

## Agenda

| # | Topic |
|---|-------|
| 01 | Project briefing & team formation |
| 02 | Architecture walkthrough |
| 03 | Integration points deep dive |
| 04 | Sprint 1: Bug triage & cross-stack fixes |
| 05 | Lunch |
| 06 | Sprint 2: Feature integration & testing |
| 07 | Sprint 3: Polish & documentation |
| 08 | Team presentations & retrospective |

> Full-day hands-on project integrating Modules 1-16

---

## Why an Integration Capsule?

- Real sustain engineering work spans **multiple layers**
- A single Jira ticket often touches frontend, backend, and database
- Teams must collaborate across technology stacks
- This capsule simulates a **real production incident sprint**

**FoodExpress scenario:** The production system has several cross-stack bugs reported by customers. Your team must triage, fix, and verify all issues within a single sprint day.

---

## FoodExpress Architecture Overview

```
                    +------------------+
                    |   Browser/App    |
                    |  (HTML/CSS/JS)   |
                    +--------+---------+
                             |
                    +--------+---------+
                    |   Frontend       |
                    |   (JavaScript)   |
                    +--------+---------+
                             |
                +------------+------------+
                |                         |
       +--------+--------+     +---------+--------+
       |  Java Backend   |     |  Node.js Backend  |
       |  (Order Service)|     |  (Menu Service)   |
       +--------+--------+     +---------+--------+
                |                         |
                +------------+------------+
                             |
                    +--------+---------+
                    |    Database       |
                    |   (MySQL/SQL)     |
                    +------------------+
```

---

## System Components

| Component | Technology | Responsibility |
|-----------|-----------|----------------|
| Menu Page | HTML/CSS/JS | Display menu, add to cart |
| Order Page | HTML/CSS/JS | Checkout flow, payment form |
| Order Service | Java (Spring) | Process orders, calculate totals |
| Menu Service | Node.js (Express) | Serve menu items, search, filter |
| Database | MySQL | Store menu items, orders, users |
| Tests | JUnit + Jest | Unit and integration tests |

---

## Integration Points

### Frontend <-> Backend

```javascript
// Frontend: Fetching menu items
fetch('/api/menu/items')
  .then(response => response.json())
  .then(items => renderMenu(items));

// Frontend: Placing an order
fetch('/api/orders', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(orderData)
});
```

Key concerns: **data format consistency**, **error handling**, **status codes**

---

## Integration Points

### Backend <-> Database

```java
// Java Order Service: Saving an order
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByCustomerIdOrderByCreatedAtDesc(Long customerId);

    @Query("SELECT o FROM Order o WHERE o.status = :status")
    List<Order> findByStatus(@Param("status") String status);
}
```

```javascript
// Node.js Menu Service: Querying menu
const getMenuItems = async (category) => {
  const query = 'SELECT * FROM menu_items WHERE category = ? AND active = 1';
  return await db.execute(query, [category]);
};
```

---

## Integration Points

### Service <-> Service

```java
// Java calling Node.js Menu Service
@Service
public class MenuClient {
    private final RestTemplate restTemplate;

    public List<MenuItem> getAvailableItems() {
        ResponseEntity<MenuItem[]> response = restTemplate.getForEntity(
            "http://menu-service:3000/api/menu/items",
            MenuItem[].class
        );
        return Arrays.asList(response.getBody());
    }
}
```

Key concerns: **timeout handling**, **circuit breakers**, **data serialization**

---

## Common Cross-Stack Bug Categories

| Category | Example | Layers Affected |
|----------|---------|-----------------|
| Data type mismatch | Price as string vs number | Frontend + Backend |
| Missing error handling | Unhandled 500 from API | Frontend + Backend |
| SQL injection | Unsanitized user input | Backend + Database |
| Schema mismatch | Column renamed in DB | Backend + Database |
| CORS issues | Missing headers | Frontend + Backend |
| Encoding problems | Special chars in menu names | All layers |

---

## Team Structure

### Recommended Team Composition (3-4 members)

| Role | Responsibility |
|------|---------------|
| **Frontend Lead** | HTML/CSS/JS bug fixes, UI testing |
| **Backend Lead** | Java/Node.js service fixes |
| **Database Lead** | SQL queries, schema fixes |
| **QE/Integration** | Test cases, verification, JIRA updates |

- Rotate roles if team has fewer members
- All members should review cross-stack issues together

---

## Sprint Workflow

```
 JIRA Board (Kanban)
 ┌──────────┬──────────┬──────────┬──────────┐
 │ BACKLOG  │ IN PROG  │ REVIEW   │   DONE   │
 ├──────────┼──────────┼──────────┼──────────┤
 │ BUG-001  │          │          │          │
 │ BUG-002  │          │          │          │
 │ BUG-003  │          │          │          │
 │ BUG-004  │          │          │          │
 │ FEAT-001 │          │          │          │
 └──────────┴──────────┴──────────┴──────────┘
```

- Move tickets as you work
- Add comments with root cause analysis
- Link related tickets across stacks

---

## Bug Ticket Format

### Standard Jira Bug Ticket

```
Title: [FE-001] Menu prices display NaN on checkout page
Priority: P1 - Critical
Reporter: Customer Support
Environment: Production

Description:
When customers add items with special pricing (combo meals)
to cart, the checkout page shows "NaN" instead of the total.

Steps to Reproduce:
1. Navigate to Menu page
2. Add "Family Combo" to cart
3. Click "Checkout"
4. Observe total price shows "NaN"

Expected: Total should show ₹599.00
Actual: Total shows "NaN"

Affected Component: Frontend (checkout.js)
Linked: May be related to BE-002 (price format change)
```

---

## Cross-Stack Bug #1: Price Display Issue

### Symptom
Menu prices show as "NaN" on the checkout page for combo meals

### Root Cause Analysis Path

1. **Frontend (checkout.js):** `parseFloat(item.price)` returns NaN
2. **Backend (Java):** OrderService returns price as `"₹599.00"` (string with currency symbol)
3. **Database:** `price` column stores `DECIMAL(10,2)` correctly

### Fix Required
- **Backend:** Return raw numeric price, add separate `currency` field
- **Frontend:** Handle both formats gracefully with fallback parsing

---

## Cross-Stack Bug #2: Search Returns Empty

### Symptom
Searching for menu items with special characters returns empty results

### Root Cause Analysis Path

1. **Frontend (menu.js):** Search query sent without URL encoding
2. **Backend (Node.js):** `req.query.search` received as garbled text
3. **Database:** `LIKE` query with unescaped characters fails silently

```javascript
// BUG: No encoding
fetch(`/api/menu/search?q=${searchTerm}`);

// FIX: Proper encoding
fetch(`/api/menu/search?q=${encodeURIComponent(searchTerm)}`);
```

---

## Cross-Stack Bug #3: Order History Missing

### Symptom
Customer order history shows only the latest order, not all past orders

### Root Cause Analysis Path

1. **Frontend (orders.js):** Renders only `response.data[0]` instead of iterating
2. **Backend (Java):** `findByCustomerId` missing `ORDER BY` clause
3. **Database:** Missing index on `customer_id` column causes timeout on large datasets

```sql
-- BUG: Missing index causes slow query
SELECT * FROM orders WHERE customer_id = 42;

-- FIX: Add index
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

---

## Cross-Stack Bug #4: Rating Submission Fails

### Symptom
Submitting a restaurant rating returns 500 Internal Server Error

### Root Cause Analysis Path

1. **Frontend (rating.js):** Sends `rating` as string `"4.5"` instead of number
2. **Backend (Java):** `Integer.parseInt("4.5")` throws NumberFormatException
3. **Database:** `rating` column is `TINYINT` (cannot store decimals)

### Fix Required
- **Frontend:** Send integer rating (1-5 scale)
- **Backend:** Validate and parse with `Double.parseDouble()`, then round
- **Database:** Alter column to `DECIMAL(2,1)` or enforce integer constraint

---

## Acceptance Criteria

### Definition of Done for Each Bug

| Criteria | Description |
|----------|-------------|
| Root Cause | Written root cause analysis in Jira comment |
| Code Fix | Fix applied to all affected layers |
| Unit Tests | At least 1 test per layer for the fix |
| Integration Test | End-to-end test proving the fix works |
| No Regression | Existing tests still pass |
| Peer Review | At least 1 teammate reviewed the fix |
| Documentation | Brief note on what changed and why |

---

## Quality Expectations

### Code Quality Checklist

- [ ] No hardcoded values (use constants/config)
- [ ] Error handling on all API calls
- [ ] Input validation on both client and server
- [ ] SQL queries use parameterized statements
- [ ] No console.log/System.out.println in production code
- [ ] Code follows existing naming conventions
- [ ] Comments explain "why", not "what"

---

## Testing Strategy

### Test Pyramid for FoodExpress

```
        /\
       /  \       E2E Tests (1-2 per bug)
      /    \      - Full flow: UI -> API -> DB
     /------\
    /        \    Integration Tests (2-3 per bug)
   /          \   - API contract tests
  /            \  - DB query tests
 /--------------\
/                \ Unit Tests (3-5 per bug)
/                  \ - Function-level tests
/                    \ - Edge cases
```

---

## Testing Examples

### Unit Test (JavaScript)

```javascript
describe('Price Formatter', () => {
  test('should handle numeric price', () => {
    expect(formatPrice(599.00)).toBe('₹599.00');
  });

  test('should handle string price with currency', () => {
    expect(formatPrice('₹599.00')).toBe('₹599.00');
  });

  test('should return 0 for invalid input', () => {
    expect(formatPrice('invalid')).toBe('₹0.00');
  });
});
```

---

## Testing Examples

### Unit Test (Java)

```java
@Test
void shouldCalculateOrderTotal() {
    List<OrderItem> items = Arrays.asList(
        new OrderItem("Burger", 2, new BigDecimal("199.00")),
        new OrderItem("Fries", 1, new BigDecimal("99.00"))
    );

    Order order = new Order(items);

    assertEquals(new BigDecimal("497.00"), order.getTotal());
}

@Test
void shouldHandleEmptyOrder() {
    Order order = new Order(Collections.emptyList());
    assertEquals(BigDecimal.ZERO, order.getTotal());
}
```

---

## Testing Examples

### Integration Test (SQL)

```sql
-- Test: Order history returns all orders for a customer
-- Setup
INSERT INTO orders (customer_id, total, status, created_at) VALUES
(42, 599.00, 'DELIVERED', '2026-07-01'),
(42, 299.00, 'DELIVERED', '2026-07-15'),
(42, 450.00, 'IN_PROGRESS', '2026-07-20');

-- Verify: Should return 3 rows ordered by date desc
SELECT COUNT(*) FROM orders WHERE customer_id = 42;
-- Expected: 3

SELECT * FROM orders
WHERE customer_id = 42
ORDER BY created_at DESC;
-- First row should be the July 20 order
```

---

## SDLC Integration

### Mapping to SDLC Phases

| Phase | Activity in This Capsule |
|-------|-------------------------|
| **Analysis** | Read bug tickets, understand requirements |
| **Design** | Plan fix across layers, discuss with team |
| **Implementation** | Write code fixes |
| **Testing** | Run unit + integration tests |
| **Review** | Peer code review |
| **Deployment** | Verify fix in running application |
| **Documentation** | Update Jira, write RCA |

---

## JIRA Workflow for Today

### Bug Lifecycle

```
Open -> In Progress -> Code Review -> Testing -> Done
  |                       |              |
  v                       v              v
 Won't Fix           Changes Needed   Reopened
```

### Required JIRA Fields
- **Summary:** Clear, concise bug title
- **Description:** Steps to reproduce
- **Priority:** P1 (Critical) to P4 (Minor)
- **Assignee:** Team member responsible
- **Labels:** `frontend`, `backend`, `database`, `cross-stack`
- **Story Points:** Estimated effort

---

## Sprint Planning

### Prioritization Matrix

| Bug | Impact | Effort | Priority |
|-----|--------|--------|----------|
| Price NaN (#1) | High - Revenue | Medium | P1 |
| Search Empty (#2) | Medium - UX | Low | P2 |
| Order History (#3) | Medium - UX | Medium | P2 |
| Rating 500 (#4) | Low - Feature | High | P3 |

**Sprint Goal:** Fix all P1 and P2 bugs, attempt P3 if time permits

---

## Root Cause Analysis (RCA) Template

### 5 Whys Example

```
Bug: Menu prices show NaN

1. Why? → parseFloat returns NaN
2. Why? → Input string contains currency symbol "₹"
3. Why? → Backend started sending formatted price
4. Why? → A recent backend change added currency formatting
5. Why? → No API contract was documented between frontend and backend

Root Cause: Missing API contract documentation
Preventive Action: Add API schema validation (OpenAPI/Swagger)
```

---

## Collaboration Best Practices

### Communication During the Sprint

- **Stand-up (every 2 hours):** Quick sync on progress
- **Pair programming:** For cross-stack bugs, pair frontend + backend devs
- **Slack/Teams channel:** Quick questions and blockers
- **Shared screen:** When debugging integration issues

### Git Workflow

```bash
# Feature branch per bug
git checkout -b fix/FE-001-price-nan
# Commit with ticket reference
git commit -m "FE-001: Fix price parsing to handle currency prefix"
# Pull request with cross-reference
git push origin fix/FE-001-price-nan
```

---

## Debugging Strategies

### Cross-Stack Debugging

| Layer | Tool | Command/Action |
|-------|------|---------------|
| Frontend | Browser DevTools | Network tab, Console |
| Node.js | Debug logs | `console.log(req.body)` |
| Java | IDE Debugger | Breakpoints in IntelliJ |
| Database | SQL Client | Run queries manually |
| API | Postman/curl | Test endpoints directly |

```bash
# Quick API test
curl -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customerId": 42, "items": [{"id": 1, "qty": 2}]}'
```

---

## Presentation Guidelines

### Final Team Presentation (15 min/team)

| Section | Duration | Content |
|---------|----------|---------|
| Overview | 2 min | Bugs assigned, team roles |
| Demo | 5 min | Before/after of each fix |
| RCA | 3 min | Root cause analysis for hardest bug |
| Learnings | 3 min | What you learned about cross-stack debugging |
| Q&A | 2 min | Questions from other teams |

---

## Presentation Scoring Rubric

| Criteria | Points | Description |
|----------|--------|-------------|
| Bug Fixes | 30 | All bugs fixed correctly |
| Test Coverage | 20 | Unit + integration tests written |
| RCA Quality | 15 | Deep root cause, not surface-level |
| Code Quality | 15 | Clean, readable, well-structured |
| JIRA Updates | 10 | Tickets updated, comments added |
| Presentation | 10 | Clear, organized, time-managed |
| **Total** | **100** | |

---

## Common Mistakes to Avoid

| Mistake | Better Approach |
|---------|----------------|
| Fixing symptoms, not root cause | Trace the bug across all layers |
| Not testing edge cases | What about null, empty, negative? |
| Hardcoding fixes | Use configuration and constants |
| Skipping code review | Fresh eyes catch issues you miss |
| Not updating JIRA | Document everything for future reference |
| Working in silos | Cross-stack bugs need collaboration |

---

## Retrospective Questions

At the end of the day, reflect on:

1. **What went well?** Which debugging strategies worked?
2. **What was challenging?** Where did you get stuck?
3. **What would you do differently?** Process improvements?
4. **Key learning?** What's the most important thing you learned?

### Sustain Engineering Takeaway
> In production, cross-stack bugs are the norm, not the exception.
> The ability to trace issues across layers is a **critical sustain skill**.

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Cross-stack debugging | Trace bugs from UI through API to database |
| Root cause analysis | Use 5 Whys to find the real cause |
| Team collaboration | Pair programming for multi-layer issues |
| Testing | Test at every layer: unit, integration, E2E |
| JIRA workflow | Document everything: RCA, fix, verification |
| Communication | API contracts prevent integration bugs |
| Sustain mindset | Fix the system, not just the symptom |

> **Next: Module 18 -- DevOps Fundamentals**
