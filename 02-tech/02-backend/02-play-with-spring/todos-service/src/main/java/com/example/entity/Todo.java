package com.example.entity;

import java.time.LocalDateTime;

// - todo: {
        //     id: string,
        //     title: string,
        //     description: string,
        //     status: string, // e.g., "pending", "completed"
        //     createdAt: Date,
        //     updatedAt: Date
        // }

public class Todo {

    private Long id;
    private String title;
    private String description;
    private TodoStatus status; // Use the TodoStatus enum for status
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // Many-to-One relationship with User
    private User user; // Reference to the User entity

    // setters and getters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public TodoStatus getStatus() {
        return status;
    }

    public void setStatus(TodoStatus status) {
        this.status = status;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    @Override
    public String toString() {
        return "Todo{" +
                "id=" + id +
                ", title='" + title + '\'' +
                ", description='" + description + '\'' +
                ", status=" + status +
                ", createdAt=" + createdAt +
                ", updatedAt=" + updatedAt +
                '}';
    }
    
}
