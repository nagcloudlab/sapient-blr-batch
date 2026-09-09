package com.example.helloapi;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.time.LocalDateTime;
import java.util.Map;

@RestController
public class HelloController {

    @GetMapping("/")
    public Map<String, String> home() {
        return Map.of(
            "app", "hello-api",
            "status", "running",
            "timestamp", LocalDateTime.now().toString()
        );
    }

    @GetMapping("/api/hello")
    public Map<String, String> hello(@RequestParam(defaultValue = "World") String name) {
        return Map.of(
            "message", "Hello, " + name + "!",
            "from", System.getenv().getOrDefault("HOSTNAME", "unknown")
        );
    }

    @GetMapping("/api/info")
    public Map<String, Object> info() {
        Runtime rt = Runtime.getRuntime();
        return Map.of(
            "java.version", System.getProperty("java.version"),
            "os", System.getProperty("os.name"),
            "cpus", rt.availableProcessors(),
            "memory.free.mb", rt.freeMemory() / (1024 * 1024),
            "memory.total.mb", rt.totalMemory() / (1024 * 1024)
        );
    }
}
