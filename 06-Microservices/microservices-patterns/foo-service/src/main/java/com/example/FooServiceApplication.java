package com.example;

import java.net.InetAddress;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
@RestController
public class FooServiceApplication {

	private final RestTemplate restTemplate;
	private final DiscoveryClient discoveryClient;

	@Value("${psi.location}")
	private String psiLocation;

	public FooServiceApplication(RestTemplate restTemplate, DiscoveryClient discoveryClient) {
		this.restTemplate = restTemplate;
		this.discoveryClient = discoveryClient;
	}

	@GetMapping("/foo")
	public String sayHello() throws Exception {

		List<ServiceInstance> barInstances = discoveryClient.getInstances("bar-service");
		String discoveredInstances = barInstances.isEmpty()
				? "none"
				: barInstances.stream()
						.map(instance -> instance.getHost() + ":" + instance.getPort())
						.collect(Collectors.joining(", "));

		// Call Bar Service using service-id so Spring Cloud LoadBalancer picks an instance.
		String barServiceEndpoint = "http://bar-service/bar";
		String barServiceResponse = restTemplate.getForObject(barServiceEndpoint, String.class);

		String ip = InetAddress.getLocalHost().getHostAddress();
		return "Hello from Foo Service! psi.location-: " + psiLocation + " | ip-: " + ip
				+ " | Eureka instances for bar-service: " + discoveredInstances
				+ " | Bar Service Response: " + barServiceResponse;
	}

	public static void main(String[] args) {
		SpringApplication.run(FooServiceApplication.class, args);
	}

}
