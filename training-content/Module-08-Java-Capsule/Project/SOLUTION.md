# Module 08 Solutions -- TRAINER ONLY

## Ticket FOOD-21: GET /orders/{id} Returns 500

**Root Cause:** `OrderService.getOrderById()` calls `order.getRestaurant().getName()` without null-checking the restaurant reference. When an order has a deleted or missing restaurant, this throws a `NullPointerException`.

**Fix:**
```java
// Before
String restaurantName = order.getRestaurant().getName();

// After
String restaurantName = order.getRestaurant() != null
    ? order.getRestaurant().getName()
    : "Unknown Restaurant";
```

Also add proper 404 handling in the controller:
```java
return orderService.getOrderById(id)
    .map(ResponseEntity::ok)
    .orElse(ResponseEntity.notFound().build());
```

## Ticket FOOD-22: Add Status Filter Endpoint

**Implementation:** Add a query parameter to the existing list endpoint.

```java
// OrderRepository.java
List<Order> findByStatus(String status);

// OrderController.java
@GetMapping("/orders")
public ResponseEntity<List<Order>> getOrders(
        @RequestParam(required = false) String status) {
    if (status != null) {
        return ResponseEntity.ok(orderRepository.findByStatus(status));
    }
    return ResponseEntity.ok(orderRepository.findAll());
}
```

## Ticket FOOD-23: No Pagination on Order List

**Root Cause:** `findAll()` returns the entire orders table. With 50+ orders the response is 5+ MB and the mobile app times out.

**Fix:**
```java
// OrderRepository.java -- extend PagingAndSortingRepository or use Pageable
Page<Order> findAll(Pageable pageable);

// OrderController.java
@GetMapping("/orders")
public ResponseEntity<Page<Order>> getOrders(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size) {
    Pageable pageable = PageRequest.of(page, size, Sort.by("orderDate").descending());
    return ResponseEntity.ok(orderService.getOrders(pageable));
}
```

## Ticket FOOD-24: Negative Quantities Accepted

**Root Cause:** No validation on the `Order` entity or service layer. `POST /orders` with `"quantity": -3` creates a valid order.

**Fix:**
```java
// Order.java -- add Bean Validation
@Min(value = 1, message = "Quantity must be at least 1")
private int quantity;

// OrderController.java -- add @Valid
public ResponseEntity<Order> createOrder(@Valid @RequestBody Order order) { ... }
```

## Hints

| Ticket | Level 1 | Level 2 |
|--------|---------|---------|
| FOOD-21 | "Check what happens when the restaurant FK is null" | "Add a null check before calling getRestaurant().getName()" |
| FOOD-22 | "Add a @RequestParam to the GET /orders endpoint" | "Create a findByStatus method in the repository" |
| FOOD-23 | "Look at Spring Data's Pageable interface" | "Use PageRequest.of(page, size) and return Page<Order>" |
| FOOD-24 | "What happens if you POST quantity = -5?" | "Use @Min(1) on the entity field and @Valid on the controller" |
