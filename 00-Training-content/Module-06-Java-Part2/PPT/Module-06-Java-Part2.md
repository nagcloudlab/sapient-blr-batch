# Java Programming (Part 2)
## Module 06 | Sustain Engineering Training | Day 7

**1 day | Workshop + guided lab**

---

## By the end of this session

You can handle exceptions properly, design with interfaces and abstract classes, and read/write files using Java I/O streams.

| Pillar | What you will do |
|--------|-----------------|
| **Exceptions** | Checked vs unchecked, throw, throws, custom exceptions |
| **Exception Hierarchy** | Throwable, Error, Exception, RuntimeException |
| **try/catch/finally** | Catch specific exceptions, multi-catch, try-with-resources |
| **Interfaces** | Define contracts, implement multiple interfaces |
| **Abstract Classes** | Partial implementation, template method pattern |
| **Implementation Dependencies** | Coupling, coding to interfaces, dependency injection |
| **I/O Streams** | InputStream, OutputStream, byte-level I/O |
| **Readers & Writers** | Character-level I/O, BufferedReader, PrintWriter |
| **Filter Streams** | BufferedInputStream, DataInputStream, ObjectInputStream |

---

## Session agenda

| # | Topic |
|---|-------|
| 01 | Exception fundamentals |
| 02 | Exception hierarchy |
| 03 | try/catch/finally and multi-catch |
| 04 | Custom exceptions and best practices |
| 05 | try-with-resources |
| 06 | Interfaces |
| 07 | Abstract classes |
| 08 | Coding to interfaces and loose coupling |
| 09 | I/O streams: byte streams |
| 10 | Readers and writers: character streams |
| 11 | Filter streams and buffering |
| 12 | Guided lab |

---

## What is an exception?

An exception is an event that disrupts the normal flow of a program.

```java
// This code crashes at runtime
String input = "abc";
int quantity = Integer.parseInt(input);  // NumberFormatException!

// Without handling, the program terminates
// Stack trace printed to console:
// Exception in thread "main" java.lang.NumberFormatException:
//     For input string: "abc"
//     at java.lang.Integer.parseInt(Integer.java:652)
//     at OrderService.processInput(OrderService.java:42)
//     at Main.main(Main.java:15)
```

### Common exceptions in sustain engineering

| Exception | Cause | Example |
|-----------|-------|---------|
| `NullPointerException` | Calling method on null | `order.getCustomer().getName()` |
| `NumberFormatException` | Invalid string to number | `Integer.parseInt("abc")` |
| `ArrayIndexOutOfBoundsException` | Index >= array length | `items[10]` when length is 5 |
| `FileNotFoundException` | File does not exist | `new FileReader("missing.txt")` |
| `IOException` | I/O operation failed | Network timeout, disk full |
| `ClassCastException` | Invalid type cast | `(String) integerObject` |

---

## Exception hierarchy

```
                    Throwable
                    /       \
                Error      Exception
                /             /     \
    OutOfMemoryError   IOException  RuntimeException
    StackOverflowError FileNotFound     /    |     \
                       SQLException  NPE  IOOBE  NFE
```

| Type | Checked? | Must handle? | Examples |
|------|----------|-------------|---------|
| **Error** | No | No (unrecoverable) | `OutOfMemoryError`, `StackOverflowError` |
| **Checked Exception** | Yes | Yes (compile error if not) | `IOException`, `SQLException`, `FileNotFoundException` |
| **Unchecked Exception** | No | No (but should handle) | `NullPointerException`, `IllegalArgumentException` |

### The rule

- **Checked exceptions** extend `Exception` (but not `RuntimeException`)
- **Unchecked exceptions** extend `RuntimeException`
- **Errors** extend `Error` -- do NOT catch these

> Checked exceptions force the caller to handle them. Unchecked exceptions indicate programming bugs.

---

## try / catch / finally

```java
// Basic try/catch
try {
    String input = getInput();
    int quantity = Integer.parseInt(input);
    processOrder(quantity);
} catch (NumberFormatException e) {
    System.err.println("Invalid quantity: " + e.getMessage());
}

// Multiple catch blocks (most specific first)
try {
    MenuItem item = loadMenuItem(id);
    Order order = createOrder(item, quantity);
    saveOrder(order);
} catch (FileNotFoundException e) {
    System.err.println("Menu file not found: " + e.getMessage());
} catch (IOException e) {
    System.err.println("I/O error: " + e.getMessage());
} catch (Exception e) {
    System.err.println("Unexpected error: " + e.getMessage());
}

// finally: always runs (cleanup)
FileReader reader = null;
try {
    reader = new FileReader("menu.json");
    // process file
} catch (IOException e) {
    System.err.println("Error reading file");
} finally {
    if (reader != null) {
        try { reader.close(); } catch (IOException e) { }
    }
}
```

