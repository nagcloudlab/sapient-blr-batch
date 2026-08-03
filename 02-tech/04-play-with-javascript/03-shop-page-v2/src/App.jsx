
import React, { useState } from 'react'
import Navbar from './components/Navbar';
import ProductList from './components/ProductList';

function App() {
  const title = "Shop IT"

  return (
    <div className="container">
      <Navbar title={title} />
      <hr />
      {0} item(s) in the cart
      <hr />
      <ProductList />
    </div>
  )
}

export default App