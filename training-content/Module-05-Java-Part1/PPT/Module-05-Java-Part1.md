# Java Programming (Part 1)
## Module 05 | Sustain Engineering Training | Day 6

**1 day | Workshop + guided lab**

---

## By the end of this session

You can write, compile, and run Java programs using OOP principles -- classes, objects, encapsulation, constructors, and access control.

| Pillar | What you will do |
|--------|-----------------|
| **Core Java** | JDK, JRE, JVM, compilation, execution |
| **Classes & Objects** | Define classes, create objects, invoke methods |
| **Packages** | Organize code, import statements, naming conventions |
| **Encapsulation** | Private fields, getters/setters, data hiding |
| **Access Control** | public, private, protected, default (package-private) |
| **Constructors** | Default, parameterized, constructor overloading |
| **Static Members** | Static fields, static methods, constants |
| **Scopes & Blocks** | Local, instance, class scope, initializer blocks |
| **References** | Object references, `this`, `null`, garbage collection |

---

## Session agenda

| # | Topic |
|---|-------|
| 01 | Java platform overview: JDK, JRE, JVM |
| 02 | Hello World: compile and run |
| 03 | Variables, data types, operators |
| 04 | Control flow: if/else, switch, loops |
| 05 | Classes and objects |
| 06 | Packages and imports |
| 07 | Encapsulation and access control |
| 08 | Constructors and overloading |
| 09 | Static members and constants |
| 10 | Scopes, blocks, and references |
| 11 | Guided lab |

---

## Why Java for sustain engineering

- **Enterprise standard** -- most large-scale backend systems run on Java
- **Strong typing** -- catches bugs at compile time, not runtime
- **Mature ecosystem** -- Spring, Hibernate, Maven, Gradle, JUnit
- **Platform independent** -- "write once, run anywhere" (JVM)
- **Backward compatible** -- Java 8 code runs on Java 21
- **Sustain reality** -- you will maintain Java services daily

### Java in the FoodExpress architecture

```
Browser (HTML/CSS/JS)
    |
    v
API Gateway
    |
    +-- Order Service (Java/Spring Boot)
    +-- Restaurant Service (Java/Spring Boot)
    +-- Payment Service (Java/Spring Boot)
    +-- Notification Service (Node.js)
```

> Most FoodExpress backend services are Java. Understanding Java is essential for sustain engineers.

---

## Java platform: JDK, JRE, JVM

<!--VISUAL:jdk-jre-jvm-layers-->

```
+-------------------------------------------+
|  JDK (Java Development Kit)               |
|  +-------------------------------------+  |
|  |  JRE (Java Runtime Environment)     |  |
|  |  +-------------------------------+  |  |
|  |  |  JVM (Java Virtual Machine)   |  |  |
|  |  |  - Loads bytecode             |  |  |
|  |  |  - Verifies code              |  |  |
|  |  |  - Executes (JIT compiler)    |  |  |
|  |  |  - Garbage collection         |  |  |
|  |  +-------------------------------+  |  |
|  |  + Java Class Libraries (rt.jar)   |  |
|  +-------------------------------------+  |
|  + Compiler (javac)                       |
|  + Debugger (jdb)                         |
|  + Tools (jar, javadoc, jshell)           |
+-------------------------------------------+
```

| Component | Contains | Used by |
|-----------|----------|---------|
| **JVM** | Virtual machine that runs bytecode | End users |
| **JRE** | JVM + standard libraries | End users |
| **JDK** | JRE + compiler + dev tools | Developers |

> Install the JDK for development. Production servers need only the JRE (or a minimal JDK image in containers).

---

## Compilation and execution

```
Source code         Compiler         Bytecode           JVM
(.java)   -------> (javac)  ------> (.class)  -------> Runs on
                                                        any OS
```

```bash
# Step 1: Write source code
# File: HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, FoodExpress!");
    }
}

# Step 2: Compile
javac HelloWorld.java
# Produces: HelloWorld.class (bytecode)

# Step 3: Run
java HelloWorld
# Output: Hello, FoodExpress!
```

