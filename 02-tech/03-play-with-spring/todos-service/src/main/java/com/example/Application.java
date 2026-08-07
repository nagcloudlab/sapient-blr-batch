package com.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

import com.example.repository.JdbcTodoRepository;
import com.example.repository.TodoRepository;
import com.example.service.TodoService;
import com.example.service.TodoServiceImpl;

// @Configuration
// @EnableAutoConfiguration
// @ComponentScan(basePackages = {"com.example"})
@SpringBootApplication
public class Application {

    private static Logger logger = LoggerFactory.getLogger(Application.class);
    public static void main(String[] args) {

        //----------------------------
        // boot
        //----------------------------
        logger.info("-".repeat(50));

        logger.info("Starting application...");

        ConfigurableApplicationContext context=null;
        context=SpringApplication.run(Application.class, args);

        
        //----------------------------
        // Use the service
        //----------------------------
        logger.info("-".repeat(50));

        // TodoService todoService = context.getBean(TodoService.class);

        // todoService.createNewTodo("Learn Java","Learn the basics of Java programming language.");
        // todoService.createNewTodo("Learn Spring Boot","Learn how to build RESTful APIs using Spring Boot.");
        // //todoService.markTodoAsCompleted(1L);

        // logger.info("All Todos:");
        // todoService.getAllTodos().forEach(todo -> logger.info(todo.toString()));

        logger.info("-".repeat(50));
        //----------------------------
        // shutdown
        //----------------------------
        logger.info("-".repeat(50));
        //context.close();


    }
}