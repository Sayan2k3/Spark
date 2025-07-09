"""
Product Recommendation API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from ..services.recommender import ProductRecommender
from ..services.actions import get_mock_products


class RecommendationRequest(BaseModel):
    budget: float
    priorities: List[str]  # e.g., ['camera', 'storage', 'gaming']
    include_stores: bool = True


class StorePrice(BaseModel):
    store: str
    store_id: int
    distance: str
    price: float
    availability: str
    savings: float


class ProductRecommendation(BaseModel):
    product: str
    product_id: int
    online_price: float
    score: Dict[str, float]
    overall_score: float
    value_score: float
    store_prices: Optional[List[Dict[str, Any]]] = None


class BestChoice(BaseModel):
    product: str
    product_id: int
    overall_score: float
    reasons: List[str]
    best_store_deal: Optional[Dict[str, Any]] = None
    savings: float


class RecommendationResponse(BaseModel):
    recommendations: List[ProductRecommendation]
    best_choice: Optional[BestChoice]
    priorities_analyzed: List[str]
    budget: float
    status: str = "success"


router = APIRouter()
recommender = ProductRecommender()


@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get product recommendations based on budget and priorities
    """
    try:
        # Validate priorities
        valid_priorities = ['camera', 'storage', 'gaming', 'battery', 'display', 'performance']
        invalid_priorities = [p for p in request.priorities if p not in valid_priorities]
        
        if invalid_priorities:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid priorities: {invalid_priorities}. Valid options: {valid_priorities}"
            )
        
        # Get all products
        all_products = get_mock_products()
        
        # Get recommendations
        result = recommender.get_budget_recommendations(
            products=all_products,
            budget=request.budget,
            priorities=request.priorities,
            include_stores=request.include_stores
        )
        
        return RecommendationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommend/priorities")
async def get_available_priorities():
    """
    Get list of available priority features for recommendations
    """
    return {
        "priorities": [
            {
                "key": "camera",
                "display": "Camera Quality",
                "description": "Prioritize phones with excellent cameras"
            },
            {
                "key": "storage",
                "display": "Storage Capacity",
                "description": "Prioritize phones with more storage"
            },
            {
                "key": "gaming",
                "display": "Gaming Performance",
                "description": "Prioritize phones optimized for gaming"
            },
            {
                "key": "battery",
                "display": "Battery Life",
                "description": "Prioritize phones with long battery life"
            },
            {
                "key": "display",
                "display": "Display Quality",
                "description": "Prioritize phones with great displays"
            },
            {
                "key": "performance",
                "display": "Overall Performance",
                "description": "Prioritize phones with fast processors"
            }
        ]
    }


@router.post("/recommend/quick")
async def quick_recommendation(budget: float):
    """
    Get a quick recommendation based on budget alone
    """
    try:
        # Use balanced priorities for quick recommendation
        default_priorities = ['performance', 'camera', 'battery']
        
        all_products = get_mock_products()
        
        result = recommender.get_budget_recommendations(
            products=all_products,
            budget=budget,
            priorities=default_priorities,
            include_stores=True
        )
        
        if result['best_choice']:
            return {
                "recommendation": result['best_choice']['product'],
                "price": next(r['online_price'] for r in result['recommendations'] 
                            if r['product'] == result['best_choice']['product']),
                "reason": f"Best overall phone under ${budget}",
                "quick_tip": "Ask me to compare specific features for a detailed analysis!"
            }
        else:
            return {
                "recommendation": None,
                "message": f"No phones found under ${budget}"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))