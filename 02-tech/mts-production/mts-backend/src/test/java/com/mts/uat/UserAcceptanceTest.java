package com.mts.uat;

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
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * UAT TESTS — Business Requirement Validation
 *
 * MTS equivalent of "Product owner verifies order flow"
 * Written from the BUSINESS perspective, not the technical one.
 * Each test maps to a business requirement / user story.
 *
 * Naming: "As a [user], I should be able to [action] so that [outcome]"
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
@DisplayName("UAT: Business Requirements")
class UserAcceptanceTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;
    @Autowired private AccountRepository accountRepository;
    @Autowired private UserRepository userRepository;

    private User ravi, priya;

    @BeforeEach
    void setUp() {
        ravi = userRepository.save(User.builder()
                .username("ravi.uat").email("ravi.uat@bank.com")
                .passwordHash("hash").fullName("Ravi Kumar").isActive(true).build());

        priya = userRepository.save(User.builder()
                .username("priya.uat").email("priya.uat@bank.com")
                .passwordHash("hash").fullName("Priya Sharma").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("UAT001").user(ravi).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("50000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("UAT002").user(ravi).accountType(AccountType.CURRENT)
                .balance(new BigDecimal("100000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("UAT003").user(priya).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("25000")).currency("INR").isActive(true).build());
    }

    @Nested
    @DisplayName("Story: As a user, I should be able to view my accounts")
    class ViewAccounts {

        @Test
        @DisplayName("AC1: I can see all my accounts with balances")
        void canSeeAllAccountsWithBalances() throws Exception {
            mockMvc.perform(get("/api/accounts/user/ravi.uat"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$", hasSize(2)))
                    .andExpect(jsonPath("$[0].balance").isNumber())
                    .andExpect(jsonPath("$[1].balance").isNumber());
        }

        @Test
        @DisplayName("AC2: Account details show owner name, type, and currency")
        void accountShowsCompleteDetails() throws Exception {
            mockMvc.perform(get("/api/accounts/UAT001"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.ownerName").value("Ravi Kumar"))
                    .andExpect(jsonPath("$.accountType").value("SAVINGS"))
                    .andExpect(jsonPath("$.currency").value("INR"));
        }
    }

    @Nested
    @DisplayName("Story: As a user, I should be able to transfer money to another account")
    class TransferMoney {

        @Test
        @DisplayName("AC1: I can send money and the receiver gets it")
        void canSendMoneyAndReceiverGetsIt() throws Exception {
            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("UAT001").toAccountNumber("UAT003")
                    .amount(new BigDecimal("10000")).transferMode(TransferMode.UPI)
                    .description("Birthday gift").build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isCreated())
                    .andExpect(jsonPath("$.status").value("SUCCESS"));

            // Sender's balance decreased
            mockMvc.perform(get("/api/accounts/UAT001"))
                    .andExpect(jsonPath("$.balance").value(40000.0));

            // Receiver's balance increased
            mockMvc.perform(get("/api/accounts/UAT003"))
                    .andExpect(jsonPath("$.balance").value(35000.0));
        }

        @Test
        @DisplayName("AC2: I get a unique reference ID for every transfer")
        void getUniqueReferenceForEveryTransfer() throws Exception {
            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("UAT001").toAccountNumber("UAT003")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build();

            MvcResult r1 = mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(jsonPath("$.referenceId").isString())
                    .andReturn();

            MvcResult r2 = mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andReturn();

            String ref1 = objectMapper.readTree(r1.getResponse().getContentAsString()).get("referenceId").asText();
            String ref2 = objectMapper.readTree(r2.getResponse().getContentAsString()).get("referenceId").asText();
            assertNotEquals(ref1, ref2);
        }

        @Test
        @DisplayName("AC3: I cannot send more money than my balance")
        void cannotSendMoreThanBalance() throws Exception {
            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("UAT001").toAccountNumber("UAT003")
                    .amount(new BigDecimal("60000")).transferMode(TransferMode.UPI).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.message", containsString("Insufficient")));
        }

        @Test
        @DisplayName("AC4: I cannot accidentally send money to my own account")
        void cannotSendToSameAccount() throws Exception {
            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("UAT001").toAccountNumber("UAT001")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.message", containsString("same account")));
        }

        @Test
        @DisplayName("AC5: I get a clear error message when something goes wrong")
        void getClearErrorMessages() throws Exception {
            // Missing required fields
            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content("{\"amount\": 100}"))
                    .andExpect(status().isBadRequest())
                    .andExpect(jsonPath("$.details").isArray())
                    .andExpect(jsonPath("$.details", hasSize(greaterThanOrEqualTo(2))));
        }
    }

    @Nested
    @DisplayName("Story: As a user, I should be able to view my transaction history")
    class ViewHistory {

        @Test
        @DisplayName("AC1: I can see all transactions for my account")
        void canSeeTransactionsForAccount() throws Exception {
            // Make 2 transfers
            for (int i = 0; i < 2; i++) {
                TransferRequest req = TransferRequest.builder()
                        .fromAccountNumber("UAT001").toAccountNumber("UAT003")
                        .amount(new BigDecimal("500")).transferMode(TransferMode.NEFT).build();

                mockMvc.perform(post("/api/transactions/transfer")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(objectMapper.writeValueAsString(req)))
                        .andExpect(status().isCreated());
            }

            mockMvc.perform(get("/api/transactions/account/UAT001"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$", hasSize(2)))
                    .andExpect(jsonPath("$[*].status", everyItem(is("SUCCESS"))));
        }

        @Test
        @DisplayName("AC2: I can look up a transaction by its reference ID")
        void canLookUpByReference() throws Exception {
            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("UAT001").toAccountNumber("UAT003")
                    .amount(new BigDecimal("7500")).transferMode(TransferMode.RTGS)
                    .description("Invoice #12345").build();

            MvcResult result = mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andReturn();

            String refId = objectMapper.readTree(
                    result.getResponse().getContentAsString()).get("referenceId").asText();

            mockMvc.perform(get("/api/transactions/" + refId))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.amount").value(7500.0))
                    .andExpect(jsonPath("$.description").value("Invoice #12345"))
                    .andExpect(jsonPath("$.transferMode").value("RTGS"));
        }
    }

    @Nested
    @DisplayName("Story: As a manager, I should see a dashboard with summary stats")
    class DashboardStats {

        @Test
        @DisplayName("AC1: Dashboard shows total accounts and total balance")
        void dashboardShowsAccountStats() throws Exception {
            mockMvc.perform(get("/api/transactions/stats"))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.totalAccounts").isNumber())
                    .andExpect(jsonPath("$.totalBalance").isNumber())
                    .andExpect(jsonPath("$.activeAccounts").isNumber());
        }

        @Test
        @DisplayName("AC2: Dashboard reflects transaction counts after transfers")
        void dashboardReflectsTransactions() throws Exception {
            // Make a transfer
            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("UAT001").toAccountNumber("UAT003")
                    .amount(new BigDecimal("1000")).transferMode(TransferMode.UPI).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(req)))
                    .andExpect(status().isCreated());

            mockMvc.perform(get("/api/transactions/stats"))
                    .andExpect(jsonPath("$.totalTransactions").value(1))
                    .andExpect(jsonPath("$.successfulTransactions").value(1))
                    .andExpect(jsonPath("$.totalTransferred").value(1000.0));
        }
    }
}
