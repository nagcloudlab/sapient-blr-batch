const express = require('express');
const app = express();

app.use(express.json());

const PORT = 4000;

// Charge endpoint
app.post('/charge', (req, res) => {
  const { bookingId, amount, method } = req.body;

  // Simulate 503 when X-Fail header is set (for testing DEF-303)
  if (req.headers['x-fail'] === 'true') {
    return res.status(503).json({ error: 'Service temporarily unavailable' });
  }

  res.json({
    paymentId: `pay-${Date.now()}`,
    bookingId,
    amount,
    method,
    status: 'charged',
    timestamp: new Date().toISOString()
  });
});

// Refund endpoint
app.post('/refund', (req, res) => {
  const { paymentId } = req.body;

  res.json({
    refundId: `ref-${Date.now()}`,
    paymentId,
    status: 'refunded',
    timestamp: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log(`Payment service running on port ${PORT}`);
});
