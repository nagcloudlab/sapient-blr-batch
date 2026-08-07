package com.example.todo;

import java.util.List;
import java.util.Optional;

public interface TodoRepository {
    Todo save(Todo todo);
    List<Todo> findAll();
    Optional<Todo> findById(Long id);
    Todo update(Todo todo);
    void deleteById(Long id);
}
