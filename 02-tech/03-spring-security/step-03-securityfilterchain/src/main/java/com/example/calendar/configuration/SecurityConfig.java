package com.example.calendar.configuration;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

import static org.springframework.security.config.Customizer.withDefaults;

/**
 * Step 03: Our FIRST custom security configuration!
 *
 * By defining this bean, we REPLACE the auto-configured SecurityFilterChain.
 * Now WE control what is secured and what is public.
 */
@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

        http
            // 1. Authorization rules: WHO can access WHAT
            .authorizeHttpRequests(authorize -> authorize
                // Public pages - no login needed
                .requestMatchers("/", "/login", "/logout").permitAll()
                // Static resources - CSS, JS, WebJars
                .requestMatchers("/css/**", "/webjars/**").permitAll()
                // H2 Console (for development only!)
                .requestMatchers("/h2-console/**").permitAll()
                // Everything else requires authentication
                .anyRequest().authenticated()
            )

            // 2. Form login - use Spring's default login page (for now)
            .formLogin(withDefaults())

            // 3. HTTP Basic - also allow API-style auth
            .httpBasic(withDefaults())

            // 4. H2 Console needs frames and CSRF disabled
            .headers(headers -> headers
                .frameOptions(frame -> frame.sameOrigin())
            )
            .csrf(csrf -> csrf
                .ignoringRequestMatchers("/h2-console/**")
            );

        return http.build();
    }
}
