package com.mts.smoke;

import com.mts.controller.AccountController;
import com.mts.controller.TransactionController;
import com.mts.repository.AccountRepository;
import com.mts.repository.TransactionRepository;
import com.mts.repository.UserRepository;
import com.mts.service.AccountService;
import com.mts.service.TransferService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * SMOKE TESTS — Critical path verification after deployment
 *
 * MTS equivalent of "Can users log in and search restaurants?"
 * Quick tests to verify the app is alive and core features work.
 * Run these FIRST after any deployment.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@DisplayName("Smoke: Critical Path Verification")
class SmokeTest {

    @Autowired private MockMvc mockMvc;
    @Autowired(required = false) private AccountController accountController;
    @Autowired(required = false) private TransactionController transactionController;
    @Autowired(required = false) private AccountService accountService;
    @Autowired(required = false) private TransferService transferService;
    @Autowired(required = false) private AccountRepository accountRepository;
    @Autowired(required = false) private TransactionRepository transactionRepository;
    @Autowired(required = false) private UserRepository userRepository;

    @Test
    @DisplayName("Application context loads successfully")
    void contextLoads() {
        // If this test passes, Spring Boot app started without errors
    }

    @Test
    @DisplayName("All controllers are wired")
    void controllersAreWired() {
        assertNotNull(accountController, "AccountController should be wired");
        assertNotNull(transactionController, "TransactionController should be wired");
    }

    @Test
    @DisplayName("All services are wired")
    void servicesAreWired() {
        assertNotNull(accountService, "AccountService should be wired");
        assertNotNull(transferService, "TransferService should be wired");
    }

    @Test
    @DisplayName("All repositories are wired")
    void repositoriesAreWired() {
        assertNotNull(accountRepository, "AccountRepository should be wired");
        assertNotNull(transactionRepository, "TransactionRepository should be wired");
        assertNotNull(userRepository, "UserRepository should be wired");
    }

    @Test
    @DisplayName("GET /api/accounts responds with 200")
    void accountsEndpointResponds() throws Exception {
        mockMvc.perform(get("/api/accounts"))
                .andExpect(status().isOk())
                .andExpect(content().contentType("application/json"));
    }

    @Test
    @DisplayName("GET /api/transactions responds with 200")
    void transactionsEndpointResponds() throws Exception {
        mockMvc.perform(get("/api/transactions"))
                .andExpect(status().isOk())
                .andExpect(content().contentType("application/json"));
    }

    @Test
    @DisplayName("GET /api/transactions/stats responds with 200 and correct shape")
    void statsEndpointResponds() throws Exception {
        mockMvc.perform(get("/api/transactions/stats"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalAccounts").isNumber())
                .andExpect(jsonPath("$.totalTransactions").isNumber())
                .andExpect(jsonPath("$.totalBalance").isNumber());
    }

    @Test
    @DisplayName("H2 database is accessible and has tables")
    void databaseIsAccessible() {
        long count = userRepository.count();
        // Just verifying DB connection works — count can be 0 in test profile
        assertNotNull(count);
    }
}
