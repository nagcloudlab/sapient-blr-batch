# Node.js (Part 2)
## Module 10 | Sustain Engineering Training | Day 11

**0.5 day | Workshop + guided lab**

---

## Agenda

| Session | Topics |
|---------|--------|
| First half | Express.js, Routing, HTTP Verbs (GET/POST/PUT/DELETE), Middleware |
| Second half | Intro to MongoDB, CRUD Operations, Data Modelling, Indexing |

> Building REST APIs with Express.js and persisting data with MongoDB.

---

## What Is Express.js?

- **Minimal, unopinionated** web framework for Node.js
- De facto standard for building APIs in Node.js
- Provides routing, middleware, request/response handling

### Express vs Raw HTTP

```javascript
// Raw Node.js HTTP server (verbose)
const http = require('http');
const server = http.createServer((req, res) => {
    if (req.method === 'GET' && req.url === '/restaurants') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ data: [] }));
    }
});
server.listen(3000);

// Express (clean, maintainable)
const express = require('express');
const app = express();

app.get('/restaurants', (req, res) => {
    res.json({ data: [] });
});

app.listen(3000);
```

---

## Setting Up Express

### Installation

```bash
mkdir foodexpress-api && cd foodexpress-api
npm init -y
npm install express
npm install --save-dev nodemon
```

### package.json Scripts

```json
{
  "scripts": {
    "start": "node src/index.js",
    "dev": "nodemon src/index.js"
  }
}
```

### Basic Server

```javascript
// src/index.js
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Parse JSON request bodies
app.use(express.json());

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.listen(PORT, () => {
    console.log(`FoodExpress API running on port ${PORT}`);
});
```

---

## HTTP Verbs and REST

### RESTful API Design

| HTTP Verb | CRUD Operation | URL Pattern | Purpose |
|-----------|---------------|-------------|---------|
| `GET` | Read | `/restaurants` | List all restaurants |
| `GET` | Read | `/restaurants/:id` | Get one restaurant |
| `POST` | Create | `/restaurants` | Add new restaurant |
| `PUT` | Update (full) | `/restaurants/:id` | Replace a restaurant |
| `PATCH` | Update (partial) | `/restaurants/:id` | Update specific fields |
| `DELETE` | Delete | `/restaurants/:id` | Remove a restaurant |

### Response Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| `200` | OK | Successful GET, PUT, PATCH |
| `201` | Created | Successful POST |
| `204` | No Content | Successful DELETE |
| `400` | Bad Request | Invalid input |
| `404` | Not Found | Resource doesn't exist |
| `500` | Internal Server Error | Unexpected server error |

---

## Express Routing -- GET

```javascript
const express = require('express');
const app = express();

// In-memory data store (replaced by MongoDB later)
let restaurants = [
    { id: '1', name: 'Pizza Palace', category: 'Italian', rating: 4.5 },
    { id: '2', name: 'Wok Express', category: 'Chinese', rating: 4.2 },
    { id: '3', name: 'Curry House', category: 'Indian', rating: 4.8 }
];

// GET all restaurants
app.get('/api/restaurants', (req, res) => {
    res.json({ count: restaurants.length, data: restaurants });
});

// GET restaurant by ID (route parameter)
app.get('/api/restaurants/:id', (req, res) => {
    const restaurant = restaurants.find(r => r.id === req.params.id);
    if (!restaurant) {
        return res.status(404).json({ error: 'Restaurant not found' });
    }
    res.json(restaurant);
});

// GET with query parameters: /api/restaurants?category=Italian&minRating=4.0
app.get('/api/restaurants', (req, res) => {
    let result = restaurants;
    if (req.query.category) {
        result = result.filter(r => r.category === req.query.category);
    }
    if (req.query.minRating) {
        result = result.filter(r => r.rating >= parseFloat(req.query.minRating));
    }
    res.json({ count: result.length, data: result });
});
```

---

## Express Routing -- POST

```javascript
app.use(express.json());  // Required to parse JSON body

// POST -- create new restaurant
app.post('/api/restaurants', (req, res) => {
    const { name, category, rating } = req.body;

    // Validate input
    if (!name || !category) {
        return res.status(400).json({
            error: 'Validation failed',
            details: 'name and category are required'
        });
    }

    const newRestaurant = {
        id: String(Date.now()),
        name,
        category,
        rating: rating || 0,
        createdAt: new Date().toISOString()
    };

    restaurants.push(newRestaurant);
    res.status(201).json(newRestaurant);
});
```

