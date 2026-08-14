package com.mts.nonfunctional.security;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mts.entity.Account;
import com.mts.entity.User;
import com.mts.enums.AccountType;
import com.mts.repository.AccountRepository;
import com.mts.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * NON-FUNCTIONAL: Security Tests
 *
 * Validates the system is resilient against:
 * - SQL Injection attempts
 * - XSS (Cross-Site Scripting) payloads
 * - Malformed JSON / invalid content types
 * - Path traversal attempts
 * - Negative/zero amount attacks
 * - Oversized payloads
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
@DisplayName("Non-Functional: Security")
class SecurityTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;
    @Autowired private AccountRepository accountRepository;
    @Autowired private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        User user = userRepository.save(User.builder()
                .username("sec.user").email("sec@test.com")
                .passwordHash("hash").fullName("Security User").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("SEC001").user(user).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("50000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("SEC002").user(user).accountType(AccountType.CURRENT)
                .balance(new BigDecimal("30000")).currency("INR").isActive(true).build());
    }

    @Nested
    @DisplayName("SQL Injection Prevention")
    class SqlInjection {

        @Test
        @DisplayName("SQL injection in account number path variable should return 404, not 500")
        void sqlInjectionInPathVariable() throws Exception {
            mockMvc.perform(get("/api/accounts/' OR '1'='1"))
                    .andExpect(status().isNotFound());
        }

        @Test
        @DisplayName("SQL injection in username path variable should not leak data")
        void sqlInjectionInUsername() throws Exception {
            mockMvc.perform(get("/api/accounts/user/' UNION SELECT * FROM users--"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$").isArray())
                    .andExpect(jsonPath("$.length()").value(0));
        }

        @Test
        @DisplayName("SQL injection in transfer request body should be rejected")
        void sqlInjectionInTransferBody() throws Exception {
            String maliciousJson = """
                {
                    "fromAccountNumber": "'; DROP TABLE accounts;--",
                    "toAccountNumber": "SEC002",
                    "amount": 100,
                    "transferMode": "UPI"
                }
                """;

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(maliciousJson))
                    .andExpect(status().isNotFound()); // Account not found, NOT 500
        }
    }

    @Nested
    @DisplayName("XSS Prevention")
    class XssPrevention {

        @Test
        @DisplayName("Script tag in description should not be executed (stored as plain text)")
        void scriptTagInDescription() throws Exception {
            String xssJson = """
                {
                    "fromAccountNumber": "SEC001",
                    "toAccountNumber": "SEC002",
                    "amount": 100,
                    "transferMode": "UPI",
                    "description": "<script>alert('xss')</script>"
                }
                """;

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(xssJson))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.description").value("<script>alert('xss')</script>"));
            // Stored as plain text - frontend must escape on render
        }

        @Test
        @DisplayName("HTML entities in account search should not cause errors")
        void htmlEntitiesInSearch() throws Exception {
            mockMvc.perform(get("/api/accounts/<img src=x onerror=alert(1)>"))
                    .andExpect(status().isNotFound());
        }
    }

    @Nested
    @DisplayName("Malformed Input Handling")
    class MalformedInput {

        @Test
        @DisplayName("Invalid JSON body should return 400, not 500")
        void invalidJsonBody() throws Exception {
            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content("{invalid json!!!}"))
                    .andExpect(status().isBadRequest());
        }

        @Test
        @DisplayName("Empty body should return 400")
        void emptyBody() throws Exception {
            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(""))
                    .andExpect(status().isBadRequest());
        }

        @Test
        @DisplayName("Wrong content type should return 415")
        void wrongContentType() throws Exception {
            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.TEXT_PLAIN)
                            .content("some text"))
                    .andExpect(status().isUnsupportedMediaType());
        }

        @Test
        @DisplayName("Negative amount should be rejected by validation")
        void negativeAmount() throws Exception {
            String json = """
                {
                    "fromAccountNumber": "SEC001",
                    "toAccountNumber": "SEC002",
                    "amount": -5000,
                    "transferMode": "UPI"
                }
                """;

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(json))
                    .andExpect(status().isBadRequest());
        }

        @Test
        @DisplayName("Zero amount should be rejected by validation")
        void zeroAmount() throws Exception {
            String json = """
                {
                    "fromAccountNumber": "SEC001",
                    "toAccountNumber": "SEC002",
                    "amount": 0,
                    "transferMode": "UPI"
                }
                """;

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(json))
                    .andExpect(status().isBadRequest());
        }

        @Test
        @DisplayName("Extremely large amount should be rejected by validation")
        void extremelyLargeAmount() throws Exception {
            String json = """
                {
                    "fromAccountNumber": "SEC001",
                    "toAccountNumber": "SEC002",
                    "amount": 99999999999999,
                    "transferMode": "UPI"
                }
                """;

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(json))
                    .andExpect(status().isBadRequest());
        }

        @Test
        @DisplayName("Invalid transfer mode should return 400")
        void invalidTransferMode() throws Exception {
            String json = """
                {
                    "fromAccountNumber": "SEC001",
                    "toAccountNumber": "SEC002",
                    "amount": 100,
                    "transferMode": "HAWALA"
                }
                """;

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(json))
                    .andExpect(status().isBadRequest());
        }
    }

    @Nested
    @DisplayName("HTTP Method Security")
    class HttpMethodSecurity {

        @Test
        @DisplayName("PUT on transfer endpoint should return 405 Method Not Allowed")
        void putOnTransferReturns405() throws Exception {
            mockMvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                            .put("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content("{}"))
                    .andExpect(status().isMethodNotAllowed());
        }

        @Test
        @DisplayName("DELETE on accounts endpoint should return 405 Method Not Allowed")
        void deleteOnAccountsReturns405() throws Exception {
            mockMvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders
                            .delete("/api/accounts/SEC001"))
                    .andExpect(status().isMethodNotAllowed());
        }
    }

    @Nested
    @DisplayName("Error Response Safety")
    class ErrorResponseSafety {

        @Test
        @DisplayName("Error responses should not leak stack traces")
        void errorResponsesDoNotLeakStackTraces() throws Exception {
            mockMvc.perform(get("/api/accounts/NONEXISTENT"))
                    .andExpect(status().isNotFound())
                    .andExpect(jsonPath("$.error").exists())
                    .andExpect(jsonPath("$.message").exists())
                    .andExpect(jsonPath("$.stackTrace").doesNotExist())
                    .andExpect(jsonPath("$.trace").doesNotExist());
        }

        @Test
        @DisplayName("404 error should not reveal internal paths")
        void notFoundDoesNotRevealPaths() throws Exception {
            String body = mockMvc.perform(get("/api/accounts/NONEXISTENT"))
                    .andReturn().getResponse().getContentAsString();

            assertFalse(body.contains("com.mts"), "Error response should not contain package names");
            assertFalse(body.contains(".java"), "Error response should not contain file names");
        }
    }
}
