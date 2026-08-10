# Module 05: Java (Part 1) -- Fix the Issues

## Lab Overview

The FoodExpress backend is being built in Java. The domain classes for `MenuItem`, `Order`, and `OrderService` have been written but contain several bugs. The unit tests are failing.

> "Hi Team, the Java domain classes are not working. Creating an Order crashes with NullPointerException, the order totals are wrong across different orders, and the code won't even compile in some places due to import errors. Also, any code can set a negative price on menu items. Please fix before we build the REST API."

---

## Setup

1. Open `starter-code/foodexpress-java/` in IntelliJ IDEA (or VS Code with Java extensions)
2. Run `mvn compile` -- notice the compilation error from the wrong import
3. Fix the compilation error first, then run `mvn test` -- notice the test failures
4. Open the debugger and set a breakpoint in `Order.addItem()`

---

## Bug List

### Bug #1: MenuItem Fields Are Public
- **Where:** `MenuItem.java` -- field declarations
- **Symptom:** Any code can do `item.price = -50` with no validation
- **Hint:** Fields should be `private` with getters and setters. Add validation in `setPrice()` to reject negative values.
- **Debug:** Try `item.price = -99` from a test class. It works -- but it should not.

### Bug #2: Order Constructor Throws NullPointerException
- **Where:** `Order.java` -- constructor
- **Symptom:** `new Order("C001").addItem(burger)` throws NPE at `items.add()`
- **Hint:** The `items` list is declared but never initialized. Add `this.items = new ArrayList<>()` in the constructor.
- **Debug:** Set a breakpoint in the constructor. Inspect the value of `items` after construction.

### Bug #3: Static Field Shared Across Instances
- **Where:** `Order.java` -- `totalAmount` field
- **Symptom:** Creating two orders and adding items to one shows the wrong total on the other
- **Hint:** `totalAmount` is declared `static`. Remove `static` so each order has its own total.
- **Debug:** Create `order1` and `order2`. Add an item to `order1`. Check `order2.getTotalAmount()` -- it should be 0 but it is not.

### Bug #4: Wrong Package Import
- **Where:** `OrderService.java` -- import statement
- **Symptom:** `mvn compile` fails with "package does not exist"
- **Hint:** Check the import path carefully. There is a typo in the package name (`modal` instead of `model`).
- **Fix:** Correct the package name to match the actual directory structure.

### Enhancement #5: Add toString() to MenuItem
- **Where:** `MenuItem.java`
- **Hint:** Override `toString()` to return something like `"MenuItem{id=1, name='Burger', price=9.99}"`

### Enhancement #6: Implement equals() and hashCode()
- **Where:** `MenuItem.java`
- **Hint:** Two MenuItems with the same `id` should be considered equal. Override both methods.

---

## Checkpoints

1. [ ] `mvn compile` succeeds with no import errors
2. [ ] `new Order("C001")` creates an order without NPE
3. [ ] `item.price = -50` does not compile (field is private)
4. [ ] Two separate orders have independent totals
5. [ ] `System.out.println(item)` shows readable output
6. [ ] Two MenuItems with the same ID are `.equals()` true

## Bonus Challenges

1. Add an `OrderStatus` enum (PLACED, PREPARING, DELIVERED, CANCELLED) and use it in Order
2. Create a `MenuItem.Builder` with fluent API: `new MenuItem.Builder().name("Burger").price(9.99).build()`
3. Add a `getSubtotal()` method to Order that calculates price * quantity for each item
4. Write a JUnit test class for MenuItem that covers all getters, setters, and edge cases
