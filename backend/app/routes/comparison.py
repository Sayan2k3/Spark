"""
Product Comparison API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

from ..services.comparator import ProductComparator
from ..services.actions import get_mock_products


class ComparisonRequest(BaseModel):
    cart_items: List[str]  # List of product IDs
    criteria: List[str]    # List of criteria to compare (e.g., ['battery', 'camera'])


class ComparisonResponse(BaseModel):
    comparison: Dict[str, Any]
    summary: str
    recommendation: Dict[str, Any]
    winner_by_criteria: Dict[str, str]
    status: str = "success"


router = APIRouter()
comparator = ProductComparator()


@router.post("/compare", response_model=ComparisonResponse)
async def compare_products(request: ComparisonRequest):
    """
    Compare multiple products based on specified criteria
    """
    try:
        # Get product data for the requested items
        all_products = get_mock_products()
        
        # Filter to get only the products in cart
        cart_products = []
        for product_id in request.cart_items:
            product = next((p for p in all_products if str(p['id']) == product_id), None)
            if product:
                cart_products.append(product)
        
        if len(cart_products) < 2:
            raise HTTPException(
                status_code=400, 
                detail="At least 2 products are required for comparison"
            )
        
        # Perform comparison
        comparison_result = comparator.compare_products(cart_products, request.criteria)
        
        return ComparisonResponse(
            comparison=comparison_result['comparison'],
            summary=comparison_result['summary'],
            recommendation=comparison_result['recommendation'],
            winner_by_criteria=comparison_result['winner_by_criteria']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare/criteria")
async def get_available_criteria():
    """
    Get list of available comparison criteria
    """
    return {
        "criteria": [
            {"key": "battery", "display": "Battery Life", "description": "Battery capacity and user feedback"},
            {"key": "camera", "display": "Camera Quality", "description": "Camera specs and photo quality"},
            {"key": "performance", "display": "Performance", "description": "Speed and gaming capabilities"},
            {"key": "display", "display": "Display", "description": "Screen quality and features"},
            {"key": "storage", "display": "Storage", "description": "Internal storage capacity"},
            {"key": "build", "display": "Build Quality", "description": "Materials and durability"}
        ]
    }