
import { useState } from 'react';
import Review from './Review';

import { useContext } from 'react';
import CartContext from '../context/CartContext';

function Product({ product }) {

    const [currentTab, setCurrentTab] = useState(1);
    const { cart, onBuy } = useContext(CartContext);

    const reviews = [
        { id: 1, author: 'John Doe', stars: 5, content: 'Great product!' },
        { id: 2, author: 'Jane Smith', stars: 4, content: 'Good value for money.' },
        { id: 3, author: 'Alice Johnson', stars: 5, content: 'Highly recommend this.' }
    ];

    const isInCart = cart.some(item => item.id === product.id);
    let qty = 0;
    if (isInCart) {
        const cartItem = cart.find(item => item.id === product.id);
        qty = cartItem.quantity;
    }

    const handleTabChange = (tabIndex) => {
        setCurrentTab(tabIndex);
    }

    const renderTabPanel = (tabIndex, product) => {
        switch (tabIndex) {
            case 1:
                return <div>{product.description}</div>;
            case 2:
                return <div>Specification content goes here.</div>;
            case 3:
                return (
                    <div>
                        {reviews.map((review) => (
                            <Review key={review.id} review={review} />
                        ))}
                    </div>
                );
            default:
                return null;
        }
    };

    const handleAddToCart = () => {
        console.log(`Added ${product.name} to cart.`);
        if (onBuy) {
            onBuy(product);
        }
    }

    return (
        <div className="row" key={product.id}>
            <div className="col-md-4">
                <img src={product.imagePath} alt={product.name} className="img-fluid" />
            </div>
            <div className="col-md-8">
                <div>{product.name}</div>
                <div>&#8377;{product.price}</div>
                <button disabled={isInCart} onClick={handleAddToCart} className="btn btn-primary">Add to Cart</button>
                <span className="ms-2">Qty: {qty}</span>
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
    );
}

export default Product;