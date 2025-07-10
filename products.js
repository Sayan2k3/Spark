// Products page specific functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check for search parameters from AI navigation
    const urlParams = new URLSearchParams(window.location.search);
    const searchQuery = urlParams.get('search');
    const aiMode = urlParams.get('aiMode');
    
    if (searchQuery) {
        // Special handling for "phone" search to show all phones
        if (searchQuery.toLowerCase() === 'phone' || searchQuery.toLowerCase() === 'phones') {
            // Show all phones for the demo
            loadPhones();
            if (aiMode === 'true') {
                showNotification('Showing phones under ₹50,000');
            }
        } else {
            // Normal search for specific products
            loadProducts(searchQuery);
            
            // Update search input if it exists
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.value = searchQuery;
            }
            
            // Show notification if from AI
            if (aiMode === 'true') {
                showNotification(`Showing results for "${searchQuery}"`);
            }
        }
    } else {
        loadProducts();
    }
    
    initializeFilters();
});

// Sample products data - DEMO PHONES FIRST
const productsData = [
    // DEMO PHONES - All under 50k
    {
        id: 13,
        name: "iPhone 13",
        price: 45999,
        originalPrice: 52999,
        image: "https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=300&h=300&fit=crop",
        rating: 4.7,
        reviews: 3521,
        category: "electronics"
    },
    {
        id: 14,
        name: "OnePlus 11",
        price: 38999,
        originalPrice: 42999,
        image: "https://images.unsplash.com/photo-1614796740292-50ae67262ff0?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8b25lcGx1c3xlbnwwfHwwfHx8MA%3D%3D",
        rating: 4.6,
        reviews: 1876,
        category: "electronics"
    },
    {
        id: 15,
        name: "Samsung Galaxy S23",
        price: 42999,
        originalPrice: 49999,
        image: "https://media.wired.com/photos/63ee8e4fcde6e0e4f71293ef/master/pass/Samsung-Galaxy-S23-SOURCE-Samsung.jpg",
        rating: 4.7,
        reviews: 2341,
        category: "electronics"
    },
    {
        id: 17,
        name: "Xiaomi 13 Pro",
        price: 35999,
        originalPrice: 39999,
        image: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=300&h=300&fit=crop",
        rating: 4.5,
        reviews: 2134,
        category: "electronics"
    },
    {
        id: 18,
        name: "Realme GT 3",
        price: 29999,
        originalPrice: 34999,
        image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop",
        rating: 4.4,
        reviews: 1876,
        category: "electronics"
    },
    // Premium phone (above 50k)
    {
        id: 1,
        name: "iPhone 15 Pro",
        price: 134999,
        originalPrice: 149999,
        image: "https://i0.wp.com/www.icenter-iraq.com/wp-content/uploads/2023/09/iPhone_15_Pink_PDP_Image_Position-1__en-ME-scaled.jpg?fit=2560%2C2560&ssl=1",
        rating: 4.8,
        reviews: 2847,
        category: "electronics"
    },
    {
        id: 2,
        name: "MacBook Air M2",
        price: 89999,
        originalPrice: 99999,
        image: "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=300&h=300&fit=crop",
        rating: 4.6,
        reviews: 1523,
        category: "electronics"
    },
    {
        id: 3,
        name: "Sony WH-1000XM4",
        price: 19999,
        originalPrice: 24999,
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop",
        rating: 4.9,
        reviews: 3241,
        category: "electronics"
    },
    {
        id: 4,
        name: "Apple Watch Series 9",
        price: 35999,
        originalPrice: 41999,
        image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop",
        rating: 4.7,
        reviews: 1876,
        category: "electronics"
    },
    {
        id: 15,
        name: "Samsung Galaxy S23",
        price: 42999.00,
        originalPrice: 49999.00,
        image: "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=300&h=300&fit=crop",
        rating: 4.7,
        reviews: 2341,
        category: "electronics"
    },
    {
        id: 16,
        name: "Samsung TV 55\" 4K",
        price: 69999,
        originalPrice: 89999,
        image: "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=300&h=300&fit=crop",
        rating: 4.6,
        reviews: 1523,
        category: "electronics"
    },
    {
        id: 17,
        name: "Xiaomi 13 Pro",
        price: 35999.00,
        originalPrice: 39999.00,
        image: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=300&h=300&fit=crop",
        rating: 4.5,
        reviews: 2134,
        category: "electronics"
    },
    {
        id: 18,
        name: "Realme GT 3",
        price: 29999.00,
        originalPrice: 34999.00,
        image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop",
        rating: 4.4,
        reviews: 1876,
        category: "electronics"
    },
    {
        id: 5,
        name: "Nike Air Max 270",
        price: 129.99,
        originalPrice: 150.00,
        image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop",
        rating: 4.4,
        reviews: 892,
        category: "fashion"
    },
    {
        id: 6,
        name: "Levi's 501 Jeans",
        price: 79.99,
        originalPrice: null,
        image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=300&h=300&fit=crop",
        rating: 4.3,
        reviews: 654,
        category: "fashion"
    },
    {
        id: 7,
        name: "KitchenAid Stand Mixer",
        price: 299.99,
        originalPrice: 379.99,
        image: "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=300&h=300&fit=crop",
        rating: 4.8,
        reviews: 2156,
        category: "home"
    },
    {
        id: 8,
        name: "Dyson V15 Vacuum",
        price: 449.99,
        originalPrice: 549.99,
        image: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop",
        rating: 4.6,
        reviews: 1432,
        category: "home"
    }
];