---

## Multi-catch and re-throw

```java
// Multi-catch (Java 7+): handle multiple exceptions the same way
try {
    MenuItem item = findMenuItem(name);
    Order order = createOrder(item, quantity);
} catch (NumberFormatException | IllegalArgumentException e) {
    // Same handling for both
    System.err.println("Invalid input: " + e.getMessage());
} catch (IOException e) {
    System.err.println("I/O error: " + e.getMessage());
}

// Re-throw: catch, log, and re-throw
public Order processOrder(String input) throws OrderException {
    try {
        // ... processing logic ...
        return createOrder(input);
    } catch (NumberFormatException e) {
        // Log the technical details
        logger.error("Invalid order input", e);
        // Throw a business-level exception
        throw new OrderException("Invalid order data", e);
    }
}

// Chained exceptions: preserve the original cause
catch (SQLException e) {
    throw new OrderException("Failed to save order", e);
    // e is the "cause" -- accessible via getCause()
}
```

---

## The throws keyword

```java
// Declaring that a method may throw a checked exception
public MenuItem loadFromFile(String filename) throws IOException {
    FileReader reader = new FileReader(filename);  // may throw
    // ... read and parse ...
    return menuItem;
}

// Caller MUST handle or propagate
// Option 1: Handle it
try {
    MenuItem item = loadFromFile("menu.json");
} catch (IOException e) {
    System.err.println("Cannot load menu");
}

// Option 2: Propagate it (add throws to calling method)
public void initializeMenu() throws IOException {
    MenuItem item = loadFromFile("menu.json");
}
```

| Keyword | Purpose | Where |
|---------|---------|-------|
| `throw` | Actually throw an exception | Inside method body |
| `throws` | Declare that method MAY throw | In method signature |
| `try` | Start a protected block | Before risky code |
| `catch` | Handle a specific exception | After `try` block |
| `finally` | Always execute (cleanup) | After `catch` blocks |

---

## Custom exceptions

```java
// Custom checked exception
public class OrderNotFoundException extends Exception {
    private final String orderId;

    public OrderNotFoundException(String orderId) {
        super("Order not found: " + orderId);
        this.orderId = orderId;
    }

    public String getOrderId() {
        return orderId;
    }
}

// Custom unchecked exception
public class InvalidMenuItemException extends RuntimeException {
    private final String field;

    public InvalidMenuItemException(String field, String message) {
        super(message);
        this.field = field;
    }

    public String getField() {
        return field;
    }
}
```

```java
// Using custom exceptions
public Order findOrder(String id) throws OrderNotFoundException {
    Order order = orderRepository.findById(id);
    if (order == null) {
        throw new OrderNotFoundException(id);
    }
    return order;
}
```

---

## When to use checked vs unchecked

| Scenario | Type | Example |
|----------|------|---------|
| Caller can recover | Checked | `OrderNotFoundException` -- show "not found" page |
| Programming bug | Unchecked | `InvalidMenuItemException` -- should be caught in tests |
| External system failure | Checked | `PaymentServiceException` -- retry or fallback |
| Invalid argument | Unchecked | `IllegalArgumentException` -- fix the calling code |
| Resource not found | Checked | `FileNotFoundException` -- prompt user for correct path |
| Null where not expected | Unchecked | `NullPointerException` -- add null check |

### Best practices

```java
// DO: Catch specific exceptions
catch (FileNotFoundException e) { ... }

// DON'T: Catch generic Exception unless necessary
catch (Exception e) { ... }  // too broad

// DO: Include context in messages
throw new OrderException("Failed to process order " + orderId, e);

// DON'T: Swallow exceptions silently
catch (Exception e) { }  // NEVER do this

// DO: Log the exception
catch (Exception e) {
    logger.error("Order processing failed for " + orderId, e);
    throw e;  // or throw a new exception with cause
}
```

---

## try-with-resources (Java 7+)

