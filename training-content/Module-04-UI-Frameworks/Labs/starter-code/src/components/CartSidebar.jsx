// FoodExpress - CartSidebar Component
// A slide-in sidebar showing cart contents, quantities, and total.
//
// ========================================================================
// BUG: Cart count badge does not reflect the actual cart size.
// Expected: The badge should always show the real number of items in the
//           cart (passed via the `cartCount` prop from App).
// ========================================================================

import React, { useState } from 'react';

function CartSidebar({ isOpen, cart, cartCount, cartTotal, onClose, onRemove, onUpdateQuantity }) {
  // BUG: localCount is initialised from the prop but never updated when
  // cartCount changes. This means adding/removing items won't update
  // the count shown inside the sidebar header.
  const [localCount] = useState(cartCount); // <-- should use cartCount prop directly

  const overlayStyle = {
    display: isOpen ? 'block' : 'none',
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0,0,0,0.4)',
    zIndex: 999,
  };

  const sidebarStyle = {
    position: 'fixed',
    top: 0,
    right: isOpen ? '0' : '-400px',
    width: '380px',
    height: '100%',
    backgroundColor: '#fff',
    boxShadow: '-4px 0 20px rgba(0,0,0,0.15)',
    zIndex: 1000,
    transition: 'right 0.3s ease',
    display: 'flex',
    flexDirection: 'column',
    fontFamily: 'Segoe UI, sans-serif',
  };

  const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px',
    borderBottom: '2px solid #e84c3d',
    backgroundColor: '#2c3e50',
    color: '#fff',
  };

  const closeBtnStyle = {
    background: 'none',
    border: 'none',
    color: '#fff',
    fontSize: '1.5rem',
    cursor: 'pointer',
  };

  const itemsContainerStyle = {
    flex: 1,
    overflowY: 'auto',
    padding: '16px',
  };

  const cartItemStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '12px 0',
    borderBottom: '1px solid #eee',
  };

  const qtyBtnStyle = {
    width: '28px',
    height: '28px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    backgroundColor: '#f8f8f8',
    cursor: 'pointer',
    fontSize: '1rem',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
  };

  const removeBtnStyle = {
    background: 'none',
    border: 'none',
    color: '#e84c3d',
    cursor: 'pointer',
    fontSize: '0.85rem',
    fontWeight: '600',
  };

  const footerStyle = {
    padding: '20px',
    borderTop: '2px solid #e0e0e0',
  };

  const totalStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    fontWeight: '700',
    fontSize: '1.2rem',
    color: '#2c3e50',
    marginBottom: '16px',
  };

  const checkoutBtnStyle = {
    width: '100%',
    padding: '14px',
    backgroundColor: '#27ae60',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1.05rem',
    fontWeight: '700',
    cursor: 'pointer',
  };

  return (
    <>
      <div style={overlayStyle} onClick={onClose} />
      <div style={sidebarStyle}>
        <div style={headerStyle}>
          {/* BUG: localCount never updates — badge is frozen at the initial value */}
          <h2 style={{ margin: 0 }}>Your Cart ({localCount})</h2>
          <button style={closeBtnStyle} onClick={onClose}>&times;</button>
        </div>

        <div style={itemsContainerStyle}>
          {cart.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#999', marginTop: '40px' }}>
              Your cart is empty. Add some delicious items!
            </p>
          ) : (
            cart.map((ci) => (
              <div key={ci.id} style={cartItemStyle}>
                <div>
                  <div style={{ fontWeight: '600', color: '#2c3e50' }}>
                    {ci.image} {ci.name}
                  </div>
                  <div style={{ color: '#27ae60', fontWeight: '600' }}>
                    ${ci.price.toFixed(2)}
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <button
                    style={qtyBtnStyle}
                    onClick={() => onUpdateQuantity(ci.id, ci.quantity - 1)}
                  >
                    -
                  </button>
                  <span style={{ fontWeight: '600', minWidth: '20px', textAlign: 'center' }}>
                    {ci.quantity}
                  </span>
                  <button
                    style={qtyBtnStyle}
                    onClick={() => onUpdateQuantity(ci.id, ci.quantity + 1)}
                  >
                    +
                  </button>
                  <button style={removeBtnStyle} onClick={() => onRemove(ci.id)}>
                    Remove
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {cart.length > 0 && (
          <div style={footerStyle}>
            <div style={totalStyle}>
              <span>Total:</span>
              <span>${cartTotal.toFixed(2)}</span>
            </div>
            <button style={checkoutBtnStyle}>
              Proceed to Checkout
            </button>
          </div>
        )}
      </div>
    </>
  );
}

export default CartSidebar;
