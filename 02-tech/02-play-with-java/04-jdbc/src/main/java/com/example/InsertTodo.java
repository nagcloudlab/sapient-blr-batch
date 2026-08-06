package com.example;

import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import com.example.model.Todo;

public class InsertTodo {

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
        String sql = "INSERT INTO todos (id, title, completed) VALUES (?, ?, ?)";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        preparedStatement.setLong(1, todo.getId());
        preparedStatement.setString(2, todo.getTitle());
        preparedStatement.setBoolean(3, todo.isCompleted());

        // step-4: execute the statement & step-5: process the result
        int rowsAffected = preparedStatement.executeUpdate();
        if(rowsAffected == 1) {
            System.out.println("Todo inserted successfully!");
        } else {
            System.out.println("Failed to insert todo.");
        }

        connection.close();

    }catch(SQLException e){
        e.printStackTrace();
    }

    }
    
}
