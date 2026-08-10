# Module 06: Java (Part 2) -- Exception Handling and I/O Bugs

## Sustain Context

The client escalated:

> "The domain classes are solid now. But the Order Service is crashing in production. When a customer enters an invalid quantity, the app shows a raw stack trace instead of a friendly message. The order export feature leaks file handles and eventually the server runs out of resources. Also, the PaymentProcessor interface was implemented wrong -- it compiles but throws at runtime. Please fix these before we lose more uptime."

---

## Tasks

| # | Type | Issue | File |
|---|------|-------|------|
| 1 | BUG | NumberFormatException not caught on quantity input | `OrderService.java` |
| 2 | BUG | Catch blocks in wrong order (parent before child) | `OrderService.java` |
| 3 | BUG | File handle never closed after writing order receipt | `ReceiptWriter.java` |
| 4 | BUG | Interface method not implemented (AbstractMethodError) | `CreditCardProcessor.java` |
| 5 | ENH | Custom `InvalidOrderException` with order context | `InvalidOrderException.java` |
| 6 | ENH | try-with-resources for all I/O operations | `ReceiptWriter.java` |
| 7 | ENH | Implement a `Payable` interface for multiple payment types | `PaymentProcessor.java` |
| 8 | DEBUG | Trace the resource leak using JVisualVM or IDE profiler | IDE Profiler |

## Deliverables

- [ ] All 4 bugs fixed, 3 enhancements added
- [ ] At least one bug traced with stack trace analysis (screenshot)
- [ ] Brief notes: root cause and fix for each bug
