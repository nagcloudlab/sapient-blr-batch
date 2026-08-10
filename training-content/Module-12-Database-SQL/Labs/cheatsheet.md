# SQL Quick Reference -- FoodExpress

> Single-page reference for SQL essentials. Tables used in examples: `customers`, `restaurants`, `orders`, `order_items`, `menu_items`.

---

## SELECT Basics

| Command / Syntax | Example | Description |
|---|---|---|
| `SELECT * FROM table` | `SELECT * FROM customers;` | Return all columns and rows |
| `SELECT col1, col2 FROM table` | `SELECT name, email FROM customers;` | Return specific columns |
| `SELECT DISTINCT col FROM table` | `SELECT DISTINCT city FROM restaurants;` | Unique values only |
| `SELECT col AS alias FROM table` | `SELECT total_amount AS total FROM orders;` | Column alias |
| `SELECT 'literal', col FROM table` | `SELECT 'FoodExpress', name FROM menu_items;` | Mix literals and columns |

---

## WHERE / Operators

| Command / Syntax | Example | Description |
|---|---|---|
| `WHERE col = value` | `WHERE status = 'delivered'` | Equality filter |
| `WHERE col != value` | `WHERE status != 'cancelled'` | Not equal |
| `WHERE col > value` | `WHERE total_amount > 500` | Greater than |
| `WHERE col BETWEEN a AND b` | `WHERE total_amount BETWEEN 100 AND 500` | Inclusive range |
| `WHERE col IN (list)` | `WHERE status IN ('pending', 'confirmed')` | Match any in list |
| `WHERE col NOT IN (list)` | `WHERE city NOT IN ('Delhi', 'Mumbai')` | Exclude list values |
| `WHERE col LIKE pattern` | `WHERE name LIKE 'Pizza%'` | Pattern match (`%` = wildcard, `_` = single char) |
| `WHERE col IS NULL` | `WHERE delivered_at IS NULL` | Null check |
| `WHERE col IS NOT NULL` | `WHERE phone IS NOT NULL` | Non-null check |
| `WHERE cond1 AND cond2` | `WHERE city = 'Bangalore' AND rating > 4` | Both conditions true |
| `WHERE cond1 OR cond2` | `WHERE status = 'pending' OR status = 'confirmed'` | Either condition true |
| `WHERE NOT condition` | `WHERE NOT status = 'cancelled'` | Negate condition |

---

## JOIN Types

| Join Type | Syntax | Example | Description |
|---|---|---|---|
| INNER JOIN | `FROM a INNER JOIN b ON a.id = b.a_id` | `FROM orders o INNER JOIN customers c ON o.customer_id = c.id` | Rows with matches in both tables |
| LEFT JOIN | `FROM a LEFT JOIN b ON a.id = b.a_id` | `FROM customers c LEFT JOIN orders o ON c.id = o.customer_id` | All left rows; NULL for unmatched right |
| RIGHT JOIN | `FROM a RIGHT JOIN b ON a.id = b.a_id` | `FROM orders o RIGHT JOIN restaurants r ON o.restaurant_id = r.id` | All right rows; NULL for unmatched left |
| FULL OUTER JOIN | `FROM a FULL OUTER JOIN b ON a.id = b.a_id` | `FROM customers c FULL OUTER JOIN orders o ON c.id = o.customer_id` | All rows from both; NULL where no match |
| SELF JOIN | `FROM a t1 JOIN a t2 ON t1.col = t2.col` | `FROM customers c1 JOIN customers c2 ON c1.referral_id = c2.id` | Join table to itself |

**Multi-join example:**
```sql
SELECT c.name, r.name AS restaurant, o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
INNER JOIN restaurants r ON o.restaurant_id = r.id
WHERE o.status = 'delivered';
```

---

## GROUP BY + HAVING

| Command / Syntax | Example | Description |
|---|---|---|
| `GROUP BY col` | `GROUP BY restaurant_id` | Group rows by column value |
| `GROUP BY col1, col2` | `GROUP BY city, status` | Group by multiple columns |
| `HAVING condition` | `HAVING COUNT(*) > 10` | Filter groups (use instead of WHERE for aggregates) |
| `GROUP BY col HAVING aggregate` | `GROUP BY restaurant_id HAVING SUM(total_amount) > 10000` | Restaurants with revenue > 10000 |

**Example:**
```sql
SELECT restaurant_id, COUNT(*) AS order_count, AVG(total_amount) AS avg_order
FROM orders
WHERE status = 'delivered'
GROUP BY restaurant_id
HAVING COUNT(*) > 5
ORDER BY avg_order DESC;
```

---

## ORDER BY + LIMIT

| Command / Syntax | Example | Description |
|---|---|---|
| `ORDER BY col ASC` | `ORDER BY total_amount ASC` | Ascending order (default) |
| `ORDER BY col DESC` | `ORDER BY created_at DESC` | Descending order |
| `ORDER BY col1 ASC, col2 DESC` | `ORDER BY city ASC, rating DESC` | Multiple sort keys |
| `LIMIT n` | `LIMIT 10` | Return at most n rows |
| `LIMIT n OFFSET m` | `LIMIT 10 OFFSET 20` | Skip m rows, return next n (pagination) |

