// FoodExpress Order Routes - Capsule (Solution)
// Ticket 2: Fixed input validation and error responses

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

    // FIX: Added input validation with 400 response for missing/invalid fields
    if (!restaurantId) {
      return res.status(400).json({ error: 'restaurantId is required' });
    }
    if (!customerName) {
      return res.status(400).json({ error: 'customerName is required' });
    }
    if (!items || !Array.isArray(items) || items.length === 0) {
      return res.status(400).json({ error: 'items must be a non-empty array' });
    }

    // FIX: Safe price calculation after validation ensures items exist
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
