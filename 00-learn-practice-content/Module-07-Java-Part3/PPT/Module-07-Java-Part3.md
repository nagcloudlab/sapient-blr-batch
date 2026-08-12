# Java Programming (Part 3)
## Module 07 | Sustain Engineering Training | Day 8

**1 day | Workshop + guided lab**

---

## Agenda

| Session | Topics |
|---------|--------|
| Morning (1st half) | Collections Framework, Generics, List, Set, Map, Maven |
| Afternoon (2nd half) | Iterator, Autoboxing, JDBC, DriverManager, Connection |
| Backend Ops | Memory Management, Performance Tuning, Logging, Debugging |

> Building on Module 05-06 Java foundations -- today we go deeper into real-world backend Java.

---

## Why Collections Matter in Sustain Engineering

- Legacy codebases are **full** of collections -- `List`, `Map`, `Set` everywhere
- Understanding collection behavior is critical for:
  - Debugging `ConcurrentModificationException`
  - Fixing memory leaks from growing collections
  - Optimizing slow loops over large datasets
- In sustain work, you **read** collections code far more than you write it

---

## Java Collections Framework -- Overview

```
                  Iterable
                     |
                 Collection
                /    |     \
             List   Set    Queue
              |      |       |
         ArrayList HashSet PriorityQueue
         LinkedList TreeSet
```

| Interface | Duplicates | Ordered | Key Use Case |
|-----------|-----------|---------|--------------|
| `List` | Yes | Yes (insertion order) | Ordered items, indexed access |
| `Set` | No | Depends on impl | Unique items, membership checks |
| `Map` | Keys: No, Values: Yes | Depends on impl | Key-value lookups |

---

## Generics -- Type Safety

### Without Generics (raw types -- legacy code)

```java
List items = new ArrayList();
items.add("Pizza");
items.add(42);  // No compile error!
String name = (String) items.get(1);  // ClassCastException at runtime!
```

### With Generics

```java
List<String> items = new ArrayList<>();
items.add("Pizza");
// items.add(42);  // Compile error -- caught early!
String name = items.get(0);  // No cast needed
```

> Generics move errors from **runtime** to **compile time** -- crucial for sustain reliability.

---

## Generic Classes and Methods

### Generic Class

```java
public class OrderResult<T> {
    private T data;
    private boolean success;

    public OrderResult(T data, boolean success) {
        this.data = data;
        this.success = success;
    }

    public T getData() { return data; }
}

// Usage
OrderResult<MenuItem> result = new OrderResult<>(menuItem, true);
OrderResult<String> error = new OrderResult<>("Not found", false);
```

### Generic Method

```java
public static <T> List<T> filterByCondition(List<T> items, Predicate<T> condition) {
    List<T> filtered = new ArrayList<>();
    for (T item : items) {
        if (condition.test(item)) filtered.add(item);
    }
    return filtered;
}
```

---

## Bounded Type Parameters

```java
// T must extend Comparable
public static <T extends Comparable<T>> T findMax(List<T> items) {
    T max = items.get(0);
    for (T item : items) {
        if (item.compareTo(max) > 0) max = item;
    }
    return max;
}
```

### Wildcards

| Wildcard | Meaning | Use Case |
|----------|---------|----------|
| `<?>` | Any type | Read-only access |
| `<? extends T>` | T or subclass | Producer (read) |
| `<? super T>` | T or superclass | Consumer (write) |

```java
// Accepts List of MenuItem or any subclass of MenuItem
public void displayItems(List<? extends MenuItem> items) {
    for (MenuItem item : items) {
        System.out.println(item.getName());
    }
}
```

---

## List Interface -- ArrayList

