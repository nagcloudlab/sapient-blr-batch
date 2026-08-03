
import './CartBadge.css';

import { useContext } from 'react';
import CartContext from '../context/CartContext';

function CartBadge({ compact = false }) {
    const { cart } = useContext(CartContext);
    const itemCount = cart.length;
    const itemLabel = itemCount === 1 ? 'item' : 'items';

    return (
        <aside
            className={`cart-badge ${compact ? 'cart-badge--compact' : ''} ${itemCount > 0 ? 'is-active' : 'is-empty'}`}
            aria-live="polite"
            aria-label={`Cart has ${itemCount} ${itemLabel}`}
            title={`Cart has ${itemCount} ${itemLabel}`}
        >
            <div className="cart-badge__icon-wrap" aria-hidden="true">
                <i className="fa fa-shopping-bag"></i>
            </div>

            {!compact && (
                <div className="cart-badge__content">
                    <span className="cart-badge__title">My Cart</span>
                    <span className="cart-badge__subtitle">
                        {itemCount === 0
                            ? 'Your picks will appear here'
                            : `${itemCount} ${itemLabel} selected`}
                    </span>
                </div>
            )}

            <span className="cart-badge__count" title={`${itemCount} ${itemLabel}`}>
                {itemCount}
            </span>
        </aside>
    );
}

export default CartBadge;