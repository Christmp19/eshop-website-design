document.addEventListener("DOMContentLoaded", function () {
    const cartBadge = document.querySelector('.badge1');
    const cartCount = document.querySelector('.badge');

    // Fonction pour mettre à jour le DOM du panier
    function updateCartDisplay(itemCount) {
        cartBadge.textContent = `Cart (${itemCount})`;
        cartCount.textContent = `(${itemCount})`;
    }

    // Fonction pour récupérer le panier depuis le serveur et mettre à jour l'affichage
    function updateCartCount() {
        fetch('http://localhost:8000/cart')
            .then(response => response.json())
            .then(cart => {
                const itemCount = cart.reduce((total, item) => total + item.quantity, 0);
                updateCartDisplay(itemCount);
            })
            .catch(error => console.error('Error fetching cart:', error));
    }

    // Fonction pour ajouter un produit au panier et mettre à jour le serveur et le DOM
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

    // Fonction pour supprimer un produit du panier
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

    // Fonction pour vider le panier
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

    // Gestionnaires d'événements pour les boutons d'ajout au panier
    const addToCartButtons = document.querySelectorAll('.add-to-cart');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function () {
            const productId = parseInt(this.getAttribute('data-product-id'));
            addToCart(productId);
        });
    });

    // Initialiser l'affichage du panier au chargement de la page
    updateCartCount();

    // Exemple de gestionnaire d'événement pour vider le panier, si vous avez un bouton pour cela
    const clearCartButton = document.querySelector('#clear-cart-button');
    if (clearCartButton) {
        clearCartButton.addEventListener('click', function () {
            clearCart();
        });
    }
});