```java
// OLD way: manual close in finally
FileReader reader = null;
try {
    reader = new FileReader("orders.csv");
    BufferedReader br = new BufferedReader(reader);
    String line;
    while ((line = br.readLine()) != null) {
        processLine(line);
    }
} catch (IOException e) {
    System.err.println("Error: " + e.getMessage());
} finally {
    if (reader != null) {
        try { reader.close(); } catch (IOException e) { }
    }
}

// NEW way: try-with-resources (auto-close)
try (FileReader reader = new FileReader("orders.csv");
     BufferedReader br = new BufferedReader(reader)) {

    String line;
    while ((line = br.readLine()) != null) {
        processLine(line);
    }

} catch (IOException e) {
    System.err.println("Error: " + e.getMessage());
}
// reader and br are automatically closed!
```

> Any class that implements `AutoCloseable` can be used in try-with-resources. This includes all I/O streams, database connections, and network sockets.

---

## Interfaces: defining contracts

```java
// Interface: defines WHAT, not HOW
public interface Payable {
    double calculateTotal();
    String getPaymentSummary();

    // Default method (Java 8+): provides optional implementation
    default String formatCurrency(double amount) {
        return String.format("$%.2f", amount);
    }

    // Static method (Java 8+)
    static double addTax(double amount, double rate) {
        return amount * (1 + rate);
    }

    // Constant (implicitly public static final)
    double TAX_RATE = 0.08;
}
```

```java
// Implementation
public class Order implements Payable {
    private List<OrderItem> items;

    @Override
    public double calculateTotal() {
        double subtotal = items.stream()
            .mapToDouble(OrderItem::getSubtotal)
            .sum();
        return Payable.addTax(subtotal, TAX_RATE);
    }

    @Override
    public String getPaymentSummary() {
        return "Order total: " + formatCurrency(calculateTotal());
    }
}
```

---

## Interface rules and features

| Feature | Interface | Notes |
|---------|-----------|-------|
| Fields | `public static final` only | Constants, implicitly |
| Abstract methods | `public abstract` | Implicitly, no body |
| Default methods | `default` keyword (Java 8+) | Has body, can be overridden |
| Static methods | `static` keyword (Java 8+) | Called on interface, not instance |
| Private methods | Java 9+ | Helper methods for defaults |
| Constructors | NOT allowed | Cannot instantiate an interface |
| Multiple inheritance | YES | A class can implement many interfaces |

```java
// Multiple interface implementation
public class DeliveryOrder implements Payable, Trackable, Cancellable {
    @Override
    public double calculateTotal() { /* ... */ }

    @Override
    public String getPaymentSummary() { /* ... */ }

    @Override
    public String getTrackingStatus() { /* ... */ }

    @Override
    public boolean cancel() { /* ... */ }
}
```

> Interfaces support multiple inheritance. Classes do not (single inheritance only). This is a key design advantage.

---

## FoodExpress interface examples

```java
// Trackable: anything with a status
public interface Trackable {
    String getStatus();
    void updateStatus(String newStatus);
    long getLastUpdated();
}

// Cancellable: anything that can be cancelled
public interface Cancellable {
    boolean cancel();
    boolean isCancellable();
}

// Priceable: anything with a price
public interface Priceable {
    double getPrice();
    double getDiscountedPrice(double discountRate);

    default String getFormattedPrice() {
        return String.format("$%.2f", getPrice());
    }
}
```

```java
// MenuItem implements Priceable
public class MenuItem implements Priceable {
    private String name;
    private double price;

    @Override
    public double getPrice() { return price; }

    @Override
    public double getDiscountedPrice(double rate) {
        return price * (1 - rate);
    }
}
```

---

## Abstract classes: partial implementation

```java
// Abstract class: cannot be instantiated
public abstract class AbstractOrder {
    // Concrete fields
    protected String orderId;
    protected String customerName;
    protected double subtotal;
    private long createdAt;

    // Constructor (called by subclasses)
    public AbstractOrder(String orderId, String customerName) {
        this.orderId = orderId;
        this.customerName = customerName;
        this.createdAt = System.currentTimeMillis();
    }

    // Abstract method: subclass MUST implement
    public abstract double calculateDeliveryFee();

    // Abstract method
    public abstract String getOrderType();

    // Concrete method: shared by all subclasses
    public double getTotal() {
        return subtotal + calculateDeliveryFee();
    }

    // Concrete method
    public String getSummary() {
        return getOrderType() + " order " + orderId
            + " for " + customerName
            + " - Total: $" + String.format("%.2f", getTotal());
    }
}
```

---

## Extending abstract classes

