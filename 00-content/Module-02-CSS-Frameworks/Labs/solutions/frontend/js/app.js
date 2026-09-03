/**
 * FoodExpress Frontend - Module 02 (Solution)
 * Same as starter - JS bugs will be introduced in Module 03
 */

let cart = [];

// ==================== CART FUNCTIONS ====================

function addToCart(id, name, price, restaurant) {
  const existing = cart.find(item => item.id === id);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ id, name, price: parseFloat(price), restaurant, quantity: 1 });
  }
  updateCartDisplay();
}

function removeFromCart(id) {
  cart = cart.filter(item => item.id !== id);
  updateCartDisplay();
}

function updateCartDisplay() {
  const cartItemsEl = document.getElementById('cart-items');
  const cartTotalEl = document.getElementById('cart-total');
  const cartCountEl = document.getElementById('cart-count');
  const modalSubtotal = document.getElementById('modal-subtotal');

  const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
  cartCountEl.textContent = totalItems;

  if (cart.length === 0) {
    cartItemsEl.innerHTML = '<p class="text-muted text-center mt-4"><i class="bi bi-cart-x" style="font-size: 2rem;"></i><br>Your cart is empty</p>';
    cartTotalEl.textContent = '$0.00';
    if (modalSubtotal) modalSubtotal.textContent = '$0.00';
    return;
  }

  let html = '';
  let total = 0;

  cart.forEach(item => {
    const itemTotal = item.price * item.quantity;
    total += itemTotal;
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
  cartTotalEl.textContent = `$${total.toFixed(2)}`;
  if (modalSubtotal) modalSubtotal.textContent = `$${total.toFixed(2)}`;
}

// ==================== CUISINE FILTER ====================

document.addEventListener('DOMContentLoaded', function() {
  // Cuisine filter pills
  const filterLinks = document.querySelectorAll('#cuisine-filter .nav-link');
  filterLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      filterLinks.forEach(l => l.classList.remove('active'));
      this.classList.add('active');

      const cuisine = this.dataset.cuisine;
      const cards = document.querySelectorAll('#restaurant-grid > div');

      cards.forEach(card => {
        if (cuisine === 'all') {
          card.style.display = '';
        } else {
          const cuisineText = card.querySelector('.card-text small');
          if (cuisineText && cuisineText.textContent.toLowerCase().includes(cuisine)) {
            card.style.display = '';
          } else {
            card.style.display = 'none';
          }
        }
      });
    });
  });

  // Add to cart buttons
  document.querySelectorAll('.add-to-cart').forEach(btn => {
    btn.addEventListener('click', function() {
      addToCart(
        this.dataset.id,
        this.dataset.name,
        this.dataset.price,
        this.dataset.restaurant
      );
    });
  });
});
