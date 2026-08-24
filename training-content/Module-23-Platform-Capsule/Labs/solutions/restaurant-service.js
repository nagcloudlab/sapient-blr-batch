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

// FIX: Changed from readFileSync to readFile (async) to avoid blocking event loop
function getMenuData(restaurantId) {
    return new Promise((resolve, reject) => {
        const filePath = path.join(__dirname, 'data', `restaurant-${restaurantId}-menu.json`);
        // FIX: Asynchronous file read does not block the event loop
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                reject(err);
                return;
            }
            const menu = JSON.parse(data);
            resolve(menu);
        });
    });
}

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'UP', service: 'restaurant-service' });
});

// Get restaurant menu
app.get('/api/v1/restaurants/:id/menu', async (req, res) => {
    const restaurantId = req.params.id;
    try {
        const menu = await getMenuData(restaurantId);
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

// FIX: Added uncaughtException handler for graceful error handling
process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
    // Log the error and perform graceful shutdown
    process.exit(1);
});

// FIX: Added unhandledRejection handler
process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

app.listen(PORT, () => {
    console.log(`Restaurant Service running on port ${PORT}`);
});
