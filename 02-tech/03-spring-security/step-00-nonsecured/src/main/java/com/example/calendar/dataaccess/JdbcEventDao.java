package com.example.calendar.dataaccess;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Calendar;
import java.util.List;

import com.example.calendar.domain.CalendarUser;
import com.example.calendar.domain.Event;

import org.springframework.jdbc.core.JdbcOperations;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
public class JdbcEventDao implements EventDao {

    private static final String EVENT_QUERY =
            "SELECT e.id, e.summary, e.description, e.date_when, " +
            "o.id AS o_id, o.first_name AS o_fn, o.last_name AS o_ln, o.email AS o_email, o.password AS o_pw, " +
            "a.id AS a_id, a.first_name AS a_fn, a.last_name AS a_ln, a.email AS a_email, a.password AS a_pw " +
            "FROM events e " +
            "JOIN calendar_users o ON e.owner = o.id " +
            "JOIN calendar_users a ON e.attendee = a.id";

    private final JdbcOperations jdbc;

    public JdbcEventDao(JdbcOperations jdbc) {
        this.jdbc = jdbc;
    }

    @Override
    @Transactional(readOnly = true)
    public Event getEvent(int eventId) {
        return jdbc.queryForObject(EVENT_QUERY + " WHERE e.id = ?", EVENT_MAPPER, eventId);
    }

    @Override
    public int createEvent(Event event) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(
                    "INSERT INTO events (date_when, summary, description, owner, attendee) VALUES (?, ?, ?, ?, ?)",
                    new String[]{"id"});
            ps.setTimestamp(1, new java.sql.Timestamp(event.dateWhen().getTimeInMillis()));
            ps.setString(2, event.summary());
            ps.setString(3, event.description());
            ps.setInt(4, event.owner().getId());
            ps.setInt(5, event.attendee().getId());
            return ps;
        }, keyHolder);
        return keyHolder.getKey().intValue();
    }

    @Override
    @Transactional(readOnly = true)
    public List<Event> findForUser(int userId) {
        return jdbc.query(EVENT_QUERY + " WHERE e.owner = ? OR e.attendee = ? ORDER BY e.id",
                EVENT_MAPPER, userId, userId);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Event> getEvents() {
        return jdbc.query(EVENT_QUERY + " ORDER BY e.id", EVENT_MAPPER);
    }

    private static final RowMapper<Event> EVENT_MAPPER = (ResultSet rs, int rowNum) -> {
        CalendarUser owner = new CalendarUser(
                rs.getInt("o_id"), rs.getString("o_fn"), rs.getString("o_ln"),
                rs.getString("o_email"), rs.getString("o_pw"));
        CalendarUser attendee = new CalendarUser(
                rs.getInt("a_id"), rs.getString("a_fn"), rs.getString("a_ln"),
                rs.getString("a_email"), rs.getString("a_pw"));
        Calendar when = Calendar.getInstance();
        when.setTime(rs.getTimestamp("date_when"));
        return new Event(rs.getInt("id"), rs.getString("summary"),
                rs.getString("description"), when, owner, attendee);
    };
}
