package com.npci.settlement.service;

import com.npci.settlement.model.SettlementRequest;
import com.npci.settlement.model.SettlementResponse;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.Map;
import java.util.Random;
import java.util.UUID;

@Service
public class SettlementService {

    private final RestTemplate restTemplate;
    private final String transactionServiceUrl;
    private final Counter settledCounter;
    private final Counter failedCounter;
    private final Counter settledAmountCounter;
    private final Timer settlementTimer;
    private final Random random = new Random();

    private static final String[] BANKS = {
        "SBI", "HDFC", "ICICI", "Axis", "PNB", "BOB", "Kotak", "IndusInd", "YES", "IDBI"
    };

    public SettlementService(
            RestTemplate restTemplate,
            @Value("${upi.transaction-service-url}") String transactionServiceUrl,
            MeterRegistry registry) {
        this.restTemplate = restTemplate;
        this.transactionServiceUrl = transactionServiceUrl;
        this.settledCounter = Counter.builder("upi_settlements_total")
                .tag("status", "settled").register(registry);
        this.failedCounter = Counter.builder("upi_settlements_total")
                .tag("status", "failed").register(registry);
        this.settledAmountCounter = Counter.builder("upi_settlement_amount_total")
                .description("Total settled amount in INR").register(registry);
        this.settlementTimer = Timer.builder("upi_settlement_duration_seconds")
                .description("Settlement processing time").register(registry);
    }

    public SettlementResponse processSettlement(SettlementRequest request) {
        return settlementTimer.record(() -> doSettle(request));
    }

    @SuppressWarnings("unchecked")
    private SettlementResponse doSettle(SettlementRequest request) {
        SettlementResponse response = new SettlementResponse();
        response.setSettlementId("STL" + UUID.randomUUID().toString().substring(0, 10).toUpperCase());
        response.setAmount(request.getAmount());
        response.setPayerBank(BANKS[random.nextInt(BANKS.length)]);
        response.setPayeeBank(BANKS[random.nextInt(BANKS.length)]);

        // Call transaction service to initiate payment
        try {
            Map<String, Object> payRequest = Map.of(
                "payerVpa", request.getPayerVpa(),
                "payeeVpa", request.getPayeeVpa(),
                "amount", request.getAmount(),
                "remarks", request.getRemarks() != null ? request.getRemarks() : "Settlement"
            );

            ResponseEntity<Map> payResponse = restTemplate.postForEntity(
                transactionServiceUrl + "/api/upi/pay",
                payRequest,
                Map.class
            );

            if (payResponse.getStatusCode().is2xxSuccessful() && payResponse.getBody() != null) {
                response.setTransactionId((String) payResponse.getBody().get("transactionId"));
                response.setStatus("SETTLED");
                settledCounter.increment();
                settledAmountCounter.increment(request.getAmount());
            } else {
                response.setStatus("FAILED");
                response.setErrorMessage("Transaction service returned error");
                failedCounter.increment();
            }
        } catch (RestClientException e) {
            response.setStatus("FAILED");
            response.setErrorMessage("Transaction service unreachable: " + e.getMessage());
            failedCounter.increment();
        }

        return response;
    }
}
