const express = require('express');
const client = require('prom-client');

const app = express();
app.use(express.json());

client.collectDefaultMetrics({ prefix: 'notification_' });
const notificationsTotal = new client.Counter({ name: 'notifications_sent_total', help: 'Total notifications', labelNames: ['channel'] });

function log(level, msg, fields = {}) {
  console.log(JSON.stringify({ timestamp: new Date().toISOString(), level, service: 'notification-service', ...fields, message: msg }));
}

app.post('/api/notify', (req, res) => {
  const traceId = req.headers['x-trace-id'] || 'unknown';
  const { orderId, userId, type } = req.body;

  const delay = 50 + Math.floor(Math.random() * 150);
  setTimeout(() => {
    notificationsTotal.inc({ channel: type || 'sms' });
    log('INFO', 'Notification sent', { traceId, orderId, userId, channel: type || 'sms', duration_ms: delay });
    res.json({ status: 'sent', traceId });
  }, delay);
});

app.get('/metrics', async (req, res) => { res.set('Content-Type', client.register.contentType); res.end(await client.register.metrics()); });
app.get('/health', (req, res) => res.json({ status: 'UP' }));
app.listen(8082, () => log('INFO', 'Started', { port: 8082 }));
