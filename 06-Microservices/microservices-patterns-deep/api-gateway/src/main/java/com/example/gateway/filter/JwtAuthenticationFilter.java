package com.example.gateway.filter;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * DEMO: Security & Auth - JWT Authentication Filter
 *
 * Validates JWT tokens on protected routes.
 * Extracts user info from token and passes it as headers to downstream services.
 * Public routes (like /auth/**, /actuator/**) bypass authentication.
 */
@Component
public class JwtAuthenticationFilter implements GlobalFilter, Ordered {

    private static final Logger log = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

    // Public routes that don't require authentication
    private static final List<String> PUBLIC_PATHS = List.of(
            "/auth/", "/actuator/", "/public/"
    );

    @Value("${jwt.secret:MyDemoSecretKeyForJWTTokenGeneration2024!}")
    private String jwtSecret;

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String path = exchange.getRequest().getURI().getPath();

        // Skip auth for public paths
        if (isPublicPath(path)) {
            return chain.filter(exchange);
        }

        // Check for API Key first (alternative auth method)
        String apiKey = exchange.getRequest().getHeaders().getFirst("X-API-Key");
        if ("demo-api-key-2024".equals(apiKey)) {
            log.info("Request authenticated via API Key for path: {}", path);
            ServerWebExchange mutated = exchange.mutate()
                    .request(r -> r.header("X-User", "api-key-user")
                            .header("X-User-Role", "SERVICE"))
                    .build();
            return chain.filter(mutated);
        }

        // Check for Bearer token
        String authHeader = exchange.getRequest().getHeaders().getFirst("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            log.warn("Missing or invalid Authorization header for path: {}", path);
            return unauthorizedResponse(exchange, "Missing or invalid Authorization header");
        }

        String token = authHeader.substring(7);
        try {
            SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));
            Claims claims = Jwts.parser()
                    .verifyWith(key)
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();

            String username = claims.getSubject();
            String role = claims.get("role", String.class);

            log.info("JWT authenticated: user={}, role={}, path={}", username, role, path);

            // Pass user info to downstream services via headers
            ServerWebExchange mutated = exchange.mutate()
                    .request(r -> r.header("X-User", username)
                            .header("X-User-Role", role != null ? role : "USER"))
                    .build();

            return chain.filter(mutated);

        } catch (Exception e) {
            log.warn("Invalid JWT token: {}", e.getMessage());
            return unauthorizedResponse(exchange, "Invalid or expired JWT token");
        }
    }

    private Mono<Void> unauthorizedResponse(ServerWebExchange exchange, String message) {
        exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
        exchange.getResponse().getHeaders().setContentType(MediaType.APPLICATION_JSON);
        String body = "{\"error\":\"Unauthorized\",\"message\":\"" + message + "\"}";
        DataBuffer buffer = exchange.getResponse().bufferFactory()
                .wrap(body.getBytes(StandardCharsets.UTF_8));
        return exchange.getResponse().writeWith(Mono.just(buffer));
    }

    private boolean isPublicPath(String path) {
        return PUBLIC_PATHS.stream().anyMatch(path::startsWith);
    }

    @Override
    public int getOrder() {
        return 1; // Run after rate limiting
    }
}
