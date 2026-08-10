# Capsule Project: Java
## Module 08 | Sustain Engineering Training | Day 9

**1 day | Capsule project + presentation + MCQ**

---

## Agenda -- Full Day Schedule

| # | Activity |
|---|-------|
| 01 | Project briefing & architecture review |
| 02 | Team formation & repo setup |
| 03 | Sprint 1: Core development |
| 04 | Lunch break |
| 05 | Sprint 2: Integration & testing |
| 06 | Code freeze & prepare presentation |
| 07 | Team presentations & feedback |
| 08 | MCQ assessment |

---

## What Is a Capsule Project?

- A **time-boxed**, hands-on project that consolidates learning from Modules 05-07
- Simulates real sustain engineering work:
  - Read and understand existing code
  - Fix bugs and add features
  - Work under time pressure
  - Present your work to stakeholders

### Evaluation Criteria

| Criteria | Weight |
|----------|--------|
| Code correctness & functionality | 30% |
| Code quality & best practices | 20% |
| Bug fixes completed | 20% |
| Presentation & communication | 15% |
| MCQ score | 15% |

---

## Project: FoodExpress Order Management System

### Business Context

FoodExpress needs a **console-based Order Management System** that allows:

- Restaurant staff to manage the menu catalog
- Customers to browse menu and place orders
- System to calculate totals, apply discounts, and persist data

### You Will Build

```
FoodExpress Order Management System
+---------------------+
|   MenuService       |  --> Manage menu items (CRUD)
+---------------------+
|   OrderService      |  --> Create & manage orders
+---------------------+
|   ReportService     |  --> Generate order summaries
+---------------------+
|   Database (JDBC)   |  --> Persist data to MySQL
+---------------------+
```

---

## Architecture Overview

### Class Diagram

```
MenuItem
  - id: String
  - name: String
  - price: double
  - category: String
  - available: boolean
  + equals(), hashCode()

OrderItem
  - menuItem: MenuItem
  - quantity: int
  + getSubtotal(): double

Order
  - orderId: String
  - customerName: String
  - items: List<OrderItem>
  - status: OrderStatus
  - createdAt: LocalDateTime
  + getTotal(): double

OrderStatus (enum)
  PENDING, CONFIRMED, PREPARING, DELIVERED, CANCELLED
```

---

## Technical Requirements

### Must Use (from Modules 05-07)

| Concept | Where to Apply |
|---------|---------------|
| Classes & Objects | MenuItem, Order, OrderItem |
| Inheritance | Base `Service` class for common operations |
| Interfaces | `Searchable<T>` for menu search |
| Encapsulation | Private fields, getters/setters |
| ArrayList | Order items collection |
| HashMap | Menu catalog (id -> MenuItem) |
| HashSet | Track unique categories |
| Generics | Type-safe collections and methods |
| Iterator | Safe removal of cancelled orders |
| JDBC | Persist menu items and orders to MySQL |
| PreparedStatement | All database queries |
| Exception handling | Custom exceptions, try-with-resources |
| Maven | Project structure and dependency management |

---

## Project Structure

```
foodexpress-capsule/
  pom.xml
  src/
    main/
      java/
        com/foodexpress/
          model/
            MenuItem.java
            OrderItem.java
            Order.java
            OrderStatus.java
          service/
            MenuService.java
            OrderService.java
            ReportService.java
          dao/
            MenuItemDAO.java
            OrderDAO.java
          util/
            DatabaseConfig.java
            InputValidator.java
          App.java              <-- Main entry point
      resources/
        db-schema.sql           <-- Database setup script
        application.properties  <-- DB connection config
    test/
      java/
        com/foodexpress/
          service/
            MenuServiceTest.java
            OrderServiceTest.java
```

---

## Feature Requirements -- Sprint 1

### Feature 1: Menu Management

```
Console Menu:
1. Add Menu Item
2. Update Menu Item Price
3. Remove Menu Item
4. View All Menu Items
5. Search by Category
```

