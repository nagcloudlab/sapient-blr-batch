package com.example.order;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.net.InetAddress;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private static final Logger log = LoggerFactory.getLogger(OrderController.class);

    private final RestTemplate restTemplate;
    private final Counter orderCounter;
    private final Timer orderTimer;
    private final Map<Long, Map<String, Object>> orders = new ConcurrentHashMap<>();
    private final AtomicLong idGenerator = new AtomicLong(1);

    @Value("${server.port:8081}")
    private int serverPort;

    public OrderController(RestTemplate restTemplate, MeterRegistry meterRegistry) {
        this.restTemplate = restTemplate;
        this.orderCounter = Counter.builder("orders.created.total")
                .description("Total orders created")
                .register(meterRegistry);
        this.orderTimer = Timer.builder("orders.processing.time")
                .description("Order processing time")
                .register(meterRegistry);
    }

    @GetMapping
    public ResponseEntity<Map<String, Object>> getAllOrders(HttpServletRequest request) {
        String correlationId = request.getHeader("X-Correlation-ID");
        log.info("[correlationId={}] GET /orders from instance port {}", correlationId, serverPort);

        Map<String, Object> response = new LinkedHashMap<>();
        response.put("service", "order-service");
        response.put("port", serverPort);
        response.put("correlationId", correlationId);
        response.put("orders", orders.values());
        response.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Map<String, Object>> getOrder(@PathVariable Long id, HttpServletRequest request) {
        String correlationId = request.getHeader("X-Correlation-ID");
        log.info("[correlationId={}] GET /orders/{} from instance port {}", correlationId, id, serverPort);

        Map<String, Object> order = orders.get(id);
        if (order == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(order);
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> createOrder(@RequestBody Map<String, Object> orderRequest,
                                                            HttpServletRequest request) {
        return orderTimer.record(() -> {
            String correlationId = request.getHeader("X-Correlation-ID");
            String userHeader = request.getHeader("X-User");
            String roleHeader = request.getHeader("X-User-Role");

            log.info("[correlationId={}] POST /orders by user={} role={}", correlationId, userHeader, roleHeader);

            // Check inventory
            String productId = (String) orderRequest.getOrDefault("productId", "PROD-001");
            String inventoryResponse;
            try {
                inventoryResponse = restTemplate.getForObject(
                        "http://inventory-service/inventory/" + productId, String.class);
                log.info("[correlationId={}] Inventory check: {}", correlationId, inventoryResponse);
            } catch (Exception e) {
                log.error("[correlationId={}] Inventory service unavailable: {}", correlationId, e.getMessage());
                inventoryResponse = "UNAVAILABLE";
            }

            long orderId = idGenerator.getAndIncrement();
            Map<String, Object> order = new LinkedHashMap<>();
            order.put("orderId", orderId);
            order.put("productId", productId);
            order.put("quantity", orderRequest.getOrDefault("quantity", 1));
            order.put("status", "CREATED");
            order.put("createdBy", userHeader);
            order.put("inventoryCheck", inventoryResponse);
            order.put("instancePort", serverPort);
            order.put("correlationId", correlationId);
            order.put("createdAt", LocalDateTime.now().toString());

            orders.put(orderId, order);
            orderCounter.increment();

            log.info("[correlationId={}] Order {} created successfully", correlationId, orderId);
            return ResponseEntity.ok(order);
        });
    }

    @GetMapping("/health-details")
    public ResponseEntity<Map<String, Object>> healthDetails() {
        Map<String, Object> health = new LinkedHashMap<>();
        health.put("service", "order-service");
        health.put("status", "UP");
        health.put("port", serverPort);
        health.put("totalOrders", orders.size());
        try {
            health.put("host", InetAddress.getLocalHost().getHostAddress());
        } catch (Exception e) {
            health.put("host", "unknown");
        }
        health.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(health);
    }
}