```java
public class DeliveryOrder extends AbstractOrder {
    private String deliveryAddress;
    private double distance;

    public DeliveryOrder(String id, String customer, String address, double distance) {
        super(id, customer);  // call parent constructor
        this.deliveryAddress = address;
        this.distance = distance;
    }

    @Override
    public double calculateDeliveryFee() {
        return distance > 5.0 ? 4.99 : 2.99;
    }

    @Override
    public String getOrderType() {
        return "Delivery";
    }
}

public class PickupOrder extends AbstractOrder {
    public PickupOrder(String id, String customer) {
        super(id, customer);
    }

    @Override
    public double calculateDeliveryFee() {
        return 0.0;  // no delivery fee for pickup
    }

    @Override
    public String getOrderType() {
        return "Pickup";
    }
}
```

---

## Abstract class vs interface

| Feature | Abstract class | Interface |
|---------|---------------|-----------|
| Instantiate? | No | No |
| Constructors? | Yes | No |
| Fields? | Any (instance, static) | `public static final` only |
| Methods? | Abstract + concrete | Abstract + default + static |
| Inheritance | Single (`extends` one) | Multiple (`implements` many) |
| Access modifiers | Any | `public` (methods implicitly) |
| When to use | Common base with shared state | Contract / capability definition |

### Decision guide

```
Need shared state (fields)?
  YES -> Abstract class
  NO  -> Interface

Need multiple inheritance?
  YES -> Interface
  NO  -> Either works

Is it "is-a" relationship?
  YES -> Abstract class (DeliveryOrder IS-A Order)
  NO  -> Interface (Order IS Payable, IS Trackable)

Need constructor logic?
  YES -> Abstract class
  NO  -> Interface
```

---

## Coding to interfaces (loose coupling)

```java
// TIGHT coupling: depends on concrete class
public class OrderProcessor {
    private MySQLOrderRepository repository;  // locked to MySQL

    public OrderProcessor() {
        this.repository = new MySQLOrderRepository();
    }
}

// LOOSE coupling: depends on interface
public class OrderProcessor {
    private OrderRepository repository;  // any implementation

    public OrderProcessor(OrderRepository repository) {
        this.repository = repository;  // injected
    }

    public void process(Order order) {
        // Works with MySQL, PostgreSQL, MongoDB, InMemory...
        repository.save(order);
    }
}
```

```java
// Interface
public interface OrderRepository {
    void save(Order order);
    Order findById(String id);
    List<Order> findAll();
}

// Implementations
public class MySQLOrderRepository implements OrderRepository { /* ... */ }
public class MongoOrderRepository implements OrderRepository { /* ... */ }
public class InMemoryOrderRepository implements OrderRepository { /* ... */ }
```

---

## Dependency injection pattern

```java
// Production: use MySQL
OrderRepository repo = new MySQLOrderRepository(connectionString);
OrderProcessor processor = new OrderProcessor(repo);

// Testing: use in-memory
OrderRepository testRepo = new InMemoryOrderRepository();
OrderProcessor testProcessor = new OrderProcessor(testRepo);

// Spring Boot does this automatically
@Service
public class OrderProcessor {
    private final OrderRepository repository;

    @Autowired  // Spring injects the implementation
    public OrderProcessor(OrderRepository repository) {
        this.repository = repository;
    }
}
```

| Principle | Description |
|-----------|------------|
| **Program to interfaces** | Declare variables as interface types, not concrete |
| **Dependency injection** | Pass dependencies in, don't create them inside |
| **Single responsibility** | Each class does one thing |
| **Open/closed** | Open for extension (new implementations), closed for modification |

> In sustain engineering, you often swap implementations (database, cache, API client) without changing business logic. Interfaces make this possible.

---

## Polymorphism in action

```java
// Process any type of order through a single method
public class OrderService {
    public void processOrder(AbstractOrder order) {
        System.out.println(order.getSummary());
        System.out.println("Delivery fee: $"
            + String.format("%.2f", order.calculateDeliveryFee()));
    }
}

// Usage
OrderService service = new OrderService();

AbstractOrder delivery = new DeliveryOrder("FE-1001", "Alice", "123 Main St", 3.5);
delivery.subtotal = 24.97;

AbstractOrder pickup = new PickupOrder("FE-1002", "Bob");
pickup.subtotal = 18.50;

service.processOrder(delivery);
// Delivery order FE-1001 for Alice - Total: $27.96
// Delivery fee: $2.99

service.processOrder(pickup);
// Pickup order FE-1002 for Bob - Total: $18.50
// Delivery fee: $0.00
```

> Same method call (`calculateDeliveryFee`) produces different results based on the actual object type. This is polymorphism.

---

