// FoodExpress Menu Reader
// Reads menu data using async/await (refactored from callback hell)

const fs = require('fs');
const path = require('path');

const DATA_PATH = path.join(__dirname, '..', 'data', 'restaurants.json');

// FIX: Promisified fs.readFile for clean async/await usage
function readData() {
  return new Promise((resolve, reject) => {
    fs.readFile(DATA_PATH, 'utf8', (err, data) => {
      if (err) return reject(err);
      resolve(JSON.parse(data));
    });
  });
}

// FIX: Flattened callback hell into async/await with proper error handling
async function readMenuForRestaurant(restaurantId) {
  try {
    const restaurants = await readData();
    const restaurant = restaurants.find(r => r.id === restaurantId);

    if (!restaurant) {
      console.log(`Restaurant ${restaurantId} not found`);
      return;
    }

    const menu = restaurant.menu;
    const prices = menu.map(item => item.price);
    const total = prices.reduce((sum, p) => sum + p, 0);
    const avg = total / prices.length;

    console.log(`Restaurant: ${restaurant.name}`);
    console.log(`Menu Items: ${menu.length}`);
    console.log(`Average Price: Rs.${avg.toFixed(2)}`);
    menu.forEach(item => {
      console.log(`  ${item.item} - Rs.${item.price} [${item.category}]`);
    });
  } catch (err) {
    console.error('Error reading menu:', err.message);
  }
}

// FIX: Added proper error handling with (err, data) callback signature
async function listAllMenuItems() {
  try {
    const restaurants = await readData();
    restaurants.forEach(r => {
      console.log(`\n--- ${r.name} ---`);
      r.menu.forEach(item => {
        console.log(`  ${item.item}: Rs.${item.price}`);
      });
    });
  } catch (err) {
    console.error('Error listing menus:', err.message);
  }
}

// Main execution
async function main() {
  console.log('FoodExpress Menu Reader');
  console.log('='.repeat(40));
  await readMenuForRestaurant('rest-001');
  await listAllMenuItems();
}

main();
