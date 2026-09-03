-- FoodExpress Database Initialization Script
-- Mount to /docker-entrypoint-initdb.d/ for auto-execution

CREATE DATABASE IF NOT EXISTS foodexpress;
USE foodexpress;

CREATE TABLE IF NOT EXISTS restaurants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cuisine VARCHAR(100),
    rating DECIMAL(2,1) DEFAULT 0.0,
    delivery_time VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'PLACED',
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO restaurants (name, cuisine, rating, delivery_time) VALUES
('Spice Garden', 'Indian', 4.5, '30-45 min'),
('Pizza Palace', 'Italian', 4.2, '25-35 min'),
('Sushi House', 'Japanese', 4.7, '40-50 min');
