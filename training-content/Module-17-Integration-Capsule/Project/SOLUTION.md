# Integration Capsule Project -- Trainer Solutions & Hints
## Module 17 | Day 18

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Price NaN | Backend: remove currency symbol from JSON response, return raw `double`. Frontend: add `parsePrice()` fallback that strips non-numeric chars | Students may fix only frontend or only backend. Emphasize: fix the root cause (backend), add defense (frontend) | Ask: "If another frontend consumer uses this API, would they also have this bug?" |
| 2 | Search Special Chars | Frontend: `encodeURIComponent()`. Backend: parameterized SQL query, input validation, sanitized error response | Students often fix only the URL encoding and miss the SQL injection. Push them to test with `'; DROP TABLE` | Ask: "What if a malicious user types into this search box?" |
| 3 | Order History | Frontend: iterate with `.map()` instead of `[0]`. Backend: add `OrderByCreatedAtDesc`, pagination. DB: add index | Students fix the frontend loop but forget pagination and indexing. Ask about production scale | Ask: "What happens when a customer has 10,000 orders?" |
| 4 | Rating 500 | Frontend: `parseInt()` + validation. Backend: `Double.parseDouble()` + range check. DB: decide on integer vs decimal scale | Students struggle with the design decision: integer vs decimal ratings. Guide them to pick one and be consistent | Ask: "Should your system support half-star ratings? What are the tradeoffs?" |
| 5 | Unit Tests | At least 2 tests per bug: happy path + edge case. Use Jest for JS, JUnit for Java | Students write only happy-path tests. Push for edge cases: null, empty, negative, very large numbers | Ask: "What input would break your fix?" |
| 6 | RCA Documents | Use 5 Whys template. Root cause should be systemic (e.g., missing API contract) not surface-level | Students often stop at the first "why". Push to the systemic root cause | Ask: "How do we prevent this category of bug in the future?" |
| 7 | JIRA Updates | Ticket should have: assignee, status changes, RCA comment, linked tickets | Students forget to link related tickets across stacks | Remind: "In production, other teams need to find this context later" |
| 8 | Presentation | Demo before/after. Show the debugging process, not just the fix. Time management is key | Teams spend too long on demo and rush RCA. Practice timing | Remind: "Stakeholders care about why it happened and how you'll prevent it" |

---

## Scoring Guide

| Grade | Points | Description |
|-------|--------|-------------|
| Excellent | 35-40 | All bugs fixed, comprehensive tests, deep RCA, polished presentation |
| Good | 28-34 | Most bugs fixed, adequate tests, solid RCA |
| Satisfactory | 20-27 | P1/P2 fixed, basic tests, surface-level RCA |
| Needs Improvement | <20 | Major bugs unfixed, minimal tests, incomplete RCA |

---

## Discussion Points for Retrospective

1. Which bug was hardest? Why? (Usually #4 due to design decisions)
2. How did you divide work? Did role assignment help?
3. What would you change about your debugging approach?
4. How would you set up monitoring to catch these bugs earlier?
5. What API contract practices would prevent cross-stack bugs?
