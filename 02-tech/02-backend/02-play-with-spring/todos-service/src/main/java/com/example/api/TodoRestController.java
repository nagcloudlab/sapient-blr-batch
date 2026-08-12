package com.example.api;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.entity.Todo;
import com.example.service.TodoService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;


@RestController
@RequestMapping("/api/todos")
public class TodoRestController {

    private final TodoService todoService;

    @Autowired
    public TodoRestController(TodoService todoService) {
        this.todoService = todoService;
    }

    @GetMapping(
        produces = "application/json"
    )
    public List<Todo> getAllTodos() {
        return todoService.getAllTodos();
    }
    
    
}