```java
import java.util.ArrayList;
import java.util.List;

List<MenuItem> menu = new ArrayList<>();

// Add items
menu.add(new MenuItem("Burger", 9.99));
menu.add(new MenuItem("Pizza", 12.99));
menu.add(0, new MenuItem("Salad", 7.99));  // Insert at index

// Access
MenuItem first = menu.get(0);          // Salad
int size = menu.size();                 // 3
boolean has = menu.contains(burger);    // true

// Modify
menu.set(1, new MenuItem("Veggie Burger", 10.99));
menu.remove(0);                         // Remove by index
menu.remove(burger);                    // Remove by object
```

### ArrayList Internals

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| `get(i)` | O(1) | Direct array access |
| `add(e)` | O(1) amortized | May trigger resize |
| `add(i, e)` | O(n) | Shifts elements |
| `remove(i)` | O(n) | Shifts elements |
| `contains(e)` | O(n) | Linear search |

---

## ArrayList vs LinkedList

```java
List<OrderItem> arrayList = new ArrayList<>();   // Array-backed
List<OrderItem> linkedList = new LinkedList<>();  // Node-backed
```

| Criteria | ArrayList | LinkedList |
|----------|-----------|------------|
| Random access `get(i)` | O(1) -- fast | O(n) -- slow |
| Add/Remove at end | O(1) amortized | O(1) |
| Add/Remove at middle | O(n) -- shifting | O(1) if at node |
| Memory overhead | Lower | Higher (node pointers) |
| Cache performance | Better (contiguous) | Worse (scattered) |

> **Sustain tip:** In 95% of cases, `ArrayList` is the right choice. Only use `LinkedList` when you have measured proof it helps.

---

## FoodExpress: OrderItem List Example

```java
public class OrderService {
    private List<OrderItem> orderItems = new ArrayList<>();

    public void addItem(MenuItem menuItem, int quantity) {
        // Check if item already exists in order
        for (OrderItem item : orderItems) {
            if (item.getMenuItemId().equals(menuItem.getId())) {
                item.setQuantity(item.getQuantity() + quantity);
                return;
            }
        }
        orderItems.add(new OrderItem(menuItem, quantity));
    }

    public double calculateTotal() {
        double total = 0;
        for (OrderItem item : orderItems) {
            total += item.getPrice() * item.getQuantity();
        }
        return total;
    }

    public List<OrderItem> getItems() {
        return Collections.unmodifiableList(orderItems);  // Defensive copy
    }
}
```

---

## Set Interface -- HashSet

```java
import java.util.HashSet;
import java.util.Set;

Set<String> cuisines = new HashSet<>();
cuisines.add("Italian");
cuisines.add("Chinese");
cuisines.add("Italian");   // Duplicate -- ignored!

System.out.println(cuisines.size());  // 2
System.out.println(cuisines.contains("Italian"));  // true
```

### How HashSet Works

1. Calls `hashCode()` on the object
2. Determines bucket from hash
3. If bucket has items, calls `equals()` to check duplicates
4. Stores only if no equal object found

> **Critical:** If you override `equals()`, you **must** override `hashCode()` too!

---

## equals() and hashCode() Contract

```java
public class MenuItem {
    private String id;
    private String name;
    private double price;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        MenuItem that = (MenuItem) o;
        return Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
```

### The Rules

| Rule | Violation Impact |
|------|-----------------|
| Equal objects must have same hashCode | Items "disappear" from HashSet/HashMap |
| Same hashCode does NOT mean equal | Normal -- hash collisions happen |
| hashCode must be consistent | Unpredictable behavior |

---

## Set Implementations Compared

```java
Set<String> hashSet   = new HashSet<>();    // Unordered, fastest
Set<String> linkedSet = new LinkedHashSet<>();  // Insertion order
Set<String> treeSet   = new TreeSet<>();    // Sorted (natural order)
```

| Implementation | Order | Add/Remove/Contains | Use Case |
|---------------|-------|-------------------|----------|
| `HashSet` | None | O(1) average | Default choice |
| `LinkedHashSet` | Insertion order | O(1) average | Need order preserved |
| `TreeSet` | Sorted | O(log n) | Need sorted iteration |

