-- FoodExpress Inventory Management
-- This SQL script handles inventory updates after order placement.
--
-- CONTAINS BUGS - Find and fix them!

-- ============================================
-- Table: menu_items (for reference)
-- ============================================
-- CREATE TABLE menu_items (
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     name VARCHAR(100) NOT NULL,
--     price DECIMAL(10,2) NOT NULL,
--     category VARCHAR(50),
--     stock_quantity INT DEFAULT 0,
--     is_available BOOLEAN DEFAULT TRUE
-- );

-- ============================================
-- Table: orders (for reference)
-- ============================================
-- CREATE TABLE orders (
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     customer_id INT NOT NULL,
--     order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     total_amount DECIMAL(10,2),
--     status VARCHAR(20) DEFAULT 'PENDING'
-- );

-- ============================================
-- Table: order_items (for reference)
-- ============================================
-- CREATE TABLE order_items (
--     id INT PRIMARY KEY AUTO_INCREMENT,
--     order_id INT NOT NULL,
--     menu_item_id INT NOT NULL,
--     quantity INT NOT NULL,
--     unit_price DECIMAL(10,2) NOT NULL,
--     FOREIGN KEY (order_id) REFERENCES orders(id),
--     FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
-- );

-- ============================================
-- Procedure: Process a new order
-- BUG: Inventory is NOT decremented after order placement!
-- The INSERT into order_items works, but stock_quantity in
-- menu_items is never updated.
-- ============================================

-- Step 1: Insert the order
INSERT INTO orders (customer_id, total_amount, status)
VALUES (101, 630.00, 'CONFIRMED');

-- Get the last inserted order ID
SET @new_order_id = LAST_INSERT_ID();

-- Step 2: Insert order items
INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price)
VALUES (@new_order_id, 1, 1, 350.00);  -- Butter Chicken x1

INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price)
VALUES (@new_order_id, 2, 1, 280.00);  -- Paneer Tikka x1

-- BUG: Missing Step 3!
-- The inventory (stock_quantity) in menu_items is never decremented.
-- After placing an order, the stock should be reduced.
-- Without this UPDATE, menu_items still shows the old stock count,
-- allowing overselling of items.

-- Step 3 is MISSING: Should have UPDATE statements like:
-- UPDATE menu_items SET stock_quantity = stock_quantity - <qty>
-- WHERE id = <menu_item_id> AND stock_quantity >= <qty>;

-- Step 4: Check for out-of-stock items and mark as unavailable
-- BUG: This runs but has no effect because stock was never decremented
UPDATE menu_items
SET is_available = FALSE
WHERE stock_quantity <= 0;

-- Step 5: Verify the order (for debugging)
SELECT o.id AS order_id,
       o.total_amount,
       o.status,
       oi.menu_item_id,
       mi.name,
       oi.quantity,
       mi.stock_quantity AS remaining_stock
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN menu_items mi ON oi.menu_item_id = mi.id
WHERE o.id = @new_order_id;
