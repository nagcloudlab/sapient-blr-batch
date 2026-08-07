package com.example.entity;
import java.time.LocalDateTime;
import java.util.List;
        // - user: {
        //     id: string,
        //     name: string,
        //     email: string,
        //     password: string, // hashed
        //     createdAt: Date,
        //     updatedAt: Date
        // }

public class User {

    private Long id;
    private String name;
    private String email;
    private String password; // hashed
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // One-to-Many relationship with Todo
    private List<Todo> todos; // List of Todo entities associated with the User

    
}
