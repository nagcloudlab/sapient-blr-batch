# Module 05: Java Part 1 -- Lab Setup

## Prerequisites

- Java JDK 17 or higher (`java -version` to confirm)
- Maven 3.8 or higher (`mvn -version` to confirm)
- A terminal / command prompt

## Running the Starter Code

```bash
cd Labs/starter-code/order-service
mvn compile exec:java
```

Maven downloads dependencies on first run. Compilation errors appear immediately and point to the
buggy lines -- this is expected before fixes are applied.

## Verifying Your Fixes

1. After each fix, re-run `mvn compile exec:java`.
2. Watch the console output for:
   - Order creation confirmation lines
   - Discount calculation results (check the values are mathematically correct)
   - Customer lookup results (name and address printed)
3. Compare output against the expected results table in `lab-exercises.md`.
4. All bugs fixed = program runs to completion with no exceptions.

## Expected Behavior

- An order is created with the correct item total.
- Discount is applied and the discounted total is printed.
- Customer details are retrieved and printed by customer ID.
- Program exits cleanly with no stack trace.

## Troubleshooting

**`mvn` not found:** Add Maven's `bin/` directory to your `PATH` environment variable, then restart your
terminal.

**`java.lang.UnsupportedClassVersionError`:** Your JRE is older than JDK 17. Install JDK 17+ and ensure
`JAVA_HOME` points to it.
