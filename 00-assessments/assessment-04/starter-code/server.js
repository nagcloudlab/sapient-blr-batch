const express = require('express');
const mongoose = require('mongoose');

const authRoutes = require('./routes/auth');
const eventRoutes = require('./routes/events');
const authMiddleware = require('./middleware/auth');

const app = express();

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Public routes
app.use('/api/auth', authRoutes);

// Protected routes — auth middleware applied
app.use('/api/events', authMiddleware, eventRoutes);

// Error handling middleware — must be last
// BUG: wrong signature — should be (err, req, res, next)
app.use((req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// Database connection
mongoose.connect('mongodb://localhost:27017/quickticket')
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`QuickTicket API running on port ${PORT}`);
});

module.exports = app;
