# Module 06: Java (Part 2) -- Fix the Issues

## Lab Overview

The FoodExpress Order Service now handles order processing, receipt generation, and payment. But the exception handling is broken, file I/O leaks resources, and an interface implementation is incomplete.

> "Hi Team, we're seeing raw stack traces in production when customers enter bad data. The receipt export is leaking file handles -- after a few hundred orders the server crashes with 'Too many open files'. And the refund feature throws AbstractMethodError. Please fix all exception and I/O issues."

---

## Setup

1. Open `starter-code/foodexpress-java/` in IntelliJ IDEA
2. Run `mvn test` -- notice several test failures
3. Look at the test output: stack traces tell you exactly which line threw
4. Open `OrderService.java` and trace the exception flow

---

## Bug List

### Bug #1: Uncaught NumberFormatException
- **Where:** `OrderService.java` -- `setQuantity()` method
- **Symptom:** Passing "two" as quantity crashes with `NumberFormatException` and shows raw stack trace to user
- **Hint:** Wrap `Integer.parseInt()` in a try-catch. Convert to a custom `InvalidOrderException` with a friendly message.
- **Debug:** Run the test `testInvalidQuantity()`. Read the stack trace. The crash is at `Integer.parseInt()`.

### Bug #2: Catch Blocks in Wrong Order
- **Where:** `OrderService.java` -- `processOrder()` method
- **Symptom:** Compiler warning or error: "exception already caught". The specific `InvalidOrderException` handler never runs.
- **Hint:** `catch (Exception e)` must come after `catch (InvalidOrderException e)`, not before. Java matches the first compatible catch block.
- **Fix:** Reorder the catch blocks from most specific to most general.

### Bug #3: File Handle Leak in ReceiptWriter
- **Where:** `ReceiptWriter.java` -- `writeReceipt()` method
- **Symptom:** After many orders, the server throws `IOException: Too many open files`
- **Hint:** `FileWriter` is created but never closed. If `writer.write()` throws, the handle leaks. Use try-with-resources.
- **Debug:** Add `System.out.println("File handle opened")` before and `"closed"` after. Run 10 receipts. Count the "closed" messages.

### Bug #4: Interface Method Not Implemented
- **Where:** `CreditCardProcessor.java` -- implements `PaymentProcessor`
- **Symptom:** Calling `processor.refund()` throws `AbstractMethodError` at runtime
- **Hint:** The `refund()` method from the `PaymentProcessor` interface is missing. Add the `@Override` implementation.
- **Debug:** Check which methods `PaymentProcessor` declares. Compare with what `CreditCardProcessor` implements.

### Enhancement #5: Custom InvalidOrderException
- **Where:** Create `InvalidOrderException.java`
- **Hint:** Extend `Exception`. Add fields for `orderId` and `reason`. Include a constructor that chains the cause.

### Enhancement #6: try-with-resources Everywhere
- **Where:** `ReceiptWriter.java`, any other I/O code
- **Hint:** Replace all manual close() calls with try-with-resources blocks.

---

## Checkpoints

1. [ ] `testInvalidQuantity()` passes -- friendly error, no raw stack trace
2. [ ] `processOrder()` compiles with catch blocks in correct order
3. [ ] Receipt export works 100 times without "Too many open files"
4. [ ] `processor.refund()` works without AbstractMethodError
5. [ ] Custom exception carries orderId and reason
6. [ ] All I/O uses try-with-resources

## Bonus Challenges

1. Add a `finally` block that logs "Order processing complete" regardless of success or failure
2. Create a `CashOnDeliveryProcessor` that also implements `PaymentProcessor`
3. Write a method that reads a menu from a CSV file using `BufferedReader` with try-with-resources
4. Implement exception chaining: wrap low-level IOException in a custom `ReceiptGenerationException`
