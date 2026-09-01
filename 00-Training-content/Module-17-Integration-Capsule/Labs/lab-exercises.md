# Integration Capsule Project -- Lab Exercises
## Module 17 | Day 18

---

## Client Email

```
From: priya.sharma@foodexpress.in
To: sustain-engineering@team.com
Subject: URGENT - Multiple production bugs affecting customer experience
Date: 2026-07-28

Team,

We've had a spike in customer complaints over the weekend. Our support
team has logged 4 critical bugs that span multiple systems. I need
ALL of these resolved today -- our daily order volume is dropping.

Key issues:
1. Checkout page shows "NaN" for combo meal prices
2. Menu search breaks with special characters (e.g., "Chicken & Waffles")
3. Order history only shows the most recent order
4. Restaurant rating submission returns a 500 error

Each bug touches multiple layers. Please coordinate across frontend,
backend, and database teams. I need root cause analysis for each.

-- Priya Sharma, VP Engineering, FoodExpress
```

---

## Bug #1: Price Display Shows NaN (Cross-Stack)

**Priority:** P1 - Critical | **Points:** 8

### Affected Files

**Frontend -- checkout.js**
```javascript
// BUG AREA: Price calculation
function calculateTotal(cartItems) {
  let total = 0;
  cartItems.forEach(item => {
    const price = parseFloat(item.price);  // Bug 1a
    const qty = item.quantity;
    total += price * qty;
  });
  return total.toFixed(2);
}

function displayPrice(price) {
  return '₹' + price;  // Bug 1b: No validation
}

// Rendering cart
function renderCart(items) {
  const cartHtml = items.map(item => `
    <div class="cart-item">
      <span>${item.name}</span>
      <span>${displayPrice(item.price)}</span>
      <span>x${item.quantity}</span>
      <span>Subtotal: ${displayPrice(calculateTotal([item]))}</span>
    </div>
  `).join('');
  document.getElementById('cart').innerHTML = cartHtml;
}
```

**Backend -- OrderService.java**
```java
@Service
public class OrderService {

    public OrderDTO getOrderDetails(Long orderId) {
        Order order = orderRepository.findById(orderId)
            .orElseThrow(() -> new OrderNotFoundException(orderId));

        OrderDTO dto = new OrderDTO();
        dto.setItems(order.getItems().stream()
            .map(item -> {
                ItemDTO itemDto = new ItemDTO();
                itemDto.setName(item.getName());
                // Bug 1c: Formatting price with currency symbol before sending to frontend
                itemDto.setPrice("₹" + String.format("%.2f", item.getPrice()));
                itemDto.setQuantity(item.getQuantity());
                return itemDto;
            })
            .collect(Collectors.toList()));
        return dto;
    }
}
```

**Database -- schema check**
```sql
-- Verify the price column type
DESC menu_items;
-- price column: DECIMAL(10,2) -- This is correct
```

### Bugs to Find and Fix

| # | Hint | Layer |
|---|------|-------|
| 1a | `parseFloat("₹599.00")` returns NaN because of the currency symbol prefix | Frontend |
| 1b | `displayPrice` does not handle NaN or undefined values | Frontend |
| 1c | The backend formats price with currency symbol before sending as JSON | Backend |

### How to Fix

1. **Backend (OrderService.java):** Return raw numeric price. Add a separate `currency` field if needed:
   ```java
   itemDto.setPrice(item.getPrice().doubleValue());  // Raw number
   itemDto.setCurrency("INR");
   ```

2. **Frontend (checkout.js):** Add defensive parsing:
   ```javascript
   function parsePrice(price) {
     if (typeof price === 'number') return price;
     const cleaned = String(price).replace(/[^0-9.]/g, '');
     const parsed = parseFloat(cleaned);
     return isNaN(parsed) ? 0 : parsed;
   }
   ```

3. **Frontend (displayPrice):** Add validation:
   ```javascript
   function displayPrice(price) {
     const numPrice = parsePrice(price);
     return '₹' + numPrice.toFixed(2);
   }
   ```

### Checkpoint
- [ ] Combo meal prices display correctly (e.g., ₹599.00)
- [ ] Cart total calculates correctly with mixed item types
- [ ] No NaN appears anywhere in the checkout flow
- [ ] Unit test covers: numeric input, string with currency, invalid input

---

## Bug #2: Search Fails with Special Characters (Cross-Stack)

**Priority:** P2 - High | **Points:** 5

### Affected Files

**Frontend -- menu.js**
```javascript
// BUG AREA: Search functionality
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', async (e) => {
  const query = e.target.value;
  if (query.length < 2) return;

  // Bug 2a: No URL encoding of search term
  const response = await fetch(`/api/menu/search?q=${query}`);
  const items = await response.json();
  renderMenuItems(items);
});
```

