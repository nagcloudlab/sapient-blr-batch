package com.example;

import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import com.example.model.Todo;

public class SelectTodos {

    public static void main(String[] args) {
        
        Todo todo = new Todo(2L, "Learn MySQL", false);

        try{
        // JDBC api
        // step-1: register the driver
        DriverManager.registerDriver(new com.mysql.cj.jdbc.Driver());
        // step-2: create connection
        String url="jdbc:mysql://localhost:3306/todosdb";
        String username="root";
        String password="yourpassword";
        java.sql.Connection connection = DriverManager.getConnection(url, username, password);
        System.out.println("Connection established successfully!");

        // step-3: create SQL statement
        String sql = "SELECT id, title, completed FROM todos";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        java.sql.ResultSet resultSet = preparedStatement.executeQuery();
        List<Todo> todos = new ArrayList<>();
        while(resultSet.next()) {
            Long id = resultSet.getLong("id");
            String title = resultSet.getString("title");
            boolean completed = resultSet.getBoolean("completed");
           Todo fetchedTodo = new Todo(id, title, completed);
            todos.add(fetchedTodo);
        }

        connection.close();

        for(Todo t : todos) {
            System.out.println(t);
        }

    }catch(SQLException e){
        e.printStackTrace();
    }

    }
    
}
