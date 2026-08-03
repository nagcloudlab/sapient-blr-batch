// FoodExpress - MenuCard Component
// Displays a single menu item with name, price, and an "Add to Cart" button.
//
// ========================================================================
// BUG: Stale state — the displayed price does not update when the parent
//      passes a new price prop (e.g., during a flash sale).
// Expected: When the `item.price` prop changes, the displayed price should
//           update automatically on screen.
// ========================================================================

import React, { useState, useEffect } from 'react';

function MenuCard({ item, onAddToCart }) {
  // BUG: price is copied into local state but never synced when prop changes.
  // The useEffect below is supposed to keep it in sync, but it is missing
  // `item.price` in its dependency array, so it only runs once on mount.
  const [displayPrice, setDisplayPrice] = useState(item.price);

  // BUG: Empty dependency array means this effect runs only on mount.
  // If item.price changes later, displayPrice stays stale.
  useEffect(() => {
    setDisplayPrice(item.price);
  }, []); // <-- missing item.price dependency

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
          {/* BUG: displayPrice is stale — shows old price even after prop update */}
          <div style={priceStyle}>${displayPrice.toFixed(2)}</div>
        </div>
      </div>
      <button
        className="add-btn"
        onClick={() => onAddToCart(item)}
      >
        Add to Cart
      </button>
    </div>
  );
}

export default MenuCard;