| Rule | Description |
|------|-------------|
| File name must match class name | `MenuItem.java` contains `class MenuItem` |
| Every app needs `main` method | Entry point: `public static void main(String[] args)` |
| Java is case-sensitive | `menuItem` and `MenuItem` are different |
| Statements end with `;` | Missing semicolons cause compile errors |

---

## Variables and data types

```java
// Primitive types (stored on stack)
byte    itemCount    = 5;           // 8-bit  (-128 to 127)
short   portNumber   = 8080;        // 16-bit (-32768 to 32767)
int     orderId      = 104253;      // 32-bit (most common integer)
long    timestamp    = 1690000000L; // 64-bit (note the L suffix)
float   taxRate      = 0.08f;       // 32-bit decimal (note the f)
double  price        = 8.99;        // 64-bit decimal (default)
boolean isOpen       = true;        // true or false
char    grade        = 'A';         // single character (single quotes)

// Reference types (stored on heap)
String  name         = "Burger Barn";   // immutable string
int[]   ratings      = {4, 5, 3, 4};   // array
```

| Type | Size | Range | Default |
|------|------|-------|---------|
| `byte` | 1 byte | -128 to 127 | 0 |
| `short` | 2 bytes | -32,768 to 32,767 | 0 |
| `int` | 4 bytes | -2.1B to 2.1B | 0 |
| `long` | 8 bytes | very large | 0L |
| `float` | 4 bytes | ~7 decimal digits | 0.0f |
| `double` | 8 bytes | ~15 decimal digits | 0.0 |
| `boolean` | 1 bit | true / false | false |
| `char` | 2 bytes | Unicode character | '\u0000' |

---

## Type casting and conversion

```java
// Widening (implicit) -- safe, no data loss
int quantity = 5;
double amount = quantity;  // int -> double: 5.0

// Narrowing (explicit) -- may lose data
double price = 8.99;
int rounded = (int) price;  // 8 (decimal truncated, NOT rounded)

// String to number
String input = "42";
int value = Integer.parseInt(input);        // 42
double dValue = Double.parseDouble("8.99"); // 8.99

// Number to String
String text = String.valueOf(42);           // "42"
String text2 = Integer.toString(42);        // "42"
String text3 = "" + 42;                     // "42" (concatenation)

// Common bug: NumberFormatException
try {
    int bad = Integer.parseInt("abc");  // throws!
} catch (NumberFormatException e) {
    System.out.println("Invalid number format");
}
```

> Always use `try/catch` when parsing user input to numbers. Invalid input causes `NumberFormatException`.

---

## Operators

```java
// Arithmetic
int total = price * quantity;    // + - * / %
int remainder = 10 % 3;         // 1

// Division: integer vs floating point
int result = 7 / 2;             // 3 (integer division!)
double result2 = 7.0 / 2;       // 3.5

// Comparison
price == 8.99     // true (for primitives)
price != 9.99     // true
price > 5         // true
price >= 8.99     // true

// Logical
isOpen && hasItems    // AND
isOpen || isTakeaway  // OR
!isOpen               // NOT

// Assignment shortcuts
total += 5;   // total = total + 5
count++;      // count = count + 1
count--;      // count = count - 1

// Ternary
String status = isOpen ? "Open" : "Closed";
```

> Use `==` for primitives. Use `.equals()` for objects (especially `String`). `==` on objects compares references, not values.

---

## String operations

```java
String name = "Burger Barn";

// Common methods
name.length();                    // 11
name.charAt(0);                   // 'B'
name.substring(0, 6);            // "Burger"
name.toLowerCase();               // "burger barn"
name.toUpperCase();               // "BURGER BARN"
name.contains("Burger");          // true
name.startsWith("Burger");        // true
name.indexOf("Barn");             // 7
name.trim();                      // removes leading/trailing spaces
name.replace("Barn", "Palace");   // "Burger Palace"
name.split(" ");                  // ["Burger", "Barn"]

// String comparison (ALWAYS use .equals())
String a = "hello";
String b = new String("hello");
a == b;          // false (different references!)
a.equals(b);     // true (same content)

// String concatenation
String msg = "Order for " + name + " - $" + price;

// StringBuilder (efficient for many concatenations)
StringBuilder sb = new StringBuilder();
sb.append("Order #").append(orderId).append(": ").append(name);
String result = sb.toString();
```

