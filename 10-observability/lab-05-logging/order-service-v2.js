const express = require('express');
const client = require('prom-client');
const crypto = require('crypto');

const app = express();

// Structured logger
function log(level, message, fields = {}) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level, service: 'order-service', ...fields, message
  }));
}

// Metrics
client.collectDefaultMetrics();
const httpRequestsTotal = new client.Counter({ name: 'http_requests_total', help: 'Total HTTP requests', labelNames: ['method', 'path', 'status'] });
const httpRequestDuration = new client.Histogram({ name: 'http_request_duration_seconds', help: 'Request duration', labelNames: ['method', 'path'], buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5] });
const ordersTotal = new client.Counter({ name: 'orders_placed_total', help: 'Total orders', labelNames: ['status'] });
const activeOrders = new client.Gauge({ name: 'active_orders', help: 'Active orders' });

// Middleware: metrics + logging
app.use((req, res, next) => {
  req.requestId = crypto.randomUUID().substring(0, 8);
  const end = httpRequestDuration.startTimer({ method: req.method, path: req.path });
  res.on('finish', () => {
    httpRequestsTotal.inc({ method: req.method, path: req.path, status: res.statusCode });
    const duration = end();
    log(res.statusCode >= 400 ? 'ERROR' : 'INFO', `${req.method} ${req.path}`, {
      requestId: req.requestId, statusCode: res.statusCode, duration_ms: Math.round(duration * 1000)
    });
  });
  next();
});

// Routes
app.get('/', (req, res) => res.json({ service: 'FoodExpress', status: 'healthy' }));

app.post('/api/orders', (req, res) => {
  const orderId = `ORD-${Date.now()}`;
  activeOrders.inc();
  log('INFO', 'Order received', { requestId: req.requestId, orderId });

  const delay = Math.random() < 0.05 ? 3000 : Math.floor(Math.random() * 200);
  setTimeout(() => {
    if (Math.random() < 0.1) {
      ordersTotal.inc({ status: 'failed' });
      activeOrders.dec();
      log('ERROR', 'Payment gateway timeout', { requestId: req.requestId, orderId, error: 'PaymentGatewayTimeout', duration_ms: delay });
      res.status(500).json({ error: 'Payment gateway timeout', orderId });
      return;
    }
    ordersTotal.inc({ status: 'success' });
    activeOrders.dec();
    log('INFO', 'Order placed', { requestId: req.requestId, orderId, duration_ms: delay });
    res.json({ orderId, status: 'placed' });
  }, delay);
});

app.get('/health', (req, res) => res.json({ status: 'UP' }));
app.get('/metrics', async (req, res) => { res.set('Content-Type', client.register.contentType); res.end(await client.register.metrics()); });

log('INFO', 'Server starting', { port: 8080 });
app.listen(8080);
