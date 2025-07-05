from fastapi import APIRouter, HTTPException
from typing import List
from app.models import (
    CommandRequest, AgentResponse, ExtractRequest, 
    SummarizeRequest, ActionRequest, ActionType
)
from app.services import CommandParser, Navigator, ActionHandler

router = APIRouter()
parser = CommandParser()
navigator = Navigator()
action_handler = ActionHandler()

@router.post("/command", response_model=AgentResponse)
async def process_command(request: CommandRequest):
    """Process natural language commands from the user"""
    
    try:
        # Parse the command
        action_type, data = parser.parse_command(request.command)
        
        # Handle unknown commands
        if action_type == ActionType.UNKNOWN:
            return AgentResponse(
                action=action_type,
                message="I didn't understand that command. Try saying things like 'Show me iPhone 13' or 'What do reviews say?'",
                status="error",
                suggestions=[
                    "Show me iPhone 13",
                    "Add it to my cart",
                    "Summarize the reviews",
                    "Show my recent orders"
                ]
            )
        
        # Get navigation target if needed
        navigation = navigator.get_navigation_target(action_type, data)
        
        # Process based on action type
        if action_type == ActionType.SEARCH:
            products = action_handler.search_products(data.get("query", ""))
            return AgentResponse(
                action=action_type,
                message=f"Found {len(products)} products for '{data.get('query', '')}'",
                navigation=navigation,
                data={"products": products},
                status="success"
            )
        
        elif action_type == ActionType.ADD_TO_CART:
            # Get product ID from context if available
            product_id = request.context.get("current_product_id", "unknown")
            result = action_handler.add_to_cart(product_id)
            
            return AgentResponse(
                action=action_type,
                message=result["message"],
                data=result,
                status="success" if result["success"] else "error"
            )
        
        elif action_type == ActionType.SUMMARIZE:
            # Get product ID from context
            product_id = request.context.get("current_product_id", "unknown")
            review_summary = action_handler.get_review_summary(product_id)
            
            return AgentResponse(
                action=action_type,
                message="Here's what customers are saying:",
                summary=review_summary["summary"],
                data=review_summary,
                status="success"
            )
        
        elif action_type == ActionType.SHOW_ORDERS:
            orders = action_handler.get_recent_orders(data.get("count", 10))
            
            return AgentResponse(
                action=action_type,
                message=f"Here are your last {len(orders)} orders",
                navigation=navigation,
                data={"orders": orders},
                status="success"
            )
        
        elif action_type == ActionType.NAVIGATE:
            return AgentResponse(
                action=action_type,
                message=f"Navigating to {data.get('target', 'requested page')}",
                navigation=navigation,
                status="success"
            )
        
        else:
            return AgentResponse(
                action=action_type,
                message="Processing your request...",
                navigation=navigation,
                data=data,
                status="success"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/navigate")
async def navigate(target: str):
    """Navigate to a specific page"""
    
    navigation = navigator.get_navigation_target(
        ActionType.NAVIGATE, 
        {"target": target}
    )
    
    return {
        "navigation": navigation,
        "breadcrumb": navigator.get_breadcrumb(navigation.page if navigation else "")
    }

@router.post("/extract")
async def extract_content(request: ExtractRequest):
    """Extract specific content from page"""
    
    # Mock extraction based on type
    if request.extract_type == "products":
        return {
            "extracted": {
                "product_count": 24,
                "categories": ["Electronics", "Home", "Grocery"],
                "price_range": {"min": 9.99, "max": 999.99}
            }
        }
    elif request.extract_type == "reviews":
        return {
            "extracted": {
                "review_count": 156,
                "average_rating": 4.3,
                "verified_purchases": 142
            }
        }
    else:
        return {"extracted": {"type": request.extract_type, "content": "General content"}}

@router.post("/summarize")
async def summarize_content(request: SummarizeRequest):
    """Summarize content using AI"""
    
    # Mock summarization
    if len(request.content) > request.max_length:
        summary = request.content[:request.max_length] + "..."
    else:
        summary = request.content
    
    return {
        "summary": summary,
        "original_length": len(request.content),
        "summary_length": len(summary)
    }

@router.post("/action")
async def perform_action(request: ActionRequest):
    """Perform specific actions like add to cart"""
    
    if request.action_type == "add_to_cart":
        result = action_handler.add_to_cart(
            request.product_id or "unknown",
            request.quantity
        )
        return result
    
    elif request.action_type == "remove_from_cart":
        return {
            "success": True,
            "message": "Item removed from cart",
            "cart_total_items": 2
        }
    
    else:
        return {
            "success": False,
            "message": f"Unknown action: {request.action_type}"
        }

@router.get("/suggestions")
async def get_suggestions():
    """Get command suggestions for users"""
    
    return {
        "suggestions": [
            "Show me iPhone 13",
            "Get me laptops under $500",
            "What do the reviews say?",
            "Add this to my cart",
            "Show my last 5 orders",
            "Take me to my cart",
            "Find Samsung TVs",
            "Summarize this product"
        ]
    }