package com.mts.nonfunctional.resilience;

import com.mts.dto.TransferRequest;
import com.mts.dto.TransferResponse;
import com.mts.entity.Account;
import com.mts.entity.User;
import com.mts.enums.AccountType;
import com.mts.enums.TransactionStatus;
import com.mts.enums.TransferMode;
import com.mts.exception.AccountNotFoundException;
import com.mts.exception.InsufficientBalanceException;
import com.mts.repository.AccountRepository;
import com.mts.repository.TransactionRepository;
import com.mts.repository.UserRepository;
import com.mts.service.NotificationClient;
import com.mts.service.TransferService;
import com.mts.service.UpiTransferService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

/**
 * NON-FUNCTIONAL: Resilience Tests
 *
 * Validates system behavior when external dependencies fail.
 * The system should degrade gracefully — core functionality must continue
 * even when non-critical services (notifications) are unavailable.
 */
@SpringBootTest
@ActiveProfiles("test")
@Transactional
@DisplayName("Non-Functional: Resilience")
class ResilienceTest {

    @Autowired private AccountRepository accountRepository;
    @Autowired private TransactionRepository transactionRepository;
    @Autowired private UserRepository userRepository;

    private User user;

    @BeforeEach
    void setUp() {
        user = userRepository.save(User.builder()
                .username("res.user").email("res@test.com")
                .passwordHash("hash").fullName("Resilience User").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("RES001").user(user).accountType(AccountType.SAVINGS)
                .balance(new BigDecimal("50000")).currency("INR").isActive(true).build());

        accountRepository.save(Account.builder()
                .accountNumber("RES002").user(user).accountType(AccountType.CURRENT)
                .balance(new BigDecimal("20000")).currency("INR").isActive(true).build());
    }

    @Nested
    @DisplayName("Notification Service Down")
    class NotificationServiceDown {

        @Test
        @DisplayName("Transfer should succeed even when notification service throws exception")
        void transferSucceedsWhenNotificationFails() {
            // Create a service with a mocked notification client that throws
            NotificationClient failingClient = mock(NotificationClient.class);
            doThrow(new RuntimeException("Connection refused: localhost:3000"))
                    .when(failingClient).sendTransactionNotification(any());

            TransferService service = new UpiTransferService(
                    accountRepository, transactionRepository, failingClient);

            TransferRequest request = TransferRequest.builder()
                    .fromAccountNumber("RES001").toAccountNumber("RES002")
                    .amount(new BigDecimal("5000")).transferMode(TransferMode.UPI).build();

            // Transfer should NOT throw
            TransferResponse response = service.transferFunds(request);

            assertEquals(TransactionStatus.SUCCESS, response.getStatus());
            assertNotNull(response.getReferenceId());

            // Balances should be updated
            Account from = accountRepository.findByAccountNumber("RES001").orElseThrow();
            assertEquals(0, new BigDecimal("45000").compareTo(from.getBalance()));
        }

        @Test
        @DisplayName("Transfer should succeed when notification client returns null")
        void transferSucceedsWhenNotificationReturnsNull() {
            NotificationClient silentClient = mock(NotificationClient.class);
            // Does nothing — simulates a timeout with no response

            TransferService service = new UpiTransferService(
                    accountRepository, transactionRepository, silentClient);

            TransferRequest request = TransferRequest.builder()
                    .fromAccountNumber("RES001").toAccountNumber("RES002")
                    .amount(new BigDecimal("1000")).transferMode(TransferMode.NEFT).build();

            TransferResponse response = service.transferFunds(request);
            assertEquals(TransactionStatus.SUCCESS, response.getStatus());
        }
    }

    @Nested
    @DisplayName("Graceful Error Recovery")
    class GracefulRecovery {

        @Autowired
        private TransferService transferService;

        @Test
        @DisplayName("After a failed transfer, the next transfer should still work")
        void systemRecoveryAfterFailure() {
            // Attempt 1: Should fail (insufficient balance)
            TransferRequest badRequest = TransferRequest.builder()
                    .fromAccountNumber("RES001").toAccountNumber("RES002")
                    .amount(new BigDecimal("99999")).transferMode(TransferMode.UPI).build();

            assertThrows(InsufficientBalanceException.class,
                    () -> transferService.transferFunds(badRequest));

            // Attempt 2: Should succeed
            TransferRequest goodRequest = TransferRequest.builder()
                    .fromAccountNumber("RES001").toAccountNumber("RES002")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build();

            TransferResponse response = transferService.transferFunds(goodRequest);
            assertEquals(TransactionStatus.SUCCESS, response.getStatus());
        }

        @Test
        @DisplayName("After account-not-found error, valid transfer should still work")
        void recoveryAfterNotFoundError() {
            // Attempt with invalid account
            TransferRequest badRequest = TransferRequest.builder()
                    .fromAccountNumber("GHOST").toAccountNumber("RES002")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build();

            assertThrows(AccountNotFoundException.class,
                    () -> transferService.transferFunds(badRequest));

            // Valid transfer should still work
            TransferRequest goodRequest = TransferRequest.builder()
                    .fromAccountNumber("RES001").toAccountNumber("RES002")
                    .amount(new BigDecimal("100")).transferMode(TransferMode.UPI).build();

            TransferResponse response = transferService.transferFunds(goodRequest);
            assertEquals(TransactionStatus.SUCCESS, response.getStatus());
        }

        @Test
        @DisplayName("Multiple consecutive failures should not corrupt state")
        void multipleFailuresDoNotCorruptState() {
            BigDecimal originalBalance = accountRepository.findByAccountNumber("RES001")
                    .orElseThrow().getBalance();

            // 5 consecutive failures
            for (int i = 0; i < 5; i++) {
                TransferRequest badRequest = TransferRequest.builder()
                        .fromAccountNumber("RES001").toAccountNumber("RES002")
                        .amount(new BigDecimal("99999")).transferMode(TransferMode.UPI).build();

                assertThrows(InsufficientBalanceException.class,
                        () -> transferService.transferFunds(badRequest));
            }

            // Balance should be unchanged after all failures
            BigDecimal currentBalance = accountRepository.findByAccountNumber("RES001")
                    .orElseThrow().getBalance();
            assertEquals(0, originalBalance.compareTo(currentBalance),
                    "Balance should be unchanged after multiple failures");
        }
    }
}
