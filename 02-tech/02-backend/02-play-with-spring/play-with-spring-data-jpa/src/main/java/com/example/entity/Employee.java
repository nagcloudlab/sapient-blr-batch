package com.example.entity;

import java.time.LocalDate;
import java.util.List;

import org.hibernate.annotations.DiscriminatorOptions;

import jakarta.persistence.AttributeOverride;
import jakarta.persistence.AttributeOverrides;
import jakarta.persistence.CollectionTable;
import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import jakarta.persistence.Table;
import jakarta.persistence.Temporal;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Entity
@Table(name = "employees")
public class Employee {

    @Id
    private Long id;
    @Column(nullable = false)
    private String name;
    @Column(nullable = false)
    private double salary;
    @Enumerated(EnumType.STRING)
    private Gender gender;
    @Column(name="dob")
    @Temporal(jakarta.persistence.TemporalType.DATE)
    private LocalDate dateOfBirth;
    @Lob
    private String profile;
    @Lob
    private byte[] image;

    @ElementCollection
    @CollectionTable(name = "employee_address",foreignKey = @jakarta.persistence.ForeignKey(name = "emp_id"))
   private List<Address> addressList;

    @Override
    public String toString() {
        return "Employee [id=" + id + ", name=" + name + ", salary=" + salary + "]";
    }
    
}
