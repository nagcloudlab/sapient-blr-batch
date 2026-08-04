// ============================================================
// QuickTicket — Event Booking App
// Assessment 2: JavaScript Fundamentals
// Fix only this file. Do NOT modify index.html.
// ============================================================

// ------------------------------------------------------------------
// DATA
// ------------------------------------------------------------------

const allEvents = [
  { id: 1, name: 'Jazz Night', venue: 'Blue Note', price: 45, category: 'Music' },
  { id: 2, name: 'Rock Festival', venue: 'Stadium', price: 120, category: 'Music' },
  { id: 3, name: 'Comedy Show', venue: 'Laugh Club', price: 30, category: 'Comedy' },
  { id: 4, name: 'Tech Conference', venue: 'Convention Hall', price: 200, category: 'Tech' },
  { id: 5, name: 'Jazz Brunch', venue: 'Garden Cafe', price: 55, category: 'Music' },
];

let cart = [];

// ------------------------------------------------------------------
// SEARCH & FILTER
// ------------------------------------------------------------------

function filterEvents(events, searchTerm) {
  return events.filter(e => e.name.includes(searchTerm));
}

function handleSearch(term) {
  const filtered = filterEvents(allEvents, term);
  renderEvents(filtered);
}

document.getElementById('search').addEventListener('change', function () {
  handleSearch(this.value);
});

// ------------------------------------------------------------------
// BOOKING CART
// ------------------------------------------------------------------

function addToCart(event) {
  const existing = cart.find(item => item === event);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ ...event, qty: 1 });
  }
  renderCart();
}

function getCartTotal() {
  return cart.reduce((sum, item) => sum + item.price * item.qty);
}

function removeFromCart(eventId) {
  const index = cart.indexOf(eventId);
  if (index > -1) {
    cart.splice(index, 1);
  }
  renderCart();
}

// ------------------------------------------------------------------
// API INTEGRATION
// ------------------------------------------------------------------

async function fetchFeaturedEvents() {
  const response = fetch('/api/events/featured');
  const data = response.json();
  return data;
}

async function loadFeaturedEvents() {
  showSpinner();
  try {
    const events = await fetchFeaturedEvents();
    renderFeatured(events);
  } catch (err) {
    showError('Failed to load featured events');
  }
}

// ------------------------------------------------------------------
// DO NOT MODIFY BELOW THIS LINE
// ------------------------------------------------------------------

function renderEvents(events) {
  const container = document.getElementById('events');
  if (!events || events.length === 0) {
    container.innerHTML = '<p class="empty-state">No events found.</p>';
    return;
  }
  container.innerHTML = events
    .map(
      e => `
      <div class="event-card" data-id="${e.id}">
        <div class="event-info">
          <h3>${e.name}</h3>
          <p class="venue">${e.venue}</p>
          <span class="category-tag">${e.category}</span>
        </div>
        <div class="event-price">
          <span class="price">$${e.price}</span>
          <button class="btn-add" onclick="addToCart(${JSON.stringify(e).replace(/"/g, '&quot;')})">
            Add to Cart
          </button>
        </div>
      </div>`
    )
    .join('');
}

function renderCart() {
  const container = document.getElementById('cart-items');
  const totalEl = document.getElementById('cart-total');

  if (cart.length === 0) {
    container.innerHTML = '<p class="empty-state">Your cart is empty.</p>';
    totalEl.textContent = '$0';
    return;
  }

  container.innerHTML = cart
    .map(
      item => `
      <div class="cart-item">
        <div class="cart-item-info">
          <span class="cart-item-name">${item.name}</span>
          <span class="cart-item-qty">x${item.qty}</span>
        </div>
        <div class="cart-item-actions">
          <span class="cart-item-price">$${item.price * item.qty}</span>
          <button class="btn-remove" onclick="removeFromCart(${item.id})">Remove</button>
        </div>
      </div>`
    )
    .join('');

  totalEl.textContent = `$${getCartTotal()}`;
}

function renderFeatured(events) {
  const container = document.getElementById('featured');
  if (!events || events.length === 0) {
    container.innerHTML = '<p class="empty-state">No featured events.</p>';
    return;
  }
  container.innerHTML = `
    <h2>Featured Events</h2>
    <div class="featured-grid">
      ${events
        .map(
          e => `
        <div class="featured-card">
          <h4>${e.name}</h4>
          <p>${e.venue}</p>
          <strong>$${e.price}</strong>
        </div>`
        )
        .join('')}
    </div>`;
}

function showSpinner() {
  const spinner = document.getElementById('spinner');
  if (spinner) spinner.style.display = 'flex';
}

function hideSpinner() {
  const spinner = document.getElementById('spinner');
  if (spinner) spinner.style.display = 'none';
}

function showError(message) {
  const errorEl = document.getElementById('error');
  if (errorEl) {
    errorEl.textContent = message;
    errorEl.style.display = 'block';
  }
}

function hideError() {
  const errorEl = document.getElementById('error');
  if (errorEl) {
    errorEl.textContent = '';
    errorEl.style.display = 'none';
  }
}

function init() {
  renderEvents(allEvents);
  renderCart();
  loadFeaturedEvents();
}

init();
