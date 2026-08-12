# FoodExpress Architecture

## System Overview

FoodExpress is a food delivery platform with a microservices architecture:

```
                    +------------------+
                    |   Web Frontend   |
                    | (HTML/CSS/JS/    |
                    |  React)          |
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
     +--------v---+  +------v------+  +----v--------+
     | Restaurant |  |    Cart     |  |    Order     |
     | Service    |  |   Service   |  |   Service    |
     | (Node.js)  |  | (Node.js)  |  |   (Java)     |
     | Port: 3000 |  | Port: 3001 |  | Port: 8080   |
     +--------+---+  +------+------+  +----+----+---+
              |              |              |    |
     +--------v---+  +------v------+  +----v-+  +---v-------+
     |  MongoDB   |  |  MongoDB   |  | MySQL|  | Delivery   |
     | (menus,    |  | (carts,    |  |(orders|  | Service    |
     | restaurants)|  | sessions) |  | items)|  | (Node.js)  |
     +------------+  +------------+  +------+  | Port: 3002 |
                                                +------+-----+
                                                       |
                                               +-------v-----+
                                               |   MongoDB    |
                                               | (deliveries, |
                                               |  tracking)   |
                                               +--------------+
```

## Services

### Frontend (HTML/CSS/JS -> React)
- Restaurant browsing and search
- Menu display with categories
- Cart management
- Order placement and tracking
- Delivery status tracking

### Restaurant Service (Node.js, Port 3000)
- Restaurant listing with filters (cuisine, rating, location)
- Menu items per restaurant
- Search (by name, cuisine type)
- Stock/availability management per restaurant

### Cart Service (Node.js, Port 3001)
- Add/remove/update cart items
- Session-based cart persistence
- Discount code application
- Cart total calculation with delivery fees

### Order Service (Java Spring Boot, Port 8080)
- Order creation and management
- Order status lifecycle: PLACED -> CONFIRMED -> PREPARING -> READY -> PICKED_UP -> DELIVERED
- Order history per customer
- Revenue and reporting queries

### Delivery Service (Node.js, Port 3002)
- Delivery assignment
- Real-time delivery tracking (ETA)
- Delivery status updates
- Driver management

### Payment Service (Node.js, Port 3003)
- Payment processing via external gateway
- Payment status tracking
- Refund processing

## Database Schema

### MongoDB (Restaurant Service)
- `restaurants` collection: name, address, cuisine, rating, hours, isOpen
- `menuItems` collection: restaurantId, name, description, price, category, image, stock, isAvailable

### MongoDB (Cart Service)
- `carts` collection: sessionId, items[], discountCode, createdAt, updatedAt

### MySQL (Order Service)
- `customers` table: id, name, email, phone, address
- `orders` table: id, customerId, restaurantId, status, subtotal, deliveryFee, discount, total, createdAt
- `order_items` table: id, orderId, menuItemId, name, price, quantity, itemTotal
- `order_status_history` table: id, orderId, status, changedAt

### MongoDB (Delivery Service)
- `deliveries` collection: orderId, driverId, pickupAddress, deliveryAddress, status, estimatedTime, actualTime

## FoodExpress Menu Categories

| Restaurant | Cuisine | Sample Items |
|-----------|---------|-------------|
| Burger Barn | American | Classic Burger ($8.99), Cheese Fries ($4.99), Milkshake ($5.99) |
| Pizza Palace | Italian | Margherita ($12.99), Pepperoni ($14.99), Garlic Bread ($3.99) |
| Dragon Wok | Chinese | Fried Rice ($9.99), Spring Rolls ($5.99), Kung Pao Chicken ($11.99) |
| Spice Route | Indian | Butter Chicken ($13.99), Naan ($2.99), Biryani ($11.99) |
| Fresh & Green | Healthy | Caesar Salad ($7.99), Smoothie Bowl ($8.99), Quinoa Wrap ($9.99) |
| Sweet Tooth | Desserts | Chocolate Cake ($6.99), Ice Cream Sundae ($5.99), Cheesecake ($7.99) |
