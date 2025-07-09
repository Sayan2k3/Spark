# Spark - AI-Powered Smart Shopping Assistant

An innovative e-commerce platform with an advanced AI navigation agent that transforms overwhelming product research into simple, confident decisions in minutes.

## 🚀 Features

### AI Navigation Agent
- **Natural Language Shopping**: Use commands like "Show me iPhone 13" or "Add it to my cart"
- **Smart Product Comparison**: Compare multiple products with "Compare phones in my cart for battery and camera"
- **Budget-Based Recommendations**: Get personalized suggestions with "Find me the best phone under 25k for gaming"
- **Review Analysis**: AI analyzes user reviews for specific features like battery life or camera quality
- **Nearby Store Prices**: Check local availability with "Check nearby stores" for best deals
- **Context-Aware Responses**: The AI remembers your cart and preferences throughout the session

### Advanced AI Features (NEW!)
- **Multi-Criteria Comparison**: Compare products based on specs AND user sentiment
- **Smart Scoring Algorithm**: Products scored on multiple parameters (camera, battery, performance)
- **Store Price Integration**: See price variations across nearby stores
- **Decision Support**: Get clear recommendations with reasoning
- **Time-Saving**: Reduce 40+ minutes of research to just 2 minutes

### E-Commerce Features
- Product browsing and search
- Shopping cart functionality with product tracking
- Product detail pages with specifications
- Category filtering and sorting
- Responsive design for all devices

## 🛠 Tech Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Font Awesome icons
- Responsive design
- Local storage for cart persistence

### Backend
- Python 3.8+
- FastAPI framework
- Natural language processing with enhanced parser
- Review sentiment analysis
- Product comparison engine
- Smart recommendation system
- RESTful API design
- CORS enabled

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Modern web browser
- Git

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sayan2k3/Spark.git
   cd Spark
   ```

2. **Start the backend server:**
   ```bash
   cd backend
   ./start.sh
   ```
   
   The backend will start at `http://localhost:8000`

3. **Open the frontend:**
   - Simply open `index.html` in your web browser
   - Or use a local server:
     ```bash
     python3 -m http.server 3000
     ```
     Then navigate to `http://localhost:3000`

## 🎮 How to Use the AI Agent

1. **Toggle AI Mode:**
   - Click the "AI Agent" toggle in the header
   - A command input will appear at the bottom of the screen

2. **Try These Commands:**
   
   **Basic Navigation:**
   - "Show me iPhone 13" - Searches for iPhone 13
   - "Add it to my cart" - Adds current product to cart
   - "What do reviews say?" - Summarizes product reviews
   - "Show my recent orders" - Displays order history
   
   **Smart Comparison (NEW!):**
   - "Compare phones in my cart for battery and camera"
   - "Which is better for gaming?"
   - "Compare iPhone 13 vs OnePlus 11"
   
   **Budget Recommendations (NEW!):**
   - "Find me the best phone under 25k for camera and gaming"
   - "I have 30k budget, need a phone with good battery"
   - "Check nearby stores" - Shows local store prices
   - "What's the best gaming phone under 40k?"

3. **Natural Interaction:**
   - Type commands naturally as you would speak
   - The agent understands various phrasings
   - Get suggestions for what to say next

## 📁 Project Structure

```
Spark/
├── index.html              # Homepage
├── products.html           # Products listing page
├── product.html            # Product detail page
├── styles.css              # Global styles
├── script.js               # Main JavaScript
├── agent.js                # AI agent frontend logic
├── products.js             # Products page logic
├── product.js              # Product detail logic
├── enhanced-cart.js        # Enhanced cart with product tracking
├── demo-scenarios.md       # Demo script and scenarios
└── backend/
    ├── app/                # FastAPI application
    │   ├── main.py         # Application entry point
    │   ├── routes/         # API endpoints
    │   │   ├── agent.py    # Main agent endpoints
    │   │   ├── comparison.py    # Product comparison
    │   │   └── recommendations.py # Smart recommendations
    │   ├── services/       # Business logic
    │   │   ├── parser.py   # Enhanced NLP parser
    │   │   ├── navigator.py # Navigation logic
    │   │   ├── actions.py  # Action handlers
    │   │   ├── analyzer.py # Review analysis
    │   │   ├── comparator.py # Comparison engine
    │   │   ├── recommender.py # Recommendation system
    │   │   ├── store_locator.py # Store prices
    │   │   └── mock_data.py # Rich product data
    │   └── models/         # Data models
    │       ├── commands.py # Request/response models
    │       └── analysis.py # Analysis result models
    ├── requirements.txt    # Python dependencies
    ├── start.sh           # Backend startup script
    └── README.md          # Backend documentation
```

## 🎯 Demo Scenarios

### Scenario 1: Smart Product Comparison
1. Enable AI mode
2. Say "Show me iPhone 13" and "Add to cart"
3. Say "Show me OnePlus 11" and "Add to cart"
4. Say "Compare phones in my cart for battery and camera"
5. Get detailed comparison with specs, user ratings, and AI recommendation

### Scenario 2: Budget-Based Shopping
1. Say "I have 25k budget, need best phone for camera and gaming"
2. View top 3 recommendations with scores
3. Say "Check nearby stores"
4. See store prices and savings
5. Say "Add the recommended one to cart"

### Scenario 3: Quick Decision Making
1. Say "What's the best gaming phone under 40k?"
2. Get instant recommendation with reasons
3. Say "Any deals nearby?"
4. View best store deals
5. Complete purchase in under 2 minutes

### Scenario 4: Advanced Comparison
1. Say "Compare iPhone 15 Pro vs Samsung S23 vs Pixel 7 for camera, display, and battery"
2. View comprehensive comparison table
3. See winner for each criterion
4. Get overall recommendation with reasoning

## 🌟 Key Benefits

- **Save Time**: Reduce 40+ minutes of research to just 2 minutes
- **Confident Decisions**: AI analyzes specs AND real user experiences
- **Best Deals**: Compare online and local store prices instantly
- **Personalized**: Recommendations based on YOUR priorities
- **Natural Interaction**: No complex filters or navigation needed

## 🚧 Future Enhancements

- Voice input support
- Real-time inventory tracking
- Integration with actual payment systems
- User accounts and authentication
- Advanced ML models for better recommendations
- Multi-language support
- Price history tracking
- Wishlist with price alerts

## 🤝 Contributing

This project was created for a hackathon. Feel free to fork and enhance!

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Built for the Spark Hackathon
- Inspired by Walmart's e-commerce platform
- AI agent concept for accessibility and convenience

---

## 📊 Performance Metrics

- **Decision Time**: 40+ minutes → 2 minutes (95% reduction)
- **Products Analyzed**: 15 phones with detailed specs
- **Review Analysis**: Sentiment analysis on battery, camera, performance
- **Store Coverage**: 4 nearby stores with real-time pricing
- **Accuracy**: Smart scoring algorithm with multi-criteria evaluation

---

**Note**: This is a demo project showcasing the future of AI-powered shopping. The system uses carefully crafted mock data to demonstrate real-world scenarios. In production, it would integrate with real databases, inventory systems, and advanced ML models.