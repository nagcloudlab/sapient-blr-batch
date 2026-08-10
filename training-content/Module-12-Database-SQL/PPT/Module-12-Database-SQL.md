# Database & SQL
## Module 12 | Sustain Engineering Training | Day 13

**1 day | Lecture + hands-on labs**

---

## Agenda

| Session | Topics |
|---------|--------|
| First half | RDBMS Concepts, Create/Drop DB, Data Types, Tables, CRUD (Insert/Select/Where/Update/Delete), LIKE |
| Second half | Sorting, Duplicates, Grouping, HAVING, Joins, Sub-Queries, Aliases, NULL Values |
| DB Ops | Query Optimization, Indexing, Backup & Recovery, Transaction Failure, Clustering |

> Master SQL with the FoodExpress schema: orders, order_items, customers, restaurants.

---

## Why Databases Matter for Sustain Engineers

- **70%+ of production incidents** involve database issues
- Slow queries, missing indexes, deadlocks, data corruption
- Sustain engineers must:
  - Read and debug existing SQL queries
  - Optimize slow queries
  - Understand backup/recovery procedures
  - Handle transaction failures gracefully

### FoodExpress Database

```
FoodExpress uses MySQL 8.0 with 4 core tables:
- customers     (user profiles, addresses)
- restaurants   (restaurant info, cuisine, rating)
- orders        (order header: customer, restaurant, status, total)
- order_items   (line items: what was ordered, quantity, price)
```

---

## Relational Database Concepts

### What Is an RDBMS?

| Term | Definition |
|------|-----------|
| Database | Organized collection of structured data |
| Table | A set of rows and columns (like a spreadsheet) |
| Row (Record) | A single entry in a table |
| Column (Field) | A specific attribute of the data |
| Primary Key | Unique identifier for each row |
| Foreign Key | A column that references a primary key in another table |
| Schema | The structure/blueprint of the database |

### RDBMS vs NoSQL

| Feature | RDBMS (MySQL) | NoSQL (MongoDB) |
|---------|---------------|-----------------|
| Structure | Fixed schema, tables | Flexible schema, documents |
| Query Language | SQL | MongoDB Query Language |
| Relationships | JOINs | Embedded documents / references |
| ACID | Full support | Varies by engine |
| Best For | Structured, relational data | Unstructured, rapidly changing data |

---

## Create and Drop Database

```sql
-- Create a new database
CREATE DATABASE foodexpress;

-- Create with character set
CREATE DATABASE foodexpress
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Show all databases
SHOW DATABASES;

-- Use a specific database
USE foodexpress;

-- Drop (delete) a database -- DANGEROUS!
DROP DATABASE foodexpress;

-- Safe drop: only if it exists
DROP DATABASE IF EXISTS foodexpress;
```

### Best Practice
- Always use `IF EXISTS` / `IF NOT EXISTS` to prevent errors
- Never drop a database in production without authorization
- In sustain work: you read/query databases, rarely create/drop them

---

## MySQL Data Types

### Numeric Types

| Type | Range | Use Case |
|------|-------|----------|
| `INT` | -2B to 2B | Order IDs, quantities |
| `BIGINT` | Very large numbers | Auto-increment IDs at scale |
| `DECIMAL(10,2)` | Exact precision | Prices, totals (money!) |
| `FLOAT` | Approximate | Ratings, coordinates |
| `TINYINT` | 0-255 | Boolean flags, small counts |

### String Types

| Type | Max Size | Use Case |
|------|----------|----------|
| `VARCHAR(n)` | Up to 65,535 | Names, emails, addresses |
| `CHAR(n)` | Fixed length | Status codes, country codes |
| `TEXT` | 65,535 | Descriptions, notes |
| `ENUM('a','b')` | Predefined set | Status values, categories |

### Date/Time Types

| Type | Format | Use Case |
|------|--------|----------|
| `DATE` | YYYY-MM-DD | Birth dates |
| `DATETIME` | YYYY-MM-DD HH:MM:SS | Order timestamps |
| `TIMESTAMP` | Auto-updates | created_at, updated_at |

