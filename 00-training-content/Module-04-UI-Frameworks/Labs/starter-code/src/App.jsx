// FoodExpress - Main App Component (Module 04: UI Frameworks - React)
// This file sets up React Router and manages top-level state.

import React, { useState, useMemo } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import RestaurantList from './components/RestaurantList';
import CartSidebar from './components/CartSidebar';
import './App.css';

// FoodExpress restaurant and menu data
// (Carried forward from Module 03 vanilla JS version)
const restaurants = [
  {
    id: 1,
    name: 'Burger Barn',
    cuisine: 'American',
    rating: 4.3,
    deliveryTime: '25-35 min',
    image: 'https://placehold.co/600x200/e84c3d/fff?text=Burger+Barn',
    menu: [
      { id: 101, name: 'Classic Burger', price: 8.99, image: '🍔' },
      { id: 102, name: 'Cheese Fries', price: 4.99, image: '🍟' },
      { id: 103, name: 'Milkshake', price: 5.49, image: '🥤' },
    ],
  },
  {
    id: 2,
    name: 'Pizza Palace',
    cuisine: 'Italian',
    rating: 4.5,
    deliveryTime: '30-40 min',
    image: 'https://placehold.co/600x200/e67e22/fff?text=Pizza+Palace',
    menu: [
      { id: 201, name: 'Margherita Pizza', price: 12.99, image: '🍕' },
      { id: 202, name: 'Garlic Bread', price: 3.99, image: '🧄' },
      { id: 203, name: 'Tiramisu', price: 6.99, image: '🍰' },
    ],
  },
  {
    id: 3,
    name: 'Dragon Wok',
    cuisine: 'Chinese',
    rating: 4.1,
    deliveryTime: '20-30 min',
    image: 'https://placehold.co/600x200/c0392b/fff?text=Dragon+Wok',
    menu: [
      { id: 301, name: 'Kung Pao Chicken', price: 11.49, image: '🍗' },
      { id: 302, name: 'Fried Rice', price: 7.99, image: '🍚' },
      { id: 303, name: 'Spring Rolls', price: 5.99, image: '🥟' },
    ],
  },
  {
    id: 4,
    name: 'Spice Route',
    cuisine: 'Indian',
    rating: 4.6,
    deliveryTime: '35-45 min',
    image: 'https://placehold.co/600x200/f39c12/fff?text=Spice+Route',
    menu: [
      { id: 401, name: 'Butter Chicken', price: 13.99, image: '🍛' },
      { id: 402, name: 'Garlic Naan', price: 2.99, image: '🫓' },
      { id: 403, name: 'Mango Lassi', price: 3.99, image: '🥭' },
    ],
  },
  {
    id: 5,
    name: 'Fresh & Green',
    cuisine: 'Healthy',
    rating: 4.4,
    deliveryTime: '15-25 min',
    image: 'https://placehold.co/600x200/27ae60/fff?text=Fresh+%26+Green',
    menu: [
      { id: 501, name: 'Caesar Salad', price: 9.99, image: '🥗' },
      { id: 502, name: 'Smoothie Bowl', price: 8.49, image: '🫐' },
      { id: 503, name: 'Avocado Toast', price: 7.99, image: '🥑' },
    ],
  },
  {
    id: 6,
    name: 'Sweet Tooth',
    cuisine: 'Desserts',
    rating: 4.7,
    deliveryTime: '20-30 min',
    image: 'https://placehold.co/600x200/8e44ad/fff?text=Sweet+Tooth',
    menu: [
      { id: 601, name: 'Chocolate Cake', price: 6.99, image: '🎂' },
      { id: 602, name: 'Ice Cream Sundae', price: 5.49, image: '🍨' },
      { id: 603, name: 'Churros', price: 4.99, image: '🍩' },
    ],
  },
];

function App() {
  const [cart, setCart] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCuisine, setSelectedCuisine] = useState('All');
  const [isCartOpen, setIsCartOpen] = useState(false);

  // Add item to cart
  const addToCart = (item) => {
    setCart((prevCart) => {
      const existing = prevCart.find((ci) => ci.id === item.id);
      if (existing) {
        return prevCart.map((ci) =>
          ci.id === item.id ? { ...ci, quantity: ci.quantity + 1 } : ci
        );
      }
      return [...prevCart, { ...item, quantity: 1 }];
    });
  };

  // Remove item from cart
  const removeFromCart = (itemId) => {
    setCart((prevCart) => prevCart.filter((ci) => ci.id !== itemId));
  };

  // Update item quantity
  const updateQuantity = (itemId, newQty) => {
    if (newQty <= 0) {
      removeFromCart(itemId);
      return;
    }
    setCart((prevCart) =>
      prevCart.map((ci) =>
        ci.id === itemId ? { ...ci, quantity: newQty } : ci
      )
    );
  };

  // Cart total
  const cartTotal = cart.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  // Cart item count
  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  // Filter restaurants (useMemo prevents unnecessary re-renders)
  const filteredRestaurants = useMemo(
    () =>
      restaurants.filter((r) => {
        const matchesSearch = r.name
          .toLowerCase()
          .includes(searchTerm.toLowerCase());
        const matchesCuisine =
          selectedCuisine === 'All' || r.cuisine === selectedCuisine;
        return matchesSearch && matchesCuisine;
      }),
    [searchTerm, selectedCuisine]
  );

  const cuisines = ['All', ...new Set(restaurants.map((r) => r.cuisine))];

  return (
    <Router>
      <div className="app">
        <Header
          cartCount={cartCount}
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          onCartClick={() => setIsCartOpen(true)}
          cuisines={cuisines}
          selectedCuisine={selectedCuisine}
          onCuisineChange={setSelectedCuisine}
        />

        <main style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
          <Routes>
            <Route
              path="/"
              element={
                <RestaurantList
                  restaurants={filteredRestaurants}
                  onAddToCart={addToCart}
                />
              }
            />
          </Routes>
        </main>

        <CartSidebar
          isOpen={isCartOpen}
          cart={cart}
          cartCount={cartCount}
          cartTotal={cartTotal}
          onClose={() => setIsCartOpen(false)}
          onRemove={removeFromCart}
          onUpdateQuantity={updateQuantity}
        />

        <footer className="app-footer">
          <div className="footer-brand">FoodExpress</div>
          <div>support@foodexpress.com | 1-800-FOOD-EXP</div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
