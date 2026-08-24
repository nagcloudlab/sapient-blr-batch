// FoodExpress Async Order Processor
// Demonstrates Promises and async/await patterns

const fs = require('fs');
const path = require('path');

// FIX: Used path.join instead of hardcoded backslash separators
const DATA_PATH = path.join(__dirname, '..', 'data', 'restaurants.json');

function readRestaurantsAsync() {
  return new Promise((resolve, reject) => {
    fs.readFile(DATA_PATH, 'utf8', (err, data) => {
      if (err) reject(err);
      resolve(JSON.parse(data));
    });
  });
}

function calculateDeliveryEstimate(restaurant) {
  return new Promise((resolve) => {
    setTimeout(() => {
      const estimate = restaurant.deliveryTime + Math.floor(Math.random() * 10);
      resolve({ name: restaurant.name, estimate });
    }, 100);
  });
}

// FIX: Added proper await on Promise.all and wrapped in try/catch
async function processOrders() {
  try {
    const restaurants = await readRestaurantsAsync();
    const openRestaurants = restaurants.filter(r => r.isOpen);

    console.log('Processing FoodExpress delivery estimates...');

    const estimates = openRestaurants.map(r => calculateDeliveryEstimate(r));

    // FIX: Added await to Promise.all so results are resolved values
    const results = await Promise.all(estimates);

    results.forEach(r => {
      console.log(`  ${r.name}: ~${r.estimate} minutes`);
    });
  } catch (err) {
    console.error('Error processing orders:', err.message);
  }
}

// FIX: Added .catch() for unhandled promise rejection
processOrders().catch(err => console.error('Fatal:', err.message));

module.exports = { readRestaurantsAsync, calculateDeliveryEstimate, processOrders };
