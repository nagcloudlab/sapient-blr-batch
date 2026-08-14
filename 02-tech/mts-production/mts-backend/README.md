# MTS Backend

Spring Boot REST API for the Money Transfer System.

## Tech Stack

- Java 17, Spring Boot 3.3
- Spring Data JPA, Bean Validation
- H2 (default) / MySQL (prod)
- Lombok, SLF4J logging

## Run

```bash
# Default (H2 in-memory)
mvn spring-boot:run

# Production (MySQL)
mvn spring-boot:run -Dspring-boot.run.profiles=prod
```

API available at `http://localhost:8080/api/accounts`

H2 Console at `http://localhost:8080/h2-console` (JDBC URL: `jdbc:h2:mem:mtsdb`, User: `sa`)

## Project Structure

```
src/main/java/com/mts/
├── config/           # CORS, RestTemplate beans
├── controller/       # REST controllers (Account, Transaction)
├── dto/              # Request/Response DTOs, ErrorResponse, DashboardStats
├── entity/           # JPA entities (User, Account, Transaction)
├── enums/            # AccountType, TransferMode, TransactionStatus
├── exception/        # Custom exceptions + GlobalExceptionHandler
├── repository/       # Spring Data JPA repositories
└── service/          # Business logic (TransferService, AccountService)

src/main/resources/
├── application.yml        # Default profile (H2)
├── application-prod.yml   # Production profile (MySQL)
├── application-test.yml   # Test profile (H2, no seed data)
└── data.sql               # Seed data for H2
```

## Tests (135)

```bash
mvn test                                                   # All tests
mvn test -Dtest="com.mts.unit.*"                           # Unit (33)
mvn test -Dtest="com.mts.integration.*"                    # Integration (8)
mvn test -Dtest="com.mts.system.*"                         # System E2E (3)
mvn test -Dtest="com.mts.smoke.*"                          # Smoke (8)
mvn test -Dtest="com.mts.sanity.*"                         # Sanity (10)
mvn test -Dtest="com.mts.regression.*"                     # Regression (8)
mvn test -Dtest="com.mts.uat.*"                            # UAT (21)
mvn test -Dtest="com.mts.nonfunctional.performance.*"      # Performance (6)
mvn test -Dtest="com.mts.nonfunctional.concurrency.*"      # Concurrency (4)
mvn test -Dtest="com.mts.nonfunctional.security.*"         # Security (15)
mvn test -Dtest="com.mts.nonfunctional.resilience.*"       # Resilience (5)
mvn test -Dtest="com.mts.nonfunctional.datainteg.*"        # Data Integrity (10)
```

## Key Patterns

- **DTO pattern** — Separate request/response from entities
- **Global exception handler** — Consistent error responses with HTTP codes
- **Bean Validation** — `@NotBlank`, `@DecimalMin`, `@DecimalMax` on DTOs
- **@Transactional** — Atomic transfers with rollback on failure
- **Spring Profiles** — H2 for dev/test, MySQL for prod
- **Interface-based services** — `TransferService` interface, `UpiTransferService` impl
- **Non-blocking notifications** — Try-catch around notification client calls
