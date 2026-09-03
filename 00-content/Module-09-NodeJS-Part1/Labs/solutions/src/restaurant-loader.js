// FoodExpress Restaurant Loader
// Loads restaurant data from JSON file using Node.js fs module

const fs = require('fs');
const path = require('path');

// FIX: Corrected path to use path.join with __dirname for reliable resolution
const DATA_PATH = path.join(__dirname, '..', 'data', 'restaurants.json');

// FIX: Changed from sync to async fs.readFile with proper callback
function loadRestaurants(callback) {
  console.log('Loading FoodExpress restaurant data...');

  fs.readFile(DATA_PATH, 'utf8', (err, data) => {
    if (err) {
      console.error('Error loading restaurants:', err.message);
      return callback(err, null);
    }
    const restaurants = JSON.parse(data);
    console.log(`Loaded ${restaurants.length} restaurants`);
    callback(null, restaurants);
  });
}

function getOpenRestaurants(callback) {
  loadRestaurants((err, restaurants) => {
    if (err) return callback(err, null);
    const open = restaurants.filter(r => r.isOpen === true);
    console.log(`Open restaurants: ${open.length}`);
    callback(null, open);
  });
}

function getRestaurantById(id, callback) {
  loadRestaurants((err, restaurants) => {
    if (err) return callback(err, null);
    const found = restaurants.find(r => r.id === id);
    if (!found) {
      console.log(`Restaurant ${id} not found`);
    }
    callback(null, found);
  });
}

// Main execution
loadRestaurants((err, allRestaurants) => {
  if (err) return;
  allRestaurants.forEach(r => {
    console.log(`  ${r.name} (${r.cuisine}) - Rating: ${r.rating}`);
  });

  getOpenRestaurants((err, openOnes) => {
    if (err) return;
    openOnes.forEach(r => {
      console.log(`  OPEN: ${r.name} - Delivery: ${r.deliveryTime} mins`);
    });
  });
});

module.exports = { loadRestaurants, getOpenRestaurants, getRestaurantById };
