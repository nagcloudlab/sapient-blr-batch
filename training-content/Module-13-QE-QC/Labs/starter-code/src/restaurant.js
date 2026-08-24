/**
 * FoodExpress -- Restaurant Service
 *
 * Manages restaurant data, search, and availability.
 * No tests. Some known customer complaints about search results.
 */

const restaurants = [
  { id: 1, name: 'Biryani Palace', cuisine: 'Indian', rating: 4.5, isActive: true, opensAt: '08:00', closesAt: '23:00' },
  { id: 2, name: 'Pizza Corner', cuisine: 'Italian', rating: 4.2, isActive: true, opensAt: '10:00', closesAt: '22:00' },
  { id: 3, name: 'Dragon Wok', cuisine: 'Chinese', rating: 3.8, isActive: false, opensAt: '11:00', closesAt: '21:00' },
  { id: 4, name: 'Burger Barn', cuisine: 'American', rating: 4.0, isActive: true, opensAt: '09:00', closesAt: '23:30' },
  { id: 5, name: 'Sushi Studio', cuisine: 'Japanese', rating: 4.7, isActive: true, opensAt: '12:00', closesAt: '22:00' },
  { id: 6, name: 'Taco Town', cuisine: 'Mexican', rating: 3.5, isActive: false, opensAt: '10:00', closesAt: '20:00' },
  { id: 7, name: 'Dosa Darbar', cuisine: 'South Indian', rating: 4.3, isActive: true, opensAt: '06:00', closesAt: '22:00' },
];

function getAllRestaurants() {
  // BUG: returns ALL restaurants including inactive ones
  // Customers see closed restaurants with "Order Now" button
  return restaurants;
}

function searchByName(query) {
  if (!query) return [];
  // BUG: case-sensitive search -- "pizza" won't find "Pizza Corner"
  return restaurants.filter(r => r.name.includes(query));
}

function searchByCuisine(cuisine) {
  if (!cuisine) return [];
  // BUG: also returns inactive restaurants
  return restaurants.filter(r => r.cuisine.toLowerCase() === cuisine.toLowerCase());
}

function getById(id) {
  return restaurants.find(r => r.id === id) || null;
}

function isOpen(restaurantId) {
  const restaurant = getById(restaurantId);
  if (!restaurant) return false;
  if (!restaurant.isActive) return false;

  // BUG: doesn't actually check current time against opensAt/closesAt
  // Always returns true if restaurant is active
  return true;
}

function getTopRated(limit = 3) {
  // BUG: doesn't filter out inactive restaurants before sorting
  return [...restaurants]
    .sort((a, b) => b.rating - a.rating)
    .slice(0, limit);
}

function addReview(restaurantId, rating) {
  const restaurant = getById(restaurantId);
  if (!restaurant) throw new Error('Restaurant not found');

  if (rating < 1 || rating > 5) {
    throw new Error('Rating must be between 1 and 5');
  }

  // BUG: overwrites rating instead of averaging
  // Should calculate: (oldRating * reviewCount + newRating) / (reviewCount + 1)
  restaurant.rating = rating;
}

module.exports = {
  getAllRestaurants,
  searchByName,
  searchByCuisine,
  getById,
  isOpen,
  getTopRated,
  addReview,
};
