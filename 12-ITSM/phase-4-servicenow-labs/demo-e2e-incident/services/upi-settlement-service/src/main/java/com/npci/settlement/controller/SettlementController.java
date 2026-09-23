package com.npci.settlement.controller;

import com.npci.settlement.model.SettlementRequest;
import com.npci.settlement.model.SettlementResponse;
import com.npci.settlement.service.ChaosService;
import com.npci.settlement.service.SettlementService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
public class SettlementController {

    private final SettlementService settlementService;
    private final ChaosService chaosService;

    public SettlementController(SettlementService settlementService, ChaosService chaosService) {
        this.settlementService = settlementService;
        this.chaosService = chaosService;
    }

    @PostMapping("/api/settlement/process")
    public ResponseEntity<SettlementResponse> process(@RequestBody SettlementRequest request) {
        if (chaosService.isServiceDown()) {
            SettlementResponse resp = new SettlementResponse();
            resp.setStatus("FAILED");
            resp.setErrorMessage("Settlement service unavailable");
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(resp);
        }
        SettlementResponse response = settlementService.processSettlement(request);
        if ("FAILED".equals(response.getStatus())) {
            return ResponseEntity.status(502).body(response);
        }
        return ResponseEntity.ok(response);
    }

    // --- Chaos endpoints for demo ---

    @PostMapping("/chaos/enable")
    public Map<String, Object> chaosEnable() {
        chaosService.enableChaos();
        return Map.of("chaos", "enabled", "failure_rate_percent", 80, "service", "upi-settlement-service");
    }

    @PostMapping("/chaos/disable")
    public Map<String, Object> chaosDisable() {
        chaosService.disableChaos();
        return Map.of("chaos", "disabled", "service", "upi-settlement-service");
    }

    @PostMapping("/chaos/latency")
    public Map<String, Object> chaosLatency(@RequestParam(defaultValue = "3000") int ms) {
        chaosService.setLatency(ms);
        return Map.of("chaos", "latency_injected", "latency_ms", ms, "service", "upi-settlement-service");
    }

    @PostMapping("/chaos/down")
    public Map<String, Object> chaosDown() {
        chaosService.setServiceDown(true);
        return Map.of("chaos", "service_down", "service", "upi-settlement-service");
    }

    @GetMapping("/chaos/status")
    public Map<String, Object> chaosStatus() {
        return chaosService.getStatus();
    }
}
