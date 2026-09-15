const express = require('express');
const client = require('prom-client');
const crypto = require('crypto');
const http = require('http');

const app = express();
app.use(express.json());

client.collectDefaultMetrics({ prefix: 'order_' });
const httpRequestsTotal = new client.Counter({ name: 'http_requests_total', help: 'Total HTTP requests', labelNames: ['method', 'path', 'status'] });
const httpRequestDuration = new client.Histogram({ name: 'http_request_duration_seconds', help: 'Request duration', labelNames: ['method', 'path'], buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5] });
const ordersTotal = new client.Counter({ name: 'orders_placed_total', help: 'Total orders', labelNames: ['status'] });

function log(level, msg, fields = {}) {
  console.log(JSON.stringify({ timestamp: new Date().toISOString(), level, service: 'order-service', ...fields, message: msg }));
}

function callService(host, port, path, data, traceId) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(data);
    const req = http.request({ hostname: host, port, path, method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Trace-Id': traceId, 'Content-Length': body.length } }, (res) => {
      let responseData = '';
      res.on('data', chunk => responseData += chunk);
      res.on('end', () => {
        if (res.statusCode >= 400) reject(new Error(`${host}:${port}${path} returned ${res.statusCode}: ${responseData}`));
        else resolve(JSON.parse(responseData));
      });
    });
    req.on('error', reject);
    req.end(body);
  });
}

const PAYMENT_HOST = process.env.PAYMENT_HOST || 'localhost';
const NOTIFY_HOST = process.env.NOTIFY_HOST || 'localhost';

app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer({ method: req.method, path: req.path });
  res.on('finish', () => { httpRequestsTotal.inc({ method: req.method, path: req.path, status: res.statusCode }); end(); });
  next();
});

app.post('/api/orders', async (req, res) => {
  const traceId = crypto.randomUUID().substring(0, 12);
  const orderId = `ORD-${Date.now()}`;
  const startTime = Date.now();

  log('INFO', 'Order received', { traceId, orderId });

  try {
    log('INFO', 'Calling payment service', { traceId, orderId });
    const payResult = await callService(PAYMENT_HOST, 8081, '/api/pay', { orderId, amount: 499 }, traceId);
    log('INFO', 'Payment completed', { traceId, orderId, txnId: payResult.txnId });

    log('INFO', 'Calling notification service', { traceId, orderId });
    await callService(NOTIFY_HOST, 8082, '/api/notify', { orderId, userId: 'user-123', type: 'sms' }, traceId);
    log('INFO', 'Notification sent', { traceId, orderId });

    ordersTotal.inc({ status: 'success' });
    const totalTime = Date.now() - startTime;
    log('INFO', 'Order completed', { traceId, orderId, total_ms: totalTime });
    res.json({ orderId, status: 'placed', traceId, total_ms: totalTime });

  } catch (err) {
    ordersTotal.inc({ status: 'failed' });
    log('ERROR', 'Order failed', { traceId, orderId, error: err.message, total_ms: Date.now() - startTime });
    res.status(500).json({ orderId, error: err.message, traceId });
  }
});

app.get('/', (req, res) => res.json({ service: 'FoodExpress Order Service', status: 'healthy' }));
app.get('/metrics', async (req, res) => { res.set('Content-Type', client.register.contentType); res.end(await client.register.metrics()); });
app.get('/health', (req, res) => res.json({ status: 'UP' }));
app.listen(8080, () => log('INFO', 'Started', { port: 8080 }));
