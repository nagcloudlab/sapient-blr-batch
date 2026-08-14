package com.mts.nonfunctional.performance;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mts.dto.TransferRequest;
import com.mts.entity.Account;
import com.mts.entity.User;
import com.mts.enums.AccountType;
import com.mts.enums.TransferMode;
import com.mts.repository.AccountRepository;
import com.mts.repository.UserRepository;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * NON-FUNCTIONAL: Performance Tests
 *
 * Validates that API responses are within acceptable time limits.
 * In production, tools like JMeter or Gatling would be used for load testing.
 * These tests verify baseline response times under minimal load.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
@DisplayName("Non-Functional: Performance")
class ApiPerformanceTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;
    @Autowired private AccountRepository accountRepository;
    @Autowired private UserRepository userRepository;

    private static final long MAX_READ_MS = 500;     // Read APIs should respond within 500ms
    private static final long MAX_WRITE_MS = 1000;    // Write APIs should respond within 1s
    private static final long MAX_STATS_MS = 500;     // Stats API should respond within 500ms

    @BeforeEach
    void setUp() {
        User user = userRepository.save(User.builder()
                .username("perf.user").email("perf@test.com")
                .passwordHash("hash").fullName("Perf User").isActive(true).build());

        for (int i = 1; i <= 10; i++) {
            accountRepository.save(Account.builder()
                    .accountNumber("PERF" + String.format("%03d", i))
                    .user(user).accountType(AccountType.SAVINGS)
                    .balance(new BigDecimal("50000")).currency("INR").isActive(true).build());
        }
    }

    @Test
    @DisplayName("GET /api/accounts should respond within 500ms")
    void accountsListResponseTime() throws Exception {
        long start = System.currentTimeMillis();

        mockMvc.perform(get("/api/accounts"))
                .andExpect(status().isOk());

        long duration = System.currentTimeMillis() - start;
        assertTrue(duration < MAX_READ_MS,
                "GET /api/accounts took " + duration + "ms, expected < " + MAX_READ_MS + "ms");
    }

    @Test
    @DisplayName("GET /api/accounts/{number} should respond within 500ms")
    void singleAccountResponseTime() throws Exception {
        long start = System.currentTimeMillis();

        mockMvc.perform(get("/api/accounts/PERF001"))
                .andExpect(status().isOk());

        long duration = System.currentTimeMillis() - start;
        assertTrue(duration < MAX_READ_MS,
                "GET /api/accounts/PERF001 took " + duration + "ms, expected < " + MAX_READ_MS + "ms");
    }

    @Test
    @DisplayName("POST /api/transactions/transfer should complete within 1 second")
    void transferResponseTime() throws Exception {
        TransferRequest request = TransferRequest.builder()
                .fromAccountNumber("PERF001").toAccountNumber("PERF002")
                .amount(new BigDecimal("100")).transferMode(TransferMode.UPI)
                .description("Performance test").build();

        long start = System.currentTimeMillis();

        mockMvc.perform(post("/api/transactions/transfer")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated());

        long duration = System.currentTimeMillis() - start;
        assertTrue(duration < MAX_WRITE_MS,
                "POST transfer took " + duration + "ms, expected < " + MAX_WRITE_MS + "ms");
    }

    @Test
    @DisplayName("GET /api/transactions/stats should respond within 500ms")
    void statsResponseTime() throws Exception {
        long start = System.currentTimeMillis();

        mockMvc.perform(get("/api/transactions/stats"))
                .andExpect(status().isOk());

        long duration = System.currentTimeMillis() - start;
        assertTrue(duration < MAX_STATS_MS,
                "GET stats took " + duration + "ms, expected < " + MAX_STATS_MS + "ms");
    }

    @Test
    @DisplayName("10 sequential transfers should complete within 5 seconds (throughput)")
    void transferThroughput() throws Exception {
        long start = System.currentTimeMillis();

        for (int i = 1; i <= 10; i++) {
            TransferRequest request = TransferRequest.builder()
                    .fromAccountNumber("PERF001").toAccountNumber("PERF002")
                    .amount(new BigDecimal("10")).transferMode(TransferMode.UPI).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andExpect(status().isCreated());
        }

        long duration = System.currentTimeMillis() - start;
        long avgPerRequest = duration / 10;
        assertTrue(duration < 5000,
                "10 transfers took " + duration + "ms (avg " + avgPerRequest + "ms/req), expected < 5000ms");
    }

    @Test
    @DisplayName("GET /api/transactions/account/{number} should respond within 500ms with transaction history")
    void transactionHistoryResponseTime() throws Exception {
        // Create some transactions first
        for (int i = 0; i < 5; i++) {
            TransferRequest request = TransferRequest.builder()
                    .fromAccountNumber("PERF001").toAccountNumber("PERF003")
                    .amount(new BigDecimal("10")).transferMode(TransferMode.NEFT).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andExpect(status().isCreated());
        }

        long start = System.currentTimeMillis();

        mockMvc.perform(get("/api/transactions/account/PERF001"))
                .andExpect(status().isOk());

        long duration = System.currentTimeMillis() - start;
        assertTrue(duration < MAX_READ_MS,
                "GET transaction history took " + duration + "ms, expected < " + MAX_READ_MS + "ms");
    }
}