---

## FoodExpress Schema Design

```sql
CREATE TABLE customers (
    customer_id   INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(150) UNIQUE NOT NULL,
    phone         VARCHAR(15),
    address       VARCHAR(255),
    city          VARCHAR(50) DEFAULT 'Bangalore',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    cuisine       VARCHAR(50) NOT NULL,
    rating        DECIMAL(2,1) DEFAULT 0.0,
    is_active     TINYINT(1) DEFAULT 1,
    city          VARCHAR(50) DEFAULT 'Bangalore',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## FoodExpress Schema (continued)

```sql
CREATE TABLE orders (
    order_id      INT AUTO_INCREMENT PRIMARY KEY,
    customer_id   INT NOT NULL,
    restaurant_id INT NOT NULL,
    order_date    DATETIME DEFAULT CURRENT_TIMESTAMP,
    status        ENUM('placed','confirmed','preparing',
                       'out_for_delivery','delivered','cancelled')
                  DEFAULT 'placed',
    total_amount  DECIMAL(10,2) NOT NULL,
    delivery_address VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

CREATE TABLE order_items (
    item_id       INT AUTO_INCREMENT PRIMARY KEY,
    order_id      INT NOT NULL,
    item_name     VARCHAR(100) NOT NULL,
    quantity      INT NOT NULL DEFAULT 1,
    unit_price    DECIMAL(10,2) NOT NULL,
    subtotal      DECIMAL(10,2) GENERATED ALWAYS AS
                  (quantity * unit_price) STORED,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

---

## Entity Relationship Diagram

```
+----------------+       +----------------+
|   customers    |       |  restaurants   |
+----------------+       +----------------+
| customer_id PK |       | restaurant_id PK|
| name           |       | name           |
| email          |       | cuisine        |
| phone          |       | rating         |
| address        |       | is_active      |
| city           |       | city           |
+-------+--------+       +-------+--------+
        |                         |
        | 1:N                     | 1:N
        |                         |
+-------v-------------------------v--------+
|                 orders                    |
+-------------------------------------------+
| order_id PK                               |
| customer_id FK  -----> customers          |
| restaurant_id FK ----> restaurants        |
| order_date, status, total_amount          |
+-------------------+-----------------------+
                    | 1:N
                    |
          +---------v----------+
          |    order_items     |
          +--------------------+
          | item_id PK         |
          | order_id FK        |
          | item_name          |
          | quantity           |
          | unit_price         |
          | subtotal (computed)|
          +--------------------+
```

---

## INSERT -- Adding Data

```sql
-- Insert a single customer
INSERT INTO customers (name, email, phone, address, city)
VALUES ('Priya Sharma', 'priya@email.com', '9876543210',
        '42 MG Road', 'Bangalore');

-- Insert multiple restaurants
INSERT INTO restaurants (name, cuisine, rating, is_active, city)
VALUES
  ('Spice Garden', 'Indian', 4.5, 1, 'Bangalore'),
  ('Pizza Palace', 'Italian', 4.2, 1, 'Bangalore'),
  ('Dragon Wok', 'Chinese', 3.8, 1, 'Bangalore'),
  ('Burger Barn', 'American', 4.0, 0, 'Bangalore'),
  ('Sushi House', 'Japanese', 4.7, 1, 'Mumbai');

-- Insert an order
INSERT INTO orders (customer_id, restaurant_id, status, total_amount,
                    delivery_address)
VALUES (1, 1, 'placed', 649.00, '42 MG Road, Bangalore');

-- Insert order items
INSERT INTO order_items (order_id, item_name, quantity, unit_price)
VALUES
  (1, 'Butter Chicken', 2, 249.00),
  (1, 'Naan', 3, 49.00),
  (1, 'Mango Lassi', 1, 99.00);
```

---

## SELECT -- Reading Data

```sql
-- Select all columns
SELECT * FROM customers;

-- Select specific columns
SELECT name, email, city FROM customers;

-- Select with alias
SELECT name AS customer_name,
       email AS contact_email
FROM customers;

-- Count rows
SELECT COUNT(*) AS total_customers FROM customers;

-- Distinct values
SELECT DISTINCT city FROM customers;
SELECT DISTINCT cuisine FROM restaurants;
```

### FoodExpress Example
```sql
-- All active restaurants with their ratings
SELECT name, cuisine, rating
FROM restaurants
WHERE is_active = 1
ORDER BY rating DESC;
```

---

## WHERE -- Filtering Data

```sql
-- Comparison operators
SELECT * FROM orders WHERE total_amount > 500;
SELECT * FROM orders WHERE status = 'delivered';
SELECT * FROM restaurants WHERE rating >= 4.0;

-- AND / OR
SELECT * FROM restaurants
WHERE cuisine = 'Indian' AND rating >= 4.0;

SELECT * FROM orders
WHERE status = 'cancelled' OR status = 'delivered';

-- IN operator
SELECT * FROM orders
WHERE status IN ('placed', 'confirmed', 'preparing');

-- BETWEEN
SELECT * FROM orders
WHERE total_amount BETWEEN 200 AND 1000;

-- NOT
SELECT * FROM restaurants
WHERE cuisine NOT IN ('Chinese', 'Japanese');

-- NULL checks
SELECT * FROM customers WHERE phone IS NULL;
SELECT * FROM customers WHERE phone IS NOT NULL;
```

---

## LIKE -- Pattern Matching

```sql
-- % matches zero or more characters
SELECT * FROM customers WHERE name LIKE 'P%';      -- starts with P
SELECT * FROM customers WHERE email LIKE '%gmail%'; -- contains gmail
SELECT * FROM restaurants WHERE name LIKE '%Palace'; -- ends with Palace

-- _ matches exactly one character
SELECT * FROM customers WHERE phone LIKE '98765_____'; -- starts with 98765

-- FoodExpress: Find restaurants with "Pizza" in the name
SELECT name, cuisine, rating
FROM restaurants
WHERE name LIKE '%Pizza%'
  AND is_active = 1;

-- Case-insensitive search (MySQL default for utf8)
SELECT * FROM restaurants WHERE name LIKE '%garden%';
```

### LIKE Performance Warning

| Pattern | Uses Index? | Performance |
|---------|-------------|-------------|
| `LIKE 'Pizza%'` | Yes (prefix) | Fast |
| `LIKE '%Pizza'` | No (suffix) | Slow -- full table scan |
| `LIKE '%Pizza%'` | No (contains) | Slow -- full table scan |

---

## UPDATE -- Modifying Data

```sql
-- Update a single column
UPDATE customers
SET phone = '9999888877'
WHERE customer_id = 1;

-- Update multiple columns
UPDATE orders
SET status = 'delivered',
    total_amount = 699.00
WHERE order_id = 1;

-- Update with condition
UPDATE restaurants
SET is_active = 0
WHERE rating < 3.0;

-- DANGER: UPDATE without WHERE affects ALL rows!
UPDATE restaurants SET rating = 5.0;  -- DO NOT DO THIS!

-- Safe update: Always include WHERE
UPDATE restaurants
SET rating = 4.8
WHERE restaurant_id = 5;
```

### FoodExpress: Update Order Status
```sql
-- Typical order lifecycle
UPDATE orders SET status = 'confirmed' WHERE order_id = 1;
UPDATE orders SET status = 'preparing' WHERE order_id = 1;
UPDATE orders SET status = 'out_for_delivery' WHERE order_id = 1;
UPDATE orders SET status = 'delivered' WHERE order_id = 1;
```

---

## DELETE -- Removing Data

```sql
-- Delete specific rows
DELETE FROM order_items WHERE item_id = 3;

-- Delete with condition
DELETE FROM orders WHERE status = 'cancelled';

-- DANGER: DELETE without WHERE removes ALL rows!
DELETE FROM customers;  -- DO NOT DO THIS!

-- Safe delete: Always use WHERE
DELETE FROM customers WHERE customer_id = 10;
```

### Soft Delete vs Hard Delete

| Approach | SQL | Pros | Cons |
|----------|-----|------|------|
| Hard Delete | `DELETE FROM restaurants WHERE id = 5` | Frees storage | Data lost forever |
| Soft Delete | `UPDATE restaurants SET is_active = 0 WHERE id = 5` | Recoverable, audit trail | Extra storage, queries need filter |

### FoodExpress Uses Soft Delete
```sql
-- "Delete" a restaurant (soft)
UPDATE restaurants
SET is_active = 0
WHERE restaurant_id = 4;

-- All queries must filter:
SELECT * FROM restaurants WHERE is_active = 1;
```

---

## ORDER BY -- Sorting Results

```sql
-- Sort ascending (default)
SELECT * FROM restaurants ORDER BY rating ASC;

-- Sort descending
SELECT * FROM restaurants ORDER BY rating DESC;

-- Sort by multiple columns
SELECT * FROM orders
ORDER BY status ASC, order_date DESC;

-- FoodExpress: Top-rated active restaurants
SELECT name, cuisine, rating
FROM restaurants
WHERE is_active = 1
ORDER BY rating DESC
LIMIT 5;
```

### LIMIT and OFFSET (Pagination)

```sql
-- First page (items 1-10)
SELECT * FROM orders ORDER BY order_date DESC LIMIT 10 OFFSET 0;

-- Second page (items 11-20)
SELECT * FROM orders ORDER BY order_date DESC LIMIT 10 OFFSET 10;

-- Shorthand: LIMIT offset, count
SELECT * FROM orders ORDER BY order_date DESC LIMIT 10, 10;
```

---

## DISTINCT -- Removing Duplicates

```sql
-- Unique cuisines
SELECT DISTINCT cuisine FROM restaurants;

-- Unique cities where we have customers
SELECT DISTINCT city FROM customers;

-- Count of unique cuisines
SELECT COUNT(DISTINCT cuisine) AS cuisine_count
FROM restaurants;

-- Distinct combinations
SELECT DISTINCT city, cuisine
FROM restaurants
ORDER BY city, cuisine;
```

### When to Use DISTINCT

| Scenario | Use DISTINCT? |
|----------|---------------|
| List all cuisine types | Yes |
| Count unique customers who ordered | Yes |
| Get all orders for a customer | No (orders are already unique by PK) |
| Find duplicate emails | No (use GROUP BY + HAVING) |

---

## GROUP BY -- Aggregating Data

```sql
-- Count orders per customer
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id;

-- Total revenue per restaurant
SELECT restaurant_id,
       SUM(total_amount) AS total_revenue,
       COUNT(*) AS order_count,
       AVG(total_amount) AS avg_order_value
FROM orders
GROUP BY restaurant_id;

-- Orders per status
SELECT status, COUNT(*) AS count
FROM orders
GROUP BY status
ORDER BY count DESC;
```

### Aggregate Functions

| Function | Description | Example |
|----------|-------------|---------|
| `COUNT(*)` | Count rows | Number of orders |
| `SUM(col)` | Total | Total revenue |
| `AVG(col)` | Average | Average order value |
| `MIN(col)` | Minimum | Cheapest order |
| `MAX(col)` | Maximum | Most expensive order |

---

## HAVING -- Filtering Groups

```sql
-- Customers with more than 5 orders
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;

-- Restaurants with average order > 500
SELECT restaurant_id,
       AVG(total_amount) AS avg_order
FROM orders
GROUP BY restaurant_id
HAVING AVG(total_amount) > 500;

-- Cuisines with more than 2 restaurants
SELECT cuisine, COUNT(*) AS restaurant_count
FROM restaurants
GROUP BY cuisine
HAVING COUNT(*) > 2;
```

### WHERE vs HAVING

| Clause | Filters On | Timing |
|--------|-----------|--------|
| `WHERE` | Individual rows | Before grouping |
| `HAVING` | Grouped results | After grouping |

```sql
-- WHERE filters rows, HAVING filters groups
SELECT restaurant_id, SUM(total_amount) AS revenue
FROM orders
WHERE status = 'delivered'        -- filter rows first
GROUP BY restaurant_id
HAVING SUM(total_amount) > 10000; -- then filter groups
```

---

## Joins -- Combining Tables

### INNER JOIN

```sql
-- Orders with customer names
SELECT o.order_id, c.name AS customer_name,
       o.total_amount, o.status
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- Orders with restaurant names
SELECT o.order_id, r.name AS restaurant_name,
       o.total_amount, o.order_date
FROM orders o
INNER JOIN restaurants r ON o.restaurant_id = r.restaurant_id;
```

### Multi-Table JOIN

```sql
-- Complete order view: customer + restaurant + items
SELECT o.order_id,
       c.name AS customer,
       r.name AS restaurant,
       oi.item_name,
       oi.quantity,
       oi.unit_price,
       oi.subtotal,
       o.total_amount,
       o.status
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN restaurants r ON o.restaurant_id = r.restaurant_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
ORDER BY o.order_id;
```

---

## Join Types Comparison

```
INNER JOIN          LEFT JOIN           RIGHT JOIN          FULL OUTER JOIN
+---+---+          +---+---+          +---+---+           +---+---+
| A | B |          | A | B |          | A | B |           | A | B |
+---+---+          +---+---+          +---+---+           +---+---+
|   |XXX|          |XXX|XXX|          |   |XXX|           |XXX|XXX|
|   |XXX|          |XXX|XXX|          |   |XXX|           |XXX|XXX|
+---+---+          |XXX|   |          +---+---+           |XXX|   |
                   +---+---+                              |   |XXX|
                                                          +---+---+
Only matching      All from A,        All from B,         All from both
rows               NULL if no B       NULL if no A
```

### FoodExpress Examples

```sql
-- LEFT JOIN: All customers, even those with no orders
SELECT c.name, COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Customers who NEVER ordered (LEFT JOIN + IS NULL)
SELECT c.name, c.email
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

---

## Sub-Queries

```sql
-- Find customers who ordered more than average
SELECT name, email
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total_amount) > (
        SELECT AVG(total_amount) FROM orders
    )
);

