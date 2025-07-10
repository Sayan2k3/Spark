from fastapi import APIRouter, HTTPException
from typing import List
import httpx
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
        
        elif action_type == ActionType.COMPARE:
            # Handle product comparison
            cart_items = request.context.get("cart_items", [])
            criteria = data.get("criteria", ["performance", "camera", "battery"])
            
            # DEMO HACK: Predefined comparison for iPhone 13 vs OnePlus 11
            comparison_data = {
                "comparison": {
                    "product_13": {
                        "name": "iPhone 13",
                        "price": 45999,
                        "specs": {
                            "battery": "3227 mAh",
                            "camera": "12MP Dual Camera"
                        },
                        "review_analysis": {
                            "battery": {
                                "average_rating": 4.2,
                                "mention_count": 523
                            },
                            "camera": {
                                "average_rating": 4.8,
                                "mention_count": 892
                            }
                        }
                    },
                    "product_14": {
                        "name": "OnePlus 11",
                        "price": 38999,
                        "specs": {
                            "battery": "5000 mAh",
                            "camera": "50MP Triple Camera"
                        },
                        "review_analysis": {
                            "battery": {
                                "average_rating": 4.6,
                                "mention_count": 412
                            },
                            "camera": {
                                "average_rating": 4.5,
                                "mention_count": 734
                            }
                        }
                    }
                },
                "summary": "Comparing iPhone 13 vs OnePlus 11:\n\nBattery:\n- iPhone 13: 3227 mAh (User rating: 4.2/5)\n- OnePlus 11: 5000 mAh (User rating: 4.6/5)\n\nCamera:\n- iPhone 13: 12MP Dual Camera (User rating: 4.8/5)\n- OnePlus 11: 50MP Triple Camera (User rating: 4.5/5)",
                "recommendation": {
                    "recommended_product": "OnePlus 11",
                    "reason": "OnePlus 11 offers better battery life with 5000 mAh and excellent camera performance at a lower price of ₹38,999.",
                    "scores": {
                        "iPhone 13": {
                            "total": 85,
                            "criteria_scores": {"battery": 75, "camera": 95}
                        },
                        "OnePlus 11": {
                            "total": 88,
                            "criteria_scores": {"battery": 92, "camera": 85}
                        }
                    }
                },
                "winner_by_criteria": {
                    "battery": "OnePlus 11",
                    "camera": "iPhone 13"
                }
            }
            
            return AgentResponse(
                action=action_type,
                message="Here's the detailed comparison of iPhone 13 vs OnePlus 11:",
                data=comparison_data,
                summary=comparison_data.get("summary", ""),
                status="success"
            )
        
        elif action_type == ActionType.RECOMMEND:
            # Handle product recommendations
            budget = data.get("budget", 30000)
            priorities = data.get("priorities", ["performance", "camera", "battery"])
            
            # Make internal API call to recommendation endpoint
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8000/api/agent/recommend",
                    json={"budget": budget, "priorities": priorities, "include_stores": True}
                )
                recommendation_data = response.json()
            
            best_choice = recommendation_data.get("best_choice")
            message = f"Based on your ₹{budget} budget and priorities ({', '.join(priorities)}), "
            if best_choice:
                message += f"I recommend the {best_choice['product']}."
            else:
                message += "I couldn't find suitable options."
            
            # Navigate to products page with budget filter
            navigation = NavigationTarget(
                page="products.html",
                params={
                    "budget": str(budget),
                    "aiMode": "true",
                    "action": "recommend"
                }
            )
            
            return AgentResponse(
                action=action_type,
                message=message,
                data=recommendation_data,
                navigation=navigation,
                status="success",
                suggestions=["Check nearby stores", "Compare these phones", "Add to cart"]
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
    """Get command suggestions for users - Demo flow optimized"""
    
    return {
        "suggestions": [
            # Main Demo Flow - Copy & Paste These in Order:
            "Show me phones under 50k",
            "Show me iPhone 13",
            "Add it to my cart",
            "Show me OnePlus 11", 
            "Add it to my cart",
            "Compare phones in my cart for battery and camera",
            "What do reviews say?",
            "Take me to my cart",
            
            # Alternative Commands
            "Show me Samsung phones",
            "Show my recent orders",
            "Find phones",
            "Show me all phones"
        ]
    }