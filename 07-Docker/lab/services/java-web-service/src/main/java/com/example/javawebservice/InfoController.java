package com.example.javawebservice;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class InfoController {

    @Value("${spring.profiles.active:default}")
    private String activeProfile;

    @GetMapping("/api/info")
    public Map<String, String> info() {
        return Map.of(
            "service", "java-web-service",
            "version", "1.0.0",
            "profile", activeProfile
        );
    }

    @GetMapping("/api/health")
    public Map<String, String> health() {
        return Map.of("status", "UP");
    }
}
