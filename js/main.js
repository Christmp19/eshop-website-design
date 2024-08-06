document.addEventListener("DOMContentLoaded", function () {
    const cartBadge = document.querySelector('.badge1');
    const cartCount = document.querySelector('.badge');
    const cartList = document.querySelector('.cart-list');
    const emptyCartMessage = document.querySelector('#empty-cart-message');
    const CartMessage = document.querySelector('#cart-message');
    const cartActions = document.querySelector('.cart-actions');

    // Fonction pour mettre à jour l'affichage du panier
    function updateCartDisplay(itemCount) {
        cartBadge.textContent = `Cart (${itemCount})`;
        cartCount.textContent = `(${itemCount})`;
    }

    // Fonction pour afficher les éléments du panier
    function renderCartItems(cartItems) {
        cartList.innerHTML = '';

        if (cartItems.length === 0) {
            emptyCartMessage.style.display = 'block';
            CartMessage.style.display = 'none';
            cartActions.style.display = 'none';
            return;
        }

        emptyCartMessage.style.display = 'none';
        CartMessage.style.display = 'block';
        cartActions.style.display = 'flex';

        cartItems.forEach(item => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <div class="item-info">
                    <img src="${item.img_url}" class="img-fluid" alt="${item.name}">
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

        // Attacher des écouteurs d'événements pour supprimer les éléments
        document.querySelectorAll('.item-actions .remove').forEach(button => {
            button.addEventListener('click', function () {
                const productId = parseInt(this.getAttribute('data-product-id'));
                removeFromCart(productId);
            });
        });
    }

    // Fonction pour mettre à jour le compteur du panier
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

    // Fonction pour ajouter un produit au panier
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

    // Exemple de gestion des boutons d'ajout au panier
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function () {
            const productId = parseInt(this.getAttribute('data-product-id'));
            addToCart(productId);
        });
    });

    // Initialiser l'affichage du panier
    updateCartCount();

    // Gestion du bouton pour vider le panier
    const clearCartButton = document.querySelector('#clear-cart-button');
    if (clearCartButton) {
        clearCartButton.addEventListener('click', function () {
            clearCart();
        });
    }

    // Fonction pour récupérer et afficher les produits dans store
    async function fetchAndDisplayHomeProducts() {
        try {
            const response = await fetch('http://localhost:8000/products/home');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const products = await response.json();

            // Afficher les produits pour hommes
            const mensProductsContainer = document.getElementById('home-mens-products');
            mensProductsContainer.innerHTML = products.men.map(createProductCard).join('');

            // Afficher les produits pour femmes
            const womensProductsContainer = document.getElementById('home-womens-products');
            womensProductsContainer.innerHTML = products.women.map(createProductCard).join('');

            // Afficher les produits pour enfants
            const kidsProductsContainer = document.getElementById('home-kids-products');
            kidsProductsContainer.innerHTML = products.kids.map(createProductCard).join('');

            // Attacher les écouteurs d'événements pour les boutons "add to cart" après le chargement des produits
            attachAddToCartListeners();

        } catch (error) {
            console.error('Error fetching home products:', error);
        }
    }

    // Fonction pour afficher les produits de la page de store
    async function fetchAndDisplayProducts() {
        try {
            const response = await fetch('http://localhost:8000/products');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const products = await response.json();

            // Afficher les produits pour hommes
            const mensProductsContainer = document.getElementById('store-mens-products');
            mensProductsContainer.innerHTML = products.men.map(createProductCard).join('');

            // Afficher les produits pour femmes
            const womensProductsContainer = document.getElementById('store-womens-products');
            womensProductsContainer.innerHTML = products.women.map(createProductCard).join('');

            // Afficher les produits pour enfants
            const kidsProductsContainer = document.getElementById('store-kids-products');
            kidsProductsContainer.innerHTML = products.kids.map(createProductCard).join('');

            // Attacher les écouteurs d'événements pour les boutons "add to cart" après le chargement des produits
            attachAddToCartListeners();

        } catch (error) {
            console.error('Error fetching products:', error);
        }
    }

    // Fonction pour créer la carte d'un produit
    function createProductCard(product) {
        return `
            <div class="product-card">
                <a href="#">
                    <img src="${product.img_url}" alt="${product.name}" />
                </a>
                <div class="product-info">
                    <h3><a href="#">${product.name}</a></h3>
                    <div class="color-options">
                        <div class='bagde-black'></div>
                        <div class='bagde-blue'></div>
                        <div class='bagde-white'></div>
                        <div class='bagde-red'></div>
                        <div class='bagde-green'></div>
                    </div>
                    <div class="size-options">
                        <a href="#">XL</a>
                        <a href="#">XXL</a>
                        <a href="#">L</a>
                        <a href="#">M</a>
                        <a href="#">S</a>
                    </div>
                    <div class="product-buttons">
                        <button class="add-to-cart" data-product-id="${product.id}">
                            <img src="./img/cart.svg" alt="cart">
                            Add to cart
                        </button>
                        <a class="view-details" href="#">
                            <img src="./img/arrow-right.svg" alt="arrow-right">
                            View Details
                        </a>
                    </div>
                </div>
            </div>
        `;
    }

    // Fonction pour attacher les écouteurs d'événements aux boutons "add to cart"
    function attachAddToCartListeners() {
        document.querySelectorAll('.add-to-cart').forEach(button => {
            button.addEventListener('click', function () {
                const productId = parseInt(this.getAttribute('data-product-id'));
                addToCart(productId);
            });
        });
    }

    // Appeler la fonction pour charger et afficher les produits
    fetchAndDisplayProducts();

    // Appeler la fonction pour charger et afficher les produits d'accueil
    fetchAndDisplayHomeProducts();
    

});
