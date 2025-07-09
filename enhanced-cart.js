// Enhanced cart management with product tracking
class CartManager {
    constructor() {
        this.cart = this.loadCart();
    }
    
    loadCart() {
        const cartData = localStorage.getItem('cartData');
        return cartData ? JSON.parse(cartData) : { items: [], count: 0 };
    }
    
    saveCart() {
        localStorage.setItem('cartData', JSON.stringify(this.cart));
        localStorage.setItem('cartCount', this.cart.count.toString());
    }
    
    addItem(productId, productName, price) {
        const existingItem = this.cart.items.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity++;
        } else {
            this.cart.items.push({
                id: productId,
                name: productName,
                price: price,
                quantity: 1
            });
        }
        
        this.cart.count = this.cart.items.reduce((sum, item) => sum + item.quantity, 0);
        this.saveCart();
        
        // Update AI agent context if available
        if (window.aiAgent) {
            window.aiAgent.updateContext('cart_items', this.cart.items.map(item => item.id.toString()));
        }
        
        return this.cart;
    }
    
    getItems() {
        return this.cart.items;
    }
    
    getItemIds() {
        return this.cart.items.map(item => item.id.toString());
    }
    
    getCount() {
        return this.cart.count;
    }
    
    clear() {
        this.cart = { items: [], count: 0 };
        this.saveCart();
    }
}

// Initialize global cart manager
window.cartManager = new CartManager();

// Enhanced addToCart function
function enhancedAddToCart(productId, productName, price) {
    const cart = window.cartManager.addItem(productId, productName, price);
    
    // Update display
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(el => el.textContent = cart.count);
    
    // Show notification
    showNotification(`${productName} added to cart!`);
    
    // AI suggestions for comparison
    if (cart.items.length >= 2 && window.aiAgent) {
        showNotification('💡 You have multiple items in cart. Try: "Compare phones in my cart"');
    }
    
    return cart;
}