### Set Operations

```java
Set<String> a = new HashSet<>(Arrays.asList("Pizza", "Burger", "Pasta"));
Set<String> b = new HashSet<>(Arrays.asList("Pizza", "Sushi", "Pasta"));

Set<String> union = new HashSet<>(a);
union.addAll(b);          // [Pizza, Burger, Pasta, Sushi]

Set<String> intersection = new HashSet<>(a);
intersection.retainAll(b); // [Pizza, Pasta]

Set<String> difference = new HashSet<>(a);
difference.removeAll(b);   // [Burger]
```

---

## Map Interface -- HashMap

```java
import java.util.HashMap;
import java.util.Map;

Map<String, Double> menuPrices = new HashMap<>();

// Put entries
menuPrices.put("Burger", 9.99);
menuPrices.put("Pizza", 12.99);
menuPrices.put("Salad", 7.99);

// Access
Double price = menuPrices.get("Pizza");        // 12.99
Double missing = menuPrices.get("Sushi");      // null
Double safe = menuPrices.getOrDefault("Sushi", 0.0);  // 0.0

// Check
boolean hasKey = menuPrices.containsKey("Burger");     // true
boolean hasVal = menuPrices.containsValue(9.99);       // true

// Remove
menuPrices.remove("Salad");

// Size
int count = menuPrices.size();  // 2
```

---

## Iterating Over Maps

```java
Map<String, MenuItem> menuCatalog = new HashMap<>();

// Method 1: entrySet (most common, most efficient)
for (Map.Entry<String, MenuItem> entry : menuCatalog.entrySet()) {
    System.out.println(entry.getKey() + " -> " + entry.getValue().getPrice());
}

// Method 2: keySet
for (String key : menuCatalog.keySet()) {
    MenuItem item = menuCatalog.get(key);  // Extra lookup
}

// Method 3: values only
for (MenuItem item : menuCatalog.values()) {
    System.out.println(item.getName());
}

// Method 4: forEach (Java 8+)
menuCatalog.forEach((key, value) ->
    System.out.println(key + ": " + value.getPrice())
);
```

> **Best practice:** Use `entrySet()` when you need both key and value. Avoids extra `get()` calls.

---

## FoodExpress: Order Tracking with Map

```java
public class OrderTracker {
    // orderId -> Order
    private Map<String, Order> activeOrders = new HashMap<>();
    // customerId -> list of orderIds
    private Map<String, List<String>> customerOrders = new HashMap<>();

    public void placeOrder(Order order) {
        activeOrders.put(order.getId(), order);

        // computeIfAbsent: create list if customer has no orders yet
        customerOrders
            .computeIfAbsent(order.getCustomerId(), k -> new ArrayList<>())
            .add(order.getId());
    }

    public Order getOrder(String orderId) {
        Order order = activeOrders.get(orderId);
        if (order == null) {
            throw new OrderNotFoundException("Order not found: " + orderId);
        }
        return order;
    }

    public List<Order> getCustomerOrders(String customerId) {
        List<String> orderIds = customerOrders.getOrDefault(customerId, List.of());
        return orderIds.stream()
            .map(activeOrders::get)
            .collect(Collectors.toList());
    }
}
```

---

## Map Implementations Compared

| Implementation | Order | Performance | Null Keys | Thread Safe |
|---------------|-------|-------------|-----------|-------------|
| `HashMap` | None | O(1) avg | 1 allowed | No |
| `LinkedHashMap` | Insertion | O(1) avg | 1 allowed | No |
| `TreeMap` | Sorted | O(log n) | No | No |
| `Hashtable` | None | O(1) avg | No | Yes (legacy) |
| `ConcurrentHashMap` | None | O(1) avg | No | Yes (modern) |

> **Sustain tip:** Never use `Hashtable` in new code. Use `ConcurrentHashMap` for thread safety.

---

## Maven -- Build Tool Overview

### What Maven Does

