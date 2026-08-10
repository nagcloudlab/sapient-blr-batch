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

// BUG: Route order is wrong - /search is AFTER /:id, so "search" matches as an id
// Expected: Move /search route BEFORE /:id so it matches first
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

// This route will never be reached because /:id catches "search" first
router.get('/search', async (req, res) => {
  try {
    const model = new Restaurant(req.app.locals.db);
    const results = await model.search(req.query.q);
    res.json(results);
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

// BUG: Wrong HTTP verb - using GET instead of PUT for update
// Expected: router.put('/:id', ...) for updating a restaurant
router.get('/:id/update', async (req, res) => {
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