### Testing with curl

```bash
curl -X POST http://localhost:3000/api/restaurants \
  -H "Content-Type: application/json" \
  -d '{"name": "Sushi Bar", "category": "Japanese", "rating": 4.6}'
```

---

## Express Routing -- PUT and DELETE

### PUT -- Full Update

```javascript
app.put('/api/restaurants/:id', (req, res) => {
    const index = restaurants.findIndex(r => r.id === req.params.id);
    if (index === -1) {
        return res.status(404).json({ error: 'Restaurant not found' });
    }

    const { name, category, rating } = req.body;
    if (!name || !category) {
        return res.status(400).json({ error: 'name and category are required' });
    }

    restaurants[index] = {
        ...restaurants[index],
        name,
        category,
        rating: rating || restaurants[index].rating
    };

    res.json(restaurants[index]);
});
```

### DELETE

```javascript
app.delete('/api/restaurants/:id', (req, res) => {
    const index = restaurants.findIndex(r => r.id === req.params.id);
    if (index === -1) {
        return res.status(404).json({ error: 'Restaurant not found' });
    }

    restaurants.splice(index, 1);
    res.status(204).send();  // No content
});
```

---

## Express Middleware

### What Is Middleware?

Functions that have access to `req`, `res`, and `next`. They execute **in order**.

```
Request --> Middleware 1 --> Middleware 2 --> Route Handler --> Response
```

### Built-in Middleware

```javascript
// Parse JSON bodies
app.use(express.json());

// Parse URL-encoded bodies (form data)
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static('public'));
```

### Custom Middleware: Request Logger

```javascript
function requestLogger(req, res, next) {
    const start = Date.now();
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);

    res.on('finish', () => {
        const duration = Date.now() - start;
        console.log(`[${new Date().toISOString()}] ${req.method} ${req.url} ${res.statusCode} ${duration}ms`);
    });

    next();  // Pass control to next middleware
}

app.use(requestLogger);
```

---

## More Middleware Patterns

### Error Handling Middleware

```javascript
// Error handler (4 parameters -- Express recognizes this as error middleware)
function errorHandler(err, req, res, next) {
    console.error('Error:', err.message);
    console.error('Stack:', err.stack);

    const statusCode = err.statusCode || 500;
    res.status(statusCode).json({
        error: err.message || 'Internal Server Error',
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    });
}

// Must be registered LAST
app.use(errorHandler);
```

### Validation Middleware

```javascript
function validateRestaurant(req, res, next) {
    const { name, category } = req.body;
    const errors = [];

    if (!name || name.trim().length === 0) errors.push('name is required');
    if (!category) errors.push('category is required');
    if (req.body.rating && (req.body.rating < 0 || req.body.rating > 5)) {
        errors.push('rating must be between 0 and 5');
    }

    if (errors.length > 0) {
        return res.status(400).json({ error: 'Validation failed', details: errors });
    }
    next();
}

// Apply to specific routes
app.post('/api/restaurants', validateRestaurant, (req, res) => { /* ... */ });
app.put('/api/restaurants/:id', validateRestaurant, (req, res) => { /* ... */ });
```

---

## Express Router -- Organizing Routes

```javascript
// src/routes/restaurantRoutes.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    // GET /api/restaurants
    res.json({ data: restaurants });
});

router.get('/:id', (req, res) => {
    // GET /api/restaurants/:id
    const restaurant = findById(req.params.id);
    if (!restaurant) return res.status(404).json({ error: 'Not found' });
    res.json(restaurant);
});

router.post('/', (req, res) => {
    // POST /api/restaurants
    const newRestaurant = createRestaurant(req.body);
    res.status(201).json(newRestaurant);
});

module.exports = router;
```

```javascript
// src/index.js
const restaurantRoutes = require('./routes/restaurantRoutes');
const menuRoutes = require('./routes/menuRoutes');

app.use('/api/restaurants', restaurantRoutes);
app.use('/api/menu', menuRoutes);
```

