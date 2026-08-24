// FoodExpress - Header Component
// Renders the top navigation bar with logo, search box, cuisine filter,
// and cart icon.
//
// ========================================================================
// BUG: Typing in the search box does not filter the restaurant list.
// Expected: As the user types, the restaurant list should filter in
//           real time to show only matching restaurant names.
// ========================================================================

import React from 'react';

function Header({ cartCount, searchTerm, onSearchChange, onCartClick, cuisines, selectedCuisine, onCuisineChange }) {
  const headerStyle = {
    backgroundColor: '#2c3e50',
    color: '#fff',
    padding: '14px 24px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: '12px',
    fontFamily: 'Segoe UI, sans-serif',
  };

  const logoStyle = {
    fontSize: '1.6rem',
    fontWeight: '700',
    color: '#e84c3d',
    margin: 0,
  };

  const searchStyle = {
    padding: '8px 14px',
    borderRadius: '6px',
    border: '1px solid #555',
    backgroundColor: '#3d566e',
    color: '#fff',
    fontSize: '0.95rem',
    width: '240px',
    outline: 'none',
  };

  const selectStyle = {
    padding: '8px 12px',
    borderRadius: '6px',
    border: '1px solid #555',
    backgroundColor: '#3d566e',
    color: '#fff',
    fontSize: '0.95rem',
    outline: 'none',
    cursor: 'pointer',
  };

  const cartBtnStyle = {
    backgroundColor: '#e84c3d',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    padding: '8px 18px',
    fontSize: '1rem',
    cursor: 'pointer',
    fontWeight: '600',
    position: 'relative',
  };

  const badgeStyle = {
    position: 'absolute',
    top: '-8px',
    right: '-8px',
    backgroundColor: '#27ae60',
    color: '#fff',
    borderRadius: '50%',
    width: '22px',
    height: '22px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '0.75rem',
    fontWeight: '700',
  };

  // BUG: The search handler reads e.target.value but calls onSearchChange
  // with the wrong argument. Instead of passing the value, it passes the
  // entire event object, so the filter receives "[object Object]".
  const handleSearch = (e) => {
    onSearchChange(e); // <-- should be e.target.value
  };

  return (
    <header style={headerStyle}>
      <h1 style={logoStyle}>FoodExpress</h1>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <input
          type="text"
          placeholder="Search restaurants..."
          style={searchStyle}
          value={searchTerm}
          onChange={handleSearch}
        />

        <select
          style={selectStyle}
          value={selectedCuisine}
          onChange={(e) => onCuisineChange(e.target.value)}
        >
          {cuisines.map((c) => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      <button style={cartBtnStyle} onClick={onCartClick}>
        Cart
        {cartCount > 0 && <span style={badgeStyle}>{cartCount}</span>}
      </button>
    </header>
  );
}

export default Header;
