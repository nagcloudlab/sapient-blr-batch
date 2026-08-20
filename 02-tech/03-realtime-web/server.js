import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { WebSocketServer } from 'ws';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = 3000;

// ─── Shared state ───
let messageId = 0;
const messages = [];          // Store for polling
const longPollWaiters = [];   // Queued long-poll responses
const sseClients = [];        // Connected SSE clients

function broadcast(msg) {
  const entry = { id: ++messageId, ...msg, timestamp: new Date().toISOString() };
  messages.push(entry);
  if (messages.length > 100) messages.shift();

  // Notify long-poll waiters
  while (longPollWaiters.length > 0) {
    const waiter = longPollWaiters.shift();
    if (!waiter.res.writableEnded) {
      waiter.res.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
      waiter.res.end(JSON.stringify(entry));
      clearTimeout(waiter.timeout);
    }
  }

  // Notify SSE clients
  sseClients.forEach(res => {
    if (!res.writableEnded) {
      res.write(`id: ${entry.id}\n`);
      res.write(`data: ${JSON.stringify(entry)}\n\n`);
    }
  });

  // Notify WebSocket clients
  wss.clients.forEach(client => {
    if (client.readyState === 1) { // WebSocket.OPEN
      client.send(JSON.stringify({ type: 'message', ...entry }));
    }
  });
}

// ─── Simulated server events (temperature sensor) ───
setInterval(() => {
  broadcast({
    source: 'sensor',
    type: 'temperature',
    value: +(20 + Math.random() * 15).toFixed(1),
    unit: 'C'
  });
}, 4000);

// ─── MIME types ───
const MIME = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
};

// ─── HTTP Server ───
const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  // ── CORS for all API routes ──
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.writeHead(204); return res.end(); }

  // ── POST /api/send — send a message from any pattern ──
  if (url.pathname === '/api/send' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const msg = JSON.parse(body);
        broadcast({ source: 'user', type: 'chat', text: msg.text || '(empty)' });
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true }));
      } catch {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Invalid JSON' }));
      }
    });
    return;
  }

  // ── GET /api/poll — Short Polling ──
  if (url.pathname === '/api/poll') {
    const since = parseInt(url.searchParams.get('since') || '0', 10);
    const newMessages = messages.filter(m => m.id > since);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ messages: newMessages, lastId: messageId }));
    return;
  }

  // ── GET /api/long-poll — Long Polling ──
  if (url.pathname === '/api/long-poll') {
    const since = parseInt(url.searchParams.get('since') || '0', 10);
    const newMessages = messages.filter(m => m.id > since);
    if (newMessages.length > 0) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(newMessages[newMessages.length - 1]));
      return;
    }
    // Hold connection open for up to 30 seconds
    const timeout = setTimeout(() => {
      if (!res.writableEnded) {
        res.writeHead(204);
        res.end();
      }
    }, 30000);
    longPollWaiters.push({ res, timeout });
    req.on('close', () => {
      const idx = longPollWaiters.findIndex(w => w.res === res);
      if (idx !== -1) { clearTimeout(longPollWaiters[idx].timeout); longPollWaiters.splice(idx, 1); }
    });
    return;
  }

  // ── GET /api/sse — Server-Sent Events ──
  if (url.pathname === '/api/sse') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    });
    res.write(`data: ${JSON.stringify({ type: 'connected', message: 'SSE stream open' })}\n\n`);
    sseClients.push(res);
    req.on('close', () => {
      const idx = sseClients.indexOf(res);
      if (idx !== -1) sseClients.splice(idx, 1);
    });
    return;
  }

  // ── Serve static files ──
  let filePath = url.pathname === '/' ? '/demo.html' : url.pathname;
  const fullPath = path.join(__dirname, filePath);
  const ext = path.extname(fullPath);

  fs.readFile(fullPath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('Not Found');
      return;
    }
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

// ─── WebSocket Server ───
const wss = new WebSocketServer({ server });

wss.on('connection', (ws) => {
  ws.send(JSON.stringify({ type: 'system', text: 'WebSocket connected!', timestamp: new Date().toISOString() }));

  ws.on('message', (raw) => {
    try {
      const msg = JSON.parse(raw);
      broadcast({ source: 'websocket', type: 'chat', text: msg.text || raw.toString() });
    } catch {
      broadcast({ source: 'websocket', type: 'chat', text: raw.toString() });
    }
  });
});

// ─── Start ───
server.listen(PORT, () => {
  console.log(`\n  Real-Time Web Demo Server`);
  console.log(`  ========================`);
  console.log(`  Dashboard:  http://localhost:${PORT}`);
  console.log(`  Slides:     http://localhost:${PORT}/presentation.html`);
  console.log(`\n  API Endpoints:`);
  console.log(`    POST /api/send        Send a message`);
  console.log(`    GET  /api/poll        Short polling`);
  console.log(`    GET  /api/long-poll   Long polling`);
  console.log(`    GET  /api/sse         SSE stream`);
  console.log(`    WS   ws://localhost:${PORT}  WebSocket\n`);
});
