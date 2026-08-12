const express = require('express');
const fs = require('fs').promises;
const path = require('path');

const app = express();
const PORT = 3002;
const DATA_FILE = path.join(__dirname, 'products.json');

// NON-BLOCKING: Uses fs.promises.readFile — does NOT block the event loop
// While one request waits for I/O, other requests can be processed
app.get('/api/products', async (req, res) => {
  try {
    const data = await fs.readFile(DATA_FILE, 'utf-8');

    // Same simulated work, but wrapped in setImmediate to yield to event loop
    await new Promise((resolve) => setImmediate(resolve));

    const products = JSON.parse(data);
    res.json({ mode: 'NON-BLOCKING', products });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/health', (req, res) => res.json({ status: 'ok', mode: 'non-blocking' }));

app.listen(PORT, () => {
  console.log(`[NON-BLOCKING server] running on http://localhost:${PORT}`);
});
