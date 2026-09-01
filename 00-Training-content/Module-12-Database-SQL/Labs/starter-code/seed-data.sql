-- ============================================================
-- FoodExpress Sample Data
-- ============================================================
USE foodexpress;

-- ------------------------------------------------------------
-- 8 Customers
-- ------------------------------------------------------------
INSERT INTO customers (first_name, last_name, email, phone, address) VALUES
('Aarav',   'Sharma',  'aarav.sharma@email.com',   '9876543210', '12 MG Road'),
('Priya',   'Patel',   'priya.patel@email.com',    '9876543211', '45 Brigade Road'),
('Rohan',   'Gupta',   'rohan.gupta@email.com',    '9876543212', '78 Koramangala 5th Block'),
('Sneha',   'Reddy',   'sneha.reddy@email.com',    '9876543213', '23 Indiranagar'),
('Vikram',  'Nair',    'vikram.nair@email.com',     '9876543214', '56 Whitefield'),
('Ananya',  'Iyer',    'ananya.iyer@email.com',     '9876543215', '89 Jayanagar'),
('Karthik', 'Das',     'karthik.das@email.com',     '9876543216', '34 HSR Layout'),
('Meera',   'Singh',   'meera.singh@email.com',     NULL,         '67 Electronic City');

-- ------------------------------------------------------------
-- 6 Restaurants
-- ------------------------------------------------------------
INSERT INTO restaurants (name, cuisine, rating, address) VALUES
('Biryani Blues',      'Indian',     4.5, '10 MG Road'),
('Pizza Paradise',     'Italian',    4.2, '22 Brigade Road'),
('Dragon Wok',         'Chinese',    4.0, '33 Koramangala'),
('Dosa Factory',       'South Indian', 4.7, '44 Jayanagar'),
('Burger Barn',        'American',   3.9, '55 Whitefield'),
('Sushi Spot',         'Japanese',   4.3, '66 Indiranagar');

-- ------------------------------------------------------------
-- 22 Menu Items
-- ------------------------------------------------------------
INSERT INTO menu_items (restaurant_id, name, price, category) VALUES
-- Biryani Blues (1)
(1, 'Chicken Biryani',      250.00, 'Main Course'),
(1, 'Mutton Biryani',       350.00, 'Main Course'),
(1, 'Veg Biryani',          180.00, 'Main Course'),
(1, 'Raita',                 50.00, 'Sides'),
-- Pizza Paradise (2)
(2, 'Margherita Pizza',     300.00, 'Pizza'),
(2, 'Pepperoni Pizza',      400.00, 'Pizza'),
(2, 'Garlic Bread',         120.00, 'Sides'),
(2, 'Pasta Alfredo',        280.00, 'Pasta'),
-- Dragon Wok (3)
(3, 'Chicken Fried Rice',   220.00, 'Main Course'),
(3, 'Veg Manchurian',       180.00, 'Starters'),
(3, 'Spring Rolls',         150.00, 'Starters'),
(3, 'Hakka Noodles',        200.00, 'Main Course'),
-- Dosa Factory (4)
(4, 'Masala Dosa',          120.00, 'Main Course'),
(4, 'Rava Dosa',            130.00, 'Main Course'),
(4, 'Idli Vada Combo',       90.00, 'Combo'),
(4, 'Filter Coffee',         40.00, 'Beverages'),
-- Burger Barn (5)
(5, 'Classic Burger',       200.00, 'Burgers'),
(5, 'Cheese Burger',        250.00, 'Burgers'),
(5, 'French Fries',         100.00, 'Sides'),
(5, 'Milkshake',            150.00, 'Beverages'),
-- Sushi Spot (6)
(6, 'California Roll',      350.00, 'Sushi'),
(6, 'Salmon Nigiri',        400.00, 'Sushi');

-- ------------------------------------------------------------
-- 12 Orders
-- ------------------------------------------------------------
INSERT INTO orders (customer_id, restaurant_id, order_date, status, delivery_fee, discount, total_amount, notes) VALUES
(1, 1, '2026-07-01 12:30:00', 'delivered',  30.00,  0.00,  580.00, NULL),
(2, 2, '2026-07-01 19:00:00', 'delivered',  30.00, 50.00,  700.00, 'Extra cheese please'),
(3, 3, '2026-07-02 13:15:00', 'delivered',  30.00,  0.00,  600.00, NULL),
(4, 4, '2026-07-02 08:00:00', 'delivered',   0.00,  0.00,  250.00, NULL),
(1, 1, '2026-07-03 12:00:00', 'delivered',  30.00, 20.00,  460.00, 'Less spicy'),
(5, 5, '2026-07-05 20:00:00', 'delivered',  30.00,  0.00,  580.00, NULL),
(6, 6, '2026-07-07 19:30:00', 'cancelled',  30.00,  0.00,  780.00, NULL),
(2, 1, '2026-07-08 13:00:00', 'delivered',  30.00,  0.00,  330.00, NULL),
(3, 4, '2026-07-10 08:30:00', 'delivered',   0.00, 10.00,  240.00, NULL),
(7, 2, '2026-07-12 20:00:00', 'preparing',  30.00,  0.00,  830.00, NULL),
(4, 3, '2026-07-14 12:45:00', 'dispatched', 30.00,  0.00,  400.00, NULL),
(8, 5, '2026-07-15 18:00:00', 'placed',     30.00,  0.00,  330.00, 'No onions');

-- ------------------------------------------------------------
-- Order Items
-- ------------------------------------------------------------
INSERT INTO order_items (order_id, item_id, quantity, unit_price) VALUES
-- Order 1: Chicken Biryani x2 + Raita x1
(1,  1, 2, 250.00),
(1,  4, 1,  50.00),
-- Order 2: Margherita + Pepperoni + Garlic Bread
(2,  5, 1, 300.00),
(2,  6, 1, 400.00),
(2,  7, 1, 120.00),
-- Order 3: Fried Rice x2 + Spring Rolls x1
(3,  9, 2, 220.00),
(3, 11, 1, 150.00),
-- Order 4: Masala Dosa + Idli Vada + Coffee
(4, 13, 1, 120.00),
(4, 15, 1,  90.00),
(4, 16, 1,  40.00),
-- Order 5: Chicken Biryani + Veg Biryani + Raita
(5,  1, 1, 250.00),
(5,  3, 1, 180.00),
(5,  4, 1,  50.00),
-- Order 6: Classic Burger + Cheese Burger + Fries + Milkshake
(6, 17, 1, 200.00),
(6, 18, 1, 250.00),
(6, 19, 1, 100.00),
(6, 20, 1, 150.00),
-- Order 7: California Roll x2 + Salmon Nigiri
(7, 21, 2, 350.00),
(7, 22, 1, 400.00),
-- Order 8: Mutton Biryani + Raita
(8,  2, 1, 350.00),
(8,  4, 1,  50.00),
-- Order 9: Rava Dosa + Idli Vada + Coffee
(9, 14, 1, 130.00),
(9, 15, 1,  90.00),
(9, 16, 1,  40.00),
-- Order 10: Pepperoni x2 + Pasta Alfredo
(10, 6, 2, 400.00),
(10, 8, 1, 280.00),
-- Order 11: Veg Manchurian + Hakka Noodles
(11, 10, 1, 180.00),
(11, 12, 1, 200.00),
-- Order 12: Cheese Burger + Fries
(12, 18, 1, 250.00),
(12, 19, 1, 100.00);
