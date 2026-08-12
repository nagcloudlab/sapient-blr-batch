// FoodExpress Restaurant Loader
// Loads restaurant data from JSON file using Node.js fs module

const fs = require('fs');

// BUG: Wrong require path - using ./data instead of ../data
// Expected: Path should be relative to THIS file's location (src/), so ../data/restaurants.json
const DATA_PATH = './data/restaurants.json';

function loadRestaurants() {
  console.log('Loading FoodExpress restaurant data...');

  // BUG: Uses synchronous fs.readFileSync where async fs.readFile is needed
  // Expected: Use fs.readFile (async) with a callback to avoid blocking the event loop
  const data = fs.readFileSync(DATA_PATH, 'utf8');
  const restaurants = JSON.parse(data);

  console.log(`Loaded ${restaurants.length} restaurants`);
  return restaurants;
}

function getOpenRestaurants() {
  const restaurants = loadRestaurants();
  const open = restaurants.filter(r => r.isOpen === true);
  console.log(`Open restaurants: ${open.length}`);
  return open;
}

function getRestaurantById(id) {
  const restaurants = loadRestaurants();
  const found = restaurants.find(r => r.id === id);
  if (!found) {
    console.log(`Restaurant ${id} not found`);
  }
  return found;
}

// Main execution
const allRestaurants = loadRestaurants();
allRestaurants.forEach(r => {
  console.log(`  ${r.name} (${r.cuisine}) - Rating: ${r.rating}`);
});

const openOnes = getOpenRestaurants();
openOnes.forEach(r => {
  console.log(`  OPEN: ${r.name} - Delivery: ${r.deliveryTime} mins`);
});

module.exports = { loadRestaurants, getOpenRestaurants, getRestaurantById };
