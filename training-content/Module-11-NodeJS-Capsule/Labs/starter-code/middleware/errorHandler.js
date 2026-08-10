// FoodExpress Error Handler Middleware - Capsule
// Ticket 3: Fix error handler signature

// BUG: Error handler has 3 parameters instead of 4
// Expected: Express error middleware MUST have exactly 4 parameters (err, req, res, next)
// With only 3 params, Express treats this as regular middleware and skips it for errors
function errorHandler(req, res, next) {
  console.error('FoodExpress Error:', req.message);

  const statusCode = req.statusCode || 500;
  const message = req.message || 'Internal Server Error';

  res.status(statusCode).json({
    error: {
      message: message,
      status: statusCode,
      service: 'FoodExpress Capsule'
    }
  });
}

module.exports = errorHandler;
