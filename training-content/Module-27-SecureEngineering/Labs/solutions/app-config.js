/**
 * FoodExpress Node.js API Configuration
 * FIX: Security issues resolved
 */

const express = require('express');
// FIX: Import and use helmet for security headers
const helmet = require('helmet');

const app = express();
app.use(express.json());

// FIX: Enable helmet middleware for security headers
app.use(helmet());

// FIX: Read API key from environment variable
const STRIPE_API_KEY = process.env.STRIPE_API_KEY;
if (!STRIPE_API_KEY) {
    console.error('STRIPE_API_KEY environment variable is not set');
    process.exit(1);
}

// FIX: Restrict CORS to specific allowed origins
const cors = require('cors');
app.use(cors({
    origin: ['https://foodexpress.in', 'https://admin.foodexpress.in'],
    credentials: true
}));

// Error handler
// FIX: Do not expose stack trace in production
app.use((err, req, res, next) => {
    console.error(err.stack);  // Log full error server-side
    res.status(500).json({
        error: process.env.NODE_ENV === 'production'
            ? 'Internal server error'  // FIX: Generic message for clients
            : err.message
        // FIX: Stack trace removed from response
    });
});

module.exports = app;
