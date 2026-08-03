// FoodExpress - MenuCard Component (SOLUTION)
// Displays a single menu item with name, price, and an "Add to Cart" button.
//
// ========================================================================
// FIX: Added `item.price` to the useEffect dependency array so that
//      displayPrice stays in sync whenever the prop changes.
//
//      Root cause: The original code used an empty dependency array [],
//      which meant the effect only ran on mount. When item.price changed
//      (e.g., during a flash sale), displayPrice remained stale.
//
//      Alternative (simpler) fix: remove local state entirely and just
//      render item.price directly. Local state is unnecessary here because
//      the price is derived data. However, we keep the useEffect approach
//      to demonstrate proper dependency management.
// ========================================================================

import React, { useState, useEffect } from 'react';

function MenuCard({ item, onAddToCart }) {
  const [displayPrice, setDisplayPrice] = useState(item.price);
  const [added, setAdded] = useState(false);

  // FIX: Added [item.price] as the dependency so the effect re-runs
  // whenever the price prop changes, keeping displayPrice in sync.
  useEffect(() => {
    setDisplayPrice(item.price);
  }, [item.price]); // <-- FIX: was [] (empty), now [item.price]

  const cardStyle = {
    border: '1px solid #e0e0e0',
    borderRadius: '10px',
    padding: '16px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
    backgroundColor: '#ffffff',
    transition: 'box-shadow 0.2s',
  };

  const infoStyle = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  };

  const emojiStyle = {
    fontSize: '2rem',
  };

  const nameStyle = {
    fontWeight: '600',
    fontSize: '1rem',
    color: '#2c3e50',
  };

  const priceStyle = {
    color: '#27ae60',
    fontWeight: '700',
    fontSize: '0.95rem',
  };

  const buttonStyle = {
    backgroundColor: '#e84c3d',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    padding: '8px 16px',
    cursor: 'pointer',
    fontWeight: '600',
    fontSize: '0.9rem',
  };

  return (
    <div style={cardStyle}>
      <div style={infoStyle}>
        <span style={emojiStyle}>{item.image}</span>
        <div>
          <div style={nameStyle}>{item.name}</div>
          {/* FIX: displayPrice now stays in sync with item.price */}
          <div style={priceStyle}>${displayPrice.toFixed(2)}</div>
        </div>
      </div>
      <button
        className={`add-btn${added ? ' added' : ''}`}
        onClick={() => {
          onAddToCart(item);
          setAdded(true);
          setTimeout(() => setAdded(false), 1500);
        }}
      >
        {added ? 'Added!' : 'Add to Cart'}
      </button>
    </div>
  );
}

export default MenuCard;