> Never compare strings with `==`. Always use `.equals()`. This is the #1 Java bug in sustain engineering.

---

## Control flow: if / else / switch

```java
// if / else if / else
double cartTotal = 27.50;
double deliveryFee;

if (cartTotal >= 25.0) {
    deliveryFee = 0.0;
    System.out.println("Free delivery!");
} else if (cartTotal >= 15.0) {
    deliveryFee = 1.99;
} else {
    deliveryFee = 3.99;
}

// switch (classic)
String status = "preparing";
switch (status) {
    case "placed":
        System.out.println("Order received");
        break;
    case "preparing":
        System.out.println("Kitchen is cooking");
        break;
    case "delivered":
        System.out.println("Enjoy your meal!");
        break;
    default:
        System.out.println("Unknown status");
}

// switch expression (Java 14+)
String message = switch (status) {
    case "placed" -> "Order received";
    case "preparing" -> "Kitchen is cooking";
    case "delivered" -> "Enjoy your meal!";
    default -> "Unknown status";
};
```

---

## Control flow: loops

```java
// for loop
String[] menuItems = {"Burger", "Fries", "Shake", "Salad"};
for (int i = 0; i < menuItems.length; i++) {
    System.out.println((i + 1) + ". " + menuItems[i]);
}

// enhanced for (for-each) -- preferred for arrays/collections
for (String item : menuItems) {
    System.out.println(item);
}

// while loop
int attempts = 0;
while (attempts < 3) {
    System.out.println("Attempt " + (attempts + 1));
    attempts++;
}

// do-while loop (runs at least once)
do {
    retryConnection();
    attempts++;
} while (!isConnected && attempts < 5);

// break and continue
for (String item : menuItems) {
    if (item.equals("Fries")) continue;  // skip Fries
    if (item.equals("Salad")) break;     // stop at Salad
    System.out.println(item);
}
// Output: Burger, Shake
```

---

## Arrays

```java
// Declaration and initialization
int[] ratings = new int[5];           // size 5, all zeros
String[] cuisines = {"Italian", "Japanese", "Indian", "Mexican"};

// Access and modify
cuisines[0];                          // "Italian"
cuisines[2] = "Thai";                 // replace "Indian"
cuisines.length;                      // 4

// Iterate
for (int i = 0; i < cuisines.length; i++) {
    System.out.println(cuisines[i]);
}

// Multi-dimensional array
double[][] prices = {
    {8.99, 4.99, 5.99},   // restaurant 0
    {10.99, 6.99, 7.99},  // restaurant 1
};
prices[0][1];  // 4.99

// Common operations (java.util.Arrays)
import java.util.Arrays;
Arrays.sort(ratings);                  // sort in place
Arrays.fill(ratings, 0);              // fill with zeros
String str = Arrays.toString(ratings); // "[0, 0, 0, 0, 0]"
int idx = Arrays.binarySearch(ratings, 4); // find index
```

> Arrays have a fixed size. For dynamic sizing, use `ArrayList` (covered in Part 2).

---

## Classes and objects: the foundation

<!--VISUAL:java-class-anatomy-->

```java
// A class is a blueprint
public class MenuItem {
    // Fields (attributes)
    String name;
    double price;
    String category;
    boolean isAvailable;

    // Method (behavior)
    String getInfo() {
        return name + " - $" + String.format("%.2f", price);
    }

    void toggleAvailability() {
        isAvailable = !isAvailable;
    }
}
```

```java
// Creating objects (instances)
MenuItem burger = new MenuItem();
burger.name = "Smash Burger";
burger.price = 8.99;
burger.category = "Mains";
burger.isAvailable = true;

MenuItem fries = new MenuItem();
fries.name = "Loaded Fries";
fries.price = 4.99;
fries.category = "Sides";
fries.isAvailable = true;

System.out.println(burger.getInfo());  // "Smash Burger - $8.99"
```

