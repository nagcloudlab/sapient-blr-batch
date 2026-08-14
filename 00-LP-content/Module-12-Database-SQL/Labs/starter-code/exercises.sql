-- ============================================================
-- FoodExpress SQL Exercises
-- ============================================================
USE foodexpress;

-- ============================================================
-- Exercise 1: Weekly Revenue Report
-- ============================================================
-- Write a query that shows total revenue per calendar week.
-- Include: week_start (Monday), order_count, total_revenue
-- Only count 'delivered' orders.
-- Sort by week_start ascending.
--
-- Hints:
--   - Use DATE_FORMAT or YEARWEEK() to group by week
--   - SUM(total_amount) for revenue
--   - COUNT(*) for order count
-- ============================================================

-- TODO: Write your query below



-- ============================================================
-- Exercise 2: Create Composite Index
-- ============================================================
-- Orders are frequently queried by customer + date range, e.g.:
--   SELECT * FROM orders
--   WHERE customer_id = 1
--     AND order_date BETWEEN '2026-07-01' AND '2026-07-31';
--
-- Create a composite index on (customer_id, order_date) to
-- speed up this common query pattern.
--
-- Then run EXPLAIN on the query above to verify the index is used.
-- ============================================================

-- TODO: Create the composite index below


-- TODO: Run EXPLAIN on the query to verify index usage



-- ============================================================
-- Exercise 3: Order Placement Transaction
-- ============================================================
-- Write a transaction that places a new order:
--   1. INSERT into orders (customer_id=1, restaurant_id=2, ...)
--   2. INSERT two order_items for the new order
--   3. UPDATE menu_items to decrement a hypothetical stock column
--      (you may ALTER TABLE first to add a stock column)
--   4. COMMIT if all succeed; ROLLBACK if any step fails
--
-- Hints:
--   - BEGIN; ... COMMIT;
--   - Use LAST_INSERT_ID() to get the new order_id
--   - Add error handling with a simple check or DECLARE HANDLER
-- ============================================================

-- TODO: Write your transaction below

