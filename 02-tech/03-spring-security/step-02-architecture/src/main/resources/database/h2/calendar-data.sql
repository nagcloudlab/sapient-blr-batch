-- Users (passwords stored in plain text - THIS IS INSECURE!)
INSERT INTO calendar_users(id, email, password, first_name, last_name) VALUES (0, 'user1@example.com', 'user1', 'User', 'One');
INSERT INTO calendar_users(id, email, password, first_name, last_name) VALUES (1, 'admin1@example.com', 'admin1', 'Admin', 'One');
INSERT INTO calendar_users(id, email, password, first_name, last_name) VALUES (2, 'user2@example.com', 'user2', 'User', 'Two');

-- Events
INSERT INTO events(id, date_when, summary, description, owner, attendee) VALUES (100, '2025-01-15 18:00:00', 'Birthday Party', 'This is going to be a great birthday party!', 0, 1);
INSERT INTO events(id, date_when, summary, description, owner, attendee) VALUES (101, '2025-02-20 14:00:00', 'Conference Call', 'Discuss the quarterly numbers with the team', 2, 0);
INSERT INTO events(id, date_when, summary, description, owner, attendee) VALUES (102, '2025-03-10 12:30:00', 'Lunch Meeting', 'Casual lunch to discuss the new project plans', 1, 2);
