
import CartBadge from './CartBadge';
import { Link, NavLink } from 'react-router-dom';

function Navbar({ title }) {
    return (
        <nav className="navbar bg-body-tertiary rounded border px-2">
            <div className="container-fluid gap-3">
                <Link className="navbar-brand fw-semibold mb-0" to="/">{title}</Link>

                <ul className="navbar-nav flex-row gap-1 me-auto">
                    <li className="nav-item">
                        <NavLink to="/" end className={({ isActive }) => `nav-link px-2 ${isActive ? 'active fw-semibold' : ''}`}>
                            Home
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <NavLink to="/products" className={({ isActive }) => `nav-link px-2 ${isActive ? 'active fw-semibold' : ''}`}>
                            Products
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <NavLink to="/cart" className={({ isActive }) => `nav-link px-2 ${isActive ? 'active fw-semibold' : ''}`}>
                            Cart
                        </NavLink>
                    </li>
                    <li className="nav-item">
                        <NavLink to="/login" className={({ isActive }) => `nav-link px-2 ${isActive ? 'active fw-semibold' : ''}`}>
                            Login
                        </NavLink>
                    </li>
                </ul>

                <Link to="/cart" className="text-decoration-none" aria-label="Open cart">
                    <CartBadge compact />
                </Link>
            </div>
        </nav>
    );
}

export default Navbar;