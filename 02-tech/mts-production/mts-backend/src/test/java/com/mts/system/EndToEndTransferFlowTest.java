package com.mts.system;

import com.fasterxml.jackson.databind.JsonNode;
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

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * SYSTEM TESTS — Complete end-to-end user journeys
 *
 * MTS equivalent of "Place order -> confirm -> deliver flow"
 * Simulates a real user performing a complete transfer workflow.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
@DisplayName("System: End-to-End Transfer Flow")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class EndToEndTransferFlowTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;
    @Autowired private AccountRepository accountRepository;
    @Autowired private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        User ravi = userRepository.save(User.builder()
                .username("ravi.e2e").email("ravi.e2e@test.com")
                .passwordHash("hash").fullName("Ravi Kumar").isActive(true).build());

        User priya = userRepository.save(User.builder()
                .username("priya.e2e").email("priya.e2e@test.com")
                .passwordHash("hash").fullName("Priya Sharma").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("E2E001").user(ravi).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("50000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("E2E002").user(priya).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("30000")).currency("INR").isActive(true).build());
    }

    @Test
    @Order(1)
    @DisplayName("E2E: User views accounts -> makes transfer -> checks updated balance -> views history")
    void completeTransferJourney() throws Exception {
        // Step 1: User views their accounts
        mockMvc.perform(get("/api/accounts/E2E001"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.balance").value(50000.0));

        // Step 2: User initiates a transfer
        TransferRequest request = TransferRequest.builder()
                .fromAccountNumber("E2E001").toAccountNumber("E2E002")
                .amount(new BigDecimal("15000")).transferMode(TransferMode.UPI)
                .description("Rent payment for August").build();

        MvcResult transferResult = mockMvc.perform(post("/api/transactions/transfer")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status").value("SUCCESS"))
                .andReturn();

        String referenceId = objectMapper.readTree(
                transferResult.getResponse().getContentAsString()).get("referenceId").asText();

        // Step 3: User checks updated balances
        mockMvc.perform(get("/api/accounts/E2E001"))
                .andExpect(jsonPath("$.balance").value(35000.0));

        mockMvc.perform(get("/api/accounts/E2E002"))
                .andExpect(jsonPath("$.balance").value(45000.0));

        // Step 4: User views transaction by reference
        mockMvc.perform(get("/api/transactions/" + referenceId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.fromAccountNumber").value("E2E001"))
                .andExpect(jsonPath("$.toAccountNumber").value("E2E002"))
                .andExpect(jsonPath("$.amount").value(15000.0))
                .andExpect(jsonPath("$.description").value("Rent payment for August"));

        // Step 5: User views transaction history for their account
        mockMvc.perform(get("/api/transactions/account/E2E001"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].referenceId").value(referenceId));

        // Step 6: Dashboard stats reflect the transfer
        mockMvc.perform(get("/api/transactions/stats"))
                .andExpect(jsonPath("$.totalTransactions").value(1))
                .andExpect(jsonPath("$.successfulTransactions").value(1))
                .andExpect(jsonPath("$.totalTransferred").value(15000.0));
    }

    @Test
    @Order(2)
    @DisplayName("E2E: Multiple transfers between accounts -> cumulative balances correct")
    void multipleTransfersJourney() throws Exception {
        // Transfer 1: E2E001 -> E2E002 (10,000)
        TransferRequest req1 = TransferRequest.builder()
                .fromAccountNumber("E2E001").toAccountNumber("E2E002")
                .amount(new BigDecimal("10000")).transferMode(TransferMode.NEFT).build();

        mockMvc.perform(post("/api/transactions/transfer")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req1)))
                .andExpect(status().isCreated());

        // Transfer 2: E2E002 -> E2E001 (5,000) — reverse direction
        TransferRequest req2 = TransferRequest.builder()
                .fromAccountNumber("E2E002").toAccountNumber("E2E001")
                .amount(new BigDecimal("5000")).transferMode(TransferMode.IMPS).build();

        mockMvc.perform(post("/api/transactions/transfer")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req2)))
                .andExpect(status().isCreated());

        // Transfer 3: E2E001 -> E2E002 (2,000)
        TransferRequest req3 = TransferRequest.builder()
                .fromAccountNumber("E2E001").toAccountNumber("E2E002")
                .amount(new BigDecimal("2000")).transferMode(TransferMode.RTGS).build();

        mockMvc.perform(post("/api/transactions/transfer")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(req3)))
                .andExpect(status().isCreated());

        // Verify: E2E001 = 50000 - 10000 + 5000 - 2000 = 43000
        mockMvc.perform(get("/api/accounts/E2E001"))
                .andExpect(jsonPath("$.balance").value(43000.0));

        // Verify: E2E002 = 30000 + 10000 - 5000 + 2000 = 37000
        mockMvc.perform(get("/api/accounts/E2E002"))
                .andExpect(jsonPath("$.balance").value(37000.0));

        // Verify: 3 transactions in history
        mockMvc.perform(get("/api/transactions/account/E2E001"))
                .andExpect(jsonPath("$.length()").value(3));

        // Verify: All transactions
        mockMvc.perform(get("/api/transactions"))
                .andExpect(jsonPath("$.length()").value(3));
    }

    @Test
    @Order(3)
    @DisplayName("E2E: Failed transfer does not corrupt system state")
    void failedTransferJourney() throws Exception {
        // Attempt transfer with insufficient funds
        TransferRequest badRequest = TransferRequest.builder()
                .fromAccountNumber("E2E001").toAccountNumber("E2E002")
                .amount(new BigDecimal("99999")).transferMode(TransferMode.UPI).build();

        mockMvc.perform(post("/api/transactions/transfer")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(badRequest)))
                .andExpect(status().isBadRequest());

        // System state must be unchanged
        mockMvc.perform(get("/api/accounts/E2E001"))
                .andExpect(jsonPath("$.balance").value(50000.0));

        mockMvc.perform(get("/api/accounts/E2E002"))
                .andExpect(jsonPath("$.balance").value(30000.0));

        // Now a valid transfer should still work
        TransferRequest goodRequest = TransferRequest.builder()
                .fromAccountNumber("E2E001").toAccountNumber("E2E002")
                .amount(new BigDecimal("1000")).transferMode(TransferMode.UPI).build();

        mockMvc.perform(post("/api/transactions/transfer")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(goodRequest)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status").value("SUCCESS"));
    }
}
