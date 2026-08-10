# Module 05 Solutions -- TRAINER ONLY

## Bug #1: Public Fields Violate Encapsulation

**Root Cause:** `MenuItem` declares fields as `public String name; public double price;` allowing direct mutation from anywhere.

**Fix:**
```java
// Before
public class MenuItem {
    public String name;
    public double price;
    public String category;
}

// After -- private fields with getters/setters
public class MenuItem {
    private String name;
    private double price;
    private String category;

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public double getPrice() { return price; }
    public void setPrice(double price) {
        if (price < 0) throw new IllegalArgumentException("Price cannot be negative");
        this.price = price;
    }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
}
```

## Bug #2: NullPointerException in Order Constructor

**Root Cause:** `Order` has a `List<MenuItem> items` field but the constructor never initializes it. Calling `order.addItem()` triggers NPE.

**Fix:**
```java
// Before
public class Order {
    private List<MenuItem> items;

    public Order(String customerId) {
        this.customerId = customerId;
        // items never initialized
    }
}

// After
public Order(String customerId) {
    this.customerId = customerId;
    this.items = new ArrayList<>();
}
```

## Bug #3: Static Field Shared Across All Instances

**Root Cause:** `totalAmount` is declared `static`, so all Order objects share the same total. Adding items to one order inflates the total on every order.

**Fix:**
```java
// Before
private static double totalAmount = 0;

// After -- instance field
private double totalAmount = 0;
```

## Bug #4: Wrong Package Import

**Root Cause:** `OrderService.java` imports `java.util.Date` but uses `LocalDateTime`. Or imports from a wrong package path like `com.foodexpress.modal.MenuItem` (typo: `modal` instead of `model`).

**Fix:**
```java
// Before
import com.foodexpress.modal.MenuItem; // typo in package name

// After
import com.foodexpress.model.MenuItem;
```

## Hints

| Bug | Level 1 | Level 2 |
|-----|---------|---------|
| #1 | "Can external code set `price` to -50? Should it be allowed?" | "Make fields `private`. Add getters/setters with validation." |
| #2 | "What is the value of `items` when the constructor finishes?" | "Initialize `items = new ArrayList<>()` in the constructor." |
| #3 | "Create two Order objects. Add an item to one. Check the total on both." | "Remove `static` from `totalAmount`. Static means shared across all instances." |
| #4 | "Read the exact import statement. Does the package path match the directory structure?" | "Check for typos: `modal` vs `model`." |