---

## FoodExpress: Complete API Structure

```
foodexpress-api/
  src/
    index.js                # App entry point
    routes/
      restaurantRoutes.js   # /api/restaurants
      menuRoutes.js         # /api/menu
      orderRoutes.js        # /api/orders
    middleware/
      logger.js             # Request logging
      errorHandler.js       # Error handling
      validator.js          # Input validation
    models/
      Restaurant.js         # Mongoose model
      MenuItem.js           # Mongoose model
    config/
      database.js           # MongoDB connection
  package.json
  .env                      # Environment variables
```

---

## Introduction to MongoDB

### What Is MongoDB?

- **NoSQL** document database
- Stores data as **JSON-like documents** (BSON)
- Schema-flexible -- no fixed table structure
- Horizontally scalable
- Great for: APIs, content management, real-time analytics

### MongoDB vs SQL

| Concept | SQL (MySQL) | MongoDB |
|---------|------------|---------|
| Database | Database | Database |
| Table | Table | Collection |
| Row | Row | Document |
| Column | Column | Field |
| Primary Key | `id INT` | `_id ObjectId` |
| Join | `JOIN` clause | `$lookup` or embed |
| Schema | Fixed, enforced | Flexible, optional |

---

## MongoDB Documents

### Document Structure (JSON/BSON)

```json
{
    "_id": "ObjectId('64f1a2b3c4d5e6f7a8b9c0d1')",
    "name": "Pizza Palace",
    "category": "Italian",
    "address": {
        "street": "123 Main St",
        "city": "Bangalore",
        "pincode": "560001"
    },
    "menu": [
        { "name": "Margherita", "price": 299, "vegetarian": true },
        { "name": "Pepperoni", "price": 399, "vegetarian": false }
    ],
    "rating": 4.5,
    "isActive": true,
    "createdAt": "2024-01-15T10:30:00Z"
}
```

### Key Differences from SQL

- Documents can have **nested objects** (address)
- Documents can have **arrays** (menu items)
- Documents in the same collection can have **different fields**
- No need for JOINs when data is embedded

---

## Mongoose -- MongoDB ODM

### What Is Mongoose?

- **Object Document Mapper** for MongoDB and Node.js
- Provides schema validation, type casting, query building
- Similar to JPA/Hibernate in Java

### Installation

```bash
npm install mongoose
```

### Connection

```javascript
// src/config/database.js
const mongoose = require('mongoose');

async function connectDB() {
    try {
        await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/foodexpress');
        console.log('Connected to MongoDB');
    } catch (err) {
        console.error('MongoDB connection error:', err.message);
        process.exit(1);
    }
}

module.exports = connectDB;
```

```javascript
// src/index.js
const connectDB = require('./config/database');
connectDB();
```

---

## Mongoose Schema and Model

```javascript
// src/models/Restaurant.js
const mongoose = require('mongoose');

const menuItemSchema = new mongoose.Schema({
    name: { type: String, required: true },
    price: { type: Number, required: true, min: 0 },
    category: { type: String },
    vegetarian: { type: Boolean, default: false },
    available: { type: Boolean, default: true }
});

const restaurantSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, 'Restaurant name is required'],
        trim: true,
        maxlength: 100
    },
    category: {
        type: String,
        required: true,
        enum: ['Italian', 'Chinese', 'Indian', 'Japanese', 'Mexican', 'American']
    },
    address: {
        street: String,
        city: String,
        pincode: String
    },
    menu: [menuItemSchema],      // Embedded array of subdocuments
    rating: {
        type: Number,
        default: 0,
        min: 0,
        max: 5
    },
    isActive: { type: Boolean, default: true }
}, {
    timestamps: true  // Adds createdAt and updatedAt automatically
});

module.exports = mongoose.model('Restaurant', restaurantSchema);
```

---

## MongoDB CRUD -- Create

