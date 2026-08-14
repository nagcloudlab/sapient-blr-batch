package com.mts.nonfunctional.datainteg;

import com.mts.dto.TransferRequest;
import com.mts.dto.TransferResponse;
import com.mts.entity.Account;
import com.mts.entity.Transaction;
import com.mts.entity.User;
import com.mts.enums.AccountType;
import com.mts.enums.TransactionStatus;
import com.mts.enums.TransferMode;
import com.mts.exception.InsufficientBalanceException;
import com.mts.repository.AccountRepository;
import com.mts.repository.TransactionRepository;
import com.mts.repository.UserRepository;
import com.mts.service.TransferService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * NON-FUNCTIONAL: Data Integrity Tests
 *
 * Validates that the system maintains data consistency at all times.
 * - Total money in the system is conserved (no money created/destroyed)
 * - Transaction records match actual balance changes
 * - Failed transfers don't leave partial state
 * - Every debit has a corresponding credit
 */
@SpringBootTest
@ActiveProfiles("test")
@Transactional
@DisplayName("Non-Functional: Data Integrity")
class DataIntegrityTest {

    @Autowired private TransferService transferService;
    @Autowired private AccountRepository accountRepository;
    @Autowired private TransactionRepository transactionRepository;
    @Autowired private UserRepository userRepository;

    private BigDecimal initialTotalBalance;

