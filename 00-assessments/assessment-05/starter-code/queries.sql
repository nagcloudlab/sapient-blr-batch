-- =============================================================
-- QuickTicket Database Queries
-- Database: quickticket
-- =============================================================

-- =============================================================
-- DEF-101 (10 pts): Fix the revenue report query below.
--
-- Current issues:
--   1. Excludes events with zero bookings (they should appear with 0 revenue)
--   2. Includes cancelled bookings in revenue (only confirmed should count)
--   3. Returns aggregate error because results are not grouped
--   4. Shows all events regardless of revenue (should only show revenue > 1000)
--
-- Expected columns: event_name, total_revenue
-- Sorted descending by total_revenue.
-- =============================================================

SELECT
    e.id,
    e.name,
    SUM(p.amount) AS total_revenue
FROM events e
INNER JOIN bookings b ON b.event_id = e.id
INNER JOIN payments p ON p.booking_id = b.id
ORDER BY total_revenue DESC;


-- =============================================================
-- DEF-102 (10 pts): Write a NEW query to find the top 3 users
-- by total spending on confirmed bookings.
--
-- Expected columns: user_name, email, total_spent
-- Sorted descending by total_spent, limited to top 3.
-- =============================================================

-- YOUR QUERY HERE


-- =============================================================
-- DEF-103 (10 pts): Fix the slow event search query below.
--
-- Issues:
--   1. Uses SELECT * (should select specific columns)
--   2. LIKE pattern uses leading wildcard preventing index usage
--
-- Rewrite the query with proper column selection and add a
-- SQL comment explaining why the pattern is slow and what
-- alternatives exist.
-- =============================================================

SELECT * FROM events WHERE name LIKE '%concert%';

-- YOUR FIXED QUERY AND EXPLANATION HERE
