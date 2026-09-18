package com.foodexpress.controller;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.List;
import java.util.Map;

@RestController
public class ApiController {

    // ─── PUBLIC (no token needed) ───
    @GetMapping("/public/health")
    public Map<String, Object> health() {
        return Map.of(
            "status", "ok",
            "service", "resource-server",
            "timestamp", Instant.now().toString()
        );
    }

    @GetMapping("/public/menu")
    public List<Map<String, Object>> menu() {
        return List.of(
            Map.of("id", 1, "name", "Biryani", "price", 350),
            Map.of("id", 2, "name", "Dosa", "price", 120),
            Map.of("id", 3, "name", "Paneer Tikka", "price", 280),
            Map.of("id", 4, "name", "Naan", "price", 60),
            Map.of("id", 5, "name", "Gulab Jamun", "price", 80)
        );
    }

    // ─── PROTECTED (any valid token) ───
    @GetMapping("/profile")
    public Map<String, Object> profile(@AuthenticationPrincipal Jwt jwt) {
        return Map.of(
            "message", "This is a PROTECTED endpoint. You have a valid token!",
            "username", jwt.getClaimAsString("preferred_username"),
            "email", jwt.getClaimAsString("email"),
            "name", jwt.getClaimAsString("name"),
            "roles", extractRoles(jwt),
            "tokenIssuer", jwt.getIssuer().toString(),
            "tokenExpiry", jwt.getExpiresAt().toString(),
            "tokenId", jwt.getId()
        );
    }

    @GetMapping("/orders")
    public Map<String, Object> orders(@AuthenticationPrincipal Jwt jwt) {
        String username = jwt.getClaimAsString("preferred_username");
        return Map.of(
            "message", "Orders for " + username,
            "orders", List.of(
                Map.of("id", "ORD-001", "item", "Biryani x2", "total", 700, "status", "DELIVERED"),
                Map.of("id", "ORD-002", "item", "Dosa x3", "total", 360, "status", "PREPARING"),
                Map.of("id", "ORD-003", "item", "Paneer Tikka x1", "total", 280, "status", "CONFIRMED")
            )
        );
    }

    // ─── ROLE-BASED (specific role needed) ───
    @GetMapping("/admin/users")
    @PreAuthorize("hasRole('admin')")
    public Map<String, Object> adminUsers(@AuthenticationPrincipal Jwt jwt) {
        return Map.of(
            "message", "Admin-only endpoint! You have the 'admin' role.",
            "requestedBy", jwt.getClaimAsString("preferred_username"),
            "users", List.of(
                Map.of("username", "rahul", "role", "customer"),
                Map.of("username", "priya", "role", "restaurant-owner"),
                Map.of("username", "admin", "role", "admin")
            )
        );
    }

    @GetMapping("/restaurant/dashboard")
    @PreAuthorize("hasRole('restaurant-owner') or hasRole('admin')")
    public Map<String, Object> restaurantDashboard(@AuthenticationPrincipal Jwt jwt) {
        return Map.of(
            "message", "Restaurant dashboard. Requires 'restaurant-owner' or 'admin' role.",
            "requestedBy", jwt.getClaimAsString("preferred_username"),
            "todayOrders", 42,
            "revenue", 18500,
            "avgRating", 4.3
        );
    }

    // ─── TOKEN INTROSPECTION (for teaching) ───
    @GetMapping("/debug/token")
    public Map<String, Object> debugToken(@AuthenticationPrincipal Jwt jwt) {
        return Map.of(
            "header", Map.of(
                "algorithm", jwt.getHeaders().get("alg"),
                "type", jwt.getHeaders().get("typ"),
                "keyId", jwt.getHeaders().get("kid")
            ),
            "payload", jwt.getClaims(),
            "roles", extractRoles(jwt),
            "issuedAt", jwt.getIssuedAt().toString(),
            "expiresAt", jwt.getExpiresAt().toString(),
            "issuer", jwt.getIssuer().toString(),
            "subject", jwt.getSubject(),
            "audience", jwt.getAudience()
        );
    }

    @SuppressWarnings("unchecked")
    private List<String> extractRoles(Jwt jwt) {
        Map<String, Object> realmAccess = jwt.getClaimAsMap("realm_access");
        if (realmAccess != null && realmAccess.containsKey("roles")) {
            return (List<String>) realmAccess.get("roles");
        }
        return List.of();
    }
}
