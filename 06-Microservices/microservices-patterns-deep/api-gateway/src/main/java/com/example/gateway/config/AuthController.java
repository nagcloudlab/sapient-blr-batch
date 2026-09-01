package com.example.gateway.config;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * DEMO: Security & Auth - Token Generation Endpoint
 *
 * Provides JWT token generation for demo purposes.
 * In production, this would be a separate auth service (Keycloak, Auth0, etc.)
 */
@RestController
@RequestMapping("/auth")
public class AuthController {

    @Value("${jwt.secret:MyDemoSecretKeyForJWTTokenGeneration2024!}")
    private String jwtSecret;

    @PostMapping("/login")
    public Mono<ResponseEntity<Map<String, Object>>> login(@RequestBody Map<String, String> credentials) {
        String username = credentials.getOrDefault("username", "");
        String password = credentials.getOrDefault("password", "");

        // Simple demo authentication
        String role;
        if ("admin".equals(username) && "admin123".equals(password)) {
            role = "ADMIN";
        } else if ("user".equals(username) && "user123".equals(password)) {
            role = "USER";
        } else {
            Map<String, Object> error = new LinkedHashMap<>();
            error.put("error", "Invalid credentials");
            error.put("message", "Use admin/admin123 or user/user123");
            return Mono.just(ResponseEntity.status(401).body(error));
        }

        SecretKey key = Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8));

        String token = Jwts.builder()
                .subject(username)
                .claim("role", role)
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + 3600000)) // 1 hour
                .signWith(key)
                .compact();

        Map<String, Object> response = new LinkedHashMap<>();
        response.put("token", token);
        response.put("type", "Bearer");
        response.put("username", username);
        response.put("role", role);
        response.put("expiresIn", "3600s");

        return Mono.just(ResponseEntity.ok(response));
    }

    @GetMapping("/info")
    public Mono<ResponseEntity<Map<String, String>>> info() {
        Map<String, String> info = new LinkedHashMap<>();
        info.put("endpoint", "POST /auth/login");
        info.put("body", "{\"username\": \"admin\", \"password\": \"admin123\"}");
        info.put("alternative", "Header: X-API-Key: demo-api-key-2024");
        info.put("users", "admin/admin123 (ADMIN role), user/user123 (USER role)");
        return Mono.just(ResponseEntity.ok(info));
    }
}
