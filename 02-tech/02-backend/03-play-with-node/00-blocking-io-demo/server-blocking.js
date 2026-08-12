const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;
const DATA_FILE = path.join(__dirname, 'products.json');

// BLOCKING: Uses readFileSync — blocks the entire event loop
// While one request reads the file, ALL other requests must wait
app.get('/api/products', (req, res) => {
  try {
    const data = fs.readFileSync(DATA_FILE, 'utf-8');

    // Simulate extra CPU work (e.g., parsing a large file)
    // This makes the blocking effect more visible under load
    let sum = 0;
    for (let i = 0; i < 1_000_000; i++) sum += i;

    const products = JSON.parse(data);
    res.json({ mode: 'BLOCKING', products });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/health', (req, res) => res.json({ status: 'ok', mode: 'blocking' }));

app.listen(PORT, () => {
  console.log(`[BLOCKING server] running on http://localhost:${PORT}`);
});
