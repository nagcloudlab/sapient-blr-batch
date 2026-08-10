package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;


@SpringBootApplication
@RestController
public class GreetServiceApplication {

	@GetMapping("/greet")
	public String doGreet() {
		String threadName = Thread.currentThread().getName();
		System.out.println("Thread name: " + threadName);
		// IO simulation
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		return "Hello, welcome to the Greet Service! (served by " + threadName + ")";
	}
	

	public static void main(String[] args) {
		SpringApplication.run(GreetServiceApplication.class, args);
	}

}
