package com.mts.sanity;

import com.mts.dto.TransferRequest;
import com.mts.dto.TransferResponse;
import com.mts.entity.Account;
import com.mts.entity.User;
import com.mts.enums.AccountType;
import com.mts.enums.TransactionStatus;
import com.mts.enums.TransferMode;
import com.mts.exception.AccountInactiveException;
import com.mts.exception.InsufficientBalanceException;
import com.mts.exception.SameAccountTransferException;
import com.mts.repository.AccountRepository;
import com.mts.repository.UserRepository;
import com.mts.service.TransferService;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;

/**
 * SANITY TESTS — Specific business rule verification
 *
 * MTS equivalent of "Bug fix for tax calculation works"
 * Targeted tests that verify specific business rules are enforced.
 * Run after a specific fix or rule change to verify it works.
 */
@SpringBootTest
@ActiveProfiles("test")
@Transactional
@DisplayName("Sanity: Business Rules Verification")
class TransferBusinessRulesSanityTest {

    @Autowired private TransferService transferService;
    @Autowired private AccountRepository accountRepository;
    @Autowired private UserRepository userRepository;

    private User user;

    @BeforeEach
    void setUp() {
        user = userRepository.save(User.builder()
                .username("sanity.user").email("sanity@test.com")
                .passwordHash("hash").fullName("Sanity User").isActive(true).build());
    }

    private Account createAccount(String number, BigDecimal balance, boolean active) {
        return accountRepository.save(Account.builder()
                .accountNumber(number).user(user).accountType(AccountType.SAVINGS)
                .balance(balance).currency("INR").isActive(active).build());
    }

    @Nested
    @DisplayName("Business Rule: Balance must never go negative")
    class BalanceNeverNegative {

        @Test
        @DisplayName("Transfer of exact balance leaves zero, not negative")
        void exactBalanceTransferLeavesZero() {
            createAccount("SAN001", new BigDecimal("1000.00"), true);
            createAccount("SAN002", new BigDecimal("500.00"), true);

            TransferResponse response = transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("SAN001").toAccountNumber("SAN002")
                    .amount(new BigDecimal("1000.00")).transferMode(TransferMode.UPI).build());

            assertEquals(TransactionStatus.SUCCESS, response.getStatus());
            Account from = accountRepository.findByAccountNumber("SAN001").orElseThrow();
            assertEquals(0, from.getBalance().compareTo(BigDecimal.ZERO));
        }

        @Test
        @DisplayName("Transfer exceeding balance by 0.01 is rejected")
        void oneRupeeOverBalanceFails() {
            createAccount("SAN003", new BigDecimal("1000.00"), true);
            createAccount("SAN004", new BigDecimal("500.00"), true);

            assertThrows(InsufficientBalanceException.class, () ->
                    transferService.transferFunds(TransferRequest.builder()
                            .fromAccountNumber("SAN003").toAccountNumber("SAN004")
                            .amount(new BigDecimal("1000.01")).transferMode(TransferMode.UPI).build()));
        }
    }

    @Nested
    @DisplayName("Business Rule: Self-transfer is blocked")
    class SelfTransferBlocked {

        @Test
        @DisplayName("Transfer to same account is rejected immediately")
        void sameAccountTransferRejected() {
            createAccount("SAN005", new BigDecimal("5000"), true);

            assertThrows(SameAccountTransferException.class, () ->
                    transferService.transferFunds(TransferRequest.builder()
                            .fromAccountNumber("SAN005").toAccountNumber("SAN005")
                            .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build()));
        }
    }

    @Nested
    @DisplayName("Business Rule: Inactive accounts cannot transact")
    class InactiveAccountsBlocked {

        @Test
        @DisplayName("Transfer from inactive account is rejected")
        void fromInactiveAccountFails() {
            createAccount("SAN006", new BigDecimal("5000"), false);
            createAccount("SAN007", new BigDecimal("5000"), true);

            assertThrows(AccountInactiveException.class, () ->
                    transferService.transferFunds(TransferRequest.builder()
                            .fromAccountNumber("SAN006").toAccountNumber("SAN007")
                            .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build()));
        }

        @Test
        @DisplayName("Transfer to inactive account is rejected")
        void toInactiveAccountFails() {
            createAccount("SAN008", new BigDecimal("5000"), true);
            createAccount("SAN009", new BigDecimal("5000"), false);

            assertThrows(AccountInactiveException.class, () ->
                    transferService.transferFunds(TransferRequest.builder()
                            .fromAccountNumber("SAN008").toAccountNumber("SAN009")
                            .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build()));
        }
    }

    @Nested
    @DisplayName("Business Rule: All transfer modes produce successful transactions")
    class AllModesWork {

        @BeforeEach
        void setUpAccounts() {
            createAccount("MODE_FROM", new BigDecimal("100000"), true);
            createAccount("MODE_TO", new BigDecimal("10000"), true);
        }

        @Test
        @DisplayName("UPI transfer succeeds")
        void upiWorks() {
            TransferResponse r = transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("MODE_FROM").toAccountNumber("MODE_TO")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build());
            assertEquals(TransactionStatus.SUCCESS, r.getStatus());
            assertEquals(TransferMode.UPI, r.getTransferMode());
        }

        @Test
        @DisplayName("NEFT transfer succeeds")
        void neftWorks() {
            TransferResponse r = transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("MODE_FROM").toAccountNumber("MODE_TO")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.NEFT).build());
            assertEquals(TransactionStatus.SUCCESS, r.getStatus());
        }

        @Test
        @DisplayName("IMPS transfer succeeds")
        void impsWorks() {
            TransferResponse r = transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("MODE_FROM").toAccountNumber("MODE_TO")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.IMPS).build());
            assertEquals(TransactionStatus.SUCCESS, r.getStatus());
        }

        @Test
        @DisplayName("RTGS transfer succeeds")
        void rtgsWorks() {
            TransferResponse r = transferService.transferFunds(TransferRequest.builder()
                    .fromAccountNumber("MODE_FROM").toAccountNumber("MODE_TO")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.RTGS).build());
            assertEquals(TransactionStatus.SUCCESS, r.getStatus());
        }
    }

    @Nested
    @DisplayName("Business Rule: Transaction reference is unique")
    class UniqueReference {

        @Test
        @DisplayName("Two transfers produce different reference IDs")
        void twoTransfersHaveDifferentRefs() {
            createAccount("REF001", new BigDecimal("50000"), true);
            createAccount("REF002", new BigDecimal("10000"), true);

            TransferRequest req = TransferRequest.builder()
                    .fromAccountNumber("REF001").toAccountNumber("REF002")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build();

            TransferResponse r1 = transferService.transferFunds(req);
            TransferResponse r2 = transferService.transferFunds(req);

            assertNotEquals(r1.getReferenceId(), r2.getReferenceId());
        }
    }
}