let filteredProducts = [...productsData];

function loadProducts(searchQuery = '') {
    let productsToShow = filteredProducts;
    
    // If there's a search query, filter products
    if (searchQuery) {
        productsToShow = productsData.filter(product => 
            product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            product.category.toLowerCase().includes(searchQuery.toLowerCase())
        );
        
        // Update the global filtered products
        filteredProducts = productsToShow;
    }
    
    displayProducts(productsToShow);
}

function loadPhones() {
    // Show only phones under 50k for the demo
    const phones = productsData.filter(product => 
        product.price <= 50000 && 
        product.category === 'electronics' &&
        (product.name.toLowerCase().includes('phone') || 
         product.name.toLowerCase().includes('iphone') ||
         product.name.toLowerCase().includes('galaxy') ||
         product.name.toLowerCase().includes('oneplus') ||
         product.name.toLowerCase().includes('xiaomi') ||
         product.name.toLowerCase().includes('realme'))
    );
    
    // Sort by price to show affordable ones first
    phones.sort((a, b) => a.price - b.price);
    
    // Update the global filtered products
    filteredProducts = phones;
    
    displayProducts(phones);
}

function displayProducts(products) {
    const productsGrid = document.getElementById('productsGrid');
    
    if (!productsGrid) return;
    
    productsGrid.innerHTML = '';
    
    products.forEach(product => {
        const productCard = createProductCard(product);
        productsGrid.appendChild(productCard);
    });
    
    if (products.length === 0) {
        productsGrid.innerHTML = '<p style="text-align: center; grid-column: 1/-1; padding: 40px;">No products found matching your criteria.</p>';
    }
}

function createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.onclick = () => goToProductDetail(product.id);
    
    const stars = '★'.repeat(Math.floor(product.rating)) + '☆'.repeat(5 - Math.floor(product.rating));
    const originalPriceHTML = product.originalPrice ? 
        `<span class="original-price">$${product.originalPrice.toFixed(2)}</span>` : '';
    
    card.innerHTML = `
        <img src="${product.image}" alt="${product.name}">
        <div class="product-info">
            <h3>${product.name}</h3>
            <div class="price">
                <span class="current-price">$${product.price.toFixed(2)}</span>
                ${originalPriceHTML}
            </div>
            <div class="rating">
                <span class="stars">${stars}</span>
                <span>(${product.reviews})</span>
            </div>
        </div>
    `;
    
    return card;
}

function initializeFilters() {
    const categoryFilter = document.getElementById('category');
    const priceFilter = document.getElementById('priceRange');
    const sortFilter = document.getElementById('sortBy');
    
    if (categoryFilter) {
        categoryFilter.addEventListener('change', applyFilters);
    }
    
    if (priceFilter) {
        priceFilter.addEventListener('change', applyFilters);
    }
    
    if (sortFilter) {
        sortFilter.addEventListener('change', applyFilters);
    }
}

function applyFilters() {
    const categoryFilter = document.getElementById('category').value;
    const priceFilter = document.getElementById('priceRange').value;
    const sortFilter = document.getElementById('sortBy').value;
    
    // Start with all products
    filteredProducts = [...productsData];
    
    // Apply category filter
    if (categoryFilter) {
        filteredProducts = filteredProducts.filter(product => product.category === categoryFilter);
    }
    
    // Apply price filter
    if (priceFilter) {
        filteredProducts = filteredProducts.filter(product => {
            const price = product.price;
            switch (priceFilter) {
                case '0-50':
                    return price <= 50;
                case '50-200':
                    return price > 50 && price <= 200;
                case '200-500':
                    return price > 200 && price <= 500;
                case '500+':
                    return price > 500;
                default:
                    return true;
            }
        });
    }
    
    // Apply sorting
    switch (sortFilter) {
        case 'price-low':
            filteredProducts.sort((a, b) => a.price - b.price);
            break;
        case 'price-high':
            filteredProducts.sort((a, b) => b.price - a.price);
            break;
        case 'rating':
            filteredProducts.sort((a, b) => b.rating - a.rating);
            break;
        default:
            // Keep original order for relevance
            break;
    }
    
    displayProducts(filteredProducts);
    
    if (isAgentMode) {
        showNotification(`AI Agent filtered ${filteredProducts.length} products for you!`);
    }
}

function goToProductDetail(productId) {
    window.location.href = `product.html?id=${productId}`;
}
