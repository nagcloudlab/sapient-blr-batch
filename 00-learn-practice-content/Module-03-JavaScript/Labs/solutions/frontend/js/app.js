/**
 * FoodExpress Frontend - Module 03 (SOLUTION)
 * All bugs fixed, validation added, DOM manipulation corrected
 */

const menuData = {
  'burger-barn': [
    { id: 101, name: 'Classic Smash Burger', price: 8.99, category: 'mains', stock: 45 },
    { id: 102, name: 'BBQ Bacon Burger', price: 10.99, category: 'mains', stock: 30 },
    { id: 103, name: 'Loaded Cheese Fries', price: 4.99, category: 'sides', stock: 80 },
    { id: 104, name: 'Chocolate Milkshake', price: 5.99, category: 'drinks', stock: 50 },
  ],
  'pizza-palace': [
    { id: 201, name: 'Margherita Pizza', price: 12.99, category: 'mains', stock: 25 },
    { id: 202, name: 'Pepperoni Pizza', price: 14.99, category: 'mains', stock: 20 },
    { id: 203, name: 'Garlic Bread', price: 3.99, category: 'sides', stock: 60 },
    { id: 204, name: 'Tiramisu', price: 6.99, category: 'desserts', stock: 15 },
  ],
  'dragon-wok': [
    { id: 301, name: 'Fried Rice', price: 9.99, category: 'mains', stock: 40 },
    { id: 302, name: 'Spring Rolls', price: 5.99, category: 'sides', stock: 0 },
    { id: 303, name: 'Kung Pao Chicken', price: 11.99, category: 'mains', stock: 35 },
  ],
};

// Load cart from localStorage (persists across pages)
let cart = JSON.parse(localStorage.getItem('foodexpress-cart') || '[]');
let discountValue = parseInt(localStorage.getItem('foodexpress-discount') || '0');

function saveCart() {
  localStorage.setItem('foodexpress-cart', JSON.stringify(cart));
  localStorage.setItem('foodexpress-discount', String(discountValue));
}

// ==================== CART FUNCTIONS ====================

// FIX #1: Check if item exists before adding
function addToCart(id, name, price, restaurant) {
  const existing = cart.find(item => item.id === id);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({
      id,
      name,
      price: parseFloat(price),
      restaurant,
      quantity: 1
    });
  }
  saveCart();
  updateCartDisplay();
}

// FIX #2: Correct calculation -- price * quantity, numeric discount
function getCartTotal() {
  let total = 0;
  cart.forEach(item => {
    total += item.price * item.quantity;
  });

  if (discountValue > 0) {
    total = total * (1 - discountValue / 100);
  }

  return total;
}

function removeFromCart(itemId) {
  cart = cart.filter(item => item.id !== itemId);
  saveCart();
  updateCartDisplay();
}

// FIX: Store numeric discount value, not the code string
function applyDiscount(code) {
  const validCodes = { 'SAVE10': 10, 'SAVE20': 20, 'FIRST50': 50 };
  if (validCodes[code]) {
    discountValue = validCodes[code];
    saveCart();
    updateCartDisplay();
    return true;
  }
  return false;
}

// ==================== DISPLAY ====================

function updateCartDisplay() {
  const cartItemsEl = document.getElementById('cart-items');
  const cartTotalEl = document.getElementById('cart-total');
  const cartCountEl = document.getElementById('cart-count');

  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
  if (cartCountEl) cartCountEl.textContent = totalItems;

  if (cart.length === 0) {
    cartItemsEl.innerHTML = '<p class="text-muted text-center mt-4">Your cart is empty</p>';
    cartTotalEl.textContent = '$0.00';
    return;
  }

  let html = '';
  cart.forEach(item => {
    html += `
      <div class="d-flex justify-content-between align-items-center mb-2 pb-2 border-bottom">
        <div>
          <small class="fw-bold">${item.name}</small><br>
          <small class="text-muted">${item.restaurant} | $${item.price.toFixed(2)} x ${item.quantity}</small>
        </div>
        <div>
          <button class="btn btn-sm btn-outline-danger" onclick="removeFromCart('${item.id}')">
            <i class="bi bi-trash"></i>
          </button>
        </div>
      </div>
    `;
  });

  cartItemsEl.innerHTML = html;
  const total = getCartTotal();
  cartTotalEl.textContent = `$${total.toFixed(2)}`;

  // Also update modal subtotal if visible
  const modalSubtotal = document.getElementById('modal-subtotal');
  if (modalSubtotal) modalSubtotal.textContent = `$${total.toFixed(2)}`;
}

// ==================== CUISINE FILTERING ====================

