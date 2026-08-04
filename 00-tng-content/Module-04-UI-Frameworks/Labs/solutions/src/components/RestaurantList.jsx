// FoodExpress - RestaurantList Component (SOLUTION)
// Renders all restaurants as expandable cards. Clicking a restaurant
// reveals its menu items (rendered via MenuCard).
//
// ========================================================================
// FIX: Added [restaurants] as the dependency array to the useEffect call.
//
//      Root cause: Without a dependency array, useEffect runs after EVERY
//      render. Inside the effect, setExpandedId(null) triggers a state
//      change, which causes a re-render, which runs the effect again —
//      creating an infinite loop.
//
//      With [restaurants], the effect only runs when the restaurants prop
//      actually changes (e.g., when the user applies a filter), which is
//      the intended behavior: collapse any expanded card when the list
//      changes.
//
//      Lesson: Always provide a dependency array to useEffect. An empty
//      array [] means "run once on mount". A populated array means "run
//      when these values change". Omitting it entirely means "run after
//      every render" — which is almost never what you want.
// ========================================================================

import React, { useState, useEffect } from 'react';
import MenuCard from './MenuCard';

function RestaurantList({ restaurants, onAddToCart }) {
  const [expandedId, setExpandedId] = useState(null);

  // FIX: Added [restaurants] dependency array — effect now only runs
  // when the restaurants list changes, not on every render.
  useEffect(() => {
    setExpandedId(null);
  }, [restaurants]); // <-- FIX: was missing entirely, now [restaurants]

  const toggleExpand = (id) => {
    setExpandedId((prev) => (prev === id ? null : id));
  };

  const listStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  };

  const cardStyle = {
    border: '1px solid #ddd',
    borderRadius: '12px',
    overflow: 'hidden',
    backgroundColor: '#fff',
    boxShadow: '0 2px 8px rgba(0,0,0,0.06)',
  };

  const cardHeaderStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '18px 20px',
    cursor: 'pointer',
    backgroundColor: '#fafafa',
    transition: 'background-color 0.2s',
  };

  const nameStyle = {
    fontWeight: '700',
    fontSize: '1.15rem',
    color: '#2c3e50',
  };

  const metaStyle = {
    display: 'flex',
    gap: '16px',
    fontSize: '0.9rem',
    color: '#666',
  };

  const cuisineBadgeStyle = {
    backgroundColor: '#eef2ff',
    color: '#2563eb',
    padding: '3px 10px',
    borderRadius: '12px',
    fontSize: '0.8rem',
    fontWeight: '600',
  };

  const menuContainerStyle = {
    padding: '12px 20px 20px',
    backgroundColor: '#f9fafb',
    borderTop: '1px solid #eee',
  };

  return (
    <div style={listStyle}>
      <h2 style={{ color: '#2c3e50', marginBottom: '4px' }}>
        Restaurants ({restaurants.length})
      </h2>

      {restaurants.length === 0 && (
        <p style={{ color: '#999', textAlign: 'center', padding: '40px' }}>
          No restaurants match your search. Try a different term or cuisine.
        </p>
      )}

      {restaurants.map((restaurant) => (
        <div key={restaurant.id} className="restaurant-card">
          {restaurant.image && (
            <img
              src={restaurant.image}
              alt={restaurant.name}
              className="restaurant-card-img"
            />
          )}
          <div
            style={cardHeaderStyle}
            onClick={() => toggleExpand(restaurant.id)}
          >
            <div>
              <div style={nameStyle}>{restaurant.name}</div>
              <div style={metaStyle}>
                <span className="star-badge">{restaurant.rating}</span>
                <span className="delivery-badge">{restaurant.deliveryTime}</span>
              </div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <span style={cuisineBadgeStyle}>{restaurant.cuisine}</span>
              <span style={{ fontSize: '1.2rem', color: '#888' }}>
                {expandedId === restaurant.id ? '▲' : '▼'}
              </span>
            </div>
          </div>

          {expandedId === restaurant.id && (
            <div style={menuContainerStyle}>
              <h3 style={{ margin: '0 0 12px', color: '#2c3e50', fontSize: '1rem' }}>
                Menu
              </h3>
              {restaurant.menu.map((menuItem) => (
                <MenuCard
                  key={menuItem.id}
                  item={menuItem}
                  onAddToCart={onAddToCart}
                />
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default RestaurantList;
