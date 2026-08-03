import React, { useState } from 'react';
import Product from './Product';

function ProductList({ onBuy }) {

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

    const renderProducts = () => {
        return products.map((product) => {
            return (
                <div key={product.id} className='list-group-item'>
                    <Product product={product} onBuy={onBuy} />
                </div>
            );
        });
    }

    return (
        <div className='list-group'>
            {renderProducts()}
        </div>
    );

}

export default ProductList;