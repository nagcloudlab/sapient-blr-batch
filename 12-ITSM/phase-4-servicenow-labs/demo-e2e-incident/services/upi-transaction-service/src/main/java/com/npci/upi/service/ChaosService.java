package com.npci.upi.service;

import org.springframework.stereotype.Service;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

@Service
public class ChaosService {

    private final AtomicBoolean serviceDown = new AtomicBoolean(false);
    private final AtomicInteger failureRatePercent = new AtomicInteger(0);
    private final AtomicInteger latencyMs = new AtomicInteger(0);

    public boolean isServiceDown() {
        return serviceDown.get();
    }

    public int getFailureRatePercent() {
        return failureRatePercent.get();
    }

    public int getLatencyMs() {
        return latencyMs.get();
    }

    public void enableChaos() {
        failureRatePercent.set(80);
    }

    public void disableChaos() {
        failureRatePercent.set(0);
        latencyMs.set(0);
        serviceDown.set(false);
    }

    public void setLatency(int ms) {
        latencyMs.set(ms);
    }

    public void setServiceDown(boolean down) {
        serviceDown.set(down);
    }

    public Map<String, Object> getStatus() {
        return Map.of(
            "service_down", serviceDown.get(),
            "failure_rate_percent", failureRatePercent.get(),
            "latency_ms", latencyMs.get()
        );
    }
}
