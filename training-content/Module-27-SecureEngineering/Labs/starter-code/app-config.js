/**
 * FoodExpress Node.js API Configuration
 * BUG: Multiple security issues
 */

const express = require('express');
// BUG: Helmet not imported or used -- missing security headers
// const helmet = require('helmet');

const app = express();
app.use(express.json());

// BUG: No helmet middleware -- missing security headers
// Should have: app.use(helmet());

// BUG: Hardcoded Stripe API key
const STRIPE_API_KEY = process.env.STRIPE_API_KEY || "your-stripe-key-here";

// BUG: CORS too permissive -- allows any origin
const cors = require('cors');
app.use(cors({
    origin: '*',  // BUG: Should restrict to specific domains
    credentials: true
}));

// Error handler
// BUG: Exposes stack trace in production
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: err.message,
        stack: err.stack  // BUG: Stack trace exposed to client
    });
});

module.exports = app;