- **Dependency management** -- downloads JAR files automatically
- **Build lifecycle** -- compile, test, package, deploy
- **Project structure** -- standard directory layout
- **Plugin ecosystem** -- extend build capabilities

### Standard Maven Project Structure

```
my-project/
  pom.xml
  src/
    main/
      java/          # Application source code
      resources/     # Config files, properties
    test/
      java/          # Test source code
      resources/     # Test config files
  target/            # Build output (generated)
```

---

## POM.xml -- Project Object Model

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.foodexpress</groupId>
    <artifactId>order-service</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <java.version>17</java.version>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.33</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

---

## Maven Lifecycle & Commands

| Phase | Description | Command |
|-------|-------------|---------|
| `validate` | Check project structure | `mvn validate` |
| `compile` | Compile source code | `mvn compile` |
| `test` | Run unit tests | `mvn test` |
| `package` | Create JAR/WAR | `mvn package` |
| `install` | Install to local repo | `mvn install` |
| `deploy` | Deploy to remote repo | `mvn deploy` |
| `clean` | Delete target/ directory | `mvn clean` |

### Common Commands in Sustain Work

```bash
# Clean build
mvn clean package

# Skip tests (use sparingly!)
mvn clean package -DskipTests

# Run specific test class
mvn test -Dtest=OrderServiceTest

# Check dependency tree (debug dependency conflicts)
mvn dependency:tree

# Check for outdated dependencies
mvn versions:display-dependency-updates
```

---

## Iterator Pattern

```java
List<OrderItem> items = getOrderItems();
Iterator<OrderItem> iterator = items.iterator();

while (iterator.hasNext()) {
    OrderItem item = iterator.next();
    if (item.getQuantity() == 0) {
        iterator.remove();  // Safe removal during iteration!
    }
}
```

### Why Iterator Matters

```java
// THIS WILL CRASH -- ConcurrentModificationException
for (OrderItem item : items) {
    if (item.getQuantity() == 0) {
        items.remove(item);  // Modifying list during for-each!
    }
}

// Use Iterator.remove() instead -- or Java 8+:
items.removeIf(item -> item.getQuantity() == 0);
```

> **Sustain bug pattern:** `ConcurrentModificationException` is one of the most common collection bugs in production code.

---

## ListIterator -- Bidirectional Traversal

```java
List<MenuItem> menu = new ArrayList<>(Arrays.asList(
    new MenuItem("Burger", 9.99),
    new MenuItem("Pizza", 12.99),
    new MenuItem("Salad", 7.99)
));

ListIterator<MenuItem> li = menu.listIterator();

// Forward traversal
while (li.hasNext()) {
    int index = li.nextIndex();
    MenuItem item = li.next();
    System.out.println(index + ": " + item.getName());
}

// Backward traversal
while (li.hasPrevious()) {
    MenuItem item = li.previous();
    System.out.println(item.getName());
}

// Modify during iteration
ListIterator<MenuItem> li2 = menu.listIterator();
while (li2.hasNext()) {
    MenuItem item = li2.next();
    if (item.getPrice() > 10.0) {
        li2.set(new MenuItem(item.getName(), item.getPrice() * 0.9));  // 10% discount
    }
}
```

---

## Autoboxing and Unboxing

### What Is It?

```java
// Autoboxing: primitive -> wrapper (automatic)
int primitivePrice = 10;
Integer wrappedPrice = primitivePrice;  // int -> Integer

// Unboxing: wrapper -> primitive (automatic)
Integer wrappedQty = 5;
int primitiveQty = wrappedQty;  // Integer -> int
```

### Primitive-Wrapper Mapping

| Primitive | Wrapper | Size |
|-----------|---------|------|
| `byte` | `Byte` | 1 byte |
| `short` | `Short` | 2 bytes |
| `int` | `Integer` | 4 bytes |
| `long` | `Long` | 8 bytes |
| `float` | `Float` | 4 bytes |
| `double` | `Double` | 8 bytes |
| `char` | `Character` | 2 bytes |
| `boolean` | `Boolean` | 1 bit |

