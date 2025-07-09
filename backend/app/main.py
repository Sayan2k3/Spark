from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import agent, comparison, recommendations

app = FastAPI(
    title="Spark AI Navigation Agent",
    description="AI-powered navigation agent for Walmart clone",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
app.include_router(comparison.router, prefix="/api/agent", tags=["comparison"])
app.include_router(recommendations.router, prefix="/api/agent", tags=["recommendations"])

@app.get("/")
async def root():
    return {
        "message": "Spark AI Navigation Agent API",
        "status": "active",
        "endpoints": {
            "command": "/api/agent/command",
            "navigate": "/api/agent/navigate",
            "extract": "/api/agent/extract",
            "summarize": "/api/agent/summarize",
            "action": "/api/agent/action",
            "compare": "/api/agent/compare",
            "recommend": "/api/agent/recommend"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}