**Backend -- menuRoutes.js (Node.js)**
```javascript
router.get('/search', async (req, res) => {
  try {
    const searchTerm = req.query.q;
    // Bug 2b: No input validation
    // Bug 2c: SQL injection vulnerability
    const query = `SELECT * FROM menu_items WHERE name LIKE '%${searchTerm}%' AND active = 1`;
    const [rows] = await db.execute(query);
    res.json(rows);
  } catch (error) {
    // Bug 2d: Exposing internal error details
    res.status(500).json({ error: error.message, stack: error.stack });
  }
});
```

### Bugs to Find and Fix

| # | Hint | Layer |
|---|------|-------|
| 2a | Special characters like `&` break the URL query parameter | Frontend |
| 2b | No validation of search term length or content on the server | Backend |
| 2c | String interpolation in SQL query allows SQL injection | Backend |
| 2d | Error response leaks stack trace to the client | Backend |

### How to Fix

1. **Frontend:** Use `encodeURIComponent()`:
   ```javascript
   const response = await fetch(`/api/menu/search?q=${encodeURIComponent(query)}`);
   ```

2. **Backend:** Add input validation:
   ```javascript
   const searchTerm = req.query.q;
   if (!searchTerm || searchTerm.length < 2 || searchTerm.length > 100) {
     return res.status(400).json({ error: 'Search term must be 2-100 characters' });
   }
   ```

3. **Backend:** Use parameterized query:
   ```javascript
   const query = 'SELECT * FROM menu_items WHERE name LIKE ? AND active = 1';
   const [rows] = await db.execute(query, [`%${searchTerm}%`]);
   ```

4. **Backend:** Sanitize error response:
   ```javascript
   res.status(500).json({ error: 'An internal error occurred' });
   console.error('Search error:', error);  // Log internally only
   ```

### Checkpoint
- [ ] Searching "Chicken & Waffles" returns correct results
- [ ] Searching with quotes, ampersands, and other special chars works
- [ ] SQL injection attempt `'; DROP TABLE menu_items; --` is blocked
- [ ] Error responses do not contain stack traces

---

## Bug #3: Order History Shows Only Latest Order (Cross-Stack)

**Priority:** P2 - High | **Points:** 5

### Affected Files

**Frontend -- orders.js**
```javascript
// BUG AREA: Order history rendering
async function loadOrderHistory(customerId) {
  const response = await fetch(`/api/orders/history/${customerId}`);
  const data = await response.json();

  // Bug 3a: Only rendering first order
  const order = data[0];
  const html = `
    <div class="order-card">
      <h3>Order #${order.id}</h3>
      <p>Date: ${order.createdAt}</p>
      <p>Total: ₹${order.total}</p>
      <p>Status: ${order.status}</p>
    </div>
  `;
  document.getElementById('order-history').innerHTML = html;
}
```

**Backend -- OrderController.java**
```java
@GetMapping("/history/{customerId}")
public ResponseEntity<List<OrderDTO>> getOrderHistory(
    @PathVariable Long customerId) {

    // Bug 3b: No pagination, returns ALL orders
    List<Order> orders = orderRepository.findByCustomerId(customerId);
    List<OrderDTO> dtos = orders.stream()
        .map(this::toDTO)
        .collect(Collectors.toList());
    return ResponseEntity.ok(dtos);
}
```

**Backend -- OrderRepository.java**
```java
public interface OrderRepository extends JpaRepository<Order, Long> {
    // Bug 3c: Missing ORDER BY clause
    List<Order> findByCustomerId(Long customerId);
}
```

**Database**
```sql
-- Bug 3d: Missing index on customer_id
-- Current table:
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    total DECIMAL(10,2),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- No index on customer_id
```

### Bugs to Find and Fix

| # | Hint | Layer |
|---|------|-------|
| 3a | Frontend only renders `data[0]` instead of iterating over all orders | Frontend |
| 3b | No pagination -- could return thousands of orders for a frequent customer | Backend |
| 3c | Results are not sorted by date; latest order may not be first | Backend |
| 3d | Missing database index causes slow queries on large datasets | Database |

### How to Fix

1. **Frontend:** Render all orders:
   ```javascript
   const html = data.map(order => `
     <div class="order-card">
       <h3>Order #${order.id}</h3>
       <p>Date: ${new Date(order.createdAt).toLocaleDateString()}</p>
       <p>Total: ₹${order.total.toFixed(2)}</p>
       <p>Status: ${order.status}</p>
     </div>
   `).join('');
   ```

2. **Backend:** Add pagination:
   ```java
   @GetMapping("/history/{customerId}")
   public ResponseEntity<Page<OrderDTO>> getOrderHistory(
       @PathVariable Long customerId,
       @RequestParam(defaultValue = "0") int page,
       @RequestParam(defaultValue = "10") int size) {
       Page<Order> orders = orderRepository
           .findByCustomerIdOrderByCreatedAtDesc(customerId, PageRequest.of(page, size));
       return ResponseEntity.ok(orders.map(this::toDTO));
   }
   ```

