package com.example.entity;

public enum TodoStatus {
    
    PENDING("pending"),
    COMPLETED("completed");

    private final String status;

    TodoStatus(String status) {
        this.status = status;
    }
    public String getStatus() {
        return status;
    }

}
