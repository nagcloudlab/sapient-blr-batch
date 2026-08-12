package com.example;

import java.util.List;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import com.example.entity.Address;
import com.example.entity.Employee;
import com.example.entity.Department;
import com.example.repository.DepartmentRepository;
import com.example.repository.EmployeeRepository;

@SpringBootApplication
@EnableTransactionManagement
@EnableJpaRepositories
public class Application {

	public static void main(String[] args) {
		ConfigurableApplicationContext context =
		SpringApplication.run(Application.class, args);

		EmployeeRepository employeeRepository = context.getBean(EmployeeRepository.class);
		DepartmentRepository departmentRepository = context.getBean(DepartmentRepository.class);

		// >>> Insert a new department and employees
		// Department department = new Department();
		// department.setId(1L);
		// department.setName("IT");
		// department.setLocation("Bangalore");


		// Employee employee1 = new Employee();
		// employee1.setId(1L);
		// employee1.setName("John Doe");

		// Employee employee2 = new Employee();
		// employee2.setId(2L);
		// employee2.setName("Jane Smith");	

		// employeeRepository.saveAll(List.of(employee1, employee2));

		// department.setEmployees(List.of(employee1, employee2));
		// departmentRepository.save(department);

		// >>> select department  by primary key
		Department department = departmentRepository.findById(1L).orElse(null);
		// dep details
		System.out.println(department.getId());
		System.out.println(department.getName());
		System.out.println(department.getLocation());
		// employee details
		List<Employee> employees = department.getEmployees();
		for (Employee employee : employees) {
			System.out.println(employee.getId());
			System.out.println(employee.getName());
		}

		//>>> select department by name
		// Department department = departmentRepository.findByName("IT");
		// System.out.println(department.getId());
		// System.out.println(department.getName());
		// System.out.println(department.getLocation());


		context.close();

	}

}
