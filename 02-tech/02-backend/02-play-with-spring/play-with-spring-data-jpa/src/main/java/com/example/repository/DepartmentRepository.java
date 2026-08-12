package com.example.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import com.example.entity.Department;

public interface DepartmentRepository extends JpaRepository<Department, Long> {
    
    @Query("SELECT d FROM Department d WHERE d.name = ?1")
    Department findByName(String name);

    // Native SQL query example
    // @Query(value = "SELECT * FROM departments WHERE name = ?1", nativeQuery = true)
    // Department findByNameNative(String name);

    

}
