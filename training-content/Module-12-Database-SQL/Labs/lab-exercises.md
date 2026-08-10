# Module 12: Database & SQL -- Fix the Issues

## Lab Overview

The FoodExpress database has been set up by a junior developer. The schema has design flaws, the seed data has errors, and the reporting queries are returning incorrect results. Your job is to fix the schema issues, correct the queries, and optimize performance.

> "Hi Team, we migrated FoodExpress to MySQL last week but the reports are all wrong. The daily revenue report shows double the actual revenue, the customer loyalty query misses customers who have no orders, and the cancellation rate query divides by zero for new restaurants. Also the order listing page takes 8 seconds to load -- it is doing a full table scan on 100K rows. Fix the queries, add proper indexes, and get the reports accurate by end of day."

---

## Setup

1. Open MySQL client: `mysql -u root -p`
2. Run the setup script: `SOURCE starter-code/foodexpress_setup.sql`
3. Verify: `SHOW TABLES;` should show 4 tables
4. Check data: `SELECT COUNT(*) FROM orders;` should return 50+ rows
5. Run the broken report: `SOURCE starter-code/reports.sql` -- notice incorrect results

---

## Bug List

### Bug #1: Duplicate Revenue from Missing JOIN Condition
- **Where:** `reports.sql` -- Daily Revenue Report query
- **Symptom:** Revenue report shows exactly 3x the actual daily revenue.
- **Hint:** The query joins `orders` with `order_items` but is missing the `ON` clause, creating a Cartesian product. Each order row is multiplied by every item row.
- **Debug:** Run `SELECT COUNT(*) FROM orders, order_items;` vs `SELECT COUNT(*) FROM orders JOIN order_items ON orders.order_id = order_items.order_id;`. Compare the row counts.
- **Impact:** Finance team is making decisions based on inflated revenue numbers.

### Bug #2: LEFT JOIN Needed for Customer Loyalty Report
- **Where:** `reports.sql` -- Customer Loyalty query
- **Symptom:** The query "all customers with their order count" misses customers who have never placed an order. They should appear with `order_count = 0`.
- **Hint:** Change `INNER JOIN` to `LEFT JOIN` between `customers` and `orders`. Use `COUNT(o.order_id)` instead of `COUNT(*)` so NULL orders are counted as 0.
- **Debug:** Compare `SELECT COUNT(*) FROM customers;` with the number of rows in the loyalty report. If they differ, customers are being excluded.
- **Impact:** Marketing cannot identify inactive customers for re-engagement campaigns.

### Bug #3: Division by Zero in Cancellation Rate
- **Where:** `reports.sql` -- Restaurant Cancellation Rate query
- **Symptom:** Query crashes with `ERROR 1365: Division by 0` for restaurants with zero orders.
- **Hint:** Use `NULLIF(COUNT(*), 0)` in the denominator, or add `HAVING COUNT(*) > 0` to exclude restaurants with no orders.
- **Debug:** Check which restaurants have zero orders: `SELECT restaurant_id FROM restaurants WHERE restaurant_id NOT IN (SELECT restaurant_id FROM orders);`
- **Impact:** Report crashes entirely -- no cancellation data for any restaurant.

### Bug #4: WHERE vs HAVING Confusion
- **Where:** `reports.sql` -- Top Customers query
- **Symptom:** Query `SELECT customer_id, SUM(total_amount) AS total_spend FROM orders WHERE total_spend > 1000 GROUP BY customer_id;` fails with "Unknown column 'total_spend' in WHERE clause".
- **Hint:** `total_spend` is an alias for an aggregate. Aggregates must be filtered with `HAVING`, not `WHERE`. WHERE runs before GROUP BY, so the alias does not exist yet.
- **Debug:** Move the filter from `WHERE` to `HAVING`. The alias is available in HAVING.
- **Impact:** Top customer report cannot be generated.

