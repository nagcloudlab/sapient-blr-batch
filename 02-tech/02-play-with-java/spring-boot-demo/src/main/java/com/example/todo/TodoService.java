package com.example.todo;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

@Service
public class TodoService {
    private final TodoRepository todoRepository;

    public TodoService(TodoRepository todoRepository) {
        this.todoRepository = todoRepository;
    }

    public Todo createTodo(Todo todo) {
        return todoRepository.save(todo);
    }

    public List<Todo> getAllTodos() {
        return todoRepository.findAll();
    }

    public Optional<Todo> getTodoById(Long id) {
        return todoRepository.findById(id);
    }

    public Todo updateTodo(Long id, Todo todo) {
        Todo existingTodo = todoRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Todo not found"));
        existingTodo.setTitle(todo.getTitle());
        existingTodo.setDescription(todo.getDescription());
        existingTodo.setCompleted(todo.isCompleted());
        return todoRepository.update(existingTodo);
    }

    public void deleteTodo(Long id) {
        todoRepository.deleteById(id);
    }
}
