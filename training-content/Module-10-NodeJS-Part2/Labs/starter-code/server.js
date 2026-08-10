// FoodExpress Express Server
// Main entry point for the restaurant API

const express = require('express');
const { MongoClient } = require('mongodb');
const restaurantRoutes = require('./routes/restaurants');
const menuRoutes = require('./routes/menu');

const app = express();
const PORT = process.env.PORT || 3000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017';

// BUG: express.json() middleware is missing - req.body will be undefined for POST/PUT
// Expected: Add app.use(express.json()) to parse JSON request bodies

app.use('/api/restaurants', restaurantRoutes);
app.use('/api/menu', menuRoutes);

app.get('/', (req, res) => {
  res.json({
    service: 'FoodExpress Restaurant API',
    version: '1.0.0',
    endpoints: ['/api/restaurants', '/api/menu']
  });
});

async function startServer() {
  try {
    const client = await MongoClient.connect(MONGO_URI);
    const db = client.db('foodexpress');
    console.log('Connected to MongoDB');

    app.locals.db = db;

    app.listen(PORT, () => {
      console.log(`FoodExpress API running on port ${PORT}`);
    });
  } catch (err) {
    console.error('Failed to start server:', err.message);
    process.exit(1);
  }
}

startServer();
