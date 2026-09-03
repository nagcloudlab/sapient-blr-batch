// FoodExpress Menu Reader
// Reads menu data for each restaurant using callbacks

const fs = require('fs');
const path = require('path');

const DATA_PATH = path.join(__dirname, '..', 'data', 'restaurants.json');

// BUG: Callback hell - deeply nested callbacks with no error handling
// Expected: Flatten with named functions or convert to async/await, add error handling
function readMenuForRestaurant(restaurantId) {
  fs.readFile(DATA_PATH, 'utf8', function(data) {
    // BUG: Callback signature is wrong - fs.readFile passes (err, data) but err is ignored
    // Expected: First parameter should be err, check for errors before proceeding
    const restaurants = JSON.parse(data);
    const restaurant = restaurants.find(r => r.id === restaurantId);

    fs.readFile(DATA_PATH, 'utf8', function(data2) {
      const allData = JSON.parse(data2);
      const menu = restaurant.menu;

      fs.readFile(DATA_PATH, 'utf8', function(data3) {
        const prices = menu.map(item => item.price);
        const total = prices.reduce((sum, p) => sum + p, 0);
        const avg = total / prices.length;

        console.log(`Restaurant: ${restaurant.name}`);
        console.log(`Menu Items: ${menu.length}`);
        console.log(`Average Price: Rs.${avg.toFixed(2)}`);
        menu.forEach(item => {
          console.log(`  ${item.item} - Rs.${item.price} [${item.category}]`);
        });
      });
    });
  });
}

function listAllMenuItems() {
  fs.readFile(DATA_PATH, 'utf8', function(data) {
    const restaurants = JSON.parse(data);
    restaurants.forEach(r => {
      console.log(`\n--- ${r.name} ---`);
      r.menu.forEach(item => {
        console.log(`  ${item.item}: Rs.${item.price}`);
      });
    });
  });
}

// Main execution
console.log('FoodExpress Menu Reader');
console.log('='.repeat(40));
readMenuForRestaurant('rest-001');
listAllMenuItems();
