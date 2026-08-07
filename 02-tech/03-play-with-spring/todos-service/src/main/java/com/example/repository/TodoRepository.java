package com.example.repository;

import java.util.List;

import com.example.entity.Todo;

public interface TodoRepository {
    
    void save(Todo todo);
    void delete(Todo todo);
    Todo findById(Long id);
    List<Todo> findAll(); 


}