## I/O streams overview

```
Java I/O Stream Hierarchy

Byte Streams (binary data)          Character Streams (text)
+-----------------+                 +-----------------+
| InputStream     |                 | Reader          |
|   FileInput...  |                 |   FileReader    |
|   BufferedInput..|                |   BufferedReader|
|   DataInput...  |                 |   InputStreamR. |
+-----------------+                 +-----------------+
| OutputStream    |                 | Writer          |
|   FileOutput... |                 |   FileWriter    |
|   BufferedOutput.|                |   BufferedWriter|
|   DataOutput... |                 |   PrintWriter   |
+-----------------+                 +-----------------+
```

| Stream type | Unit | Use for |
|-------------|------|---------|
| **Byte streams** | `byte` (8-bit) | Binary files: images, PDFs, serialized objects |
| **Character streams** | `char` (16-bit) | Text files: CSV, JSON, logs, config |

> Use character streams for text files. Use byte streams for binary files. Using the wrong type corrupts data.

---

## Byte streams: FileInputStream / FileOutputStream

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

// Reading bytes from a file
try (FileInputStream fis = new FileInputStream("logo.png")) {
    int byteData;
    while ((byteData = fis.read()) != -1) {
        // process each byte
    }
} catch (IOException e) {
    System.err.println("Error reading file: " + e.getMessage());
}

// Writing bytes to a file
try (FileOutputStream fos = new FileOutputStream("copy.png")) {
    fos.write(byteArray);
} catch (IOException e) {
    System.err.println("Error writing file: " + e.getMessage());
}

// Copy a file byte by byte
try (FileInputStream in = new FileInputStream("source.dat");
     FileOutputStream out = new FileOutputStream("dest.dat")) {

    int b;
    while ((b = in.read()) != -1) {
        out.write(b);
    }
} catch (IOException e) {
    System.err.println("Copy failed: " + e.getMessage());
}
```

---

## Reading with a buffer (efficient)

```java
// Reading byte by byte: SLOW (one system call per byte)
while ((b = fis.read()) != -1) { ... }

// Reading with buffer: FAST (one system call per chunk)
byte[] buffer = new byte[8192];  // 8 KB buffer
int bytesRead;
while ((bytesRead = fis.read(buffer)) != -1) {
    out.write(buffer, 0, bytesRead);
}
```

| Approach | System calls for 1 MB file | Speed |
|----------|---------------------------|-------|
| Byte-by-byte | ~1,000,000 | Very slow |
| 1 KB buffer | ~1,024 | Fast |
| 8 KB buffer | ~128 | Very fast |
| 64 KB buffer | ~16 | Fastest (diminishing returns) |

```java
// Complete efficient file copy
public static void copyFile(String src, String dest) throws IOException {
    try (FileInputStream in = new FileInputStream(src);
         FileOutputStream out = new FileOutputStream(dest)) {

        byte[] buffer = new byte[8192];
        int bytesRead;
        while ((bytesRead = in.read(buffer)) != -1) {
            out.write(buffer, 0, bytesRead);
        }
    }
}
```

> Always use a buffer when reading/writing files. Byte-by-byte I/O is orders of magnitude slower.

---

## Character streams: FileReader / FileWriter

```java
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

// Reading characters from a text file
try (FileReader reader = new FileReader("menu.txt")) {
    int ch;
    while ((ch = reader.read()) != -1) {
        System.out.print((char) ch);
    }
} catch (IOException e) {
    System.err.println("Error: " + e.getMessage());
}

// Writing text to a file
try (FileWriter writer = new FileWriter("output.txt")) {
    writer.write("FoodExpress Order Report\n");
    writer.write("========================\n");
    writer.write("Order ID: FE-1001\n");
    writer.write("Total: $24.97\n");
}

// Append mode (don't overwrite)
try (FileWriter writer = new FileWriter("log.txt", true)) {
    writer.write("2026-07-27 10:30:00 Order placed FE-1001\n");
}
```

| Parameter | `new FileWriter("file.txt")` | `new FileWriter("file.txt", true)` |
|-----------|------------------------------|--------------------------------------|
| Mode | Overwrite | Append |
| Existing content | Deleted | Preserved |

---

## BufferedReader and BufferedWriter

```java
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;

// BufferedReader: read line by line
try (BufferedReader br = new BufferedReader(new FileReader("orders.csv"))) {
    String line;
    int lineNumber = 0;
    while ((line = br.readLine()) != null) {
        lineNumber++;
        String[] fields = line.split(",");
        System.out.printf("Line %d: Order %s, Total $%s%n",
            lineNumber, fields[0], fields[2]);
    }
}

