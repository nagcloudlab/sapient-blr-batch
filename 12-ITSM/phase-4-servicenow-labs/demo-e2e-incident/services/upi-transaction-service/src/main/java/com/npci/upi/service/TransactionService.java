package com.npci.upi.service;

import com.npci.upi.model.UpiPaymentRequest;
import com.npci.upi.model.UpiPaymentResponse;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.stereotype.Service;

import java.util.Random;
import java.util.UUID;

@Service
public class TransactionService {

    private final ChaosService chaosService;
    private final Counter successCounter;
    private final Counter failureCounter;
    private final Counter totalAmountCounter;
    private final Timer transactionTimer;
    private final Random random = new Random();

    public TransactionService(ChaosService chaosService, MeterRegistry registry) {
        this.chaosService = chaosService;
        this.successCounter = Counter.builder("upi_transactions_total")
                .tag("status", "success")
                .description("Total successful UPI transactions")
                .register(registry);
        this.failureCounter = Counter.builder("upi_transactions_total")
                .tag("status", "failed")
                .description("Total failed UPI transactions")
                .register(registry);
        this.totalAmountCounter = Counter.builder("upi_transaction_amount_total")
                .description("Total UPI transaction amount in INR")
                .register(registry);
        this.transactionTimer = Timer.builder("upi_transaction_duration_seconds")
                .description("UPI transaction processing time")
                .register(registry);
    }

    public UpiPaymentResponse processPayment(UpiPaymentRequest request) {
        return transactionTimer.record(() -> doProcess(request));
    }

    private UpiPaymentResponse doProcess(UpiPaymentRequest request) {
        UpiPaymentResponse response = new UpiPaymentResponse();
        response.setTransactionId("TXN" + UUID.randomUUID().toString().substring(0, 12).toUpperCase());
        response.setRrn(String.valueOf(100000000000L + random.nextLong(900000000000L)));
        response.setPayerVpa(request.getPayerVpa());
        response.setPayeeVpa(request.getPayeeVpa());
        response.setAmount(request.getAmount());

        // Simulate latency
        int extraLatency = chaosService.getLatencyMs();
        if (extraLatency > 0) {
            try { Thread.sleep(extraLatency); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }

        // Simulate failures
        if (random.nextInt(100) < chaosService.getFailureRatePercent()) {
            response.setStatus("FAILED");
            String[] errorCodes = {"U16", "U28", "U30", "U67", "U78"};
            String[] errorMsgs = {
                "Risk threshold exceeded",
                "Unable to decrypt credentials",
                "Transaction not permitted to account",
                "Debit timeout at remitter bank",
                "PSP request timeout"
            };
            int idx = random.nextInt(errorCodes.length);
            response.setErrorCode(errorCodes[idx]);
            response.setErrorMessage(errorMsgs[idx]);
            failureCounter.increment();
            return response;
        }

        response.setStatus("SUCCESS");
        successCounter.increment();
        totalAmountCounter.increment(request.getAmount());
        return response;
    }
}
