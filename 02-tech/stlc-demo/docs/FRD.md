# Functional Requirements Document (FRD)

## Project: Web Calculator

| Field            | Details                          |
| ---------------- | -------------------------------- |
| Project Name     | Web Calculator                   |
| Prepared By      | Development / BA Team            |
| Version          | 1.0                              |
| Status           | Approved                         |

---

## 1. Overview

This document translates the business requirements into detailed functional specifications that developers and testers can work from.

## 2. UI Layout

```
+-----------------------------------+
|          [ Display Area ]         |   <- Shows input & result
+-----------------------------------+
|   AC   |   +/-  |   %    |   /   |
+-----------------------------------+
|    7   |    8   |    9   |   *   |
+-----------------------------------+
|    4   |    5   |    6   |   -   |
+-----------------------------------+
|    1   |    2   |    3   |   +   |
+-----------------------------------+
|       0        |    .    |   =   |
+-----------------------------------+
```

## 3. Functional Requirements

### FR-01: Display

| ID     | Requirement |
|--------|-------------|
| FR-01a | The display shows `0` on initial load. |
| FR-01b | The display updates as the user clicks digit buttons. |
| FR-01c | The display shows the result after pressing `=`. |
| FR-01d | Maximum display length is 12 characters. |

### FR-02: Digit Input

| ID     | Requirement |
|--------|-------------|
| FR-02a | Clicking digits 0-9 appends to the current number. |
| FR-02b | Leading zeros are not allowed (e.g., `007` becomes `7`). |
| FR-02c | Only one decimal point is allowed per number. |

### FR-03: Arithmetic Operations

| ID     | Requirement |
|--------|-------------|
| FR-03a | **Addition (+):** Returns the sum of two operands. |
| FR-03b | **Subtraction (-):** Returns the difference of two operands. |
| FR-03c | **Multiplication (*):** Returns the product of two operands. |
| FR-03d | **Division (/):** Returns the quotient of two operands. |
| FR-03e | Division by zero displays `Error`. |

### FR-04: Equals (=)

| ID     | Requirement |
|--------|-------------|
| FR-04a | Pressing `=` evaluates the current expression and shows the result. |
| FR-04b | Pressing `=` with no operator does nothing (displays current number). |
| FR-04c | Result becomes the starting number for the next operation. |

### FR-05: Clear (AC)

| ID     | Requirement |
|--------|-------------|
| FR-05a | Pressing `AC` resets the display to `0`. |
| FR-05b | Pressing `AC` clears all stored operands and operators. |

### FR-06: Decimal Point (.)

| ID     | Requirement |
|--------|-------------|
| FR-06a | Pressing `.` adds a decimal point to the current number. |
| FR-06b | If the current number already has a `.`, pressing `.` again is ignored. |
| FR-06c | Pressing `.` at the start creates `0.` |

### FR-07: Percentage (%)

| ID     | Requirement |
|--------|-------------|
| FR-07a | Pressing `%` divides the current number by 100. |

### FR-08: Toggle Sign (+/-)

| ID     | Requirement |
|--------|-------------|
| FR-08a | Pressing `+/-` toggles the current number between positive and negative. |

## 4. Edge Cases & Error Handling

| Scenario                          | Expected Behavior              |
| --------------------------------- | ------------------------------ |
| Divide by zero                    | Display shows `Error`          |
| Multiple operator presses         | Last operator wins             |
| Very large result (> 12 digits)   | Display shows scientific notation or `Error` |
| Pressing `=` without full expression | Displays the current number  |
| Pressing operator without first number | Uses `0` as first operand   |

## 5. Non-Functional Requirements

| ID      | Requirement |
|---------|-------------|
| NFR-01  | Page loads in under 1 second (no server dependency). |
| NFR-02  | Works on Chrome, Firefox, and Edge (latest versions). |
| NFR-03  | Responsive — usable on screens 320px and above. |
| NFR-04  | No external runtime dependencies (pure HTML/CSS/JS). |
