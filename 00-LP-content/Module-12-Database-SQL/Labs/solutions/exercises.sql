-- ============================================================
-- FoodExpress SQL Exercises (Solutions)
-- ============================================================
USE foodexpress;

-- ============================================================
-- Exercise 1: Weekly Revenue Report
-- ============================================================
SELECT DATE(order_date - INTERVAL (WEEKDAY(order_date)) DAY) AS week_start,
       COUNT(*)            AS order_count,
       SUM(total_amount)   AS total_revenue
FROM   orders
WHERE  status = 'delivered'
GROUP  BY week_start
ORDER  BY week_start;

-- Alternative using YEARWEEK:
-- SELECT YEARWEEK(order_date, 1) AS year_week,
--        COUNT(*)                AS order_count,
--        SUM(total_amount)       AS total_revenue
-- FROM   orders
-- WHERE  status = 'delivered'
-- GROUP  BY year_week
-- ORDER  BY year_week;


-- ============================================================
-- Exercise 2: Create Composite Index
-- ============================================================
CREATE INDEX idx_orders_customer_date
    ON orders (customer_id, order_date);

-- Verify index usage:
EXPLAIN
SELECT * FROM orders
WHERE  customer_id = 1
  AND  order_date BETWEEN '2026-07-01' AND '2026-07-31';
-- EXPLAIN should show key = idx_orders_customer_date, type = range or ref


-- ============================================================
-- Exercise 3: Order Placement Transaction
-- ============================================================
-- First, add a stock column to menu_items (if not exists):
ALTER TABLE menu_items ADD COLUMN stock INT DEFAULT 100;

DELIMITER //

CREATE PROCEDURE place_order()
BEGIN
    DECLARE new_order_id INT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Transaction rolled back due to error' AS result;
    END;

    START TRANSACTION;

    -- Step 1: Create the order
    INSERT INTO orders (customer_id, restaurant_id, status, delivery_fee, discount, total_amount)
    VALUES (1, 2, 'placed', 30.00, 0.00, 450.00);

    SET new_order_id = LAST_INSERT_ID();

    -- Step 2: Add order items
    INSERT INTO order_items (order_id, item_id, quantity, unit_price)
    VALUES (new_order_id, 5, 1, 300.00);   -- Margherita Pizza

    INSERT INTO order_items (order_id, item_id, quantity, unit_price)
    VALUES (new_order_id, 7, 1, 120.00);   -- Garlic Bread

    -- Step 3: Decrement stock
    UPDATE menu_items SET stock = stock - 1 WHERE item_id = 5;
    UPDATE menu_items SET stock = stock - 1 WHERE item_id = 7;

    COMMIT;
    SELECT CONCAT('Order ', new_order_id, ' placed successfully') AS result;
END //

DELIMITER ;

-- Run the procedure:
CALL place_order();
