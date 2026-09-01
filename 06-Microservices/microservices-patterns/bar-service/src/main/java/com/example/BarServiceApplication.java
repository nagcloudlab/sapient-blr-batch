package com.example;

import java.net.InetAddress;

import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class BarServiceApplication {
	private static final Logger logger = LoggerFactory.getLogger(BarServiceApplication.class);

	@Value("${server.port}")
	private String port;

	@GetMapping("/bar")
	public String sayHello(HttpServletRequest request) throws Exception {
		String ip = InetAddress.getLocalHost().getHostAddress();
		logger.info("Received /bar request from {}:{} on bar-service port {}", request.getRemoteAddr(), request.getRemotePort(), port);
		return "Hello from Bar Service! ip-: " + ip + " | port-: " + port;
	}

	public static void main(String[] args) {
		SpringApplication.run(BarServiceApplication.class, args);
	}

}