-- Restaurant with the highest average order value
SELECT name, cuisine
FROM restaurants
WHERE restaurant_id = (
    SELECT restaurant_id
    FROM orders
    GROUP BY restaurant_id
    ORDER BY AVG(total_amount) DESC
    LIMIT 1
);

-- Orders above the average order amount
SELECT order_id, total_amount
FROM orders
WHERE total_amount > (SELECT AVG(total_amount) FROM orders);
```

---

## Sub-Queries (continued)

### Correlated Sub-Queries

```sql
-- Find each customer's latest order
SELECT c.name, o.order_id, o.order_date, o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date = (
    SELECT MAX(o2.order_date)
    FROM orders o2
    WHERE o2.customer_id = o.customer_id
);

-- Restaurants with orders above their own average
SELECT r.name, o.order_id, o.total_amount
FROM orders o
INNER JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.total_amount > (
    SELECT AVG(o2.total_amount)
    FROM orders o2
    WHERE o2.restaurant_id = o.restaurant_id
);
```

### EXISTS Sub-Query

```sql
-- Active restaurants that have at least one order
SELECT r.name, r.cuisine
FROM restaurants r
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.restaurant_id = r.restaurant_id
);
```

---

## Aliases

```sql
-- Column aliases
SELECT
    c.name AS customer_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS lifetime_value,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

