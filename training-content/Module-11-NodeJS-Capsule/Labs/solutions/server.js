// FoodExpress Capsule Server
// Full project combining Express + MongoDB + Error Handling

const express = require('express');
const { connectDB } = require('./config/db');
const restaurantRoutes = require('./routes/restaurants');
const orderRoutes = require('./routes/orders');
const errorHandler = require('./middleware/errorHandler');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({
    service: 'FoodExpress Capsule API',
    version: '1.0.0',
    endpoints: ['/api/restaurants', '/api/orders']
  });
});

app.use('/api/restaurants', restaurantRoutes);
app.use('/api/orders', orderRoutes);

// Error handling middleware (must be last)
app.use(errorHandler);

async function start() {
  try {
    await connectDB();
    app.listen(PORT, () => {
      console.log(`FoodExpress Capsule running on port ${PORT}`);
    });
  } catch (err) {
    console.error('Startup failed:', err.message);
    process.exit(1);
  }
}

start();
