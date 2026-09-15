package com.example.payment;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
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

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "UP", "service", "payment-service");
    }

    @PostMapping("/payments")
    public ResponseEntity<Payment> createPayment(@RequestBody Map<String, Object> request) {
        String orderId = (String) request.get("orderId");
        double amount = ((Number) request.get("amount")).doubleValue();

        if (orderId == null || amount <= 0) {
            log.warn("Invalid payment request - orderId: {}, amount: {}", orderId, amount);
            return ResponseEntity.badRequest().build();
        }

        Payment payment = new Payment(orderId, amount);

        // Add context to MDC for structured logging
        MDC.put("orderId", orderId);
        MDC.put("paymentId", payment.getId());
        MDC.put("amount", String.valueOf(amount));

        try {
            double random = Math.random();

            // 5% chance: Internal server error
            if (random < 0.05) {
                log.error("DATABASE CONNECTION FAILED - cannot process payment");
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
            }

            // 5% chance: Slow processing (2-5 seconds)
            if (random < 0.10) {
                long delay = (long) (Math.random() * 3000 + 2000);
                log.warn("SLOW PROCESSING detected - delay: {}ms", delay);
                Thread.sleep(delay);
            }

            // Normal processing delay
            Thread.sleep((long) (Math.random() * 200 + 50));

            // 10% chance: Payment declined
            if (random < 0.20) {
                payment.setStatus("FAILED");
                log.warn("Payment DECLINED - insufficient funds for amount: {}", amount);
            }
            // 5% chance: Gateway timeout
            else if (random < 0.25) {
                payment.setStatus("FAILED");
                log.error("GATEWAY TIMEOUT - payment gateway did not respond");
            } else {
                log.info("Payment COMPLETED successfully - amount: {}", amount);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.error("Payment processing INTERRUPTED", e);
        } finally {
            MDC.clear();
        }

        payments.put(payment.getId(), payment);
        return ResponseEntity.status(HttpStatus.CREATED).body(payment);
    }

    @GetMapping("/payments")
    public List<Payment> getAllPayments() {
        return new ArrayList<>(payments.values());
    }

    @GetMapping("/payments/{id}")
    public ResponseEntity<Payment> getPayment(@PathVariable String id) {
        Payment payment = payments.get(id);
        if (payment == null) {
            log.warn("Payment not found: {}", id);
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(payment);
    }
}
