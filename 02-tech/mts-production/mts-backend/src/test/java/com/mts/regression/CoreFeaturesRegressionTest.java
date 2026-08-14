package com.mts.regression;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mts.dto.TransferRequest;
import com.mts.entity.Account;
import com.mts.entity.User;
import com.mts.enums.AccountType;
import com.mts.enums.TransferMode;
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

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * REGRESSION TESTS — Ensure previously working features still work
 *
 * MTS equivalent of "Old order flow still works after new feature"
 * Run these after adding new features (stats, all-transactions, etc.)
 * to ensure original account + transfer features are not broken.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
@DisplayName("Regression: Core Features Still Work")
class CoreFeaturesRegressionTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;
    @Autowired private AccountRepository accountRepository;
    @Autowired private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        User user1 = userRepository.save(User.builder()
                .username("reg.user1").email("reg1@test.com")
                .passwordHash("hash").fullName("Regression User 1").isActive(true).build());

        User user2 = userRepository.save(User.builder()
                .username("reg.user2").email("reg2@test.com")
                .passwordHash("hash").fullName("Regression User 2").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("REG001").user(user1).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("50000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("REG002").user(user1).accountType(AccountType.CURRENT)
                .balance(new BigDecimal("80000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("REG003").user(user2).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("25000")).currency("INR").isActive(true).build());
    }

    @Nested
    @DisplayName("Account Listing (original feature)")
    class AccountListing {

        @Test
        @DisplayName("GET /api/accounts still returns correct JSON structure")
        void accountListingStructure() throws Exception {
            mockMvc.perform(get("/api/accounts"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$").isArray())
                    .andExpect(jsonPath("$[0].accountNumber").isString())
                    .andExpect(jsonPath("$[0].ownerName").isString())
                    .andExpect(jsonPath("$[0].accountType").isString())
                    .andExpect(jsonPath("$[0].balance").isNumber())
                    .andExpect(jsonPath("$[0].currency").isString())
                    .andExpect(jsonPath("$[0].isActive").isBoolean());
        }

        @Test
        @DisplayName("GET /api/accounts/{number} still returns single account")
        void singleAccountStillWorks() throws Exception {
            mockMvc.perform(get("/api/accounts/REG001"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.accountNumber").value("REG001"))
                    .andExpect(jsonPath("$.balance").value(50000.0));
        }

        @Test
        @DisplayName("GET /api/accounts/{invalid} still returns 404 with error body")
        void accountNotFoundStillReturns404() throws Exception {
            mockMvc.perform(get("/api/accounts/INVALID"))
                    .andExpect(status().isNotFound())
                    .andExpect(jsonPath("$.status").value(404))
                    .andExpect(jsonPath("$.error").value("Account Not Found"))
                    .andExpect(jsonPath("$.message").isString())
                    .andExpect(jsonPath("$.timestamp").isString());
        }

        @Test
        @DisplayName("GET /api/accounts/user/{username} still filters by user")
        void accountsByUserStillWorks() throws Exception {
            mockMvc.perform(get("/api/accounts/user/reg.user1"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$", hasSize(2)))
                    .andExpect(jsonPath("$[*].ownerName", everyItem(is("Regression User 1"))));
        }
    }

    @Nested
    @DisplayName("Transfer (original feature)")
    class Transfer {

        @Test
        @DisplayName("POST transfer still returns 201 with correct response shape")
        void transferResponseShape() throws Exception {
            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("REG001").toAccountNumber("REG003")
                    .amount(new BigDecimal("5000")).transferMode(TransferMode.UPI)
                    .description("Regression test").build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.referenceId").isString())
                    .andExpect(jsonPath("$.fromAccountNumber").value("REG001"))
                    .andExpect(jsonPath("$.toAccountNumber").value("REG003"))
                    .andExpect(jsonPath("$.amount").value(5000.0))
                    .andExpect(jsonPath("$.currency").value("INR"))
                    .andExpect(jsonPath("$.transferMode").value("UPI"))
                    .andExpect(jsonPath("$.status").value("SUCCESS"))
                    .andExpect(jsonPath("$.timestamp").isString());
        }

        @Test
        @DisplayName("Validation errors still return 400 with field details")
        void validationErrorsStillWork() throws Exception {
            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content("{}"))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.error").value("Validation Failed"))
                    .andExpect(jsonPath("$.details").isArray())
                    .andExpect(jsonPath("$.details", hasSize(greaterThanOrEqualTo(3))));
        }

        @Test
        @DisplayName("Insufficient balance still returns 400 with specific error")
        void insufficientBalanceStillWorks() throws Exception {
            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("REG001").toAccountNumber("REG003")
                    .amount(new BigDecimal("999999")).transferMode(TransferMode.UPI).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.error").value("Insufficient Balance"));
        }
    }

    @Nested
    @DisplayName("Transaction History (original feature)")
    class TransactionHistory {

        @Test
        @DisplayName("GET /api/transactions/account/{number} still works after transfer")
        void historyByAccountStillWorks() throws Exception {
            // Create a transfer
            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("REG001").toAccountNumber("REG003")
                    .amount(new BigDecimal("1000")).transferMode(TransferMode.NEFT).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isCreated());

            // Verify history still works
            mockMvc.perform(get("/api/transactions/account/REG001"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$").isArray())
                    .andExpect(jsonPath("$[0].referenceId").isString())
                    .andExpect(jsonPath("$[0].status").value("SUCCESS"));
        }
    }
}
