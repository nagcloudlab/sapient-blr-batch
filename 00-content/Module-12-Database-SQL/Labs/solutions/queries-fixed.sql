-- ============================================================
-- FoodExpress SQL Queries  (FIXED VERSION — all 7 bugs resolved)
-- ============================================================
USE foodexpress;

-- ============================================================
-- Q1  List every order with restaurant name and customer name
-- ============================================================
-- FIX 1: Added missing JOIN condition for restaurants table.
--   The original used an implicit cross join (FROM a, b, c) and
--   omitted o.restaurant_id = r.restaurant_id, creating a
--   Cartesian product (12 x 6 = 72 rows instead of 12).
--   Rewritten with explicit JOIN syntax for clarity.
SELECT c.first_name, c.last_name,
       r.name AS restaurant,
       o.order_id, o.order_date, o.total_amount
FROM   orders o
JOIN   customers c   ON c.customer_id   = o.customer_id
JOIN   restaurants r ON r.restaurant_id  = o.restaurant_id;


-- ============================================================
-- Q2  Calculate the true total for each order from line items
-- ============================================================
-- FIX 2: Changed CAST(... AS FLOAT) to CAST(... AS DECIMAL(10,2)).
--   FLOAT introduces binary rounding errors (e.g. 0.1 + 0.2 != 0.3).
--   DECIMAL stores exact values, which is essential for money.
SELECT o.order_id,
       CAST(SUM(oi.quantity * oi.unit_price) AS DECIMAL(10,2)) AS calculated_total,
       o.total_amount AS stored_total
FROM   orders o
JOIN   order_items oi ON oi.order_id = o.order_id
GROUP  BY o.order_id, o.total_amount;


-- ============================================================
-- Q3  Find customers who have never placed an order
-- ============================================================
-- FIX 3: Changed "= NULL" to "IS NULL".
--   In SQL, NULL is not a value — it is the absence of a value.
--   Any comparison with = returns NULL (unknown), not TRUE/FALSE.
--   IS NULL is the correct operator for NULL checks.
SELECT c.customer_id, c.first_name, c.last_name
FROM   customers c
LEFT   JOIN orders o ON o.customer_id = c.customer_id
WHERE  o.order_id IS NULL;


-- ============================================================
-- Q4  Revenue per restaurant (only delivered orders)
-- ============================================================
-- FIX 4: Removed o.order_date from SELECT (not aggregated and
--   not in GROUP BY). In strict SQL mode this is an error;
--   in permissive mode it returns an arbitrary date — misleading.
--   If you need the date range, use MIN/MAX:
--     MIN(o.order_date) AS first_order, MAX(o.order_date) AS last_order
SELECT r.name,
       SUM(o.total_amount) AS revenue,
       COUNT(*)            AS order_count
FROM   restaurants r
JOIN   orders o ON o.restaurant_id = r.restaurant_id
WHERE  o.status = 'delivered'
GROUP  BY r.name;


-- ============================================================
-- Q5  Find the restaurant with the highest single-order value
-- ============================================================
-- FIX 5: Changed subquery to return a single scalar value.
--   The original grouped by restaurant_id, returning one MAX
--   per restaurant (multiple rows). Using = with a multi-row
--   subquery causes ERROR 1242. Solution: remove GROUP BY so
--   MAX() returns the global maximum.
SELECT r.name, o.total_amount
FROM   restaurants r
JOIN   orders o ON o.restaurant_id = r.restaurant_id
WHERE  o.total_amount = (
           SELECT MAX(total_amount)
           FROM   orders
       );


-- ============================================================
-- Q6  Search orders by customer email (performance check)
-- ============================================================
-- FIX 6: Create an index on customers.email to avoid full table scan.
--   The email column already has a UNIQUE constraint (which creates
--   an index in MySQL/PostgreSQL). If it did not, we would add:
CREATE INDEX idx_customers_email ON customers(email);
-- Now EXPLAIN shows type=ref or const instead of ALL.
EXPLAIN
SELECT o.order_id, o.order_date, o.total_amount
FROM   orders o
JOIN   customers c ON c.customer_id = o.customer_id
WHERE  c.email = 'aarav.sharma@email.com';


-- ============================================================
-- Q7  List all restaurants and their orders (include those
--     with zero orders)
-- ============================================================
-- FIX 7: Moved the status filter from WHERE to the ON clause.
--   When a WHERE clause references columns from the RIGHT side
--   of a LEFT JOIN, NULLs (i.e., no-match rows) are filtered out,
--   effectively converting the LEFT JOIN into an INNER JOIN.
--   Moving the condition to ON preserves unmatched rows.
SELECT r.name AS restaurant,
       o.order_id,
       o.total_amount,
       o.status
FROM   restaurants r
LEFT   JOIN orders o ON o.restaurant_id = r.restaurant_id
                    AND o.status != 'cancelled';
