import { Link } from 'react-router-dom';

function HomePage() {
    return (
        <section className="p-4 p-md-5 bg-light border rounded-3 text-center">
            <h1 className="display-6 fw-semibold mb-3">Welcome to Shop IT</h1>
            <p className="lead text-secondary mb-4">
                Discover premium gadgets, compare products, and checkout with a smooth cart experience.
            </p>
            <div className="d-flex flex-wrap justify-content-center gap-2">
                <Link className="btn btn-dark" to="/products">Browse Products</Link>
                <Link className="btn btn-outline-dark" to="/cart">View Cart</Link>
                <Link className="btn btn-outline-primary" to="/login">Login</Link>
            </div>
        </section>
    );
}

export default HomePage;
