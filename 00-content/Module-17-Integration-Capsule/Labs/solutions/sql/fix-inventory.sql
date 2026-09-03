-- FoodExpress Inventory Management (FIXED)
-- This SQL script handles inventory updates after order placement.
--
-- ALL BUGS FIXED

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
-- Procedure: Process a new order (FIXED)
-- FIX: Inventory is now properly decremented after order placement.
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

-- FIX: Step 3 - Decrement inventory for each ordered item
-- This prevents overselling by reducing stock_quantity
UPDATE menu_items
SET stock_quantity = stock_quantity - 1
WHERE id = 1 AND stock_quantity >= 1;  -- Butter Chicken: reduce by 1

UPDATE menu_items
SET stock_quantity = stock_quantity - 1
WHERE id = 2 AND stock_quantity >= 1;  -- Paneer Tikka: reduce by 1

-- Step 4: Check for out-of-stock items and mark as unavailable
-- Now this works correctly because stock was decremented in Step 3
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
