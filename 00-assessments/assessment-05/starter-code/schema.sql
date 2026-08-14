-- =============================================================
-- QuickTicket Event Booking -- Database Schema
-- Database: quickticket
-- =============================================================
-- TASK 2a (20 pts): Fix the 4 schema defects below.
-- DEF-201, DEF-202, DEF-203, DEF-204
-- =============================================================

CREATE TABLE users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    email      VARCHAR(255) NOT NULL,
    name       VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    category   VARCHAR(100) NOT NULL,
    date       TIMESTAMP   NOT NULL,
    venue      VARCHAR(255) NOT NULL,
    price      DECIMAL(10, 2) NOT NULL,
    capacity   INT NOT NULL CHECK (capacity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DEF-201, DEF-202: See PROBLEM.md for defect details.
CREATE TABLE bookings (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    event_id     INT NOT NULL,
    status       VARCHAR(50) NOT NULL DEFAULT 'pending',
    seats        INT NOT NULL CHECK (seats > 0),
    total_amount DECIMAL(10, 2) NOT NULL,
    booked_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DEF-203, DEF-204: See PROBLEM.md for defect details.

CREATE TABLE payments (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    amount     DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    method     VARCHAR(50) NOT NULL,
    paid_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
