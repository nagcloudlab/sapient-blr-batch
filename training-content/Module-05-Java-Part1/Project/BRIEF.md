# Module 05: Java (Part 1) -- Domain Class Bugs

## Sustain Context

The client escalated:

> "The React frontend is stable now. We're building the backend in Java. The dev team created the MenuItem and Order domain classes, but the unit tests are failing. Items have wrong prices, the Order constructor crashes, and some fields are accessible when they shouldn't be. We need the domain model solid before we build the API layer."

---

## Tasks

| # | Type | Issue | File |
|---|------|-------|------|
| 1 | BUG | MenuItem fields are public -- violates encapsulation | `MenuItem.java` |
| 2 | BUG | Order constructor throws NullPointerException (missing initialization) | `Order.java` |
| 3 | BUG | Static field shared across all instances (order counter) | `Order.java` |
| 4 | BUG | Wrong package import causes compilation error | `OrderService.java` |
| 5 | ENH | Add a `toString()` override for MenuItem (for logging) | `MenuItem.java` |
| 6 | ENH | Add a `Builder` pattern to construct MenuItem | `MenuItem.java` |
| 7 | ENH | Implement `equals()` and `hashCode()` based on item ID | `MenuItem.java` |
| 8 | DEBUG | Trace the static vs instance bug using IntelliJ debugger | IDE Debugger |

## Deliverables

- [ ] All 4 bugs fixed, 3 enhancements added
- [ ] At least one bug traced with IDE debugger (screenshot)
- [ ] Brief notes: root cause and fix for each bug
