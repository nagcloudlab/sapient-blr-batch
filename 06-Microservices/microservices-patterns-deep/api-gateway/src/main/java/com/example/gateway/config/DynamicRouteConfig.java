package com.example.gateway.config;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;

/**
 * DEMO: Dynamic Routing & Traffic Management
 *
 * Programmatic route definitions using RouteLocatorBuilder.
 * Shows various predicates (path, method, header, weight) and filters.
 *
 * Routes defined here work alongside YAML-based routes in application.yml
 */
@Configuration
public class DynamicRouteConfig {

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()

                // ---- DYNAMIC ROUTING: Header-based routing ----
                // Routes to order-service only if X-Version header is "v2"
                .route("order-service-v2-header", r -> r
                        .path("/orders/**")
                        .and().header("X-Version", "v2")
                        .filters(f -> f
                                .addRequestHeader("X-Routed-By", "header-predicate-v2")
                                .addResponseHeader("X-Route-Match", "header-based"))
                        .uri("lb://order-service"))

                // ---- DYNAMIC ROUTING: Method-based routing ----
                // Only allow POST to /orders via this specific route
                .route("order-service-post-only", r -> r
                        .path("/orders")
                        .and().method(HttpMethod.POST)
                        .filters(f -> f
                                .addRequestHeader("X-Routed-By", "method-predicate-POST")
                                .addResponseHeader("X-Route-Match", "method-based"))
                        .uri("lb://order-service"))

                // ---- TRAFFIC MANAGEMENT: Weight-based routing (Canary) ----
                // 80% traffic to inventory-service (stable)
                .route("inventory-stable", r -> r
                        .path("/inventory/**")
                        .and().weight("inventory-group", 8)
                        .filters(f -> f
                                .addRequestHeader("X-Routed-By", "canary-stable")
                                .addResponseHeader("X-Canary", "false"))
                        .uri("lb://inventory-service"))

                // 20% traffic to inventory-service (canary) - same service, different header
                .route("inventory-canary", r -> r
                        .path("/inventory/**")
                        .and().weight("inventory-group", 2)
                        .filters(f -> f
                                .addRequestHeader("X-Routed-By", "canary-new")
                                .addRequestHeader("X-Canary-Version", "v2")
                                .addResponseHeader("X-Canary", "true"))
                        .uri("lb://inventory-service"))

                // ---- GATEWAY: Circuit Breaker route ----
                // Wraps order-service calls with circuit breaker
                .route("order-service-circuit-breaker", r -> r
                        .path("/orders/**")
                        .filters(f -> f
                                .circuitBreaker(cb -> cb
                                        .setName("orderServiceCB")
                                        .setFallbackUri("forward:/fallback/orders"))
                                .retry(retryConfig -> retryConfig.setRetries(2))
                                .addRequestHeader("X-Routed-By", "circuit-breaker-route"))
                        .uri("lb://order-service"))

                // ---- DYNAMIC ROUTING: Path rewrite ----
                // /api/v1/inventory/** -> /inventory/**
                .route("inventory-path-rewrite", r -> r
                        .path("/api/v1/inventory/**")
                        .filters(f -> f
                                .rewritePath("/api/v1/inventory/(?<segment>.*)", "/inventory/${segment}")
                                .addResponseHeader("X-Route-Match", "path-rewrite"))
                        .uri("lb://inventory-service"))

                .build();
    }
}
