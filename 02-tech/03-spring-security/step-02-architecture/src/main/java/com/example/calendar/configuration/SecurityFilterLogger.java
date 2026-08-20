package com.example.calendar.configuration;

import jakarta.servlet.Filter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.boot.CommandLineRunner;
import org.springframework.security.web.FilterChainProxy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.stereotype.Component;

/**
 * Step 02: Prints ALL security filters in the chain at startup.
 * This helps participants SEE what Spring Security registers.
 */
@Component
public class SecurityFilterLogger implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(SecurityFilterLogger.class);

    private final FilterChainProxy filterChainProxy;

    public SecurityFilterLogger(FilterChainProxy filterChainProxy) {
        this.filterChainProxy = filterChainProxy;
    }

    @Override
    public void run(String... args) {
        log.info("╔══════════════════════════════════════════════════════════════╗");
        log.info("║         SPRING SECURITY FILTER CHAIN                       ║");
        log.info("╠══════════════════════════════════════════════════════════════╣");

        int chainNum = 0;
        for (SecurityFilterChain chain : filterChainProxy.getFilterChains()) {
            chainNum++;
            log.info("║ Chain #{}: {}", chainNum, chain.getClass().getSimpleName());
            int filterNum = 0;
            for (Filter filter : chain.getFilters()) {
                filterNum++;
                String name = filter.getClass().getSimpleName();
                log.info("║   [{}] {}", String.format("%2d", filterNum), name);
            }
        }

        log.info("╚══════════════════════════════════════════════════════════════╝");
    }
}
