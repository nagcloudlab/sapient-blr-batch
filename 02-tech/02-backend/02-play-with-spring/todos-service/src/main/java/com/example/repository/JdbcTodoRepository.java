package com.example.repository;

import java.util.List;

import javax.sql.DataSource;

import org.slf4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import com.example.entity.Todo;
import com.example.entity.TodoStatus;

@Repository
public class JdbcTodoRepository implements TodoRepository {

    private Logger logger= org.slf4j.LoggerFactory.getLogger(JdbcTodoRepository.class);

    private final JdbcTemplate jdbcTemplate;
    
    @Autowired
    public JdbcTodoRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
        logger.info("JdbcTodoRepository initialized");
    }

    @Override
    public void save(Todo todo) {
        logger.info("Saving todo: {}", todo);
        String sql = "INSERT INTO todos (id, title, description, status) VALUES (?, ?, ?, ?)";
        jdbcTemplate.update(sql,
                todo.getId(),
                todo.getTitle(),
                todo.getDescription(),
                todo.getStatus().toString());

        // step-1: get free connection from the connection pool
        // step-2: create a prepared statement
        // step-3: set the parameters in the prepared statement
        // step-4: execute the prepared statement
        // step-5: close the prepared statement
        // step-6: return the connection to the connection pool        
    }

    @Override
    public void delete(Todo todo) {
        logger.info("Deleting todo with id: {}", todo.getId());
        String sql = "DELETE FROM todos WHERE id = ?";
        jdbcTemplate.update(sql, todo.getId());
    }

    @Override
    public Todo findById(Long id) {
        logger.info("Finding todo with id: {}", id);
        String sql = "SELECT * FROM todos WHERE id = ?";
        return jdbcTemplate.queryForObject(sql, new Object[]{id}, (rs, rowNum) -> {
            Todo todo = new Todo();
            todo.setId(rs.getLong("id"));
            todo.setTitle(rs.getString("title"));
            todo.setDescription(rs.getString("description"));
            todo.setStatus(TodoStatus.valueOf(rs.getString("status")));
            return todo;
        });
    }

    @Override
    public List<Todo> findAll() {
        logger.info("Finding all todos");
        String sql = "SELECT * FROM todos";
        return jdbcTemplate.query(sql, (rs, rowNum) -> {
            Todo todo = new Todo();
            todo.setId(rs.getLong("id"));
            todo.setTitle(rs.getString("title"));
            todo.setDescription(rs.getString("description"));
            todo.setStatus(TodoStatus.valueOf(rs.getString("status")));
            return todo;
        });
    }
    
}
