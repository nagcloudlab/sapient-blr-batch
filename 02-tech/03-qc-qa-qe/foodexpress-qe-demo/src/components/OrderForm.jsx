import { useState } from 'react';
import { calculateTotal, validateOrder } from '../utils/calculateTotal';

const MENU = [
  { id: 1, name: 'Margherita Pizza', price: 299 },
  { id: 2, name: 'Chicken Biryani', price: 249 },
  { id: 3, name: 'Masala Dosa', price: 99 },
  { id: 4, name: 'Coke', price: 49 },
  { id: 5, name: 'Gulab Jamun', price: 79 },
];

export default function OrderForm() {
  const [cart, setCart] = useState([]);
  const [discount, setDiscount] = useState(0);
  const [couponCode, setCouponCode] = useState('');
  const [couponApplied, setCouponApplied] = useState(false);
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [error, setError] = useState('');

  const addToCart = (menuItem) => {
    setCart((prev) => {
      const existing = prev.find((i) => i.id === menuItem.id);
      if (existing) {
        return prev.map((i) =>
          i.id === menuItem.id ? { ...i, qty: i.qty + 1 } : i
        );
      }
      return [...prev, { ...menuItem, qty: 1 }];
    });
    setError('');
  };

  const removeFromCart = (id) => {
    setCart((prev) => prev.filter((i) => i.id !== id));
  };

  const updateQty = (id, qty) => {
    if (qty < 1) return;
    setCart((prev) => prev.map((i) => (i.id === id ? { ...i, qty } : i)));
  };

  const applyCoupon = () => {
    if (couponCode === 'SAVE20') {
      setDiscount(20);
      setCouponApplied(true);
      setError('');
    } else if (couponCode === 'SAVE10') {
      setDiscount(10);
      setCouponApplied(true);
      setError('');
    } else {
      setError('Invalid coupon code');
      setDiscount(0);
      setCouponApplied(false);
    }
  };

  const placeOrder = () => {
    const validation = validateOrder({
      customerId: 'CUST-001',
      restaurantId: 'REST-001',
      items: cart,
    });
    if (!validation.valid) {
      setError(validation.error);
      return;
    }
    setOrderPlaced(true);
    setError('');
  };

  const totals = calculateTotal(cart, discount);

  if (orderPlaced) {
    return (
      <div className="order-success">
        <h2>Order Confirmed!</h2>
        <p>Order ID: FE-{Math.floor(Math.random() * 10000)}</p>
        <p>Total: Rs {totals.total}</p>
        <button onClick={() => { setOrderPlaced(false); setCart([]); setDiscount(0); setCouponApplied(false); setCouponCode(''); }}>
          New Order
        </button>
      </div>
    );
  }

  return (
    <div className="order-form">
      <h1>FoodExpress - Place Order</h1>

      {/* Menu */}
      <section className="menu">
        <h2>Menu</h2>
        <ul>
          {MENU.map((item) => (
            <li key={item.id} data-testid={`menu-item-${item.id}`}>
              <span>{item.name} - Rs {item.price}</span>
              <button onClick={() => addToCart(item)} data-testid={`add-${item.id}`}>
                Add
              </button>
            </li>
          ))}
        </ul>
      </section>

      {/* Cart */}
      <section className="cart">
        <h2>Cart ({cart.length} items)</h2>
        {cart.length === 0 ? (
          <p data-testid="empty-cart">Your cart is empty</p>
        ) : (
          <table>
            <thead>
              <tr><th>Item</th><th>Price</th><th>Qty</th><th>Total</th><th></th></tr>
            </thead>
            <tbody>
              {cart.map((item) => (
                <tr key={item.id} data-testid={`cart-item-${item.id}`}>
                  <td>{item.name}</td>
                  <td>Rs {item.price}</td>
                  <td>
                    <button onClick={() => updateQty(item.id, item.qty - 1)} data-testid={`dec-${item.id}`}>-</button>
                    <span data-testid={`qty-${item.id}`}>{item.qty}</span>
                    <button onClick={() => updateQty(item.id, item.qty + 1)} data-testid={`inc-${item.id}`}>+</button>
                  </td>
                  <td>Rs {item.price * item.qty}</td>
                  <td><button onClick={() => removeFromCart(item.id)} data-testid={`remove-${item.id}`}>Remove</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {/* Coupon */}
      <section className="coupon">
        <h2>Coupon</h2>
        <input
          type="text"
          placeholder="Enter coupon code"
          value={couponCode}
          onChange={(e) => setCouponCode(e.target.value)}
          data-testid="coupon-input"
          disabled={couponApplied}
        />
        <button onClick={applyCoupon} data-testid="apply-coupon" disabled={couponApplied}>
          {couponApplied ? 'Applied' : 'Apply'}
        </button>
        {couponApplied && <span data-testid="coupon-success">{discount}% off applied!</span>}
      </section>

      {/* Order Summary */}
      <section className="summary">
        <h2>Order Summary</h2>
        <p>Subtotal: <span data-testid="subtotal">Rs {totals.subtotal}</span></p>
        <p>Tax (5%): <span data-testid="tax">Rs {totals.tax}</span></p>
        {discount > 0 && (
          <p>Discount ({discount}%): <span data-testid="discount">- Rs {totals.discount}</span></p>
        )}
        <p><strong>Total: <span data-testid="total">Rs {totals.total}</span></strong></p>
      </section>

      {/* Error */}
      {error && <p className="error" data-testid="error-message">{error}</p>}

      {/* Place Order */}
      <button onClick={placeOrder} data-testid="place-order" disabled={cart.length === 0}>
        Place Order
      </button>
    </div>
  );
}
