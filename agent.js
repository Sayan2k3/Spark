// AI Agent functionality
class AIAgent {
    constructor() {
        this.apiUrl = 'http://localhost:8000/api/agent';
        this.isActive = false;
        this.sessionId = this.generateSessionId();
        this.currentContext = {};
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    async sendCommand(command) {
        try {
            const response = await fetch(`${this.apiUrl}/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    command: command,
                    context: this.currentContext,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Agent command error:', error);
            return {
                action: 'unknown',
                message: 'Sorry, I couldn\'t process that command. Please try again.',
                status: 'error'
            };
        }
    }

    processResponse(response) {
        // Handle navigation
        if (response.navigation) {
            this.navigateToPage(response.navigation);
        }

        // Show message
        if (response.message) {
            showNotification(response.message);
        }

        // Handle specific actions
        switch (response.action) {
            case 'search':
                if (response.data && response.data.products) {
                    this.displaySearchResults(response.data.products);
                }
                break;
            
            case 'add_to_cart':
                if (response.data && response.data.success) {
                    // Update cart count
                    if (typeof addToCart === 'function') {
                        addToCart();
                    }
                }
                break;
            
            case 'summarize':
                if (response.summary) {
                    this.displaySummary(response.summary, response.data);
                }
                break;
            
            case 'show_orders':
                if (response.data && response.data.orders) {
                    this.displayOrders(response.data.orders);
                }
                break;
            
            case 'compare':
                if (response.data) {
                    this.displayComparison(response.data);
                }
                break;
            
            case 'recommend':
                if (response.data) {
                    this.displayRecommendations(response.data);
                }
                break;
        }

        // Show suggestions if available
        if (response.suggestions && response.suggestions.length > 0) {
            this.showSuggestions(response.suggestions);
        }
    }

    navigateToPage(navigation) {
        let url = navigation.page;
        
        // Add query parameters if any
        if (navigation.params && Object.keys(navigation.params).length > 0) {
            const params = new URLSearchParams(navigation.params);
            url += '?' + params.toString();
        }

        // Navigate to the page
        window.location.href = url;
    }

    displaySearchResults(products) {
        // If we're on the products page, update the display
        if (window.location.pathname.includes('products.html')) {
            // This would integrate with the existing products display logic
            console.log('Displaying search results:', products);
            
            // Store search results for products page to use
            sessionStorage.setItem('aiSearchResults', JSON.stringify(products));
            
            // Trigger a custom event that products.js can listen to
            window.dispatchEvent(new CustomEvent('aiSearchResults', { detail: products }));
        }
    }

    displaySummary(summary, data) {
        // Create a modal or notification to show the summary
        const summaryModal = document.createElement('div');
        summaryModal.className = 'ai-summary-modal';
        summaryModal.innerHTML = `
            <div class="ai-summary-content">
                <h3>Review Summary</h3>
                <p>${summary}</p>
                ${data && data.overall_rating ? `
                    <div class="summary-stats">
                        <span>Overall Rating: ${data.overall_rating.toFixed(1)}/5</span>
                        <span>${data.total_reviews} reviews</span>
                    </div>
                ` : ''}
                ${data && data.recommendation ? `<p class="recommendation">${data.recommendation}</p>` : ''}
                <button onclick="this.parentElement.parentElement.remove()">Close</button>
            </div>
        `;
        
        // Add styles
        summaryModal.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            z-index: 10001;
            max-width: 500px;
            width: 90%;
        `;
        
        document.body.appendChild(summaryModal);
    }

    displayOrders(orders) {
        // Store orders for the orders page
        sessionStorage.setItem('aiOrderResults', JSON.stringify(orders));
        
        // If we're already on the orders page, update display
        if (window.location.pathname.includes('orders.html')) {
            window.dispatchEvent(new CustomEvent('aiOrderResults', { detail: orders }));
        }
    }

    showSuggestions(suggestions) {
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'ai-suggestions';
        suggestionsDiv.innerHTML = `
            <p>Try saying:</p>
            <ul>
                ${suggestions.map(s => `<li>${s}</li>`).join('')}
            </ul>
        `;
        
        // Style the suggestions
        suggestionsDiv.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #f0f2f5;
            padding: 15px;
            border-radius: 8px;
            max-width: 250px;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
        `;
        
        document.body.appendChild(suggestionsDiv);
        
        // Remove after 10 seconds
        setTimeout(() => {
            if (suggestionsDiv.parentNode) {
                suggestionsDiv.remove();
            }
        }, 10000);
    }

    displayComparison(comparisonData) {
        // Create a comprehensive comparison modal
        const modal = document.createElement('div');
        modal.className = 'ai-comparison-modal';
        
        let comparisonHTML = '<div class="comparison-content"><h2>Product Comparison</h2>';
        
        // Add summary
        if (comparisonData.summary) {
            comparisonHTML += `<div class="comparison-summary">${comparisonData.summary.replace(/\n/g, '<br>')}</div>`;
        }
        
        // Create comparison table
        if (comparisonData.comparison) {
            comparisonHTML += '<table class="comparison-table"><thead><tr><th>Feature</th>';
            
            // Add product names as headers
            const products = Object.values(comparisonData.comparison);
            products.forEach(product => {
                comparisonHTML += `<th>${product.name}<br><span class="price">₹${product.price}</span></th>`;
            });
            comparisonHTML += '</tr></thead><tbody>';
            
            // Add comparison rows
            const criteria = Object.keys(products[0].specs || {});
            criteria.forEach(criterion => {
                comparisonHTML += `<tr><td><strong>${criterion}</strong></td>`;
                products.forEach(product => {
                    const spec = product.specs[criterion] || 'N/A';
                    const reviewData = product.review_analysis[criterion];
                    comparisonHTML += '<td>';
                    comparisonHTML += `<div>${spec}</div>`;
                    if (reviewData && reviewData.average_rating) {
                        comparisonHTML += `<div class="rating">⭐ ${reviewData.average_rating.toFixed(1)}/5</div>`;
                    }
                    comparisonHTML += '</td>';
                });
                comparisonHTML += '</tr>';
            });
            
            comparisonHTML += '</tbody></table>';
        }
        
        // Add recommendation
        if (comparisonData.recommendation) {
            const rec = comparisonData.recommendation;
            comparisonHTML += `
                <div class="ai-recommendation">
                    <h3>AI Recommendation</h3>
                    <p><strong>${rec.recommended_product}</strong></p>
                    <p>${rec.reason}</p>
                </div>
            `;
        }
        
        comparisonHTML += '<button class="close-btn" onclick="this.parentElement.parentElement.remove()">Close</button></div>';
        
        modal.innerHTML = comparisonHTML;
        
        // Style the modal
        modal.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            z-index: 10001;
            max-width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            width: 800px;
        `;
        
        // Add CSS for the table
        const style = document.createElement('style');
        style.textContent = `
            .comparison-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            .comparison-table th, .comparison-table td {
                padding: 12px;
                text-align: left;
                border: 1px solid #ddd;
            }
            .comparison-table th {
                background-color: #f8f9fa;
                font-weight: 600;
            }
            .comparison-table .price {
                color: #0071dc;
                font-size: 14px;
            }
            .comparison-table .rating {
                color: #f57c00;
                font-size: 12px;
                margin-top: 4px;
            }
            .comparison-summary {
                margin: 20px 0;
                padding: 15px;
                background: #f0f2f5;
                border-radius: 8px;
                white-space: pre-line;
            }
            .ai-recommendation {
                margin: 20px 0;
                padding: 20px;
                background: #e3f2fd;
                border-radius: 8px;
                border-left: 4px solid #0071dc;
            }
            .close-btn {
                margin-top: 20px;
                padding: 10px 20px;
                background: #0071dc;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(modal);
    }
    
    displayRecommendations(recommendationData) {
        // Create recommendations modal
        const modal = document.createElement('div');
        modal.className = 'ai-recommendations-modal';
        
        let html = '<div class="recommendations-content"><h2>AI Recommendations</h2>';
        
        // Budget info
        html += `<p class="budget-info">Based on your budget of ₹${recommendationData.budget} and priorities: ${recommendationData.priorities_analyzed.join(', ')}</p>`;
        
        // Display recommendations
        if (recommendationData.recommendations && recommendationData.recommendations.length > 0) {
            html += '<div class="recommendations-list">';
            
            recommendationData.recommendations.forEach((rec, index) => {
                html += `
                    <div class="recommendation-card">
                        <h3>${index + 1}. ${rec.product}</h3>
                        <div class="rec-price">₹${rec.online_price}</div>
                        <div class="scores">
                `;
                
                // Show scores for each priority
                Object.entries(rec.score).forEach(([feature, score]) => {
                    html += `<div class="score-item">${feature}: ${score.toFixed(1)}/100</div>`;
                });
                
                html += `
                        </div>
                        <div class="overall-score">Overall Score: ${rec.overall_score}/100</div>
                `;
                
                // Show store prices if available
                if (rec.store_prices && rec.store_prices.length > 0) {
                    html += '<div class="store-prices"><h4>Available at nearby stores:</h4>';
                    rec.store_prices.forEach(store => {
                        html += `
                            <div class="store-item">
                                <span>${store.store} (${store.distance})</span>
                                <span>₹${store.price}</span>
                                ${store.savings > 0 ? `<span class="savings">Save ₹${store.savings}</span>` : ''}
                            </div>
                        `;
                    });
                    html += '</div>';
                }
                
                html += '</div>';
            });
            
            html += '</div>';
        }
        
        // Best choice
        if (recommendationData.best_choice) {
            const best = recommendationData.best_choice;
            html += `
                <div class="best-choice">
                    <h3>🏆 Best Choice: ${best.product}</h3>
                    <p>Score: ${best.overall_score}/100</p>
                    <p>Why: ${best.reasons.join(', ')}</p>
                    ${best.best_store_deal ? `
                        <p class="best-deal">Best deal at ${best.best_store_deal.store} - Save ₹${best.savings}</p>
                    ` : ''}
                </div>
            `;
        }
        
        html += '<button class="close-btn" onclick="this.parentElement.parentElement.remove()">Close</button></div>';
        
        modal.innerHTML = html;
        
        // Style the modal
        modal.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            z-index: 10001;
            max-width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            width: 700px;
        `;
        
        // Add CSS
        const style = document.createElement('style');
        style.textContent = `
            .recommendations-content { font-family: Arial, sans-serif; }
            .budget-info { 
                margin: 20px 0; 
                padding: 15px; 
                background: #f8f9fa; 
                border-radius: 8px; 
            }
            .recommendation-card {
                margin: 20px 0;
                padding: 20px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background: #fafafa;
            }
            .rec-price {
                font-size: 24px;
                color: #0071dc;
                font-weight: bold;
                margin: 10px 0;
            }
            .scores {
                display: flex;
                gap: 15px;
                margin: 10px 0;
                flex-wrap: wrap;
            }
            .score-item {
                padding: 5px 10px;
                background: #e3f2fd;
                border-radius: 4px;
                font-size: 14px;
            }
            .overall-score {
                margin: 10px 0;
                font-weight: bold;
                color: #388e3c;
            }
            .store-prices {
                margin-top: 15px;
                padding: 15px;
                background: #f5f5f5;
                border-radius: 8px;
            }
            .store-item {
                display: flex;
                justify-content: space-between;
                margin: 8px 0;
                padding: 8px;
                background: white;
                border-radius: 4px;
            }
            .savings {
                color: #388e3c;
                font-weight: bold;
            }
            .best-choice {
                margin: 30px 0;
                padding: 20px;
                background: #e8f5e9;
                border-radius: 8px;
                border: 2px solid #4caf50;
            }
            .best-deal {
                color: #388e3c;
                font-weight: bold;
                margin-top: 10px;
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(modal);
    }

    updateContext(key, value) {
        this.currentContext[key] = value;
    }

    clearContext() {
        this.currentContext = {};
    }
}

// Initialize the AI agent
const aiAgent = new AIAgent();

// Add command input UI when AI mode is active
function initializeAICommandInput() {
    const existingInput = document.getElementById('aiCommandInput');
    if (existingInput) return;

    const commandInputDiv = document.createElement('div');
    commandInputDiv.id = 'aiCommandInput';
    commandInputDiv.className = 'ai-command-input';
    commandInputDiv.innerHTML = `
        <input type="text" placeholder="Tell me what you're looking for..." id="aiInput">
        <button onclick="handleAICommand()">
            <i class="fas fa-paper-plane"></i>
        </button>
    `;
    
    // Style the command input
    commandInputDiv.style.cssText = `
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        background: white;
        padding: 10px;
        border-radius: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 10px;
        z-index: 1000;
        width: 90%;
        max-width: 600px;
    `;
    
    const inputStyle = `
        flex: 1;
        border: none;
        outline: none;
        padding: 10px 15px;
        font-size: 16px;
        background: transparent;
    `;
    
    const buttonStyle = `
        background: #0071ce;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.3s;
    `;
    
    document.body.appendChild(commandInputDiv);
    
    // Apply styles after adding to DOM
    document.getElementById('aiInput').style.cssText = inputStyle;
    commandInputDiv.querySelector('button').style.cssText = buttonStyle;
    
    // Add enter key handler
    document.getElementById('aiInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleAICommand();
        }
    });
}

// Handle AI command submission
async function handleAICommand() {
    const input = document.getElementById('aiInput');
    const command = input.value.trim();
    
    if (!command) return;
    
    // Clear input
    input.value = '';
    
    // Show processing notification
    showNotification('Processing your request...');
    
    // Send command to AI agent
    const response = await aiAgent.sendCommand(command);
    
    // Process the response
    aiAgent.processResponse(response);
}

// Enhance the agent toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    // Wait for the original toggle to be initialized
    setTimeout(() => {
        const agentToggle = document.getElementById('agentToggle');
        if (agentToggle) {
            // Add our enhanced click handler
            agentToggle.addEventListener('click', function() {
                setTimeout(() => {
                    // Check the current agent mode state
                    const isActive = agentToggle.classList.contains('active');
                    
                    if (isActive) {
                        initializeAICommandInput();
                        
                        // Get suggestions on activation
                        fetch('http://localhost:8000/api/agent/suggestions')
                            .then(res => res.json())
                            .then(data => {
                                if (data.suggestions) {
                                    aiAgent.showSuggestions(data.suggestions.slice(0, 4));
                                }
                            })
                            .catch(console.error);
                    } else {
                        const commandInput = document.getElementById('aiCommandInput');
                        if (commandInput) {
                            commandInput.remove();
                        }
                    }
                }, 100);
            });
        }
    }, 500);
});

// Update context when on product page
if (window.location.pathname.includes('product.html')) {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    if (productId) {
        aiAgent.updateContext('current_product_id', productId);
        aiAgent.updateContext('current_page', 'product');
    }
}