> A class defines what an object looks like. An object is a specific instance of that class.

---

## Class vs Object analogy

```
Class (Blueprint)              Object (Instance)
+-----------------+            +-----------------+
| MenuItem        |            | burger          |
+-----------------+   new      +-----------------+
| name            | ---------> | "Smash Burger"  |
| price           |            | 8.99            |
| category        |            | "Mains"         |
| isAvailable     |            | true            |
+-----------------+            +-----------------+
| getInfo()       |
| toggle...()     |            | fries           |
+-----------------+   new      +-----------------+
                   ---------> | "Loaded Fries"  |
                              | 4.99            |
                              | "Sides"         |
                              | true            |
                              +-----------------+
```

| Concept | Class | Object |
|---------|-------|--------|
| What | Blueprint / template | Instance / real thing |
| Memory | No memory allocated for data | Allocated on heap |
| Count | One per type | Many per class |
| Fields | Defines structure | Holds actual values |
| Methods | Defines behavior | Executes behavior |

---

## FoodExpress: OrderItem class

```java
public class OrderItem {
    String menuItemName;
    double unitPrice;
    int quantity;
    String specialInstructions;

    double getSubtotal() {
        return unitPrice * quantity;
    }

    String getSummary() {
        String line = quantity + "x " + menuItemName
            + " @ $" + String.format("%.2f", unitPrice)
            + " = $" + String.format("%.2f", getSubtotal());
        if (specialInstructions != null && !specialInstructions.isEmpty()) {
            line += " [" + specialInstructions + "]";
        }
        return line;
    }
}
```

```java
// Usage
OrderItem item = new OrderItem();
item.menuItemName = "Smash Burger";
item.unitPrice = 8.99;
item.quantity = 2;
item.specialInstructions = "No onions";

System.out.println(item.getSummary());
// 2x Smash Burger @ $8.99 = $17.98 [No onions]
System.out.println(item.getSubtotal());
// 17.98
```

---

## Packages: organizing code

```java
// Package declaration (first line of file)
package com.foodexpress.order;

// File structure must match package
// src/com/foodexpress/order/OrderItem.java
// src/com/foodexpress/menu/MenuItem.java
// src/com/foodexpress/customer/Customer.java
```

```
com.foodexpress
    |
    +-- order/
    |     OrderItem.java
    |     OrderService.java
    |
    +-- menu/
    |     MenuItem.java
    |     MenuService.java
    |
    +-- customer/
          Customer.java
          CustomerService.java
```

### Import statements

```java
// Import a specific class
import com.foodexpress.menu.MenuItem;

// Import all classes in a package
import com.foodexpress.menu.*;

// java.lang is auto-imported (String, System, Math, etc.)
```

| Convention | Example |
|-----------|---------|
| Reverse domain name | `com.foodexpress.order` |
| All lowercase | `com.example.myapp` |
| Avoid `java.*` and `javax.*` | Reserved for JDK |

---

## Package naming conventions

| Package | Purpose | Example classes |
|---------|---------|----------------|
| `com.foodexpress.model` | Data classes (entities) | `MenuItem`, `Order`, `Customer` |
| `com.foodexpress.service` | Business logic | `OrderService`, `MenuService` |
| `com.foodexpress.controller` | HTTP handlers | `OrderController` |
| `com.foodexpress.repository` | Data access | `OrderRepository` |
| `com.foodexpress.util` | Utility/helper classes | `PriceFormatter`, `Validator` |
| `com.foodexpress.exception` | Custom exceptions | `OrderNotFoundException` |
| `com.foodexpress.config` | Configuration | `AppConfig`, `DatabaseConfig` |

```java
// Full example with package and import
package com.foodexpress.order;

import com.foodexpress.menu.MenuItem;
import java.util.List;
import java.util.ArrayList;

public class OrderService {
    private List<OrderItem> items = new ArrayList<>();

    public void addItem(MenuItem menuItem, int quantity) {
        OrderItem item = new OrderItem();
        item.menuItemName = menuItem.name;
        item.unitPrice = menuItem.price;
        item.quantity = quantity;
        items.add(item);
    }
}
```