// BufferedWriter: write with buffering
try (BufferedWriter bw = new BufferedWriter(new FileWriter("report.txt"))) {
    bw.write("FoodExpress Daily Report");
    bw.newLine();  // platform-independent line separator
    bw.write("========================");
    bw.newLine();

    for (Order order : orders) {
        bw.write(order.getSummary());
        bw.newLine();
    }
}
```

> `BufferedReader.readLine()` is the most common way to read text files in Java. It reads one line at a time and returns `null` at end of file.

---

## PrintWriter: convenient text output

```java
import java.io.PrintWriter;
import java.io.FileWriter;

// PrintWriter: printf-style formatting
try (PrintWriter pw = new PrintWriter(new FileWriter("report.csv"))) {
    // Header
    pw.println("OrderID,Customer,Total,Status");

    // Data rows
    for (Order order : orders) {
        pw.printf("%s,%s,%.2f,%s%n",
            order.getOrderId(),
            order.getCustomerName(),
            order.getTotal(),
            order.getStatus());
    }

    pw.flush();  // ensure all data is written
}

// PrintWriter to System.out
PrintWriter console = new PrintWriter(System.out, true);
console.printf("Processing order %s for %s%n", orderId, customer);
```

| Method | Description |
|--------|-------------|
| `print(x)` | Write without newline |
| `println(x)` | Write with newline |
| `printf(format, args)` | Formatted output (like C) |
| `flush()` | Force write buffered data |
| `close()` | Flush and close |

---

## InputStreamReader: bridging byte and character streams

```java
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.nio.charset.StandardCharsets;

// Read from System.in (keyboard input)
try (BufferedReader br = new BufferedReader(
        new InputStreamReader(System.in))) {

    System.out.print("Enter order ID: ");
    String orderId = br.readLine();
    System.out.println("Looking up: " + orderId);
}

// Read a file with specific encoding
try (BufferedReader br = new BufferedReader(
        new InputStreamReader(
            new FileInputStream("menu.txt"),
            StandardCharsets.UTF_8))) {

    String line;
    while ((line = br.readLine()) != null) {
        System.out.println(line);
    }
}
```

```
Byte Stream  -->  InputStreamReader  -->  Reader
(bytes)           (bridge: bytes->chars)  (characters)

Writer       -->  OutputStreamWriter -->  Byte Stream
(characters)      (bridge: chars->bytes)  (bytes)
```

> Always specify the encoding (`UTF-8`) when reading/writing text across systems. Default encoding varies by OS.

---

## Filter streams: DataInputStream / DataOutputStream

```java
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;

// Write primitive types to a binary file
try (DataOutputStream dos = new DataOutputStream(
        new FileOutputStream("order.dat"))) {

    dos.writeUTF("FE-1001");      // String (with length prefix)
    dos.writeDouble(24.97);        // 8 bytes
    dos.writeInt(3);               // 4 bytes
    dos.writeBoolean(true);        // 1 byte
    dos.writeLong(System.currentTimeMillis());  // 8 bytes
}

// Read primitive types from a binary file
try (DataInputStream dis = new DataInputStream(
        new FileInputStream("order.dat"))) {

    String orderId = dis.readUTF();
    double total = dis.readDouble();
    int itemCount = dis.readInt();
    boolean isPaid = dis.readBoolean();
    long timestamp = dis.readLong();

    System.out.printf("Order %s: $%.2f (%d items, paid=%b)%n",
        orderId, total, itemCount, isPaid);
}
```

> Read in the SAME ORDER as written. `DataInputStream`/`DataOutputStream` do not store field names -- only raw values in sequence.

---

## BufferedInputStream / BufferedOutputStream

```java
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;

// Stack streams for efficient binary I/O
try (BufferedInputStream bis = new BufferedInputStream(
         new FileInputStream("large-file.dat"), 16384);
     BufferedOutputStream bos = new BufferedOutputStream(
         new FileOutputStream("copy.dat"), 16384)) {

    byte[] buffer = new byte[8192];
    int bytesRead;
    while ((bytesRead = bis.read(buffer)) != -1) {
        bos.write(buffer, 0, bytesRead);
    }
}
```

### Stream decorator pattern

```
FileInputStream        (raw bytes from file)
  |
  v
BufferedInputStream    (adds buffering)
  |
  v
