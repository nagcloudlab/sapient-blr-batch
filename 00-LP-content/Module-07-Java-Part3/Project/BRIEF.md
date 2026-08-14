# Module 07: Java (Part 3) -- Collections and JDBC Bugs

## Sustain Context

The client escalated:

> "The exception handling is clean now, but we have new production issues. The order history page crashes when a customer modifies their cart while we're iterating over it. The menu listing shows raw Object references instead of item names. And the JDBC code for saving orders has a connection leak -- the database pool is exhausted after an hour of traffic. This is our highest-priority fix."

---

## Tasks

| # | Type | Issue | File |
|---|------|-------|------|
| 1 | BUG | ConcurrentModificationException when removing items during iteration | `CartService.java` |
| 2 | BUG | Wrong collection type -- ArrayList used where HashSet needed (duplicates) | `MenuService.java` |
| 3 | BUG | Missing generics -- List stores raw Objects, requires casting | `OrderRepository.java` |
| 4 | BUG | JDBC connection never closed (connection pool exhaustion) | `OrderRepository.java` |
| 5 | ENH | Use Iterator.remove() or removeIf() for safe removal | `CartService.java` |
| 6 | ENH | PreparedStatement with parameterized queries (prevent SQL injection) | `OrderRepository.java` |
| 7 | ENH | Connection pooling with try-with-resources | `OrderRepository.java` |
| 8 | DEBUG | Trace the ConcurrentModificationException using stack trace | IDE Debugger |

## Deliverables

- [ ] All 4 bugs fixed, 3 enhancements added
- [ ] At least one bug traced with debugger or stack trace (screenshot)
- [ ] Brief notes: root cause and fix for each bug
