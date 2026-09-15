const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/api/orders' && req.method === 'POST') {
    // 10% failures, random latency (some very slow)
    if (Math.random() < 0.1) {
      res.writeHead(500);
      res.end(JSON.stringify({ error: 'Payment timeout' }));
      return;
    }
    const delay = Math.random() < 0.05 ? 3000 : Math.floor(Math.random() * 200);
    setTimeout(() => {
      res.writeHead(200);
      res.end(JSON.stringify({ orderId: `ORD-${Date.now()}`, status: 'placed' }));
    }, delay);
    return;
  }
  res.writeHead(200);
  res.end('FoodExpress Order Service');
});

server.listen(8080, () => console.log('Running on port 8080'));
