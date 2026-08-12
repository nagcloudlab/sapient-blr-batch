// FoodExpress Error Handler Middleware - Capsule (Solution)
// Ticket 3: Fixed error handler signature

// FIX: Added 'err' as first parameter - Express requires exactly 4 params (err, req, res, next)
// to recognize this as error-handling middleware
function errorHandler(err, req, res, next) {
  console.error('FoodExpress Error:', err.message);

  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  res.status(statusCode).json({
    error: {
      message: message,
      status: statusCode,
      service: 'FoodExpress Capsule'
    }
  });
}

module.exports = errorHandler;
