# User Stories with Acceptance Criteria

## Project: Web Calculator

---

## US-01: Perform Addition

**As a** user,
**I want to** add two numbers,
**So that** I can get the sum.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `0` | I click `5`, `+`, `3`, `=` | Display shows `8` |
| 2 | Display shows `0` | I click `1`, `.`, `5`, `+`, `2`, `.`, `5`, `=` | Display shows `4` |
| 3 | Previous result is `10` | I click `+`, `5`, `=` | Display shows `15` |

---

## US-02: Perform Subtraction

**As a** user,
**I want to** subtract one number from another,
**So that** I can get the difference.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `0` | I click `9`, `-`, `4`, `=` | Display shows `5` |
| 2 | Display shows `0` | I click `3`, `-`, `7`, `=` | Display shows `-4` |
| 3 | Display shows `0` | I click `1`, `0`, `.`, `5`, `-`, `3`, `.`, `2`, `=` | Display shows `7.3` |

---

## US-03: Perform Multiplication

**As a** user,
**I want to** multiply two numbers,
**So that** I can get the product.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `0` | I click `6`, `*`, `7`, `=` | Display shows `42` |
| 2 | Display shows `0` | I click `5`, `*`, `0`, `=` | Display shows `0` |
| 3 | Display shows `0` | I click `2`, `.`, `5`, `*`, `4`, `=` | Display shows `10` |

---

## US-04: Perform Division

**As a** user,
**I want to** divide one number by another,
**So that** I can get the quotient.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `0` | I click `8`, `/`, `2`, `=` | Display shows `4` |
| 2 | Display shows `0` | I click `7`, `/`, `2`, `=` | Display shows `3.5` |
| 3 | Display shows `0` | I click `5`, `/`, `0`, `=` | Display shows `Error` |

---

## US-05: Clear Calculator

**As a** user,
**I want to** clear the calculator,
**So that** I can start a fresh calculation.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `123` | I click `AC` | Display shows `0` |
| 2 | A partial expression `5 +` is entered | I click `AC` | Display shows `0`, all operands and operators are cleared |
| 3 | Display shows `Error` | I click `AC` | Display shows `0` |

---

## US-06: Use Decimal Numbers

**As a** user,
**I want to** enter decimal numbers,
**So that** I can perform calculations with fractions.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `0` | I click `.` | Display shows `0.` |
| 2 | Display shows `3.14` | I click `.` | Display still shows `3.14` (second decimal ignored) |
| 3 | Display shows `0` | I click `.`, `5`, `+`, `.`, `5`, `=` | Display shows `1` |

---

## US-07: Handle Division by Zero

**As a** user,
**I want to** see an error when dividing by zero,
**So that** I know the operation is invalid.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `0` | I click `5`, `/`, `0`, `=` | Display shows `Error` |
| 2 | Display shows `Error` | I click `AC` | Display shows `0`, calculator is fully reset |
| 3 | Display shows `Error` | I click any digit | Display shows that digit, calculator resets |

---

## US-08: Toggle Positive/Negative

**As a** user,
**I want to** toggle a number's sign,
**So that** I can work with negative numbers.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `5` | I click `+/-` | Display shows `-5` |
| 2 | Display shows `-5` | I click `+/-` | Display shows `5` |
| 3 | Display shows `0` | I click `+/-` | Display shows `0` (no `-0`) |

---

## US-09: Calculate Percentage

**As a** user,
**I want to** convert a number to its percentage value,
**So that** I can quickly calculate percentages.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `50` | I click `%` | Display shows `0.5` |
| 2 | Display shows `100` | I click `%` | Display shows `1` |
| 3 | Display shows `0` | I click `%` | Display shows `0` |

---

## US-10: Chain Operations

**As a** user,
**I want to** chain multiple operations without pressing `=` each time,
**So that** I can perform sequential calculations efficiently.

### Acceptance Criteria

| # | Given | When | Then |
|---|-------|------|------|
| 1 | Display shows `0` | I click `2`, `+`, `3`, `*` | Display shows `5` (evaluates `2+3` before accepting `*`) |
| 2 | Continued from above | I click `4`, `=` | Display shows `20` (evaluates `5*4`) |
| 3 | Display shows `0` | I click `1`, `0`, `-`, `3`, `+`, `2`, `=` | Display shows `9` |

---

## Traceability Matrix

| User Story | FRD Requirement(s)       | BRD Feature |
|------------|--------------------------|-------------|
| US-01      | FR-03a, FR-04a           | Feature 1   |
| US-02      | FR-03b, FR-04a           | Feature 1   |
| US-03      | FR-03c, FR-04a           | Feature 1   |
| US-04      | FR-03d, FR-03e, FR-04a   | Feature 1   |
| US-05      | FR-05a, FR-05b           | Feature 2   |
| US-06      | FR-06a, FR-06b, FR-06c   | Feature 3   |
| US-07      | FR-03e                   | Feature 1   |
| US-08      | FR-08a                   | Feature 1   |
| US-09      | FR-07a                   | Feature 1   |
| US-10      | FR-04a, FR-04c           | Feature 4   |
