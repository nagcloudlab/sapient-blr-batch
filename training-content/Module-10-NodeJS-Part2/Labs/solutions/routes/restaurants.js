// FoodExpress Restaurant Routes
// CRUD endpoints for restaurant management

const express = require('express');
const router = express.Router();
const Restaurant = require('../models/restaurant');

// GET all restaurants
router.get('/', async (req, res) => {
  try {
    const model = new Restaurant(req.app.locals.db);
    const restaurants = await model.findAll();
    res.json(restaurants);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// FIX: Moved /search route BEFORE /:id so it matches first
router.get('/search', async (req, res) => {
  try {
    const model = new Restaurant(req.app.locals.db);
    const results = await model.search(req.query.q);
    res.json(results);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET single restaurant by id
router.get('/:id', async (req, res) => {
  try {
    const model = new Restaurant(req.app.locals.db);
    const restaurant = await model.findById(req.params.id);
    if (!restaurant) {
      return res.status(404).json({ error: 'Restaurant not found' });
    }
    res.json(restaurant);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST new restaurant
router.post('/', async (req, res) => {
  try {
    const model = new Restaurant(req.app.locals.db);
    const result = await model.create(req.body);
    res.status(201).json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// FIX: Changed from GET to PUT for update (correct RESTful verb)
router.put('/:id', async (req, res) => {
  try {
    const model = new Restaurant(req.app.locals.db);
    const result = await model.update(req.params.id, req.body);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE restaurant
router.delete('/:id', async (req, res) => {
  try {
    const model = new Restaurant(req.app.locals.db);
    const result = await model.delete(req.params.id);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