---

## Autoboxing Pitfalls

### NullPointerException from Unboxing

```java
Map<String, Integer> itemCounts = new HashMap<>();
// itemCounts.get("Burger") returns null (not in map)
int count = itemCounts.get("Burger");  // NPE! Unboxing null -> crash

// Fix:
Integer count = itemCounts.get("Burger");
if (count != null) {
    // safe to use
}
// Or:
int count = itemCounts.getOrDefault("Burger", 0);
```

### Performance Trap

```java
// BAD: Creates ~1000 Integer objects due to autoboxing
Long sum = 0L;
for (long i = 0; i < 1000; i++) {
    sum += i;  // Unbox, add, rebox on every iteration!
}

// GOOD: Use primitives for calculations
long sum = 0L;
for (long i = 0; i < 1000; i++) {
    sum += i;
}
```

> **Sustain tip:** Watch for autoboxing in loops -- it silently creates garbage and slows performance.

---

## JDBC Overview

### What Is JDBC?

- **Java Database Connectivity** -- standard API for relational databases
- Part of `java.sql` package
- Works with MySQL, PostgreSQL, Oracle, SQLite, etc.

### JDBC Architecture

```
Java Application
      |
   JDBC API (java.sql)
      |
   JDBC Driver (vendor-specific)
      |
   Database Server
```

### Key JDBC Interfaces

| Interface | Purpose |
|-----------|---------|
| `DriverManager` | Manages database drivers, creates connections |
| `Connection` | Represents a database session |
| `Statement` | Executes SQL queries |
| `PreparedStatement` | Pre-compiled SQL (prevents SQL injection) |
| `ResultSet` | Holds query results |

---

## JDBC Connection Setup

### 1. Add MySQL Driver (Maven)

```xml
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.33</version>
</dependency>
```

### 2. Establish Connection

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConfig {
    private static final String URL = "jdbc:mysql://localhost:3306/foodexpress";
    private static final String USER = "app_user";
    private static final String PASSWORD = "secret";

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}
```

### 3. Always Use Try-with-Resources

```java
try (Connection conn = DatabaseConfig.getConnection()) {
    // Use connection
} catch (SQLException e) {
    System.err.println("Database connection failed: " + e.getMessage());
}
// Connection auto-closed here
```

---

## JDBC CRUD Operations

### INSERT

```java
String sql = "INSERT INTO menu_items (name, price, category) VALUES (?, ?, ?)";
try (Connection conn = DatabaseConfig.getConnection();
     PreparedStatement pstmt = conn.prepareStatement(sql)) {

    pstmt.setString(1, "Margherita Pizza");
    pstmt.setDouble(2, 12.99);
    pstmt.setString(3, "Italian");

    int rowsInserted = pstmt.executeUpdate();
    System.out.println(rowsInserted + " row(s) inserted.");
}
```

### SELECT

```java
String sql = "SELECT id, name, price FROM menu_items WHERE category = ?";
try (Connection conn = DatabaseConfig.getConnection();
     PreparedStatement pstmt = conn.prepareStatement(sql)) {

    pstmt.setString(1, "Italian");
    try (ResultSet rs = pstmt.executeQuery()) {
        while (rs.next()) {
            int id = rs.getInt("id");
            String name = rs.getString("name");
            double price = rs.getDouble("price");
            System.out.println(id + ": " + name + " - $" + price);
        }
    }
}
```

---

## PreparedStatement vs Statement

### NEVER Use String Concatenation (SQL Injection!)

```java
// DANGEROUS -- SQL Injection vulnerability
String sql = "SELECT * FROM users WHERE username = '" + username + "'";
// If username = "admin' OR '1'='1" -- returns ALL users!