DataInputStream        (adds readInt, readDouble, etc.)
```

> Streams are composed using the decorator pattern. Wrap a stream to add capability without changing the base stream.

---

## Java NIO: modern file operations (Java 7+)

```java
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

// Read entire file as a string
String content = Files.readString(Path.of("menu.json"));

// Read all lines into a list
List<String> lines = Files.readAllLines(Path.of("orders.csv"));

// Write a string to a file
Files.writeString(Path.of("output.txt"), "Hello FoodExpress");

// Write lines to a file
List<String> reportLines = List.of("Header", "Line 1", "Line 2");
Files.write(Path.of("report.txt"), reportLines);

// Check file properties
Path path = Path.of("menu.json");
Files.exists(path);           // true/false
Files.size(path);             // file size in bytes
Files.isReadable(path);       // true/false
Files.getLastModifiedTime(path);

// Copy and move
Files.copy(Path.of("src.txt"), Path.of("dest.txt"));
Files.move(Path.of("old.txt"), Path.of("new.txt"));
Files.delete(Path.of("temp.txt"));
```

> For simple file operations, prefer `java.nio.file.Files` over the stream-based API. It is more concise and handles encoding properly.

---

## Reading CSV: FoodExpress menu example

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class MenuLoader {
    public static List<MenuItem> loadMenu(String filename) throws IOException {
        List<MenuItem> items = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String header = br.readLine();  // skip header row
            String line;

            while ((line = br.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length < 3) continue;  // skip malformed lines

                String name = parts[0].trim();
                double price = Double.parseDouble(parts[1].trim());
                String category = parts[2].trim();

                items.add(new MenuItem(name, price, category));
            }
        }

        return items;
    }
}
```

```
// menu.csv
Name,Price,Category
Smash Burger,8.99,Mains
Loaded Fries,4.99,Sides
Chocolate Shake,5.99,Drinks
Caesar Salad,7.49,Starters
```

---

## Writing reports: FoodExpress order summary

```java
import java.io.PrintWriter;
import java.io.FileWriter;
import java.io.IOException;

public class ReportGenerator {
    public static void generateOrderReport(List<Order> orders, String filename)
            throws IOException {

        try (PrintWriter pw = new PrintWriter(new FileWriter(filename))) {
            pw.println("=== FoodExpress Order Report ===");
            pw.printf("Generated: %s%n%n", java.time.LocalDateTime.now());

            pw.printf("%-12s %-15s %10s %10s %-12s%n",
                "Order ID", "Customer", "Subtotal", "Total", "Status");
            pw.println("-".repeat(65));

            double grandTotal = 0;
            for (Order order : orders) {
                pw.printf("%-12s %-15s %10.2f %10.2f %-12s%n",
                    order.getOrderId(),
                    order.getCustomerName(),
                    order.getSubtotal(),
                    order.getTotal(),
                    order.getStatus());
                grandTotal += order.getTotal();
            }

            pw.println("-".repeat(65));
            pw.printf("%-27s %10s %10.2f%n", "GRAND TOTAL", "", grandTotal);
            pw.printf("%nTotal orders: %d%n", orders.size());
        }
    }
}
```

---

## Object serialization (overview)

```java
import java.io.Serializable;
import java.io.ObjectOutputStream;
import java.io.ObjectInputStream;
import java.io.FileOutputStream;
import java.io.FileInputStream;

// Class must implement Serializable
public class MenuItem implements Serializable {
    private static final long serialVersionUID = 1L;

    private String name;
    private double price;
    private String category;
    private transient int viewCount;  // transient = NOT serialized
}

// Serialize (write object to file)
try (ObjectOutputStream oos = new ObjectOutputStream(
        new FileOutputStream("menuItem.ser"))) {
    oos.writeObject(burger);
}

// Deserialize (read object from file)
try (ObjectInputStream ois = new ObjectInputStream(
        new FileInputStream("menuItem.ser"))) {
    MenuItem loaded = (MenuItem) ois.readObject();
}
```

| Keyword | Meaning |
|---------|---------|
| `Serializable` | Marker interface -- enables serialization |
| `serialVersionUID` | Version control for serialized format |
| `transient` | Skip this field during serialization |

> In modern Java, prefer JSON serialization (Jackson, Gson) over `ObjectOutputStream`. Binary serialization has security risks and versioning issues.

---

## Exception handling in I/O: complete pattern

