// FoodExpress Order Routes - Capsule
// Ticket 2: Fix input validation and error responses

const express = require('express');
const router = express.Router();
const { getDB } = require('../config/db');

// GET all orders
router.get('/', async (req, res, next) => {
  try {
    const db = getDB();
    const orders = await db.collection('orders').find({}).toArray();
    res.json(orders);
  } catch (err) {
    next(err);
  }
});

// GET order by id
router.get('/:id', async (req, res, next) => {
  try {
    const db = getDB();
    const order = await db.collection('orders').findOne({ orderId: req.params.id });

    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }
    res.json(order);
  } catch (err) {
    next(err);
  }
});

// POST create new order
router.post('/', async (req, res, next) => {
  try {
    const db = getDB();
    const { restaurantId, items, customerName, address } = req.body;

    // BUG: No input validation - missing fields will cause errors downstream
    // Expected: Validate that restaurantId, items (non-empty array), customerName are present
    // Return 400 with descriptive error if validation fails

    // BUG: When data is invalid, this throws an unhandled error returning 500
    // Expected: Return res.status(400).json({ error: '...' }) for invalid input
    const totalPrice = items.reduce((sum, item) => sum + item.price * item.qty, 0);

    const order = {
      orderId: `ord-${Date.now()}`,
      restaurantId,
      customerName,
      address,
      items,
      totalPrice,
      status: 'pending',
      createdAt: new Date()
    };

    await db.collection('orders').insertOne(order);
    res.status(201).json(order);
  } catch (err) {
    next(err);
  }
});

// PUT update order status
router.put('/:id/status', async (req, res, next) => {
  try {
    const db = getDB();
    const { status } = req.body;
    const validStatuses = ['pending', 'confirmed', 'preparing', 'delivering', 'delivered'];

    if (!validStatuses.includes(status)) {
      return res.status(400).json({
        error: `Invalid status. Must be one of: ${validStatuses.join(', ')}`
      });
    }

    const result = await db.collection('orders').updateOne(
      { orderId: req.params.id },
      { $set: { status, updatedAt: new Date() } }
    );
    res.json(result);
  } catch (err) {
    next(err);
  }
});

module.exports = router;