```javascript
const Restaurant = require('./models/Restaurant');

// Create a single document
async function createRestaurant() {
    const restaurant = new Restaurant({
        name: 'Pizza Palace',
        category: 'Italian',
        address: { street: '123 Main St', city: 'Bangalore', pincode: '560001' },
        menu: [
            { name: 'Margherita', price: 299, vegetarian: true },
            { name: 'Pepperoni', price: 399, vegetarian: false }
        ],
        rating: 4.5
    });

    const saved = await restaurant.save();
    console.log('Created:', saved._id);
    return saved;
}

// Alternative: Model.create()
const restaurant = await Restaurant.create({
    name: 'Wok Express',
    category: 'Chinese',
    rating: 4.2
});

// Create multiple
const restaurants = await Restaurant.insertMany([
    { name: 'Curry House', category: 'Indian', rating: 4.8 },
    { name: 'Sushi Bar', category: 'Japanese', rating: 4.6 }
]);
```

---

## MongoDB CRUD -- Read

```javascript
// Find all
const allRestaurants = await Restaurant.find();

// Find with filter
const italianPlaces = await Restaurant.find({ category: 'Italian' });

// Find one by ID
const restaurant = await Restaurant.findById('64f1a2b3c4d5e6f7a8b9c0d1');

// Find one by condition
const topRated = await Restaurant.findOne({ rating: { $gte: 4.5 } });

// Query with operators
const results = await Restaurant.find({
    category: { $in: ['Italian', 'Indian'] },
    rating: { $gte: 4.0 },
    isActive: true
});

// Select specific fields (projection)
const names = await Restaurant.find({}, 'name category rating');

// Sort, limit, skip (pagination)
const page1 = await Restaurant.find()
    .sort({ rating: -1 })     // Descending by rating
    .skip(0)                   // Skip 0 for page 1
    .limit(10);                // 10 per page

// Count
const count = await Restaurant.countDocuments({ category: 'Italian' });
```

---

## MongoDB Query Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `$eq` | Equal | `{ rating: { $eq: 5 } }` |
| `$ne` | Not equal | `{ category: { $ne: 'Italian' } }` |
| `$gt` / `$gte` | Greater than / or equal | `{ rating: { $gte: 4.0 } }` |
| `$lt` / `$lte` | Less than / or equal | `{ price: { $lt: 500 } }` |
| `$in` | In array | `{ category: { $in: ['Italian', 'Indian'] } }` |
| `$nin` | Not in array | `{ category: { $nin: ['Chinese'] } }` |
| `$exists` | Field exists | `{ phone: { $exists: true } }` |
| `$regex` | Pattern match | `{ name: { $regex: /pizza/i } }` |
| `$and` | Logical AND | `{ $and: [{ rating: { $gte: 4 } }, { isActive: true }] }` |
| `$or` | Logical OR | `{ $or: [{ category: 'Italian' }, { category: 'Indian' }] }` |

```javascript
// Search restaurants by name (case-insensitive)
const results = await Restaurant.find({
    name: { $regex: req.query.search, $options: 'i' }
});
```

---

## MongoDB CRUD -- Update

```javascript
// Update one document
await Restaurant.findByIdAndUpdate(
    '64f1a2b3c4d5e6f7a8b9c0d1',
    { rating: 4.7 },
    { new: true, runValidators: true }  // Return updated doc, validate
);

// Update with operators
await Restaurant.findByIdAndUpdate(id, {
    $set: { rating: 4.7, 'address.city': 'Mumbai' },
    $push: { menu: { name: 'Garlic Bread', price: 149, vegetarian: true } }
});

// Update many
await Restaurant.updateMany(
    { isActive: false },
    { $set: { isActive: true } }
);
```

### Update Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `$set` | Set field value | `{ $set: { rating: 4.5 } }` |
| `$unset` | Remove a field | `{ $unset: { phone: "" } }` |
| `$inc` | Increment value | `{ $inc: { orderCount: 1 } }` |
| `$push` | Add to array | `{ $push: { menu: newItem } }` |
| `$pull` | Remove from array | `{ $pull: { menu: { name: 'Pasta' } } }` |
| `$addToSet` | Add unique to array | `{ $addToSet: { tags: 'popular' } }` |

---

## MongoDB CRUD -- Delete

```javascript
// Delete one by ID
await Restaurant.findByIdAndDelete('64f1a2b3c4d5e6f7a8b9c0d1');

// Delete one by condition
await Restaurant.deleteOne({ name: 'Closed Restaurant' });

// Delete many
const result = await Restaurant.deleteMany({ isActive: false });
console.log(`Deleted ${result.deletedCount} inactive restaurants`);
```