---

## Encapsulation: hiding internal data

**Problem:** Direct field access allows invalid state.

```java
// Without encapsulation (BAD)
MenuItem burger = new MenuItem();
burger.price = -5.00;  // negative price? No protection!
burger.name = "";       // empty name? Allowed!
```

**Solution:** Make fields `private`, provide controlled access via methods.

```java
public class MenuItem {
    // Private fields -- cannot be accessed directly
    private String name;
    private double price;
    private String category;
    private boolean available;

    // Getter: controlled read access
    public String getName() {
        return name;
    }

    // Setter: controlled write access with validation
    public void setName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Name cannot be empty");
        }
        this.name = name.trim();
    }

    public void setPrice(double price) {
        if (price < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
        this.price = price;
    }

    public double getPrice() {
        return price;
    }
}
```

---

## Encapsulation benefits

```java
// With encapsulation -- invalid state prevented
MenuItem burger = new MenuItem();
burger.setName("Smash Burger");    // OK
burger.setPrice(8.99);             // OK
burger.setPrice(-5.00);            // throws IllegalArgumentException!
burger.setName("");                 // throws IllegalArgumentException!

// Read-only field (getter only, no setter)
public class Order {
    private final String orderId;
    private final long createdAt;

    public Order(String orderId) {
        this.orderId = orderId;
        this.createdAt = System.currentTimeMillis();
    }

    public String getOrderId() { return orderId; }
    public long getCreatedAt() { return createdAt; }
    // No setters -- orderId and createdAt cannot change
}
```

| Benefit | How |
|---------|-----|
| **Data validation** | Setters reject invalid values |
| **Read-only fields** | Getter only, no setter |
| **Computed properties** | Getter calculates on the fly |
| **Internal changes** | Can change field type without breaking callers |
| **Debugging** | Set breakpoints in getters/setters |

> Encapsulation is the #1 OOP principle. Every field should be `private` unless there's a strong reason not to.

---

## Access modifiers

```java
public class MenuItem {
    public String name;           // accessible everywhere
    protected String category;    // same package + subclasses
    String cuisine;               // package-private (default)
    private double cost;          // this class only
}
```

| Modifier | Same class | Same package | Subclass | Everywhere |
|----------|-----------|-------------|----------|-----------|
| `public` | Yes | Yes | Yes | Yes |
| `protected` | Yes | Yes | Yes | No |
| (default) | Yes | Yes | No | No |
| `private` | Yes | No | No | No |

### Rules of thumb

| What | Modifier | Why |
|------|----------|-----|
| Fields | `private` | Encapsulation -- always |
| Getters/Setters | `public` | External access through controlled methods |
| Helper methods | `private` | Internal implementation detail |
| API methods | `public` | Part of the class's contract |
| Constants | `public static final` | Shared configuration values |

---

## Access control in practice

```java
package com.foodexpress.order;

public class Order {
    // Private: only Order methods can access
    private String orderId;
    private double total;
    private String status;

    // Public: anyone can call
    public String getOrderId() {
        return orderId;
    }

    public String getStatus() {
        return status;
    }

    // Public: controlled state transition
    public void cancel() {
        if (!"placed".equals(status)) {
            throw new IllegalStateException(
                "Cannot cancel order in status: " + status);
        }
        this.status = "cancelled";
        logStatusChange("cancelled");  // private helper
    }

    // Private: internal helper
    private void logStatusChange(String newStatus) {
        System.out.println("Order " + orderId
            + " status changed to " + newStatus);
    }

    // Package-private: only classes in same package
    void setStatus(String status) {
        this.status = status;
    }
}
```

---

## Constructors: initializing objects

```java
public class MenuItem {
    private String name;
    private double price;
    private String category;
    private boolean available;

    // Default constructor (no arguments)
    public MenuItem() {
        this.name = "Unknown";
        this.price = 0.0;
        this.category = "Uncategorized";
        this.available = false;
    }

    // Parameterized constructor
    public MenuItem(String name, double price, String category) {
        this.name = name;
        this.price = price;
        this.category = category;
        this.available = true;
    }
}
```