**Acceptance Criteria:**
- Add item with name, price, category
- Prevent duplicate item IDs
- Update price by item ID
- Remove item (mark as unavailable, don't delete)
- List all items in a formatted table
- Search/filter by category using HashMap

---

## Feature Requirements -- Sprint 1 (continued)

### Feature 2: Order Management

```
Console Menu:
1. Create New Order
2. Add Item to Order
3. Remove Item from Order
4. View Order Summary
5. Confirm Order
6. Cancel Order
```

**Acceptance Criteria:**
- Create order with customer name and auto-generated ID
- Add menu items with quantity (validate item exists and is available)
- Remove item using Iterator (safe removal)
- Calculate subtotal, tax (8%), and total
- Change order status through valid transitions only
- Prevent adding items to confirmed/cancelled orders

---

## Feature Requirements -- Sprint 2

### Feature 3: Database Persistence

**Acceptance Criteria:**
- Create MySQL tables for `menu_items` and `orders`
- Use `PreparedStatement` for all queries (no SQL injection)
- Use `try-with-resources` for all connections
- Save menu items and orders to database
- Load menu catalog from database on startup

### Feature 4: Reports

**Acceptance Criteria:**
- Total orders count by status
- Revenue report (sum of confirmed orders)
- Most popular items (frequency count using Map)
- Category breakdown using Set operations

---

## Database Schema

```sql
-- db-schema.sql
CREATE DATABASE IF NOT EXISTS foodexpress;
USE foodexpress;

CREATE TABLE menu_items (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    total DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    menu_item_id VARCHAR(36) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);
```

---

## Starter Code Provided

### App.java (Main Entry Point)

```java
public class App {
    private static final Scanner scanner = new Scanner(System.in);
    private static MenuService menuService;
    private static OrderService orderService;

    public static void main(String[] args) {
        System.out.println("=== FoodExpress Order Management ===");
        menuService = new MenuService(new MenuItemDAO());
        orderService = new OrderService(new OrderDAO());

        // Load menu from database
        menuService.loadFromDatabase();

        boolean running = true;
        while (running) {
            printMainMenu();
            int choice = getIntInput("Enter choice: ");
            switch (choice) {
                case 1: manageMenu(); break;
                case 2: manageOrders(); break;
                case 3: viewReports(); break;
                case 0: running = false; break;
                default: System.out.println("Invalid choice!");
            }
        }
        System.out.println("Goodbye!");
    }
}
```

---

## Bugs to Fix (Pre-planted)

The starter code has **intentional bugs**. Part of the project is finding and fixing them.

| # | Module | Bug Type | Symptom |
|---|--------|----------|---------|
| 1 | MenuItem | Missing hashCode | Duplicates appear in HashSet |
| 2 | OrderService | Raw types | Unsafe cast warnings |
| 3 | OrderService | ConcurrentModification | Crash when removing items in loop |
| 4 | MenuItemDAO | SQL injection | String concatenation in query |
| 5 | DatabaseConfig | Resource leak | Connection never closed |
| 6 | Order.getTotal() | Autoboxing NPE | Crashes when item price is null |
| 7 | ReportService | Wrong collection type | TreeMap used without Comparable |

> Participants must identify these bugs and apply fixes learned in Modules 05-07.

---

## Coding Standards

### Must Follow

- [ ] All classes in appropriate packages
- [ ] Private fields with getters/setters
- [ ] Meaningful variable and method names
- [ ] JavaDoc comments on public methods
- [ ] No raw types (use generics everywhere)
- [ ] try-with-resources for all I/O and JDBC
- [ ] Custom exceptions (not generic Exception)
- [ ] Logging with SLF4J (not System.out.println)
- [ ] Constants for magic numbers/strings
- [ ] Input validation on all user inputs

---

## Team Formation

### Team Size: 2-3 members

### Role Distribution

| Role | Responsibilities |
|------|-----------------|
| **Developer 1** | MenuItem model, MenuService, MenuItemDAO |
| **Developer 2** | Order model, OrderService, OrderDAO |
| **Developer 3** | ReportService, App.java, integration, testing |

### Collaboration Guidelines

- Use a shared Git repository
- Commit frequently with meaningful messages
- Communicate before modifying shared classes (model classes)
- Resolve merge conflicts together

---

## Sprint 1 Checklist (09:30 - 12:30)

### Milestone 1 (by 10:30): Project Setup
- [ ] Maven project created with correct structure
- [ ] pom.xml with MySQL connector dependency
- [ ] Model classes created (MenuItem, Order, OrderItem, OrderStatus)
- [ ] Database schema executed

### Milestone 2 (by 11:30): Core Services
- [ ] MenuService with add, update, remove, list, search
- [ ] HashMap-based menu catalog
- [ ] HashSet for category tracking
- [ ] Basic input validation

### Milestone 3 (by 12:30): Order Flow
- [ ] OrderService with create, addItem, removeItem
- [ ] Order total calculation with tax
- [ ] Iterator-based safe removal
- [ ] Status transitions validated

---

## Sprint 2 Checklist (13:30 - 15:30)

### Milestone 4 (by 14:30): Database Integration
- [ ] DatabaseConfig with connection pooling
- [ ] MenuItemDAO with CRUD (PreparedStatement)
- [ ] OrderDAO with save and load
- [ ] try-with-resources on all DB operations
- [ ] Load menu from DB on startup

### Milestone 5 (by 15:30): Reports & Bug Fixes
- [ ] ReportService with order counts, revenue, popular items
- [ ] All 7 pre-planted bugs identified and fixed
- [ ] Basic error handling for edge cases
- [ ] Console output formatted cleanly

---

## Presentation Guidelines

### Format: 10 minutes per team

### Structure

| Section | Time | Content |
|---------|------|---------|
| Demo | 4 min | Live walkthrough of working features |
| Architecture | 2 min | Class diagram, key design decisions |
| Bug Fixes | 2 min | Which bugs found, how fixed |
| Challenges | 2 min | What was hard, what you learned |

### Tips

- Start with a working demo (most impactful)
- Show the console output, not just code
- Explain **why** you chose a particular collection type
- Highlight the most interesting bug you fixed
- Be prepared for questions from the trainer and peers

---

## Presentation Scoring Rubric

| Criteria | Excellent (5) | Good (3) | Needs Work (1) |
|----------|--------------|----------|----------------|
| Demo | All features work, smooth flow | Most features work | Major issues |
| Explanation | Clear, concise, technical depth | Adequate explanation | Vague or missing |
| Bug fixes | All 7 found and explained | 4-6 found | < 4 found |
| Code quality | Clean, follows standards | Minor issues | Significant issues |
| Q&A | Confident, accurate answers | Adequate | Unable to answer |

---

## MCQ Assessment Topics

### The 30-minute MCQ will cover all Java topics (Modules 05-07):

| Topic Area | # of Questions | Example Topic |
|-----------|---------------|---------------|
| OOP Basics | 5 | Classes, objects, constructors |
| Inheritance & Polymorphism | 5 | extends, implements, override |
| Collections | 5 | List vs Set vs Map behavior |
| Generics | 3 | Wildcards, bounded types |
| JDBC | 4 | PreparedStatement, Connection |
| Exception Handling | 3 | try-catch, custom exceptions |
| Memory & GC | 3 | Heap, stack, GC types |
| Logging & Debugging | 2 | Log levels, debug techniques |

**Total: 30 questions, 1 minute each**

---

## Sample MCQ Questions

### Question 1

What happens when you add a duplicate element to a `HashSet`?

- A) Throws `DuplicateElementException`
- B) Replaces the existing element
- C) The add method returns `false` and the set is unchanged
- D) Both elements are stored

