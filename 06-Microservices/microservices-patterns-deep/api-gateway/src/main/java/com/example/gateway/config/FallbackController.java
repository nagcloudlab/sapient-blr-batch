package com.example.gateway.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * DEMO: Gateway - Circuit Breaker Fallback Controller
 *
 * Provides fallback responses when downstream services are unavailable.
 * The circuit breaker routes to these endpoints when the service is down.
 */
@RestController
@RequestMapping("/fallback")
public class FallbackController {

    private static final Logger log = LoggerFactory.getLogger(FallbackController.class);

    @GetMapping("/orders")
    public Mono<ResponseEntity<Map<String, Object>>> ordersFallback() {
        log.warn("Circuit breaker triggered - order-service fallback");
        Map<String, Object> fallback = new LinkedHashMap<>();
        fallback.put("service", "order-service");
        fallback.put("status", "SERVICE_UNAVAILABLE");
        fallback.put("message", "Order service is temporarily unavailable. Please try again later.");
        fallback.put("fallback", true);
        fallback.put("timestamp", LocalDateTime.now().toString());
        return Mono.just(ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(fallback));
    }

    @GetMapping("/inventory")
    public Mono<ResponseEntity<Map<String, Object>>> inventoryFallback() {
        log.warn("Circuit breaker triggered - inventory-service fallback");
        Map<String, Object> fallback = new LinkedHashMap<>();
        fallback.put("service", "inventory-service");
        fallback.put("status", "SERVICE_UNAVAILABLE");
        fallback.put("message", "Inventory service is temporarily unavailable.");
        fallback.put("fallback", true);
        fallback.put("timestamp", LocalDateTime.now().toString());
        return Mono.just(ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(fallback));
    }
}
