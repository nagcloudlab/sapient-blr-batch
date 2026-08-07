package com.example.web;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.example.entity.Todo;
import com.example.service.TodoService;

import org.springframework.ui.Model;


@Controller
@RequestMapping("/todos")
public class TodoController {

    private final TodoService todoService;

    @Autowired
    public TodoController(TodoService todoService) {
        this.todoService = todoService;
    }

    @GetMapping
    public String viewTodos(Model model) {
       List<Todo> todos = todoService.getAllTodos();
       model.addAttribute("todos", todos);
       return "todos-view"; // Return the name of the view (e.g., todos.html)
    }
    
    
}
