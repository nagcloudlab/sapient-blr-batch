package com.example.repository;

import org.springframework.data.jpa.repository.JpaRepository;

public interface AccountRepository extends JpaRepository<com.example.entity.Account, String> {
    
}
