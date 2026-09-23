package com.npci.settlement.controller;

import com.npci.settlement.model.SettlementRequest;
import com.npci.settlement.model.SettlementResponse;
import com.npci.settlement.service.SettlementService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class SettlementController {

    private final SettlementService settlementService;

    public SettlementController(SettlementService settlementService) {
        this.settlementService = settlementService;
    }

    @PostMapping("/api/settlement/process")
    public ResponseEntity<SettlementResponse> process(@RequestBody SettlementRequest request) {
        SettlementResponse response = settlementService.processSettlement(request);
        if ("FAILED".equals(response.getStatus())) {
            return ResponseEntity.status(502).body(response);
        }
        return ResponseEntity.ok(response);
    }
}
