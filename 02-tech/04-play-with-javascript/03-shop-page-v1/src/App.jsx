
import React, { useState } from 'react'

function App() {
  const title = "Shop IT"

  const products = [
    {
      id: 1,
      name: "Mobile",
      price: 139900,
      imagePath: './Mobile.png',
      description: "Product description goes here. "
    },
    {
      id: 2,
      name: "Laptop",
      price: 124999,
      imagePath: './Laptop.png',
      description: "Product description goes here. "
    },
  ]

  const [currentTab, setCurrentTab] = useState(1);

  const handleTabChange = (tabIndex) => {
    console.log(`Tab changed to index: ${tabIndex}`);
    setCurrentTab(tabIndex);
  }


  const renderTabPanel = (tabIndex, product) => {
    switch (tabIndex) {
      case 1:
        return <div>{product.description}</div>;
      case 2:
        return <div>Specification content goes here.</div>;
      case 3:
        return <div>Reviews content goes here.</div>;
      default:
        return null;
    }
  };

  const renderProducts = () => {
    return products.map((product) => {
      return (
        <div className='list-group-item'>
          <div className="row" key={product.id}>
            <div className="col-md-4">
              <img src={product.imagePath} alt={product.name} className="img-fluid" />
            </div>
            <div className="col-md-8">
              <div>{product.name}</div>
              <div>&#8377;{product.price}</div>
              <button className="btn btn-primary">Add to Cart</button>
              <ul className="nav nav-tabs mt-3">
                <li className="nav-item">
                  <a onClick={() => handleTabChange(1)} className={`nav-link ${currentTab === 1 ? 'active' : ''}`} href="#">Description</a>
                </li>
                <li className="nav-item">
                  <a onClick={() => handleTabChange(2)} className={`nav-link ${currentTab === 2 ? 'active' : ''}`} href="#">Specification</a>
                </li>
                <li className="nav-item">
                  <a onClick={() => handleTabChange(3)} className={`nav-link ${currentTab === 3 ? 'active' : ''}`} href="#">Reviews</a>
                </li>
              </ul>
              {renderTabPanel(currentTab, product)}
            </div>
          </div>
        </div>
      );
    });
  }

  return (
    <div className="container">
      <h1 className="display-1">{title}</h1>
      <hr />
      <div className='list-group'>
        {renderProducts()}
      </div>
    </div>
  )
}

export default App