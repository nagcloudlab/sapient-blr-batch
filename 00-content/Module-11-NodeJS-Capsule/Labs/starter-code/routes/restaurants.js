// FoodExpress Restaurant Routes - Capsule
// Ticket 1: Fix async/await and search issues

const express = require('express');
const router = express.Router();
const { getDB } = require('../config/db');

// GET all restaurants
router.get('/', async (req, res, next) => {
  try {
    const db = getDB();
    const restaurants = await db.collection('restaurants').find({}).toArray();
    res.json(restaurants);
  } catch (err) {
    next(err);
  }
});

// GET search restaurants by name
router.get('/search', async (req, res, next) => {
  try {
    const db = getDB();
    const query = req.query.q;

    if (!query) {
      return res.status(400).json({ error: 'Search query (q) is required' });
    }

    // BUG: Case-sensitive search - searching "food" won't find "FoodExpress"
    // Expected: Use $options: 'i' for case-insensitive regex matching
    const results = await db.collection('restaurants')
      .find({ name: { $regex: query } })
      .toArray();

    res.json(results);
  } catch (err) {
    next(err);
  }
});

// GET restaurant by id
router.get('/:id', async (req, res, next) => {
  try {
    const db = getDB();
    // BUG: Missing await on async DB call - returns a Promise instead of the document
    // Expected: Add await before db.collection(...).findOne(...)
    const restaurant = db.collection('restaurants').findOne({ id: req.params.id });

    if (!restaurant) {
      return res.status(404).json({ error: 'Restaurant not found' });
    }
    res.json(restaurant);
  } catch (err) {
    next(err);
  }
});

// POST create a restaurant
router.post('/', async (req, res, next) => {
  try {
    const db = getDB();
    const { id, name, cuisine, rating, menu, deliveryTime } = req.body;

    const newRestaurant = {
      id, name, cuisine, rating,
      menu: menu || [],
      isOpen: true,
      deliveryTime: deliveryTime || 30
    };

    await db.collection('restaurants').insertOne(newRestaurant);
    res.status(201).json(newRestaurant);
  } catch (err) {
    next(err);
  }
});

module.exports = router;
