
// Global variables
let isAgentMode = false;
let cartCount = 0;

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    initializeAgentToggle();
    initializeSearch();
    loadCartCount();
});

// AI Agent Toggle Functionality
function initializeAgentToggle() {
    const agentToggle = document.getElementById('agentToggle');
    const aiBanner = document.getElementById('aiBanner');
    
    if (agentToggle) {
        // Check for saved AI mode state from localStorage
        // Support both keys for compatibility
        const savedAIModeEnabled = localStorage.getItem('aiModeEnabled') === 'true';
        const savedAgentMode = localStorage.getItem('agentMode') === 'true';
        
        if (savedAIModeEnabled || savedAgentMode) {
            isAgentMode = true;
            agentToggle.classList.add('active');
            if (aiBanner) {
                aiBanner.style.display = 'block';
            }
        }
        
        agentToggle.addEventListener('click', function() {
            isAgentMode = !isAgentMode;
            agentToggle.classList.toggle('active', isAgentMode);
            
            if (aiBanner) {
                aiBanner.style.display = isAgentMode ? 'block' : 'none';
            }
            
            // Store agent mode state with both keys for compatibility
            localStorage.setItem('agentMode', isAgentMode);
            localStorage.setItem('aiModeEnabled', isAgentMode);
            
            // Log agent mode change
            console.log('AI Agent Mode:', isAgentMode ? 'Activated' : 'Deactivated');
            
            // Show notification
            if (isAgentMode) {
                showNotification('AI Agent Mode Activated! Getting smart recommendations...');
            } else {
                showNotification('AI Agent Mode Deactivated');
            }
        });
    }
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.querySelector('.search-btn');
    
    if (searchInput && searchBtn) {
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
}

function performSearch() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();
    
    if (query) {
        console.log('Searching for:', query);
        showNotification(`Searching for "${query}"...`);
        
        // In a real app, this would redirect to search results
        // For demo purposes, we'll just log it
        if (isAgentMode) {
            showNotification('AI Agent is finding personalized results for you!');
        }
    }
}

// Cart functionality
function loadCartCount() {
    const savedCount = localStorage.getItem('cartCount') || '0';
    cartCount = parseInt(savedCount);
    updateCartDisplay();
}

function updateCartDisplay() {
    const cartCountElement = document.querySelector('.cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = cartCount;
    }
}

function addToCart() {
    cartCount++;
    localStorage.setItem('cartCount', cartCount.toString());
    updateCartDisplay();
    showNotification('Item added to cart!');
    
    if (isAgentMode) {
        showNotification('AI Agent suggests: "You might also like similar products!"');
    }
}

// Navigation functions
function goToProduct(productId) {
    window.location.href = `product.html?id=${productId}`;
}

// Notification system
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #0071ce;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        z-index: 10000;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        animation: slideIn 0.3s ease-out;
    `;
    
    // Add animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Utility functions
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

// Department menu toggle (for mobile)
document.addEventListener('click', function(e) {
    if (e.target.closest('.departments-btn')) {
        showNotification('Departments menu coming soon!');
    }
});
