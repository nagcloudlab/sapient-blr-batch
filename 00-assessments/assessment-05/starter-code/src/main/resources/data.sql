-- Sample data for QuickTicket

-- Users
INSERT INTO users (name, email) VALUES ('Alice Johnson', 'alice@example.com');
INSERT INTO users (name, email) VALUES ('Bob Smith', 'bob@example.com');
INSERT INTO users (name, email) VALUES ('Charlie Brown', 'charlie@example.com');
INSERT INTO users (name, email) VALUES ('Diana Prince', 'diana@example.com');
INSERT INTO users (name, email) VALUES ('Eve Wilson', 'eve@example.com');

-- Events
INSERT INTO events (name, category, date, venue, price, capacity) VALUES ('Summer Concert', 'Music', '2026-09-15 19:00:00', 'City Arena', 75.00, 500);
INSERT INTO events (name, category, date, venue, price, capacity) VALUES ('Tech Conference', 'Technology', '2026-10-01 09:00:00', 'Convention Center', 150.00, 300);
INSERT INTO events (name, category, date, venue, price, capacity) VALUES ('Comedy Night', 'Entertainment', '2026-09-20 20:00:00', 'Laugh Lounge', 40.00, 100);
INSERT INTO events (name, category, date, venue, price, capacity) VALUES ('Art Exhibition', 'Art', '2026-11-05 10:00:00', 'Gallery Hall', 25.00, 200);
INSERT INTO events (name, category, date, venue, price, capacity) VALUES ('Concert Under Stars', 'Music', '2026-09-25 21:00:00', 'Open Air Theatre', 90.00, 400);

-- Bookings (mix of confirmed, pending, cancelled)
INSERT INTO bookings (user_id, event_id, status, seats, total_amount) VALUES (1, 1, 'confirmed', 2, 150.00);
INSERT INTO bookings (user_id, event_id, status, seats, total_amount) VALUES (2, 1, 'confirmed', 4, 300.00);
INSERT INTO bookings (user_id, event_id, status, seats, total_amount) VALUES (3, 1, 'cancelled', 1, 75.00);
INSERT INTO bookings (user_id, event_id, status, seats, total_amount) VALUES (1, 2, 'confirmed', 1, 150.00);
INSERT INTO bookings (user_id, event_id, status, seats, total_amount) VALUES (4, 2, 'confirmed', 2, 300.00);
INSERT INTO bookings (user_id, event_id, status, seats, total_amount) VALUES (2, 3, 'confirmed', 3, 120.00);
INSERT INTO bookings (user_id, event_id, status, seats, total_amount) VALUES (5, 3, 'pending', 2, 80.00);
INSERT INTO bookings (user_id, event_id, status, seats, total_amount) VALUES (3, 5, 'confirmed', 2, 180.00);
INSERT INTO bookings (user_id, event_id, status, seats, total_amount) VALUES (1, 5, 'cancelled', 1, 90.00);

-- Payments (only for confirmed bookings)
INSERT INTO payments (booking_id, amount, method) VALUES (1, 150.00, 'credit_card');
INSERT INTO payments (booking_id, amount, method) VALUES (2, 300.00, 'upi');
INSERT INTO payments (booking_id, amount, method) VALUES (4, 150.00, 'credit_card');
INSERT INTO payments (booking_id, amount, method) VALUES (5, 300.00, 'debit_card');
INSERT INTO payments (booking_id, amount, method) VALUES (6, 120.00, 'upi');
INSERT INTO payments (booking_id, amount, method) VALUES (8, 180.00, 'credit_card');