    @BeforeEach
    void setUp() {
        User user1 = userRepository.save(User.builder()
                .username("integ.user1").email("integ1@test.com")
                .passwordHash("hash").fullName("User One").isActive(true).build());

        User user2 = userRepository.save(User.builder()
                .username("integ.user2").email("integ2@test.com")
                .passwordHash("hash").fullName("User Two").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("DI001").user(user1).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("50000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("DI002").user(user1).accountType(AccountType.CURRENT)
                .balance(new BigDecimal("80000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("DI003").user(user2).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("30000")).currency("INR").isActive(true).build());

        // Calculate total balance before any transfers
        initialTotalBalance = accountRepository.findAll().stream()
                .map(Account::getBalance)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    @Nested
    @DisplayName("Money Conservation (Total balance never changes)")
    class MoneyConservation {

        @Test
        @DisplayName("Total system balance must remain same after a successful transfer")
        void totalBalanceConservedAfterTransfer() {
            transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("DI001").toAccountNumber("DI003")
                    .amount(new BigDecimal("15000")).transferMode(TransferMode.UPI).build());

            BigDecimal totalAfter = accountRepository.findAll().stream()
                    .map(Account::getBalance)
                    .reduce(BigDecimal.ZERO, BigDecimal::add);

            assertEquals(0, initialTotalBalance.compareTo(totalAfter),
                    "Total balance must be conserved. Before: " + initialTotalBalance + ", After: " + totalAfter);
        }

        @Test
        @DisplayName("Total system balance must remain same after multiple transfers")
        void totalBalanceConservedAfterMultipleTransfers() {
            // DI001 -> DI003
            transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("DI001").toAccountNumber("DI003")
                    .amount(new BigDecimal("10000")).transferMode(TransferMode.UPI).build());

            // DI002 -> DI001
            transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("DI002").toAccountNumber("DI001")
                    .amount(new BigDecimal("5000")).transferMode(TransferMode.NEFT).build());

            // DI003 -> DI002
            transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("DI003").toAccountNumber("DI002")
                    .amount(new BigDecimal("20000")).transferMode(TransferMode.IMPS).build());

            BigDecimal totalAfter = accountRepository.findAll().stream()
                    .map(Account::getBalance)
                    .reduce(BigDecimal.ZERO, BigDecimal::add);

            assertEquals(0, initialTotalBalance.compareTo(totalAfter),
                    "Total balance must be conserved after circular transfers");
        }

        @Test
        @DisplayName("Total system balance must remain same after a failed transfer")
        void totalBalanceConservedAfterFailedTransfer() {
            assertThrows(InsufficientBalanceException.class, () ->
                    transferService.transferFunds(TransferRequest.builder()
                            .fromAccountNumber("DI001").toAccountNumber("DI003")
                            .amount(new BigDecimal("99999")).transferMode(TransferMode.UPI).build()));

            BigDecimal totalAfter = accountRepository.findAll().stream()
                    .map(Account::getBalance)
                    .reduce(BigDecimal.ZERO, BigDecimal::add);

            assertEquals(0, initialTotalBalance.compareTo(totalAfter),
                    "Total balance must be conserved even after failed transfer");
        }
    }

    @Nested
    @DisplayName("Transaction Record Integrity")
    class TransactionRecordIntegrity {

        @Test
        @DisplayName("Every successful transfer must have a SUCCESS transaction record")
        void successfulTransferHasRecord() {
            TransferResponse response = transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("DI001").toAccountNumber("DI003")
                    .amount(new BigDecimal("5000")).transferMode(TransferMode.UPI).build());

            TransferResponse found = transferService.getTransactionByReferenceId(response.getReferenceId());

            assertNotNull(found);
            assertEquals(TransactionStatus.SUCCESS, found.getStatus());
            assertEquals(new BigDecimal("5000"), found.getAmount());
            assertEquals("DI001", found.getFromAccountNumber());
            assertEquals("DI003", found.getToAccountNumber());
        }

        @Test
        @DisplayName("Failed transfer must have a FAILED transaction record with reason")
        void failedTransferHasRecordWithReason() {
            assertThrows(InsufficientBalanceException.class, () ->
                    transferService.transferFunds(TransferRequest.builder()
                            .fromAccountNumber("DI001").toAccountNumber("DI003")
                            .amount(new BigDecimal("99999")).transferMode(TransferMode.UPI).build()));

            // Check that a FAILED transaction was recorded
            List<Transaction> transactions = transactionRepository.findByAccountNumber("DI001");
            assertFalse(transactions.isEmpty(), "Failed transfer should still be recorded");

            Transaction failedTxn = transactions.stream()
                    .filter(t -> t.getStatus() == TransactionStatus.FAILED)
                    .findFirst().orElse(null);

            assertNotNull(failedTxn, "Should have a FAILED transaction record");
            assertNotNull(failedTxn.getFailureReason(), "Failed transaction should have a reason");
            assertTrue(failedTxn.getFailureReason().contains("Insufficient"),
                    "Failure reason should mention insufficient balance");
        }

        @Test
        @DisplayName("Debit amount must exactly equal credit amount in every transaction")
        void debitEqualsCreditInEveryTransaction() {
            transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("DI001").toAccountNumber("DI003")
                    .amount(new BigDecimal("7777.77")).transferMode(TransferMode.RTGS).build());

            List<Transaction> transactions = transactionRepository.findByAccountNumber("DI001");
            Transaction txn = transactions.stream()
                    .filter(t -> t.getStatus() == TransactionStatus.SUCCESS)
                    .findFirst().orElseThrow();

            // The single transaction amount represents both the debit and credit
            assertEquals(0, new BigDecimal("7777.77").compareTo(txn.getAmount()));

            // Verify actual balance changes match
            Account from = accountRepository.findByAccountNumber("DI001").orElseThrow();
            Account to = accountRepository.findByAccountNumber("DI003").orElseThrow();

            assertEquals(0, new BigDecimal("42222.23").compareTo(from.getBalance()));
            assertEquals(0, new BigDecimal("37777.77").compareTo(to.getBalance()));
        }
    }

    @Nested
    @DisplayName("Referential Integrity")
    class ReferentialIntegrity {

        @Test
        @DisplayName("Transaction must reference valid from and to accounts")
        void transactionReferencesValidAccounts() {
            TransferResponse response = transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("DI001").toAccountNumber("DI002")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build());

            List<Transaction> txns = transactionRepository.findByAccountNumber("DI001");
            Transaction txn = txns.get(0);

            assertNotNull(txn.getFromAccount());
            assertNotNull(txn.getToAccount());
            assertEquals("DI001", txn.getFromAccount().getAccountNumber());
            assertEquals("DI002", txn.getToAccount().getAccountNumber());
        }

        @Test
        @DisplayName("Transaction timestamps must be set correctly")
        void transactionTimestampsAreSet() {
            transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("DI001").toAccountNumber("DI002")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build());

            List<Transaction> txns = transactionRepository.findByAccountNumber("DI001");
            Transaction txn = txns.stream()
                    .filter(t -> t.getStatus() == TransactionStatus.SUCCESS)
                    .findFirst().orElseThrow();

            assertNotNull(txn.getCreatedAt(), "createdAt must be set");
            assertNotNull(txn.getCompletedAt(), "completedAt must be set for SUCCESS");
            assertFalse(txn.getCompletedAt().isBefore(txn.getCreatedAt()),
                    "completedAt must not be before createdAt");
        }

        @Test
        @DisplayName("All accounts must belong to a valid user")
        void allAccountsHaveValidUser() {
            List<Account> accounts = accountRepository.findAll();

            for (Account account : accounts) {
                assertNotNull(account.getUser(), "Account " + account.getAccountNumber() + " must have a user");
                assertNotNull(account.getUser().getUsername(), "User must have a username");
            }
        }
    }
}
