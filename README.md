# Spark - AI-Powered Walmart Clone

An innovative e-commerce platform with an AI navigation agent that allows users to shop using natural language commands.

## 🚀 Features

### AI Navigation Agent
- **Natural Language Shopping**: Use commands like "Show me iPhone 13" or "Add it to my cart"
- **Smart Navigation**: The AI agent navigates the website for you based on your commands
- **Review Summarization**: Get AI-powered summaries of product reviews
- **Hands-Free Shopping**: Complete shopping experience through conversational interface

### E-Commerce Features
- Product browsing and search
- Shopping cart functionality
- Product detail pages with image galleries
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
- Natural language processing
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
   - "Show me iPhone 13" - Searches for iPhone 13
   - "Add it to my cart" - Adds current product to cart
   - "What do reviews say?" - Summarizes product reviews
   - "Show my recent orders" - Displays order history
   - "Take me to my cart" - Navigates to cart page

3. **Natural Interaction:**
   - Type commands naturally as you would speak
   - The agent understands various phrasings
   - Get suggestions for what to say next

## 📁 Project Structure

```
Spark/
├── index.html           # Homepage
├── products.html        # Products listing page
├── product.html         # Product detail page
├── styles.css          # Global styles
├── script.js           # Main JavaScript
├── agent.js            # AI agent frontend logic
├── products.js         # Products page logic
├── product.js          # Product detail logic
└── backend/
    ├── app/            # FastAPI application
    ├── requirements.txt # Python dependencies
    ├── start.sh        # Backend startup script
    └── README.md       # Backend documentation
```

## 🎯 Demo Scenarios

### Scenario 1: Product Search
1. Enable AI mode
2. Say "Get me iPhone 13"
3. Agent navigates to products and shows results

### Scenario 2: Smart Shopping
1. On a product page
2. Say "Summarize the reviews"
3. Agent provides review summary
4. Say "Add to cart"
5. Product added automatically

### Scenario 3: Order Management
1. Say "Show my last 5 orders"
2. Agent navigates to order history
3. View your recent purchases

## 🚧 Future Enhancements

- Voice input support
- Real-time product recommendations
- Multi-language support
- Integration with actual payment systems
- User accounts and authentication
- Advanced NLP with machine learning

## 🤝 Contributing

This project was created for a hackathon. Feel free to fork and enhance!

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- Built for the Spark Hackathon
- Inspired by Walmart's e-commerce platform
- AI agent concept for accessibility and convenience

---

**Note**: This is a demo project. The AI agent uses mock data and simulated responses. In a production environment, it would integrate with real databases and advanced NLP models.