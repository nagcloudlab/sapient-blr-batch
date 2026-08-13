// ============================================================
// FoodExpress: Component Tests for OrderForm
// Demonstrates: Integration/Component Testing with RTL
// Maps to Slides: 10 (Integration Testing), 15 (Automation Pyramid)
// ============================================================

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import OrderForm from '../components/OrderForm';

describe('OrderForm - Rendering', () => {
  test('should render the menu with 5 items', () => {
    render(<OrderForm />);
    expect(screen.getByText('FoodExpress - Place Order')).toBeInTheDocument();
    expect(screen.getByText(/Margherita Pizza/)).toBeInTheDocument();
    expect(screen.getByText(/Chicken Biryani/)).toBeInTheDocument();
    expect(screen.getByText(/Masala Dosa/)).toBeInTheDocument();
    expect(screen.getByText(/Coke/)).toBeInTheDocument();
    expect(screen.getByText(/Gulab Jamun/)).toBeInTheDocument();
  });

  test('should show empty cart message initially', () => {
    render(<OrderForm />);
    expect(screen.getByTestId('empty-cart')).toHaveTextContent('Your cart is empty');
  });

  test('should disable Place Order button when cart is empty', () => {
    render(<OrderForm />);
    expect(screen.getByTestId('place-order')).toBeDisabled();
  });
});

describe('OrderForm - Add to Cart', () => {
  test('should add item to cart when Add button is clicked', async () => {
    const user = userEvent.setup();
    render(<OrderForm />);

    await user.click(screen.getByTestId('add-1'));  // Add Pizza
    expect(screen.getByTestId('cart-item-1')).toBeInTheDocument();
    expect(screen.getByTestId('qty-1')).toHaveTextContent('1');
  });

  test('should increment quantity when adding same item twice', async () => {
    const user = userEvent.setup();
    render(<OrderForm />);

    await user.click(screen.getByTestId('add-1'));
    await user.click(screen.getByTestId('add-1'));
    expect(screen.getByTestId('qty-1')).toHaveTextContent('2');
  });

  test('should remove item from cart', async () => {
    const user = userEvent.setup();
    render(<OrderForm />);

    await user.click(screen.getByTestId('add-1'));
    expect(screen.getByTestId('cart-item-1')).toBeInTheDocument();

    await user.click(screen.getByTestId('remove-1'));
    expect(screen.queryByTestId('cart-item-1')).not.toBeInTheDocument();
  });
});

describe('OrderForm - Order Summary', () => {
  test('should show correct subtotal and tax', async () => {
    const user = userEvent.setup();
    render(<OrderForm />);

    await user.click(screen.getByTestId('add-3'));  // Masala Dosa Rs 99
    expect(screen.getByTestId('subtotal')).toHaveTextContent('Rs 99');
    expect(screen.getByTestId('tax')).toHaveTextContent('Rs 5');       // 5% of 99 = 4.95 ~ 5
    expect(screen.getByTestId('total')).toHaveTextContent('Rs 104');   // 99 + 5
  });
});

describe('OrderForm - Coupon', () => {
  test('should show error for invalid coupon', async () => {
    const user = userEvent.setup();
    render(<OrderForm />);

    await user.type(screen.getByTestId('coupon-input'), 'INVALID');
    await user.click(screen.getByTestId('apply-coupon'));
    expect(screen.getByTestId('error-message')).toHaveTextContent('Invalid coupon code');
  });

  test('should apply valid coupon SAVE20', async () => {
    const user = userEvent.setup();
    render(<OrderForm />);

    await user.type(screen.getByTestId('coupon-input'), 'SAVE20');
    await user.click(screen.getByTestId('apply-coupon'));
    expect(screen.getByTestId('coupon-success')).toHaveTextContent('20% off applied!');
  });
});

describe('OrderForm - Place Order', () => {
  test('should show error when placing order with empty cart', async () => {
    const user = userEvent.setup();
    render(<OrderForm />);

    // Button is disabled, but let's verify the validation works
    expect(screen.getByTestId('place-order')).toBeDisabled();
  });

  test('should show confirmation after placing order', async () => {
    const user = userEvent.setup();
    render(<OrderForm />);

    await user.click(screen.getByTestId('add-1'));  // Add Pizza
    await user.click(screen.getByTestId('place-order'));
    expect(screen.getByText('Order Confirmed!')).toBeInTheDocument();
  });
});
