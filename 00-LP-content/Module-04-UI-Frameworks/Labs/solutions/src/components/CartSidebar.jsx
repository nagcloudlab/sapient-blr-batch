// FoodExpress - CartSidebar Component (SOLUTION)
// A slide-in sidebar showing cart contents, quantities, and total.
//
// ========================================================================
// FIX: Removed the local `localCount` state and use the `cartCount` prop
//      directly in the JSX.
//
//      Root cause: useState(cartCount) captures the initial value of the
//      prop at mount time. React does NOT automatically re-sync state
//      with props — useState only uses its argument as the *initial* value.
//      As the cart changed, localCount stayed frozen at the original value.
//
//      Lesson: Don't copy props into state unless you have a specific
//      reason to "fork" the data. If you just need to display a prop,
//      render it directly.
// ========================================================================

import React from 'react';

// FIX: Removed `useState` import — no longer needed in this component
function CartSidebar({ isOpen, cart, cartCount, cartTotal, onClose, onRemove, onUpdateQuantity }) {
  // FIX: Removed `const [localCount] = useState(cartCount);`
  // Now we use `cartCount` prop directly below.

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
          {/* FIX: Use cartCount prop directly instead of stale localCount */}
          <h2 style={{ margin: 0 }}>Your Cart ({cartCount})</h2>
          <button style={closeBtnStyle} onClick={onClose}>&times;</button>
        </div>

        <div style={itemsContainerStyle}>
          {cart.length === 0 ? (
            <div style={{ textAlign: 'center', color: '#999', marginTop: '40px' }}>
              <span className="empty-cart-icon">🛒</span>
              <p>Your cart is empty. Add some delicious items!</p>
            </div>
          ) : (
            cart.map((ci) => (
              <div key={ci.id} style={cartItemStyle}>
                <div>
                  <div style={{ fontWeight: '600', color: '#2c3e50' }}>
                    {ci.image} {ci.name}
                  </div>
                  <div style={{ color: '#27ae60', fontWeight: '600' }}>
                    ${ci.price.toFixed(2)} x {ci.quantity} = ${(ci.price * ci.quantity).toFixed(2)}
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