-- Table aliases (shorthand)
SELECT o.order_id, c.name, r.name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id;

-- Derived table (sub-query as table)
SELECT restaurant_name, total_revenue
FROM (
    SELECT r.name AS restaurant_name,
           SUM(o.total_amount) AS total_revenue
    FROM orders o
    JOIN restaurants r ON o.restaurant_id = r.restaurant_id
    GROUP BY r.restaurant_id, r.name
) AS revenue_summary
WHERE total_revenue > 5000;
```

---

## NULL Values

```sql
-- NULL is not a value -- it means "unknown" or "missing"

-- Check for NULL (cannot use = or !=)
SELECT * FROM customers WHERE phone IS NULL;
SELECT * FROM customers WHERE phone IS NOT NULL;

-- NULL in calculations
SELECT 5 + NULL;           -- Result: NULL
SELECT NULL = NULL;        -- Result: NULL (not TRUE!)
SELECT NULL != NULL;       -- Result: NULL

-- COALESCE: Replace NULL with a default
SELECT name,
       COALESCE(phone, 'No phone') AS phone,
       COALESCE(address, 'No address') AS address
FROM customers;

-- IFNULL (MySQL-specific)
SELECT name, IFNULL(phone, 'N/A') AS phone FROM customers;

-- NULL-safe comparison
SELECT * FROM customers WHERE phone <=> NULL; -- same as IS NULL
```

### NULL Gotcha in Aggregations

```sql
-- COUNT(*) counts all rows, COUNT(col) skips NULLs
SELECT COUNT(*) AS total_rows,
       COUNT(phone) AS rows_with_phone
