-- ============================================================
-- FoodExpress SQL Queries  (BUGGY VERSION — 7 bugs to find)
-- ============================================================
USE foodexpress;

-- ============================================================
-- Q1  List every order with restaurant name and customer name
-- ============================================================
-- BUG 1: Cartesian product — missing JOIN condition
SELECT c.first_name, c.last_name,
       r.name AS restaurant,
       o.order_id, o.order_date, o.total_amount
FROM   customers c, restaurants r, orders o
WHERE  o.customer_id = c.customer_id;
-- Expect ~12 rows, but this returns 12 x 6 = 72 rows!


-- ============================================================
-- Q2  Calculate the true total for each order from line items
-- ============================================================
-- BUG 2: FLOAT rounding — use FLOAT instead of DECIMAL
SELECT o.order_id,
       CAST(SUM(oi.quantity * oi.unit_price) AS FLOAT) AS calculated_total,
       o.total_amount AS stored_total
FROM   orders o
JOIN   order_items oi ON oi.order_id = o.order_id
GROUP  BY o.order_id, o.total_amount;


-- ============================================================
-- Q3  Find customers who have never placed an order
-- ============================================================
-- BUG 3: NULL comparison with = instead of IS NULL
SELECT c.customer_id, c.first_name, c.last_name
FROM   customers c
LEFT   JOIN orders o ON o.customer_id = c.customer_id
WHERE  o.order_id = NULL;


-- ============================================================
-- Q4  Revenue per restaurant (only delivered orders)
-- ============================================================
-- BUG 4: GROUP BY includes non-aggregated column without aggregate
SELECT r.name,
       o.order_date,
       SUM(o.total_amount) AS revenue
FROM   restaurants r
JOIN   orders o ON o.restaurant_id = r.restaurant_id
WHERE  o.status = 'delivered'
GROUP  BY r.name;
-- o.order_date is in SELECT but not in GROUP BY and not aggregated


-- ============================================================
-- Q5  Find the restaurant with the highest single-order value
-- ============================================================
-- BUG 5: Subquery returns multiple rows where single value expected
SELECT r.name, o.total_amount
FROM   restaurants r
JOIN   orders o ON o.restaurant_id = r.restaurant_id
WHERE  o.total_amount = (
           SELECT MAX(total_amount)
           FROM   orders
           GROUP  BY restaurant_id
       );
-- Subquery returns one MAX per restaurant (6 rows), but = expects 1 row


-- ============================================================
-- Q6  Search orders by customer email (performance check)
-- ============================================================
-- BUG 6: No index on customers.email — full table scan
-- Run: EXPLAIN SELECT ... to confirm type = ALL
-- EXPLAIN
SELECT o.order_id, o.order_date, o.total_amount
FROM   orders o
JOIN   customers c ON c.customer_id = o.customer_id
WHERE  c.email = 'aarav.sharma@email.com';
-- Without an index on email, this does a full table scan on customers


-- ============================================================
-- Q7  List all restaurants and their orders (include those
--     with zero orders)
-- ============================================================
-- BUG 7: WHERE clause on wrong side of LEFT JOIN
--         This filters out NULLs, turning LEFT JOIN into INNER JOIN
SELECT r.name AS restaurant,
       o.order_id,
       o.total_amount,
       o.status
FROM   restaurants r
LEFT   JOIN orders o ON o.restaurant_id = r.restaurant_id
WHERE  o.status != 'cancelled';
-- Restaurants with zero orders have o.status = NULL,
-- and NULL != 'cancelled' evaluates to NULL (falsy), so they vanish
