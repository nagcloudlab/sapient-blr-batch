package com.example.service;

import com.example.entity.Todo;

public interface TodoService {
    
    void createNewTodo(String title, String description);
    void updateTodo(Long id, String title, String description);
    void deleteTodo(Long id);
    void markTodoAsCompleted(Long id);
    Todo getTodoById(Long id);
    java.util.List<Todo> getAllTodos();


}
