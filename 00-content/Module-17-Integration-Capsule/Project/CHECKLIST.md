# Integration Capsule Project -- Submission Checklist
## Module 17 | Day 18

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Bug #1 (Price NaN) -- Fixed in both frontend and backend | [ ] |
| 2 | Bug #2 (Search) -- URL encoding, parameterized SQL, error sanitization | [ ] |
| 3 | Bug #3 (Order History) -- Iteration, pagination, sorting, index | [ ] |
| 4 | Bug #4 (Rating 500) -- Type parsing, validation, schema decision | [ ] |
| 5 | Unit tests -- Minimum 2 per bug (8 total) | [ ] |
| 6 | Integration tests -- At least 1 per bug (4 total) | [ ] |
| 7 | RCA document -- 5 Whys for each bug | [ ] |
| 8 | JIRA tickets -- Updated with assignee, status, comments | [ ] |
| 9 | Related tickets linked across stacks | [ ] |
| 10 | Team presentation prepared (15 min) | [ ] |
| 11 | Demo: before/after for each bug | [ ] |
| 12 | Retrospective notes written | [ ] |

---

## Self-Check Questions

1. **Does your price fix handle all edge cases?** What if price is `null`, `undefined`, `""`, `"free"`, or `0`?
2. **Is your search endpoint safe from SQL injection?** Try: `' OR 1=1 --`
3. **What happens when a customer has zero orders?** Does the order history page handle an empty array?
4. **Did you validate on both client AND server?** Never trust client-side validation alone.
5. **Are your error messages user-friendly?** No stack traces, no technical jargon for the end user.
6. **Did you add the database index?** Run `EXPLAIN SELECT` to verify it is being used.
7. **Do your tests cover edge cases?** Not just the happy path -- test with bad input.
8. **Is your RCA systemic?** "Missing API contract" is better than "wrong format" as a root cause.
9. **Can another developer understand your fix?** Are your commit messages and code comments clear?
10. **Would your fixes survive a code review?** No hardcoded values, no TODO comments, no dead code.
