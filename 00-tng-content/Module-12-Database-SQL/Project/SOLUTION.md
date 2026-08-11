# Module 12 Solutions -- TRAINER ONLY

## Bug #1: Cartesian Product in Revenue Report

**Root Cause:** The query uses `FROM orders, order_items` (implicit cross join) without a JOIN condition. Every order row is paired with every item row, inflating the revenue by a factor of N (number of items).

**Fix:**
```sql
-- Before (Cartesian product)
SELECT DATE(o.order_date) AS day, SUM(o.total_amount) AS revenue
FROM orders o, order_items oi
GROUP BY DATE(o.order_date);

-- After (proper JOIN)
SELECT DATE(o.order_date) AS day, SUM(o.total_amount) AS revenue
FROM orders o
GROUP BY DATE(o.order_date);

-- OR if you need item-level detail:
SELECT DATE(o.order_date) AS day, SUM(oi.subtotal) AS revenue
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY DATE(o.order_date);
```

## Bug #2: INNER JOIN Excludes Zero-Order Customers

**Root Cause:** `INNER JOIN` only returns rows that match in both tables. Customers with no orders have no matching row in `orders`, so they are excluded.

**Fix:**
```sql
-- Before
SELECT c.name, COUNT(*) AS order_count
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- After
SELECT c.name, COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```
Note: `COUNT(o.order_id)` returns 0 for NULL (no orders), while `COUNT(*)` would return 1.

## Bug #3: Division by Zero in Cancellation Rate

**Root Cause:** For restaurants with zero orders, `COUNT(*)` is 0, and dividing by 0 causes an error.

**Fix:**
```sql
-- Before
SELECT r.name,
       SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) * 100
       AS cancel_rate
FROM restaurants r
JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id, r.name;

-- After
SELECT r.name,
       ROUND(SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END)
             * 100.0 / NULLIF(COUNT(o.order_id), 0), 1)
       AS cancel_rate
FROM restaurants r
LEFT JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id, r.name;
```

## Bug #4: WHERE vs HAVING for Aggregate

**Root Cause:** `WHERE total_spend > 1000` fails because `total_spend` is an alias for `SUM(total_amount)`, which is computed after GROUP BY. WHERE runs before GROUP BY and cannot reference aggregates.

**Fix:**
```sql
-- Before
SELECT customer_id, SUM(total_amount) AS total_spend
FROM orders
WHERE total_spend > 1000
GROUP BY customer_id;

-- After
SELECT customer_id, SUM(total_amount) AS total_spend
FROM orders
GROUP BY customer_id
HAVING SUM(total_amount) > 1000;
```

## Bug #5: NULL Comparison

**Root Cause:** `NULL = NULL` evaluates to NULL (unknown), not TRUE. The `=` operator cannot match NULL values.

**Fix:**
```sql
-- Before
SELECT * FROM customers WHERE phone = NULL;

-- After
SELECT * FROM customers WHERE phone IS NULL;
```

## Bug #6: Function Prevents Index Usage

**Root Cause:** `WHERE YEAR(order_date) = 2026` applies a function to the column, preventing MySQL from using the index on `order_date`. MySQL must evaluate `YEAR()` for every row (full table scan).

**Fix:**
```sql
-- Before (full table scan)
SELECT MONTH(order_date), SUM(total_amount)
FROM orders
WHERE YEAR(order_date) = 2026
GROUP BY MONTH(order_date);

-- After (uses index via range scan)
SELECT MONTH(order_date), SUM(total_amount)
FROM orders
WHERE order_date >= '2026-01-01' AND order_date < '2027-01-01'
GROUP BY MONTH(order_date);
```

## Bug #7: Missing Index on Foreign Key

**Fix:**
```sql
-- Verify existing indexes
SHOW INDEX FROM order_items;

-- Add if missing
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

## Hints

| Bug | Level 1 | Level 2 |
|-----|---------|---------|
| #1 | "How many rows does `FROM orders, order_items` return? Is that expected?" | "Add `ON o.order_id = oi.order_id` to the JOIN, or remove the join if not needed" |
| #2 | "Count total customers vs rows in the report. Do they match?" | "Change INNER JOIN to LEFT JOIN; use COUNT(o.order_id) not COUNT(*)" |
| #3 | "What happens when you divide by zero?" | "Use NULLIF(COUNT(*), 0) as the denominator" |
| #4 | "Which runs first: WHERE or GROUP BY?" | "Move the aggregate filter from WHERE to HAVING" |
| #5 | "What does `SELECT NULL = NULL` return?" | "Use IS NULL instead of = NULL" |
| #6 | "Run EXPLAIN on the query. Is the index being used?" | "Rewrite YEAR(col) = X as col >= 'X-01-01' AND col < 'X+1-01-01'" |
| #7 | "Run SHOW INDEX FROM order_items. Is order_id indexed?" | "CREATE INDEX idx_order_items_order_id ON order_items(order_id)" |