// FIX #4: Only update the grid, not the entire page
function filterByCuisine(cuisine) {
  const cards = document.querySelectorAll('#restaurant-grid > div');
  cards.forEach(card => {
    if (cuisine === 'all') {
      card.style.display = '';
    } else {
      const text = card.querySelector('.card-text small');
      if (text && text.textContent.toLowerCase().includes(cuisine)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    }
  });
}

// ==================== CHECKOUT VALIDATION ====================

// FIX #3: Validate and prevent default
function handleCheckout(e) {
  e.preventDefault();

  const name = document.getElementById('name')?.value.trim();
  const phone = document.getElementById('phone')?.value.trim();
  const address = document.getElementById('address')?.value.trim();

  const errors = [];
  if (!name) errors.push({ field: 'name', msg: 'Name is required' });
  if (phone && !/^\d{10}$/.test(phone)) errors.push({ field: 'phone', msg: 'Phone must be 10 digits' });
  if (!address) errors.push({ field: 'address', msg: 'Address is required' });

  clearErrors();

  if (errors.length > 0) {
    errors.forEach(err => showFieldError(err.field, err.msg));
    return;
  }

  alert('Order placed successfully!');
}

function showFieldError(fieldId, message) {
  const field = document.getElementById(fieldId);
  if (!field) return;
  field.classList.add('is-invalid');
  const errDiv = document.createElement('div');
  errDiv.className = 'invalid-feedback';
  errDiv.textContent = message;
  field.parentNode.appendChild(errDiv);
}

function clearErrors() {
  document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
  document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
}

// ==================== CHECKOUT PAGE ====================

function renderCheckout() {
  const checkoutItems = document.getElementById('checkout-items');
  const checkoutSubtotal = document.getElementById('checkout-subtotal');
  const checkoutTotal = document.getElementById('checkout-total');
  if (!checkoutItems) return; // not on checkout page

  if (cart.length === 0) {
    checkoutItems.innerHTML = '<p class="text-muted">No items in cart. <a href="index.html">Browse restaurants</a></p>';
    return;
  }

  let html = '';
  let subtotal = 0;
  cart.forEach(item => {
    const itemTotal = item.price * item.quantity;
    subtotal += itemTotal;
    html += `
      <div class="d-flex justify-content-between mb-2">
        <div>
          <span class="fw-bold">${item.name}</span>
          <small class="text-muted d-block">${item.restaurant} | $${item.price.toFixed(2)} x ${item.quantity}</small>
        </div>
        <span class="fw-bold">$${itemTotal.toFixed(2)}</span>
      </div>
    `;
  });

  checkoutItems.innerHTML = html;
  if (checkoutSubtotal) checkoutSubtotal.textContent = `$${subtotal.toFixed(2)}`;

  const deliveryFee = subtotal >= 25 ? 0 : 2.99;
  const deliveryEl = document.getElementById('checkout-delivery');
  if (deliveryEl) deliveryEl.textContent = deliveryFee === 0 ? 'FREE' : `$${deliveryFee.toFixed(2)}`;

  let total = subtotal + deliveryFee;
  if (discountValue > 0) {
    total = total * (1 - discountValue / 100);
  }
  if (checkoutTotal) checkoutTotal.textContent = `$${total.toFixed(2)}`;
}

// ==================== EVENT LISTENERS ====================

document.addEventListener('DOMContentLoaded', function() {
  // Render checkout page if on checkout.html
  renderCheckout();

  // Update cart display on index.html (if cart was loaded from localStorage)
  if (document.getElementById('cart-items')) {
    updateCartDisplay();
  }
  // Cuisine filter
  const filterLinks = document.querySelectorAll('#cuisine-filter .nav-link');
  filterLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      filterLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');
      filterByCuisine(this.dataset.cuisine);
    });
  });

  // Add to cart buttons -- use event delegation for buttons inside modals
  document.addEventListener('click', function(e) {
    const btn = e.target.closest('.add-to-cart');
    if (btn) {
      e.preventDefault();
      e.stopPropagation();
      addToCart(btn.dataset.id, btn.dataset.name, btn.dataset.price, btn.dataset.restaurant);
    }
  });

  // Discount code
  const discountBtn = document.getElementById('apply-discount');
  if (discountBtn) {
    discountBtn.addEventListener('click', function() {
      const code = document.getElementById('discount-code')?.value.trim();
      if (code && applyDiscount(code)) {
        alert('Discount applied!');
      } else {
        alert('Invalid discount code');
      }
    });
  }

  // Checkout form
  const checkoutForm = document.getElementById('checkout-form');
  if (checkoutForm) {
    checkoutForm.addEventListener('submit', handleCheckout);
  }

  // Disable closed restaurant buttons
  document.querySelectorAll('.card').forEach(card => {
    const status = card.querySelector('.text-danger');
    if (status && status.textContent.includes('Closed')) {
      const btn = card.querySelector('.btn');
      if (btn) {
        btn.classList.add('disabled');
        btn.setAttribute('tabindex', '-1');
      }
    }
  });
});
