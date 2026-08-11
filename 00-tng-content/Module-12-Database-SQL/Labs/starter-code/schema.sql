-- ============================================================
-- FoodExpress Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS foodexpress;
USE foodexpress;

-- ------------------------------------------------------------
-- Customers
-- ------------------------------------------------------------
CREATE TABLE customers (
    customer_id   INT            AUTO_INCREMENT PRIMARY KEY,
    first_name    VARCHAR(50)    NOT NULL,
    last_name     VARCHAR(50)    NOT NULL,
    email         VARCHAR(100)   NOT NULL UNIQUE,
    phone         VARCHAR(15),
    address       VARCHAR(200),
    city          VARCHAR(50)    DEFAULT 'Bangalore',
    created_at    DATETIME       DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Restaurants
-- ------------------------------------------------------------
CREATE TABLE restaurants (
    restaurant_id INT            AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100)   NOT NULL,
    cuisine       VARCHAR(50)    NOT NULL,
    rating        DECIMAL(2,1)   DEFAULT 0.0,
    address       VARCHAR(200),
    city          VARCHAR(50)    DEFAULT 'Bangalore',
    is_active     BOOLEAN        DEFAULT TRUE,
    created_at    DATETIME       DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Menu Items
-- ------------------------------------------------------------
CREATE TABLE menu_items (
    item_id       INT            AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT            NOT NULL,
    name          VARCHAR(100)   NOT NULL,
    description   VARCHAR(255),
    price         DECIMAL(8,2)   NOT NULL,
    category      VARCHAR(50),
    is_available  BOOLEAN        DEFAULT TRUE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- ------------------------------------------------------------
-- Orders
-- ------------------------------------------------------------
CREATE TABLE orders (
    order_id      INT            AUTO_INCREMENT PRIMARY KEY,
    customer_id   INT            NOT NULL,
    restaurant_id INT            NOT NULL,
    order_date    DATETIME       DEFAULT CURRENT_TIMESTAMP,
    status        ENUM('placed','confirmed','preparing','dispatched','delivered','cancelled')
                                 DEFAULT 'placed',
    delivery_fee  DECIMAL(6,2)   DEFAULT 30.00,
    discount      DECIMAL(6,2)   DEFAULT 0.00,
    total_amount  DECIMAL(10,2),
    notes         VARCHAR(255),
    FOREIGN KEY (customer_id)   REFERENCES customers(customer_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

-- ------------------------------------------------------------
-- Order Items (line items within an order)
-- ------------------------------------------------------------
CREATE TABLE order_items (
    order_item_id INT            AUTO_INCREMENT PRIMARY KEY,
    order_id      INT            NOT NULL,
    item_id       INT            NOT NULL,
    quantity      INT            NOT NULL DEFAULT 1,
    unit_price    DECIMAL(8,2)   NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id)  REFERENCES menu_items(item_id)
);
