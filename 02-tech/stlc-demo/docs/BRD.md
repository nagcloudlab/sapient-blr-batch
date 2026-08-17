# Business Requirements Document (BRD)

## Project: Web Calculator

| Field            | Details                          |
| ---------------- | -------------------------------- |
| Project Name     | Web Calculator                   |
| Prepared By      | Product / Business Team          |
| Version          | 1.0                              |
| Status           | Approved                         |

---

## 1. Business Objective

Build a simple, browser-based calculator application to demonstrate the complete Software Testing Life Cycle (STLC) — from requirements through test closure.

## 2. Business Need

- Trainees need a real, working application to practice functional testing techniques.
- The application must be simple enough to understand in one session, yet rich enough to generate meaningful test scenarios.

## 3. Scope

### In Scope

| # | Feature                                | Priority |
|---|----------------------------------------|----------|
| 1 | Basic arithmetic: Add, Subtract, Multiply, Divide | Must Have |
| 2 | Clear / Reset functionality            | Must Have |
| 3 | Decimal number support                 | Must Have |
| 4 | Chained operations (e.g., 2 + 3 * 4)  | Should Have |
| 5 | Keyboard input support                 | Nice to Have |
| 6 | Responsive layout (mobile-friendly)    | Nice to Have |

### Out of Scope

- Scientific / advanced math functions (sin, cos, log, etc.)
- History / memory storage
- User authentication
- Backend / API integration

## 4. Stakeholders

| Role              | Responsibility                        |
| ----------------- | ------------------------------------- |
| Trainer           | Define requirements, review deliverables |
| Trainees / QA     | Write and execute test cases          |
| Developer         | Build the calculator application      |

## 5. Success Criteria

- All four basic arithmetic operations work correctly.
- Unit tests achieve at least 90% code coverage on calculator logic.
- E2E tests cover all critical user flows.
- Zero critical or high-severity defects remain at release.

## 6. Constraints

- Must use only HTML, CSS, and plain JavaScript (no frameworks).
- Must run in any modern browser without a server.
- Must be completed within a single training session.

## 7. Assumptions

- Trainees have basic knowledge of HTML, CSS, and JavaScript.
- Node.js is available on training machines for running tests.
- Modern browsers (Chrome / Firefox / Edge) are available.