// SAFE -- Use PreparedStatement
String sql = "SELECT * FROM users WHERE username = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setString(1, username);  // Properly escaped
```

| Feature | Statement | PreparedStatement |
|---------|-----------|-------------------|
| SQL Injection | Vulnerable | Protected |
| Performance | Parsed every time | Pre-compiled, cached |
| Readability | Hard (concatenation) | Clean (placeholders) |
| Batch support | Limited | Full support |

> **Rule:** Always use `PreparedStatement`. No exceptions.

---

## FoodExpress: Menu Item DAO

```java
public class MenuItemDAO {
    public List<MenuItem> findByCategory(String category) throws SQLException {
        String sql = "SELECT id, name, price, category FROM menu_items WHERE category = ?";
        List<MenuItem> items = new ArrayList<>();

        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, category);
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    items.add(new MenuItem(
                        rs.getInt("id"),
                        rs.getString("name"),
                        rs.getDouble("price"),
                        rs.getString("category")
                    ));
                }
            }
        }
        return items;
    }

    public boolean updatePrice(int itemId, double newPrice) throws SQLException {
        String sql = "UPDATE menu_items SET price = ? WHERE id = ?";
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setDouble(1, newPrice);
            pstmt.setInt(2, itemId);
            return pstmt.executeUpdate() > 0;
        }
    }
}
```

---

## Memory Management -- JVM Heap

### JVM Memory Areas

| Area | Stores | Managed By |
|------|--------|------------|
| **Heap** | Objects, arrays | Garbage Collector |
| **Stack** | Method frames, local vars, refs | Automatic (per thread) |
| **Metaspace** | Class metadata, method info | JVM |
| **Code Cache** | JIT-compiled native code | JVM |

### Heap Generations

```
Heap Memory
+-------------------+-------------------+
|    Young Gen      |     Old Gen       |
| +-----+--------+ |                   |
| | Eden | S0 |S1| |   (Tenured)       |
| +-----+--------+ |                   |
+-------------------+-------------------+
```

- **Eden:** New objects created here
- **Survivor (S0/S1):** Objects that survived minor GC
- **Old Gen:** Long-lived objects promoted from Young Gen

---

## Garbage Collection Basics

### How GC Works

1. **Mark:** Identify reachable objects (from GC roots)
2. **Sweep:** Remove unreachable objects
3. **Compact:** Defragment memory (optional)

### Common GC Algorithms

| Algorithm | Flag | Best For |
|-----------|------|----------|
| Serial GC | `-XX:+UseSerialGC` | Small apps, single CPU |
| Parallel GC | `-XX:+UseParallelGC` | Throughput-focused |
| G1 GC | `-XX:+UseG1GC` | Balanced (default Java 9+) |
| ZGC | `-XX:+UseZGC` | Ultra-low latency |

### JVM Memory Flags

```bash
# Set heap sizes
java -Xms512m -Xmx2g -jar order-service.jar

# -Xms: Initial heap size
# -Xmx: Maximum heap size
# Rule of thumb: Set -Xms = -Xmx to avoid resize overhead
```

---

## Common Memory Issues in Sustain Work

### Memory Leak Patterns

```java
// 1. Static collections that grow forever
public class EventLog {
    private static List<Event> events = new ArrayList<>();  // Never cleared!
    public static void log(Event e) { events.add(e); }
}

// 2. Unclosed resources
public void readFile(String path) {
    FileInputStream fis = new FileInputStream(path);  // Never closed!
    // ...
}

// 3. Listener/callback not deregistered
button.addActionListener(this);  // Holds reference to 'this' forever
```

### Detection

```bash
# Generate heap dump when OOM occurs
java -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/heapdump.hprof -jar app.jar

