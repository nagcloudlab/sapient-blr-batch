


-- public class Event {

--     public Long id;
--     public String name;
--     public String venue;
--     public double price;
--     public int availableSeats;
-- }

CREATE TABLE events (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    venue VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    available_seats INT NOT NULL
);

INSERT INTO events (id, name, venue, price, available_seats) VALUES
(1, 'Concert A', 'Venue A', 50.00, 100),
(2, 'Concert B', 'Venue B', 75.00, 150),
(3, 'Concert C', 'Venue C', 100.00, 200);