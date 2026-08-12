// FoodExpress Menu Routes
// Endpoints for managing restaurant menus

const express = require('express');
const router = express.Router();

// GET menu for a restaurant
router.get('/:restaurantId', async (req, res) => {
  try {
    const db = req.app.locals.db;
    // FIX: Changed field name from 'restaurantId' to 'id' to match data schema
    const restaurant = await db.collection('restaurants')
      .findOne({ id: req.params.restaurantId });

    if (!restaurant) {
      return res.status(404).json({ error: 'Restaurant not found' });
    }
    res.json(restaurant.menu);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST add item to menu
router.post('/:restaurantId/items', async (req, res) => {
  try {
    const db = req.app.locals.db;
    const { item, price, category } = req.body;

    const result = await db.collection('restaurants').updateOne(
      { id: req.params.restaurantId },
      { $push: { menu: { item, price, category } } }
    );
    res.status(201).json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// PUT update a menu item's price
router.put('/:restaurantId/items/:itemName', async (req, res) => {
  try {
    const db = req.app.locals.db;
    const { price } = req.body;

    // FIX: Changed $push to $set with positional operator to update price
    const result = await db.collection('restaurants').updateOne(
      { id: req.params.restaurantId, 'menu.item': req.params.itemName },
      { $set: { 'menu.$.price': price } }
    );
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE a menu item
router.delete('/:restaurantId/items/:itemName', async (req, res) => {
  try {
    const db = req.app.locals.db;
    const result = await db.collection('restaurants').updateOne(
      { id: req.params.restaurantId },
      { $pull: { menu: { item: req.params.itemName } } }
    );
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
