
import { useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import CartContext from './context/CartContext';
import CartPage from './pages/CartPage';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import ProductsPage from './pages/ProductsPage';

function App() {
  const title = 'Shop IT';
  const [cart, setCart] = useState([]);

  const handleBuy = (product) => {
    const cartLine = { ...product, quantity: 1, total: product.price * 1 };
    if (cart.some((item) => item.id === product.id)) {
      setCart(cart.map((item) => (item.id === product.id
        ? { ...item, quantity: item.quantity + 1, total: item.price * (item.quantity + 1) }
        : item)));
    } else {
      setCart([...cart, cartLine]);
    }
  };

  const handleRemove = (productId) => {
    setCart(cart.filter((item) => item.id !== productId));
  };

  const handleQtyChange = (productId, change) => {
    setCart(cart.map((item) => {
      if (item.id === productId) {
        const newQuantity = item.quantity + change;
        return { ...item, quantity: newQuantity, total: item.price * newQuantity };
      }
      return item;
    }).filter(item => item.quantity > 0));
  };

  return (
    <BrowserRouter>
      <div className="container py-3">
        <CartContext.Provider value={{ cart, onRemove: handleRemove, onQtyChange: handleQtyChange, onBuy: handleBuy }}>
          <Navbar title={title} />
          <main className="mt-4">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/products" element={<ProductsPage onBuy={handleBuy} />} />
              <Route path="/cart" element={<CartPage />} />
              <Route path="/login" element={<LoginPage />} />
            </Routes>
          </main>
        </CartContext.Provider>
      </div>
    </BrowserRouter>
  );
}

export default App;