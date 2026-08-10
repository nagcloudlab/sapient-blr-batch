# Module 06 Solutions -- TRAINER ONLY

## Bug #1: NumberFormatException Not Caught

**Root Cause:** `Integer.parseInt(quantityStr)` is called on user input without a try-catch. Non-numeric input like "two" crashes the service.

**Fix:**
```java
// Before
int quantity = Integer.parseInt(quantityStr); // crashes on "two"

// After
int quantity;
try {
    quantity = Integer.parseInt(quantityStr);
    if (quantity <= 0) throw new InvalidOrderException("Quantity must be positive");
} catch (NumberFormatException e) {
    throw new InvalidOrderException("Invalid quantity: " + quantityStr, e);
}
```

## Bug #2: Catch Blocks in Wrong Order

**Root Cause:** `catch (Exception e)` appears before `catch (InvalidOrderException e)`. Since Exception is the parent class, it catches everything first and the specific handler is unreachable.

**Fix:**
```java
// Before
try {
    processOrder(order);
} catch (Exception e) {           // catches everything
    log.error("General error");
} catch (InvalidOrderException e) { // unreachable -- compiler error
    log.error("Invalid order: " + e.getOrderId());
}

// After -- specific exceptions first
try {
    processOrder(order);
} catch (InvalidOrderException e) {
    log.error("Invalid order: " + e.getOrderId());
} catch (Exception e) {
    log.error("Unexpected error", e);
}
```

## Bug #3: File Handle Never Closed

**Root Cause:** `FileWriter` is created but never closed in a `finally` block. If an exception occurs during writing, the file handle leaks.

**Fix:**
```java
// Before
FileWriter writer = new FileWriter("receipt_" + orderId + ".txt");
writer.write(receiptContent);
// writer.close() never called

// After -- try-with-resources
try (FileWriter writer = new FileWriter("receipt_" + orderId + ".txt")) {
    writer.write(receiptContent);
}
```

## Bug #4: Interface Method Not Implemented

**Root Cause:** `CreditCardProcessor` implements `PaymentProcessor` but does not override the `refund()` method. The class is not declared `abstract`, so it compiles (if using a default method in the interface) but throws `AbstractMethodError` or behaves incorrectly at runtime.

**Fix:**
```java
// Before
public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public boolean charge(double amount) { /* implemented */ }
    // refund() missing
}

// After
public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public boolean charge(double amount) { /* implemented */ }

    @Override
    public boolean refund(String transactionId, double amount) {
        // call payment gateway refund API
        System.out.println("Refunding " + amount + " for txn " + transactionId);
        return true;
    }
}
```

## Hints

| Bug | Level 1 | Level 2 |
|-----|---------|---------|
| #1 | "What happens when you pass 'two' to Integer.parseInt()?" | "Wrap in try-catch(NumberFormatException). Rethrow as a custom exception." |
| #2 | "Which catch block runs first? Does the order matter?" | "Put the most specific exception first: InvalidOrderException before Exception." |
| #3 | "Run the receipt export 100 times. Check open file handles with the OS." | "Use try-with-resources: `try (FileWriter w = new FileWriter(...)) { }`" |
| #4 | "Call `processor.refund()`. What error do you get?" | "Add the missing `@Override public boolean refund(...)` method." |
