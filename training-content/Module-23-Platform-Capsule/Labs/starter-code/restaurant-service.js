/**
 * FoodExpress Restaurant Service (Node.js)
 * Provides restaurant and menu data via REST API
 */

const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json());

// BUG: Using readFileSync blocks the event loop -- should use readFile (async)
// This causes 8-second response times under load
function getMenuData(restaurantId) {
    const filePath = path.join(__dirname, 'data', `restaurant-${restaurantId}-menu.json`);
    // BUG: Synchronous file read blocks the entire event loop
    const data = fs.readFileSync(filePath, 'utf8');
    // Simulate processing delay
    const menu = JSON.parse(data);
    return menu;
}

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'UP', service: 'restaurant-service' });
});

// Get restaurant menu
app.get('/api/v1/restaurants/:id/menu', (req, res) => {
    const restaurantId = req.params.id;
    try {
        const menu = getMenuData(restaurantId);
        res.json(menu);
    } catch (err) {
        console.error(`Error loading menu for restaurant ${restaurantId}:`, err.message);
        res.status(500).json({ error: 'Failed to load menu' });
    }
});

// Get restaurant details
app.get('/api/v1/restaurants/:id', (req, res) => {
    // Simulated restaurant data
    res.json({
        id: req.params.id,
        name: 'FoodExpress Partner Restaurant',
        rating: 4.5,
        deliveryTime: '30-45 min'
    });
});

// List all restaurants
app.get('/api/v1/restaurants', (req, res) => {
    res.json({
        restaurants: [
            { id: 1, name: 'Spice Garden', cuisine: 'Indian' },
            { id: 2, name: 'Pizza Palace', cuisine: 'Italian' },
            { id: 3, name: 'Sushi House', cuisine: 'Japanese' }
        ]
    });
});

// BUG: No uncaughtException handler -- process crashes silently
// Should have:
// process.on('uncaughtException', (err) => {
//     console.error('Uncaught Exception:', err);
//     // Graceful shutdown logic
// });

// BUG: No unhandledRejection handler
// process.on('unhandledRejection', (reason, promise) => {
//     console.error('Unhandled Rejection at:', promise, 'reason:', reason);
// });

app.listen(PORT, () => {
    console.log(`Restaurant Service running on port ${PORT}`);
});
