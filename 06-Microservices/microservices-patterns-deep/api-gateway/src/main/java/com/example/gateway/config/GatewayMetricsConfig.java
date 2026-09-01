package com.example.gateway.config;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * DEMO: API Monitoring & Observability - Custom Metrics
 *
 * Custom Micrometer metrics for gateway traffic monitoring.
 * Tracks requests per route, error rates, and gateway health.
 */
@Configuration
public class GatewayMetricsConfig {

    private final AtomicLong totalRequests = new AtomicLong(0);
    private final AtomicLong totalErrors = new AtomicLong(0);
    private final Map<String, AtomicLong> routeCounters = new ConcurrentHashMap<>();

    @Bean
    public GlobalFilter metricsFilter(MeterRegistry meterRegistry) {
        Counter requestCounter = Counter.builder("gateway.requests.total")
                .description("Total requests through gateway")
                .register(meterRegistry);

        Counter errorCounter = Counter.builder("gateway.errors.total")
                .description("Total error responses from gateway")
                .register(meterRegistry);

        return (ServerWebExchange exchange, GatewayFilterChain chain) -> {
            totalRequests.incrementAndGet();
            requestCounter.increment();

            String path = exchange.getRequest().getURI().getPath();
            String routeKey = extractRouteKey(path);
            routeCounters.computeIfAbsent(routeKey, k -> new AtomicLong(0)).incrementAndGet();

            Counter.builder("gateway.route.requests")
                    .tag("route", routeKey)
                    .register(meterRegistry)
                    .increment();

            return chain.filter(exchange).then(Mono.fromRunnable(() -> {
                int status = exchange.getResponse().getStatusCode() != null
                        ? exchange.getResponse().getStatusCode().value() : 0;
                if (status >= 400) {
                    totalErrors.incrementAndGet();
                    errorCounter.increment();
                }
            }));
        };
    }

    public Map<String, Object> getStats() {
        Map<String, Object> stats = new java.util.LinkedHashMap<>();
        stats.put("totalRequests", totalRequests.get());
        stats.put("totalErrors", totalErrors.get());
        double errorRate = totalRequests.get() > 0
                ? (double) totalErrors.get() / totalRequests.get() * 100 : 0;
        stats.put("errorRate", String.format("%.2f%%", errorRate));
        stats.put("routeStats", routeCounters);
        return stats;
    }

    private String extractRouteKey(String path) {
        if (path.startsWith("/orders")) return "order-service";
        if (path.startsWith("/inventory")) return "inventory-service";
        if (path.startsWith("/api/v1/inventory")) return "inventory-service-v1";
        if (path.startsWith("/auth")) return "auth";
        if (path.startsWith("/actuator")) return "actuator";
        return "other";
    }
}
