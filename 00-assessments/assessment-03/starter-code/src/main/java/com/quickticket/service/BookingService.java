package com.quickticket.service;

import com.quickticket.model.Event;
import org.springframework.stereotype.Service;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

/**
 * QuickTicket — Booking service.
 */
@Service
public class BookingService {

    public List<Event> removeSoldOut(List<Event> events) {
        events.removeIf(e -> e.getAvailableSeats() <= 0);
        return events;
    }

    public List<Event> sortByPrice(List<Event> events) {
        Collections.sort(events, Comparator.comparingDouble(Event::getPrice));
        return events;
    }

    public Event findByName(Connection conn, String name) throws SQLException {
        String sql = "SELECT * FROM events WHERE name = ?";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, name);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return new Event(
                        rs.getLong("id"),
                        rs.getString("name"),
                        rs.getString("venue"),
                        rs.getDouble("price"),
                        rs.getInt("available_seats")
                    );
                }
            }
        }
        return null;
    }

    public void bookTicket(Connection conn, Long eventId, Long userId) throws SQLException {
        boolean originalAutoCommit = conn.getAutoCommit();
        conn.setAutoCommit(false);

        try {
            try (PreparedStatement ps1 = conn.prepareStatement(
                "UPDATE events SET available_seats = available_seats - 1 WHERE id = ? AND available_seats > 0")) {
                ps1.setLong(1, eventId);
                int updatedRows = ps1.executeUpdate();
                if (updatedRows == 0) {
                    throw new SQLException("No seats available or event not found for event id: " + eventId);
                }
            }

            try (PreparedStatement ps2 = conn.prepareStatement(
                "INSERT INTO bookings (event_id, user_id, booked_at) VALUES (?, ?, NOW())")) {
                ps2.setLong(1, eventId);
                ps2.setLong(2, userId);
                ps2.executeUpdate();
            }

            conn.commit();
        } catch (SQLException ex) {
            conn.rollback();
            throw ex;
        } finally {
            conn.setAutoCommit(originalAutoCommit);
        }
    }
}
