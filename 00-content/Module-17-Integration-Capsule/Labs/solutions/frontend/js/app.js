/**
 * FoodExpress - Order Page Frontend (FIXED)
 *
 * This file handles the order page UI interactions:
 * - Menu item selection
 * - Cart management
 * - Price calculation
 * - Order submission
 *
 * ALL BUGS FIXED
 */

// Menu data (simulating API response)
const menuItems = [
    { id: 1, name: "Butter Chicken", price: 350, category: "Main Course" },
    { id: 2, name: "Paneer Tikka", price: 280, category: "Starters" },
    { id: 3, name: "Biryani", price: 320, category: "Main Course" },
    { id: 4, name: "Gulab Jamun", price: 120, category: "Desserts" },
    { id: 5, name: "Masala Dosa", price: 180, category: "South Indian" }
];

let cart = [];

// FIX 1: Correct element ID - matches the HTML <div id="menu-container">
document.getElementById("menu-container").addEventListener("click", function(e) {
    if (e.target.classList.contains("add-to-cart-btn")) {
        const itemId = parseInt(e.target.dataset.itemId);
        addToCart(itemId);
    }
});

// Render menu items
function renderMenu() {
    const container = document.getElementById("menu-container");
    menuItems.forEach(item => {
        const div = document.createElement("div");
        div.className = "menu-item";
        div.innerHTML = `
            <h3>${item.name}</h3>
            <p class="category">${item.category}</p>
            <p class="price">Rs. ${item.price}</p>
            <button class="add-to-cart-btn" data-item-id="${item.id}">
                Add to Cart
            </button>
        `;
        container.appendChild(div);
    });
}

// Add item to cart
function addToCart(itemId) {
    const item = menuItems.find(m => m.id === itemId);
    if (!item) return;

    const existing = cart.find(c => c.id === itemId);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ ...item, quantity: 1 });
    }
    updateCartDisplay();
}

// FIX 2: Initialize total as number 0, not string "0"
// This ensures arithmetic addition instead of string concatenation
function calculateTotal() {
    let total = 0;  // FIX: number, not string
    for (let i = 0; i < cart.length; i++) {
        total = total + cart[i].price * cart[i].quantity;
    }
    return total;
}

// Update cart display
function updateCartDisplay() {
    const cartContainer = document.getElementById("cart-items");
    cartContainer.innerHTML = "";

    cart.forEach(item => {
        const div = document.createElement("div");
        div.className = "cart-item";
        div.innerHTML = `
            <span>${item.name} x ${item.quantity}</span>
            <span>Rs. ${item.price * item.quantity}</span>
            <button class="remove-btn" onclick="removeFromCart(${item.id})">
                Remove
            </button>
        `;
        cartContainer.appendChild(div);
    });

    const total = calculateTotal();
    document.getElementById("cart-total").textContent = "Total: Rs. " + total;
}

// Remove item from cart
function removeFromCart(itemId) {
    cart = cart.filter(item => item.id !== itemId);
    updateCartDisplay();
}

// Apply discount
function applyDiscount(code) {
    const discounts = {
        "WELCOME10": 0.10,
        "FOOD20": 0.20,
        "FIRST50": 0.50
    };

    const discount = discounts[code];
    if (discount) {
        const total = calculateTotal();
        const discounted = total - (total * discount);
        document.getElementById("cart-total").textContent =
            "Total: Rs. " + discounted + " (Discount applied!)";
        return discounted;
    } else {
        alert("Invalid discount code!");
        return calculateTotal();
    }
}

// Submit order
function submitOrder() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    const orderData = {
        items: cart,
        total: calculateTotal(),
        timestamp: new Date().toISOString()
    };

    // Simulate API call
    console.log("Submitting order:", JSON.stringify(orderData));
    fetch("/api/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        alert("Order placed successfully! Order ID: " + data.orderId);
        cart = [];
        updateCartDisplay();
    })
    .catch(err => {
        console.error("Order failed:", err);
        alert("Failed to place order. Please try again.");
    });
}

// Initialize
renderMenu();