```java
// Using constructors
MenuItem unknown = new MenuItem();
// name="Unknown", price=0.0, category="Uncategorized"

MenuItem burger = new MenuItem("Smash Burger", 8.99, "Mains");
// name="Smash Burger", price=8.99, category="Mains", available=true
```

| Rule | Description |
|------|-------------|
| Same name as class | `MenuItem()` inside `class MenuItem` |
| No return type | Not even `void` |
| Called with `new` | `new MenuItem()` |
| Auto-generated | Java adds a no-arg constructor if you write none |
| Disappears | If you define ANY constructor, the default is NOT added |

---

## Constructor overloading

```java
public class OrderItem {
    private String menuItemName;
    private double unitPrice;
    private int quantity;
    private String specialInstructions;

    // Constructor 1: all fields
    public OrderItem(String name, double price, int qty, String instructions) {
        this.menuItemName = name;
        this.unitPrice = price;
        this.quantity = qty;
        this.specialInstructions = instructions;
    }

    // Constructor 2: without special instructions
    public OrderItem(String name, double price, int qty) {
        this(name, price, qty, null);  // delegate to constructor 1
    }

    // Constructor 3: single item (quantity = 1)
    public OrderItem(String name, double price) {
        this(name, price, 1, null);  // delegate to constructor 1
    }
}
```

```java
// Different ways to create
OrderItem item1 = new OrderItem("Burger", 8.99, 2, "No onions");
OrderItem item2 = new OrderItem("Fries", 4.99, 1);
OrderItem item3 = new OrderItem("Shake", 5.99);
```

> Use `this(...)` to call another constructor in the same class. It must be the first statement.

---

## Constructor validation

```java
public class MenuItem {
    private String name;
    private double price;
    private String category;

    public MenuItem(String name, double price, String category) {
        // Validate in constructor -- prevent invalid objects
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Name is required");
        }
        if (price < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
        if (category == null || category.trim().isEmpty()) {
            throw new IllegalArgumentException("Category is required");
        }

        this.name = name.trim();
        this.price = price;
        this.category = category.trim();
    }

    // No setters for name/category -- immutable after creation
    public String getName() { return name; }
    public double getPrice() { return price; }
    public String getCategory() { return category; }
}
```

> Validate early, fail fast. Constructor validation ensures no invalid object ever exists.

---

## Static members: class-level data

```java
public class Order {
    // Static field: shared across ALL instances
    private static int orderCounter = 1000;

    // Static constant
    public static final double TAX_RATE = 0.08;
    public static final double FREE_DELIVERY_THRESHOLD = 25.00;

    // Instance fields
    private String orderId;
    private double subtotal;

    public Order() {
        orderCounter++;
        this.orderId = "FE-" + orderCounter;  // FE-1001, FE-1002, ...
    }

    // Static method: does NOT need an instance
    public static double calculateTax(double amount) {
        return amount * TAX_RATE;
    }

    // Instance method: needs an instance
    public double getTotal() {
        return subtotal + Order.calculateTax(subtotal);
    }

    // Static method: access static field
    public static int getOrderCount() {
        return orderCounter - 1000;
    }
}
```

---

## Static vs instance

```java
// Static: called on the CLASS
double tax = Order.calculateTax(24.97);
int count = Order.getOrderCount();
double threshold = Order.FREE_DELIVERY_THRESHOLD;

// Instance: called on an OBJECT
Order order = new Order();
String id = order.getOrderId();
double total = order.getTotal();
```

| Feature | Static | Instance |
|---------|--------|----------|
| Belongs to | Class | Object |
| Access | `ClassName.method()` | `object.method()` |
| Can access static fields? | Yes | Yes |
| Can access instance fields? | No | Yes |
| Memory | One copy | One per object |
| Use for | Utility methods, constants, counters | Object-specific behavior |

### Common static examples in Java

```java
Math.max(a, b);              // utility method
Math.PI;                     // constant
Integer.parseInt("42");      // conversion
String.valueOf(42);          // conversion
System.currentTimeMillis();  // utility
Collections.sort(list);     // utility
```

---

## Scopes in Java

