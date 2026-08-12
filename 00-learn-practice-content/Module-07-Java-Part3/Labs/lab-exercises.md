# Module 07: Java (Part 3) -- Fix the Issues

## Lab Overview

The FoodExpress backend now uses Java Collections for cart and menu management and JDBC for order persistence. But the code has critical bugs: concurrent modification crashes, duplicate data from wrong collection types, raw type warnings, and database connection leaks.

> "Hi Team, the order history page is crashing intermittently -- stack trace shows ConcurrentModificationException. The cuisine filter dropdown shows 'Italian' three times. And the database pool is exhausted after about an hour of traffic. We also see compiler warnings about raw types everywhere. Please fix urgently."

---

## Setup

1. Open `starter-code/foodexpress-java/` in IntelliJ IDEA
2. Ensure MySQL/H2 is running (check `db.properties` for connection details)
3. Run `mvn test` -- notice ConcurrentModificationException and connection failures
4. Check compiler warnings -- notice "unchecked or unsafe operations" messages

---

## Bug List

### Bug #1: ConcurrentModificationException
- **Where:** `CartService.java` -- `removeExpiredItems()` method
- **Symptom:** Removing items from the cart during a for-each loop crashes with ConcurrentModificationException
- **Hint:** You cannot call `list.remove()` inside a for-each loop. Use `removeIf()` or an explicit `Iterator` with `it.remove()`.
- **Debug:** Set a breakpoint inside the for-each loop. Step through. The exception occurs on the second iteration after a removal.

### Bug #2: Wrong Collection Type Allows Duplicates
- **Where:** `MenuService.java` -- `getCategories()` method
- **Symptom:** The cuisine filter dropdown shows "Italian", "Italian", "Chinese", "Italian" instead of unique values
- **Hint:** `ArrayList` allows duplicates. Switch to `LinkedHashSet` to maintain insertion order while eliminating duplicates.
- **Debug:** Print the categories collection. Count the duplicates.

### Bug #3: Raw Types and Unsafe Casts
- **Where:** `OrderRepository.java` -- `findAll()` method
- **Symptom:** Compiler warns "unchecked or unsafe operations". A `ClassCastException` can occur at runtime if the wrong type is added.
- **Hint:** Change `List orders = new ArrayList()` to `List<Order> orders = new ArrayList<>()`. Remove manual casts.
- **Fix:** Add type parameters to all collection declarations.

### Bug #4: JDBC Connection Leak
- **Where:** `OrderRepository.java` -- `save()` and `findByCustomerId()` methods
- **Symptom:** After ~100 orders, the app throws "Cannot get a connection, pool exhausted"
- **Hint:** `Connection`, `PreparedStatement`, and `ResultSet` are opened but never closed. Use try-with-resources for all three.
- **Debug:** Add logging to track when connections are opened and closed. After 10 orders, check how many "opened" vs "closed" messages appear.

### Enhancement #5: Use PreparedStatement Instead of Statement
- **Where:** `OrderRepository.java`
- **Hint:** Replace string concatenation (`"SELECT * FROM orders WHERE id = " + id`) with `PreparedStatement` and `setString()`.

### Enhancement #6: Implement removeIf() for Cart Cleanup
- **Where:** `CartService.java`
- **Hint:** Replace the for-each + remove pattern with a single `cart.removeIf(item -> item.getQuantity() == 0)` call.

---

## Checkpoints

1. [ ] Cart removal works without ConcurrentModificationException
2. [ ] Cuisine categories list has no duplicates
3. [ ] No compiler warnings about raw types or unchecked operations
4. [ ] App runs for 10+ minutes without database pool exhaustion
5. [ ] All SQL uses PreparedStatement with parameters
6. [ ] JDBC resources use try-with-resources

## Bonus Challenges

1. Use `Collections.unmodifiableList()` to return a read-only view of the cart
2. Implement a `Map<String, List<MenuItem>>` to group menu items by category
3. Add a `findByDateRange()` method to OrderRepository using PreparedStatement with date parameters
4. Replace raw JDBC with a connection pool library (HikariCP) and compare resource usage
