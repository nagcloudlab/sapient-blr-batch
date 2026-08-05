
import './CartTable.css';

import { useContext } from 'react';
import CartContext from '../context/CartContext';

function CartTable() {
    const { cart, onRemove, onQtyChange } = useContext(CartContext);
    const currencyFormatter = new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0,
    });

    const totalItems = cart.reduce((sum, cartLine) => sum + cartLine.quantity, 0);
    const grandTotal = cart.reduce((sum, cartLine) => sum + cartLine.price * cartLine.quantity, 0);

    if (cart.length === 0) {
        return (
            <section className="cart-table-shell cart-empty text-center" aria-live="polite">
                <i className="fa fa-shopping-basket cart-empty__icon" aria-hidden="true"></i>
                <h5 className="mb-1">Your cart is empty</h5>
                <p className="text-secondary mb-0">Add products to see a detailed bill summary in INR.</p>
            </section>
        );
    }

    return (
        <section className="cart-table-shell" aria-live="polite">
            <div className="cart-table__header">
                <h5 className="mb-0">Cart Summary</h5>
                <span className="badge text-bg-dark rounded-pill">
                    {totalItems} {totalItems === 1 ? 'item' : 'items'}
                </span>
            </div>

            <div className="table-responsive">
                <table className="table table-hover align-middle cart-table mb-0">
                    <thead>
                        <tr>
                            <th scope="col">Product</th>
                            <th scope="col" className="text-end">Unit Price</th>
                            <th scope="col" className="text-center">Qty</th>
                            <th scope="col" className="text-end">Line Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        {cart.map((cartLine) => {
                            const lineTotal = cartLine.price * cartLine.quantity;

                            return (
                                <tr key={cartLine.id}>
                                    <td className="fw-medium">{cartLine.name}</td>
                                    <td className="text-end">{currencyFormatter.format(cartLine.price)}</td>
                                    <td className="text-center">
                                        <button className='btn btn-sm btn-dark' onClick={() => onQtyChange(cartLine.id, -1)}>-</button>
                                        <span className="badge text-bg-light border">{cartLine.quantity}</span>
                                        <button className='btn btn-sm btn-dark' onClick={() => onQtyChange(cartLine.id, 1)}>+</button>
                                    </td>
                                    <td className="text-end fw-semibold">{currencyFormatter.format(lineTotal)}</td>
                                    <td>
                                        <button
                                            className="btn btn-sm btn-outline-danger"
                                            onClick={() => onRemove(cartLine.id)}
                                        >
                                            <i className="fa fa-trash" aria-hidden="true"></i>
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colSpan="3" className="text-end fw-bold">Grand Total</td>
                            <td className="text-end fw-bold cart-total">{currencyFormatter.format(grandTotal)}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
        </section>
    );
}

export default CartTable;