package com.example.payment;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@RestController
public class PaymentController {

    private static final Logger log = LoggerFactory.getLogger(PaymentController.class);
    private final Map<String, Payment> payments = new ConcurrentHashMap<>();

    private final Counter paymentsCompletedCounter;
    private final Counter paymentsFailedCounter;
    private final Counter paymentsErrorCounter;
    private final Timer paymentProcessingTimer;

    public PaymentController(MeterRegistry registry) {
        this.paymentsCompletedCounter = Counter.builder("payments_completed_total")
                .description("Total completed payments")
                .register(registry);
        this.paymentsFailedCounter = Counter.builder("payments_failed_total")
                .description("Total failed payments")
                .register(registry);
        this.paymentsErrorCounter = Counter.builder("payments_error_total")
                .description("Total payment internal errors")
                .register(registry);
        this.paymentProcessingTimer = Timer.builder("payment_processing_duration")
                .description("Payment processing duration")
                .register(registry);
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "UP", "service", "payment-service");
    }

    @PostMapping("/payments")
    public ResponseEntity<Payment> createPayment(@RequestBody Map<String, Object> request) {
        return paymentProcessingTimer.record(() -> {
            String orderId = (String) request.get("orderId");
            double amount = ((Number) request.get("amount")).doubleValue();

            if (orderId == null || amount <= 0) {
                return ResponseEntity.badRequest().<Payment>build();
            }

            Payment payment = new Payment(orderId, amount);
            double random = Math.random();

            // --- Simulate real-world failure scenarios ---

            // 5% chance: Internal server error (e.g., DB connection failed)
            if (random < 0.05) {
                paymentsErrorCounter.increment();
                log.error("Payment {} INTERNAL ERROR for order {} - database connection failed", payment.getId(), orderId);
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).<Payment>build();
            }

            // 5% chance: Slow response (simulates downstream timeout, 2-5 seconds)
            if (random < 0.10) {
                try {
                    long slowDelay = (long) (Math.random() * 3000 + 2000);
                    log.warn("Payment {} SLOW PROCESSING for order {} - delay: {}ms", payment.getId(), orderId, slowDelay);
                    Thread.sleep(slowDelay);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }

            // Normal processing delay (50-250ms)
            try {
                Thread.sleep((long) (Math.random() * 200 + 50));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }

            // 10% chance: Payment declined (e.g., insufficient funds)
            if (random < 0.20) {
                payment.setStatus("FAILED");
                paymentsFailedCounter.increment();
                log.warn("Payment {} DECLINED for order {} - insufficient funds", payment.getId(), orderId);
            }
            // 5% chance: Payment timeout from gateway
            else if (random < 0.25) {
                payment.setStatus("FAILED");
                paymentsFailedCounter.increment();
                log.warn("Payment {} TIMEOUT for order {} - gateway did not respond", payment.getId(), orderId);
            } else {
                paymentsCompletedCounter.increment();
                log.info("Payment {} completed for order {} - amount: {}", payment.getId(), orderId, amount);
            }

            payments.put(payment.getId(), payment);
            return ResponseEntity.status(HttpStatus.CREATED).body(payment);
        });
    }

    @GetMapping("/payments")
    public List<Payment> getAllPayments() {
        return new ArrayList<>(payments.values());
    }

    @GetMapping("/payments/{id}")
    public ResponseEntity<Payment> getPayment(@PathVariable String id) {
        Payment payment = payments.get(id);
        if (payment == null) return ResponseEntity.notFound().build();
        return ResponseEntity.ok(payment);
    }
}
