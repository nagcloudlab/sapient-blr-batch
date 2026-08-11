const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'quickticket-secret';

// Auth middleware — verifies Bearer token
const authMiddleware = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
  } catch (err) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
};

// Error-handling middleware
const errorMiddleware = (req, res, next) => {
  console.error('Unhandled error:', req.message || 'Unknown error');
  res.status(500).json({ error: 'Something went wrong' });
};

module.exports = authMiddleware;
module.exports.errorMiddleware = errorMiddleware;
