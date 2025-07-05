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