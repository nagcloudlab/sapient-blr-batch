
import React, { useState } from 'react'
import Navbar from './components/Navbar';
import ProductList from './components/ProductList';
import CartBadge from './components/CartBadge';

function App() {
  const title = "Shop IT"
  const [cart, setCart] = useState([]);
  const handleBuy = (product) => {
    setCart([...cart, product]);
  }

  return (
    <div className="container">
      <Navbar title={title} />
      <hr />
      <CartBadge cart={cart} />
      <hr />
      <ProductList onBuy={handleBuy} />
    </div>
  )
}

export default App