package com.example.gateway.filter;

import io.github.bucket4j.Bandwidth;
import io.github.bucket4j.Bucket;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * DEMO: Traffic Management - Rate Limiting Filter
 *
 * In-memory rate limiting using Bucket4j (Token Bucket algorithm).
 * Limits each client IP to a configurable number of requests per minute.
 * Returns 429 Too Many Requests when limit is exceeded.
 */
@Component
public class RateLimitingFilter implements GlobalFilter, Ordered {

    private static final Logger log = LoggerFactory.getLogger(RateLimitingFilter.class);
    private static final int REQUESTS_PER_MINUTE = 30;

    private final Map<String, Bucket> buckets = new ConcurrentHashMap<>();

    private Bucket createBucket() {
        return Bucket.builder()
                .addLimit(Bandwidth.simple(REQUESTS_PER_MINUTE, Duration.ofMinutes(1)))
                .build();
    }

    private Bucket resolveBucket(String clientIp) {
        return buckets.computeIfAbsent(clientIp, k -> createBucket());
    }

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        // Skip rate limiting for actuator endpoints
        String path = exchange.getRequest().getURI().getPath();
        if (path.startsWith("/actuator")) {
            return chain.filter(exchange);
        }

        String clientIp = exchange.getRequest().getRemoteAddress() != null
                ? exchange.getRequest().getRemoteAddress().getAddress().getHostAddress() : "unknown";

        Bucket bucket = resolveBucket(clientIp);

        if (bucket.tryConsume(1)) {
            long remaining = bucket.getAvailableTokens();
            exchange.getResponse().getHeaders().add("X-RateLimit-Remaining", String.valueOf(remaining));
            exchange.getResponse().getHeaders().add("X-RateLimit-Limit", String.valueOf(REQUESTS_PER_MINUTE));
            return chain.filter(exchange);
        } else {
            log.warn("Rate limit exceeded for client: {}", clientIp);
            exchange.getResponse().setStatusCode(HttpStatus.TOO_MANY_REQUESTS);
            exchange.getResponse().getHeaders().add("X-RateLimit-Retry-After", "60");
            return exchange.getResponse().setComplete();
        }
    }

    @Override
    public int getOrder() {
        return -1; // Run after logging but before other filters
    }
}
