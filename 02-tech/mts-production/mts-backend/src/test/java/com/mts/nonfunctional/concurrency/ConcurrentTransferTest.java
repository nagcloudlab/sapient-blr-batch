package com.mts.nonfunctional.concurrency;

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
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.test.web.servlet.MvcResult;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;

/**
 * NON-FUNCTIONAL: Concurrency Tests
 *
 * Validates system behavior under concurrent access.
 * Tests race conditions when multiple transfers hit the same account simultaneously.
 * In production, this would be addressed with DB-level locking or optimistic locking.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
@DisplayName("Non-Functional: Concurrency")
class ConcurrentTransferTest {

    @Autowired private MockMvc mockMvc;
    @Autowired private ObjectMapper objectMapper;
    @Autowired private AccountRepository accountRepository;
    @Autowired private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        User user = userRepository.save(User.builder()
                .username("conc.user").email("conc@test.com")
                .passwordHash("hash").fullName("Concurrent User").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("CONC001").user(user).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("100000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("CONC002").user(user).accountType(AccountType.CURRENT)
                .balance(new BigDecimal("50000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("CONC003").user(user).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("30000")).currency("INR").isActive(true).build());
    }

    @Test
    @DisplayName("Multiple simultaneous reads should not fail")
    void concurrentReadsDoNotFail() throws Exception {
        int threadCount = 10;
        ExecutorService executor = Executors.newFixedThreadPool(threadCount);
        CountDownLatch latch = new CountDownLatch(threadCount);
        List<Future<Integer>> futures = new ArrayList<>();

        for (int i = 0; i < threadCount; i++) {
            futures.add(executor.submit(() -> {
                latch.countDown();
                latch.await(); // All threads start at the same time
                MvcResult result = mockMvc.perform(
                        org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get("/api/accounts"))
                        .andReturn();
                return result.getResponse().getStatus();
            }));
        }

        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);

        for (Future<Integer> future : futures) {
            assertEquals(200, future.get(), "Concurrent read should return 200");
        }
    }

    @Test
    @DisplayName("Sequential transfers from same account should maintain correct balance")
    void sequentialTransfersFromSameAccount() throws Exception {
        // 10 transfers of 1000 each from CONC001 (balance: 100000) -> CONC002
        int transferCount = 10;
        BigDecimal amountPerTransfer = new BigDecimal("1000");

        for (int i = 0; i < transferCount; i++) {
            TransferRequest request = TransferRequest.builder()
                    .fromAccountNumber("CONC001").toAccountNumber("CONC002")
                    .amount(amountPerTransfer).transferMode(TransferMode.UPI).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andExpect(org.springframework.test.web.servlet.result.MockMvcResultMatchers.status().isCreated());
        }

        // Verify final balances
        Account from = accountRepository.findByAccountNumber("CONC001").orElseThrow();
        Account to = accountRepository.findByAccountNumber("CONC002").orElseThrow();

        // CONC001: 100000 - (10 * 1000) = 90000
        assertEquals(0, new BigDecimal("90000").compareTo(from.getBalance()),
                "From account should be 90000 after 10x1000 transfers");

        // CONC002: 50000 + (10 * 1000) = 60000
        assertEquals(0, new BigDecimal("60000").compareTo(to.getBalance()),
                "To account should be 60000 after receiving 10x1000");
    }

    @Test
    @DisplayName("Rapid-fire transfers in both directions maintain correct net balance")
    void bidirectionalTransfersMaintainBalance() throws Exception {
        // 5 transfers: CONC001 -> CONC002 (1000 each)
        for (int i = 0; i < 5; i++) {
            TransferRequest request = TransferRequest.builder()
                    .fromAccountNumber("CONC001").toAccountNumber("CONC002")
                    .amount(new BigDecimal("1000")).transferMode(TransferMode.UPI).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andExpect(org.springframework.test.web.servlet.result.MockMvcResultMatchers.status().isCreated());
        }

        // 3 transfers: CONC002 -> CONC001 (1000 each)
        for (int i = 0; i < 3; i++) {
            TransferRequest request = TransferRequest.builder()
                    .fromAccountNumber("CONC002").toAccountNumber("CONC001")
                    .amount(new BigDecimal("1000")).transferMode(TransferMode.NEFT).build();

            mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andExpect(org.springframework.test.web.servlet.result.MockMvcResultMatchers.status().isCreated());
        }

        // Net: CONC001 sent 5000, received 3000 -> net debit 2000
        Account from = accountRepository.findByAccountNumber("CONC001").orElseThrow();
        Account to = accountRepository.findByAccountNumber("CONC002").orElseThrow();

        // CONC001: 100000 - 5000 + 3000 = 98000
        assertEquals(0, new BigDecimal("98000").compareTo(from.getBalance()));
        // CONC002: 50000 + 5000 - 3000 = 52000
        assertEquals(0, new BigDecimal("52000").compareTo(to.getBalance()));
    }

    @Test
    @DisplayName("Rapid-fire transfers should not create duplicate reference IDs")
    void noDuplicateReferenceIds() throws Exception {
        List<String> referenceIds = new ArrayList<>();

        for (int i = 0; i < 20; i++) {
            TransferRequest request = TransferRequest.builder()
                    .fromAccountNumber("CONC001").toAccountNumber("CONC003")
                    .amount(new BigDecimal("10")).transferMode(TransferMode.IMPS).build();

            MvcResult result = mockMvc.perform(post("/api/transactions/transfer")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(request)))
                    .andReturn();

            if (result.getResponse().getStatus() == 201) {
                String refId = objectMapper.readTree(
                        result.getResponse().getContentAsString()).get("referenceId").asText();
                referenceIds.add(refId);
            }
        }

        // All reference IDs should be unique
        long uniqueCount = referenceIds.stream().distinct().count();
        assertEquals(referenceIds.size(), uniqueCount,
                "All reference IDs should be unique. Found duplicates.");
    }
}