### Bug #5: NULL Comparison Bug
- **Where:** `reports.sql` -- Customers Without Phone query
- **Symptom:** `SELECT * FROM customers WHERE phone = NULL;` returns 0 rows even though some customers have NULL phone values.
- **Hint:** `NULL = NULL` evaluates to NULL (unknown), not TRUE. Use `IS NULL` instead of `= NULL`.
- **Debug:** Run `SELECT * FROM customers WHERE phone IS NULL;` and compare the result.
- **Impact:** Cannot identify customers with missing contact info for data cleanup.

### Bug #6: Function on Indexed Column Prevents Index Usage
- **Where:** `reports.sql` -- Monthly Revenue query
- **Symptom:** `SELECT MONTH(order_date), SUM(total_amount) FROM orders WHERE YEAR(order_date) = 2026 GROUP BY MONTH(order_date);` is slow despite an index on `order_date`.
- **Hint:** Applying a function (`YEAR()`) to the indexed column prevents MySQL from using the index. Rewrite as a range condition: `WHERE order_date >= '2026-01-01' AND order_date < '2027-01-01'`.
- **Debug:** Run `EXPLAIN` on both versions. Check the `key` column -- the original shows NULL (no index), the fixed version shows the index name.
- **Impact:** Monthly report takes 15 seconds on production data.

### Bug #7: Missing Index on Foreign Key
- **Where:** Schema -- `order_items` table
- **Symptom:** Joining `orders` with `order_items` is slow for large datasets.
- **Hint:** The `order_id` foreign key in `order_items` does not have an explicit index. While MySQL auto-creates indexes for foreign keys in InnoDB, verify with `SHOW INDEX FROM order_items;`. If missing, add it.
- **Debug:** Run `EXPLAIN SELECT * FROM orders o JOIN order_items oi ON o.order_id = oi.order_id WHERE o.order_id = 1;` and check if an index is used on `order_items`.
- **Impact:** All queries involving order details are unnecessarily slow.

---

## Enhancement Exercises

### Enhancement #1: Create a View for Order Details
```sql
-- Create a view that joins orders with customers, restaurants, and items
-- so report queries can simply SELECT from the view
CREATE VIEW v_order_details AS ...
```

### Enhancement #2: Write a Transaction for Order Placement
```sql
-- Write a transaction that:
-- 1. Inserts into orders
-- 2. Inserts multiple rows into order_items
-- 3. Rolls back if any step fails
START TRANSACTION;
...
COMMIT;
```

### Enhancement #3: Add Backup Script
```bash
# Write a mysqldump command that backs up the foodexpress database
# with timestamps in the filename
mysqldump -u root -p foodexpress > backup_$(date +%Y%m%d_%H%M%S).sql
```

---

## Checkpoints

### Checkpoint 1 (Morning)
- [ ] Bug #1 fixed: Revenue report shows correct numbers (JOIN condition added)
- [ ] Bug #2 fixed: All customers appear in loyalty report (LEFT JOIN)
- [ ] Bug #3 fixed: Cancellation rate handles zero-order restaurants
- [ ] Bug #4 fixed: Top customer query uses HAVING instead of WHERE
- [ ] Bug #5 fixed: NULL comparison uses IS NULL

### Checkpoint 2 (Afternoon)
- [ ] Bug #6 fixed: Monthly revenue uses range condition (index used)
- [ ] Bug #7 fixed: Foreign key index verified or added
- [ ] Enhancement #1: Order details view created
- [ ] Enhancement #2: Order placement transaction works
- [ ] Enhancement #3: Backup command tested

---

## Bonus Challenges

1. **Find duplicate customers** -- Write a query to find customers with the same email (data quality check)
2. **Pagination** -- Implement cursor-based pagination for the orders list (faster than OFFSET for large tables)
3. **Slow query log** -- Enable MySQL slow query log, run a slow query, and find it in the log
4. **Stored procedure** -- Create a stored procedure `place_order(customer_id, restaurant_id, items_json)` that handles the full transaction
5. **Window functions** -- Use `ROW_NUMBER()` to find the most recent order per customer without a sub-query