# Monitor GC activity
java -verbose:gc -jar app.jar
```

---

## Performance Tuning Checklist

| Area | Check | Tool |
|------|-------|------|
| Slow queries | Enable slow query log | MySQL slow log |
| Memory usage | Monitor heap utilization | JVisualVM, JConsole |
| Thread contention | Check for deadlocks | `jstack <pid>` |
| CPU hotspots | Profile method execution time | JFR, async-profiler |
| GC pauses | Monitor GC frequency and duration | GC logs |

### Quick JVM Diagnostic Commands

```bash
# List running Java processes
jps -l

# Thread dump (find deadlocks, blocked threads)
jstack <pid>

# Heap summary
jmap -heap <pid>

# GC statistics
jstat -gcutil <pid> 1000 10   # Every 1s, 10 samples
```

---

## Logging with java.util.logging and SLF4J

### java.util.logging (built-in)

```java
import java.util.logging.Logger;
import java.util.logging.Level;

public class OrderService {
    private static final Logger logger = Logger.getLogger(OrderService.class.getName());

    public void placeOrder(Order order) {
        logger.info("Placing order: " + order.getId());
        try {
            // process order
            logger.fine("Order processed successfully");  // DEBUG level
        } catch (Exception e) {
            logger.log(Level.SEVERE, "Failed to place order", e);
        }
    }
}
```

### Log Levels

| Level | When to Use |
|-------|------------|
| `SEVERE` | System errors, unrecoverable failures |
| `WARNING` | Potential problems, degraded behavior |
| `INFO` | Key business events, startup/shutdown |
| `FINE` | Debug details (development/troubleshooting) |
| `FINER/FINEST` | Very detailed tracing |

---

## SLF4J + Logback (Industry Standard)

```xml
<!-- pom.xml -->
<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-api</artifactId>
    <version>2.0.9</version>
</dependency>
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.4.11</version>
</dependency>
```

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OrderService {
    private static final Logger log = LoggerFactory.getLogger(OrderService.class);

    public void placeOrder(Order order) {
        log.info("Placing order id={} for customer={}", order.getId(), order.getCustomerId());
        // Parameterized logging -- no string concatenation overhead if level disabled
    }
}
```

> **Why SLF4J?** Facade pattern -- switch logging backends (Logback, Log4j2) without changing code.

---

## Debugging Techniques

### IDE Debugging (IntelliJ / Eclipse)

| Feature | Shortcut (IntelliJ) | Purpose |
|---------|---------------------|---------|
| Set breakpoint | Click gutter / Ctrl+F8 | Pause execution |
| Step Over | F8 | Execute current line |
| Step Into | F7 | Enter method call |
| Step Out | Shift+F8 | Exit current method |
| Evaluate Expression | Alt+F8 | Inspect values |
| Conditional Breakpoint | Right-click breakpoint | Break only when condition true |

### Remote Debugging

```bash
# Start JVM with debug agent
java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 -jar app.jar

# Then attach IDE debugger to localhost:5005
```

> **Sustain scenario:** Use remote debugging to troubleshoot issues in staging/test environments.

---

## Deployment Basics

### Building a Deployable JAR

```bash
# Standard JAR
mvn clean package
# Output: target/order-service-1.0.0.jar

# Fat JAR (all dependencies included)
# Add maven-shade-plugin or spring-boot-maven-plugin
mvn clean package
java -jar target/order-service-1.0.0.jar
```

### Environment Configuration

```java
// Read from environment variables (12-factor app)
String dbUrl = System.getenv("DATABASE_URL");
String dbUser = System.getenv("DATABASE_USER");

// Or from properties file
Properties props = new Properties();
props.load(new FileInputStream("config.properties"));
String dbUrl = props.getProperty("db.url");
```

### Deployment Checklist

| Step | Action |
|------|--------|
| 1 | Run all tests: `mvn test` |
| 2 | Build artifact: `mvn clean package` |
| 3 | Verify config for target environment |
| 4 | Deploy JAR to server |
| 5 | Check application logs for startup errors |
| 6 | Run smoke tests against deployed app |

---

## Collections Utility Methods