### Soft Delete Pattern (Recommended for Sustain)

```javascript
// Instead of actually deleting, mark as inactive
async function softDelete(id) {
    const restaurant = await Restaurant.findByIdAndUpdate(
        id,
        {
            $set: {
                isActive: false,
                deletedAt: new Date()
            }
        },
        { new: true }
    );
    return restaurant;
}

// Always filter out soft-deleted records in queries
const activeRestaurants = await Restaurant.find({ isActive: true });
```

> **Sustain tip:** In production systems, prefer soft delete. Data recovery is much easier.

---

## Data Modelling -- Embedding vs Referencing

### Embedding (Denormalized)

```javascript
// Menu items embedded inside restaurant document
{
    name: "Pizza Palace",
    menu: [
        { name: "Margherita", price: 299 },
        { name: "Pepperoni", price: 399 }
    ]
}
```

### Referencing (Normalized)

```javascript
// Restaurant document
{ _id: "REST001", name: "Pizza Palace", menu: ["ITEM001", "ITEM002"] }

// Separate MenuItem documents
{ _id: "ITEM001", name: "Margherita", price: 299, restaurantId: "REST001" }
{ _id: "ITEM002", name: "Pepperoni", price: 399, restaurantId: "REST001" }
```

### When to Use Which?

| Criteria | Embed | Reference |
|----------|-------|-----------|
| Data accessed together? | Yes -- embed | No -- reference |
| Data changes frequently? | Embed (few updates) | Reference (frequent updates) |
| Array size? | Small (< 100 items) | Large or unbounded |
| Need to query independently? | No | Yes |
| One-to-few | Embed | -- |
| One-to-many | Embed or reference | Reference |
| Many-to-many | -- | Reference |

---

## Populate -- Joining Referenced Documents

```javascript
// Order model with references
const orderSchema = new mongoose.Schema({
    customer: { type: String, required: true },
    restaurant: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Restaurant',      // Reference to Restaurant model
        required: true
    },
    items: [{
        menuItem: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'MenuItem'
        },
        quantity: Number
    }],
    total: Number,
    status: {
        type: String,
        enum: ['pending', 'confirmed', 'preparing', 'delivered', 'cancelled'],
        default: 'pending'
    }
}, { timestamps: true });

// Query with populate (like SQL JOIN)
const order = await Order.findById(orderId)
    .populate('restaurant', 'name category')    // Only get name and category
    .populate('items.menuItem', 'name price');   // Populate nested ref
```

---

## MongoDB Indexing

### Why Indexes?

Without indexes, MongoDB scans **every document** (collection scan). With indexes, it jumps directly to matching documents.

```javascript
// Create indexes in Mongoose schema
const restaurantSchema = new mongoose.Schema({
    name: { type: String, index: true },          // Single field index
    category: String,
    rating: Number,
    location: {
        type: { type: String, default: 'Point' },
        coordinates: [Number]
    }
});

// Compound index (queries on both fields)
restaurantSchema.index({ category: 1, rating: -1 });

// Unique index
restaurantSchema.index({ name: 1 }, { unique: true });

// Text index (full-text search)
restaurantSchema.index({ name: 'text', 'menu.name': 'text' });
```

### Index Types

| Type | Use Case | Example |
|------|----------|---------|
| Single field | Filter by one field | `{ category: 1 }` |
| Compound | Filter by multiple fields | `{ category: 1, rating: -1 }` |
| Unique | Prevent duplicates | `{ email: 1 }, { unique: true }` |
| Text | Full-text search | `{ name: 'text' }` |
| TTL | Auto-expire documents | `{ createdAt: 1 }, { expireAfterSeconds: 3600 }` |

---

## Index Best Practices

### Check Query Performance

```javascript
// Explain query execution plan
const explanation = await Restaurant.find({ category: 'Italian' }).explain('executionStats');
console.log(explanation.executionStats);
// Look for: totalDocsExamined vs nReturned
// Ideal: totalDocsExamined === nReturned (no unnecessary scans)
```

### Rules of Thumb

