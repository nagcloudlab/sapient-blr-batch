/**
 * FoodExpress Frontend - Module 03
 * Cart management, cuisine filtering, form validation
 *
 * Known issues (from client reports):
 * - Cart duplicates items instead of incrementing
 * - Total shows NaN with discount code
 * - Category filter causes full page re-render
 * - Checkout form submits with empty fields
 */

// Restaurant/menu data (simulating API response)
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

// Cart persists across pages via localStorage
let cart = JSON.parse(localStorage.getItem('foodexpress-cart') || '[]');
let discountCode = localStorage.getItem('foodexpress-discount') || null;

function saveCart() {
  localStorage.setItem('foodexpress-cart', JSON.stringify(cart));
  if (discountCode) localStorage.setItem('foodexpress-discount', discountCode);
}

// ==================== CART FUNCTIONS ====================

/**
 * BUG #1: Adding same item creates duplicate instead of incrementing quantity
 *
 * Current behavior: Always pushes a new object to cart array
 * Expected: If item already in cart, increment its quantity
 */
function addToCart(id, name, price, restaurant) {
  // BUG: Always creates new entry -- never checks if item already exists
  const cartItem = {
    id: id,
    name: name,
    price: parseFloat(price),
    restaurant: restaurant,
    quantity: 1
  };
  cart.push(cartItem);

  saveCart();
  updateCartDisplay();
}

/**
 * BUG #2: Cart total returns NaN when discount is applied
 *
 * Issue 1: price + quantity instead of price * quantity
 * Issue 2: Subtracting the string discount code instead of numeric value
 */
function getCartTotal() {
  let total = 0;

  cart.forEach(item => {
    // BUG: Should be item.price * item.quantity
    total = total + item.price + item.quantity;
  });

  // BUG: discountCode stores the code string like "SAVE10"
  // We subtract the STRING "10" instead of calculating the numeric discount
  if (discountCode) {
    total = total - discountCode;  // String subtraction = NaN
  }

  return total;
}

function removeFromCart(itemId) {
  cart = cart.filter(item => item.id !== itemId);
  saveCart();
  updateCartDisplay();
}

function applyDiscount(code) {
  const validCodes = { 'SAVE10': 10, 'SAVE20': 20, 'FIRST50': 50 };
  if (validCodes[code]) {
    discountCode = code;  // BUG: stores the code string, not the numeric value
    updateCartDisplay();
    return true;
  }
  return false;
}

// ==================== DISPLAY FUNCTIONS ====================

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
  cartTotalEl.textContent = `$${total.toFixed(2)}`;  // BUG: NaN.toFixed(2) = "NaN"
}

// ==================== CUISINE FILTERING ====================

/**
 * BUG #4: Cuisine filter re-renders ENTIRE page
 *
 * Current: Uses document.body.innerHTML = '' which clears everything
 * Expected: Only update the #restaurant-grid section
 */
function filterByCuisine(cuisine) {
  // BUG: This clears the ENTIRE page including header, footer, cart
  document.body.innerHTML = '';
  location.reload();  // Forces full page reload

  // What it SHOULD do:
  // const cards = document.querySelectorAll('#restaurant-grid > div');
  // cards.forEach(card => {
  //   if (cuisine === 'all') {
  //     card.style.display = '';
  //   } else {
  //     const text = card.querySelector('.card-text small');
  //     if (text && text.textContent.toLowerCase().includes(cuisine)) {
  //       card.style.display = '';
  //     } else {
  //       card.style.display = 'none';
  //     }
  //   }
  // });
}

// ==================== CHECKOUT VALIDATION ====================

/**
 * BUG #3: Checkout form submits with empty required fields
 *
 * Missing: e.preventDefault() and field validation
 */
function handleCheckout(e) {
  // BUG: No preventDefault -- form reloads the page
  // BUG: No validation -- empty fields are accepted

  const name = document.getElementById('name')?.value;
  const phone = document.getElementById('phone')?.value;

  // Should validate but doesn't
  console.log('Order submitted:', { name, phone });

  // Should show success message but just logs
}

// ==================== EVENT LISTENERS ====================

// ==================== CHECKOUT PAGE ====================

function renderCheckout() {
  const checkoutItems = document.getElementById('checkout-items');
  const checkoutSubtotal = document.getElementById('checkout-subtotal');
  const checkoutTotal = document.getElementById('checkout-total');
  if (!checkoutItems) return;

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
  if (checkoutTotal) checkoutTotal.textContent = `$${total.toFixed(2)}`;
}

// ==================== EVENT LISTENERS ====================

document.addEventListener('DOMContentLoaded', function() {
  // Render checkout if on checkout page
  renderCheckout();

  // Update cart display on index page (reload from localStorage)
  if (document.getElementById('cart-items')) {
    updateCartDisplay();
  }
  // Cuisine filter pills
  const filterLinks = document.querySelectorAll('#cuisine-filter .nav-link');
  filterLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      filterLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');

      const cuisine = this.dataset.cuisine;
      filterByCuisine(cuisine);  // BUG: this function destroys the page
    });
  });

  // Add to cart buttons -- event delegation for modal buttons
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
});
