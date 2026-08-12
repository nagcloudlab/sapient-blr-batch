# Module 07: Java Part 3 -- Lab Setup

## Prerequisites

- Java JDK 17 or higher (`java -version` to confirm)
- Maven 3.8 or higher (`mvn -version` to confirm)
- A terminal / command prompt

## Running the Starter Code

```bash
cd Labs/starter-code/order-service
mvn compile exec:java
```

Bugs in this module relate to collections, hashing, and JDBC. Some will produce wrong output rather
than exceptions, so read the output carefully against the expected values.

## Verifying Your Fixes

1. Re-run `mvn compile exec:java` after each fix.
2. Check the console for:
   - Correct order lookup results (right order for given ID)
   - Menu item hash operations returning consistent results
   - JDBC query results matching the seeded test data
3. Use the expected output table in `lab-exercises.md` as the comparison baseline.
4. No `ConcurrentModificationException` or `ClassCastException` in the output.

## Expected Behavior

- Order lookups by ID return the correct order object.
- `HashMap` / `HashSet` operations on menu items behave consistently across runs.
- JDBC queries return the correct row counts and field values from the test database.
- Collections are iterated without throwing `ConcurrentModificationException`.

## Troubleshooting

**JDBC connection refused:** The lab uses an embedded H2 in-memory database by default -- no external
database is needed. If you see a connection error, check the JDBC URL in the source file matches the
H2 driver class name configured in `pom.xml`.

**Wrong output but no exception:** Trace through the collection logic manually or add temporary
`System.out.println` statements to inspect intermediate values.
