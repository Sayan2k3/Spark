
// Product detail page specific functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeProductPage();
    initializeQuantityControls();
    initializeTabs();
});

function initializeProductPage() {
    // Get product ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    // In a real app, you would fetch product data based on ID
    // For now, we'll use static data
    console.log('Loading product:', productId);
}

function changeMainImage(thumbnail) {
    const mainImage = document.getElementById('mainProductImage');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    if (mainImage && thumbnail) {
        // Update main image
        mainImage.src = thumbnail.src.replace('w=100&h=100', 'w=600&h=600');
        
        // Update active thumbnail
        thumbnails.forEach(thumb => thumb.classList.remove('active'));
        thumbnail.classList.add('active');
    }
}

function initializeQuantityControls() {
    const quantityInput = document.getElementById('quantity');
    
    if (quantityInput) {
        quantityInput.addEventListener('change', function() {
            const value = parseInt(this.value);
            if (value < 1) {
                this.value = 1;
            }
        });
    }
}

function increaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    if (quantityInput) {
        const currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    }
}

function decreaseQuantity() {
    const quantityInput = document.getElementById('quantity');
    if (quantityInput) {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    }
}

function addToCart() {
    const quantity = parseInt(document.getElementById('quantity').value);
    
    // Update global cart count
    cartCount += quantity;
    localStorage.setItem('cartCount', cartCount.toString());
    updateCartDisplay();
    
    showNotification(`Added ${quantity} item(s) to cart!`);
    
    if (isAgentMode) {
        setTimeout(() => {
            showNotification('AI Agent suggests: "Customers who bought this also liked iPhone cases and screen protectors!"');
        }, 1500);
    }
}

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanels = document.querySelectorAll('.tab-panel');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.textContent.toLowerCase();
            showTab(tabName);
        });
    });
}

function showTab(tabName) {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanels = document.querySelectorAll('.tab-panel');
    
    // Remove active class from all buttons and panels
    tabButtons.forEach(button => button.classList.remove('active'));
    tabPanels.forEach(panel => panel.classList.remove('active'));
    
    // Add active class to selected button and panel
    const activeButton = Array.from(tabButtons).find(button => 
        button.textContent.toLowerCase() === tabName
    );
    const activePanel = document.getElementById(tabName);
    
    if (activeButton) activeButton.classList.add('active');
    if (activePanel) activePanel.classList.add('active');
}

// Wishlist functionality
function toggleWishlist() {
    const wishlistBtn = document.querySelector('.wishlist-btn');
    const isWishlisted = wishlistBtn.classList.contains('wishlisted');
    
    if (isWishlisted) {
        wishlistBtn.classList.remove('wishlisted');
        wishlistBtn.innerHTML = '<i class="fas fa-heart"></i>';
        showNotification('Removed from wishlist');
    } else {
        wishlistBtn.classList.add('wishlisted');
        wishlistBtn.innerHTML = '<i class="fas fa-heart" style="color: red;"></i>';
        showNotification('Added to wishlist!');
    }
}

// Share functionality
function shareProduct() {
    if (navigator.share) {
        navigator.share({
            title: 'iPhone 15 Pro - Walmart',
            text: 'Check out this amazing product!',
            url: window.location.href
        });
    } else {
        // Fallback - copy to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
            showNotification('Product link copied to clipboard!');
        });
    }
}

// Add click event listeners when page loads
document.addEventListener('DOMContentLoaded', function() {
    const wishlistBtn = document.querySelector('.wishlist-btn');
    const shareBtn = document.querySelector('.share-btn');
    
    if (wishlistBtn) {
        wishlistBtn.addEventListener('click', toggleWishlist);
    }
    
    if (shareBtn) {
        shareBtn.addEventListener('click', shareProduct);
    }
});
