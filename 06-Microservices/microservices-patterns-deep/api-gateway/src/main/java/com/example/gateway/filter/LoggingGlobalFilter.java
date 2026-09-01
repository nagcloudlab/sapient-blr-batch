package com.example.gateway.filter;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

import java.util.UUID;

/**
 * DEMO: API Monitoring - Request/Response Logging Filter
 *
 * Logs every request flowing through the gateway with timing info.
 * Adds a correlation ID for distributed tracing across services.
 */
@Component
public class LoggingGlobalFilter implements GlobalFilter, Ordered {

    private static final Logger log = LoggerFactory.getLogger(LoggingGlobalFilter.class);

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        long startTime = System.currentTimeMillis();

        // Generate correlation ID if not present
        String correlationId = exchange.getRequest().getHeaders().getFirst("X-Correlation-ID");
        if (correlationId == null) {
            correlationId = UUID.randomUUID().toString().substring(0, 8);
        }

        String method = exchange.getRequest().getMethod().name();
        String path = exchange.getRequest().getURI().getPath();
        String clientIp = exchange.getRequest().getRemoteAddress() != null
                ? exchange.getRequest().getRemoteAddress().getAddress().getHostAddress() : "unknown";

        log.info("[{}] >>> {} {} from {} | Headers: Host={}", correlationId, method, path, clientIp,
                exchange.getRequest().getHeaders().getFirst("Host"));

        // Add correlation ID to downstream request
        String finalCorrelationId = correlationId;
        ServerWebExchange mutatedExchange = exchange.mutate()
                .request(r -> r.header("X-Correlation-ID", finalCorrelationId))
                .build();

        return chain.filter(mutatedExchange).then(Mono.fromRunnable(() -> {
            long duration = System.currentTimeMillis() - startTime;
            int statusCode = mutatedExchange.getResponse().getStatusCode() != null
                    ? mutatedExchange.getResponse().getStatusCode().value() : 0;
            log.info("[{}] <<< {} {} | Status: {} | Duration: {}ms",
                    finalCorrelationId, method, path, statusCode, duration);
        }));
    }

    @Override
    public int getOrder() {
        return -2; // Run early in the filter chain
    }
}