**Answer: C**

---

## Sample MCQ Questions (continued)

### Question 2

Which code prevents SQL injection?

```java
// Option A
String sql = "SELECT * FROM users WHERE id = " + userId;
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(sql);

// Option B
String sql = "SELECT * FROM users WHERE id = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setInt(1, userId);
ResultSet rs = pstmt.executeQuery();
```

**Answer: Option B**

---

## Sample MCQ Questions (continued)

### Question 3

What does this code print?

```java
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);
map.put("B", 2);
map.put("A", 3);
System.out.println(map.size() + " " + map.get("A"));
```

- A) `3 1`
- B) `2 3`
- C) `3 3`
- D) `2 1`

**Answer: B** -- `put` with existing key overwrites the value. Size remains 2.

---

## Sample MCQ Questions (continued)

### Question 4

Which exception is thrown by this code?

```java
List<String> list = new ArrayList<>(Arrays.asList("A", "B", "C"));
for (String s : list) {
    if (s.equals("B")) {
        list.remove(s);
    }
}
```

- A) `IndexOutOfBoundsException`
- B) `NullPointerException`
- C) `ConcurrentModificationException`
- D) No exception is thrown

**Answer: C**

---

## Sample MCQ Questions (continued)

### Question 5

What is the output?

```java
Integer a = 128;
Integer b = 128;
System.out.println(a == b);
System.out.println(a.equals(b));
```

