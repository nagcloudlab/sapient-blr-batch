// FoodExpress - Header Component (SOLUTION)
// Renders the top navigation bar with logo, search box, cuisine filter,
// and cart icon.
//
// ========================================================================
// FIX: Changed handleSearch to pass `e.target.value` instead of the raw
//      event object `e` to onSearchChange.
//
//      Root cause: onSearchChange (which is App's setSearchTerm) expects
//      a string. The buggy code passed the entire SyntheticEvent object,
//      so searchTerm became "[object Object]" and no restaurant name
//      could ever match that string.
//
//      Lesson: Always check what the callback expects. React's onChange
//      gives you an event — you must extract .target.value yourself.
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

  // FIX: Extract e.target.value and pass the string to onSearchChange
  const handleSearch = (e) => {
    onSearchChange(e.target.value); // <-- FIX: was `onSearchChange(e)`
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
