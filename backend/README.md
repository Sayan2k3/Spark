# Spark AI Navigation Agent Backend

This is the backend API for the Spark AI Navigation Agent - a natural language interface for navigating and interacting with the Walmart clone website.

## Features

- **Natural Language Processing**: Understands user commands in plain English
- **Smart Navigation**: Automatically navigates to relevant pages based on commands
- **Product Search**: Find products using natural language queries
- **Cart Management**: Add items to cart with simple commands
- **Review Summarization**: Get AI-powered summaries of product reviews
- **Order History**: View recent orders with voice commands

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.8+**: Core programming language
- **Pydantic**: Data validation using Python type annotations
- **CORS**: Enabled for frontend integration

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Run the start script:**
   ```bash
   ./start.sh
   ```

   This script will:
   - Create a virtual environment
   - Install all dependencies
   - Start the FastAPI server

   **OR** manually set up:

   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start the server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Verify the API is running:**
   - Open http://localhost:8000 in your browser
   - You should see the API welcome message
   - API documentation available at http://localhost:8000/docs

## API Endpoints

### Main Endpoints

- `POST /api/agent/command` - Process natural language commands
- `POST /api/agent/navigate` - Handle navigation requests
- `POST /api/agent/extract` - Extract content from pages
- `POST /api/agent/summarize` - Summarize content
- `POST /api/agent/action` - Perform actions (add to cart, etc.)
- `GET /api/agent/suggestions` - Get command suggestions

### Health Check

- `GET /health` - Check if the API is running

## Usage Examples

### Send a Command

```bash
curl -X POST "http://localhost:8000/api/agent/command" \
     -H "Content-Type: application/json" \
     -d '{
       "command": "Show me iPhone 13",
       "context": {},
       "session_id": "session_123"
     }'
```

### Response Format

```json
{
  "action": "search",
  "message": "Found 3 products for 'iPhone 13'",
  "navigation": {
    "page": "products.html",
    "params": {
      "search": "iPhone 13",
      "aiMode": true
    }
  },
  "data": {
    "products": [...]
  },
  "status": "success"
}
```

## Frontend Integration

The frontend automatically integrates with this backend when:
1. The backend is running on `http://localhost:8000`
2. AI mode is toggled on in the UI
3. User types commands in the AI input field

## Demo Commands

See [demo_commands.md](demo_commands.md) for a list of example commands to try.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── routes/
│   │   └── agent.py      # API endpoints
│   ├── services/
│   │   ├── parser.py     # Command parsing logic
│   │   ├── navigator.py  # Navigation handling
│   │   └── actions.py    # Action handlers
│   └── models/
│       └── commands.py   # Pydantic models
├── requirements.txt      # Python dependencies
├── start.sh             # Startup script
└── README.md            # This file
```

## Development

- The API runs with auto-reload enabled by default
- Make changes to the code and the server will restart automatically
- Check logs in the terminal for debugging

## Future Enhancements

- Integration with actual product database
- User authentication and personalization
- Machine learning for better command understanding
- Real shopping cart and order management
- Voice input support
- Multi-language support

## Troubleshooting

1. **Port already in use**: Change the port in start.sh or kill the process using port 8000
2. **Module not found**: Make sure virtual environment is activated
3. **CORS errors**: Backend must be running before accessing the frontend

## License

This project is part of the Spark hackathon project.