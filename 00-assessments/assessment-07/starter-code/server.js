const express = require('express');
const app = express();

app.use(express.json());

const PORT = process.env.PORT || 3000;

const events = [
  { id: "evt-1", name: "Bangalore Tech Summit", category: "tech", date: "2026-10-15T09:00:00Z", price: 500, capacity: 200, availableSeats: 142 },
  { id: "evt-2", name: "Indie Music Fest",      category: "music", date: "2026-11-01T17:00:00Z", price: 1200, capacity: 5000, availableSeats: 3800 }
];

// List / Create events
app.get('/api/events', (req, res) => res.json(events));

app.post('/api/events', (req, res) => {
  const { name, category, date, price, capacity } = req.body;
  if (!name || !category) return res.status(400).json({ error: "name and category are required" });
  const event = { id: `evt-${Date.now()}`, name, category, date, price, capacity, availableSeats: capacity };
  events.push(event);
  res.status(201).json(event);
});

// Get event by ID
app.get('/api/events/:id', (req, res) => {
  const event = events.find(e => e.id === req.params.id);
  if (!event) return res.status(404).json({ error: "Event not found" });
  res.json(event);
});

// Health check
app.get('/health', (req, res) => res.json({ status: 'ok', uptime: process.uptime() }));

app.listen(PORT, () => {
  console.log(`QuickTicket API running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});