- A) `true true`
- B) `false true`
- C) `true false`
- D) `false false`

**Answer: B** -- Integer cache only covers -128 to 127. `==` compares references; `equals()` compares values.

---

## Bonus Challenges

For teams that finish early:

### Challenge 1: Discount Engine
- Implement a discount system: 10% off orders over $50, 20% off orders over $100
- Use a Strategy pattern with a `DiscountStrategy` interface

### Challenge 2: Order History Search
- Search orders by customer name, date range, or status
- Use Streams API with filtering

### Challenge 3: Concurrent Orders
- Simulate multiple customers ordering simultaneously
- Use `ConcurrentHashMap` instead of `HashMap`
- Handle thread safety in OrderService

### Challenge 4: Export to CSV
- Export order history to a CSV file
- Use `BufferedWriter` with proper resource management

---

## Common Pitfalls to Avoid

| Pitfall | Why It Happens | Prevention |
|---------|---------------|------------|
| Starting to code without planning | Time pressure | Spend 15 min on design first |
| Not testing incrementally | "I'll test at the end" | Test each feature as you build it |
| Ignoring compiler warnings | "It works anyway" | Treat warnings as errors |
| Hardcoding DB credentials | Quick shortcut | Use properties file |
| Giant methods (100+ lines) | No refactoring | Extract helper methods |
| Not committing to Git | Forget | Commit after each milestone |
| System.out.println everywhere | Easy debug | Use SLF4J logger from the start |

---

## Resources & Reference

### Quick Reference During Project

| Topic | Where to Look |
|-------|--------------|
| Collections API | Module 07 slides or Java docs |
| JDBC template code | Module 07 JDBC section |
| Maven setup | Module 07 Maven slides |
| OOP patterns | Module 05-06 slides |
| Java docs | https://docs.oracle.com/en/java/javase/17/docs/api/ |

### Getting Help

1. Check the error message carefully -- read the stack trace
2. Search the Module 05-07 slides for the concept
3. Ask your teammate
4. Ask the trainer (last resort -- try to debug first!)

---

## End-of-Day Reflection

### After presentations, reflect on:

- What Java concept was hardest to apply in practice?
- Which bug was most surprising to find?
- How did pair/team programming help or hinder?
- What would you do differently with more time?

### These skills transfer directly to sustain engineering:
- Reading and understanding existing code
- Fixing bugs under time pressure
- Communicating technical decisions to stakeholders
- Working in a team with shared code

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Capsule project | Consolidates Modules 05-07 into hands-on practice |
| Collections | HashMap for catalog, ArrayList for orders, HashSet for categories |
| JDBC | PreparedStatement for all DB access, try-with-resources always |
| Bug fixing | 7 pre-planted bugs testing real-world patterns |
| Code quality | Follow standards: generics, logging, exception handling |
| Teamwork | Divide work, commit often, communicate changes |
| Presentation | Demo first, explain architecture, highlight bug fixes |
| MCQ | 30 questions covering all Java topics from Modules 05-07 |

> **Next: Module 09 -- Node.js Part 1 (server-side JavaScript fundamentals)**
