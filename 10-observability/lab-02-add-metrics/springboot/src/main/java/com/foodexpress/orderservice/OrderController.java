package com.foodexpress.orderservice;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Duration;
import java.util.Map;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;

@RestController
public class OrderController {

    private final Counter ordersSuccessCounter;
    private final Counter ordersFailedCounter;
    private final Timer orderDurationTimer;
    private final AtomicInteger activeOrders = new AtomicInteger(0);

    public OrderController(MeterRegistry registry) {
        // COUNTER: Total orders placed (same as orders_placed_total in Node.js)
        this.ordersSuccessCounter = Counter.builder("orders_placed_total")
                .tag("status", "success")
                .description("Total orders placed")
                .register(registry);

        this.ordersFailedCounter = Counter.builder("orders_placed_total")
                .tag("status", "failed")
                .description("Total orders placed")
                .register(registry);

        // HISTOGRAM/TIMER: Order request duration (same as http_request_duration_seconds in Node.js)
        this.orderDurationTimer = Timer.builder("http_request_duration_seconds")
                .description("Request duration in seconds")
                .publishPercentileHistogram()
                .sla(Duration.ofMillis(10), Duration.ofMillis(50), Duration.ofMillis(100),
                     Duration.ofMillis(250), Duration.ofMillis(500), Duration.ofSeconds(1),
                     Duration.ofMillis(2500), Duration.ofSeconds(5))
                .register(registry);

        // GAUGE: Currently active orders (same as active_orders in Node.js)
        Gauge.builder("active_orders", activeOrders, AtomicInteger::get)
                .description("Currently active orders")
                .register(registry);
    }

    @GetMapping("/")
    public Map<String, String> home() {
        return Map.of("service", "FoodExpress Order Service", "status", "healthy");
    }

    @PostMapping("/api/orders")
    public ResponseEntity<?> placeOrder() throws InterruptedException {
        activeOrders.incrementAndGet();

        return orderDurationTimer.record(() -> {
            try {
                // 5% of requests are extremely slow (3 seconds)
                int delay = ThreadLocalRandom.current().nextDouble() < 0.05
                        ? 3000
                        : ThreadLocalRandom.current().nextInt(200);
                Thread.sleep(delay);

                // 10% of requests fail
                if (ThreadLocalRandom.current().nextDouble() < 0.1) {
                    ordersFailedCounter.increment();
                    activeOrders.decrementAndGet();
                    return ResponseEntity.status(500)
                            .body(Map.of("error", "Payment gateway timeout"));
                }

                ordersSuccessCounter.increment();
                activeOrders.decrementAndGet();
                return ResponseEntity.ok(
                        Map.of("orderId", "ORD-" + System.currentTimeMillis(), "status", "placed"));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                activeOrders.decrementAndGet();
                return ResponseEntity.status(500)
                        .body(Map.of("error", "Interrupted"));
            }
        });
    }
}