**Top 5 most expensive orders:**
```sql
SELECT id, total_amount FROM orders ORDER BY total_amount DESC LIMIT 5;
```

---

## Subqueries

| Pattern | Example | Description |
|---|---|---|
| Subquery in WHERE | `WHERE customer_id IN (SELECT id FROM customers WHERE city = 'Bangalore')` | Filter using result of inner query |
| Subquery in FROM | `FROM (SELECT restaurant_id, AVG(total_amount) AS avg FROM orders GROUP BY restaurant_id) AS r_avg` | Use subquery as derived table |
| Subquery in SELECT | `SELECT name, (SELECT COUNT(*) FROM orders WHERE customer_id = c.id) AS order_count FROM customers c` | Scalar correlated subquery |
| EXISTS | `WHERE EXISTS (SELECT 1 FROM orders WHERE customer_id = c.id)` | True if subquery returns any row |

---

## INSERT / UPDATE / DELETE

| Command / Syntax | Example | Description |
|---|---|---|
| `INSERT INTO table (cols) VALUES (vals)` | `INSERT INTO customers (name, email, city) VALUES ('Ravi', 'ravi@example.com', 'Bangalore');` | Insert single row |
| `INSERT INTO table (cols) VALUES (...),(...)` | `INSERT INTO menu_items (name, price, restaurant_id) VALUES ('Biryani', 180, 1), ('Naan', 40, 1);` | Insert multiple rows |
| `UPDATE table SET col = val WHERE cond` | `UPDATE orders SET status = 'delivered' WHERE id = 101;` | Update matching rows |
| `UPDATE table SET col1 = v1, col2 = v2 WHERE cond` | `UPDATE menu_items SET price = 200, is_available = 1 WHERE id = 5;` | Update multiple columns |
| `DELETE FROM table WHERE cond` | `DELETE FROM orders WHERE status = 'cancelled' AND created_at < '2026-01-01';` | Delete matching rows |
| `TRUNCATE TABLE table` | `TRUNCATE TABLE order_items;` | Delete all rows, fast (no WHERE) |

---

## CREATE TABLE / INDEX

| Command / Syntax | Example | Description |
|---|---|---|
| `CREATE TABLE name (col type constraints, ...)` | See below | Define new table |
| `PRIMARY KEY` | `id INT PRIMARY KEY AUTO_INCREMENT` | Unique row identifier |
| `NOT NULL` | `name VARCHAR(100) NOT NULL` | Column must have a value |
| `UNIQUE` | `email VARCHAR(150) UNIQUE` | No duplicate values |
| `DEFAULT value` | `status VARCHAR(20) DEFAULT 'pending'` | Default when not supplied |
| `FOREIGN KEY` | `FOREIGN KEY (customer_id) REFERENCES customers(id)` | Enforce referential integrity |
| `CREATE INDEX name ON table(col)` | `CREATE INDEX idx_orders_customer ON orders(customer_id);` | Speed up lookups |
| `CREATE UNIQUE INDEX` | `CREATE UNIQUE INDEX idx_customers_email ON customers(email);` | Index + uniqueness constraint |
| `DROP TABLE table` | `DROP TABLE IF EXISTS temp_orders;` | Delete table |
| `ALTER TABLE table ADD col type` | `ALTER TABLE restaurants ADD cuisine_type VARCHAR(50);` | Add column |

**CREATE TABLE example:**
```sql
CREATE TABLE orders (
    id           INT PRIMARY KEY AUTO_INCREMENT,
    customer_id  INT NOT NULL,
    restaurant_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status       VARCHAR(20) DEFAULT 'pending',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
```

---

## Aggregate Functions

| Function | Example | Description |
|---|---|---|
| `COUNT(*)` | `SELECT COUNT(*) FROM orders WHERE status = 'delivered';` | Total number of rows |
| `COUNT(col)` | `SELECT COUNT(delivered_at) FROM orders;` | Count non-NULL values |
| `COUNT(DISTINCT col)` | `SELECT COUNT(DISTINCT customer_id) FROM orders;` | Count unique values |
| `SUM(col)` | `SELECT SUM(total_amount) FROM orders WHERE restaurant_id = 3;` | Sum of values |
| `AVG(col)` | `SELECT AVG(total_amount) FROM orders;` | Average value |
| `MIN(col)` | `SELECT MIN(price) FROM menu_items WHERE restaurant_id = 3;` | Smallest value |
| `MAX(col)` | `SELECT MAX(total_amount) FROM orders WHERE status = 'delivered';` | Largest value |

**Combined example:**
```sql
SELECT
    r.name,
    COUNT(o.id)          AS total_orders,
    SUM(o.total_amount)  AS revenue,
    AVG(o.total_amount)  AS avg_order_value,
    MIN(o.total_amount)  AS min_order,
    MAX(o.total_amount)  AS max_order
FROM restaurants r
LEFT JOIN orders o ON r.id = o.restaurant_id
GROUP BY r.id, r.name
ORDER BY revenue DESC;
```

---

*FoodExpress Training | Module 12: Database & SQL | Publicis Sapient Sustain Eng 2026*