```java
import java.util.Collections;

List<MenuItem> menu = new ArrayList<>(/* ... */);

// Sort
Collections.sort(menu, Comparator.comparing(MenuItem::getPrice));

// Reverse
Collections.reverse(menu);

// Shuffle (random order)
Collections.shuffle(menu);

// Unmodifiable (defensive programming)
List<MenuItem> readOnly = Collections.unmodifiableList(menu);
// readOnly.add(item);  // UnsupportedOperationException!

// Immutable (Java 9+)
List<String> categories = List.of("Italian", "Chinese", "Indian");
Map<String, Double> fixed = Map.of("Tax", 0.08, "Tip", 0.15);
Set<String> statuses = Set.of("PENDING", "CONFIRMED", "DELIVERED");
```

---

## Common Collection Patterns in Sustain Code

### Frequency Count

```java
Map<String, Integer> orderCounts = new HashMap<>();
for (Order order : allOrders) {
    orderCounts.merge(order.getCategory(), 1, Integer::sum);
}
```

### Grouping

```java
Map<String, List<MenuItem>> byCategory = new HashMap<>();
for (MenuItem item : menu) {
    byCategory.computeIfAbsent(item.getCategory(), k -> new ArrayList<>()).add(item);
}
```

### Top-N Pattern

```java
List<MenuItem> topExpensive = menu.stream()
    .sorted(Comparator.comparing(MenuItem::getPrice).reversed())
    .limit(5)
    .collect(Collectors.toList());
```

---

## Lab: FoodExpress Order Service Collections

### Objective

Build a complete `OrderService` class using Java Collections and JDBC.

### Tasks

1. **Menu Catalog (Map):** Store `MenuItem` objects in a `HashMap<String, MenuItem>` keyed by item ID
2. **Order Cart (List):** Maintain an `ArrayList<OrderItem>` for the shopping cart
3. **Unique Categories (Set):** Extract unique cuisine categories using `HashSet`
4. **Iterator Cleanup:** Remove out-of-stock items using `Iterator.remove()`
5. **JDBC Integration:** Save completed orders to a MySQL database using `PreparedStatement`

### Acceptance Criteria

- All CRUD operations work correctly
- No `ConcurrentModificationException`
- SQL injection is prevented (PreparedStatement only)
- Resources are closed properly (try-with-resources)
- Proper logging with SLF4J

---

## Lab: Debugging Exercise

### Scenario

The FoodExpress OrderService has 5 bugs reported in production. Find and fix them.

### Bug List

| # | Symptom | Hint |
|---|---------|------|
| 1 | `NullPointerException` on checkout | Check autoboxing with Map.get() |
| 2 | Duplicate menu items in catalog | Check equals/hashCode in MenuItem |
| 3 | `ConcurrentModificationException` | Look at the for-each loop removing items |
| 4 | Slow order history query | Check if PreparedStatement is used |
| 5 | Database connection leak | Look for missing close/try-with-resources |

### Tools to Use

- IDE debugger with breakpoints
- `jstack` for thread analysis
- GC logs for memory issues

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Collections | Framework of interfaces (List, Set, Map) and implementations |
| Generics | Type safety at compile time; avoid raw types |
| ArrayList | Default List choice; O(1) access, O(n) insert/remove |
| HashSet | No duplicates; requires proper equals/hashCode |
| HashMap | Key-value pairs; O(1) average lookup |
| Maven | Build tool; POM.xml manages dependencies and lifecycle |
| Iterator | Safe removal during iteration; avoids ConcurrentModificationException |
| Autoboxing | Automatic primitive-wrapper conversion; watch for NPE and perf |
| JDBC | Standard DB access; always use PreparedStatement |
| Memory Mgmt | Heap generations, GC algorithms, JVM flags |
| Logging | Use SLF4J; parameterized messages; proper log levels |
| Debugging | IDE breakpoints, remote debug, jstack, jmap |

> **Next: Module 08 -- Capsule Project: Java (full-day hands-on project)**