```java
public class OrderFileProcessor {

    public List<Order> readOrders(String filename) {
        List<Order> orders = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(
                new FileReader(filename))) {

            br.readLine();  // skip header
            String line;
            int lineNum = 1;

            while ((line = br.readLine()) != null) {
                lineNum++;
                try {
                    Order order = parseLine(line);
                    orders.add(order);
                } catch (NumberFormatException e) {
                    System.err.printf("Line %d: Invalid number - %s%n",
                        lineNum, e.getMessage());
                } catch (IllegalArgumentException e) {
                    System.err.printf("Line %d: Invalid data - %s%n",
                        lineNum, e.getMessage());
                }
            }

        } catch (FileNotFoundException e) {
            System.err.println("File not found: " + filename);
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }

        return orders;
    }
}
```

> Separate file-level errors (IOException) from line-level errors (NumberFormatException). Process as many valid lines as possible.

---

## Checkpoint: exception handling

What happens in each scenario?

```java
public void scenario1() {
    try {
        int result = 10 / 0;
    } catch (ArithmeticException e) {
        System.out.println("A");
    } finally {
        System.out.println("B");
    }
    System.out.println("C");
}

public void scenario2() throws IOException {
    try {
        throw new IOException("file error");
    } catch (FileNotFoundException e) {
        System.out.println("D");
    } finally {
        System.out.println("E");
    }
    System.out.println("F");
}
```

| Scenario | Output | Explanation |
|----------|--------|-------------|
| 1 | `A B C` | ArithmeticException caught, finally runs, continues |
| 2 | `E` then IOException propagates | IOException is NOT FileNotFoundException, not caught, finally runs, F skipped |

---

## Checkpoint: interfaces and abstract classes

Which should you use?

| Requirement | Answer | Why |
|------------|--------|-----|
| Multiple unrelated classes need a `save()` method | Interface | No shared state, just a contract |
| All orders share `orderId`, `createdAt`, `getSummary()` | Abstract class | Shared fields and implementation |
| A class needs to be both `Payable` and `Trackable` | Interface | Multiple interfaces, one abstract class |
| Want to enforce a template: validate -> process -> save | Abstract class | Template method pattern |
| Third-party classes need to integrate with your system | Interface | Cannot change their inheritance |

---

## Guided lab: FoodExpress order file processor

| Step | Task |
|------|------|
| 01 | Fix: `OrderNotFoundException` extends `RuntimeException` but should be checked (extend `Exception`) |
| 02 | Fix: Exception caught but silently swallowed (empty catch block) |
| 03 | Fix: `FileReader` not closed on exception (use try-with-resources) |
| 04 | Fix: `readLine()` result not checked for null (NullPointerException at end of file) |
| 05 | Fix: CSV parser crashes on malformed lines (missing try/catch for NumberFormatException) |
| 06 | Add: `Priceable` interface with `getPrice()` and `getFormattedPrice()` |
| 07 | Add: Abstract `AbstractOrder` class with shared fields and `calculateDeliveryFee()` |
| 08 | Add: Read `menu.csv`, create `MenuItem` objects, write `report.txt` using PrintWriter |

---

## Lab acceptance criteria

- [ ] `OrderNotFoundException` is a checked exception (extends `Exception`)
- [ ] No empty catch blocks -- all exceptions are logged or re-thrown
- [ ] All file I/O uses try-with-resources (no manual close)
- [ ] `readLine()` null check prevents NPE at end of file
- [ ] Malformed CSV lines are skipped with a warning (not crash)
- [ ] `Priceable` interface implemented by `MenuItem` and `OrderItem`
- [ ] `AbstractOrder` extended by `DeliveryOrder` and `PickupOrder`
- [ ] Report file generated with formatted output
- [ ] Code compiles without warnings
- [ ] Custom exceptions include meaningful messages and cause chaining

---

## Key takeaways

| Concept | Remember |
|---------|----------|
| Checked vs unchecked | Checked = must handle; unchecked = programming bug |
| try-with-resources | Always use for I/O. Ensures close even on exception |
| Custom exceptions | Include context (orderId, field name) in the exception |
| Never swallow | Empty `catch {}` is the worst pattern. Log or re-throw |
| Interfaces | Define contracts. Support multiple inheritance |
| Abstract classes | Share state + partial implementation. Single inheritance |
| Code to interfaces | Declare variables as interface types for loose coupling |
| Byte streams | `InputStream`/`OutputStream` for binary data |
| Character streams | `Reader`/`Writer` for text. Always specify encoding |
| Buffering | Always buffer I/O. `BufferedReader.readLine()` for text files |

> **Next: Module 07 -- Database Fundamentals: SQL, relational databases, CRUD operations**