| Rule | Why |
|------|-----|
| Index fields used in `find()` filters | Speed up reads |
| Index fields used in `sort()` | Avoid in-memory sorting |
| Don't over-index | Each index slows writes |
| Compound index field order matters | Most selective field first |
| Monitor with `explain()` | Verify indexes are used |

> **Sustain tip:** Missing indexes are the #1 cause of slow MongoDB queries in production. Always check `explain()` output.

---

## Putting It All Together: Express + MongoDB

```javascript
// src/routes/restaurantRoutes.js
const express = require('express');
const router = express.Router();
const Restaurant = require('../models/Restaurant');

// GET all restaurants
router.get('/', async (req, res, next) => {
    try {
        const { category, minRating, page = 1, limit = 10 } = req.query;
        const filter = { isActive: true };
        if (category) filter.category = category;
        if (minRating) filter.rating = { $gte: parseFloat(minRating) };

        const restaurants = await Restaurant.find(filter)
            .sort({ rating: -1 })
            .skip((page - 1) * limit)
            .limit(parseInt(limit));

        const total = await Restaurant.countDocuments(filter);

        res.json({
            data: restaurants,
            pagination: { page: parseInt(page), limit: parseInt(limit), total }
        });
    } catch (err) {
        next(err);
    }
});

// POST create restaurant
router.post('/', async (req, res, next) => {
    try {
        const restaurant = await Restaurant.create(req.body);
        res.status(201).json(restaurant);
    } catch (err) {
        if (err.name === 'ValidationError') {
            return res.status(400).json({ error: err.message });
        }
        next(err);
    }
});

module.exports = router;
```

---

## Lab: FoodExpress Restaurant API

### Objective

Build a complete REST API for the FoodExpress Restaurant Service using Express.js and MongoDB.

### Tasks

1. **Project Setup:**
   - Initialize Node.js project with Express and Mongoose
   - Create folder structure: `src/`, `routes/`, `models/`, `middleware/`, `config/`
   - Connect to MongoDB

2. **Restaurant Model:**
   - Fields: name, category, address (embedded), menu (embedded array), rating, isActive
   - Validation: name required, category from enum, rating 0-5

3. **CRUD API Endpoints:**
   - `GET /api/restaurants` -- list all (with filtering, sorting, pagination)
   - `GET /api/restaurants/:id` -- get by ID
   - `POST /api/restaurants` -- create new
   - `PUT /api/restaurants/:id` -- update
   - `DELETE /api/restaurants/:id` -- soft delete

4. **Menu Endpoints:**
   - `POST /api/restaurants/:id/menu` -- add menu item
   - `DELETE /api/restaurants/:id/menu/:itemId` -- remove menu item

---

## Lab: Continued

### Tasks (continued)

5. **Middleware:**
   - Request logger (log method, URL, status code, duration)
   - Error handler (catch all errors, return proper JSON)
   - Input validator for restaurant creation

6. **Indexing:**
   - Add index on `category` field
   - Add compound index on `category` + `rating`
   - Verify with `explain()`

### Acceptance Criteria

- [ ] All 6 CRUD endpoints work correctly
- [ ] Proper HTTP status codes (200, 201, 204, 400, 404)
- [ ] Input validation with meaningful error messages
- [ ] MongoDB connected with error handling
- [ ] Soft delete (not hard delete)
- [ ] Pagination on list endpoint
- [ ] At least 2 indexes created

---

## Key Takeaways

| Topic | Key Point |
|-------|-----------|
| Express.js | Minimal web framework; routing, middleware, req/res handling |
| HTTP Verbs | GET (read), POST (create), PUT (update), DELETE (remove) |
| Middleware | Functions in the request pipeline; logging, validation, errors |
| Express Router | Organize routes into separate files by resource |
| MongoDB | NoSQL document database; flexible schema, JSON-like documents |
| Mongoose | ODM for MongoDB; schemas, models, validation |
| CRUD | create(), find(), findByIdAndUpdate(), findByIdAndDelete() |
| Data Modelling | Embed for small, related data; reference for large, independent data |
| Indexing | Speed up queries; always check with explain() |
| Soft Delete | Mark inactive instead of removing; safer for production |

> **Next: Module 11 -- Linux Fundamentals (server administration for sustain engineers)**
