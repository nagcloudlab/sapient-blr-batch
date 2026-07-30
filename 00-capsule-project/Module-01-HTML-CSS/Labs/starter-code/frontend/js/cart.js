// Basic cart functionality (minimal JS for Module 01)
// Full JS bugs will be introduced in Module 03

let cart = [];

// Add to cart (basic version)
document.querySelectorAll('.view-menu').forEach(button => {
  button.addEventListener('click', function() {
    if (this.disabled) return;

    const restaurant = this.dataset.restaurant;
    // Placeholder: In Module 03, this will open a menu and add individual items
    alert('Menu for ' + restaurant.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) + ' coming soon!\n\nFor now, try fixing the CSS bugs on this page.');
  });
});

function updateCartDisplay() {
  const cartItems = document.getElementById('cart-items');
  const cartSubtotal = document.getElementById('cart-subtotal');
  const cartTotal = document.getElementById('cart-total');
  const cartBadge = document.getElementById('cart-badge');

  if (cart.length === 0) {
    cartItems.innerHTML = '<p class="text-muted">Your cart is empty. Browse restaurants and add items!</p>';
    cartSubtotal.textContent = '$0.00';
    cartTotal.textContent = '$2.99';
    cartBadge.textContent = 'Cart: 0';
    return;
  }

  let html = '';
  let subtotal = 0;

  cart.forEach((item, index) => {
    html += `
      <div class="d-flex justify-content-between align-items-center mb-2">
        <div>
          <small class="fw-bold">${item.name}</small><br>
          <small class="text-muted">$${item.price.toFixed(2)} x ${item.quantity}</small>
        </div>
        <button class="btn btn-sm btn-outline-danger" onclick="removeItem(${index})">x</button>
      </div>
    `;
    subtotal += item.price * item.quantity;
  });

  const deliveryFee = 2.99;
  const total = subtotal + deliveryFee;

  cartItems.innerHTML = html;
  cartSubtotal.textContent = `$${subtotal.toFixed(2)}`;
  cartTotal.textContent = `$${total.toFixed(2)}`;
  cartBadge.textContent = `Cart: ${cart.length}`;
}

function removeItem(index) {
  cart.splice(index, 1);
  updateCartDisplay();
}
