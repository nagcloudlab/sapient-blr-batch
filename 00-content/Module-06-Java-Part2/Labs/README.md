# Module 06: Java Part 2 -- Lab Setup

## Prerequisites

- Java JDK 17 or higher (`java -version` to confirm)
- Maven 3.8 or higher (`mvn -version` to confirm)
- A terminal / command prompt

## Running the Starter Code

```bash
cd Labs/starter-code/order-service
mvn compile exec:java
```

Some bugs will cause the program to throw exceptions immediately on startup. The stack trace tells you
which class and line number to investigate first.

## Verifying Your Fixes

1. Re-run `mvn compile exec:java` after each fix.
2. Check the console for:
   - Meaningful exception messages (not raw stack traces leaking to the end user)
   - A confirmation line that the CSV file was written successfully
   - A "resources closed" or "connection closed" log at program end
3. Open the generated CSV file (path printed in output) and verify its contents.
4. All bugs fixed = no unhandled exceptions, CSV present, streams closed.

## Expected Behavior

- Custom exception messages are printed for invalid order states (not raw `NullPointerException`).
- Order data is exported to a CSV file in the working directory.
- File and database resources are closed in `finally` blocks -- no resource-leak warnings.
- Program exits with code 0 (no unhandled exceptions).

## Troubleshooting

**CSV file not created:** Check the file path used in the code -- a missing parent directory causes a
`FileNotFoundException`. Create the directory or fix the path to use the current directory.

**Exception swallowed silently:** If the program exits too quickly with no output, a `catch` block may
be empty. Add a `System.err.println(e.getMessage())` to expose what went wrong.
