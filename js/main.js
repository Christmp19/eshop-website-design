document.addEventListener("DOMContentLoaded", function () {
    const cartBadge = document.querySelector('.badge1');
    const cartCount = document.querySelector('.badge');
    const cartList = document.querySelector('.cart-list');

    function updateCartDisplay(itemCount) {
        cartBadge.textContent = `Cart (${itemCount})`;
        cartCount.textContent = `(${itemCount})`;
    }

    function renderCartItems(cartItems) {
        cartList.innerHTML = '';
        cartItems.forEach(item => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <div class="item-info">
                    <span>Name</span>
                    <span>Price</span>
                    <span>Quantity</span>
                </div>
                <div class="item-info">
                    <span>${item.name}</span>
                    <span>$${item.price}</span>
                    <span>${item.quantity}</span>
                </div>

                <div class="item-actions">
                <button class="remove" data-product-id="${item.product_id}">Remove</button>
                </div>
            `;
            cartList.appendChild(listItem);
        });

        // Attach remove event listeners
        document.querySelectorAll('.item-actions .remove').forEach(button => {
            button.addEventListener('click', function () {
                const productId = parseInt(this.getAttribute('data-product-id'));
                removeFromCart(productId);
            });
        });
    }

    function updateCartCount() {
        fetch('http://localhost:8000/cart')
            .then(response => response.json())
            .then(cart => {
                const itemCount = cart.reduce((total, item) => total + item.quantity, 0);
                updateCartDisplay(itemCount);
                renderCartItems(cart);
            })
            .catch(error => console.error('Error fetching cart:', error));
    }

    function addToCart(productId) {
        fetch(`http://localhost:8000/cart/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: productId })
        })
            .then(response => response.json())
            .then(cartItem => {
                updateCartCount();
                alert(`Product added to cart: ${cartItem.name}`);
            })
            .catch(error => console.error('Error adding to cart:', error));
    }

    function removeFromCart(productId) {
        fetch(`http://localhost:8000/cart/remove/${productId}`, {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(cartItem => {
                updateCartCount();
                alert(`Product removed from cart: ${cartItem.name}`);
            })
            .catch(error => console.error('Error removing from cart:', error));
    }

    function clearCart() {
        fetch('http://localhost:8000/cart/clear', {
            method: 'DELETE'
        })
            .then(response => response.json())
            .then(data => {
                updateCartCount();
                alert(data.message);
            })
            .catch(error => console.error('Error clearing cart:', error));
    }

    // Example of handling add-to-cart buttons
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function () {
            const productId = parseInt(this.getAttribute('data-product-id'));
            addToCart(productId);
        });
    });

    // Initialize cart display
    updateCartCount();

    // Handle clear cart button
    const clearCartButton = document.querySelector('#clear-cart-button');
    if (clearCartButton) {
        clearCartButton.addEventListener('click', function () {
            clearCart();
        });
    }
});
