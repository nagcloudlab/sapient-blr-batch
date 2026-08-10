# Module 12 Checklist -- Participant Submission

## Bug Fixes
- [ ] Bug #1: Revenue report shows correct daily totals (no Cartesian product)
- [ ] Bug #2: Customer loyalty report includes all customers, even with zero orders
- [ ] Bug #3: Cancellation rate handles restaurants with zero orders (no division by zero)
- [ ] Bug #4: Top customer query uses HAVING for aggregate filter
- [ ] Bug #5: NULL phone query uses `IS NULL` and returns correct results

## Performance Fixes
- [ ] Bug #6: Monthly revenue query uses range condition; EXPLAIN shows index usage
- [ ] Bug #7: `order_items.order_id` has an index; verified with SHOW INDEX

## Enhancements
- [ ] View `v_order_details` created and returns correct joined data
- [ ] Order placement transaction tested with COMMIT and ROLLBACK scenarios
- [ ] Backup command documented and executed successfully

## Query Verification
- [ ] Revenue numbers verified against manual calculation
- [ ] Customer count in loyalty report matches `SELECT COUNT(*) FROM customers`
- [ ] EXPLAIN output captured for Bug #6 (before and after)

## Self-Check Questions
1. What is a Cartesian product and when does it occur?
2. When should you use LEFT JOIN instead of INNER JOIN?
3. Why can you not use a column alias in a WHERE clause?
4. What is the difference between WHERE and HAVING?
5. Why does `NULL = NULL` return NULL instead of TRUE?
6. Why does applying a function to an indexed column prevent index usage?
7. What are the ACID properties of a transaction?
8. When should you add an index to a column?