FROM customers;
-- If 10 rows, 3 have NULL phone: total_rows=10, rows_with_phone=7
```

---

## Query Optimization

### EXPLAIN -- Understanding Query Plans

```sql
-- See how MySQL executes a query
EXPLAIN SELECT * FROM orders
WHERE customer_id = 1 AND status = 'delivered';

-- Key columns in EXPLAIN output:
-- type:    ALL (full scan), ref (index), const (PK lookup)
-- key:     Which index is used (NULL = no index)
-- rows:    Estimated rows to examine
-- Extra:   Using where, Using index, Using filesort
```

### Optimization Rules

| Problem | Bad Query | Good Query |
|---------|-----------|------------|
| No index on filter | `WHERE status = 'delivered'` | Add index on `status` |
| SELECT * | `SELECT * FROM orders` | `SELECT order_id, status` |
| Function on column | `WHERE YEAR(order_date) = 2026` | `WHERE order_date >= '2026-01-01'` |
| Leading wildcard | `WHERE name LIKE '%Pizza%'` | `WHERE name LIKE 'Pizza%'` |
| N+1 queries | Loop with single SELECTs | Use JOIN instead |

---

## Indexing

### Creating Indexes

```sql
-- Single column index
CREATE INDEX idx_orders_status ON orders(status);

