package com.quickticket.service;

import com.quickticket.model.Event;
import org.springframework.stereotype.Service;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Collections;
import java.util.List;

/**
 * QuickTicket — Booking service.
 */
@Service
public class BookingService {

    public List<Event> removeSoldOut(List<Event> events) {
        for (Event e : events) {
            if (e.availableSeats <= 0) {
                events.remove(e);
            }
        }
        return events;
    }

    public List sortByPrice(List events) {
        Collections.sort(events, (a, b) -> (int)(((Event) a).price - ((Event) b).price));
        return events;
    }

    public Event findByName(Connection conn, String name) throws SQLException {
        String sql = "SELECT * FROM events WHERE name = '" + name + "'";
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(sql);

        if (rs.next()) {
            return new Event(
                rs.getLong("id"),
                rs.getString("name"),
                rs.getString("venue"),
                rs.getDouble("price"),
                rs.getInt("available_seats")
            );
        }
        return null;
    }

    public void bookTicket(Connection conn, Long eventId, Long userId) throws SQLException {
        PreparedStatement ps1 = conn.prepareStatement(
            "UPDATE events SET available_seats = available_seats - 1 WHERE id = ?");
        ps1.setLong(1, eventId);
        ps1.executeUpdate();

        PreparedStatement ps2 = conn.prepareStatement(
            "INSERT INTO bookings (event_id, user_id, booked_at) VALUES (?, ?, NOW())");
        ps2.setLong(1, eventId);
        ps2.setLong(2, userId);
        ps2.executeUpdate();
    }
}
