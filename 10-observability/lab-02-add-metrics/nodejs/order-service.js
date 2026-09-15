const express = require('express');
const client = require('prom-client');

const app = express();

// Default Node.js metrics (CPU, memory, event loop)
client.collectDefaultMetrics();

// Custom metrics
const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'path', 'status']
});

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Request duration in seconds',
  labelNames: ['method', 'path'],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]
});

const ordersTotal = new client.Counter({
  name: 'orders_placed_total',
  help: 'Total orders placed',
  labelNames: ['status']
});

const activeOrders = new client.Gauge({
  name: 'active_orders',
  help: 'Currently active orders'
});

// Middleware: measure every request
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer({ method: req.method, path: req.path });
  res.on('finish', () => {
    httpRequestsTotal.inc({ method: req.method, path: req.path, status: res.statusCode });
    end();
  });
  next();
});

// Routes
app.get('/', (req, res) => {
  res.json({ service: 'FoodExpress Order Service', status: 'healthy' });
});

app.post('/api/orders', (req, res) => {
  activeOrders.inc();
  const delay = Math.random() < 0.05 ? 3000 : Math.floor(Math.random() * 200);

  setTimeout(() => {
    if (Math.random() < 0.1) {
      ordersTotal.inc({ status: 'failed' });
      activeOrders.dec();
      res.status(500).json({ error: 'Payment gateway timeout' });
      return;
    }
    ordersTotal.inc({ status: 'success' });
    activeOrders.dec();
    res.json({ orderId: `ORD-${Date.now()}`, status: 'placed' });
  }, delay);
});

app.get('/health', (req, res) => res.json({ status: 'UP' }));

// Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

app.listen(8080, () => console.log('Order Service on :8080 | Metrics at /metrics'));
