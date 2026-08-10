# Module 12: Database & SQL -- FoodExpress Reporting Fixes

## Sustain Context

The client escalated:

> "Our FoodExpress reporting dashboard is broken. The daily revenue shows 3x the actual amount because of a Cartesian product in the SQL, the customer loyalty report excludes users who never ordered, the cancellation rate crashes with division by zero, and the monthly report takes 15 seconds because a function call prevents index usage. Fix all the SQL queries, add missing indexes, and set up a proper backup routine. Full day -- morning for query fixes, afternoon for optimization and backup."

---

## Tasks

| # | Type | Issue | File |
|---|------|-------|------|
| 1 | BUG | Revenue report shows 3x actual -- Cartesian product from missing JOIN ON clause | `reports.sql` |
| 2 | BUG | Customer loyalty report excludes zero-order customers -- needs LEFT JOIN | `reports.sql` |
| 3 | BUG | Cancellation rate query crashes -- division by zero for new restaurants | `reports.sql` |
| 4 | BUG | Top customer query fails -- WHERE used instead of HAVING for aggregate filter | `reports.sql` |
| 5 | BUG | NULL phone query returns no rows -- `= NULL` instead of `IS NULL` | `reports.sql` |
| 6 | PERF | Monthly revenue ignores index -- `YEAR(order_date)` prevents index usage | `reports.sql` |
| 7 | PERF | Missing index on `order_items.order_id` FK -- slow joins | Schema |
| 8 | ENH | Create `v_order_details` view for simplified reporting | Schema |
| 9 | ENH | Write atomic transaction for order placement | Schema |

## Deliverables

- [ ] All 7 bugs/perf issues fixed with corrected SQL
- [ ] EXPLAIN output showing index usage before and after
- [ ] Order details view created and tested
- [ ] Transaction for order placement with rollback tested
- [ ] Backup command documented and tested
