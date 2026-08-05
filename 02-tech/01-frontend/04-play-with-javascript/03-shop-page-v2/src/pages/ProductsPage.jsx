import ProductList from '../components/ProductList';

function ProductsPage({ onBuy }) {
    return (
        <section>
            <div className="d-flex align-items-center justify-content-between mb-3">
                <h2 className="h4 mb-0">Products</h2>
                <small className="text-secondary">Add items to your cart from here</small>
            </div>
            <ProductList onBuy={onBuy} />
        </section>
    );
}

export default ProductsPage;
