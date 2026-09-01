package com.example.gateway.config;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

import java.util.Map;

/**
 * DEMO: API Monitoring - Gateway Stats Endpoint
 *
 * Exposes custom gateway traffic statistics as a REST endpoint.
 */
@RestController
@RequestMapping("/public")
public class GatewayStatsController {

    private final GatewayMetricsConfig metricsConfig;

    public GatewayStatsController(GatewayMetricsConfig metricsConfig) {
        this.metricsConfig = metricsConfig;
    }

    @GetMapping("/gateway-stats")
    public Mono<ResponseEntity<Map<String, Object>>> getStats() {
        return Mono.just(ResponseEntity.ok(metricsConfig.getStats()));
    }
}