-- Composite index (order matters!)
CREATE INDEX idx_orders_cust_status
ON orders(customer_id, status);

-- Unique index
CREATE UNIQUE INDEX idx_customers_email
ON customers(email);

-- Show indexes on a table
SHOW INDEX FROM orders;

-- Drop an index
DROP INDEX idx_orders_status ON orders;
```

### When to Index

| Index When | Do Not Index When |
|------------|-------------------|
| Column in WHERE/JOIN | Table has very few rows |
| Column in ORDER BY | Column has low cardinality (e.g., boolean) |
| Column in GROUP BY | Column is rarely queried |
| Foreign key columns | Table has heavy writes |

### FoodExpress Indexes

```sql
-- Essential indexes for FoodExpress
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_restaurant ON orders(restaurant_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_items_order ON order_items(order_id);
CREATE INDEX idx_restaurants_cuisine ON restaurants(cuisine);
```

---

## Backup and Recovery

### mysqldump

```bash
# Full database backup
mysqldump -u root -p foodexpress > foodexpress_backup.sql

# Backup specific tables
mysqldump -u root -p foodexpress orders order_items > orders_backup.sql

# Backup with structure only (no data)
mysqldump -u root -p --no-data foodexpress > schema_only.sql

# Backup with data only (no structure)
mysqldump -u root -p --no-create-info foodexpress > data_only.sql
```

### Restore

```bash
# Restore from backup
mysql -u root -p foodexpress < foodexpress_backup.sql

# Restore to a new database
mysql -u root -p -e "CREATE DATABASE foodexpress_restored"
mysql -u root -p foodexpress_restored < foodexpress_backup.sql
```

### Backup Best Practices

| Practice | Why |
|----------|-----|
| Schedule daily backups | Minimize data loss window |
| Test restores regularly | Backups are worthless if they cannot be restored |
| Store backups off-site | Protect against hardware failure |
| Use binary logs for point-in-time recovery | Recover to any point, not just last backup |

---

## Transactions

### ACID Properties

| Property | Meaning | Example |
|----------|---------|---------|
| **A**tomicity | All or nothing | Transfer money: debit AND credit both succeed or both fail |
| **C**onsistency | Valid state to valid state | Order total matches sum of items |
| **I**solation | Concurrent transactions don't interfere | Two customers ordering same last item |
| **D**urability | Committed data survives crashes | Power failure after COMMIT -- data is safe |

### Transaction Syntax

```sql
-- FoodExpress: Place an order (atomic)
START TRANSACTION;

INSERT INTO orders (customer_id, restaurant_id, status, total_amount)
VALUES (1, 2, 'placed', 598.00);

SET @order_id = LAST_INSERT_ID();

INSERT INTO order_items (order_id, item_name, quantity, unit_price)
VALUES (@order_id, 'Margherita Pizza', 2, 299.00);

-- If everything succeeded:
COMMIT;

-- If something went wrong:
-- ROLLBACK;
```

---

## Transaction Failure Handling

### Common Transaction Failures

| Failure | Cause | Impact |
|---------|-------|--------|
| Deadlock | Two transactions wait for each other's locks | One is rolled back automatically |
| Lock timeout | Transaction waits too long for a lock | Error: lock wait timeout |
| Constraint violation | FK/unique violation mid-transaction | Insert/update fails |
| Connection drop | Network or server crash | Uncommitted work is lost |

### Deadlock Example

```sql
-- Transaction A:                    Transaction B:
-- UPDATE orders SET ...             UPDATE order_items SET ...
--   WHERE order_id = 1;               WHERE order_id = 2;
-- UPDATE order_items SET ...        UPDATE orders SET ...
--   WHERE order_id = 2;               WHERE order_id = 1;
-- DEADLOCK! A waits for B, B waits for A
```

### Prevention

```sql
-- Always access tables in the same order
-- Keep transactions short
-- Use appropriate isolation levels:
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

---

## MySQL Clustering

### Replication Architecture

```
+--------+     writes     +--------+
| Client | ------------> | Primary |
+--------+               +----+----+
                              |
              +---------------+---------------+
              | replication   | replication   |
              v               v               v
         +---------+    +---------+    +---------+
         | Replica |    | Replica |    | Replica |
         |   (R1)  |    |   (R2)  |    |   (R3)  |
         +---------+    +---------+    +---------+
              ^               ^               ^
              |   reads       |   reads       |   reads
         +--------+      +--------+      +--------+
         | Client |      | Client |      | Client |
         +--------+      +--------+      +--------+
```

### Clustering Concepts

| Concept | Description |
|---------|-------------|
| Primary-Replica | One writer, multiple readers |
| Read replicas | Scale read-heavy workloads |
| Failover | Promote replica to primary on failure |
| Replication lag | Replicas may be seconds behind primary |
| Split-brain | Two nodes think they are primary -- dangerous |

---

## FoodExpress Database Operations

### Common Sustain Queries

```sql
-- 1. Daily order summary
SELECT DATE(order_date) AS day,
       COUNT(*) AS order_count,
       SUM(total_amount) AS revenue
FROM orders
WHERE order_date >= CURDATE() - INTERVAL 7 DAY
GROUP BY DATE(order_date)
ORDER BY day;

-- 2. Top 5 customers by lifetime value
SELECT c.name, SUM(o.total_amount) AS lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'delivered'
GROUP BY c.customer_id, c.name
ORDER BY lifetime_value DESC
LIMIT 5;

-- 3. Most popular items
SELECT oi.item_name,
       SUM(oi.quantity) AS total_ordered,
       SUM(oi.subtotal) AS total_revenue
FROM order_items oi
GROUP BY oi.item_name
ORDER BY total_ordered DESC
LIMIT 10;
```

---

## FoodExpress Database Operations (continued)

```sql
-- 4. Cancelled order rate by restaurant
SELECT r.name,
       COUNT(*) AS total_orders,
       SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END)
             * 100.0 / COUNT(*), 1) AS cancel_rate
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.restaurant_id, r.name
ORDER BY cancel_rate DESC;

-- 5. Stuck orders (placed > 30 min ago, not confirmed)
SELECT o.order_id, c.name, r.name AS restaurant,
       o.order_date, o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
WHERE o.status = 'placed'
  AND o.order_date < NOW() - INTERVAL 30 MINUTE;

-- 6. Revenue by cuisine type
SELECT r.cuisine,
       COUNT(o.order_id) AS order_count,
       SUM(o.total_amount) AS total_revenue
FROM orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
GROUP BY r.cuisine
ORDER BY total_revenue DESC;
```

---

## SQL Execution Order

```
SELECT   columns        -- 5. Pick columns
FROM     table           -- 1. Choose table
JOIN     other_table     -- 2. Combine tables
WHERE    condition       -- 3. Filter rows
GROUP BY column          -- 4. Group rows
HAVING   group_condition -- 6. Filter groups
ORDER BY column          -- 7. Sort results
LIMIT    n               -- 8. Limit output
```

Understanding this order explains:
- Why you **cannot** use column aliases in WHERE (alias defined in step 5, WHERE is step 3)
- Why you **can** use column aliases in ORDER BY (step 7 comes after step 5)
- Why HAVING exists separately from WHERE (different steps)

---

## Common SQL Mistakes in Sustain Work

| Mistake | Example | Fix |
|---------|---------|-----|
| Missing WHERE on UPDATE/DELETE | `UPDATE orders SET status='cancelled'` | Always add WHERE clause |
| Comparing with NULL using `=` | `WHERE phone = NULL` | `WHERE phone IS NULL` |
| GROUP BY missing columns | `SELECT name, COUNT(*) FROM ...` (no GROUP BY) | Add `GROUP BY name` |
| String vs number comparison | `WHERE status = 0` (status is ENUM) | `WHERE status = 'placed'` |
| Case sensitivity | `WHERE name = 'pizza palace'` | Use `LOWER()` or `COLLATE` |
| Cartesian product | `FROM orders, customers` (no JOIN condition) | Always specify JOIN ON |
| Ignoring index hints | Slow query on indexed column | Check EXPLAIN output |

---

## Key Takeaways

| Concept | Key Lesson |
|---------|------------|
| CRUD | INSERT, SELECT, UPDATE, DELETE -- always use WHERE for mutations |
| Filtering | WHERE for rows, HAVING for groups, LIKE for patterns |
| Joins | INNER JOIN for matching rows, LEFT JOIN to include unmatched |
| Sub-Queries | Nest queries for complex conditions; correlated sub-queries for per-row logic |
| NULL | Use IS NULL, COALESCE; NULL propagates in calculations |
| Indexing | Index columns used in WHERE, JOIN, ORDER BY; check with EXPLAIN |
| Transactions | ACID guarantees; keep transactions short; handle deadlocks |
| Backup | mysqldump regularly; test restores; use binary logs for PITR |
| Clustering | Primary-Replica for read scaling; handle replication lag |

> **Next: Module 13 -- QE/QC: Quality Engineering and Quality Control fundamentals for sustain teams.**
