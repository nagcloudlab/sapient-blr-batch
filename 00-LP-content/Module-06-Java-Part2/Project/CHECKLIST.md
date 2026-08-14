# Module 06 Checklist -- Participant Submission

## Bug Fixes
- [ ] Bug #1: Invalid quantity input returns friendly error (no raw stack trace)
- [ ] Bug #2: Catch blocks are in correct order (specific before general)
- [ ] Bug #3: File handles are properly closed (try-with-resources)
- [ ] Bug #4: All interface methods are implemented (no AbstractMethodError)

## Enhancements
- [ ] Custom InvalidOrderException carries order context (orderId, reason)
- [ ] All I/O operations use try-with-resources
- [ ] Payable interface implemented for CreditCard and CashOnDelivery

## Debugging Evidence
- [ ] Screenshot of stack trace showing the exception chain
- [ ] Brief description of how you read the stack trace to find root cause

## Self-Check Questions
1. Why must specific exception catches come before general ones?
2. What is the difference between checked and unchecked exceptions?
3. How does try-with-resources guarantee the resource is closed?
4. When should you create a custom exception vs. using a built-in one?
5. What is the difference between an interface and an abstract class?