```java
public class OrderService {
    // Class scope: accessible in all methods
    private static final double TAX_RATE = 0.08;

    // Instance scope: one per object
    private List<OrderItem> items;

    public OrderService() {
        this.items = new ArrayList<>();
    }

    public double calculateTotal() {
        // Local scope: only inside this method
        double subtotal = 0;

        for (OrderItem item : items) {
            // Block scope: only inside this loop
            double lineTotal = item.getUnitPrice() * item.getQuantity();
            subtotal += lineTotal;
        }
        // lineTotal is NOT accessible here

        double tax = subtotal * TAX_RATE;
        return subtotal + tax;
    }
    // subtotal and tax are NOT accessible here
}
```

| Scope | Lifetime | Accessible in |
|-------|----------|---------------|
| **Class** (static) | Program lifetime | All methods (via class name) |
| **Instance** | Object lifetime | All instance methods |
| **Local** | Method execution | The method only |
| **Block** | Block execution | The `{}` block only |

---

## Initializer blocks

```java
public class MenuItem {
    private String id;
    private String name;
    private double price;
    private long createdAt;

    // Static initializer: runs ONCE when class is loaded
    private static int counter;
    static {
        counter = 0;
        System.out.println("MenuItem class loaded");
    }

    // Instance initializer: runs EVERY TIME an object is created
    // Runs BEFORE the constructor
    {
        counter++;
        this.id = "ITEM-" + counter;
        this.createdAt = System.currentTimeMillis();
    }

    public MenuItem(String name, double price) {
        // id and createdAt already set by initializer block
        this.name = name;
        this.price = price;
    }
}
```

| Block type | When it runs | Use for |
|-----------|-------------|---------|
| `static { }` | Once, when class first loaded | Load config, initialize static data |
| `{ }` (instance) | Every time an object is created, before constructor | Common setup for all constructors |

---

## References and memory

```java
// Primitives: value is stored directly
int a = 5;
int b = a;    // b gets a COPY of 5
b = 10;       // a is still 5

// Objects: variable holds a REFERENCE (pointer)
MenuItem burger = new MenuItem("Burger", 8.99);
MenuItem alias = burger;   // alias points to SAME object
alias.setPrice(9.99);      // changes the shared object
System.out.println(burger.getPrice());  // 9.99 (CHANGED!)
```

```
Stack                    Heap
+--------+              +-------------------+
| burger | -----------> | MenuItem          |
+--------+         /--> | name: "Burger"    |
| alias  | -------/     | price: 9.99       |
+--------+              +-------------------+
```

| Concept | Primitive | Reference |
|---------|-----------|-----------|
| Stores | Actual value | Memory address |
| Copy | Copies value | Copies reference (not object) |
| `==` compares | Values | References (use `.equals()`) |
| Default | `0`, `false`, `'\0'` | `null` |

---

## The `this` keyword

```java
public class Order {
    private String orderId;
    private String customerName;
    private double total;

    // 'this' disambiguates field from parameter
    public Order(String orderId, String customerName) {
        this.orderId = orderId;           // field = parameter
        this.customerName = customerName;
    }

    // 'this' calls another constructor
    public Order(String orderId) {
        this(orderId, "Guest");  // must be FIRST statement
    }

    // 'this' enables method chaining (fluent API)
    public Order setTotal(double total) {
        this.total = total;
        return this;
    }

    public Order applyDiscount(double rate) {
        this.total *= (1 - rate);
        return this;
    }
}
```

```java
// Method chaining
Order order = new Order("FE-1001", "Alice")
    .setTotal(24.97)
    .applyDiscount(0.10);
```

---

## Null references and NullPointerException

```java
// null means "no object"
MenuItem item = null;
item.getName();  // NullPointerException! (NPE)

// Defensive coding: check for null
if (item != null) {
    System.out.println(item.getName());
}

// Common NPE scenarios
String name = order.getCustomer().getName();
// If getCustomer() returns null, calling .getName() throws NPE

// Defensive approach
Customer customer = order.getCustomer();
if (customer != null) {
    String name = customer.getName();
}

// Java Optional (Java 8+) -- better approach
import java.util.Optional;

Optional<Customer> customer = Optional.ofNullable(order.getCustomer());
String name = customer.map(Customer::getName).orElse("Unknown");
```

