class ShoppingCart {
    constructor() {
        this.cartItems = {};
        this.total = 0;
        this.initEventListeners();
    }

    initEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            this.setupAddToCartButtons();
        });
    }

    setupAddToCartButtons() {
        document.querySelectorAll('.agregar-carrito').forEach(button => {
            button.addEventListener('click', () => this.addToCart(button));
        });
    }

    addToCart(button) {
        const id = button.dataset.id;
        const precio = parseFloat(button.dataset.precio);
        const nombre = button.closest('.art-card').querySelector('h3').textContent;
        const cantidad = parseInt(button.closest('.art-card').querySelector('.cantidad').value);

        if (this.cartItems[id]) {
            this.cartItems[id].cantidad += cantidad;
        } else {
            this.cartItems[id] = {
                nombre: nombre,
                precio: precio,
                cantidad: cantidad
            };
        }

        this.updateCart();
        this.showNotification(cantidad, nombre);
    }

    updateCart() {
        const cartItemsDiv = document.getElementById('cartItems');
        const cartTotalSpan = document.getElementById('cartTotal');
        const cartCountSpan = document.getElementById('cartCount');
        cartItemsDiv.innerHTML = '';
        this.total = 0;
        let totalItems = 0;

        for (const id in this.cartItems) {
            const item = this.cartItems[id];
            this.total += item.precio * item.cantidad;
            totalItems += item.cantidad;
            
            const itemDiv = document.createElement('div');
            itemDiv.className = 'cart-item d-flex justify-content-between align-items-center mb-3';
            itemDiv.innerHTML = `
                <div>
                    <h6 class="mb-0">${item.nombre}</h6>
                    <small class="text-muted">${item.cantidad} x S/. ${item.precio.toFixed(2)}</small>
                </div>
                <div class="d-flex align-items-center">
                    <span class="me-3">S/. ${(item.precio * item.cantidad).toFixed(2)}</span>
                    <button class="btn btn-sm btn-outline-danger" onclick="cart.removeItem('${id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
            cartItemsDiv.appendChild(itemDiv);
        }

        cartTotalSpan.textContent = `S/. ${this.total.toFixed(2)}`;
        cartCountSpan.textContent = totalItems;
    }

    removeItem(id) {
        delete this.cartItems[id];
        this.updateCart();
    }

    showNotification(cantidad, nombre) {
        const toast = new bootstrap.Toast(document.createElement('div'));
        toast._element.className = 'toast position-fixed top-0 end-0 m-3';
        toast._element.innerHTML = `
            <div class="toast-header bg-success text-white">
                <strong class="me-auto">Producto Agregado</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                Se agregó ${cantidad} ${cantidad > 1 ? 'unidades' : 'unidad'} de ${nombre} al carrito
            </div>
        `;
        document.body.appendChild(toast._element);
        toast.show();
        setTimeout(() => toast._element.remove(), 3000);
    }
}

// Inicializar el carrito
const cart = new ShoppingCart();