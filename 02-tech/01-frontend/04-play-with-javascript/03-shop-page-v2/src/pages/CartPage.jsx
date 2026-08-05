import CartTable from '../components/CartTable';

function CartPage() {
    return (
        <section>
            <div className="d-flex align-items-center justify-content-between mb-3">
                <h2 className="h4 mb-0">Your Cart</h2>
                <small className="text-secondary">Review quantity, remove items, and check totals</small>
            </div>
            <CartTable />
        </section>
    );
}

export default CartPage;