3. **Repository:** Add ordering:
   ```java
   Page<Order> findByCustomerIdOrderByCreatedAtDesc(Long customerId, Pageable pageable);
   ```

4. **Database:** Add index:
   ```sql
   CREATE INDEX idx_orders_customer_id ON orders(customer_id);
   ```

### Checkpoint
- [ ] All past orders display on the history page
- [ ] Orders are sorted by date (newest first)
- [ ] Page loads within 2 seconds even with 100+ orders
- [ ] Pagination works (10 orders per page)

---

## Bug #4: Rating Submission Returns 500 Error (Cross-Stack)

**Priority:** P3 - Medium | **Points:** 8

### Affected Files

**Frontend -- rating.js**
```javascript
// BUG AREA: Rating submission
async function submitRating(restaurantId) {
  const ratingInput = document.getElementById('rating-input');
  // Bug 4a: Sending rating as string, allowing decimals
  const rating = ratingInput.value;

  // Bug 4b: No client-side validation
  const response = await fetch('/api/ratings', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      restaurantId: restaurantId,
      rating: rating,  // String "4.5" instead of integer
      comment: document.getElementById('comment').value
    })
  });

  // Bug 4c: Not checking response status
  const result = await response.json();
  showMessage('Rating submitted!');
}
```

**Backend -- RatingController.java**
```java
@PostMapping("/ratings")
public ResponseEntity<String> submitRating(@RequestBody RatingRequest request) {
    // Bug 4d: Integer.parseInt fails on decimal strings
    int rating = Integer.parseInt(request.getRating());

    // Bug 4e: No range validation
    ratingService.saveRating(
        request.getRestaurantId(),
        rating,
        request.getComment()
    );
    return ResponseEntity.ok("Rating saved");
}
```

**Database**
```sql
-- Bug 4f: TINYINT cannot store decimal ratings
CREATE TABLE ratings (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id BIGINT NOT NULL,
    rating TINYINT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Bugs to Find and Fix

| # | Hint | Layer |
|---|------|-------|
| 4a | Rating value is sent as a string instead of a number | Frontend |
| 4b | No client-side validation for rating range (1-5) | Frontend |
| 4c | Response status is not checked before showing success message | Frontend |
| 4d | `Integer.parseInt("4.5")` throws NumberFormatException | Backend |
| 4e | No validation that rating is between 1 and 5 | Backend |
| 4f | `TINYINT` column cannot store decimal values like 4.5 | Database |

### How to Fix

1. **Frontend:** Parse and validate before sending:
   ```javascript
   const ratingValue = parseInt(ratingInput.value, 10);
   if (isNaN(ratingValue) || ratingValue < 1 || ratingValue > 5) {
     showMessage('Please select a rating between 1 and 5');
     return;
   }
   // Send as integer
   body: JSON.stringify({ restaurantId, rating: ratingValue, comment: ... })
   ```

2. **Frontend:** Check response status:
   ```javascript
   if (!response.ok) {
     const error = await response.json();
     showMessage('Error: ' + error.message);
     return;
   }
   ```

3. **Backend:** Use proper parsing and validation:
   ```java
   int rating = (int) Math.round(Double.parseDouble(request.getRating()));
   if (rating < 1 || rating > 5) {
     return ResponseEntity.badRequest().body("Rating must be between 1 and 5");
   }
   ```

4. **Database:** Keep TINYINT (if integer scale) or alter to DECIMAL:
   ```sql
   -- Option A: Keep integer scale (1-5), no schema change needed
   -- Option B: Support half-stars
   ALTER TABLE ratings MODIFY COLUMN rating DECIMAL(2,1) NOT NULL;
   ```

### Checkpoint
- [ ] Rating submission succeeds with valid integer (1-5)
- [ ] Invalid ratings (0, 6, -1, "abc") show user-friendly error
- [ ] Decimal ratings are rounded or rejected consistently
- [ ] Success/error feedback is displayed to the user

---

## Bonus Challenge: API Contract Documentation

If your team finishes all 4 bugs early:

1. Create an OpenAPI/Swagger spec for the 3 endpoints you fixed
2. Add request/response schema validation middleware
3. Write a brief "API Contract" document listing:
   - Endpoint URL
   - HTTP method
   - Request body schema (with types)
   - Response body schema (with types)
   - Error response format

This prevents future cross-stack bugs caused by mismatched data formats.

---

## Submission Requirements

| Deliverable | Format |
|-------------|--------|
| Fixed code files | All layers (JS + Java + SQL) |
| Unit tests | At least 2 per bug |
| RCA document | 5 Whys for each bug |
| JIRA updates | Screenshots of ticket flow |
| Team presentation | 15-minute slide deck |
| Retrospective notes | What went well / what to improve |
