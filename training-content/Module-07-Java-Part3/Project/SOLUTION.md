# Module 07 Solutions -- TRAINER ONLY

## Bug #1: ConcurrentModificationException

**Root Cause:** The code iterates over `cart` with a for-each loop and calls `cart.remove(item)` inside the loop. Java's fail-fast iterators throw `ConcurrentModificationException` when the collection is modified during iteration.

**Fix:**
```java
// Before
for (MenuItem item : cart) {
    if (item.getQuantity() == 0) {
        cart.remove(item); // ConcurrentModificationException
    }
}

// After -- use removeIf()
cart.removeIf(item -> item.getQuantity() == 0);

// Or use Iterator explicitly
Iterator<MenuItem> it = cart.iterator();
while (it.hasNext()) {
    if (it.next().getQuantity() == 0) {
        it.remove();
    }
}
```

## Bug #2: Wrong Collection Type (Duplicates Allowed)

**Root Cause:** `MenuService` uses `ArrayList<String>` for cuisine categories. When menus are loaded from multiple restaurants, duplicate categories like "Italian" appear multiple times in the filter dropdown.

**Fix:**
```java
// Before
List<String> categories = new ArrayList<>();
for (MenuItem item : allItems) {
    categories.add(item.getCategory()); // duplicates added
}

// After -- use LinkedHashSet to preserve order and eliminate duplicates
Set<String> categories = new LinkedHashSet<>();
for (MenuItem item : allItems) {
    categories.add(item.getCategory()); // duplicates ignored
}
```

## Bug #3: Missing Generics (Raw Types)

**Root Cause:** `List orders = new ArrayList();` uses raw types. Items are stored as `Object` and require unsafe casting. The compiler warns but allows it, leading to `ClassCastException` at runtime.

**Fix:**
```java
// Before
List orders = new ArrayList();          // raw type
orders.add(order);
Order o = (Order) orders.get(0);        // unsafe cast

// After -- parameterized type
List<Order> orders = new ArrayList<>();
orders.add(order);
Order o = orders.get(0);                // no cast needed
```

## Bug #4: JDBC Connection Never Closed

**Root Cause:** `DriverManager.getConnection()` is called but the `Connection`, `PreparedStatement`, and `ResultSet` are never closed. Each request opens a new connection that is never returned to the pool.

**Fix:**
```java
// Before
Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery("SELECT * FROM orders");
// conn, stmt, rs never closed

// After -- try-with-resources
try (Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
     PreparedStatement stmt = conn.prepareStatement("SELECT * FROM orders WHERE customer_id = ?")) {
    stmt.setString(1, customerId);
    try (ResultSet rs = stmt.executeQuery()) {
        while (rs.next()) {
            // process rows
        }
    }
}
```

## Hints

| Bug | Level 1 | Level 2 |
|-----|---------|---------|
| #1 | "Can you modify a list while iterating over it with for-each?" | "Use `removeIf(predicate)` or `Iterator.remove()`." |
| #2 | "Print the categories list. Do you see duplicates?" | "Use a `Set` instead of a `List` to eliminate duplicates automatically." |
| #3 | "What does the compiler warning 'raw type' mean?" | "Add the type parameter: `List<Order>` instead of `List`." |
| #4 | "Run the app for 5 minutes. Check active DB connections." | "Use try-with-resources for Connection, PreparedStatement, and ResultSet." |
