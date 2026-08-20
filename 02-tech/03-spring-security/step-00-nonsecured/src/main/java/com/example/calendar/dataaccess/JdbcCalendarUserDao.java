package com.example.calendar.dataaccess;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

import com.example.calendar.domain.CalendarUser;

import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.jdbc.core.JdbcOperations;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
public class JdbcCalendarUserDao implements CalendarUserDao {

    private static final String USER_QUERY =
            "SELECT id, email, password, first_name, last_name FROM calendar_users WHERE ";

    private final JdbcOperations jdbc;

    public JdbcCalendarUserDao(JdbcOperations jdbc) {
        this.jdbc = jdbc;
    }

    @Override
    @Transactional(readOnly = true)
    public CalendarUser getUser(int id) {
        return jdbc.queryForObject(USER_QUERY + "id = ?", USER_MAPPER, id);
    }

    @Override
    @Transactional(readOnly = true)
    public CalendarUser findUserByEmail(String email) {
        try {
            return jdbc.queryForObject(USER_QUERY + "email = ?", USER_MAPPER, email);
        } catch (EmptyResultDataAccessException e) {
            return null;
        }
    }

    @Override
    @Transactional(readOnly = true)
    public List<CalendarUser> findUsersByEmail(String partialEmail) {
        return jdbc.query(USER_QUERY + "email LIKE ? ORDER BY id",
                USER_MAPPER, partialEmail + "%");
    }

    @Override
    public int createUser(CalendarUser user) {
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbc.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(
                    "INSERT INTO calendar_users (email, password, first_name, last_name) VALUES (?, ?, ?, ?)",
                    new String[]{"id"});
            ps.setString(1, user.getEmail());
            ps.setString(2, user.getPassword());
            ps.setString(3, user.getFirstName());
            ps.setString(4, user.getLastName());
            return ps;
        }, keyHolder);
        return keyHolder.getKey().intValue();
    }

    static final RowMapper<CalendarUser> USER_MAPPER = (ResultSet rs, int rowNum) ->
            new CalendarUser(
                    rs.getInt("id"),
                    rs.getString("first_name"),
                    rs.getString("last_name"),
                    rs.getString("email"),
                    rs.getString("password")
            );
}
