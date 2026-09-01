package com.example.inventory;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.InetAddress;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@RestController
@RequestMapping("/inventory")
public class InventoryController {

    private static final Logger log = LoggerFactory.getLogger(InventoryController.class);

    private final Counter inventoryCheckCounter;
    private final Map<String, Map<String, Object>> inventory = new ConcurrentHashMap<>();

    @Value("${server.port:8082}")
    private int serverPort;

    @Value("${app.version:v1}")
    private String appVersion;

    public InventoryController(MeterRegistry meterRegistry) {
        this.inventoryCheckCounter = Counter.builder("inventory.checks.total")
                .description("Total inventory checks")
                .register(meterRegistry);

        // Seed some inventory data
        seedInventory("PROD-001", "Laptop", 50);
        seedInventory("PROD-002", "Phone", 120);
        seedInventory("PROD-003", "Tablet", 30);
    }

    private void seedInventory(String productId, String name, int quantity) {
        Map<String, Object> item = new LinkedHashMap<>();
        item.put("productId", productId);
        item.put("name", name);
        item.put("quantity", quantity);
        item.put("available", true);
        inventory.put(productId, item);
    }

    @GetMapping
    public ResponseEntity<Map<String, Object>> getAllInventory(HttpServletRequest request) {
        String correlationId = request.getHeader("X-Correlation-ID");
        log.info("[correlationId={}] GET /inventory from version={} port={}", correlationId, appVersion, serverPort);

        Map<String, Object> response = new LinkedHashMap<>();
        response.put("service", "inventory-service");
        response.put("version", appVersion);
        response.put("port", serverPort);
        response.put("correlationId", correlationId);
        response.put("inventory", inventory.values());
        response.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{productId}")
    public ResponseEntity<Map<String, Object>> checkInventory(@PathVariable String productId,
                                                               HttpServletRequest request) {
        String correlationId = request.getHeader("X-Correlation-ID");
        log.info("[correlationId={}] GET /inventory/{} from version={} port={}",
                correlationId, productId, appVersion, serverPort);

        inventoryCheckCounter.increment();

        Map<String, Object> item = inventory.get(productId);
        if (item == null) {
            Map<String, Object> notFound = new LinkedHashMap<>();
            notFound.put("productId", productId);
            notFound.put("available", false);
            notFound.put("message", "Product not found");
            notFound.put("version", appVersion);
            notFound.put("port", serverPort);
            return ResponseEntity.ok(notFound);
        }

        Map<String, Object> response = new LinkedHashMap<>(item);
        response.put("version", appVersion);
        response.put("port", serverPort);
        response.put("correlationId", correlationId);
        response.put("checkedAt", LocalDateTime.now().toString());
        return ResponseEntity.ok(response);
    }

    @GetMapping("/health-details")
    public ResponseEntity<Map<String, Object>> healthDetails() {
        Map<String, Object> health = new LinkedHashMap<>();
        health.put("service", "inventory-service");
        health.put("version", appVersion);
        health.put("status", "UP");
        health.put("port", serverPort);
        health.put("totalProducts", inventory.size());
        try {
            health.put("host", InetAddress.getLocalHost().getHostAddress());
        } catch (Exception e) {
            health.put("host", "unknown");
        }
        health.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(health);
    }
}
