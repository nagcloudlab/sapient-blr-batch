package com.npci.upi.controller;

import com.npci.upi.model.UpiPaymentRequest;
import com.npci.upi.model.UpiPaymentResponse;
import com.npci.upi.service.ChaosService;
import com.npci.upi.service.TransactionService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
public class TransactionController {

    private final TransactionService transactionService;
    private final ChaosService chaosService;

    public TransactionController(TransactionService transactionService, ChaosService chaosService) {
        this.transactionService = transactionService;
        this.chaosService = chaosService;
    }

    @PostMapping("/api/upi/pay")
    public ResponseEntity<UpiPaymentResponse> pay(@RequestBody UpiPaymentRequest request) {
        if (chaosService.isServiceDown()) {
            UpiPaymentResponse resp = new UpiPaymentResponse();
            resp.setStatus("FAILED");
            resp.setErrorCode("U78");
            resp.setErrorMessage("UPI service unavailable");
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(resp);
        }
        UpiPaymentResponse response = transactionService.processPayment(request);
        if ("FAILED".equals(response.getStatus())) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
        }
        return ResponseEntity.ok(response);
    }

    @GetMapping("/api/upi/status/{transactionId}")
    public ResponseEntity<Map<String, String>> txnStatus(@PathVariable String transactionId) {
        if (chaosService.isServiceDown()) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(Map.of("error", "Service unavailable"));
        }
        return ResponseEntity.ok(Map.of(
                "transactionId", transactionId,
                "status", "SUCCESS",
                "message", "Transaction completed"
        ));
    }

    // --- Chaos endpoints for demo ---

    @PostMapping("/chaos/enable")
    public Map<String, Object> chaosEnable() {
        chaosService.enableChaos();
        return Map.of("chaos", "enabled", "failure_rate_percent", 80);
    }

    @PostMapping("/chaos/disable")
    public Map<String, Object> chaosDisable() {
        chaosService.disableChaos();
        return Map.of("chaos", "disabled");
    }

    @PostMapping("/chaos/latency")
    public Map<String, Object> chaosLatency(@RequestParam(defaultValue = "3000") int ms) {
        chaosService.setLatency(ms);
        return Map.of("chaos", "latency_injected", "latency_ms", ms);
    }

    @PostMapping("/chaos/down")
    public Map<String, Object> chaosDown() {
        chaosService.setServiceDown(true);
        return Map.of("chaos", "service_down");
    }

    @GetMapping("/chaos/status")
    public Map<String, Object> chaosStatus() {
        return chaosService.getStatus();
    }
}
