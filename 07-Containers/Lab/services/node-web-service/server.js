const express = require('express');
const app = express();
const PORT = process.env.PORT || 8080;

app.get('/api/info', (req, res) => {
  res.json({ service: 'node-web-service', version: '1.0.0' });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'UP' });
});

app.listen(PORT, () => console.log(`Listening on port ${PORT}`));
