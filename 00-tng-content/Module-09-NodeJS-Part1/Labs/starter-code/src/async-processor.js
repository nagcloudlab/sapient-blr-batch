// FoodExpress Async Order Processor
// Demonstrates Promises and async/await patterns

const fs = require('fs');

// BUG: Hardcoded path separator (backslash) instead of using path.join
// Expected: Use const path = require('path') and path.join(__dirname, '..', 'data', 'restaurants.json')
const DATA_PATH = __dirname + '\\..\\data\\restaurants.json';

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

// BUG: Unhandled promise rejection - missing .catch() on promise chain
// Expected: Add .catch(err => console.error('Error:', err.message)) to handle rejections
async function processOrders() {
  const restaurants = await readRestaurantsAsync();
  const openRestaurants = restaurants.filter(r => r.isOpen);

  console.log('Processing FoodExpress delivery estimates...');

  const estimates = openRestaurants.map(r => calculateDeliveryEstimate(r));

  // BUG: Missing await on Promise.all - results will be pending promises
  // Expected: const results = await Promise.all(estimates)
  const results = Promise.all(estimates);

  results.forEach(r => {
    console.log(`  ${r.name}: ~${r.estimate} minutes`);
  });
}

// BUG: No .catch() on the top-level promise call
// Expected: processOrders().catch(err => console.error('Fatal:', err.message))
processOrders();

module.exports = { readRestaurantsAsync, calculateDeliveryEstimate, processOrders };
