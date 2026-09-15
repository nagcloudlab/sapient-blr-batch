const express = require('express');
const client = require('prom-client');
const crypto = require('crypto');

const app = express();
app.use(express.json());

client.collectDefaultMetrics({ prefix: 'payment_' });
const paymentDuration = new client.Histogram({ name: 'payment_processing_seconds', help: 'Payment processing time', buckets: [0.1, 0.5, 1, 2, 5] });
const paymentsTotal = new client.Counter({ name: 'payments_total', help: 'Total payments', labelNames: ['status'] });

function log(level, msg, fields = {}) {
  console.log(JSON.stringify({ timestamp: new Date().toISOString(), level, service: 'payment-service', ...fields, message: msg }));
}

app.post('/api/pay', (req, res) => {
  const traceId = req.headers['x-trace-id'] || crypto.randomUUID().substring(0, 8);
  const end = paymentDuration.startTimer();

  log('INFO', 'Payment request received', { traceId, orderId: req.body.orderId, amount: req.body.amount });

  const delay = 200 + Math.floor(Math.random() * 600);
  setTimeout(() => {
    end();
    if (Math.random() < 0.08) {
      paymentsTotal.inc({ status: 'failed' });
      log('ERROR', 'Payment failed', { traceId, orderId: req.body.orderId, error: 'InsufficientFunds', duration_ms: delay });
      res.status(500).json({ error: 'Payment failed', traceId });
      return;
    }
    paymentsTotal.inc({ status: 'success' });
    log('INFO', 'Payment processed', { traceId, orderId: req.body.orderId, duration_ms: delay, txnId: `TXN-${Date.now()}` });
    res.json({ status: 'paid', txnId: `TXN-${Date.now()}`, traceId });
  }, delay);
});

app.get('/metrics', async (req, res) => { res.set('Content-Type', client.register.contentType); res.end(await client.register.metrics()); });
app.get('/health', (req, res) => res.json({ status: 'UP' }));
app.listen(8081, () => log('INFO', 'Started', { port: 8081 }));
