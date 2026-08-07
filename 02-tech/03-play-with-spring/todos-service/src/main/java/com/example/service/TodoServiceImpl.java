package com.example.service;

import java.util.Random;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.entity.Todo;
import com.example.entity.TodoStatus;
import com.example.repository.TodoRepository;

@Service
public class TodoServiceImpl implements TodoService {

    private Logger logger = LoggerFactory.getLogger(TodoServiceImpl.class);

    private Random random = new Random();

    public TodoServiceImpl() {
        logger.info("TodoServiceImpl initialized");
    }

    private TodoRepository todoRepository;

    @Autowired
    public TodoServiceImpl(TodoRepository todoRepository) {
        this.todoRepository = todoRepository;
        logger.info("TodoServiceImpl initialized with TodoRepository");
    }

    @Override
    public void createNewTodo(String title, String description) {
        logger.info("Creating new todo with title: {} and description: {}", title, description);
        Todo newTodo = new Todo();
        newTodo.setId((long) random.nextInt(1000)); // Random ID for demonstration
        newTodo.setTitle(title);
        newTodo.setDescription(description);
        newTodo.setStatus(TodoStatus.PENDING);
        newTodo.setCreatedAt(java.time.LocalDateTime.now());
        newTodo.setUpdatedAt(java.time.LocalDateTime.now());
        todoRepository.save(newTodo);
    }

    @Override
    public void updateTodo(Long id, String title, String description) {
        logger.info("Updating todo with ID: {} to have title: {} and description: {}", id, title, description);
        Todo existingTodo = todoRepository.findById(id);
        if (existingTodo != null) {
            existingTodo.setTitle(title);
            existingTodo.setDescription(description);
            existingTodo.setUpdatedAt(java.time.LocalDateTime.now());
            todoRepository.save(existingTodo);
        }
    }

    @Override
    public void deleteTodo(Long id) {
        logger.info("Deleting todo with ID: {}", id);
        Todo existingTodo = todoRepository.findById(id);
        if (existingTodo != null) {
            todoRepository.delete(existingTodo);
        }
    }

    @Override
    public void markTodoAsCompleted(Long id) {
        logger.info("Marking todo with ID: {} as completed", id);
        Todo existingTodo = todoRepository.findById(id);
        if (existingTodo != null) {
            existingTodo.setStatus(TodoStatus.COMPLETED);
            existingTodo.setUpdatedAt(java.time.LocalDateTime.now());
            todoRepository.save(existingTodo);
        }
    }

    @Override
    public Todo getTodoById(Long id) {
        logger.info("Retrieving todo with ID: {}", id);
        return todoRepository.findById(id);
    }

    @Override
    public java.util.List<Todo> getAllTodos() {
        logger.info("Retrieving all todos");
        return todoRepository.findAll();
    }
    
}
