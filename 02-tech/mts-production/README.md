# MTS - Money Transfer System (Production Grade)

A full-stack, production-grade money transfer application built for training purposes. Demonstrates real-world patterns across **Java Spring Boot**, **React**, **Node.js**, **SQL**, and **QC/QA/QE testing**.

## Architecture

```
                    +-------------------+
                    |   React Frontend  |  Port 5173
                    |   (Vite + Router) |
                    +--------+----------+
                             |
                             | REST API (JSON)
                             v
                    +-------------------+
                    | Spring Boot API   |  Port 8080
                    | (Controllers,     |
                    |  Services, JPA)   |
                    +--------+----------+
                             |
                    +--------+----------+
                    |   H2 / MySQL DB   |  In-memory (default)
                    +-------------------+
                             |
                    +--------+----------+
                    | Node.js Notif.    |  Port 3000
                    | Service (Express) |
                    +-------------------+
```

## Project Structure

```
mts-production/
├── mts-backend/                 # Java Spring Boot REST API
├── mts-frontend/                # React SPA (Vite)
├── mts-notification-service/    # Node.js Express microservice
├── database/                    # SQL schema for production (MySQL)
└── README.md                    # This file
```

## Quick Start

### Prerequisites

- Java 17+
- Maven
- Node.js 18+
- npm

### Start All Services

```bash
# 1. Notification Service (Port 3000)
cd mts-notification-service
npm install
npm start

# 2. Backend (Port 8080) - uses H2 in-memory DB by default
cd mts-backend
mvn spring-boot:run

# 3. Frontend (Port 5173)
cd mts-frontend
npm install
npm run dev
```

### Access

| Service | URL |
|---------|-----|
| React App | http://localhost:5173 |
| Spring Boot API | http://localhost:8080/api/accounts |
| H2 Console | http://localhost:8080/h2-console |
| Notification Dashboard | http://localhost:3000 |

**H2 Console credentials:** JDBC URL: `jdbc:h2:mem:mtsdb`, User: `sa`, Password: _(empty)_

## Spring Boot Profiles

| Profile | Database | Command |
|---------|----------|---------|
| **default** | H2 in-memory | `mvn spring-boot:run` |
| **test** | H2 in-memory | `@ActiveProfiles("test")` in JUnit |
| **prod** | MySQL | `mvn spring-boot:run -Dspring-boot.run.profiles=prod` |

For **prod** profile, first run `database/schema.sql` against your MySQL instance.

## API Endpoints

### Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts` | List all accounts |
| GET | `/api/accounts/{number}` | Get account by number |
| GET | `/api/accounts/user/{username}` | Get accounts by username |

### Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/transactions/transfer` | Execute a fund transfer |
| GET | `/api/transactions` | List all transactions |
| GET | `/api/transactions/{referenceId}` | Get transaction by reference |
| GET | `/api/transactions/account/{number}` | Get transactions for account |
| GET | `/api/transactions/stats` | Dashboard statistics |

### Transfer Request Body

```json
{
  "fromAccountNumber": "ACC001",
  "toAccountNumber": "ACC003",
  "amount": 5000.00,
  "transferMode": "UPI",
  "description": "Rent payment"
}
```

Transfer modes: `UPI`, `NEFT`, `IMPS`, `RTGS`

## Running Tests

### Backend (135 tests)

```bash
cd mts-backend

# Run all tests
mvn test

# Run by category
mvn test -Dtest="com.mts.unit.*"                          # Unit tests
mvn test -Dtest="com.mts.integration.*"                   # Integration tests
mvn test -Dtest="com.mts.system.*"                        # System (E2E) tests
mvn test -Dtest="com.mts.smoke.*"                         # Smoke tests
mvn test -Dtest="com.mts.sanity.*"                        # Sanity tests
mvn test -Dtest="com.mts.regression.*"                    # Regression tests
mvn test -Dtest="com.mts.uat.*"                           # UAT tests
mvn test -Dtest="com.mts.nonfunctional.performance.*"     # Performance tests
mvn test -Dtest="com.mts.nonfunctional.concurrency.*"     # Concurrency tests
mvn test -Dtest="com.mts.nonfunctional.security.*"        # Security tests
mvn test -Dtest="com.mts.nonfunctional.resilience.*"      # Resilience tests
mvn test -Dtest="com.mts.nonfunctional.datainteg.*"       # Data integrity tests
```

### Frontend

```bash
cd mts-frontend
npm test
```

### Notification Service

```bash
cd mts-notification-service
npm test
```

## Test Coverage Summary

### Functional Tests (95)

| Type | Tests | What It Validates |
|------|-------|-------------------|
| Unit | 33 | Individual methods, DTO validation, exceptions |
| Integration | 12 | API -> Service -> Repository -> H2 DB |
| System (E2E) | 3 | Complete user journeys end-to-end |
| Smoke | 8 | App boots, beans wired, endpoints respond |
| Sanity | 10 | Specific business rules (balance, modes, refs) |
| Regression | 8 | Original features unchanged after updates |
| UAT | 21 | Business stories from user perspective |

### Non-Functional Tests (40)

| Type | Tests | What It Validates |
|------|-------|-------------------|
| Performance | 6 | Response time < 500ms, throughput |
| Concurrency | 4 | Concurrent reads, rapid transfers, unique refs |
| Security | 15 | SQL injection, XSS, malformed input, error safety |
| Resilience | 5 | Notification down, recovery after failures |
| Data Integrity | 10 | Money conservation, atomicity, timestamps |

## Topics Covered

This project demonstrates concepts from the following training modules:

| Module | How It's Used |
|--------|---------------|
| HTML/CSS | Frontend UI, responsive design, CSS Grid/Flexbox |
| JavaScript | Fetch API, async/await, ES modules, error handling |
| React | Components, hooks, React Router, state management |
| Java | Entities, enums, interfaces, streams, builder pattern |
| Spring Boot | REST, JPA, validation, profiles, exception handling |
| Node.js | Express server, middleware, routing, API design |
| SQL | Schema design, constraints, indexes, relationships |
| QC/QA/QE | 135 tests across 12 testing categories |

## Seed Data (Default Profile)

| User | Accounts | Balance |
|------|----------|---------|
| Ravi Kumar | ACC001 (Savings), ACC002 (Current) | 50,000 / 1,20,000 |
| Priya Sharma | ACC003 (Savings) | 75,000 |
| Amit Patel | ACC004 (Savings), ACC005 (Current) | 30,000 / 2,00,000 |