> `NullPointerException` is the most common runtime error in Java. Always check for null before calling methods on objects.

---

## Garbage collection

```java
// Object becomes eligible for GC when no references point to it
MenuItem burger = new MenuItem("Burger", 8.99);
burger = null;  // original object has no references -> eligible for GC

// Also eligible when reference goes out of scope
void processOrder() {
    MenuItem temp = new MenuItem("Temp", 0.0);
    // ... use temp ...
}  // temp goes out of scope -> eligible for GC

// Cannot force GC, only suggest
System.gc();  // suggestion only, JVM may ignore
```

| GC concept | Description |
|-----------|-------------|
| **Heap** | Where objects live |
| **Stack** | Where references and primitives live |
| **GC roots** | Static fields, local variables, active threads |
| **Eligible** | Object with no path from any GC root |
| **Automatic** | JVM runs GC when it decides (no manual free/delete) |

> Java manages memory automatically. You do not call `free()` or `delete`. But you must avoid holding unnecessary references (memory leaks).

---

## Checkpoint: code reading

What does this code print?

```java
public class Test {
    private int x = 10;
    private static int count = 0;

    public Test() { count++; }

    public static void main(String[] args) {
        Test a = new Test();
        Test b = new Test();
        Test c = a;

        a.x = 20;
        System.out.println(c.x);       // ?
        System.out.println(Test.count); // ?
        System.out.println(a == c);     // ?
        System.out.println(a == b);     // ?
    }
}
```

| Line | Output | Reason |
|------|--------|--------|
| `c.x` | `20` | `c` and `a` reference the same object |
| `Test.count` | `2` | Two `new Test()` calls |
| `a == c` | `true` | Same reference |
| `a == b` | `false` | Different objects |

---

## Guided lab: build the FoodExpress OrderItem

| Step | Task |
|------|------|
| 01 | Fix: `MenuItem` fields are public -- make them private with getters/setters |
| 02 | Fix: Constructor does not validate price (allows negative values) |
| 03 | Fix: `OrderItem.getSubtotal()` returns wrong result (integer division bug) |
| 04 | Fix: String comparison uses `==` instead of `.equals()` |
| 05 | Fix: `NullPointerException` when `specialInstructions` is null |
| 06 | Add: Static `orderCounter` that generates unique order IDs |
| 07 | Add: Constructor overloading for `OrderItem` (with/without instructions) |
| 08 | Add: `toString()` method that returns a formatted order summary |

---

## Lab acceptance criteria

- [ ] All fields are `private` with appropriate getters/setters
- [ ] Constructor rejects negative price and empty name
- [ ] `getSubtotal()` returns correct `double` result
- [ ] String comparison uses `.equals()` throughout
- [ ] No `NullPointerException` when optional fields are null
- [ ] Static counter generates unique IDs (FE-1001, FE-1002, ...)
- [ ] At least two constructor overloads work correctly
- [ ] `toString()` returns readable output
- [ ] Code compiles with `javac` without warnings
- [ ] Code follows Java naming conventions (camelCase, PascalCase)

---

## Key takeaways

| Concept | Remember |
|---------|----------|
| JDK vs JRE vs JVM | JDK for development, JRE for running, JVM executes bytecode |
| Primitives vs References | Primitives hold values, references hold addresses |
| String comparison | Always `.equals()`, never `==` for strings |
| Encapsulation | Fields `private`, access via getters/setters |
| Access modifiers | `private` > default > `protected` > `public` (least privilege) |
| Constructors | Same name as class, no return type, validate inputs |
| Static | Belongs to class, not object. Use for utilities and constants |
| `this` | Refers to current object. Disambiguates fields from params |
| Null safety | Check for `null` before calling methods. NPE is #1 Java bug |
| Garbage collection | Automatic. No references = eligible for GC |

> **Next: Module 06 -- Java Programming (Part 2): Exceptions, interfaces, abstract classes, I/O streams**