package com.example.todo;

import java.sql.PreparedStatement;
import java.sql.Statement;
import java.util.List;
import java.util.Optional;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

@Repository
public class JdbcTodoRepository implements TodoRepository {

    private final JdbcTemplate jdbcTemplate;

    private final RowMapper<Todo> todoRowMapper = (rs, rowNum) -> new Todo(
            rs.getLong("id"),
            rs.getString("title"),
            rs.getString("description"),
            rs.getBoolean("completed")
    );

    public JdbcTodoRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public Todo save(Todo todo) {
        String sql = "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)";
        KeyHolder keyHolder = new GeneratedKeyHolder();
        jdbcTemplate.update(connection -> {
            PreparedStatement ps = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
            ps.setString(1, todo.getTitle());
            ps.setString(2, todo.getDescription());
            ps.setBoolean(3, todo.isCompleted());
            return ps;
        }, keyHolder);
        todo.setId(keyHolder.getKey().longValue());
        return todo;
    }

    @Override
    public List<Todo> findAll() {
        return jdbcTemplate.query("SELECT id, title, description, completed FROM todos ORDER BY id", todoRowMapper);
    }

    @Override
    public Optional<Todo> findById(Long id) {
        List<Todo> todos = jdbcTemplate.query(
                "SELECT id, title, description, completed FROM todos WHERE id = ?",
                todoRowMapper,
                id
        );
        return todos.isEmpty() ? Optional.empty() : Optional.of(todos.get(0));
    }

    @Override
    public Todo update(Todo todo) {
        jdbcTemplate.update(
                "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
                todo.getTitle(),
                todo.getDescription(),
                todo.isCompleted(),
                todo.getId()
        );
        return todo;
    }

    @Override
    public void deleteById(Long id) {
        jdbcTemplate.update("DELETE FROM todos WHERE id = ?", id);
    }
}
