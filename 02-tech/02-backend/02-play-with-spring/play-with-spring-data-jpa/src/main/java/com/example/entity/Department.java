package com.example.entity;

import java.util.List;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinTable;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Entity
@Table(name = "departments")
public class Department {

    @Id
    private Long id;
    private String name;
    private String location;

    @OneToMany(cascade = jakarta.persistence.CascadeType.PERSIST,fetch = FetchType.EAGER)
    @JoinTable(name="department_employees",
            joinColumns = @jakarta.persistence.JoinColumn(name="department_id"),
            inverseJoinColumns = @jakarta.persistence.JoinColumn(name="employee_id"))
    private List<Employee> employees=new java.util.ArrayList<>();
    
}
